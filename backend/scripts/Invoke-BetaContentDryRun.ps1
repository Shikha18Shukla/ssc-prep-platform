param(
    [string]$PythonExe = '.\.venv-disease-import\Scripts\python.exe'
)

$resolvedPython = Resolve-Path -LiteralPath $PythonExe -ErrorAction Stop
$securePassword = Read-Host 'Local PostgreSQL password for postgres (masked)' -AsSecureString
if ($null -eq $securePassword -or $securePassword.Length -eq 0) {
    throw 'No password entered; no database connection was attempted.'
}
$passwordPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword)
$previousPassword = [Environment]::GetEnvironmentVariable('PGPASSWORD', 'Process')
try {
    $env:PGPASSWORD = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($passwordPointer)
    & $resolvedPython.Path -m app.scripts.plan_beta_content_import
    $pythonExitCode = $LASTEXITCODE
}
finally {
    if ($null -eq $previousPassword) {
        Remove-Item Env:PGPASSWORD -ErrorAction SilentlyContinue
    }
    else {
        [Environment]::SetEnvironmentVariable('PGPASSWORD', $previousPassword, 'Process')
    }
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($passwordPointer)
    $securePassword.Dispose()
}

if ($null -ne $pythonExitCode -and $pythonExitCode -ne 0) {
    # Preserve the Python stage/type/message already printed; do not replace it
    # with a generic PowerShell exception.
    exit $pythonExitCode
}
