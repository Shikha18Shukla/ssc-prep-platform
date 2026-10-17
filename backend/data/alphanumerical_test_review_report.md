# Alphanumerical Test Question Bank Review

## Scope and source review

- `Alphanumerical test 01_.pdf`: 22 pages, visually reviewed. Twelve complete MCQ prompts were selected from pages 8–19.
- `Alphanumerical test 02_.pdf`: 21 pages, visually reviewed. Thirteen complete MCQ prompts were selected from pages 4–16.
- The PDFs are image-only; embedded text extraction returned no selectable text. Question wording and options were transcribed from rendered page images.
- The PDFs are instructional lecture slides. No exam/year provenance is stated or claimed; all PDF-derived items are Normal questions with `is_pyq=false` and null PYQ metadata.
- One question-like notation on PDF 02 page 17 (`L10, L3, R4, R5, L2 → ?`) was excluded because the slide does not state a complete transformation rule or give answer options. Other recap, worked-note, and closing slides are not complete MCQs.

## Included records and independent checks

| Origin | Included | Difficulty | Verification |
|---|---:|---|---|
| PDF 01 | 12 | 4 Easy, 8 Medium, 0 Hard | Each arrangement, index operation, count, or arithmetic result independently recomputed from the visible sequence. |
| PDF 02 | 13 | 6 Easy, 4 Medium, 3 Hard | Digit swaps, word positions, vowel removal, alphabet indexing, and the chained alphabet-position question independently recomputed. |
| Original practice | 5 | 0 Easy, 0 Medium, 5 Hard | Independently solved original sequence, conversion, and adjacency-rule questions; no official source attribution. |
| **Total** | **30** | **10 Easy, 12 Medium, 8 Hard** | Four distinct A–D options and one keyed correct answer per record. |

The chained PDF 02 page 16 item was interpreted in the order shown by the slide’s worked marks: start at the 15th letter from the right (L), move 4 right (P), 6 left (J), 7 right (Q), then 3 left (N). The options are G, K, F, and “None of these”; N is not listed, so “None of these” is correct.

## Duplicate and catalog review

- Exact/near-verbatim duplicate checks within the 30 stems passed.
- Exact stem comparison against 95 existing JSON artifacts under `backend/data/` found no match.
- The live chapter had no pre-existing questions at the verified baseline. The database importer checks for existing normalized stems and refuses conflicting records.
- Semantic review compared the underlying displayed sequences, operands, and operations. The selected PDF items retain their source arrangements; the five original items use different constructions. The two original paired-term questions have distinct numeric and letter progressions and distinct solutions.

## Database and import

- Chapter: `Alphanumerical Test`, `d6e05bdf-64ee-4e28-9994-ee8649702c9c` (`reasoning/alphanumerical-test`, direct chapter).
- Verified initial live counts: 0 active Normal, 0 active PYQ, 0 total chapter records.
- Dry-run: 30 planned inserts; 0 duplicates, 0 rejected, 0 errors; no changes made during dry-run.
- Import: 30 inserted; 0 duplicates, 0 rejected, 0 errors.
- Post-import verification: 30 active Normal, 0 active PYQ, 30 total records. Question text, explanation, difficulty, source, active/PYQ metadata, four option rows, distinct option text, and exactly one correct key were checked against the canonical batch.
- Idempotency replay: 0 planned inserts; all 30 existing records matched the canonical content and option metadata.

## Validation

- Focused artifact tests: 4 passed.
- Focused artifact validation: `python -m pytest tests/test_alphanumerical_test_verified_batch.py -q` — 4 passed.
- `git diff --check` — passed; Git emitted only line-ending conversion warnings for three pre-existing unrelated modified files.
