"""Focused service and handler tests for email-independent beta codes."""

from datetime import datetime, timedelta, timezone
import hashlib
import uuid

import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_admin_user
from app.auth.security import hash_password
from app.config import settings
from app.models import BetaCapacity, BetaInvitation, User
from app.routers.admin import (
    create_generic_invitations,
    list_generic_invitations,
    read_generic_invitation_summary,
    revoke_invitation,
)
from app.schemas.auth import (
    BetaInvitationBatchRequest,
    GenericInvitationBatchRequest,
    GenericInvitationBatchResponse,
    RegisterRequest,
)
from app.services.auth_service import issue_beta_invitations, issue_generic_invitations, register_user


def _admin(db: Session, max_accounts: int = 200) -> User:
    db.add(BetaCapacity(id=1, max_accounts=max_accounts))
    admin = User(
        email="bulk-admin@example.com",
        full_name="Beta Admin",
        password_hash=hash_password("AdminPassword123"),
        is_active=True,
        is_admin=True,
    )
    db.add(admin)
    db.commit()
    return admin


def _generate_50(db: Session, admin: User) -> dict:
    payload = create_generic_invitations(GenericInvitationBatchRequest(), admin, db)
    return GenericInvitationBatchResponse.model_validate(payload).model_dump(mode="json")


def _register(code: str, email: str) -> RegisterRequest:
    return RegisterRequest(
        full_name="Beta Student",
        email=email,
        password="StudentPass123",
        invitation_code=code,
    )


def test_batch_request_is_fixed_at_50_and_expiry_is_bounded():
    assert GenericInvitationBatchRequest().count == 50
    with pytest.raises(ValidationError):
        GenericInvitationBatchRequest(count=49)
    with pytest.raises(ValidationError):
        GenericInvitationBatchRequest(expires_in_days=31)


def test_bulk_codes_are_unique_hashed_reserved_and_plaintext_only_in_creation_response(db_session: Session):
    admin = _admin(db_session)

    response = _generate_50(db_session, admin)

    codes = [row["invitation_code"] for row in response["invitations"]]
    assert len(codes) == 50
    assert len(set(codes)) == 50
    assert all(len(code) >= 40 for code in codes)
    invitations = db_session.execute(select(BetaInvitation)).scalars().all()
    hashes = {item.token_hash for item in invitations}
    assert len(hashes) == 50
    assert all(item.email is None and item.revoked_at is None for item in invitations)
    assert hashes == {hashlib.sha256(code.encode()).hexdigest() for code in codes}
    assert all(code not in item.token_hash for code in codes for item in invitations)
    assert response["pending_invitations"] == 50
    assert response["remaining_slots"] == 149
    public_listing = list_generic_invitations(
        limit=200, offset=0, invitation_status="available", current_admin=admin, db=db_session
    )
    assert len(public_listing) == 50
    assert all("token_hash" not in item and "invitation_code" not in item for item in public_listing)


def test_generic_code_registers_any_email_and_is_redeemed_once(db_session: Session, monkeypatch):
    monkeypatch.setattr(settings, "BETA_INVITATIONS_REQUIRED", True)
    admin = _admin(db_session)
    code = _generate_50(db_session, admin)["invitations"][0]["invitation_code"]

    user = register_user(db_session, _register(code, "student.one@example.com"))
    assert user.email == "student.one@example.com" and user.is_admin is False
    invitation = db_session.execute(select(BetaInvitation).where(
        BetaInvitation.token_hash == hashlib.sha256(code.encode()).hexdigest()
    )).scalar_one()
    assert invitation.email is None and invitation.redeemed_at is not None

    with pytest.raises(HTTPException) as replay:
        register_user(db_session, _register(code, "student.two@example.com"))
    assert replay.value.status_code == 403


def test_failed_registration_does_not_consume_generic_code(db_session: Session, monkeypatch):
    monkeypatch.setattr(settings, "BETA_INVITATIONS_REQUIRED", True)
    admin = _admin(db_session)
    code = _generate_50(db_session, admin)["invitations"][0]["invitation_code"]
    db_session.add(User(
        email="already-used@example.com",
        full_name="Existing",
        password_hash=hash_password("ExistingPass123"),
        is_active=True,
    ))
    db_session.commit()

    with pytest.raises(HTTPException) as failed:
        register_user(db_session, _register(code, "already-used@example.com"))
    assert failed.value.status_code == 409
    invitation = db_session.execute(select(BetaInvitation).where(
        BetaInvitation.token_hash == hashlib.sha256(code.encode()).hexdigest()
    )).scalar_one()
    assert invitation.redeemed_at is None

    user = register_user(db_session, _register(code, "valid-student@example.com"))
    assert user.email == "valid-student@example.com"
    assert invitation.redeemed_at is not None


def test_expiry_revocation_and_status_counts(db_session: Session, monkeypatch):
    monkeypatch.setattr(settings, "BETA_INVITATIONS_REQUIRED", True)
    admin = _admin(db_session)
    response = _generate_50(db_session, admin)
    issued = response["invitations"]
    expired_id, revoked_id = uuid.UUID(issued[0]["id"]), uuid.UUID(issued[1]["id"])
    expired_code, revoked_code = issued[0]["invitation_code"], issued[1]["invitation_code"]
    expired = db_session.get(BetaInvitation, expired_id)
    expired.expires_at = datetime.now(timezone.utc) - timedelta(seconds=1)
    db_session.commit()

    assert revoke_invitation(revoked_id, admin, db_session) == {"revoked": True}
    for code, email in ((expired_code, "expired@example.com"), (revoked_code, "revoked@example.com")):
        with pytest.raises(HTTPException) as rejected:
            register_user(db_session, _register(code, email))
        assert rejected.value.status_code == 403

    assert read_generic_invitation_summary(current_admin=admin, db=db_session) == {
        "available": 48, "redeemed": 0, "expired": 1, "revoked": 1,
    }
    listed = db_session.execute(select(BetaInvitation.token_hash)).scalars().all()
    assert all(code not in listed for code in (expired_code, revoked_code))


def test_admin_guard_and_capacity_reservation(db_session: Session):
    admin = _admin(db_session, max_accounts=50)
    student = User(
        email="ordinary@example.com",
        full_name="Student",
        password_hash=hash_password("StudentPass123"),
        is_active=True,
        is_admin=False,
    )
    db_session.add(student)
    db_session.commit()

    assert get_current_admin_user(admin) is admin
    with pytest.raises(HTTPException) as denied:
        get_current_admin_user(student)
    assert denied.value.status_code == 403

    with pytest.raises(HTTPException) as full:
        issue_generic_invitations(db_session, GenericInvitationBatchRequest(), admin.id)
    assert full.value.status_code == 409
    assert db_session.scalar(select(func.count(BetaInvitation.id))) == 0


def test_existing_email_bound_invitation_keeps_email_matching_behavior(db_session: Session, monkeypatch):
    monkeypatch.setattr(settings, "BETA_INVITATIONS_REQUIRED", True)
    admin = _admin(db_session)
    response = issue_beta_invitations(
        db_session,
        BetaInvitationBatchRequest(emails=["bound@example.com"], expires_in_days=14),
        admin.id,
    )
    code = response["invitations"][0]["invitation_code"]
    with pytest.raises(HTTPException) as wrong_email:
        register_user(db_session, _register(code, "other@example.com"))
    assert wrong_email.value.status_code == 403
    assert register_user(db_session, _register(code, "bound@example.com")).email == "bound@example.com"
