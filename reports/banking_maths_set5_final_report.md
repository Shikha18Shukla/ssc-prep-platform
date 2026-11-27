# Banking Maths Set 5 - Final Report

## Scope

Six Banking Maths chapters were completed for **Banking Clerk** and
**Banking PO** only:

- Mensuration – 3D (`mensuration-3d`)
- Permutations (`permutations`)
- Combinations (`combinations`)
- Probability (`probability`)
- Data Interpretation (`data-interpretation`)
- Caselet Data Interpretation (`caselet-data-interpretation`)

`Banking Others` was never written and was checked explicitly before and after
import. No Set 1–4 question was modified.

## Question bank

Each chapter has 120 original, independently verified questions split into
four parts:

| Part | Questions | Duration |
| ---: | ---: | ---: |
| 1 | 15 | 630 seconds (10.5 minutes) |
| 2 | 20 | 840 seconds (14 minutes) |
| 3 | 30 | 1260 seconds (21 minutes) |
| 4 | 55 | 2310 seconds (38.5 minutes) |

Totals: **720 dataset questions**, **1,440 imported rows** (720 Clerk + 720
PO), 48 new sections (24 per exam), 144 distinct question families exercised
five times each, 2,880 option rows after import.

Every item has four distinct options, one correct option, a matching answer
text/index, a non-empty explanation, a valid difficulty, `source_type =
ORIGINAL_VERIFIED`, `verification_status = VERIFIED`, and `exam_year = null`.
No item is labelled as a previous-year question.

## Source inspection and ledger

Ten supplied PDF decks were inspected page by page:

- 211 pages total;
- 0 text-layer pages;
- 211 image-only pages read with OCR at 150 dpi;
- 211 page-level ledger rows plus 720 shipped-question rows = 931 ledger rows.

The chapter assignment was derived from extracted slide content, not from file
names. Several deck names referred to the preceding lecture. The resulting
mapping was:

| PDF(s) | Chapter |
| --- | --- |
| Mensurations 3D 01, Mensurations 3D 02 | Mensuration – 3D |
| Permuations 01 | Permutations |
| Combinations 01 | Combinations |
| Probability 01, 7e88503c-… | Probability |
| DATA INTERPRETATION 01, dd6dc577-…, d0d52b32-… | Data Interpretation |
| e1183040-… | Caselet Data Interpretation |

Printed questions, options and keys were treated as untrusted reference data
and were not copied. The decks defined topic scope and difficulty only. Every
shipped item is an original written for this bank; its `source_page` is a topic
reference, not a verbatim citation. Full evidence is in
`reports/banking_maths_set5_source_ledger.csv` and
`reports/banking_maths_set5_source_ledger.md`.

## Independent verification and deduplication

`backend/verify_banking_maths_set5_questions.py` recomputed all 720 answers
from `verification_data` without trusting the stored answer. It checked option
uniqueness, answer/index agreement, explanation consistency, units and
rounding, difficulty, part sizes, chapter counts and the absence of PYQ flags.
Result: **720 checked, 0 failures**.

`backend/dedup_banking_maths_set5.py` screened:

| Comparison | Result |
| --- | ---: |
| Exact duplicates within Set 5 | 0 |
| Normalized duplicates within Set 5 | 0 |
| Repeated number-masked templates within or across chapters | 0 |
| Set 5 vs Banking Maths Sets 1–4 (2,640 items) | 0 collisions |
| Set 5 vs pre-import database (16,612 items) | 0 collisions |
| Lexical near-duplicates, prior batches / DB / cross-chapter | 0 / 0 / 0 |
| Semantic flags, prior batches / DB | 0 / 0 |

No question was reworded to evade a check. Details are in
`reports/banking_maths_set5_dedup_report.md`.

## Database reconciliation and import safety

A verified custom-format backup was taken before import. All database scripts
used a process-only local override; `.env` was not modified, no credential was
written to a file, and no hosted database was contacted.

The importer ran preflight, one dry run, one live import and one recorded
idempotency replay:

| Run | Result |
| --- | --- |
| Dry run | preflight OK, no database changes |
| Live import | 1,440 inserted, 0 updated |
| Idempotency replay | 0 inserted, 1,440 updated, no duplication |

The import was transactional and rolled back on any failed post-check.
Reconciliation from `reports/banking_maths_set5_db_reconciliation.md`:

| Measure | Before | After | Delta |
| --- | ---: | ---: | ---: |
| `questions` | 16,612 | 18,052 | +1,440 |
| `question_options` | 72,573 | 78,333 | +5,760 |
| Set 5 section questions | 0 | 1,440 | +1,440 |
| Prior Maths section questions | 3,840 | 3,840 | 0 |
| Banking Others Maths questions | 0 | 0 | 0 |
| Maths sections | 176 | 224 | +48 |
| Banking Clerk Maths questions | 2,640 | 3,360 | +720 |
| Banking PO Maths questions | 2,640 | 3,360 | +720 |
| `test_attempts` | 61 | 61 | 0 |
| `test_questions` | 2,667 | 2,667 | 0 |
| `user_answers` | 272 | 272 | 0 |
| Users, attempts, catalog tables | unchanged | unchanged | 0 |

Only `questions` and `question_options` changed. No attempt, answer, progress,
user or catalog row was modified by the import.

## Chapter and section mapping

Sections use the unique template
`banking_{clerk|po}_maths_<chapter_key>_part_<part>`. Each of the 12 target
chapters received 120 questions per exam, split 15 / 20 / 30 / 55.

| Chapter key | Clerk chapter ID | PO chapter ID |
| --- | --- | --- |
| `mensuration_3d` | `9a74ea2e-c9d2-4717-97df-2d75006711b7` | `927f785d-6653-47c8-ad0b-355ff9f3f911` |
| `permutations` | `0176866a-5224-45aa-992a-81e1cc3fe146` | `1807d804-d552-4309-aa11-22c458e098ed` |
| `combinations` | `2881820c-5a17-4a43-9dfc-4e83f6c32c81` | `15959cfb-c2c2-405f-b8ff-09736fdf9c06` |
| `probability` | `5825b87d-f750-4e02-9638-287e95dcb357` | `f9e40c3d-a35a-4a05-9cae-7ff4c10b5e6d` |
| `data_interpretation` | `2f13c6fd-8ea9-40e9-a22c-a67dd776ade6` | `0c1ec4e8-d99e-42b2-885a-9f39610e675f` |
| `caselet_data_interpretation` | `6b7677ef-c307-4016-8ccf-00f8ff013a57` | `c7999381-c529-4ca1-b757-e7eba4543638` |

## Availability and real `create_test`

`backend/validate_banking_maths_set5_bank.py` used the real
`get_test_availability` service for all **48/48** new sections and confirmed
the exact counts, deterministic IDs, options, explanations, no PYQ flags and
the 42-second-per-question rule. Result: **ALL CHECKS PASSED**.

A restored isolated copy of the imported bank was used for
`backend/check_banking_maths_set5_create_test.py`. That script called the real
`create_test` with `chapter_id` omitted and only `section_filter` set. It
verified 48/48 sections, exact section isolation, 1,440 distinct selected
questions, and durations of 630 / 840 / 1260 / 2310 seconds. Result:
**ALL CHECKS PASSED**. The isolated copy was then dropped and its absence was
confirmed.

A second restored-copy exercise,
`backend/check_banking_maths_set5_di_rendering.py`, rendered all 16 Data
Interpretation and Caselet Data Interpretation sections through the real
`create_test`: **480/480 questions and 1,920/1,920 options** were rendered,
every question carried its data inline, no external image/table/graph/passage
was required, and every rendered question had one correct option. Result:
**ALL CHECKS PASSED**.

## Frontend and builds

Six slug-to-key mappings were added to `mathsChapterKeys` in
`frontend/src/pages/BankingPage.tsx` immediately after the existing Mensuration
– 2D entry. No other frontend logic changed.

- Frontend production build (`npm run build`, `tsc -b && vite build`): **passed**.
- Full backend pytest suite: **465 passed, 2 skipped, 0 failed, 0 errors,
  1 warning in 1230.04s (0:20:30)**. The single warning is the pre-existing
  Starlette/FastAPI `httpx` deprecation notice from the test client and is
  unrelated to Set 5.

## Git safety and exclusions

Nothing was staged, committed, pushed, reset, stashed, cleaned or discarded.
The unrelated tracked modification to `backend/app/services/test_service.py`
was preserved untouched. Existing unstaged Set 1–3 mappings and all Set 1–4
files were preserved. Scratch-database helpers, page maps, extraction logs and
temporary investigation scripts are working evidence only; they are not part
of the question bank and are ignored by Git.

## Deliverables

Core Set 5 files:

- `backend/maths_set5/` (package with `bank.py`, `common.py` and six chapter builders)
- `backend/generate_banking_maths_set5_questions.py`
- `backend/verify_banking_maths_set5_questions.py`
- `backend/dedup_banking_maths_set5.py`
- `backend/build_banking_maths_set5_source_ledger.py`
- `backend/report_banking_maths_set5_db.py`
- `backend/report_banking_maths_set5_reconciliation.py`
- `backend/import_banking_maths_set5_questions.py`
- `backend/validate_banking_maths_set5_bank.py`
- `backend/check_banking_maths_set5_create_test.py`
- `backend/check_banking_maths_set5_di_rendering.py`
- six `data/banking_maths_*_questions.json` datasets
- reports listed above, including this final report
- six frontend mapping lines in `frontend/src/pages/BankingPage.tsx`

## Result

Banking Maths Set 5 is complete: 720 original verified questions, 1,440
Clerk/PO rows, 48 validated sections, zero deduplication failures, full source
ledger coverage, exact database reconciliation, successful real-service
rendering, and no unresolved Set 5 issue.
