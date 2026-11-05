"""Support generic one-time beta codes and persistent revocation state.

Revision ID: 0009_generic_beta_invites
Revises: 0008_beta_access_and_rate_limits
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0009_generic_beta_invites"
down_revision: Union[str, None] = "0008_beta_access_and_rate_limits"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("beta_invitations", "email", existing_type=sa.String(255), nullable=True)
    op.add_column(
        "beta_invitations",
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_beta_invitations_revoked_at", "beta_invitations", ["revoked_at"])


def downgrade() -> None:
    bind = op.get_bind()
    generic_count = bind.execute(sa.text(
        "SELECT count(*) FROM beta_invitations WHERE email IS NULL"
    )).scalar_one()
    revoked_count = bind.execute(sa.text(
        "SELECT count(*) FROM beta_invitations WHERE revoked_at IS NOT NULL"
    )).scalar_one()
    if generic_count or revoked_count:
        raise RuntimeError(
            "Refusing downgrade: generic or revoked invitations exist; preserve their single-use state before rollback."
        )
    op.drop_index("ix_beta_invitations_revoked_at", table_name="beta_invitations")
    op.drop_column("beta_invitations", "revoked_at")
    op.alter_column("beta_invitations", "email", existing_type=sa.String(255), nullable=False)
