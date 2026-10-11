# Brain & Nervous System Chapter Review

- Catalog chapter: **Brain & Nervous System** (`brain-and-nervous-system`), ID `2237850c-bf16-4627-970a-33f548ae8398`; confirmed through a read-only query beneath `gk-gs/science`.
- Source pages: `respiratory system - science.pdf` pp. 2–22 (all 21 question pages); `Disease.pdf` p. 15 checked as an additional candidate. `brain and nervous system - science.pdf` pp. 2–21 were also visually sampled; its 20 question pages contain excretory-system content and add no Brain & Nervous System questions.
- The Respiratory PDF pages with Brain & Nervous System content are pp. 2–18 and 20–22. Page 3 duplicates p. 4; p. 19 is a Skeleton System question.
- The additional `Disease.pdf` p. 15 question asks which organ contains the hypothalamus; its answer is Brain, but the explanation is clipped, so it remains pending.

## Disposition counts

| Difficulty | Type | Verified | Needs review | Rejected | Duplicate |
|---|---|---:|---:|---:|---:|
| EASY | Ordinary | 4 | 1 | 0 | 1 |
| EASY | PYQ | 0 | 1 | 0 | 0 |
| MEDIUM | Ordinary | 5 | 2 | 1 | 0 |
| MEDIUM | PYQ | 4 | 1 | 0 | 0 |
| HARD | Ordinary | 0 | 1 | 0 | 0 |
| HARD | PYQ | 1 | 0 | 0 | 0 |

- Verified/import-ready records: 14 (9 ordinary, 5 PYQ).
- Needs review: 6; rejected as outside chapter: 1; confirmed duplicate records: 1.
- Confirmed duplicate retained only once: Respiratory PDF p. 3 is duplicate of p. 4.

## Ordinary target gaps

| Difficulty | Verified ordinary | Target | Remaining |
|---|---:|---:|---:|
| EASY | 4 | 25 | 21 |
| MEDIUM | 5 | 25 | 20 |
| HARD | 0 | 25 | 25 |

PYQs are tracked separately and do not count toward ordinary targets. No exam names were visible; none were inferred.

## Duplicate audit

Compared 20 distinct Brain candidates (19 from the Respiratory PDF and the additional Disease p. 15 candidate) with 33 active question-bank rows and all 99 prior chapter-review rows (85 had nonempty stems). No active-question or prior-batch duplicate was confirmed. The nearest text-similarity lead was Respiratory PDF p. 16 vs. a Circulatory System valve question (0.815); visual/content comparison shows unrelated subjects and different answer choices. Similar concept mentions were not counted as duplicates.

## Review limits

Pages with clipped explanations (Respiratory PDF pp. 2, 5, 7, 17, 22 and Disease p. 15) remain NEEDS_REVIEW and are excluded from both importer CSVs. Page text, option order, highlighted answers, explanation completeness, visible difficulty, and PYQ labels/years were checked against rendered source pages. The PDF titled `brain and nervous system - science.pdf` was not treated as topic evidence.

## Validation

Importer dry-run validation is covered by `tests/test_science_import_candidates.py`; it uses the isolated test database, asserts all 14 eligible rows are accepted and imported count is zero, and checks the test database remains empty. No production import was run.
