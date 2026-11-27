# Tabular Puzzles — Class Notes and prior Arpit source audit

## Source coverage and destination
- `20 TABULAR PUZZLE by Arpit sir.pdf` — 20 pages; the prior audit found Q1–Q4 MCQs already imported and Q5–Q23 clue-only entries without individual options (held, not converted into questions).
- `Tabular Puzzles 01 _ Class Notes.pdf` — 19 pages; four MCQs, Q1–Q4, independently solved and verified.
- `Tabular Puzzles 02  Class Notes.pdf` — 19 pages; four MCQs, Q1–Q4, independently solved; Q3 has 12 valid full assignments but its odd pair is invariant.
- `Tabular Puzzles 03  Class Notes.pdf` — 11 pages; two MCQs, Q1–Q2, independently verified. The source question uses “height Peach”; interpreted as the visible “who bought Peach” prompt, with no change to its requested answer.
- Target `f00ab2eb-5830-4425-8dc9-c2b3efe96863` (`tabular-puzzles`); initial count 9 active / 0 inactive.

## Classification and answers
Ten new source MCQs are verified and unique; no exact/semantic duplicates against the existing nine target questions or among these ten. Tabular 01 Q1–Q4 answers: C, D, E, E. Tabular 02 Q1–Q4: C, B, E, C. Tabular 03 Q1–Q2: D, C. Solver enumeration was used for the wage, exam, ring, city/movie, shirt/car and fruit/weight groups; the resulting mappings and answer explanations are in the ledger.

The Arpit Q1–Q4 already in the database are retained and not re-imported. Q5–Q23 of that source remain held as clue-only items without an individual MCQ prompt/options. Recap/solution slides were not counted as additional questions. The Year-Based recap section was not assigned to Tabular Puzzles.

## Dry-run / import
`tabular_puzzles_01_03_batch1_verified_import.json` has 10 records. Dry-run: 10 eligible, 0 duplicates, 0 rejected, 0 errors. Transactional write and database read-back are recorded in the final batch report.

## Post-import verification
Initial 9 active / 0 inactive; imported 10; final 19 active / 0 inactive. New IDs: Set 01 Q1 `f3a1cfd8-a282-4437-92f0-685c0f1643ee`, Q2 `9713df19-b76c-4a5d-89b1-265a2447e156`, Q3 `6f5e63c7-229f-4041-be7b-1ff1c1f8599b`, Q4 `67f5bc9a-3be4-4b69-b87d-ed3703a4a84d`; Set 02 Q1 `bb0a6e7a-9751-40f2-88d0-af331c2dce18`, Q2 `2c3863da-0192-456b-b529-c85692432c49`, Q3 `564dc8ba-78ab-46ba-a56a-6eb69eeaca8e`, Q4 `db36fdc2-1649-4d0b-98ee-634f765b38be`; Set 03 Q1 `c1475696-6611-4aae-be17-51384481fbdf`, Q2 `f6acb3d4-942b-4450-87be-5555e65334a1`. Replay: 10 duplicates, 0 inserts.
