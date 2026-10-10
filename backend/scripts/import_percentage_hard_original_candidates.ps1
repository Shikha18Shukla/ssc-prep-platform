param(
    [ValidateNotNullOrEmpty()]
    [string]$ApiBaseUrl = "http://127.0.0.1:8000/api"
)

$ErrorActionPreference = "Stop"
Import-Module (Join-Path $PSScriptRoot "percentage_question_verification.psm1") -Force
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
    return Invoke-AuthenticatedQuestionJsonGet `
        -Uri "$ApiBaseUrl/questions?chapter_id=$script:ChapterId&$Filter&limit=200" `
        -Headers $script:Headers
}

function Assert-CleanDryRun {
    param([Parameter(Mandatory = $true)]$Summary)
    if (-not $Summary.dry_run -or $Summary.aborted -or $Summary.total_records -ne 4 -or
        $Summary.would_import -ne 4 -or $Summary.duplicates -ne 0 -or
        $Summary.rejected -ne 0 -or $Summary.errors.Count -ne 0) {
        throw "Validation did not return exactly 4 clean, non-duplicate rows. No import request was sent. Review the report above."
    }
}

$backendRoot = Split-Path -Parent $PSScriptRoot
$csvPath = Join-Path $backendRoot "data/imports/percentage/percentage_hard_original_candidates.csv"
$ChapterId = "ba38c03a-3c13-4de1-bdb8-77c612df7b76"
if (-not (Test-Path -LiteralPath $csvPath -PathType Leaf)) {
    throw "Approved candidate CSV not found: $csvPath"
}
$candidateRows = @(Import-Csv -LiteralPath $csvPath -Encoding UTF8)
if ($candidateRows.Count -ne 4) {
    throw "Expected exactly four rows in the approved candidate CSV; found $($candidateRows.Count). No API request was sent."
}
foreach ($row in $candidateRows) {
    if ($row.subject_slug -ne "maths" -or $row.subcategory_slug -ne "arithmetic-maths" -or
        $row.chapter_slug -ne "percentage" -or $row.difficulty -ne "HARD" -or
        $row.is_pyq -ne "false" -or $row.pyq_year -or $row.pyq_exam_name) {
        throw "Candidate CSV identity or metadata changed. No API request was sent."
    }
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

    # Confirm the expected database baseline before offering the commit prompt.
    $beforeEasy = Get-QuestionList "difficulty=EASY&is_pyq=false"
    $beforeMedium = Get-QuestionList "difficulty=MEDIUM&is_pyq=false"
    $beforeHard = Get-QuestionList "difficulty=HARD"
    $beforeHardOrdinary = Get-QuestionList "difficulty=HARD&is_pyq=false"
    $beforeHardPyq = Get-QuestionList "difficulty=HARD&is_pyq=true"
    if ($beforeEasy.total -ne 12 -or $beforeMedium.total -ne 11 -or
        $beforeHard.total -ne 6 -or $beforeHardOrdinary.total -ne 3 -or $beforeHardPyq.total -ne 3) {
        throw "Database baseline changed (Easy=$($beforeEasy.total), Medium=$($beforeMedium.total), Hard total=$($beforeHard.total), ordinary Hard=$($beforeHardOrdinary.total), Hard PYQ=$($beforeHardPyq.total)). No import request was sent."
    }

    $preflight = Invoke-MultipartQuestionImport `
        -Uri "$ApiBaseUrl/questions/import?dry_run=true" -Jwt $jwt -Path $csvPath
    $preflight | ConvertTo-Json -Depth 8
    Assert-CleanDryRun $preflight

    $confirmation = Read-Host "Type exactly IMPORT 4 ORIGINAL HARD PERCENTAGE QUESTIONS to continue"
    if ($confirmation -cne "IMPORT 4 ORIGINAL HARD PERCENTAGE QUESTIONS") {
        Write-Host "Canceled. No import request was sent."
        return
    }

    # Revalidate after confirmation immediately before the only commit request.
    $finalCheck = Invoke-MultipartQuestionImport `
        -Uri "$ApiBaseUrl/questions/import?dry_run=true" -Jwt $jwt -Path $csvPath
    $finalCheck | ConvertTo-Json -Depth 8
    Assert-CleanDryRun $finalCheck

    # The only write request in this script uploads only the fixed four-row CSV.
    $importResult = Invoke-MultipartQuestionImport `
        -Uri "$ApiBaseUrl/questions/import?dry_run=false" -Jwt $jwt -Path $csvPath
    $importResult | ConvertTo-Json -Depth 8

    # Verify database state even when the endpoint reports an unexpected summary.
    $afterEasy = Get-QuestionList "difficulty=EASY&is_pyq=false"
    $afterMedium = Get-QuestionList "difficulty=MEDIUM&is_pyq=false"
    $afterHard = Get-QuestionList "difficulty=HARD"
    $afterHardOrdinary = Get-QuestionList "difficulty=HARD&is_pyq=false"
    $afterHardPyq = Get-QuestionList "difficulty=HARD&is_pyq=true"
    $chapterQuestions = Get-QuestionList "include_inactive=true"
    $ordinaryAvailability = Invoke-RestMethod -Method Get `
        -Uri "$ApiBaseUrl/exams/chapters/$ChapterId/availability?level=HARD&question_count=10" -Headers $Headers
    $pyqAvailability = Invoke-RestMethod -Method Get `
        -Uri "$ApiBaseUrl/exams/chapters/$ChapterId/availability?level=PYQ" -Headers $Headers

    $candidateVerifications = @(Get-QuestionCandidateVerification `
        -Candidates $candidateRows -Questions $chapterQuestions.items -ExpectedChapterId $ChapterId)
    $verifiedCandidates = @($candidateVerifications | Where-Object { $_.status -eq "VERIFIED_ACTIVE" }).Count
    $missingCandidates = @($candidateVerifications | Where-Object { $_.status -ne "VERIFIED_ACTIVE" })

    $baselineCsvPath = Join-Path $backendRoot "data/imports/percentage/percentage_hard.csv"
    $baselineRows = @(Import-Csv -LiteralPath $baselineCsvPath -Encoding UTF8)
    $knownHardText = @{}
    foreach ($row in $baselineRows) { $knownHardText[(Get-QuestionVerificationKey $row.question_text)] = $true }
    foreach ($row in $candidateRows) { $knownHardText[(Get-QuestionVerificationKey $row.question_text)] = $true }
    $unclassifiedHardRows = @($afterHardOrdinary.items | Where-Object {
        -not $knownHardText.ContainsKey((Get-QuestionVerificationKey $_.question_text))
    } | ForEach-Object {
        [PSCustomObject]@{
            id = $_.id
            question_text = $_.question_text
            is_active = $_.is_active
            difficulty = $_.difficulty
            is_pyq = $_.is_pyq
            chapter_id = $_.chapter_id
            source = $_.source
        }
    })

    $verification = [PSCustomObject]@{
        active_easy = $afterEasy.total
        active_medium = $afterMedium.total
        active_hard_total = $afterHard.total
        active_hard_ordinary = $afterHardOrdinary.total
        active_hard_pyq = $afterHardPyq.total
        new_candidates_verified_active = $verifiedCandidates
        candidate_verifications = $candidateVerifications
        candidates_not_verified = $missingCandidates
        active_hard_rows_not_matching_baseline_or_candidate_text = $unclassifiedHardRows
        hard_availability = $ordinaryAvailability.available_question_count
        hard_10_question_test_available = $ordinaryAvailability.can_satisfy_request
        pyq_availability = $pyqAvailability.available_question_count
    }
    $verification | ConvertTo-Json

    if ($importResult.dry_run -or $importResult.aborted -or $importResult.imported -ne 4 -or
        $importResult.duplicates -ne 0 -or $importResult.rejected -ne 0 -or
        $importResult.errors.Count -ne 0 -or $afterEasy.total -ne 12 -or
        $afterMedium.total -ne 11 -or $afterHard.total -ne 10 -or
        $afterHardOrdinary.total -ne 7 -or $afterHardPyq.total -ne 3 -or
        $ordinaryAvailability.available_question_count -ne 7 -or
        $ordinaryAvailability.can_satisfy_request -ne $false -or $pyqAvailability.available_question_count -ne 3) {
        throw "Post-import verification did not match expectations. Stop; inspect the displayed import result and database counts before retrying."
    }
}
finally {
    $plainPassword = $null
    $loginBody = $null
    $jwt = $null
    $Headers = $null
    $login = $null
    $credential = $null
}
