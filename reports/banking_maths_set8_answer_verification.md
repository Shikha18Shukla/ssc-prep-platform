# Banking Maths Set 8 - Answer Verification Report

## Method

Every shipped answer was recomputed from `verification_data.inputs` by
`backend/verify_banking_maths_set8_questions.py` using the independent formula
sheets in `backend/maths_set8/formulas_*.py`. The verifier never reads the stored
`correct_answer` when deriving the expected value; it also checks the exact
20-field schema, deterministic IDs, 15/20/30/55 part split, four distinct
options, `correct_option`/`correct_answer` agreement, nonempty explanations,
`ORIGINAL_VERIFIED` provenance, `VERIFIED` status, null `exam_year`, difficulty
separation, and inline DI data.

Separate builder/formula modules were used for each chapter. Every family and
variant was additionally self-tested before generation: 120/120 answer matches
per chapter, 720/720 overall.

## Verifier output

```
verified 720 questions across 6 chapters
families per chapter: 24; variants per family: 5
Time and Work (Mains): HARD=120, EASY=0, MEDIUM=0
Time and Work - Data Interpretation: EASY=35, MEDIUM=85, HARD=0
Time, Speed and Distance (Mains): HARD=120, EASY=0, MEDIUM=0
Simple and Compound Interest (Mains): HARD=120, EASY=0, MEDIUM=0
Simple and Compound Interest - Data Interpretation: EASY=35, MEDIUM=85, HARD=0
Pipe and Cistern (Mains): HARD=120, EASY=0, MEDIUM=0
ALL CHECKS PASSED
```

## Distribution

| Chapter | Questions | Families | Variants/family | Difficulty |
| --- | ---: | ---: | ---: | --- |
| Time and Work (Mains) | 120 | 24 | 5 | HARD only |
| Time and Work - Data Interpretation | 120 | 24 | 5 | 35 EASY / 85 MEDIUM |
| Time, Speed and Distance (Mains) | 120 | 24 | 5 | HARD only |
| Simple and Compound Interest (Mains) | 120 | 24 | 5 | HARD only |
| Simple and Compound Interest - Data Interpretation | 120 | 24 | 5 | 35 EASY / 85 MEDIUM |
| Pipe and Cistern (Mains) | 120 | 24 | 5 | HARD only |

## Result

- Independent recomputation mismatches: **0**
- Schema, option, ID, provenance, and difficulty failures: **0**
- Status: **ALL CHECKS PASSED**
