# Coding Decoding PDF import audit

## Scope and result

- Destination: Banking → Clerk → Reasoning → Coding Decoding.
- Chapter ID: `e9b8d302-10ef-426b-b8a6-06de9fcba612`.
- Local database inspection found 5 active questions and 0 inactive questions before this batch. Their shared source passage is the network-speed coding set; no normalized prompt duplicates were found among the reviewed PDF questions.
- All 49 pages of the three supplied PDFs were rendered and visually reviewed. The files are image-based; PDF text extraction was not sufficient for questions, options, markings, or diagrams.
- Inventory: 23 distinct question prompts (Lecture 01: 9, Lecture 02: 9, Lecture 03: 5). The first lecture’s page 5 repeats the page 4 “Has” item as its worked solution and is counted as the same item, not a second question.
- Eligible MCQs: 18 from Lectures 01 and 02. Lecture 03 has 5 open-response letter-coding items with no answer-choice sets; these are held because the current importer and question schema require four or five complete options. No distractors were invented.
- Duplicate prompts within the three PDFs: 0 beyond the page 4/page 5 worked repetition noted above. Duplicate prompts against the 5 pre-existing local chapter records: 0.

## Page-by-page inventory

| PDF / lecture | Pages reviewed | Question pages and classification |
|---|---:|---|
| Coding Decoding 01 | 16 | p. 4: “Has” question; p. 5: worked solution/repetition of p. 4; p. 6: code for “Home’s there red”; p. 7: meaning of “No”; p. 8: decode “Ea Qhi Oic”; p. 9: possible code for “he has fresh demand”; p. 10: shared passage only; pp. 11–14: Energy, Work, meaning of “Si”, and Market questions. pp. 1–3 and 15–16 are introduction/topic/summary/closing material. |
| Coding Decoding 02 | 21 | p. 4: code for “proposed good rule queen”; pp. 5–7: Greenhouse, meaning of “im”, and possible code for “Warming Gas”; p. 8: code for “sky”; p. 9: answer/working; p. 10: “always sky before”; p. 11: answer/working; p. 12: meaning of “go”; p. 13: answer/working; p. 14: code for “war”; p. 15: answer/working; p. 16: possible code for “people safe”; p. 17: answer/working. Remaining pages are lecture topic, recap, reverse-alphabet teaching examples, or closing material rather than additional questions. |
| Coding Decoding 03 | 12 | pp. 6–10: five open-response letter-coding questions (STAFF→SELECTION; SENSITIVE→MICROSOFT; CYLINDER→AROMATIC; GEOPHYSICS→ALTIMETERS; PATHOLOGIST→NATIONALISM). pp. 1–5 establish/review alphabet coding rules; pp. 11–12 are summary/closing material. |

## Verification notes

Each eligible imported item includes its full relevant common passage, all five source options in source order, one independently checked answer, an explanation, and PDF/lecture/page metadata. The legible Hindi question text was retained for Lecture 01 page 4 and Lecture 02 pages 8, 10, 12, 14, and 16. No Hindi translations were generated for slides that did not supply one.

### Held for manual review: Lecture 03

The five items below are genuine questions and are not silently discarded. The handwritten answers are visible, but the slides contain no multiple-choice options. The current question import architecture accepts only four- or five-option MCQs; adding invented distractors would alter the source.

| Page | Source prompt | Handwritten result / review note |
|---:|---|---|
| 6 | STAFF is coded as HGZUU; how is SELECTION written? | Atbash/complement mapping gives `HVOVXGRLM`; handwritten result is legible. Held only because no source options exist. |
| 7 | SENSITIVE is coded as QHLVGWGYC; how is MICROSOFT written? | Alternating −2,+3 shifts give `KLAUMVMIR`; handwritten result is legible. Held only because no source options exist. |
| 8 | CYLINDER is coded as UHGQGJWA; how is AROMATIC written? | Reverse the word, shift the first half +3 and second half −2: `FLWDKMPY`; handwritten result is legible. Held only because no source options exist. |
| 9 | GEOPHYSICS is coded as IOPDHZRJBT; how is ALTIMETERS written? | Source working is image-based and the handwritten target string is not reliably legible enough to certify. Held for both missing options and answer transcription review. |
| 10 | PATHOLOGIST is coded as PIUBQKSRHFN; how is NATIONALISM written? | Handwritten result appears to be `PJUBOMLRHKZ`, but the rule/working is not independently clear from the slide. Held for answer/rule review as well as missing options. |

## Import artifacts

- `coding_decoding_01_02_verified.json`: 18 candidate MCQs.
- `coding_decoding_review_report.md`: source inventory and manual-review notes.
- `backend/tests/test_coding_decoding_01_02_import.py`: checks field/source completeness, dry-run behavior, import option integrity, and duplicate detection on replay.

## Database and application verification

- Connection was explicitly pinned to local `127.0.0.1:5432/ssc_prep`; server address/port and database name were checked in-session. Alembic revision remains `0010_banking_catalog`; no migration was run.
- Pre-import target count: 5 active, 0 inactive. Chapter mapping was checked against the specified ID and `coding-decoding` slug.
- Importer dry-run: 18 eligible, 0 duplicates, 0 rejected, 0 validation errors.
- Transactional import: 18 inserted, 0 duplicates, 0 rejected, 0 errors. The 5 pre-existing records were snapshotted and verified unchanged.
- Post-import count: 23 active, 0 inactive. Every new record has 5 options, exactly one correct option, a non-empty explanation, and source filename/lecture/PDF page metadata.
- Importer replay dry-run: 0 eligible to write, all 18 detected as duplicates.
- Authenticated local `GET /api/questions?chapter_id=…&limit=100`: HTTP 200, 23 returned, including all 18 new records; options, one-correct integrity, explanations, and source metadata were present. Six records retained the readable Hindi prompt text.
- Backend tests: `pytest tests/test_coding_decoding_01_02_import.py -q` passed (2 passed). A combined run with `test_question_bank.py` was interrupted after it stalled without producing a result; it is not reported as passed.
- Frontend production build: `npm run build` passed (TypeScript build and Vite build; 55 modules transformed).

No migration, reset, truncation, deletion, production connection, commit, or push was performed. API behavior was verified through the authenticated local API; no visual browser walkthrough of the chapter page was performed.
