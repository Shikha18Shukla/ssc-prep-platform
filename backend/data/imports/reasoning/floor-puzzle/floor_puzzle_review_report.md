# Floor Puzzle source audit and verified import batch

Target: Banking Clerk → Reasoning → Floor Puzzle (`ea5788f0-8dd6-4d4f-8dd1-585d2ff29dcc`)

## Source reconciliation

| Source PDF | Pages | Appearances | Verified candidates | Held | Duplicate appearances |
|---|---:|---:|---:|---:|---:|
| Flat & Floor Based Puzzle 03.pdf | 1 | 45 | 32 | 13 | 0 |
| FLOOR BASED 19 PUZZLES by Arpit sir.pdf | 2 | 19 | 15 | 4 | 0 |
| Floor Based Puzzles 01.pdf | 3 | 75 | 72 | 3 | 0 |
| Floor Based Puzzles 02.pdf | 4 | 15 | 0 | 0 | 15 |
| Floor Based Puzzles 02 (1).pdf | 5 | 15 | 0 | 0 | 15 |

Total appearances: **169**.
Distinct question prompts after exact and semantic review: **139**.
Repeated exact source appearances: **30**; within-file repeats: **0**; cross-file repeats: **30**.
Existing local database overlaps: **0** (376 Banking Clerk Reasoning records reviewed; target was 0/0 before import).
Verified import candidates: **119**. Held: **20**. Pending: **0**.

The two `Floor Based Puzzles 02` files are pixel-identical and repeat Floor Based Puzzles 01 Q31–Q45. No other source repeat or semantic match was identified. The source-level and local-bank deduplication review is recorded in `tmp/pdfs/floor-puzzle-audit/floor_puzzle_deduplication.json`.

## Import validation rules

Only inventory rows classified `verified_import_candidate` are present in the JSON. Each record contains the original shared English directions (when the PDF presents a shared group), the source question prompt, five source options, the independently verified answer, the saved explanation, difficulty, and source PDF/page/group metadata. Hindi OCR was omitted where extraction was corrupted rather than guessed. The correct option was not changed to follow a printed key.

Selected questions and answers:

| Source PDF | Printed Q | Physical question page | Correct option |
|---|---:|---:|:---:|
| Flat & Floor Based Puzzle 03.pdf | 2 | 4 | B |
| Flat & Floor Based Puzzle 03.pdf | 3 | 4 | E |
| Flat & Floor Based Puzzle 03.pdf | 4 | 5 | D |
| Flat & Floor Based Puzzle 03.pdf | 6 | 9 | D |
| Flat & Floor Based Puzzle 03.pdf | 7 | 9 | A |
| Flat & Floor Based Puzzle 03.pdf | 8 | 9 | B |
| Flat & Floor Based Puzzle 03.pdf | 9 | 10 | C |
| Flat & Floor Based Puzzle 03.pdf | 10 | 10 | D |
| Flat & Floor Based Puzzle 03.pdf | 11 | 14 | A |
| Flat & Floor Based Puzzle 03.pdf | 12 | 14 | D |
| Flat & Floor Based Puzzle 03.pdf | 13 | 14 | A |
| Flat & Floor Based Puzzle 03.pdf | 14 | 15 | B |
| Flat & Floor Based Puzzle 03.pdf | 15 | 15 | C |
| Flat & Floor Based Puzzle 03.pdf | 16 | 19 | D |
| Flat & Floor Based Puzzle 03.pdf | 17 | 19 | B |
| Flat & Floor Based Puzzle 03.pdf | 18 | 19 | A |
| Flat & Floor Based Puzzle 03.pdf | 19 | 20 | E |
| Flat & Floor Based Puzzle 03.pdf | 20 | 20 | A |
| Flat & Floor Based Puzzle 03.pdf | 21 | 24 | C |
| Flat & Floor Based Puzzle 03.pdf | 22 | 24 | E |
| Flat & Floor Based Puzzle 03.pdf | 23 | 24 | B |
| Flat & Floor Based Puzzle 03.pdf | 24 | 25 | A |
| Flat & Floor Based Puzzle 03.pdf | 25 | 25 | D |
| Flat & Floor Based Puzzle 03.pdf | 31 | 34 | E |
| Flat & Floor Based Puzzle 03.pdf | 32 | 34 | D |
| Flat & Floor Based Puzzle 03.pdf | 33 | 34 | C |
| Flat & Floor Based Puzzle 03.pdf | 34 | 35 | B |
| Flat & Floor Based Puzzle 03.pdf | 35 | 35 | A |
| Flat & Floor Based Puzzle 03.pdf | 36 | 39 | C |
| Flat & Floor Based Puzzle 03.pdf | 37 | 39 | A |
| Flat & Floor Based Puzzle 03.pdf | 39 | 40 | D |
| Flat & Floor Based Puzzle 03.pdf | 40 | 40 | B |
| FLOOR BASED 19 PUZZLES by Arpit sir.pdf | 2 | 4 | B |
| FLOOR BASED 19 PUZZLES by Arpit sir.pdf | 3 | 4 | E |
| FLOOR BASED 19 PUZZLES by Arpit sir.pdf | 4 | 5 | E |
| FLOOR BASED 19 PUZZLES by Arpit sir.pdf | 5 | 6 | E |
| FLOOR BASED 19 PUZZLES by Arpit sir.pdf | 6 | 6 | B |
| FLOOR BASED 19 PUZZLES by Arpit sir.pdf | 7 | 6 | B |
| FLOOR BASED 19 PUZZLES by Arpit sir.pdf | 8 | 7 | E |
| FLOOR BASED 19 PUZZLES by Arpit sir.pdf | 9 | 7 | B |
| FLOOR BASED 19 PUZZLES by Arpit sir.pdf | 10 | 8 | D |
| FLOOR BASED 19 PUZZLES by Arpit sir.pdf | 11 | 8 | E |
| FLOOR BASED 19 PUZZLES by Arpit sir.pdf | 12 | 9 | C |
| FLOOR BASED 19 PUZZLES by Arpit sir.pdf | 16 | 11 | E |
| FLOOR BASED 19 PUZZLES by Arpit sir.pdf | 17 | 12 | A |
| FLOOR BASED 19 PUZZLES by Arpit sir.pdf | 18 | 12 | E |
| FLOOR BASED 19 PUZZLES by Arpit sir.pdf | 19 | 13 | A |
| Floor Based Puzzles 01.pdf | 1 | 4 | D |
| Floor Based Puzzles 01.pdf | 2 | 4 | B |
| Floor Based Puzzles 01.pdf | 3 | 4 | E |
| Floor Based Puzzles 01.pdf | 4 | 4 | D |
| Floor Based Puzzles 01.pdf | 5 | 4 | A |
| Floor Based Puzzles 01.pdf | 6 | 8 | A |
| Floor Based Puzzles 01.pdf | 7 | 8 | E |
| Floor Based Puzzles 01.pdf | 8 | 8 | D |
| Floor Based Puzzles 01.pdf | 9 | 8 | B |
| Floor Based Puzzles 01.pdf | 12 | 12 | B |
| Floor Based Puzzles 01.pdf | 13 | 12 | E |
| Floor Based Puzzles 01.pdf | 14 | 12 | A |
| Floor Based Puzzles 01.pdf | 15 | 12 | D |
| Floor Based Puzzles 01.pdf | 16 | 16 | B |
| Floor Based Puzzles 01.pdf | 17 | 16 | D |
| Floor Based Puzzles 01.pdf | 18 | 16 | C |
| Floor Based Puzzles 01.pdf | 19 | 16 | A |
| Floor Based Puzzles 01.pdf | 20 | 16 | E |
| Floor Based Puzzles 01.pdf | 21 | 20 | D |
| Floor Based Puzzles 01.pdf | 22 | 20 | B |
| Floor Based Puzzles 01.pdf | 23 | 20 | B |
| Floor Based Puzzles 01.pdf | 24 | 20 | D |
| Floor Based Puzzles 01.pdf | 26 | 24 | E |
| Floor Based Puzzles 01.pdf | 27 | 24 | B |
| Floor Based Puzzles 01.pdf | 28 | 24 | D |
| Floor Based Puzzles 01.pdf | 29 | 24 | C |
| Floor Based Puzzles 01.pdf | 30 | 24 | E |
| Floor Based Puzzles 01.pdf | 1 | 28 | D |
| Floor Based Puzzles 01.pdf | 2 | 28 | C |
| Floor Based Puzzles 01.pdf | 3 | 28 | D |
| Floor Based Puzzles 01.pdf | 4 | 28 | C |
| Floor Based Puzzles 01.pdf | 5 | 28 | E |
| Floor Based Puzzles 01.pdf | 6 | 32 | B |
| Floor Based Puzzles 01.pdf | 7 | 32 | C |
| Floor Based Puzzles 01.pdf | 8 | 32 | E |
| Floor Based Puzzles 01.pdf | 9 | 32 | D |
| Floor Based Puzzles 01.pdf | 10 | 32 | A |
| Floor Based Puzzles 01.pdf | 11 | 36 | C |
| Floor Based Puzzles 01.pdf | 12 | 36 | B |
| Floor Based Puzzles 01.pdf | 13 | 36 | D |
| Floor Based Puzzles 01.pdf | 14 | 36 | A |
| Floor Based Puzzles 01.pdf | 15 | 36 | C |
| Floor Based Puzzles 01.pdf | 16 | 40 | E |
| Floor Based Puzzles 01.pdf | 17 | 40 | E |
| Floor Based Puzzles 01.pdf | 18 | 40 | E |
| Floor Based Puzzles 01.pdf | 19 | 40 | A |
| Floor Based Puzzles 01.pdf | 20 | 40 | A |
| Floor Based Puzzles 01.pdf | 21 | 44 | C |
| Floor Based Puzzles 01.pdf | 22 | 44 | E |
| Floor Based Puzzles 01.pdf | 23 | 44 | B |
| Floor Based Puzzles 01.pdf | 24 | 44 | D |
| Floor Based Puzzles 01.pdf | 25 | 44 | A |
| Floor Based Puzzles 01.pdf | 26 | 48 | D |
| Floor Based Puzzles 01.pdf | 27 | 48 | D |
| Floor Based Puzzles 01.pdf | 28 | 48 | B |
| Floor Based Puzzles 01.pdf | 29 | 48 | A |
| Floor Based Puzzles 01.pdf | 30 | 48 | E |
| Floor Based Puzzles 01.pdf | 31 | 52 | E |
| Floor Based Puzzles 01.pdf | 32 | 52 | D |
| Floor Based Puzzles 01.pdf | 33 | 52 | B |
| Floor Based Puzzles 01.pdf | 34 | 52 | D |
| Floor Based Puzzles 01.pdf | 35 | 52 | A |
| Floor Based Puzzles 01.pdf | 36 | 56 | B |
| Floor Based Puzzles 01.pdf | 37 | 56 | C |
| Floor Based Puzzles 01.pdf | 38 | 56 | A |
| Floor Based Puzzles 01.pdf | 39 | 56 | D |
| Floor Based Puzzles 01.pdf | 40 | 56 | E |
| Floor Based Puzzles 01.pdf | 41 | 60 | B |
| Floor Based Puzzles 01.pdf | 42 | 60 | A |
| Floor Based Puzzles 01.pdf | 43 | 60 | B |
| Floor Based Puzzles 01.pdf | 44 | 60 | B |
| Floor Based Puzzles 01.pdf | 45 | 60 | C |

## Held questions

Held items are excluded from the import JSON. Reasons are preserved verbatim from the audit inventory.

| Source PDF | Physical pages | Q | Reason held |
|---|---|---:|---|
| Flat & Floor Based Puzzle 03.pdf | 2-6 | 1 | Written clues place M on floor 3, but M is absent from the options; printed solution table/key instead puts G there. |
| Flat & Floor Based Puzzle 03.pdf | 2-6 | 5 | Under the unique arrangement from written clues, both options A and B are true; source key marks A, so the MCQ lacks exactly one correct option. |
| Flat & Floor Based Puzzle 03.pdf | 27-31 | 26 | Exhaustive search found six arrangements satisfying the written clues; this question’s answer is not invariant. |
| Flat & Floor Based Puzzle 03.pdf | 27-31 | 27 | Exhaustive search found six arrangements satisfying the written clues; this question’s answer is not invariant. |
| Flat & Floor Based Puzzle 03.pdf | 27-31 | 28 | Exhaustive search found six arrangements satisfying the written clues; this question’s answer is not invariant. |
| Flat & Floor Based Puzzle 03.pdf | 27-31 | 29 | Six clue-satisfying arrangements remain; additionally the source does not define whether both floor and lift assignments change when E and B swap designated floors. |
| Flat & Floor Based Puzzle 03.pdf | 27-31 | 30 | Exhaustive search found six arrangements satisfying the written clues; this question’s answer is not invariant. |
| Flat & Floor Based Puzzle 03.pdf | 37-41 | 38 | Two arrangements satisfy the clues and the odd-one-out answer changes. |
| Flat & Floor Based Puzzle 03.pdf | 42-46 | 41 | Ten valid arrangements remain; the person immediately below the Muskmelon occupant is not invariant (sometimes F, sometimes another person not represented by a specific fruit option). |
| Flat & Floor Based Puzzle 03.pdf | 42-46 | 42 | Ten valid arrangements remain; the occupant immediately below B varies and can be absent or have different fruit assignments. |
| Flat & Floor Based Puzzle 03.pdf | 42-46 | 43 | C’s fruit and floor/flat vary across valid arrangements, changing which listed statement combination is true. |
| Flat & Floor Based Puzzle 03.pdf | 42-46 | 44 | The odd pairing among A–Litchi, G–Peach, F–Pineapple, C–Pear, E–Cherry is not invariant across the valid arrangements; the printed key cannot select a unique outlier. |
| Flat & Floor Based Puzzle 03.pdf | 42-46 | 45 | The listed people in Flat P vary across valid arrangements. |
| FLOOR BASED 19 PUZZLES by Arpit sir.pdf | 4 | 1 | The school location/floor is not specified; going three floors down does not determine Raman’s floor or Rakesh’s floor. |
| FLOOR BASED 19 PUZZLES by Arpit sir.pdf | 9-10 | 13 | Two valid arrangements satisfy all written clues and the truth of option B changes; in one arrangement none of A–D is true. |
| FLOOR BASED 19 PUZZLES by Arpit sir.pdf | 10 | 14 | Two valid arrangements remain; both option C (U below H) and option E (M on floor 6) are false, so the MCQ has multiple correct responses. |
| FLOOR BASED 19 PUZZLES by Arpit sir.pdf | 11 | 15 | The unique arrangement makes both option A (B on an even floor) and option C (G above H) true. |
| Floor Based Puzzles 01.pdf | 6-9 | 10 | The source repeats the correct combination D, H, X as both option B and option D. The arrangement is clear, but two option labels are correct, violating the single-correct-option requirement. |
| Floor Based Puzzles 01.pdf | 10-13 | 11 | The arrangement is unique, but the odd-one-out criterion is not coherent from the listed descriptions: under the natural “two persons below H” reading the options identify T, L, M, T, X; under a two-person-gap reading they identify T, M, M, T, X. Neither supports a unique four-item similarity, and the printed key C is not independently justified. |
| Floor Based Puzzles 01.pdf | 18-21 | 25 | Option C refers to H, but H is not among the seven people listed in the puzzle. The statement cannot be evaluated as written; it is held despite the printed key selecting A. |

## Database safety

The import destination is the existing direct Reasoning chapter, with no subcategory. Fresh read-only verification confirmed local host `127.0.0.1`, port `5432`, database `ssc_prep`, chapter ID above, and 0 active / 0 inactive before import. No migration or database write has been performed at this checkpoint.


## Post-import source correction requiring database authorization

A cross-check against the original pages 2–6 of `Flat & Floor Based Puzzle 03.pdf` found that the saved group-01 solver result had been associated with an unrelated seven-floor arrangement. The actual source is a five-storey/two-flat puzzle. Exhaustive placement over its ten floor-flat cells yields one arrangement: floor 5 P=D/Q=R; floor 4 P=T/Q=C; floor 3 P=A/Q=E; floor 2 P=Q(person)/Q-flat=S; floor 1 P=F/Q-flat=B. The verified answers for Q1–Q5 are B, C, C, C, D, matching the source key. All five are now classified as verified candidates, superseding the earlier Q1/Q5 holds.

The earlier import inserted Q2=B, Q3=E and Q4=D. Those three stored answer labels are wrong; the correct labels are C, C and C. The import omitted verified Q1=B and Q5=D. Existing question records were not changed after this discovery. The earlier 119-row authenticated API check only confirmed structural consistency with the stale import file; it does not establish answer correctness for Q2–Q4. The completed import therefore needs a narrowly scoped repair before it can be reported as fully correct.


## Authorized repair completed

The user approved repairing only the three rows created by the earlier Floor Puzzle import and adding the two omitted questions. A local-only dry-run of the corrected 121-row JSON reported 119 duplicates, 2 eligible additions, 0 rejected and 0 errors. The established importer then inserted Q1 and Q5 while the same SQLAlchemy transaction corrected the answer flags and explanations for Q2–Q4. Correct answers for Q1–Q5 are B, C, C, C, D.

The target chapter now has 121 active and 0 inactive questions. All 121 rows match the verified import JSON for question text, five A–E options, exactly one correct option, explanation, source metadata and target chapter. Importer replay reports 121 duplicates and 0 new records. An authenticated read-only API check returned HTTP 200 for `/api/auth/me` and `/api/questions`, with all 121 active records verified. The API check used an ephemeral local-only JWT for an existing active admin and a temporary backend pinned to local `ssc_prep`; that backend was stopped after the check. A before/after snapshot confirms all rows outside the target chapter are unchanged. No migration was run.
