"""Add separate PO, Clerk, and Others catalogs with the shared Banking syllabus.

Revision ID: 0010_banking_catalog
Revises: 0009_generic_beta_invites
"""
from typing import Sequence, Union
import re
import uuid

from alembic import op
import sqlalchemy as sa

from app.database.banking_catalog import BANKING_SUBJECTS

revision: str = "0010_banking_catalog"
down_revision: Union[str, None] = "0009_generic_beta_invites"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def upgrade() -> None:
    bind = op.get_bind()
    exams = sa.table("exams", sa.column("id", sa.Uuid), sa.column("name", sa.String),
                     sa.column("slug", sa.String), sa.column("description", sa.Text),
                     sa.column("is_active", sa.Boolean))
    subjects = sa.table("subjects", sa.column("id", sa.Uuid), sa.column("exam_id", sa.Uuid),
                        sa.column("name", sa.String), sa.column("slug", sa.String),
                        sa.column("description", sa.Text), sa.column("display_order", sa.Integer),
                        sa.column("is_active", sa.Boolean))
    chapters = sa.table("chapters", sa.column("id", sa.Uuid), sa.column("subject_id", sa.Uuid),
                        sa.column("subcategory_id", sa.Uuid), sa.column("name", sa.String),
                        sa.column("slug", sa.String), sa.column("description", sa.Text),
                        sa.column("display_order", sa.Integer), sa.column("is_active", sa.Boolean))
    legacy_subject_slugs = {
        "computer": "computer-awareness",
        "math-quant": "quantitative-aptitude",
    }
    for category in (("PO", "po"), ("Clerk", "clerk"), ("Others", "others")):
        exam_slug = f"banking-{category[1]}"
        exam_id = bind.execute(sa.select(exams.c.id).where(exams.c.slug == exam_slug)).scalar_one_or_none()
        if exam_id is None:
            exam_id = uuid.uuid4()
            bind.execute(exams.insert().values(id=exam_id, name=f"Banking {category[0]}", slug=exam_slug,
                description=f"Banking {category[0]} practice", is_active=True))
        else:
            bind.execute(exams.update().where(exams.c.id == exam_id).values(is_active=True))
        for subject_order, (subject_name, subject_slug, chapter_names) in enumerate(BANKING_SUBJECTS, 1):
            subject_id = bind.execute(sa.select(subjects.c.id).where(
                subjects.c.exam_id == exam_id, subjects.c.slug == subject_slug)).scalar_one_or_none()
            if subject_id is None and subject_slug in legacy_subject_slugs:
                legacy_slug = legacy_subject_slugs[subject_slug]
                subject_id = bind.execute(sa.select(subjects.c.id).where(
                    subjects.c.exam_id == exam_id, subjects.c.slug == legacy_slug)).scalar_one_or_none()
                if subject_id is not None:
                    bind.execute(subjects.update().where(subjects.c.id == subject_id).values(
                        slug=subject_slug, name=subject_name, display_order=subject_order, is_active=True))
            if subject_id is None:
                subject_id = uuid.uuid4()
                bind.execute(subjects.insert().values(id=subject_id, exam_id=exam_id, name=subject_name,
                    slug=subject_slug, description=None, display_order=subject_order, is_active=True))
            else:
                bind.execute(subjects.update().where(subjects.c.id == subject_id).values(
                    name=subject_name, display_order=subject_order, is_active=True))
            for chapter_order, chapter_name in enumerate(chapter_names, 1):
                chapter_slug = _slug(chapter_name)
                exists = bind.execute(sa.select(chapters.c.id).where(
                    chapters.c.subject_id == subject_id, chapters.c.slug == chapter_slug,
                    chapters.c.subcategory_id.is_(None))).scalar_one_or_none()
                if exists is None and subject_slug == "current-affairs":
                    general_subject_id = bind.execute(sa.select(subjects.c.id).where(
                        subjects.c.exam_id == exam_id,
                        subjects.c.slug == "general-banking-awareness")).scalar_one_or_none()
                    if general_subject_id is not None:
                        exists = bind.execute(sa.select(chapters.c.id).where(
                            chapters.c.subject_id == general_subject_id,
                            chapters.c.slug == chapter_slug,
                            chapters.c.subcategory_id.is_(None))).scalar_one_or_none()
                        if exists is not None:
                            bind.execute(chapters.update().where(chapters.c.id == exists).values(
                                subject_id=subject_id, name=chapter_name,
                                display_order=chapter_order, is_active=True))
                if exists is None:
                    bind.execute(chapters.insert().values(id=uuid.uuid4(), subject_id=subject_id,
                        subcategory_id=None, name=chapter_name, slug=chapter_slug, description=None,
                        display_order=chapter_order, is_active=True))
                else:
                    bind.execute(chapters.update().where(chapters.c.id == exists).values(
                        name=chapter_name, display_order=chapter_order, is_active=True))


def downgrade() -> None:
    # Catalog records may already have uploaded questions; preserve data on downgrade.
    pass
