"""Email/password authentication, sessions, and password recovery logic."""

from datetime import datetime, timedelta, timezone
from urllib.parse import quote

from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    secure_url_token,
    sha256_hex,
    verify_password,
    verify_unknown_user_password,
)
from app.config import settings
from app.models import AuthSession, PasswordResetToken, User
from app.schemas.auth import (
    LoginRequest,
    PasswordResetConfirm,
    PasswordResetRequest,
    RegisterRequest,
)
from app.services.email_service import EmailDeliveryError, get_email_sender


_INVALID_CREDENTIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid email or password",
    headers={"WWW-Authenticate": "Bearer"},
)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _as_utc(value: datetime) -> datetime:
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value


def _user_by_email(db: Session, email: str) -> User | None:
    normalized = email.strip().lower()
    return db.execute(
        select(User).where(User.email_normalized == normalized)
    ).scalar_one_or_none()


def issue_session(db: Session, user: User) -> tuple[str, datetime]:
    """Create a signed access token and its revocable server-side session."""
    token = create_access_token(user.id)
    payload = decode_access_token(token)
    expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    db.add(AuthSession(id=payload["jti"], user_id=user.id, expires_at=expires_at))
    db.commit()
    return token, expires_at


def revoke_user_sessions(db: Session, user_id, commit: bool = True) -> None:
    """Revoke every active session for a user (password change/deactivation)."""
    db.execute(
        update(AuthSession)
        .where(AuthSession.user_id == user_id, AuthSession.revoked_at.is_(None))
        .values(revoked_at=_now())
    )
    if commit:
        db.commit()


def register_user(db: Session, request: RegisterRequest) -> User:
    """Create a password-based account with a normalized unique email."""
    email = str(request.email).strip().lower()
    now = _now()
    if _user_by_email(db, email) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )

    user = User(
        email=email,
        full_name=request.full_name,
        password_hash=hash_password(request.password),
        password_changed_at=now,
        is_active=True,
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        ) from exc
    except Exception:
        db.rollback()
        raise


def authenticate_user(db: Session, request: LoginRequest) -> User:
    """Verify email/password credentials with uniform failure responses."""
    user = _user_by_email(db, str(request.email))
    if user is None or not user.password_hash:
        verify_unknown_user_password(request.password)
        raise _INVALID_CREDENTIALS
    password_valid = verify_password(request.password, user.password_hash)
    if not password_valid or not user.is_active:
        # Inactive accounts use the same response as every other credential
        # failure so login cannot be used to enumerate existing accounts.
        raise _INVALID_CREDENTIALS
    return user


def create_password_reset_token(db: Session, user: User) -> str:
    """Store a hashed, single-use recovery token and return plaintext once."""
    now = _now()
    db.execute(
        update(PasswordResetToken)
        .where(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.used_at.is_(None),
            PasswordResetToken.revoked_at.is_(None),
        )
        .values(revoked_at=now)
    )
    for _ in range(3):
        plaintext = secure_url_token(32)
        token_hash = sha256_hex(plaintext)
        if db.scalar(select(PasswordResetToken.id).where(
            PasswordResetToken.token_hash == token_hash
        )) is not None:
            continue
        db.add(PasswordResetToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=now + timedelta(seconds=settings.PASSWORD_RESET_TTL_SECONDS),
        ))
        db.commit()
        return plaintext
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Password setup is temporarily unavailable",
    )


def request_password_reset(
    db: Session,
    request: PasswordResetRequest,
    sender=None,
) -> tuple[bool, bool]:
    """Deliver a recovery link when a provider is configured.

    Returns `(provider_configured, delivered)`; callers choose a deliberately
    non-enumerating response and never expose the token themselves.
    """
    if settings.EMAIL_PROVIDER != "smtp":
        return False, False

    provider = sender or get_email_sender()
    user = _user_by_email(db, str(request.email))
    if user is None:
        return True, True

    plaintext = create_password_reset_token(db, user)
    reset_url = f"{settings.PASSWORD_RESET_URL.rstrip('/')}?token={quote(plaintext)}"
    try:
        delivered = provider.send_password_reset(str(user.email), reset_url)
    except EmailDeliveryError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Password setup delivery is temporarily unavailable",
        ) from exc
    return True, bool(delivered)


def confirm_password_reset(db: Session, request: PasswordResetConfirm) -> User:
    """Consume a valid reset token, set a new hash, and revoke old sessions."""
    token_hash = sha256_hex(request.token.strip())
    query = select(PasswordResetToken).where(PasswordResetToken.token_hash == token_hash)
    if db.bind.dialect.name == "postgresql":
        query = query.with_for_update()
    record = db.execute(query).scalar_one_or_none()

    invalid = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid or expired password setup link",
    )
    if record is None or record.used_at is not None or record.revoked_at is not None:
        raise invalid
    if _as_utc(record.expires_at) <= _now():
        raise invalid

    user = db.get(User, record.user_id)
    if user is None or not user.is_active:
        raise invalid

    now = _now()
    try:
        user.password_hash = hash_password(request.new_password)
        user.password_changed_at = now
        record.used_at = now
        db.execute(
            update(PasswordResetToken)
            .where(
                PasswordResetToken.user_id == user.id,
                PasswordResetToken.used_at.is_(None),
            )
            .values(revoked_at=now)
        )
        revoke_user_sessions(db, user.id, commit=False)
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        raise
