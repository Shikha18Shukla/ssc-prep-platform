"""Operator-only beta invitations and account activation controls."""

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_admin_user
from app.database.session import get_db
from app.models import BetaCapacity, BetaInvitation, User
from app.schemas.auth import (
    AccountActivationUpdate,
    BetaInvitationBatchRequest,
    BetaInvitationBatchResponse,
)
from app.security.rate_limit import enforce_rate_limit
from app.services.auth_service import issue_beta_invitations

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
    db.delete(invitation)
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
