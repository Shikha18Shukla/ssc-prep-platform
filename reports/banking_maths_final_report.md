# Banking Maths Question Bank - Final Report

Date: 2026-11-27

## Result

The five Banking Maths chapters now have a complete, verified question bank and
four progressive parts each, imported for **Banking Clerk** and **Banking PO**:

| Chapter | Questions | Part 1 | Part 2 | Part 3 | Part 4 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Vedic Maths Tricks - Calculation Techniques | 120 | 15 | 20 | 30 | 55 |
| Simplification | 120 | 15 | 20 | 30 | 55 |
| Approximation | 120 | 15 | 20 | 30 | 55 |
| Missing Number Series | 120 | 15 | 20 | 30 | 55 |
| Wrong Number Series | 120 | 15 | 20 | 30 | 55 |
| **Total** | **600** | | | | |

Imported as 1,200 rows (600 per exam) across 40 sections. `Banking Others` was
left untouched because that exam is entirely empty by design.

## Source handling

- All 17 local PW Banking Wallah PDFs were inspected directly: page/character
  inventory in `tmp/pdf_text/inventory.json`, rendered contact sheets in
  `tmp/sheets/`, and a full OCR pass (all pages, all 17 decks) in `tmp/ocr/`.
- The decks are image-only lecture slides with theory and five-option MCQs; they
  do not contain 100 four-option questions per chapter.
- The bank therefore uses **original questions** aligned to the techniques taught
  in those decks. Every item records `source_type = ORIGINAL_VERIFIED`, a
  `provenance_note`, a verification method and the recomputation data.
- No question is labelled as a previous-year question. `is_pyq` is false and
  `pyq_year` is null for all 1,200 rows.
- `source_page` is a topic reference to the class-notes pages, not a claim that a
  question was copied from a PDF page.

## Verification

| Check | Result |
| --- | --- |
| Dataset generator | 600 questions, 5 chapters x 120 |
| Independent answer recomputation | 600 checked, 0 failures |
| Four unique options per question | 600 / 600 |
| Exactly one correct option | 600 / 600 |
| Non-empty explanation | 600 / 600 |
| Part sizes 15 / 20 / 30 / 55 | all 5 chapters |
| Duplicate texts within/between datasets | 0 |
| Duplicate texts against 11,332 existing DB questions | 0 |
| DB rows compared with datasets (text, explanation, difficulty, section, source, PYQ flag, options, correctness) | 1,200 checked, 0 problems |
| Section counts in DB | 40 / 40 sections match |
| Rows with 4 options, 1 correct option, explanation | 1,200 / 1,200 |
| Rows incorrectly flagged PYQ | 0 |
| `get_test_availability` via the real test service | 40 / 40 sections pass |
| End-to-end `create_test` in a disposable DB copy | 15 / 20 / 30 / 55 sections created, correct durations, 4-option questions |
| Durations from the section branch (42 s/question) | 10.5 / 14 / 21 / 38.5 min |

## Backup and data safety

- A custom-format pre-import backup was created outside the repository and verified; backup files are not committed.
- The backup was restored into a scratch database and verified: all 16 table
  counts matched the live database and content MD5 hashes matched for
  `questions`, `question_options`, `chapters`, `subjects` and `exams`.
- The scratch database was dropped after verification.
- The import ran in a single transaction with post-import checks and rollback on
  failure. Re-running it twice produced `0 inserted, 1200 updated`, proving
  idempotency.
- Live `questions` went from 11,332 to 12,532 (+1,200); `question_options` went
  from 51,453 to 56,253 (+4,800). No existing question, attempt, answer or
  unrelated table was deleted or modified.

## Frontend

`frontend/src/pages/BankingPage.tsx` now routes the Math & Quant subject to a
chapter picker and then to four part cards per chapter (15 / 20 / 30 / 55
questions, Easy to Advanced). Starting a card creates a section-filtered test
through the existing backend flow. Production build passed.

## Tests

- Backend: `465 passed, 2 skipped` (`backend/.venv` pytest run).
- Frontend: `npm run build` passed (`tsc -b && vite build`).

## Files added

- `backend/generate_banking_maths_questions.py`
- `backend/verify_banking_maths_questions.py`
- `backend/import_banking_maths_questions.py`
- `backend/validate_banking_maths_bank.py`
- `backend/report_banking_maths_bank.py`
- `data/banking_maths_vedic_calculation_questions.json`
- `data/banking_maths_simplification_questions.json`
- `data/banking_maths_approximation_questions.json`
- `data/banking_maths_missing_number_series_questions.json`
- `data/banking_maths_wrong_number_series_questions.json`
- `reports/banking_maths_source_ledger.md`
- `reports/banking_maths_dedup_report.md`
- `reports/banking_maths_reconciliation.md`
- `reports/banking_maths_final_report.md`

## Reproduction

```powershell
# DATABASE_URL is supplied through the process environment for an isolated local database
python backend/generate_banking_maths_questions.py
python backend/verify_banking_maths_questions.py
python backend/import_banking_maths_questions.py --dry-run
python backend/import_banking_maths_questions.py
python backend/validate_banking_maths_bank.py
python backend/report_banking_maths_bank.py
```

At the time of verification nothing had been staged, committed, pushed, reset or cleaned. The
`backend/app/services/test_service.py` working-tree change was left untouched by this batch.
