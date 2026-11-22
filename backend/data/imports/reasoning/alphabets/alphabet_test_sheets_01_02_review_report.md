# Alphabet Test Sheets 01–02 — Import Review

## Scope and source integrity

The four supplied PDFs resolve to two unique source files. The two copies of Sheet 01 are byte-identical (18 pages; SHA-256 `f90cb6aa861b6782759ea3ad3d312899cd8d41177928d21e14ef46433bc31957`), as are the two copies of Sheet 02 (18 pages; SHA-256 `7d0720de4ff4d5e13126c38a68ae63a51343e407bd83e8b50d46a7d8666649a1`). The duplicate copies were excluded from reprocessing.

Each unique PDF contains 10 sets of five numbered questions: 50 appearances per PDF, 100 total. All pages were rendered and visually reviewed; extracted text was used to preserve question wording and options. The English content is retained. Extracted Hindi text was not copied because the PDF text layer rendered it unreliably; no translation was generated.

## Destination and initial state

- Banking Clerk → Reasoning → Alphabets
- Chapter ID: `b7c9305a-6af2-4a45-ae67-53eeeb63d1dd`
- Local database confirmed as `ssc_prep` on `127.0.0.1:5432`
- Initial count: 3 active, 0 inactive
- Existing records reviewed: TRIANGLE letter pairs; LAPTOP swaps; TECHNOLOGY alphabetical positions.

## Audit totals

| Classification | Count |
|---|---:|
| Verified unique import candidates | 94 |
| Duplicate question appearances within the two unique sheets | 5 |
| Held | 1 |
| Total numbered appearances | 100 |

Set 14 Q1–Q5 in Sheet 02 repeat Set 6 Q1–Q5 in Sheet 01, with the same source series and same operations/questions. Each duplicate is linked to its Set 6 canonical source in the answer ledger. No question matched the three existing chapter records.

## Held question

- Sheet 02, physical page 14, Set 19 Q1 (`RED OFF SUM HAG JIB`): replacing each vowel with A yields `RAD`, `AFF`, `SAM`, `HAG`, `JAB`. The printed key counts `SAM` as meaningful, but it is a proper name/initialism, not an unambiguous common English word. Since the question does not define whether names count, it is held rather than selecting a subjective answer.

## Printed-key comparison

- Sheet 02, physical page 12, Set 17 Q5: the printed key is C (2), while the stated vowel-next/consonant-previous transformation yields `IRG, FJQ, KFX, MFU, LYJ, VLB`. Only `MFU` contains a vowel, so the independently verified answer is B (1). The import record uses B and includes the corrected explanation.
- The held Set 19 Q1 has printed key D; it remains held for the word-validity ambiguity described above.
- All other verified candidates' independently derived answers match the printed key.

## Deduplication and import contents

The import JSON contains only the 94 verified unique questions. Each record preserves the English source prompt, shared directions and word series, all five answer options, answer, explanation, difficulty, PDF filename, physical page, sheet level, set and question number.

## Import verification

- Existing importer dry-run: 94 eligible; 0 duplicates; 0 rejected; 0 errors.
- Transactional import: 94 inserted into the target chapter.
- Final chapter count: 97 active, 0 inactive (initially 3 active, 0 inactive).
- Direct database verification: all 94 inserted records have the target chapter ID, five options, exactly one correct option, matching answer/explanation/source, and active status. The three pre-existing IDs remain present and active.
- Authenticated local API: `GET /api/questions` for the target chapter returned 97 active items; all 94 imported items matched the verified file, including options, correct flags, explanations and source attribution.
- Idempotency replay: 94 duplicates detected; 0 eligible new inserts; 0 rejected; 0 errors.
- Existing import behavior is insert-only; no pre-existing question or other chapter was updated.

The first dry-run exposed an extraction bug where numeric options were blank. No writes occurred in that attempt. The extraction was corrected, the JSON was regenerated and checked for five non-empty options per item, and the passing dry-run above was completed before the import.

## Imported source coverage

- Sheet 01 (PO Prelims): all 50 questions imported — Sets 1–10, Q1–Q5 in each set.
- Sheet 02 (Clerk Prelims): 44 questions imported — Sets 11–13 and 15–18, Q1–Q5; Set 19 Q2–Q5; Set 20 Q1–Q5.
- Sheet 02 Set 14 Q1–Q5 were excluded as duplicates of Sheet 01 Set 6 Q1–Q5.
- Sheet 02 Set 19 Q1 was held.
- The second copy of each source PDF was not reprocessed because its file hash matches the corresponding unique PDF.

## Artifacts

- `backend/data/imports/reasoning/alphabets/alphabet_test_sheets_01_02_verified.json`
- `backend/data/imports/reasoning/alphabets/alphabet_test_sheets_01_02_answer_ledger.json`
- `backend/data/imports/reasoning/alphabets/alphabet_test_sheets_01_02_review_report.md`

