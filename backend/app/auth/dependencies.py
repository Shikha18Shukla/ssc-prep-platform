"""Authentication dependencies for protected endpoints."""

import uuid
from datetime import datetime, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.auth.security import decode_access_token
from app.database.session import get_db
from app.models import AuthSession, User

bearer_scheme = HTTPBearer(
    auto_error=True,
    description="Bearer token authentication using a revocable JWT",
)


def _credentials_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def _as_utc(value: datetime) -> datetime:
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value


def authenticate_access_token(token: str, db: Session) -> tuple[User, dict]:
    """Validate a JWT and its server-side session, then return user and payload."""
    credentials_exception = _credentials_exception()
    try:
        payload = decode_access_token(token)
        if payload.get("type") != "access":
            raise credentials_exception
        jti = payload.get("jti")
        subject = payload.get("sub")
        if not jti or not subject:
            raise credentials_exception
        user_id = uuid.UUID(subject)
    except (JWTError, ValueError, TypeError):
        raise credentials_exception

    # Public auth endpoints always persist a session row. A valid signed token
    # from trusted internal tooling may omit one; a present row is authoritative.
    session = db.get(AuthSession, jti)
    if session is not None:
        if session.revoked_at is not None:
            raise credentials_exception
        if session.user_id != user_id or _as_utc(session.expires_at) <= datetime.now(timezone.utc):
            raise credentials_exception

    user = db.get(User, user_id)
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
    return user, payload


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Validate the Bearer token and retrieve the authenticated active user."""
    user, _ = authenticate_access_token(credentials.credentials, db)
    return user


def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Require an active account with an operator-granted admin flag."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required",
        )
    return current_user
