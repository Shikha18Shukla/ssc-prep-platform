# Direction and Distance (Mains) — Batch 1 audit

## Source and destination
- Source: `Direction and Distance 01  Class Notes.pdf` (10 pages; rendered source checked on question pages and the contents inventory reviewed).
- Target: Banking Clerk → Reasoning → Direction and Distance (Mains), chapter `10b96d9e-f228-4eab-990a-c5d061ae818f` (`direction-and-distance-mains`).
- Database confirmed as local `ssc_prep` at `127.0.0.1:5432`; starting count 0 active / 0 inactive.

## Question classification
- Direction/coded-road MCQs: 3 (Q1 p.4; Q2–Q3 p.8); all independently verified and included in the import JSON.
- Syllogism recap material on p.2 is wrong-chapter content and was excluded.
- Intro/cover and worked explanation pages were not counted as separate questions.
- Duplicate/existing overlap: 0.
- Held/invalid: 0 among the three Direction and Distance MCQs.

## Answers
Q1 A; Q2 A; Q3 E. The fixed intersection mapping and six operator definitions were applied to every expression. The marked answers were compared after solving; imported answers agree with the verified mappings.

## Dry-run / import
The source JSON is `direction_distance_mains_batch1_verified_import.json` (3 records). Dry-run: 3 eligible, 0 duplicate, 0 rejected, 0 errors. Transactional database write and read-back are recorded in the final batch report.

## Post-import verification
Imported IDs: Q1 `e8fa7f9e-c397-4fbb-86b8-deee509f14d9`; Q2 `fa54f268-0edf-41db-9ff6-a3cff69e579e`; Q3 `9792a22d-96f9-4568-b638-0d2c69c6da15`. Final chapter count: 3 active / 0 inactive. Replay: 3 duplicates, 0 inserts.
