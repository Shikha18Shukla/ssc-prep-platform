# Calendar Chapter Review Report

## Source review

All five supplied class-note PDFs were rendered and every page was visually inspected because the PDFs contain scanned page images without selectable text. Source questions were transcribed only where the prompt, target, and intended rule were clear. A candidate was retained only when its calendar rule was not already represented by a selected question. No source slide explicitly identified a selected item as a PYQ, so all 30 records are stored as Normal (`is_pyq=false`).

| PDF | Pages | Explicit candidates reviewed | Selected | Review notes |
| --- | ---: | ---: | ---: | --- |
| Calendar 01 | 11 | 0 | 0 | Lecture material and example values; no standalone question prompt. |
| Calendar 02 | 22 | 12 | 7 | Kept one day-offset question, distinct Gregorian-year rules, first/last weekday cases, and the maximum leap-year gap. Excluded repeated remainder-zero day offsets, repeated leap/common-year classification, and other repeated concepts. |
| Calendar 03 | 12 | 5 | 1 | Five date-to-weekday examples use the same operation; kept the 26 March 1995 example only. |
| Calendar 04 (Reschedule@4) | 9 | 1 | 0 | The recap's 17 June 2006 example repeats the date-to-weekday operation; remaining pages are worked lecture examples, including inconsistent handwritten claims. |
| Calendar 05 | 14 | 7 | 1 | Kept the clear 12 February 2005 to 24 May 2017 weekday prompt. Excluded repeated weekday-offset examples and prompts with a false or unclear supplied date/weekday premise. |

The seven retained Calendar 02 items are on pages 11, 13, 15, 16, 17, 18, and 20. The two other retained items are Calendar 03 page 6 and Calendar 05 page 6. The original-source question and page provenance is recorded in the answer ledger.

## Bank summary

- 30 active Normal questions in the canonical batch; 10 Easy, 10 Medium, and 10 Hard.
- 9 PDF-derived and 21 original SSC-style questions.
- Every record has four distinct options, one keyed answer, an explanation, and `is_pyq=false` with null PYQ metadata.
- Original questions were added to meet the minimum test size for every level while covering distinct rules: year structure, odd days, weekday offsets, Gregorian century exceptions, and elapsed-day calculations.
- All displayed dates and weekday offsets were independently checked with Python's `datetime.date`/`calendar` operations and hand-checked modulo-seven arithmetic. The source-date premise in the Calendar 05 selected item is also accurate.
- Stems, rule signatures, and normalized similarity were checked within this batch and against the existing Series verified batch. The PDF candidate review also screened repeated source concepts, including examples with different dates but the same operation.

## Exclusions

- Calendar 02 page 12's “380th day since purchase” wording does not establish whether the purchase date is day one or whether 380 full days have elapsed.
- Calendar 02 pages 9 and 10 both reduce to a zero remainder modulo 7; page 11 was kept as the distinct nonzero-remainder representative.
- Calendar 02 page 14 asks for a common year and repeats page 13's leap/common-year classification.
- Calendar 02 page 19 repeats the first-day/last-day weekday rule already represented by pages 17–18.
- Calendar 05 pages 7, 8, 10, and 11 give incorrect or doubtful base date/weekday facts; they were not silently corrected. The remaining candidate prompts repeat date-offset methods already represented.
- Worked formulas, month-code tables, and examples without a distinct question prompt were recorded as instructional material, not promoted to questions.

## Import and application verification

The target is the active SSC → Reasoning → Calendar (Recorded) chapter, slug `calendar-recorded`, ID `12bc9994-13ee-4522-88c7-9a98371eb900`. Its verified pre-import state was zero question records, zero active Normal, and zero active PYQ. The guarded importer reported a clean dry-run of 30 inserts, zero rejects, duplicates, or errors. Apply inserted 30; replay reported 30 duplicates, zero new inserts, rejects, or errors. Final database verification found 30 active Normal, zero active PYQ, and no other records, with counts 10/10/10.

Authenticated live API checks confirmed the chapter appears under Reasoning with this ID; chapter availability and test availability each return 10 Easy, 10 Medium, and 10 Hard, with each 10-question request satisfiable. PYQ returns zero, so none are mixed into Normal. Mixed practice returns 30 available questions and the standard `[10, 15, 20, 25]` choices. The read-only question API returned all 30 records with four options, one correct key, and explanations. Existing catalog and test selection rules remain unchanged.

## Final re-verification — 2026-11-02

Using the verified project interpreter (`backend/.venv-disease-import`, Python 3.10.9), the live baseline was re-read before any import action: 30 active Normal, 0 active PYQ, 30 total, distributed 10/10/10. The canonical batch exactly matched those live records. Guarded dry-run reported 30 duplicates and 0 inserts, rejects, or errors. The importer's `--apply` path verified the already-complete state and returned `IDEMPOTENT_REPLAY`, with no database changes.

Focused Calendar artifact checks passed; 14 combined Calendar/Series/Clock/Importer checks passed with one Calendar API fixture test deselected (live API verification was performed directly). Fifteen catalog/session service regressions passed. Python compilation, frontend production build, and `git diff --check` passed. Live authenticated API rechecks confirmed catalog visibility, 10 available questions per difficulty, 0 PYQs, supported mixed-practice sizes `[10, 15, 20, 25]`, and all 30 question payloads with options, keys, and explanations. No browser test was performed.
