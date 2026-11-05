"""Keep question rotation cycles independent by selection mode.

Revision ID: 0007_question_rotation_modes
Revises: 0006_user_question_rotation
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0007_question_rotation_modes"
down_revision: Union[str, None] = "0006_user_question_rotation"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Existing chapter-wide state is kept under MIXED; no history is discarded.
    op.add_column(
        "user_chapter_rotations",
        sa.Column("selection_mode", sa.String(length=16), server_default="MIXED", nullable=False),
    )
    op.add_column(
        "user_question_history",
        sa.Column("selection_mode", sa.String(length=16), server_default="MIXED", nullable=False),
    )
    op.drop_constraint("uq_user_chapter_rotation", "user_chapter_rotations", type_="unique")
    op.drop_constraint("uq_user_chapter_question_history", "user_question_history", type_="unique")
    op.create_unique_constraint(
        "uq_user_chapter_rotation_mode",
        "user_chapter_rotations",
        ["user_id", "chapter_id", "selection_mode"],
    )
    op.create_unique_constraint(
        "uq_user_chapter_mode_question_history",
        "user_question_history",
        ["user_id", "chapter_id", "selection_mode", "question_id"],
    )


def downgrade() -> None:
    # Merge rows created by separate modes before restoring the legacy unique keys.
    op.execute(
        """
        WITH ranked AS (
            SELECT id,
                   MAX(rotation) OVER (PARTITION BY user_id, chapter_id, question_id) AS rotation,
                   SUM(served_count) OVER (PARTITION BY user_id, chapter_id, question_id) AS served_count,
                   MAX(last_served_at) OVER (PARTITION BY user_id, chapter_id, question_id) AS last_served_at,
                   ROW_NUMBER() OVER (PARTITION BY user_id, chapter_id, question_id ORDER BY id) AS row_num
            FROM user_question_history
        )
        UPDATE user_question_history AS history
        SET rotation = ranked.rotation,
            served_count = ranked.served_count,
            last_served_at = ranked.last_served_at
        FROM ranked
        WHERE history.id = ranked.id AND ranked.row_num = 1
        """
    )
    op.execute(
        """
        DELETE FROM user_question_history AS history
        USING (
            SELECT id,
                   ROW_NUMBER() OVER (PARTITION BY user_id, chapter_id, question_id ORDER BY id) AS row_num
            FROM user_question_history
        ) AS ranked
        WHERE history.id = ranked.id AND ranked.row_num > 1
        """
    )
    op.execute(
        """
        WITH ranked AS (
            SELECT id,
                   MAX(rotation) OVER (PARTITION BY user_id, chapter_id) AS rotation,
                   ROW_NUMBER() OVER (PARTITION BY user_id, chapter_id ORDER BY id) AS row_num
            FROM user_chapter_rotations
        )
        UPDATE user_chapter_rotations AS state
        SET rotation = ranked.rotation
        FROM ranked
        WHERE state.id = ranked.id AND ranked.row_num = 1
        """
    )
    op.execute(
        """
        DELETE FROM user_chapter_rotations AS state
        USING (
            SELECT id,
                   ROW_NUMBER() OVER (PARTITION BY user_id, chapter_id ORDER BY id) AS row_num
            FROM user_chapter_rotations
        ) AS ranked
        WHERE state.id = ranked.id AND ranked.row_num > 1
        """
    )
    op.drop_constraint("uq_user_chapter_rotation_mode", "user_chapter_rotations", type_="unique")
    op.drop_constraint(
        "uq_user_chapter_mode_question_history",
        "user_question_history",
        type_="unique",
    )
    op.drop_column("user_chapter_rotations", "selection_mode")
    op.drop_column("user_question_history", "selection_mode")
    op.create_unique_constraint(
        "uq_user_chapter_rotation",
        "user_chapter_rotations",
        ["user_id", "chapter_id"],
    )
    op.create_unique_constraint(
        "uq_user_chapter_question_history",
        "user_question_history",
        ["user_id", "chapter_id", "question_id"],
    )
