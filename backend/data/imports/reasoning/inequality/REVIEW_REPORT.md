# Inequality source review

## Source inventory

- `Inequality 02_Class Notes.pdf`: 21 pages; 16 genuine practice questions identified on pages 4–19.
- `Inequality 03_Class Notes.pdf`: 17 pages; 5 genuine practice questions identified on pages 9–13.
- `Inequality 04_Class Notes.pdf`: 22 pages; 13 genuine practice questions identified on pages 7–17 and 20–21.
- All 60 pages were visually reviewed. Covers, recaps, rules, teaching examples, summaries, and thank-you slides were not imported. The instructional Hindi rules were not treated as questions.

## Verification and deduplication

- 34 genuine questions found across the three PDFs.
- 32 questions independently verified for one answer choice (counting the five repeated question items once per appearance).
- Five lecture 03 questions are repeated in lecture 04: source pages 9–13 of lecture 03 match pages 7–11 of lecture 04 (same statement and conclusions). The lecture 03 copies are retained; lecture 04 copies are omitted.
- Two questions are held for manual review and excluded from the import.
- 27 unique, verified questions are in `inequality_verified_import.json`.

## Manual review

1. `Inequality 04_Class Notes.pdf`, p. 12 (Question 9): conclusions are `H ≤ M` and `H ≥ M`, while the statement does not order H and M. If H<M only conclusion I is true; if H>M only II is true; if H=M both are true. The source choices distinguish either conclusion from both, so there is no single answer valid across all permitted cases.
2. `Inequality 04_Class Notes.pdf`, p. 20 (Missing inequality): at least two listed symbol pairs satisfy both requested relations (`1 > 4` and `3 ≥ 6`), so the item has multiple valid options.

## Catalog and database state

- Target path: Banking Clerk (`banking-clerk`) → Reasoning (`reasoning`) → Inequality (`inequality`), direct subject chapter (no subcategory).
- Chapter ID: `f969744d-074e-4535-987d-4181b2471884`.
- Existing question count before import: 0. The separate `Inequality (Mains)` chapter was not touched.
- Local Alembic version observed read-only: `0010_banking_catalog`; no migration run.
- Scope is the local database `127.0.0.1:5432/ssc_prep` only.
