# Direction and Distance (Mains) — Batch 1 completion audit

## Destination and database

- Destination: Banking Clerk → Reasoning → Direction and Distance (Mains).
- Chapter ID: `10b96d9e-f228-4eab-990a-c5d061ae818f` (`direction-and-distance-mains`).
- Local target verified as `ssc_prep` on `127.0.0.1:5432`.
- Active baseline before original top-up: 3; inactive baseline: 0.
- Final direct database count: **40 active / 0 inactive**; 40 active prompts are distinct under the importer's normalization.

## Source audit reused

- PDFs: `Direction and Distance 01  Class Notes.pdf`.
- Pages visually audited in the existing source review: 10.
- Numbered question appearances recorded for this chapter: 3; distinct source prompts: 3.
- Source dispositions: 3 verified source-derived questions were already represented in the database (including items added by the earlier Batch 1 import where applicable); 0 repeated appearance(s); 0 held; 0 wrong-chapter; 0 exercises without MCQ options.
- Findings: Three complete coded-direction MCQs were verified and imported in the preceding batch. The Syllogism recap on p.2 is wrong-topic material; no target questions were held.
- Existing question-level source ledger: `direction_distance_mains_batch1_answer_ledger.json`. Earlier source review files and renders were preserved; the source extraction was not restarted.

## Original practice top-up

- Created and imported **37** in-house questions, explicitly labeled `Original Practice Question`; none are labeled PYQ or attributed to a PDF.
- Each prompt has five distinct options, exactly one correct key, and a non-empty explanation. Puzzle sets were enumerated from their clues; table assignments were checked against the generated constraint sets.
- Pre-import dry-run: 37 eligible, 0 duplicates, 0 rejects, 0 errors.
- Isolated transactional import: 37 inserted, 0 duplicates, 0 rejects, 0 errors.
- Database read-back: all 37 matched their import records, are active and belong to the exact chapter; text, options, answer, explanation, and original-practice source label match.
- Replay dry-run: 37 duplicates, 0 proposed inserts, 0 rejects, 0 errors.
- Final chapter active target: **met**.

The complete original-question text, options, answer key, explanation, and database ID are in `direction_distance_final_answer_ledger.json` and `direction_distance_original_topup_verified.json`. Existing source-derived questions were not rewritten or deactivated.
