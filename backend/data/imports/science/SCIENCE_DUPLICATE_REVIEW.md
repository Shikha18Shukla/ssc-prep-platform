# Science Possible Duplicate Review

OCR-prefix similarity produced 17 candidate pairs at a 0.90 threshold after the Excretory System review. Six pairs are confirmed by visual/content review and 11 remain unresolved leads. OCR errors, repeated question stems, and truncated page text can create false positives.

| Similarity | Type | Source A | Page | Source B | Page | OCR question prefix |
|---:|---|---|---:|---|---:|---|
| 1.000 | CONFIRMED duplicate | Digestive system - science.pdf | 6 | Digestive system - science.pdf | 27 | the inner walls of the small intestine have thousands of finger like outgrowths these are called |
| 1.000 | exact OCR prefix | Tissues.pdf | 19 | Tissues.pdf | 28 | which of the following options does not represent a property of solids c3 it is not difficult to change their shape they have dist |
| 1.000 | exact OCR prefix | brain and nervous system - science.pdf | 12 | brain and nervous system - science.pdf | 21 | main excretory product in birds and reptile |
| 1.000 | exact OCR prefix | brain and nervous system - science.pdf | 2 | brain and nervous system - science.pdf | 19 | main excretory substance in mammals is b |
| 1.000 | CONFIRMED duplicate | cell -science.pdf | 4 | cell -science.pdf | 17 | which among the following is the food tub |
| 1.000 | exact OCR prefix | matter and atoms.pdf | 7 | matter and atoms.pdf | 20 | hit crs toro tym mrcentei cots eg metals react with acids and |
| 1.000 | exact OCR prefix | matter and atoms.pdf | 9 | matter and atoms.pdf | 18 | which of the following is the most reactive metal b |
| 0.983 | CONFIRMED duplicate | respiratory system - science.pdf | 3 | respiratory system - science.pdf | 4 | which one of the following makes up the central nervous system together with the brain |
| 0.980 | near-duplicate candidate | optics and human eye.pdf | 3 | optics and human eye.pdf | 4 | which type of sound waves can propagate in solids |
| 0.979 | near-duplicate candidate | brain and nervous system - science.pdf | 7 | brain and nervous system - science.pdf | 20 | the waste product released by the excretory system of fish is mostly b |
| 0.977 | near-duplicate candidate | Tissues.pdf | 4 | Tissues.pdf | 30 | plasma is often called the state of matter 8 |
| 0.949 | near-duplicate candidate | cell -science.pdf | 27 | Digestive system - science.pdf | 17 | which among the following statements is incorrect b |
| 0.912 | near-duplicate candidate | nutrition - science.pdf | 4 | nutrition - science.pdf | 18 | which microorganism is responsible for causing malaria b |
| 0.909 | near-duplicate candidate | chemistry in every day life.pdf | 9 | motion and force.pdf | 10 | which of the following is not an example of a body at rest b |
| 1.000 | CONFIRMED duplicate | brain and nervous system - science.pdf | 2 | brain and nervous system - science.pdf | 19 | main excretory substance in mammals is |
| 1.000 | CONFIRMED duplicate | brain and nervous system - science.pdf | 7 | brain and nervous system - science.pdf | 20 | the waste product released by the excretory system of fish is mostly |
| 1.000 | CONFIRMED duplicate | brain and nervous system - science.pdf | 12 | brain and nervous system - science.pdf | 21 | main excretory product in birds and reptiles |


## Tissues batch duplicate audit (2026-10-10)

The 17 Tissues candidates from `animal kingdom.pdf` pages 2–7 and 11–21 were compared against the active question bank (33 active questions), all OCR queue stems, and previously reviewed Science import batches. No exact match or near match at similarity ≥0.88 was found. One lower-similarity OCR lead (0.813) paired page 14, “Which of the following is a characteristic of permanent tissue?”, with `Tissues.pdf` page 5, “Which of the following is not a characteristic of a solid?”; visual/content comparison confirms these are different topics, not duplicates. No Tissues candidate was classified as a duplicate. At the time of this Tissues audit, all 14 global possible-pair leads were unresolved. The later Digestive System audit below confirmed two of those pairs and left 12 unresolved.

## Digestive System batch duplicate audit (2026-10-10)

The 31 Digestive System candidates (Digestive system - science.pdf pages 2–8, 10, 12, 14–15, 27–31; cell -science.pdf pages 2–5, 10–20) were checked against all 33 active database questions and the 12 prior verified Science-batch rows (excluding the already-reviewed Cell page 2 as a self-match). No matching active Science question or prior-batch duplicate was found. The highest database text similarity was 0.414 to an unrelated percentage question. A 0.693 lexical score caused by “Which among the following” was visually/content checked and is not a duplicate.

Three source duplicates are confirmed by page-image comparison:

| Source page | Duplicate of | Decision |
|---|---|---|
| Digestive system - science.pdf, p. 27 | Digestive system - science.pdf, p. 6 | Same question/options/answer/explanation; p. 27 excluded; p. 6 remains NEEDS_REVIEW due to explanation conflict. |
| cell -science.pdf, p. 17 | cell -science.pdf, p. 4 | Exact repeated PYQ 2020 food-tube question; p. 17 excluded; p. 4 remains NEEDS_REVIEW due to clipped explanation. |
| Digestive system - science.pdf, p. 28 | Digestive system - science.pdf, p. 2 | Semantic duplicate: “amylase” and “ptyalin” name the same salivary enzyme; p. 28 excluded. |

Twelve of the 14 earlier global OCR-pair leads remain unresolved as recorded above; the other two pairs were confirmed only after page-image/content comparison. The page 28 semantic duplicate is an additional confirmed duplicate not surfaced as a global high-similarity pair.


## Circulatory System batch duplicate audit (2026-10-10)

The 31 topic-relevant candidates (dedicated Circulatory PDF pages 2–16, 18, 20; Digestive PDF pages 9, 11, 13, 16–26) were reviewed against active question rows and all earlier import-ready chapter batches. All 31 candidate question stems were compared with 33 active DB rows and 23 earlier verified batch rows, and all candidate pairs were compared within the batch. One cross-catalog score of 0.718 (Circulatory p. 3 vs a salivary-gland question) is a generic “Which of the following…” overlap; the actual stems, topics, and options differ. The within-batch leads were p. 15 vs p. 18 (four-chambered vs three-chambered heart) and Digestive PDF p. 9 vs p. 11 (organ vs body-system question); they are related concepts but distinct questions/options. No duplicate was confirmed; similar concepts such as arterial/venous flow were not treated as duplicates. Three pages in the dedicated file (17 respiratory objective, 19 ATP, 21 plant respiration) were rejected as out of chapter scope and are not duplicates.


## Respiratory System source audit (2026-10-10)

The purported Respiratory System PDF contains 21 question pages (pp. 2–22); page-image review shows 20 Brain & Nervous System questions and one Skeleton System question, with no question that maps to the Respiratory System chapter. The p. 3/p. 4 lead above is an exact duplicate: both have the same stem, four options in the same order, and the same correct answer. Page 3 is the duplicate record; page 4 is retained as the more complete explanation capture.

Three additional respiratory-disease questions in `nutrition - science.pdf` (pp. 18, 20, 21: pneumonia, bronchitis, and pertussis) map to the existing Disease chapter, not Respiratory System. The 24 source rows were checked against 33 active question-bank records and all 123 rows in previous Science review datasets/import batches. No cross-bank duplicate was confirmed. Similarity leads (Respiratory PDF p. 16 vs a prior heart-valve question, 0.818; Nutrition PDF p. 21 vs a generic “incorrect statement” question, 0.752) were manually compared and are distinct questions.

Following this audit, 3 OCR-suggested pairs are confirmed and 11 remain unresolved; 4 duplicate source records are confirmed overall (3 earlier source duplicates plus Respiratory PDF p. 3).


## Brain & Nervous System duplicate audit (2026-10-10)

The 20 distinct Brain & Nervous System candidates (19 questions in `respiratory system - science.pdf` pp. 2–18 and 20–22, plus the mapped candidate from `Disease.pdf` p. 15) were compared against all 33 active question-bank rows and all 99 prior chapter-review rows (85 with a nonempty question stem, including every prior import-ready batch row). No cross-bank or prior-batch duplicate was confirmed. The confirmed source duplicate is Respiratory PDF p. 3 vs. p. 4; p. 3 is excluded and p. 4 is retained.

One text-similarity lead (Respiratory PDF p. 16 vs. Circulatory System PDF p. 3; the previous OCR score was 0.818) was checked against the page images and content: p. 16 asks which structure is not part of the hindbrain, while the other asks which structure is not a heart valve. They are not duplicates. No new confirmed duplicate pair or duplicate record was added by this review.

## Excretory System batch duplicate audit (2026-10-10)

All 20 question pages (pp. 2–21) of `brain and nervous system - science.pdf` were visually reviewed. Candidates were compared with the 33 active question-bank records and all previously prepared Science chapter batches. No duplicate against the active bank or prior batches was confirmed; maximum active-question stem similarity was 0.412. The highest prior-batch scores (0.830) came from generic “Which of the following…” phrasing; full stems, options, and topics differ. Three exact within-source duplicate pairs were confirmed by matching question, all options/order, marked answer, and explanation where present: pp. 2/19, pp. 7/20, and pp. 12/21. The earlier page in each pair is retained. Pages 2 and 7 remain pending because their explanations are clipped; page 12 is verified. The global duplicate ledger now contains 17 candidate pairs: 6 confirmed and 11 unresolved, representing 7 duplicate source records overall.

## Disease batch duplicate audit (2026-10-10)

The 25 Disease candidates (Disease.pdf pp. 4–7, 9 and `nutrition - science.pdf` pp. 2–21) were compared with all 33 active question-bank records and prior Science review batches, excluding self-matches to the same source page in earlier out-of-scope review datasets. No duplicate against the active bank or a previous different source page was confirmed; maximum active-question stem similarity was 0.420. The largest prior-batch text lead was 0.826 between Nutrition p. 6 (“Which of the following combinations is correct?”) and prior Digestive PDF p. 17 / p. 30 “Which of the following statements is INCORRECT?” items. Their stems, options, answers, and topics differ; the match is generic wording. Another high lexical match (0.909) between Nutrition p. 4 (malaria) and Nutrition p. 18 (pneumonia) uses the same “Which microorganism…” pattern but asks different diseases with different correct organisms and options. These are distinct questions. Nutrition pp. 18, 20, and 21 were already present as rejected-from-Respiratory-scope rows; those same-page records are rescope history, not duplicates. No Disease candidate was classified as a duplicate.


## Glands batch duplicate audit (2026-10-10)

The 15 Glands candidates (`Disease.pdf` pp. 2, 3, 8, 10–14, 16–21 and `Glands.pdf` p. 30) were compared with all 44 active question records and 249 prior non-Glands review/import rows, including the completed Disease batch. No exact stem match or cross-source match with stem similarity >=0.80 was found. The highest active stem score was 0.650; its candidate and active questions ask unrelated disease topics. The highest prior score was 0.667 and came from generic wording. Related endocrine concepts within this batch (hormone roles; endocrine/exocrine distinction; growth-hormone source) are distinct stems/options, not duplicates. No cross-bank, prior-batch, or within-batch duplicate was confirmed.


## 2026-10-10 earlier database and batch reconciliation

The earlier snapshot contained 44 active questions and the prepared chapter importer batches. Disease CSV rows matched their own active database rows and were not new duplicate candidates. Four high lexical-similarity leads were manually checked and found distinct by complete content/options/answer. This historical snapshot is superseded by the current 108-question read-only snapshot below. Existing duplicate and mapping decisions were preserved.

## Supplemental source-page duplicate check — 2026-10-10

The 18 currently import-eligible supplemental records were compared by normalized stem with the 75 existing Science importer rows (the same eight batches that reconcile to the 75 active Science database questions) and against one another. The highest lexical similarity against the existing Science rows was 0.612; manual review found the scored leads below to be unrelated questions using generic wording. The full similarity score is a review lead, not a duplicate verdict.

| Similarity | Supplemental question | Compared question | Disposition |
|---:|---|---|---|
| 0.612 | Nutrition: “Kwashiorkor is caused by which deficiency?” | Disease: Typhoid pathogen question | Different deficiency and pathogen facts; generic “caused by which” wording. |
| 0.571 | Electricity: SI unit of electric charge | Circulatory: function of vein valves | Different subject and fact; generic “what is the” form. |
| 0.539 | Reproduction: asexual reproduction type in Amoeba | Circulatory: function of vein valves | Different fact and chapter. |
| 0.539 | Chemistry in Every Day Life: sodium hydroxide application | Disease: Typhoid pathogen question | Different fact and chapter. |
| 0.500 | Chemistry in Every Day Life: saponification reagent | Disease: disease/vector matching | Different fact and chapter. |

One within-supplement semantic overlap was identified: chemical reactions.pdf p. 6 and p. 9 both ask about sodium hydroxide’s role in soap production. Page 6 is marked DUPLICATE and excluded from the importer file; page 9 is retained as the explicit PYQ. One Sound record remains NEEDS_REVIEW because its marked answer conflicts with the scientifically correct option. The remaining supplemental stems were manually reviewed and no likely exact or semantic duplicates were found. The supplemental importer dry-run is in memory and therefore proves file validity, not against-live-database duplicate status.

## Historical pre-supplement database snapshot

At that pre-supplement snapshot, the live database had 108 active questions total, including 75 Science questions across 28 chapters. This historical value is superseded by the later read-only snapshot below.

## Source-page supplement decision correction — 2026-10-10

The original scanned source `C:\Users\shikh\Documents\chemical reactions.pdf` was rendered and visually checked at PDF pages 6 and 9. Page 6 asks, “Which of the following substances is commonly used in the saponification process to produce soap?” Its options are sodium bicarbonate, sodium chloride, sodium hydroxide, and sodium carbonate; the green correct marker is on option 3, sodium hydroxide. Its solution explains that saponification uses a strong alkali and that sodium hydroxide is the primary substance used to make solid soap. Page 9 asks, “Sodium Hydroxide is used:” with options antacid, alkaline batteries, manufacturing of soap, and cleansing agent; option 3 is marked correct. Its solution says sodium hydroxide is widely used in soap and detergent manufacturing through saponification.

These are not textually identical questions, but the complete options, marked answers, and explanations show that both test the same fact: sodium hydroxide is used to manufacture soap by saponification. Page 6 is therefore classified as a semantic duplicate and excluded; page 9 is kept as the explicit PYQ 2022 source record. The duplicate decision does not rest on stem similarity alone.

The source-page review CSV already recorded page 6 as `DUPLICATE` and excluded it. The central decision ledger and global queue had an older `VERIFIED` entry for the same source page. On 2026-10-10, the ledger was corrected to `DUPLICATE`; its new note preserves the previous VERIFIED decision and note as superseded history. The review CSV and generated queue now agree with that decision. Page 6 remains absent from importer CSVs, and the separate Sound record remains `NEEDS_REVIEW` and excluded.

At the pre-import snapshot, the live database was queried read-only and 108 active questions were checked. Page 6 had no exact normalized stem match in the active bank. The approved 18 supplement rows were checked against all active questions, all 75 pre-existing Science importer rows, and one another. This historical review is retained; the source-page supplement was later imported and post-verified.

## Sound candidate duplicate audit — 2026-10-10

Five visually verified Sound candidates (`optics and human eye.pdf` pp. 4, 9–12) were compared against all 126 active question stems and the 93 pre-existing Science importer rows. No exact match was found; the highest lexical lead among those five was 0.525 against an unrelated Amoeba question. Across all reviewed pages, the largest lead was 0.818 for pending page 8, a generic “Which of the following statements is INCORRECT?” match to a Circulatory System blood-function question. Its options, answer, explanation, and topic differ. No semantic duplicate was confirmed among the five prepared rows. Page 3 is a source duplicate of page 4 and is excluded; page 4 is retained with the complete explanation. Pages 2 and 5–8 remain excluded/pending for the reasons documented in the Sound review report.

## Current read-only database snapshot — 2026-10-10

A new read-only query confirmed 126 active questions total, including 93 Science questions across 28 chapters. Per-chapter ordinary/PYQ counts are documented in SCIENCE_COVERAGE_MATRIX.md.

## Acid Base & Salt candidate duplicate audit — 2026-10-10

Before import, two candidates (`chemical reactions.pdf` p.10 and `matter and atoms.pdf` p.15) were checked read-only against all 126 active questions and all 98 other prepared Science rows. No complete exact/near match of stem, options, and correct answer was found. The closest active-bank stem similarities were 0.618 and 0.463 respectively; these are not duplicate evidence. Both rows were subsequently imported and verified as part of the approved seven-row follow-up batch.

## Approved follow-up duplicate check — 2026-10-10

All seven approved rows were checked against the 126 active pre-import questions and the other prepared Science rows. No complete question/options/correct-answer duplicate was found. The live importer dry-run also reported zero duplicates. The approved rows were then imported once transactionally; page 2 Sound remains pending, page 3 remains excluded as a duplicate of page 4, and pages 5–8 remain excluded.
