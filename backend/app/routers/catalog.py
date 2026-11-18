"""Authenticated exam catalog endpoints for practice selection."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models import Chapter, Exam, Question, Subject
from app.schemas.catalog import ChapterAvailability, PracticeLevel, SubcategoryRead
from app.schemas.common import ChapterRead, ExamRead, SubjectRead
from app.services.catalog_service import (
    get_chapter_availability,
    list_active_chapters_for_selection,
    list_active_exams,
    list_active_subjects,
    list_active_subcategories,
)
from app.services.beta_scope import subject_is_in_beta

router = APIRouter(
    prefix="/exams",
    tags=["Exam Catalog"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=list[ExamRead], summary="List active exams")
def get_exams(db: Session = Depends(get_db)) -> list[Exam]:
    return list_active_exams(db)


@router.get(
    "/{exam_id}/subjects",
    response_model=list[SubjectRead],
    summary="List active subjects for an exam",
)
def get_subjects(exam_id: uuid.UUID, db: Session = Depends(get_db)) -> list[Subject]:
    subjects = list_active_subjects(db, exam_id)
    if subjects is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Active exam not found")
    return subjects


@router.get(
    "/subjects/{subject_id}/subcategories",
    response_model=list[SubcategoryRead],
    summary="List active subcategories for a subject",
)
def get_subcategories(
    subject_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    subcategories = list_active_subcategories(db, subject_id)
    if subcategories is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Active subject not found")
    return subcategories


@router.get(
    "/subjects/{subject_id}/chapters",
    response_model=list[ChapterRead],
    summary="List active chapters for a subject",
)
def get_chapters(
    subject_id: uuid.UUID,
    subcategory_id: uuid.UUID | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[Chapter]:
    chapters = list_active_chapters_for_selection(db, subject_id, subcategory_id)
    if chapters is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Active subject not found")
    return chapters


@router.get("/subjects/{subject_id}/chapter-counts", summary="Get active question counts for every chapter in a subject")
def get_subject_chapter_counts(subject_id: uuid.UUID, db: Session = Depends(get_db)) -> list[dict]:
    subject = db.execute(
        select(Subject.id, Subject.slug, Exam.slug)
        .join(Exam, Exam.id == Subject.exam_id)
        .where(Subject.id == subject_id, Subject.is_active.is_(True), Exam.is_active.is_(True))
    ).one_or_none()
    if subject is None or not subject_is_in_beta(subject[2], subject[1]):
        raise HTTPException(status_code=404, detail="Active subject not found")
    rows = db.execute(
        select(Chapter.id, func.count(Question.id))
        .outerjoin(Question, (Question.chapter_id == Chapter.id) & Question.is_active.is_(True))
        .where(Chapter.subject_id == subject_id, Chapter.is_active.is_(True))
        .group_by(Chapter.id)
        .order_by(Chapter.id)
    ).all()
    return [{"chapter_id": chapter_id, "question_count": count} for chapter_id, count in rows]


@router.get(
    "/chapters/{chapter_id}/availability",
    response_model=ChapterAvailability,
    summary="Check active question availability for a chapter and level",
)
def get_availability(
    chapter_id: uuid.UUID,
    level: PracticeLevel,
    question_count: Annotated[int | None, Query(ge=1, le=25)] = None,
    db: Session = Depends(get_db),
) -> ChapterAvailability:
    availability = get_chapter_availability(db, chapter_id, level, question_count)
    if availability is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Active chapter not found")
    return ChapterAvailability.model_validate(availability)
