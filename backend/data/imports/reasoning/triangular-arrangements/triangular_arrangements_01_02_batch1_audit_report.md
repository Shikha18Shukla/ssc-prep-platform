# Triangular Arrangements — Batch 1 audit

## Sources and destination
- `Triangular Arrangements 01  Class Notes.pdf` — 13 pages.
- `Triangular Arrangements 02 _ Class Notes.pdf.pdf` — 14 pages.
- Target chapter `a17ca992-53a7-44a8-8217-90cc130193fd` (`triangular-arrangements`); local `ssc_prep` baseline 0 active / 0 inactive.

## Classification
Six question appearances across five distinct prompts/groups: 4 verified unique candidates, 1 held, 1 duplicate occurrence. The Designation-Based recap heading on Set 01 p.2 is not a triangular question. The sports-group question in Set 01 is repeated in Set 02; its second appearance is linked to the first and not imported.

- Set 01 p.4 Q1 laptop brands: verified B. Enumeration fixing rotational symmetry gives U Acer, V Asus, W HP, X Apple, Y Dell, Z Sony.
- Set 01 p.7 Q2 cartoon/corners: verified D. Enumerated arrangement makes IV true and I–III false.
- Set 01 pp.9–10 Q3 sports/facing: held. More than one seating satisfies the written clues and the requested count relative to X changes; the key/diagram does not resolve the written-clue ambiguity.
- Set 02 p.4 sports question: duplicate of Set 01 Q3; excluded.
- Set 02 p.7 Q1 nine-person colour group: verified D; unique arrangement up to rotation places Kartik second right of Anuj and Kartik likes Blue.
- Set 02 p.11 Q1 inward colour group: verified B; unique arrangement up to rotation makes Red wearer and Abhay non-neighbours; other listed pairs are adjacent.

## Dry-run / import
`triangular_arrangements_01_02_batch1_verified_import.json` has 4 records. Dry-run: 4 eligible, 0 duplicate, 0 rejected, 0 errors. Transactional database write and read-back are recorded in the final batch report.

## Post-import verification
Imported IDs: Set 01 Q1 `120d3d02-6693-4c72-b35f-b0fadc167ba8`; Set 01 Q2 `12965b3d-529a-437f-b5ca-a7987cfbb098`; Set 02 p.7 `5dd8c62f-663c-4c99-92c9-9580a972a458`; Set 02 p.11 `9d802353-283b-435e-85a2-e04cf2aa44e4`. Final count: 4 active / 0 inactive. Replay: 4 duplicates, 0 inserts.
