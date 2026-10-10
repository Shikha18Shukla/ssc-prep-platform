"""Comprehensive authentication and authorization tests.

Tests cover:
1. Successful registration
2. Duplicate email registration rejection (409)
3. Successful login & JWT issuance
4. Invalid password rejection (401)
5. Inactive user login rejection (403)
6. Valid JWT token decoding and acceptance
7. Invalid JWT token rejection (401)
8. Expired JWT token rejection (401)
9. GET /api/auth/me with valid authentication
10. GET /api/auth/me without authentication (401)
11. Password strength enforcement
12. Email normalization
"""

from datetime import timedelta
import uuid

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.security import create_access_token, decode_access_token, hash_password, verify_password
from app.config import settings
from app.models.user import User


# =====================================================================
# Unit Tests for Security Utilities
# =====================================================================

def test_password_hashing_and_verification():
    """Verify Argon2id hashes passwords and correctly verifies plaintexts."""
    password = "SecurePassword123"
    hashed = hash_password(password)

    assert hashed != password
    assert hashed.startswith("$argon2id$")
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword123", hashed) is False
    assert verify_password("", hashed) is False


def test_jwt_token_creation_and_decoding():
    """Verify JWT access tokens encode user IDs and decode correctly."""
    user_id = uuid.uuid4()
    token = create_access_token(user_id=user_id)
    payload = decode_access_token(token)

    assert payload["sub"] == str(user_id)
    assert "exp" in payload
    assert "iat" in payload


def test_jwt_expired_token():
    """Verify expired JWT tokens raise error when decoded."""
    user_id = uuid.uuid4()
    # Create token that expired 10 minutes ago
    expired_token = create_access_token(
        user_id=user_id,
        expires_delta=timedelta(minutes=-10),
    )

    with pytest.raises(Exception):
        decode_access_token(expired_token)


def test_jwt_invalid_token():
    """Verify tampered or invalid JWT tokens raise error when decoded."""
    with pytest.raises(Exception):
        decode_access_token("not.a.valid.jwt.token")


# =====================================================================
# Integration Tests for API Endpoints
# =====================================================================

def test_1_successful_registration(client: TestClient, db_session: Session):
    """Test 1: Register a new user with valid details."""
    response = client.post(
        "/api/auth/register",
        json={
            "full_name": "Aspirant Rahul",
            "email": "rahul.ssc@example.com",
            "password": "Password123",
            "is_admin": True,
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["email"] == "rahul.ssc@example.com"
    assert data["full_name"] == "Aspirant Rahul"
    assert data["is_active"] is True
    assert "password" not in data
    assert "password_hash" not in data

    # Verify directly in DB that password is encrypted and not plaintext
    stmt = select(User).where(User.email == "rahul.ssc@example.com")
    db_user = db_session.execute(stmt).scalar_one()
    assert db_user.password_hash.startswith("$argon2id$")
    assert db_user.password_hash != "Password123"
    assert verify_password("Password123", db_user.password_hash) is True
    assert db_user.is_admin is False


def test_2_duplicate_email_registration(client: TestClient):
    """Test 2: Attempting to register an already-registered email returns 409."""
    # Register initial user
    client.post(
        "/api/auth/register",
        json={
            "full_name": "First User",
            "email": "duplicate@example.com",
            "password": "Password123",
        },
    )

    # Attempt to register identical email
    response = client.post(
        "/api/auth/register",
        json={
            "full_name": "Second User",
            "email": "duplicate@example.com",
            "password": "OtherPassword456",
        },
    )

    assert response.status_code == 409
    assert "already exists" in response.json()["detail"].lower()


def test_email_normalization_on_registration(client: TestClient):
    """Verify emails with uppercase or surrounding whitespace are normalized."""
    response = client.post(
        "/api/auth/register",
        json={
            "full_name": "Caps User",
            "email": "  USER.Caps@Example.COM  ",
            "password": "Password123",
        },
    )
    assert response.status_code == 201
    assert response.json()["email"] == "user.caps@example.com"


def test_password_strength_validation(client: TestClient):
    """Verify weak passwords (too short, missing numbers/letters) are rejected with 422."""
    # Too short (< 8 chars)
    r1 = client.post(
        "/api/auth/register",
        json={"full_name": "Test", "email": "short@example.com", "password": "Pass1"},
    )
    assert r1.status_code == 422

    # No numbers
    r2 = client.post(
        "/api/auth/register",
        json={"full_name": "Test", "email": "nonum@example.com", "password": "PasswordOnly"},
    )
    assert r2.status_code == 422

    # No letters
    r3 = client.post(
        "/api/auth/register",
        json={"full_name": "Test", "email": "noletter@example.com", "password": "1234567890"},
    )
    assert r3.status_code == 422


def test_3_successful_login(client: TestClient):
    """Test 3: Log in with correct credentials returns a Bearer access token."""
    # Register user
    client.post(
        "/api/auth/register",
        json={
            "full_name": "Login User",
            "email": "login.user@example.com",
            "password": "ValidPassword1",
        },
    )

    # Login
    response = client.post(
        "/api/auth/login",
        json={
            "email": "login.user@example.com",
            "password": "ValidPassword1",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "login.user@example.com"
    assert "password_hash" not in data["user"]


def test_4_invalid_password_login(client: TestClient):
    """Test 4: Attempting to log in with an incorrect password returns 401."""
    client.post(
        "/api/auth/register",
        json={
            "full_name": "Target User",
            "email": "target@example.com",
            "password": "CorrectPassword1",
        },
    )

    response = client.post(
        "/api/auth/login",
        json={
            "email": "target@example.com",
            "password": "WrongPassword999",
        },
    )

    assert response.status_code == 401
    assert "invalid email or password" in response.json()["detail"].lower()


def test_5_inactive_user_login(client: TestClient, db_session: Session):
    """Test 5: Inactive user account is rejected upon login with 403."""
    # Create user directly in DB with is_active = False
    inactive_user = User(
        email="inactive@example.com",
        full_name="Inactive User",
        password_hash=hash_password("Password123"),
        is_active=False,
    )
    db_session.add(inactive_user)
    db_session.commit()

    response = client.post(
        "/api/auth/login",
        json={
            "email": "inactive@example.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 403
    assert "inactive" in response.json()["detail"].lower()


def test_6_valid_jwt_and_me_endpoint(client: TestClient):
    """Test 6 & 9: Authenticated user can fetch /api/auth/me using valid Bearer token."""
    reg = client.post(
        "/api/auth/register",
        json={
            "full_name": "Me User",
            "email": "me@example.com",
            "password": "SecurePassword1",
        },
    )
    user_id = reg.json()["id"]

    login = client.post(
        "/api/auth/login",
        json={"email": "me@example.com", "password": "SecurePassword1"},
    )
    token = login.json()["access_token"]

    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == "me@example.com"
    assert data["full_name"] == "Me User"
    assert data["is_active"] is True
    assert "password_hash" not in data


def test_7_invalid_jwt(client: TestClient):
    """Test 7: Providing a malformed or forged JWT returns 401."""
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer forged.invalid.token"},
    )
    assert response.status_code == 401


def test_8_expired_jwt(client: TestClient, db_session: Session):
    """Test 8: Providing an expired JWT token returns 401."""
    # Create active user
    user = User(
        email="expired.token@example.com",
        full_name="Expired User",
        password_hash=hash_password("Password123"),
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    # Generate token with negative delta
    expired_token = create_access_token(
        user_id=user.id,
        expires_delta=timedelta(minutes=-30),
    )

    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {expired_token}"},
    )
    assert response.status_code == 401


def test_10_me_without_authentication(client: TestClient):
    """Test 10: Requesting /api/auth/me without an Authorization header returns 401 or 403."""
    response = client.get("/api/auth/me")
    assert response.status_code in (401, 403)
