# Syllogism source review and top-up report

## Scope and catalog
Reviewed all pages of the available Syllogism Lecture 02–06 PDFs. The target is Banking → Clerk → Reasoning → Syllogism, chapter `b73b3f68-ca65-43eb-a723-df798401ca37`. The local DB was at Alembic revision `0010_banking_catalog`; no migration was run.

## Source audit
- Lecture 02 (53 pages): 23 question slides identified (Q1–15 and Q26–33). Thirteen questions were independently verified and imported from pages 13, 15, 17, 21, 25, 27, 29, 31, 35, 37, 39, 44, and 46. Ten were held: Q4 has no matching answer option under the printed statements; Q6 is missing a premise on the slide; Q11 and Q15 were not sufficiently clear to resolve reliably; Q26 and Q27/Q29 use ambiguous “can not be” wording; Q31 is missing its statements on this lecture’s slide; Q32 is missing conclusions/options; Q33 was not included because it repeats content and lacks verified source answer evidence.
- Lecture 03 (30 pages): 11 question slides identified. Ten repeat full question content also found in Lecture 02; they were not imported twice. Q31 on p. 24 supplies complete statements absent from Lecture 02’s Q31 slide; its verified answer is only conclusion II, and it was imported once with this source citation.
- Lecture 04 (9 pages): no exam-style question slides; theory and summary only.
- Lecture 05 (20 pages): 10 question slides. Nine were imported previously; p. 15 remains held because a handwritten edit and the printed answer choices conflict.
- Lecture 06 (16 pages): six question slides were imported previously. The p. 5 diagram is teaching material, not an MCQ.

Lecture 02 p. 31’s handwritten answer marking appears to omit conclusion II, even though Some B are C and All C are D make conclusion II true. The imported key is “both,” independently recomputed from the statements.

## Syllogism import and verification
- Before this top-up: 17 active, 3 inactive.
- Dry-run before first insert: 13 eligible; 0 duplicates, 0 rejected, 0 validation errors.
- First append-only import: 13 inserted. A replay detected all 13 as duplicates.
- After identifying the complete Lecture 03 Q31, its dry-run found one new record and 13 duplicates; it was then appended through the same transactional importer.
- Final Syllogism count: 31 active, 3 inactive. All 14 new records were verified against source page, explanation, five options, and exactly one correct answer. No previous question was changed.
- A later replay detected all 14 new records as duplicates.
- All active Syllogism questions have 4 or 5 options, exactly one correct option, and a nonempty explanation. The two older active questions without lecture-PDF provenance were reviewed; their keys agree with their statements.

## Inequality source gap
The existing Inequality chapter remains unchanged at 27 active questions. No Inequality class-note PDFs were found in Downloads, Desktop, Documents, or the project tree. Missing filenames: `Inequality 02_Class Notes.pdf`, `Inequality 03_Class Notes.pdf`, and `Inequality 04_Class Notes.pdf`. The two earlier held Lecture 04 questions cannot be rechecked without their source PDF. The existing 27-question import replay returned 27 duplicates, no validation errors, and zero new records. The Inequality chapter remains 3 questions short of the target.
