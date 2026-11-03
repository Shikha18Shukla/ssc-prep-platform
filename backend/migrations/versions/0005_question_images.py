"""Add optional question image references for visual reasoning items.

Revision ID: 0005_question_images
Revises: 0004_test_type
Create Date: 2026-11-03
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0005_question_images"
down_revision: Union[str, None] = "0004_test_type"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("questions", sa.Column("image_url", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("questions", "image_url")
