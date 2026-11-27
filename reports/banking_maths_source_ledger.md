# Banking Maths Question Bank - Source and Verification Ledger

## Scope

Five Banking Maths chapters were filled for **Banking Clerk** and **Banking PO**
only. The entirely empty `Banking Others` exam was deliberately left untouched.

| Chapter | Dataset | Questions | Parts |
| --- | --- | ---: | --- |
| Vedic Maths Tricks - Calculation Techniques | `data/banking_maths_vedic_calculation_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Simplification | `data/banking_maths_simplification_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Approximation | `data/banking_maths_approximation_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Missing Number Series | `data/banking_maths_missing_number_series_questions.json` | 120 | 15 / 20 / 30 / 55 |
| Wrong Number Series | `data/banking_maths_wrong_number_series_questions.json` | 120 | 15 / 20 / 30 / 55 |

## Provenance

The 17 source PDFs are PW Banking Wallah class-note decks (17-42 pages each). They are image-only lecture slides with
theory and a limited number of five-option MCQs, so they cannot supply 100
four-option questions per chapter. They were inspected directly (text-layer
inventory plus OCR and rendered-page review) and used as the topic/technique
scope for this bank.

Every question in this bank is an **original question written for this bank**,
not an extracted PDF MCQ and **not a previous-year question**. Each item is
tagged `source_type = ORIGINAL_VERIFIED` and carries a `provenance_note` saying
so. The `source_page` field is a *topic reference* to the class-notes pages that
teach the technique, not a claim that the question was copied from that page.

## Verification

`backend/generate_banking_maths_questions.py` computes every answer in Python
from a seeded generator. `backend/verify_banking_maths_questions.py` then
recomputes every answer from the stored `verification_data` without trusting
the generator's answer field, re-checks every series rule, and validates:

- exactly four unique options per question;
- `correct_option` (A-D) points at `correct_answer`;
- one correct option only;
- a non-empty explanation;
- difficulty in EASY / MEDIUM / HARD;
- part sizes 15 / 20 / 30 / 55;
- 120 unique question texts per chapter and no duplicates across chapters.

Verification result: **600 questions checked, 0 failures**.

## Chapter detail

### Vedic Maths Tricks - Calculation Techniques

- Dataset: `data/banking_maths_vedic_calculation_questions.json`
- Questions: 120 (parts: {1: 15, 2: 20, 3: 30, 4: 55})
- Difficulty: EASY 24, MEDIUM 34, HARD 62
- Verification: independent arithmetic recomputation, 0 failures
- Source type: `ORIGINAL_VERIFIED` (not PYQ, not an extracted PDF MCQ)

Topic references used while writing the chapter:

- Vedic Maths 01, pp. 10-14 (4 questions)
- Vedic Maths 01, pp. 5-9 (5 questions)
- Vedic Maths 02, pp. 10-16 (13 questions)
- Vedic Maths 02, pp. 4-9 (3 questions)
- Vedic Maths 03, pp. 10-14 (5 questions)
- Vedic Maths 03, pp. 4-9 (10 questions)
- Vedic Maths 04, pp. 11-16 (3 questions)
- Vedic Maths 04, pp. 17-22 (3 questions)
- Vedic Maths 04, pp. 4-10 (12 questions)
- Vedic Maths 05, pp. 19-26 (4 questions)
- Vedic Maths 05, pp. 27-32 (4 questions)
- Vedic Maths 05, pp. 33-38 (10 questions)
- Vedic Maths 05, pp. 4-18 (25 questions)
- Vedic Maths 06, pp. 11-14 (3 questions)
- Vedic Maths 06, pp. 15-19 (6 questions)
- Vedic Maths 06, pp. 4-10 (10 questions)

### Simplification

- Dataset: `data/banking_maths_simplification_questions.json`
- Questions: 120 (parts: {1: 15, 2: 20, 3: 30, 4: 55})
- Difficulty: EASY 25, MEDIUM 32, HARD 63
- Verification: independent arithmetic recomputation, 0 failures
- Source type: `ORIGINAL_VERIFIED` (not PYQ, not an extracted PDF MCQ)

Topic references used while writing the chapter:

- Simplifications 01, pp. 14-18 (4 questions)
- Simplifications 01, pp. 19-23 (3 questions)
- Simplifications 01, pp. 5-13 (14 questions)
- Simplifications 02, pp. 13-18 (11 questions)
- Simplifications 02, pp. 19-25 (17 questions)
- Simplifications 02, pp. 4-12 (14 questions)
- Simplifications 03, pp. 11-16 (14 questions)
- Simplifications 03, pp. 17-19 (10 questions)
- Simplifications 03, pp. 4-10 (10 questions)
- Simplifications 04, pp. 11-16 (11 questions)
- Simplifications 04, pp. 4-10 (12 questions)

### Approximation

- Dataset: `data/banking_maths_approximation_questions.json`
- Questions: 120 (parts: {1: 15, 2: 20, 3: 30, 4: 55})
- Difficulty: EASY 24, MEDIUM 27, HARD 69
- Verification: independent arithmetic recomputation, 0 failures
- Source type: `ORIGINAL_VERIFIED` (not PYQ, not an extracted PDF MCQ)

Topic references used while writing the chapter:

- Approximations 01, pp. 10-14 (17 questions)
- Approximations 01, pp. 15-17 (3 questions)
- Approximations 01, pp. 4-9 (24 questions)
- Approximations 02, pp. 14-19 (9 questions)
- Approximations 02, pp. 15-19 (4 questions)
- Approximations 02, pp. 4-8 (15 questions)
- Approximations 02, pp. 9-13 (10 questions)
- Approximations 02, pp. 9-14 (6 questions)
- Approximations 03, pp. 11-16 (3 questions)
- Approximations 03, pp. 14-20 (8 questions)
- Approximations 03, pp. 17-20 (5 questions)
- Approximations 03, pp. 4-10 (9 questions)
- Approximations 03, pp. 4-8 (4 questions)
- Approximations 03, pp. 9-13 (3 questions)

### Missing Number Series

- Dataset: `data/banking_maths_missing_number_series_questions.json`
- Questions: 120 (parts: {1: 15, 2: 20, 3: 30, 4: 55})
- Difficulty: EASY 23, MEDIUM 27, HARD 70
- Verification: independent arithmetic recomputation, 0 failures
- Source type: `ORIGINAL_VERIFIED` (not PYQ, not an extracted PDF MCQ)

Topic references used while writing the chapter:

- Missing Number Series 01, pp. 13-20 (8 questions)
- Missing Number Series 01, pp. 21-28 (16 questions)
- Missing Number Series 01, pp. 29-38 (19 questions)
- Missing Number Series 01, pp. 4-12 (21 questions)
- Missing Number Series 02, pp. 11-16 (32 questions)
- Missing Number Series 02, pp. 17-23 (15 questions)
- Missing Number Series 02, pp. 4-10 (9 questions)

### Wrong Number Series

- Dataset: `data/banking_maths_wrong_number_series_questions.json`
- Questions: 120 (parts: {1: 15, 2: 20, 3: 30, 4: 55})
- Difficulty: EASY 19, MEDIUM 31, HARD 70
- Verification: independent arithmetic recomputation, 0 failures
- Source type: `ORIGINAL_VERIFIED` (not PYQ, not an extracted PDF MCQ)

Topic references used while writing the chapter:

- Wrong Number Series 01, pp. 15-21 (13 questions)
- Wrong Number Series 01, pp. 4-8 (14 questions)
- Wrong Number Series 01, pp. 9-14 (23 questions)
- Wrong Number Series 02, pp. 14-21 (29 questions)
- Wrong Number Series 02, pp. 4-8 (13 questions)
- Wrong Number Series 02, pp. 9-13 (28 questions)

## Source PDF inventory

The PDFs were inventoried page by page in `tmp/pdf_text/inventory.json`;
rendered contact sheets are in `tmp/sheets/`. All 17 decks were also passed
through OCR (`rapidocr_onnxruntime`) with per-page output in `tmp/ocr/` to
confirm the taught techniques and the five-option MCQ format. No PDF was
modified, renamed, moved or deleted.

| PDF | Pages | Text-layer characters |
| --- | ---: | ---: |
| Approximations 01_Class Notes.pdf | 17 | 21 |
| Approximations 02_Class Notes.pdf | 19 | 28 |
| Approximations 03_Class Notes.pdf | 20 | 88 |
| Missing Number Series 01_Class Notes.pdf | 38 | 70 |
| Missing Number Series 02_Class Notes.pdf | 23 | 77 |
| Simplifications 01_Class Notes.pdf | 23 | 20 |
| Simplifications 02_Class Notes.pdf | 25 | 20 |
| Simplifications 03 Class Notes.pdf | 19 | 6 |
| Simplifications 04_Class Notes.pdf | 16 | 6 |
| Vedic Maths Tricks - Calculations Techniques 01_Class Notes.pdf | 20 | 140 |
| Vedic Maths Tricks - Calculations Techniques 02_Class Notes.pdf | 20 | 200 |
| Vedic Maths Tricks - Calculations Techniques 03 _ Class Notes.pdf | 14 | 154 |
| Vedic Maths Tricks - Calculations Techniques 04_Class Notes.pdf | 28 | 207 |
| Vedic Maths Tricks - Calculations Techniques 05_Class Notes.pdf | 42 | 207 |
| Vedic Maths Tricks - Calculations Techniques 06_Class Notes.pdf | 19 | 155 |
| Wrong Number Series 01_Class Notes.pdf | 14 | 73 |
| Wrong Number Series 02_Class Notes.pdf | 21 | 59 |

The near-empty text layer confirms these are image-only slide decks, which is
why OCR plus rendered-page review was used and why the final bank is built from
independently verified original questions rather than noisy OCR transcriptions.

## Reproduction

```powershell
# DATABASE_URL is supplied through the process environment for an isolated local database
python backend/generate_banking_maths_questions.py
python backend/verify_banking_maths_questions.py
python backend/import_banking_maths_questions.py --dry-run
python backend/import_banking_maths_questions.py
python backend/validate_banking_maths_bank.py
python backend/report_banking_maths_bank.py
```
