"""Focused tests for beta admission, scoped catalog and shared rate limits."""

import hashlib

from fastapi import HTTPException
import pytest
from sqlalchemy import select

from app.auth.security import create_access_token
from app.models import BetaCapacity, BetaInvitation, RateLimitWindow, Subcategory, Chapter, Exam, Subject, User
from app.schemas.auth import BetaInvitationBatchRequest
from app.security.rate_limit import enforce_rate_limit
from app.services.auth_service import issue_beta_invitations
from app.services.catalog_service import (
    list_active_chapters_for_selection,
    list_active_exams,
    list_active_subjects,
    list_active_subcategories,
)
from app.services.beta_scope import chapter_is_in_beta


def _user(db_session, email: str, *, is_admin: bool = False) -> User:
    user = User(email=email, password_hash="fixture-only", is_active=True, is_admin=is_admin)
    db_session.add(user)
    db_session.commit()
    return user


def test_admin_invite_is_email_bound_one_time_and_hash_only(client, db_session, monkeypatch):
    from app.config import settings

    monkeypatch.setattr(settings, "BETA_INVITATIONS_REQUIRED", True)
    admin = _user(db_session, "beta-admin@example.test", is_admin=True)
    db_session.add(BetaCapacity(id=1, max_accounts=200))
    db_session.commit()
    headers = {"Authorization": f"Bearer {create_access_token(admin.id)}"}

    created = client.post(
        "/api/admin/invitations",
        headers=headers,
        json={"emails": ["approved.student@example.com"]},
    )
    assert created.status_code == 201, created.text
    code = created.json()["invitations"][0]["invitation_code"]
    stored = db_session.scalar(select(BetaInvitation).where(
        BetaInvitation.email == "approved.student@example.com",
    ))
    assert stored is not None
    assert stored.token_hash == hashlib.sha256(code.encode()).hexdigest()
    assert code not in stored.token_hash

    registered = client.post(
        "/api/auth/register",
        json={
            "full_name": "Approved Student",
            "email": "approved.student@example.com",
            "password": "SecurePassword123",
            "invitation_code": code,
        },
    )
    assert registered.status_code == 201, registered.text

    replay = client.post(
        "/api/auth/register",
        json={
            "full_name": "Another Student",
            "email": "approved.student@example.com",
            "password": "SecurePassword123",
            "invitation_code": code,
        },
    )
    assert replay.status_code == 403

    student = db_session.scalar(select(User).where(User.email == "approved.student@example.com"))
    disabled = client.patch(
        f"/api/admin/users/{student.id}/activation",
        headers=headers,
        json={"is_active": False},
    )
    assert disabled.status_code == 200
    assert disabled.json()["is_active"] is False
    access_token = create_access_token(student.id)
    profile = client.get("/api/auth/me", headers={"Authorization": f"Bearer {access_token}"})
    assert profile.status_code == 403


def test_beta_invitation_cap_reserves_pending_accounts(db_session):
    admin = _user(db_session, "capacity-admin@example.test", is_admin=True)
    db_session.add(BetaCapacity(id=1, max_accounts=2))
    db_session.commit()
    request = BetaInvitationBatchRequest(emails=["one@example.com"])
    first = issue_beta_invitations(db_session, request, admin.id)
    assert first["remaining_slots"] == 0
    with pytest.raises(HTTPException) as exc:
        issue_beta_invitations(
            db_session,
            BetaInvitationBatchRequest(emails=["two@example.com"]),
            admin.id,
        )
    assert exc.value.status_code == 409


def test_regular_student_cannot_issue_beta_invitations(client, db_session):
    student = _user(db_session, "ordinary-student@example.test")
    response = client.post(
        "/api/admin/invitations",
        headers={"Authorization": f"Bearer {create_access_token(student.id)}"},
        json={"emails": ["another.student@example.test"]},
    )
    assert response.status_code == 403


def test_database_rate_limit_returns_retry_after(db_session):
    enforce_rate_limit(db_session, "unit-test:identity", limit=1, window_seconds=60)
    with pytest.raises(HTTPException) as exc:
        enforce_rate_limit(db_session, "unit-test:identity", limit=1, window_seconds=60)
    assert exc.value.status_code == 429
    assert int(exc.value.headers["Retry-After"]) in range(1, 61)
    assert db_session.query(RateLimitWindow).count() == 1


def test_production_catalog_scope_only_exposes_math_reasoning_and_science(client, db_session, monkeypatch):
    from app.config import settings

    monkeypatch.setattr(settings, "BETA_CATALOG_SCOPE", True)
    exam = Exam(name="SSC", slug="ssc", is_active=True)
    db_session.add(exam)
    db_session.flush()
    subjects_by_slug = {}
    for slug, name in (("maths", "Maths"), ("reasoning", "Reasoning"), ("gk-gs", "GK / GS"), ("english", "English")):
        subject = Subject(exam_id=exam.id, name=name, slug=slug, is_active=True)
        db_session.add(subject)
        db_session.flush()
        subjects_by_slug[slug] = subject
    science = Subcategory(subject_id=subjects_by_slug["gk-gs"].id, name="Science", slug="science", is_active=True)
    computer = Subcategory(subject_id=subjects_by_slug["gk-gs"].id, name="Computer", slug="computer", is_active=True)
    db_session.add_all([science, computer])
    db_session.flush()
    science_chapter = Chapter(subject_id=science.subject_id, subcategory_id=science.id, name="Cell", slug="cell", is_active=True)
    computer_chapter = Chapter(subject_id=computer.subject_id, subcategory_id=computer.id, name="Basics", slug="basics", is_active=True)
    english_chapter = Chapter(subject_id=subjects_by_slug["english"].id, name="Parts of Speech", slug="parts-of-speech", is_active=True)
    db_session.add_all([science_chapter, computer_chapter, english_chapter])
    user = _user(db_session, "scope-student@example.test")
    db_session.commit()
    token = create_access_token(user.id)
    exams = list_active_exams(db_session)
    assert [exam.slug for exam in exams] == ["ssc"]
    subjects = list_active_subjects(db_session, exam.id)
    assert {subject.slug for subject in subjects} == {"maths", "reasoning", "gk-gs"}

    categories = list_active_subcategories(db_session, science.subject_id)
    assert [category.slug for category in categories] == ["science"]
    chapters = list_active_chapters_for_selection(db_session, science.subject_id)
    assert [chapter.slug for chapter in chapters] == ["cell"]

    response = client.post(
        "/api/tests",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "exam_id": str(exam.id),
            "subject_id": str(subjects_by_slug["english"].id),
            "test_type": "CHAPTER_WISE",
            "chapter_id": str(english_chapter.id),
            "difficulty": None,
            "question_count": 10,
        },
    )
    assert response.status_code == 404


def test_beta_chapter_scope_is_disabled_outside_production(monkeypatch):
    from app.config import settings

    monkeypatch.setattr(settings, "BETA_CATALOG_SCOPE", False)
    assert chapter_is_in_beta("ssc", "gk-gs", None)
    monkeypatch.setattr(settings, "BETA_CATALOG_SCOPE", True)
    assert chapter_is_in_beta("ssc", "gk-gs", "science")
    assert not chapter_is_in_beta("ssc", "gk-gs", None)


@pytest.mark.parametrize("origin", [
    "*",
    "https://example.com/path",
    "https://user@example.com",
    "https://example.com?redirect=elsewhere",
    "https://*.example.com",
    "https://example.com:bad",
    "http://example.com",
    "https://localhost",
])
def test_production_cors_requires_exact_https_origin(origin):
    from pydantic import ValidationError
    from app.config import Settings

    with pytest.raises(ValidationError):
        Settings(
            _env_file=None,
            ENVIRONMENT="production",
            SECRET_KEY="test-secret-key-that-is-long-enough-for-production",
            DATABASE_URL="postgresql+psycopg://app:password@db.example.net:5432/ssc?sslmode=verify-full",
            CORS_ORIGINS=[origin],
            BETA_INVITATIONS_REQUIRED=True,
            BETA_CATALOG_SCOPE=True,
        )
