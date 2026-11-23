# Input Output (Mains) source audit and top-up

Source: `INPUT OUTPUT MAINS SETS by Arpit sir (1).pdf` (30 physical pages; 41 numbered MCQ appearances). The existing regular Banking Clerk Input Output chapter already contains exact normalized copies of the 20 previously imported questions from this same set. Those are excluded from this Mains chapter to avoid cross-chapter duplication.

Target: Banking Clerk → Reasoning → Input Output (Mains), chapter `2ab41ac9-09e8-4c4e-b8df-e293c6de48a8`. Initial count: 0 active / 0 inactive.

- Source appearances: 41.
- Exact cross-chapter duplicates: 20.
- Previously held: Q5, Q7, Q21, Q22 (source ambiguity from the prior audit).
- Newly held: Q28 (digit position scope ambiguous across separate numbers and printed answer D conflicts with the natural concatenated reading).
- Verified new unique candidates: 16 (Q12, Q24, Q27, Q29–Q41 except Q28).
- Printed-key disagreements: Q29 (independent E, key D; deduplicated Step VI totals 150 and third-from-right Step IV is 895, sum 1045); Q35 (independent E because B and C are both true; key B).
- Q27, Q30–Q34, Q36–Q41 agree with printed key. Q12 and Q24 have no printed key.

Independent computations are recorded in the answer ledger and import JSON. No source prompt/options were fabricated. Existing records are unchanged.

Import verification: all 16 candidates passed the existing importer dry-run, were inserted transactionally, and replayed as 16 duplicates with zero new insertions. Direct local database verification found 16 active / 0 inactive records in this Mains chapter; all have five options, one correct option, explanation, and source metadata. The target remains 24 short of 40.
