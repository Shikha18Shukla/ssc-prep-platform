# Banking Maths Set 9 - Answer Verification Report

## Method

Every shipped answer was independently recomputed by
`backend/verify_banking_maths_set9_questions.py` from `verification_data.inputs`.
The verifier uses the separate formula dispatch in
`backend/maths_set9/formulas.py` backed by `formula_helpers.calc()`; it never
reads the stored `correct_answer` when deriving the expected value. Inputs are
stored as JSON-native values, so no `Fraction` object leaks into a dataset.

The verifier checks the exact 20-field schema, deterministic IDs, 120 items per
chapter, 15/20/30/55 part sizes, four distinct A/B/C/D options,
`correct_option`/`correct_answer` agreement, nonempty explanations,
`ORIGINAL_VERIFIED` provenance, `VERIFIED` status, null `exam_year`, difficulty
separation, and inline DI data with internally consistent shared values.

Separate builders and formula helpers were used per chapter. Every one of the
840 items was recomputed after generation; no stored answer was accepted on
trust.

## Per-chapter result

| Chapter | Questions | Families | Variants/family | Difficulty | Part sizes |
| --- | ---: | ---: | ---: | --- | --- |
| Pipe and Cistern - Data Interpretation | 120 | 24 | 5 | EASY 35, MEDIUM 85 | 15 / 20 / 30 / 55 |
| Trains (Mains) | 120 | 24 | 5 | HARD 120 | 15 / 20 / 30 / 55 |
| Trains - Data Interpretation | 120 | 24 | 5 | EASY 35, MEDIUM 85 | 15 / 20 / 30 / 55 |
| Boats and Streams (Mains) | 120 | 24 | 5 | HARD 120 | 15 / 20 / 30 / 55 |
| Boats and Streams - Data Interpretation | 120 | 24 | 5 | EASY 35, MEDIUM 85 | 15 / 20 / 30 / 55 |
| Probability (Mains) | 120 | 24 | 5 | HARD 120 | 15 / 20 / 30 / 55 |
| Probability - Data Interpretation | 120 | 24 | 5 | EASY 35, MEDIUM 85 | 15 / 20 / 30 / 55 |
| **Total** | **840** | **168** | **5** | **HARD 360, EASY 140, MEDIUM 340** | **15 / 20 / 30 / 55** |

The three Mains chapters are genuinely HARD and cover multi-step Banking PO
Mains patterns such as delayed starts, opposite-bank meetings, conditional
branching and data sufficiency. The four DI chapters are Prelims-level
(EASY/MEDIUM only) and each question carries its own inline table/values.

## Verifier output

```
verified 840 questions across 7 chapters
ALL CHECKS PASSED
```

## Related checks

- Exact/normalized duplicate texts within the batch: 0.
- Number-masked templates repeated only inside the expected five-variant
  families: 168; templates shared across families or chapters: 0.
- Four distinct options and matching answer key on all 840 items.
- All 840 items are `ORIGINAL_VERIFIED` / `VERIFIED` with `exam_year` null.
