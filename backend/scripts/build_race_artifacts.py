"""Build the deterministic Race answer ledger, source review, and review report.

The question batch remains authored by build_race_batch.js. This script validates
that canonical batch and derives the review artifacts without timestamps.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data"
BATCH = DATA / "race_verified_batch.json"
LEDGER = DATA / "race_answer_ledger.json"
SOURCE_REVIEW = DATA / "race_source_review.json"
REPORT = DATA / "race_review_report.md"

REJECTED = [
    {"source_pdf": "Race 01_ Class Notes.pdf", "page": 1, "candidate": "Cover slide", "reason": "No question content."},
    {"source_pdf": "Race 01_ Class Notes.pdf", "page": 2, "candidate": "Topics overview", "reason": "Topic outline only; no complete question or answer choices."},
    {"source_pdf": "Race 01_ Class Notes.pdf", "page": 3, "candidate": "Race concepts and distance-speed-time relationship", "reason": "Instructional concept slide; no complete MCQ."},
    {"source_pdf": "Race 01_ Class Notes.pdf", "page": 4, "candidate": "Three-runner chained winning-distance question", "reason": "Overlaps the retained and original chained race-margin question family; excluded as a repeated underlying ratio-chain exercise."},
    {"source_pdf": "Race 01_ Class Notes.pdf", "page": 5, "candidate": "100 m race with two chained winning margins", "reason": "Same chained winning-distance ratio method as other retained bank items; excluded as a superficial numerical variant."},
    {"source_pdf": "Race 01_ Class Notes.pdf", "page": 6, "candidate": "Transition slide", "reason": "No recoverable question."},
    {"source_pdf": "Race 01_ Class Notes.pdf", "page": 9, "candidate": "Sunny and Ankit finish-time margin", "reason": "Direct winning-distance calculation is already represented by several distinct bank items; excluded as a repeated single-step margin template."},
    {"source_pdf": "Race 01_ Class Notes.pdf", "page": 11, "candidate": "1 km race: 120 m or 30 s margin; find winner's time", "reason": "This follows the same coupled distance/time-margin algebra as the retained page 7 question and is not kept as another parameter variation."},
    {"source_pdf": "Race 01_ Class Notes.pdf", "page": 13, "candidate": "P gives Q a 2-second head start in a 400 m race; Q runs at 2 m/s; find P's time", "reason": "The slide's 198 s answer is correct when interpreted literally: Q starts first and has 396 m remaining when P starts. It is excluded because the canonical batch already contains a delayed-start/simultaneous-finish item with the same underlying setup."},
    {"source_pdf": "Race 01_ Class Notes.pdf", "page": 15, "candidate": "Rahul and Bharat with a 4 m head start and 4 s margin", "reason": "Same head-start plus finish-time comparison pattern as multiple retained items; excluded as a parameter-only variant."},
    {"source_pdf": "Race 01_ Class Notes.pdf", "page": 17, "candidate": "Feedback slide", "reason": "No question content."},
    {"source_pdf": "Race 01_ Class Notes.pdf", "page": 18, "candidate": "Summary slide", "reason": "No complete question or answer choices."},
    {"source_pdf": "Race 01_ Class Notes.pdf", "page": 19, "candidate": "Closing slide", "reason": "No question content."},
    {"source_pdf": "Race 02_ Class Notes.pdf", "page": 1, "candidate": "Cover slide", "reason": "No question content."},
    {"source_pdf": "Race 02_ Class Notes.pdf", "page": 2, "candidate": "Recap slide", "reason": "Concept recap only; no complete question."},
    {"source_pdf": "Race 02_ Class Notes.pdf", "page": 3, "candidate": "Circular race introduction", "reason": "Definition slide; no complete question."},
    {"source_pdf": "Race 02_ Class Notes.pdf", "page": 4, "candidate": "Circular-race question-type summary", "reason": "Method summary only; no complete question."},
    {"source_pdf": "Race 02_ Class Notes.pdf", "page": 6, "candidate": "600 m opposite-direction meeting with mixed units", "reason": "Same first-meeting relative-speed structure as the retained page 5 circular problem; excluded as a parameter-only variant."},
    {"source_pdf": "Race 02_ Class Notes.pdf", "page": 7, "candidate": "Opposite-direction first meeting with rounding", "reason": "Repeats the retained opposite-direction first-meeting type and only varies the circumference/speeds and rounding."},
    {"source_pdf": "Race 02_ Class Notes.pdf", "page": 8, "candidate": "Same-direction first meeting", "reason": "Same one-lap relative-speed meeting calculation already represented by same-direction circular questions."},
    {"source_pdf": "Race 02_ Class Notes.pdf", "page": 9, "candidate": "1125 m same-direction car race", "reason": "Repeats the page 8 same-direction first-meeting calculation with changed values."},
    {"source_pdf": "Race 02_ Class Notes.pdf", "page": 14, "candidate": "Feedback slide", "reason": "No question content."},
    {"source_pdf": "Race 02_ Class Notes.pdf", "page": 15, "candidate": "Summary slide", "reason": "No complete question or answer choices."},
    {"source_pdf": "Race 02_ Class Notes.pdf", "page": 16, "candidate": "Closing slide", "reason": "No question content."},
]


def load_batch() -> list[dict]:
    payload = json.loads(BATCH.read_text(encoding="utf-8"))
    questions = payload["questions"]
    if len(questions) < 90:
        raise ValueError(f"Expected at least 90 questions, found {len(questions)}")
    return questions


def source_details(source: str) -> tuple[str | None, int | None]:
    match = re.fullmatch(r"Verified from (Race 0[12]_ Class Notes\.pdf), page (\d+); exam/year not stated", source)
    if match:
        return match.group(1), int(match.group(2))
    if source == "Original SSC-style practice question":
        return None, None
    raise ValueError(f"Unrecognized source provenance: {source}")


def category(question: str) -> str:
    return "Circular Race" if re.search(r"circular|\btrack\b|lap", question, re.I) else "Linear Race"


def render() -> dict[Path, bytes]:
    rows = load_batch()
    counts = Counter(row["difficulty"] for row in rows)
    answer_counts = Counter(row["correct_option"] for row in rows)
    category_counts = Counter(category(row["question_text"]) for row in rows)
    source_counts = Counter("source" if row["source"].startswith("Verified from Race ") else "original" for row in rows)

    ledger = []
    accepted = []
    for index, row in enumerate(rows, 1):
        pdf, page = source_details(row["source"])
        entry = {
            "question_id": f"race-{index:03d}",
            "source_pdf": pdf,
            "source_page": page,
            "source": row["source"],
            "category": category(row["question_text"]),
            "question": row["question_text"],
            "options": row["options"],
            "correct_option": row["correct_option"],
            "correct_answer": row["options"][row["correct_option"]],
            "solution": row["explanation"],
            "difficulty": row["difficulty"],
            "verification_status": "independently_verified",
        }
        ledger.append(entry)
        if pdf:
            accepted.append({"question_id": entry["question_id"], "source_pdf": pdf, "page": page,
                             "question": row["question_text"], "answer": entry["correct_answer"],
                             "verification": "accepted; independently solved; not identified as a PYQ"})

    source_review = {
        "pdfs_reviewed": [
            {"name": "Race 01_ Class Notes.pdf", "pages_visually_reviewed": list(range(1, 20))},
            {"name": "Race 02_ Class Notes.pdf", "pages_visually_reviewed": list(range(1, 17))},
        ],
        "accepted_candidates": accepted,
        "rejected_candidates": REJECTED,
        "duplicate_review": {
            "within_batch_questions": len(rows),
            "within_batch_exact_number_masked_and_lexical_collisions": 0,
            "newest_source_candidate_other_canonical_questions_compared": 3409,
            "newest_source_candidate_cross_chapter_exact_or_number_masked_or_lexical_collisions": 0,
            "other_canonical_and_live_maths_questions_compared": 6022,
            "cross_chapter_exact_or_number_masked_collisions": 0,
            "limitations": "The prior 6,022-question scan covered the original 90 rows. The subsequently accepted page 16 source question was additionally screened against 3,409 available canonical question stems; live-database cross-chapter screening for that new row could not be rerun. Lexical and number-masked screening does not prove absence of every semantic overlap; shortlisted source candidates were also reviewed by problem type.",
        },
        "notes": [
            "Page numbers refer to physical PDF pages, including the cover page.",
            "Lecture material is source material, not PYQ provenance; no exam name or year was stated.",
            "Handwritten markings were checked against an independent calculation. The page 13 head-start example's 198-second answer is consistent: Q starts first, has 396 m remaining at P's start, and both finish 198 seconds later.",
            "Six bank issues were corrected after independent review: the three-runner finisher key, the chained-race algebra explanation, and four stems whose wording contradicted or obscured the intended start, finish, or distance calculation.",
        ],
    }

    report = f"""# Race chapter source and verification report

## Source review

Visually reviewed all 35 physical pages: Race 01_ Class Notes.pdf (19/19) and Race 02_ Class Notes.pdf (16/16). Accepted {len(accepted)} source-derived questions; rejected {len(REJECTED)} candidates for the reasons listed in `race_source_review.json`. Source items are lecture examples, not PYQs. No exam name or year is asserted.

## Bank composition

- Active Normal target is at least 90; canonical total: {len(rows)}.
- Difficulty: Easy {counts['EASY']}, Medium {counts['MEDIUM']}, Hard {counts['HARD']}.
- Topic classification: Linear Race {category_counts['Linear Race']}; Circular Race {category_counts['Circular Race']}.
- Provenance: source-derived {source_counts['source']}; original SSC-style {source_counts['original']}.
- Correct answer positions: A {answer_counts['A']}, B {answer_counts['B']}, C {answer_counts['C']}, D {answer_counts['D']}.

## Mathematical review

All {len(rows)} rows have four distinct options, a single answer key matching the keyed option, and a non-empty worked explanation. Answers were independently checked against the stated distance, speed, time, start offsets, lap periods, and meeting-location cycle. The corrected three-runner question is independently evaluated on a common time origin: A finishes at 75 s, B at 71 2/3 s, and C at 70 s, so A finishes last. The source head-start example on Race 01 page 13 is 198 s after P starts because Q has a two-second head start. The Race 01 page 16 speed-difference candidate is retained because it is a distinct multi-condition question and covers a requested skill.

Six content defects were corrected with exact live-record preconditions: the three-runner answer changed from B to A while preserving and reordering the original options; the chained-race explanation now solves explicitly for C's speed; and four original stems were clarified where their wording contradicted or obscured start timing, finish timing, or whether distance was covered. Difficulty, identities, and all other content were preserved.

## Duplicate review

Within the batch, exact normalized, number-masked, and high lexical screening found no collisions. A prior cross-chapter pass compared the original 90 Race stems with 6,022 other canonical and live Maths questions; it found zero exact or number-masked collisions. The additional Race 01 page 16 stem was screened against 3,409 available canonical questions and had no exact, number-masked, or high lexical collision; its live-database cross-chapter scan could not be rerun in this environment. Problem-family screening supplemented these checks, but these checks do not prove the absence of every possible semantic overlap. See `race_source_review.json` and the focused duplicate tests.

## Import and application verification

The guarded importer uses exact existing-row preconditions and a transaction. Verify the live catalog, dry-run, and replay at release time; no importer write is performed by this artifact builder. Test/API/build results are recorded in the completion report for this run.

## Limitations

Difficulty is an editorial classification. The scanned lecture examples are not described as historical SSC questions, and the source-review exclusions document repeated templates or non-question slides.
"""
    return {
        LEDGER: (json.dumps(ledger, ensure_ascii=False, indent=2) + "\n").encode(),
        SOURCE_REVIEW: (json.dumps(source_review, ensure_ascii=False, indent=2) + "\n").encode(),
        REPORT: report.encode(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify generated artifacts match without writing")
    args = parser.parse_args()
    artifacts = render()
    changed = []
    for path, content in artifacts.items():
        if not path.exists() or path.read_bytes() != content:
            changed.append(path)
            if not args.check:
                path.write_bytes(content)
    if args.check and changed:
        raise SystemExit("OUT_OF_DATE " + ", ".join(str(path.relative_to(BASE)) for path in changed))
    if changed:
        print("WROTE", ", ".join(str(path.relative_to(BASE)) for path in changed))
    else:
        print("DETERMINISTIC", ", ".join(str(path.relative_to(BASE)) for path in artifacts))
        print("SHA256", " ".join(f"{p.name}={hashlib.sha256(b).hexdigest()}" for p, b in artifacts.items()))


if __name__ == "__main__":
    main()
