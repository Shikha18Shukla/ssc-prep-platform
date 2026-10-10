param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
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
        [Parameter(Mandatory = $true)] [System.Collections.IDictionary]$Headers,
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
        [void]$client.DefaultRequestHeaders.TryAddWithoutValidation("Authorization", $Headers.Authorization)

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

$batches = @(
    @{ Path = "data/imports/percentage/percentage_easy.csv"; Expected = 12; Difficulty = "EASY" },
    @{ Path = "data/imports/percentage/percentage_medium.csv"; Expected = 11; Difficulty = "MEDIUM" },
    @{ Path = "data/imports/percentage/percentage_hard.csv"; Expected = 3; Difficulty = "HARD" }
)
$backendRoot = Split-Path -Parent $PSScriptRoot
$percentageChapterId = "ba38c03a-3c13-4de1-bdb8-77c612df7b76"

$credential = Get-Credential -UserName $Email -Message "Sign in as the question-bank administrator"
$plainPassword = $null
$loginBody = $null
$login = $null
$headers = $null

try {
    $plainPassword = $credential.GetNetworkCredential().Password
    $loginBody = @{ email = $credential.UserName; password = $plainPassword } | ConvertTo-Json
    $login = Invoke-RestMethod -Method Post -Uri "$ApiBaseUrl/auth/login" `
        -ContentType "application/json" -Body $loginBody
    $headers = @{ Authorization = "Bearer $($login.access_token)" }

    foreach ($batch in $batches) {
        $path = Join-Path $backendRoot $batch.Path
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
            throw "Import file not found: $path"
        }
        $preview = Invoke-MultipartQuestionImport `
            -Uri "$ApiBaseUrl/questions/import?dry_run=true" `
            -Headers $headers -Path $path
        if ($preview.aborted -or $preview.errors.Count -ne 0 -or $preview.duplicates -ne 0 -or $preview.would_import -ne $batch.Expected) {
            throw "Dry-run stopped for $($batch.Difficulty): expected $($batch.Expected) clean rows, got $($preview.would_import) candidates, $($preview.duplicates) duplicates, $($preview.errors.Count) errors. No files have been committed yet."
        }
        Write-Host "DRY-RUN $($batch.Difficulty): $($preview.would_import) ready; 0 duplicates; 0 errors."
    }

    foreach ($batch in $batches) {
        $path = Join-Path $backendRoot $batch.Path
        $result = Invoke-MultipartQuestionImport `
            -Uri "$ApiBaseUrl/questions/import?dry_run=false" `
            -Headers $headers -Path $path
        if ($result.aborted -or $result.errors.Count -ne 0 -or $result.duplicates -ne 0 -or $result.imported -ne $batch.Expected) {
            throw "Import stopped for $($batch.Difficulty): expected $($batch.Expected), imported $($result.imported), duplicates $($result.duplicates), errors $($result.errors.Count). Earlier files may already be committed; verify the database before retrying."
        }
        Write-Host "IMPORTED $($batch.Difficulty): $($result.imported)."
    }

    foreach ($batch in $batches) {
        $managed = Invoke-RestMethod -Method Get `
            -Uri "$ApiBaseUrl/questions?chapter_id=$percentageChapterId&difficulty=$($batch.Difficulty)&is_pyq=false&limit=1" `
            -Headers $headers
        $availability = Invoke-RestMethod -Method Get `
            -Uri "$ApiBaseUrl/exams/chapters/$percentageChapterId/availability?level=$($batch.Difficulty)&question_count=10" `
            -Headers $headers
        if ($managed.total -ne $batch.Expected -or $availability.available_question_count -ne $batch.Expected) {
            throw "Post-import verification failed for $($batch.Difficulty): expected $($batch.Expected) active rows; management count $($managed.total), availability count $($availability.available_question_count)."
        }
        $expectedCanSatisfy = $batch.Expected -ge 10
        if ($availability.can_satisfy_request -ne $expectedCanSatisfy) {
            throw "Availability verification failed for $($batch.Difficulty) at a 10-question minimum."
        }
        Write-Host "VERIFIED $($batch.Difficulty): $($managed.total) active database questions; 10-question request satisfied = $($availability.can_satisfy_request)."
    }
}
finally {
    $plainPassword = $null
    $loginBody = $null
    $headers = $null
    $login = $null
    $credential = $null
}
