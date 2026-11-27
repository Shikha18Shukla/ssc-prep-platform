# Banking Maths Batch 2 — Final Report

Date: 2026-11-27
Project: SSC Prep Platform
Scope: five new Banking Maths chapters for **Banking Clerk** and **Banking PO** only.

## 1. Dataset counts and part structure

| Chapter | Dataset file | Questions | Part 1 | Part 2 | Part 3 | Part 4 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Quadratic Equations | `data/banking_maths_quadratic_equations_questions.json` | 120 | 15 | 20 | 30 | 55 |
| Number System | `data/banking_maths_number_system_questions.json` | 120 | 15 | 20 | 30 | 55 |
| Percentage | `data/banking_maths_percentage_questions.json` | 120 | 15 | 20 | 30 | 55 |
| Ratio and Proportion | `data/banking_maths_ratio_proportion_questions.json` | 120 | 15 | 20 | 30 | 55 |
| Profit, Loss and Discount | `data/banking_maths_profit_loss_discount_questions.json` | 120 | 15 | 20 | 30 | 55 |
| **Total** | | **600** | **75** | **100** | **150** | **275** |

Each of the 600 items has four distinct options, one correct option, a non-empty explanation, a valid `EASY`/`MEDIUM`/`HARD` difficulty and the same schema as batch 1. All 600 are tagged `ORIGINAL_VERIFIED` / `VERIFIED`, with `exam_year = null`; none is a PYQ or a verbatim PDF MCQ. `source_page` is a topic reference only.

The 600 dataset questions were imported twice into the bank (once per exam), producing **1,200** database rows.

## 2. Source-ledger coverage — all 28 PDFs / 425 pages

All 28 supplied PDFs were inspected page by page. Thirteen image-only decks (247 pages) were rendered at 150 dpi and read with RapidOCR; the remaining 15 PDFs (178 pages) had a usable text layer. Question and solution blocks were matched by printed number where possible; printed keys were recorded but never trusted.

| File | Chapter | Topic | Pages | Read as | Items | OCR pages | With options | With key |
| --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: |
| Number System 01 _ Class Notes.pdf | Number System | Number System - set/notes 1 | 27 | OCR (image-only PDF) | 0 | 27 | 0 | 0 |
| Number System 02  Class Notes.pdf | Number System | Number System - set/notes 2 | 16 | OCR (image-only PDF) | 0 | 16 | 0 | 0 |
| Number System 03_Class Notes.pdf | Number System | Number System - class notes | 12 | OCR (image-only PDF) | 0 | 12 | 0 | 0 |
| PROFIT&LOSS SET-1 (Eng).pdf | Profit, Loss and Discount | Profit, Loss and Discount - set/notes 1 | 5 | text layer | 9 | 0 | 9 | 9 |
| PROFIT&LOSS SET-2 (Eng).pdf | Profit, Loss and Discount | Profit, Loss and Discount - set/notes 2 | 5 | text layer | 10 | 0 | 10 | 10 |
| PROFIT&LOSS SET-3 (Eng).pdf | Profit, Loss and Discount | Profit, Loss and Discount - set/notes 3 | 6 | text layer | 10 | 0 | 10 | 10 |
| PROFIT&LOSS SET-4 (Eng).pdf | Profit, Loss and Discount | Profit, Loss and Discount - set/notes 4 | 6 | text layer | 10 | 0 | 10 | 10 |
| PROFIT&LOSS SET-6 (Eng).pdf | Profit, Loss and Discount | Profit, Loss and Discount - set/notes 6 | 7 | text layer | 10 | 0 | 10 | 10 |
| Percentage 01_Class Notes.pdf | Percentage | Percentage - class notes | 19 | OCR (image-only PDF) | 0 | 19 | 0 | 0 |
| Percentage 02 _ Class Notes.pdf | Percentage | Percentage - set/notes 2 | 17 | OCR (image-only PDF) | 0 | 17 | 0 | 0 |
| Percentage 03_Class Notes.pdf | Percentage | Percentage - class notes | 25 | OCR (image-only PDF) | 0 | 25 | 0 | 0 |
| Percentage 04_Class Notes.pdf | Percentage | Percentage - class notes | 19 | OCR (image-only PDF) | 0 | 19 | 0 | 0 |
| Percentage 05_Class Notes.pdf | Percentage | Percentage - class notes | 19 | OCR (image-only PDF) | 0 | 19 | 0 | 0 |
| Percentage 06_Class Notes.pdf | Percentage | Percentage - class notes | 19 | OCR (image-only PDF) | 0 | 19 | 0 | 0 |
| Percentage 07_Class Notes.pdf | Percentage | Percentage - class notes | 19 | OCR (image-only PDF) | 0 | 19 | 0 | 0 |
| Percentage 08_Class Notes.pdf | Percentage | Percentage - class notes | 21 | OCR (image-only PDF) | 0 | 21 | 0 | 0 |
| Profit, Loss and Discount 05 _Class Notes.pdf | Profit, Loss and Discount | Profit, Loss and Discount - set/notes 5 | 17 | OCR (image-only PDF) | 0 | 17 | 0 | 0 |
| Profit, Loss and Discount 06_Class Notes.pdf | Profit, Loss and Discount | Profit, Loss and Discount - class notes | 17 | OCR (image-only PDF) | 0 | 17 | 0 | 0 |
| QUADRATIC EQUATION SET-1 (Eng).pdf | Quadratic Equations | Quadratic Equations - set/notes 1 | 20 | text layer | 50 | 0 | 50 | 50 |
| QUADRATIC EQUATION SET-2 (Eng).pdf | Quadratic Equations | Quadratic Equations - set/notes 2 | 20 | text layer | 50 | 0 | 50 | 50 |
| QUADRATIC EQUATION SET-3 (Eng).pdf | Quadratic Equations | Quadratic Equations - set/notes 3 | 20 | text layer | 50 | 0 | 50 | 50 |
| QUADRATIC EQUATION SET-4 (Eng).pdf | Quadratic Equations | Quadratic Equations - set/notes 4 | 20 | text layer | 50 | 0 | 50 | 50 |
| QUADRATIC EQUATION SET-5 (Eng).pdf | Quadratic Equations | Quadratic Equations - set/notes 5 | 20 | text layer | 50 | 0 | 50 | 49 |
| QUADRATIC EQUATION SET-6 (Eng).pdf | Quadratic Equations | Quadratic Equations - set/notes 6 | 20 | text layer | 50 | 0 | 50 | 50 |
| Ratio_and_Proportion_Set-1_(Mains).pdf | Ratio and Proportion | Ratio and Proportion - class notes | 7 | text layer | 10 | 0 | 10 | 10 |
| Ratio_and_Proportion_Set-2_(Mains).pdf | Ratio and Proportion | Ratio and Proportion - class notes | 8 | text layer | 10 | 0 | 10 | 10 |
| Ratio_and_Proportion_Set-3_(Mains).pdf | Ratio and Proportion | Ratio and Proportion - class notes | 7 | text layer | 10 | 0 | 10 | 10 |
| Ratio_and_Proportion_Set-4_(Mains).pdf | Ratio and Proportion | Ratio and Proportion - class notes | 7 | text layer | 10 | 0 | 10 | 10 |
| **Total** | | | **425** | | **389** | **247** | **389** | **388** |

Ledger output: `reports/banking_maths_set2_source_ledger.csv` has **1,236 rows** — 636 PDF/OCR reference rows plus 600 shipped-question provenance rows. The Markdown summary is `reports/banking_maths_set2_source_ledger.md`.

Reconciliation per chapter:

| Chapter | Dataset questions | Parts | PDF rows inspected | PDF rows imported | Original rows |
| --- | ---: | --- | ---: | ---: | ---: |
| Quadratic Equations | 120 | 15 / 20 / 30 / 55 | 300 | 0 | 120 |
| Number System | 120 | 15 / 20 / 30 / 55 | 55 | 0 | 120 |
| Percentage | 120 | 15 / 20 / 30 / 55 | 158 | 0 | 120 |
| Ratio and Proportion | 120 | 15 / 20 / 30 / 55 | 40 | 0 | 120 |
| Profit, Loss and Discount | 120 | 15 / 20 / 30 / 55 | 83 | 0 | 120 |

No printed MCQ was copied into a dataset. The five-option Guidely sets and unreliable OCR notation made verbatim extraction unsuitable; the PDFs defined topic scope and difficulty only.

## 3. Answer verification and deduplication

- `backend/verify_banking_maths_set2_questions.py` independently recomputed every answer from `verification_data`: **600 questions checked, 0 failures**.
- Checks included four unique options, one correct option, correct `correct_option`/`correct_answer` agreement, non-empty explanation, valid difficulty, 120 unique IDs per chapter and exact part counts.
- `backend/dedup_banking_maths_set2.py` and `reports/banking_maths_set2_dedup_report.md`:
  - exact duplicates inside new batch: **0**
  - normalized duplicates inside new batch: **0**
  - exact/normalized collisions with batch 1: **0**
  - number-masked collisions with batch 1: **0**
  - database rows scanned: **12,532** (pre-import baseline)
  - exact/normalized database matches: **0**
  - number-masked database matches: **0**
  - lexical near-duplicates against batch 1, database and across chapters: **0**
- One true database duplicate found during generation (`If x + 1/x = 2, find x^2 + 1/x^2.`) was excluded before shipping; masked-template repeats are deliberate and use fresh values.
- Combined validator `backend/validate_banking_maths_set2_bank.py`: **all checks passed** — 600 dataset questions, 1,200 planned deterministic IDs, 40 availability checks, schema/provenance checks and zero duplicate hits.

## 4. Database import and reconciliation

Database access used a process-only `DATABASE_URL` override to an isolated local database; `.env` was not modified.

A custom-format backup was taken and verified before import; `pg_restore --list` confirmed 122 TOC entries. Backup files are not committed.

Importer behaviour (`backend/import_banking_maths_set2_questions.py`):

- preflight: **10 target chapters, 1,200 planned questions**
- `--dry-run` before import: no database writes
- real import: **1,200 inserted, 0 updated**, transactional
- second `--dry-run`: no database writes
- idempotency re-run: **0 inserted, 1,200 updated**, no row-count growth
- Clerk and PO only; Banking Others explicitly checked and untouched
- deterministic `uuid5` IDs from `https://ssc-prep.local/banking-maths/<exam_slug>/<dataset_id>`
- each of the 10 exam/chapter combinations ended with `{1: 15, 2: 20, 3: 30, 4: 55}`

Database reconciliation (`reports/banking_maths_set2_db_reconciliation.md`):

| Table | Before | After | Delta |
| --- | ---: | ---: | ---: |
| `questions` | 12,532 | 13,732 | +1,200 |
| `question_options` | 56,253 | 61,053 | +4,800 |
| all other tables | unchanged | unchanged | 0 |

Only `questions` and `question_options` changed. Clerk `math-quant` went 600 → 1,200 and PO `math-quant` went 600 → 1,200. Batch-1 section questions stayed at 600; Banking Others maths questions stayed at 0. Attempts, answers, users, chapters, subjects, exams and all other rows were unchanged.

Snapshots: `reports/banking_maths_set2_db_before.json`, `reports/banking_maths_set2_db_after.json`.

## 5. Scratch `create_test` end-to-end verification

A fresh restored local copy was created with `pg_dump`/`pg_restore`. The verification script refused to run against the live database, and the temporary copy was dropped afterwards and confirmed absent.

`backend/check_banking_maths_set2_create_test.py` called the real `create_test` for all **40** sections:

| Check | Result |
| --- | ---: |
| Sections exercised | 40 / 40 |
| Attempts created on scratch DB | 40 |
| Banking Clerk chapters covered | 5 / 5 |
| Banking PO chapters covered | 5 / 5 |
| Part sizes per chapter | 15 / 20 / 30 / 55 |
| Section-based selection | every attempt selected 15/15, 20/20, 30/30 or 55/55 questions from its own section |
| 15-question duration | 630 s = 10.5 min |
| 20-question duration | 840 s = 14 min |
| 30-question duration | 1260 s = 21 min |
| 55-question duration | 2310 s = 38.5 min |

Duration rule confirmed: **42 seconds per question**. Full per-section evidence is in `reports/banking_maths_set2_create_test_report.md`. After the scratch exercise, live `ssc_prep` still had 13,732 questions, 61,053 options, 61 attempts and 2,667 test questions.

## 6. Test and build results

- Backend: `cd backend; .\.venv\Scripts\python.exe -m pytest tests -q`
  **465 passed, 2 skipped, 1 warning in 947.51s (0:15:47)**.
  The only warning is a pre-existing `StarletteDeprecationWarning` about `httpx`/`starlette.testclient`, unrelated to this change. No relevant failures.
- Frontend: `cd frontend; npm run build`
  `tsc -b && vite build` passed; 55 modules transformed; 4 assets emitted; built in 17.48s.
  Output: `index.html` 0.90 kB, CSS 23.09 kB, JS 242.99 kB (gzip 72.32 kB).

## 7. Frontend integration

`frontend/src/pages/BankingPage.tsx` gained exactly five entries in `mathsChapterKeys`:

```ts
"quadratic-equations": "quadratic_equations",
"number-system": "number_system",
percentage: "percentage",
"ratio-and-proportion": "ratio_proportion",
"profit-loss-and-discount": "profit_loss_discount",
```

No other frontend logic was changed.

## 8. Exact changed and untracked files

Tracked diff:

- `M backend/app/services/test_service.py` — **unrelated pre-existing work, inspected only and not modified by this batch**
- `M frontend/src/pages/BankingPage.tsx` — the five mappings above

`git diff --check` produced no errors at verification time. No commit, push, reset, stash or clean had been performed when this report was written.

Batch-2 files created in this work:

- Scripts: `backend/build_banking_maths_set2_ledger.py`, `backend/check_banking_maths_set2_create_test.py`, `backend/dedup_banking_maths_set2.py`, `backend/generate_banking_maths_set2_questions.py`, `backend/import_banking_maths_set2_questions.py`, `backend/report_banking_maths_set2_db.py`, `backend/report_banking_maths_set2_reconciliation.py`, `backend/validate_banking_maths_set2_bank.py`, `backend/verify_banking_maths_set2_questions.py`, `backend/maths_set2/`
- Datasets: the five `data/banking_maths_*_questions.json` files listed in section 1
- Reports: `reports/banking_maths_set2_create_test_report.md`, `reports/banking_maths_set2_db_after.json`, `reports/banking_maths_set2_db_before.json`, `reports/banking_maths_set2_db_reconciliation.md`, `reports/banking_maths_set2_dedup_report.md`, `reports/banking_maths_set2_source_ledger.csv`, `reports/banking_maths_set2_source_ledger.md`, `reports/banking_maths_set2_validation_report.md`, `reports/banking_maths_set2_final_report.md`

Ignored helper scripts under `tmp/` were used for scratch setup and inspection; they are not shown by Git because `tmp/` is ignored.

Full final `git status --short` (including this report):

```text
 M backend/app/services/test_service.py
 M frontend/src/pages/BankingPage.tsx
?? HEAD_test_service.py
?? OLD_test_service.py
?? add67.py
?? add_clerk5_config.py
?? add_test6_ids.py
?? addtests.py
?? analyze_existing.py
?? backend/build_banking_maths_set2_ledger.py
?? backend/check_banking_maths_set2_create_test.py
?? backend/dedup_banking_maths_set2.py
?? backend/generate_banking_maths_set2_questions.py
?? backend/import_banking_clerk_test6.py
?? backend/import_banking_maths_set2_questions.py
?? backend/maths_set2/
?? backend/report_banking_maths_bank.py
?? backend/report_banking_maths_set2_db.py
?? backend/report_banking_maths_set2_reconciliation.py
?? backend/restore_filters.py
?? backend/seed_clerk_current_affairs_sections.py
?? backend/tmp_db.py
?? backend/validate_banking_maths_set2_bank.py
?? backend/verify_banking_maths_set2_questions.py
?? balance3.py
?? balance_secs.py
?? balance_secs2.py
?? batch10.py
?? batch11.py
?? batch12.py
?? batch8.py
?? batch9.py
?? build_report.py
?? check67.py
?? check_abort.py
?? check_history.py
?? chk.py
?? clerk_check.py
?? corrupt_test.py
?? data/banking_clerk_current_affairs_section_ids.json
?? data/banking_clerk_current_affairs_test5_questions.json
?? data/banking_clerk_current_affairs_test6_questions.json
?? data/banking_maths_number_system_questions.json
?? data/banking_maths_percentage_questions.json
?? data/banking_maths_profit_loss_discount_questions.json
?? data/banking_maths_quadratic_equations_questions.json
?? data/banking_maths_ratio_proportion_questions.json
?? dedupe_clerk5.py
?? export_clerk_backup.py
?? export_ids.py
?? export_test5.py
?? fix_card_style.py
?? fix_clerk_configs.py
?? fix_clerk_render.py
?? fix_encoding.py
?? fixcounts.py
?? fixcounts2.py
?? fixcounts3.py
?? fixcounts4.py
?? fixcounts5.py
?? fixcounts6.py
?? fixcounts_final.py
?? fixjsx.py
?? fixpo.py
?? fixpoconfig.py
?? gen_clerk5.py
?? inspect_a.py
?? inspect_attempts.py
?? inspect_ids.py
?? inspect_schema.py
?? inspect_sections.py
?? make_ledger.py
?? pagecount.py
?? reconcile.py
?? rename_importer.py
?? reports/banking_maths_final_report.md
?? reports/banking_maths_set2_create_test_report.md
?? reports/banking_maths_set2_db_after.json
?? reports/banking_maths_set2_db_before.json
?? reports/banking_maths_set2_db_reconciliation.md
?? reports/banking_maths_set2_dedup_report.md
?? reports/banking_maths_set2_final_report.md
?? reports/banking_maths_set2_source_ledger.csv
?? reports/banking_maths_set2_source_ledger.md
?? reports/banking_maths_set2_validation_report.md
?? reports/banking_maths_source_ledger.md
?? reports/clerk_test6_evidence_ledger.md
?? reports_review_data.json
?? restore_corrupt.py
?? restore_rotation.py
?? review_automated.py
?? review_count.py
?? review_datasets.py
?? review_dups.py
?? review_early.py
?? review_early2.py
?? review_json.py
?? review_times.py
?? show_block.py
?? split_test4.py
?? tmp_bp.py
?? tmp_bp2.py
?? tmp_check.py
?? tmp_empty.py
?? tmp_ids.py
?? tmp_ids2.py
?? tmp_ids3.py
?? tmp_keys.py
?? tmp_maths_chapters.py
?? tmp_maths_chapters2.py
?? tmp_maths_chapters3.py
?? tmp_maths_subjects.py
?? tmp_po.py
?? tmp_po2.py
?? tmp_po3.py
?? tmp_q.py
?? tmp_schema2.py
?? tmp_sec.py
?? tmp_subj_totals.py
?? tmp_tables.py
?? tmp_users.py
?? tmp_valid.py
?? used_pages.py
?? validate17.py
?? verify_clerk.py
?? verify_datasets.py
?? verify_secs.py
?? verify_temp_after.py
?? verify_temp_before.py
```

All untracked files outside the batch-2 list are pre-existing Clerk Current Affairs / investigation work and were left untouched.

## 9. Remaining issues

No blocking issue remains for Banking Maths batch 2. Every requested check completed successfully.

Non-blocking notes:

- The text-layer parse found 9 items in `PROFIT&LOSS SET-1 (Eng).pdf` versus 10 in the other profit sets, and one printed key was missing in `QUADRATIC EQUATION SET-5 (Eng).pdf`. These are source-reference observations only; no PDF MCQ was imported, so they do not affect the shipped bank.
- The pytest run emitted one pre-existing `StarletteDeprecationWarning` from FastAPI's test client.
- The temporary verification database was dropped after verification; backup files were kept outside the publication scope.
