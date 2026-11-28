# Banking Maths Set 8 - Source PDF Mapping

Seven PDFs were supplied. All 102 pages were inspected with PyMuPDF; every page
was image-only and was OCR'd at 150 dpi. Chapter assignment was made from the
extracted slide titles/content, not from filenames. Printed questions and answer
keys were treated as untrusted reference data and were not copied.

## Final content-based mapping

| PDF | Pages | Extracted title/topic | Assigned target chapter | Pages cited |
| --- | ---: | --- | --- | --- |
| `87fda602-e97e-4aa7-90cc-9f316d0af672.pdf` | 13 | `TIME & WORK MAINS`, Lecture No. 01 | `time_and_work_mains` | 4-5, 6-7, 8-9, 10-11 |
| `ce788d06-e730-4963-97ca-208b2af36699 (2).pdf` | 11 | `TIME & WORK DI MAINS`, Lecture No. 01 | `time_and_work_data_interpretation` | 4-5, 6-7, 8-9, 10-11 |
| `0da2c67a-4985-4a86-9772-b0c4b826b42f.pdf` | 15 | `TIME SPEED & DISTANCE MAINS`, Lecture No. 01 | `time_speed_and_distance_mains` | 3-5, 6-8, 9-11, 12-14 |
| `Simple and Compound Interest Mains 01  Class Notes.pdf` | 12 | `Simple and Compound Interest Mains`, Lecture No. 01 | `simple_and_compound_interest_mains` | 3-5, 6-8, 9-11, 3-12 |
| `f5b22d88-8d5a-494e-b7b2-9e5b1b05d260.pdf` | 20 | `Simple and Compound Interest Data Interpretation`, Lecture No. 01 | `simple_and_compound_interest_data_interpretation` | 2-4, 5-7, 8-10, 11-13 |
| `Pipe and Cistern Mains 01 _Class Notes.pdf` | 15 | `PIPE & CISTERN MAINS`, Lecture No. 01 | `pipe_and_cistern_mains` | 2-4, 5-8, 9-12, 13-14 |
| `Time Speed and Distance Mains 02 Class Notes.pdf` | 16 | `TIME SPEED & DISTANCE DI MAINS`, Part 02 | **Unmapped extra reference** - no matching target chapter | none |

## Filename corrections

The following provisional filename-based assumptions were corrected after OCR:

1. `87fda602-e97e-4aa7-90cc-9f316d0af672.pdf` was initially treated as an
   unrelated/partnership-style extra deck. Its title page and every topic slide
   identify it as **Time & Work Mains**, so it is the source for
   `time_and_work_mains`.
2. `ce788d06-e730-4963-97ca-208b2af36699 (2).pdf` was initially assigned to
   Time and Work Mains. The extracted topic is **Time & Work DI Mains**, so it is
   the source for `time_and_work_data_interpretation`.
3. `0da2c67a-4985-4a86-9772-b0c4b826b42f.pdf` was initially assigned to Time
   and Work DI. It is actually **Time Speed & Distance Mains, Lecture 01**, so it
   is the source for `time_speed_and_distance_mains`.
4. `Time Speed and Distance Mains 02 Class Notes.pdf` is actually **Time Speed &
   Distance DI Mains, Part 02**. There is no Time/Speed/Distance DI target
   chapter in this task, so it was inspected and recorded but not shipped from.

## Usage rules

- All shipped questions are original, `ORIGINAL_VERIFIED` / `VERIFIED`, with
  `exam_year = null` and no PYQ flags.
- `source_page` is a topic-scope reference only, never a claim that a question
  was copied from that page.
- No printed MCQ, printed option set, or printed answer key was imported.
- Full page-by-page and shipped-row detail is in
  `reports/banking_maths_set8_source_ledger.csv`; the reconciliation is in
  `reports/banking_maths_set8_source_ledger.md`.
