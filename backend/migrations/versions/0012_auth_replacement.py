"""Replace beta invitation access with password/Google authentication.

Revision ID: 0012_auth_replacement
Revises: 0011_current_affairs_sections
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0012_auth_replacement"
down_revision: Union[str, None] = "0011_current_affairs_sections"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _has_table(name: str) -> bool:
    return name in sa.inspect(op.get_bind()).get_table_names()


def upgrade() -> None:
    bind = op.get_bind()

    # Additive user columns first; user IDs and all learning records stay intact.
    op.add_column("users", sa.Column("email_normalized", sa.String(255), nullable=True))
    op.add_column(
        "users",
        sa.Column("password_changed_at", sa.DateTime(timezone=True), nullable=True),
    )
    bind.execute(sa.text("""
        UPDATE users
        SET email_normalized = lower(btrim(email)),
            password_changed_at = COALESCE(password_changed_at, created_at)
    """))

    duplicates = bind.execute(sa.text("""
        SELECT email_normalized, COUNT(*) AS total
        FROM users
        GROUP BY email_normalized
        HAVING COUNT(*) > 1
    """)).all()
    if duplicates:
        raise RuntimeError(
            "Refusing auth migration: duplicate normalized email addresses must be resolved manually"
        )

    op.alter_column("users", "email_normalized", nullable=False)
    op.alter_column("users", "password_hash", nullable=True)
    op.create_index(
        "ix_users_email_normalized", "users", ["email_normalized"], unique=True
    )

    op.create_table(
        "auth_sessions",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column(
            "user_id",
            sa.Uuid(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_auth_sessions_user_id", "auth_sessions", ["user_id"])

    op.create_table(
        "oauth_identities",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "user_id",
            sa.Uuid(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("provider", sa.String(32), nullable=False),
        sa.Column("provider_user_id", sa.String(255), nullable=False),
        sa.Column("provider_email", sa.String(255), nullable=True),
        sa.Column("email_verified", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_oauth_identities_user_id", "oauth_identities", ["user_id"])
    op.create_index(
        "ix_oauth_identity_provider_email",
        "oauth_identities",
        ["provider", "provider_email"],
    )
    op.create_index(
        "uq_oauth_identity_provider_subject",
        "oauth_identities",
        ["provider", "provider_user_id"],
        unique=True,
    )
    op.create_index(
        "uq_oauth_identity_user_provider",
        "oauth_identities",
        ["user_id", "provider"],
        unique=True,
    )

    op.create_table(
        "oauth_states",
        sa.Column("state_hash", sa.String(64), primary_key=True),
        sa.Column("browser_key_hash", sa.String(64), nullable=False),
        sa.Column("nonce_hash", sa.String(64), nullable=False),
        sa.Column("code_verifier", sa.String(128), nullable=False),
        sa.Column("redirect_uri", sa.String(512), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )

    op.create_table(
        "oauth_exchange_codes",
        sa.Column("code_hash", sa.String(64), primary_key=True),
        sa.Column(
            "user_id",
            sa.Uuid(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("browser_key_hash", sa.String(64), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_oauth_exchange_codes_user_id", "oauth_exchange_codes", ["user_id"])

    op.create_table(
        "password_reset_tokens",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "user_id",
            sa.Uuid(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("token_hash", sa.String(64), nullable=False, unique=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_password_reset_tokens_user_id", "password_reset_tokens", ["user_id"])
    op.create_index(
        "uq_password_reset_one_live_per_user",
        "password_reset_tokens",
        ["user_id"],
        unique=True,
        postgresql_where=sa.text("used_at IS NULL AND revoked_at IS NULL"),
    )

    if _has_table("beta_invitations"):
        invitations = bind.execute(sa.text("SELECT COUNT(*) FROM beta_invitations")).scalar_one()
        if invitations:
            raise RuntimeError(
                "Refusing auth migration: beta_invitations still contains rows; clear them deliberately first"
            )
        op.drop_table("beta_invitations")
    if _has_table("beta_capacity"):
        op.drop_table("beta_capacity")


def downgrade() -> None:
    bind = op.get_bind()
    null_passwords = bind.execute(
        sa.text("SELECT COUNT(*) FROM users WHERE password_hash IS NULL")
    ).scalar_one()
    if null_passwords:
        raise RuntimeError(
            "Refusing auth downgrade: provider-only accounts have no local password"
        )

    op.create_table(
        "beta_capacity",
        sa.Column("id", sa.SmallInteger, primary_key=True),
        sa.Column("max_accounts", sa.Integer, nullable=False),
        sa.CheckConstraint("id = 1", name="ck_beta_capacity_singleton"),
        sa.CheckConstraint("max_accounts BETWEEN 1 AND 200", name="ck_beta_capacity_max_200"),
    )
    bind.execute(sa.text("INSERT INTO beta_capacity (id, max_accounts) VALUES (1, 200)"))

    op.create_table(
        "beta_invitations",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("token_hash", sa.String(64), nullable=False, unique=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("redeemed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_by_user_id",
            sa.Uuid(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "redeemed_by_user_id",
            sa.Uuid(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_beta_invitations_email", "beta_invitations", ["email"])
    op.create_index("ix_beta_invitations_expires_at", "beta_invitations", ["expires_at"])
    op.create_index("ix_beta_invitations_revoked_at", "beta_invitations", ["revoked_at"])

    op.drop_table("password_reset_tokens")
    op.drop_table("oauth_exchange_codes")
    op.drop_table("oauth_states")
    op.drop_table("oauth_identities")
    op.drop_table("auth_sessions")

    op.drop_index("ix_users_email_normalized", table_name="users")
    op.alter_column("users", "password_hash", nullable=False)
    op.drop_column("users", "password_changed_at")
    op.drop_column("users", "email_normalized")
