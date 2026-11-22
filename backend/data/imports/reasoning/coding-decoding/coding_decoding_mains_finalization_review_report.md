# Banking Clerk Mains Reasoning finalization — coding-decoding

## Source audit carried forward

The prior source-PDF audit and question ledger are preserved and embedded in `coding_decoding_mains_finalization_answer_ledger.json`. The audit covers 19 + 8 physical PDF pages. Existing source-ledger status counts: {'verified_import_candidate': 3, 'held': 8, 'duplicate': 1}. The chapter's pre-finalization active count was 3 and target is 40 active. Existing active source-derived questions remain unchanged. The prior audit found no additional source question that was both safe to reproduce and suitable to close this full remaining gap; held questions remain held.

## Online reference and reuse decision

Access date: 2026-11-23 (Asia/Kolkata). These pages were consulted only to check the exam format/topic mix; none of their question text or answer content is reproduced in this batch. All new items below are original practice questions authored for this platform, not PYQs.

- [NDLI Tutor — IBPS Clerk (Mains): Reasoning Ability Question Paper 20_T2_01](https://www.ndl.iitkgp.ac.in/cd_document/ndli_tutor_ibps_clerk/ndli_career_ibpsc/IBPS_C_20_T2_01_Q_GI) — NDLI item page says the hosted resource is a 50-question English MCQ set and marks access Open. This is an open-access repository listing, but the page does not state a reuse license; no questions were copied.
- [Adda247 — IBPS Clerk Mains paper held 13.10.2024](https://www.adda247.com/jobs/wp-content/uploads/sites/22/2025/06/19181917/IBPS-Clerk-Mains-Question-Paper-Held-on-13.10.2024.pdf) — third-party memory-based document; not represented here as an official IBPS release; no question text copied.
- [Previous Year Questions — IBPS Clerk topic-wise practice](https://previousyearquestions.app/ibps-clerk/topics/) — the publisher identifies these as its labelled mock questions, not actual past papers; used only as a mock-pattern taxonomy reference, not copied.

## New verified original practice

- Added to the candidate file: 37 original questions, all `is_pyq: false`; no publication-year or exam attribution is claimed.
- Coverage: position-dependent shifts with reversal and set-coded-language decoding using unordered code lists.
- Every item has five distinct options, one keyed answer, a worked explanation, HARD difficulty, and unique question/concept identifiers.
- Verification: deterministic rules/relationship graph, exhaustive ordering enumeration, explicit machine transformation computations, or exhaustive three-set Venn-region model checking as appropriate. Answer keys in the artifact are derived from those checks, not copied from the references.
- Duplicate review: stems and concept signatures are unique within this batch; a local database-wide normalized/near-text scan and importer dry-run are required before any write.

## Import and final verification

Guarded local dry-run and transactional import passed; final database counts and idempotent replay were verified. Authenticated question payload verification remains unavailable because this process has no signed-in bearer session. No production source is used. The exact target chapter is `0bac0e64-d8a0-485b-a263-4b1da7a33d81` (`coding-decoding-mains`).

## Guarded local import and database verification

- Database target was asserted at runtime as `127.0.0.1:5432/ssc_prep`; no hosted database was used.
- Initial dry-run: all records eligible; 0 duplicates, 0 rejects, 0 errors.
- Transaction: imported 37 records for this chapter; 0 duplicates, 0 rejects, 0 errors.
- Replay dry-run: 37 duplicates, 0 would-import, 0 rejects, 0 errors.
- Final count: 40 active, 0 inactive. The pre-existing active rows and any pre-existing inactive row were unchanged.
- Each new row was matched to its import source and checked for correct chapter assignment, five option keys A-E, one correct option, matching explanation/source, active status, and `is_pyq=false`. Database question IDs are recorded per ledger row.
- Text duplicate screening across all five destination chapters found 0 exact overlaps and 0 high-similarity review matches.

## API verification

The local backend was started on 127.0.0.1:8000 using a process-only URL for local `ssc_prep`. `/api/health` returned 200 (`healthy`) and `/api/ready` returned 200 (`ready`). Authenticated `GET /api/exams` and `GET /api/questions?chapter_id=<target>&limit=1` both returned 401 `Not authenticated`. No valid signed-in user/admin bearer session was available to this process, so the chapter payload was not verified through an authenticated API. No credentials or tokens were fabricated.
