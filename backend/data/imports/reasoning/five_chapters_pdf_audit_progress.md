# Five Reasoning PDF Audit — Final Consolidated Status

**Audit and integration complete:** all 16 supplied PDFs (241 physical pages) were visually reviewed; every identified appearance is classified. The 37 verified unique PDF questions are integrated across the five local chapters, with 37 original practice records soft-deactivated to keep each chapter at 40 active. OCR extracts and rendered pages remain under `tmp/pdfs/five-reasoning-finalization/`.

| Chapter | PDFs | Pages reviewed | Question appearances | Distinct prompts | Verified unique | Held | Repeated appearances | Complete with options | Wrong chapter |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Scheduling Puzzles — Month Based | 4 | 66/66 | 12 | 8 | 6 | 2 | 4 | 12 | 0 |
| Scheduling Puzzles — Year Based | 4 | 52/52 | 10 | 10 | 9 | 1 | 0 | 10 | 0 |
| HOT Category Puzzles — Flat + Floor Based | 2 | 31/31 | 6 | 6 | 4 | 2 | 0 | 6 | 0 |
| HOT Category Puzzles — Uncertain Seating Arrangement Based | 4 | 68/68 | 14 | 13 | 11 | 2 | 1 | 14 | 0 |
| Inequality (Mains) | 2 | 24/24 | 13 | 13 | 7 | 6 | 0 | 13 | 0 |
| **Total** | **16** | **241/241** | **55** | **50** | **37** | **13** | **5** | **55** | **0** |

“Repeated appearances” includes repeat prompts, bilingual repeats, and the duplicate Uncertain Seating appearance. For Month Based, nine worked-example groups (including three repeated worked examples across Lectures 03 and 04) are documented separately and are not counted as MCQs. Each question appearance has five source options recorded; held questions are not treated as answer-verified.

## Answer-key findings

- **Month Based:** one independently derived answer disagrees with a visible source mark (Lecture 02, p.13); the written constraints yield option B. One separate question is held because the shared clue conflicts across pp.7–8.
- **Year Based:** no answer-key disagreement among verified answers. Lecture 04’s held question omits the operation joining two box counts.
- **Flat + Floor Based:** no answer-key disagreements among verified answers. Two questions are held because the answer is not invariant across valid layouts / displayed cases.
- **Uncertain Seating:** Lecture 01 p.5–6 has conflicting clues; Lecture 04 p.10–11 contradicts the ten named people with a seven-seat row. The Lecture 04 printed mark is not accepted as resolution. No verified answer conflicts with a reliable printed key.
- **Inequality:** Lecture 01 p.4’s visible mark near E conflicts with the independent result D (only II). Six other questions remain held for missing variables, absent answer combinations, or source ambiguity; see the ledger for each reason.

## Deduplication scope and database safety

Within-source question duplicates and repeated appearances were checked for every chapter. Verified candidates were compared read-only against all active and inactive records in each exact destination chapter; no destination-bank duplicates were found. The seven Inequality candidates were additionally compared against all 6,119 question rows in local `ssc_prep` at `127.0.0.1:5432`; no exact or semantic relation-graph duplicate was identified. No production connection or database write was used. A broad semantic scan of candidates across unrelated chapter banks was not performed.

## Held questions

- **Month Based (2 unique):** Lecture 02 p.7–9, conflicting G/H versus C/H clue creates ambiguity; Lecture 05 p.4–7, the correct identity appears as separate options and a combined option, so multiple choices are true. The repeated appearances at Lecture 05 pp.5 and 8 are retained in the ledger and share the canonical item’s status.
- **Year Based (1):** Lecture 04 pp.4–7, the written clue does not say whether box counts are added, multiplied, or otherwise combined.
- **Flat + Floor Based (2):** Lecture 01 pp.8–10, two valid layouts produce different outcomes; pp.11–14, displayed cases do not establish a unique odd-one-out criterion.
- **Uncertain Seating (2):** Lecture 01 pp.5–6, incompatible D–G / D–C clue; Lecture 04 pp.10–11, ten named participants cannot fit the stated seven-seat row.
- **Inequality (6):** Lecture 01 pp.6–7, correct combination absent from choices; Lecture 02 p.4, all three conclusions are true but no matching choice; p.5, conclusion uses undefined G; pp.7–8, correct either/or combination is absent from transcribed choices; p.11, all three conclusions follow but no matching choice; p.12, source transcription is insufficiently reliable.

## Chapter artifacts

- Month Based: `backend/data/imports/reasoning/scheduling-month-based/pdf_audit_answer_ledger.json`, `pdf_audit_report.md`
- Year Based: `backend/data/imports/reasoning/scheduling-year-based/pdf_audit_answer_ledger.json`, `pdf_audit_report.md`
- Flat + Floor Based: `backend/data/imports/reasoning/flat-floor-based/pdf_audit_answer_ledger.json`, `pdf_audit_report.md`
- Uncertain Seating: `backend/data/imports/reasoning/uncertain-seating-arrangement-based/pdf_audit_answer_ledger.json`, `pdf_audit_report.md`
- Inequality: `backend/data/imports/reasoning/inequality-mains/inequality_pdf_audit_answer_ledger.json`, `inequality_pdf_audit_report.md`
- Page-level checkpoint: `tmp/pdfs/five-reasoning-finalization/pdf_audit_progress_checkpoint.json`

## Integration completion

All 37 verified unique PDF-derived questions were imported into the five existing chapters. Thirty-seven original self-authored questions were soft-deactivated to keep each chapter at exactly 40 active questions. All five imports replayed idempotently. No held question was imported.

| Chapter | Imported | Retired | Active after | Inactive after |
|---|---:|---:|---:|---:|
| Month Based | 6 | 6 | 40 | 6 |
| Year Based | 9 | 9 | 40 | 9 |
| Flat + Floor Based | 4 | 4 | 40 | 4 |
| Uncertain Seating | 11 | 11 | 40 | 11 |
| Inequality (Mains) | 7 | 7 | 40 | 7 |

Full integration report and record-level before/after ledger: `five_chapters_pdf_integration_report.md` and `five_chapters_pdf_integration_record_ledger.json`.


## Integration completed

See `five_chapters_pdf_integration_report.md` and `five_chapters_pdf_integration_record_ledger.json` for exact imported/retired IDs and before/after records.
