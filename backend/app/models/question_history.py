"""Persistent per-user question rotation state."""
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class UserChapterRotation(Base):
    __tablename__ = "user_chapter_rotations"
    __table_args__ = (UniqueConstraint("user_id", "chapter_id", "selection_mode", name="uq_user_chapter_rotation_mode"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    chapter_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False, index=True)
    selection_mode: Mapped[str] = mapped_column(String(16), nullable=False, default="MIXED", server_default="MIXED")
    rotation: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")


class UserQuestionHistory(Base):
    __tablename__ = "user_question_history"
    __table_args__ = (UniqueConstraint("user_id", "chapter_id", "selection_mode", "question_id", name="uq_user_chapter_mode_question_history"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    chapter_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False, index=True)
    selection_mode: Mapped[str] = mapped_column(String(16), nullable=False, default="MIXED", server_default="MIXED")
    question_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    rotation: Mapped[int] = mapped_column(Integer, nullable=False)
    served_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1, server_default="1")
    last_served_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
