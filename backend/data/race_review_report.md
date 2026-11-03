# Race chapter source and verification report

## Source review

Visually reviewed all 35 physical pages: Race 01_ Class Notes.pdf (19/19) and Race 02_ Class Notes.pdf (16/16). Accepted 11 source-derived questions; rejected 24 candidates for the reasons listed in `race_source_review.json`. Source items are lecture examples, not PYQs. No exam name or year is asserted.

## Bank composition

- Active Normal target is at least 90; canonical total: 91.
- Difficulty: Easy 30, Medium 30, Hard 31.
- Topic classification: Linear Race 71; Circular Race 20.
- Provenance: source-derived 11; original SSC-style 80.
- Correct answer positions: A 23, B 23, C 22, D 23.

## Mathematical review

All 91 rows have four distinct options, a single answer key matching the keyed option, and a non-empty worked explanation. Answers were independently checked against the stated distance, speed, time, start offsets, lap periods, and meeting-location cycle. The corrected three-runner question is independently evaluated on a common time origin: A finishes at 75 s, B at 71 2/3 s, and C at 70 s, so A finishes last. The source head-start example on Race 01 page 13 is 198 s after P starts because Q has a two-second head start. The Race 01 page 16 speed-difference candidate is retained because it is a distinct multi-condition question and covers a requested skill.

Six content defects were corrected with exact live-record preconditions: the three-runner answer changed from B to A while preserving and reordering the original options; the chained-race explanation now solves explicitly for C's speed; and four original stems were clarified where their wording contradicted or obscured start timing, finish timing, or whether distance was covered. Difficulty, identities, and all other content were preserved.

## Duplicate review

Within the batch, exact normalized, number-masked, and high lexical screening found no collisions. A prior cross-chapter pass compared the original 90 Race stems with 6,022 other canonical and live Maths questions; it found zero exact or number-masked collisions. The additional Race 01 page 16 stem was screened against 3,409 available canonical questions and had no exact, number-masked, or high lexical collision; its live-database cross-chapter scan could not be rerun in this environment. Problem-family screening supplemented these checks, but these checks do not prove the absence of every possible semantic overlap. See `race_source_review.json` and the focused duplicate tests.

## Import and application verification

The guarded importer uses exact existing-row preconditions and a transaction. Verify the live catalog, dry-run, and replay at release time; no importer write is performed by this artifact builder. Test/API/build results are recorded in the completion report for this run.

## Limitations

Difficulty is an editorial classification. The scanned lecture examples are not described as historical SSC questions, and the source-review exclusions document repeated templates or non-question slides.
