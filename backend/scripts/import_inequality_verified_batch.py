"""Guarded dry-run and idempotent importer for the CH-16 Inequality bank."""

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
from build_inequality_artifacts import classify_claim, conclusion_outcome

BATCH = BASE / "data" / "inequality_verified_batch.json"
LEDGER = BASE / "data" / "inequality_answer_ledger.json"
CHAPTER_ID = "6d8b6da5-6635-417c-99e4-0bb7f511520b"
COUNTS = Counter({"EASY": 10, "MEDIUM": 10, "HARD": 10})


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def load_artifacts():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    selected = [entry for entry in ledger if entry.get("record_type") == "selected_question"]
    rejected = [entry for entry in ledger if entry.get("record_type") == "rejected_source_prompt"]
    if len(rows) != 30 or len(selected) != 30 or len(rejected) != 2 or Counter(r["difficulty"] for r in rows) != COUNTS:
        raise ValueError("Canonical bank must contain 30 questions, 10 per difficulty")
    stems, signatures = set(), set()
    for i, (row, audit) in enumerate(zip(rows, selected), 1):
        if (row.get("subject_slug"), row.get("subcategory_slug"), row.get("chapter_slug")) != ("reasoning", None, "inequality"):
            raise ValueError(f"Row {i} has incorrect catalog metadata")
        if row.get("is_pyq") is not False or row.get("pyq_year") is not None or row.get("pyq_exam_name") is not None:
            raise ValueError(f"Row {i} is not a Normal question")
        opts = row.get("options")
        if not isinstance(opts, dict) or set(opts) != set("ABCD") or any(not isinstance(v, str) or not v.strip() for v in opts.values()) or len({norm(v) for v in opts.values()}) != 4:
            raise ValueError(f"Row {i} must have four distinct nonempty options")
        if row.get("correct_option") not in opts or not row.get("explanation", "").strip():
            raise ValueError(f"Row {i} has an invalid key or missing explanation")
        stem = norm(row["question_text"])
        if stem in stems:
            raise ValueError(f"Duplicate bank question at row {i}")
        stems.add(stem)
        signature = audit.get("concept_signature")
        if not signature or signature in signatures:
            raise ValueError(f"Missing/repeated concept signature at row {i}")
        signatures.add(signature)
        if audit.get("row") != i or audit.get("question") != row["question_text"] or audit.get("chapter_id") != CHAPTER_ID:
            raise ValueError(f"Ledger alignment failure at row {i}")
        if audit.get("correct_option") != row["correct_option"] or audit.get("correct_answer") != opts[row["correct_option"]]:
            raise ValueError(f"Ledger answer mismatch at row {i}")
        if audit.get("options") != opts:
            raise ValueError(f"Ledger options mismatch at row {i}")
        if audit.get("difficulty") != row["difficulty"] or audit.get("is_pyq") is not False or not audit.get("independent_verification", "").strip():
            raise ValueError(f"Ledger validation failure at row {i}")
        src = row.get("source", "")
        if not src or len(src) > 255:
            raise ValueError(f"Invalid source provenance at row {i}")
        result = classify_claim(audit["statements"], audit["claim"]) if audit.get("claim") else conclusion_outcome(audit["statements"], audit["conclusions"])
        if result != audit.get("expected_outcome") or not audit.get("explanation", "").strip():
            raise ValueError(f"Independent mathematical validation failed at row {i}")
    return rows


def chapter_context(db):
    return db.execute(select(Exam, Subject, Chapter)
        .join(Subject, Subject.exam_id == Exam.id).join(Chapter, Chapter.subject_id == Subject.id)
        .where(Exam.slug == "ssc", Exam.is_active.is_(True), Subject.slug == "reasoning",
               Subject.is_active.is_(True), Chapter.slug == "inequality", Chapter.is_active.is_(True),
               Chapter.subcategory_id.is_(None))).one_or_none()


def verify_existing(rows, existing):
    expected = {norm(row["question_text"]): row for row in rows}
    found = set()
    for q in existing:
        stem = norm(q.question_text)
        if stem in found or stem not in expected:
            raise ValueError("Unexpected or duplicate Inequality record blocks safe import")
        found.add(stem)
        row = expected[stem]
        options = {o.option_key: o.option_text for o in q.options}
        correct = [o.option_key for o in q.options if o.is_correct]
        if (q.question_text != row["question_text"] or q.explanation != row["explanation"]
            or q.difficulty.value != row["difficulty"] or q.is_pyq is not False
            or q.pyq_year is not None or q.pyq_exam_name is not None or q.source != row["source"]
            or not q.is_active or options != row["options"] or correct != [row["correct_option"]]):
            raise ValueError("Existing Inequality record conflicts with canonical content")


def validate_preview(preview, existing_count):
    if (preview.aborted or preview.errors or preview.rejected
            or preview.duplicates != existing_count or preview.would_import != 30 - existing_count):
        raise ValueError("Importer dry-run differs from the expected count")


def validate_replay(replay):
    if replay.aborted or replay.errors or replay.rejected or replay.would_import or replay.duplicates != 30:
        raise ValueError("Replay dry-run was not idempotent")


def duplicate_scan(db, chapter_id, rows):
    prior = db.scalars(select(Question.question_text).join(Chapter, Chapter.id == Question.chapter_id)
        .join(Subject, Subject.id == Chapter.subject_id).where(Subject.slug == "reasoning", Question.chapter_id != chapter_id)).all()
    exact, near = [], []
    for text in prior:
        for row in rows:
            score = SequenceMatcher(None, norm(text), norm(row["question_text"])).ratio()
            if score == 1:
                exact.append(text)
            elif score >= .94:
                near.append((text, row["question_text"], round(score, 3)))
    if exact or near:
        raise ValueError(f"Cross-chapter duplicate review needed: exact={exact[:3]!r}; near={near[:3]!r}")
    return len(prior)


def canonical_duplicate_scan(rows):
    """Compare this bank against every canonical question batch in backend/data."""
    exact, near, scanned = [], [], 0
    candidate = [(norm(row["question_text"]), row["question_text"]) for row in rows]
    for path in (BASE / "data").glob("*.json"):
        if path.resolve() == BATCH.resolve() or "answer_ledger" in path.name or "source_review" in path.name:
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        prior_rows = payload.get("questions", []) if isinstance(payload, dict) else []
        for prior in prior_rows if isinstance(prior_rows, list) else []:
            if not isinstance(prior, dict) or prior.get("subject_slug") != "reasoning":
                continue
            text = prior.get("question_text")
            if not isinstance(text, str) or not text.strip():
                continue
            scanned += 1
            normalized = norm(text)
            for current, current_raw in candidate:
                ratio = SequenceMatcher(None, normalized, current).ratio()
                if ratio == 1:
                    exact.append((path.name, text))
                elif ratio >= .94:
                    near.append((path.name, text, current_raw, round(ratio, 3)))
    if exact or near:
        raise ValueError(f"Canonical duplicate review needed: exact={exact[:3]!r}; near={near[:3]!r}")
    return scanned


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="import only from exact empty baseline after clean dry-run")
    args = parser.parse_args(argv)
    engine.echo = False
    rows = load_artifacts()
    print("BATCH", len(rows), dict(Counter(r["difficulty"] for r in rows)))
    print("CANONICAL_REASONING_ROWS_SCANNED", canonical_duplicate_scan(rows))
    with SessionLocal() as db:
        context = chapter_context(db)
        if context is None:
            raise SystemExit("Active SSC → Reasoning → Inequality chapter was not uniquely found")
        _, _, chapter = context
        if str(chapter.id) != CHAPTER_ID:
            raise SystemExit(f"Chapter id mismatch: {chapter.id}")
        existing = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        verify_existing(rows, existing)
        active_normal = sum(q.is_active and not q.is_pyq for q in existing)
        active_pyq = sum(q.is_active and q.is_pyq for q in existing)
        if (len(existing), active_normal, active_pyq) not in {(0, 0, 0), (30, 30, 0)}:
            raise SystemExit("Baseline must be empty or exactly the completed 30-row batch")
        print("CROSS_CHAPTER_REASONING_RECORDS_SCANNED", duplicate_scan(db, chapter.id, rows))
        payload = json.dumps({"questions": rows}, ensure_ascii=False).encode()
        dry = import_questions(db, payload, "application/json", BATCH.name, True)
        print("DRY_RUN", dry.model_dump())
        try:
            validate_preview(dry, len(existing))
        except ValueError as exc:
            raise SystemExit(str(exc))
        if not args.apply:
            print("NO_DATABASE_CHANGES")
            return
        if len(existing) == 30:
            print("IDEMPOTENT_REPLAY: zero additional inserts")
            return
        result = import_questions(db, payload, "application/json", BATCH.name, False)
        print("IMPORT", result.model_dump())
        if result.aborted or result.errors or result.rejected or result.imported != 30 or result.duplicates:
            raise SystemExit("Importer did not insert exactly 30 questions")
        after = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        verify_existing(rows, after)
        active = [q for q in after if q.is_active and not q.is_pyq]
        pyq = [q for q in after if q.is_pyq and q.is_active]
        counts = Counter(q.difficulty.value for q in active)
        if len(after) != 30 or len(active) != 30 or pyq or counts != COUNTS:
            raise SystemExit(f"Post-import verification failed: {len(after)=}, {len(active)=}, {len(pyq)=}, {dict(counts)=}")
        replay = import_questions(db, payload, "application/json", BATCH.name, True)
        print("REPLAY_DRY_RUN", replay.model_dump())
        try:
            validate_replay(replay)
        except ValueError as exc:
            raise SystemExit(str(exc))
        print("AFTER", {"active_normal": 30, "active_pyq": 0, "difficulty": dict(counts)})
        print("POST_IMPORT_VERIFIED")


if __name__ == "__main__":
    main()
