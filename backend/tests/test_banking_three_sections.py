"""Coverage for Banking Clerk/PO 10/15/15 chapter sections."""

from datetime import datetime, timedelta, timezone
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.security import create_access_token
from app.database.banking_catalog import BANKING_SUBJECTS
from app.database.ssc_catalog import slugify
from app.models import (
    Chapter,
    Difficulty,
    Exam,
    Question,
    QuestionOption,
    Subject,
    TestQuestion as QuestionAttemptLink,
    User,
)
from app.schemas.tests import TestCreate as CreateTestPayload
from app.services.test_service import create_test, get_test_availability
from banking_three_sections_common import (
    EXAM_SLUGS,
    SECTION_COUNTS,
    SUBJECT_SLUGS,
    expected_sections,
)

TARGET_CHAPTERS = [
    (name, subject_slug)
    for name, subject_slug, chapters in BANKING_SUBJECTS
    if subject_slug in SUBJECT_SLUGS
    for _ in chapters
]
TARGET_SUBJECT_NAMES = {
    subject_slug: name
    for name, subject_slug, _ in BANKING_SUBJECTS
    if subject_slug in SUBJECT_SLUGS
}


def _stable_uuid(label: str) -> uuid.UUID:
    return uuid.uuid5(uuid.NAMESPACE_URL, f"three-sections-test:{label}")


def _question_options(question_id: uuid.UUID, label: str) -> list[QuestionOption]:
    return [
        QuestionOption(
            id=_stable_uuid(f"option:{question_id}:{key}"),
            question_id=question_id,
            option_key=key,
            option_text=f"Option {key} for {label}",
            display_order=position,
            is_correct=key == "A",
        )
        for position, key in enumerate("ABCD", start=1)
    ]


@pytest.fixture
def banking_three_sections(db_session: Session):
    """Seed all 98 target chapters with the deterministic section layout."""
    user = User(email="three-sections@example.com", password_hash="unused", is_active=True)
    db_session.add(user)
    db_session.flush()

    records: list[dict] = []
    questions_by_section: dict[str, list[uuid.UUID]] = {}
    all_questions: list[Question] = []
    all_options: list[QuestionOption] = []
    base_time = datetime(2026, 1, 1, tzinfo=timezone.utc)

    for exam_slug in EXAM_SLUGS:
        exam = Exam(name=f"Banking {exam_slug}", slug=exam_slug, is_active=True)
        db_session.add(exam)
        db_session.flush()

        for subject_slug in SUBJECT_SLUGS:
            subject = Subject(
                exam_id=exam.id,
                name=TARGET_SUBJECT_NAMES[subject_slug],
                slug=subject_slug,
                is_active=True,
            )
            db_session.add(subject)
            db_session.flush()

            for name, chapter_slug, display_order in _chapter_definitions(subject_slug):
                chapter = Chapter(
                    subject_id=subject.id,
                    name=name,
                    slug=chapter_slug,
                    display_order=display_order,
                    is_active=True,
                )
                db_session.add(chapter)
                db_session.flush()

                section_names = expected_sections(exam_slug, subject_slug, chapter_slug)
                for name in section_names:
                    questions_by_section[name] = []

                for index in range(sum(SECTION_COUNTS)):
                    part = 1 if index < SECTION_COUNTS[0] else 2 if index < SECTION_COUNTS[0] + SECTION_COUNTS[1] else 3
                    section = section_names[part - 1]
                    label = f"{exam_slug}:{subject_slug}:{chapter_slug}:{index}"
                    question_id = _stable_uuid(label)
                    question = Question(
                        id=question_id,
                        chapter_id=chapter.id,
                        question_text=f"Question {index} for {label}",
                        difficulty=Difficulty.EASY,
                        is_pyq=False,
                        is_active=True,
                        section=section,
                        created_at=base_time + timedelta(seconds=len(all_questions)),
                    )
                    all_questions.append(question)
                    questions_by_section[section].append(question_id)
                    all_options.extend(_question_options(question_id, label))

                records.append({
                    "exam": exam,
                    "subject": subject,
                    "chapter": chapter,
                    "sections": section_names,
                })

    db_session.bulk_save_objects(all_questions)
    db_session.bulk_save_objects(all_options)
    db_session.commit()
    return {
        "user": user,
        "records": records,
        "questions_by_section": questions_by_section,
    }


def _chapter_definitions(subject_slug: str) -> list[tuple[str, str, int]]:
    for name, slug, chapters in BANKING_SUBJECTS:
        if slug == subject_slug:
            return [(chapter_name, slugify(chapter_name), order) for order, chapter_name in enumerate(chapters, start=1)]
    raise AssertionError(f"missing canonical subject {subject_slug}")


def test_every_target_chapter_has_three_stable_sections(
    db_session: Session, banking_three_sections
):
    records = banking_three_sections["records"]
    questions_by_section = banking_three_sections["questions_by_section"]
    user = banking_three_sections["user"]

    assert len(records) == len(EXAM_SLUGS) * sum(
        1 for _, subject_slug, chapters in BANKING_SUBJECTS if subject_slug in SUBJECT_SLUGS
        for _ in chapters
    )
    assert len(records) == 98
    assert len(questions_by_section) == len(records) * 3

    assigned_ids = [question_id for ids in questions_by_section.values() for question_id in ids]
    assert len(assigned_ids) == len(records) * sum(SECTION_COUNTS)
    assert len(set(assigned_ids)) == len(assigned_ids)

    section_names_seen: set[str] = set()

    for record in records:
        exam = record["exam"]
        subject = record["subject"]
        chapter = record["chapter"]
        section_names = record["sections"]

        assert len(set(section_names)) == 3
        assert section_names_seen.isdisjoint(section_names)
        section_names_seen.update(section_names)

        for part, (section, count) in enumerate(zip(section_names, SECTION_COUNTS), start=1):
            expected_ids = questions_by_section[section]
            assert len(expected_ids) == count

            availability = get_test_availability(
                db_session,
                exam.id,
                subject.id,
                "CHAPTER_WISE",
                chapter.id,
                None,
                None,
                count,
                None,
                section,
            )
            assert availability["available_question_count"] == count
            assert count in availability["allowed_question_counts"]
            assert availability["can_satisfy_request"] is True

            attempt = create_test(db_session, user.id, CreateTestPayload(
                exam_id=exam.id,
                subject_id=subject.id,
                subcategory_id=None,
                test_type="CHAPTER_WISE",
                chapter_id=chapter.id,
                chapter_ids=None,
                difficulty=None,
                question_count=count,
                section_filter=section,
            ))
            assert attempt.question_count == count
            assert attempt.duration_seconds == count * 42
            assert attempt.chapter_id == chapter.id

            rows = db_session.execute(
                select(QuestionAttemptLink)
                .where(QuestionAttemptLink.test_attempt_id == attempt.id)
                .order_by(QuestionAttemptLink.question_order)
            ).scalars().all()
            assert [row.question_id for row in rows] == expected_ids
            assert len({row.question_id for row in rows}) == count

    assert len(section_names_seen) == 294


def test_active_test_endpoint_reports_single_section(client: TestClient, db_session: Session):
    user = User(email="api-three-sections@example.com", password_hash="unused", is_active=True)
    exam = Exam(name="Banking Clerk", slug="banking-clerk", is_active=True)
    db_session.add_all([user, exam])
    db_session.flush()
    subject = Subject(exam_id=exam.id, name="English", slug="english", is_active=True)
    db_session.add(subject)
    db_session.flush()
    chapter = Chapter(subject_id=subject.id, name="Noun", slug="noun", is_active=True)
    db_session.add(chapter)
    db_session.flush()

    section = expected_sections("banking-clerk", "english", "noun")[0]
    questions: list[Question] = []
    options: list[QuestionOption] = []
    for index in range(10):
        question_id = _stable_uuid(f"api:{section}:{index}")
        question = Question(
            id=question_id,
            chapter_id=chapter.id,
            question_text=f"API section question {index}",
            difficulty=Difficulty.EASY,
            is_pyq=False,
            is_active=True,
            section=section,
            created_at=datetime(2026, 2, 1, tzinfo=timezone.utc) + timedelta(seconds=index),
        )
        questions.append(question)
        options.extend(_question_options(question_id, f"api:{index}"))
    db_session.bulk_save_objects(questions)
    db_session.bulk_save_objects(options)
    db_session.commit()

    response = client.post(
        "/api/tests",
        json={
            "exam_id": str(exam.id),
            "subject_id": str(subject.id),
            "chapter_id": str(chapter.id),
            "test_type": "CHAPTER_WISE",
            "question_count": 10,
            "section_filter": section,
        },
        headers={"Authorization": f"Bearer {create_access_token(user.id)}"},
    )
    assert response.status_code == 201, response.text
    body = response.json()
    assert body["section"] == section
    assert body["question_count"] == 10
    assert body["duration_seconds"] == 420
    assert len(body["questions"]) == 10


def test_malformed_three_section_question_is_not_eligible(db_session: Session):
    user = User(email="malformed-sections@example.com", password_hash="unused", is_active=True)
    exam = Exam(name="Banking Clerk", slug="banking-clerk", is_active=True)
    db_session.add_all([user, exam])
    db_session.flush()
    subject = Subject(exam_id=exam.id, name="English", slug="english", is_active=True)
    db_session.add(subject)
    db_session.flush()
    chapter = Chapter(subject_id=subject.id, name="Noun", slug="noun", is_active=True)
    db_session.add(chapter)
    db_session.flush()

    section = expected_sections("banking-clerk", "english", "noun")[0]
    questions: list[Question] = []
    options: list[QuestionOption] = []
    valid_ids: list[uuid.UUID] = []
    base_time = datetime(2026, 3, 1, tzinfo=timezone.utc)

    for index in range(11):
        question_id = _stable_uuid(f"malformed:{section}:{index}")
        question = Question(
            id=question_id,
            chapter_id=chapter.id,
            question_text=f"Section question {index}",
            difficulty=Difficulty.EASY,
            is_pyq=False,
            is_active=True,
            section=section,
            created_at=base_time + timedelta(seconds=index),
        )
        questions.append(question)
        if index < 10:
            valid_ids.append(question_id)
            options.extend(_question_options(question_id, f"valid:{index}"))
        else:
            options.extend(
                QuestionOption(
                    id=_stable_uuid(f"malformed-option:{question_id}:{key}"),
                    question_id=question_id,
                    option_key=key,
                    option_text=f"Option {key}",
                    display_order=position,
                    is_correct=True,
                )
                for position, key in enumerate("ABCD", start=1)
            )

    db_session.bulk_save_objects(questions)
    db_session.bulk_save_objects(options)
    db_session.commit()

    availability = get_test_availability(
        db_session,
        exam.id,
        subject.id,
        "CHAPTER_WISE",
        chapter.id,
        None,
        None,
        10,
        None,
        section,
    )
    assert availability["available_question_count"] == 10
    assert availability["can_satisfy_request"] is True

    attempt = create_test(db_session, user.id, CreateTestPayload(
        exam_id=exam.id,
        subject_id=subject.id,
        subcategory_id=None,
        test_type="CHAPTER_WISE",
        chapter_id=chapter.id,
        chapter_ids=None,
        difficulty=None,
        question_count=10,
        section_filter=section,
    ))
    rows = db_session.execute(
        select(QuestionAttemptLink)
        .where(QuestionAttemptLink.test_attempt_id == attempt.id)
        .order_by(QuestionAttemptLink.question_order)
    ).scalars().all()
    assert [row.question_id for row in rows] == valid_ids
