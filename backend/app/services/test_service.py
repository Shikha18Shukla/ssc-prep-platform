"""Transactional test creation, answer persistence and submission."""

import random
from datetime import datetime, timedelta, timezone
import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import (
    Chapter,
    Difficulty,
    Exam,
    Question,
    Subject,
    Subcategory,
    TestAttempt,
    TestAttemptStatus,
    TestQuestion,
    UserAnswer,
)

ALLOWED_COUNTS = {10, 15, 20, 25}
SECONDS_PER_QUESTION = 36


def _aware(value: datetime) -> datetime:
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value


def deadline(attempt: TestAttempt) -> datetime:
    return _aware(attempt.started_at) + timedelta(seconds=attempt.duration_seconds)


def _owned_attempt(db: Session, attempt_id: uuid.UUID, user_id: uuid.UUID, lock=False):
    query = select(TestAttempt).where(
        TestAttempt.id == attempt_id, TestAttempt.user_id == user_id
    )
    if lock:
        query = query.with_for_update()
    attempt = db.execute(query).scalar_one_or_none()
    if attempt is None:
        raise HTTPException(status_code=404, detail="Test session not found")
    return attempt


def _finalize(db: Session, attempt: TestAttempt, now: datetime, timed_out: bool):
    answers = list(
        db.execute(
            select(UserAnswer)
            .where(UserAnswer.test_attempt_id == attempt.id)
            .options(joinedload(UserAnswer.test_question).joinedload(TestQuestion.question).joinedload(Question.options))
        ).scalars().unique()
    )
    attempted = sum(answer.is_answered for answer in answers)
    correct = 0
    for answer in answers:
        correct_option = next(
            (option.option_key for option in answer.test_question.question.options if option.is_correct),
            None,
        )
        answer.is_correct = bool(answer.is_answered and answer.selected_option == correct_option)
        correct += bool(answer.is_correct)
    attempt.correct_count = correct
    attempt.wrong_count = attempted - correct
    attempt.unanswered_count = attempt.question_count - attempted
    attempt.score = (2.0 * attempt.correct_count) - (0.5 * attempt.wrong_count)
    attempt.time_taken_seconds = min(
        attempt.duration_seconds,
        max(0, int((_aware(now) - _aware(attempt.started_at)).total_seconds())),
    )
    attempt.status = TestAttemptStatus.AUTO_SUBMITTED if timed_out else TestAttemptStatus.COMPLETED
    attempt.submitted_at = now
    db.flush()


def create_test(db: Session, user_id: uuid.UUID, payload) -> TestAttempt:
    if payload.question_count not in ALLOWED_COUNTS:
        raise HTTPException(status_code=422, detail="Question count must be 10, 15, 20 or 25")
    is_pyq = payload.difficulty == "PYQ"
    try:
        difficulty = None if is_pyq else Difficulty(payload.difficulty)
    except ValueError:
        raise HTTPException(status_code=422, detail="Difficulty must be EASY, MEDIUM, HARD or PYQ")

    exam = db.get(Exam, payload.exam_id)
    subject = db.get(Subject, payload.subject_id)
    chapter = db.get(Chapter, payload.chapter_id)
    if not exam or not exam.is_active:
        raise HTTPException(status_code=404, detail="Active exam not found")
    if not subject or not subject.is_active or subject.exam_id != exam.id:
        raise HTTPException(status_code=422, detail="Subject does not belong to the selected active exam")
    if not chapter or not chapter.is_active or chapter.subject_id != subject.id:
        raise HTTPException(status_code=422, detail="Chapter does not belong to the selected active subject")
    if chapter.subcategory_id != payload.subcategory_id:
        raise HTTPException(status_code=422, detail="Category does not match the selected chapter")
    if payload.subcategory_id:
        category = db.get(Subcategory, payload.subcategory_id)
        if not category or not category.is_active or category.subject_id != subject.id:
            raise HTTPException(status_code=422, detail="Category does not belong to the selected subject")

    question_query = select(Question).where(
        Question.chapter_id == chapter.id,
        Question.is_active.is_(True),
        Question.is_pyq.is_(is_pyq),
    )
    if not is_pyq:
        question_query = question_query.where(Question.difficulty == difficulty)
    eligible = list(db.execute(question_query.options(joinedload(Question.options))).scalars().unique())
    eligible = [
        q for q in eligible
        if {option.option_key for option in q.options} == {"A", "B", "C", "D"}
        and all(option.option_text.strip() for option in q.options)
        and sum(option.is_correct for option in q.options) == 1
    ]
    if len(eligible) < payload.question_count:
        raise HTTPException(
            status_code=409,
            detail=f"Only {len(eligible)} eligible active questions are available; {payload.question_count} are required.",
        )

    selected = random.SystemRandom().sample(eligible, payload.question_count)
    attempt = TestAttempt(
        user_id=user_id,
        exam_id=exam.id,
        subject_id=subject.id,
        chapter_id=chapter.id,
        difficulty=difficulty,
        is_pyq=is_pyq,
        question_count=payload.question_count,
        duration_seconds=payload.question_count * SECONDS_PER_QUESTION,
    )
    try:
        db.add(attempt)
        db.flush()
        db.add_all(
            TestQuestion(test_attempt_id=attempt.id, question_id=q.id, question_order=index)
            for index, q in enumerate(selected, start=1)
        )
        db.commit()
        db.refresh(attempt)
        return attempt
    except Exception:
        db.rollback()
        raise


def get_active_test(db: Session, attempt_id: uuid.UUID, user_id: uuid.UUID):
    try:
        attempt = _owned_attempt(db, attempt_id, user_id, lock=True)
        now = datetime.now(timezone.utc)
        if attempt.status == TestAttemptStatus.IN_PROGRESS and now >= deadline(attempt):
            _finalize(db, attempt, now, timed_out=True)
            db.commit()
        else:
            db.commit()
        return attempt
    except Exception:
        db.rollback()
        raise


def save_answer(
    db: Session,
    attempt_id: uuid.UUID,
    test_question_id: uuid.UUID,
    selected_option: str,
    user_id: uuid.UUID,
):
    try:
        attempt = _owned_attempt(db, attempt_id, user_id, lock=True)
        now = datetime.now(timezone.utc)
        if attempt.status != TestAttemptStatus.IN_PROGRESS:
            raise HTTPException(status_code=409, detail="This test has already been submitted")
        if now >= deadline(attempt):
            _finalize(db, attempt, now, timed_out=True)
            db.commit()
            raise HTTPException(status_code=409, detail="Time expired; the test was auto-submitted")
        tq = db.execute(
            select(TestQuestion)
            .where(TestQuestion.id == test_question_id, TestQuestion.test_attempt_id == attempt.id)
            .options(joinedload(TestQuestion.question).joinedload(Question.options))
        ).unique().scalar_one_or_none()
        if tq is None:
            raise HTTPException(status_code=404, detail="Question is not part of this test")
        if not any(option.option_key == selected_option for option in tq.question.options):
            raise HTTPException(status_code=422, detail="Selected option is not valid for this question")
        answer = db.execute(
            select(UserAnswer).where(
                UserAnswer.test_attempt_id == attempt.id,
                UserAnswer.test_question_id == tq.id,
            )
        ).scalar_one_or_none()
        if answer is None:
            answer = UserAnswer(test_attempt_id=attempt.id, test_question_id=tq.id)
            db.add(answer)
        answer.selected_option = selected_option
        answer.is_answered = True
        answer.answered_at = now
        db.commit()
        return answer
    except HTTPException:
        if db.in_transaction():
            db.rollback()
        raise
    except Exception:
        db.rollback()
        raise


def submit_test(db: Session, attempt_id: uuid.UUID, user_id: uuid.UUID):
    try:
        attempt = _owned_attempt(db, attempt_id, user_id, lock=True)
        if attempt.status == TestAttemptStatus.IN_PROGRESS:
            now = datetime.now(timezone.utc)
            _finalize(db, attempt, now, timed_out=now >= deadline(attempt))
        db.commit()
        return attempt
    except Exception:
        db.rollback()
        raise
