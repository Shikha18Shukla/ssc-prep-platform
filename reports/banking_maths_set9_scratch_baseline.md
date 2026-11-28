# Banking Maths Set 9 - Scratch Baseline and Safety

## Local-only target

All work used the verified local PostgreSQL target
`postgresql://***:***@127.0.0.1:5432/ssc_prep` (credentials masked). The running
backend and every importer/check process received the same local target through
process-only environment overrides. No remote/Neon/production database was
contacted, and `.env` was not modified.

The importer's preflight refused scratch/remote-looking targets before the live
run and confirmed 14 target chapters and 1,680 planned rows.

## Scratch databases

Two local scratch databases were used:

- `ssc_prep_scratch_maths9` - functional checks after the import.
- `ssc_prep_scratch_maths9_baseline` - immutable pre-import comparison copy.

`backend/../set9_scratch_db.py baseline` captured a full `pg_dump` to
`C:\Users\shikh\AppData\Local\Temp\opencode\ssc_prep_set9_baseline.dump` and
restored both scratch databases from it. Exit code: 0.

After the live import and replay, `set9_scratch_db.py post` restored the scratch
database from a post-import dump. All availability, `create_test`, and DI
rendering checks were then run only on that scratch copy. The live database was
not written by any functional check.

## Baseline comparison

`backend/check_banking_maths_set9_data_integrity.py` compared the live database
with the restored pre-import baseline after excluding the 1,680 deterministic
Set 9 rows and their 6,720 options. All 19 unrelated tables matched by content
hash; see `reports/banking_maths_set9_data_integrity_report.md`.

The before/after snapshots and reconciliation are in:

- `reports/banking_maths_set9_db_before.json`
- `reports/banking_maths_set9_db_after.json`
- `reports/banking_maths_set9_db_reconciliation.md`

## Result

Scratch baseline and restore operations completed successfully. No unrelated
data was changed, and no check wrote to the live database.
