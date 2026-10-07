"""Structural seed data for SSC Prep Platform.

Seeds foundational exam categories and SSC subjects.
Does NOT create test questions or user accounts.
Idempotent — safe to run multiple times.
"""

import logging
import sys

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.models.exam import Exam
from app.models.subject import Subject

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

EXAMS_SEED_DATA = [
    {
        "name": "SSC",
        "slug": "ssc",
        "description": "Staff Selection Commission Examinations (CGL, CHSL, MTS, CPO, GD)",
        "is_active": True,
    },
    {
        "name": "Railway",
        "slug": "railway",
        "description": "Railway Recruitment Board Examinations (RRB NTPC, Group D, ALP)",
        "is_active": False,
    },
    {
        "name": "Banking",
        "slug": "banking",
        "description": "Banking Sector Examinations (IBPS PO/Clerk, SBI PO/Clerk, RBI)",
        "is_active": False,
    },
    {
        "name": "Police",
        "slug": "police",
        "description": "State and Central Police Force Examinations (SI, Constable)",
        "is_active": False,
    },
]

SSC_SUBJECTS_SEED_DATA = [
    {
        "name": "GK/GS",
        "slug": "gk-gs",
        "description": "General Knowledge & General Studies (History, Polity, Geography, Economy, Science, Current Affairs)",
        "display_order": 1,
        "is_active": True,
    },
    {
        "name": "Maths",
        "slug": "maths",
        "description": "Quantitative Aptitude (Arithmetic, Advanced Maths, Geometry, Trigonometry, Algebra)",
        "display_order": 2,
        "is_active": True,
    },
    {
        "name": "English",
        "slug": "english",
        "description": "English Language & Comprehension (Grammar, Vocabulary, Reading Comprehension)",
        "display_order": 3,
        "is_active": True,
    },
    {
        "name": "Reasoning",
        "slug": "reasoning",
        "description": "General Intelligence & Reasoning (Verbal, Non-Verbal, Analytical)",
        "display_order": 4,
        "is_active": True,
    },
]


def seed_database(db: Session) -> None:
    """Seed base exams and SSC subjects if not already present."""
    logger.info("Starting database seed...")

    # Seed Exams
    exams_by_slug: dict[str, Exam] = {}
    for exam_info in EXAMS_SEED_DATA:
        stmt = select(Exam).where(Exam.slug == exam_info["slug"])
        existing = db.execute(stmt).scalar_one_or_none()

        if existing is None:
            exam = Exam(**exam_info)
            db.add(exam)
            db.flush()
            exams_by_slug[exam.slug] = exam
            logger.info("Created exam: %s (active=%s)", exam.name, exam.is_active)
        else:
            exams_by_slug[existing.slug] = existing
            logger.info("Exam already exists: %s", existing.name)

    # Seed Subjects for SSC
    ssc_exam = exams_by_slug.get("ssc")
    if ssc_exam:
        for subj_info in SSC_SUBJECTS_SEED_DATA:
            stmt = select(Subject).where(
                Subject.exam_id == ssc_exam.id,
                Subject.slug == subj_info["slug"],
            )
            existing_subj = db.execute(stmt).scalar_one_or_none()

            if existing_subj is None:
                subject = Subject(exam_id=ssc_exam.id, **subj_info)
                db.add(subject)
                logger.info("Created subject: %s for SSC", subj_info["name"])
            else:
                logger.info("Subject already exists: %s", existing_subj.name)

    db.commit()
    logger.info("Database seed completed successfully.")


def main() -> None:
    """CLI entrypoint for seeding."""
    db = SessionLocal()
    try:
        seed_database(db)
    except Exception as exc:
        db.rollback()
        logger.error("Seeding failed: %s", exc)
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
