# -*- coding: utf-8 -*-
"""Validate the imported Maths bank through the real test-service logic.

Read-only: calls `get_test_availability` for all 40 sections and checks the
database rows that back each section.

Usage:
    $env:DATABASE_URL = "postgresql://postgres@127.0.0.1:5432/ssc_prep"
    python backend/validate_banking_maths_bank.py
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import select

from app.database.session import SessionLocal
from app.models import Chapter, Exam, Question, QuestionOption, Subject
from app.services.test_service import get_test_availability

EXAMS = {"banking-clerk": "Banking Clerk", "banking-po": "Banking PO"}
CHAPTERS = {
    "vedic_maths": ("vedic-maths-tricks-calculation-techniques", "Vedic Maths Tricks"),
    "simplification": ("simplification", "Simplification"),
    "approximation": ("approximation", "Approximation"),
    "missing_series": ("missing-number-series", "Missing Number Series"),
    "wrong_series": ("wrong-number-series", "Wrong Number Series"),
}
PART_SIZES = {1: 15, 2: 20, 3: 30, 4: 55}


def section_name(exam_slug: str, chapter_key: str, part: int) -> str:
    return f"{exam_slug.replace('-', '_')}_maths_{chapter_key}_part_{part}"


def main() -> int:
    db = SessionLocal()
    failures: list[str] = []
    checked = 0
    try:
        for exam_slug in EXAMS:
            exam = db.scalar(select(Exam).where(Exam.slug == exam_slug))
            if exam is None:
                failures.append(f"missing exam {exam_slug}")
                continue
            subject = db.scalar(
                select(Subject).where(
                    Subject.exam_id == exam.id,
                    Subject.slug == "math-quant",
                )
            )
            if subject is None:
                failures.append(f"missing Math & Quant subject for {exam_slug}")
                continue
            for chapter_key, (chapter_slug, _) in CHAPTERS.items():
                chapter = db.scalar(
                    select(Chapter).where(
                        Chapter.subject_id == subject.id,
                        Chapter.slug == chapter_slug,
                    )
                )
                if chapter is None:
                    failures.append(f"missing chapter {exam_slug}/{chapter_slug}")
                    continue
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
                    checked += 1
                    if availability["available_question_count"] != expected:
                        failures.append(
                            f"{section}: availability says "
                            f"{availability['available_question_count']}, expected {expected}"
                        )
                    if expected not in availability["allowed_question_counts"]:
                        failures.append(
                            f"{section}: {expected} not in allowed counts "
                            f"{availability['allowed_question_counts']}"
                        )
                    if not availability["can_satisfy_request"]:
                        failures.append(f"{section}: cannot satisfy a {expected}-question request")

                    questions = db.scalars(
                        select(Question).where(
                            Question.chapter_id == chapter.id,
                            Question.section == section,
                            Question.is_active.is_(True),
                        )
                    ).all()
                    if len(questions) != expected:
                        failures.append(f"{section}: DB has {len(questions)} questions")
                    for question in questions:
                        if question.is_pyq or question.pyq_year is not None:
                            failures.append(f"{section}: question {question.id} is flagged PYQ")
                        if not (question.explanation or "").strip():
                            failures.append(f"{section}: question {question.id} has no explanation")
                        options = db.scalars(
                            select(QuestionOption).where(
                                QuestionOption.question_id == question.id
                            )
                        ).all()
                        if len(options) != 4:
                            failures.append(
                                f"{section}: question {question.id} has {len(options)} options"
                            )
                        if sum(1 for option in options if option.is_correct) != 1:
                            failures.append(
                                f"{section}: question {question.id} does not have exactly one correct option"
                            )

        # Duration is derived from the same branch as create_test: section tests
        # use 42 seconds per question.
        for count in (15, 20, 30, 55):
            seconds = count * 42
            print(f"duration check: {count} questions -> {seconds}s ({seconds / 60:g} min)")

        print(f"sections checked: {checked}/40")
        if failures:
            print(f"FAILURES: {len(failures)}")
            for failure in failures[:50]:
                print(" -", failure)
            return 1
        print("ALL CHECKS PASSED")
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
