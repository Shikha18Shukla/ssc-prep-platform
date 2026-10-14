"""Focused tests for Discount planning, transactional import and repeat runs."""
import json
from collections import Counter

import pytest
from sqlalchemy import event, func, select
from sqlalchemy.exc import IntegrityError

from app.models import Chapter, Difficulty, Exam, Question, QuestionOption, Subject, Subcategory
from app.services.question_import_service import import_questions
from scripts.import_discount_verified_batch import BATCH, load_batch, plan_missing


@pytest.fixture
def discount_catalog(db_session):
    exam = Exam(name="SSC", slug="ssc", is_active=True)
    db_session.add(exam)
    db_session.flush()
    subject = Subject(exam_id=exam.id, name="Maths", slug="maths", is_active=True)
    db_session.add(subject)
    db_session.flush()
    category = Subcategory(subject_id=subject.id, name="Arithmetic Maths", slug="arithmetic-maths", is_active=True)
    db_session.add(category)
    db_session.flush()
    chapter = Chapter(subject_id=subject.id, subcategory_id=category.id, name="Discount", slug="discount", is_active=True)
    db_session.add(chapter)
    db_session.commit()
    return chapter


def test_planner_targets_thirty_per_level_and_keeps_bank_rows():
    records = load_batch()
    assert len(records) == 90
    assert Counter(row["difficulty"] for row in records) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    # The planner groups the selected rows by difficulty, while preserving each
    # bank row's content. Compare the full rows without requiring batch order.
    planned = plan_missing(records, [])
    assert sorted(json.dumps(row, sort_keys=True) for row in planned) == sorted(
        json.dumps(row, sort_keys=True) for row in records
    )


def test_import_dry_run_commit_and_replay_are_idempotent(db_session, discount_catalog):
    data = BATCH.read_bytes()
    preview = import_questions(db_session, data, "application/json", BATCH.name, True)
    assert preview.aborted is False and preview.errors == []
    assert preview.would_import == 90 and preview.duplicates == 0
    assert db_session.scalar(select(func.count(Question.id))) == 0

    first = import_questions(db_session, data, "application/json", BATCH.name, False)
    assert first.imported == 90 and first.duplicates == 0 and first.errors == []
    rows = db_session.scalars(select(Question).where(Question.chapter_id == discount_catalog.id)).all()
    assert Counter(row.difficulty.value for row in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert all(row.is_active and not row.is_pyq for row in rows)
    assert plan_missing(load_batch(), rows) == []

    replay = import_questions(db_session, data, "application/json", BATCH.name, False)
    assert replay.imported == 0 and replay.duplicates == 90
    assert db_session.scalar(select(func.count(Question.id))) == 90


def test_planner_preserves_existing_rows_and_fills_only_the_active_deficit(db_session, discount_catalog):
    record = load_batch()[0]
    matching = next(option for option in "ABCD" if option == record["correct_option"])
    options = [QuestionOption(option_key=key, option_text=record["options"][key], is_correct=key == matching,
                              display_order=index) for index, key in enumerate("ABCD", 1)]
    existing = Question(chapter_id=discount_catalog.id, question_text=record["question_text"],
                         explanation=record["explanation"], difficulty=Difficulty(record["difficulty"]), is_pyq=False,
                         is_active=True, source=record["source"], options=options)
    db_session.add(existing)
    db_session.commit()
    selected = plan_missing(load_batch(), [existing])
    assert len(selected) == 89
    assert record["question_text"] not in {row["question_text"] for row in selected}


def test_unrelated_integrity_error_is_raised_and_rolled_back(db_session, discount_catalog):
    failure = IntegrityError("simulated unrelated constraint", {}, RuntimeError("not duplicate"))

    def fail_flush(_session, _flush_context, _instances):
        raise failure

    event.listen(db_session, "before_flush", fail_flush)
    try:
        with pytest.raises(IntegrityError, match="simulated unrelated constraint"):
            import_questions(db_session, json.dumps({"questions": [load_batch()[0]]}).encode(),
                            "application/json", "discount.json", False)
    finally:
        event.remove(db_session, "before_flush", fail_flush)
    assert db_session.scalar(select(func.count(Question.id))) == 0
    assert db_session.scalar(select(func.count(QuestionOption.id))) == 0
