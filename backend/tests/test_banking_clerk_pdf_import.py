"""Regression coverage for the Banking Clerk PDF payload and five-choice import."""

import json
from collections import Counter
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import Chapter, Exam, Question, QuestionOption, Subject
from app.services.question_import_service import import_questions


PAYLOAD = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "imports"
    / "banking"
    / "banking_clerk_reasoning_26_december.json"
)


def test_banking_clerk_pdf_payload_imports_five_options_idempotently(db_session: Session):
    records = json.loads(PAYLOAD.read_text(encoding="utf-8"))["questions"]
    assert len(records) == 35
    assert all(set(record["options"]) == set("ABCDE") for record in records)
    assert all(record["exam_slug"] == "banking-clerk" for record in records)
    assert all(record["subject_slug"] == "reasoning" for record in records)
    assert all(record["is_pyq"] is False and record["pyq_year"] is None for record in records)
    assert Counter(record["chapter_slug"] for record in records) == {
        "coding-decoding": 5,
        "tabular-puzzles": 5,
        "analytical-reasoning-mains": 5,
        "linear-arrangements": 5,
        "syllogism": 5,
        "circular-arrangements": 5,
        "alphabets": 3,
        "blood-relations": 2,
    }

    exam = Exam(name="Banking Clerk", slug="banking-clerk", is_active=True)
    db_session.add(exam)
    db_session.flush()
    subject = Subject(exam_id=exam.id, name="Reasoning", slug="reasoning", is_active=True)
    db_session.add(subject)
    db_session.flush()
    chapter_slugs = sorted({record["chapter_slug"] for record in records})
    db_session.add_all(
        Chapter(subject_id=subject.id, name=slug.replace("-", " ").title(), slug=slug, is_active=True)
        for slug in chapter_slugs
    )
    db_session.commit()

    data = PAYLOAD.read_bytes()
    preview = import_questions(
        db_session, data, "application/json", PAYLOAD.name, dry_run=True,
    )
    assert not preview.aborted
    assert preview.total_records == preview.would_import == 35
    assert preview.duplicates == 0
    assert preview.errors == []

    imported = import_questions(
        db_session, data, "application/json", PAYLOAD.name, dry_run=False,
    )
    assert imported.imported == 35
    assert imported.duplicates == 0

    questions = db_session.scalars(
        select(Question)
        .options(joinedload(Question.options))
        .join(Chapter, Question.chapter_id == Chapter.id)
        .where(Chapter.slug.in_(chapter_slugs))
    ).unique().all()
    assert len(questions) == 35
    assert all([option.option_key for option in question.options] == list("ABCDE") for question in questions)
    assert all(sum(option.is_correct for option in question.options) == 1 for question in questions)
    assert sum(not question.is_active for question in questions) == 4

    replay = import_questions(
        db_session, data, "application/json", PAYLOAD.name, dry_run=True,
    )
    assert not replay.aborted
    assert replay.would_import == 0
    assert replay.duplicates == 35
