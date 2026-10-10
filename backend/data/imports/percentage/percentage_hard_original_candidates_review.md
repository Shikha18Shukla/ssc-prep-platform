# Original Hard Percentage candidate review

## Provenance and metadata

These are four original questions authored for the SSC Prep Platform for this review. They are not copied from the supplied PDF or represented as past-year questions. Each row uses the existing Percentage catalog identifiers `maths / arithmetic-maths / percentage`, difficulty `HARD`, `is_pyq=false`, blank `pyq_year`, and blank `pyq_exam_name`. The source field says `Original question authored for SSC Prep Platform`.

The four question texts were compared with every existing import CSV under `backend/data/imports`; none is an exact or normalized-text duplicate. The authenticated importer dry-run provides the authoritative database duplicate check.

## Candidate questions and verification

### 1. Markup and two discounts

**Question:** An article is marked 50% above its cost price. A discount of 20% is given on the marked price, followed by a further discount on the reduced price. If the final selling price is 8% above cost price, what is the further discount?

- A. 8%
- B. 10%
- C. 12%
- D. 15%
- **Correct answer: B — 10%**

**Worked check:** Set cost price to 100. Marked price is 150. After a 20% discount it is 120. An 8% profit requires a final price of 108. The further discount is `(120 − 108) / 120 × 100 = 10%`.

### 2. Loss changed to gain

**Question:** A trader sells an article at a 12% loss. If it had been sold for ₹216 more, the sale would instead have produced a 6% gain. What was the cost price?

- A. ₹1,080
- B. ₹1,200
- C. ₹1,350
- D. ₹1,440
- **Correct answer: B — ₹1,200**

**Worked check:** The change from 12% below cost to 6% above cost is an 18% change in cost price. Therefore `0.18 × CP = ₹216`, giving `CP = ₹216 / 0.18 = ₹1,200`. Check: the 12%-loss price is ₹1,056; ₹216 more is ₹1,272, which is 6% above ₹1,200.

### 3. Payroll and headcount

**Question:** A firm's average monthly pay per employee rises by 25%, while its headcount is reduced. The new total monthly payroll is 10% lower than before. By what percentage was the headcount reduced?

- A. 20%
- B. 25%
- C. 28%
- D. 30%
- **Correct answer: C — 28%**

**Worked check:** Let original headcount and average pay be `H` and `P`. The new total payroll is `0.90HP`, and pay per employee is `1.25P`. New headcount is `0.90HP / 1.25P = 0.72H`; the reduction is `1 − 0.72 = 28%`.

### 4. Weighted failure rates

**Question:** A company has two departments. Department A has 40% of all employees, and 25% of its employees fail a certification test. Overall, 19% of all employees fail. What percentage of employees in Department B fail?

- A. 12%
- B. 15%
- C. 18%
- D. 20%
- **Correct answer: B — 15%**

**Worked check:** Department A contributes `40% × 25% = 10%` of all employees to the failed group. Department B contributes the remaining `19% − 10% = 9%` of all employees. Since B has 60% of employees, its failure rate is `9% / 60% = 15%`.

## Validation status

CSV structure and fields are prepared using the existing question-import template. Rows have four non-empty options, one valid correct-option label, `HARD` difficulty, non-PYQ metadata, and worked explanations. No row has a year or exam name because these are original questions.

The authenticated dry-run succeeded: `dry_run=true`, 4 total records, 4 would import, 0 duplicates, 0 rejected, 0 errors, and `aborted=false`. This confirms the backend importer found the four candidate texts eligible and non-duplicate at dry-run time. Current active counts remain Easy 12, Medium 11, and Hard 6. No questions have been imported and no database rows have been modified.

The separate command `backend/scripts/import_percentage_hard_original_candidates.ps1` is prepared but has not been run. It authenticates as an administrator, checks the expected baseline, repeats the dry-run, requires the exact confirmation phrase `IMPORT 4 ORIGINAL HARD PERCENTAGE QUESTIONS`, repeats the dry-run again, and only then sends the one-file `dry_run=false` request. Afterward it checks the counts and Hard/PYQ availability. If the four original non-PYQs are imported, expected counts are 10 total Hard rows (7 ordinary Hard and 3 PYQs); ordinary Hard availability would be 7, PYQ availability 3, and a 10-question ordinary Hard test would remain unavailable.
