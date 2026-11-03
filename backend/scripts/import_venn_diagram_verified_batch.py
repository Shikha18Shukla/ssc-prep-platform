"""Validate, dry-run, and safely import the reviewed Venn Diagram Normal bank."""

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

BATCH = BASE / "data" / "venn_diagram_verified_batch.json"
LEDGER = BASE / "data" / "venn_diagram_answer_ledger.json"
EXPECTED_CHAPTER_ID = "4834b66c-18db-49f8-8e0c-6ad98ed3c6e1"
EXPECTED_COUNTS = Counter({"EASY": 10, "MEDIUM": 10, "HARD": 10})
ORIGINAL = "Original SSC-style practice question"


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def load_artifacts():
    rows = json.loads(BATCH.read_text(encoding="utf-8")).get("questions")
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    selected = [entry for entry in ledger if entry.get("record_type") == "selected_question"]
    if not isinstance(rows, list) or len(rows) != 30 or len(selected) != len(rows):
        raise ValueError("Venn batch must contain 30 rows aligned with selected ledger entries")
    if Counter(row.get("difficulty") for row in rows) != EXPECTED_COUNTS:
        raise ValueError("Difficulty distribution must be 10 EASY, 10 MEDIUM, 10 HARD")
    if sum(entry.get("record_type") == "rejected_source_prompt" for entry in ledger) != 12:
        raise ValueError("Ledger must preserve all 12 rejected source-prompt reviews")
    stems, signatures = set(), set()
    for i, (row, audit) in enumerate(zip(rows, selected), 1):
        if (row.get("subject_slug"), row.get("subcategory_slug"), row.get("chapter_slug")) != ("reasoning", None, "venn-diagram"):
            raise ValueError(f"Row {i} has incorrect catalog metadata")
        if row.get("is_pyq") is not False or row.get("pyq_year") is not None or row.get("pyq_exam_name") is not None:
            raise ValueError(f"Row {i} is not valid Normal metadata")
        if not row.get("question_text", "").strip() or not row.get("explanation", "").strip():
            raise ValueError(f"Row {i} is missing its stem or explanation")
        options = row.get("options")
        if not isinstance(options, dict) or set(options) != set("ABCD"):
            raise ValueError(f"Row {i} must have exactly options A-D")
        if any(not isinstance(v, str) or not v.strip() for v in options.values()) or len({norm(v) for v in options.values()}) != 4:
            raise ValueError(f"Row {i} options must be four distinct nonempty strings")
        key = row.get("correct_option")
        if key not in options or norm(options[key]) not in {norm(v) for v in options.values()}:
            raise ValueError(f"Row {i} has no uniquely keyed answer")
        source = row.get("source")
        valid_pdf = isinstance(source, str) and source.startswith("Venn Diagram 0") and source.endswith("; exam/year not stated")
        if source != ORIGINAL and not valid_pdf:
            raise ValueError(f"Row {i} has unsupported provenance")
        if len(source) > 255:
            raise ValueError(f"Row {i} provenance exceeds the database field length")
        stem = norm(row["question_text"])
        if stem in stems:
            raise ValueError(f"Repeated stem in row {i}")
        stems.add(stem)
        if audit.get("question_id") != f"venn-{i:03}" or audit.get("row") != i or audit.get("question") != row["question_text"]:
            raise ValueError(f"Row {i} does not align with stable ledger identifiers")
        if audit.get("options") != options or audit.get("expected_answer") != options[key] or audit.get("correct_option") != key:
            raise ValueError(f"Row {i} answer/options conflict with ledger")
        if audit.get("difficulty") != row["difficulty"] or audit.get("source") != source:
            raise ValueError(f"Row {i} difficulty/source conflicts with ledger")
        if not audit.get("independent_verification", "").strip() or not audit.get("validation_status", "").startswith("PASS"):
            raise ValueError(f"Row {i} lacks independent answer verification")
        signature = audit.get("concept_signature")
        if not signature or signature in signatures:
            raise ValueError(f"Row {i} has a missing or repeated concept signature")
        signatures.add(signature)
        if audit.get("is_pyq") is not False:
            raise ValueError(f"Row {i} is not Normal in the ledger")
        if audit.get("question_category") not in {"logical_classification", "numerical"}:
            raise ValueError(f"Row {i} has invalid question category")
    return rows


def chapter_context(db):
    return db.execute(
        select(Exam, Subject, Chapter)
        .join(Subject, Subject.exam_id == Exam.id)
        .join(Chapter, Chapter.subject_id == Subject.id)
        .where(
            Exam.slug == "ssc", Exam.is_active.is_(True), Subject.slug == "reasoning",
            Subject.is_active.is_(True), Chapter.slug == "venn-diagram", Chapter.is_active.is_(True),
            Chapter.subcategory_id.is_(None),
        )
    ).one_or_none()


def verify_existing(rows, existing):
    expected = {norm(row["question_text"]): row for row in rows}
    actual = {}
    for question in existing:
        stem = norm(question.question_text)
        if stem in actual or stem not in expected:
            raise ValueError("Unexpected or duplicate existing Venn Diagram record prevents safe import")
        actual[stem] = question
        row = expected[stem]
        options = {o.option_key: o.option_text for o in question.options}
        keys = [o.option_key for o in question.options if o.is_correct]
        if (question.question_text != row["question_text"] or question.explanation != row["explanation"]
                or question.difficulty.value != row["difficulty"] or question.is_pyq is not False
                or question.pyq_year is not None or question.pyq_exam_name is not None
                or question.source != row["source"] or not question.is_active
                or options != row["options"] or keys != [row["correct_option"]]):
            raise ValueError("Existing Venn Diagram record conflicts with canonical batch")
    return actual


def check_reasoning_duplicates(db, chapter_id, rows):
    candidate_stems = [norm(row["question_text"]) for row in rows]
    existing = db.scalars(
        select(Question.question_text)
        .join(Chapter, Chapter.id == Question.chapter_id)
        .join(Subject, Subject.id == Chapter.subject_id)
        .where(Subject.slug == "reasoning", Question.chapter_id != chapter_id)
    ).all()
    exact, near = [], []
    for text in existing:
        prior = norm(text)
        for candidate in candidate_stems:
            ratio = SequenceMatcher(None, prior, candidate).ratio()
            if ratio == 1:
                exact.append(text)
            elif ratio >= 0.94:
                near.append((text, candidate, round(ratio, 3)))
    if exact or near:
        raise ValueError(f"Cross-chapter Reasoning duplicate review required: exact={exact[:3]!r}; near={near[:3]!r}")
    return len(existing)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="apply only after every catalog, baseline and dry-run guard passes")
    args = parser.parse_args(argv)
    engine.echo = False
    rows = load_artifacts()
    print("BATCH", len(rows), dict(Counter(row["difficulty"] for row in rows)))
    with SessionLocal() as db:
        context = chapter_context(db)
        if context is None:
            raise SystemExit("Active SSC → Reasoning → Venn Diagram chapter was not found uniquely")
        _, _, chapter = context
        if str(chapter.id) != EXPECTED_CHAPTER_ID:
            raise SystemExit(f"Chapter ID mismatch: expected reference {EXPECTED_CHAPTER_ID}, found {chapter.id}")
        existing = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        active_normal = sum(q.is_active and not q.is_pyq for q in existing)
        active_pyq = sum(q.is_active and q.is_pyq for q in existing)
        print("CHAPTER", chapter.id, chapter.name)
        print("BEFORE", {"active_normal": active_normal, "active_pyq": active_pyq, "all_records": len(existing)})
        verify_existing(rows, existing)
        reasoning_record_count = check_reasoning_duplicates(db, chapter.id, rows)
        print("CROSS_CHAPTER_REASONING_RECORDS_SCANNED", reasoning_record_count)
        if (active_normal, active_pyq, len(existing)) not in {(0, 0, 0), (30, 0, 30)}:
            raise SystemExit("Baseline must be the verified empty Venn chapter or exact completed 30-question bank")
        payload = json.dumps({"questions": rows}, ensure_ascii=False).encode("utf-8")
        preview = import_questions(db, payload, "application/json", BATCH.name, True)
        print("DRY_RUN", preview.model_dump())
        if preview.aborted or preview.errors or preview.rejected or preview.duplicates != len(existing) or preview.would_import != 30 - len(existing):
            raise SystemExit("Importer dry-run did not match the expected inserts/duplicates")
        if not args.apply:
            print("NO_DATABASE_CHANGES")
            return
        if active_normal == 30:
            print("IDEMPOTENT_REPLAY: zero additional inserts")
            return
        if active_normal or active_pyq or len(existing) or preview.duplicates or preview.would_import != 30:
            raise SystemExit("Apply requires the exact verified empty Venn baseline and 30 clean inserts")
        result = import_questions(db, payload, "application/json", BATCH.name, False)
        print("IMPORT", result.model_dump())
        if result.aborted or result.errors or result.rejected or result.imported != 30 or result.duplicates:
            raise SystemExit("Actual importer results differed from the expected 30 inserts")
        after = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        normal = [q for q in after if q.is_active and not q.is_pyq]
        pyq = [q for q in after if q.is_active and q.is_pyq]
        counts = Counter(q.difficulty.value for q in normal)
        if len(normal) != 30 or pyq or len(after) != 30 or counts != EXPECTED_COUNTS:
            raise SystemExit(f"Post-import counts mismatch: active normal={len(normal)} pyq={len(pyq)} difficulty={dict(counts)}")
        verify_existing(rows, after)
        replay = import_questions(db, payload, "application/json", BATCH.name, True)
        print("REPLAY_DRY_RUN", replay.model_dump())
        if replay.aborted or replay.errors or replay.rejected or replay.would_import or replay.duplicates != 30:
            raise SystemExit("Post-import replay was not idempotent")
        print("AFTER", {"active_normal": len(normal), "active_pyq": 0, "all_records": len(after), "difficulty": dict(counts)})
        print("POST_IMPORT_VERIFIED")


if __name__ == "__main__":
    main()
