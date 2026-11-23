"""Regression coverage for the verified Coding Decoding lectures 01 and 02 batch."""

import json
from collections import Counter
from pathlib import Path

from sqlalchemy import func, select

from app.models import Chapter, Exam, Question, QuestionOption, Subject
from app.services.question_import_service import import_questions

BATCH = (
    Path(__file__).resolve().parents[1]
    / "data/imports/reasoning/coding-decoding/coding_decoding_01_02_verified.json"
)


def _catalog(db_session):
    exam = Exam(name="Banking Clerk", slug="banking-clerk", is_active=True)
    db_session.add(exam)
    db_session.flush()
    subject = Subject(exam_id=exam.id, name="Reasoning", slug="reasoning", is_active=True)
    db_session.add(subject)
    db_session.flush()
    chapter = Chapter(
        subject_id=subject.id,
        name="Coding Decoding",
        slug="coding-decoding",
        is_active=True,
    )
    db_session.add(chapter)
    db_session.commit()
    return chapter


def test_verified_batch_has_complete_traceable_mcqs():
    records = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    assert len(records) == 18
    for record in records:
        assert record["chapter_slug"] == "coding-decoding"
        assert "PDF page " in record["source"]
        assert record["explanation"].strip()
        assert set(record["options"]) == {"A", "B", "C", "D", "E"}
        assert record["correct_option"] in record["options"]


def test_import_dry_run_commit_and_replay_are_safe(db_session):
    chapter = _catalog(db_session)
    data = BATCH.read_bytes()

    preview = import_questions(db_session, data, "application/json", BATCH.name, True)
    assert preview.aborted is False and preview.errors == []
    assert preview.would_import == 18 and preview.duplicates == 0
    assert db_session.scalar(select(func.count(Question.id))) == 0

    result = import_questions(db_session, data, "application/json", BATCH.name, False)
    assert result.imported == 18 and result.errors == []
    questions = db_session.scalars(
        select(Question).where(Question.chapter_id == chapter.id)
    ).all()
    assert len(questions) == 18
    assert all(question.is_active and question.explanation for question in questions)
    assert all(question.source and "PDF page " in question.source for question in questions)

    options = db_session.scalars(
        select(QuestionOption).where(QuestionOption.question_id.in_([q.id for q in questions]))
    ).all()
    by_question = {}
    for option in options:
        by_question.setdefault(option.question_id, []).append(option)
    assert len(by_question) == 18
    assert all(len(rows) == 5 for rows in by_question.values())
    assert all(sum(option.is_correct for option in rows) == 1 for rows in by_question.values())
    assert Counter(option.option_key for option in options) == Counter({key: 18 for key in "ABCDE"})

    replay = import_questions(db_session, data, "application/json", BATCH.name, True)
    assert replay.aborted is False and replay.errors == []
    assert replay.would_import == 0 and replay.duplicates == 18
    assert db_session.scalar(select(func.count(Question.id))) == 18
