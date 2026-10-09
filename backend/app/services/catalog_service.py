"""Database-backed queries for the authenticated exam catalog."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Chapter, Difficulty, Exam, Question, Subject, Subcategory
from app.schemas.catalog import PracticeLevel

QUESTION_COUNTS = (10, 15, 20, 25)


def list_active_exams(db: Session) -> list[Exam]:
    return list(
        db.execute(select(Exam).where(Exam.is_active.is_(True)).order_by(Exam.slug))
        .scalars()
        .all()
    )


def list_active_subjects(db: Session, exam_id) -> list[Subject] | None:
    active_exam = db.execute(
        select(Exam.id).where(Exam.id == exam_id, Exam.is_active.is_(True))
    ).scalar_one_or_none()
    if active_exam is None:
        return None

    return list(
        db.execute(
            select(Subject)
            .where(Subject.exam_id == exam_id, Subject.is_active.is_(True))
            .order_by(Subject.display_order, Subject.name)
        )
        .scalars()
        .all()
    )


def list_active_subcategories(db: Session, subject_id) -> list[Subcategory] | None:
    active_subject = db.execute(
        select(Subject.id)
        .join(Exam, Exam.id == Subject.exam_id)
        .where(
            Subject.id == subject_id,
            Subject.is_active.is_(True),
            Exam.is_active.is_(True),
        )
    ).scalar_one_or_none()
    if active_subject is None:
        return None

    return list(
        db.execute(
            select(Subcategory)
            .where(
                Subcategory.subject_id == subject_id,
                Subcategory.is_active.is_(True),
            )
            .order_by(Subcategory.display_order, Subcategory.name)
        )
        .scalars()
        .all()
    )


def list_active_chapters_for_selection(
    db: Session,
    subject_id,
    subcategory_id=None,
) -> list[Chapter] | None:
    active_subject = db.execute(
        select(Subject.id)
        .join(Exam, Exam.id == Subject.exam_id)
        .where(
            Subject.id == subject_id,
            Subject.is_active.is_(True),
            Exam.is_active.is_(True),
        )
    ).scalar_one_or_none()
    if active_subject is None:
        return None

    chapter_query = select(Chapter).where(
        Chapter.subject_id == subject_id,
        Chapter.is_active.is_(True),
    )
    if subcategory_id is None:
        chapter_query = chapter_query.where(Chapter.subcategory_id.is_(None))
    else:
        active_subcategory = db.execute(
            select(Subcategory.id).where(
                Subcategory.id == subcategory_id,
                Subcategory.subject_id == subject_id,
                Subcategory.is_active.is_(True),
            )
        ).scalar_one_or_none()
        if active_subcategory is None:
            return None
        chapter_query = chapter_query.where(Chapter.subcategory_id == subcategory_id)

    return list(
        db.execute(chapter_query.order_by(Chapter.display_order, Chapter.name))
        .scalars()
        .all()
    )


def get_chapter_availability(
    db: Session,
    chapter_id,
    level: PracticeLevel,
    requested_question_count: int | None = None,
) -> dict | None:
    active_chapter = db.execute(
        select(Chapter.id)
        .join(Subject, Subject.id == Chapter.subject_id)
        .join(Exam, Exam.id == Subject.exam_id)
        .where(
            Chapter.id == chapter_id,
            Chapter.is_active.is_(True),
            Subject.is_active.is_(True),
            Exam.is_active.is_(True),
        )
    ).scalar_one_or_none()
    if active_chapter is None:
        return None

    question_query = select(func.count(Question.id)).where(
        Question.chapter_id == chapter_id,
        Question.is_active.is_(True),
    )
    if level is PracticeLevel.PYQ:
        question_query = question_query.where(Question.is_pyq.is_(True))
    else:
        question_query = question_query.where(
            Question.is_pyq.is_(False),
            Question.difficulty == Difficulty(level.value),
        )

    available_count = db.execute(question_query).scalar_one()
    return {
        "chapter_id": chapter_id,
        "level": level,
        "available_question_count": available_count,
        "allowed_question_counts": [
            count for count in QUESTION_COUNTS if count <= available_count
        ],
        "requested_question_count": requested_question_count,
        "can_satisfy_request": (
            available_count >= requested_question_count
            if requested_question_count is not None
            else None
        ),
    }
