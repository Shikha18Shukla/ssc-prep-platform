from __future__ import annotations

import json
import unicodedata
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models import Chapter, Exam, Question, Subject
from app.services.question_import_service import import_questions


BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "imports" / "reasoning" / "order-and-ranking" / "order_and_ranking_01_03_verified.json"
REPORT = BASE / "data" / "imports" / "reasoning" / "order-and-ranking" / "order_and_ranking_01_03_review_report.md"


def test_order_ranking_batch_is_verified_and_source_traceable(db_session):
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    assert len(rows) == 30
    assert all((row["exam_slug"], row["subject_slug"], row["chapter_slug"]) == (
        "banking-clerk", "reasoning", "order-and-ranking"
    ) for row in rows)
    assert all(row["is_pyq"] is False for row in rows)
    assert len({" ".join(unicodedata.normalize("NFKC", row["question_text"]).casefold().split()) for row in rows}) == 30
    for row in rows:
        assert row["source"].startswith("Order and Ranking ")
        assert "lecture 0" in row["source"]
        assert "page" in row["source"]
        assert row["explanation"].strip()
        assert set(row["options"]) == set("ABCDE")
        assert row["correct_option"] in row["options"]
        assert row["difficulty"] in {"EASY", "MEDIUM", "HARD"}

    report = REPORT.read_text(encoding="utf-8")
    assert "physical page 13" in report
    assert "followers of S and T" in report

    exam = Exam(name="Banking Clerk", slug="banking-clerk", is_active=True)
    db_session.add(exam)
    db_session.flush()
    subject = Subject(exam_id=exam.id, name="Reasoning", slug="reasoning", is_active=True)
    db_session.add(subject)
    db_session.flush()
    chapter = Chapter(subject_id=subject.id, name="Order and Ranking", slug="order-and-ranking", is_active=True)
    db_session.add(chapter)
    db_session.commit()

    data = BATCH.read_bytes()
    preview = import_questions(db_session, data, "application/json", BATCH.name, dry_run=True)
    assert not preview.aborted and preview.errors == []
    assert preview.total_records == preview.would_import == 30
    assert preview.duplicates == preview.rejected == 0

    imported = import_questions(db_session, data, "application/json", BATCH.name, dry_run=False)
    assert not imported.aborted and imported.errors == []
    assert imported.imported == 30
    assert imported.duplicates == imported.rejected == 0

    questions = db_session.scalars(
        select(Question).options(joinedload(Question.options)).where(Question.chapter_id == chapter.id)
    ).unique().all()
    assert len(questions) == 30
    for question in questions:
        assert question.explanation
        assert question.source.startswith("Order and Ranking ")
        assert len(question.options) == 5
        assert {option.option_key for option in question.options} == set("ABCDE")
        assert sum(option.is_correct for option in question.options) == 1

    replay = import_questions(db_session, data, "application/json", BATCH.name, dry_run=True)
    assert not replay.aborted and replay.errors == []
    assert replay.duplicates == 30
    assert replay.would_import == 0
