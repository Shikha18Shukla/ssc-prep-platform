# Five-Chapter Verified PDF Question Integration — Final Report

Database: local `ssc_prep` at `127.0.0.1:5432`. Per-chapter inserts and soft-retirements were performed in isolated transactions. No held questions were imported; no existing records were deleted or altered except the planned `is_active=false` changes.

| Chapter | PDF questions added | Original questions retired | Final active | Final inactive |
|---|---:|---:|---:|---:|
| Scheduling Puzzles – Month Based | 6 | 6 | 40 | 6 |
| Scheduling Puzzles – Year Based | 9 | 9 | 40 | 9 |
| HOT Category Puzzles – Flat + Floor Based | 4 | 4 | 40 | 4 |
| HOT Category Puzzles – Uncertain Seating Arrangement Based | 11 | 11 | 40 | 11 |
| Inequality (Mains) | 7 | 7 | 40 | 7 |

## Verification

- All five importer dry-runs passed before writes: 37 eligible, 0 duplicates, 0 rejected, 0 errors.
- Every chapter transaction verified 40 active questions and the planned inactive count before commit.
- All 200 pre-existing records were checked for five options, exactly one correct answer, and non-empty explanation before writes. The 163 retained records were verified unchanged; 37 selected original records changed only to inactive.
- All 37 inserted records were checked for exact chapter, five options, exactly one correct option, explanation, source filename/page metadata, and active status.
- Import replay for each chapter reported zero new inserts and all batch rows as duplicates.
- No migrations, schema changes, `.env` changes, unrelated tests, commits, or pushes were performed.

Full before/after records: `backend/data/imports/reasoning/five_chapters_pdf_integration_record_ledger.json`.
Import JSON, answer ledgers, and audit reports were updated in each chapter folder.

## Inserted and retired record IDs

### Scheduling Puzzles – Month Based

Inserted PDF questions:

- `f9b3b50f-74a6-462f-9954-54e1ca5204ad` — PDF: Scheduling Puzzles Month Based 02  Class Notes.pdf; physical page(s) 4-6 — answer D: Bajaj
- `44a1f464-8996-400f-a6b6-6afe0d19eb2e` — PDF: Scheduling Puzzles Month Based 02  Class Notes.pdf; physical page(s) 10-12 — answer E: September
- `55d20fde-e442-45b3-b4e9-15cec18a03cf` — PDF: Scheduling Puzzles Month Based 02  Class Notes.pdf; physical page(s) 13-14 — answer B: Israel
- `f99afef5-af9b-4324-ad64-b96c2b8a5c6c` — PDF: Scheduling Puzzles Month Based 04  Class Notes.pdf; physical page(s) 19-21 — answer B: September
- `cf5e0ae1-d0e4-4939-a05e-a5fd5e8dc617` — PDF: Scheduling Puzzles Month Based 04  Class Notes.pdf; physical page(s) 23-25 — answer B: September
- `9ba26ad0-b2f3-4299-b26e-81f9caea1d92` — PDF: Scheduling Puzzles Month Based 05 Class Notes.pdf; physical page(s) 8-11 — answer D: U-Delhi

Soft-deactivated original questions:

- `249f4365-573d-4159-8b3b-36d724ca5d97` — In which month is A scheduled?
- `613436c9-0c8a-4541-bfa1-fce90b9e12a0` — In which month is B scheduled?
- `cb2ea773-5f0b-483a-9118-3fc4a63b568a` — In which month is E scheduled?
- `36845130-dac1-4a2a-a6b7-2cf675d19b7b` — In which month is E scheduled?
- `c9908082-b147-408f-901d-ae7499996867` — In which month is F scheduled?
- `27dad3e0-72a4-4391-bc8a-0fb0a9d0fa6e` — In which month is A scheduled?

### Scheduling Puzzles – Year Based

Inserted PDF questions:

- `d7c01a4e-d5d4-44fc-899e-e152104e5c70` — PDF: Scheduling Puzzles Year Based Puzzles 01 Class Notes.pdf; physical page(s) 4-6 — answer D: 1985
- `764fde7d-75b0-4621-b9f1-2f47e33a0ac2` — PDF: Scheduling Puzzles Year Based Puzzles 01 Class Notes.pdf; physical page(s) 7-9 — answer A: The person born immediately before P
- `4614057b-a0d1-40e8-b577-85979107f11a` — PDF: Scheduling Puzzles Year Based Puzzles 01 Class Notes.pdf; physical page(s) 10-12 — answer B: 1990
- `b15c459d-a56b-414e-854a-d071734f81ab` — PDF: Scheduling Puzzles Year Based Puzzles 02 Class Notes-.pdf; physical page(s) 5-7 — answer D: I
- `0a9988cb-ccf5-422e-930d-037d3062cc6f` — PDF: Scheduling Puzzles Year Based Puzzles 02 Class Notes-.pdf; physical page(s) 8-10 — answer C: Eight years younger than F
- `3f66d27d-9a07-4134-8a6f-0dce0bcbf095` — PDF: Scheduling Puzzles Year Based Puzzles 03 _ Class Notes.pdf; physical page(s) 4-6 — answer C: B
- `73c304c8-6048-43d8-9b06-6fc1d54d7831` — PDF: Scheduling Puzzles Year Based Puzzles 03 _ Class Notes.pdf; physical page(s) 7-9 — answer C: 12
- `f440b403-323c-43af-89f8-5796cba21345` — PDF: Scheduling Puzzles Year Based Puzzles 03 _ Class Notes.pdf; physical page(s) 10-13 — answer E: Both C & D
- `91fa4b0d-9930-4a73-bd69-aa4afbbfff10` — PDF: Scheduling Puzzles Year Based Puzzles 04 _ Class Notes.pdf; physical page(s) 8-11 — answer B: The one who is three years younger than V

Soft-deactivated original questions:

- `bff3a14b-d71a-4fac-9372-ead69ded72ae` — In which year was A born?
- `d3873c2c-561c-4382-acfe-ba7d4a3c6201` — In which year was D born?
- `e04ee40c-fc0c-4fcc-a995-fd16d1aa2ab8` — In which year was B born?
- `9b3dca10-ea45-4b71-9270-a36a1b511a79` — In which year was A born?
- `fc7fb563-5124-4588-ac9c-921eb666ed2b` — In which year was C born?
- `175c61b0-4391-4f11-97b5-b40861d40919` — In which year was F born?
- `ef159da3-485b-444d-bc7c-ccf8ef8498d5` — In which year was A born?
- `dddc281a-f519-4563-9bf6-47dc9ceb0cec` — In which year was A born?
- `153f3b32-5809-4c8f-bc7c-908a8f0eb066` — In which year was C born?

### HOT Category Puzzles – Flat + Floor Based

Inserted PDF questions:

- `5893029d-3ac6-4755-979c-9c3ed2d7e315` — PDF: HOT Category Puzzles Flat   Floor puzzles based 01 _ Class Notes.pdf.pdf; physical page(s) 5-7 — answer C: T
- `7755622a-824c-4189-9728-2a572781d712` — PDF: HOT Category Puzzles Flat   Floor puzzles based 02 _ Class Notes.pdf; physical page(s) 4-6; printed Q1 — answer B: B
- `89e7ae3c-e273-4ce9-8d19-78da1f20025e` — PDF: HOT Category Puzzles Flat   Floor puzzles based 02 _ Class Notes.pdf; physical page(s) 7-9; printed Q6 — answer C: F
- `004b1ce5-84ae-4703-b898-4e2694d073b6` — PDF: HOT Category Puzzles Flat   Floor puzzles based 02 _ Class Notes.pdf; physical page(s) 10-13; printed Q11 — answer D: U, R, Z

Soft-deactivated original questions:

- `25eb852a-5cde-425a-bfdf-f856d7fd0e0a` — Who lives on floor 1 in the East flat?
- `f4e8e032-c4fe-47d0-bbb2-17c461e2db0a` — Who lives on floor 1 in the West flat?
- `332dcfb0-2b4c-48b3-863e-83608915b935` — Who lives on floor 1 in the West flat?
- `1550dcc9-95b3-4b8f-9fba-fa3da3e324aa` — Who lives on floor 1 in the East flat?

### HOT Category Puzzles – Uncertain Seating Arrangement Based

Inserted PDF questions:

- `6ba243b8-8655-4302-877c-0b1b5feef180` — PDF: HOT Category Puzzles Uncertain Seating Arrangement based 01 _ Class Notes.pdf; physical page(s) 8-10 — answer A: 20
- `e21bfbc8-bf6e-42dd-9531-be9631bebe6a` — PDF: HOT Category Puzzles Uncertain Seating Arrangement based 01 _ Class Notes.pdf; physical page(s) 11-13 — answer B: 19
- `e7274b6c-e00c-48a4-9ad2-0c96472b33c7` — PDF: HOT Category Puzzles Uncertain Seating Arrangement based 01 _ Class Notes.pdf; physical page(s) 14-16 — answer A: V
- `c1addf03-a2cb-4bb2-bc3a-b0e5797f907f` — PDF: HOT Category Puzzles Uncertain Seating Arrangement based 02 _ Class Notes.pdf.pdf; physical page(s) 4-6 — answer E: None of these
- `abdd2f3f-079f-4267-840e-59d85f9a0b1b` — PDF: HOT Category Puzzles Uncertain Seating Arrangement based 02 _ Class Notes.pdf.pdf; physical page(s) 7-9 — answer C: 19
- `3d31c576-4f1c-45ef-b082-c4920a1bdcfd` — PDF: HOT Category Puzzles Uncertain Seating Arrangement based 02 _ Class Notes.pdf.pdf; physical page(s) 10-12 — answer A: Sixth to the right
- `1cd011cd-61e0-4021-a85b-440672e7716c` — PDF: HOT Category Puzzles Uncertain Seating Arrangement based 03  Class Notes.pdf; physical page(s) 8-10 — answer A: Only I and III
- `f53010fd-bfbb-4886-95db-e1af489ac474` — PDF: HOT Category Puzzles Uncertain Seating Arrangement based 03  Class Notes.pdf; physical page(s) 11-12 — answer D: 13
- `a60af440-db9c-4ae3-b8aa-d6048a7271eb` — PDF: HOT Category Puzzles Uncertain Seating Arrangement based 04 _ Class Notes.pdf.pdf; physical page(s) 7-8 — answer B: 24
- `77b2ae69-95ae-4f24-921e-436ed1dfe73d` — PDF: HOT Category Puzzles Uncertain Seating Arrangement based 04 _ Class Notes.pdf.pdf; physical page(s) 13-15 — answer A: F
- `b92a1ad9-6dde-460b-b227-d0b9cdd095aa` — PDF: HOT Category Puzzles Uncertain Seating Arrangement based 04 _ Class Notes.pdf.pdf; physical page(s) 16-18 — answer D: 14

Soft-deactivated original questions:

- `fe1f08fb-729e-43f2-b3a1-1d70b3989e5f` — Who occupies seat 11?
- `13903279-a671-4d96-a2d7-9f984ba483b9` — Who occupies seat 11?
- `e48a896f-ddf5-448e-bf00-766824d3949f` — Who occupies seat 11?
- `666cdf2a-6d36-4e0b-a8e3-a9afc435823f` — Who occupies seat 11?
- `07c48e01-c35a-43b3-b2c0-9f5e6879448c` — Who occupies seat 11?
- `5d48db69-6122-466c-8c54-91e618b4ddda` — Who occupies seat 11?
- `b6a322cc-f2d4-4f38-abef-6812ccf437ec` — Who occupies seat 11?
- `a9fa9373-f66b-4e2c-b7e9-57933ee06a34` — Who occupies seat 11?
- `6f8098cf-b038-4be9-837c-7633d1bf4a11` — Who occupies seat 4 from the left?
- `3e18e357-dd8b-4d2c-94aa-135cce2ffe0e` — Who occupies seat 4 from the left?
- `7baf4b99-0671-4b06-80d3-5cc148367cca` — Who occupies seat 4 from the left?

### Inequality (Mains)

Inserted PDF questions:

- `25f0800e-f98c-4347-8934-d73de06b72c5` — PDF: Inequality 01  Class Notes.pdf.pdf; physical page(s) 3 — answer D: Only II follows
- `c68f87b0-56e0-4451-9da8-e25c037ce246` — PDF: Inequality 01  Class Notes.pdf.pdf; physical page(s) 4 — answer D: Only II follows
- `f17f20af-ad63-4957-b60a-27af3223f993` — PDF: Inequality 01  Class Notes.pdf.pdf; physical page(s) 5 — answer E: None is true
- `b8eb8b60-dc0a-49bc-bc2b-21f881cefd54` — PDF: Inequality 02  Class Notes.pdf; physical page(s) 6 — answer A: Only conclusion i follows
- `782540bb-92fb-4660-9702-dca13ca24939` — PDF: Inequality 02  Class Notes.pdf; physical page(s) 9 — answer B: Only conclusion ii follows
- `0f58a87d-7e27-4267-848b-0d00655a497d` — PDF: Inequality 02  Class Notes.pdf; physical page(s) 10 — answer C: Only conclusion iii follows
- `381a6927-7484-4d5c-a333-fbda83ed5383` — PDF: Inequality 02  Class Notes.pdf; physical page(s) 13 — answer A: Only conclusion i follows

Soft-deactivated original questions:

- `d8dd253c-d21c-4e51-b0e4-7d0b8b6dc63a` — Original Practice Question — Given the inequalities: G < A, A >= F, F <= E, E > C, C <= B. Which one of the following conclusions must be true?
- `78b9931c-5615-473e-8702-3d4a992ec0fc` — Original Practice Question — Given the inequalities: B >= A, A < G, G > F, F >= D, D <= E. Which one of the following conclusions must be true?
- `453faa3d-6bcd-46fd-80e8-8a98595eb677` — Original Practice Question — Given the inequalities: E > A, A < G, G <= B, B >= D, D <= C. Which one of the following conclusions must be true?
- `70f659d1-dd67-4cff-8ab9-c8ccc983fad6` — Original Practice Question — Given the inequalities: B < E, E <= A, A <= G, G = F, F <= D. Which one of the following conclusions must be true?
- `fde2dfd7-fd81-4fe0-bd11-5394b1890330` — Original Practice Question — Given the inequalities: D <= G, G > A, A <= E, E > F, F = C. Which one of the following conclusions must be true?
- `d50266dd-4071-4e24-b8f0-056027a63742` — Original Practice Question — Given the inequalities: F >= A, A > E, E = D, D < G, G > C. Which one of the following conclusions must be true?
- `54429781-d9d2-4138-b582-7204b36b34ac` — Original Practice Question — Given the inequalities: E < C, C <= B, B > G, G < D, D >= F. Which one of the following conclusions must be true?
