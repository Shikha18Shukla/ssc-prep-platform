# Banking Maths Set 9 - Progress Report

Status: **complete**.

## Scope

Seven chapters were filled for Banking Clerk and Banking PO only:

1. Pipe and Cistern - Data Interpretation
2. Trains (Mains)
3. Trains - Data Interpretation
4. Boats and Streams (Mains)
5. Boats and Streams - Data Interpretation
6. Probability (Mains)
7. Probability - Data Interpretation

Banking Others was not touched.

## Pre-import phase

- Read-only catalog/DB checks confirmed all 14 target chapter rows (7 per exam)
  exist exactly once, are active, are under `math-quant`, and had `0` questions.
- Exam IDs: Clerk `6b2645e2-c596-4455-b449-71474971a11b`, PO
  `2262a4f9-eb9b-4228-b00a-337ca591192f`. Subject IDs: Clerk
  `2772e1ec-ff23-4735-ac5f-e52f41be59dd`, PO
  `99de33c1-5926-40e4-89d5-2f61cec40dd4`.
- All seven supplied PDFs were inspected: 89 pages, all image-only, OCR'd at
  150 dpi. Chapter mapping came from slide content, not filenames; no exam year
  was invented. See `reports/banking_maths_set9_pdf_mapping.md`.
- Seven builders, shared bank helpers, family names, formulas and independent
  calculation helpers were added under `backend/maths_set9/`.
- 840 original questions were generated (120 per chapter; 24 families x 5
  variants per chapter) with parts 15/20/30/55.
- Independent verifier: `verified 840 questions across 7 chapters` /
  `ALL CHECKS PASSED`. See `reports/banking_maths_set9_answer_verification.md`.
- Source ledger: 929 rows (89 PDF/OCR + 840 shipped);
  `ledger valid: 89 pages inspected, 840 shipped questions`.
- Dedup: 0 exact/normalized matches, 0 lexical/semantic flags against Sets 1-8
  or the DB, 0 cross-chapter templates, 168 expected within-family variant
  repeats. See `reports/banking_maths_set9_dedup_report.md`.
- Live before snapshot: `questions=22372`, `question_options=95613`,
  `set9=0`.
- Scratch baseline dump captured and both scratch DBs restored successfully.
- Importer dry-run/preflight: `14 target chapters, 1680 planned questions`,
  no database changes.

## Import phase

- Live transactional import: `1680 inserted, 0 updated, 1680 total rows`.
- Replay: `0 inserted, 1680 updated, 1680 total rows` - deterministic IDs and
  idempotency confirmed.
- Every chapter/exam combination showed part counts `{1: 15, 2: 20, 3: 30,
  4: 55}`.
- Live after snapshot: `questions=24052`, `question_options=102333`,
  `set9=1680`.
- Reconciliation: only `questions` (+1,680) and `question_options` (+6,720)
  changed. See `reports/banking_maths_set9_db_reconciliation.md`.

## Post-import verification

- Combined validator: 840 dataset questions, 56/56 sections, duration rule
  verified, `ALL CHECKS PASSED`.
- Unrelated-data integrity: all 19 unrelated tables hash-identical to the
  pre-import baseline; `ALL UNRELATED DATA UNCHANGED`.
- Scratch-only availability: 56/56 sections, `ALL CHECKS PASSED`.
- Scratch-only `create_test`: 56/56 sections, 56 attempts, durations matched.
- Scratch-only DI rendering: 32/32 DI sections, 960 questions, 3,840 options,
  all questions self-contained with inline data.
- Frontend: only seven missing mappings added in `BankingPage.tsx`; production
  build passed; UI on a fresh client showed `120 questions · 4 parts` for all
  seven chapters under both Banking Clerk and Banking PO.

## Final checks

- Static compile/stale-constant scan passed; `git diff --check` clean.
- Relevant backend pytest suite: 165 passed. Full suite had one unrelated flaky
  Google OAuth failure that passed on isolated rerun; auth files are unmodified.
- Git baseline had 184 entries; current status contains every baseline entry
  plus only Set 9 files and the frontend mapping edit. No staging, commit,
  push, remote DB contact, `.env` edit, or unrelated cleanup occurred.

See `reports/banking_maths_set9_final_report.md` for the consolidated result.
