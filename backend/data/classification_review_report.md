# Classification Question Bank Review

## Scope and provenance

The two supplied scanned slide PDFs were reviewed visually. The batch contains 17 adapted/clarified items from the slides (7 from *Classification 01_.pdf*, slides 5, 6, 7, 8, 10, 12, and 14; 10 from *Classification 02_.pdf*, slides 5, 7, 8, 10, 12, 13, 14, 19, 20, and 21) and 13 original SSC-style practice items. Source slides do not establish exam/year provenance; all records are therefore Normal (`is_pyq=false`) and have no PYQ year or exam metadata. Original items are explicitly labeled as such.

Some source stems were made more explicit to state the classification relation shown by the teaching annotation (deficiency disease, natural disaster, or geographic/professional category). Items with unclear handwritten figure annotations, a five-option layout, or a relation that did not support one defensible answer were not included. A second proposed `n²+n` item was also excluded because that exact operation was already represented by another selected question.

## Review totals

- 30 proposed Normal questions: 10 Easy, 12 Medium, 8 Hard.
- 17 PDF-derived and 13 original.
- 0 PYQs; no exam or year is claimed.
- Four distinct A–D choices and a keyed answer are present for every row.
- The answer ledger records the answer, independent reasoning, options, source, and a distinct problem signature for each row.
- No repeated normalized stems or repeated problem signatures were found within the proposed batch. Canonical batch artifacts were checked for exact stem overlap. Semantic uniqueness against the live database still depends on the importer’s chapter-wide comparison at dry-run time.

## Answer verification notes

Each selected item was solved from the stated category or numeric/letter rule, rather than accepted solely from a slide mark. Arithmetic items were recomputed directly (including cubes, linear pair rules, and successive differences); letter items were checked by alphabet positions, including wraparound for the PDF pair question. Word/category items were checked against the explicit relation in the stem and explanation. The focused tests independently recheck a set of numeric answer checkpoints and the batch/ledger alignment.

## Database and import status

Previously confirmed baseline for active SSC → Reasoning → Classification (`8179a4a3-b760-4a0d-bb35-a71dc5964b0b`) was 0 active Normal and 0 active PYQ. This review report does not itself establish the current baseline. The importer requires that exact chapter ID and either the empty baseline or an exact, verified 30-question replay. Run artifact tests and `python scripts/import_classification_verified_batch.py` from `backend` for a dry-run. Apply only if the dry-run reports exactly 30 planned inserts, zero duplicates, zero rejected rows, and zero errors, and the current baseline remains 0/0. After apply, rerun without `--apply` to verify the 30-row replay plans zero additional inserts.

No database import is authorized by this report alone; use the user's task authorization only after all runtime checks pass.
