"""Add approved beta invitations, account cap, and shared rate-limit storage.

Revision ID: 0008_beta_access_and_rate_limits
Revises: 0007_question_rotation_modes
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0008_beta_access_and_rate_limits"
down_revision: Union[str, None] = "0007_question_rotation_modes"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "beta_capacity",
        sa.Column("id", sa.SmallInteger(), nullable=False),
        sa.Column("max_accounts", sa.Integer(), nullable=False),
        sa.CheckConstraint("id = 1", name="ck_beta_capacity_singleton"),
        sa.CheckConstraint("max_accounts BETWEEN 1 AND 200", name="ck_beta_capacity_max_200"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.bulk_insert(
        sa.table("beta_capacity", sa.column("id", sa.SmallInteger()), sa.column("max_accounts", sa.Integer())),
        [{"id": 1, "max_accounts": 200}],
    )
    op.create_table(
        "beta_invitations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("redeemed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by_user_id", sa.Uuid(), nullable=True),
        sa.Column("redeemed_by_user_id", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["redeemed_by_user_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token_hash", name="uq_beta_invitation_token_hash"),
    )
    op.create_index("ix_beta_invitations_email", "beta_invitations", ["email"])
    op.create_index("ix_beta_invitations_expires_at", "beta_invitations", ["expires_at"])
    op.create_table(
        "rate_limit_windows",
        sa.Column("key_hash", sa.String(length=64), nullable=False),
        sa.Column("window_started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("request_count", sa.Integer(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("key_hash"),
    )


def downgrade() -> None:
    op.drop_table("rate_limit_windows")
    op.drop_index("ix_beta_invitations_expires_at", table_name="beta_invitations")
    op.drop_index("ix_beta_invitations_email", table_name="beta_invitations")
    op.drop_table("beta_invitations")
    op.drop_table("beta_capacity")
