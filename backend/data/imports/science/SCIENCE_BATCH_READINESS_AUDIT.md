# Science Batch Readiness Audit — 2026-10-10

## Current live database snapshot

Read-only queries against the configured database confirm **140 active questions overall**, including **107 Science questions in the Science subcategory**, across all **28 Science chapters**. There are 560 active options. The approved source-derived gap-fill added 2 rows (Respiratory System 1 ordinary; Carbon & Its Compound 1 ordinary). The subsequent original Physics Revision batch added 5 ordinary questions. No PYQ metadata was assigned to the original questions. Exact chapter totals and selectable lengths are in `SCIENCE_COVERAGE_MATRIX.md`.

The two prepared source rows passed a combined live importer dry-run (2 accepted; 0 rejected, duplicates, or errors), then the existing transactional importer inserted exactly 2. The five-question Physics Revision CSV passed a separate live dry-run (5 accepted; 0 rejected, duplicates, or errors), then one transaction inserted exactly 5. Read-only post-import queries confirmed all rows active, mapped to their intended chapters, classified ordinary, and populated with four options and exactly one correct option. The imported source provenance and original-question labels are in the CSV `source` fields.

## Current chapter and mode availability

The live test-availability service was checked against all 28 catalog chapters, for ordinary and PYQ selection, with every response validated as `TestAvailabilityRead`. All chapters offer at least one allowed test length. **26 chapters have ordinary questions and 18 have PYQs** (the sets overlap). Science ordinary mode uses all ordinary difficulty levels; the frontend does not show Easy/Medium/Hard for Science. PYQ uses its own selector and pool. Small pools offer their exact size, so Respiratory System offers 1, Carbon & Its Compound offers 1, and Physics Revision offers 5. Circulatory System ordinary offers 10 and 11. The existing test-selection service only samples active, valid options from the selected chapter and mode.

## Import and review history

Earlier verified imports remain recorded in the manifest: source-page-supplement (18 rows), approved Science follow-up (7 rows), then the approved gap-fill (2 rows) and original Physics Revision batch (5 rows). The earlier source-page-supplement page 6 semantic duplicate and pending Sound question remain excluded; the Sound page 3 duplicate and pending Sound page 2 remain excluded. Carbon p.8 remains pending because its explanation is clipped. The original Physics Revision items are explicitly authored questions, not PDF-derived or previous-year questions.

The OCR review queue still has 333 `NEEDS_REVIEW` rows, alongside 102 verified source-review decisions, 9 duplicates, and 8 rejected rows. Those remaining OCR candidates have not all been re-reviewed in this turn; the bank's current testability does not mean every available source question has been exhausted. Existing eligibility and duplicate decisions remain in their ledgers.

## Validation performed

- `tests/test_science_import_candidates.py`: **18 passed** (isolated SQLite test database).
- `tests/test_test_sessions.py -k science_short_pool_selection_service_isolated_from_http_client`: **14 passed, 37 deselected**.
- Frontend `npm run lint`: passed (`tsc --noEmit`).
- Frontend `npm run build`: passed (TypeScript and Vite production build).
- In-memory route-handler flow: started a 5-question Science test, verified answer fields hidden during the active test, saved and re-read an answer, submitted, checked score/unanswered counts, and reviewed correct answers/explanations after submission. The test used an isolated in-memory SQLite database.
- Live test-availability service responses were checked read-only across all 28 Science chapters and both modes.

Authenticated HTTP `TestClient` test startup stalled in the current Windows environment, including the focused submit/score integration case; those runs were interrupted. No browser-based end-to-end flow was performed. Therefore timer countdown rendering, browser answer persistence, and full UI navigation remain unverified.

## Remaining work

Every Science chapter currently has an available test mode, but broader source review is incomplete while 333 OCR rows remain pending. Browser-based full-flow verification should follow once a working local API/UI test setup is available. No commit or push was made.
