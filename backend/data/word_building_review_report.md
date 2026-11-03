# CH-15 Word Building — Source Review and Import Report

## Chapter and final bank

- Catalog path: SSC → Reasoning → Word Building (`word-building`).
- Live chapter ID: `886e3a61-031f-48ce-9c62-aff6db3ba7a5`.
- Final live state: 30 active Normal questions, 0 active PYQs; 10 Easy, 10 Medium, 10 Hard.
- Provenance: 20 selected PDF-derived questions and 10 original SSC-style questions. No item was identified reliably as a previous-year question.
- Every row has four distinct choices, exactly one keyed answer, a nonempty explanation, and Normal metadata.

## Source inspection and selection

Both scanned PDFs were rendered and every page visually inspected: Word Building 01 (16 pages) and Word Building 02 (24 pages). They contain no selectable text, so the review used rendered pages, including enlarged question slides and handwritten annotations.

Selected source questions:

| Source | Pages | Selected | Main concepts |
|---|---:|---:|---|
| Word Building 01 | 7, 10, 12, 14 | 4 | Dictionary ordering; letter-frequency formation/cannot-form |
| Word Building 02 | 4, 5, 6, 7, 9, 10, 11, 12, 14, 15, 16, 17, 18, 20, 21, 22 | 16 | Number-to-word mapping; suffix/prefix; unchanged positions; letter spacing/pairs |

Rejected or not selected source items:

| Source | Page(s) | Reason |
|---|---:|---|
| Word Building 01 | 4–6 | Board notes/examples without a complete, uniquely specified standalone question and answer choices. |
| Word Building 01 | 8 | The apparent word “Cutiase” is not sufficiently clear/reliable for a spelling-sensitive dictionary-order item. |
| Word Building 01 | 9 | “Ropped” appears misspelled or nonstandard, so the dictionary-order item is not dependable. |
| Word Building 01 | 11 | ENVIRONMENT has multiple choices that cannot be formed (including MOVEMENT, ENTRANCE and ENTERTAIN); the single-answer prompt is invalid. |
| Word Building 01 | 13 | FANTASTICATE has more than one unformable choice (including TASTY and FASTING); the single-answer prompt is invalid. |
| Word Building 02 | 8 | The PRESIDENT numeric-sequence options include a visibly truncated six-digit choice although the task needs nine positions. The missing digits were not guessed. |
| Word Building 02 | 13 | The common-prefix example relies on “SPILE,” an uncommon word, and does not meet the bank’s clear, familiar-word standard. |
| Word Building 02 | 19 | Pairing-of-letters board examples without a complete question/options; related complete prompts on pages 20–22 were retained. |

The selected items preserve each source-marked answer separately in the ledger and independently recheck the answer. The visibly incomplete page-8 item was initially transcribed into the first import, then excluded after enlargement confirmed the truncation. Its newly imported row was corrected to an original dictionary-order question after verifying the exact old row, active Normal status, and absence of test-attempt references. No other record was changed.

## Topic and difficulty distributions

| Topic | PDF-derived | Original | Total |
|---|---:|---:|---:|
| Dictionary arrangement | 1 | 3 | 4 |
| Can/cannot be formed (letter frequency) | 3 | 2 | 5 |
| Letter jumbling and meaningful word formation | 5 | 2 | 7 |
| Prefixes and suffixes | 3 | 1 | 4 |
| Alphabetical order and unchanged positions | 4 | 1 | 5 |
| Letter pairs and letter-position distance | 4 | 1 | 5 |
| **Total** | **20** | **10** | **30** |

| Difficulty | Count |
|---|---:|
| Easy | 10 |
| Medium | 10 |
| Hard | 10 |

## Answer verification and duplicate review

- Letter formation: frequency Counters validate every specified valid/unformable option, including repeated-letter limits.
- Dictionary arrangement: full spellings are lexicographically sorted and checked against the keyed order.
- Letter mappings: each number sequence is decoded programmatically against the intended word.
- Alphabetical positions: sorted letters are compared index-by-index, including repeated-letter positions.
- Letter pairs: every word-position pair is enumerated once; a pair qualifies when the absolute alphabet-position gap equals its word-position gap. Source examples are also enumerated independently.
- Prefix/suffix questions: every resulting word is listed and checked for the common affix.
- Options, provenance, question signatures, and ledger alignment are validated by the focused test and importer.
- Exact/near-duplicate review scanned 520 canonical Reasoning stems and 520 live pre-import Reasoning records; no exact collision or ≥0.94 stem similarity was found. Similar-looking within-bank instruction templates were reviewed as different target words, mappings, or mathematical tasks; no semantic duplicates were retained.

## Import, API, and tests

- Initial guarded dry-run against the empty chapter: 30 would insert, 0 duplicate, 0 rejected, 0 errors.
- Initial apply: 30 inserted, 0 duplicate, 0 rejected, 0 errors.
- After the page-8 source correction, guarded canonical replay: 30 duplicates, 0 would insert, 0 rejected, 0 errors; no second import occurred.
- Final PostgreSQL state: 30 active Normal; 0 active PYQ; 10/10/10 difficulty counts. All records have four distinct options, exactly one correct option and an explanation.
- Authenticated API checks list the chapter under Reasoning. Both chapter availability and test availability report 10 questions and accept a 10-question request for Easy, Medium and Hard. PYQ availability is 0; mixed Normal availability is 30.
- A rollback-scoped authenticated API exam loaded 10 Hard questions and four options each, saved and reloaded answers, submitted, scored 10/10, and returned correct answers and explanations. Duration/deadline fields were supplied for the 360-second test; the temporary test attempt was rolled back.
- Frontend inspection confirms the existing exam player consumes the API’s question/option payload, supports answer selection and question navigation, uses the returned deadline for its timer, and displays result explanations. No special-case Word Building behavior was added.
- Focused Word Building tests: 4 passed. Related backend regressions (catalog, auth, test sessions, and question-bank service): 120 passed. Frontend TypeScript/Vite production build passed. Python compilation passed for the builder, importer, and focused test. `git diff --check` passed.
- No browser UI automation was performed.

## Artifacts

- `data/word_building_verified_batch.json` — canonical import payload.
- `data/word_building_answer_ledger.json` — selected answers, source-marked answers, independent verification, and provenance.
- `data/word_building_review_report.md` — this source and validation report.
- `scripts/build_word_building_artifacts.py` — deterministic builder and mathematical checks.
- `scripts/import_word_building_verified_batch.py` — guarded, idempotent importer.
- `tests/test_word_building_verified_batch.py` — schema, answer, duplicate, importer dry-run/replay tests.

## Limitations

Source handwritten annotations are recorded only where legible; they were not treated as authoritative. Question content was translated/transcribed into English for the existing application schema. Browser-driven visual testing was not performed; the live authenticated API flow was exercised instead.
