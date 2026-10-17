# Mathematical Operations Normal Bank Review

## Result

- Chapter: Mathematical Operations (`a9a0ce3b-9d82-401e-8ed7-c73d0110c646`), SSC → Reasoning.
- Live baseline verified before import: 0 active Normal, 0 active PYQ, 0 total chapter records.
- Proposed batch: 30 PDF-derived Normal questions; 0 original questions; 0 PYQs.
- Difficulty: 10 Easy, 12 Medium, 8 Hard.
- The PDFs identify lecture content but do not state a verifiable exam, year, or shift. Such provenance is explicitly left unstated; no item is claimed as a PYQ.

## Source review

Both supplied PDFs were visually inspected page by page. PDF 1 has 23 pages and PDF 2 has 24 pages. Question slides were read from rendered scans and calculations were independently checked using standard order of operations. The retained source pages are:

- `Mathematical Operations 01 _.pdf`: pages 7, 9, 10, 12–19, and 21 (12 questions).
- `Mathematical Operations 02_.pdf`: pages 4–21 (18 questions).

All included rows have four distinct A–D options, one keyed answer, a worked explanation, and `is_pyq=false`. The answer ledger captures the expected answer, independent calculation, option review, difficulty, source page, and a problem signature for every row.

## Exclusions

The source review yielded 34 candidate items (16 from PDF 1 and 18 from PDF 2). Four were not included:

1. PDF 1 page 6 repeats the exact underlying equation on PDF 2 page 9 (`18×14+6−16÷4=254`); PDF 2 page 9 is retained with its four-option sequence format.
2. PDF 1 page 8 includes five answer choices (including “None of these”), outside the four-option bank format.
3. PDF 1 page 11 includes five answer choices, outside the four-option bank format.
4. PDF 1 page 20 repeats the `n−n` prompt form used on page 19; page 19 is retained to avoid adding a near-repetitive item.

No exam/year provenance was visible in either source. No additional source claims were inferred.

## Verification and duplication

The arithmetic, symbol substitutions, digit encodings, equality conditions, fractions, and order-of-operations cases were independently recomputed. The full retained set was checked against itself, the available canonical batch stems, and the live chapter (which had no records at the verified baseline). The repeated equation described above was excluded. No other exact or underlying-problem duplicate was identified in the reviewed set. Semantic review was manual; automated tests also enforce normalized-stem and concept-signature uniqueness and scan other batch JSON files for exact stem collisions.

## Import plan

The importer is pinned to the chapter ID above and only permits either the verified empty baseline or an exact replay of this canonical batch. It verifies option text, answer key, explanation, source, difficulty, Normal metadata, and active state on any matching records. It performs a dry-run by default and applies only with `--apply` after confirming exactly 30 inserts, zero duplicates/rejections/errors. After an apply it checks the live rows and runs a replay dry-run requiring 30 duplicates and zero new inserts.

## Import verification

The guarded dry-run reported 30 planned inserts, 0 duplicates, 0 rejections, and 0 errors against the verified empty baseline. The importer inserted 30 records. Post-import verification found 30 active Normal questions, 0 active PYQs, and 30 total chapter records with a 10 Easy / 12 Medium / 8 Hard distribution. A replay dry-run reported 30 duplicates and 0 additional inserts, with no rejections or errors. The importer compared every live stem, option set, answer key, explanation, difficulty, source, active flag, and Normal/PYQ metadata against the canonical batch.
