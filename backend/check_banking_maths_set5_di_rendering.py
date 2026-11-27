# -*- coding: utf-8 -*-
"""Validate DI and caselet rendering through the real create_test service.

Runs only against the restored local scratch database.  For every Data
Interpretation and Caselet Data Interpretation section it creates a test, reads
the selected questions back through ``TestQuestion``, and verifies that the
rendered question carries its data inline with four distinct options and one
correct option.  No question depends on an external image, table or passage.
"""

from __future__ import annotations

import os
import re
import sys

from psycopg2.extensions import parse_dsn
from sqlalchemy import func, select

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from app.database.session import SessionLocal
from app.models import Chapter, Exam, Question, QuestionOption, Subject, TestAttempt, TestQuestion, User
from app.schemas.tests import TestCreate
from app.services.test_service import create_test

EXPECTED_DB = "ssc_prep_scratch_maths5"
CHAPTERS = {
    "data_interpretation": ("data-interpretation", 15),
    "caselet_data_interpretation": ("caselet-data-interpretation", 15),
}
PART_SIZES = {1: (15, 630), 2: (20, 840), 3: (30, 1260), 4: (55, 2310)}
EXTERNAL_REFERENCE = re.compile(
    r"\b(the|above|following)\b.*\b(table|graph|chart|passage|information|data)\b", re.I
)
NUMBER_RE = re.compile(r"\d")


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
        raise SystemExit("refusing database; expected the scratch database")


def main() -> int:
    guard()
    db = SessionLocal()
    failures: list[str] = []
    checked_sections = 0
    checked_questions = 0
    checked_options = 0
    lines = [
        "# Banking Maths Set 5 - DI and Caselet Rendering Report",
        "",
        "Executed against a restored local copy of the imported bank through the",
        "real `create_test` service; the live database was never written.",
        "",
        "| Section | Questions rendered | Inline-data questions | Options rendered | Correct options |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    try:
        user = db.scalar(select(User).where(User.is_active.is_(True)).limit(1))
        if user is None:
            raise SystemExit("no active user in scratch database")
        attempts_before = db.scalar(select(func.count()).select_from(TestAttempt))
        for exam_slug in ("banking-clerk", "banking-po"):
            exam = db.scalar(select(Exam).where(Exam.slug == exam_slug))
            if exam is None:
                raise SystemExit(f"missing exam {exam_slug}")
            subject = db.scalar(
                select(Subject).where(Subject.exam_id == exam.id, Subject.slug == "math-quant")
            )
            if subject is None:
                raise SystemExit(f"missing subject {exam_slug}/math-quant")
            for chapter_key, (chapter_slug, expected_each) in CHAPTERS.items():
                chapter = db.scalar(
                    select(Chapter).where(
                        Chapter.subject_id == subject.id, Chapter.slug == chapter_slug
                    )
                )
                if chapter is None:
                    raise SystemExit(f"missing chapter {exam_slug}/{chapter_slug}")
                for part, (count, expected_seconds) in PART_SIZES.items():
                    section = section_name(exam_slug, chapter_key, part)
                    attempt = create_test(
                        db,
                        user.id,
                        TestCreate(
                            exam_id=exam.id,
                            subject_id=subject.id,
                            test_type="CHAPTER_WISE",
                            question_count=count,
                            section_filter=section,
                        ),
                    )
                    db.refresh(attempt)
                    questions = db.scalars(
                        select(Question)
                        .join(TestQuestion, TestQuestion.question_id == Question.id)
                        .where(
                            TestQuestion.test_attempt_id == attempt.id,
                            Question.section == section,
                        )
                    ).all()
                    if len(questions) != count:
                        failures.append(f"{section}: rendered {len(questions)} questions, expected {count}")
                    if attempt.duration_seconds != expected_seconds:
                        failures.append(f"{section}: duration {attempt.duration_seconds}, expected {expected_seconds}")
                    inline = 0
                    correct_total = 0
                    section_options = 0
                    for question in questions:
                        text = question.question_text or ""
                        if EXTERNAL_REFERENCE.search(text):
                            failures.append(f"{section}/{question.id}: references external data")
                        if len(NUMBER_RE.findall(text)) < 2:
                            failures.append(f"{section}/{question.id}: data not embedded in question text")
                        else:
                            inline += 1
                        if not (question.explanation or "").strip():
                            failures.append(f"{section}/{question.id}: missing explanation")
                        options = db.scalars(
                            select(QuestionOption).where(QuestionOption.question_id == question.id)
                        ).all()
                        checked_options += len(options)
                        section_options += len(options)
                        if len(options) != 4 or len({option.option_text for option in options}) != 4:
                            failures.append(f"{section}/{question.id}: rendered options are not four distinct values")
                        correct = sum(1 for option in options if option.is_correct)
                        correct_total += correct
                        if correct != 1:
                            failures.append(f"{section}/{question.id}: rendered correct-option count is {correct}")
                        checked_questions += 1
                    lines.append(
                        f"| {section} | {len(questions)} | {inline} | {section_options} | {correct_total} |"
                    )
                    if inline != count:
                        failures.append(f"{section}: {inline}/{count} questions carry inline data")
                    checked_sections += 1
        attempts_after = db.scalar(select(func.count()).select_from(TestAttempt))
        created = attempts_after - attempts_before
        lines += [
            "",
            f"- Sections rendered: {checked_sections}/16",
            f"- Questions rendered: {checked_questions}/480",
            f"- Options rendered: {checked_options}/1920",
            f"- Attempts created on the scratch copy: {created}",
            "- Data dependency: every rendered question carries its own values; no external",
            "  image, table, graph or passage is required.",
            "",
        ]
        if created != checked_sections:
            failures.append(f"created {created} attempts for {checked_sections} sections")
        if failures:
            lines += [f"## Failures ({len(failures)})", ""] + [f"- {failure}" for failure in failures] + [""]
        else:
            lines += ["## Result", "", "ALL CHECKS PASSED", ""]
    finally:
        db.close()

    path = os.path.join(ROOT, "reports", "banking_maths_set5_di_rendering_report.md")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    print(f"wrote {path}")
    if failures:
        for failure in failures[:60]:
            print(" -", failure)
        return 1
    print(f"ALL CHECKS PASSED ({checked_sections} sections, {checked_questions} questions)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
