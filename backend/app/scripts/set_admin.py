"""Grant or revoke question-bank administrator access for an existing user.

Run from the backend directory after applying Alembic migrations:
    python -m app.scripts.set_admin --email admin@example.com --grant
"""

import argparse
import sys

from sqlalchemy import func, select

from app.database.session import SessionLocal
from app.models import User


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--email", required=True, help="Existing account email")
    access = parser.add_mutually_exclusive_group(required=True)
    access.add_argument("--grant", action="store_true", help="Grant admin access")
    access.add_argument("--revoke", action="store_true", help="Revoke admin access")
    args = parser.parse_args()
    email = args.email.strip().casefold()
    if not email:
        parser.error("--email cannot be blank")

    with SessionLocal() as db:
        user = db.execute(
            select(User).where(func.lower(User.email) == email)
        ).scalar_one_or_none()
        if user is None:
            print("No existing account has that email. Create and verify the account first.", file=sys.stderr)
            return 2
        desired = bool(args.grant)
        if desired and not user.is_active:
            print("Cannot grant admin access to an inactive account.", file=sys.stderr)
            return 2
        if user.is_admin == desired:
            print(f"Admin access already {'enabled' if desired else 'disabled'} for {email}.")
            return 0
        user.is_admin = desired
        db.commit()
        print(f"Admin access {'granted to' if desired else 'revoked from'} {email}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
