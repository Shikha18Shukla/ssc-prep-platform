"""Initial schema for SSC Prep Platform.

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-10-07 16:45:00.000000

Creates core entities:
- users
- exams
- subjects
- chapters
- questions
- question_options
- test_attempts
- test_questions
- user_answers

Includes all enums, constraints, composite indexes, and foreign keys.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "0001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

difficulty_enum = postgresql.ENUM("EASY", "MEDIUM", "HARD", name="difficulty_level", create_type=False)
test_status_enum = postgresql.ENUM("IN_PROGRESS", "COMPLETED", "AUTO_SUBMITTED", name="test_attempt_status", create_type=False)


def upgrade() -> None:
    # Create enum types if in postgresql
    bind = op.get_bind()
    difficulty_enum.create(bind, checkfirst=True)
    test_status_enum.create(bind, checkfirst=True)

    # 1. users
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    # 2. exams
    op.create_table(
        "exams",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_exams_slug"), "exams", ["slug"], unique=True)

    # 3. subjects
    op.create_table(
        "subjects",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("exam_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("display_order", sa.Integer(), server_default="0", nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["exam_id"], ["exams.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("exam_id", "slug", name="uq_subject_exam_slug"),
    )
    op.create_index(op.f("ix_subjects_exam_id"), "subjects", ["exam_id"], unique=False)

    # 4. chapters
    op.create_table(
        "chapters",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("subject_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("slug", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("display_order", sa.Integer(), server_default="0", nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["subject_id"], ["subjects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("subject_id", "slug", name="uq_chapter_subject_slug"),
    )
    op.create_index(op.f("ix_chapters_subject_id"), "chapters", ["subject_id"], unique=False)

    # 5. questions
    op.create_table(
        "questions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("chapter_id", sa.Uuid(), nullable=False),
        sa.Column("question_text", sa.Text(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=True),
        sa.Column("difficulty", difficulty_enum, nullable=False),
        sa.Column("is_pyq", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("pyq_year", sa.Integer(), nullable=True),
        sa.Column("pyq_exam_name", sa.String(length=100), nullable=True),
        sa.Column("source", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["chapter_id"], ["chapters.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_questions_chapter_id"), "questions", ["chapter_id"], unique=False)
    op.create_index(op.f("ix_questions_difficulty"), "questions", ["difficulty"], unique=False)
    op.create_index(op.f("ix_questions_is_pyq"), "questions", ["is_pyq"], unique=False)
    op.create_index(op.f("ix_questions_pyq_year"), "questions", ["pyq_year"], unique=False)
    op.create_index(op.f("ix_questions_is_active"), "questions", ["is_active"], unique=False)
    op.create_index(
        "ix_questions_chapter_diff_pyq_active",
        "questions",
        ["chapter_id", "difficulty", "is_pyq", "is_active"],
        unique=False,
    )

    # 6. question_options
    op.create_table(
        "question_options",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("question_id", sa.Uuid(), nullable=False),
        sa.Column("option_key", sa.String(length=10), nullable=False),
        sa.Column("option_text", sa.Text(), nullable=False),
        sa.Column("display_order", sa.Integer(), server_default="1", nullable=False),
        sa.Column("is_correct", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("question_id", "option_key", name="uq_question_option_key"),
    )
    op.create_index(op.f("ix_question_options_question_id"), "question_options", ["question_id"], unique=False)

    # 7. test_attempts
    op.create_table(
        "test_attempts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("exam_id", sa.Uuid(), nullable=False),
        sa.Column("subject_id", sa.Uuid(), nullable=False),
        sa.Column("chapter_id", sa.Uuid(), nullable=True),
        sa.Column("difficulty", difficulty_enum, nullable=True),
        sa.Column("is_pyq", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("question_count", sa.Integer(), nullable=False),
        sa.Column("duration_seconds", sa.Integer(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", test_status_enum, server_default="IN_PROGRESS", nullable=False),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column("correct_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("wrong_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("unanswered_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("time_taken_seconds", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["chapter_id"], ["chapters.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["exam_id"], ["exams.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["subject_id"], ["subjects.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_test_attempts_chapter_id"), "test_attempts", ["chapter_id"], unique=False)
    op.create_index(op.f("ix_test_attempts_exam_id"), "test_attempts", ["exam_id"], unique=False)
    op.create_index(op.f("ix_test_attempts_status"), "test_attempts", ["status"], unique=False)
    op.create_index(op.f("ix_test_attempts_subject_id"), "test_attempts", ["subject_id"], unique=False)
    op.create_index(op.f("ix_test_attempts_user_id"), "test_attempts", ["user_id"], unique=False)
    op.create_index("ix_test_attempts_user_created", "test_attempts", ["user_id", "created_at"], unique=False)

    # 8. test_questions
    op.create_table(
        "test_questions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("test_attempt_id", sa.Uuid(), nullable=False),
        sa.Column("question_id", sa.Uuid(), nullable=False),
        sa.Column("question_order", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["test_attempt_id"], ["test_attempts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("test_attempt_id", "question_id", name="uq_test_attempt_question"),
        sa.UniqueConstraint("test_attempt_id", "question_order", name="uq_test_attempt_question_order"),
    )
    op.create_index(op.f("ix_test_questions_question_id"), "test_questions", ["question_id"], unique=False)
    op.create_index(op.f("ix_test_questions_test_attempt_id"), "test_questions", ["test_attempt_id"], unique=False)

    # 9. user_answers
    op.create_table(
        "user_answers",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("test_attempt_id", sa.Uuid(), nullable=False),
        sa.Column("test_question_id", sa.Uuid(), nullable=False),
        sa.Column("selected_option", sa.String(length=10), nullable=True),
        sa.Column("is_correct", sa.Boolean(), nullable=True),
        sa.Column("is_answered", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("answered_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["test_attempt_id"], ["test_attempts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["test_question_id"], ["test_questions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("test_attempt_id", "test_question_id", name="uq_test_attempt_test_question_answer"),
    )
    op.create_index(op.f("ix_user_answers_test_attempt_id"), "user_answers", ["test_attempt_id"], unique=False)
    op.create_index(op.f("ix_user_answers_test_question_id"), "user_answers", ["test_question_id"], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order of dependencies
    op.drop_index(op.f("ix_user_answers_test_question_id"), table_name="user_answers")
    op.drop_index(op.f("ix_user_answers_test_attempt_id"), table_name="user_answers")
    op.drop_table("user_answers")

    op.drop_index(op.f("ix_test_questions_test_attempt_id"), table_name="test_questions")
    op.drop_index(op.f("ix_test_questions_question_id"), table_name="test_questions")
    op.drop_table("test_questions")

    op.drop_index("ix_test_attempts_user_created", table_name="test_attempts")
    op.drop_index(op.f("ix_test_attempts_user_id"), table_name="test_attempts")
    op.drop_index(op.f("ix_test_attempts_subject_id"), table_name="test_attempts")
    op.drop_index(op.f("ix_test_attempts_status"), table_name="test_attempts")
    op.drop_index(op.f("ix_test_attempts_exam_id"), table_name="test_attempts")
    op.drop_index(op.f("ix_test_attempts_chapter_id"), table_name="test_attempts")
    op.drop_table("test_attempts")

    op.drop_index(op.f("ix_question_options_question_id"), table_name="question_options")
    op.drop_table("question_options")

    op.drop_index("ix_questions_chapter_diff_pyq_active", table_name="questions")
    op.drop_index(op.f("ix_questions_is_active"), table_name="questions")
    op.drop_index(op.f("ix_questions_pyq_year"), table_name="questions")
    op.drop_index(op.f("ix_questions_is_pyq"), table_name="questions")
    op.drop_index(op.f("ix_questions_difficulty"), table_name="questions")
    op.drop_index(op.f("ix_questions_chapter_id"), table_name="questions")
    op.drop_table("questions")

    op.drop_index(op.f("ix_chapters_subject_id"), table_name="chapters")
    op.drop_table("chapters")

    op.drop_index(op.f("ix_subjects_exam_id"), table_name="subjects")
    op.drop_table("subjects")

    op.drop_index(op.f("ix_exams_slug"), table_name="exams")
    op.drop_table("exams")

    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")

    bind = op.get_bind()
    test_status_enum.drop(bind, checkfirst=True)
    difficulty_enum.drop(bind, checkfirst=True)
