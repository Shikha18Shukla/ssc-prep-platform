"""Tests for authenticated catalog and practice availability endpoints."""

import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.auth.security import create_access_token
from app.database.seed import seed_database
from app.models import Chapter, Difficulty, Exam, Question, Subject, Subcategory, User


@pytest.fixture
def catalog_headers(db_session: Session) -> dict[str, str]:
    user = User(email="catalog@example.com", password_hash="not-used", is_active=True)
    db_session.add(user)
    db_session.commit()
    token = create_access_token(user_id=user.id)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def catalog_records(db_session: Session) -> dict[str, object]:
    exam = Exam(name="SSC", slug="ssc", is_active=True)
    inactive_exam = Exam(name="Railway", slug="railway", is_active=False)
    db_session.add_all([exam, inactive_exam])
    db_session.flush()

    subject = Subject(exam_id=exam.id, name="Maths", slug="maths", is_active=True)
    other_subject = Subject(
        exam_id=exam.id,
        name="Inactive subject",
        slug="inactive",
        is_active=False,
    )
    other_exam_subject = Subject(
        exam_id=inactive_exam.id,
        name="Railway Maths",
        slug="maths",
        is_active=True,
    )
    db_session.add_all([subject, other_subject, other_exam_subject])
    db_session.flush()

    category = Subcategory(
        subject_id=subject.id,
        name="Arithmetic Maths",
        slug="arithmetic-maths",
        display_order=1,
        is_active=True,
    )
    other_category = Subcategory(
        subject_id=subject.id,
        name="Advanced Maths",
        slug="advanced-maths",
        display_order=2,
        is_active=True,
    )
    inactive_category = Subcategory(
        subject_id=subject.id,
        name="Inactive category",
        slug="inactive-category",
        display_order=3,
        is_active=False,
    )
    db_session.add_all([category, other_category, inactive_category])
    db_session.flush()

    chapter = Chapter(
        subject_id=subject.id,
        subcategory_id=category.id,
        name="Arithmetic",
        slug="arithmetic",
        is_active=True,
    )
    unrelated_chapter = Chapter(
        subject_id=subject.id,
        subcategory_id=other_category.id,
        name="Geometry",
        slug="geometry",
        is_active=True,
    )
    inactive_chapter = Chapter(
        subject_id=subject.id,
        name="Hidden chapter",
        slug="hidden",
        is_active=False,
    )
    db_session.add_all([chapter, unrelated_chapter, inactive_chapter])
    db_session.flush()

    for index in range(4):
        db_session.add(
            Question(
                chapter_id=chapter.id,
                question_text=f"Easy {index}",
                difficulty=Difficulty.EASY,
                is_pyq=False,
                is_active=True,
            )
        )
        db_session.add(
            Question(
                chapter_id=chapter.id,
                question_text=f"PYQ {index}",
                difficulty=Difficulty.HARD,
                is_pyq=True,
                is_active=True,
            )
        )
    db_session.add(
        Question(
            chapter_id=chapter.id,
            question_text="Inactive easy question",
            difficulty=Difficulty.EASY,
            is_pyq=False,
            is_active=False,
        )
    )
    db_session.commit()

    return {
        "exam": exam,
        "inactive_exam": inactive_exam,
        "subject": subject,
        "other_subject": other_subject,
        "other_exam_subject": other_exam_subject,
        "category": category,
        "other_category": other_category,
        "inactive_category": inactive_category,
        "chapter": chapter,
        "unrelated_chapter": unrelated_chapter,
        "inactive_chapter": inactive_chapter,
    }


def test_catalog_requires_authentication(client: TestClient) -> None:
    response = client.get("/api/exams")
    assert response.status_code in (401, 403)


def test_lists_only_active_exams_subjects_and_chapters(
    client: TestClient,
    db_session: Session,
    catalog_headers: dict[str, str],
    catalog_records: dict[str, object],
) -> None:
    exams = client.get("/api/exams", headers=catalog_headers)
    assert exams.status_code == 200
    assert [item["slug"] for item in exams.json()] == ["ssc"]

    exam_id = str(catalog_records["exam"].id)
    subjects = client.get(f"/api/exams/{exam_id}/subjects", headers=catalog_headers)
    assert subjects.status_code == 200
    assert [item["slug"] for item in subjects.json()] == ["maths"]

    subject_id = str(catalog_records["subject"].id)
    categories = client.get(
        f"/api/exams/subjects/{subject_id}/subcategories", headers=catalog_headers
    )
    assert categories.status_code == 200
    assert [item["slug"] for item in categories.json()] == ["arithmetic-maths", "advanced-maths"]

    category_id = str(catalog_records["category"].id)
    chapters = client.get(
        f"/api/exams/subjects/{subject_id}/chapters",
        params={"subcategory_id": category_id},
        headers=catalog_headers,
    )
    assert chapters.status_code == 200
    assert [item["slug"] for item in chapters.json()] == ["arithmetic"]

    # Without a subcategory filter only direct subject chapters are returned.
    assert client.get(
        f"/api/exams/subjects/{subject_id}/chapters", headers=catalog_headers
    ).json() == []

    wrong_category_id = str(catalog_records["inactive_category"].id)
    assert client.get(
        f"/api/exams/subjects/{subject_id}/chapters",
        params={"subcategory_id": wrong_category_id},
        headers=catalog_headers,
    ).status_code == 404

    hidden_subject_id = str(catalog_records["other_exam_subject"].id)
    assert client.get(
        f"/api/exams/subjects/{hidden_subject_id}/chapters",
        headers=catalog_headers,
    ).status_code == 404
    assert db_session.scalar(select(func.count(Chapter.id))) == 3


def test_availability_separates_difficulty_from_pyq_and_validates_counts(
    client: TestClient,
    catalog_headers: dict[str, str],
    catalog_records: dict[str, object],
) -> None:
    chapter_id = str(catalog_records["chapter"].id)
    easy = client.get(
        f"/api/exams/chapters/{chapter_id}/availability",
        params={"level": "EASY"},
        headers=catalog_headers,
    )
    assert easy.status_code == 200
    assert easy.json()["available_question_count"] == 4
    assert easy.json()["allowed_question_counts"] == []

    pyq = client.get(
        f"/api/exams/chapters/{chapter_id}/availability",
        params={"level": "PYQ", "question_count": 10},
        headers=catalog_headers,
    )
    assert pyq.status_code == 200, pyq.text
    assert pyq.json()["available_question_count"] == 4
    assert pyq.json()["can_satisfy_request"] is False

    invalid_count = client.get(
        f"/api/exams/chapters/{chapter_id}/availability",
        params={"level": "EASY", "question_count": 11},
        headers=catalog_headers,
    )
    assert invalid_count.status_code == 422


def test_unknown_or_inactive_parent_ids_return_not_found(
    client: TestClient,
    catalog_headers: dict[str, str],
    catalog_records: dict[str, object],
) -> None:
    unknown_id = uuid.uuid4()
    assert client.get(
        f"/api/exams/{unknown_id}/subjects", headers=catalog_headers
    ).status_code == 404

    inactive_chapter_id = str(catalog_records["inactive_chapter"].id)
    assert client.get(
        f"/api/exams/chapters/{inactive_chapter_id}/availability",
        params={"level": "HARD"},
        headers=catalog_headers,
    ).status_code == 404


def test_seed_imports_catalog_idempotently_and_excludes_session_cards(db_session: Session) -> None:
    exam = Exam(name="Old name", slug="ssc", is_active=False)
    db_session.add(exam)
    db_session.flush()
    db_session.add(
        Subject(
            exam_id=exam.id,
            name="Old label",
            slug="gk-gs",
            is_active=False,
        )
    )
    db_session.commit()

    assert seed_database(db_session) == []
    first_ids = {
        (chapter.subcategory_id, chapter.slug): chapter.id
        for chapter in db_session.execute(select(Chapter)).scalars().all()
    }
    assert len(first_ids) == 196

    assert seed_database(db_session) == []
    seed_database(db_session)

    ssc_exam = db_session.execute(select(Exam).where(Exam.slug == "ssc")).scalar_one()
    assert ssc_exam.name == "SSC"
    assert ssc_exam.is_active is True
    subjects = db_session.execute(
        select(Subject).where(Subject.exam_id == ssc_exam.id).order_by(Subject.display_order)
    ).scalars().all()
    assert [subject.name for subject in subjects] == ["GK / GS", "Maths", "English", "Reasoning"]
    assert len({subject.slug for subject in subjects}) == 4
    assert all(subject.is_active for subject in subjects)
    assert db_session.scalar(select(func.count(Chapter.id))) == 196
    assert db_session.scalar(select(func.count(Subcategory.id))) == 9
    assert db_session.scalar(
        select(func.count(Chapter.id)).where(Chapter.name.in_([
            "Brain Storming Session - 1",
            "Brain Storming Session -2",
            "Brain Storming Session -3",
            "Doubt Session",
            "Practice Set",
            "Practice Set - 01",
            "Practice Set - 02",
        ]))
    ) == 0
    second_ids = {
        (chapter.subcategory_id, chapter.slug): chapter.id
        for chapter in db_session.execute(select(Chapter)).scalars().all()
    }
    assert second_ids == first_ids
    assert db_session.scalar(select(func.count(Question.id))) == 0


def test_seed_preserves_question_bearing_legacy_chapters_for_manual_reconciliation(
    db_session: Session,
) -> None:
    exam = Exam(name="SSC", slug="ssc", is_active=True)
    db_session.add(exam)
    db_session.flush()
    subject = Subject(exam_id=exam.id, name="GK / GS", slug="gk-gs", is_active=True)
    db_session.add(subject)
    db_session.flush()
    legacy_chapter = Chapter(
        subject_id=subject.id,
        name="Cell",
        slug="cell",
        display_order=1,
        is_active=True,
    )
    db_session.add(legacy_chapter)
    db_session.flush()
    question = Question(
        chapter_id=legacy_chapter.id,
        question_text="Existing question",
        difficulty=Difficulty.EASY,
        is_pyq=False,
        is_active=True,
    )
    db_session.add(question)
    db_session.commit()

    conflicts = seed_database(db_session)

    db_session.refresh(legacy_chapter)
    assert legacy_chapter.subcategory_id is None
    assert db_session.get(Question, question.id).chapter_id == legacy_chapter.id
    assert any("Cell" in conflict and "questions=1" in conflict for conflict in conflicts)
    science = db_session.execute(
        select(Subcategory).where(
            Subcategory.subject_id == subject.id,
            Subcategory.slug == "science",
        )
    ).scalar_one()
    assert db_session.execute(
        select(Chapter).where(
            Chapter.subcategory_id == science.id,
            Chapter.slug == "cell",
        )
    ).scalar_one_or_none() is None
