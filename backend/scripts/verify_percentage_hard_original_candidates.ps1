param(
    [ValidateNotNullOrEmpty()]
    [string]$ApiBaseUrl = "http://127.0.0.1:8000/api"
)

$ErrorActionPreference = "Stop"
Import-Module (Join-Path $PSScriptRoot "percentage_question_verification.psm1") -Force
$ApiBaseUrl = $ApiBaseUrl.TrimEnd("/")
$ChapterId = "ba38c03a-3c13-4de1-bdb8-77c612df7b76"
$backendRoot = Split-Path -Parent $PSScriptRoot
$csvPath = Join-Path $backendRoot "data/imports/percentage/percentage_hard_original_candidates.csv"
$baselineCsvPath = Join-Path $backendRoot "data/imports/percentage/percentage_hard.csv"

function Get-QuestionList {
    param([string]$Filter)
    return Invoke-AuthenticatedQuestionJsonGet `
        -Uri "$ApiBaseUrl/questions?chapter_id=$script:ChapterId&$Filter&limit=200" `
        -Headers $script:Headers
}

function Get-AllManagedQuestions {
    $all = @()
    $offset = 0
    $total = 0
    do {
        $page = Invoke-AuthenticatedQuestionJsonGet `
            -Uri "$ApiBaseUrl/questions?include_inactive=true&limit=200&offset=$offset" `
            -Headers $script:Headers
        $total = [int]$page.total
        $all += @($page.items)
        $offset += [int]$page.limit
    } while ($offset -lt $total)
    return $all
}

if (-not (Test-Path -LiteralPath $csvPath -PathType Leaf) -or
    -not (Test-Path -LiteralPath $baselineCsvPath -PathType Leaf)) {
    throw "Candidate or baseline CSV is missing. No request was sent."
}
$candidateRows = @(Import-Csv -LiteralPath $csvPath -Encoding UTF8)
$baselineRows = @(Import-Csv -LiteralPath $baselineCsvPath -Encoding UTF8)

$credential = $null
$plainPassword = $null
$loginBody = $null
$login = $null
$jwt = $null
$Headers = $null
try {
    $credential = Get-Credential -Message "Read-only Percentage question verification (administrator login)"
    $plainPassword = $credential.GetNetworkCredential().Password
    $loginBody = @{ email = $credential.UserName; password = $plainPassword } | ConvertTo-Json
    $login = Invoke-RestMethod -Method Post -Uri "$ApiBaseUrl/auth/login" `
        -ContentType "application/json" -Body $loginBody
    $jwt = $login.access_token
    if (-not $jwt) { throw "Login did not return an access token." }
    $Headers = @{ Authorization = "Bearer $jwt" }

    # Management reads include inactive rows so the report can distinguish missing from inactive.
    $allQuestions = @(Get-AllManagedQuestions)
    $candidateResults = @(Get-QuestionCandidateVerification `
        -Candidates $candidateRows -Questions $allQuestions -ExpectedChapterId $ChapterId)

    $hard = Get-QuestionList "difficulty=HARD"
    $ordinaryHard = Get-QuestionList "difficulty=HARD&is_pyq=false"
    $hardPyq = Get-QuestionList "difficulty=HARD&is_pyq=true"
    $availabilityHard = Invoke-RestMethod -Method Get `
        -Uri "$ApiBaseUrl/exams/chapters/$ChapterId/availability?level=HARD&question_count=10" -Headers $Headers
    $availabilityPyq = Invoke-RestMethod -Method Get `
        -Uri "$ApiBaseUrl/exams/chapters/$ChapterId/availability?level=PYQ" -Headers $Headers

    $baselineKeys = @{}
    foreach ($row in $baselineRows) { $baselineKeys[(Get-QuestionVerificationKey $row.question_text)] = $true }
    $candidateKeys = @{}
    foreach ($row in $candidateRows) { $candidateKeys[(Get-QuestionVerificationKey $row.question_text)] = $true }
    $unclassifiedHardRows = @($ordinaryHard.items | Where-Object {
        $key = Get-QuestionVerificationKey $_.question_text
        -not $baselineKeys.ContainsKey($key) -and -not $candidateKeys.ContainsKey($key)
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

    [PSCustomObject]@{
        counts = [PSCustomObject]@{
            active_hard_total = $hard.total
            active_hard_ordinary = $ordinaryHard.total
            active_hard_pyq = $hardPyq.total
        }
        availability = [PSCustomObject]@{
            hard_question_count = $availabilityHard.available_question_count
            hard_10_question_test_available = $availabilityHard.can_satisfy_request
            pyq_question_count = $availabilityPyq.available_question_count
        }
        candidate_verifications = $candidateResults
        active_hard_rows_not_matching_baseline_or_candidate_text = $unclassifiedHardRows
        read_only = $true
    } | ConvertTo-Json -Depth 8
}
finally {
    $plainPassword = $null
    $loginBody = $null
    $jwt = $null
    $Headers = $null
    $login = $null
    $credential = $null
}
