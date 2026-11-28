# Banking Maths Set 8 - Final Report

Status: **complete**. All six chapters were generated, verified, deduplicated,
imported into the verified local `ssc_prep` database, and exercised through the
real test service on a scratch copy. No commit or push was made.

## Database target and safety

- Database used: `postgresql://***:***@127.0.0.1:5432/ssc_prep` (masked).
- The running backend and every importer/check process used this same local
  target through process-only environment overrides.
- Remote Neon was never contacted. `.env` was not modified. No credential is
  recorded in any report.
- The importer refused a scratch target and a remote-like target before the live
  run, confirming its local-only guard.
- All 12 target chapters were reconfirmed active, correctly named and at zero
  questions immediately before import.

## Scratch baseline

- The first background restore stalled and was stopped; no live write occurred.
- The corrected restore completed with exit code 0.
- Full-table count and content hashes matched across live, scratch and baseline:
  20,932 questions / 89,853 options / 0 Set 8 rows / 19 tables.
- `BASELINE_MATCH=True`; `LIVE_UNTOUCHED_BY_SCRATCH=True`.

## Generation and verification

- 720 original questions: six datasets x 120, 24 families x 5 variants each.
- Exact 20-field schema, deterministic IDs, 15/20/30/55 part split, four distinct
  options, one correct option, answer/index agreement, nonempty explanations,
  `ORIGINAL_VERIFIED` / `VERIFIED`, `exam_year = null`, structured
  `verification_data`.
- Independent recomputation from `verification_data` passed for all 720 questions.
- Mains chapters are `HARD`-only (480 questions total).
- Both DI chapters remain Prelims-level: 35 `EASY` + 85 `MEDIUM` each (240 total).
- Deduplication passed with 0 exact, normalized, number-masked, lexical or
  semantic collisions against Sets 1-7 (4,800 questions) and the live DB
  excluding this batch.

## Source PDFs

Seven PDFs / 102 pages were inspected by OCR. Final content-based mapping:

| PDF | Target |
| --- | --- |
| `87fda602-e97e-4aa7-90cc-9f316d0af672.pdf` | `time_and_work_mains` |
| `ce788d06-e730-4963-97ca-208b2af36699 (2).pdf` | `time_and_work_data_interpretation` |
| `0da2c67a-4985-4a86-9772-b0c4b826b42f.pdf` | `time_speed_and_distance_mains` |
| `Simple and Compound Interest Mains 01  Class Notes.pdf` | `simple_and_compound_interest_mains` |
| `f5b22d88-8d5a-494e-b7b2-9e5b1b05d260.pdf` | `simple_and_compound_interest_data_interpretation` |
| `Pipe and Cistern Mains 01 _Class Notes.pdf` | `pipe_and_cistern_mains` |
| `Time Speed and Distance Mains 02 Class Notes.pdf` | Unmapped extra reference (Time/Speed/Distance DI), not shipped from |

All shipped questions are original; printed MCQs and answer keys were not copied.

## Import and idempotency

- Live transactional import: **1,440 inserted, 0 updated**.
- Idempotency replay: **0 inserted, 1,440 updated**.
- Replay preserved all 1,440 deterministic IDs, chapter assignments and section
  assignments; ID lists before and after replay were identical.
- No existing question was deleted, replaced or deactivated. No generic import
  endpoint was used.

## Final database counts

| Exam | Chapter | Active questions | Parts |
| --- | --- | ---: | --- |
| Banking Clerk | Time and Work (Mains) | 120 | 15 / 20 / 30 / 55 |
| Banking Clerk | Time and Work - Data Interpretation | 120 | 15 / 20 / 30 / 55 |
| Banking Clerk | Time, Speed and Distance (Mains) | 120 | 15 / 20 / 30 / 55 |
| Banking Clerk | Simple and Compound Interest (Mains) | 120 | 15 / 20 / 30 / 55 |
| Banking Clerk | Simple and Compound Interest - Data Interpretation | 120 | 15 / 20 / 30 / 55 |
| Banking Clerk | Pipe and Cistern (Mains) | 120 | 15 / 20 / 30 / 55 |
| Banking PO | Time and Work (Mains) | 120 | 15 / 20 / 30 / 55 |
| Banking PO | Time and Work - Data Interpretation | 120 | 15 / 20 / 30 / 55 |
| Banking PO | Time, Speed and Distance (Mains) | 120 | 15 / 20 / 30 / 55 |
| Banking PO | Simple and Compound Interest (Mains) | 120 | 15 / 20 / 30 / 55 |
| Banking PO | Simple and Compound Interest - Data Interpretation | 120 | 15 / 20 / 30 / 55 |
| Banking PO | Pipe and Cistern (Mains) | 120 | 15 / 20 / 30 / 55 |

Totals: 6 chapters, 2 exams, 12 chapter/exam combinations, 1,440 live rows,
48 sections, 48/48 part selections, 48 total part selections across two exams.

## Functional verification

- Availability API: 48/48 sections passed with correct counts and durations.
- `create_test`: 48/48 sections passed; 48 scratch attempts created only on the
  scratch copy; correct 630/840/1260/2310 second durations.
- DI rendering: 16 sections / 480 questions / 1,920 options passed; every DI
  question carries inline data with four distinct options and one correct option.
- No real test was submitted on the live database; no live attempt or answer
  record was changed.

## Reconciliation and integrity

- Only `questions` (+1,440) and `question_options` (+5,760) changed.
- Questions by exam: Banking Clerk Math & Quant +720; Banking PO Math & Quant +720.
- All 12 target chapters changed by exactly +120; all prior sections unchanged.
- Banking Others maths questions unchanged.
- Unrelated-data integrity: every table outside the 1,440 Set 8 questions and
  5,760 options was content-hash identical to the pre-import baseline.

## Reports

- `reports/banking_maths_set8_pdf_mapping.md`
- `reports/banking_maths_set8_source_ledger.md`
- `reports/banking_maths_set8_source_ledger.csv`
- `reports/banking_maths_set8_progress.md`
- `reports/banking_maths_set8_dedup_report.md`
- `reports/banking_maths_set8_answer_verification.md`
- `reports/banking_maths_set8_validation_report.md`
- `reports/banking_maths_set8_db_before.json`
- `reports/banking_maths_set8_db_after.json`
- `reports/banking_maths_set8_db_reconciliation.md`
- `reports/banking_maths_set8_import_idempotency_report.md`
- `reports/banking_maths_set8_scratch_baseline.md`
- `reports/banking_maths_set8_availability_scratch_report.md`
- `reports/banking_maths_set8_create_test_report.md`
- `reports/banking_maths_set8_di_rendering_report.md`
- `reports/banking_maths_set8_data_integrity_report.md`
- `reports/banking_maths_set8_final_report.md`

## Datasets

- `data/banking_maths_time_and_work_mains_questions.json`
- `data/banking_maths_time_and_work_di_questions.json`
- `data/banking_maths_time_speed_and_distance_mains_questions.json`
- `data/banking_maths_simple_and_compound_interest_mains_questions.json`
- `data/banking_maths_simple_and_compound_interest_di_questions.json`
- `data/banking_maths_pipe_and_cistern_mains_questions.json`

## Git safeguards

- 46 staged Set 7 files preserved exactly.
- The pre-existing unstaged `frontend/src/pages/BankingPage.tsx` modification was
  preserved; six Set 7 mappings were left intact and six Set 8 mappings added.
- No file was staged, unstaged, committed or pushed by this Set 8 workflow.
- `git diff --check` produced no output.
- Pre-existing unrelated untracked files were left untouched.

## Unresolved issues

- None in the Set 8 workflow.
- Pre-existing unrelated issues (one OAuth pytest failure and the UTF-8 BOM in
  `backend/.env`) were not touched.
