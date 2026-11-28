# Banking Maths Set 8 - Progress Report

Status: **complete**.

## Generation and pre-import phase

- Read-only catalog and DB checks passed: 12 exact active target chapters, zero
  questions, Clerk subject `2772e1ec-ff23-4735-ac5f-e52f41be59dd`, PO subject
  `99de33c1-5926-40e4-89d5-2f61cec40dd4`.
- Running backend confirmed on `127.0.0.1:5432/ssc_prep`; no remote DB or `.env`
  changes.
- All seven supplied PDFs inspected: 102 pages, all image-only, OCR at 150 dpi.
- Content-based PDF mapping finalized; four provisional filename-based
  assumptions corrected. See `reports/banking_maths_set8_pdf_mapping.md`.
- Six builder modules and six independent formula modules created; each passed
  120/120 self-tests before generation.
- 720 original questions generated: 120 per chapter, 24 families x 5 variants.
- Independent verifier passed: exact 20-field schema, deterministic IDs,
  15/20/30/55 parts, four distinct options, answer/index agreement, explanations,
  provenance, HARD-only Mains, EASY/MEDIUM DI, inline DI data.
- Dedup passed: 0 exact/normalized/number-masked/lexical/semantic collisions
  against Sets 1-7 (4,800 questions) or the live DB excluding this batch.
- Source ledger valid: 102 PDF/OCR page rows + 720 shipped rows = 822 rows.
- Frontend `mathsChapterKeys` extended with six Set 8 mappings; Set 7 mappings
  left intact. `npm run build` passed.
- Live DB before snapshot captured; importer dry-run passed 12 chapters /
  1,440 planned rows with no writes.

## Import and functional phase

- Scratch baseline restore completed and matched the pre-import live state.
- Importer refused scratch and remote-like targets before live use.
- Live transactional import inserted exactly 1,440 rows: 120 per exam/chapter.
- Idempotency replay inserted 0 rows, updated the same 1,440 deterministic IDs,
  and left IDs and chapter/section assignments unchanged.
- After snapshot and reconciliation confirmed only `questions` (+1,440) and
  `question_options` (+5,760) changed.
- Scratch availability checks passed for all 48 part selections.
- Scratch `create_test` checks passed for all 48 sections with correct durations.
- DI rendering checks passed for all 16 DI sections / 480 questions / 1,920 options.
- Unrelated-data integrity confirmed every other table byte-equivalent to the
  pre-import baseline.
- Combined Set 8 validation passed.
