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

$backendRoot = Split-Path -Parent $PSScriptRoot
$csvPath = Join-Path $backendRoot "data/imports/percentage/percentage_hard_additional.csv"
if (-not (Test-Path -LiteralPath $csvPath -PathType Leaf)) {
    throw "Import file not found: $csvPath"
}

$credential = $null
$plainPassword = $null
$loginBody = $null
$login = $null
$jwt = $null
try {
    $credential = Get-Credential -UserName $Email -Message "Sign in as the question-bank administrator"
    $plainPassword = $credential.GetNetworkCredential().Password
    $loginBody = @{ email = $credential.UserName; password = $plainPassword } | ConvertTo-Json
    $login = Invoke-RestMethod -Method Post -Uri "$ApiBaseUrl/auth/login" `
        -ContentType "application/json" -Body $loginBody
    $jwt = $login.access_token
    if (-not $jwt) { throw "Login did not return an access token." }

    $preview = Invoke-MultipartDryRun `
        -Uri "$ApiBaseUrl/questions/import?dry_run=true" `
        -Jwt $jwt -Path $csvPath
    $preview | ConvertTo-Json -Depth 8
    if ($preview.aborted -or $preview.errors.Count -ne 0 -or $preview.duplicates -ne 0 -or $preview.would_import -ne 3) {
        throw "Dry-run did not match the expected 3 clean, non-duplicate questions. Nothing was imported. Review the report above."
    }
}
finally {
    $plainPassword = $null
    $loginBody = $null
    $jwt = $null
    $login = $null
    $credential = $null
}
