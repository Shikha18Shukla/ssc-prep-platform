"""Validate and idempotently import the curated Simple Interest batch."""
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

BATCH = BASE / "data" / "simple_interest_verified_batch.json"
TARGET = 30
LEVELS = ("EASY", "MEDIUM", "HARD")


def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def number_masked(text: str) -> str:
    value = unicodedata.normalize("NFKC", text).casefold()
    value = re.sub(r"\d[\d,]*(?:\.\d+)?%?", " <number> ", value)
    value = re.sub(r"[^a-z<> ]", " ", value)
    return " ".join(value.split())


def chapter_context(db):
    return db.execute(
        select(Exam, Subject, Subcategory, Chapter)
        .join(Subject, Subject.exam_id == Exam.id)
        .join(Subcategory, Subcategory.subject_id == Subject.id)
        .join(Chapter, Chapter.subcategory_id == Subcategory.id)
        .where(
            Exam.slug == "ssc", Exam.is_active.is_(True),
            Subject.slug == "maths", Subject.is_active.is_(True),
            Subcategory.slug == "arithmetic-maths", Subcategory.is_active.is_(True),
            Chapter.slug == "simple-interest", Chapter.is_active.is_(True),
        )
    ).one_or_none()


def counts(rows):
    result = Counter()
    for question in rows:
        if question.is_active:
            result[(question.difficulty.value, "PYQ" if question.is_pyq else "ordinary", "active")] += 1
        else:
            result[(question.difficulty.value, "PYQ" if question.is_pyq else "ordinary", "inactive")] += 1
    return result


def check_batch(records, existing):
    errors = []
    stems = [record["question_text"] for record in records]
    existing_by_stem = {normalized(question.question_text): question for question in existing}
    for i, record in enumerate(records):
        opts = record.get("options", {})
        if set(opts) != {"A", "B", "C", "D"}:
            errors.append(f"row {i + 1}: expected exactly options A-D")
        elif len({normalized(value) for value in opts.values()}) != 4:
            errors.append(f"row {i + 1}: options are not distinct")
        elif record.get("correct_option") not in opts:
            errors.append(f"row {i + 1}: answer key does not identify one option")
        if record.get("is_pyq") is not False:
            errors.append(f"row {i + 1}: ordinary batch has PYQ metadata")
        if record.get("difficulty") not in LEVELS:
            errors.append(f"row {i + 1}: invalid difficulty")
        source = record.get("source", "")
        if not record.get("explanation") or not (
            "Original SSC-style practice question" in source
            or "Source-derived practice question" in source
        ):
            errors.append(f"row {i + 1}: missing explanation or provenance")
        prior = existing_by_stem.get(normalized(record["question_text"]))
        if prior is not None:
            prior_options = {option.option_key: option.option_text for option in prior.options}
            prior_answer = next((option.option_key for option in prior.options if option.is_correct), None)
            if prior_options != opts or prior_answer != record.get("correct_option"):
                errors.append(f"row {i + 1}: existing exact-match record has different options or answer key")
            if prior.difficulty.value != record.get("difficulty") or prior.is_pyq is not record.get("is_pyq"):
                errors.append(f"row {i + 1}: existing exact-match record has different type or difficulty")

    exact = Counter(normalized(stem) for stem in stems)
    for stem, count in exact.items():
        if count > 1:
            errors.append(f"exact duplicate in batch: {stem}")

    # Compare wording and number-masked templates within this batch and against
    # every existing chapter question, including inactive questions.
    existing_stems = [q.question_text for q in existing]
    combined = [("batch", i, stem) for i, stem in enumerate(stems)] + [
        ("database", i, stem) for i, stem in enumerate(existing_stems)
    ]
    for i, (source_a, index_a, stem_a) in enumerate(combined):
        for source_b, index_b, stem_b in combined[:i]:
            if source_a == source_b == "database":
                continue
            a, b = normalized(stem_a), normalized(stem_b)
            if a == b:
                if source_a == source_b:
                    errors.append(f"exact duplicate: batch row {index_a + 1} and {source_b} row {index_b + 1}")
                # Exact existing records are retained as idempotent matches.
                continue
            if SequenceMatcher(None, a, b).ratio() >= 0.92:
                errors.append(f"near-duplicate wording: batch row {index_a + 1} vs {source_b} row {index_b + 1}")
            elif SequenceMatcher(None, number_masked(stem_a), number_masked(stem_b)).ratio() >= 0.92:
                errors.append(f"same-template/number-only variant: batch row {index_a + 1} vs {source_b} row {index_b + 1}")
    return errors


def display_counts(label, counts_by_group):
    print(label)
    for level in LEVELS:
        print(level, {
            "active_ordinary": counts_by_group[(level, "ordinary", "active")],
            "inactive_ordinary": counts_by_group[(level, "ordinary", "inactive")],
            "active_PYQ": counts_by_group[(level, "PYQ", "active")],
            "inactive_PYQ": counts_by_group[(level, "PYQ", "inactive")],
        })


def main():
    engine.echo = False
    payload = json.loads(BATCH.read_text(encoding="utf-8"))
    records = payload["questions"]
    if len(records) != TARGET * len(LEVELS):
        raise SystemExit(f"Expected 90 curated records, found {len(records)}")
    levels = Counter(item["difficulty"] for item in records)
    if any(levels[level] != TARGET for level in LEVELS):
        raise SystemExit(f"Batch difficulty counts are invalid: {dict(levels)}")

    with SessionLocal() as db:
        context = chapter_context(db)
        if context is None:
            raise SystemExit("Active SSC → Maths → Arithmetic Maths → Simple Interest chapter was not found uniquely")
        _, _, _, chapter = context
        existing = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        before = counts(existing)
        print("CHAPTER", chapter.id, chapter.name, chapter.slug)
        display_counts("BEFORE", before)

        errors = check_batch(records, existing)
        if errors:
            raise SystemExit("Curated batch checks failed:\n" + "\n".join(errors[:30]))

        exact_existing = {normalized(q.question_text) for q in existing}
        selected = []
        remaining = {
            level: max(0, TARGET - before[(level, "ordinary", "active")])
            for level in LEVELS
        }
        for level in LEVELS:
            for record in records:
                if record["difficulty"] != level or remaining[level] == 0:
                    continue
                if normalized(record["question_text"]) in exact_existing:
                    continue
                selected.append(record)
                exact_existing.add(normalized(record["question_text"]))
                remaining[level] -= 1
            if remaining[level]:
                raise SystemExit(f"Batch lacks {remaining[level]} nonduplicate {level} questions")

        if not selected:
            print("NOOP: difficulty targets already met; no database changes made")
        else:
            import_payload = json.dumps({"questions": selected}, ensure_ascii=False).encode("utf-8")
            dry = import_questions(db, import_payload, "application/json", BATCH.name, True)
            print("DRY_RUN", dry.model_dump())
            if dry.aborted or dry.errors or dry.would_import != len(selected):
                raise SystemExit("Validated import dry-run did not approve the entire selected deficit")
            committed = import_questions(db, import_payload, "application/json", BATCH.name, False)
            print("IMPORT", committed.model_dump())
            if committed.aborted or committed.errors or committed.imported != len(selected):
                raise SystemExit("Database import did not commit the complete selected batch")

        after_rows = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        after = counts(after_rows)
        display_counts("AFTER", after)
        print("TOTAL_ADDED", sum(after.values()) - sum(before.values()))
        if any(after[(level, "ordinary", "active")] < TARGET for level in LEVELS):
            raise SystemExit("Post-import active ordinary question counts are below target")


if __name__ == "__main__":
    main()
