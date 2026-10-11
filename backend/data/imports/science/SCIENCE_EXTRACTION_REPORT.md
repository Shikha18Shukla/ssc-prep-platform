# Science PDF Extraction Report

Source set: 21 PDFs, 473 PDF pages. The first page in each source is the course/lecture listing; 452 remaining pages were carried into the OCR review queue.

OCR used Tesseract English on embedded page images. The original PDFs remain the source of truth. Transcripts retain original PDF page numbers and filenames.

## Current disposition

- Raw page-level OCR candidates: 452 (expected 452 question pages).
- Structured, source-verified question records: 102 (current queue; includes verified supplemental, Sound, Acid Base & Salt, one prepared Respiratory System record, and one prepared Carbon & Its Compound record).
- NEEDS_REVIEW: 333 (current queue).
- Rejected: 9 confirmed.
- Confirmed duplicate records: 9 (includes the excluded source-page supplement semantic duplicate).
- Import-ready: 102 verified CSV rows. This includes already-imported rows and prepared rows; it is not the count of unimported questions. The OCR queue is intentionally not in the production import schema.
- Production import events, batch contents, and live verification are recorded in SCIENCE_BATCH_MANIFEST.json.
- Exam names: none inferred. PYQ and difficulty values below are OCR labels only.

## OCR field extraction completeness (unverified candidates)

- Question text detected: 451/452.
- All four option fields detected: 315/452.
- Explanation text detected: 447/452.
- Correct option phrase mapped from OCR explanation: 126/452. The remaining answer markers may be present only as green highlighting and require visual review.
- Candidate completeness labeled FOUR_OPTIONS_AND_TEXT: 311; PARTIAL_OR_UNCERTAIN: 141.
These are parsing counts, not accuracy or approval counts. Per-record dispositions are in SCIENCE_REVIEW_DECISIONS.csv and the chapter review datasets.

## OCR label counts by source PDF

| Source PDF | Candidate pages | EASY | MEDIUM | HARD | Unread | PYQ labels |
|---|---:|---:|---:|---:|---:|---:|
| animal kingdom.pdf | 20 | 7 | 13 | 0 | 0 | 9 |
| brain and nervous system - science.pdf | 20 | 5 | 15 | 0 | 0 | 3 |
| cell -science.pdf | 40 | 9 | 27 | 4 | 0 | 22 |
| chemical reactions.pdf | 10 | 3 | 7 | 0 | 0 | 1 |
| chemistry in every day life.pdf | 30 | 8 | 22 | 0 | 0 | 6 |
| circulatory system - science.pdf | 20 | 3 | 17 | 0 | 0 | 9 |
| Digestive system - science.pdf | 30 | 7 | 22 | 1 | 0 | 16 |
| Disease.pdf | 20 | 2 | 18 | 0 | 0 | 2 |
| excretory system - science.pdf | 20 | 3 | 17 | 0 | 0 | 6 |
| Glands.pdf | 30 | 2 | 28 | 0 | 0 | 9 |
| gravitational work and energy.pdf | 30 | 2 | 25 | 3 | 0 | 12 |
| matter and atoms.pdf | 20 | 2 | 16 | 2 | 0 | 12 |
| metal and non metals.pdf | 20 | 3 | 16 | 1 | 0 | 9 |
| motion and force.pdf | 10 | 2 | 7 | 1 | 0 | 3 |
| nutrition - science.pdf | 20 | 5 | 15 | 0 | 0 | 2 |
| optics and human eye.pdf | 11 | 0 | 11 | 0 | 0 | 8 |
| periodic table.pdf | 10 | 2 | 8 | 0 | 0 | 3 |
| reproduction.pdf | 20 | 4 | 14 | 2 | 0 | 9 |
| respiratory system - science.pdf | 21 | 7 | 12 | 2 | 0 | 7 |
| sound.pdf | 20 | 5 | 14 | 1 | 0 | 11 |
| Tissues.pdf | 30 | 2 | 24 | 3 | 1 | 13 |
| TOTAL | 452 | 83 | 348 | 20 | 1 | 172 |

## PYQ years detected by OCR

| OCR year | Pages |
|---|---:|
| 2017 | 47 |
| 2018 | 13 |
| 2019 | 11 |
| 2020 | 6 |
| 2021 | 26 |
| 2022 | 31 |
| 2023 | 31 |
| 2024 | 4 |
| YEAR_UNREAD | 3 |

## Source-verified batch counts

| Chapter slug | Difficulty | Type | PYQ year | Records |
|---|---|---|---|---:|
| animal-kingdom | MEDIUM | PYQ | 2017 | 1 |
| animal-kingdom | MEDIUM | PYQ | 2021 | 1 |
| animal-kingdom | MEDIUM | PYQ | 2023 | 1 |
| brain-and-nervous-system | EASY | ORDINARY | — | 4 |
| brain-and-nervous-system | HARD | PYQ | 2017 | 1 |
| brain-and-nervous-system | MEDIUM | ORDINARY | — | 5 |
| brain-and-nervous-system | MEDIUM | PYQ | 2018 | 1 |
| brain-and-nervous-system | MEDIUM | PYQ | 2019 | 1 |
| brain-and-nervous-system | MEDIUM | PYQ | 2021 | 2 |
| circulatory-system | EASY | ORDINARY | — | 3 |
| circulatory-system | MEDIUM | ORDINARY | — | 8 |
| circulatory-system | MEDIUM | PYQ | 2017 | 2 |
| circulatory-system | MEDIUM | PYQ | 2019 | 1 |
| circulatory-system | MEDIUM | PYQ | 2021 | 1 |
| digestive-system | EASY | ORDINARY | — | 2 |
| digestive-system | EASY | PYQ | 2017 | 1 |
| digestive-system | HARD | ORDINARY | — | 2 |
| digestive-system | HARD | PYQ | 2023 | 1 |
| digestive-system | MEDIUM | ORDINARY | — | 1 |
| digestive-system | MEDIUM | PYQ | 2017 | 4 |
| digestive-system | MEDIUM | PYQ | 2022 | 1 |
| disease | EASY | ORDINARY | — | 4 |
| disease | MEDIUM | ORDINARY | — | 6 |
| disease | MEDIUM | PYQ | 2022 | 1 |
| excretory-system | EASY | PYQ | 2020 | 1 |
| excretory-system | MEDIUM | ORDINARY | — | 8 |
| excretory-system | MEDIUM | PYQ | 2022 | 1 |
| glands | MEDIUM | ORDINARY | — | 1 |
| glands | MEDIUM | PYQ | 2018 | 1 |
| tissues | EASY | ORDINARY | — | 5 |
| tissues | EASY | PYQ | 2022 | 1 |
| tissues | MEDIUM | ORDINARY | — | 1 |
| tissues | MEDIUM | PYQ | 2017 | 1 |

Source-specific chapter assignments and unresolved mapping notes are recorded in SCIENCE_CHAPTER_MAPPING_REVIEW.md and the chapter review datasets.


## Batch audit snapshot

Reconciled 2026-10-10: the approved 18-row source-page-supplement batch and seven-row follow-up batch were imported and verified. Current OCR queue dispositions are 102 VERIFIED, 333 NEEDS_REVIEW, 8 REJECTED, and 9 DUPLICATE. A read-only database query confirmed 133 active questions total and 100 Science questions across 28 chapters; per-chapter values are in SCIENCE_COVERAGE_MATRIX.md. Exact import times for older batches are UNKNOWN. Earlier batch details and Glands source-review decisions remain in the chapter datasets and SCIENCE_BATCH_READINESS_AUDIT.md.

## Cross-corpus source review — 2026-10-10

Visual inspection confirmed one prepared ordinary Respiratory System row from `circulatory system - science.pdf` p. 17. Its global review decision is VERIFIED, but it is not imported and the live chapter remains empty. The misleading `respiratory system - science.pdf` contains 19 distinct Brain & Nervous System questions, one Skeleton question, and one repeated Brain question. Cross-corpus review also verified one ordinary Carbon & Its Compound candidate from `excretory system - science.pdf` p. 6; its live chapter remains empty. A saponification candidate from `chemical reactions.pdf` p. 8 remains pending because its explanation is clipped. No verified Physics Revision candidate was found; specific physics items remain in their matching chapters.
