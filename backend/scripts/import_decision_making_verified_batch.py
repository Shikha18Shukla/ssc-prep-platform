"""Guarded, dry-run-first importer for the reviewed CH-20 bank."""
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
from scripts.build_decision_making_artifacts import evaluate_candidate

BATCH = BASE / "data" / "decision_making_verified_batch.json"
LEDGER = BASE / "data" / "decision_making_answer_ledger.json"
CHAPTER_ID = "382f7052-28c0-4d51-a117-d59dde2934d5"
LEVELS = {"EASY": 11, "MEDIUM": 12, "HARD": 11}
ORIGINAL = "Original SSC-style practice question"


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def load_artifacts():
    rows = json.loads(BATCH.read_text(encoding="utf-8")).get("questions")
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    if not isinstance(rows, list) or len(rows) != 34 or not isinstance(ledger, list) or len(ledger) != 34:
        raise ValueError("CH-20 batch and ledger must each contain exactly 34 questions")
    if Counter(row.get("difficulty") for row in rows) != Counter(LEVELS):
        raise ValueError("Difficulty distribution must be 11 EASY, 12 MEDIUM, 11 HARD")
    if Counter(item.get("category") for item in ledger) != Counter({"ELIGIBILITY": 18, "SITUATIONAL": 16}):
        raise ValueError("Expected 18 eligibility and 16 situational questions")
    if Counter(row.get("correct_option") for row in rows) != Counter({"A": 9, "B": 9, "C": 8, "D": 8}):
        raise ValueError("Answer-position distribution must be A=9, B=9, C=8, D=8")
    ids, stems = set(), set()
    for index, (row, audit) in enumerate(zip(rows, ledger), 1):
        if (row.get("subject_slug"), row.get("subcategory_slug"), row.get("chapter_slug")) != ("reasoning", None, "decision-making"):
            raise ValueError(f"Row {index} chapter metadata mismatch")
        if row.get("is_pyq") is not False or row.get("pyq_year") is not None or row.get("pyq_exam_name") is not None:
            raise ValueError(f"Row {index} must be a Normal question, not a PYQ")
        if row.get("difficulty") not in LEVELS or not row.get("question_text", "").strip() or not row.get("explanation", "").strip():
            raise ValueError(f"Row {index} is missing stem/explanation or has invalid difficulty")
        options = row.get("options")
        if not isinstance(options, dict) or set(options) != set("ABCD") or any(not isinstance(value, str) or not value.strip() for value in options.values()) or len({norm(value) for value in options.values()}) != 4:
            raise ValueError(f"Row {index} must have four distinct non-empty options")
        correct = row.get("correct_option")
        if correct not in options or audit.get("row") != index or audit.get("id") != f"dm-{index:03d}":
            raise ValueError(f"Row {index} has an invalid answer or identity")
        if audit.get("question") != row["question_text"] or audit.get("options") != options or audit.get("correct_option") != correct:
            raise ValueError(f"Ledger mismatch at row {index}")
        if options[correct] != audit.get("correct_answer") or audit.get("independent_reasoning") != row["explanation"]:
            raise ValueError(f"Correct answer/explanation mismatch at row {index}")
        if audit.get("difficulty") != row["difficulty"] or audit.get("verification_status") != "independently_verified":
            raise ValueError(f"Verification metadata mismatch at row {index}")
        if len(row.get("source") or "") > 255 or (row["source"] != ORIGINAL and ("page " not in row["source"] or "exam/year not stated" not in row["source"])):
            raise ValueError(f"Unsupported provenance at row {index}")
        qid = audit.get("id")
        if qid in ids:
            raise ValueError(f"Duplicate stable ID {qid}")
        ids.add(qid)
        stem = norm(row["question_text"])
        if stem in stems:
            raise ValueError(f"Duplicate question text at row {index}")
        stems.add(stem)
        if audit.get("category") == "ELIGIBILITY":
            case = audit.get("eligibility")
            if not case:
                raise ValueError(f"Eligibility evaluator result missing at row {index}")
            evaluated = evaluate_candidate(case["candidate"], case["criteria"], case.get("referrals", []))
            if evaluated != case.get("evaluator_result") or evaluated.get("outcome") != case.get("expected_outcome"):
                raise ValueError(f"Independent eligibility evaluation conflicts at row {index}")
            answer_text = options[correct]
            expected_prefix = {"SELECT": "Select the candidate.", "REJECT": "Reject the candidate.", "INSUFFICIENT": "The information is insufficient to decide."}.get(evaluated["outcome"])
            if expected_prefix and answer_text != expected_prefix:
                raise ValueError(f"Eligibility answer choice conflicts with evaluator at row {index}")
            if evaluated["outcome"] == "REFER" and evaluated["authority"] not in answer_text:
                raise ValueError(f"Referral authority conflicts with evaluator at row {index}")
    return rows


def chapter_context(db):
    return db.execute(select(Exam, Subject, Chapter).join(Subject, Subject.exam_id == Exam.id).join(Chapter, Chapter.subject_id == Subject.id).where(
        Exam.slug == "ssc", Exam.is_active.is_(True), Subject.slug == "reasoning", Subject.is_active.is_(True),
        Chapter.slug == "decision-making", Chapter.is_active.is_(True), Chapter.subcategory_id.is_(None),
    )).one_or_none()


def verify_existing(rows, existing):
    expected = {norm(row["question_text"]): row for row in rows}
    seen = set()
    for question in existing:
        stem = norm(question.question_text)
        if stem in seen:
            raise ValueError("Database contains duplicate normalized CH-20 question text")
        seen.add(stem)
        row = expected.get(stem)
        if row is None:
            raise ValueError(f"Unexpected CH-20 record; refusing to modify it: {question.question_text!r}")
        options = {option.option_key: option.option_text for option in question.options}
        correct = [option.option_key for option in question.options if option.is_correct]
        if (question.question_text != row["question_text"] or question.explanation != row["explanation"]
                or question.difficulty.value != row["difficulty"] or question.is_pyq is not False
                or not question.is_active or question.source != row["source"] or options != row["options"]
                or correct != [row["correct_option"]]):
            raise ValueError(f"Existing CH-20 row conflicts with the canonical batch: {question.question_text!r}")


def duplicate_scan(rows, questions):
    candidates = {norm(row["question_text"]): row["question_text"] for row in rows}
    collisions, near = [], []
    for question in questions:
        candidate = norm(question.question_text)
        if candidate in candidates:
            collisions.append((question.id, candidates[candidate]))
            continue
        for stem in candidates.values():
            score = SequenceMatcher(None, candidate, norm(stem)).ratio()
            if score >= 0.92:
                near.append((question.id, round(score, 3), stem))
    if collisions or near:
        raise ValueError(f"Duplicate scan conflict: exact={collisions[:5]}, near={near[:5]}")


def canonical_question_texts(rows):
    for path in (BASE / "data").glob("*_verified_batch.json"):
        if path == BATCH:
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        records = data.get("questions", []) if isinstance(data, dict) else data if isinstance(data, list) else []
        for item in records:
            if isinstance(item, dict) and isinstance(item.get("question_text"), str):
                yield type("CanonicalQuestion", (), {"id": path.name, "question_text": item["question_text"]})()


def chapter_snapshot(db, chapter_id):
    return {str(question.id) for question in db.scalars(select(Question).where(Question.chapter_id != chapter_id)).all()}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="write only after guarded dry-run validation")
    args = parser.parse_args(argv)
    engine.echo = False
    rows = load_artifacts()
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    print("BATCH", len(rows), dict(Counter(row["difficulty"] for row in rows)))
    print("CATEGORIES", dict(Counter(item["category"] for item in ledger)))
    print("ANSWER_POSITIONS", dict(Counter(row["correct_option"] for row in rows)))
    print("PROVENANCE", {"source_derived": sum(row["source"] != ORIGINAL for row in rows), "original": sum(row["source"] == ORIGINAL for row in rows), "pyq": 0})
    with SessionLocal() as db:
        context = chapter_context(db)
        if context is None:
            raise SystemExit("Active SSC → Reasoning → Decision Making chapter was not found uniquely")
        _, _, chapter = context
        if str(chapter.id) != CHAPTER_ID:
            raise SystemExit(f"CH-20 ID mismatch: expected {CHAPTER_ID}, found {chapter.id}")
        existing = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        counts = Counter(q.difficulty.value for q in existing if q.is_active and not q.is_pyq)
        initial = {"records": len(existing), "active_normal": sum(q.is_active and not q.is_pyq for q in existing),
                   "active_pyq": sum(q.is_active and q.is_pyq for q in existing), "difficulty": dict(counts),
                   "question_ids": sorted(str(q.id) for q in existing)}
        print("CHAPTER", chapter.id, chapter.name, "BEFORE", initial)
        empty = not existing
        if not empty and len(existing) != 34:
            raise SystemExit("CH-20 baseline differs from empty chapter or exact replay; refusing import")
        verify_existing(rows, existing)
        other_live = db.scalars(select(Question).join(Chapter, Question.chapter_id == Chapter.id).join(Subject, Chapter.subject_id == Subject.id).join(Exam, Subject.exam_id == Exam.id).where(
            Exam.slug == "ssc", Subject.slug == "reasoning", Question.is_active.is_(True), Question.is_pyq.is_(False), Question.chapter_id != chapter.id
        )).all()
        duplicate_scan(rows, other_live)
        duplicate_scan(rows, canonical_question_texts(rows))
        before_other_ids = chapter_snapshot(db, chapter.id)
        preview = import_questions(db, json.dumps({"questions": rows}, ensure_ascii=False).encode(), "application/json", BATCH.name, True)
        print("DRY_RUN", preview.model_dump())
        if preview.aborted or preview.errors or preview.rejected or preview.duplicates != len(existing) or preview.would_import != 34 - len(existing):
            raise SystemExit("Dry-run differs from the guarded empty/replay expectation")
        if not args.apply:
            print("NO_DATABASE_CHANGES")
            return
        if not empty:
            print("IDEMPOTENT_REPLAY: no database writes")
            return
        applied = import_questions(db, json.dumps({"questions": rows}, ensure_ascii=False).encode(), "application/json", BATCH.name, False)
        print("IMPORT", applied.model_dump())
        if applied.aborted or applied.errors or applied.rejected or applied.duplicates or applied.imported != 34:
            db.rollback()
            raise SystemExit("Import result differs from the successful dry-run")
        after = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        verify_existing(rows, after)
        final_levels = Counter(q.difficulty.value for q in after if q.is_active and not q.is_pyq)
        if len(after) != 34 or final_levels != Counter(LEVELS) or any(q.is_pyq for q in after):
            db.rollback()
            raise SystemExit(f"Post-import CH-20 check failed: records={len(after)}, difficulties={final_levels}")
        if chapter_snapshot(db, chapter.id) != before_other_ids:
            db.rollback()
            raise SystemExit("Question IDs outside CH-20 changed; import rolled back")
        db.commit()
        print("AFTER", {"active_normal": 34, "active_pyq": 0, "difficulty": dict(final_levels), "other_chapter_ids_unchanged": True})
        print("POST_IMPORT_VERIFIED")


if __name__ == "__main__":
    main()
