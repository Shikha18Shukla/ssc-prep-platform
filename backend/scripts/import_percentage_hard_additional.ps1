param(
    [Parameter(Mandatory = $false)]
    [string]$Email,
    [ValidateNotNullOrEmpty()]
    [string]$ApiBaseUrl = "http://127.0.0.1:8000/api"
)

$ErrorActionPreference = "Stop"
$ApiBaseUrl = $ApiBaseUrl.TrimEnd("/")
if (-not [Uri]::IsWellFormedUriString($ApiBaseUrl, [UriKind]::Absolute)) {
    throw "ApiBaseUrl must be an absolute URL."
}

function Invoke-MultipartQuestionImport {
    param(
        [Parameter(Mandatory = $true)] [string]$Uri,
        [Parameter(Mandatory = $true)] [string]$Jwt,
        [Parameter(Mandatory = $true)] [string]$Path
    )

    Add-Type -AssemblyName System.Net.Http -ErrorAction Stop
    $client = $null
    $multipart = $null
    $fileStream = $null
    $response = $null
    try {
        $client = New-Object System.Net.Http.HttpClient
        $multipart = New-Object System.Net.Http.MultipartFormDataContent
        $fileStream = [System.IO.File]::OpenRead($Path)
        $fileContent = [System.Net.Http.StreamContent]::new($fileStream)
        $fileContent.Headers.ContentType = [System.Net.Http.Headers.MediaTypeHeaderValue]::Parse("text/csv")
        $multipart.Add($fileContent, "file", [System.IO.Path]::GetFileName($Path))
        [void]$client.DefaultRequestHeaders.TryAddWithoutValidation("Authorization", "Bearer $Jwt")

        $response = $client.PostAsync($Uri, $multipart).GetAwaiter().GetResult()
        $responseBody = $response.Content.ReadAsStringAsync().GetAwaiter().GetResult()
        if (-not $response.IsSuccessStatusCode) {
            throw "Import API returned HTTP $([int]$response.StatusCode): $responseBody"
        }
        return ConvertFrom-Json -InputObject $responseBody
    }
    finally {
        if ($response) { $response.Dispose() }
        if ($multipart) { $multipart.Dispose() }
        if ($fileStream) { $fileStream.Dispose() }
        if ($client) { $client.Dispose() }
    }
}

function Get-QuestionList {
    param([string]$Filter)
    return Invoke-RestMethod -Method Get -Uri "$ApiBaseUrl/questions?chapter_id=$script:ChapterId&$Filter&limit=200" -Headers $script:Headers
}

$backendRoot = Split-Path -Parent $PSScriptRoot
$csvPath = Join-Path $backendRoot "data/imports/percentage/percentage_hard_additional.csv"
$ChapterId = "ba38c03a-3c13-4de1-bdb8-77c612df7b76"
if (-not (Test-Path -LiteralPath $csvPath -PathType Leaf)) {
    throw "Import file not found: $csvPath"
}

$credential = $null
$plainPassword = $null
$loginBody = $null
$login = $null
$jwt = $null
$Headers = $null
try {
    if ([string]::IsNullOrWhiteSpace($Email)) {
        $credential = Get-Credential -Message "Sign in as the question-bank administrator"
    } else {
        $credential = Get-Credential -UserName $Email -Message "Sign in as the question-bank administrator"
    }
    $plainPassword = $credential.GetNetworkCredential().Password
    $loginBody = @{ email = $credential.UserName; password = $plainPassword } | ConvertTo-Json
    $login = Invoke-RestMethod -Method Post -Uri "$ApiBaseUrl/auth/login" `
        -ContentType "application/json" -Body $loginBody
    $jwt = $login.access_token
    if (-not $jwt) { throw "Login did not return an access token." }
    $Headers = @{ Authorization = "Bearer $jwt" }

    # Recheck the approved batch immediately before the commit request.
    $preview = Invoke-MultipartQuestionImport `
        -Uri "$ApiBaseUrl/questions/import?dry_run=true" -Jwt $jwt -Path $csvPath
    $preview | ConvertTo-Json -Depth 8
    if ($preview.aborted -or $preview.total_records -ne 3 -or $preview.would_import -ne 3 -or $preview.duplicates -ne 0 -or $preview.errors.Count -ne 0) {
        throw "Pre-import validation changed or failed. No import request was sent. Review the dry-run report above."
    }

    # This is the sole commit request. It uploads only percentage_hard_additional.csv.
    $result = Invoke-MultipartQuestionImport `
        -Uri "$ApiBaseUrl/questions/import?dry_run=false" -Jwt $jwt -Path $csvPath
    $result | ConvertTo-Json -Depth 8
    if ($result.aborted -or $result.imported -ne 3 -or $result.duplicates -ne 0 -or $result.errors.Count -ne 0) {
        throw "Import result was unexpected. Stop and inspect the database before any retry."
    }

    $easy = Get-QuestionList "difficulty=EASY&is_pyq=false"
    $medium = Get-QuestionList "difficulty=MEDIUM&is_pyq=false"
    $hard = Get-QuestionList "difficulty=HARD"
    $hardPyq = Get-QuestionList "difficulty=HARD&is_pyq=true"
    $expectedRows = Import-Csv -LiteralPath $csvPath
    if ($easy.total -ne 12 -or $medium.total -ne 11 -or $hard.total -ne 6 -or $hardPyq.total -ne 3) {
        throw "Post-import count mismatch (Easy=$($easy.total), Medium=$($medium.total), Hard=$($hard.total), Hard PYQ=$($hardPyq.total)). Stop and inspect the database."
    }
    foreach ($expected in $expectedRows) {
        $matching = @($hardPyq.items | Where-Object { $_.source -eq $expected.source })
        if ($matching.Count -ne 1) {
            throw "Expected one active PYQ row for source '$($expected.source)', found $($matching.Count). Stop and inspect the database."
        }
        $question = $matching[0]
        if (-not $question.is_active -or -not $question.is_pyq -or $question.pyq_year -ne [int]$expected.pyq_year -or $null -ne $question.pyq_exam_name) {
            throw "PYQ verification mismatch for source '$($expected.source)'. Stop and inspect the database."
        }
    }

    $hardTen = Invoke-RestMethod -Method Get `
        -Uri "$ApiBaseUrl/exams/chapters/$ChapterId/availability?level=HARD&question_count=10" -Headers $Headers
    $pyqAvailability = Invoke-RestMethod -Method Get `
        -Uri "$ApiBaseUrl/exams/chapters/$ChapterId/availability?level=PYQ" -Headers $Headers
    if ($hardTen.can_satisfy_request -ne $false) {
        throw "Expected a 10-question Hard test to remain unavailable."
    }
    [PSCustomObject]@{
        active_easy = $easy.total
        active_medium = $medium.total
        active_hard_all_pyq_flags = $hard.total
        active_hard_pyq = $hardPyq.total
        hard_level_availability = $hardTen.available_question_count
        hard_10_question_test_available = $hardTen.can_satisfy_request
        pyq_level_availability = $pyqAvailability.available_question_count
    } | ConvertTo-Json
}
finally {
    $plainPassword = $null
    $loginBody = $null
    $jwt = $null
    $Headers = $null
    $login = $null
    $credential = $null
}
