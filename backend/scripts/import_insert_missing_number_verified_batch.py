"""Guarded, dry-run-first importer for the reviewed CH-19 bank."""
import argparse
import json
import sys
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
from sqlalchemy import select
from app.database.session import SessionLocal, engine
from app.models import Chapter, Exam, Question, Subject
from app.services.question_import_service import import_questions

BATCH = BASE / "data" / "insert_missing_number_verified_batch.json"
LEDGER = BASE / "data" / "insert_missing_number_answer_ledger.json"
CHAPTER_ID = "5c689750-c989-44e6-a221-58ba3977744f"
LEVELS = {"EASY": 10, "MEDIUM": 10, "HARD": 10}
ORIGINAL = "Original SSC-style practice question"


def norm(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def load_artifacts():
    rows = json.loads(BATCH.read_text(encoding="utf-8")).get("questions")
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    if not isinstance(rows, list) or len(rows) != 30 or not isinstance(ledger, list) or len(ledger) != 30:
        raise ValueError("CH-19 batch and ledger must each contain exactly 30 records")
    if Counter(row.get("difficulty") for row in rows) != Counter(LEVELS):
        raise ValueError("Difficulty distribution must be 10 EASY, 10 MEDIUM, 10 HARD")
    ids, stems, signatures = set(), set(), set()
    for index, (row, audit) in enumerate(zip(rows, ledger), 1):
        if (row.get("subject_slug"), row.get("subcategory_slug"), row.get("chapter_slug")) != ("reasoning", None, "insert-the-missing-number"):
            raise ValueError(f"Row {index} chapter metadata mismatch")
        if row.get("is_pyq") is not False or row.get("pyq_year") is not None or row.get("pyq_exam_name") is not None:
            raise ValueError(f"Row {index} must be Normal, not PYQ")
        if row.get("difficulty") not in LEVELS or not row.get("question_text", "").strip() or not row.get("explanation", "").strip():
            raise ValueError(f"Row {index} has missing stem/explanation or invalid difficulty")
        options = row.get("options")
        if not isinstance(options, dict) or set(options) != set("ABCD"):
            raise ValueError(f"Row {index} must have options A-D")
        if any(not isinstance(v, str) or not v.strip() for v in options.values()) or len({norm(v) for v in options.values()}) != 4:
            raise ValueError(f"Row {index} must have four distinct non-empty options")
        if row.get("correct_option") not in options:
            raise ValueError(f"Row {index} has invalid correct_option")
        source = row.get("source")
        if source != ORIGINAL and not (source.startswith("Insert the Missing Number 01 Class Notes.pdf, page ") and "exam/year not stated" in source):
            raise ValueError(f"Row {index} has unsupported provenance")
        if len(source) > 255:
            raise ValueError(f"Row {index} source is too long")
        if audit.get("row") != index or audit.get("id") != f"imn-{index:03d}" or audit.get("question") != row["question_text"]:
            raise ValueError(f"Ledger identity mismatch at row {index}")
        if audit.get("options") != options or audit.get("correct_option") != row["correct_option"]:
            raise ValueError(f"Ledger options/key mismatch at row {index}")
        if audit.get("expected_answer") != options[row["correct_option"]] or audit.get("difficulty") != row["difficulty"] or audit.get("source") != source:
            raise ValueError(f"Ledger answer/metadata mismatch at row {index}")
        if not audit.get("independent_reasoning", "").strip() or audit.get("verification_status") != "independently_verified":
            raise ValueError(f"Ledger missing independent solution at row {index}")
        stem = norm(row["question_text"])
        if stem in stems:
            raise ValueError(f"Duplicate question stem at row {index}")
        stems.add(stem)
        if audit.get("pattern") in signatures:
            raise ValueError(f"Repeated pattern signature at row {index}: {audit['pattern']}")
        signatures.add(audit["pattern"])
    return rows


def chapter_context(db):
    return db.execute(select(Exam, Subject, Chapter).join(Subject, Subject.exam_id == Exam.id).join(Chapter, Chapter.subject_id == Subject.id).where(
        Exam.slug == "ssc", Exam.is_active.is_(True), Subject.slug == "reasoning", Subject.is_active.is_(True),
        Chapter.slug == "insert-the-missing-number", Chapter.is_active.is_(True), Chapter.subcategory_id.is_(None),
    )).one_or_none()


def verify_existing(rows, existing):
    expected = {norm(r["question_text"]): r for r in rows}
    seen = set()
    for question in existing:
        stem = norm(question.question_text)
        if stem in seen:
            raise ValueError("Database contains duplicate normalized CH-19 stems")
        seen.add(stem)
        row = expected.get(stem)
        if row is None:
            raise ValueError(f"Unexpected CH-19 record; refusing to alter it: {question.question_text!r}")
        options = {o.option_key: o.option_text for o in question.options}
        correct = [o.option_key for o in question.options if o.is_correct]
        if (question.question_text != row["question_text"] or question.explanation != row["explanation"]
                or question.difficulty.value != row["difficulty"] or question.is_pyq is not False or not question.is_active
                or question.source != row["source"] or options != row["options"] or correct != [row["correct_option"]]):
            raise ValueError(f"Existing record conflicts with canonical CH-19: {question.question_text!r}")


def duplicate_scan(rows, questions):
    target = {norm(row["question_text"]): row["question_text"] for row in rows}
    collisions, near = [], []
    for question in questions:
        candidate = norm(question.question_text)
        if candidate in target:
            collisions.append((question.id, target[candidate]))
            continue
        for new_stem in target.values():
            score = SequenceMatcher(None, candidate, norm(new_stem)).ratio()
            if score >= 0.92:
                near.append((question.id, round(score, 3), new_stem))
    if collisions or near:
        raise ValueError(f"Duplicate scan conflict: exact={collisions[:5]}, near={near[:5]}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="apply only after guarded dry-run checks")
    args = parser.parse_args(argv)
    engine.echo = False
    rows = load_artifacts()
    print("BATCH", len(rows), dict(Counter(r["difficulty"] for r in rows)))
    print("PROVENANCE", {"source_derived": sum(r["source"] != ORIGINAL for r in rows), "original": sum(r["source"] == ORIGINAL for r in rows), "pyq": 0})
    with SessionLocal() as db:
        context = chapter_context(db)
        if context is None:
            raise SystemExit("Active SSC → Reasoning → Insert the Missing Number chapter was not found uniquely")
        _, _, chapter = context
        if str(chapter.id) != CHAPTER_ID:
            raise SystemExit(f"CH-19 ID mismatch: expected {CHAPTER_ID}, found {chapter.id}")
        existing = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        normal = sum(q.is_active and not q.is_pyq for q in existing)
        pyq = sum(q.is_active and q.is_pyq for q in existing)
        print("CHAPTER", chapter.id, chapter.name, "BEFORE", {"normal": normal, "pyq": pyq, "records": len(existing)})
        if (normal, pyq, len(existing)) not in {(0, 0, 0), (30, 0, 30)}:
            raise SystemExit("CH-19 baseline differs from empty chapter or exact replay; refusing import")
        verify_existing(rows, existing)
        reasoning_questions = db.scalars(select(Question).join(Chapter, Question.chapter_id == Chapter.id).join(Subject, Chapter.subject_id == Subject.id).join(Exam, Subject.exam_id == Exam.id).where(
            Exam.slug == "ssc", Subject.slug == "reasoning", Question.is_active.is_(True), Question.is_pyq.is_(False)
        )).all()
        duplicate_scan(rows, [q for q in reasoning_questions if q.chapter_id != chapter.id])
        result = import_questions(db, json.dumps({"questions": rows}, ensure_ascii=False).encode(), "application/json", BATCH.name, True)
        print("DRY_RUN", result.model_dump())
        if result.aborted or result.errors or result.rejected or result.duplicates != len(existing) or result.would_import != 30-len(existing):
            raise SystemExit("Dry-run did not match the guarded insert/replay count")
        if not args.apply:
            print("NO_DATABASE_CHANGES")
            return
        if normal == 30:
            print("IDEMPOTENT_REPLAY: zero additional inserts")
            return
        applied = import_questions(db, json.dumps({"questions": rows}, ensure_ascii=False).encode(), "application/json", BATCH.name, False)
        print("IMPORT", applied.model_dump())
        if applied.aborted or applied.errors or applied.rejected or applied.imported != 30 or applied.duplicates:
            db.rollback()
            raise SystemExit("Import result differed from successful guarded dry-run")
        after = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        verify_existing(rows, after)
        counts = Counter(q.difficulty.value for q in after if q.is_active and not q.is_pyq)
        if len(after) != 30 or counts != Counter(LEVELS) or any(q.is_pyq for q in after):
            db.rollback()
            raise SystemExit(f"Post-import verification failed: records={len(after)}, levels={counts}")
        db.commit()
        print("AFTER", {"active_normal": 30, "active_pyq": 0, "difficulty": dict(counts)})
        print("POST_IMPORT_VERIFIED")

if __name__ == "__main__":
    main()
