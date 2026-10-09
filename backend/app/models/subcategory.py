"""Optional subcategory within a main subject."""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.chapter import Chapter
    from app.models.subject import Subject


class Subcategory(Base, TimestampMixin):
    """An optional grouping such as Science within GK / GS."""

    __tablename__ = "subcategories"
    __table_args__ = (
        UniqueConstraint("subject_id", "slug", name="uq_subcategory_subject_slug"),
        UniqueConstraint("id", "subject_id", name="uq_subcategory_id_subject"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    subject_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("subjects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    subject: Mapped["Subject"] = relationship(
        "Subject",
        back_populates="subcategories",
    )
    chapters: Mapped[list["Chapter"]] = relationship(
        "Chapter",
        back_populates="subcategory",
        order_by="Chapter.display_order",
        overlaps="chapters,subject",
    )

    def __repr__(self) -> str:
        return f"<Subcategory id={self.id} slug={self.slug!r} subject_id={self.subject_id}>"
