"""Idempotently seed SSC exams, subjects, subcategories, and source chapters.

This script never creates or modifies question-bank content and never deletes
catalog records. Existing question-bearing chapters are not renamed or moved.
"""

import logging
import sys
from collections import Counter, defaultdict
from pathlib import Path

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.database.ssc_catalog import EXCLUDED_SOURCE_CARDS, SSC_CATALOG, iter_catalog_chapters, slugify
from app.models import Chapter, Exam, Question, Subject, Subcategory

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
        "name": "GK / GS",
        "slug": "gk-gs",
        "description": "General Knowledge & General Studies",
        "display_order": 1,
        "is_active": True,
    },
    {
        "name": "Maths",
        "slug": "maths",
        "description": "Quantitative Aptitude",
        "display_order": 2,
        "is_active": True,
    },
    {
        "name": "English",
        "slug": "english",
        "description": "English Language & Comprehension",
        "display_order": 3,
        "is_active": True,
    },
    {
        "name": "Reasoning",
        "slug": "reasoning",
        "description": "General Intelligence & Reasoning",
        "display_order": 4,
        "is_active": True,
    },
]


def _upsert_by_slug(db: Session, model, values: dict) -> object:
    existing = db.execute(select(model).where(model.slug == values["slug"])).scalar_one_or_none()
    if existing is None:
        existing = model(**values)
        db.add(existing)
        db.flush()
        return existing
    for key, value in values.items():
        setattr(existing, key, value)
    return existing


def _chapter_conflict(db: Session, chapter: Chapter, target_name: str, target_category: str | None) -> str:
    question_count = db.execute(
        select(func.count(Question.id)).where(Question.chapter_id == chapter.id)
    ).scalar_one()
    category_name = target_category or "directly under the subject"
    return (
        f"Chapter '{chapter.name}' (id={chapter.id}, slug='{chapter.slug}', "
        f"questions={question_count}) conflicts with PDF chapter '{target_name}' "
        f"in '{category_name}'. It was left unchanged; reconcile it manually."
    )


def _seed_chapters(db: Session, subject_ids: dict[str, object], subcategory_ids: dict[tuple[str, str], object]) -> list[str]:
    targets = [
        (subject_slug, category_slug, name, order, slugify(name))
        for subject_slug, category_slug, name, order in iter_catalog_chapters()
    ]
    scope_count: Counter[tuple[str, str]] = Counter(
        (subject_slug, chapter_slug) for subject_slug, _, _, _, chapter_slug in targets
    )

    subject_id_to_slug = {subject_ids[slug]: slug for slug in subject_ids}
    existing = list(
        db.execute(
            select(Chapter).where(Chapter.subject_id.in_(list(subject_id_to_slug)))
        ).scalars().all()
    )
    by_scope: dict[tuple[object, object | None, str], Chapter] = {
        (chapter.subject_id, chapter.subcategory_id, chapter.slug): chapter
        for chapter in existing
    }
    by_subject_slug: dict[tuple[object, str], list[Chapter]] = defaultdict(list)
    for chapter in existing:
        by_subject_slug[(chapter.subject_id, slugify(chapter.name))].append(chapter)
        if chapter.slug != slugify(chapter.name):
            by_subject_slug[(chapter.subject_id, chapter.slug)].append(chapter)

    question_counts = dict(
        db.execute(
            select(Question.chapter_id, func.count(Question.id))
            .where(Question.chapter_id.in_([chapter.id for chapter in existing]))
            .group_by(Question.chapter_id)
        ).all()
    ) if existing else {}
    conflicts: set[str] = set()

    for subject_slug, category_slug, name, order, chapter_slug in targets:
        subject_id = subject_ids[subject_slug]
        category_id = (
            subcategory_ids[(subject_slug, category_slug)] if category_slug is not None else None
        )
        target_scope = (subject_id, category_id, chapter_slug)
        chapter = by_scope.get(target_scope)

        if chapter is not None:
            question_count = question_counts.get(chapter.id, 0)
            if chapter.name != name and question_count:
                conflicts.add(_chapter_conflict(db, chapter, name, category_slug))
                continue
            chapter.display_order = order
            if not question_count:
                chapter.name = name
                chapter.is_active = True
            continue

        matching = by_subject_slug.get((subject_id, chapter_slug), [])
        direct_candidates = [item for item in matching if item.subcategory_id is None]
        if direct_candidates and category_id is not None:
            legacy = direct_candidates[0]
            if scope_count[(subject_slug, chapter_slug)] != 1:
                conflicts.add(_chapter_conflict(db, legacy, name, category_slug))
                continue
            if legacy.name != name or question_counts.get(legacy.id, 0):
                conflicts.add(_chapter_conflict(db, legacy, name, category_slug))
                continue
            legacy.subcategory_id = category_id
            legacy.display_order = order
            legacy.is_active = True
            by_scope[target_scope] = legacy
            continue

        if matching and category_id is None:
            conflicts.add(_chapter_conflict(db, matching[0], name, None))
            continue

        if matching and category_id is not None and scope_count[(subject_slug, chapter_slug)] == 1:
            conflicting_category = matching[0]
            conflicts.add(_chapter_conflict(db, conflicting_category, name, category_slug))
            continue

        chapter = Chapter(
            subject_id=subject_id,
            subcategory_id=category_id,
            name=name,
            slug=chapter_slug,
            display_order=order,
            is_active=True,
        )
        db.add(chapter)
        db.flush()
        by_scope[target_scope] = chapter
        by_subject_slug[(subject_id, chapter_slug)].append(chapter)

    return sorted(conflicts)


def seed_database(db: Session) -> list[str]:
    """Seed active SSC catalog records without deleting or duplicating rows.

    Returns reconciliation messages for existing chapter conflicts. The CLI
    writes these messages to ``backend/catalog_reconciliation_report.md``.
    """
    logger.info("Starting SSC catalog seed...")
    exams_by_slug = {
        exam_info["slug"]: _upsert_by_slug(db, Exam, exam_info)
        for exam_info in EXAMS_SEED_DATA
    }
    ssc_exam = exams_by_slug["ssc"]

    subject_ids: dict[str, object] = {}
    for subject_info in SSC_SUBJECTS_SEED_DATA:
        subject = db.execute(
            select(Subject).where(
                Subject.exam_id == ssc_exam.id,
                Subject.slug == subject_info["slug"],
            )
        ).scalar_one_or_none()
        if subject is None:
            subject = Subject(exam_id=ssc_exam.id, **subject_info)
            db.add(subject)
            db.flush()
        else:
            for key, value in subject_info.items():
                setattr(subject, key, value)
        subject_ids[subject_info["slug"]] = subject.id

    subcategory_ids: dict[tuple[str, str], object] = {}
    for subject_slug, groups in SSC_CATALOG.items():
        for display_order, (name, _chapter_names) in enumerate(groups, start=1):
            if name is None:
                continue
            slug = slugify(name)
            values = {
                "name": name,
                "slug": slug,
                "display_order": display_order,
                "is_active": True,
            }
            subcategory = db.execute(
                select(Subcategory).where(
                    Subcategory.subject_id == subject_ids[subject_slug],
                    Subcategory.slug == slug,
                )
            ).scalar_one_or_none()
            if subcategory is None:
                subcategory = Subcategory(
                    subject_id=subject_ids[subject_slug],
                    description=None,
                    **values,
                )
                db.add(subcategory)
                db.flush()
            else:
                for key, value in values.items():
                    setattr(subcategory, key, value)
            subcategory_ids[(subject_slug, slug)] = subcategory.id

    conflicts = _seed_chapters(db, subject_ids, subcategory_ids)
    db.commit()
    logger.info(
        "SSC catalog seed complete: %d chapters requested; %d excluded source cards.",
        sum(len(chapters) for groups in SSC_CATALOG.values() for _, chapters in groups),
        len(EXCLUDED_SOURCE_CARDS),
    )
    if conflicts:
        logger.warning("Chapter reconciliation required for %d existing record(s).", len(conflicts))
        for conflict in conflicts:
            logger.warning("%s", conflict)
    return conflicts


def _write_reconciliation_report(conflicts: list[str]) -> None:
    report_path = Path(__file__).resolve().parents[2] / "catalog_reconciliation_report.md"
    bullets = "\n".join(f"- {conflict}" for conflict in conflicts)
    report_path.write_text(
        "# SSC catalog reconciliation required\n\n"
        "The seed preserved these existing chapter records and did not rename, "
        "move, or duplicate them. Review each item before assigning it to the "
        "PDF catalog.\n\n"
        f"{bullets}\n",
        encoding="utf-8",
    )
    logger.warning("Wrote reconciliation report: %s", report_path)


def main() -> None:
    """CLI entrypoint for safe catalog seeding."""
    db = SessionLocal()
    try:
        conflicts = seed_database(db)
        if conflicts:
            _write_reconciliation_report(conflicts)
    except Exception as exc:
        db.rollback()
        logger.error("Catalog seed failed: %s", exc)
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
