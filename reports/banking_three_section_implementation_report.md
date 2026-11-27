# Banking Three-Section Implementation Report

## Status

Implemented and validated. Every targeted chapter has exactly three stable sections with 10, 15 and 15 questions. No targeted chapter was left unallocated, and no validation step failed.

## Scope

The rollout covers only Banking Clerk and Banking PO chapters under:

- English
- General/Banking Awareness
- Computer

Other exams, subjects, Banking Maths, and Current Affairs were left unchanged.

Totals:

- 98 target chapters
- 294 sections
- 3,920 allocated questions
- 92 surplus usable questions preserved without section assignment
- 0 shortage chapters

## Implementation

The existing `Question.section` field and `section_filter` request path are reused; no new section table was introduced.

Section names are globally unique and deterministic:

`<exam_slug_with_underscores>_<subject_slug_with_underscores>_<chapter_key>_part_<1|2|3>`

Allocation considers only active questions. Normalized duplicate question texts are skipped. The first 40 usable rows are selected by `created_at`, then `id`, and split 10 / 15 / 15. Inactive rows and surplus usable rows are preserved and not allocated.

Section-only availability accepts 10 and 15 questions only for the six three-section Banking prefixes. Section question selection is deterministic for those prefixes. Durations are 42 seconds per question: 10 questions produce 420 seconds and 15 questions produce 630 seconds.

The Banking frontend chooser now follows chapter → section → start test for the targeted subjects. The Banking Maths four-part chooser and Current Affairs behavior remain unchanged.

## Files changed

Backend:

- `backend/app/routers/tests.py`
  - Reports the section on active test reads when all questions share one section.
- `backend/app/schemas/tests.py`
  - Adds `section` to `ActiveTestRead`.
- `backend/app/services/test_service.py`
  - Adds the three-section prefix rules, deterministic ordering and 10/15 section counts.
- `backend/banking_three_sections_common.py`
  - Shared section names, normalization, diagnostics and deterministic allocation rules.
- `backend/build_banking_three_section_baseline.py`
  - Generates the read-only pre-allocation baseline.
- `backend/allocate_banking_three_sections.py`
  - Transactional, idempotent allocator.
- `backend/check_banking_three_sections.py`
  - Live validation and disposable-copy create/answer/submit checks.
- `backend/tests/test_banking_three_sections.py`
  - Backend coverage for all 98 chapters and API section reporting.

Frontend:

- `frontend/src/pages/BankingPage.tsx`
  - Adds the chapter/section chooser for the three targeted subjects.
- `frontend/src/services/tests.ts`
  - Adds `section` to the active test type.

Evidence:

- `reports/banking_three_section_baseline_report.md`
- `reports/banking_three_section_baseline.csv`
- `reports/banking_three_section_allocation_report.md`
- `reports/banking_three_section_allocation_dry_run.md`
- `reports/banking_three_section_validation_report.md`
- `reports/banking_three_section_create_test_report.md`
- `reports/banking_three_section_implementation_report.md`

## Pre-write safeguards

The baseline was written before any allocation write. It recorded 98 chapters, 3,920 planned questions, 92 surplus questions and 0 shortage chapters.

A verified local database backup was captured before writes. Verification reported 4,824,829 bytes and 118 table-of-contents entries. All database access used the local development database; no hosted database was contacted and no environment file was modified.

## Allocation and replay

Live allocation changed only `questions.section`. No questions were inserted, deleted or rewritten.

Result:

- 98 chapters allocated
- 3,920 questions allocated
- 3,920 rows changed
- 92 surplus questions preserved
- 0 shortages

A full replay after the final code state reported 0 rows changed, confirming idempotence.

## Validation results

### Static and service-level validation

`reports/banking_three_section_validation_report.md` records read-only validation against the live database:

- 98 chapters checked
- 294 sections checked
- 0 tests created
- 0 failures

Checks confirmed exactly three sections per chapter, exact 10/15/15 active counts, deterministic membership and ordering, unique question IDs, no repeated content across a chapter's sections, no section-name reuse, preserved surplus questions, and real service availability.

### Create/answer/submit validation

`reports/banking_three_section_create_test_report.md` records checks on a disposable database copy:

- 98 chapters checked
- 294 sections checked
- 294 tests created
- 0 failures

The disposable database copy was removed after verification.

### Browser verification

Live browser navigation verified chapter → section → test start for Clerk English sections 1/2/3, Clerk General/Banking Awareness section 1, Clerk Computer section 2, and PO English section 3. Each attempt reached the test page with the expected section, question count and duration.

### Backend tests

Scoped full backend suite from `backend/`:

- 467 passed
- 2 skipped
- 1 warning
- 0 failed
- 1561.16 seconds (0:26:01)

The single warning is the pre-existing Starlette/TestClient `httpx` deprecation warning.

A root-level `python -m pytest -q` collection is not usable in this checkout because standalone legacy scripts require `psycopg2`, which is not installed in the backend environment. The authoritative full backend suite is `python -m pytest tests -q` from `backend/`, and it passed.

### Frontend build

`npm run build` passed with TypeScript checking and Vite production build:

- 55 modules transformed
- built in 26.78 seconds

## Result

All targeted chapters are allocated and validated. The implementation is complete.
