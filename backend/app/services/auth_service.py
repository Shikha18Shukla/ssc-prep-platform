"""Authentication, beta invitation, and account access business logic."""

from datetime import datetime, timedelta, timezone
import hashlib
import secrets

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.security import hash_password, verify_password, verify_unknown_user_password
from app.config import settings
from app.models import BetaCapacity, BetaInvitation, User
from app.schemas.auth import (
    BetaInvitationBatchRequest,
    GenericInvitationBatchRequest,
    LoginRequest,
    RegisterRequest,
)


def _capacity_row(db: Session) -> BetaCapacity:
    query = select(BetaCapacity).where(BetaCapacity.id == 1)
    if db.bind.dialect.name == "postgresql":
        query = query.with_for_update()
    capacity = db.execute(query).scalar_one_or_none()
    if capacity is None:
        raise HTTPException(status_code=503, detail="Beta registration is not configured")
    return capacity


def issue_beta_invitations(
    db: Session,
    request: BetaInvitationBatchRequest,
    admin_user_id,
) -> dict:
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(days=request.expires_in_days)
    emails = [str(email).lower() for email in request.emails]
    try:
        capacity = _capacity_row(db)
        accounts = db.scalar(select(func.count(User.id))) or 0
        pending_query = select(func.count(BetaInvitation.id)).where(
            BetaInvitation.redeemed_at.is_(None), BetaInvitation.expires_at > now,
            BetaInvitation.revoked_at.is_(None),
        )
        pending = db.scalar(pending_query) or 0
        already_registered = set(db.scalars(select(User.email).where(User.email.in_(emails))).all())
        already_invited = set(db.scalars(select(BetaInvitation.email).where(
            BetaInvitation.email.in_(emails),
            BetaInvitation.redeemed_at.is_(None),
            BetaInvitation.expires_at > now,
            BetaInvitation.revoked_at.is_(None),
        )).all())
        duplicates = already_registered | already_invited
        if duplicates:
            raise HTTPException(status_code=409, detail="One or more addresses already have an account or pending invitation")
        if accounts + pending + len(emails) > capacity.max_accounts:
            raise HTTPException(status_code=409, detail="The 200-account beta capacity is full")

        created = []
        for email in emails:
            code = secrets.token_urlsafe(32)
            invitation = BetaInvitation(
                email=email,
                token_hash=hashlib.sha256(code.encode("utf-8")).hexdigest(),
                expires_at=expires_at,
                created_by_user_id=admin_user_id,
            )
            db.add(invitation)
            created.append({"email": email, "invitation_code": code, "expires_at": expires_at})
        db.commit()
        return {
            "invitations": created,
            "total_accounts": accounts,
            "pending_invitations": pending + len(created),
            "remaining_slots": capacity.max_accounts - accounts - pending - len(created),
        }
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise


def issue_generic_invitations(
    db: Session,
    request: GenericInvitationBatchRequest,
    admin_user_id,
) -> dict:
    """Create a reserved batch of high-entropy, email-independent codes.

    Plaintext is returned only in this creation response. Only SHA-256 digests
    of 256-bit random tokens are persisted.
    """
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(days=request.expires_in_days)
    try:
        # Serializes generation and registration capacity decisions on PostgreSQL.
        capacity = _capacity_row(db)
        accounts = db.scalar(select(func.count(User.id))) or 0
        pending = db.scalar(select(func.count(BetaInvitation.id)).where(
            BetaInvitation.redeemed_at.is_(None),
            BetaInvitation.expires_at > now,
            BetaInvitation.revoked_at.is_(None),
        )) or 0
        if accounts + pending + request.count > capacity.max_accounts:
            raise HTTPException(status_code=409, detail="The 200-account beta capacity is full")

        created = []
        plaintext_codes: list[tuple[BetaInvitation, str]] = []
        batch_hashes: set[str] = set()
        for _ in range(request.count):
            code = secrets.token_urlsafe(32)
            token_hash = hashlib.sha256(code.encode("utf-8")).hexdigest()
            while token_hash in batch_hashes:
                code = secrets.token_urlsafe(32)
                token_hash = hashlib.sha256(code.encode("utf-8")).hexdigest()
            batch_hashes.add(token_hash)
            invitation = BetaInvitation(
                email=None,
                token_hash=token_hash,
                expires_at=expires_at,
                created_by_user_id=admin_user_id,
            )
            db.add(invitation)
            plaintext_codes.append((invitation, code))

        db.flush()
        for invitation, code in plaintext_codes:
            created.append({
                "id": invitation.id,
                "invitation_code": code,
                "expires_at": expires_at,
            })
        db.commit()
        return {
            "invitations": created,
            "expires_at": expires_at,
            "total_accounts": accounts,
            "pending_invitations": pending + len(created),
            "remaining_slots": capacity.max_accounts - accounts - pending - len(created),
        }
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise


def register_user(db: Session, request: RegisterRequest) -> User:
    """Register a new user account.

    Args:
        db: Active database session.
        request: Validated registration payload.

    Returns:
        User: Newly created User instance.

    Raises:
        HTTPException 409: If an account with the specified email already exists.
    """
    invitation = None
    now = datetime.now(timezone.utc)
    try:
        if settings.BETA_INVITATIONS_REQUIRED:
            if not request.invitation_code:
                raise HTTPException(status_code=403, detail="A valid beta invitation is required")
            token_hash = hashlib.sha256(request.invitation_code.encode("utf-8")).hexdigest()
            invitation_query = select(BetaInvitation).where(BetaInvitation.token_hash == token_hash)
            if db.bind.dialect.name == "postgresql":
                invitation_query = invitation_query.with_for_update()
            invitation = db.execute(invitation_query).scalar_one_or_none()
            invitation_expires = invitation.expires_at if invitation is not None else None
            if invitation_expires is not None and invitation_expires.tzinfo is None:
                invitation_expires = invitation_expires.replace(tzinfo=timezone.utc)
            if (invitation is None
                    or (invitation.email is not None and invitation.email != request.email)
                    or invitation.revoked_at is not None
                    or invitation.redeemed_at is not None
                    or invitation_expires is None
                    or invitation_expires <= now):
                raise HTTPException(status_code=403, detail="A valid beta invitation is required")
            capacity = _capacity_row(db)
            account_count = db.scalar(select(func.count(User.id))) or 0
            if account_count >= capacity.max_accounts:
                raise HTTPException(status_code=409, detail="The 200-account beta capacity is full")

        existing_user = db.execute(select(User).where(User.email == request.email)).scalar_one_or_none()
        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists",
            )

        user = User(
            email=request.email,
            full_name=request.full_name,
            password_hash=hash_password(request.password),
            is_active=True,
        )
        db.add(user)
        if invitation is not None:
            db.flush()
            invitation.redeemed_at = now
            invitation.redeemed_by_user_id = user.id
        db.commit()
        db.refresh(user)
        return user
    except HTTPException:
        db.rollback()
        raise
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account could not be created because the email address is already registered",
        ) from exc
    except Exception:
        db.rollback()
        raise


def authenticate_user(db: Session, request: LoginRequest) -> User:
    """Authenticate an existing user via email and password.

    Args:
        db: Active database session.
        request: Validated login payload.

    Returns:
        User: Authenticated User instance.

    Raises:
        HTTPException 401: If email does not exist or password does not match.
        HTTPException 403: If the user's account is inactive.
    """
    stmt = select(User).where(User.email == request.email)
    user = db.execute(stmt).scalar_one_or_none()

    invalid_credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if user is None:
        verify_unknown_user_password(request.password)
        raise invalid_credentials_exception

    if not verify_password(request.password, user.password_hash):
        raise invalid_credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return user
