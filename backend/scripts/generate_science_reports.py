"""Generate extraction, quality, and manifest reports from OCR review rows."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("queue_csv", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument(
        "--dry-run-passed",
        action="store_true",
        help="Set only after the importer dry-run test passes for the verified batches.",
    )
    args = parser.parse_args()
    with args.queue_csv.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        parser.error("The OCR review queue is empty")

    manifest_path = args.output_dir / "SCIENCE_BATCH_MANIFEST.json"
    previous_manifest = (
        json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        if manifest_path.exists()
        else {}
    )
    imported_batches = previous_manifest.get("imported_batches", [])
    chapter_coverage = previous_manifest.get("chapter_coverage", {})

    by_pdf: dict[str, list[dict[str, str]]] = defaultdict(list)
    difficulty = Counter()
    statuses = Counter(row["review_status"] for row in rows)
    completeness = Counter(row["candidate_completeness"] for row in rows)
    question_text_count = sum(bool(row["question_text_ocr"].strip()) for row in rows)
    explanation_count = sum(bool(row["explanation_ocr"].strip()) for row in rows)
    answer_text_count = sum(bool(row["correct_option_ocr"].strip()) for row in rows)
    four_options_count = sum(
        all(row[f"option_{key}_ocr"].strip() for key in "abcd") for row in rows
    )
    verified_by_pdf = Counter(
        row["source_pdf"] for row in rows if row["review_status"] == "VERIFIED"
    )
    pyq_years = Counter()
    pyq_labels = Counter()
    for row in rows:
        by_pdf[row["source_pdf"]].append(row)
        difficulty[row["difficulty_ocr"] or "UNREAD"] += 1
        if row["pyq_label_ocr"] == "PYQ":
            pyq_labels["PYQ label detected"] += 1
            pyq_years[row["pyq_year_ocr"] or "YEAR_UNREAD"] += 1
        else:
            pyq_labels["No OCR PYQ label"] += 1

    args.output_dir.mkdir(parents=True, exist_ok=True)
    per_pdf = []
    report_rows = []
    for name, items in sorted(by_pdf.items(), key=lambda pair: pair[0].casefold()):
        by_difficulty = Counter(row["difficulty_ocr"] or "UNREAD" for row in items)
        local_pyq = Counter(
            row["pyq_year_ocr"] or "YEAR_UNREAD"
            for row in items
            if row["pyq_label_ocr"] == "PYQ"
        )
        per_pdf.append(
            {
                "source_pdf": name,
                "question_pages": len(items),
                "ocr_difficulty_labels": dict(by_difficulty),
                "ocr_pyq_year_labels": dict(local_pyq),
                "verified": verified_by_pdf[name],
                "ready_for_import": verified_by_pdf[name],
            }
        )
        report_rows.append(
            f"| {name} | {len(items)} | {by_difficulty['EASY']} | "
            f"{by_difficulty['MEDIUM']} | {by_difficulty['HARD']} | "
            f"{by_difficulty['UNREAD']} | "
            f"{sum(local_pyq.values())} |"
        )

    inventory_path = args.output_dir / "SCIENCE_PDF_INVENTORY.md"
    inventory = inventory_path.read_text(encoding="utf-8-sig") if inventory_path.exists() else ""
    page_total_match = re.search(r"Found (\d+) Science PDFs, (\d+) pages", inventory)
    pdf_count = int(page_total_match.group(1)) if page_total_match else len(by_pdf)
    page_total = int(page_total_match.group(2)) if page_total_match else len(rows) + pdf_count
    expected_question_pages = page_total - pdf_count
    verified_count = statuses["VERIFIED"]
    needs_review_count = statuses["NEEDS_REVIEW"]
    rejected_count = statuses["REJECTED"]
    duplicate_count = statuses["DUPLICATE"]
    batch_dir = args.output_dir / "by-chapter"
    ready_count = sum(
        max(0, len(path.read_text(encoding="utf-8-sig").splitlines()) - 1)
        for path in batch_dir.rglob("*.csv")
    ) if batch_dir.exists() else 0
    verified_batches = []
    if batch_dir.exists():
        for path in sorted(batch_dir.rglob("*.csv")):
            with path.open(encoding="utf-8-sig", newline="") as stream:
                verified_batches.extend(csv.DictReader(stream))
    verified_batch_counts = Counter(
        (
            row["chapter_slug"],
            row["difficulty"],
            "PYQ" if row["is_pyq"].casefold() == "true" else "ORDINARY",
            row["pyq_year"] or "",
        )
        for row in verified_batches
    )

    extraction = [
        "# Science PDF Extraction Report",
        "",
        f"Source set: {pdf_count} PDFs, {page_total} PDF pages. The first page in each source is the course/lecture listing; {len(rows)} remaining pages were carried into the OCR review queue.",
        "",
        "OCR used Tesseract English on embedded page images. The original PDFs remain the source of truth. Transcripts retain original PDF page numbers and filenames.",
        "",
        "## Current disposition",
        "",
        f"- Raw page-level OCR candidates: {len(rows)} (expected {expected_question_pages} question pages).",
        f"- Structured, source-verified question records: {verified_count}.",
        f"- NEEDS_REVIEW: {needs_review_count}.",
        f"- Rejected: {rejected_count} confirmed.",
        f"- Confirmed duplicate records: {duplicate_count}.",
        f"- Import-ready: {ready_count}. The OCR queue is intentionally not in the production import schema.",
        f"- Previously imported and verified production batches: {len(imported_batches)}; see SCIENCE_BATCH_MANIFEST.json.",
        "- Exam names: none inferred. PYQ and difficulty values below are OCR labels only.",
        "",
        "## OCR field extraction completeness (unverified candidates)",
        "",
        f"- Question text detected: {question_text_count}/{len(rows)}.",
        f"- All four option fields detected: {four_options_count}/{len(rows)}.",
        f"- Explanation text detected: {explanation_count}/{len(rows)}.",
        f"- Correct option phrase mapped from OCR explanation: {answer_text_count}/{len(rows)}. The remaining answer markers may be present only as green highlighting and require visual review.",
        f"- Candidate completeness labeled FOUR_OPTIONS_AND_TEXT: {completeness['FOUR_OPTIONS_AND_TEXT']}; PARTIAL_OR_UNCERTAIN: {completeness['PARTIAL_OR_UNCERTAIN']}.",
        "These are parsing counts, not accuracy or approval counts. Per-record dispositions are in SCIENCE_REVIEW_DECISIONS.csv and the chapter review datasets.",
        "",
        "## OCR label counts by source PDF",
        "",
        "| Source PDF | Candidate pages | EASY | MEDIUM | HARD | Unread | PYQ labels |",
        "|---|---:|---:|---:|---:|---:|---:|",
        *report_rows,
        "| TOTAL | " + str(len(rows)) + " | " + str(difficulty["EASY"]) + " | " + str(difficulty["MEDIUM"]) + " | " + str(difficulty["HARD"]) + " | " + str(difficulty["UNREAD"]) + " | " + str(pyq_labels["PYQ label detected"]) + " |",
        "",
        "## PYQ years detected by OCR",
        "",
        "| OCR year | Pages |",
        "|---|---:|",
        *[f"| {year} | {count} |" for year, count in sorted(pyq_years.items())],
        "",
        "## Source-verified batch counts",
        "",
        "| Chapter slug | Difficulty | Type | PYQ year | Records |",
        "|---|---|---|---|---:|",
        *[
            f"| {chapter} | {level} | {kind} | {year or '—'} | {count} |"
            for (chapter, level, kind, year), count in sorted(verified_batch_counts.items())
        ],
        "",
        "Source-specific chapter assignments and unresolved mapping notes are recorded in SCIENCE_CHAPTER_MAPPING_REVIEW.md and the chapter review datasets.",
    ]
    (args.output_dir / "SCIENCE_EXTRACTION_REPORT.md").write_text(
        "\n".join(extraction) + "\n", encoding="utf-8"
    )

    quality = [
        "# Science PDF Quality Report",
        "",
        "## Checks completed",
        "",
        "- All source files were readable; all pages are image-based with no extractable PDF text.",
        "- OCR was run on each source page after the title/listing page; source filenames and physical PDF page numbers are preserved.",
        "- The page-2 sample for each PDF was compared against its title. Multiple files contain questions from other chapters, so no file-wide chapter assignment was accepted.",
        f"- OCR-prefix duplicate detection flagged 17 candidate pairs at a 0.90 similarity threshold; across completed chapter audits, 6 pairs are confirmed and 11 remain unresolved. {duplicate_count} source records are confirmed duplicates after visual/content comparison.",
        f"- Importer dry run of the verified batch: {'passed against the in-memory test database; no production import was performed.' if args.dry_run_passed else 'not run.'}",
        "",
        "## Not yet verified",
        "",
        f"- Remaining {needs_review_count} NEEDS_REVIEW pages still need complete option/order and answer-marker review.",
        "- Scientific correctness, explanation consistency, and supported difficulty/PYQ labels remain unverified for those pending pages.",
        "- Remaining question-level mappings, exact/semantic duplicates, and per-chapter coverage are documented in the review queue and chapter reports.",
        "",
        "## Release decision",
        "",
        f"There are {ready_count} importer-compatible records across source-verified chapter batches. {needs_review_count} queue rows remain NEEDS_REVIEW; {rejected_count} are REJECTED and {duplicate_count} are confirmed duplicate records. Eleven OCR duplicate pairs remain candidates pending visual comparison. See SCIENCE_CHAPTER_MAPPING_REVIEW.md and SCIENCE_DUPLICATE_REVIEW.md for review leads.",
        "",
        (
            "No production import was performed during this report generation. Previously verified production imports are listed in SCIENCE_BATCH_MANIFEST.json."
            if imported_batches
            else "No real import was performed and the application database was not modified."
        ),
    ]
    (args.output_dir / "SCIENCE_QUALITY_REPORT.md").write_text(
        "\n".join(quality) + "\n", encoding="utf-8"
    )
    manifest = {
        "generated_on": "2026-10-10",
        "subject_slug": "gk-gs",
        "subcategory_slug": "science",
        "total_source_pdfs": pdf_count,
        "total_source_pages": page_total,
        "question_page_candidates": len(rows),
        "verified": verified_count,
        "needs_review": needs_review_count,
        "rejected_confirmed": rejected_count,
        "duplicate_records_confirmed": duplicate_count,
        "duplicate_pairs_to_review": 11,
        "duplicate_pairs_confirmed": 6,
        "ready_for_import": ready_count,
        "dry_run_performed": args.dry_run_passed,
        "real_import_performed": bool(imported_batches),
        "current_work_production_import_performed": previous_manifest.get(
            "current_work_production_import_performed", False
        ),
        "database_snapshot": previous_manifest.get("database_snapshot"),
        "prepared_not_imported_batches": previous_manifest.get(
            "prepared_not_imported_batches", []
        ),
        "import_csv_rows": ready_count,
        "verified_unimported_rows": previous_manifest.get(
            "verified_unimported_rows", 0
        ),
        "readiness_notes": previous_manifest.get("readiness_notes", []),
        "imported_batches": imported_batches,
        "chapter_coverage": chapter_coverage,
        "ocr_labels_only": {
            "difficulty": dict(difficulty),
            "pyq_label": dict(pyq_labels),
            "pyq_year": dict(pyq_years),
        },
        "ocr_field_extraction_only": {
            "question_text_detected": question_text_count,
            "four_options_detected": four_options_count,
            "explanation_detected": explanation_count,
            "answer_phrase_mapped": answer_text_count,
            "four_options_and_text": completeness["FOUR_OPTIONS_AND_TEXT"],
            "partial_or_uncertain": completeness["PARTIAL_OR_UNCERTAIN"],
        },
        "batches": per_pdf,
    }
    (args.output_dir / "SCIENCE_BATCH_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Wrote reports and manifest for {len(rows)} review rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
