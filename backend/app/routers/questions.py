"""JWT-protected question bank import and management endpoints."""

import uuid

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_admin_user
from app.database.session import get_db
from app.models import Difficulty, Question
from app.schemas.questions import (
    QuestionImportSummary,
    QuestionListResponse,
    QuestionManagementRead,
    QuestionStatusUpdate,
    QuestionUpdate,
)
from app.services.question_import_service import ImportFileError, import_questions
from app.services.question_service import get_question, list_questions, update_question

router = APIRouter(
    prefix="/questions",
    tags=["Question Bank Management"],
    dependencies=[Depends(get_current_admin_user)],
)


@router.post("/import", response_model=QuestionImportSummary, summary="Import CSV or JSON questions")
async def import_question_file(
    file: UploadFile = File(...),
    dry_run: bool = Query(default=True),
    db: Session = Depends(get_db),
) -> QuestionImportSummary:
    """Dry-run defaults to true; set it false only after reviewing the report."""
    filename = file.filename or "upload.csv"
    content = await file.read(5 * 1024 * 1024 + 1)
    try:
        return import_questions(db, content, file.content_type or "", filename, dry_run)
    except ImportFileError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Import was rolled back because the database rejected the batch. Resolve the conflict and retry.",
        ) from exc


@router.get("", response_model=QuestionListResponse, summary="Filter questions for management")
def get_questions(
    chapter_id: uuid.UUID | None = None,
    difficulty: Difficulty | None = None,
    is_pyq: bool | None = None,
    include_inactive: bool = False,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> QuestionListResponse:
    total, items = list_questions(db, chapter_id, difficulty, is_pyq, include_inactive, offset, limit)
    return QuestionListResponse(total=total, offset=offset, limit=limit, items=items)


@router.get("/{question_id}", response_model=QuestionManagementRead, summary="Get question details for management")
def get_question_details(
    question_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> Question:
    question = get_question(db, question_id)
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    return question


@router.put("/{question_id}", response_model=QuestionManagementRead, summary="Correct a managed question")
def correct_question(
    question_id: uuid.UUID,
    values: QuestionUpdate,
    db: Session = Depends(get_db),
) -> Question:
    question = get_question(db, question_id)
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    try:
        return update_question(db, question, values)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Question correction was rolled back") from exc


@router.patch("/{question_id}/status", response_model=QuestionManagementRead, summary="Activate or deactivate a question")
def set_question_status(
    question_id: uuid.UUID,
    values: QuestionStatusUpdate,
    db: Session = Depends(get_db),
) -> Question:
    question = get_question(db, question_id)
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    question.is_active = values.is_active
    try:
        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Question status update was rolled back") from exc
    db.refresh(question)
    return question
