# Banking Maths Set 9 - Source PDF Mapping

Seven PDFs were supplied. All 89 pages were inspected with PyMuPDF. Every page
was image-only and was rendered/OCR'd at 150 dpi. Chapter assignment was made
from extracted slide titles and substantive content, not from filenames. Several
files are UUID-named, and recap slides naming another chapter were not treated as
evidence. Printed questions and answer keys were treated as untrusted reference
material and were never copied. No exam year was inferred from the slides, and
no source page was invented.

## Final content-based mapping

| PDF | Pages | Extracted title/topic | Assigned target chapter | Pages cited |
| --- | ---: | --- | --- | --- |
| `f9d83e47-9397-4b2e-99aa-92595ea4647c.pdf` | 17 | Probability Data Interpretation - bag/diamond tables, missing probabilities, transfers and comparisons | `probability_data_interpretation` | OCR-derived topic reference |
| `106c989f-3149-4b18-8084-66e351389c37.pdf` | 12 | Probability Mains - counting, conditional branching, committees and data sufficiency | `probability_mains` | OCR-derived topic reference |
| `245ea656-5a7f-4175-9bd5-b920dada2d07.pdf` | 12 | Boats and Streams Data Interpretation - upstream/downstream ratio tables, current-speed shares and derived trip times | `boats_and_streams_data_interpretation` | OCR-derived topic reference |
| `ce7bd62e-b49c-41dc-9441-23cfd6cc40f8.pdf` | 10 | Boats and Streams Mains - opposite-bank meetings, delayed starts, stream decomposition and speed ratios | `boats_and_streams_mains` | OCR-derived topic reference |
| `207b546a-6d75-4080-8b00-114f9d7c977d.pdf` | 12 | Trains Data Interpretation - length/coach tables, algebraic cells, tunnel crossing and passenger changes | `trains_data_interpretation` | OCR-derived topic reference |
| `98b402b7-32a0-4ce4-bed3-b059242c8e14.pdf` | 9 | Trains Mains - station stops, delayed starts, crossing trains, changing speeds and quantity comparison | `trains_mains` | OCR-derived topic reference |
| `Pipe and Cistern Data Interpretation 01  Class Notes.pdf` | 17 | Pipe and Cistern Data Interpretation - percentage/time tables, sequential and alternate operation, flow rates and leak pipes | `pipe_and_cistern_data_interpretation` | OCR-derived topic reference |

Totals: **7 PDFs, 89 pages, 89 OCR pages, 0 text-layer pages**. Branding on the
decks reads `BANKING WALLAH` / `By- SUMIT JAISWAL Sir`. Where legible, lecture
numbers are `01`; a second lecture number was unclear and was not asserted. A
`2024` mark on one Pipe/Cistern slide had unclear context and was not used as an
exam year.

## Use of the source material

- The PDFs defined topic scope and the kinds of data tables used in DI items.
- Every shipped item is an original question written for this bank.
- `source_type` is `ORIGINAL_VERIFIED`; `exam_year` is null.
- `source_page` is a topic reference to the reviewed slide range, not a claim
  that a question was copied from that page.
- Full page-level and shipped-question detail is in
  `reports/banking_maths_set9_source_ledger.csv` (929 rows: 89 PDF/OCR + 840
  shipped).

## Reconciliation

| Chapter | Dataset questions | Ledger shipped rows | Source PDF/OCR rows |
| --- | ---: | ---: | ---: |
| Pipe and Cistern - Data Interpretation | 120 | 120 | 17 |
| Trains (Mains) | 120 | 120 | 9 |
| Trains - Data Interpretation | 120 | 120 | 12 |
| Boats and Streams (Mains) | 120 | 120 | 10 |
| Boats and Streams - Data Interpretation | 120 | 120 | 12 |
| Probability (Mains) | 120 | 120 | 12 |
| Probability - Data Interpretation | 120 | 120 | 17 |

No PDF question was imported verbatim.
