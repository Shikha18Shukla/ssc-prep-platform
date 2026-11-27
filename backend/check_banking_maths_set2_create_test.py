# -*- coding: utf-8 -*-
"""Exercise create_test for all 40 batch-2 sections on a scratch DB.

Reads DATABASE_URL and refuses anything except the local scratch database.
Writes a report under reports/.  The scratch database must be created from a
pg_dump of ssc_prep first; this script never connects to ssc_prep.
"""

from __future__ import annotations

import os
import sys
import uuid
from collections import Counter

from psycopg2.extensions import parse_dsn
from sqlalchemy import func, select

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from app.database.session import SessionLocal
from app.models import Chapter, Exam, Question, Subject, TestAttempt, TestQuestion, User
from app.schemas.tests import TestCreate
from app.services.test_service import create_test

EXPECTED_DB = "ssc_prep_scratch_maths2"
EXAMS = {"banking-clerk": "Banking Clerk", "banking-po": "Banking PO"}
CHAPTERS = {
    "quadratic_equations": ("quadratic-equations", "Quadratic Equations"),
    "number_system": ("number-system", "Number System"),
    "percentage": ("percentage", "Percentage"),
    "ratio_proportion": ("ratio-and-proportion", "Ratio and Proportion"),
    "profit_loss_discount": ("profit-loss-and-discount", "Profit, Loss and Discount"),
}
PART_SIZES = {1: (15, 630), 2: (20, 840), 3: (30, 1260), 4: (55, 2310)}


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
        raise SystemExit(f"refusing database {dsn.get('dbname')!r}; expected {EXPECTED_DB}")


def main() -> int:
    guard()
    db = SessionLocal()
    failures: list[str] = []
    lines = [
        "# Banking Maths Batch 2 - create_test verification",
        "",
        "Executed against a pg_dump/pg_restore copy of ssc_prep "
        f"(`{EXPECTED_DB}`), never against the live database.",
        "",
        "| Section | Questions | Expected seconds | Actual seconds | Selected in section |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    try:
        user = db.scalar(select(User).where(User.is_active.is_(True)).limit(1))
        if user is None:
            raise SystemExit("no active user in scratch database")
        attempts_before = db.scalar(select(func.count()).select_from(TestAttempt))
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
            for chapter_key, (chapter_slug, _) in CHAPTERS.items():
                chapter = db.scalar(
                    select(Chapter).where(
                        Chapter.subject_id == subject.id, Chapter.slug == chapter_slug
                    )
                )
                if chapter is None:
                    raise SystemExit(f"missing chapter {exam_slug}/{chapter_slug}")
                for part, (count, expected_seconds) in PART_SIZES.items():
                    section = section_name(exam_slug, chapter_key, part)
                    payload = TestCreate(
                        exam_id=exam.id,
                        subject_id=subject.id,
                        test_type="CHAPTER_WISE",
                        question_count=count,
                        section_filter=section,
                    )
                    attempt = create_test(db, user.id, payload)
                    db.refresh(attempt)
                    selected_ids = [
                        row[0]
                        for row in db.execute(
                            select(Question.id).join(
                                TestQuestion, TestQuestion.question_id == Question.id
                            ).where(
                                TestQuestion.test_attempt_id == attempt.id,
                                Question.section == section,
                            )
                        ).all()
                    ]
                    in_section = len(selected_ids)
                    lines.append(
                        f"| {section} | {attempt.question_count} | {expected_seconds} | "
                        f"{attempt.duration_seconds} | {in_section}/{count} |"
                    )
                    checked += 1
                    if attempt.question_count != count:
                        failures.append(f"{section}: question_count {attempt.question_count}")
                    if attempt.duration_seconds != expected_seconds:
                        failures.append(
                            f"{section}: duration {attempt.duration_seconds}, expected {expected_seconds}"
                        )
                    if in_section != count or len(set(selected_ids)) != count:
                        failures.append(
                            f"{section}: {in_section} distinct selected questions from the section"
                        )
        attempts_after = db.scalar(select(func.count()).select_from(TestAttempt))
        created = attempts_after - attempts_before
        lines += [
            "",
            f"- Sections exercised: {checked}/40",
            f"- Attempts created on scratch DB: {created}",
            "- Duration rule verified: 42 seconds per question "
            "(630 / 840 / 1260 / 2310 seconds)",
            "",
        ]
        if created != checked:
            failures.append(f"created {created} attempts for {checked} sections")
        if failures:
            lines += [f"## Failures ({len(failures)})", ""] + [f"- {f}" for f in failures] + [""]
        else:
            lines += ["## Result", "", "ALL CHECKS PASSED", ""]
    finally:
        db.close()

    path = os.path.join(ROOT, "reports", "banking_maths_set2_create_test_report.md")
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
