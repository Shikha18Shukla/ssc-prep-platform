# Tissues chapter review report

Review date: 2026-10-10

## Catalog mapping

The active database catalog contains `gk-gs` → `Science` → `Tissues`, slug `tissues`, chapter UUID `223afb7a-d83c-4e12-ba7d-ff3137575099`. The importer uses the stable subject/category/chapter slugs; the chapter UUID is recorded in the review dataset for provenance. The reviewed source is `animal kingdom.pdf`; mapping was made from question content, not the filename.

## Candidate pages and status

All 17 candidate pages (PDF pages 2–7 and 11–21) were rendered and checked visually against the raw OCR transcript. All ask about plant tissues or tissue-level organization. Each record preserves the source PDF name and physical PDF page number.

| Status | Count | Notes |
|---|---:|---|
| Verified | 8 | Complete visible question, four options, marked answer, explanation, and explicit metadata checked |
| Needs review | 9 | Explanation clipped or inconsistent; excluded from import files |
| Rejected | 0 | No candidate was from an unrelated topic |
| Confirmed duplicates | 0 | No exact or near duplicate confirmed |

Verified pages: 2, 4, 6, 7, 11, 15, 16, 21. Needs review: 3, 5, 12, 13, 14, 17, 18, 19, 20. Pages needing review remain in the review CSV with their available transcription and a reason; none are in the import-ready CSVs.

## Difficulty and PYQ coverage

Among verified rows: Easy 6, Medium 2, Hard 0. Explicit PYQs: 2 (2022 and 2017); ordinary questions with no PYQ label: 6. No exam names appear in the source. The nine pending rows include 1 Easy and 8 Medium; none are labelled Hard. Four of those pending rows have explicit PYQ labels (2018, 2022, 2021, 2022), and the other five show no PYQ label. There is no defined per-difficulty or PYQ target in the catalog/importer. If using a 25-question batch target, the current verified batch is 17 short overall; no difficulty mix is invented to fill that gap.

## Duplicate review

A read-only transaction inspected the active question bank (33 active questions) and confirmed the Tissues chapter catalog identity; it was rolled back without writes. No exact or near duplicate at similarity ≥0.88 matched any of the 17 stems. The candidates were also compared against all 452 OCR queue stems and the previously reviewed import batches. One low textual similarity candidate (page 14 versus `Tissues.pdf`, page 5; 0.813) is not a duplicate: the other item asks about a solid, while page 14 asks about permanent plant tissue. No pair was counted as duplicate without a content match. The existing global duplicate review still has 14 unconfirmed pairs unrelated to these candidates.

## Dry-run results

The existing importer was invoked with `dry_run=True` for the separate PYQ and ordinary CSVs. The expected results are 2 and 6 would-import records, respectively; 0 imported, 0 rejected, 0 duplicates, no errors, and no persisted rows. The focused backend tests assert those outcomes and the in-memory question count remains zero.

No production records were imported or modified.
