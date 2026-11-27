# Banking Maths Set 3 — Final Report

Scope: six new Banking Maths chapters for **Banking Clerk** and **Banking PO** only. Banking Others was never written and remained empty of Maths section questions.

## 1. Dataset counts and structure

| Chapter | Dataset file | Questions | Part 1 | Part 2 | Part 3 | Part 4 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Simple Interest | `data/banking_maths_simple_interest_questions.json` | 120 | 15 | 20 | 30 | 55 |
| Compound Interest | `data/banking_maths_compound_interest_questions.json` | 120 | 15 | 20 | 30 | 55 |
| Mixture and Alligation | `data/banking_maths_mixture_alligation_questions.json` | 120 | 15 | 20 | 30 | 55 |
| Problems on Age | `data/banking_maths_problems_on_age_questions.json` | 120 | 15 | 20 | 30 | 55 |
| Partnership | `data/banking_maths_partnership_questions.json` | 120 | 15 | 20 | 30 | 55 |
| Time and Work | `data/banking_maths_time_and_work_questions.json` | 120 | 15 | 20 | 30 | 55 |
| **Total** | | **720** | **90** | **120** | **180** | **330** |

Each chapter uses 24 independently generated families with five fresh variants. Every item has four distinct options, one correct option, a non-empty explanation, a valid `EASY` / `MEDIUM` / `HARD` difficulty and the same schema as Sets 1 and 2. All 720 are tagged `VERIFIED` / `ORIGINAL_VERIFIED` with `exam_year = null`; none is a PYQ or a verbatim PDF MCQ. `source_page` records a topic reference only.

## 2. Source ledger and PDF coverage

All 29 supplied PDFs (772 pages) were inspected page by page. 486 pages exposed a text layer; 286 image-only pages were rendered and read with OCR. Printed keys were recorded as untrusted reference data and were never copied into the bank.

`reports/banking_maths_set3_source_ledger.csv` has 1,650 rows: 930 PDF/OCR reference rows and 720 shipped-question provenance rows. It records the PDF filename, page, question number where available, chapter/subtopic, original text, options, printed answer where available, usability, verification status and source-derived versus original classification. `reports/banking_maths_set3_source_ledger.md` summarises the per-file inventory and reconciles all 720 shipped originals to their topic references.

No PDF item was imported verbatim: several reference sets use five options instead of four, printed keys were not trusted, and OCR of mathematical notation is not reliable enough to certify an answer. The PDFs defined topic scope and difficulty only.

## 3. Verification and deduplication

- `backend/verify_banking_maths_set3_questions.py`: **720 questions verified, 0 failures**. Every answer was recomputed from `verification_data` without trusting the stored answer; options, explanations, difficulty labels, part sizes and uniqueness were also checked.
- `backend/dedup_banking_maths_set3.py`: run before import against the pre-import database. **720 new questions**, **1,200 Set 1+2 questions**, **13,732 database questions** screened. Exact duplicates, normalized duplicates, number-masked collisions, lexical near-duplicates, cross-chapter near-duplicates and semantic flags were all **0**. Repeated number-only templates found during development were replaced with distinct names, contexts and wording before shipping.
- `backend/validate_banking_maths_set3_bank.py`: **ALL CHECKS PASSED** — 720 dataset questions, 1,440 planned deterministic IDs, schema/provenance checks, recomputed answers, deduplication excluding the planned IDs, and 48 availability checks through the real `get_test_availability` service.

## 4. Database import and reconciliation

A local backup was taken and verified before import. All database work used a process-only local override; the environment file was not modified. The importer validates the six datasets, resolves the 12 target chapters, checks that no foreign rows occupy them, plans 1,440 deterministic `uuid5` IDs, and writes only `questions` and `question_options`. The transaction rolls back on any failed post-check.

- `--dry-run` before import: preflight OK, no writes.
- Real import: **1,440 inserted, 0 updated**, all 12 exam/chapter combinations ended with part counts 15 / 20 / 30 / 55.
- Idempotency re-run: **0 inserted, 1,440 updated**, no row-count growth.
- Banking Others remained empty of these section questions.
- One initial post-check failed because of a condition-precedence bug; the transaction rolled back cleanly, the importer was corrected, and the subsequent import and re-run passed. No residue remained from the failed attempt.

`reports/banking_maths_set3_db_reconciliation.md` confirms:

| Table | Before | After | Delta |
| --- | ---: | ---: | ---: |
| `questions` | 13,732 | 15,172 | +1,440 |
| `question_options` | 61,053 | 66,813 | +5,760 |
| all other tables | unchanged | unchanged | 0 |

Questions by exam/subject: Clerk `math-quant` and PO `math-quant` each gained 720; all other exam/subject groups were unchanged. Prior Maths sections stayed at 1,200 questions, 48 new sections appeared, attempts/answers/users/chapters/subjects/exams and all other rows were unchanged.

## 5. Scratch `create_test` verification

A fresh restored local copy of the imported bank was used. The checker refuses any database other than the designated scratch copy, so the live database was never used for `create_test`. The scratch copy was dropped afterwards and confirmed absent.

`backend/check_banking_maths_set3_create_test.py` exercised the real `create_test` for all **48** sections:

| Check | Result |
| --- | ---: |
| Sections exercised | 48 / 48 |
| Attempts created on the scratch copy | 48 |
| Banking Clerk chapters covered | 6 / 6 |
| Banking PO chapters covered | 6 / 6 |
| Part sizes per chapter | 15 / 20 / 30 / 55 |
| Section-based selection | every attempt selected 15/15, 20/20, 30/30 or 55/55 questions from its own section |
| 15-question duration | 630 s = 10.5 min |
| 20-question duration | 840 s = 14 min |
| 30-question duration | 1260 s = 21 min |
| 55-question duration | 2310 s = 38.5 min |

Duration rule confirmed: **42 seconds per question**. Full per-section evidence is in `reports/banking_maths_set3_create_test_report.md`. After the scratch exercise, the live database still had 15,172 questions, 66,813 options, 61 attempts and 2,667 test questions.

## 6. Test and build results

- Frontend: `npm run build` passed (`tsc -b && vite build`); 55 modules transformed and the production assets were emitted.
- Backend: `python -m pytest tests -q` — **465 passed, 2 skipped, 1 warning in 1628.55s (0:27:08)**. The only warning is a pre-existing `StarletteDeprecationWarning` about `httpx` / `starlette.testclient`, unrelated to this batch. No failures or errors.

## 7. Frontend integration

`frontend/src/pages/BankingPage.tsx` gained exactly six entries in `mathsChapterKeys`:

```ts
"simple-interest": "simple_interest",
"compound-interest": "compound_interest",
"mixture-and-alligation": "mixture_alligation",
"problems-on-age": "problems_on_age",
partnership: "partnership",
"time-and-work": "time_and_work",
```

No other frontend logic was changed.

## 8. Exact Set 3 files

Scripts and packages:

- `backend/build_banking_maths_set3_ledger.py`
- `backend/check_banking_maths_set3_create_test.py`
- `backend/dedup_banking_maths_set3.py`
- `backend/generate_banking_maths_set3_questions.py`
- `backend/import_banking_maths_set3_questions.py`
- `backend/report_banking_maths_set3_db.py`
- `backend/report_banking_maths_set3_reconciliation.py`
- `backend/validate_banking_maths_set3_bank.py`
- `backend/verify_banking_maths_set3_questions.py`
- `backend/maths_set3/` (`__init__.py`, `bank.py`, and the six chapter builders)

Datasets: the six `data/banking_maths_*_questions.json` files listed in section 1.

Reports:

- `reports/banking_maths_set3_create_test_report.md`
- `reports/banking_maths_set3_db_after.json`
- `reports/banking_maths_set3_db_before.json`
- `reports/banking_maths_set3_db_reconciliation.md`
- `reports/banking_maths_set3_dedup_report.md`
- `reports/banking_maths_set3_final_report.md`
- `reports/banking_maths_set3_source_ledger.csv`
- `reports/banking_maths_set3_source_ledger.md`
- `reports/banking_maths_set3_validation_report.md`

Backups: two local dumps were retained outside the Set 3 commit scope (one pre-import and one scratch-source copy). No dump filename is recorded in Git-facing reports.

Frontend: `frontend/src/pages/BankingPage.tsx` — the six mappings above.

## 9. Remaining issues

None blocking. `git diff --check` was clean at verification time. The pre-existing modification to `backend/app/services/test_service.py` and all unrelated untracked files were preserved and excluded from this batch. No commit, push, reset, stash, clean or staging operation had been performed when this report was written.
