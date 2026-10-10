"""Authenticated test session and result endpoints."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models import Question, TestAttempt, TestAttemptStatus, TestQuestion, UserAnswer
from app.models.user import User
from app.schemas.tests import (
    ActiveTestQuestion,
    ActiveTestRead,
    AnswerUpdate,
    DashboardHistory,
    ReviewQuestion,
    TestCreate,
    TestResultRead,
    TestSummary,
    TestOption,
)
from app.services.test_service import create_test, deadline, get_active_test, save_answer, submit_test

router = APIRouter(prefix="/tests", tags=["Tests"], dependencies=[Depends(get_current_user)])


def _current(attempt: TestAttempt, db: Session) -> ActiveTestRead:
    rows = db.execute(
        select(TestQuestion)
        .where(TestQuestion.test_attempt_id == attempt.id)
        .order_by(TestQuestion.question_order)
        .options(joinedload(TestQuestion.question).joinedload(Question.options))
    ).scalars().unique().all()
    answers = {
        answer.test_question_id: answer.selected_option
        for answer in db.execute(
            select(UserAnswer).where(UserAnswer.test_attempt_id == attempt.id)
        ).scalars()
    }
    return ActiveTestRead(
        id=attempt.id,
        exam_id=attempt.exam_id,
        subject_id=attempt.subject_id,
        chapter_id=attempt.chapter_id,
        difficulty="PYQ" if attempt.is_pyq else (attempt.difficulty.value if attempt.difficulty else ""),
        question_count=attempt.question_count,
        duration_seconds=attempt.duration_seconds,
        started_at=attempt.started_at,
        deadline_at=deadline(attempt),
        status=attempt.status,
        questions=[
            ActiveTestQuestion(
                test_question_id=row.id,
                question_order=row.question_order,
                question_text=row.question.question_text,
                options=[TestOption(option_key=o.option_key, option_text=o.option_text) for o in row.question.options],
                selected_option=answers.get(row.id),
            )
            for row in rows
        ],
    )


def _summary(attempt: TestAttempt, db: Session) -> TestSummary:
    attempted = db.execute(
        select(func.count(UserAnswer.id)).where(
            UserAnswer.test_attempt_id == attempt.id,
            UserAnswer.is_answered.is_(True),
        )
    ).scalar_one()
    submitted = attempt.status != TestAttemptStatus.IN_PROGRESS
    return TestSummary(
        id=attempt.id,
        status=attempt.status,
        question_count=attempt.question_count,
        attempted_count=attempted,
        unanswered_count=attempt.question_count - attempted,
        correct_count=attempt.correct_count if submitted else None,
        wrong_count=attempt.wrong_count if submitted else None,
        score=attempt.score if submitted else None,
        scoring_pending=not submitted,
        duration_seconds=attempt.duration_seconds,
        time_taken_seconds=attempt.time_taken_seconds,
        started_at=attempt.started_at,
        submitted_at=attempt.submitted_at,
    )


@router.post("", response_model=ActiveTestRead, status_code=status.HTTP_201_CREATED)
def start_test(
    payload: TestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    attempt = create_test(db, current_user.id, payload)
    return _current(attempt, db)


@router.get("/{attempt_id}", response_model=ActiveTestRead)
def read_test(
    attempt_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    attempt = get_active_test(db, attempt_id, current_user.id)
    return _current(attempt, db)


@router.put("/{attempt_id}/questions/{test_question_id}/answer", response_model=TestSummary)
def update_answer(
    attempt_id: uuid.UUID,
    test_question_id: uuid.UUID,
    payload: AnswerUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    save_answer(db, attempt_id, test_question_id, payload.selected_option, current_user.id)
    attempt = get_active_test(db, attempt_id, current_user.id)
    return _summary(attempt, db)


@router.post("/{attempt_id}/submit", response_model=TestSummary)
def finish_test(
    attempt_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    attempt = submit_test(db, attempt_id, current_user.id)
    return _summary(attempt, db)


@router.get("/{attempt_id}/result", response_model=TestResultRead)
def test_result(
    attempt_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    attempt = get_active_test(db, attempt_id, current_user.id)
    if attempt.status == TestAttemptStatus.IN_PROGRESS:
        raise HTTPException(status_code=409, detail="Submit the test before viewing results")
    summary = _summary(attempt, db)
    rows = db.execute(
        select(TestQuestion)
        .where(TestQuestion.test_attempt_id == attempt.id)
        .order_by(TestQuestion.question_order)
        .options(joinedload(TestQuestion.question).joinedload(Question.options))
    ).scalars().unique().all()
    answers = {
        answer.test_question_id: answer
        for answer in db.execute(
            select(UserAnswer).where(UserAnswer.test_attempt_id == attempt.id)
        ).scalars()
    }
    review = []
    for row in rows:
        answer = answers.get(row.id)
        question = row.question
        correct = next((o.option_key for o in question.options if o.is_correct), "")
        review.append(ReviewQuestion(
            question_order=row.question_order,
            question_text=question.question_text,
            options=[TestOption(option_key=o.option_key, option_text=o.option_text) for o in question.options],
            selected_option=answer.selected_option if answer else None,
            correct_option=correct,
            explanation=question.explanation,
            is_correct=bool(answer and answer.is_answered and answer.selected_option == correct),
        ))
    return TestResultRead(**summary.model_dump(), review=review)


@router.get("/history/me", response_model=DashboardHistory)
def test_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    attempts = list(db.execute(
        select(TestAttempt)
        .where(TestAttempt.user_id == current_user.id)
        .order_by(TestAttempt.created_at.desc())
    ).scalars())
    completed = [item for item in attempts if item.status != TestAttemptStatus.IN_PROGRESS]
    scored = [item.score for item in completed if item.score is not None]
    summaries = [_summary(item, db) for item in attempts[:20]]
    return DashboardHistory(
        tests_attempted=len(completed),
        average_score=sum(scored) / len(scored) if scored else None,
        best_score=max(scored) if scored else None,
        previous_tests=summaries,
    )
