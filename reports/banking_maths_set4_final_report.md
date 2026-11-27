# Banking Maths Set 4 - Final Report

## Scope

This batch adds **720 verified questions** for **Banking Clerk** and **Banking PO**
only, across six new chapters:

| Chapter | Key | Questions | Part sizes |
| --- | --- | ---: | --- |
| Pipe and Cistern | `pipe_and_cistern` | 120 | 15 / 20 / 30 / 55 |
| Average | `average` | 120 | 15 / 20 / 30 / 55 |
| Speed, Time and Distance | `speed_time_distance` | 120 | 15 / 20 / 30 / 55 |
| Problems on Trains | `problems_on_trains` | 120 | 15 / 20 / 30 / 55 |
| Boats and Streams | `boats_and_streams` | 120 | 15 / 20 / 30 / 55 |
| Mensuration - 2D | `mensuration_2d` | 120 | 15 / 20 / 30 / 55 |

Each dataset question is duplicated into exactly two exam sections:

`banking_clerk_maths_<key>_part_<n>` and `banking_po_maths_<key>_part_<n>`.

That produces 48 new sections and 1,440 imported question rows.

## Source inspection and provenance

All 23 locally supplied PDFs were inspected under
`tmp/set4_pdf_text2`: **214 pages total**, 171 with a usable text layer and
43 image-only pages rendered at 150 dpi and read with OCR. The per-file,
per-page detail is in `reports/banking_maths_set4_source_ledger.csv` and the
summary is in `reports/banking_maths_set4_source_ledger.md`. All 23 PDFs are
also referenced by at least one shipped item's `source_page` topic reference.

The PDFs were treated as topic/reference evidence only. The ledger separates
613 recorded PDF/OCR source rows from 720 shipped question rows:

- no PDF MCQ was imported verbatim;
- printed answer keys were recorded as untrusted reference data;
- the two image-only Mensuration decks were not assigned question numbers
  because OCR of mathematical notation is not certifiable;
- every shipped item is `ORIGINAL_VERIFIED`, `exam_year = null`,
  `verification_status = VERIFIED`, and carries the explicit disclaimer that it
  is neither an extracted PDF MCQ nor a PYQ. No shipped item is classified as
  `SOURCE_DERIVED` or as an PYQ.

A final read of the six datasets confirmed 120 questions per chapter, 24
families per chapter, and part counts of exactly 15 / 20 / 30 / 55 for every
chapter, including Average.

## Generation and verification

`backend/generate_banking_maths_set4_questions.py` generated 720 questions
with 24 families per chapter and five distinct variants per family. Answers
were computed in Python from exact `Fraction` arithmetic, never copied from a
printed key.

`backend/verify_banking_maths_set4_questions.py` independently recomputed all
720 answers from `verification_data.inputs` using 144 embedded formula lambdas
written separately from the builders. It also checked:

- exact schema and 120 items per chapter;
- part sizes 15 / 20 / 30 / 55;
- four distinct options and exactly one correct option;
- correct letter/index agreement;
- non-empty explanations and valid difficulty labels.

Result: **720 questions checked, 0 failures**.

Two defects found during independent checking were corrected before final
verification and are reflected in the shipped artifacts:

- the pipe alternate-flow formulas now treat the stored `X` and `Y` values as
  completion times and use their reciprocals as rates. The two previously
  mismatching samples (`pipe_and_cistern-0025`,
  `pipe_and_cistern-0110`) now recompute to the shipped answer `9.5`;
- the Boats and Streams builder and its independent formula sheet now use the
  exact `Fraction` alias directly, removing a helper that accepted only one
  argument. All 20 affected boat families now recompute correctly.

The final verifier that embeds these corrected formulas passed all 720 items.

## Deduplication

`backend/dedup_banking_maths_set4.py` screened the new batch against itself,
all 1,920 questions in Banking Maths Sets 1-3, and all 15,172 pre-import
database questions using exact, normalized, number-masked, lexical and
semantic checks.

- Exact duplicates: 0
- Normalized duplicates: 0
- Number-masked template collisions: 0
- Lexical near-duplicates: 0
- Semantic flags: 1, manually reviewed and retained as generic topic overlap
  (different second-leg data and different answer, not a verbatim duplicate)

No question was reworded to evade a duplicate check. Details are in
`reports/banking_maths_set4_dedup_report.md`.

## Import safety and database reconciliation

Import used only the approved local database, passed as a process-only
`DATABASE_URL`. No credentials were written to files, `.env` was not modified,
and no hosted or production database was contacted. A verified custom-format
backup was taken before import.

The importer ran a preflight, one dry run, one live import, and one recorded
idempotency re-run:

| Run | Result |
| --- | --- |
| Dry run | preflight OK, no changes written |
| Live import | 1,440 inserted, 0 updated |
| Idempotency re-run | 0 inserted, 1,440 updated, no duplication |

Reconciliation from `reports/banking_maths_set4_db_reconciliation.md`:

| Measure | Before | After | Delta |
| --- | ---: | ---: | ---: |
| `questions` | 15,172 | 16,612 | +1,440 |
| `question_options` | 66,813 | 72,573 | +5,760 |
| Set 4 section questions | 0 | 1,440 | +1,440 |
| Prior section questions | 3,840 | 3,840 | 0 |
| Banking Others maths questions | 0 | 0 | 0 |
| Maths sections | 128 | 176 | +48 |
| Banking Clerk maths questions | 1,920 | 2,640 | +720 |
| Banking PO maths questions | 1,920 | 2,640 | +720 |
| `test_attempts` | 61 | 61 | 0 |
| `test_questions` | 2,667 | 2,667 | 0 |
| `user_answers` | 272 | 272 | 0 |
| `users`, `chapters`, `subjects`, `exams` | unchanged | unchanged | 0 |

Only `questions` and `question_options` changed. No attempts, answers,
progress, users, chapters, subjects or exams were modified by the import.

## Availability and real `create_test`

`backend/validate_banking_maths_set4_bank.py` used the real
`get_test_availability` service for all **48** new sections and confirmed the
42-second-per-question rule (630 / 840 / 1260 / 2310 seconds). Result:
**ALL CHECKS PASSED** (`reports/banking_maths_set4_validation_report.md`).

A scratch copy restored from the live database was used for
`backend/check_banking_maths_set4_create_test.py`, which called the real
`create_test` for all 48 sections. Each attempt selected exactly its own
section with the correct count and duration. Result: **48/48 passed**; the
scratch database was then dropped and its absence confirmed.

## Frontend and backend builds

- Frontend: `npm run build` passed (`tsc -b && vite build`).
- Backend pytest using the repository virtual environment: **465 passed,
  2 skipped, 0 failed, 0 errors, 1 warning in 1294.05s (0:21:34)**. The single
  warning is a Starlette/FastAPI `httpx` deprecation notice from the test
  client and is unrelated to Set 4. An earlier attempt with the system Python
  was abandoned because that interpreter has no pytest installed; it did not
  run any tests.

## Git safety

No files were staged, committed, pushed, reset, stashed, cleaned or discarded.
The unrelated tracked modification `backend/app/services/test_service.py` was
left untouched. `frontend/src/pages/BankingPage.tsx` already contained Set 1-3
mappings from prior work; this batch added only the six Set 4 slug-to-key
entries. Set 1, Set 2 and Set 3 files were preserved unchanged.

The final `git status --short` and exact safe file list are provided in the
final response.

## Limitations and unresolved issues

No unresolved Set 4 issues remain. The only stated limitation is deliberate:
the two image-only Mensuration decks were retained as reference evidence but
were not assigned printed question numbers because OCR of mathematical
notation could not be certified. Their topics still appear in shipped original
questions, and all 23 PDFs are referenced by shipped metadata.
