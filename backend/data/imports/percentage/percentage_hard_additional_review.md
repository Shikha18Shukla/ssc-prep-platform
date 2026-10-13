# Percentage Hard additional question review

## Result

The seven-page Hard source contains **three distinct question texts beyond the three Hard questions already imported**. All three have a determinate answer and four readable answer choices. They are all visibly marked PYQ, so they cannot be imported as ordinary non-PYQs.

The source marks pages 1 and 7 as the same question (2023); only one copy is represented in the candidate CSV. Page 1/7's election question is not textually duplicated by the existing Percentage database records. The two other candidates are from pages 4 (2023) and 6 (2019); neither matches the existing 26 question texts. Page 2, 3 and 5 are the three already-imported Hard questions and are excluded from the new CSV.

The configured database was queried read-only. Chapter `percentage` is the existing Percentage chapter, and it currently has 12 active Easy, 11 active Medium, and 3 active Hard questions. No database rows were changed.

## Candidate review

| Candidate | Source | Difficulty / PYQ year | Independently verified answer | Duplicate check |
| --- | --- | --- | --- | --- |
| Election turnout and valid votes | pp. 1 and 7 (identical source pages) | Hard / 2023 | A — 15,000 voters | One copy in source; no matching existing DB wording |
| Savings after income/expenditure increases | p. 4 | Hard / 2023 | B — 14% increase | No matching existing DB wording |
| Two students' combined marks | p. 6 | Hard / 2019 | C — 40 marks | No matching existing DB wording |

For page 1/7: valid votes equal 81% of the voter list; the 12% winner-loser margin equals 1,458, giving 12,150 valid votes and 15,000 enrolled voters. For page 4: savings rise from ₹4,000 to ₹4,560, a 14% increase. For page 6: A's 60% share exceeds B's 40% share by 20%; a difference of 8 therefore means 40 combined marks.

The CSV preserves the source wording/options and records the source pages. It marks each row `is_pyq=true` with the visible year. `pyq_exam_name` is intentionally empty because no specific examination name is shown in the source. The importer now allows this absent exam name and stores it as `NULL`, while still requiring the known year. No exam name has been inferred or fabricated.

## Import validation status

An authenticated API dry-run and import have not been performed. No authenticated administrator credential was available to this validation-change session. No production database writes were made. Use `backend/scripts/dry_run_percentage_hard_additional.ps1` to review only this three-row file; it cannot commit/import. The existing `import_percentage_batch.ps1` was not run because it would also process the already-imported Easy and Medium CSVs.

## Next requirement

From the repository root, run `backend/scripts/dry_run_percentage_hard_additional.ps1 -Email "admin@example.com"`. Review its authenticated report and proceed with a separate, explicitly approved commit only if it reports 3 records ready, 0 errors, and 0 duplicates. Do not run `import_percentage_batch.ps1`; that existing script also processes Easy and Medium.

Expected active Hard count after a clean import: 6. The platform's 10-question minimum would still require four more verified Hard questions.
