# -*- coding: utf-8 -*-
"""Check get_test_availability for all 48 Set 7 sections on the scratch copy.

Reads DATABASE_URL and refuses anything except the local scratch database.
Writes a report under reports/.  The live database is never written.
"""

from __future__ import annotations

import os
import sys

from psycopg2.extensions import parse_dsn
from sqlalchemy import select

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from app.database.session import SessionLocal
from app.models import Chapter, Exam, Subject
from app.services.test_service import get_test_availability

EXPECTED_DB = "ssc_prep_scratch_maths7"
EXAMS = {"banking-clerk": "Banking Clerk", "banking-po": "Banking PO"}
CHAPTERS = {
    "mixture_alligation_mains": "mixture-and-alligation-mains",
    "mixture_alligation_data_interpretation": "mixture-and-alligation-data-interpretation",
    "ages_mains": "ages-mains",
    "ages_data_interpretation": "ages-data-interpretation",
    "partnership_mains": "partnership-mains",
    "partnership_data_interpretation": "partnership-data-interpretation",
}
PART_SIZES = {1: 15, 2: 20, 3: 30, 4: 55}
DURATIONS = {15: 630, 20: 840, 30: 1260, 55: 2310}
EXPECTED_SECTIONS = len(EXAMS) * len(CHAPTERS) * len(PART_SIZES)


def section_name(exam_slug: str, chapter_key: str, part: int) -> str:
    return f"{exam_slug.replace('-', '_')}_maths_{chapter_key}_part_{part}"


def guard() -> None:
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise SystemExit("DATABASE_URL is required")
    dsn = parse_dsn(url)
    if (dsn.get("host") or "").lower() not in {"127.0.0.1", "localhost", "::1"}:
        raise SystemExit("refusing non-local host")
    if dsn.get("dbname") != EXPECTED_DB:
        raise SystemExit(f"refusing database {dsn.get('dbname')!r}; expected the scratch database")


def main() -> int:
    guard()
    db = SessionLocal()
    failures: list[str] = []
    lines = [
        "# Banking Maths Set 7 - Availability Verification",
        "",
        "Executed against a restored local copy of the imported bank with the real",
        "`get_test_availability` service; the live database was never written.",
        "",
        "| Section | Available | Allowed request | Can satisfy | Expected seconds |",
        "| --- | ---: | ---: | --- | ---: |",
    ]
    try:
        checked = 0
        for exam_slug in EXAMS:
            exam = db.scalar(select(Exam).where(Exam.slug == exam_slug))
            if exam is None:
                raise SystemExit(f"missing exam {exam_slug}")
            subject = db.scalar(
                select(Subject).where(Subject.exam_id == exam.id, Subject.slug == "math-quant")
            )
            if subject is None:
                raise SystemExit(f"missing subject {exam_slug}/math-quant")
            for chapter_key, chapter_slug in CHAPTERS.items():
                chapter = db.scalar(
                    select(Chapter).where(
                        Chapter.subject_id == subject.id, Chapter.slug == chapter_slug
                    )
                )
                if chapter is None:
                    raise SystemExit(f"missing chapter {exam_slug}/{chapter_slug}")
                for part, expected in PART_SIZES.items():
                    section = section_name(exam_slug, chapter_key, part)
                    availability = get_test_availability(
                        db,
                        exam.id,
                        subject.id,
                        "CHAPTER_WISE",
                        chapter.id,
                        None,
                        None,
                        question_count=None,
                        chapter_ids=None,
                        section_filter=section,
                    )
                    available = availability["available_question_count"]
                    allowed = expected in availability["allowed_question_counts"]
                    can_satisfy = bool(availability["can_satisfy_request"])
                    lines.append(
                        f"| {section} | {available} | {allowed} | {can_satisfy} | "
                        f"{DURATIONS[expected]} |"
                    )
                    checked += 1
                    if available != expected:
                        failures.append(f"{section}: available {available}, expected {expected}")
                    if not allowed:
                        failures.append(f"{section}: {expected} is not an allowed question count")
                    if not can_satisfy:
                        failures.append(f"{section}: cannot satisfy a {expected}-question request")
        lines += [
            "",
            f"- Sections checked: {checked}/{EXPECTED_SECTIONS}",
            "- Duration rule: 42 seconds per question "
            "(630 / 840 / 1260 / 2310 seconds)",
            "",
        ]
        if checked != EXPECTED_SECTIONS:
            failures.append(f"checked {checked} sections, expected {EXPECTED_SECTIONS}")
        if failures:
            lines += [f"## Failures ({len(failures)})", ""] + [f"- {f}" for f in failures] + [""]
        else:
            lines += ["## Result", "", "ALL CHECKS PASSED", ""]
    finally:
        db.close()

    path = os.path.join(ROOT, "reports", "banking_maths_set7_availability_scratch_report.md")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    print(f"wrote {path}")
    if failures:
        for failure in failures:
            print(" -", failure)
        return 1
    print(f"ALL CHECKS PASSED ({checked} sections)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
