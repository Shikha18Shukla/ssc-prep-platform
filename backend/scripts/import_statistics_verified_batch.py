"""Validate, preview and idempotently import the reviewed Statistics bank."""
import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
from sqlalchemy import select
from app.database.session import SessionLocal, engine
from app.models import Chapter, Exam, Question, Subject, Subcategory
from app.services.question_import_service import import_questions

BATCH = BASE / "data" / "statistics_verified_batch.json"
LEDGER = BASE / "data" / "statistics_answer_ledger.json"
LEVELS = ("EASY", "MEDIUM", "HARD")
TARGET = {level: 30 for level in LEVELS}
ORIGINAL = "Original SSC-style practice question"


def normalized(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def number_masked(value):
    value = normalized(value)
    value = re.sub(r"\d[\d,]*(?:\.\d+)?%?", " <number> ", value)
    return " ".join(re.sub(r"[^a-z<> ]", " ", value).split())


def check_stems(stems, existing=()):
    prior_stems = []
    for stem in stems:
        for prior in prior_stems:
            if normalized(stem) == normalized(prior):
                raise ValueError(f"Exact duplicate: {stem!r}")
            if SequenceMatcher(None, normalized(stem), normalized(prior)).ratio() >= .97:
                raise ValueError(f"Near-identical wording: {stem!r} / {prior!r}")
        prior_stems.append(stem)
    for stem in stems:
        for prior in existing:
            if normalized(stem) == normalized(prior):
                continue
            if SequenceMatcher(None, normalized(stem), normalized(prior)).ratio() >= .97:
                raise ValueError(f"Near-identical duplicate against existing: {stem!r}")


def load_batch():
    payload = json.loads(BATCH.read_text(encoding="utf-8"))
    rows = payload.get("questions") if isinstance(payload, dict) else None
    if not isinstance(rows, list) or len(rows) != 90:
        raise ValueError("Statistics batch must contain exactly 90 questions")
    if Counter(row.get("difficulty") for row in rows if isinstance(row, dict)) != TARGET:
        raise ValueError("Statistics batch must contain 30 questions per difficulty")
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    if len(ledger) != 90:
        raise ValueError("Statistics answer ledger must contain 90 entries")
    required = {"subject_slug", "subcategory_slug", "chapter_slug", "question_text", "options", "correct_option", "explanation", "difficulty", "is_pyq", "source"}
    for index, (row, audit) in enumerate(zip(rows, ledger), start=1):
        if not isinstance(row, dict) or required - set(row):
            raise ValueError(f"Row {index} is missing required fields")
        if (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) != ("maths", "advanced-maths", "statistics"):
            raise ValueError(f"Row {index} catalog mismatch")
        if row["difficulty"] not in LEVELS or row["is_pyq"] is not False or row.get("pyq_year") is not None or row.get("pyq_exam_name") is not None:
            raise ValueError(f"Row {index} difficulty/PYQ metadata is invalid")
        source = row["source"]
        if source != ORIGINAL:
            raise ValueError(f"Row {index} provenance is invalid: {source!r}")
        options = row["options"]
        if not isinstance(options, dict) or set(options) != set("ABCD") or len({normalized(v) for v in options.values()}) != 4:
            raise ValueError(f"Row {index} must have four distinct A-D options")
        if row["correct_option"] not in options or not row["question_text"].strip() or not row["explanation"].strip():
            raise ValueError(f"Row {index} has an invalid stem/key/explanation")
        if sum(normalized(value) == normalized(options[row["correct_option"]]) for value in options.values()) != 1:
            raise ValueError(f"Row {index} does not have exactly one correct option")
        if (audit["row"] != index or audit["question"] != row["question_text"]
                or audit["difficulty"] != row["difficulty"] or not audit["independent_calculation"].strip()):
            raise ValueError(f"Row {index} does not align with its answer-ledger entry")
        if options[row["correct_option"]] != audit["expected_answer"]:
            raise ValueError(f"Row {index} answer key conflicts with ledger")
    check_stems([row["question_text"] for row in rows])
    return rows


def chapter_context(db):
    return db.execute(
        select(Exam, Subject, Subcategory, Chapter)
        .join(Subject, Subject.exam_id == Exam.id)
        .join(Subcategory, Subcategory.subject_id == Subject.id)
        .join(Chapter, Chapter.subcategory_id == Subcategory.id)
        .where(
            Exam.slug == "ssc", Exam.is_active.is_(True), Subject.slug == "maths",
            Subject.is_active.is_(True), Subcategory.slug == "advanced-maths",
            Subcategory.is_active.is_(True), Chapter.slug == "statistics",
            Chapter.is_active.is_(True),
        )
    ).one_or_none()


def counts(rows):
    result = Counter()
    for question in rows:
        state = "active" if question.is_active else "inactive"
        kind = "PYQ" if question.is_pyq else "ordinary"
        result[(question.difficulty.value, state, kind)] += 1
    return result


def plan_missing(records, existing):
    by_stem = {normalized(row["question_text"]): row for row in records}
    known, active = {}, Counter()
    for question in existing:
        key = normalized(question.question_text)
        if key in known:
            raise ValueError(f"Existing Statistics exact duplicate: {question.question_text!r}")
        known[key] = question
        expected = by_stem.get(key)
        if expected:
            actual = {option.option_key: option.option_text for option in question.options}
            correct = [option.option_key for option in question.options if option.is_correct]
            if actual != expected["options"] or correct != [expected["correct_option"]] or question.difficulty.value != expected["difficulty"] or question.is_pyq or not question.is_active:
                raise ValueError(f"Existing exact match conflicts with batch: {question.question_text!r}")
        if question.is_active and not question.is_pyq:
            active[question.difficulty.value] += 1
    check_stems([row["question_text"] for row in records], [q.question_text for q in existing if normalized(q.question_text) not in by_stem])
    deficits = {level: 30 - active[level] for level in LEVELS}
    if any(value < 0 for value in deficits.values()):
        raise ValueError(f"Existing active ordinary counts exceed target; preserving rows: {deficits}")
    selected = []
    for row in records:
        level = row["difficulty"]
        if normalized(row["question_text"]) in known or deficits[level] == 0:
            continue
        selected.append(row)
        deficits[level] -= 1
    if any(deficits.values()):
        raise ValueError(f"Batch cannot fill Statistics deficits: {deficits}")
    return selected


def print_counts(label, result):
    print(label)
    for level in LEVELS:
        print(level, {f"{state}_{kind}": result[(level, state, kind)] for state in ("active", "inactive") for kind in ("ordinary", "PYQ")})


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    engine.echo = False
    records = load_batch()
    print("BATCH", len(records), dict(Counter(row["difficulty"] for row in records)))
    print("PROVENANCE", {"supplied_pdf": sum(row["source"] != ORIGINAL for row in records), "original": sum(row["source"] == ORIGINAL for row in records), "pyq": 0})
    with SessionLocal() as db:
        context = chapter_context(db)
        if context is None:
            raise SystemExit("Active SSC -> Maths -> Advanced Maths -> Statistics chapter not found uniquely")
        _, _, subcategory, chapter = context
        existing = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        print("CHAPTER", chapter.id, chapter.name, chapter.slug, "SUBCATEGORY", subcategory.slug)
        print_counts("BEFORE", counts(existing))
        try:
            selected = plan_missing(records, existing)
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc
        print("PLANNED_INSERTS", len(selected), dict(Counter(row["difficulty"] for row in selected)))
        if not selected:
            print("NOOP: active ordinary targets met; zero inserts")
            return
        preview = import_questions(db, json.dumps({"questions": selected}, ensure_ascii=False).encode(), "application/json", BATCH.name, True)
        print("DRY_RUN", preview.model_dump())
        if preview.aborted or preview.errors or preview.would_import != len(selected) or preview.duplicates:
            raise SystemExit("Importer dry run did not approve every planned insert")
        if args.dry_run:
            print("NO_DATABASE_CHANGES")
            return
        result = import_questions(db, json.dumps({"questions": selected}, ensure_ascii=False).encode(), "application/json", BATCH.name, False)
        print("IMPORT", result.model_dump())
        if result.aborted or result.errors or result.imported != len(selected):
            raise SystemExit("Import did not match dry run")
        after = counts(db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all())
        print_counts("AFTER", after)
        if any(after[(level, "active", "ordinary")] != 30 for level in LEVELS):
            raise SystemExit("Post-import Statistics ordinary counts differ from target")
        print("POST_IMPORT_COUNTS_VERIFIED")


if __name__ == "__main__":
    main()
