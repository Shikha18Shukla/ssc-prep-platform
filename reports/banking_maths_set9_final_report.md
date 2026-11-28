# Banking Maths Set 9 - Final Report

Status: **complete**. All seven chapters were generated, independently verified,
deduplicated, imported into the verified local `ssc_prep` database, exercised
through the real test service on a scratch copy, and confirmed in the frontend.
No commit or push was made.

## 1. Database target and safety

- Database used: `postgresql://***:***@127.0.0.1:5432/ssc_prep` (masked).
- The running backend and every importer/check process used this same local
  target through process-only environment overrides.
- Remote Neon/production was never contacted. `.env` was not modified; no
  credential appears in any report.
- The importer refused scratch/remote-looking targets in preflight before the
  live run.
- All 14 target chapters were reconfirmed active, correctly named, under
  `math-quant`, and at zero questions immediately before import.

## 2. Exact catalog mapping

Exam IDs:

| Exam | ID |
| --- | --- |
| Banking Clerk | `6b2645e2-c596-4455-b449-71474971a11b` |
| Banking PO | `2262a4f9-eb9b-4228-b00a-337ca591192f` |

Subject IDs:

| Exam / subject | ID |
| --- | --- |
| Banking Clerk / math-quant | `2772e1ec-ff23-4735-ac5f-e52f41be59dd` |
| Banking PO / math-quant | `99de33c1-5926-40e4-89d5-2f61cec40dd4` |

Chapters (required order). Section keys are
`banking_clerk_maths_<chapter_key>_part_<1..4>` and
`banking_po_maths_<chapter_key>_part_<1..4>`.

| # | Chapter | Chapter key | Clerk chapter ID | PO chapter ID |
| ---: | --- | --- | --- | --- |
| 1 | Pipe and Cistern - Data Interpretation | `pipe_and_cistern_data_interpretation` | `e721bca9-b0a7-4a58-8ff7-19ace7c5181d` | `e972e9b1-cc3d-4027-a6f8-72ef551fb89c` |
| 2 | Trains (Mains) | `trains_mains` | `d4536a1e-9bca-4b7f-a164-765261055639` | `42b0ffd2-63bd-4c5f-acfc-5cffee211e85` |
| 3 | Trains - Data Interpretation | `trains_data_interpretation` | `a860fd97-1f72-4a04-a2f8-6879e5a8827c` | `83a1f672-9718-40a0-bd4c-3cf8ef7b65fa` |
| 4 | Boats and Streams (Mains) | `boats_and_streams_mains` | `4e4348d8-24f7-4bfa-869b-8d2c7ccaf39f` | `6dc40aaf-9ec0-4466-995a-f841825c9bf5` |
| 5 | Boats and Streams - Data Interpretation | `boats_and_streams_data_interpretation` | `04572173-26ab-4ea7-8a43-5b88d6843304` | `aa2f8a4c-1ce2-4fe5-b3eb-6c75a46c9327` |
| 6 | Probability (Mains) | `probability_mains` | `13f877fc-bd67-416a-9d6d-368e1f7e3245` | `b9c4dc55-7f29-4b2f-abf3-13739a1d9ed3` |
| 7 | Probability - Data Interpretation | `probability_data_interpretation` | `40ab1ced-e54b-4b01-9252-e691da893c66` | `7d33a530-4d6e-4c33-b5e0-b2fd318d3373` |

Live row IDs are deterministic:
`uuid.uuid5(uuid.NAMESPACE_URL, f"https://ssc-prep.local/banking-maths/{exam_slug}/{item_id}")`.
Each exam/chapter has `15 / 20 / 30 / 55` questions in parts 1-4 (120 total).

## 3. Generation and verification

- 840 unique original questions: 120 per chapter, 24 families x 5 variants.
- Parts: 15 / 20 / 30 / 55. Durations: 630 / 840 / 1260 / 2310 seconds.
- Mains chapters: HARD only, with multi-step Banking PO Mains patterns.
- DI chapters: EASY/MEDIUM only, with shared, internally consistent inline data.
- Independent verifier recomputed every answer from `verification_data.inputs`
  without reading the stored answer: `verified 840 questions across 7 chapters`
  / `ALL CHECKS PASSED`.
- Four distinct options, matching answer key, clear explanations,
  `ORIGINAL_VERIFIED`, `VERIFIED`, and null `exam_year` on all items.
- See `reports/banking_maths_set9_answer_verification.md`.

## 4. Sources and deduplication

- Seven PDFs, 89 pages, all image-only and OCR'd; mapping based on extracted
  slide content, not filenames. No exam year/source page was invented.
- Source ledger: 929 rows = 89 PDF/OCR pages + 840 shipped questions.
  See `reports/banking_maths_set9_source_ledger.csv`,
  `reports/banking_maths_set9_source_ledger.md`, and
  `reports/banking_maths_set9_pdf_mapping.md`.
- Dedup screened 840 new questions against 5,520 Set 1-8 questions and 22,372
  existing DB questions: 0 exact, 0 normalized, 0 lexical, 0 semantic flags,
  0 cross-chapter templates. The 168 repeated masked templates are the expected
  five variants within each of the 168 families.
  See `reports/banking_maths_set9_dedup_report.md`.

## 5. Import and reconciliation

- Before snapshot: `questions=22372`, `question_options=95613`, Set 9 rows `0`.
- Dry-run/preflight: `14 target chapters, 1680 planned questions`, no writes.
- Live import: `1680 inserted, 0 updated, 1680 total rows`.
- Replay: `0 inserted, 1680 updated, 1680 total rows`.
- After snapshot: `questions=24052`, `question_options=102333`, Set 9 rows
  `1680`.
- Only `questions` (+1,680) and `question_options` (+6,720) changed. All other
  tables, including users, attempts, answers, progress, and Banking Others, are
  unchanged.
- See `reports/banking_maths_set9_db_before.json`,
  `reports/banking_maths_set9_db_after.json`,
  `reports/banking_maths_set9_db_reconciliation.md`, and
  `reports/banking_maths_set9_data_integrity_report.md`.

## 6. Scratch functional verification

All functional checks ran against restored local scratch copies; live was not
written.

| Check | Result | Evidence |
| --- | --- | --- |
| `get_test_availability` | 56/56 sections | `banking_maths_set9_availability_scratch_report.md` |
| `create_test` | 56/56 sections, correct durations | `banking_maths_set9_create_test_report.md` |
| DI rendering | 32/32 sections, 960 questions, 3,840 options | `banking_maths_set9_di_rendering_report.md` |
| Unrelated-data integrity | 19/19 tables hash-identical | `banking_maths_set9_data_integrity_report.md` |

Scratch baseline/restore details are in
`reports/banking_maths_set9_scratch_baseline.md`.

## 7. Frontend and UI

- Only the seven missing frontend mappings were added in
  `frontend/src/pages/BankingPage.tsx` (19 inserted lines, no Set 1-8 edits).
- Production build passed.
- Fresh-client browser check with cache bypass showed all seven target chapters
  as `120 questions · 4 parts` under both Banking Clerk and Banking PO.
- The temporary UI token file was deleted; no token is stored in the repo.
- See `reports/banking_maths_set9_ui_report.md`.

## 8. Build and tests

- Static compile and stale-constant scan passed; `git diff --check` clean.
- Relevant backend pytest suite: **165 passed**.
- Full suite: 484 passed, 1 transient failure in an unrelated Google OAuth test;
  the isolated rerun of that exact test passed and both auth files are
  unmodified from HEAD.
- See `reports/banking_maths_set9_test_report.md`.

## 9. Git preservation

- Baseline status file: 184 entries, SHA-256
  `CEB045BD880DB0690B39FE5A2DE4330744FB440DCC9F8CDCFBCD76B2DDEDC214`.
- Current status: 222 entries = all 184 baseline entries + 38 Set 9 additions;
  no baseline line is missing. The 47 pre-existing staged entries are unchanged,
  and no new entry is staged.
- No `git add`, commit, push, remote DB access, `.env` edit, Set 1-8 overwrite,
  or unrelated cleanup was performed.

## 10. Summary

All Set 9 requirements pass: 840 verified original questions, 1,680 live rows,
6,720 options, 56 availability combinations, 56 create-test paths, 32 DI
sections, frontend counts for both exams, clean reconciliation, preserved Git
state, and a complete report package.

Status: **complete**.
