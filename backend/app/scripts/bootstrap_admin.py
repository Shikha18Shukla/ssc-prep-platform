"""Create the first administrator on a fresh, invitation-protected beta DB.

Run from the backend directory with DATABASE_URL pointing only at the new beta
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
from app.models import BetaCapacity, User
from app.scripts.neon_beta_db import BetaDatabaseError, beta_url_from_environment


def main() -> int:
    if settings.ENVIRONMENT.strip().lower() != "production" or not settings.BETA_INVITATIONS_REQUIRED:
        print("Refusing bootstrap: require ENVIRONMENT=production and invitation-only registration.", file=sys.stderr)
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
    if input("Type CREATE FIRST BETA ADMIN to continue: ").strip() != "CREATE FIRST BETA ADMIN":
        print("Cancelled.")
        return 1

    password = getpass.getpass("New administrator password (min 8 chars, letter and number): ")
    confirm = getpass.getpass("Confirm password: ")
    if password != confirm or len(password) < 8 or not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
        print("Passwords must match and contain at least 8 characters, a letter, and a number.", file=sys.stderr)
        return 2

    try:
        with SessionLocal.begin() as db:
            # Serialize simultaneous first-admin attempts on the same singleton
            # row; only one process may pass the empty-user checks at a time.
            capacity = db.execute(
                select(BetaCapacity).where(BetaCapacity.id == 1).with_for_update()
            ).scalar_one_or_none()
            if capacity is None or capacity.max_accounts != 200:
                print("Refusing bootstrap: apply and verify migration 0008 first.", file=sys.stderr)
                return 2
            if db.scalar(select(User.id).where(User.is_admin.is_(True)).limit(1)) is not None:
                print("Refusing bootstrap: an administrator already exists.", file=sys.stderr)
                return 2
            if db.scalar(select(func.count(User.id))) != 0:
                print("Refusing first-admin bootstrap: the beta database already contains user accounts.", file=sys.stderr)
                return 2
            if db.scalar(select(User.id).where(User.email == email).limit(1)) is not None:
                print("Refusing bootstrap: this email already has an account; use the admin grant procedure.", file=sys.stderr)
                return 2
            db.add(User(
                email=email,
                full_name="Beta Administrator",
                password_hash=hash_password(password),
                is_active=True,
                is_admin=True,
            ))
    except IntegrityError:
        print("First-admin creation conflicted with another account operation; inspect the database before retrying.", file=sys.stderr)
        return 2

    print("First beta administrator created. Sign in and issue invitations immediately.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
