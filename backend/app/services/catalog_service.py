"""Database-backed queries for the authenticated exam catalog."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Chapter, Difficulty, Exam, Question, Subject, Subcategory
from app.schemas.catalog import PracticeLevel
from app.config import settings
from app.services.beta_scope import chapter_is_in_beta, subcategory_is_in_beta, subject_is_in_beta

QUESTION_COUNTS = (10, 15, 20, 25)


def _allowed_question_counts(available_count: int) -> list[int]:
    if 0 < available_count < QUESTION_COUNTS[0]:
        return [available_count]
    return [count for count in QUESTION_COUNTS if count <= available_count]


def list_active_exams(db: Session) -> list[Exam]:
    query = select(Exam).where(Exam.is_active.is_(True))
    if settings.BETA_CATALOG_SCOPE:
        query = query.where(Exam.slug == "ssc")
    return list(db.execute(query.order_by(Exam.slug)).scalars().all())


def list_active_subjects(db: Session, exam_id) -> list[Subject] | None:
    exam_query = select(Exam.id).where(Exam.id == exam_id, Exam.is_active.is_(True))
    if settings.BETA_CATALOG_SCOPE:
        exam_query = exam_query.where(Exam.slug == "ssc")
    active_exam = db.execute(exam_query).scalar_one_or_none()
    if active_exam is None:
        return None

    subject_query = select(Subject).where(Subject.exam_id == exam_id, Subject.is_active.is_(True))
    if settings.BETA_CATALOG_SCOPE:
        subject_query = subject_query.where(Subject.slug.in_(["maths", "reasoning", "gk-gs"]))
    return list(
        db.execute(
            subject_query.order_by(Subject.display_order, Subject.name)
        )
        .scalars()
        .all()
    )


def list_active_subcategories(db: Session, subject_id) -> list[Subcategory] | None:
    subject_row = db.execute(
        select(Subject.id, Subject.slug, Exam.slug)
        .join(Exam, Exam.id == Subject.exam_id)
        .where(
            Subject.id == subject_id,
            Subject.is_active.is_(True),
            Exam.is_active.is_(True),
        )
    ).one_or_none()
    if subject_row is None:
        return None
    _, subject_slug, exam_slug = subject_row
    if not subject_is_in_beta(exam_slug, subject_slug):
        return None

    subcategory_query = select(Subcategory).where(
        Subcategory.subject_id == subject_id,
        Subcategory.is_active.is_(True),
    )
    if settings.BETA_CATALOG_SCOPE and subject_slug == "gk-gs":
        subcategory_query = subcategory_query.where(Subcategory.slug == "science")
    return list(
        db.execute(
            subcategory_query.order_by(Subcategory.display_order, Subcategory.name)
        )
        .scalars()
        .all()
    )


def list_active_chapters_for_selection(
    db: Session,
    subject_id,
    subcategory_id=None,
) -> list[Chapter] | None:
    subject_row = db.execute(
        select(Subject.id, Subject.slug, Exam.slug)
        .join(Exam, Exam.id == Subject.exam_id)
        .where(
            Subject.id == subject_id,
            Subject.is_active.is_(True),
            Exam.is_active.is_(True),
        )
    ).one_or_none()
    if subject_row is None:
        return None
    _, subject_slug, exam_slug = subject_row
    if not subject_is_in_beta(exam_slug, subject_slug):
        return None

    chapter_query = select(Chapter).where(
        Chapter.subject_id == subject_id,
        Chapter.is_active.is_(True),
    )
    if subcategory_id is not None:
        active_subcategory = db.execute(
            select(Subcategory.id, Subcategory.slug).where(
                Subcategory.id == subcategory_id,
                Subcategory.subject_id == subject_id,
                Subcategory.is_active.is_(True),
            )
        ).one_or_none()
        if active_subcategory is None:
            return None
        if not subcategory_is_in_beta(subject_slug, active_subcategory.slug):
            return None
        chapter_query = chapter_query.where(Chapter.subcategory_id == subcategory_id)
    elif settings.BETA_CATALOG_SCOPE and subject_slug == "gk-gs":
        chapter_query = chapter_query.join(Subcategory, Subcategory.id == Chapter.subcategory_id).where(
            Subcategory.slug == "science",
        )

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
        select(Exam.slug, Subject.slug, Subcategory.slug)
        .select_from(Chapter)
        .join(Subject, Subject.id == Chapter.subject_id)
        .join(Exam, Exam.id == Subject.exam_id)
        .outerjoin(Subcategory, Subcategory.id == Chapter.subcategory_id)
        .where(
            Chapter.id == chapter_id,
            Chapter.is_active.is_(True),
            Subject.is_active.is_(True),
            Exam.is_active.is_(True),
        )
    ).one_or_none()
    if active_chapter is None or not chapter_is_in_beta(*active_chapter):
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
    allowed_counts = _allowed_question_counts(available_count)
    return {
        "chapter_id": chapter_id,
        "level": level,
        "available_question_count": available_count,
        "allowed_question_counts": allowed_counts,
        "requested_question_count": requested_question_count,
        "can_satisfy_request": (
            requested_question_count in allowed_counts
            if requested_question_count is not None
            else None
        ),
    }
