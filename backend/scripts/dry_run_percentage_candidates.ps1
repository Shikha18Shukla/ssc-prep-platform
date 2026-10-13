param(
    [Parameter(Mandatory = $true)]
    [ValidateScript({ Test-Path -LiteralPath $_ -PathType Leaf })]
    [string]$CsvPath,
    [ValidateNotNullOrEmpty()]
    [string]$ApiBaseUrl = "http://127.0.0.1:8000/api"
)

$ErrorActionPreference = "Stop"
$ApiBaseUrl = $ApiBaseUrl.TrimEnd("/")
if (-not [Uri]::IsWellFormedUriString($ApiBaseUrl, [UriKind]::Absolute)) {
    throw "ApiBaseUrl must be an absolute URL."
}
$CsvPath = (Resolve-Path -LiteralPath $CsvPath).Path

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

$credential = $null
$plainPassword = $null
$loginBody = $null
$login = $null
$jwt = $null
try {
    $candidateRows = @(Import-Csv -LiteralPath $CsvPath)
    if ($candidateRows.Count -ne 4) {
        throw "Expected exactly four candidate rows; found $($candidateRows.Count). No API request was sent."
    }
    foreach ($row in $candidateRows) {
        if ($row.difficulty -ne "HARD" -or $row.is_pyq -ne "false" -or $row.pyq_year -or $row.pyq_exam_name) {
            throw "Every candidate must be HARD, non-PYQ, and have no PYQ metadata. No API request was sent."
        }
    }

    $credential = Get-Credential -Message "Sign in as the question-bank administrator for dry-run validation only"
    $plainPassword = $credential.GetNetworkCredential().Password
    $loginBody = @{ email = $credential.UserName; password = $plainPassword } | ConvertTo-Json
    $login = Invoke-RestMethod -Method Post -Uri "$ApiBaseUrl/auth/login" `
        -ContentType "application/json" -Body $loginBody
    $jwt = $login.access_token
    if (-not $jwt) { throw "Login did not return an access token." }

    # Dry-run only: this script has no dry_run=false request.
    $preview = Invoke-MultipartDryRun `
        -Uri "$ApiBaseUrl/questions/import?dry_run=true" -Jwt $jwt -Path $CsvPath
    $preview | ConvertTo-Json -Depth 8
    if ($preview.aborted -or $preview.total_records -ne 4 -or $preview.would_import -ne 4 -or $preview.duplicates -ne 0 -or $preview.rejected -ne 0 -or $preview.errors.Count -ne 0) {
        Write-Warning "Dry-run did not match the expected clean four-row batch. No database write was requested. Review the report above."
        exit 2
    }
}
finally {
    $plainPassword = $null
    $loginBody = $null
    $jwt = $null
    $login = $null
    $credential = $null
}
