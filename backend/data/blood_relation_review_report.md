# Blood Relation Normal Bank Review

## Scope and source status

The live chapter is SSC → Reasoning → Blood Relation, ID `cf83a214-1a3c-4af9-89bf-63b25503a2bf`, slug `blood-relation`. The verified pre-import baseline was 0 active Normal, 0 active PYQ, 0 total.

All three supplied scanned lecture PDFs were rendered and visually reviewed: *Blood relation 01_.pdf* (11 pages), *Blood relation 02_.pdf* (16 pages), and *Blood relation 03_.pdf* (19 pages). The first deck is topic/relationship notes without complete question-and-option sets. Fourteen selected items are derived from the latter two decks: six from deck 02 and eight from deck 03. The remaining 16 are original practice questions. No PDF item provides independently verified exam/year attribution; all records are Normal, with `is_pyq=false` and null PYQ fields. Original items are labeled `Original SSC-style practice question`.

## Batch

- 30 questions: 10 Easy, 12 Medium, 8 Hard.
- 14 PDF-derived / clarified, 16 original.
- 0 PYQs.
- Every row has four distinct A–D options, a single keyed answer, and an explanation. The ledger records the answer, independent derivation, source, option set, and unique concept signature.
- Family statements that otherwise leave parentage or sibling status unstated were clarified in selected source-derived stems; those clarifications are identified in the source metadata and explanation.

## Independently checked relations

The review derives each relation from the stated family chain and checks the keyed option against the alternatives. Coded items are evaluated operator by operator from the definitions printed on the source slide. The numeric family-count item was recomputed as 1 mother + 1 unmarried daughter + 3 wives + 4 granddaughters = 9 women. Generational and in-law chains were traced from the named parent/spouse/sibling links; any required full-sibling or co-parent assumption is explicit in the stem. Original items are solved from their text and do not claim PDF or PYQ provenance.

## Exclusions

- The R/C/B/A chain on deck 02 slide 7 does not identify a listed defensible relation for R to G; excluded.
- The D/S chain on deck 02 slide 9 does not establish that the spouses share the relevant child; excluded.
- The Reena/Monika item on deck 02 slide 14 has five options; excluded rather than altering its original choice set.
- The operator expression on deck 03 slide 5 is malformed/unclear; excluded.
- The B-to-W coded chain on deck 03 slide 10 relies on an unstated marriage/parent link; excluded.
- The M*(N+O@P) item on deck 03 slide 15 has five options and gender/parent ambiguity; excluded.
- The M*H@D*K item on deck 03 slide 16 does not determine the requested parent's gender/identity; excluded.
- The repeated Q÷E+R−C×D exercise appears twice in deck 03; included once only.

## Duplicate and import status

No existing Blood Relation batch or ledger was present in the repository. The live chapter had no rows at baseline. Batch stems and ledger concept signatures are checked for uniqueness; the importer refuses any unexpected chapter row, compares all existing row fields before replay, validates the exact chapter ID and 0/0/0 initial baseline, and verifies active status, options, answer key, source, PYQ metadata, and difficulty counts after import.

Run `python -m pytest -q -p no:cacheprovider tests/test_blood_relation_verified_batch.py`, then `python scripts/import_blood_relation_verified_batch.py` from `backend`. Apply only if live baseline remains 0/0/0 and the dry-run reports 30 inserts with zero duplicates, rejected rows, and errors. After importing, rerun the command without `--apply` to confirm 30 duplicates and zero new inserts.
