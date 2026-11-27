# Banking Maths Set 6 - Final Report

## Status: complete

Banking Maths Set 6 is complete for **Banking Clerk** and **Banking PO** only.
The six catalog chapters were already present; no catalog migration or schema
change was needed. `Banking Others` was never written.

| Chapter | Frontend slug | Questions | Difficulty |
| --- | --- | ---: | --- |
| Percentage Arithmetic (Mains) | `percentage-arithmetic-mains` | 120 | HARD |
| Percentage - Data Interpretation (Mains) | `percentage-data-interpretation-mains` | 120 | HARD |
| Ratio Arithmetic (Mains) | `ratio-arithmetic-mains` | 120 | HARD |
| Ratio - Data Interpretation (Mains) | `ratio-data-interpretation-mains` | 120 | HARD |
| Profit and Loss (Mains) | `profit-and-loss-mains` | 120 | HARD |
| Profit and Loss - Data Interpretation | `profit-and-loss-data-interpretation` | 120 | EASY 35 / MEDIUM 85 |

Totals: **720 dataset questions**, **1,440 imported live rows** (720 Clerk +
720 PO), **5,760 option rows**, **48 sections** (24 per exam), **144 question
families** exercised five times each.

Every item has four distinct options, one correct option, a matching answer
text/index, a non-empty explanation, a valid difficulty,
`source_type = ORIGINAL_VERIFIED`, `verification_status = VERIFIED`,
`exam_year = null`, and a `verification_method` naming the independent
verification script. Each provenance note explicitly states that the item is
not an extracted PDF MCQ and is not a previous-year question. No item is
labelled as PYQ.

## Source inspection and ledger

Six supplied PDF decks were inspected page by page:

- 89 pages total;
- 0 text-layer pages;
- 89 image-only pages read with OCR at 150 dpi;
- 89 page-level ledger rows plus 720 shipped-question rows = 809 ledger rows.

Chapter assignment was derived from extracted slide content, not from file
names. Printed keys and worked-example answers were treated as untrusted
reference material. The PDFs supplied topic scope only; all shipped questions
are originals written for this bank. The five Mains chapters are `HARD`
throughout, while Profit and Loss - Data Interpretation is deliberately
Prelims-level.

`backend/verify_banking_maths_set6_questions.py` recomputed every answer from
`verification_data` without trusting the stored answer: **720 checked, 0
failures**. It also confirmed the 20-field schema, 24 families with five
variants per chapter, part sizes 15 / 20 / 30 / 55, four unique options, one
correct option, answer/index agreement, explanation consistency, valid
difficulty, and no PYQ flag.

## Deduplication

- Exact duplicate texts inside the new batch: 0
- Normalized duplicate texts inside the new batch: 0
- Number-masked templates shared by more than one family: 0
- Cross-chapter repeated number-masked templates: 0

The 147 repeated number-masked templates are the expected five fresh numeric
variants inside each of the 144 families; none is shared across families.

The available prior Banking Maths datasets in Sets 1-5 total **3,360
questions** (28 datasets x 120); all were screened. Against that pool and the
18,052-question pre-import database pool:

| Screen | Exact | Normalized | Number-masked | Lexical | Semantic flags |
| --- | ---: | ---: | ---: | ---: | ---: |
| Sets 1-5 | 0 | 0 | 0 | 0 | 0 |
| Existing database | 0 | 0 | 0 | 0 | 0 |
| Cross-chapter within Set 6 | - | - | 0 | 0 | - |

## Backup, baseline and dry run

An initial archival attempt produced an empty file and was discarded rather
than accepted. The replacement pre-import archive was verified as a usable
custom-format archive (gzip compression, 122 table-of-contents entries) and was
later restored successfully for content comparison.

Before import:

- All 16 live tables, 224 existing Banking Maths sections and every
  questions-by-exam/subject bucket matched the captured baseline exactly;
- Live totals were 18,052 questions and 78,333 options;
- All six target chapters had 0 questions;
- The transaction-safe importer dry run passed: 12 target chapters, 1,440
  planned questions, no writes.

The full backend test suite had already been started as a single process and
was allowed to finish; no duplicate test run was launched:

- **465 passed, 2 skipped, 0 failed, 0 errors, 23 warnings in 1338.06s
  (0:22:18)**.
- Warnings are pre-existing dependency/collection notices from AnyIO,
  Starlette/FastAPI test client and pytest model-name collection.

The frontend production build (`tsc -b && vite build`) passed.

## Import and idempotency

The live import was a single transaction with post-import checks and automatic
rollback on failure.

- First live run: **1,440 inserted, 0 updated**.
- Replay: **0 inserted, 1,440 updated**; all 16 table counts remained
  unchanged, confirming idempotency.
- Live questions: 18,052 -> 19,492 (**+1,440**).
- Live options: 78,333 -> 84,093 (**+5,760**).
- Clerk maths: 3,360 -> 4,080; PO maths: 3,360 -> 4,080.
- New sections: 224 -> 272 (**+48**), each with 15 / 20 / 30 / 55 questions.

Only `questions` and `question_options` changed. Banking Others maths remained
0 -> 0.

## Functional validation

All database work used a process-local override to the local development
instance. No environment file, hosted database or unrelated configuration was
modified.

- `backend/validate_banking_maths_set6_bank.py`: **ALL CHECKS PASSED** -
  720 datasets, 1,440 deterministic IDs, 48/48 sections through the real
  `get_test_availability`, options, explanations, no PYQ flags, deduplication
  and the 42-second duration rule.
- A restored disposable copy of the imported bank was used for all destructive
  functional checks; the live database was never used to create test attempts.
- On that copy, `backend/check_banking_maths_set6_availability.py`:
  **48/48 sections passed** through the real availability service.
- On that copy, `backend/check_banking_maths_set6_create_test.py`:
  **48/48 sections passed** with real `create_test` calls. Exact section
  isolation was confirmed, 48 attempts were created, and durations were
  630 / 840 / 1260 / 2310 seconds.
- On that copy, `backend/check_banking_maths_set6_di_rendering.py`:
  **24/24 DI sections passed**, covering all four parts of all three DI
  chapters for both exams. A total of **720/720 questions and 2,880/2,880
  options** rendered; every question carried its own inline data, no external
  image/table/graph/passage was needed, and every question had one correct
  option.

The disposable copy was dropped and its absence was confirmed. The temporary
credential helper used only for that copy was removed.

## Unrelated-data integrity

A second restored copy was made from the verified pre-import archive. The live
database and that baseline were compared after excluding the deterministic
Set 6 question IDs and their options. Every remaining row in all 16 tables was
compared by content hash.

Result: **ALL UNRELATED DATA UNCHANGED**.

This includes attempts (61), user answers (272), users (3), chapter rotations
(4), question history (92), test questions (2,667), Banking Others, the catalog
tables and every other unrelated table. The live database contains exactly
1,440 Set 6 questions and 5,760 Set 6 options.

## Frontend and repository safety

Six slug-to-key mappings were added to `mathsChapterKeys` in
`frontend/src/pages/BankingPage.tsx`. Existing entries were preserved.

- Frontend build: **passed**.
- Full backend pytest: **passed** as recorded above.
- At verification time, nothing had been staged, committed, pushed, reset, stashed, cleaned or discarded.
- The tracked modifications to `backend/app/services/test_service.py`
  and `frontend/src/pages/BankingPage.tsx` were preserved by this batch.

## Deliverables

Core Set 6 files:

- `backend/maths_set6/`
- `backend/generate_banking_maths_set6_questions.py`
- `backend/verify_banking_maths_set6_questions.py`
- `backend/build_banking_maths_set6_source_ledger.py`
- `backend/dedup_banking_maths_set6.py`
- `backend/report_banking_maths_set6_db.py`
- `backend/report_banking_maths_set6_reconciliation.py`
- `backend/import_banking_maths_set6_questions.py`
- `backend/validate_banking_maths_set6_bank.py`
- `backend/check_banking_maths_set6_availability.py`
- `backend/check_banking_maths_set6_create_test.py`
- `backend/check_banking_maths_set6_di_rendering.py`
- `backend/check_banking_maths_set6_data_integrity.py`

Evidence reports:

- `reports/banking_maths_set6_source_ledger.md`
- `reports/banking_maths_set6_source_ledger.csv`
- `reports/banking_maths_set6_dedup_report.md`
- `reports/banking_maths_set6_validation_report.md`
- `reports/banking_maths_set6_db_reconciliation.md`
- `reports/banking_maths_set6_availability_scratch_report.md`
- `reports/banking_maths_set6_create_test_report.md`
- `reports/banking_maths_set6_di_rendering_report.md`
- `reports/banking_maths_set6_data_integrity_report.md`
- `reports/banking_maths_set6_final_report.md`
