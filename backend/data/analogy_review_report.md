# Analogy Question Bank Review

## Scope and source review

Reviewed both supplied scanned lecture-slide PDFs visually: `Analogy 01_.pdf` (28 pages) and `Analogy 02_.pdf` (29 pages). Neither contains selectable text. The batch uses 21 questions transcribed from legible slides and adds 9 clearly labeled original SSC-style practice questions. PDF slides do not establish exam/year provenance; every record is a Normal question and `is_pyq=false`.

The source questions cover word relationships, number relations, letter relations, and grouped/mixed reasoning. Slide numbers in `source` refer to the page position in the corresponding PDF. Answers were independently worked from the stated relation and checked against all choices; explanations and independent derivations are recorded alongside each row in the batch and answer ledger.

## Exclusions

- `Birds : Chirp :: Bear : ?` (Analogy 01, slide 14) was excluded because both “growl” and “grunt” can reasonably describe a bear, so the displayed choices do not guarantee one uniquely correct answer.
- Other figure-reasoning slides were not transcribed because the printed figures/options plus handwritten marks do not provide a sufficiently unambiguous text-only record for this batch.
- The `China : Table Tennis :: Nepal : ?` slide was excluded because the country-to-sport association and annotations do not establish a uniquely supported answer.
- Several number/letter slides with incomplete, overwritten, or visually uncertain rules were excluded rather than reconstructed.

## Batch summary

- Total: 30 Normal questions
- Difficulty: 10 Easy, 12 Medium, 8 Hard
- Source: 21 PDF-derived, 9 original
- PYQ: 0
- All entries have four distinct options, one keyed answer, an explanation, and corresponding answer-ledger review.

## Duplicate review

No Analogy question bank records or chapter-specific batch/ledger existed at the time of preparation. The live chapter baseline was checked before import. Exact normalized stems and near-identical wording are checked against repository question batches by the focused artifact tests. Problem signatures are unique within this set; the rules and operands were also reviewed manually to avoid reusing the same underlying puzzle under different wording.

## Import gate

The importer checks the expected chapter ID and empty baseline, runs the shared importer in dry-run mode, and only writes when invoked with `--apply` after the dry-run reports exactly 30 inserts, zero duplicates, and zero errors. The live chapter was observed at 0 active Normal, 0 active PYQ, and 0 total records before the proposed import.

## Database result

- Initial state: 0 active Normal, 0 active PYQ, 0 total chapter records.
- Pre-import dry-run: 30 planned inserts, 0 duplicates, 0 rejected, 0 errors.
- Import: 30 inserted.
- Final state: 30 active Normal, 0 active PYQ, 30 total chapter records; difficulty counts are Easy 10, Medium 12, Hard 8.
- Post-import integrity check: 30 distinct stems, four option rows per question (120 total), and exactly one correct option per question.
- Idempotency replay: 30 duplicates recognized, 0 inserts planned, 0 errors; database unchanged.
