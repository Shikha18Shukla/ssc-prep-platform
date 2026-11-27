# Tabular Puzzles — Batch 1 completion audit

## Destination and database

- Destination: Banking Clerk → Reasoning → Tabular Puzzles.
- Chapter ID: `f00ab2eb-5830-4425-8dc9-c2b3efe96863` (`tabular-puzzles`).
- Local target verified as `ssc_prep` on `127.0.0.1:5432`.
- Active baseline before original top-up: 19; inactive baseline: 0.
- Final direct database count: **40 active / 0 inactive**; 40 active prompts are distinct under the importer's normalization.

## Source audit reused

- PDFs: `20 TABULAR PUZZLE by Arpit sir.pdf`, `Tabular Puzzles 01 _ Class Notes.pdf`, `Tabular Puzzles 02  Class Notes.pdf`, `Tabular Puzzles 03  Class Notes.pdf`.
- Pages visually audited in the existing source review: 69.
- Numbered question appearances recorded for this chapter: 33; distinct source prompts: 33.
- Source dispositions: 10 verified source-derived questions were already represented in the database (including items added by the earlier Batch 1 import where applicable); 0 repeated appearance(s); 19 held; 0 wrong-chapter; 0 exercises without MCQ options.
- Findings: Ten Class Notes MCQs were verified and imported in the preceding batch. Four Arpit Q1–Q4 records were already present and verified; Arpit Q5–Q23 remain held because they are clue-only items without individual MCQ options. Year-Based recap content was not forced into this chapter.
- Existing question-level source ledger: `tabular_puzzles_01_03_batch1_answer_ledger.json`. Earlier source review files and renders were preserved; the source extraction was not restarted.

## Original practice top-up

- Created and imported **21** in-house questions, explicitly labeled `Original Practice Question`; none are labeled PYQ or attributed to a PDF.
- Each prompt has five distinct options, exactly one correct key, and a non-empty explanation. Puzzle sets were enumerated from their clues; table assignments were checked against the generated constraint sets.
- Pre-import dry-run: 21 eligible, 0 duplicates, 0 rejects, 0 errors.
- Isolated transactional import: 21 inserted, 0 duplicates, 0 rejects, 0 errors.
- Database read-back: all 21 matched their import records, are active and belong to the exact chapter; text, options, answer, explanation, and original-practice source label match.
- Replay dry-run: 21 duplicates, 0 proposed inserts, 0 rejects, 0 errors.
- Final chapter active target: **met**.

The complete original-question text, options, answer key, explanation, and database ID are in `tabular_puzzles_final_answer_ledger.json` and `tabular_puzzles_original_topup_verified.json`. Existing source-derived questions were not rewritten or deactivated.
