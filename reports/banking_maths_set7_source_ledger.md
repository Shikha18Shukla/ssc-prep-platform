# Banking Maths Set 7 - Source and Verification Ledger

## Scope

Six Banking Maths chapters were filled for **Banking Clerk** and
**Banking PO** only. `Banking Others` was not touched.

| Chapter | Dataset | Questions | Parts |
| --- | --- | ---: | --- |
| Mixture and Alligation (Mains) | `data/banking_maths_mixture_alligation_mains_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Mixture and Alligation – Data Interpretation | `data/banking_maths_mixture_alligation_di_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Ages (Mains) | `data/banking_maths_ages_mains_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Ages – Data Interpretation | `data/banking_maths_ages_di_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Partnership (Mains) | `data/banking_maths_partnership_mains_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Partnership – Data Interpretation | `data/banking_maths_partnership_di_questions.json` | 120 | 15 / 20 / 30 / 55 |

## PDF inspection and content-based mapping

All 6 supplied PDFs (77 pages) were inspected page by page.
77 pages were image-only and rendered at 150 dpi for OCR;
the remaining 0 pages expose a text layer.
Deck names were not trusted: every file is UUID-named and the slide
titles are the reliable topic signal. Chapter assignment follows the extracted
slide text (mixture/alligation, ages, partnership and their DI variants).
Printed questions and answer keys were treated as untrusted reference data
and were never copied. Full page and shipped-question detail is in
`reports/banking_maths_set7_source_ledger.csv`.

| File | Chapter | Topic | Pages | Read as | Text pages | OCR pages |
| --- | --- | --- | ---: | --- | ---: | ---: |
| 9f8905f3-85dc-44f0-bda1-42d5c96a3304.pdf | partnership_data_interpretation | Partnership Data Interpretation - multi-business capital and profit tables | 13 | OCR (image-only) | 0 | 13 |
| cc2c97f4-4d95-4e6e-964f-d9318068eb13.pdf | partnership_mains | Partnership Mains - capital/time caselets, salary and ratio amendments | 14 | OCR (image-only) | 0 | 14 |
| 419d6ebd-36ff-4b8a-80e5-178a8bde98d6.pdf | ages_data_interpretation | Ages Data Interpretation - quantity comparison, averages and inline age tables | 13 | OCR (image-only) | 0 | 13 |
| 97c1911e-319b-4bc6-8383-48a92c70a378.pdf | ages_mains | Ages Mains - algebraic multi-person age and ratio conditions | 11 | OCR (image-only) | 0 | 11 |
| 66052d90-202e-454e-96d2-3f7291856dba.pdf | mixture_alligation_data_interpretation | Mixture and Alligation Data Interpretation - container tables and concentration caselets | 13 | OCR (image-only) | 0 | 13 |
| 36c4c768-3fbf-4ae7-8b96-debff3f16eec.pdf | mixture_alligation_mains | Mixture and Alligation Mains - advanced multi-stage mixture and weighted-average problems | 13 | OCR (image-only) | 0 | 13 |
| **Total** | | | **77** | | **0** | **77** |

## Why the PDF items were not imported verbatim

- The decks are slide images with worked examples; OCR of mathematical
  notation is not reliable enough to certify an answer.
- Printed options/keys were not treated as authoritative.
- All shipped items are original questions written for this bank.

The PDFs defined topic scope; difficulty follows the required chapter level.
The three Mains chapters are labelled `HARD` throughout. The three normal
DI chapters are deliberately Prelims-level (`EASY` for the first seven
families and `MEDIUM` for the rest). Every shipped question is an original
written for this bank, tagged `source_type = ORIGINAL_VERIFIED`.
`source_page` is a topic reference, not a copy citation; no item is a PYQ.

## Verification

`backend/verify_banking_maths_set7_questions.py` recomputes every answer
from `verification_data` without trusting the stored answer. It checks
four unique options, one correct option, answer/index agreement, explanation
consistency, units/rounding, valid difficulty, part sizes 15 / 20 / 30 / 55,
120 unique items per chapter and no PYQ flag. Result: **720 questions
checked, 0 failures**.

## Reconciliation with the final datasets

| Chapter | Dataset questions | Parts | Shipped ledger rows | PDF/OCR rows |
| --- | ---: | --- | ---: | ---: |
| Mixture and Alligation (Mains) | 120 | 15 / 20 / 30 / 55 | 120 | 13 |
| Mixture and Alligation – Data Interpretation | 120 | 15 / 20 / 30 / 55 | 120 | 13 |
| Ages (Mains) | 120 | 15 / 20 / 30 / 55 | 120 | 11 |
| Ages – Data Interpretation | 120 | 15 / 20 / 30 / 55 | 120 | 13 |
| Partnership (Mains) | 120 | 15 / 20 / 30 / 55 | 120 | 14 |
| Partnership – Data Interpretation | 120 | 15 / 20 / 30 / 55 | 120 | 13 |

No PDF item was copied into a dataset. The 720 shipped questions are
originals with a topic-page reference to the inspected sources; none is a
previous-year question.
