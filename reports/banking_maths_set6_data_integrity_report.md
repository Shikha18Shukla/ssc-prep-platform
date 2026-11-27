# Banking Maths Set 6 - Unrelated Data Integrity Report

The live database was compared with a restored pre-import baseline.
The 1,440 deterministic Set 6 question rows and their 5,760 options were
excluded; every remaining row was compared by content hash.

| Table | Rows compared | Live hash | Baseline hash | Result |
| --- | ---: | --- | --- | --- |
| alembic_version | 1 | `2984cd90ea0a285e...` | `2984cd90ea0a285e...` | SAME |
| beta_capacity | 1 | `6061141cb52c7907...` | `6061141cb52c7907...` | SAME |
| beta_invitations | 0 | `e3b0c44298fc1c14...` | `e3b0c44298fc1c14...` | SAME |
| chapters | 598 | `6b27ae580b002292...` | `6b27ae580b002292...` | SAME |
| exams | 7 | `604a26722a342444...` | `604a26722a342444...` | SAME |
| question_options | 78333 | `ed4efa299d782419...` | `ed4efa299d782419...` | SAME |
| questions | 18052 | `60b012e24a2e278f...` | `60b012e24a2e278f...` | SAME |
| rate_limit_windows | 9 | `5a54fc8a42897701...` | `5a54fc8a42897701...` | SAME |
| subcategories | 9 | `7ee74922022c3bee...` | `7ee74922022c3bee...` | SAME |
| subjects | 22 | `bb1e727783dfecc7...` | `bb1e727783dfecc7...` | SAME |
| test_attempts | 61 | `4167772d770a8c64...` | `4167772d770a8c64...` | SAME |
| test_questions | 2667 | `6a4f0383607ea57d...` | `6a4f0383607ea57d...` | SAME |
| user_answers | 272 | `b7e44d90f5a76aab...` | `b7e44d90f5a76aab...` | SAME |
| user_chapter_rotations | 4 | `30525eacff6c2e2f...` | `30525eacff6c2e2f...` | SAME |
| user_question_history | 92 | `475fd19d4000229d...` | `475fd19d4000229d...` | SAME |
| users | 3 | `9b067c26a3da157a...` | `9b067c26a3da157a...` | SAME |

- Set 6 rows on the live database: 1440 questions, 5760 options
- Tables compared: 16

## Result

ALL UNRELATED DATA UNCHANGED

Banking Others, attempts, answers, users, progress, history and every
other unrelated table are byte-equivalent to the pre-import baseline.