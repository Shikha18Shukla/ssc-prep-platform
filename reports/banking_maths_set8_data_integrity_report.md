# Banking Maths Set 8 - Unrelated Data Integrity Report

The live database was compared with a restored pre-import baseline.
The 1,440 deterministic Set 8 question rows and their 5,760 options were
excluded; every remaining row was compared by content hash.

| Table | Rows compared | Live hash | Baseline hash | Result |
| --- | ---: | --- | --- | --- |
| alembic_version | 1 | `53c3bb88cc1ace30...` | `53c3bb88cc1ace30...` | SAME |
| auth_sessions | 7 | `d0cdcf54461098ca...` | `d0cdcf54461098ca...` | SAME |
| chapters | 598 | `6b27ae580b002292...` | `6b27ae580b002292...` | SAME |
| exams | 7 | `604a26722a342444...` | `604a26722a342444...` | SAME |
| oauth_exchange_codes | 4 | `621727eab6edc2cd...` | `621727eab6edc2cd...` | SAME |
| oauth_identities | 2 | `15004b03a5bdcc6c...` | `15004b03a5bdcc6c...` | SAME |
| oauth_states | 14 | `45474ada0b375a57...` | `45474ada0b375a57...` | SAME |
| password_reset_tokens | 0 | `e3b0c44298fc1c14...` | `e3b0c44298fc1c14...` | SAME |
| question_options | 89853 | `17f69c1e30792750...` | `17f69c1e30792750...` | SAME |
| questions | 20932 | `4a7ed9515e68dc61...` | `4a7ed9515e68dc61...` | SAME |
| rate_limit_windows | 13 | `67bb41e2b388542a...` | `67bb41e2b388542a...` | SAME |
| subcategories | 9 | `7ee74922022c3bee...` | `7ee74922022c3bee...` | SAME |
| subjects | 22 | `bb1e727783dfecc7...` | `bb1e727783dfecc7...` | SAME |
| test_attempts | 69 | `149d145a7dbd36c8...` | `149d145a7dbd36c8...` | SAME |
| test_questions | 2797 | `409fb5a859b6c568...` | `409fb5a859b6c568...` | SAME |
| user_answers | 272 | `b7e44d90f5a76aab...` | `b7e44d90f5a76aab...` | SAME |
| user_chapter_rotations | 4 | `30525eacff6c2e2f...` | `30525eacff6c2e2f...` | SAME |
| user_question_history | 92 | `475fd19d4000229d...` | `475fd19d4000229d...` | SAME |
| users | 4 | `442b2dbb0ce3391a...` | `442b2dbb0ce3391a...` | SAME |

- Set 8 rows on the live database: 1440 questions, 5760 options
- Tables compared: 19

## Result

ALL UNRELATED DATA UNCHANGED

Banking Others, attempts, answers, users, progress, history and every
other unrelated table are byte-equivalent to the pre-import baseline.