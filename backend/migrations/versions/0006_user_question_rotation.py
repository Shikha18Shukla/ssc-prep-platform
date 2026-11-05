"""Persist per-user question rotation by chapter.

Revision ID: 0006_user_question_rotation
Revises: 0005_question_images
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0006_user_question_rotation"
down_revision: Union[str, None] = "0005_question_images"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_chapter_rotations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("chapter_id", sa.Uuid(), nullable=False),
        sa.Column("rotation", sa.Integer(), server_default="0", nullable=False),
        sa.ForeignKeyConstraint(["chapter_id"], ["chapters.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "chapter_id", name="uq_user_chapter_rotation"),
    )
    op.create_index("ix_user_chapter_rotations_user_id", "user_chapter_rotations", ["user_id"])
    op.create_index("ix_user_chapter_rotations_chapter_id", "user_chapter_rotations", ["chapter_id"])
    op.create_table(
        "user_question_history",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("chapter_id", sa.Uuid(), nullable=False),
        sa.Column("question_id", sa.Uuid(), nullable=False),
        sa.Column("rotation", sa.Integer(), nullable=False),
        sa.Column("served_count", sa.Integer(), server_default="1", nullable=False),
        sa.Column("last_served_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["chapter_id"], ["chapters.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "chapter_id", "question_id", name="uq_user_chapter_question_history"),
    )
    op.create_index("ix_user_question_history_user_id", "user_question_history", ["user_id"])
    op.create_index("ix_user_question_history_chapter_id", "user_question_history", ["chapter_id"])
    op.create_index("ix_user_question_history_question_id", "user_question_history", ["question_id"])


def downgrade() -> None:
    op.drop_table("user_question_history")
    op.drop_table("user_chapter_rotations")
