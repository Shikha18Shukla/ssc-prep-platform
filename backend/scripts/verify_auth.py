"""Validation script to verify all Stage 3 endpoints and security mechanics.

Runs an automated end-to-end flow:
1. Health check (GET /api/health)
2. User registration (POST /api/auth/register)
3. Duplicate registration rejection (HTTP 409)
4. Weak password rejection (HTTP 422)
5. User login & token retrieval (POST /api/auth/login)
6. Fetching profile with Bearer token (GET /api/auth/me)
7. Unauthenticated access rejection (HTTP 401/403)
8. Invalid token rejection (HTTP 401)
"""

import sys
from pathlib import Path

# Ensure backend root is in sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.base import Base
from app.database.session import get_db
from app.main import create_app

# Isolated SQLite in-memory engine for runtime verification
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def run_verification() -> bool:
    print("=" * 60)
    print("STAGE 3 — AUTHENTICATION END-TO-END VERIFICATION")
    print("=" * 60)

    Base.metadata.create_all(bind=engine)
    app = create_app()

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        # 1. Health check
        res = client.get("/api/health")
        print(f"[1] GET /api/health -> Status: {res.status_code}")
        assert res.status_code == 200, f"Health check failed: {res.text}"
        assert res.json()["status"] == "healthy"

        # 2. Registration
        res = client.post(
            "/api/auth/register",
            json={
                "full_name": "Test Candidate",
                "email": "candidate@example.com",
                "password": "Password123",
            },
        )
        print(f"[2] POST /api/auth/register -> Status: {res.status_code}")
        assert res.status_code == 201, f"Registration failed: {res.text}"
        reg_data = res.json()
        assert reg_data["email"] == "candidate@example.com"
        assert "password_hash" not in reg_data
        print(f"    Created User ID: {reg_data['id']}")

        # 3. Duplicate email rejection
        res = client.post(
            "/api/auth/register",
            json={
                "full_name": "Duplicate Candidate",
                "email": "candidate@example.com",
                "password": "Password123",
            },
        )
        print(f"[3] POST /api/auth/register (Duplicate) -> Status: {res.status_code}")
        assert res.status_code == 409, f"Duplicate check failed: {res.text}"
        print(f"    Rejected with message: {res.json()['detail']}")

        # 4. Weak password rejection
        res = client.post(
            "/api/auth/register",
            json={
                "full_name": "Weak User",
                "email": "weak@example.com",
                "password": "short",
            },
        )
        print(f"[4] POST /api/auth/register (Weak password) -> Status: {res.status_code}")
        assert res.status_code == 422

        # 5. Login
        res = client.post(
            "/api/auth/login",
            json={
                "email": "candidate@example.com",
                "password": "Password123",
            },
        )
        print(f"[5] POST /api/auth/login -> Status: {res.status_code}")
        assert res.status_code == 200, f"Login failed: {res.text}"
        token_data = res.json()
        token = token_data["access_token"]
        assert token_data["token_type"] == "bearer"
        print(f"    JWT Token issued (length: {len(token)})")

        # 6. Fetch profile (/api/auth/me) with token
        res = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        print(f"[6] GET /api/auth/me (Authenticated) -> Status: {res.status_code}")
        assert res.status_code == 200, f"Profile fetch failed: {res.text}"
        profile = res.json()
        assert profile["id"] == reg_data["id"]
        assert profile["email"] == "candidate@example.com"
        assert profile["is_active"] is True
        assert "password_hash" not in profile

        # 7. /api/auth/me without token
        res = client.get("/api/auth/me")
        print(f"[7] GET /api/auth/me (Unauthenticated) -> Status: {res.status_code}")
        assert res.status_code in (401, 403)

        # 8. /api/auth/me with invalid token
        res = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid.malformed.token"},
        )
        print(f"[8] GET /api/auth/me (Invalid token) -> Status: {res.status_code}")
        assert res.status_code == 401

    print("=" * 60)
    print("ALL VERIFICATION CHECKS PASSED SUCCESSFULLY!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = run_verification()
    sys.exit(0 if success else 1)
