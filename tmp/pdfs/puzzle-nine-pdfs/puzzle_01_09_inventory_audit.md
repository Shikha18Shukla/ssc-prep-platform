# Puzzle PDF source inventory audit

Phase 1 only: transcription and source reconciliation. Answer solving, deduplication, and importing are not included.

- PDFs: 9
- Source pages: 105
- Inventory entries: 180
- Previously missing 24 IDs: 24 recovered from source page extracts and rendered sheets
- Rows with unresolved extraction status: 0
- Rows missing statement, five options, or directions: 0
- Stable source IDs: 180/180 unique

## Per-PDF reconciliation

- `DAY BASED PUZZLE SET-1 (Eng).pdf`: 9 pages; 20 entries; Q1–Q20 numbering complete=True; unresolved=0
- `DAY BASED PUZZLE SET-2 (Eng).pdf`: 11 pages; 20 entries; Q1–Q20 numbering complete=True; unresolved=0
- `DAY BASED PUZZLE SET-3 (Eng).pdf`: 12 pages; 20 entries; Q1–Q20 numbering complete=True; unresolved=0
- `DAY BASED PUZZLE SET-4 (Eng).pdf`: 13 pages; 20 entries; Q1–Q20 numbering complete=True; unresolved=0
- `DAY BASED PUZZLE SET-5 (Eng).pdf`: 12 pages; 20 entries; Q1–Q20 numbering complete=True; unresolved=0
- `DAY BASED PUZZLE SET-6 (Eng).pdf`: 12 pages; 20 entries; Q1–Q20 numbering complete=True; unresolved=0
- `DESIGNATION BASED PUZZLE SET-2 (Eng).pdf`: 12 pages; 20 entries; Q1–Q20 numbering complete=True; unresolved=0
- `DESIGNATION BASED PUZZLE SET-3 (Eng).pdf`: 12 pages; 20 entries; Q1–Q20 numbering complete=True; unresolved=0
- `DESIGNATION BASED PUZZLE SET-4 (Eng).pdf`: 12 pages; 20 entries; Q1–Q20 numbering complete=True; unresolved=0

## Entries needing source transcription follow-up


## Notes

- The old candidate generator's page value of 1 was discarded; physical page numbers were reconciled from page extracts and rendered source pages.
- Page spans are retained where a prompt or its options continue onto another physical page.
- The 24 previously omitted question numbers are separate source appearances; no text-based merging or deduplication was done.
- `answer_verification_status` is intentionally `not_in_scope_phase_1`.
- No database access or writes, migrations, answer-key verification, or import were performed.
