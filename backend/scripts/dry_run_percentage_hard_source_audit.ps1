param(
    [ValidateNotNullOrEmpty()]
    [string]$ApiBaseUrl = "http://127.0.0.1:8000/api"
)

$ErrorActionPreference = "Stop"
$ApiBaseUrl = $ApiBaseUrl.TrimEnd("/")
if (-not [Uri]::IsWellFormedUriString($ApiBaseUrl, [UriKind]::Absolute)) {
    throw "ApiBaseUrl must be an absolute URL."
}

function Invoke-MultipartDryRun {
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
    return Invoke-RestMethod -Method Get `
        -Uri "$ApiBaseUrl/questions?chapter_id=$script:ChapterId&$Filter&limit=200" `
        -Headers $script:Headers
}

$backendRoot = Split-Path -Parent $PSScriptRoot
$csvPath = Join-Path $backendRoot "data/imports/percentage/percentage_hard_source_audit.csv"
$ChapterId = "ba38c03a-3c13-4de1-bdb8-77c612df7b76"
if (-not (Test-Path -LiteralPath $csvPath -PathType Leaf)) {
    throw "Audit CSV not found: $csvPath"
}

$credential = $null
$plainPassword = $null
$loginBody = $null
$login = $null
$jwt = $null
$Headers = $null
try {
    $credential = Get-Credential -Message "Sign in as the question-bank administrator"
    $plainPassword = $credential.GetNetworkCredential().Password
    $loginBody = @{ email = $credential.UserName; password = $plainPassword } | ConvertTo-Json
    $login = Invoke-RestMethod -Method Post -Uri "$ApiBaseUrl/auth/login" `
        -ContentType "application/json" -Body $loginBody
    $jwt = $login.access_token
    if (-not $jwt) { throw "Login did not return an access token." }
    $Headers = @{ Authorization = "Bearer $jwt" }

    # This helper intentionally has no dry_run=false call.
    $preview = Invoke-MultipartDryRun `
        -Uri "$ApiBaseUrl/questions/import?dry_run=true" -Jwt $jwt -Path $csvPath
    $preview | ConvertTo-Json -Depth 8
    if ($preview.aborted -or $preview.total_records -ne 6 -or $preview.would_import -ne 0 -or $preview.duplicates -ne 6 -or $preview.errors.Count -ne 0) {
        throw "Source audit dry-run differed from the expected six existing duplicates. No database write was requested. Review the report above."
    }

    $easy = Get-QuestionList "difficulty=EASY&is_pyq=false"
    $medium = Get-QuestionList "difficulty=MEDIUM&is_pyq=false"
    $hard = Get-QuestionList "difficulty=HARD"
    $hardOrdinary = Get-QuestionList "difficulty=HARD&is_pyq=false"
    $hardPyq = Get-QuestionList "difficulty=HARD&is_pyq=true"
    if ($easy.total -ne 12 -or $medium.total -ne 11 -or $hard.total -ne 6 -or $hardOrdinary.total -ne 3 -or $hardPyq.total -ne 3) {
        throw "Active count mismatch: Easy=$($easy.total), Medium=$($medium.total), Hard total=$($hard.total), ordinary Hard=$($hardOrdinary.total), Hard PYQ=$($hardPyq.total)."
    }

    $hardAvailability = Invoke-RestMethod -Method Get `
        -Uri "$ApiBaseUrl/exams/chapters/$ChapterId/availability?level=HARD&question_count=10" -Headers $Headers
    $pyqAvailability = Invoke-RestMethod -Method Get `
        -Uri "$ApiBaseUrl/exams/chapters/$ChapterId/availability?level=PYQ" -Headers $Headers
    if ($hardAvailability.available_question_count -ne 3 -or $hardAvailability.can_satisfy_request -ne $false -or $pyqAvailability.available_question_count -ne 3) {
        throw "Availability mismatch: ordinary Hard=$($hardAvailability.available_question_count), 10-question Hard=$($hardAvailability.can_satisfy_request), PYQ=$($pyqAvailability.available_question_count)."
    }

    [PSCustomObject]@{
        active_easy = $easy.total
        active_medium = $medium.total
        active_hard_total = $hard.total
        active_hard_ordinary = $hardOrdinary.total
        active_hard_pyq = $hardPyq.total
        hard_availability = $hardAvailability.available_question_count
        hard_10_question_test_available = $hardAvailability.can_satisfy_request
        pyq_availability = $pyqAvailability.available_question_count
        import_mode = "dry_run_only"
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
