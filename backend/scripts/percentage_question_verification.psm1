function Get-QuestionVerificationKey {
    param([AllowNull()][string]$Text)

    if ($null -eq $Text) { return "" }
    $normalized = $Text.Normalize([Text.NormalizationForm]::FormKC).ToLowerInvariant().Trim()
    return [regex]::Replace($normalized, "\s+", " ")
}

function ConvertFrom-QuestionJsonUtf8 {
    param([Parameter(Mandatory = $true)][byte[]]$ContentBytes)

    $jsonText = [Text.Encoding]::UTF8.GetString($ContentBytes)
    return ConvertFrom-Json -InputObject $jsonText
}

function Invoke-AuthenticatedQuestionJsonGet {
    param(
        [Parameter(Mandatory = $true)][string]$Uri,
        [Parameter(Mandatory = $true)][System.Collections.IDictionary]$Headers
    )

    Add-Type -AssemblyName System.Net.Http -ErrorAction Stop
    $client = $null
    $response = $null
    try {
        $client = New-Object System.Net.Http.HttpClient
        [void]$client.DefaultRequestHeaders.TryAddWithoutValidation("Authorization", $Headers.Authorization)
        $response = $client.GetAsync($Uri).GetAwaiter().GetResult()
        $contentBytes = $response.Content.ReadAsByteArrayAsync().GetAwaiter().GetResult()
        if (-not $response.IsSuccessStatusCode) {
            $body = [Text.Encoding]::UTF8.GetString($contentBytes)
            throw "Question API returned HTTP $([int]$response.StatusCode): $body"
        }
        return ConvertFrom-QuestionJsonUtf8 $contentBytes
    }
    finally {
        if ($response) { $response.Dispose() }
        if ($client) { $client.Dispose() }
    }
}

function Get-QuestionCandidateVerification {
    param(
        [Parameter(Mandatory = $true)][object[]]$Candidates,
        [Parameter(Mandatory = $true)][object[]]$Questions,
        [Parameter(Mandatory = $true)][string]$ExpectedChapterId
    )

    $results = @()
    for ($index = 0; $index -lt $Candidates.Count; $index++) {
        $candidate = $Candidates[$index]
        $key = Get-QuestionVerificationKey ([string]$candidate.question_text)
        $found = @($Questions | Where-Object {
            (Get-QuestionVerificationKey ([string]$_.question_text)) -ceq $key
        })

        if ($found.Count -eq 0) {
            $results += [PSCustomObject]@{
                csv_row = $index + 2
                question_text = $candidate.question_text
                status = "MISSING"
                question_id = $null
                stored_question_text = $null
                is_active = $null
                difficulty = $null
                is_pyq = $null
                chapter_id = $null
                pyq_year = $null
                pyq_exam_name = $null
            }
            continue
        }

        if ($found.Count -gt 1) {
            $results += [PSCustomObject]@{
                csv_row = $index + 2
                question_text = $candidate.question_text
                status = "AMBIGUOUS_MATCH"
                question_id = (($found | ForEach-Object { [string]$_.id }) -join ",")
                stored_question_text = (($found | ForEach-Object { [string]$_.question_text }) -join " | ")
                is_active = $null
                difficulty = $null
                is_pyq = $null
                chapter_id = $null
                pyq_year = $null
                pyq_exam_name = $null
            }
            continue
        }

        $question = $found[0]
        $status = "VERIFIED_ACTIVE"
        if ([string]$question.chapter_id -ne $ExpectedChapterId) { $status = "WRONG_CHAPTER" }
        elseif ([string]$question.difficulty -ne "HARD") { $status = "WRONG_DIFFICULTY" }
        elseif ([bool]$question.is_pyq) { $status = "WRONG_PYQ_STATUS" }
        elseif ($null -ne $question.pyq_year -or $null -ne $question.pyq_exam_name) { $status = "UNEXPECTED_PYQ_METADATA" }
        elseif (-not [bool]$question.is_active) { $status = "INACTIVE" }

        $results += [PSCustomObject]@{
            csv_row = $index + 2
            question_text = $candidate.question_text
            status = $status
            question_id = [string]$question.id
            stored_question_text = [string]$question.question_text
            is_active = [bool]$question.is_active
            difficulty = [string]$question.difficulty
            is_pyq = [bool]$question.is_pyq
            chapter_id = [string]$question.chapter_id
            pyq_year = $question.pyq_year
            pyq_exam_name = $question.pyq_exam_name
        }
    }
    return $results
}

Export-ModuleMember -Function Get-QuestionVerificationKey, ConvertFrom-QuestionJsonUtf8, Invoke-AuthenticatedQuestionJsonGet, Get-QuestionCandidateVerification
