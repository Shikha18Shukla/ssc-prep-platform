# Direction and Distance PDF inventory and import audit

Target: Banking → Clerk → Reasoning → Direction and Distance  
Chapter ID: `8e72d063-3c61-4885-b9cb-73dac1655e30`  
Database: local `ssc_prep` at `127.0.0.1:5432`; Alembic revision `0010_banking_catalog`.

## Complete question inventory

The inventory is based on visual inspection of every page. Worked solutions and route diagrams for the same prompt are not counted as new questions.

| Lecture | Question pages and prompts | Occurrences |
|---|---|---:|
| 01 | p. 7 (1), p. 10 (1), p. 13 (1) | 3 |
| 02 | p. 4 (1), p. 7 (3), p. 10 (3), p. 13 (2), p. 16 (3) | 12 |
| 03 | p. 4 (3), p. 7 (1), p. 10 (1), p. 12 (1), p. 14 (2), p. 16 (3), p. 20 (3) | 14 |
| **Total** |  | **29** |

Lecture 03 page 20 repeats the three-question F/K/V/P/C/T/A/Q scenario from Lecture 02 page 16. There are **26 unique questions** across the PDFs.

The old audit missed Lecture 02 page 10, which contains three distinct questions. Those were independently solved against the route and worked diagram and imported. The Ayush question on Lecture 02 page 10 previously described as a repeat is not on that page; it occurs only on Lecture 01 page 10.

## Reconciliation and disposition

- Already in the target chapter before this continuation: 21 active questions, 0 inactive.
- Newly imported from Lecture 02 page 10: 3.
- Repeated occurrences skipped: 3 (Lecture 03 page 20 repeats Lecture 02 page 16).
- Unique questions held: 2.
  - Lecture 02 page 7, second prompt (P with respect to A): A's position is only constrained to be west of Z and north of R. Different allowed positions give different directions from A to P, so no unique answer can be established.
  - Lecture 03 page 14, first prompt: Abhay's stated route ends at R, but the question asks about meeting at Q. The annotated answer conflicts with the described endpoints; do not infer a correction.
- Final database count: 24 active, 0 inactive. The source set has 2 held unique questions and 3 repeated occurrences; no further unique source question remains unaccounted for.

## Page 10 additions

All three new records contain the original English scenario, a Hindi transcription of the scenario statements, all five original options, the verified answer, an explanation, and lecture/page metadata. The question prompts on the source slide are in English.

## Existing-record limitations found during re-audit

Three pre-existing records for the F/K/V/P/C/T/A/Q scenario incorrectly cited Lecture 02 PDF page 15; visual inspection locates that question slide on page 16, repeated on Lecture 03 page 20. I corrected only the `source` metadata on those three local DB rows and in the original import JSON. Their IDs, question text, options, answers, explanations, and active status were not changed.

The original 21 records contain English question text only, although Hindi source text is present on some source pages. They were not rewritten because the instruction was to preserve the 21 existing questions. The three new records include a verified Hindi transcription of their shared scenario statements.

## Validation

- Dry-run for page 10 addendum: 3 eligible, 0 duplicates, 0 rejected, 0 validation errors.
- Transactional import: 3 inserted, 0 duplicates, 0 rejected.
- Final DB integrity: 24 records; all active; each has 4 or 5 non-empty options, exactly one correct option, and an explanation.
- Replay of original import file: all 21 detected as duplicates, none would import.
- Replay of page 10 addendum: all 3 detected as duplicates, none would import.
- Authenticated local API: HTTP 200, all 24 returned with options, answer flags, explanations, and source metadata.
- Backend tests: `test_banking_clerk_pdf_import.py` and `test_direction_distance_verified_batch.py`, 5 passed.
- Frontend production build: passed.
- No migrations run. No existing question content or other chapter was changed; only three source metadata fields were corrected.
