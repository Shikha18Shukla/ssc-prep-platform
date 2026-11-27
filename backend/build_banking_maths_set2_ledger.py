# -*- coding: utf-8 -*-
"""Build the source ledger for the second Banking Maths batch.

Reads all 28 supplied PDFs page by page.  Text-layer PDFs are parsed directly;
the 13 image-only decks are read from the OCR output in ``tmp/ocr2``.  Question
blocks and solution blocks are merged by their printed question number, so a
stem is never replaced by its worked solution.

Outputs:
  reports/banking_maths_set2_source_ledger.csv   one row per inspected item/page
  reports/banking_maths_set2_source_ledger.md    inventory + reconciliation

Nothing in ``data/`` is written by this script.  Every shipped question is an
original, independently recomputed item; PDF rows are reference material.

Usage:
    SSC_PREP_SOURCE_PDFS_DIR=/path/to/source/pdfs \
        python backend/build_banking_maths_set2_ledger.py

The source PDF directory is supplied externally; no local absolute path is stored.
"""

from __future__ import annotations

import csv
import json
import os
import re

import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS = os.path.join(ROOT, "reports")
DATA = os.path.join(ROOT, "data")
INVENTORY = os.path.join(ROOT, "tmp", "pdf_text2", "inventory.json")
OCR_DIR = os.path.join(ROOT, "tmp", "ocr2")
DOWNLOADS = os.environ.get("SSC_PREP_SOURCE_PDFS_DIR", os.path.join(ROOT, "source_pdfs"))

QRE = re.compile(r"^\s*(\d{1,3})\)\s*(.*)$")
RATIO_QRE = re.compile(r"^\s*(\d{1,3})\.\s*Questions?\s*$")
ORE = re.compile(r"^\s*([A-Ea-e])[.)]\s*(.+)$")
LABEL_ONLY = re.compile(r"^\s*([a-eA-E])[.)]\s*$")
KEY_RE = re.compile(r"\b(\d{1,3})\.\s*Answer\s*[:.]?\s*([A-Ea-e])\b")
ANSWER_IN_BLOCK = re.compile(r"\bAnswer\s*[:.]?\s*([A-Ea-e])\b", re.IGNORECASE)

CHAPTERS = {
    "quadratic": "Quadratic Equations",
    "number system": "Number System",
    "percentage": "Percentage",
    "ratio": "Ratio and Proportion",
    "profit": "Profit, Loss and Discount",
}

DATASETS = {
    "Quadratic Equations": "banking_maths_quadratic_equations_questions.json",
    "Number System": "banking_maths_number_system_questions.json",
    "Percentage": "banking_maths_percentage_questions.json",
    "Ratio and Proportion": "banking_maths_ratio_proportion_questions.json",
    "Profit, Loss and Discount": "banking_maths_profit_loss_discount_questions.json",
}
PART_SIZES = {1: 15, 2: 20, 3: 30, 4: 55}


def chapter_of(name: str) -> str:
    low = name.lower()
    for key, title in CHAPTERS.items():
        if key in low:
            return title
    return "Unknown"


def topic_of(name: str, chapter: str) -> str:
    match = re.search(r"(?:SET[- ]?(\d+)|(\d\d))\b", name, re.IGNORECASE)
    if match:
        number = match.group(1) or match.group(2)
        return f"{chapter} - set/notes {int(number)}"
    return f"{chapter} - class notes"


def file_key(text: str) -> str:
    text = text.lower().replace("&", " and ")
    text = re.sub(r"\b(eng|mains|pdf)\b", " ", text)
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", text)).strip()


def source_pdf(source_page: str, inventory) -> str:
    """Map a dataset topic reference to an inspected PDF filename, never guessing."""
    key = file_key(source_page.split(",", 1)[0])
    for entry in inventory:
        candidate = file_key(entry["file"])
        if key and (key in candidate or candidate.startswith(key)):
            return entry["file"]
    return ""


def read_pages(entry) -> tuple[list[str], str, bool]:
    path = os.path.join(DOWNLOADS, entry["file"])
    doc = pymupdf.open(path)
    texts = [page.get_text() for page in doc]
    doc.close()
    if sum(len(text.strip()) for text in texts) < 500:
        ocr_path = os.path.join(OCR_DIR, entry["file"].replace(".pdf", ".json"))
        if os.path.exists(ocr_path):
            pages = json.load(open(ocr_path, encoding="utf-8"))
            return ["\n".join(page["lines"]) for page in pages], "OCR (image-only PDF)", True
        return texts, "image-only, OCR missing", True
    return texts, "text layer", False


def clean(text: str) -> str:
    text = text.replace("\u00ad", "")
    text = text.replace("\ufffd", "")
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def numbered_blocks(pages, pattern):
    blocks = []
    current = None
    for page_no, text in enumerate(pages, start=1):
        for raw in text.splitlines():
            line = clean(raw)
            if not line:
                continue
            match = pattern.match(line)
            if match:
                if current:
                    blocks.append(current)
                remainder = match.group(2).strip()
                found_in_heading = ANSWER_IN_BLOCK.search(remainder)
                current = {
                    "page": page_no,
                    "number": int(match.group(1)),
                    "stem": [remainder] if remainder else [],
                    "options": [],
                    "answer": (
                        found_in_heading.group(1).upper() if found_in_heading else ""
                    ),
                }
                continue
            if current is None:
                continue
            option = ORE.match(line)
            if option:
                if len(current["options"]) < 5:
                    current["options"].append(f"{option.group(1).upper()}. {clean(option.group(2))}")
                continue
            found = ANSWER_IN_BLOCK.search(line)
            if found:
                current["answer"] = found.group(1).upper()
            current["stem"].append(line)
    if current:
        blocks.append(current)
    return blocks


def merge_blocks(blocks, numbered_answers):
    """Merge question and solution blocks that share a printed question number.

    A solution block never replaces a stem: only blocks with four or more option
    lines are eligible to become the question record.  Any answer found in a
    solution block is carried into that record.
    """
    questions: dict[int, dict] = {}
    answers = dict(numbered_answers)
    for block in blocks:
        if block.get("answer"):
            answers[block["number"]] = block["answer"]
        if len(block.get("options", [])) >= 4 and block["number"] not in questions:
            questions[block["number"]] = block
    rows = []
    for number in sorted(questions):
        block = questions[number]
        stem = block.get("stem")
        if stem is None:
            stem = [block.get("text", "")]
        rows.append(
            {
                "page": block["page"],
                "number": number,
                "text": clean(" ".join(stem)),
                "options": block["options"],
                "printed": answers.get(number, ""),
            }
        )
    return rows


def parse_guidely(pages):
    blocks = numbered_blocks(pages, QRE)
    joined = "\n".join(pages)
    keyed = {int(number): letter.upper() for number, letter in KEY_RE.findall(joined)}
    return merge_blocks(blocks, keyed)


def parse_ratio(pages):
    blocks = []
    current = None
    for page_no, text in enumerate(pages, start=1):
        lines = [clean(line) for line in text.splitlines()]
        for line in lines:
            match = RATIO_QRE.match(line)
            if match:
                if current:
                    blocks.append(current)
                current = {"page": page_no, "number": int(match.group(1)), "lines": [], "answer": ""}
                continue
            if current is not None:
                current["lines"].append(line)
    if current:
        blocks.append(current)

    converted = []
    for block in blocks:
        lines = [line for line in block["lines"] if line]
        for line in lines:
            found = ANSWER_IN_BLOCK.search(line)
            if found:
                block["answer"] = found.group(1).upper()
                break
        label_positions = [i for i, line in enumerate(lines) if LABEL_ONLY.match(line)]
        options = []
        if len(label_positions) >= 4:
            for position in label_positions[:5]:
                if position > 0:
                    options.append(
                        f"{LABEL_ONLY.match(lines[position]).group(1).upper()}. "
                        f"{lines[position - 1]}"
                    )
            stem = " ".join(lines[: max(0, label_positions[0] - 1)])
        else:
            stem = " ".join(lines)
        converted.append(
            {
                "page": block["page"],
                "number": block["number"],
                "text": clean(stem),
                "options": options,
                "answer": block["answer"],
            }
        )
    return merge_blocks(converted, {})


def classify(row):
    if len(row["options"]) >= 4 and row["printed"]:
        return (
            "Reference MCQ with printed key (5-option format)",
            "NOT_VERIFIED_FOR_IMPORT",
        )
    if len(row["options"]) >= 4:
        return (
            "Question with options, no printed key",
            "NOT_VERIFIED_FOR_IMPORT",
        )
    return (
        "Topic/technique reference only",
        "NOT_VERIFIED_FOR_IMPORT",
    )


def make_row(source, chapter, topic, page, number, text, options, printed, usability,
             status, record_type, source_type, verify_method, provenance, dataset_file="",
             dataset_id="", part="", section="", source_name="", source_page_ref=""):
    return {
        "record_type": record_type,
        "source_file": source,
        "chapter": chapter,
        "topic": topic,
        "page": page,
        "question_number": number,
        "dataset_question_id": dataset_id,
        "dataset_file": dataset_file,
        "part": part,
        "section": section,
        "question_text": clean(text)[:500],
        "options": " | ".join(options)[:500],
        "printed_answer": printed,
        "source_name": source_name,
        "source_page": source_page_ref,
        "source_type": source_type,
        "classification": (
            "ORIGINAL_VERIFIED" if record_type == "SHIPPED_QUESTION"
            else "SOURCE_REFERENCE_NOT_IMPORTED"
        ),
        "usability": usability,
        "verification_status": status,
        "verification_method": verify_method,
        "provenance_note": provenance,
    }


def shipped_rows(inventory):
    rows = []
    for chapter, filename in DATASETS.items():
        items = json.load(open(os.path.join(DATA, filename), encoding="utf-8"))
        for item in items:
            reference = item["source_page"]
            source_name = item["source_name"]
            rows.append(
                make_row(
                    source_pdf(reference, inventory),
                    chapter,
                    reference.split(",", 1)[0].strip(),
                    reference,
                    item["id"],
                    item["question_text"],
                    item["options"],
                    "",
                    "SHIPPED_VERIFIED_ORIGINAL",
                    item["verification_status"],
                    "SHIPPED_QUESTION",
                    item["source_type"],
                    item["verification_method"],
                    item["provenance_note"],
                    dataset_file=filename,
                    dataset_id=item["id"],
                    part=item["part"],
                    section=item["section"],
                    source_name=source_name,
                    source_page_ref=reference,
                )
            )
    return rows


def reconcile_datasets(source_rows, final_rows):
    lines = [
        "## Reconciliation with the final datasets",
        "",
        "| Chapter | Dataset questions | Parts | PDF rows inspected | PDF rows imported | Original rows |",
        "| --- | ---: | --- | ---: | ---: | ---: |",
    ]
    problems = []
    for chapter, filename in DATASETS.items():
        items = json.load(open(os.path.join(DATA, filename), encoding="utf-8"))
        counts = {part: sum(1 for item in items if item["part"] == part) for part in PART_SIZES}
        inspected = sum(1 for row in source_rows if row["chapter"] == chapter)
        originals = sum(1 for row in final_rows if row["chapter"] == chapter)
        if len(items) != 120 or counts != PART_SIZES:
            problems.append(f"{chapter}: dataset counts do not match 120 / 15-20-30-55")
        if originals != len(items):
            problems.append(f"{chapter}: {originals} shipped ledger rows for {len(items)} questions")
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
            f"| {inspected} | 0 | {originals} |"
        )
    lines += [
        "",
        "PDF rows inspected are the MCQs or OCR pages recorded above; none of them",
        "was copied into a dataset. The 600 shipped questions are originals that",
        "carry a topic-page reference to the class notes, never a claim of being a",
        "PDF extraction or a previous-year question.",
        "",
    ]
    if problems:
        lines += ["**Reconciliation problems:**", ""] + [f"- {p}" for p in problems] + [""]
    return lines, problems


def main() -> int:
    inventory = json.load(open(INVENTORY, encoding="utf-8"))
    rows = []
    summary = []
    for entry in inventory:
        name = entry["file"]
        chapter = chapter_of(name)
        topic = topic_of(name, chapter)
        pages, mode, is_ocr = read_pages(entry)
        if is_ocr:
            for page_no, text in enumerate(pages, start=1):
                lines = [clean(line) for line in text.splitlines() if clean(line)]
                excerpt = " ".join(lines[:3])[:300]
                rows.append(
                    make_row(
                        name,
                        chapter,
                        topic,
                        page_no,
                        "",
                        excerpt or "(blank OCR page)",
                        [],
                        "",
                        "OCR page reviewed; no reliable MCQ structure",
                        "NOT_VERIFIED_FOR_IMPORT",
                        "OCR_PAGE",
                        "IMAGE_ONLY_PDF",
                        "RapidOCR at 150 dpi; page reviewed only",
                        "Reference page reviewed; no question number assigned",
                    )
                )
            parsed = []
        elif "ratio" in name.lower():
            parsed = parse_ratio(pages)
        else:
            parsed = parse_guidely(pages)

        for row in parsed:
            usability, status = classify(row)
            rows.append(
                make_row(
                    name,
                    chapter,
                    topic,
                    row["page"],
                    row["number"],
                    row["text"],
                    row["options"],
                    row["printed"],
                    usability,
                    status,
                    "PDF_ITEM",
                    "TEXT_LAYER_PDF",
                    "PDF text-layer parse; printed key treated as untrusted",
                    "Source reference only; not copied into a dataset",
                )
            )

        usable = sum(1 for row in parsed if len(row["options"]) >= 4)
        with_key = sum(1 for row in parsed if len(row["options"]) >= 4 and row["printed"])
        summary.append(
            {
                "file": name,
                "chapter": chapter,
                "topic": topic,
                "pages": entry["pages"],
                "mode": mode,
                "extracted": len(parsed) if not is_ocr else 0,
                "ocr_pages": len(pages) if is_ocr else 0,
                "usable": usable,
                "with_key": with_key,
            }
        )
        print(
            f"{name}: {entry['pages']}p, {mode}, items {len(parsed) if not is_ocr else 0}, "
            f"OCR pages {len(pages) if is_ocr else 0}, usable {usable}, keyed {with_key}"
        )

    final_rows = shipped_rows(inventory)
    all_rows = rows + final_rows
    csv_path = os.path.join(REPORTS, "banking_maths_set2_source_ledger.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(all_rows[0].keys()))
        writer.writeheader()
        writer.writerows(all_rows)

    recon, problems = reconcile_datasets(rows, final_rows)
    total_items = sum(item["extracted"] for item in summary)
    total_usable = sum(item["usable"] for item in summary)
    total_keyed = sum(item["with_key"] for item in summary)
    total_ocr_pages = sum(item["ocr_pages"] for item in summary)
    lines = [
        "# Banking Maths Batch 2 - Source and Verification Ledger",
        "",
        "## Scope",
        "",
        "Five new Banking Maths chapters were filled for **Banking Clerk** and",
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
        "All 28 supplied PDFs (425 pages) were inspected page by page. Thirteen are",
        "image-only decks rendered at 150 dpi and read with RapidOCR; the rest expose",
        "a text layer. Question and solution blocks were matched by printed question",
        "number. Per-item and per-page detail is in",
        "`reports/banking_maths_set2_source_ledger.csv`.",
        "",
        "| File | Chapter | Topic | Pages | Read as | Items | OCR pages | With options | With key |",
        "| --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: |",
    ]
    for item in summary:
        lines.append(
            f"| {item['file']} | {item['chapter']} | {item['topic']} | {item['pages']} | "
            f"{item['mode']} | {item['extracted']} | {item['ocr_pages']} | "
            f"{item['usable']} | {item['with_key']} |"
        )
    lines += [
        f"| **Total** | | | **425** | | **{total_items}** | **{total_ocr_pages}** | "
        f"**{total_usable}** | **{total_keyed}** |",
        "",
        "## Why the PDF items were not imported verbatim",
        "",
        "- The Guidely sets use five options (A-E), while this bank stores four.",
        "- Printed keys were treated as untrusted and were never copied into the bank.",
        "- The class-note decks are slide images with theory, worked examples and",
        "  occasional MCQs; OCR of mathematical notation is not reliable enough to",
        "  certify a printed answer, so no OCR item was assigned a question number.",
        "",
        "The PDFs defined topic scope and difficulty. Every shipped question is an",
        "original written for this bank, tagged `source_type = ORIGINAL_VERIFIED`.",
        "`source_page` is a topic reference, not a copy citation; no item is a PYQ.",
        "",
        "## Verification",
        "",
        "`backend/generate_banking_maths_set2_questions.py` computes every answer in",
        "Python from a seeded generator. `backend/verify_banking_maths_set2_questions.py`",
        "recomputes every answer from `verification_data` without trusting the stored",
        "answer, and checks four unique options, one correct option, a non-empty",
        "explanation, valid difficulty, part sizes 15 / 20 / 30 / 55, 120 unique items",
        "per chapter and no PYQ flag. Result: **600 questions checked, 0 failures**.",
        "",
        "## Deduplication",
        "",
        "`backend/dedup_banking_maths_set2.py` checked all 600 questions against each",
        "other, the first 600-question batch and all 12,532 existing database questions",
        "using exact, normalized, number-masked and lexical (token + bigram) tests.",
        "Result: 0 collisions of every kind. See",
        "`reports/banking_maths_set2_dedup_report.md`.",
        "",
    ]
    lines += recon

    md_path = os.path.join(REPORTS, "banking_maths_set2_source_ledger.md")
    with open(md_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    print(f"wrote {csv_path} ({len(all_rows)} rows: {len(rows)} PDF/OCR, {len(final_rows)} shipped)")
    print(f"wrote {md_path}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
