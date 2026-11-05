param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('verify', 'inspect', 'upgrade', 'bootstrap', 'import-content')]
    [string]$Action,

    [string]$PythonExe = '.\.venv-disease-import\Scripts\python.exe'
)

$resolvedPython = Resolve-Path -LiteralPath $PythonExe -ErrorAction Stop
$secureUrl = Read-Host 'Paste the pooled URL for Neon project ssc-prep-beta (input is masked)' -AsSecureString
$urlPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureUrl)
$environmentNames = @('DATABASE_URL')
if ($Action -eq 'import-content') {
    $environmentNames += 'PGPASSWORD'
}
if ($Action -eq 'bootstrap') {
    $environmentNames += @('ENVIRONMENT', 'DEBUG', 'SECRET_KEY', 'BETA_INVITATIONS_REQUIRED', 'BETA_CATALOG_SCOPE', 'CORS_ORIGINS')
}
$originalEnvironment = @{}
foreach ($name in $environmentNames) {
    $originalEnvironment[$name] = [Environment]::GetEnvironmentVariable($name, 'Process')
}
$sourcePassword = $null
$sourcePasswordPointer = [IntPtr]::Zero

try {
    $env:DATABASE_URL = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($urlPointer)
    if ($Action -eq 'bootstrap') {
        $env:ENVIRONMENT = 'production'
        $env:DEBUG = 'false'
        $env:BETA_INVITATIONS_REQUIRED = 'true'
        $env:BETA_CATALOG_SCOPE = 'true'
        $env:CORS_ORIGINS = '["https://ssc-prep-beta.onrender.com"]'
        $secretBytes = New-Object byte[] 48
        $randomGenerator = [System.Security.Cryptography.RandomNumberGenerator]::Create()
        try {
            $randomGenerator.GetBytes($secretBytes)
            $env:SECRET_KEY = [Convert]::ToBase64String($secretBytes)
        }
        finally {
            $randomGenerator.Dispose()
            [Array]::Clear($secretBytes, 0, $secretBytes.Length)
        }
        & $resolvedPython.Path -m app.scripts.bootstrap_admin
    }
    elseif ($Action -eq 'import-content') {
        $sourcePassword = Read-Host 'Local PostgreSQL password for postgres (masked)' -AsSecureString
        if ($null -eq $sourcePassword -or $sourcePassword.Length -eq 0) {
            throw 'No local source password entered; no import was attempted.'
        }
        $sourcePasswordPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($sourcePassword)
        $env:PGPASSWORD = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($sourcePasswordPointer)
        & $resolvedPython.Path -m app.scripts.import_beta_content
    }
    else {
        & $resolvedPython.Path -m app.scripts.neon_beta_db $Action
    }
    if ($LASTEXITCODE -ne 0) {
        throw "Neon beta $Action failed. See the safe PostgreSQL diagnostic printed above; DATABASE_URL was removed from this process afterward."
    }
}
finally {
    foreach ($name in $environmentNames) {
        $originalValue = $originalEnvironment[$name]
        if ($null -eq $originalValue) {
            Remove-Item "Env:\$name" -ErrorAction SilentlyContinue
        }
        else {
            [Environment]::SetEnvironmentVariable($name, $originalValue, 'Process')
        }
    }
    if ($sourcePasswordPointer -ne [IntPtr]::Zero) {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($sourcePasswordPointer)
    }
    if ($null -ne $sourcePassword) {
        $sourcePassword.Dispose()
    }
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($urlPointer)
    $secureUrl.Dispose()
}
