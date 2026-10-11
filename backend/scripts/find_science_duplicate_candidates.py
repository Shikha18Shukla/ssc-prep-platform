"""Find near-duplicate question-text candidates in the Science OCR queue."""

from __future__ import annotations

import argparse
import csv
import re
from difflib import SequenceMatcher
from pathlib import Path


def question_prefix(raw: str) -> str:
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    start = next(
        (i for i, line in enumerate(lines) if re.search(r"\b(EASY|MEDIUM|HARD)\b", line, re.I)),
        0,
    )
    lines = lines[start + 1 :]
    end = next(
        (i for i, line in enumerate(lines) if line.casefold().startswith("solution")),
        len(lines),
    )
    lines = lines[:end]
    option_start = next(
        (i for i, line in enumerate(lines) if re.match(r"^[1-4][.) ]+", line)),
        len(lines),
    )
    question = " ".join(lines[:option_start])
    return re.sub(r"[^a-z0-9]+", " ", question.casefold()).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("queue_csv", type=Path)
    parser.add_argument("output_md", type=Path)
    args = parser.parse_args()
    with args.queue_csv.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))

    candidates: list[tuple[float, dict[str, str], dict[str, str], str]] = []
    texts = [question_prefix(row["raw_ocr_text"]) for row in rows]
    for left_index, left in enumerate(rows):
        if len(texts[left_index]) < 20:
            continue
        for right_index in range(left_index + 1, len(rows)):
            if len(texts[right_index]) < 20:
                continue
            ratio = SequenceMatcher(None, texts[left_index], texts[right_index]).ratio()
            if ratio >= 0.90:
                kind = "exact OCR prefix" if texts[left_index] == texts[right_index] else "near-duplicate candidate"
                candidates.append((ratio, left, rows[right_index], kind))

    candidates.sort(key=lambda item: (-item[0], item[1]["source_pdf"], item[1]["source_page"]))
    lines = [
        "# Science Possible Duplicate Review",
        "",
        f"OCR-prefix similarity produced {len(candidates)} candidate pairs at a 0.90 threshold.",
        "These are leads for visual comparison, not confirmed duplicate records. OCR errors, repeated question stems, and truncated page text can create false positives.",
        "",
        "| Similarity | Type | Source A | Page | Source B | Page | OCR question prefix |",
        "|---:|---|---|---:|---|---:|---|",
    ]
    for ratio, left, right, kind in candidates:
        excerpt = question_prefix(left["raw_ocr_text"]).replace("|", "\\|")[:130]
        lines.append(
            f"| {ratio:.3f} | {kind} | {left['source_pdf']} | {left['source_page']} | "
            f"{right['source_pdf']} | {right['source_page']} | {excerpt} |"
        )
    if not candidates:
        lines.extend(["", "No OCR-prefix pairs crossed the threshold; this is not proof that no semantic duplicates exist."])
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(candidates)} duplicate candidates to {args.output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
