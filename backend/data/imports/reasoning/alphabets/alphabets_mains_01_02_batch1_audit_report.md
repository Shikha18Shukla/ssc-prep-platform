# Alphabets (Mains) — Batch 1 audit

## Sources and destination
- `Alphabets 01  Class Notes.pdf` — 24 pages.
- `Alphabets 02  Class Notes.pdf` — 19 pages.
- Target `66584d54-40f0-4c96-9bb2-f2df0f09430b` (`alphabets-mains`); local baseline 0 active / 0 inactive.

## Question classification
The source set has prompts Q1–Q17 in Sheet 01 and Q1–Q12 in Sheet 02. Sheet 02 repeats Q1–Q12 from Sheet 01 (Q11–Q12 are visible on Sheet 01 physical p. 16); these are 12 duplicate appearances, not new questions. The selected Q11–Q12 import provenance remains Sheet 02 physical p. 17, which contains the same source questions. Five unique questions are verified import candidates (Q1, Q3, Q10–Q12); two are held (Q2, Q4); five Q5–Q9 prompts are arithmetic-operation content, wrong chapter; Q13–Q17 are held (physical pp. 18–22) because the supplied sequence lacks the number/letter content required by their instructions. No existing target rows were present.

- Q1 (Sheet 01 p.5): B. Derived Step 3 positions identify 5.
- Q2 (Sheet 01 p.7): held. The two middle elements are `>` then `1`, while the marked/listed pair is `1 >`; the prompt does not state whether order is material.
- Q3 (Sheet 01 p.7): B. In Step 1, fifth left of 1 is C.
- Q4 (Sheet 01 p.7): held. The odd-one-out relation among cross-step symbol/letter pairs is not uniquely specified by the source.
- Q10 (Sheet 01 p.15; repeated Sheet 02 p.15): B. Fourteenth from right in final Step 3 string is #.
- Q11 (Sheet 02 p.17): B. After removing symbols, eighth right of Z is 5.
- Q12 (Sheet 02 p.17): E. After reversing the last ten, ninth left of 8 is `$`, absent from choices.

## Dry-run / import
`alphabets_mains_01_02_batch1_verified_import.json` contains 5 unique records. Dry-run: 5 eligible, 0 duplicate, 0 rejected, 0 errors. Transactional write and read-back are recorded in the final batch report.

## Post-import verification
Imported IDs: Q1 `a32b8c8a-fec7-4e87-86a0-156516233f15`; Q3 `5e37b15d-40f1-4075-b825-906cc0003397`; Q10 `dee3967b-69f9-48ff-b0ff-611147772c68`; Q11 `95ea6e08-7474-42f8-ab64-fe50d370a408`; Q12 `5ee75067-7c93-45f2-ad61-cd65b723b6a3`. Final count: 5 active / 0 inactive. Replay: 5 duplicates, 0 inserts.
