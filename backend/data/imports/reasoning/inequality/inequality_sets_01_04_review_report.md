# Inequality Sets 1–4: Verified Import Review

## Source inventory

| Source PDF | Pages | Question appearances | Distinct prompts | Within-PDF repeats |
|---|---:|---:|---:|---:|
| INEQUALITY SET-1 (Eng).pdf | 8 | 20 | 20 | 0 |
| INEQUALITY SET-2 (Eng).pdf | 10 | 20 | 20 | 0 |
| INEQUALITY SET-3 (Eng).pdf | 10 | 20 | 20 | 0 |
| INEQUALITY SET-4 (Eng).pdf | 9 | 20 | 20 | 0 |
| **Total** | **37** | **80** | **80** | **0** |

All 37 pages were rendered and visually reviewed, alongside text extraction. Each set contains 20 numbered questions; answer-key pages and promotional/theory pages were not counted as extra questions. No repeated prompt was found across sets. The PDFs are English editions; no Hindi text was available to preserve.

Page-by-page disposition: Set 1 p. 1 is cover/promotion; pp. 2–5 contain questions 1–20; pp. 6–7 contain solutions; p. 8 is closing/promotion. Set 2 p. 1 is cover/promotion; p. 2 has questions 1–5; pp. 3–4 continue questions 6–10; pp. 5–6 contain questions 11–15; pp. 7–8 contain questions 16–20; p. 9 is the answer key; p. 10 is closing/promotion. Set 3 p. 1 is cover/promotion; pp. 2–4 contain questions 1–10; pp. 5–7 contain questions 11–16 and their preceding solutions; p. 8 contains questions 17–20; p. 9 is the answer key; p. 10 is closing/promotion. Set 4 p. 1 is cover/promotion; pp. 2–4 contain questions 1–10; pp. 5–7 contain questions 11–17 and their preceding solutions; p. 8 contains questions 18–20 and answer-key continuation; p. 9 is closing/promotion. The complete question-to-page mapping is tabulated below.

## Catalog and baseline

- Target: Banking → Clerk → Reasoning → Inequality.
- Chapter ID: `f969744d-074e-4535-987d-4181b2471884`.
- Local database: `ssc_prep` on `127.0.0.1:5432`; Alembic revision `0010_banking_catalog`.
- Before import: 27 active, 0 inactive questions. Existing records were inspected; none will be overwritten.
- Matching used normalized statement/conclusion content and a strict-aware constraint-closure fingerprint. Three exact semantic matches were found and excluded from the new batch: Set 2 questions 1–3 (physical page 2), matching existing rows `50376285-b89b-4687-8ce0-0b68ed0fcd26`, `73cc8e14-e36b-4ea7-8383-2105b6b86cc2`, and `f8e1895b-26d5-4bc6-9ce2-767d6d50a906`.

## Independent verification and disposition

Every question was solved from its source constraints using transitive order closure that preserves strict (`<`, `>`) versus weak (`≤`, `≥`) relations and equality. Either-or was accepted only when the conclusions were mutually exclusive and exhaustive for the same comparison. Printed answer keys were checked against the computed result.

- Source appearances: **80**; distinct prompts: **80**; repeated within/across PDFs: **0**.
- Already present in target database: **3**.
- New verified questions eligible: **65**.
- Held for answer/option issues: **12**.
- Imported options preserve the source A–E wording/order; answer key and explanation are independently verified. Source metadata records PDF filename, set number, and physical page.

### Held for source answer/option issues

| Source | Page | Question | Reason |
|---|---:|---:|---|
| Set 1 | 3 | 10 | The printed choices do not provide exactly one independently verified correct answer. |
| Set 1 | 5 | 16 | The printed choices do not provide exactly one independently verified correct answer. |
| Set 1 | 5 | 17 | The printed choices do not provide exactly one independently verified correct answer. |
| Set 1 | 5 | 19 | The printed choices do not provide exactly one independently verified correct answer. |
| Set 2 | 3 | 6 | Printed key A conflicts with independent solution E. |
| Set 2 | 6 | 12 | Printed key B conflicts with independent solution E. |
| Set 2 | 8 | 19 | Printed key D conflicts with independent solution B. |
| Set 3 | 6 | 11 | Printed key A conflicts with independent solution E. |
| Set 4 | 2 | 1 | Printed key D conflicts with independent solution B. |
| Set 4 | 3 | 6 | Printed key A conflicts with independent solution E. |
| Set 4 | 4 | 10 | Printed key B conflicts with independent solution E. |
| Set 4 | 7 | 16 | Printed key B conflicts with independent solution E. |
The four held Set 1 single-choice items have more than one source option that is independently true (or the printed list has no option representing the true combination). The other eight content holds have printed keys that disagree with the independently established answer. No answer key was silently corrected. The three existing-bank overlaps are skipped, not re-imported.

### Existing-bank duplicates skipped

| Source | Page | Question | Existing question ID |
|---|---:|---:|---|
| Set 2 | 2 | 1 | `50376285-b89b-4687-8ce0-0b68ed0fcd26` |
| Set 2 | 2 | 2 | `73cc8e14-e36b-4ea7-8383-2105b6b86cc2` |
| Set 2 | 2 | 3 | `f8e1895b-26d5-4bc6-9ce2-767d6d50a906` |

### Complete question inventory

| Set | Question | Physical page | Printed key | Independently verified result | Disposition |
|---:|---:|---:|---|---|---|
| 1 | 1 | 2 | E | E | eligible |
| 1 | 2 | 2 | A | A | eligible |
| 1 | 3 | 2 | B | B | eligible |
| 1 | 4 | 2 | C | C | eligible |
| 1 | 5 | 2 | D | D | eligible |
| 1 | 6 | 3 | E | E | eligible |
| 1 | 7 | 3 | C | C | eligible |
| 1 | 8 | 3 | E | E | eligible |
| 1 | 9 | 3 | A | A | eligible |
| 1 | 10 | 3 | B | NONE | held |
| 1 | 11 | 4 | E | E | eligible |
| 1 | 12 | 4 | A | A | eligible |
| 1 | 13 | 4 | B | B | eligible |
| 1 | 14 | 4 | D | D | eligible |
| 1 | 15 | 4 | C | C | eligible |
| 1 | 16 | 5 | B | MULTI | held |
| 1 | 17 | 5 | E | MULTI | held |
| 1 | 18 | 5 | E | E | eligible |
| 1 | 19 | 5 | D | MULTI | held |
| 1 | 20 | 5 | D | D | eligible |
| 2 | 1 | 2 | D | D | existing duplicate |
| 2 | 2 | 2 | A | A | existing duplicate |
| 2 | 3 | 2 | B | B | existing duplicate |
| 2 | 4 | 2 | E | E | eligible |
| 2 | 5 | 2 | C | C | eligible |
| 2 | 6 | 3 | A | E | held |
| 2 | 7 | 4 | E | E | eligible |
| 2 | 8 | 4 | D | D | eligible |
| 2 | 9 | 4 | C | C | eligible |
| 2 | 10 | 4 | B | B | eligible |
| 2 | 11 | 5 | A | A | eligible |
| 2 | 12 | 6 | B | E | held |
| 2 | 13 | 6 | C | C | eligible |
| 2 | 14 | 6 | D | D | eligible |
| 2 | 15 | 6 | E | E | eligible |
| 2 | 16 | 7 | B | B | eligible |
| 2 | 17 | 8 | E | E | eligible |
| 2 | 18 | 8 | C | C | eligible |
| 2 | 19 | 8 | D | B | held |
| 2 | 20 | 8 | A | A | eligible |
| 3 | 1 | 2 | D | D | eligible |
| 3 | 2 | 2 | A | A | eligible |
| 3 | 3 | 2 | B | B | eligible |
| 3 | 4 | 2 | E | E | eligible |
| 3 | 5 | 2 | C | C | eligible |
| 3 | 6 | 3 | B | B | eligible |
| 3 | 7 | 4 | D | D | eligible |
| 3 | 8 | 4 | E | E | eligible |
| 3 | 9 | 4 | C | C | eligible |
| 3 | 10 | 4 | C | C | eligible |
| 3 | 11 | 6 | A | E | held |
| 3 | 12 | 6 | D | D | eligible |
| 3 | 13 | 6 | C | C | eligible |
| 3 | 14 | 7 | E | E | eligible |
| 3 | 15 | 7 | A | A | eligible |
| 3 | 16 | 7 | C | C | eligible |
| 3 | 17 | 8 | A | A | eligible |
| 3 | 18 | 8 | E | E | eligible |
| 3 | 19 | 8 | B | B | eligible |
| 3 | 20 | 8 | A | A | eligible |
| 4 | 1 | 2 | D | B | held |
| 4 | 2 | 2 | A | A | eligible |
| 4 | 3 | 2 | B | B | eligible |
| 4 | 4 | 2 | C | C | eligible |
| 4 | 5 | 2 | E | E | eligible |
| 4 | 6 | 3 | A | E | held |
| 4 | 7 | 4 | E | E | eligible |
| 4 | 8 | 4 | D | D | eligible |
| 4 | 9 | 4 | C | C | eligible |
| 4 | 10 | 4 | B | E | held |
| 4 | 11 | 5 | E | E | eligible |
| 4 | 12 | 6 | E | E | eligible |
| 4 | 13 | 6 | B | B | eligible |
| 4 | 14 | 6 | D | D | eligible |
| 4 | 15 | 6 | E | E | eligible |
| 4 | 16 | 7 | B | E | held |
| 4 | 17 | 7 | E | E | eligible |
| 4 | 18 | 8 | C | C | eligible |
| 4 | 19 | 8 | D | D | eligible |
| 4 | 20 | 8 | B | B | eligible |

## Import verification

- Pre-import importer dry-run: 65 records, 0 rejected, 0 duplicates, 0 validation errors; 65 would import. No rows were written by the dry-run.
- Transactional local import: 65 inserted, 0 rejected, 0 duplicates, 0 errors.
- Final target chapter count: 92 active, 0 inactive. All 27 original records were compared before/after and remain unchanged; all 65 new records match the import JSON with five options, one correct option, a nonempty explanation, and source metadata.
- Held content prompts: 0 of the 12 were imported. The three database duplicates were not inserted again.
- Importer replay dry-run: 65 duplicates, 0 would import, 0 rejected, 0 errors.
- Authenticated local API: HTTP 200; returned all 92 active chapter questions. All 65 imported records matched their options, answer flags, explanations, source metadata, and chapter ID.
- Backend tests: the new artifact regression and existing non-integration Inequality tests passed (`13 passed, 1 deselected`). The existing `test_series_style_chapter_availability_and_full_inequality_test_flow` stalled without completion during the combined run; it was interrupted and has no pass/fail result.
- Frontend production build: `npm run build` passed (`tsc -b` and Vite; 55 modules transformed).
- No migration was run.
- Complete per-question statements, conclusions, answer outcomes, dispositions, and reasons: `inequality_sets_01_04_answer_ledger.json`.
