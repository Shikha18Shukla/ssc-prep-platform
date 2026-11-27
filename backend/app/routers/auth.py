"""Authentication API router."""

from datetime import datetime, timezone
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.auth.dependencies import (
    authenticate_access_token,
    bearer_scheme,
    get_current_user,
)
from app.auth.security import sha256_hex
from app.config import settings
from app.database.session import get_db
from app.models import AuthSession, User
from app.schemas.auth import (
    GoogleExchangeRequest,
    GoogleStartResponse,
    LoginRequest,
    MessageResponse,
    PasswordResetConfirm,
    PasswordResetRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.security.rate_limit import enforce_rate_limit
from app.services.auth_service import (
    authenticate_user,
    confirm_password_reset,
    issue_session,
    register_user,
    request_password_reset,
)
from app.services.google_auth_service import (
    GOOGLE_COOKIE_NAME,
    GoogleAuthError,
    build_authorization_url,
    complete_google_callback,
    exchange_google_code,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


def _client_ip(http_request: Request) -> str:
    return http_request.client.host if http_request.client else "unknown"


def _rate_limit_email(email: str) -> str:
    """Use the same normalized identity as account storage for rate limits."""
    return str(email).strip().lower()


def _redirect_with_query(base: str, params: dict[str, str]) -> str:
    parts = urlsplit(base)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query.update(params)
    return urlunsplit((
        parts.scheme,
        parts.netloc,
        parts.path,
        urlencode(query),
        parts.fragment,
    ))


def _set_oauth_cookie(response: Response, browser_key: str) -> None:
    response.set_cookie(
        key=GOOGLE_COOKIE_NAME,
        value=browser_key,
        # The exchange code is created at callback time, so the browser cookie
        # must outlive both the state used there and the later code exchange.
        max_age=settings.GOOGLE_STATE_TTL_SECONDS + settings.GOOGLE_EXCHANGE_TTL_SECONDS,
        httponly=True,
        secure=settings.GOOGLE_COOKIE_SECURE,
        samesite=settings.GOOGLE_COOKIE_SAMESITE,
        path="/api/auth/google",
    )


def _clear_oauth_cookie(response: Response) -> None:
    response.delete_cookie(
        key=GOOGLE_COOKIE_NAME,
        path="/api/auth/google",
        secure=settings.GOOGLE_COOKIE_SECURE,
        samesite=settings.GOOGLE_COOKIE_SAMESITE,
    )


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an email/password account",
    description="Validates a unique normalized email and password confirmation, hashes the password, and starts a session.",
)
def register(
    request: RegisterRequest,
    http_request: Request,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Create a new user account and issue a revocable session token."""
    enforce_rate_limit(
        db, f"register:ip:{_client_ip(http_request)}", limit=20, window_seconds=3600
    )
    enforce_rate_limit(
        db, f"register:email:{_rate_limit_email(request.email)}", limit=5, window_seconds=3600
    )
    user = register_user(db=db, request=request)
    token, _ = issue_session(db, user)
    return TokenResponse(access_token=token, user=UserResponse.model_validate(user))


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate with email and password",
    description="Verifies the Argon2id hash and returns a short-lived revocable access token.",
)
def login(
    request: LoginRequest,
    http_request: Request,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Authenticate and issue a revocable JWT access token."""
    enforce_rate_limit(
        db, f"login:ip:{_client_ip(http_request)}", limit=100, window_seconds=600
    )
    enforce_rate_limit(
        db, f"login:email:{_rate_limit_email(request.email)}", limit=8, window_seconds=1800
    )
    user = authenticate_user(db=db, request=request)
    token, _ = issue_session(db, user)
    return TokenResponse(access_token=token, user=UserResponse.model_validate(user))


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Revoke the current access token",
    description="Marks the current server-side session as revoked.",
)
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> MessageResponse:
    """Revoke the presented token so it cannot be reused."""
    _, payload = authenticate_access_token(credentials.credentials, db)
    session = db.get(AuthSession, payload["jti"])
    if session is not None:
        session.revoked_at = datetime.now(timezone.utc)
        db.commit()
    return MessageResponse(message="Signed out successfully")


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    description="Returns the authenticated user's safe profile. Requires a valid, unrevoked Bearer token.",
)
def get_me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Retrieve currently authenticated user's profile."""
    return UserResponse.model_validate(current_user)


@router.post(
    "/password-reset/request",
    response_model=MessageResponse,
    summary="Request password setup or recovery",
    description="Uses a configured email provider only; otherwise reports that email delivery is unavailable.",
)
def password_reset_request(
    request: PasswordResetRequest,
    http_request: Request,
    db: Session = Depends(get_db),
) -> MessageResponse:
    """Request a single-use setup/recovery link without enumerating accounts."""
    enforce_rate_limit(
        db, f"password-reset:ip:{_client_ip(http_request)}", limit=10, window_seconds=3600
    )
    enforce_rate_limit(
        db, f"password-reset:email:{_rate_limit_email(request.email)}", limit=3, window_seconds=3600
    )
    configured, delivered = request_password_reset(db, request)
    google_available = settings.google_is_configured()
    fallback = "Use Google sign-in" if google_available else "Contact an administrator"
    if not configured:
        return MessageResponse(
            message=f"Email delivery is not configured. {fallback}."
        )
    if not delivered:
        return MessageResponse(
            message=f"Password setup delivery is unavailable. Try again later or {fallback.lower()}."
        )
    return MessageResponse(
        message="If an account exists, password setup instructions have been sent."
    )


@router.post(
    "/password-reset/confirm",
    response_model=TokenResponse,
    summary="Complete password setup or recovery",
    description="Consumes a valid single-use link, stores a new Argon2id hash, and revokes old sessions.",
)
def password_reset_confirm(
    request: PasswordResetConfirm,
    http_request: Request,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Set a new password and start a fresh session."""
    enforce_rate_limit(
        db, f"password-reset:ip:{_client_ip(http_request)}", limit=20, window_seconds=3600
    )
    enforce_rate_limit(
        db, f"password-reset:token:{sha256_hex(request.token)}", limit=10, window_seconds=3600
    )
    user = confirm_password_reset(db, request)
    token, _ = issue_session(db, user)
    return TokenResponse(access_token=token, user=UserResponse.model_validate(user))


@router.get(
    "/google/start",
    response_model=GoogleStartResponse,
    summary="Start the Google authorization-code flow",
    description="Creates server-side state, nonce, and PKCE verifier and returns the Google authorization URL.",
)
def google_start(
    http_request: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> GoogleStartResponse:
    """Create a browser-bound OAuth state and return the authorization URL."""
    enforce_rate_limit(
        db, f"google-start:ip:{_client_ip(http_request)}", limit=20, window_seconds=600
    )
    try:
        authorization_url, browser_key = build_authorization_url(db)
    except GoogleAuthError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from None
    _set_oauth_cookie(response, browser_key)
    return GoogleStartResponse(authorization_url=authorization_url)


@router.get(
    "/google/callback",
    summary="Complete Google's authorization-code redirect",
    include_in_schema=False,
)
def google_callback(
    http_request: Request,
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
    db: Session = Depends(get_db),
) -> RedirectResponse:
    """Validate the Google callback server-side and redirect to the SPA."""
    redirect = RedirectResponse(
        url=_redirect_with_query(
            settings.GOOGLE_SUCCESS_REDIRECT_URL, {"error": "google_signin_failed"}
        ),
        status_code=303,
    )
    try:
        enforce_rate_limit(
            db, f"google-callback:ip:{_client_ip(http_request)}", limit=20, window_seconds=600
        )
        if error or not code or not state:
            raise GoogleAuthError()
        exchange_code = complete_google_callback(
            db, code, state, http_request.cookies.get(GOOGLE_COOKIE_NAME)
        )
    except Exception:
        # Google follows this redirect in the browser; never leave the user on
        # a raw JSON error (including a rate-limit response or a 500).
        _clear_oauth_cookie(redirect)
        return redirect

    # Keep the browser-bound cookie until /google/exchange consumes the code;
    # clearing it here would prevent the SPA from proving the same browser.
    return RedirectResponse(
        url=_redirect_with_query(
            settings.GOOGLE_SUCCESS_REDIRECT_URL, {"code": exchange_code}
        ),
        status_code=303,
    )


@router.post(
    "/google/exchange",
    response_model=TokenResponse,
    summary="Exchange a one-time Google callback code",
    description="Validates the browser-bound single-use code and issues the normal access token.",
)
def google_exchange(
    request: GoogleExchangeRequest,
    http_request: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Trade the opaque callback code for a revocable session token."""
    enforce_rate_limit(
        db, f"google-exchange:ip:{_client_ip(http_request)}", limit=20, window_seconds=600
    )
    try:
        token, user = exchange_google_code(
            db, request.code, http_request.cookies.get(GOOGLE_COOKIE_NAME)
        )
    except GoogleAuthError as exc:
        _clear_oauth_cookie(response)
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from None
    _clear_oauth_cookie(response)
    return TokenResponse(access_token=token, user=UserResponse.model_validate(user))
