"""Apply narrowly guarded wording clarifications to the newly imported CH-19 rows."""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
from sqlalchemy import select
from app.database.session import SessionLocal
from app.models import Chapter, Question
from scripts.import_insert_missing_number_verified_batch import CHAPTER_ID, load_artifacts, norm

OLD_EXPLANATION = "The operation cycle is divide by 2, then multiply by 4. After 24÷2=12, multiply by 4 to get 48."
CLARIFICATIONS = {
    "Four numbers 2, 5, 3 and 4 are arranged around a centre. The centre is the product of the four surrounding numbers. Find it.": "Four numbers 2, 5, 3 and 4 are arranged around a centre, whose value is missing. The centre is the product of the four surrounding numbers. Find it.",
    "A segmented number row follows ÷2 and then ×4 repeatedly: 80, 40, 160, 30, 15, 60, 24, 12, __. Find the missing value.": "Each three-number row shows x, x÷2, and 2x: [80, 40, 160], [30, 15, 60], [24, 12, ?]. Find the missing value.",
    "In three rows, the third value is the product of the first two and 5: (12, 36, 60), (24, 72, 120), (33, 99, ?). Find the missing value.": "In each row, the second value is three times the first and the third is five times the first: (12, 36, 60), (24, 72, 120), (33, 99, ?). Find the missing value.",
}


def main():
    rows = load_artifacts()
    canonical = {norm(row["question_text"]): row for row in rows}
    with SessionLocal() as db:
        chapter = db.get(Chapter, CHAPTER_ID)
        if chapter is None or chapter.slug != "insert-the-missing-number":
            raise SystemExit("Refusing copy edit: guarded CH-19 chapter not found")
        existing = db.scalars(select(Question).where(Question.chapter_id == chapter.id).with_for_update()).all()
        if len(existing) != 30:
            raise SystemExit(f"Refusing copy edit: expected 30 CH-19 records, found {len(existing)}")
        updates = []
        for old_text, new_text in CLARIFICATIONS.items():
            matches = [q for q in existing if q.question_text == old_text]
            if len(matches) != 1 or norm(new_text) not in canonical:
                raise SystemExit("Refusing copy edit: exact old/new question match did not resolve uniquely")
            question = matches[0]
            target = canonical[norm(new_text)]
            actual_options = {o.option_key: o.option_text for o in question.options}
            actual_correct = [o.option_key for o in question.options if o.is_correct]
            if (actual_options != target["options"] or actual_correct != [target["correct_option"]]
                    or question.difficulty.value != target["difficulty"] or question.is_pyq
                    or question.source != target["source"] or not question.is_active):
                raise SystemExit(f"Refusing copy edit: non-wording fields differ for {old_text!r}")
            if old_text.startswith("A segmented") and question.explanation != OLD_EXPLANATION:
                raise SystemExit("Refusing copy edit: segmented-row explanation differs from the expected imported wording")
            if not old_text.startswith("A segmented") and question.explanation != target["explanation"]:
                raise SystemExit(f"Refusing copy edit: explanation unexpectedly differs for {old_text!r}")
            updates.append((question, target))
        for question, target in updates:
            question.question_text = target["question_text"]
            question.explanation = target["explanation"]
        db.commit()
        print("CH19_COPYEDIT_RECONCILED", {"records": len(updates), "fields": ["question_text", "explanation"]})


if __name__ == "__main__":
    main()
