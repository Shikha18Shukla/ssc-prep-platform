"""Add optional subcategories to the chapter catalog.

Revision ID: 0002_subcategories
Revises: 0001_initial_schema
Create Date: 2026-10-09
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0002_subcategories"
down_revision: Union[str, None] = "0001_initial_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "subcategories",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("subject_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("display_order", sa.Integer(), server_default="0", nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["subject_id"], ["subjects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("subject_id", "slug", name="uq_subcategory_subject_slug"),
        sa.UniqueConstraint("id", "subject_id", name="uq_subcategory_id_subject"),
    )
    op.create_index(op.f("ix_subcategories_subject_id"), "subcategories", ["subject_id"], unique=False)

    # Existing chapters remain in place with a NULL subcategory.
    op.add_column("chapters", sa.Column("subcategory_id", sa.Uuid(), nullable=True))
    op.create_index(op.f("ix_chapters_subcategory_id"), "chapters", ["subcategory_id"], unique=False)
    op.drop_constraint("uq_chapter_subject_slug", "chapters", type_="unique")
    op.create_unique_constraint(
        "uq_chapter_subcategory_slug",
        "chapters",
        ["subcategory_id", "slug"],
    )
    op.create_index(
        "uq_chapter_subject_slug_without_subcategory",
        "chapters",
        ["subject_id", "slug"],
        unique=True,
        postgresql_where=sa.text("subcategory_id IS NULL"),
    )
    op.create_foreign_key(
        "fk_chapter_subcategory_subject",
        "chapters",
        "subcategories",
        ["subcategory_id", "subject_id"],
        ["id", "subject_id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    bind = op.get_bind()
    duplicate_slugs = bind.execute(
        sa.text(
            "SELECT subject_id, slug FROM chapters "
            "GROUP BY subject_id, slug HAVING count(*) > 1"
        )
    ).all()
    if duplicate_slugs:
        raise RuntimeError(
            "Cannot downgrade subcategories while a subject has repeated chapter slugs. "
            "Resolve the listed chapter records before retrying: "
            f"{[(str(subject_id), slug) for subject_id, slug in duplicate_slugs]}"
        )

    op.drop_constraint("fk_chapter_subcategory_subject", "chapters", type_="foreignkey")
    op.drop_index("uq_chapter_subject_slug_without_subcategory", table_name="chapters")
    op.drop_constraint("uq_chapter_subcategory_slug", "chapters", type_="unique")
    op.create_unique_constraint(
        "uq_chapter_subject_slug",
        "chapters",
        ["subject_id", "slug"],
    )
    op.drop_index(op.f("ix_chapters_subcategory_id"), table_name="chapters")
    op.drop_column("chapters", "subcategory_id")

    op.drop_index(op.f("ix_subcategories_subject_id"), table_name="subcategories")
    op.drop_table("subcategories")
