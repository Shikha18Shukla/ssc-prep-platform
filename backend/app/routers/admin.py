"""Operator-only account administration."""

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_admin_user
from app.database.session import get_db
from app.models import AuthSession, User
from app.schemas.auth import AccountActivationUpdate
from app.security.rate_limit import enforce_rate_limit

router = APIRouter(
    prefix="/admin",
    tags=["Administration"],
    dependencies=[Depends(get_current_admin_user)],
)


@router.patch("/users/{user_id}/activation")
def update_user_activation(
    user_id: uuid.UUID,
    request: AccountActivationUpdate,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> dict[str, str | bool]:
    """Enable or disable an account and revoke all sessions on disable."""
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
        active_admins = db.scalar(
            select(func.count(User.id)).where(User.is_admin.is_(True), User.is_active.is_(True))
        ) or 0
        if active_admins <= 1:
            raise HTTPException(status_code=409, detail="The last active administrator cannot be deactivated")

    user.is_active = request.is_active
    if not request.is_active:
        db.execute(
            update(AuthSession)
            .where(AuthSession.user_id == user.id, AuthSession.revoked_at.is_(None))
            .values(revoked_at=datetime.now(timezone.utc))
        )
    db.commit()
    return {"id": str(user.id), "email": user.email, "is_active": user.is_active}
