"""Strict, transactional CSV/JSON question bank import service."""

import csv
import io
import json
import unicodedata
from dataclasses import dataclass
from datetime import date

from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import Chapter, Difficulty, Exam, Question, QuestionOption, Subject, Subcategory
from app.schemas.questions import ImportIssue, QuestionImportSummary

MAX_FILE_BYTES = 5 * 1024 * 1024
MAX_RECORDS = 5000
EXPECTED_COLUMNS = {
    "subject_slug", "subcategory_slug", "chapter_slug", "question_text", "option_a",
    "option_b", "option_c", "option_d", "correct_option", "explanation", "difficulty",
    "is_pyq", "pyq_year", "pyq_exam_name", "source",
}
ALLOWED_JSON_COLUMNS = EXPECTED_COLUMNS | {"options"}


@dataclass
class Candidate:
    row: int
    chapter: Chapter
    question_text: str
    explanation: str | None
    difficulty: Difficulty
    is_pyq: bool
    pyq_year: int | None
    pyq_exam_name: str | None
    source: str | None
    options: list[tuple[str, str, bool]]


class ImportFileError(ValueError):
    """The uploaded file cannot be interpreted as a supported import."""


def _text(value) -> str:
    return "" if value is None else str(value).strip()


def _normalized_question(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def _parse_records(data: bytes, content_type: str, filename: str) -> list[tuple[int, dict]]:
    if len(data) > MAX_FILE_BYTES:
        raise ImportFileError("File exceeds the 5 MiB limit")
    if not data:
        raise ImportFileError("File is empty")

    is_json = "json" in content_type.lower() or filename.lower().endswith(".json")
    if is_json:
        try:
            parsed = json.loads(data.decode("utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ImportFileError(f"Invalid UTF-8 JSON: {exc}") from exc
        if isinstance(parsed, dict):
            parsed = parsed.get("questions")
        if not isinstance(parsed, list):
            raise ImportFileError("JSON must be an array of questions or an object with a 'questions' array")
        if not parsed:
            raise ImportFileError("Question file has no records")
        if len(parsed) > MAX_RECORDS:
            raise ImportFileError(f"File exceeds the {MAX_RECORDS} record limit")
        return [(index + 1, row if isinstance(row, dict) else {}) for index, row in enumerate(parsed)]

    try:
        decoded = data.decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(decoded, newline=""), strict=True)
        headers = reader.fieldnames
        if not headers:
            raise ImportFileError("CSV header row is missing")
        headers = [header.strip() if header else "" for header in headers]
        if len(set(headers)) != len(headers):
            raise ImportFileError("CSV contains duplicate column names")
        missing = sorted(EXPECTED_COLUMNS - set(headers))
        if missing:
            raise ImportFileError(f"CSV is missing required columns: {', '.join(missing)}")
        unexpected = sorted(set(headers) - EXPECTED_COLUMNS)
        if unexpected:
            raise ImportFileError(f"CSV contains unsupported columns: {', '.join(unexpected)}")
        reader.fieldnames = headers
        records: list[tuple[int, dict]] = []
        for row_number, record in enumerate(reader, start=2):
            if None in record:
                raise ImportFileError(f"CSV row {row_number} has more values than the header")
            if len(records) >= MAX_RECORDS:
                raise ImportFileError(f"File exceeds the {MAX_RECORDS} record limit")
            records.append((row_number, record))
        if not records:
            raise ImportFileError("Question file has no records")
        return records
    except (UnicodeDecodeError, csv.Error) as exc:
        raise ImportFileError(f"Invalid UTF-8 CSV: {exc}") from exc


def _options_from_record(record: dict) -> dict:
    options = record.get("options")
    if isinstance(options, dict):
        return {f"option_{str(key).lower()}": value for key, value in options.items()}
    if isinstance(options, list):
        result = {}
        for option in options:
            if isinstance(option, dict):
                key = _text(option.get("option_key", option.get("key"))).upper()
                result[f"option_{key.lower()}"] = option.get("option_text", option.get("text"))
        return result
    return record


def _parse_bool(value) -> bool | None:
    text_value = _text(value).casefold()
    if text_value in {"true", "1", "yes", "y"}:
        return True
    if text_value in {"false", "0", "no", "n"}:
        return False
    return None


def _add_issue(issues: list[ImportIssue], row: int, field: str | None, message: str) -> None:
    issues.append(ImportIssue(row=row, field=field, message=message))


def _validate_record(
    db: Session,
    row_number: int,
    raw_record: dict,
    caches: dict,
    issues: list[ImportIssue],
) -> Candidate | None:
    record = dict(raw_record)
    starting_issue_count = len(issues)
    unexpected = sorted(set(record) - ALLOWED_JSON_COLUMNS)
    if unexpected:
        _add_issue(issues, row_number, None, f"Unsupported fields: {', '.join(unexpected)}")
    option_container = record.get("options")
    if isinstance(option_container, dict):
        labels = {str(key).strip().upper() for key in option_container}
        if labels != {"A", "B", "C", "D"}:
            _add_issue(issues, row_number, "options", "Options object must contain exactly A, B, C, and D")
    elif isinstance(option_container, list):
        labels = [
            _text(option.get("option_key", option.get("key"))).upper()
            for option in option_container if isinstance(option, dict)
        ]
        if len(labels) != 4 or set(labels) != {"A", "B", "C", "D"}:
            _add_issue(issues, row_number, "options", "Options array must contain exactly one each of A, B, C, and D")
    elif option_container is not None:
        _add_issue(issues, row_number, "options", "Options must be an object keyed A-D or an array of four labelled options")
    record.update(_options_from_record(record))

    for field in ("question_text", "option_a", "option_b", "option_c", "option_d", "explanation", "pyq_exam_name", "source"):
        if record.get(field) is not None and not isinstance(record[field], str):
            _add_issue(issues, row_number, field, "Value must be text")

    subject_slug = _text(record.get("subject_slug")).casefold()
    category_slug = _text(record.get("subcategory_slug")).casefold() or None
    chapter_slug = _text(record.get("chapter_slug")).casefold()

    subject = caches["subjects"].get(subject_slug)
    if subject_slug not in caches["subjects"]:
        subject = db.execute(
            select(Subject)
            .join(Exam, Exam.id == Subject.exam_id)
            .where(
                Subject.slug == subject_slug,
                Subject.is_active.is_(True),
                Exam.slug == "ssc",
                Exam.is_active.is_(True),
            )
        ).scalar_one_or_none() if subject_slug else None
        caches["subjects"][subject_slug] = subject
    if subject is None:
        _add_issue(issues, row_number, "subject_slug", "Active SSC subject slug was not found")

    category = None
    if subject is not None and category_slug:
        key = (subject.id, category_slug)
        if key not in caches["categories"]:
            caches["categories"][key] = db.execute(
                select(Subcategory).where(
                    Subcategory.subject_id == subject.id,
                    Subcategory.slug == category_slug,
                    Subcategory.is_active.is_(True),
                )
            ).scalar_one_or_none()
        category = caches["categories"][key]
        if category is None:
            _add_issue(issues, row_number, "subcategory_slug", "Active category was not found under this subject")

    chapter = None
    if subject is not None and chapter_slug:
        chapter_key = (subject.id, chapter_slug)
        if chapter_key not in caches["chapters"]:
            caches["chapters"][chapter_key] = db.execute(
                select(Chapter).where(
                    Chapter.subject_id == subject.id,
                    Chapter.slug == chapter_slug,
                    Chapter.is_active.is_(True),
                )
            ).scalar_one_or_none()
        chapter = caches["chapters"][chapter_key]
        if chapter is None:
            _add_issue(issues, row_number, "chapter_slug", "Active chapter was not found under this subject")
        elif chapter.subcategory_id != (category.id if category else None):
            _add_issue(issues, row_number, "subcategory_slug", "Chapter does not belong to the supplied category (or is not a direct subject chapter)")
    elif not chapter_slug:
        _add_issue(issues, row_number, "chapter_slug", "Chapter slug is required")

    question_text = _text(record.get("question_text"))
    if not question_text:
        _add_issue(issues, row_number, "question_text", "Question text is required")

    option_values: list[tuple[str, str, bool]] = []
    correct_label = _text(record.get("correct_option")).upper()
    if correct_label not in {"A", "B", "C", "D"}:
        _add_issue(issues, row_number, "correct_option", "Correct option must be A, B, C, or D")
    for order, label in enumerate("ABCD", start=1):
        option_text = _text(record.get(f"option_{label.lower()}"))
        if not option_text:
            _add_issue(issues, row_number, f"option_{label.lower()}", "All four option texts are required and must be non-empty")
        option_values.append((label, option_text, label == correct_label))

    try:
        difficulty = Difficulty(_text(record.get("difficulty")).upper())
    except ValueError:
        difficulty = None
        _add_issue(issues, row_number, "difficulty", "Difficulty must be EASY, MEDIUM, or HARD")

    is_pyq = _parse_bool(record.get("is_pyq"))
    if is_pyq is None:
        _add_issue(issues, row_number, "is_pyq", "is_pyq must be true or false")

    year_value = _text(record.get("pyq_year"))
    pyq_year = None
    if year_value:
        try:
            pyq_year = int(year_value)
            if not 1950 <= pyq_year <= date.today().year:
                raise ValueError
        except ValueError:
            _add_issue(issues, row_number, "pyq_year", f"PYQ year must be between 1950 and {date.today().year}")
    pyq_exam_name = _text(record.get("pyq_exam_name")) or None
    if is_pyq is True:
        if pyq_year is None:
            _add_issue(issues, row_number, "pyq_year", "PYQs require a valid year")
    elif is_pyq is False and (year_value or pyq_exam_name):
        _add_issue(issues, row_number, "pyq_year", "Non-PYQs must not include PYQ year or exam name")

    source = _text(record.get("source")) or None
    explanation = _text(record.get("explanation")) or None
    if len(source or "") > 255:
        _add_issue(issues, row_number, "source", "Source must be at most 255 characters")
    if len(pyq_exam_name or "") > 100:
        _add_issue(issues, row_number, "pyq_exam_name", "PYQ exam name must be at most 100 characters")

    if len(issues) != starting_issue_count or subject is None or chapter is None or difficulty is None or is_pyq is None:
        return None
    return Candidate(
        row=row_number,
        chapter=chapter,
        question_text=question_text,
        explanation=explanation,
        difficulty=difficulty,
        is_pyq=is_pyq,
        pyq_year=pyq_year,
        pyq_exam_name=pyq_exam_name,
        source=source,
        options=option_values,
    )


def import_questions(
    db: Session,
    data: bytes,
    content_type: str,
    filename: str,
    dry_run: bool,
) -> QuestionImportSummary:
    """Validate every row first; commit the file only if all non-duplicate rows are valid."""
    records = _parse_records(data, content_type, filename)
    issues: list[ImportIssue] = []
    candidates: list[Candidate] = []
    caches = {"subjects": {}, "categories": {}, "chapters": {}}
    for row_number, record in records:
        candidate = _validate_record(db, row_number, record, caches, issues)
        if candidate is not None:
            candidates.append(candidate)

    # Serialize import commits on PostgreSQL so two overlapping imports cannot both
    # pass the duplicate scan for the same question text.
    if not issues and db.bind is not None and db.bind.dialect.name == "postgresql":
        db.execute(text("SELECT pg_advisory_xact_lock(74192831, 1)"))

    chapter_ids = {candidate.chapter.id for candidate in candidates}
    known: dict[object, set[str]] = {chapter_id: set() for chapter_id in chapter_ids}
    if chapter_ids:
        existing = db.execute(
            select(Question.chapter_id, Question.question_text).where(Question.chapter_id.in_(chapter_ids))
        ).all()
        for chapter_id, question_text in existing:
            known[chapter_id].add(_normalized_question(question_text))

    new_candidates: list[Candidate] = []
    duplicate_rows: list[int] = []
    for candidate in candidates:
        normalized = _normalized_question(candidate.question_text)
        if normalized in known[candidate.chapter.id]:
            duplicate_rows.append(candidate.row)
        else:
            known[candidate.chapter.id].add(normalized)
            new_candidates.append(candidate)

    if issues:
        db.rollback()
        return QuestionImportSummary(
            total_records=len(records), imported=0, rejected=len(records) - len(duplicate_rows),
            duplicates=len(duplicate_rows), dry_run=dry_run, would_import=0,
            aborted=True, errors=issues, duplicate_rows=duplicate_rows,
        )

    if dry_run:
        db.rollback()
        return QuestionImportSummary(
            total_records=len(records), imported=0, rejected=0, duplicates=len(duplicate_rows),
            dry_run=True, would_import=len(new_candidates), aborted=False, errors=[], duplicate_rows=duplicate_rows,
        )

    try:
        for candidate in new_candidates:
            question = Question(
                chapter_id=candidate.chapter.id,
                question_text=candidate.question_text,
                explanation=candidate.explanation,
                difficulty=candidate.difficulty,
                is_pyq=candidate.is_pyq,
                pyq_year=candidate.pyq_year,
                pyq_exam_name=candidate.pyq_exam_name,
                source=candidate.source,
                is_active=True,
                options=[
                    QuestionOption(
                        option_key=key,
                        option_text=option_text,
                        is_correct=is_correct,
                        display_order=order,
                    )
                    for order, (key, option_text, is_correct) in enumerate(candidate.options, start=1)
                ],
            )
            db.add(question)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise

    return QuestionImportSummary(
        total_records=len(records), imported=len(new_candidates), rejected=0,
        duplicates=len(duplicate_rows), dry_run=False, would_import=len(new_candidates),
        aborted=False, errors=[], duplicate_rows=duplicate_rows,
    )
