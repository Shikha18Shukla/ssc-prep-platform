# Banking Maths Set 8 - Import and Idempotency Report

## Safety gates passed before import

- Running backend PID and importer both resolved to the same local target:
  `postgresql://***:***@127.0.0.1:5432/ssc_prep`. The remote Neon target was
  never used, and `.env` was not modified.
- The importer refused a scratch target:
  `ERROR: refusing to write to database 'ssc_prep_scratch_maths8'; expected ssc_prep`.
- The importer refused a remote-like target:
  `ERROR: refusing to write to non-local host 'remote.example.neon.tech'`.
- Rechecked all 12 target chapters: active, correct names, subject
  `math-quant`, and exactly 0 questions before import.
- Fresh pre-import snapshot: `questions=20932 options=89853 set8=0`.
- Dry run: `preflight OK: 12 target chapters, 1440 planned questions` and
  `dry run: no database changes written`.

## Live transactional import

Command result:

```text
preflight OK: 12 target chapters, 1440 planned questions
imported: 1440 inserted, 0 updated, 1440 total rows
```

Rows inserted per exam/chapter:

| Exam | Chapter | Inserted | Parts 1/2/3/4 |
| --- | --- | ---: | --- |
| banking-clerk | time_and_work_mains | 120 | 15 / 20 / 30 / 55 |
| banking-clerk | time_and_work_data_interpretation | 120 | 15 / 20 / 30 / 55 |
| banking-clerk | time_speed_and_distance_mains | 120 | 15 / 20 / 30 / 55 |
| banking-clerk | simple_and_compound_interest_mains | 120 | 15 / 20 / 30 / 55 |
| banking-clerk | simple_and_compound_interest_data_interpretation | 120 | 15 / 20 / 30 / 55 |
| banking-clerk | pipe_and_cistern_mains | 120 | 15 / 20 / 30 / 55 |
| banking-po | time_and_work_mains | 120 | 15 / 20 / 30 / 55 |
| banking-po | time_and_work_data_interpretation | 120 | 15 / 20 / 30 / 55 |
| banking-po | time_speed_and_distance_mains | 120 | 15 / 20 / 30 / 55 |
| banking-po | simple_and_compound_interest_mains | 120 | 15 / 20 / 30 / 55 |
| banking-po | simple_and_compound_interest_data_interpretation | 120 | 15 / 20 / 30 / 55 |
| banking-po | pipe_and_cistern_mains | 120 | 15 / 20 / 30 / 55 |

The importer used deterministic UUID5 identifiers, four parts per chapter, and
the established section naming. It performed a single transaction with
post-import checks and committed only after all checks passed.

## Idempotency replay

The importer was run a second time against the same local database:

```text
preflight OK: 12 target chapters, 1440 planned questions
imported: 0 inserted, 1440 updated, 1440 total rows
```

ID and count comparison before and after replay:

| Measure | Before replay | After replay |
| --- | ---: | ---: |
| Set 8 question rows | 1,440 | 1,440 |
| Unique deterministic IDs | 1,440 | 1,440 |
| Exact ID list identical | — | Yes |
| Exact chapter/section row list identical | — | Yes |

Replay introduced zero additional rows and changed no deterministic question,
chapter, or section assignment.

## Result

Status: **PASS**. Exactly 1,440 live rows were inserted once; the replay was
idempotent. No generic import endpoint was used, and no existing question was
deleted, replaced, or deactivated.
