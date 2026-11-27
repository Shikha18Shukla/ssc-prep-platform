"""Create the first administrator on a fresh production database.

Run from the backend directory with DATABASE_URL pointing only at the target
database. The password is prompted without echo and is never accepted as a CLI
argument or printed.
"""

import getpass
import sys

from pydantic import EmailStr, TypeAdapter, ValidationError
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from app.auth.security import hash_password
from app.config import settings
from app.database.session import SessionLocal
from app.models import User
from app.scripts.neon_beta_db import BetaDatabaseError, beta_url_from_environment


def main() -> int:
    if settings.ENVIRONMENT.strip().lower() != "production":
        print("Refusing bootstrap: ENVIRONMENT=production is required.", file=sys.stderr)
        return 2

    try:
        database_url = beta_url_from_environment()
    except BetaDatabaseError as exc:
        print(f"Refusing bootstrap [{exc.code}]: {exc}", file=sys.stderr)
        return 2

    parser_email = input("Owner administrator email: ").strip().lower()
    try:
        email = str(TypeAdapter(EmailStr).validate_python(parser_email)).lower()
    except ValidationError:
        print("A valid email address is required.", file=sys.stderr)
        return 2

    database_name = (database_url.database or "").lower()
    print(f"Target database: {database_name}@{database_url.host}")
    if input("Type CREATE FIRST ADMIN to continue: ").strip() != "CREATE FIRST ADMIN":
        print("Cancelled.")
        return 1

    password = getpass.getpass("New administrator password (min 8 chars, letter and number): ")
    confirm = getpass.getpass("Confirm password: ")
    if password != confirm or len(password) < 8 or not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
        print("Passwords must match and contain at least 8 characters, a letter, and a number.", file=sys.stderr)
        return 2

    try:
        with SessionLocal.begin() as db:
            if db.scalar(select(User.id).where(User.is_admin.is_(True)).limit(1)) is not None:
                print("Refusing bootstrap: an administrator already exists.", file=sys.stderr)
                return 2
            if db.scalar(select(func.count(User.id))) != 0:
                print("Refusing first-admin bootstrap: the database already contains user accounts.", file=sys.stderr)
                return 2
            db.add(User(
                email=email,
                full_name="Administrator",
                password_hash=hash_password(password),
                password_changed_at=None,
                is_active=True,
                is_admin=True,
            ))
    except IntegrityError:
        print("First-admin creation conflicted with another account operation; inspect the database before retrying.", file=sys.stderr)
        return 2

    print("First administrator created. Sign in to administrate the platform.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
