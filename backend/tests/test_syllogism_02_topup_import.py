"""Regression checks for the source-verified Syllogism lecture 02 top-up."""

import json
import unicodedata
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
    / "syllogism"
    / "syllogism_02_topup_verified.json"
)


def _normalized(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def test_topup_is_complete_source_traceable_and_has_one_keyed_answer():
    records = json.loads(PAYLOAD.read_text(encoding="utf-8"))["questions"]
    assert len(records) == 14
    assert len({_normalized(row["question_text"]) for row in records}) == 14
    for row in records:
        assert (row["exam_slug"], row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == (
            "banking-clerk", "reasoning", "", "syllogism"
        )
        assert row["source"].startswith(("Syllogism 02_Class Notes.pdf, p. ", "Syllogism 03_Class Notes.pdf, p. "))
        assert row["source"].rsplit("p. ", 1)[1].isdigit()
        assert set(row["options"]) == set("ABCDE")
        assert row["correct_option"] in row["options"]
        assert row["explanation"].strip()
        assert row["difficulty"] in {"EASY", "MEDIUM", "HARD"}


def test_topup_import_dry_run_import_and_replay_are_idempotent(db_session: Session):
    exam = Exam(name="Banking Clerk", slug="banking-clerk", is_active=True)
    db_session.add(exam)
    db_session.flush()
    subject = Subject(exam_id=exam.id, name="Reasoning", slug="reasoning", is_active=True)
    db_session.add(subject)
    db_session.flush()
    chapter = Chapter(subject_id=subject.id, name="Syllogism", slug="syllogism", is_active=True)
    db_session.add(chapter)
    db_session.commit()

    payload = PAYLOAD.read_bytes()
    preview = import_questions(db_session, payload, "application/json", PAYLOAD.name, dry_run=True)
    assert preview.aborted is False
    assert preview.would_import == 14
    assert preview.duplicates == 0
    assert preview.errors == []

    imported = import_questions(db_session, payload, "application/json", PAYLOAD.name, dry_run=False)
    assert imported.imported == 14
    assert imported.duplicates == 0

    replay = import_questions(db_session, payload, "application/json", PAYLOAD.name, dry_run=True)
    assert replay.would_import == 0
    assert replay.duplicates == 14

    questions = db_session.scalars(
        select(Question).where(Question.chapter_id == chapter.id).options(joinedload(Question.options))
    ).unique().all()
    assert len(questions) == 14
    assert all(len(question.options) == 5 for question in questions)
    assert all(sum(option.is_correct for option in question.options) == 1 for question in questions)
    assert all(question.explanation and question.source for question in questions)



