# Five-Chapter PDF Question Integration — Validated Proposal

Local database: `ssc_prep` at `127.0.0.1:5432` (identity verified). This document records the pre-write review. No rows have been changed at proposal time.

| Chapter | Before active/inactive | Inserts | Proposed retirements | Proposed active after | Dry-run |
|---|---:|---:|---:|---:|---|
| Scheduling Puzzles – Month Based | 40/0 | 6 | 6 | 40 | 6 eligible, 0 duplicates/rejected/errors |

## Scheduling Puzzles – Month Based

Target chapter ID: `792acd2d-d6b4-459d-850e-c71657696718`. Selection rationale: Retire one of the repeated direct month lookups from six full-order practice sets, retaining four questions in each affected set and all questions in two sets.

### Proposed PDF inserts

| Source | Physical page(s) | Question | Correct option | Answer |
|---|---:|---|---|---|
| Scheduling Puzzles Month Based 02  Class Notes.pdf; physical page(s) 4-6 | 4-6 | Which bike brand was registered in August? | D | Bajaj |
| Scheduling Puzzles Month Based 02  Class Notes.pdf; physical page(s) 10-12 | 10-12 | If X goes to the movie immediately after E, in which month does X go? | E | September |
| Scheduling Puzzles Month Based 02  Class Notes.pdf; physical page(s) 13-14 | 13-14 | Which country invented the vaccine in October? | B | Israel |
| Scheduling Puzzles Month Based 04  Class Notes.pdf; physical page(s) 19-21 | 19-21 | Which month does G go to the hospital? | B | September |
| Scheduling Puzzles Month Based 04  Class Notes.pdf; physical page(s) 23-25 | 23-25 | In which month does J buy a cycle? | B | September |
| Scheduling Puzzles Month Based 05 Class Notes.pdf; physical page(s) 8-11 | 8-11 | Who among the following does not belong to the group? | D | U-Delhi |

### Proposed original questions to soft-deactivate

| Existing question ID | Original prompt |
|---|---|
| `249f4365-573d-4159-8b3b-36d724ca5d97` | In which month is A scheduled? |
| `613436c9-0c8a-4541-bfa1-fce90b9e12a0` | In which month is B scheduled? |
| `cb2ea773-5f0b-483a-9118-3fc4a63b568a` | In which month is E scheduled? |
| `36845130-dac1-4a2a-a6b7-2cf675d19b7b` | In which month is E scheduled? |
| `c9908082-b147-408f-901d-ae7499996867` | In which month is F scheduled? |
| `27dad3e0-72a4-4391-bc8a-0fb0a9d0fa6e` | In which month is A scheduled? |

No question is hard-deleted. The five initial active counts are 40 each. If applied as planned, each chapter ends at 40 active, with inactive count equal to its soft-retirement count.

| Scheduling Puzzles – Year Based | 40/0 | 9 | 9 | 40 | 9 eligible, 0 duplicates/rejected/errors |

## Scheduling Puzzles – Year Based

Target chapter ID: `73959b25-9732-4d8f-adfd-1894ef4d088b`. Selection rationale: Retire repeated direct birth-year lookups (one per full-order set); one additional lookup comes from the simplest first set. All affected sets retain at least three original questions.

### Proposed PDF inserts

| Source | Physical page(s) | Question | Correct option | Answer |
|---|---:|---|---|---|
| Scheduling Puzzles Year Based Puzzles 01 Class Notes.pdf; physical page(s) 4-6 | 4-6 | C was born in which year? | D | 1985 |
| Scheduling Puzzles Year Based Puzzles 01 Class Notes.pdf; physical page(s) 7-9 | 7-9 | Who was born in 1995? | A | The person born immediately before P |
| Scheduling Puzzles Year Based Puzzles 01 Class Notes.pdf; physical page(s) 10-12 | 10-12 | H was born in which year? | B | 1990 |
| Scheduling Puzzles Year Based Puzzles 02 Class Notes-.pdf; physical page(s) 5-7 | 5-7 | Who was born in 1978? | D | I |
| Scheduling Puzzles Year Based Puzzles 02 Class Notes-.pdf; physical page(s) 8-10 | 8-10 | What is the age of G? | C | Eight years younger than F |
| Scheduling Puzzles Year Based Puzzles 03 _ Class Notes.pdf; physical page(s) 4-6 | 4-6 | Who is the youngest person? | C | B |
| Scheduling Puzzles Year Based Puzzles 03 _ Class Notes.pdf; physical page(s) 7-9 | 7-9 | What is the age difference between R and Q? | C | 12 |
| Scheduling Puzzles Year Based Puzzles 03 _ Class Notes.pdf; physical page(s) 10-13 | 10-13 | How many people were born between P and the person born in 1971? | E | Both C & D |
| Scheduling Puzzles Year Based Puzzles 04 _ Class Notes.pdf; physical page(s) 8-11 | 8-11 | Which person is working in IBM? | B | The one who is three years younger than V |

### Proposed original questions to soft-deactivate

| Existing question ID | Original prompt |
|---|---|
| `bff3a14b-d71a-4fac-9372-ead69ded72ae` | In which year was A born? |
| `d3873c2c-561c-4382-acfe-ba7d4a3c6201` | In which year was D born? |
| `e04ee40c-fc0c-4fcc-a995-fd16d1aa2ab8` | In which year was B born? |
| `9b3dca10-ea45-4b71-9270-a36a1b511a79` | In which year was A born? |
| `fc7fb563-5124-4588-ac9c-921eb666ed2b` | In which year was C born? |
| `175c61b0-4391-4f11-97b5-b40861d40919` | In which year was F born? |
| `ef159da3-485b-444d-bc7c-ccf8ef8498d5` | In which year was A born? |
| `dddc281a-f519-4563-9bf6-47dc9ceb0cec` | In which year was A born? |
| `153f3b32-5809-4c8f-bc7c-908a8f0eb066` | In which year was C born? |

No question is hard-deleted. The five initial active counts are 40 each. If applied as planned, each chapter ends at 40 active, with inactive count equal to its soft-retirement count.

| HOT Category Puzzles – Flat + Floor Based | 40/0 | 4 | 4 | 40 | 4 eligible, 0 duplicates/rejected/errors |

## HOT Category Puzzles – Flat + Floor Based

Target chapter ID: `59c468db-e3f8-44ff-be9c-0830a5a7ebce`. Selection rationale: Retire four repeated, direct floor-location lookups across four distinct fixed-arrangement sets; retain four questions in each affected set and all questions in the other four sets.

### Proposed PDF inserts

| Source | Physical page(s) | Question | Correct option | Answer |
|---|---:|---|---|---|
| HOT Category Puzzles Flat   Floor puzzles based 01 _ Class Notes.pdf.pdf; physical page(s) 5-7 | 5-7 | Who among the following persons stays on the topmost floor? | C | T |
| HOT Category Puzzles Flat   Floor puzzles based 02 _ Class Notes.pdf; physical page(s) 4-6; printed Q1 | 4-6 | Who among the following people lives on floor number first? | B | B |
| HOT Category Puzzles Flat   Floor puzzles based 02 _ Class Notes.pdf; physical page(s) 7-9; printed Q6 | 7-9 | Who lives in Flat Q on the top floor? | C | F |
| HOT Category Puzzles Flat   Floor puzzles based 02 _ Class Notes.pdf; physical page(s) 10-13; printed Q11 | 10-13 | Who among the following people lives on floor number first? | D | U, R, Z |

### Proposed original questions to soft-deactivate

| Existing question ID | Original prompt |
|---|---|
| `25eb852a-5cde-425a-bfdf-f856d7fd0e0a` | Who lives on floor 1 in the East flat? |
| `f4e8e032-c4fe-47d0-bbb2-17c461e2db0a` | Who lives on floor 1 in the West flat? |
| `332dcfb0-2b4c-48b3-863e-83608915b935` | Who lives on floor 1 in the West flat? |
| `1550dcc9-95b3-4b8f-9fba-fa3da3e324aa` | Who lives on floor 1 in the East flat? |

No question is hard-deleted. The five initial active counts are 40 each. If applied as planned, each chapter ends at 40 active, with inactive count equal to its soft-retirement count.

| HOT Category Puzzles – Uncertain Seating Arrangement Based | 40/0 | 11 | 11 | 40 | 11 eligible, 0 duplicates/rejected/errors |

## HOT Category Puzzles – Uncertain Seating Arrangement Based

Target chapter ID: `5f13ba4b-5f8d-414d-9d52-652051d463e8`. Selection rationale: Retire all eight repeated seat-11 questions whose answer is always an unnamed participant, plus three repeated seat-4 lookups from separated sets; retain at least three originals in every set.

### Proposed PDF inserts

| Source | Physical page(s) | Question | Correct option | Answer |
|---|---:|---|---|---|
| HOT Category Puzzles Uncertain Seating Arrangement based 01 _ Class Notes.pdf; physical page(s) 8-10 | 8-10 | How many persons are sitting in the row? | A | 20 |
| HOT Category Puzzles Uncertain Seating Arrangement based 01 _ Class Notes.pdf; physical page(s) 11-13 | 11-13 | How many persons are sitting in the row? | B | 19 |
| HOT Category Puzzles Uncertain Seating Arrangement based 01 _ Class Notes.pdf; physical page(s) 14-16 | 14-16 | Who is sitting second to the left of U? | A | V |
| HOT Category Puzzles Uncertain Seating Arrangement based 02 _ Class Notes.pdf.pdf; physical page(s) 4-6 | 4-6 | How many persons are sitting in the row? | E | None of these |
| HOT Category Puzzles Uncertain Seating Arrangement based 02 _ Class Notes.pdf.pdf; physical page(s) 7-9 | 7-9 | How many persons sit in the row? | C | 19 |
| HOT Category Puzzles Uncertain Seating Arrangement based 02 _ Class Notes.pdf.pdf; physical page(s) 10-12 | 10-12 | What is the position of Y with respect to W? | A | Sixth to the right |
| HOT Category Puzzles Uncertain Seating Arrangement based 03  Class Notes.pdf; physical page(s) 8-10 | 8-10 | Which of the following statements is true? I. G sits to the left of R. II. More than seven persons sit between M and S. III. Not more than two persons sit between S and Q. IV. R sits exactly midway between M and S. | A | Only I and III |
| HOT Category Puzzles Uncertain Seating Arrangement based 03  Class Notes.pdf; physical page(s) 11-12 | 11-12 | How many persons are sitting in the row? | D | 13 |
| HOT Category Puzzles Uncertain Seating Arrangement based 04 _ Class Notes.pdf.pdf; physical page(s) 7-8 | 7-8 | How many persons are sitting in the row? | B | 24 |
| HOT Category Puzzles Uncertain Seating Arrangement based 04 _ Class Notes.pdf.pdf; physical page(s) 13-15 | 13-15 | Who is sitting second to the right of G? | A | F |
| HOT Category Puzzles Uncertain Seating Arrangement based 04 _ Class Notes.pdf.pdf; physical page(s) 16-18 | 16-18 | How many persons are sitting in the row? | D | 14 |

### Proposed original questions to soft-deactivate

| Existing question ID | Original prompt |
|---|---|
| `fe1f08fb-729e-43f2-b3a1-1d70b3989e5f` | Who occupies seat 11? |
| `13903279-a671-4d96-a2d7-9f984ba483b9` | Who occupies seat 11? |
| `e48a896f-ddf5-448e-bf00-766824d3949f` | Who occupies seat 11? |
| `666cdf2a-6d36-4e0b-a8e3-a9afc435823f` | Who occupies seat 11? |
| `07c48e01-c35a-43b3-b2c0-9f5e6879448c` | Who occupies seat 11? |
| `5d48db69-6122-466c-8c54-91e618b4ddda` | Who occupies seat 11? |
| `b6a322cc-f2d4-4f38-abef-6812ccf437ec` | Who occupies seat 11? |
| `a9fa9373-f66b-4e2c-b7e9-57933ee06a34` | Who occupies seat 11? |
| `6f8098cf-b038-4be9-837c-7633d1bf4a11` | Who occupies seat 4 from the left? |
| `3e18e357-dd8b-4d2c-94aa-135cce2ffe0e` | Who occupies seat 4 from the left? |
| `7baf4b99-0671-4b06-80d3-5cc148367cca` | Who occupies seat 4 from the left? |

No question is hard-deleted. The five initial active counts are 40 each. If applied as planned, each chapter ends at 40 active, with inactive count equal to its soft-retirement count.

| Inequality (Mains) | 40/0 | 7 | 7 | 40 | 7 eligible, 0 duplicates/rejected/errors |

## Inequality (Mains)

Target chapter ID: `5615c02a-f5ce-4f67-b256-78b68de1486f`. Selection rationale: Retire seven low-discrimination items whose correct option directly repeats a premise relation; retain the remaining varied transitive/equality questions.

### Proposed PDF inserts

| Source | Physical page(s) | Question | Correct option | Answer |
|---|---:|---|---|---|
| Inequality 01  Class Notes.pdf.pdf; physical page(s) 3 | 3 | Which of the listed conclusions logically follow? | D | Only II follows |
| Inequality 01  Class Notes.pdf.pdf; physical page(s) 4 | 4 | Which of the listed conclusions logically follow? | D | Only II follows |
| Inequality 01  Class Notes.pdf.pdf; physical page(s) 5 | 5 | Which of the listed conclusions logically follow? | E | None is true |
| Inequality 02  Class Notes.pdf; physical page(s) 6 | 6 | Which of the listed conclusions logically follow? | A | Only conclusion i follows |
| Inequality 02  Class Notes.pdf; physical page(s) 9 | 9 | Which of the listed conclusions logically follow? | B | Only conclusion ii follows |
| Inequality 02  Class Notes.pdf; physical page(s) 10 | 10 | Which of the listed conclusions logically follow? | C | Only conclusion iii follows |
| Inequality 02  Class Notes.pdf; physical page(s) 13 | 13 | Which of the listed conclusions logically follow? | A | Only conclusion i follows |

### Proposed original questions to soft-deactivate

| Existing question ID | Original prompt |
|---|---|
| `d8dd253c-d21c-4e51-b0e4-7d0b8b6dc63a` | Original Practice Question — Given the inequalities: G < A, A >= F, F <= E, E > C, C <= B. Which one of the following conclusions must be true? |
| `78b9931c-5615-473e-8702-3d4a992ec0fc` | Original Practice Question — Given the inequalities: B >= A, A < G, G > F, F >= D, D <= E. Which one of the following conclusions must be true? |
| `453faa3d-6bcd-46fd-80e8-8a98595eb677` | Original Practice Question — Given the inequalities: E > A, A < G, G <= B, B >= D, D <= C. Which one of the following conclusions must be true? |
| `70f659d1-dd67-4cff-8ab9-c8ccc983fad6` | Original Practice Question — Given the inequalities: B < E, E <= A, A <= G, G = F, F <= D. Which one of the following conclusions must be true? |
| `fde2dfd7-fd81-4fe0-bd11-5394b1890330` | Original Practice Question — Given the inequalities: D <= G, G > A, A <= E, E > F, F = C. Which one of the following conclusions must be true? |
| `d50266dd-4071-4e24-b8f0-056027a63742` | Original Practice Question — Given the inequalities: F >= A, A > E, E = D, D < G, G > C. Which one of the following conclusions must be true? |
| `54429781-d9d2-4138-b582-7204b36b34ac` | Original Practice Question — Given the inequalities: E < C, C <= B, B > G, G < D, D >= F. Which one of the following conclusions must be true? |

No question is hard-deleted. The five initial active counts are 40 each. If applied as planned, each chapter ends at 40 active, with inactive count equal to its soft-retirement count.
