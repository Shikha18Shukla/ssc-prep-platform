# Banking Maths Set 5 - Source and Verification Ledger

## Scope

Six Banking Maths chapters were filled for **Banking Clerk** and
**Banking PO** only. `Banking Others` was not touched.

| Chapter | Dataset | Questions | Parts |
| --- | --- | ---: | --- |
| Mensuration – 3D | `data/banking_maths_mensuration_3d_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Permutations | `data/banking_maths_permutations_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Combinations | `data/banking_maths_combinations_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Probability | `data/banking_maths_probability_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Data Interpretation | `data/banking_maths_data_interpretation_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Caselet Data Interpretation | `data/banking_maths_caselet_data_interpretation_questions.json` | 120 | 15 / 20 / 30 / 55 |

## PDF inspection and content-based mapping

All 10 supplied PDFs (211 pages) were inspected page by page.
211 pages were image-only and rendered at 150 dpi for OCR;
the remaining 0 pages expose a text layer.
Deck names were not trusted: several files were named after the previous
lecture. Chapter assignment follows the extracted slide text (for example,
`Permuations 01` contains permutation slides and `Combinations 01` contains
combination slides). Printed keys were treated as untrusted reference data
and were never copied into the bank. Full page and shipped-question detail
is in `reports/banking_maths_set5_source_ledger.csv`.

| File | Chapter | Topic | Pages | Read as | Text pages | OCR pages |
| --- | --- | --- | ---: | --- | ---: | ---: |
| Mensurations 3D 01  Class Notes.pdf | mensuration_3d | Mensuration 3D - concepts and formulae | 9 | OCR (image-only) | 0 | 9 |
| Mensurations 3D 02  Class Notes.pdf | mensuration_3d | Mensuration 3D - miscellaneous problems | 12 | OCR (image-only) | 0 | 12 |
| Permuations 01  Class Notes.pdf | permutations | Permutation - basic concepts and problems | 17 | OCR (image-only) | 0 | 17 |
| Combinations 01  Class Notes.pdf | combinations | Combination - basic concepts and problems | 14 | OCR (image-only) | 0 | 14 |
| Probability 01  Class Notes.pdf | probability | Probability - coins, dice and basic concepts | 19 | OCR (image-only) | 0 | 19 |
| 7e88503c-399d-41ec-81d4-e2a199287a4e.pdf | probability | Probability - miscellaneous concepts and problems | 14 | OCR (image-only) | 0 | 14 |
| DATA INTERPRETATION 01  Class Notes.pdf | data_interpretation | Data Interpretation - tables and graphs | 24 | OCR (image-only) | 0 | 24 |
| dd6dc577-2571-460b-952b-3b67ddf71c1c.pdf | data_interpretation | Data Interpretation - line and pie graphs | 19 | OCR (image-only) | 0 | 19 |
| d0d52b32-a3ee-4287-a42c-a34734858e19.pdf | data_interpretation | Data Interpretation - mixed graph sets | 24 | OCR (image-only) | 0 | 24 |
| e1183040-db37-4bf1-a5c1-ebac16ca3f1f.pdf | caselet_data_interpretation | Caselet Data Interpretation - passage sets | 59 | OCR (image-only) | 0 | 59 |
| **Total** | | | **211** | | **0** | **211** |

## Why the PDF items were not imported verbatim

- The decks are slide images with worked examples; OCR of mathematical
  notation is not reliable enough to certify an answer.
- Printed options/keys were not treated as authoritative.
- All shipped items are original questions written for this bank.

The PDFs defined topic scope and difficulty. Every shipped question is an
original written for this bank, tagged `source_type = ORIGINAL_VERIFIED`.
`source_page` is a topic reference, not a copy citation; no item is a PYQ.

## Verification

`backend/verify_banking_maths_set5_questions.py` recomputes every answer
from `verification_data` without trusting the stored answer. It checks
four unique options, one correct option, answer/index agreement, explanation
consistency, units/rounding, valid difficulty, part sizes 15 / 20 / 30 / 55,
120 unique items per chapter and no PYQ flag. Result: **720 questions
checked, 0 failures**.

## Reconciliation with the final datasets

| Chapter | Dataset questions | Parts | Shipped ledger rows | PDF/OCR rows |
| --- | ---: | --- | ---: | ---: |
| Mensuration – 3D | 120 | 15 / 20 / 30 / 55 | 120 | 21 |
| Permutations | 120 | 15 / 20 / 30 / 55 | 120 | 17 |
| Combinations | 120 | 15 / 20 / 30 / 55 | 120 | 14 |
| Probability | 120 | 15 / 20 / 30 / 55 | 120 | 33 |
| Data Interpretation | 120 | 15 / 20 / 30 / 55 | 120 | 67 |
| Caselet Data Interpretation | 120 | 15 / 20 / 30 / 55 | 120 | 59 |

No PDF item was copied into a dataset. The 720 shipped questions are
originals with a topic-page reference to the inspected sources; none is a
previous-year question.
