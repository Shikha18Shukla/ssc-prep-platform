"""Persist whether a test attempt is chapter-wise or miscellaneous.

Revision ID: 0004_test_type
Revises: 0003_user_admin_flag
Create Date: 2026-10-10
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0004_test_type"
down_revision: Union[str, None] = "0003_user_admin_flag"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "test_attempts",
        sa.Column("test_type", sa.String(length=20), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("test_attempts", "test_type")
