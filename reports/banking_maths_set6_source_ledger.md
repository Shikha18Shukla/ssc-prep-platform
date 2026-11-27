# Banking Maths Set 6 - Source and Verification Ledger

## Scope

Six Banking Maths chapters were filled for **Banking Clerk** and
**Banking PO** only. `Banking Others` was not touched.

| Chapter | Dataset | Questions | Parts |
| --- | --- | ---: | --- |
| Percentage Arithmetic (Mains) | `data/banking_maths_percentage_arithmetic_mains_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Percentage – Data Interpretation (Mains) | `data/banking_maths_percentage_di_mains_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Ratio Arithmetic (Mains) | `data/banking_maths_ratio_arithmetic_mains_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Ratio – Data Interpretation (Mains) | `data/banking_maths_ratio_di_mains_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Profit and Loss (Mains) | `data/banking_maths_profit_and_loss_mains_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Profit and Loss – Data Interpretation | `data/banking_maths_profit_and_loss_di_questions.json` | 120 | 15 / 20 / 30 / 55 |

## PDF inspection and content-based mapping

All 6 supplied PDFs (89 pages) were inspected page by page.
89 pages were image-only and rendered at 150 dpi for OCR;
the remaining 0 pages expose a text layer.
Deck names were not trusted: several files are UUID-named and the slide
titles are the reliable topic signal. Chapter assignment follows the extracted
slide text: the Percentage Arithmetic deck contains percentage-main slides,
the Percentage DI deck contains percentage-distribution caselets, the Ratio
Arithmetic deck contains advanced ratio slides, and the Ratio DI deck contains
ratio-based tables and pie charts. Printed keys were treated as untrusted
reference data and were never copied. The Profit and Loss DI deck supplies
topic scope only; the shipped chapter is deliberately Prelims-level. Full
page and shipped-question detail is in
`reports/banking_maths_set6_source_ledger.csv`.

| File | Chapter | Topic | Pages | Read as | Text pages | OCR pages |
| --- | --- | --- | ---: | --- | ---: | ---: |
| 55742ecb-5ae3-4ad2-b6ab-0283e85516fa.pdf | profit_and_loss_data_interpretation | Profit and Loss Data Interpretation - shop-wise profit/loss data | 14 | OCR (image-only) | 0 | 14 |
| e6b0be93-e145-4d7c-852e-cab76407378c.pdf | profit_and_loss_mains | Profit and Loss Mains - profit, loss and discount problems | 16 | OCR (image-only) | 0 | 16 |
| b9943fe1-2ef5-4b1d-a84e-09ad8387176e.pdf | ratio_data_interpretation_mains | Ratio Data Interpretation Mains - ratio-based tables, pie charts and caselets | 25 | OCR (image-only) | 0 | 25 |
| ed99aa3d-eaea-44e4-b047-f1fdcba71c86.pdf | percentage_arithmetic_mains | Percentage Arithmetic Mains - advanced percentage concepts and problems | 12 | OCR (image-only) | 0 | 12 |
| 6a3006de-e616-4a57-94e5-8db1d4c07b67.pdf | percentage_data_interpretation_mains | Percentage Data Interpretation Mains - percentage distributions and comparisons | 11 | OCR (image-only) | 0 | 11 |
| c37283ae-286f-402f-90c5-fdba5737fd43.pdf | ratio_arithmetic_mains | Ratio Arithmetic Mains - advanced ratio and proportion problems | 11 | OCR (image-only) | 0 | 11 |
| **Total** | | | **89** | | **0** | **89** |

## Why the PDF items were not imported verbatim

- The decks are slide images with worked examples; OCR of mathematical
  notation is not reliable enough to certify an answer.
- Printed options/keys were not treated as authoritative.
- All shipped items are original questions written for this bank.

The PDFs defined topic scope; difficulty follows the required chapter level.
The five Mains chapters are labelled `HARD` throughout. Profit and Loss –
Data Interpretation is deliberately Prelims-level (`EASY` for the first seven
families and `MEDIUM` for the rest). Every shipped question is an original
written for this bank, tagged `source_type = ORIGINAL_VERIFIED`.
`source_page` is a topic reference, not a copy citation; no item is a PYQ.

## Verification

`backend/verify_banking_maths_set6_questions.py` recomputes every answer
from `verification_data` without trusting the stored answer. It checks
four unique options, one correct option, answer/index agreement, explanation
consistency, units/rounding, valid difficulty, part sizes 15 / 20 / 30 / 55,
120 unique items per chapter and no PYQ flag. Result: **720 questions
checked, 0 failures**.

## Reconciliation with the final datasets

| Chapter | Dataset questions | Parts | Shipped ledger rows | PDF/OCR rows |
| --- | ---: | --- | ---: | ---: |
| Percentage Arithmetic (Mains) | 120 | 15 / 20 / 30 / 55 | 120 | 12 |
| Percentage – Data Interpretation (Mains) | 120 | 15 / 20 / 30 / 55 | 120 | 11 |
| Ratio Arithmetic (Mains) | 120 | 15 / 20 / 30 / 55 | 120 | 11 |
| Ratio – Data Interpretation (Mains) | 120 | 15 / 20 / 30 / 55 | 120 | 25 |
| Profit and Loss (Mains) | 120 | 15 / 20 / 30 / 55 | 120 | 16 |
| Profit and Loss – Data Interpretation | 120 | 15 / 20 / 30 / 55 | 120 | 14 |

No PDF item was copied into a dataset. The 720 shipped questions are
originals with a topic-page reference to the inspected sources; none is a
previous-year question.
