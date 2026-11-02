# Series question bank review

## Scope and source review

All three supplied PDFs were inspected page by page. They are scanned slide images without a selectable text layer, so the questions and page references were checked visually against the rendered pages. Page numbers below are the physical PDF page indices.

| Source | Pages | Standalone question prompts identified | Selected valid unique questions | Excluded candidates |
|---|---:|---:|---:|---:|
| Series 01_ Class Notes.pdf | 26 | 12 | 6 | 6 |
| Series 02_ Class Notes.pdf | 23 | 18 | 12 | 6 |
| Series 03_ Class Notes.pdf | 23 | 19 | 9 | 10 |
| **Total** | **72** | **49** | **27** | **22** |

“Prompts identified” counts standalone question/example prompts, not every instructional illustration or pattern demonstration on a slide. Five original questions are now in the batch: three from initial preparation and two Hard gap-fill questions added after the first import. All selected PDF questions are Normal practice items; the slides do not explicitly label any selected item as a PYQ.

## Candidate decisions

| Source | Selected page references | Exclusions |
|---|---|---|
| Series 01 | 13, 15, 19, 20, 21, 22 | p10 prime-trap item duplicates the prime validation on Series 02 p10; p16 descending consecutive multipliers and p24 factorial pattern overlap other selected product/factorial patterns; p17 and p18 use the same repeated “multiply by n then add 1” construction as p13; p23 is an interleaved arithmetic progression near p22. |
| Series 02 | 4, 5, 6, 9, 10, 11, 12, 13, 15, 16, 17, 19 | p7 progressive multipliers overlap the factorial-style progression on Series 03 p6; p8 is a second consecutive-prime bracket check near p10; p14 is a data-table interpretation item rather than a Series question; p18's Fibonacci/doubling continuation is ambiguous; p20's digit-reversal sequence is ambiguous and overlaps the reversal concept on p12; p21's factorial ratio progression overlaps the factorial/product group. |
| Series 03 | 3 (third example only), 6, 10, 11, 12, 13, 15, 18, 21 | p3 first example duplicates a square-plus-one wrong-term rule and its second example overlaps a selected cube-offset rule; p7 square-plus-one overlaps Series 02 p9; p8-p9 progressive multipliers overlap p6; p14 Fibonacci overlaps Series 02 p17; p16 geometric ratio overlaps Series 01 p19; p17 and p20 growing-difference series overlap p15; p19 constant arithmetic progression overlaps p13. |

Exclusion totals across the three sources: **19 near-duplicate/repeated-pattern candidates**, **1 out-of-scope table question**, and **2 ambiguous or underdetermined candidates**. No selected prompt was silently rewritten to change its underlying task. The PDF's Series 02 p6 did not provide four choices; four distinct options were added and independently checked. Series 03 p3's selected third example also lacked options; four distinct choices were added. Other source choices were retained and mapped to A-D in their displayed order.

## Final batch checks

- **32 total questions:** 27 PDF-derived and 5 clearly labeled originals.
- **Difficulty:** 10 Easy, 12 Medium, 10 Hard.
- **Metadata:** every question is `subject_slug=reasoning`, `chapter_slug=series`, `is_pyq=false`, and has null PYQ year/exam metadata.
- **Options and keys:** each item has four distinct A-D options and one keyed answer; each explanation states the rule and calculation or correction.
- **Provenance:** PDF-derived ledger rows carry the exact source PDF and physical page; originals carry no artificial PDF or page reference.
- **Answers:** all selected items were independently solved; choices and alternate plausible continuations were reviewed. The two additional Hard items use (1) the recurrence `aₙ=2aₙ₋₁+aₙ₋₂`, yielding 70, and (2) first differences 1,3,9,27, yielding 124. Their patterns and stems were compared against every prior Series item; neither repeats a selected recurrence or difference rule. The ledger records reasoning, options, validation, and duplicate decisions for each row.
- **Existing question banks:** exact stem and high-similarity checks are included in the focused artifact test against top-level canonical data batches. Semantic repeated-rule screening is documented above and in each ledger row. The import append guard verifies all 30 pre-existing live records against the canonical batch before permitting two inserts.

## Incremental import and verification

The active SSC → Reasoning → Series record was verified as `782b2b35-1c76-47e6-9e26-73ed87f6b6bb`. The known pre-append baseline was 30 active Normal, 0 PYQ. The importer is restricted to that exact 30-row canonical baseline or an already-completed exact 32-row replay; it refuses an empty, partial, or unrelated bank. It checks the active chapter ID, compares every existing row's stem, answer, options, explanation, metadata, and provenance, then requires a dry-run with 30 expected duplicates and exactly 2 inserts before applying. After application it verifies 32 active Normal, 0 PYQ, then requires replay dry-run to return 32 duplicates and 0 inserts.

**Append verification result:** dry-run reported 30 duplicates, 2 would-import, 0 rejected, 0 errors. Apply imported exactly 2, with 30 expected duplicates and 0 rejected/errors. Post-import verification found 32 active Normal, 0 PYQ, and the 10/12/10 difficulty split. Replay dry-run reported 32 duplicates, 0 new inserts, 0 rejected/errors. Live database rows were compared against all 32 canonical rows, including each question's options, correct key, explanation, difficulty, and source. The Hard test availability API now returns 10 available and accepts a requested 10-question test.

From the repository root, run:

```powershell
python backend/scripts/import_series_verified_batch.py
python backend/scripts/import_series_verified_batch.py --apply
```

The first command performs the guarded dry-run. Apply only if it reports chapter ID `782b2b35-1c76-47e6-9e26-73ed87f6b6bb`, the verified 30-row baseline, zero errors/rejections, 30 expected duplicates, and exactly 2 rows to insert. After apply, the script verifies final counts and performs replay dry-run. It intentionally blocks on any unexpected or partial baseline.
