"""Authentication API router."""

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.security import create_access_token
from app.database.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.security.rate_limit import enforce_rate_limit
from app.services.auth_service import authenticate_user, register_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Registers a new user account with normalized email, strong password validation, and secure password hashing.",
)
def register(
    request: RegisterRequest,
    http_request: Request,
    db: Session = Depends(get_db),
) -> UserResponse:
    """Create a new user account."""
    client_ip = http_request.client.host if http_request.client else "unknown"
    enforce_rate_limit(db, f"register:ip:{client_ip}", limit=200, window_seconds=3600)
    user = register_user(db=db, request=request)
    return UserResponse.model_validate(user)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate user and obtain JWT token",
    description="Validates email and password, checks active status, and returns a signed JWT access token.",
)
def login(
    request: LoginRequest,
    http_request: Request,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Authenticate and issue JWT access token."""
    client_ip = http_request.client.host if http_request.client else "unknown"
    enforce_rate_limit(db, f"login:ip:{client_ip}", limit=100, window_seconds=600)
    enforce_rate_limit(db, f"login:email:{request.email}", limit=8, window_seconds=1800)
    user = authenticate_user(db=db, request=request)
    access_token = create_access_token(user_id=user.id)
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    description="Returns the currently authenticated user's safe profile. Requires a valid Bearer token.",
)
def get_me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Retrieve currently authenticated user's profile."""
    return UserResponse.model_validate(current_user)
