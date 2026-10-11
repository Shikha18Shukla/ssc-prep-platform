"""Build a page-level review queue from OCR transcripts; never imports data."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


PAGE_MARKER = re.compile(r"^===== PDF_PAGE (\d+) =====\s*$", re.MULTILINE)
DIFFICULTY = re.compile(r"\b(EASY|MEDIUM|HARD)\b", re.IGNORECASE)
PYQ = re.compile(r"\bPYQ\s*(\d{4})?\b", re.IGNORECASE)
OPTION = re.compile(r"^([1-4])(?:\s*[.)]|\s+)\s*(\S.*)$")


def parse_page_candidate(page_text: str) -> dict[str, str]:
    lines = [line.strip() for line in page_text.splitlines() if line.strip()]
    label_index = next(
        (index for index, line in enumerate(lines) if DIFFICULTY.search(line)), -1
    )
    content = lines[label_index + 1 :] if label_index >= 0 else lines
    solution_index = next(
        (index for index, line in enumerate(content) if line.casefold() == "solution"),
        len(content),
    )
    question_and_options = content[:solution_index]
    option_indexes = [
        index for index, line in enumerate(question_and_options) if OPTION.match(line)
    ]
    parsed_options: dict[str, str] = {}
    question_lines = question_and_options[: option_indexes[0]] if option_indexes else question_and_options
    if option_indexes:
        for position, option_index in enumerate(option_indexes):
            match = OPTION.match(question_and_options[option_index])
            if match is None:
                continue
            label = chr(ord("A") + int(match.group(1)) - 1)
            end = option_indexes[position + 1] if position + 1 < len(option_indexes) else len(question_and_options)
            value = [match.group(2)]
            value.extend(question_and_options[option_index + 1 : end])
            parsed_options[label] = " ".join(value).strip()

    explanation = " ".join(content[solution_index + 1 :]).strip() if solution_index < len(content) else ""
    answer_match = re.search(
        r"(?:hence,?\s*)?(?:the\s+)?correct answer is\s*[\"']?(.+?)[\"'.]*(?:$)",
        explanation,
        re.IGNORECASE,
    )
    correct_option = ""
    if answer_match:
        answer_phrase = re.sub(r"[^a-z0-9]+", " ", answer_match.group(1).casefold()).strip()
        for label, value in parsed_options.items():
            option_phrase = re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()
            if answer_phrase and (answer_phrase in option_phrase or option_phrase in answer_phrase):
                correct_option = label
                break

    return {
        "question_text_ocr": " ".join(question_lines).strip(),
        "option_a_ocr": parsed_options.get("A", ""),
        "option_b_ocr": parsed_options.get("B", ""),
        "option_c_ocr": parsed_options.get("C", ""),
        "option_d_ocr": parsed_options.get("D", ""),
        "correct_option_ocr": correct_option,
        "explanation_ocr": explanation,
        "candidate_completeness": (
            "FOUR_OPTIONS_AND_TEXT" if len(parsed_options) == 4 and question_lines else "PARTIAL_OR_UNCERTAIN"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("transcript_dir", type=Path)
    parser.add_argument("output_csv", type=Path)
    parser.add_argument(
        "--decisions-csv",
        type=Path,
        help="Optional reviewed decisions CSV with source_pdf, source_page, chapter_slug, review_status, review_note",
    )
    args = parser.parse_args()
    transcripts = sorted(args.transcript_dir.glob("*.txt"))
    if not transcripts:
        parser.error(f"No OCR transcripts found in {args.transcript_dir}")
    decisions_path = args.decisions_csv or args.output_csv.with_name(
        "SCIENCE_REVIEW_DECISIONS.csv"
    )
    decisions = {}
    if decisions_path.exists():
        with decisions_path.open(encoding="utf-8-sig", newline="") as stream:
            for decision in csv.DictReader(stream):
                decisions[(decision["source_pdf"], str(decision["source_page"]))] = decision

    fields = [
        "source_pdf",
        "source_page",
        "subject_slug",
        "subcategory_slug",
        "chapter_slug",
        "difficulty_ocr",
        "pyq_label_ocr",
        "pyq_year_ocr",
        "question_text_ocr",
        "option_a_ocr",
        "option_b_ocr",
        "option_c_ocr",
        "option_d_ocr",
        "correct_option_ocr",
        "explanation_ocr",
        "candidate_completeness",
        "raw_ocr_text",
        "review_status",
        "review_note",
    ]
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    row_count = 0
    with args.output_csv.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for transcript in transcripts:
            raw = transcript.read_text(encoding="utf-8")
            source_match = re.search(r"^SOURCE_PDF: (.+)$", raw, re.MULTILINE)
            source_pdf = source_match.group(1) if source_match else transcript.name
            markers = list(PAGE_MARKER.finditer(raw))
            for index, marker in enumerate(markers):
                page_number = int(marker.group(1))
                if page_number == 1:
                    continue  # The first page is the course/lecture listing.
                end = markers[index + 1].start() if index + 1 < len(markers) else len(raw)
                page_text = raw[marker.end() : end].strip()
                difficulty_match = DIFFICULTY.search(page_text)
                pyq_match = PYQ.search(page_text)
                if pyq_match:
                    label = "PYQ"
                    year = pyq_match.group(1) or ""
                else:
                    label = "NO_PYQ_LABEL_DETECTED"
                    year = ""
                decision = decisions.get((source_pdf, str(page_number)), {})
                candidate = parse_page_candidate(page_text)
                writer.writerow(
                    {
                        "source_pdf": source_pdf,
                        "source_page": page_number,
                        "subject_slug": "gk-gs",
                        "subcategory_slug": "science",
                        "chapter_slug": decision.get("chapter_slug", ""),
                        "difficulty_ocr": difficulty_match.group(1).upper()
                        if difficulty_match
                        else "",
                        "pyq_label_ocr": label,
                        "pyq_year_ocr": year,
                        **candidate,
                        "raw_ocr_text": page_text,
                        "review_status": decision.get("review_status", "NEEDS_REVIEW"),
                        "review_note": decision.get("review_note") or (
                            "OCR text is a transcription aid only; verify the page image, "
                            "all options, marked answer, explanation, difficulty/PYQ label, "
                            "and question-level chapter mapping before import."
                        ),
                    }
                )
                row_count += 1
    print(f"Wrote {row_count} page-level review rows to {args.output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
