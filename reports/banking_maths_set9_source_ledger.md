# Banking Maths Set 9 - Source and Verification Ledger

## Scope

Seven Banking Maths chapters were filled for **Banking Clerk** and
**Banking PO** only. `Banking Others` was not touched.

| Chapter | Dataset | Questions | Parts |
| --- | --- | ---: | --- |
| Pipe and Cistern – Data Interpretation | `data/banking_maths_pipe_and_cistern_di_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Trains (Mains) | `data/banking_maths_trains_mains_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Trains – Data Interpretation | `data/banking_maths_trains_data_interpretation_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Boats and Streams (Mains) | `data/banking_maths_boats_and_streams_mains_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Boats and Streams – Data Interpretation | `data/banking_maths_boats_and_streams_data_interpretation_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Probability (Mains) | `data/banking_maths_probability_mains_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Probability – Data Interpretation | `data/banking_maths_probability_data_interpretation_questions.json` | 120 | 15 / 20 / 30 / 55 |

## PDF inspection and content-based mapping

All 7 supplied PDFs (89 pages) were inspected page by page.
89 pages were image-only and rendered for OCR;
the remaining 0 pages expose a text layer.
Deck names were not trusted: several files are UUID-named and the slide
titles and problem content are the reliable topic signal. Chapter assignment
follows the title slide plus substantive content; recap slides naming another
chapter were not used as evidence. No exam year was inferred from the slides.
Printed questions and answer keys were treated as untrusted reference data
and were never copied. Full page and shipped-question detail is in
`reports/banking_maths_set9_source_ledger.csv`.

| File | Chapter | Topic | Pages | Read as | Text pages | OCR pages |
| --- | --- | --- | ---: | --- | ---: | ---: |
| f9d83e47-9397-4b2e-99aa-92595ea4647c.pdf | probability_data_interpretation | Probability Data Interpretation - bag/diamond tables, missing probabilities, transfers and comparisons | 17 | OCR (image-only) | 0 | 17 |
| 106c989f-3149-4b18-8084-66e351389c37.pdf | probability_mains | Probability Mains - counting, conditional branching, committees and data sufficiency | 12 | OCR (image-only) | 0 | 12 |
| 245ea656-5a7f-4175-9bd5-b920dada2d07.pdf | boats_and_streams_data_interpretation | Boats and Streams Data Interpretation - upstream/downstream ratio tables, current-speed shares and derived trip times | 12 | OCR (image-only) | 0 | 12 |
| ce7bd62e-b49c-41dc-9441-23cfd6cc40f8.pdf | boats_and_streams_mains | Boats and Streams Mains - opposite-bank meetings, delayed starts, stream decomposition and speed ratios | 10 | OCR (image-only) | 0 | 10 |
| 207b546a-6d75-4080-8b00-114f9d7c977d.pdf | trains_data_interpretation | Trains Data Interpretation - length/coach tables, algebraic cells, tunnel crossing and passenger changes | 12 | OCR (image-only) | 0 | 12 |
| 98b402b7-32a0-4ce4-bed3-b059242c8e14.pdf | trains_mains | Trains Mains - station stops, delayed starts, crossing trains, changing speeds and quantity comparison | 9 | OCR (image-only) | 0 | 9 |
| Pipe and Cistern Data Interpretation 01  Class Notes.pdf | pipe_and_cistern_data_interpretation | Pipe and Cistern Data Interpretation - percentage/time tables, sequential and alternate operation, flow rates and leak pipes | 17 | OCR (image-only) | 0 | 17 |
| **Total** | | | **89** | | **0** | **89** |

## Why the PDF items were not imported verbatim

- The decks are slide images with worked examples; OCR of mathematical
  notation is not reliable enough to certify an answer.
- Printed options/keys were not treated as authoritative.
- All shipped items are original questions written for this bank.

The PDFs defined topic scope; difficulty follows the required chapter level.
The three Mains chapters are labelled `HARD` throughout. The four DI
chapters are deliberately Prelims-level (`EASY` and `MEDIUM` only). Every
shipped question is an original written for this bank, tagged
`source_type = ORIGINAL_VERIFIED`. `source_page` is a topic reference to
the reviewed slide range, not a copy citation; no item is a PYQ.

## Verification

`backend/verify_banking_maths_set9_questions.py` recomputes every answer
from `verification_data` without trusting the stored answer. It checks
four unique options, one correct option, answer/index agreement, explanation
consistency, units/rounding, valid difficulty, part sizes 15 / 20 / 30 / 55,
120 unique items per chapter and no PYQ flag. Result: **840 questions
checked, 0 failures**.

## Reconciliation with the final datasets

| Chapter | Dataset questions | Parts | Shipped ledger rows | PDF/OCR rows |
| --- | ---: | --- | ---: | ---: |
| Pipe and Cistern – Data Interpretation | 120 | 15 / 20 / 30 / 55 | 120 | 17 |
| Trains (Mains) | 120 | 15 / 20 / 30 / 55 | 120 | 9 |
| Trains – Data Interpretation | 120 | 15 / 20 / 30 / 55 | 120 | 12 |
| Boats and Streams (Mains) | 120 | 15 / 20 / 30 / 55 | 120 | 10 |
| Boats and Streams – Data Interpretation | 120 | 15 / 20 / 30 / 55 | 120 | 12 |
| Probability (Mains) | 120 | 15 / 20 / 30 / 55 | 120 | 12 |
| Probability – Data Interpretation | 120 | 15 / 20 / 30 / 55 | 120 | 17 |

No PDF item was copied into a dataset. The 840 shipped questions are
originals with a topic-page reference to the inspected sources; none is a
previous-year question.
