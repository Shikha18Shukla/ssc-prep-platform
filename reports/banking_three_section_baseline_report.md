# Banking Three-Section Baseline Report

## Scope and method

Read-only baseline captured before any allocation write. Scope: Banking Clerk and Banking PO chapters under English, General/Banking Awareness, and Computer. No other exam, subject or catalogue record is included.

Usable questions are active rows with distinct normalized question text. A deterministic allocation plan selects the first 40 usable rows by creation time then question id, split 10 / 15 / 15. Duplicate normalized texts are skipped. Surplus usable rows are left unassigned and preserved.

Content diagnostics use three measures: exact/normalized duplicate groups, number-masked template groups, and lexical pairs with similarity at least 0.90. Similarity flags are diagnostic, not automatic removals.

## Grouped totals

| Exam | Subject | Chapters | Total rows | Active rows | Active unique | Allocated | Surplus | Shortage chapters |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| banking-clerk | computer | 12 | 527 | 526 | 526 | 480 | 46 | 0 |
| banking-clerk | english | 28 | 1120 | 1120 | 1120 | 1120 | 0 | 0 |
| banking-clerk | general-banking-awareness | 9 | 384 | 360 | 360 | 360 | 0 | 0 |
| banking-po | computer | 12 | 527 | 526 | 526 | 480 | 46 | 0 |
| banking-po | english | 28 | 1120 | 1120 | 1120 | 1120 | 0 | 0 |
| banking-po | general-banking-awareness | 9 | 482 | 360 | 360 | 360 | 0 | 0 |

Overall: **98 chapters inspected**, **3920 questions planned for allocation**, **92 surplus usable questions**, **0 shortage chapters**.

## Per-chapter baseline

| Exam | Subject | Chapter | Total | Active | Dup IDs | Active unique | Dup groups (all/active) | Masked groups | Near pairs | Usable | Plan | Surplus | Shortage | Sections before |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| banking-clerk | computer | basics-of-computer-fundamentals | 40 | 40 | 0 | 40 | 0/0 | 0 | 6 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | computer | computer-abbreviations | 63 | 63 | 0 | 63 | 0/0 | 0 | 45 | 63 | 10/15/15 | 23 | 0 | <NULL>=63 |
| banking-clerk | computer | computer-communication-and-internet | 45 | 45 | 0 | 45 | 0/0 | 1 | 29 | 45 | 10/15/15 | 5 | 0 | <NULL>=45 |
| banking-clerk | computer | computer-hardware | 40 | 40 | 0 | 40 | 0/0 | 0 | 2 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | computer | computer-software | 40 | 40 | 0 | 40 | 0/0 | 0 | 1 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | computer | history-and-generations-of-computers | 41 | 40 | 0 | 40 | 1/0 | 0 | 4 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | computer | malware-and-cyber-security | 44 | 44 | 0 | 44 | 0/0 | 0 | 2 | 44 | 10/15/15 | 4 | 0 | <NULL>=44 |
| banking-clerk | computer | microsoft-office | 45 | 45 | 0 | 45 | 0/0 | 0 | 94 | 45 | 10/15/15 | 5 | 0 | <NULL>=45 |
| banking-clerk | computer | number-system | 40 | 40 | 0 | 40 | 0/0 | 7 | 20 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | computer | programming-languages | 45 | 45 | 0 | 45 | 0/0 | 0 | 9 | 45 | 10/15/15 | 5 | 0 | <NULL>=45 |
| banking-clerk | computer | shortcut-keys | 44 | 44 | 0 | 44 | 0/0 | 1 | 31 | 44 | 10/15/15 | 4 | 0 | <NULL>=44 |
| banking-clerk | computer | windows-operating-system | 40 | 40 | 0 | 40 | 0/0 | 0 | 2 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | adjective | 40 | 40 | 0 | 40 | 0/0 | 0 | 8 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | adverb | 40 | 40 | 0 | 40 | 0/0 | 0 | 9 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | articles | 40 | 40 | 0 | 40 | 0/0 | 0 | 0 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | cloze-test | 40 | 40 | 0 | 40 | 0/0 | 8 | 16 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | column-based-exercises | 40 | 40 | 0 | 40 | 0/0 | 0 | 1 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | conditional-sentences | 40 | 40 | 0 | 40 | 0/0 | 0 | 1 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | conjunction | 40 | 40 | 0 | 40 | 0/0 | 0 | 1 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | connectors | 40 | 40 | 0 | 40 | 0/0 | 0 | 2 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | descriptive-english | 40 | 40 | 0 | 40 | 0/0 | 0 | 1 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | error-detection | 40 | 40 | 0 | 40 | 0/0 | 0 | 2 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | fillers | 40 | 40 | 0 | 40 | 0/0 | 0 | 0 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | match-the-column | 40 | 40 | 0 | 40 | 0/0 | 1 | 8 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | miscellaneous-questions | 40 | 40 | 0 | 40 | 0/0 | 0 | 1 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | noun | 40 | 40 | 0 | 40 | 0/0 | 0 | 13 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | para-jumble | 40 | 40 | 0 | 40 | 0/0 | 1 | 550 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | phrasal-verbs | 40 | 40 | 0 | 40 | 0/0 | 0 | 57 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | preposition | 40 | 40 | 0 | 40 | 0/0 | 0 | 1 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | pronoun | 40 | 40 | 0 | 40 | 0/0 | 0 | 5 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | reading-comprehension | 40 | 40 | 0 | 40 | 0/0 | 0 | 21 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | sentence-improvement | 40 | 40 | 0 | 40 | 0/0 | 0 | 4 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | sentence-rearrangement | 40 | 40 | 0 | 40 | 0/0 | 0 | 0 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | starters | 40 | 40 | 0 | 40 | 0/0 | 0 | 2 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | tenses | 40 | 40 | 0 | 40 | 0/0 | 0 | 0 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | verb | 40 | 40 | 0 | 40 | 0/0 | 0 | 5 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | vocabulary-based-questions | 40 | 40 | 0 | 40 | 0/0 | 0 | 2 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | word-improvement | 40 | 40 | 0 | 40 | 0/0 | 0 | 12 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | word-swap | 40 | 40 | 0 | 40 | 0/0 | 0 | 0 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | english | word-usage | 40 | 40 | 0 | 40 | 0/0 | 0 | 22 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | general-banking-awareness | banking-terminologies | 40 | 40 | 0 | 40 | 0/0 | 0 | 2 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | general-banking-awareness | basel-norms-and-banking-risks | 40 | 40 | 0 | 40 | 0/0 | 0 | 7 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | general-banking-awareness | basics-of-banking | 63 | 40 | 0 | 40 | 10/0 | 0 | 1 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | general-banking-awareness | financial-markets | 40 | 40 | 0 | 40 | 0/0 | 0 | 3 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | general-banking-awareness | inflation-and-monetary-policy | 40 | 40 | 0 | 40 | 0/0 | 0 | 1 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | general-banking-awareness | non-performing-assets-npa | 40 | 40 | 0 | 40 | 0/0 | 0 | 3 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | general-banking-awareness | rbi | 41 | 40 | 0 | 40 | 1/0 | 0 | 0 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | general-banking-awareness | types-of-accounts | 40 | 40 | 0 | 40 | 0/0 | 0 | 0 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-clerk | general-banking-awareness | types-of-banks | 40 | 40 | 0 | 40 | 0/0 | 0 | 2 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | computer | basics-of-computer-fundamentals | 40 | 40 | 0 | 40 | 0/0 | 0 | 6 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | computer | computer-abbreviations | 63 | 63 | 0 | 63 | 0/0 | 0 | 45 | 63 | 10/15/15 | 23 | 0 | <NULL>=63 |
| banking-po | computer | computer-communication-and-internet | 45 | 45 | 0 | 45 | 0/0 | 1 | 29 | 45 | 10/15/15 | 5 | 0 | <NULL>=45 |
| banking-po | computer | computer-hardware | 40 | 40 | 0 | 40 | 0/0 | 0 | 2 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | computer | computer-software | 40 | 40 | 0 | 40 | 0/0 | 0 | 1 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | computer | history-and-generations-of-computers | 41 | 40 | 0 | 40 | 1/0 | 0 | 4 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | computer | malware-and-cyber-security | 44 | 44 | 0 | 44 | 0/0 | 0 | 2 | 44 | 10/15/15 | 4 | 0 | <NULL>=44 |
| banking-po | computer | microsoft-office | 45 | 45 | 0 | 45 | 0/0 | 0 | 94 | 45 | 10/15/15 | 5 | 0 | <NULL>=45 |
| banking-po | computer | number-system | 40 | 40 | 0 | 40 | 0/0 | 7 | 20 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | computer | programming-languages | 45 | 45 | 0 | 45 | 0/0 | 0 | 9 | 45 | 10/15/15 | 5 | 0 | <NULL>=45 |
| banking-po | computer | shortcut-keys | 44 | 44 | 0 | 44 | 0/0 | 1 | 31 | 44 | 10/15/15 | 4 | 0 | <NULL>=44 |
| banking-po | computer | windows-operating-system | 40 | 40 | 0 | 40 | 0/0 | 0 | 2 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | adjective | 40 | 40 | 0 | 40 | 0/0 | 0 | 8 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | adverb | 40 | 40 | 0 | 40 | 0/0 | 0 | 9 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | articles | 40 | 40 | 0 | 40 | 0/0 | 0 | 0 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | cloze-test | 40 | 40 | 0 | 40 | 0/0 | 8 | 16 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | column-based-exercises | 40 | 40 | 0 | 40 | 0/0 | 0 | 1 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | conditional-sentences | 40 | 40 | 0 | 40 | 0/0 | 0 | 1 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | conjunction | 40 | 40 | 0 | 40 | 0/0 | 0 | 1 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | connectors | 40 | 40 | 0 | 40 | 0/0 | 0 | 2 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | descriptive-english | 40 | 40 | 0 | 40 | 0/0 | 0 | 1 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | error-detection | 40 | 40 | 0 | 40 | 0/0 | 0 | 2 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | fillers | 40 | 40 | 0 | 40 | 0/0 | 0 | 0 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | match-the-column | 40 | 40 | 0 | 40 | 0/0 | 1 | 8 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | miscellaneous-questions | 40 | 40 | 0 | 40 | 0/0 | 0 | 1 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | noun | 40 | 40 | 0 | 40 | 0/0 | 0 | 13 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | para-jumble | 40 | 40 | 0 | 40 | 0/0 | 1 | 550 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | phrasal-verbs | 40 | 40 | 0 | 40 | 0/0 | 0 | 57 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | preposition | 40 | 40 | 0 | 40 | 0/0 | 0 | 1 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | pronoun | 40 | 40 | 0 | 40 | 0/0 | 0 | 5 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | reading-comprehension | 40 | 40 | 0 | 40 | 0/0 | 0 | 21 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | sentence-improvement | 40 | 40 | 0 | 40 | 0/0 | 0 | 4 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | sentence-rearrangement | 40 | 40 | 0 | 40 | 0/0 | 0 | 0 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | starters | 40 | 40 | 0 | 40 | 0/0 | 0 | 2 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | tenses | 40 | 40 | 0 | 40 | 0/0 | 0 | 0 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | verb | 40 | 40 | 0 | 40 | 0/0 | 0 | 5 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | vocabulary-based-questions | 40 | 40 | 0 | 40 | 0/0 | 0 | 2 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | word-improvement | 40 | 40 | 0 | 40 | 0/0 | 0 | 12 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | word-swap | 40 | 40 | 0 | 40 | 0/0 | 0 | 0 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | english | word-usage | 40 | 40 | 0 | 40 | 0/0 | 0 | 22 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | general-banking-awareness | banking-terminologies | 58 | 40 | 0 | 40 | 18/0 | 0 | 2 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | general-banking-awareness | basel-norms-and-banking-risks | 59 | 40 | 0 | 40 | 19/0 | 0 | 7 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | general-banking-awareness | basics-of-banking | 40 | 40 | 0 | 40 | 0/0 | 0 | 1 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | general-banking-awareness | financial-markets | 57 | 40 | 0 | 40 | 15/0 | 0 | 3 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | general-banking-awareness | inflation-and-monetary-policy | 59 | 40 | 0 | 40 | 16/0 | 0 | 1 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | general-banking-awareness | non-performing-assets-npa | 58 | 40 | 0 | 40 | 15/0 | 0 | 3 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | general-banking-awareness | rbi | 67 | 40 | 0 | 40 | 14/0 | 0 | 0 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | general-banking-awareness | types-of-accounts | 40 | 40 | 0 | 40 | 0/0 | 0 | 0 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |
| banking-po | general-banking-awareness | types-of-banks | 44 | 40 | 0 | 40 | 4/0 | 0 | 2 | 40 | 10/15/15 | 0 | 0 | <NULL>=40 |

## Surplus chapters

| Exam | Subject | Chapter | Usable | Allocated | Surplus preserved |
| --- | --- | --- | ---: | ---: | ---: |
| banking-clerk | computer | computer-abbreviations | 63 | 40 | 23 |
| banking-clerk | computer | computer-communication-and-internet | 45 | 40 | 5 |
| banking-clerk | computer | malware-and-cyber-security | 44 | 40 | 4 |
| banking-clerk | computer | microsoft-office | 45 | 40 | 5 |
| banking-clerk | computer | programming-languages | 45 | 40 | 5 |
| banking-clerk | computer | shortcut-keys | 44 | 40 | 4 |
| banking-po | computer | computer-abbreviations | 63 | 40 | 23 |
| banking-po | computer | computer-communication-and-internet | 45 | 40 | 5 |
| banking-po | computer | malware-and-cyber-security | 44 | 40 | 4 |
| banking-po | computer | microsoft-office | 45 | 40 | 5 |
| banking-po | computer | programming-languages | 45 | 40 | 5 |
| banking-po | computer | shortcut-keys | 44 | 40 | 4 |

## Shortage chapters

None. Every inspected chapter has at least 40 usable unique questions.

## Machine-readable plan

`reports/banking_three_section_baseline.csv` records the deterministic section-1/2/3 question ids for every chapter.
