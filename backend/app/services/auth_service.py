"""Authentication service containing signup and login business logic."""

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.security import hash_password, verify_password
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest


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
    stmt = select(User).where(User.email == request.email)
    existing_user = db.execute(stmt).scalar_one_or_none()

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
    db.commit()
    db.refresh(user)
    return user


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
        raise invalid_credentials_exception

    if not verify_password(request.password, user.password_hash):
        raise invalid_credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return user
