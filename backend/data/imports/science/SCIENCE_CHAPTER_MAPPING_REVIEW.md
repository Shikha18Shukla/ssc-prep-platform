# Science Question-to-Chapter Mapping Review

All 21 source PDFs have a course/title page whose displayed course name generally matches its filename. That title page is not reliable provenance for the following DPP question pages: the first question page in multiple PDFs is visibly about another catalog chapter. Therefore this report records only a candidate topic for PDF page 2, not a bulk mapping for that PDF. Every question-level catalog assignment remains NEEDS_REVIEW until its own page is checked.

Subject slug: gk-gs. Category slug: science. Candidate chapter slugs below are existing catalog entries from app/database/ssc_catalog.py. No chapters were created, and no question has been assigned or imported from a filename alone.

| Source PDF | Page 2 OCR question/topic | Candidate existing chapter slug | Evidence / status |
|---|---|---|---|
| animal kingdom.pdf | Which of the following is a plant tissue? | tissues | Pages 2–7 and 11–21 visually mapped to Tissues; 8 verified records, 9 remain NEEDS_REVIEW because explanations are clipped/inconsistent; see review-datasets/tissues/tissues_review_report.md |
| brain and nervous system - science.pdf | Main excretory substance in mammals is… | excretory-system | Image inspected; question differs from title; NEEDS_REVIEW |
| cell -science.pdf | Pepsin digests… | digestive-system | Image inspected; question differs from title; VERIFIED for this page only; importer batch contains this one record |
| chemical reactions.pdf | Balanced equation for iron reacting with water | chemical-reaction | OCR-only sample; verify equation symbols and answer; NEEDS_REVIEW |
| chemistry in every day life.pdf | Velocity is a vector quantity because… | motion-and-force | Image inspected; question differs from title; NEEDS_REVIEW |
| circulatory system - science.pdf | Valve between the left atrium and left ventricle | circulatory-system | OCR-only sample; likely title match; NEEDS_REVIEW |
| Digestive system - science.pdf | Which enzyme is present in saliva? | digestive-system | OCR-only sample; likely title match; NEEDS_REVIEW |
| Disease.pdf | Effect of hypothalamus failure on pituitary regulation | glands | OCR-only sample; likely endocrine topic; NEEDS_REVIEW |
| excretory system - science.pdf | Which protein is found in hair? | (unassigned) | Topic is not sufficiently specific for a chapter; NEEDS_REVIEW |
| Glands.pdf | Number of bones in an adult human | skeleton-system | OCR-only sample; chapter has no filename-matched PDF; NEEDS_REVIEW |
| gravitational work and energy.pdf | Plane containing incident and reflected rays | optics-and-human-eye | OCR-only sample; question differs from title; NEEDS_REVIEW |
| matter and atoms.pdf | Only non-metallic element liquid at room temperature | metals-and-non-metals | OCR-only sample; likely topic match; NEEDS_REVIEW |
| metal and non metals.pdf | Who introduced the term “triads”? | periodic-table | OCR-only sample; question differs from title; NEEDS_REVIEW |
| motion and force.pdf | Gravitational force between two masses | gravitation-work-energy | OCR-only sample; likely topic match; NEEDS_REVIEW |
| nutrition - science.pdf | Jaundice and excess bilirubin | disease | OCR-only sample; question differs from title; NEEDS_REVIEW |
| optics and human eye.pdf | Why sound waves require a material medium | sound | OCR-only sample; question differs from title; NEEDS_REVIEW |
| periodic table.pdf | Calcium oxide reacting with water to form slaked lime | chemical-reaction | OCR-only sample; question differs from title; NEEDS_REVIEW |
| reproduction.pdf | Plants dependent on water for sexual reproduction | plant-kingdom | OCR-only sample; chapter has no filename-matched PDF; NEEDS_REVIEW |
| respiratory system - science.pdf | Dendron and axon are parts of the… | brain-and-nervous-system | Image inspected; question differs from title; NEEDS_REVIEW |
| sound.pdf | Magnetic field around a current-carrying conductor | (no filename-matched chapter) | Image inspected; likely magnetic-effect-and-heating, which has no filename-matched PDF; NEEDS_REVIEW |
| Tissues.pdf | Characteristic distinguishing a gas from other states of matter | matter-and-atom | Image inspected; question differs from title; NEEDS_REVIEW |

## Mapping rules applied

- Only existing subject/category/chapter slugs are candidates; database UUIDs are not needed by the CSV importer.
- Page 2 is one sample per PDF. It does not determine the content of later pages.
- The green correct-answer treatment and explanation are visual source evidence, but they do not by themselves prove that every OCR transcription or chapter assignment is correct.
- Cell PDF page 2 is the sole fully structured/verified record so far; it is assigned to digestive-system based on question content, not the Cell filename.
- Topics without a confident catalog match remain unassigned. Do not make an import batch until all four options, answer, explanation, difficulty/PYQ label, page reference, and chapter mapping are reviewed question by question.


## Circulatory System batch mapping (2026-10-10)

- Catalog chapter: `Circulatory System`, slug `circulatory-system`, ID `c0f428cb-d838-4a93-82ec-74000df22efc`; confirmed through a read-only catalog query under `gk-gs/science`. No catalog row was created or changed.
- Question-level candidates were selected from dedicated Circulatory System pages 2–16, 18, 20 and cross-topic Digestive PDF pages 9, 11, 13, 16–26 based on page content.
- Dedicated PDF pages 17, 19, and 21 are rejected as unrelated topics. Other candidate pages with clipped explanations remain pending. See `review-datasets/circulatory-system/circulatory-system_review.csv`.


## Respiratory System batch mapping (2026-10-10)

- Existing catalog chapter: `Respiratory System`, slug `respiratory-system`, ID `6afa7d76-1379-4a79-9ff5-1f934331af92`, confirmed read-only under `gk-gs/science`.
- All 21 question pages of `respiratory system - science.pdf` (pp. 2–22) were rendered and reviewed. They are Brain & Nervous System content (pp. 2–18, 20–22) or Skeleton System content (p. 19), not Respiratory System. Page 18 asks which brain part controls breathing and maps to Brain & Nervous System. Pages 3–4 are repeated CNS questions; p. 3 is a confirmed duplicate of p. 4.
- Additional respiratory-disease questions in `nutrition - science.pdf` pp. 18, 20, and 21 map by content to the existing Disease chapter.
- Cross-corpus search found `circulatory system - science.pdf` p. 17, “Which of the following is not the objective of the respiratory system?” The complete page image shows answer C and a supporting explanation. This ordinary MEDIUM question maps to Respiratory System. It supersedes the earlier Circulatory-scoped rejection in the central decision ledger; the historical rejection remains preserved. It is prepared, not imported.
- Carbon/Physics OCR and source-page searches verified one Carbon & Its Compound question about fatty-acid saturation (`excretory system - science.pdf` p. 6). Saponification at `chemical reactions.pdf` p. 8 remains pending because its explanation is clipped. Carbon-dioxide/limewater and non-metal conductivity topics fit existing specific chapters. No question was confidently mapped to the general Physics Revision chapter; horsepower-to-watts fits Gravitation Work Energy.
- Details and dispositions are in `review-datasets/respiratory-system/respiratory-system_review.csv` and the chapter report.


## Brain & Nervous System chapter mapping (2026-10-10)

- Existing catalog chapter: `Brain & Nervous System`, slug `brain-and-nervous-system`, ID `2237850c-bf16-4627-970a-33f548ae8398`, confirmed in a read-only query under `gk-gs/science`. No catalog changes were made.
- Visually reviewed all 21 question pages in `respiratory system - science.pdf` (pp. 2–22). Brain & Nervous System questions occur on pp. 2–18 and 20–22 (19 distinct candidates); p. 3 duplicates p. 4; p. 19 is Skeleton System.
- Also visually sampled the 20 question pages in `brain and nervous system - science.pdf` (pp. 2–21). They concern excretion and do not provide additional chapter candidates despite the title.
- Searched OCR queue/transcripts across all Science sources for brain, CNS/PNS, neuron, synapse, brain regions, spinal cord, reflex, and related terms. `Disease.pdf` p. 15 (“Hypothalamus is part of which organ…”) maps to this chapter by question content but remains pending because its explanation is clipped. Hormone/gland questions on Disease pp. 2, 14, and 21 were not assigned to this chapter.
- Brain review dispositions: 14 verified (9 ordinary, 5 PYQ), 6 NEEDS_REVIEW, 1 outside-chapter rejection, and 1 confirmed duplicate source record. See `review-datasets/brain-and-nervous-system/brain-and-nervous-system_review.csv`.


## Excretory System chapter mapping (2026-10-10)

- Existing catalog chapter: `Excretory System`, slug `excretory-system`, ID `f5dabc77-d970-46a4-960f-deb6ecb2c8fb`, confirmed by read-only catalog lookup under `gk-gs/science`; no catalog changes were made.
- All 20 question pages in `brain and nervous system - science.pdf` (pp. 2–21) contain Excretory System questions despite the PDF title. The first 19 pages were treated as candidates; pp. 19, 20, and 21 duplicate pp. 2, 7, and 12 respectively.
- Searched the remaining Science OCR transcripts for excretion, kidney, urine, urea, ammonia, uric acid, nephron, ureter, bladder, and nitrogenous-waste topics. No additional confidently mappable Excretory System question was identified. The nominal `excretory system - science.pdf` contains nutrition/protein questions on its reviewed pages and was not mapped by filename.
- Dispositions for the 20 source rows: 10 verified, 7 needs review, 3 confirmed duplicates, 0 rejected. The pending records include six clipped explanations and one internally inconsistent stem/options item. See `review-datasets/excretory-system/excretory-system_review_report.md`.


## Disease chapter mapping (2026-10-10)

- Existing catalog chapter: `Disease`, slug `disease`, ID `79eeb111-c0df-4863-aac2-94086844f83b`, confirmed by a read-only query under `gk-gs/science`. Existing `Glands` chapter: slug `glands`, ID `3a7d5736-5a65-434b-8c2c-0f17905bab57`.
- All Disease.pdf question pages (pp. 2–21) were inspected individually. Disease questions are pp. 4–7 and 9. Glands questions are pp. 2, 3, 8, 10–14, and 16–21; these were routed to the existing Glands chapter in the queue and remain pending for a separate Glands batch. Page 15 asks which organ contains the hypothalamus and remains in its prior Brain & Nervous System review decision.
- All 20 question pages of `nutrition - science.pdf` (pp. 2–21) were reviewed and map to Disease/health content. This includes pp. 18, 20, and 21 that a previous Respiratory System review excluded as outside its chapter; that review decision remains preserved in its existing dataset and was not treated as a duplicate.
- Other OCR hits mentioning disease-related words were checked for topic: a stomach-acid question remains Digestive, bacterial cell-envelope content remains Cell, and a Plasmodium question in `Glands.pdf` tests asexual reproduction. No additional Disease candidates were added.
- Disease dispositions: 11 verified (10 ordinary, 1 PYQ), 14 NEEDS_REVIEW, 0 rejected, 0 duplicates. See `review-datasets/disease/disease_review_report.md`.


## Glands chapter mapping (2026-10-10)

- Existing catalog chapter: **Glands**, slug `glands`, ID `3a7d5736-5a65-434b-8c2c-0f17905bab57`, under `gk-gs/science`; no duplicate chapter was created.
- The 14 reserved `Disease.pdf` pages (pp. 2, 3, 8, 10–14, 16–21) were visually reviewed and map to Glands by endocrine question content. Page 15 remains assigned to Brain & Nervous System as recorded earlier.
- Searching the OCR transcripts from all Science PDFs identified one additional Glands candidate in `Glands.pdf` p. 30, asking which accessory glands add secretions along the vas deferens. The answer/options and MEDIUM label are visible; the explanation is clipped, so it remains pending. Other pages in that mislabeled PDF concern skeletal or reproductive-system questions. The salivary-gland question in `cell -science.pdf` p. 20 retains its earlier Digestive System assignment.
- Glands dispositions: 2 verified, 13 NEEDS_REVIEW, 0 rejected within the 15 Glands candidates. The 2 verified questions are `Disease.pdf` pp. 8 and 13. See `review-datasets/glands/glands_review.csv` and its report.


## Batch readiness cross-check (2026-10-10)

Live-catalog IDs and importer mappings for the nine audited chapters are recorded in SCIENCE_BATCH_READINESS_AUDIT.md. The Digestive review CSV stale UUID was corrected to the live `digestive-system` UUID; verified status and eligibility did not change. Cross-file mappings remain content-based: Animal Kingdom→Tissues pages in `animal kingdom.pdf`, respiratory-titled source→Brain & Nervous System, brain-titled source→Excretory System, and mixed Disease.pdf mappings.


## Carbon & Its Compound cross-corpus review (2026-10-10)

- `excretory system - science.pdf` p. 6 asks for the chemical-structure classification of fatty acids. Image review confirms the complete question/options, correct answer B, MEDIUM label, and explanation distinguishing carbon-chain saturation. It maps to Carbon & Its Compound and is prepared as one ordinary row; no duplicate was found in the active bank or prepared imports.
- `chemical reactions.pdf` p. 8 asks which saponification statement is false; option D is marked, but the solution is clipped at the page edge, so it remains pending and excluded. The separate p. 6 soap-production candidate remains a duplicate of p. 9.
- Other carbon-related candidates were assigned to more specific chapters by question content: matter/non-metal properties, chemical reaction, and acid/base chemistry. Full details are in `review-datasets/carbon-and-its-compound/`.


## Physics Revision corpus review (2026-10-10)

- OCR/source review across the supplied Physics-topic PDFs found specific questions on motion/force, gravitation/work/energy, optics, sound, electricity, and magnetic effects. These map to their named chapters. The horsepower-to-watts question (`gravitational work and energy.pdf` p. 31) was visually verified and fits power/work-energy; it was not reassigned to general Physics Revision. No verified Physics Revision candidate was identified.
