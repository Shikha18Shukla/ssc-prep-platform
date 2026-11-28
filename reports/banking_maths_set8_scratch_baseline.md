# Banking Maths Set 8 - Scratch Baseline Verification

## Outcome

Status: **passed**. The live import was not started until this gate passed.

## Restore process

- The first background baseline job (`sh_222b468a5001gZs3U3o8SmTRSW`) stalled in
  `pg_restore` with no database connection or log output. It was stopped; its
  recorded process exit was `4294967295` (forced termination). No live write
  occurred.
- The helper was corrected to use the local `pgpass.conf` entry as a
  process-only password source and `stdin=DEVNULL` for `pg_dump`/`pg_restore`.
  No credential was written to a file, report, or repository.
- The rerun completed with exit code `0` and logged:
  `baseline dump captured; baseline and scratch scratch databases restored`.

## Baseline verification

All three databases were compared by full per-table row counts and content
hashes (every base table in `public`):

| Database | Masked target | Questions | Options | Set 8 rows | Tables |
| --- | --- | ---: | ---: | ---: | ---: |
| live | `postgresql://***:***@127.0.0.1:5432/ssc_prep` | 20,932 | 89,853 | 0 | 19 |
| scratch | `postgresql://***:***@127.0.0.1:5432/ssc_prep_scratch_maths8` | 20,932 | 89,853 | 0 | 19 |
| baseline | `postgresql://***:***@127.0.0.1:5432/ssc_prep_scratch_maths8_baseline` | 20,932 | 89,853 | 0 | 19 |

- `baseline_scratch_table_diffs`: empty
- `live_baseline_table_diffs`: empty
- `BASELINE_MATCH`: `True`
- `LIVE_UNTOUCHED_BY_SCRATCH`: `True`

The scratch baseline therefore matched the expected pre-import live state, and
scratch preparation/validation did not modify the live database.
