# Banking Maths Batch 2 - Source and Verification Ledger

## Scope

Five new Banking Maths chapters were filled for **Banking Clerk** and
**Banking PO** only. `Banking Others` was not touched.

| Chapter | Dataset | Questions | Parts |
| --- | --- | ---: | --- |
| Quadratic Equations | `data/banking_maths_quadratic_equations_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Number System | `data/banking_maths_number_system_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Percentage | `data/banking_maths_percentage_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Ratio and Proportion | `data/banking_maths_ratio_proportion_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Profit, Loss and Discount | `data/banking_maths_profit_loss_discount_questions.json` | 120 | 15 / 20 / 30 / 55 |

## PDF inspection

All 28 supplied PDFs (425 pages) were inspected page by page. Thirteen are
image-only decks rendered at 150 dpi and read with RapidOCR; the rest expose
a text layer. Question and solution blocks were matched by printed question
number. Per-item and per-page detail is in
`reports/banking_maths_set2_source_ledger.csv`.

| File | Chapter | Topic | Pages | Read as | Items | OCR pages | With options | With key |
| --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: |
| Number System 01 _ Class Notes.pdf | Number System | Number System - set/notes 1 | 27 | OCR (image-only PDF) | 0 | 27 | 0 | 0 |
| Number System 02  Class Notes.pdf | Number System | Number System - set/notes 2 | 16 | OCR (image-only PDF) | 0 | 16 | 0 | 0 |
| Number System 03_Class Notes.pdf | Number System | Number System - class notes | 12 | OCR (image-only PDF) | 0 | 12 | 0 | 0 |
| PROFIT&LOSS SET-1 (Eng).pdf | Profit, Loss and Discount | Profit, Loss and Discount - set/notes 1 | 5 | text layer | 9 | 0 | 9 | 9 |
| PROFIT&LOSS SET-2 (Eng).pdf | Profit, Loss and Discount | Profit, Loss and Discount - set/notes 2 | 5 | text layer | 10 | 0 | 10 | 10 |
| PROFIT&LOSS SET-3 (Eng).pdf | Profit, Loss and Discount | Profit, Loss and Discount - set/notes 3 | 6 | text layer | 10 | 0 | 10 | 10 |
| PROFIT&LOSS SET-4 (Eng).pdf | Profit, Loss and Discount | Profit, Loss and Discount - set/notes 4 | 6 | text layer | 10 | 0 | 10 | 10 |
| PROFIT&LOSS SET-6 (Eng).pdf | Profit, Loss and Discount | Profit, Loss and Discount - set/notes 6 | 7 | text layer | 10 | 0 | 10 | 10 |
| Percentage 01_Class Notes.pdf | Percentage | Percentage - class notes | 19 | OCR (image-only PDF) | 0 | 19 | 0 | 0 |
| Percentage 02 _ Class Notes.pdf | Percentage | Percentage - set/notes 2 | 17 | OCR (image-only PDF) | 0 | 17 | 0 | 0 |
| Percentage 03_Class Notes.pdf | Percentage | Percentage - class notes | 25 | OCR (image-only PDF) | 0 | 25 | 0 | 0 |
| Percentage 04_Class Notes.pdf | Percentage | Percentage - class notes | 19 | OCR (image-only PDF) | 0 | 19 | 0 | 0 |
| Percentage 05_Class Notes.pdf | Percentage | Percentage - class notes | 19 | OCR (image-only PDF) | 0 | 19 | 0 | 0 |
| Percentage 06_Class Notes.pdf | Percentage | Percentage - class notes | 19 | OCR (image-only PDF) | 0 | 19 | 0 | 0 |
| Percentage 07_Class Notes.pdf | Percentage | Percentage - class notes | 19 | OCR (image-only PDF) | 0 | 19 | 0 | 0 |
| Percentage 08_Class Notes.pdf | Percentage | Percentage - class notes | 21 | OCR (image-only PDF) | 0 | 21 | 0 | 0 |
| Profit, Loss and Discount 05 _Class Notes.pdf | Profit, Loss and Discount | Profit, Loss and Discount - set/notes 5 | 17 | OCR (image-only PDF) | 0 | 17 | 0 | 0 |
| Profit, Loss and Discount 06_Class Notes.pdf | Profit, Loss and Discount | Profit, Loss and Discount - class notes | 17 | OCR (image-only PDF) | 0 | 17 | 0 | 0 |
| QUADRATIC EQUATION SET-1 (Eng).pdf | Quadratic Equations | Quadratic Equations - set/notes 1 | 20 | text layer | 50 | 0 | 50 | 50 |
| QUADRATIC EQUATION SET-2 (Eng).pdf | Quadratic Equations | Quadratic Equations - set/notes 2 | 20 | text layer | 50 | 0 | 50 | 50 |
| QUADRATIC EQUATION SET-3 (Eng).pdf | Quadratic Equations | Quadratic Equations - set/notes 3 | 20 | text layer | 50 | 0 | 50 | 50 |
| QUADRATIC EQUATION SET-4 (Eng).pdf | Quadratic Equations | Quadratic Equations - set/notes 4 | 20 | text layer | 50 | 0 | 50 | 50 |
| QUADRATIC EQUATION SET-5 (Eng).pdf | Quadratic Equations | Quadratic Equations - set/notes 5 | 20 | text layer | 50 | 0 | 50 | 49 |
| QUADRATIC EQUATION SET-6 (Eng).pdf | Quadratic Equations | Quadratic Equations - set/notes 6 | 20 | text layer | 50 | 0 | 50 | 50 |
| Ratio_and_Proportion_Set-1_(Mains).pdf | Ratio and Proportion | Ratio and Proportion - class notes | 7 | text layer | 10 | 0 | 10 | 10 |
| Ratio_and_Proportion_Set-2_(Mains).pdf | Ratio and Proportion | Ratio and Proportion - class notes | 8 | text layer | 10 | 0 | 10 | 10 |
| Ratio_and_Proportion_Set-3_(Mains).pdf | Ratio and Proportion | Ratio and Proportion - class notes | 7 | text layer | 10 | 0 | 10 | 10 |
| Ratio_and_Proportion_Set-4_(Mains).pdf | Ratio and Proportion | Ratio and Proportion - class notes | 7 | text layer | 10 | 0 | 10 | 10 |
| **Total** | | | **425** | | **389** | **247** | **389** | **388** |

## Why the PDF items were not imported verbatim

- The Guidely sets use five options (A-E), while this bank stores four.
- Printed keys were treated as untrusted and were never copied into the bank.
- The class-note decks are slide images with theory, worked examples and
  occasional MCQs; OCR of mathematical notation is not reliable enough to
  certify a printed answer, so no OCR item was assigned a question number.

The PDFs defined topic scope and difficulty. Every shipped question is an
original written for this bank, tagged `source_type = ORIGINAL_VERIFIED`.
`source_page` is a topic reference, not a copy citation; no item is a PYQ.

## Verification

`backend/generate_banking_maths_set2_questions.py` computes every answer in
Python from a seeded generator. `backend/verify_banking_maths_set2_questions.py`
recomputes every answer from `verification_data` without trusting the stored
answer, and checks four unique options, one correct option, a non-empty
explanation, valid difficulty, part sizes 15 / 20 / 30 / 55, 120 unique items
per chapter and no PYQ flag. Result: **600 questions checked, 0 failures**.

## Deduplication

`backend/dedup_banking_maths_set2.py` checked all 600 questions against each
other, the first 600-question batch and all 12,532 existing database questions
using exact, normalized, number-masked and lexical (token + bigram) tests.
Result: 0 collisions of every kind. See
`reports/banking_maths_set2_dedup_report.md`.

## Reconciliation with the final datasets

| Chapter | Dataset questions | Parts | PDF rows inspected | PDF rows imported | Original rows |
| --- | ---: | --- | ---: | ---: | ---: |
| Quadratic Equations | 120 | 15 / 20 / 30 / 55 | 300 | 0 | 120 |
| Number System | 120 | 15 / 20 / 30 / 55 | 55 | 0 | 120 |
| Percentage | 120 | 15 / 20 / 30 / 55 | 158 | 0 | 120 |
| Ratio and Proportion | 120 | 15 / 20 / 30 / 55 | 40 | 0 | 120 |
| Profit, Loss and Discount | 120 | 15 / 20 / 30 / 55 | 83 | 0 | 120 |

PDF rows inspected are the MCQs or OCR pages recorded above; none of them
was copied into a dataset. The 600 shipped questions are originals that
carry a topic-page reference to the class notes, never a claim of being a
PDF extraction or a previous-year question.
