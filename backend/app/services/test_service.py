"""Transactional test creation, answer persistence and submission."""

import random
from datetime import datetime, timedelta, timezone
import uuid

from fastapi import HTTPException
from sqlalchemy import select, update
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
    UserChapterRotation,
    UserQuestionHistory,
)
from app.config import settings
from app.services.beta_scope import chapter_is_in_beta, subject_is_in_beta

ALLOWED_COUNTS = {10, 15, 20, 25}
SECONDS_PER_QUESTION = 36
DIFFICULTY_SUBJECT_SLUGS = {"maths", "reasoning"}
TEST_TYPES = {"CHAPTER_WISE", "MISCELLANEOUS"}


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


def _valid_questions(questions):
    return [
        question for question in questions
        if {option.option_key for option in question.options} == {"A", "B", "C", "D"}
        and all(option.option_text.strip() for option in question.options)
        and sum(option.is_correct for option in question.options) == 1
    ]


def _allowed_question_counts(available: int) -> list[int]:
    allowed = [count for count in sorted(ALLOWED_COUNTS) if count <= available]
    if 0 < available <= max(ALLOWED_COUNTS) and available not in allowed:
        allowed.append(available)
    return sorted(allowed)


def _selection_counts(available: int, subject: Subject) -> list[int]:
    if subject.slug == "reasoning":
        return [count for count in sorted(ALLOWED_COUNTS) if count <= available]
    return _allowed_question_counts(available)


def _balanced_chapter_sample(questions: list[Question], count: int) -> list[Question]:
    """Sample across chapters in rounds so large chapters do not dominate."""
    by_chapter: dict[uuid.UUID, list[Question]] = {}
    for question in questions:
        by_chapter.setdefault(question.chapter_id, []).append(question)
    rng = random.SystemRandom()
    for chapter_questions in by_chapter.values():
        rng.shuffle(chapter_questions)
    chapter_ids = list(by_chapter)
    rng.shuffle(chapter_ids)
    selected: list[Question] = []
    while len(selected) < count:
        rng.shuffle(chapter_ids)
        progressed = False
        for chapter_id in chapter_ids:
            if by_chapter[chapter_id]:
                selected.append(by_chapter[chapter_id].pop())
                progressed = True
                if len(selected) == count:
                    break
        if not progressed:
            break
    return selected


def _rotation_state(db: Session, user_id: uuid.UUID, chapter_id: uuid.UUID,
                    selection_mode: str) -> UserChapterRotation:
    """Create then lock a per-user chapter/mode row, serializing overlapping starts."""
    dialect = db.bind.dialect.name
    if dialect == "postgresql":
        from sqlalchemy.dialects.postgresql import insert
        db.execute(insert(UserChapterRotation).values(user_id=user_id, chapter_id=chapter_id,
                                                       selection_mode=selection_mode, rotation=0)
                   .on_conflict_do_nothing(constraint="uq_user_chapter_rotation_mode"))
    elif dialect == "sqlite":
        from sqlalchemy.dialects.sqlite import insert
        db.execute(insert(UserChapterRotation).values(user_id=user_id, chapter_id=chapter_id,
                                                       selection_mode=selection_mode, rotation=0)
                   .on_conflict_do_nothing(index_elements=["user_id", "chapter_id", "selection_mode"]))
    else:
        state = db.execute(select(UserChapterRotation).where(
            UserChapterRotation.user_id == user_id,
            UserChapterRotation.chapter_id == chapter_id,
            UserChapterRotation.selection_mode == selection_mode,
        )).scalar_one_or_none()
        if state is None:
            state = UserChapterRotation(user_id=user_id, chapter_id=chapter_id,
                                        selection_mode=selection_mode, rotation=0)
            db.add(state)
            db.flush()
    state = db.execute(select(UserChapterRotation).where(
        UserChapterRotation.user_id == user_id,
        UserChapterRotation.chapter_id == chapter_id,
        UserChapterRotation.selection_mode == selection_mode,
    ).with_for_update()).scalar_one()
    return state


def _rotated_sample(db: Session, user_id: uuid.UUID, chapter_id: uuid.UUID,
                    selection_mode: str,
                    questions: list[Question], count: int) -> tuple[list[Question], int]:
    """Choose unseen questions first and update history in the attempt transaction."""
    state = _rotation_state(db, user_id, chapter_id, selection_mode)
    ids = [question.id for question in questions]
    history = db.scalars(select(UserQuestionHistory).where(
        UserQuestionHistory.user_id == user_id,
        UserQuestionHistory.chapter_id == chapter_id,
        UserQuestionHistory.selection_mode == selection_mode,
        UserQuestionHistory.question_id.in_(ids),
    )).all() if ids else []
    by_id = {row.question_id: row for row in history}
    current_rotation = state.rotation
    unseen = [q for q in questions if q.id not in by_id or by_id[q.id].rotation < current_rotation]
    rng = random.SystemRandom()
    rng.shuffle(unseen)
    selected = unseen[:count]
    if len(selected) < count:
        if not unseen:
            # Every eligible item has been served in this cycle. Start another cycle;
            # the least-recently/repeated items are naturally deprioritized below.
            state.rotation += 1
            current_rotation = state.rotation
            unseen = list(questions)
            rng.shuffle(unseen)
            selected = unseen[:count]
        else:
            remaining = [q for q in questions if q not in selected]
            rng.shuffle(remaining)
            remaining.sort(key=lambda q: (by_id[q.id].served_count if q.id in by_id else 0,
                                          by_id[q.id].last_served_at.timestamp() if q.id in by_id else 0))
            selected.extend(remaining[:count - len(selected)])
    now = datetime.now(timezone.utc)
    for question in selected:
        row = by_id.get(question.id)
        if row is None:
            db.add(UserQuestionHistory(user_id=user_id, chapter_id=chapter_id,
                                       selection_mode=selection_mode, question_id=question.id,
                                       rotation=current_rotation, served_count=1, last_served_at=now))
        else:
            row.rotation = current_rotation
            row.served_count += 1
            row.last_served_at = now
    return selected, current_rotation


def _selection(db: Session, exam_id, subject_id, test_type, chapter_id, subcategory_id, requested_level):
    if test_type not in TEST_TYPES:
        raise HTTPException(status_code=422, detail="Test type must be CHAPTER_WISE or MISCELLANEOUS")
    exam = db.get(Exam, exam_id)
    subject = db.get(Subject, subject_id)
    if not exam or not exam.is_active:
        raise HTTPException(status_code=404, detail="Active exam not found")
    if not subject or not subject.is_active or subject.exam_id != exam.id:
        raise HTTPException(status_code=422, detail="Subject does not belong to the selected active exam")
    if not subject_is_in_beta(exam.slug, subject.slug):
        raise HTTPException(status_code=404, detail="This subject is not available in the beta")

    if test_type == "CHAPTER_WISE":
        if chapter_id is None:
            raise HTTPException(status_code=422, detail="A chapter is required for a chapter-wise test")
        chapter = db.get(Chapter, chapter_id)
        if not chapter or not chapter.is_active or chapter.subject_id != subject.id:
            raise HTTPException(status_code=422, detail="Chapter does not belong to the selected active subject")
        subcategory_slug = db.scalar(select(Subcategory.slug).where(Subcategory.id == chapter.subcategory_id)) if chapter.subcategory_id else None
        if not chapter_is_in_beta(exam.slug, subject.slug, subcategory_slug):
            raise HTTPException(status_code=404, detail="This chapter is not available in the beta")
        if subcategory_id is not None:
            category = db.get(Subcategory, subcategory_id)
            if not category or not category.is_active or category.subject_id != subject.id:
                raise HTTPException(status_code=422, detail="Category does not belong to the selected subject")
            if chapter.subcategory_id != category.id:
                raise HTTPException(status_code=422, detail="Category does not match the selected chapter")
    else:
        if chapter_id is not None or subcategory_id is not None:
            raise HTTPException(status_code=422, detail="Miscellaneous tests cannot include a chapter or category")
        chapter = None

    is_pyq = requested_level == "PYQ"
    difficulty = None
    if requested_level is not None and not is_pyq:
        try:
            difficulty = Difficulty(requested_level)
        except ValueError:
            raise HTTPException(status_code=422, detail="Difficulty must be EASY, MEDIUM, HARD, or PYQ")
    if is_pyq and requested_level not in {"PYQ"}:
        raise HTTPException(status_code=422, detail="PYQ selection is invalid")
    if not is_pyq:
        if subject.slug not in DIFFICULTY_SUBJECT_SLUGS and difficulty is not None:
            raise HTTPException(status_code=422, detail="Difficulty selection is only supported for Maths and Reasoning")

    query = select(Question).join(Chapter, Question.chapter_id == Chapter.id).where(
        Chapter.subject_id == subject.id,
        Chapter.is_active.is_(True),
        Question.is_active.is_(True),
        Question.is_pyq.is_(is_pyq),
    )
    if settings.BETA_CATALOG_SCOPE and subject.slug == "gk-gs":
        query = query.join(Subcategory, Subcategory.id == Chapter.subcategory_id).where(
            Subcategory.slug == "science",
        )
    if chapter is not None:
        query = query.where(Question.chapter_id == chapter.id)
    if difficulty is not None:
        query = query.where(Question.difficulty == difficulty)
    questions = _valid_questions(db.execute(query.options(joinedload(Question.options))).scalars().unique())
    return exam, subject, chapter, difficulty, is_pyq, questions


def get_test_availability(db: Session, exam_id, subject_id, test_type, chapter_id, subcategory_id, requested_level, question_count=None):
    if question_count is not None and not 1 <= question_count <= max(ALLOWED_COUNTS):
        raise HTTPException(status_code=422, detail="Question count must be between 1 and 25")
    _, subject, _, _, _, eligible = _selection(
        db, exam_id, subject_id, test_type, chapter_id, subcategory_id, requested_level,
    )
    available = len(eligible)
    allowed = _selection_counts(available, subject)
    return {
        "available_question_count": available,
        "allowed_question_counts": allowed,
        "can_satisfy_request": question_count is None or question_count in allowed,
    }


def create_test(db: Session, user_id: uuid.UUID, payload) -> TestAttempt:
    if not 1 <= payload.question_count <= max(ALLOWED_COUNTS):
        raise HTTPException(status_code=422, detail="Question count must be between 1 and 25")
    exam, subject, chapter, difficulty, is_pyq, eligible = _selection(
        db, payload.exam_id, payload.subject_id, payload.test_type, payload.chapter_id,
        payload.subcategory_id, payload.difficulty,
    )
    if payload.question_count not in _selection_counts(len(eligible), subject):
        raise HTTPException(
            status_code=409,
            detail=(
                f"{len(eligible)} eligible active questions are available; "
                f"the requested {payload.question_count}-question test is unavailable."
            ),
        )

    if chapter is not None:
        selection_mode = "PYQ" if is_pyq else difficulty.value if difficulty else "MIXED"
        selected, _ = _rotated_sample(db, user_id, chapter.id, selection_mode,
                                      eligible, payload.question_count)
    elif subject.slug == "reasoning" and payload.test_type == "MISCELLANEOUS":
        selected = _balanced_chapter_sample(eligible, payload.question_count)
    else:
        selected = random.SystemRandom().sample(eligible, payload.question_count)
    attempt = TestAttempt(
        user_id=user_id,
        exam_id=exam.id,
        subject_id=subject.id,
        chapter_id=chapter.id if chapter else None,
        test_type=payload.test_type,
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
