# Banking Maths Set 4 - Deduplication Report

## Within the new 720 questions

- Exact duplicate texts: 0
- Normalized duplicate texts: 0

Number-masked families per chapter (fresh values are expected):

| Chapter | Questions | Distinct templates | Largest family | Share |
| --- | ---: | ---: | ---: | ---: |
| average | 120 | 120 | 1 | 0.8% |
| boats_and_streams | 120 | 120 | 1 | 0.8% |
| mensuration_2d | 120 | 120 | 1 | 0.8% |
| pipe_and_cistern | 120 | 120 | 1 | 0.8% |
| problems_on_trains | 120 | 120 | 1 | 0.8% |
| speed_time_distance | 120 | 120 | 1 | 0.8% |

## Against Banking Maths Sets 1-3

- Questions screened: 720
- Pool screened: 1920
- Exact/normalized matches: 0
- Number-masked (template) matches: 0

## Against existing database questions

- Questions screened: 720
- Pool screened: 15172
- Exact/normalized matches: 0
- Number-masked (template) matches: 0

## Lexical near-duplicates (manual review)

Digits are retained. Token and bigram Jaccard are averaged; the combined score
must reach 0.90 with at least 4 bigrams.

- Against Sets 1-3: 0
- Against the database: 0
- Cross-chapter within Set 4: 0

## Semantic near-duplicates (manual review)

A shared domain signature plus a number-masked string similarity of at least
0.78 is listed for human inspection; these are not automatic failures.

- Against Sets 1-3: 0
- Against the database: 1

### Database semantic

- 0.831: speed_time_distance-0057 / 53df4fe2-f9ad-4d6d-9cbd-1ab1d6773521

## Result

- New questions: 720
- Prior-batch questions: 1920
- Database questions: 15172
- Hard problems: 0
- Semantic flags requiring review: 1

## Manual review of semantic flags

- `speed_time_distance-0057` vs DB `53df4fe2-f9ad-4d6d-9cbd-1ab1d6773521`:
  both are routine two-leg total-time questions, but the second leg differs
  (60 km at 30 km/h vs 90 km at 60 km/h), the totals differ (4 hours vs
  3.5 hours), and the wording is not a verbatim copy. Conclusion: generic
  topic overlap only, not a duplicate; retained unchanged. No wording was
  altered to evade a duplicate check.
