# Linear Arrangements — Complete Source Audit

Read-only audit of the three supplied Linear Arrangement PDFs. No database writes, migrations, imports, or configuration edits were performed.

## Source coverage

| PDF | PDF pages | Numbered questions |
|---|---:|---:|
| `Mains_Topic_wise_Linear_Based_Arrangement_Two_Variable_with_Vacant.pdf` | 28 | 10 |
| `Mains_Topic_wise_Linear_Based_Arrangement_Bi_Directional_Set_1.pdf` | 31 | 10 |
| `Mains_Topic_wise_Linear_Arrangement_with_distance_based_Set_1.pdf` | 34 | 10 |

Total: **93 PDF pages**; reviewed **30** numbered question appearances across the three source PDFs (question prompts occupy physical pages 1–4; later pages contain solutions/repeated work).

## Chapter and classification

- Chapter ID: `7a6e3168-894b-47c8-86df-ab6891f28d2b` (Banking Clerk → Reasoning → Linear Arrangements).
- Live local DB check: 20 active, 0 inactive (chapter ID and host/database verified).
- Verified unique candidates: **18**; held: **12**; duplicates: **0**; invalid: **0**.
- Achievable active count using verified candidates: **38/40** (shortfall 2).
- Read-only live database comparison: 0 exact overlaps; 0 prompt-similarity matches at/above the review threshold.
- The reusable matcher flagged 22 records for fuzzy review; manual checks found only generic wording/shared-context similarities, not duplicate questions.
- A fresh PyMuPDF extraction from the original PDFs found 30 headings; all 30 prompts and A–E options matched the saved extract after normalization. Rendered physical pages 1–4 of each original PDF were visually checked.

## Puzzle-group results

- Vacant-seat Q1–Q5: one valid arrangement; retained prior answers B, C, A, D, E.
- Vacant-seat Q6–Q10: held as a group because written clue “three persons between R and Q” conflicts with the printed final arrangement (four persons between); solver finds zero arrangements satisfying all written clues.
- Bidirectional/color Q1–Q5: five valid arrangements satisfy the written clues; each of the five questions has a specific answer-changing or unlisted-answer ambiguity, so all five are held. The printed keys match one displayed case only.
- Bidirectional/age Q6–Q10: one valid arrangement; all five answers are independently verified.
- Distance WX/YZ Q1–Q5: WX and YZ each have one solution. Q1, Q2, and Q5 verified; Q3 and Q4 held because the transformed row spacing/starting rules are not sufficiently specified.
- East-facing distance Q6–Q10: one valid arrangement; all five answers are independently verified.

## Question-level classifications and answers

| Source | Page(s) | Q | Status | Answer | Printed key | Note |
|---|---:|---:|---|---|---|---|
| `Mains_Topic_wise_Linear_Based_Arrangement_Two_Variable_with_Vacant` | 1 | 1 | verified_unique | B | B | Independent answer verified. |
| `Mains_Topic_wise_Linear_Based_Arrangement_Two_Variable_with_Vacant` | 1 | 2 | verified_unique | C | C | Independent answer verified. |
| `Mains_Topic_wise_Linear_Based_Arrangement_Two_Variable_with_Vacant` | 1-2 | 3 | verified_unique | A | A | Independent answer verified. |
| `Mains_Topic_wise_Linear_Based_Arrangement_Two_Variable_with_Vacant` | 2 | 4 | verified_unique | D | D | Independent answer verified. |
| `Mains_Topic_wise_Linear_Based_Arrangement_Two_Variable_with_Vacant` | 2 | 5 | verified_unique | E | E | Independent answer verified. |
| `Mains_Topic_wise_Linear_Based_Arrangement_Two_Variable_with_Vacant` | 2-3 | 6 | held | — | E | Written clue “three persons between R and Q” conflicts with the printed final arrangement, which places four persons between them; written-clue solver returns zero arrangements. |
| `Mains_Topic_wise_Linear_Based_Arrangement_Two_Variable_with_Vacant` | 3 | 7 | held | — | C | Written clue “three persons between R and Q” conflicts with the printed final arrangement, which places four persons between them; written-clue solver returns zero arrangements. |
| `Mains_Topic_wise_Linear_Based_Arrangement_Two_Variable_with_Vacant` | 3 | 8 | held | — | C | Written clue “three persons between R and Q” conflicts with the printed final arrangement, which places four persons between them; written-clue solver returns zero arrangements. |
| `Mains_Topic_wise_Linear_Based_Arrangement_Two_Variable_with_Vacant` | 3 | 9 | held | — | C | Written clue “three persons between R and Q” conflicts with the printed final arrangement, which places four persons between them; written-clue solver returns zero arrangements. |
| `Mains_Topic_wise_Linear_Based_Arrangement_Two_Variable_with_Vacant` | 3-4 | 10 | held | — | D | Written clue “three persons between R and Q” conflicts with the printed final arrangement, which places four persons between them; written-clue solver returns zero arrangements. |
| `Mains_Topic_wise_Linear_Based_Arrangement_Bi_Directional_Set_1` | 1 | 1 | held | — | A | Across five valid layouts, the red/grey/F facing statements yield ‘Only I’ in some layouts and ‘I and III’ in others; the latter combination is not even listed. No unique option is supported. |
| `Mains_Topic_wise_Linear_Based_Arrangement_Bi_Directional_Set_1` | 1 | 2 | held | — | D | Across valid layouts, the true relation about G changes (A in some layouts, D in another), and some layouts satisfy none of the listed relations. No unique option is supported. |
| `Mains_Topic_wise_Linear_Based_Arrangement_Bi_Directional_Set_1` | 2 | 3 | held | — | D | Across valid layouts, the queried third-right position is the Purple-color person in one layout, while in other layouts the target position falls outside the row. No unique answer is established. |
| `Mains_Topic_wise_Linear_Based_Arrangement_Bi_Directional_Set_1` | 2 | 4 | held | — | E | The five compared entities do not have one consistent outlier across all valid layouts: one layout makes White the direction outlier, while other valid layouts have multiple differing directions. The question has no invariant answer. |
| `Mains_Topic_wise_Linear_Based_Arrangement_Bi_Directional_Set_1` | 2 | 5 | held | — | D | C likes Red in one valid layout and Pink in the other valid layouts; the correct option changes. |
| `Mains_Topic_wise_Linear_Based_Arrangement_Bi_Directional_Set_1` | 2-3 | 6 | verified_unique | B | B | Independent answer verified. |
| `Mains_Topic_wise_Linear_Based_Arrangement_Bi_Directional_Set_1` | 3 | 7 | verified_unique | A | A | Independent answer verified. |
| `Mains_Topic_wise_Linear_Based_Arrangement_Bi_Directional_Set_1` | 3 | 8 | verified_unique | D | D | Independent answer verified. |
| `Mains_Topic_wise_Linear_Based_Arrangement_Bi_Directional_Set_1` | 3-4 | 9 | verified_unique | D | D | Independent answer verified. |
| `Mains_Topic_wise_Linear_Based_Arrangement_Bi_Directional_Set_1` | 4 | 10 | verified_unique | C | C | Independent answer verified. |
| `Mains_Topic_wise_Linear_Arrangement_with_distance_based_Set_1` | 1 | 1 | verified_unique | D | D | Independent answer verified. |
| `Mains_Topic_wise_Linear_Arrangement_with_distance_based_Set_1` | 1-2 | 2 | verified_unique | A | A | Independent answer verified. |
| `Mains_Topic_wise_Linear_Arrangement_with_distance_based_Set_1` | 2 | 3 | held | — | C | The transformation says the people are seated “at a consecutive multiple of 9m” but does not define the starting offset/interval sequence in row MN or how the remaining seven people continue the row at multiples of 5m. Applying the source phrasing in more than one reasonable way changes B-to-N; the printed key alone cannot resolve the missing placement rule. |
| `Mains_Topic_wise_Linear_Arrangement_with_distance_based_Set_1` | 2 | 4 | held | — | B | “At a consecutive multiple of 2m starting 12m from L” does not establish whether 12m is the first position followed by equal 2m intervals or whether adjacent intervals successively increase by multiples of 2m; these interpretations yield different distances and different options. |
| `Mains_Topic_wise_Linear_Arrangement_with_distance_based_Set_1` | 2 | 5 | verified_unique | D | D | Independent answer verified. |
| `Mains_Topic_wise_Linear_Arrangement_with_distance_based_Set_1` | 3 | 6 | verified_unique | B | B | Independent answer verified. |
| `Mains_Topic_wise_Linear_Arrangement_with_distance_based_Set_1` | 3 | 7 | verified_unique | A | A | Independent answer verified. |
| `Mains_Topic_wise_Linear_Arrangement_with_distance_based_Set_1` | 3-4 | 8 | verified_unique | C | C | Independent answer verified. |
| `Mains_Topic_wise_Linear_Arrangement_with_distance_based_Set_1` | 4 | 9 | verified_unique | C | C | Independent answer verified. |
| `Mains_Topic_wise_Linear_Arrangement_with_distance_based_Set_1` | 4 | 10 | verified_unique | B | B | Independent answer verified. |

## Answer-key conflicts and unresolved key notes

- Mains_Topic_wise_Linear_Arrangement_with_distance_based_Set_1.pdf|p2|Q3: Printed key C (96m) is not independently verifiable because the transformed-row placement rule is incomplete.

## Held items

- Mains_Topic_wise_Linear_Based_Arrangement_Two_Variable_with_Vacant.pdf|p2-3|Q6: Written clue “three persons between R and Q” conflicts with the printed final arrangement, which places four persons between them; written-clue solver returns zero arrangements.
- Mains_Topic_wise_Linear_Based_Arrangement_Two_Variable_with_Vacant.pdf|p3|Q7: Written clue “three persons between R and Q” conflicts with the printed final arrangement, which places four persons between them; written-clue solver returns zero arrangements.
- Mains_Topic_wise_Linear_Based_Arrangement_Two_Variable_with_Vacant.pdf|p3|Q8: Written clue “three persons between R and Q” conflicts with the printed final arrangement, which places four persons between them; written-clue solver returns zero arrangements.
- Mains_Topic_wise_Linear_Based_Arrangement_Two_Variable_with_Vacant.pdf|p3|Q9: Written clue “three persons between R and Q” conflicts with the printed final arrangement, which places four persons between them; written-clue solver returns zero arrangements.
- Mains_Topic_wise_Linear_Based_Arrangement_Two_Variable_with_Vacant.pdf|p3-4|Q10: Written clue “three persons between R and Q” conflicts with the printed final arrangement, which places four persons between them; written-clue solver returns zero arrangements.
- Mains_Topic_wise_Linear_Based_Arrangement_Bi_Directional_Set_1.pdf|p1|Q1: Across five valid layouts, the red/grey/F facing statements yield ‘Only I’ in some layouts and ‘I and III’ in others; the latter combination is not even listed. No unique option is supported.
- Mains_Topic_wise_Linear_Based_Arrangement_Bi_Directional_Set_1.pdf|p1|Q2: Across valid layouts, the true relation about G changes (A in some layouts, D in another), and some layouts satisfy none of the listed relations. No unique option is supported.
- Mains_Topic_wise_Linear_Based_Arrangement_Bi_Directional_Set_1.pdf|p2|Q3: Across valid layouts, the queried third-right position is the Purple-color person in one layout, while in other layouts the target position falls outside the row. No unique answer is established.
- Mains_Topic_wise_Linear_Based_Arrangement_Bi_Directional_Set_1.pdf|p2|Q4: The five compared entities do not have one consistent outlier across all valid layouts: one layout makes White the direction outlier, while other valid layouts have multiple differing directions. The question has no invariant answer.
- Mains_Topic_wise_Linear_Based_Arrangement_Bi_Directional_Set_1.pdf|p2|Q5: C likes Red in one valid layout and Pink in the other valid layouts; the correct option changes.
- Mains_Topic_wise_Linear_Arrangement_with_distance_based_Set_1.pdf|p2|Q3: The transformation says the people are seated “at a consecutive multiple of 9m” but does not define the starting offset/interval sequence in row MN or how the remaining seven people continue the row at multiples of 5m. Applying the source phrasing in more than one reasonable way changes B-to-N; the printed key alone cannot resolve the missing placement rule.
- Mains_Topic_wise_Linear_Arrangement_with_distance_based_Set_1.pdf|p2|Q4: “At a consecutive multiple of 2m starting 12m from L” does not establish whether 12m is the first position followed by equal 2m intervals or whether adjacent intervals successively increase by multiples of 2m; these interpretations yield different distances and different options.

## Artifacts

- Reusable workflow: `C:\Users\shikh\Desktop\ssc-prep-platform\tmp\pdfs\arrangement_batch_audit\arrangement_audit_workflow.py`
- Linear solver: `C:\Users\shikh\Desktop\ssc-prep-platform\tmp\pdfs\arrangement_batch_audit\linear_reaudit_solvers.py`
- Solver/checkpoint details: `C:\Users\shikh\Desktop\ssc-prep-platform\tmp\pdfs\arrangement_batch_audit\linear_group_solutions.json`
- Resumable checkpoint: `C:\Users\shikh\Desktop\ssc-prep-platform\tmp\pdfs\arrangement_batch_audit\linear_review_checkpoint.json`
- Original-PDF text extraction: `C:\Users\shikh\Desktop\ssc-prep-platform\tmp\pdfs\arrangement_batch_audit\linear_original_pdf_extract.json`
- Live database verification: `C:\Users\shikh\Desktop\ssc-prep-platform\tmp\pdfs\arrangement_batch_audit\linear_database_live_verification.json`
- Per-set checkpoint snapshots: `C:\Users\shikh\Desktop\ssc-prep-platform\tmp\pdfs\arrangement_batch_audit\linear_checkpoints`
- Answer ledger: `C:\Users\shikh\Desktop\ssc-prep-platform\tmp\pdfs\arrangement_batch_audit\linear_arrangements_answer_ledger.json`
- Verified import dataset: `C:\Users\shikh\Desktop\ssc-prep-platform\backend\data\imports\reasoning\linear-arrangements\linear_arrangements_verified_import.json`
- No database import was performed; import JSON is prepared for later review only.
