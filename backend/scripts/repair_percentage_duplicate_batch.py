"""Replace two newly imported repetitive savings templates with distinct items."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
spec = importlib.util.spec_from_file_location("percentage_bank", ROOT / "scripts" / "import_percentage_difficulty_expansion.py")
bank = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bank)

from app.database.session import SessionLocal
from app.models import Chapter, Difficulty, Exam, Question, Subject, TestQuestion
from app.services.question_import_service import import_questions

OLD_STEMS = {
    "A household's income rises 20% and its expenditure rises 30%. Initially it saves 20% of income. By what percentage does its saving amount change?",
    "A person's income increases by 15% and expenditure by 10%. Initially expenditure is 80% of income. By what percentage do savings increase?",
}
REPLACEMENT_PATTERNS = {"simple-interest-share", "defect-repair-rate"}


def main() -> None:
    replacements = [
        {key: value for key, value in row.items() if not key.startswith("_")}
        for row in bank.QUESTIONS if row["_pattern"] in REPLACEMENT_PATTERNS
    ]
    if len(replacements) != len(REPLACEMENT_PATTERNS):
        raise SystemExit("Expected exactly two curated replacement questions")
    with SessionLocal() as db:
        chapter = db.query(Chapter).join(Subject).join(Exam).filter(
            Exam.slug == "ssc", Subject.slug == "maths", Chapter.slug == "percentage",
        ).one()
        retired = db.query(Question).filter(
            Question.chapter_id == chapter.id,
            Question.question_text.in_(OLD_STEMS),
            Question.source == bank.REFERENCE,
            Question.is_pyq.is_(False),
        ).all()
        replacement_texts = {row["question_text"] for row in replacements}
        existing_texts = {
            q.question_text for q in db.query(Question).filter(
                Question.chapter_id == chapter.id, Question.question_text.in_(replacement_texts),
            ).all()
        }
        to_import = [row for row in replacements if row["question_text"] not in existing_texts]
        if to_import:
            payload = json.dumps({"questions": to_import}, ensure_ascii=False).encode("utf-8")
            preview = import_questions(db, payload, "application/json", "percentage_difficulty_expansion.json", True)
            if preview.aborted or preview.errors or preview.duplicates or preview.would_import != len(to_import):
                raise SystemExit(f"Replacement validation failed: {preview.model_dump()}")
            committed = import_questions(db, payload, "application/json", "percentage_difficulty_expansion.json", False)
            if committed.aborted or committed.errors or committed.duplicates or committed.imported != len(to_import):
                raise SystemExit(f"Replacement import failed: {committed.model_dump()}")
            print(f"Imported {committed.imported} validated replacements")

        removed = 0
        for question in retired:
            if db.query(TestQuestion.id).filter(TestQuestion.question_id == question.id).first():
                raise SystemExit(f"Refusing to remove a repeated question already assigned to an attempt: {question.id}")
            db.delete(question)
            removed += 1
        if removed:
            db.commit()
            print(f"Removed {removed} repetitive rows created by this batch")
        counts = {
            difficulty: db.query(Question).filter(
                Question.chapter_id == chapter.id, Question.is_active.is_(True),
                Question.is_pyq.is_(False), Question.difficulty == difficulty,
            ).count()
            for difficulty in (Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD)
        }
        print(f"Final active ordinary counts={{{', '.join(f'{d.value}: {n}' for d, n in counts.items())}}}")
        if any(counts[d] < bank.TARGET for d in (Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD)):
            raise SystemExit("Replacement correction left a difficulty below target")


if __name__ == "__main__":
    main()
