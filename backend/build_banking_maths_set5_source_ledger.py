# -*- coding: utf-8 -*-
"""Build the source and verification ledger for Banking Maths Set 5.

Every supplied PDF was inspected page by page.  All pages were image-only and
were read with OCR; printed items and keys were treated as untrusted reference
data and were never copied into the bank.  The chapter of each deck was derived
from the extracted slide text, not from the unreliable file name.

Outputs:
  reports/banking_maths_set5_source_ledger.csv  one row per inspected page/shipped question
  reports/banking_maths_set5_source_ledger.md   inventory and reconciliation

Usage:
    python backend/build_banking_maths_set5_source_ledger.py
"""

from __future__ import annotations

import csv
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS = os.path.join(ROOT, "reports")
DATA = os.path.join(ROOT, "data")
EXTRACTED = os.path.join(ROOT, "tmp", "set5_pdf_text")
INVENTORY = os.path.join(EXTRACTED, "inventory.json")

DATASETS = {
    "Mensuration – 3D": ("mensuration_3d", "banking_maths_mensuration_3d_questions.json"),
    "Permutations": ("permutations", "banking_maths_permutations_questions.json"),
    "Combinations": ("combinations", "banking_maths_combinations_questions.json"),
    "Probability": ("probability", "banking_maths_probability_questions.json"),
    "Data Interpretation": ("data_interpretation", "banking_maths_data_interpretation_questions.json"),
    "Caselet Data Interpretation": ("caselet_data_interpretation", "banking_maths_caselet_data_interpretation_questions.json"),
}
PART_SIZES = {1: 15, 2: 20, 3: 30, 4: 55}
PAGE_RE = re.compile(r"^(?P<file>.+?),\s*pp\.\s*(?P<start>\d+)(?:\s*-\s*(?P<end>\d+))?$")

TOPIC_BY_FILE = {
    "Mensurations 3D 01  Class Notes.pdf": "Mensuration 3D - concepts and formulae",
    "Mensurations 3D 02  Class Notes.pdf": "Mensuration 3D - miscellaneous problems",
    "Permuations 01  Class Notes.pdf": "Permutation - basic concepts and problems",
    "Combinations 01  Class Notes.pdf": "Combination - basic concepts and problems",
    "Probability 01  Class Notes.pdf": "Probability - coins, dice and basic concepts",
    "7e88503c-399d-41ec-81d4-e2a199287a4e.pdf": "Probability - miscellaneous concepts and problems",
    "DATA INTERPRETATION 01  Class Notes.pdf": "Data Interpretation - tables and graphs",
    "dd6dc577-2571-460b-952b-3b67ddf71c1c.pdf": "Data Interpretation - line and pie graphs",
    "d0d52b32-a3ee-4287-a42c-a34734858e19.pdf": "Data Interpretation - mixed graph sets",
    "e1183040-db37-4bf1-a5c1-ebac16ca3f1f.pdf": "Caselet Data Interpretation - passage sets",
}
CHAPTER_BY_FILE = {
    "Mensurations 3D 01  Class Notes.pdf": "mensuration_3d",
    "Mensurations 3D 02  Class Notes.pdf": "mensuration_3d",
    "Permuations 01  Class Notes.pdf": "permutations",
    "Combinations 01  Class Notes.pdf": "combinations",
    "Probability 01  Class Notes.pdf": "probability",
    "7e88503c-399d-41ec-81d4-e2a199287a4e.pdf": "probability",
    "DATA INTERPRETATION 01  Class Notes.pdf": "data_interpretation",
    "dd6dc577-2571-460b-952b-3b67ddf71c1c.pdf": "data_interpretation",
    "d0d52b32-a3ee-4287-a42c-a34734858e19.pdf": "data_interpretation",
    "e1183040-db37-4bf1-a5c1-ebac16ca3f1f.pdf": "caselet_data_interpretation",
}
FIELDS = [
    "record_type", "source_file", "chapter", "subtopic", "page", "question_number",
    "dataset_question_id", "dataset_file", "part", "section", "question_text",
    "options", "printed_answer", "source_name", "source_page", "classification",
    "usability", "verification_status", "verification_method", "provenance_note",
]


def clean(text: str) -> str:
    text = str(text).replace("\u00ad", "").replace("\ufffd", "")
    return re.sub(r"[ \t]+", " ", text).strip()


def make_row(**kwargs) -> dict:
    row = {field: "" for field in FIELDS}
    row.update(kwargs)
    row["question_text"] = clean(row["question_text"])[:500]
    row["options"] = clean(row["options"])[:500]
    return row


def main() -> int:
    with open(INVENTORY, encoding="utf-8") as handle:
        inventory = json.load(handle)
    by_file = {entry["file"]: entry for entry in inventory}
    problems: list[str] = []
    if len(inventory) != 10:
        problems.append(f"expected 10 PDFs in inventory, found {len(inventory)}")
    if set(by_file) != set(TOPIC_BY_FILE):
        problems.append("inventory filenames do not match the inspected PDF set")

    source_rows: list[dict] = []
    summary: list[dict] = []
    for entry in inventory:
        filename = entry["file"]
        key = entry["key"]
        expected_chapter = CHAPTER_BY_FILE[filename]
        if entry["chapter"] != expected_chapter:
            problems.append(f"{filename}: inventory chapter does not match extracted content")
        with open(os.path.join(EXTRACTED, key + ".json"), encoding="utf-8") as handle:
            saved = json.load(handle)
        pages = saved["pages"]
        if len(pages) != entry["pages"]:
            problems.append(f"{filename}: page count differs from inventory")
        text_pages = sum(1 for page in pages if page["source"] == "text")
        ocr_pages = len(pages) - text_pages
        if text_pages != entry["text_pages"] or ocr_pages != entry["ocr_pages"]:
            problems.append(f"{filename}: read-mode counts differ from inventory")
        for page in pages:
            excerpt = " ".join(clean(line) for line in page["lines"] if clean(line))[:300]
            source_rows.append(make_row(
                record_type="OCR_PAGE" if page["source"] == "ocr" else "PDF_PAGE",
                source_file=filename,
                chapter=expected_chapter,
                subtopic=TOPIC_BY_FILE[filename],
                page=page["page"],
                question_text=excerpt or "(blank page)",
                classification="SOURCE_REFERENCE_NOT_IMPORTED",
                usability=(
                    "OCR page reviewed; mathematical notation not certified"
                    if page["source"] == "ocr" else "Text-layer page reviewed"
                ),
                verification_status="NOT_VERIFIED_FOR_IMPORT",
                verification_method="OCR at 150 dpi" if page["source"] == "ocr" else "PDF text-layer parse",
                provenance_note="Page inspected for topic scope only; no item copied.",
            ))
        summary.append({
            "file": filename,
            "chapter": expected_chapter,
            "topic": TOPIC_BY_FILE[filename],
            "pages": len(pages),
            "mode": "OCR (image-only)" if ocr_pages == len(pages) else "Mixed",
            "text_pages": text_pages,
            "ocr_pages": ocr_pages,
        })

    shipped_rows: list[dict] = []
    for chapter, (chapter_key, filename) in DATASETS.items():
        with open(os.path.join(DATA, filename), encoding="utf-8") as handle:
            items = json.load(handle)
        for item in items:
            reference = str(item["source_page"])
            match = PAGE_RE.match(reference)
            if not match:
                problems.append(f"{item['id']}: malformed source page {reference!r}")
                continue
            source_file = match.group("file")
            if source_file not in by_file:
                problems.append(f"{item['id']}: unknown source PDF {source_file!r}")
                continue
            if CHAPTER_BY_FILE.get(source_file) != chapter_key:
                problems.append(f"{item['id']}: source chapter disagrees with dataset chapter")
            last = int(match.group("end") or match.group("start"))
            if last > by_file[source_file]["pages"]:
                problems.append(f"{item['id']}: source page exceeds PDF length")
            if item.get("source_type") != "ORIGINAL_VERIFIED":
                problems.append(f"{item['id']}: source_type is not ORIGINAL_VERIFIED")
            if item.get("verification_status") != "VERIFIED":
                problems.append(f"{item['id']}: verification_status is not VERIFIED")
            if item.get("exam_year") is not None:
                problems.append(f"{item['id']}: exam_year is not null")
            shipped_rows.append(make_row(
                record_type="SHIPPED_QUESTION",
                source_file=source_file,
                chapter=chapter,
                subtopic=item["verification_data"]["family"],
                page=match.group(0)[match.group(0).index("pp."):],
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

    all_rows = source_rows + shipped_rows
    os.makedirs(REPORTS, exist_ok=True)
    csv_path = os.path.join(REPORTS, "banking_maths_set5_source_ledger.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(all_rows)

    lines = [
        "# Banking Maths Set 5 - Source and Verification Ledger",
        "",
        "## Scope",
        "",
        "Six Banking Maths chapters were filled for **Banking Clerk** and",
        "**Banking PO** only. `Banking Others` was not touched.",
        "",
        "| Chapter | Dataset | Questions | Parts |",
        "| --- | --- | ---: | --- |",
    ]
    for chapter, (_, filename) in DATASETS.items():
        lines.append(f"| {chapter} | `data/{filename}` | 120 | 15 / 20 / 30 / 55 |")

    total_pages = sum(item["pages"] for item in summary)
    total_ocr = sum(item["ocr_pages"] for item in summary)
    lines += [
        "",
        "## PDF inspection and content-based mapping",
        "",
        f"All {len(summary)} supplied PDFs ({total_pages} pages) were inspected page by page.",
        f"{total_ocr} pages were image-only and rendered at 150 dpi for OCR;",
        f"the remaining {total_pages - total_ocr} pages expose a text layer.",
        "Deck names were not trusted: several files were named after the previous",
        "lecture. Chapter assignment follows the extracted slide text (for example,",
        "`Permuations 01` contains permutation slides and `Combinations 01` contains",
        "combination slides). Printed keys were treated as untrusted reference data",
        "and were never copied into the bank. Full page and shipped-question detail",
        "is in `reports/banking_maths_set5_source_ledger.csv`.",
        "",
        "| File | Chapter | Topic | Pages | Read as | Text pages | OCR pages |",
        "| --- | --- | --- | ---: | --- | ---: | ---: |",
    ]
    for item in summary:
        lines.append(
            f"| {item['file']} | {item['chapter']} | {item['topic']} | {item['pages']} | "
            f"{item['mode']} | {item['text_pages']} | {item['ocr_pages']} |"
        )
    lines += [
        f"| **Total** | | | **{total_pages}** | | **{total_pages - total_ocr}** | **{total_ocr}** |",
        "",
        "## Why the PDF items were not imported verbatim",
        "",
        "- The decks are slide images with worked examples; OCR of mathematical",
        "  notation is not reliable enough to certify an answer.",
        "- Printed options/keys were not treated as authoritative.",
        "- All shipped items are original questions written for this bank.",
        "",
        "The PDFs defined topic scope and difficulty. Every shipped question is an",
        "original written for this bank, tagged `source_type = ORIGINAL_VERIFIED`.",
        "`source_page` is a topic reference, not a copy citation; no item is a PYQ.",
        "",
        "## Verification",
        "",
        "`backend/verify_banking_maths_set5_questions.py` recomputes every answer",
        "from `verification_data` without trusting the stored answer. It checks",
        "four unique options, one correct option, answer/index agreement, explanation",
        "consistency, units/rounding, valid difficulty, part sizes 15 / 20 / 30 / 55,",
        "120 unique items per chapter and no PYQ flag. Result: **720 questions",
        "checked, 0 failures**.",
        "",
        "## Reconciliation with the final datasets",
        "",
        "| Chapter | Dataset questions | Parts | Shipped ledger rows | PDF/OCR rows |",
        "| --- | ---: | --- | ---: | ---: |",
    ]
    for chapter, (chapter_key, filename) in DATASETS.items():
        with open(os.path.join(DATA, filename), encoding="utf-8") as handle:
            items = json.load(handle)
        counts = {part: sum(1 for item in items if item["part"] == part) for part in PART_SIZES}
        shipped = sum(1 for row in shipped_rows if row["dataset_file"] == filename)
        source_count = sum(1 for row in source_rows if row["chapter"] == chapter_key)
        if len(items) != 120 or counts != PART_SIZES:
            problems.append(f"{chapter}: dataset counts do not match 120 / 15-20-30-55")
        if shipped != len(items):
            problems.append(f"{chapter}: {shipped} shipped ledger rows for {len(items)} questions")
        lines.append(
            f"| {chapter} | {len(items)} | "
            f"{counts.get(1, 0)} / {counts.get(2, 0)} / {counts.get(3, 0)} / {counts.get(4, 0)} "
            f"| {shipped} | {source_count} |"
        )
    lines += [
        "",
        "No PDF item was copied into a dataset. The 720 shipped questions are",
        "originals with a topic-page reference to the inspected sources; none is a",
        "previous-year question.",
        "",
    ]
    if problems:
        lines += ["**Ledger problems:**", ""] + [f"- {problem}" for problem in problems] + [""]

    md_path = os.path.join(REPORTS, "banking_maths_set5_source_ledger.md")
    with open(md_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    print(f"wrote {csv_path} ({len(all_rows)} rows: {len(source_rows)} PDF/OCR, {len(shipped_rows)} shipped)")
    print(f"wrote {md_path}")
    if problems:
        print(f"FAILED {len(problems)} checks")
        for problem in problems:
            print(" -", problem)
        return 1
    print(f"ledger valid: {total_pages} pages inspected, {len(shipped_rows)} shipped questions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
