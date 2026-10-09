"""Chapter model."""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.question import Question
    from app.models.subject import Subject
    from app.models.subcategory import Subcategory
    from app.models.test_attempt import TestAttempt


class Chapter(Base, TimestampMixin):
    """Chapter within a subject."""

    __tablename__ = "chapters"
    __table_args__ = (
        UniqueConstraint("subcategory_id", "slug", name="uq_chapter_subcategory_slug"),
        Index(
            "uq_chapter_subject_slug_without_subcategory",
            "subject_id",
            "slug",
            unique=True,
            postgresql_where=text("subcategory_id IS NULL"),
            sqlite_where=text("subcategory_id IS NULL"),
        ),
        ForeignKeyConstraint(
            ["subcategory_id", "subject_id"],
            ["subcategories.id", "subcategories.subject_id"],
            name="fk_chapter_subcategory_subject",
            ondelete="RESTRICT",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )
    subject_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("subjects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    subcategory_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, nullable=True, index=True)
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    slug: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    display_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Relationships
    subject: Mapped["Subject"] = relationship(
        "Subject",
        back_populates="chapters",
    )
    subcategory: Mapped["Subcategory | None"] = relationship(
        "Subcategory",
        back_populates="chapters",
        primaryjoin="and_(Chapter.subcategory_id == Subcategory.id, Chapter.subject_id == Subcategory.subject_id)",
        foreign_keys="[Chapter.subcategory_id]",
        overlaps="subject,chapters",
    )
    questions: Mapped[list["Question"]] = relationship(
        "Question",
        back_populates="chapter",
        cascade="all, delete-orphan",
    )
    test_attempts: Mapped[list["TestAttempt"]] = relationship(
        "TestAttempt",
        back_populates="chapter",
    )

    def __repr__(self) -> str:
        return f"<Chapter id={self.id} slug={self.slug!r} subject_id={self.subject_id}>"
