# Coding-Decoding PYQ review

## Result

Four records are prepared as a conservative, evidence-backed subset. All are labelled PYQ and retain the exam attribution displayed by the cited secondary sources. No official SSC paper or answer key was obtained for these records. This is not an official-source verification claim.

| # | Exam attribution | Question (short) | Answer | Check | Source class |
|---|---|---|---|---|---|
| 1 | SSC CGL Tier I, 26 Jul 2023, Shift 2 | EACH/EASY → ECHO | 83 | Reverse alphabet values sum to 91 and 58; both add 6; ECHO gives 83. Published option 3 agrees. | ExamSIDE secondary question page |
| 2 | SSC CGL Tier I, 26 Jul 2023, Shift 2 | SCOOTER/AEROPLANE → HELICOPTER | SGWTTIPTNR | Reverse, then successive +1… shifts; published option 2 agrees. | ExamSIDE secondary question page |
| 3 | SSC CGL Tier I, 2 Dec 2022, Shift 1 | NUMERICAL/SCATTERED → EXPLOSION | SIONOEXPL | Reorder input positions 6–9, then 5, then 1–4; both examples and published answer agree. | SSC Portal archived copy and Testbook; both secondary |
| 4 | SSC CGL Tier I, 3 Dec 2022, Shift 1 | MOBILE/SILENT → PAINTING | SDLQWLQJ | Caesar shift +3; published option 2 agrees. | Careers360 question and GetMyUni archived paper; secondary |

The three July 2023 questions were checked against their individual ExamSIDE pages, which show the full stem, four options, answer selection, and explanation. The two archived December papers and solution pages are secondary sources. None of the records has official SSC corroboration.

## Exclusions and duplicate review

- The `C ___ ...` July series candidate is excluded: although the page presents answer `EXCUEPCX`, the rendered stem's blank grouping is not sufficiently clear to independently reconstruct each position from the available text without relying on the published explanation alone.
- The `PEN/PAPER → CHAPTER` length-square question is excluded as a repetitive semantic duplicate of `DUST/EARTH → MAN` (both encode the square of word length).
- The December `APPRECIATE/MOTIVATION → FRIENDSHIP` reverse-word candidate is excluded as a repetitive semantic duplicate of another reverse-word transformation.
- Other unaudited July candidates are not included. The former malformed combined batch is not reused.
- Exact stem comparison against the existing 24-question Normal batch found no collision. Manual semantic comparison found no same question or same transformation instance. Generic letter shifting/reordering concepts are shared by the syllabus, but the actual records are distinct.
- The four included candidate stems are distinct from one another. No live database comparison was possible because the configured Python runtime cannot start; the last confirmed state is 24 Normal and 0 PYQ.

## Import path and validation status

The existing importer supports the shared JSON schema, chapter slug resolution, transactional dry-run, and question-text idempotency. Its CLI validator was extended to accept a separate `--source pyq` batch/ledger pair while retaining the Normal path. Target chapter remains the existing Coding-Decoding chapter configured in that importer. No second importer was added.

The batch and ledger use the existing schema, have four options per row, and carry `is_pyq=true`, year, exam/date/shift, explanations, and source URLs. Structural validation is pending execution of the repository's Python validator/tests. Import was not run: the environment's `python.exe` launchers reference a missing Microsoft Store Python installation. Database remains unchanged by this task; no import command was run.
