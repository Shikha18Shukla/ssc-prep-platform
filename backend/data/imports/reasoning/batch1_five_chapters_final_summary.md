# Batch 1 — Five Banking Clerk Reasoning Chapters final summary

## Completion

All five target chapters now have **40 active questions each** (200 active total). This task added 156 original practice questions. The 22 PDF-derived questions from the preceding Batch 1 import remain active; 13 additional PDF-derived records from earlier imports were already present (4 Tabular Arpit questions and 9 Analytical Reasoning questions). No question or chapter was deleted, overwritten, deactivated, or recreated.

## Chapter counts

| Chapter | Starting active | PDF questions added in this completion run | Original practice questions added | Final active | Target met |
|---|---:|---:|---:|---:|---|
| Direction and Distance (Mains) | 3 | 0 (prior PDF imports remain active) | 37 | 40 active / 0 inactive | Yes |
| Triangular Arrangements | 4 | 0 (prior PDF imports remain active) | 36 | 40 active / 0 inactive | Yes |
| Alphabets (Mains) | 5 | 0 (prior PDF imports remain active) | 35 | 40 active / 0 inactive | Yes |
| Tabular Puzzles | 19 | 0 (prior PDF imports remain active) | 21 | 40 active / 0 inactive | Yes |
| Analytical Reasoning (Mains) | 13 | 0 (prior PDF imports remain active) | 27 | 40 active / 1 inactive | Yes |

## Diagnosis of the prior low additions

The previous imports used the verified unique MCQs available in the supplied PDFs; they did not stop at an arbitrary selection limit. Across the 13 source PDFs (194 pages), the existing question-level audits record 92 prompt appearances: 35 verified PDF-derived questions already represented in these chapters (22 from the previous batch plus 13 already present), 13 repeated appearances, 29 held questions, 5 questions belonging to another topic, and 10 numbered exercises without source options. The primary shortfalls were incomplete/ambiguous source material and repeated prompts, not an importer cap.

- Direction and Distance: 3 verified MCQs; Syllogism recap excluded.
- Triangular Arrangements: 4 verified unique; 1 underdetermined sports question held; 1 repeated appearance.
- Alphabets: 5 verified unique; 12 repeats; 7 held; 5 arithmetic questions assigned to the wrong chapter.
- Tabular Puzzles: 10 new verified Class Notes MCQs; 4 earlier Arpit MCQs already in the DB; 19 clue-only Arpit entries held.
- Analytical Reasoning: 9 verified MCQs already active; 2 ambiguous Decision Making MCQs held; 10 exercises lack options and were not converted into MCQs.

The exact held reasons and source-page references are in each chapter completion report and its preserved source answer ledger. All source PDFs were previously visually reviewed in the existing audit; this run reused those completed audits rather than repeating extraction.

## Local database verification

- Database identity checked before import and read-back: `ssc_prep`, host `127.0.0.1`, port `5432`.
- Every newly imported row matched its JSON and answer ledger for chapter, question text, five options, exactly one correct answer, explanation, active status, and source label.
- All active prompts are unique under the existing importer normalization.
- Previously verified PDF-derived records were checked to remain present and active.
- Replay dry-runs for all five original top-up files proposed zero new inserts and detected all records as duplicates.
- No migrations, schema/config changes, production database access, commits, or pushes were performed.

## API/browser status

Backend `/api/health` and `/api/ready` returned healthy/ready; the frontend `/banking` route returned HTTP 200. The protected `/api/exams` catalog endpoint returned HTTP 401 without a bearer session. No legitimate authenticated browser session was available in this execution, so authenticated API question-count responses and browser-rendered chapter counts were not claimed. The frontend uses the subject chapter-count endpoint and displays its per-chapter count; direct database counts are verified above. An authenticated website visibility check remains outstanding.

## Artifacts

Each target folder contains an `*_original_topup_verified.json`, an `*_original_topup_answer_ledger.json`, and an `*_batch1_completion_audit_report.md`. A consolidated `*_final_answer_ledger.json` is also present for each chapter.
