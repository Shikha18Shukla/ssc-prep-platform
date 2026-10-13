# Hard Percentage PDF source audit

## Outcome

The source PDF has seven scanned pages and contains **six distinct question texts**. Pages 1 and 7 show the same election-vote question. The other five question texts appear once each. All six distinct questions are already represented in the existing Hard import files and, according to the current active database counts, have already been imported. Therefore the PDF contains **zero additional distinct questions** suitable for a new import. The shortfall toward four more questions is four.

`percentage_hard_source_audit.csv` combines the six existing Hard source rows solely to test duplicate detection against the database. It is an audit file, not a new-question candidate file. No new-candidate CSV is provided because there are no verified additional candidates. Do not import the audit file.

## Question-by-question source and answer check

| PDF page(s) | Question summary | Options in source order | Correct answer | Independent check | Existing file |
| --- | --- | --- | --- | --- | --- |
| 1 and 7 | Election: 10% do not vote; 10% of cast votes are invalid; winner gets 56% of valid votes and wins by 1,458 | 15,000; 13,000; 16,000; 14,000 | A — 15,000 | Valid votes are `0.90 × 0.90 = 0.81` of the roll. The margin is 12% of valid votes, so valid votes are `1,458 / 0.12 = 12,150`; total voters are `12,150 / 0.81 = 15,000`. Pages 1 and 7 are the same question; retain one copy. | `percentage_hard_additional.csv` |
| 2 | Father gives 8% of income to two sons; elder receives 85% and saves 10% of that amount, equal to Rs 17 | Rs. 5,000; Rs. 4,500; Rs.3,500; Rs. 2,500 | D — Rs. 2,500 | Elder receives `17 / 0.10 = 170`; total pocket money is `170 / 0.85 = 200`; income is `200 / 0.08 = 2,500`. | `percentage_hard.csv` |
| 3 | Sequential spending: 25% of income on daily goods, 18% of remainder on rent, 16% of remainder on travel; Rs 861 remains | Rs 1852 1/3; Rs 1666 2/3; Rs 1563 1/3; Rs 1426 1/3 | B — Rs 1666 2/3 | Remaining fraction is `0.75 × 0.82 × 0.84 = 0.5166`; `861 / 0.5166 = 1666 2/3`. | `percentage_hard.csv` |
| 4 | Income rises from Rs 12,000 by 10%; expenditure rises from Rs 8,000 by 8%; find savings increase | 10%; 14%; 12%; 15% | B — 14% | Initial savings are Rs 4,000. New savings are `13,200 − 8,640 = 4,560`; increase is `560 / 4,000 = 14%`. | `percentage_hard_additional.csv` |
| 5 | Successive changes: +40%, −25%, +15%, −20% | 7.2% decrease; 6.4% increase; 3.4% increase; 3.4% decrease | D — 3.4% decrease | Multiplier is `1.40 × 0.75 × 1.15 × 0.80 = 0.966`, a 3.4% decrease. | `percentage_hard.csv` |
| 6 | A has 8 more marks than B; A's marks equal 60% of their sum; find the sum | 45; 50; 40; 75 | C — 40 | The difference is `(60% − 40%) = 20%` of the sum; `8 / 0.20 = 40`. | `percentage_hard_additional.csv` |

The question text and all four option values are preserved in the audit CSV from the existing reviewed import files. The answers above were recalculated independently from the displayed source values. The three PYQ questions retain the source years already recorded in the imported additional file; the PDF does not provide specific exam names, so none are inferred.

## Database and dry-run status

The reported current active counts are Easy 12, Medium 11, and Hard 6. The coverage CSV includes only the six distinct source questions above, so a clean authenticated dry-run against that state should report 6 duplicates, 0 questions to import, 0 rejected, and 0 errors. The dedicated script `backend/scripts/dry_run_percentage_hard_source_audit.ps1` performs only `dry_run=true`, verifies those counts and the existing availability behavior, and contains no commit request. Run it from the repository root and enter administrator credentials only at its secure prompt.

Current selection behavior keeps ordinary Hard (`is_pyq=false`) and PYQ practice separate. The six total Hard rows are split between three ordinary Hard questions and three PYQs; availability is therefore expected to show 3 for Hard and 3 for PYQ, with a 10-question ordinary Hard test unavailable.

No database rows are modified by this audit or its dry-run.
