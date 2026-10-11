# Science PDF Quality Report

## Checks completed

- All source files were readable; all pages are image-based with no extractable PDF text.
- OCR was run on each source page after the title/listing page; source filenames and physical PDF page numbers are preserved.
- The page-2 sample for each PDF was compared against its title. Multiple files contain questions from other chapters, so no file-wide chapter assignment was accepted.
- OCR-prefix duplicate detection flagged 17 candidate pairs at a 0.90 similarity threshold; 7 pairs are confirmed and 10 remain unresolved. 9 source records are confirmed duplicates after visual/content comparison.
- The seven-row approved follow-up passed a live-database importer dry-run (7 would import, 0 rejects, 0 duplicates, 0 errors) before its transactional import. The existing-data fingerprint was identical before and after import.

## Not yet verified

- Remaining 334 NEEDS_REVIEW pages still need complete option/order and answer-marker review.
- Scientific correctness, explanation consistency, and supported difficulty/PYQ labels remain unverified for those pending pages.
- Remaining question-level mappings, exact/semantic duplicates, and per-chapter coverage are documented in the review queue and chapter reports.

## Release decision

There are 100 verified importer-compatible rows across source-verified chapter batches. 334 queue rows remain NEEDS_REVIEW; 9 are REJECTED and 9 are confirmed duplicate records. Ten OCR duplicate pairs remain unresolved. The approved 18-row supplement and seven-row follow-up batch are imported. The follow-up contained five Sound rows and two Acid Base & Salt rows; no verified rows remain unimported. See SCIENCE_CHAPTER_MAPPING_REVIEW.md, SCIENCE_DUPLICATE_REVIEW.md, and SCIENCE_COVERAGE_MATRIX.md.

The current database contains 133 active questions total / 100 Science across 28 chapters. All seven rows approved for the follow-up import were committed and verified; no additional candidate was imported. The approved import events are listed in SCIENCE_BATCH_MANIFEST.json.


## Batch audit snapshot

Reconciled 2026-10-10: the latest read-only database snapshot is 133 active questions total / 100 Science across 28 chapters. The approved 18-row supplement and seven-row follow-up import were verified. Test selection offers exact eligible pools when their nonstandard size is at most 25. Focused importer-candidate and isolated service regression results are recorded in SCIENCE_BATCH_READINESS_AUDIT.md. No HTTP/browser end-to-end flow is claimed.
