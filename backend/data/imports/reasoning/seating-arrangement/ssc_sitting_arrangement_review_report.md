# SSC Sitting Arrangement → Banking Clerk Reuse Review

## Scope and source audit

All work used only local PostgreSQL at `127.0.0.1:5432/ssc_prep`, Alembic revision `0010_banking_catalog`. No migration was run.

Source: SSC → Reasoning → Sitting Arrangement, chapter ID `32faa174-9f26-4524-9639-f325ef6674b8`; baseline **30 active, 0 inactive**. The 30 records comprise 16 original SSC-style items and 14 items with source lecture/page metadata from Sitting Arrangement class-note PDFs. All have text, source metadata, an explanation, no image dependency, four or five options, and exactly one keyed correct option. None of the 26 copied questions contained Hindi/Devanagari; their source text and options were copied verbatim.

## Eligibility and exclusions

| Result | Count |
|---|---:|
| Source questions inspected | 30 |
| Eligible and unique for Banking Clerk | 26 |
| Duplicate against existing Banking arrangement banks | 0 |
| Held from import | 4 |

Held questions:

- `11396733-7bfa-4c8d-bf97-fe2bc9f3a486`: circular clues conflict; two people are forced into one seat.
- `39b4c4bc-3253-46af-bbcc-b2a07b018db5`: row length is not fixed because the right end is unconstrained.
- `80f9702d-de5e-4432-ae34-aae4d6aad6a9`: the circle permits different answers for the asked neighbour; the stored key is not unique.
- `d9edf595-08f6-4587-b4ab-d328ff05f3de`: the keyed choice is consistent with the clues, but the stored explanation gives an arrangement that contradicts them.

The 26 eligible questions were assigned by arrangement type: 15 row/linear (including the two-row item), 8 circular, and 3 square/rectangular. Normalized question-text comparison and manual setup/constraint comparison found no duplicates in the pre-existing Banking Linear or Circular questions.

## Destination chapters and counts

| Banking Clerk chapter | ID | Before active/inactive | Added | After active/inactive |
|---|---|---:|---:|---:|
| Linear Arrangements | `7a6e3168-894b-47c8-86df-ab6891f28d2b` | 5 / 0 | 15 | 20 / 0 |
| Circular Arrangements | `01898051-c8fe-4cc4-b1a8-777fecc7b3b9` | 5 / 0 | 8 | 13 / 0 |
| Square / Rectangular Arrangements | `98e79592-216a-4d6e-a4fb-ab0ad3d62fe6` | 0 / 0 | 3 | 3 / 0 |

The importer created new question IDs. All original SSC questions remain in the source chapter: it still has 30 active, 0 inactive questions, and the four held records remain active. The ten pre-existing Banking Linear/Circular rows were preserved; their missing explanations were not changed.

Each imported source field retains the original source string and appends the SSC chapter ID plus original question ID. Question text, option labels/text/order, correct answer, explanation, difficulty, PYQ fields, and image field match their SSC originals.

## Import and verification

- Pre-import dry-run: 26 eligible, 0 duplicates, 0 rejected, 0 errors.
- Transactional import: 26 inserted, 0 duplicates, 0 rejected, 0 errors.
- Database integrity comparison: all 26 copies match their originals and JSON; all 26 have new unique IDs and belong to the mapped Banking chapter. All options are present with exactly one correct answer and explanations are preserved.
- Replay dry-run: 26 duplicates detected, 0 would import, 0 errors.
- Authenticated local API: HTTP 200; Linear returned 20, Circular 13, and Square/Rectangular 3 active questions. The 26 copied records matched their text, options, answer, explanation, source, and chapter ID.
- New regression test: `backend/tests/test_ssc_sitting_arrangement_reuse.py` passed (`1 passed`).
- Two existing question-bank integration tests (`test_valid_json_import_and_dry_run_are_atomic` and `test_valid_five_option_json_import_returns_option_e_in_management_api`) produced no output and hung for more than 60 seconds; they were interrupted and have no pass/fail result.
- Frontend production build: `npm run build` passed (Vite transformed 55 modules and completed the production build).
- Final read-only database verification: Linear 20 active / 0 inactive, Circular 13 / 0, Square/Rectangular 3 / 0; SSC source remains 30 / 0. All four held question IDs remain in the SSC source and none are present in the three Banking destination chapters.

## Artifacts

- `backend/data/imports/reasoning/seating-arrangement/ssc_sitting_arrangement_verified.json`
- `backend/data/imports/reasoning/seating-arrangement/ssc_sitting_arrangement_review_report.md`
- `backend/tests/test_ssc_sitting_arrangement_reuse.py`
