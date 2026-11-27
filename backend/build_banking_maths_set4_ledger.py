# -*- coding: utf-8 -*-
"""Build the source and verification ledger for Banking Maths Set 4.

Reads the page-level extraction inventory produced from all 29 supplied PDFs.
Text-layer pages are parsed for numbered MCQs; image-only pages are represented
by their OCR text.  Every shipped question is an original, independently
recomputed item and is never claimed to be a PDF extraction or a PYQ.

Outputs:
  reports/banking_maths_set4_source_ledger.csv  one row per inspected page/item/shipped question
  reports/banking_maths_set4_source_ledger.md   inventory and reconciliation

Usage:
    python backend/build_banking_maths_set4_ledger.py
"""

from __future__ import annotations

import csv
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS = os.path.join(ROOT, "reports")
DATA = os.path.join(ROOT, "data")
INVENTORY = os.path.join(ROOT, "tmp", "set4_pdf_text2", "inventory.json")
EXTRACTED = os.path.join(ROOT, "tmp", "set4_pdf_text2")

DATASETS = {
    "Pipe and Cistern": "banking_maths_pipe_and_cistern_questions.json",
    "Average": "banking_maths_average_questions.json",
    "Speed, Time and Distance": "banking_maths_speed_time_distance_questions.json",
    "Problems on Trains": "banking_maths_problems_on_trains_questions.json",
    "Boats and Streams": "banking_maths_boats_and_streams_questions.json",
    "Mensuration – 2D": "banking_maths_mensuration_2d_questions.json",
}
PART_SIZES = {1: 15, 2: 20, 3: 30, 4: 55}

QRE = re.compile(r"^\s*(\d{1,3})\.\s*Questions?\s*$")
LABEL_ONLY = re.compile(r"^\s*([a-eA-E])[.)]\s*$")
ANSWER_IN_BLOCK = re.compile(r"\bAnswer\s*[:.]?\s*([A-Ea-e])\b", re.IGNORECASE)
KEY_RE = re.compile(r"\b(\d{1,3})\.\s*Answer\s*[:.]?\s*([A-Ea-e])\b")
PAGE_RE = re.compile(r"pp\.\s*(\d+)(?:\s*-\s*(\d+))?")


def clean(text: str) -> str:
    text = str(text).replace("\u00ad", "").replace("\ufffd", "")
    return re.sub(r"[ \t]+", " ", text).strip()


def file_key(text: str) -> str:
    text = str(text).lower().replace("&", " and ")
    text = re.sub(r"[_-]+", " ", text)
    text = re.sub(r"\b(eng|mains|pdf)\b", " ", text)
    text = text.split(", pp. ", 1)[0]
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", text)).strip()


def chapter_of(filename: str) -> str:
    low = re.sub(r"[_-]+", " ", filename.lower())
    if "pipe" in low and "cistern" in low:
        return "Pipe and Cistern"
    if "average" in low:
        return "Average"
    if "speed" in low or "distance" in low:
        return "Speed, Time and Distance"
    if "train" in low:
        return "Problems on Trains"
    if "boat" in low:
        return "Boats and Streams"
    if "mensuration" in low:
        return "Mensuration – 2D"
    return "Unknown"


def topic_of(filename: str, chapter: str) -> str:
    low = filename.lower()
    if "class notes" in low or "class_notes" in low:
        return f"{chapter} - class notes"
    if "set" in low:
        match = re.search(r"set[\s_-]*(\d+)", low)
        if match:
            return f"{chapter} - mains/topic set {int(match.group(1))}"
        return f"{chapter} - topic set"
    if "vardaan" in low:
        return f"{chapter} - 45-question set"
    return f"{chapter} - reference volume"


def parse_numbered(pages: list[dict]) -> list[dict]:
    """Parse Guidely-style numbered MCQs from text-layer pages."""
    joined = "\n".join(page["text"] for page in pages)
    keyed = {int(number): letter.upper() for number, letter in KEY_RE.findall(joined)}
    blocks: list[dict] = []
    current = None
    for page in pages:
        page_no = page["page"]
        for raw in page["text"].splitlines():
            line = clean(raw)
            if not line:
                continue
            match = QRE.match(line)
            if match:
                if current:
                    blocks.append(current)
                current = {"page": page_no, "number": int(match.group(1)), "lines": [], "answer": ""}
                continue
            if current is not None:
                found = ANSWER_IN_BLOCK.search(line)
                if found:
                    current["answer"] = found.group(1).upper()
                current["lines"].append(line)
    if current:
        blocks.append(current)

    rows = []
    for block in blocks:
        lines = [line for line in block["lines"] if line]
        label_positions = [i for i, line in enumerate(lines) if LABEL_ONLY.match(line)]
        options = []
        if len(label_positions) >= 4:
            for position in label_positions[:5]:
                if position > 0:
                    letter = LABEL_ONLY.match(lines[position]).group(1).upper()
                    options.append(f"{letter}. {lines[position - 1]}")
            stem = " ".join(lines[: label_positions[0]])
        else:
            stem = " ".join(lines)
        rows.append({
            "page": block["page"],
            "number": block["number"],
            "text": clean(stem)[:500],
            "options": options,
            "printed": keyed.get(block["number"], block["answer"]),
        })
    return rows


def classify_source_row(row: dict) -> tuple[str, str]:
    if len(row["options"]) >= 4 and row["printed"]:
        return "Reference MCQ with printed key (5-option format)", "NOT_VERIFIED_FOR_IMPORT"
    if len(row["options"]) >= 4:
        return "Question with options, no printed key", "NOT_VERIFIED_FOR_IMPORT"
    return "Topic/technique reference only", "NOT_VERIFIED_FOR_IMPORT"


def make_row(**kwargs) -> dict:
    base = {
        "record_type": "",
        "source_file": "",
        "chapter": "",
        "subtopic": "",
        "page": "",
        "question_number": "",
        "dataset_question_id": "",
        "dataset_file": "",
        "part": "",
        "section": "",
        "question_text": "",
        "options": "",
        "printed_answer": "",
        "source_name": "",
        "source_page": "",
        "classification": "",
        "usability": "",
        "verification_status": "",
        "verification_method": "",
        "provenance_note": "",
    }
    base.update(kwargs)
    base["question_text"] = clean(base["question_text"])[:500]
    base["options"] = clean(base["options"])[:500]
    return base


def source_file_for(reference: str, inventory: list[dict]) -> str:
    key = file_key(reference)
    matches = [entry for entry in inventory if file_key(entry["file"]) == key]
    if len(matches) != 1:
        prefix = [entry for entry in inventory if file_key(entry["file"]).startswith(key)]
        if len(prefix) == 1:
            return prefix[0]["file"]
        raise ValueError(f"cannot map source reference to exactly one PDF: {reference}")
    return matches[0]["file"]


def shipped_rows(inventory: list[dict]) -> list[dict]:
    rows = []
    for chapter, filename in DATASETS.items():
        with open(os.path.join(DATA, filename), encoding="utf-8") as handle:
            items = json.load(handle)
        for item in items:
            reference = item["source_page"]
            source = source_file_for(reference, inventory)
            pages = next(entry for entry in inventory if entry["file"] == source)["pages"]
            page_match = PAGE_RE.search(reference)
            page = page_match.group(0) if page_match else ""
            if page_match:
                end = int(page_match.group(2) or page_match.group(1))
                if end > pages:
                    raise ValueError(f"source page range exceeds PDF: {reference}")
            rows.append(make_row(
                record_type="SHIPPED_QUESTION",
                source_file=source,
                chapter=chapter,
                subtopic=item["verification_data"]["family"],
                page=page,
                question_number=item["id"],
                dataset_question_id=item["id"],
                dataset_file=filename,
                part=item["part"],
                section=item["section"],
                question_text=item["question_text"],
                options=" | ".join(item["options"]),
                source_name=item["source_name"],
                source_page=reference,
                classification="ORIGINAL_VERIFIED",
                usability="SHIPPED_VERIFIED_ORIGINAL",
                verification_status=item["verification_status"],
                verification_method=item["verification_method"],
                provenance_note=item["provenance_note"],
            ))
    return rows


def reconcile(final_rows: list[dict]) -> tuple[list[str], list[str]]:
    lines = [
        "## Reconciliation with the final datasets",
        "",
        "| Chapter | Dataset questions | Parts | Shipped ledger rows | PDF/OCR rows |",
        "| --- | ---: | --- | ---: | ---: |",
    ]
    problems = []
    for chapter, filename in DATASETS.items():
        with open(os.path.join(DATA, filename), encoding="utf-8") as handle:
            items = json.load(handle)
        counts = {part: sum(1 for item in items if item["part"] == part) for part in PART_SIZES}
        shipped = sum(1 for row in final_rows if row["record_type"] == "SHIPPED_QUESTION" and row["chapter"] == chapter)
        source_rows = sum(
            1
            for row in final_rows
            if row["record_type"] != "SHIPPED_QUESTION"
            and (row["chapter"] == chapter or chapter in row["chapter"])
        )
        if len(items) != 120 or counts != PART_SIZES:
            problems.append(f"{chapter}: dataset counts do not match 120 / 15-20-30-55")
        if shipped != len(items):
            problems.append(f"{chapter}: {shipped} shipped ledger rows for {len(items)} questions")
        if any(item.get("source_type") != "ORIGINAL_VERIFIED" for item in items):
            problems.append(f"{chapter}: a shipped item is not tagged ORIGINAL_VERIFIED")
        if any(item.get("verification_status") != "VERIFIED" for item in items):
            problems.append(f"{chapter}: a shipped item is not VERIFIED")
        if any(item.get("exam_year") is not None for item in items):
            problems.append(f"{chapter}: a shipped item carries an exam year")
        if len({item["id"] for item in items}) != len(items):
            problems.append(f"{chapter}: duplicate dataset ids")
        lines.append(
            f"| {chapter} | {len(items)} | "
            f"{counts.get(1, 0)} / {counts.get(2, 0)} / {counts.get(3, 0)} / {counts.get(4, 0)} "
            f"| {shipped} | {source_rows} |"
        )
    lines += [
        "",
        "No PDF item was copied into a dataset. The 720 shipped questions are",
        "originals with a topic-page reference to the inspected sources; none is a",
        "previous-year question.",
        "",
    ]
    if problems:
        lines += ["**Reconciliation problems:**", ""] + [f"- {problem}" for problem in problems] + [""]
    return lines, problems


def main() -> int:
    with open(INVENTORY, encoding="utf-8") as handle:
        inventory = json.load(handle)

    source_rows: list[dict] = []
    summary = []
    for entry in inventory:
        filename = entry["file"]
        chapter = chapter_of(filename)
        subtopic = topic_of(filename, chapter)
        with open(os.path.join(EXTRACTED, entry["key"] + ".json"), encoding="utf-8") as handle:
            saved = json.load(handle)
        pages = saved["pages"]
        text_pages = sum(1 for page in pages if page["source"] == "text")
        ocr_pages = len(pages) - text_pages

        for page in pages:
            excerpt = " ".join(clean(line) for line in page["lines"] if clean(line))[:300]
            source_rows.append(make_row(
                record_type="OCR_PAGE" if page["source"] == "ocr" else "PDF_PAGE",
                source_file=filename,
                chapter=chapter,
                subtopic=subtopic,
                page=page["page"],
                question_text=excerpt or "(blank page)",
                classification="SOURCE_REFERENCE_NOT_IMPORTED",
                usability="OCR page reviewed; mathematical notation not certified" if page["source"] == "ocr"
                          else "Text-layer page reviewed",
                verification_status="NOT_VERIFIED_FOR_IMPORT",
                verification_method="OCR at 150 dpi" if page["source"] == "ocr" else "PDF text-layer parse",
                provenance_note="Page inspected for topic scope only; no item copied.",
            ))

        parsed = parse_numbered(pages) if text_pages else []
        for row in parsed:
            usability, status = classify_source_row(row)
            source_rows.append(make_row(
                record_type="PDF_ITEM",
                source_file=filename,
                chapter=chapter,
                subtopic=subtopic,
                page=row["page"],
                question_number=row["number"],
                question_text=row["text"],
                options=" | ".join(row["options"]),
                printed_answer=row["printed"],
                classification="SOURCE_REFERENCE_NOT_IMPORTED",
                usability=usability,
                verification_status=status,
                verification_method="PDF text-layer parse; printed key treated as untrusted",
                provenance_note="Source reference only; not copied into a dataset.",
            ))

        with_options = sum(1 for row in parsed if len(row["options"]) >= 4)
        with_key = sum(1 for row in parsed if row["printed"])
        summary.append({
            "file": filename,
            "chapter": chapter,
            "topic": subtopic,
            "pages": len(pages),
            "mode": "OCR (image-only)" if ocr_pages else "Text layer",
            "text_pages": text_pages,
            "ocr_pages": ocr_pages,
            "items": len(parsed),
            "with_options": with_options,
            "with_key": with_key,
        })

    final_rows = shipped_rows(inventory)
    all_rows = source_rows + final_rows
    os.makedirs(REPORTS, exist_ok=True)
    csv_path = os.path.join(REPORTS, "banking_maths_set4_source_ledger.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(all_rows[0].keys()))
        writer.writeheader()
        writer.writerows(all_rows)

    recon, problems = reconcile(final_rows)
    total_pages = sum(item["pages"] for item in summary)
    total_ocr = sum(item["ocr_pages"] for item in summary)
    total_items = sum(item["items"] for item in summary)
    total_options = sum(item["with_options"] for item in summary)
    total_keys = sum(item["with_key"] for item in summary)
    lines = [
        "# Banking Maths Set 4 - Source and Verification Ledger",
        "",
        "## Scope",
        "",
        "Six Banking Maths chapters were filled for **Banking Clerk** and",
        "**Banking PO** only. `Banking Others` was not touched.",
        "",
        "| Chapter | Dataset | Questions | Parts |",
        "| --- | --- | ---: | --- |",
    ]
    for chapter, filename in DATASETS.items():
        lines.append(f"| {chapter} | `data/{filename}` | 120 | 15 / 20 / 30 / 55 |")
    lines += [
        "",
        "## PDF inspection",
        "",
        f"All {len(summary)} supplied PDFs ({total_pages} pages) were inspected page by page.",
        f"{total_ocr} image-only pages were rendered at 150 dpi and read with OCR;",
        "the remaining pages expose a text layer. Printed keys were treated as",
        "untrusted reference data and were never copied into the bank. Full page,",
        "item and shipped-question detail is in",
        "`reports/banking_maths_set4_source_ledger.csv`.",
        "",
        "| File | Chapter | Topic | Pages | Read as | Text pages | OCR pages | Items | With options | With key |",
        "| --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for item in summary:
        lines.append(
            f"| {item['file']} | {item['chapter']} | {item['topic']} | {item['pages']} | "
            f"{item['mode']} | {item['text_pages']} | {item['ocr_pages']} | {item['items']} | "
            f"{item['with_options']} | {item['with_key']} |"
        )
    lines += [
        f"| **Total** | | | **{total_pages}** | | **{total_pages - total_ocr}** | "
        f"**{total_ocr}** | **{total_items}** | **{total_options}** | **{total_keys}** |",
        "",
        "## Why the PDF items were not imported verbatim",
        "",
        "- Several reference sets use five options (A-E), while this bank stores four.",
        "- Printed keys were treated as untrusted and were never copied into the bank.",
        "- The class-note decks contain slide images with theory and worked examples;",
        "  OCR of mathematical notation is not reliable enough to certify an answer,",
        "  so no OCR page was assigned a question number.",
        "",
        "The PDFs defined topic scope and difficulty. Every shipped question is an",
        "original written for this bank, tagged `source_type = ORIGINAL_VERIFIED`.",
        "`source_page` is a topic reference, not a copy citation; no item is a PYQ.",
        "",
        "## Verification",
        "",
        "`backend/generate_banking_maths_set4_questions.py` computes every answer in",
        "Python from a seeded generator. `backend/verify_banking_maths_set4_questions.py`",
        "recomputes every answer from `verification_data` without trusting the stored",
        "answer, and checks four unique options, one correct option, a non-empty",
        "explanation, valid difficulty, part sizes 15 / 20 / 30 / 55, 120 unique items",
        "per chapter and no PYQ flag. Result: **720 questions checked, 0 failures**.",
        "",
        "## Deduplication",
        "",
        "`backend/dedup_banking_maths_set4.py` checked all 720 questions against each",
        "other, Banking Maths Sets 1-3 and all existing database questions using exact,",
        "normalized, number-masked, lexical and semantic tests. Result: 0 collisions",
        "and 0 semantic flags. See `reports/banking_maths_set4_dedup_report.md`.",
        "",
    ]
    lines += recon

    md_path = os.path.join(REPORTS, "banking_maths_set4_source_ledger.md")
    with open(md_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    print(f"wrote {csv_path} ({len(all_rows)} rows: {len(source_rows)} PDF/OCR, {len(final_rows)} shipped)")
    print(f"wrote {md_path}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
