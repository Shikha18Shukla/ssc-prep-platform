# Banking Maths Batch 2 - Deduplication Report

## Within the new 600 questions

- Exact duplicate texts: 0
- Normalized duplicate texts: 0

Number-masked families per chapter (deliberate templates with fresh values):

| Chapter | Questions | Template families | Largest family | Share |
| --- | ---: | ---: | ---: | ---: |
| quadratic_equations | 120 | 18 | 18 | 15.0% |
| number_system | 120 | 17 | 15 | 12.5% |
| percentage | 120 | 25 | 16 | 13.3% |
| ratio_proportion | 120 | 15 | 15 | 12.5% |
| profit_loss_discount | 120 | 11 | 16 | 13.3% |

## Against the first 600-question batch

- Exact/normalized collisions: 0
- Number-masked (same template) collisions: 0

## Against existing database questions

- Active + inactive question rows scanned: 12532
- Exact/normalized matches: 0
- Number-masked (same template) matches: 0

## Lexical near-duplicates

Digits are kept and token + bigram Jaccard must both be high (combined >= 0.9,
at least 4 bigrams), so shared stems with different values do not count.

- Against the first batch: 0
- Against the database: 0
- Cross-chapter: 0

## Interpretation

Number-masked repeats inside a chapter are deliberate template families: each
family tests one technique with fresh values, and every chapter mixes at least
six independent techniques. No exact, normalized, number-masked, cross-chapter
or previous-batch duplicate was found, and no question reproduces an existing
database question.
