$ErrorActionPreference = "Stop"
$modulePath = Join-Path (Split-Path -Parent $PSScriptRoot) "scripts/percentage_question_verification.psm1"
Import-Module $modulePath -Force

$chapterId = "ba38c03a-3c13-4de1-bdb8-77c612df7b76"
$candidates = @(
    [PSCustomObject]@{ question_text = "An article is marked 50% above its cost price."; difficulty = "HARD"; is_pyq = "false" },
    [PSCustomObject]@{ question_text = "A trader sells an article at a 12% loss. If it had been sold for ₹216 more, the sale would instead have produced a 6% gain. What was the cost price?"; difficulty = "HARD"; is_pyq = "false" }
)
$databaseQuestions = @(
    [PSCustomObject]@{ id = "id-normalized"; question_text = "  AN ARTICLE is marked 50% above its cost price.  "; is_active = $true; difficulty = "HARD"; is_pyq = $false; chapter_id = $chapterId; pyq_year = $null; pyq_exam_name = $null },
    [PSCustomObject]@{ id = "unrelated"; question_text = "A different question"; is_active = $true; difficulty = "HARD"; is_pyq = $false; chapter_id = $chapterId; pyq_year = $null; pyq_exam_name = $null }
)

$results = @(Get-QuestionCandidateVerification -Candidates $candidates -Questions $databaseQuestions -ExpectedChapterId $chapterId)
if ($results.Count -ne 2) { throw "Expected two per-candidate results, got $($results.Count)." }
if ($results[0].status -ne "VERIFIED_ACTIVE" -or $results[0].question_id -ne "id-normalized") {
    throw "Case and whitespace normalization regression: expected normalized record to verify."
}
if ($results[1].status -ne "MISSING" -or $results[1].csv_row -ne 3) {
    throw "Missing-question regression: candidate 2 must be reported as missing at CSV row 3."
}
$verifiedCount = @($results | Where-Object { $_.status -eq "VERIFIED_ACTIVE" }).Count
if ($verifiedCount -ne 1) { throw "Expected one verified record while preserving the separate missing result." }

$candidate2Json = ConvertTo-Json -InputObject ([PSCustomObject]@{ question_text = $candidates[1].question_text }) -Compress
$candidate2Bytes = [Text.Encoding]::UTF8.GetBytes($candidate2Json)
$decoded = ConvertFrom-QuestionJsonUtf8 $candidate2Bytes
if ($decoded.question_text -cne $candidates[1].question_text) {
    throw "UTF-8 JSON regression: rupee character in candidate 2 was not preserved."
}
$candidate2Record = [PSCustomObject]@{
    id = "id-candidate-2"
    question_text = $decoded.question_text
    is_active = $true
    difficulty = "HARD"
    is_pyq = $false
    chapter_id = $chapterId
    pyq_year = $null
    pyq_exam_name = $null
}
$candidate2Result = @(Get-QuestionCandidateVerification -Candidates @($candidates[1]) -Questions @($candidate2Record) -ExpectedChapterId $chapterId)
if ($candidate2Result.Count -ne 1 -or $candidate2Result[0].status -ne "VERIFIED_ACTIVE" -or $candidate2Result[0].question_id -ne "id-candidate-2") {
    throw "Candidate 2 UTF-8 verification regression: expected the existing Unicode question to verify as active."
}

Write-Output "PASS: normalized candidate verified; absent candidate reported MISSING; UTF-8 candidate 2 verified active; no batch failure."
