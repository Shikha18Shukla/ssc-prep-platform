# Train question semantic review

Reviewed the 90-row Train batch against the active bank after the targeted revisions. The revisions preserve each affected row's existing database ID, difficulty, provenance, PYQ flag, and active status. The four retained PDF-derived questions were not changed.

## Duplicate checks

- Exact, normalized, number-masked, and lexical checks found no remaining cross-chapter matches at the project's configured lexical threshold (0.92).
- A TF-IDF/cosine screen generated six manual-review leads. Each was checked for the actual requested quantity and the reasoning needed to solve it. No unresolved duplicate remains:
  - Train row 34 (`b1328c4b-80f3-4cc8-82db-2b33df29ebc1`) and external row `241697d7-fc51-401d-a7fd-242eeda8b714` both involve a train and platform, but one finds speed and the other platform length.
  - Train row 38 (`f0894535-0995-4963-b93f-fdda9bef1190`) versus `9fd86b60-8630-48dd-9d2d-6b62f0a999ef`: one finds crossing time from both speeds; the other finds an unknown speed from a crossing time.
  - Train row 44 (`def03d18-9d7f-4861-baf9-7c74cc6d784a`) versus `e7cdd879-e1f5-47cb-b552-948eebc3b663`: same-direction person/train motion asks for train length; opposite-direction motion asks for train speed.
  - Train row 49 (`d31b606b-ebc4-4220-ad8c-a6e362f379f9`) versus `241697d7-fc51-401d-a7fd-242eeda8b714`: inverse platform-crossing equations ask for different unknown lengths; retained as distinct applications.
  - Train row 69 (`4aeb8cb4-20ca-4b35-9d2d-3ad6b9ff95b2`) versus `e7cdd879-e1f5-47cb-b552-948eebc3b663`: direction changes relative speed from a sum to a difference.
  - Train row 73 (`11b09dea-3060-4538-aa4b-d52436fede23`) resembles a platform-crossing item lexically, but derives train length from a train/platform length ratio and a crossing time.
- Rows 71 (`4342c698-3bec-47be-bbb8-beb6498cd29f`) and 90 (`855264c5-c6d5-4c8c-a26f-424ff9f02dd8`) intentionally cover opposite-direction crossing (sum of speeds) and same-direction overtaking (difference of speeds), with different givens and requested values.

## Revisions made

The following row IDs were retained while replacing redundant templates with distinct Train applications. The replacements' answer calculations are independently covered by `test_semantic_review_replacements_match_independent_calculations`.

| Batch row | Question ID | Previous overlap | Current distinct task |
|---:|---|---|---|
| 10 | `46720e58-a473-421c-b43b-600d0a747495` | Basic pole-speed template | Coaches and gaps; derive time to pass a signal |
| 11 | `34d047b1-29d7-4519-838c-797b4fe23263` | Basic pole-time template | Distance between kilometer posts at known speed |
| 14 | `7c9ca61e-faea-48b5-aa4b-0a54d394776a` | Direct bridge crossing | Travel-time saving over a route at two speeds |
| 21 | `956392de-f218-40e5-b03c-1853c0c6e006` | Direct tunnel crossing | Time fully inside a tunnel; infer train length |
| 24 | `394367c1-40e7-4615-a7c3-a3cfac654843` | Platform-length equation matching existing bank content | Distance over two trip segments at different speeds |
| 35 | `e59b17ae-9488-449c-a6ea-a2a08ffd5a86` | Pole/bridge speed equation | Two trains' changing separation; infer unknown speed |
| 36 | `9c232af7-03cc-49ed-8b48-02e5b2364dc3` | Two-bridge equation overlapping another row | Front/rear passage interval through a tunnel |
| 48 | `efc10291-722f-4d47-944b-cef3939b86f4` | Opposite crossing with unknown speed | Compare speeds from separate pole-pass measurements |
| 52 | `1f0945da-e6a4-4de5-88eb-a923f42c1986` | Two bridges; solve speed and length | Piecewise-speed trip with a target average speed |
| 58 | `e80fce08-94ad-41a7-890f-3c9e8a6c6f63` | Pole/platform direct equation | Infer speed and train length from three platform timings |
| 59 | `00eb9f9e-b70a-4959-a5bc-ed9a6e81dc7a` | Opposite trains; find the other speed | Multi-leg journey with unequal distance fractions and speeds |
| 64 | `c49bc5f2-558c-4163-9f37-64cd93970ba0` | Pole/platform find train length | Time from front entering to rear leaving a platform |
| 65 | `5d4dca6a-7c07-4a61-bb2a-4c7860c04c5d` | Opposite train crossing; find unknown speed | Train speed from passing cyclists moving in both directions |
| 68 | `333a7eda-2025-4c1b-9795-8db4da58326b` | Two bridges; find train length | Train length, gaps, and time between pole events |
| 71 | `4342c698-3bec-47be-bbb8-beb6498cd29f` | Train crossing with unknown speed | Opposite crossing from independently measured pole speeds |
| 72 | `bff74f41-76c0-4d97-9a10-cf6bfc65ceee` | Repeated same/opposite speed-ratio template | Equal-distance outward/return trip with a speed percentage relation |
| 73 | `11b09dea-3060-4538-aa4b-d52436fede23` | Pole time inferred from platform timings | Train length from train/platform length ratio and crossing time |
| 76 | `a766e0ac-f663-4ddc-b570-ec42c9b87718` | Pole/platform solve for platform length matching bank content | Scheduled journey time inferred from late/early arrivals |
| 78 | `b142c002-d74e-42e9-bcd8-0319bfecbb68` | Equal-length trains with same/opposite crossing times | Compare equal-distance journeys with a speed and time difference |
| 85 | `1fdc5f7b-f370-4dec-996b-ab2bdef11628` | Stationary observer/platform speed equation | Infer train speed from a person walking and jogging alongside |
| 87 | `d4f5f10e-a4f7-47b7-9e9b-d67f99ecb88b` | Pole/bridge find-length equation matching bank content | Opposing trains with one train changing speed before meeting |
| 88 | `25da1222-afd8-42c0-a6c0-3e1460b482c3` | Same-direction trains; infer slower speed | Infer coach count from total length, coach length, and gaps |
| 90 | `855264c5-c6d5-4c8c-a26f-424ff9f02dd8` | Repeated opposite-direction unknown-speed template | Same-direction overtake using each train's pole-pass speed |

## Verification state

- Active Train ordinary rows: 30 EASY, 30 MEDIUM, 30 HARD; active PYQs: 0.
- All 90 current database rows match their batch text, options, answer, explanation, source, difficulty, and flags; all have four distinct options and one correct option.
- No importer was run for this audit. The existing rows were updated in place for the reviewed replacements; no rows were deleted or re-imported.
- Focused Train tests: 7 passed. Full backend suite: 197 passed, 6 pytest collection warnings.
