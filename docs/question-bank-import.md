# Question bank imports and management

These templates are format examples only. They contain placeholders and are intentionally not importable. Replace them with approved question content; do not treat the example values as real SSC questions or answers.

- [`question_bank_template.csv`](../backend/templates/question_bank_template.csv)
- [`question_bank_template.json`](../backend/templates/question_bank_template.json)

## Import format

The authenticated endpoint accepts one CSV or JSON file at `POST /api/questions/import` as multipart form data. Dry-run defaults to `true`. CSV header names are case-sensitive and must include:

`subject_slug,subcategory_slug,chapter_slug,question_text,option_a,option_b,option_c,option_d,correct_option,explanation,difficulty,is_pyq,pyq_year,pyq_exam_name,source`

For JSON, send an array of question objects or `{ "questions": [...] }`. The four options can use the same `option_a` through `option_d` fields, or an `options` object keyed exactly `A`, `B`, `C`, and `D`. Each record identifies the active SSC catalog by subject, optional category, and chapter slugs. A direct chapter (English/Reasoning) uses an empty category in CSV or `null` in JSON.

`correct_option` is one of `A`, `B`, `C`, or `D`; `difficulty` is `EASY`, `MEDIUM`, or `HARD`. `is_pyq` accepts true/false (CSV also accepts `1`/`0`, `yes`/`no`). PYQs require a valid year; `pyq_exam_name` is optional when the source does not identify the specific exam. An absent or blank exam name is stored as `NULL`. When supplied, the name must be text of at most 100 characters. Non-PYQs must leave both PYQ metadata fields blank/null. Source and explanation are optional. The importer validates all four non-empty options, active catalog relationships, and PYQ metadata. It detects duplicate question text within a chapter after Unicode normalization, case folding, and whitespace normalization; existing inactive questions are included in this check.

## Administrator access

Question-bank import and management endpoints require an active user with the database-backed `is_admin` flag. Ordinary signed-in users receive HTTP 403. Public registration never accepts or changes this flag. The flag defaults to false for existing and new users.

After deploying the migration, an operator grants access only to an existing, active account. Run these commands from the `backend` directory:

```powershell
python -m alembic upgrade head
python -m app.scripts.set_admin --email admin@example.com --grant
```

Replace `admin@example.com` with the exact account email you control. To revoke access, use `--revoke`. Granting requires an existing active account; the command will not create accounts or promote an inactive user. Keep database access restricted to trusted operators. Restart the backend after migration; the admin flag is read from the database on every request, so revocation takes effect immediately.

## Preview and commit

Run commands from the repository root. Obtain a JWT by logging in with the promoted admin account. Do not paste or commit the token. For PowerShell, hold it in a variable:

```powershell
$login = Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/auth/login" `
  -ContentType "application/json" `
  -Body ((Get-Credential -UserName "admin@example.com" -Message "Sign in as the question-bank administrator") |
    ForEach-Object { @{ email = $_.UserName; password = $_.GetNetworkCredential().Password } | ConvertTo-Json })
$headers = @{ Authorization = "Bearer $($login.access_token)" }
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/questions/import?dry_run=true" `
  -Headers $headers -Form @{ file = Get-Item "backend/templates/question_bank_template.csv" }
```

Review `total_records`, `would_import`, `rejected`, `duplicates`, `errors`, and `duplicate_rows`. Error rows are 1-based CSV physical rows (header is row 1); JSON rows are 1-based record positions. If any record is invalid, the whole batch is aborted and no questions/options are written. Duplicate rows are reported and left unchanged; other valid, non-duplicate records may be imported. A dry run writes nothing.

After replacing the placeholder data and reviewing a clean preview, run the same file with `dry_run=false`:

```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/questions/import?dry_run=false" `
  -Headers $headers -Form @{ file = Get-Item "path\to\approved-questions.csv" }
```

The commit call revalidates the file and duplicates against the current database. It never updates an existing question. New questions and all four options are written in one database transaction; a database failure rolls the batch back. Files are limited to 5 MiB and 5,000 records.

For the reviewed Percentage batch, run the following from the repository root after setting `$headers` through the admin login example above. It dry-runs all three files first, then commits each individually only if all previews match the reviewed totals with no errors or duplicates. Each file is its own transaction. The checks stop on the first unexpected result.

```powershell
pwsh -File backend/scripts/import_percentage_batch.ps1 -Email "admin@example.com"
```

The script prompts for the admin password without echoing it, keeps the JWT in process memory, validates all three files before any commit, and stops on any unexpected duplicate, invalid row, count, or API error. It imports Easy, Medium, and Hard in separate transactions, then verifies active counts through the management API and 10-question availability through the same chapter-selection endpoint the frontend uses. Run it from the repository root using PowerShell 7 (`pwsh`).

This batch yields 12 Easy, 11 Medium, and 3 Hard questions. The three Hard questions are stored and active, but Hard remains unavailable for a 10-question set until seven additional verified Hard questions are imported.

For a one-file dry-run that must not import anything, use the PowerShell 5-compatible script below from the repository root. It prompts securely for the administrator password, keeps the JWT in memory, and submits only the named additional Hard CSV with `dry_run=true`:

```powershell
.\backend\scripts\dry_run_percentage_hard_additional.ps1 -Email "admin@example.com"
```

## Management API

All management endpoints require the admin JWT described above. The list endpoint supports `chapter_id`, `difficulty`, `is_pyq`, `include_inactive`, `offset`, and `limit` filters. `GET /api/questions/{id}` returns management details including correct-option flags. `PUT /api/questions/{id}` replaces question text, explanation, difficulty, PYQ metadata, source, and all four options after validation. `PATCH /api/questions/{id}/status` activates/deactivates a question. The separate exam catalog endpoints remain available to signed-in students and do not return Question or QuestionOption records.
