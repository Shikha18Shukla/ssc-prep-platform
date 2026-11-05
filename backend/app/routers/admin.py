"""Operator-only beta invitations and account activation controls."""

import uuid
from datetime import datetime, timezone
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_admin_user
from app.database.session import get_db
from app.models import BetaCapacity, BetaInvitation, User
from app.schemas.auth import (
    AccountActivationUpdate,
    BetaInvitationBatchRequest,
    BetaInvitationBatchResponse,
    GenericInvitationBatchRequest,
    GenericInvitationBatchResponse,
    GenericInvitationListItem,
    GenericInvitationStatus,
)
from app.security.rate_limit import enforce_rate_limit
from app.services.auth_service import issue_beta_invitations, issue_generic_invitations

router = APIRouter(
    prefix="/admin",
    tags=["Administration"],
    dependencies=[Depends(get_current_admin_user)],
)


@router.get("/beta-capacity")
def read_beta_capacity(db: Session = Depends(get_db)) -> dict[str, int]:
    capacity = db.get(BetaCapacity, 1)
    if capacity is None:
        raise HTTPException(status_code=503, detail="Beta registration is not configured")
    accounts = db.scalar(select(func.count(User.id))) or 0
    pending = db.scalar(select(func.count(BetaInvitation.id)).where(
        BetaInvitation.redeemed_at.is_(None),
        BetaInvitation.expires_at > datetime.now(timezone.utc),
        BetaInvitation.revoked_at.is_(None),
    )) or 0
    return {
        "max_accounts": capacity.max_accounts,
        "total_accounts": accounts,
        "pending_invitations": pending,
        "remaining_slots": max(0, capacity.max_accounts - accounts - pending),
    }


@router.post(
    "/invitations",
    response_model=BetaInvitationBatchResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_invitations(
    request: BetaInvitationBatchRequest,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> dict:
    enforce_rate_limit(db, f"admin-invitations:user:{current_admin.id}", limit=10, window_seconds=3600)
    return issue_beta_invitations(db, request, current_admin.id)


@router.post(
    "/invitations/bulk",
    response_model=GenericInvitationBatchResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_generic_invitations(
    request: GenericInvitationBatchRequest,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> dict:
    enforce_rate_limit(db, f"admin-generic-invitations:user:{current_admin.id}", limit=5, window_seconds=3600)
    return issue_generic_invitations(db, request, current_admin.id)


def _generic_invitation_state(invitation: BetaInvitation, now: datetime) -> str:
    if invitation.revoked_at is not None:
        return "revoked"
    if invitation.redeemed_at is not None:
        return "redeemed"
    expires_at = invitation.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at <= now:
        return "expired"
    return "available"


@router.get("/invitations/generic/summary", response_model=GenericInvitationStatus)
def read_generic_invitation_summary(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> dict[str, int]:
    enforce_rate_limit(
        db, f"admin-generic-invitation-summary:user:{current_admin.id}", limit=60, window_seconds=3600
    )
    now = datetime.now(timezone.utc)
    rows = db.execute(select(BetaInvitation).where(BetaInvitation.email.is_(None))).scalars()
    counts = {state: 0 for state in ("available", "redeemed", "expired", "revoked")}
    for invitation in rows:
        counts[_generic_invitation_state(invitation, now)] += 1
    return counts


@router.get("/invitations/generic", response_model=list[GenericInvitationListItem])
def list_generic_invitations(
    limit: int = 100,
    offset: int = 0,
    invitation_status: Literal["available", "redeemed", "expired", "revoked"] = Query(
        default="available", alias="status"
    ),
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> list[dict]:
    enforce_rate_limit(
        db, f"admin-generic-invitation-list:user:{current_admin.id}", limit=60, window_seconds=3600
    )
    if limit < 1 or limit > 200 or offset < 0:
        raise HTTPException(status_code=422, detail="Invalid invitation page")
    now = datetime.now(timezone.utc)
    query = select(BetaInvitation).where(BetaInvitation.email.is_(None))
    if invitation_status == "available":
        query = query.where(
            BetaInvitation.redeemed_at.is_(None), BetaInvitation.revoked_at.is_(None),
            BetaInvitation.expires_at > now,
        )
    elif invitation_status == "redeemed":
        query = query.where(BetaInvitation.redeemed_at.is_not(None), BetaInvitation.revoked_at.is_(None))
    elif invitation_status == "expired":
        query = query.where(
            BetaInvitation.redeemed_at.is_(None), BetaInvitation.revoked_at.is_(None),
            BetaInvitation.expires_at <= now,
        )
    else:
        query = query.where(BetaInvitation.revoked_at.is_not(None))
    rows = db.execute(
        query
        .order_by(BetaInvitation.created_at.desc(), BetaInvitation.id)
        .limit(limit)
        .offset(offset)
    ).scalars()
    return [
        {
            "id": invitation.id,
            "status": _generic_invitation_state(invitation, now),
            "expires_at": invitation.expires_at,
            "redeemed_at": invitation.redeemed_at,
            "revoked_at": invitation.revoked_at,
            "created_at": invitation.created_at,
        }
        for invitation in rows
    ]


@router.delete("/invitations/{invitation_id}")
def revoke_invitation(
    invitation_id: uuid.UUID,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> dict[str, bool]:
    enforce_rate_limit(db, f"admin-invitations:user:{current_admin.id}", limit=10, window_seconds=3600)
    query = select(BetaInvitation).where(BetaInvitation.id == invitation_id)
    if db.bind.dialect.name == "postgresql":
        query = query.with_for_update()
    invitation = db.execute(query).scalar_one_or_none()
    if invitation is None:
        raise HTTPException(status_code=404, detail="Invitation not found")
    if invitation.redeemed_at is not None:
        raise HTTPException(status_code=409, detail="A redeemed invitation cannot be revoked")
    if invitation.revoked_at is not None:
        raise HTTPException(status_code=409, detail="Invitation is already revoked")
    invitation.revoked_at = datetime.now(timezone.utc)
    db.commit()
    return {"revoked": True}


@router.patch("/users/{user_id}/activation")
def update_user_activation(
    user_id: uuid.UUID,
    request: AccountActivationUpdate,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> dict[str, str | bool]:
    enforce_rate_limit(db, f"admin-activation:user:{current_admin.id}", limit=30, window_seconds=3600)
    if user_id == current_admin.id and not request.is_active:
        raise HTTPException(status_code=409, detail="Administrators cannot deactivate their own account")
    query = select(User).where(User.id == user_id)
    if db.bind.dialect.name == "postgresql":
        query = query.with_for_update()
    user = db.execute(query).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Account not found")
    if user.is_admin and not request.is_active:
        active_admins = db.scalar(select(func.count(User.id)).where(User.is_admin.is_(True), User.is_active.is_(True))) or 0
        if active_admins <= 1:
            raise HTTPException(status_code=409, detail="The last active administrator cannot be deactivated")
    user.is_active = request.is_active
    db.commit()
    return {"id": str(user.id), "email": user.email, "is_active": user.is_active}
