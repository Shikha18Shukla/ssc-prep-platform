# Disease Chapter Review

- Existing catalog chapter: **Disease** (`disease`), ID `79eeb111-c0df-4863-aac2-94086844f83b`, confirmed under `gk-gs/science`. No catalog changes were made.
- `Disease.pdf` pages 2–21 were inspected against page images and OCR. Five pages (4–7, 9) contain Disease questions; fourteen (2, 3, 8, 10–14, 16–21) contain Glands questions and were mapped to existing Glands (`glands`, ID `3a7d5736-5a65-434b-8c2c-0f17905bab57`); page 15 asks about the brain and remains in its previously recorded Brain & Nervous System review.
- All 20 question pages of `nutrition - science.pdf` were inspected; each contains a Disease/health question and was reviewed for this batch.
- Searches of the remaining OCR transcripts found only incidental disease mentions within questions mapped to other chapters (for example stomach acid/bacteria, bacterial cell structure, and Plasmodium reproduction). No other confidently mappable Disease question was added.
- Exam names are not visible in the reviewed source pages and were not inferred.

## Disposition by difficulty and question type

| Difficulty | Type | Verified | Needs review | Rejected | Duplicate |
|---|---|---:|---:|---:|---:|
| EASY | Ordinary | 4 | 1 | 0 | 0 |
| MEDIUM | Ordinary | 6 | 12 | 0 | 0 |
| HARD | Ordinary | 0 | 0 | 0 | 0 |
| EASY | PYQ | 0 | 0 | 0 | 0 |
| MEDIUM | PYQ | 1 | 1 | 0 | 0 |
| HARD | PYQ | 0 | 0 | 0 | 0 |

- Verified/import-ready: **11** (10 ordinary, 1 PYQ).
- Needs review: **14** (13 ordinary, 1 PYQ). Pending rows have clipped explanations or, for Nutrition p. 20, no source explanation.
- Rejected: **0**. Confirmed duplicates: **0**. Similar/related questions were compared by full stem, options, and answer rather than marked duplicate from keyword similarity alone.

## Ordinary-question coverage targets

| Difficulty | Verified ordinary | Target | Remaining |
|---|---:|---:|---:|
| EASY | 4 | 25 | 21 |
| MEDIUM | 6 | 25 | 19 |
| HARD | 0 | 25 | 25 |

PYQs are tracked separately and do not count toward the ordinary targets. Difficulty labels are internal review metadata; Science users are not asked to choose a difficulty.

## Import readiness and source traceability

Only fully verified, nonduplicate Disease records with complete source explanations are included in the ordinary/PYQ CSVs. Each row preserves source filename and physical PDF page. The PYQ CSV contains the one verified source-labeled item (Nutrition p. 19, PYQ 2022); no exam name is shown.

## Validation

Isolated importer dry-run tests validate all 11 eligible rows, assert zero inserted rows, and confirm the test database remains empty. Production database access was read-only; no production import or modification was performed.
