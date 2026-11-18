"""Regression coverage for the source-verified Inequality import batch."""

import json
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import Chapter, Exam, Question, Subject
from app.services.question_import_service import import_questions


PAYLOAD = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "imports"
    / "reasoning"
    / "inequality"
    / "inequality_verified_import.json"
)


def test_verified_inequality_batch_imports_traceable_questions(db_session: Session):
    records = json.loads(PAYLOAD.read_text(encoding="utf-8"))["questions"]
    assert len(records) == 27
    assert all(record["exam_slug"] == "banking-clerk" for record in records)
    assert all(record["subject_slug"] == "reasoning" for record in records)
    assert all(record["chapter_slug"] == "inequality" for record in records)
    assert all(record["is_pyq"] is False for record in records)
    assert all(record["source"].startswith("Inequality ") for record in records)
    assert len({record["question_text"].casefold() for record in records}) == 27

    exam = Exam(name="Banking Clerk", slug="banking-clerk", is_active=True)
    db_session.add(exam)
    db_session.flush()
    subject = Subject(exam_id=exam.id, name="Reasoning", slug="reasoning", is_active=True)
    db_session.add(subject)
    db_session.flush()
    chapter = Chapter(
        subject_id=subject.id,
        name="Inequality",
        slug="inequality",
        is_active=True,
    )
    db_session.add(chapter)
    db_session.commit()

    data = PAYLOAD.read_bytes()
    preview = import_questions(
        db_session, data, "application/json", PAYLOAD.name, dry_run=True,
    )
    assert not preview.aborted
    assert preview.total_records == preview.would_import == 27
    assert preview.duplicates == preview.rejected == 0
    assert preview.errors == []

    imported = import_questions(
        db_session, data, "application/json", PAYLOAD.name, dry_run=False,
    )
    assert imported.imported == 27
    assert imported.duplicates == imported.rejected == 0

    questions = db_session.scalars(
        select(Question)
        .options(joinedload(Question.options))
        .where(Question.chapter_id == chapter.id)
    ).unique().all()
    assert len(questions) == 27
    for question in questions:
        assert question.explanation
        assert question.source.startswith("Inequality ")
        assert len(question.options) in (4, 5)
        assert sum(option.is_correct for option in question.options) == 1

    replay = import_questions(
        db_session, data, "application/json", PAYLOAD.name, dry_run=True,
    )
    assert not replay.aborted
    assert replay.would_import == 0
    assert replay.duplicates == 27
