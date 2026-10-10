# Percentage PDF import review

## Scope and result

I inspected all 78 screenshot pages at original image resolution: 45 Easy, 26 Medium, and 7 Hard. I transcribed the question and choices, calculated answers independently, and compared the results with the supplied options. No OCR was used; these image-only pages were readable by manual inspection.

The catalog identifiers in the files follow the existing hierarchy: `maths` → `arithmetic-maths` → `percentage`. The importer checks this subject/category/chapter relationship against the active SSC catalog before allowing any import.

| Source set | Pages detected | Unique pages after within-set duplicates | Verified answer (includes any cross-set repeat) | Ready CSV rows | Manual review |
| --- | ---: | ---: | ---: | ---: | ---: |
| Easy | 45 | 40 | 37 | 12 | 28 |
| Medium | 26 | 24 | 23 | 11 | 13 |
| Hard | 7 | 6 | 6 | 3 | 2 |
| **Total, before cross-level deduplication** | **78** | **70** | **66** | **26** | **43** |

There are **9 repeated source pages**: Easy pp. 40–44 repeat earlier Easy pages; Medium pp. 24–25 repeat earlier Medium pages; Hard p. 7 repeats Hard p. 1; and Hard p. 1 repeats Easy p. 5. After also removing the Hard copy of the Easy/Hard duplicate, there are **69 globally unique questions**. The table’s Hard verified count includes the Hard p. 1 copy; the CSVs retain the Easy version and omit the Hard copy.

Of the 69 globally unique questions, **26 are ready for dry-run import** (12 Easy, 11 Medium, 3 Hard). Another **39 have verified answers but are visibly tagged PYQ** and are held because no specific exam name appears in the screenshots. **Four need content or wording review** (Easy pp. 6, 8, 23 and Medium p. 11). That leaves 65 unique questions with an unambiguous calculated answer and four unresolved content cases. In total, 43 unique records await manual action (39 PYQ metadata items and four content/wording items).

## Import-ready source pages

- Easy CSV rows 2–13 map in order to Easy PDF pages: **2, 4, 14, 19, 24, 26, 28, 31, 32, 36, 39, 45**.
- Medium CSV rows 2–12 map in order to Medium PDF pages: **4, 5, 8, 10, 12, 13, 15, 17, 19, 20, 21**.
- Hard CSV rows 2–4 map in order to Hard PDF pages: **2, 3, 5**.

Each `source` cell names its source PDF and page. Each imported `explanation` is a short, independently calculated explanation; the screenshots did not supply explanations.

## Questions held for manual review

### PYQ exam name not shown

The importer requires `pyq_exam_name` as well as `pyq_year` for every PYQ. The screenshots display a year only (for example, “PYQ 2023”), not an exam name, so I did not guess “SSC”, CGL, CHSL, or another exam label. These pages have verified answers except where separately noted:

- Easy: **1, 3, 5, 7, 9–13, 15–18, 20–22, 25, 27, 29–30, 33–35, 37–38**.
- Medium: **1–3, 6–7, 9, 14, 16, 18, 22–23, 26**.
- Hard: **4, 6**.

To import these later, supply the specific exam name from an authoritative source and add it to `pyq_exam_name`. The visible years are preserved in this report; they are not placed into the CSVs because the records are not yet importable as valid PYQs under the existing schema.

### Conflicting, incomplete, or ambiguous source content

- Easy p. 6: the losing candidate is stated as having 48% of total votes, implying a 4% margin in a two-candidate election, but the same question says the margin is 3%. It also asks for invalid votes without giving enough information to determine them. **No answer imported.**
- Easy p. 8: two of the four choices are blank, and none of the visible choices matches the calculated 93.75% decrease. **No answer imported.**
- Easy p. 23: the calculated salary increase is 71 3/7%, but none of the four displayed choices matches it. **No answer imported.**
- Medium p. 11: “one spoiled fruit for every 25 fruits” can mean 25 total fruits or 25 unspoiled fruits. The listed option B (2,000) follows the first interpretation, but the wording does not disambiguate it. **Held out of the CSV pending source confirmation.**

## Duplicate pages excluded

- Easy p. 40 duplicates Easy p. 1; p. 41 duplicates p. 2; p. 42 duplicates p. 3; p. 43 duplicates p. 4; p. 44 repeats the conflicting Easy p. 6 item.
- Medium p. 24 duplicates Medium p. 1; p. 25 duplicates p. 3.
- Hard p. 1 duplicates Easy p. 5; Hard p. 7 repeats Hard p. 1. The Easy version is retained because it is the easier source set.

## Dry-run validation

Only the three CSV files in this directory contain import candidates. They contain non-PYQ records only, all use the existing `EASY`, `MEDIUM`, or `HARD` values, and each row has four non-empty choices and a single A–D correct-option label. The candidate files have not been committed to PostgreSQL. Run the authenticated importer with `dry_run=true` for each file, inspect its returned `would_import`, `duplicates`, and `errors`, and request approval before any committed import.

From the repository root, after starting the backend and obtaining a valid JWT:

```powershell
$headers = @{ Authorization = "Bearer $token" }
Get-ChildItem backend/data/imports/percentage/percentage_*.csv | ForEach-Object {
  Invoke-RestMethod -Method Post `
    -Uri "http://127.0.0.1:8000/api/questions/import?dry_run=true" `
    -Headers $headers `
    -Form @{ file = Get-Item $_.FullName }
}
```

The source PDFs remain outside the repository; no original PDF was changed or copied into the import directory.
