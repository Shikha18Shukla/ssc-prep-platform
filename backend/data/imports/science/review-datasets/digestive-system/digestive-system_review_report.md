# Digestive System Chapter Review

## Catalog mapping

- Parent path: `gk-gs/science`.
- Chapter: **Digestive System**, slug `digestive-system`, catalog ID `79d7f2e8-b911-4a6e-89fe-676b6a5ed7c3` (confirmed against the current database catalog on 2026-10-10).
- Mapping was confirmed by a read-only catalog query and by the question topics on source pages; filenames were used only to locate candidates.

## Source coverage and review

- Candidate source pages: 16 from `Digestive system - science.pdf` and 15 from `cell -science.pdf` (31 page candidates total). Each candidate page was checked against its original page image and OCR transcript.
- Digestive System PDF pages 9, 11, 13, and 16–26 contain unrelated heart/circulatory/lymph questions and were excluded from this chapter. The Cell PDF nutrition pages 6–9 and non-digestive cell questions were excluded. Cross-source keyword hits were also checked by question stem: Disease PDF p. 2 is about hypothalamic/pituitary regulation (bile and salivary secretion are distractors); Gravitational Work and Energy p. 22 is an optics/mirror question; Excretory System p. 11 is about vitamin D; Reproduction p. 20 concerns annelid traits; the Respiratory System pages using “digestive system” mention it only as a distractor. None is a Digestive System question.
- The oral/dental candidates in the Cell PDF were assigned to Digestive System because they concern the mouth, teeth, and food processing. Clipped or structurally ambiguous pages remain pending.
- Explicit difficulty badges and PYQ years were copied from source images. No exam name was visible on these pages; `pyq_exam_name` remains blank. No year was inferred.

## Disposition by difficulty and PYQ status

| Difficulty | Source status | Verified | Needs review | Rejected | Duplicate | Import-ready CSV rows |
|---|---|---:|---:|---:|---:|---:|
| EASY | PYQ | 1 | 4 | 0 | 0 | 1 |
| EASY | ORDINARY | 2 | 0 | 0 | 0 | 2 |
| MEDIUM | PYQ | 5 | 8 | 0 | 3 | 5 |
| MEDIUM | ORDINARY | 1 | 4 | 0 | 0 | 1 |
| HARD | PYQ | 1 | 0 | 0 | 0 | 1 |
| HARD | ORDINARY | 2 | 0 | 0 | 0 | 2 |
| **TOTAL** | **All** | **12** | **16** | **0** | **3** | **12** |

- Verified candidate rows include the previously reviewed Cell page 2 record. The chapter PYQ CSV retains that existing row once, plus the newly verified rows; it is not duplicated.
- No batch target or required per-difficulty allocation is defined in the existing pipeline. The table reports source-supported availability, not invented targets.

## Confirmed duplicate decisions

- `Digestive system - science.pdf` page 27 duplicates page 6 (same question, options, answer, and explanation). Page 6 remains NEEDS_REVIEW due to the villi/microvilli explanation conflict; page 27 is excluded as a duplicate.
- `cell -science.pdf` page 17 duplicates page 4 (same PYQ 2020 food-tube question and answer). Page 4 remains NEEDS_REVIEW because its explanation is clipped; page 17 is excluded as a duplicate.
- `Digestive system - science.pdf` page 28 is a semantic duplicate of page 2: both ask which enzyme is found in saliva, and Ptyalin is another name for salivary amylase. Page 28 is excluded.

## Remaining review items

- **16 NEEDS_REVIEW** records remain. They include clipped explanations, an answer/explanation terminology conflict, and a malformed duplicated solution block. They are not included in either import-ready CSV.
- **0 rejected** records. **3 confirmed duplicate** page records.
- Among the 33 active database questions checked, none belonged to an active Science chapter. Candidate stems were compared to all 33; the maximum match was a low 0.414 similarity to an unrelated percentage question. No database duplicate was found.
- The previously reviewed/import-ready Science batches (Animal Kingdom, Tissues, and the retained Cell page 2 Digestive record) were compared against new candidates. No content duplicate was found; Cell page 2 itself remains the single preserved existing row. A 0.693 stem score from the shared phrase “Which among the following” compared the oesophagus question with an Animalia question; content comparison confirmed they are unrelated.

## Dry-run decision

- Importer tests ran against the isolated in-memory SQLite test database. Both Digestive System CSVs validated; no records were imported and the database row count remained zero after each dry run.
- No production database changes or real import were performed.

## Next chapter recommendation

Proceed with **Circulatory System**. The inventory has a dedicated 20-question-page source PDF, and the Digestive System PDF also contains circulatory-topic pages that can increase source coverage. Its catalog chapter exists; verify every page by content before assigning any records.
