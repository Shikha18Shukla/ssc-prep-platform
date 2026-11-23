# Tabular Puzzles — Arpit Sohgaura source audit

## Sources and identity

Two supplied files were located:

- `20 TABULAR PUZZLE by Arpit sir.pdf` — 20 physical pages
- `20 TABULAR PUZZLE by Arpit sir (1).pdf` — 20 physical pages

Both files have the same SHA-256 (`46e60a8c91fe24c3f6e1331dcd6855847b4573eb274146297346e0f8dd67fed0`) and are byte-identical. The cover identifies the material as “Puzzles Practice pdf by Arpit Sohgaura”; the section title on physical page 2 is “TABULAR PUZZLE.” The content in the second file is therefore another copy of the same Tabular Puzzle material, not Floor-Based content. The exact filename `PUZZLES Practice pdf by Arpit Sohgaura.pdf` was not present in the checked Documents, Downloads, or project directories; the matching cover/content appears in the supplied 20 TABULAR PDF copies.

All 20 pages of the unique content were visually reviewed using five contact sheets; selectable text was extracted for all pages. Pages 13–19 contain worked tables/answer explanations; page 20 contains social links. The PDF has numbered entries Q1–Q23, not 20.

## Counts and classification

| Measure | Result |
|---|---:|
| Numbered entries in each PDF | 23 |
| Unique source entries across the two byte-identical files | 23 |
| Repeated appearances due to the second copy | 23 |
| Explicit MCQs with a question prompt and source options | 4 (Q1–Q4) |
| Verified MCQs imported | 4 |
| Held clue-only entries without an individual question/options | 19 (Q5–Q23) |
| Duplicate questions in the existing Tabular Puzzles chapter | 0 |
| Duplicates within either PDF | 0 |

Q5–Q23 provide puzzle clue sets and worked assignment tables, but no individual MCQ prompt or answer-option list. They are held from this MCQ import; converting them would require inventing the question or options. Their physical pages are: Q5–Q7 p. 4; Q8–Q9 p. 5; Q10–Q11 p. 6; Q12–Q13 p. 7; Q14–Q15 p. 8; Q16–Q17 p. 9; Q18 p. 9–10; Q19–Q20 p. 10; Q21–Q22 p. 11; Q23 p. 12. Their printed arrangements were inspected but were not independently solved because they are not importable MCQs in the existing schema.

The two PDF copies are counted once as unique source content. Across both files, the repeated numbered appearances are 23, not 23 additional distinct questions.

## Destination and baseline

- Banking Clerk → Reasoning → Tabular Puzzles
- Chapter ID: `f00ab2eb-5830-4425-8dc9-c2b3efe96863`
- Direct Reasoning chapter (no subcategory parent)
- Local database identity: `ssc_prep` at `127.0.0.1:5432`
- Initial count: 5 active, 0 inactive
- Final count: 9 active, 0 inactive
- The five existing records remain present. They concern a different people/car/state puzzle and do not duplicate Q1–Q4.
- Semantic comparison was made against 506 Banking Clerk Reasoning records; the nearest text-similarity matches concerned unrelated arrangement questions. No semantic duplicate was identified.

## Independent answer verification

- Q1: **A** (student A). C=NTS, B=GUV, D=MAX; E likes Hindi and cannot be in GUV or PAV, so E=KNP. A is PAV, whose student likes Mathematics.
- Q2: **A** (person A). C has Coffee. Since drinks are distinct, D cannot have Coffee and therefore has Banana Shake. A and B take Tea/Mango Shake; A cannot take Mango Shake, leaving Tea.
- Q3: **B** (student A). C=M, B=O, D=N; E likes Hindi and cannot be O or L, so E=K. A is L, whose student likes Mathematics.
- Q4: **A** (C–C5–B3 is not correct). Exhaustive enumeration of distinct car and bike assignments yields one valid arrangement: A=C1/B2, B=C3/B1, C=C4/B3, D=C2/B5, E=C5/B4. Options B–D are consistent; option A is not.

The printed answer tables/markings agree with the independently derived answers for Q1–Q4. No answer key was used as the sole basis for an imported answer.

## Import and final verification

- Initial dry-run: 4 eligible, 0 duplicates, 0 rejected, 0 errors.
- Transactional import: 4 imported, 0 duplicates, 0 rejected, 0 errors.
- Database read-back verified exact question wording, all five options, one correct answer, explanation, source metadata, active status, and chapter association.
- New question IDs:
  - Q1: `5ef0c36d-47be-4dcc-9512-12011555f399` (answer A)
  - Q2: `8f2d718a-c8bf-4e4f-841b-1942c4738f43` (answer A)
  - Q3: `fd496833-bea9-44a8-abd6-528489791c18` (answer B)
  - Q4: `0151019d-fd5c-42ae-b356-17020486a93e` (answer A)
- Authenticated local API: `/api/auth/me` returned HTTP 200 for an active local admin; `/api/questions?chapter_id=f00ab2eb-5830-4425-8dc9-c2b3efe96863&limit=200` returned HTTP 200 with 9 active questions. All 4 new IDs, answer keys, five-option sets, explanations, source metadata, and chapter IDs were confirmed. The temporary backend was bound to `127.0.0.1` and stopped after verification.
- Idempotency replay: 4 records detected as duplicates, 0 new rows, 0 rejected, 0 errors.
- No migrations/schema changes, existing-question modifications, commits, or pushes were performed.
- The target of 40 active questions is not reached: this unique source contains 4 MCQs suitable for the existing MCQ import schema, while 19 clue-only entries are held. The chapter now has 9 active questions.

## Files created

- `backend/data/imports/reasoning/tabular-puzzles/tabular_puzzles_arpit_verified.json`
- `backend/data/imports/reasoning/tabular-puzzles/tabular_puzzles_arpit_review_report.md`
- Temporary audit renders/extract: `tmp/pdfs/tabular-puzzles-audit/`
- Temporary API logs: `tmp/tabular_api_stdout.log` and `tmp/tabular_api_stderr.log`
