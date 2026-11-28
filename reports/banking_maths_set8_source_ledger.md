# Banking Maths Set 8 - Source and Verification Ledger

## Scope

Six Banking Maths chapters were filled for **Banking Clerk** and
**Banking PO** only. `Banking Others` was not touched.

| Chapter | Dataset | Questions | Parts |
| --- | --- | ---: | --- |
| Time and Work (Mains) | `data/banking_maths_time_and_work_mains_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Time and Work – Data Interpretation | `data/banking_maths_time_and_work_di_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Time, Speed and Distance (Mains) | `data/banking_maths_time_speed_and_distance_mains_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Simple and Compound Interest (Mains) | `data/banking_maths_simple_and_compound_interest_mains_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Simple and Compound Interest – Data Interpretation | `data/banking_maths_simple_and_compound_interest_di_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Pipe and Cistern (Mains) | `data/banking_maths_pipe_and_cistern_mains_questions.json` | 120 | 15 / 20 / 30 / 55 |

## PDF inspection and content-based mapping

All 7 supplied PDFs (102 pages) were inspected page by page.
102 pages were image-only and rendered at 150 dpi for OCR;
the remaining 0 pages expose a text layer.
Deck names were not trusted: several files are UUID-named and the slide
titles are the reliable topic signal. Chapter assignment follows the extracted
slide text; three filename/topic mismatches were corrected during inspection.
One extra Time Speed and Distance DI deck has no target chapter and is
recorded but not shipped from.
Printed questions and answer keys were treated as untrusted reference data
and were never copied. Full page and shipped-question detail is in
`reports/banking_maths_set8_source_ledger.csv`.

| File | Chapter | Topic | Pages | Read as | Text pages | OCR pages |
| --- | --- | --- | ---: | --- | ---: | ---: |
| ce788d06-e730-4963-97ca-208b2af36699 (2).pdf | time_and_work_data_interpretation | Time and Work Data Interpretation - inline worker/day tables and derived work shares | 11 | OCR (image-only) | 0 | 11 |
| 0da2c67a-4985-4a86-9772-b0c4b826b42f.pdf | time_speed_and_distance_mains | Time, Speed and Distance Mains - trains, boats, relative speed and chase conditions | 15 | OCR (image-only) | 0 | 15 |
| Time Speed and Distance Mains 02 Class Notes.pdf | unmapped_extra | Unmapped extra deck - Time Speed and Distance Data Interpretation Mains, not a target chapter | 16 | OCR (image-only) | 0 | 16 |
| Simple and Compound Interest Mains 01  Class Notes.pdf | simple_and_compound_interest_mains | Simple and Compound Interest Mains - successive rates, compounding periods and installments | 12 | OCR (image-only) | 0 | 12 |
| f5b22d88-8d5a-494e-b7b2-9e5b1b05d260.pdf | simple_and_compound_interest_data_interpretation | Simple and Compound Interest Data Interpretation - inline principal/rate/time tables | 20 | OCR (image-only) | 0 | 20 |
| Pipe and Cistern Mains 01 _Class Notes.pdf | pipe_and_cistern_mains | Pipe and Cistern Mains - inlet/outlet combinations, leakage and alternating pipes | 15 | OCR (image-only) | 0 | 15 |
| 87fda602-e97e-4aa7-90cc-9f316d0af672.pdf | time_and_work_mains | Time and Work Mains - changing efficiency, staged work and wage-contribution caselets | 13 | OCR (image-only) | 0 | 13 |
| **Total** | | | **102** | | **0** | **102** |

## Why the PDF items were not imported verbatim

- The decks are slide images with worked examples; OCR of mathematical
  notation is not reliable enough to certify an answer.
- Printed options/keys were not treated as authoritative.
- All shipped items are original questions written for this bank.

The PDFs defined topic scope; difficulty follows the required chapter level.
The four Mains chapters are labelled `HARD` throughout. The two normal
DI chapters are deliberately Prelims-level (`EASY` for the first seven
families and `MEDIUM` for the rest). Every shipped question is an original
written for this bank, tagged `source_type = ORIGINAL_VERIFIED`.
`source_page` is a topic reference, not a copy citation; no item is a PYQ.

## Verification

`backend/verify_banking_maths_set8_questions.py` recomputes every answer
from `verification_data` without trusting the stored answer. It checks
four unique options, one correct option, answer/index agreement, explanation
consistency, units/rounding, valid difficulty, part sizes 15 / 20 / 30 / 55,
120 unique items per chapter and no PYQ flag. Result: **720 questions
checked, 0 failures**.

## Reconciliation with the final datasets

| Chapter | Dataset questions | Parts | Shipped ledger rows | PDF/OCR rows |
| --- | ---: | --- | ---: | ---: |
| Time and Work (Mains) | 120 | 15 / 20 / 30 / 55 | 120 | 13 |
| Time and Work – Data Interpretation | 120 | 15 / 20 / 30 / 55 | 120 | 11 |
| Time, Speed and Distance (Mains) | 120 | 15 / 20 / 30 / 55 | 120 | 15 |
| Simple and Compound Interest (Mains) | 120 | 15 / 20 / 30 / 55 | 120 | 12 |
| Simple and Compound Interest – Data Interpretation | 120 | 15 / 20 / 30 / 55 | 120 | 20 |
| Pipe and Cistern (Mains) | 120 | 15 / 20 / 30 / 55 | 120 | 15 |

No PDF item was copied into a dataset. The 720 shipped questions are
originals with a topic-page reference to the inspected sources; none is a
previous-year question.
