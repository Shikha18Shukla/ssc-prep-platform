"""Dry-run validation of source-verified Science import batches."""

import csv
from pathlib import Path

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database.seed import seed_database
from app.models import Question
from app.services.question_import_service import import_questions


def test_verified_digestive_system_batches_pass_importer_dry_run_without_database_writes(
    db_session: Session,
) -> None:
    assert seed_database(db_session) == []
    batch_dir = (
        Path(__file__).resolve().parents[1]
        / "data/imports/science/by-chapter/digestive-system"
    )

    for filename, expected_records in (
        ("digestive-system_pyq.csv", 7),
        ("digestive-system_ordinary.csv", 5),
    ):
        batch_path = batch_dir / filename
        result = import_questions(
            db_session,
            batch_path.read_bytes(),
            "text/csv",
            batch_path.name,
            dry_run=True,
        )

        assert result.total_records == expected_records
        assert result.would_import == expected_records
        assert result.imported == 0
        assert result.rejected == 0
        assert result.duplicates == 0
        assert result.aborted is False
        assert result.errors == []
        assert db_session.scalar(select(func.count(Question.id))) == 0


def test_verified_animal_kingdom_batch_passes_importer_dry_run_without_database_writes(
    db_session: Session,
) -> None:
    assert seed_database(db_session) == []
    batch_path = (
        Path(__file__).resolve().parents[1]
        / "data/imports/science/by-chapter/animal-kingdom/animal-kingdom_pyq.csv"
    )

    result = import_questions(
        db_session,
        batch_path.read_bytes(),
        "text/csv",
        batch_path.name,
        dry_run=True,
    )

    assert result.total_records == 3
    assert result.would_import == 3
    assert result.imported == 0
    assert result.rejected == 0
    assert result.duplicates == 0
    assert result.aborted is False
    assert result.errors == []
    assert db_session.scalar(select(func.count(Question.id))) == 0


def test_verified_tissues_pyq_and_ordinary_batches_pass_dry_run_without_writes(
    db_session: Session,
) -> None:
    assert seed_database(db_session) == []
    batch_dir = (
        Path(__file__).resolve().parents[1]
        / "data/imports/science/by-chapter/tissues"
    )

    for filename, expected_records in (("tissues_pyq.csv", 2), ("tissues_ordinary.csv", 6)):
        batch_path = batch_dir / filename
        result = import_questions(
            db_session,
            batch_path.read_bytes(),
            "text/csv",
            batch_path.name,
            dry_run=True,
        )

        assert result.total_records == expected_records
        assert result.would_import == expected_records
        assert result.imported == 0
        assert result.rejected == 0
        assert result.duplicates == 0
        assert result.aborted is False
        assert result.errors == []
        assert db_session.scalar(select(func.count(Question.id))) == 0


def test_verified_circulatory_system_batches_pass_dry_run_without_database_writes(
    db_session: Session,
) -> None:
    assert seed_database(db_session) == []
    batch_dir = (
        Path(__file__).resolve().parents[1]
        / "data/imports/science/by-chapter/circulatory-system"
    )

    for filename, expected_records in (
        ("circulatory-system_ordinary.csv", 11),
        ("circulatory-system_pyq.csv", 4),
    ):
        batch_path = batch_dir / filename
        result = import_questions(
            db_session,
            batch_path.read_bytes(),
            "text/csv",
            batch_path.name,
            dry_run=True,
        )

        assert result.total_records == expected_records
        assert result.would_import == expected_records
        assert result.imported == 0
        assert result.rejected == 0
        assert result.duplicates == 0
        assert result.aborted is False
        assert result.errors == []
        assert db_session.scalar(select(func.count(Question.id))) == 0



def test_verified_brain_nervous_batches_pass_dry_run_without_database_writes(
    db_session: Session,
) -> None:
    assert seed_database(db_session) == []
    batch_dir = (
        Path(__file__).resolve().parents[1]
        / "data/imports/science/by-chapter/brain-and-nervous-system"
    )

    for filename, expected_records in (
        ("brain-and-nervous-system_ordinary.csv", 9),
        ("brain-and-nervous-system_pyq.csv", 5),
    ):
        batch_path = batch_dir / filename
        result = import_questions(
            db_session,
            batch_path.read_bytes(),
            "text/csv",
            batch_path.name,
            dry_run=True,
        )

        assert result.total_records == expected_records
        assert result.would_import == expected_records
        assert result.imported == 0
        assert result.rejected == 0
        assert result.duplicates == 0
        assert result.aborted is False
        assert result.errors == []
        assert db_session.scalar(select(func.count(Question.id))) == 0


def test_brain_nervous_review_export_excludes_unverified_and_nonchapter_rows() -> None:
    import csv

    data_dir = Path(__file__).resolve().parents[1] / "data/imports/science"
    review_path = (
        data_dir
        / "review-datasets/brain-and-nervous-system/brain-and-nervous-system_review.csv"
    )
    with review_path.open(encoding="utf-8-sig", newline="") as stream:
        review_rows = list(csv.DictReader(stream))
    eligible = [row for row in review_rows if row["import_eligible"] == "true"]
    assert len(review_rows) == 22
    assert sum(row["review_status"] == "VERIFIED" for row in review_rows) == 14
    assert sum(row["review_status"] == "NEEDS_REVIEW" for row in review_rows) == 6
    assert sum(row["review_status"] == "REJECTED" for row in review_rows) == 1
    assert sum(row["review_status"] == "DUPLICATE" for row in review_rows) == 1
    assert all(row["chapter_slug"] == "brain-and-nervous-system" for row in eligible)
    assert all(row["explanation"].strip() for row in eligible)

    imported_count = 0
    for filename in (
        "brain-and-nervous-system_ordinary.csv",
        "brain-and-nervous-system_pyq.csv",
    ):
        with (data_dir / "by-chapter/brain-and-nervous-system" / filename).open(
            encoding="utf-8-sig", newline=""
        ) as stream:
            imported_count += sum(1 for _ in csv.DictReader(stream))
    assert imported_count == len(eligible) == 14


def test_verified_respiratory_candidate_passes_dry_run_without_database_writes(
    db_session: Session,
) -> None:
    import csv

    assert seed_database(db_session) == []
    data_dir = Path(__file__).resolve().parents[1] / "data/imports/science"
    review_path = data_dir / "review-datasets/respiratory-system/respiratory-system_review.csv"
    with review_path.open(encoding="utf-8-sig", newline="") as stream:
        review_rows = list(csv.DictReader(stream))
    eligible = [row for row in review_rows if row["import_eligible"] == "true"]
    assert len(eligible) == 1
    assert eligible[0]["source_pdf"] == "circulatory system - science.pdf"
    assert eligible[0]["source_page"] == "17"
    assert eligible[0]["chapter_slug"] == "respiratory-system"
    assert eligible[0]["catalog_chapter_id"] == "6afa7d76-1379-4a79-9ff5-1f934331af92"
    assert eligible[0]["proposed_correct_option"] == "C"
    assert eligible[0]["is_pyq"] == "false"
    assert eligible[0]["review_status"] == "VERIFIED"

    batch_path = data_dir / "by-chapter/respiratory-system/respiratory-system_ordinary.csv"
    with batch_path.open(encoding="utf-8-sig", newline="") as stream:
        batch_rows = list(csv.DictReader(stream))
    assert len(batch_rows) == 1
    assert batch_rows[0]["source"] == "circulatory system - science.pdf p. 17"
    assert batch_rows[0]["chapter_slug"] == "respiratory-system"

    result = import_questions(
        db_session,
        batch_path.read_bytes(),
        "text/csv",
        batch_path.name,
        dry_run=True,
    )
    assert result.total_records == 1
    assert result.would_import == 1
    assert result.imported == 0
    assert result.rejected == 0
    assert result.duplicates == 0
    assert result.aborted is False
    assert result.errors == []
    assert db_session.scalar(select(func.count(Question.id))) == 0


def test_verified_carbon_candidate_passes_dry_run_and_saponification_stays_excluded(
    db_session: Session,
) -> None:
    import csv

    assert seed_database(db_session) == []
    data_dir = Path(__file__).resolve().parents[1] / "data/imports/science"
    review_path = (
        data_dir
        / "review-datasets/carbon-and-its-compound/carbon-and-its-compound_review.csv"
    )
    with review_path.open(encoding="utf-8-sig", newline="") as stream:
        review_rows = list(csv.DictReader(stream))
    eligible = [row for row in review_rows if row["import_eligible"] == "true"]
    assert len(eligible) == 1
    assert eligible[0]["source_pdf"] == "excretory system - science.pdf"
    assert eligible[0]["source_page"] == "6"
    assert eligible[0]["chapter_slug"] == "carbon-and-its-compound"
    assert eligible[0]["catalog_chapter_id"] == "7699583e-02b8-4cb9-8b47-72708bd426be"
    assert eligible[0]["proposed_correct_option"] == "B"
    assert eligible[0]["review_status"] == "VERIFIED"
    pending = [row for row in review_rows if row["source_page"] == "8"]
    assert len(pending) == 1
    assert pending[0]["review_status"] == "NEEDS_REVIEW"
    assert pending[0]["import_eligible"] == "false"

    batch_path = (
        data_dir
        / "by-chapter/carbon-and-its-compound/carbon-and-its-compound_ordinary.csv"
    )
    with batch_path.open(encoding="utf-8-sig", newline="") as stream:
        batch_rows = list(csv.DictReader(stream))
    assert len(batch_rows) == 1
    assert batch_rows[0]["source"] == "excretory system - science.pdf p. 6"
    assert batch_rows[0]["correct_option"] == "B"

    result = import_questions(
        db_session,
        batch_path.read_bytes(),
        "text/csv",
        batch_path.name,
        dry_run=True,
    )
    assert result.total_records == 1
    assert result.would_import == 1
    assert result.imported == 0
    assert result.rejected == 0
    assert result.duplicates == 0
    assert result.aborted is False
    assert result.errors == []
    assert db_session.scalar(select(func.count(Question.id))) == 0


def test_verified_excretory_batches_pass_dry_run_without_database_writes(
    db_session: Session,
) -> None:
    assert seed_database(db_session) == []
    batch_dir = (
        Path(__file__).resolve().parents[1]
        / "data/imports/science/by-chapter/excretory-system"
    )
    for filename, expected_records in (
        ("excretory-system_ordinary.csv", 8),
        ("excretory-system_pyq.csv", 2),
    ):
        batch_path = batch_dir / filename
        result = import_questions(
            db_session,
            batch_path.read_bytes(),
            "text/csv",
            batch_path.name,
            dry_run=True,
        )
        assert result.total_records == expected_records
        assert result.would_import == expected_records
        assert result.imported == 0
        assert result.rejected == 0
        assert result.duplicates == 0
        assert result.aborted is False
        assert result.errors == []
        assert db_session.scalar(select(func.count(Question.id))) == 0


def test_excretory_review_batch_keeps_unverified_rows_out_of_import_files() -> None:
    import csv

    data_dir = Path(__file__).resolve().parents[1] / "data/imports/science"
    review_path = (
        data_dir / "review-datasets/excretory-system/excretory-system_review.csv"
    )
    with review_path.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 20
    assert sum(row["review_status"] == "VERIFIED" for row in rows) == 10
    assert sum(row["review_status"] == "NEEDS_REVIEW" for row in rows) == 7
    assert sum(row["review_status"] == "REJECTED" for row in rows) == 0
    assert sum(row["review_status"] == "DUPLICATE" for row in rows) == 3
    assert all(row["chapter_slug"] == "excretory-system" for row in rows)
    eligible = [row for row in rows if row["import_eligible"] == "true"]
    assert len(eligible) == 10
    assert all(row["review_status"] == "VERIFIED" for row in eligible)
    assert all(row["explanation"].strip() for row in eligible)
    assert any(
        row["source_page"] == "18" and row["review_status"] == "NEEDS_REVIEW"
        for row in rows
    )

    imported = 0
    for filename in ("excretory-system_ordinary.csv", "excretory-system_pyq.csv"):
        with (data_dir / "by-chapter/excretory-system" / filename).open(
            encoding="utf-8-sig", newline=""
        ) as stream:
            imported += sum(1 for _ in csv.DictReader(stream))
    assert imported == len(eligible)


def test_verified_disease_batches_pass_dry_run_without_database_writes(
    db_session: Session,
) -> None:
    assert seed_database(db_session) == []
    batch_dir = (
        Path(__file__).resolve().parents[1]
        / "data/imports/science/by-chapter/disease"
    )
    for filename, expected_records in (
        ("disease_ordinary.csv", 10),
        ("disease_pyq.csv", 1),
    ):
        batch_path = batch_dir / filename
        result = import_questions(
            db_session,
            batch_path.read_bytes(),
            "text/csv",
            batch_path.name,
            dry_run=True,
        )
        assert result.total_records == expected_records
        assert result.would_import == expected_records
        assert result.imported == 0
        assert result.rejected == 0
        assert result.duplicates == 0
        assert result.aborted is False
        assert result.errors == []
    assert db_session.scalar(select(func.count(Question.id))) == 0


def test_glands_review_keeps_clipped_source_pages_out_of_import_and_dry_runs_verified_rows(
    db_session: Session,
) -> None:
    import csv

    assert seed_database(db_session) == []
    data_dir = Path(__file__).resolve().parents[1] / "data/imports/science"
    review_path = data_dir / "review-datasets/glands/glands_review.csv"
    with review_path.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))

    assert len(rows) == 15
    assert sum(row["review_status"] == "VERIFIED" for row in rows) == 2
    assert sum(row["review_status"] == "NEEDS_REVIEW" for row in rows) == 13
    assert sum(row["review_status"] == "REJECTED" for row in rows) == 0
    assert sum(row["review_status"] == "DUPLICATE" for row in rows) == 0
    assert all(row["chapter_slug"] == "glands" for row in rows)
    assert all(
        row["catalog_chapter_id"] == "3a7d5736-5a65-434b-8c2c-0f17905bab57"
        for row in rows
    )
    assert all(
        row["import_eligible"] == "false"
        for row in rows
        if row["review_status"] == "NEEDS_REVIEW"
    )
    assert [(row["source_pdf"], row["source_page"]) for row in rows if row["import_eligible"] == "true"] == [
        ("Disease.pdf", "8"),
        ("Disease.pdf", "13"),
    ]

    batch_dir = data_dir / "by-chapter/glands"
    for filename, expected_records in (
        ("glands_ordinary.csv", 1),
        ("glands_pyq.csv", 1),
    ):
        batch_path = batch_dir / filename
        result = import_questions(
            db_session,
            batch_path.read_bytes(),
            "text/csv",
            batch_path.name,
            dry_run=True,
        )
        assert result.total_records == expected_records
        assert result.would_import == expected_records
        assert result.imported == 0
        assert result.rejected == 0
        assert result.duplicates == 0
        assert result.aborted is False
        assert result.errors == []
        assert db_session.scalar(select(func.count(Question.id))) == 0


def test_six_prepared_chapter_import_files_match_their_verified_review_rows() -> None:
    import csv
    import re
    from collections import Counter

    data_dir = Path(__file__).resolve().parents[1] / "data/imports/science"

    def source_key(row: dict[str, str], *, importer_row: bool) -> tuple[str, str]:
        source = row.get("source", "")
        if source:
            match = re.match(r"^(.*?)(?:, PDF page | p\. )(\d+)$", source)
            if match:
                return match.group(1), match.group(2)
            return source, ""
        return row.get("source_pdf", ""), row.get("source_page", "")

    for slug in (
        "animal-kingdom",
        "tissues",
        "digestive-system",
        "circulatory-system",
        "brain-and-nervous-system",
        "excretory-system",
    ):
        review_path = next(
            (data_dir / "review-datasets" / slug).glob("*_review.csv")
        )
        with review_path.open(encoding="utf-8-sig", newline="") as stream:
            review_rows = list(csv.DictReader(stream))
        eligible = [
            row
            for row in review_rows
            if (
                row.get("import_eligible", "").casefold() == "true"
                if "import_eligible" in row
                else row["review_status"] == "VERIFIED"
            )
        ]
        expected = Counter(
            (
                row["subject_slug"],
                row["subcategory_slug"],
                row["chapter_slug"],
                row["question_text"],
                row["option_a"],
                row["option_b"],
                row["option_c"],
                row["option_d"],
                row.get("proposed_correct_option", row.get("correct_option", "")),
                row.get("explanation", ""),
                row.get("difficulty", ""),
                row.get("is_pyq", "").casefold(),
                row.get("pyq_year", "") or "",
                row.get("pyq_exam_name", "") or "",
                source_key(row, importer_row=False),
            )
            for row in eligible
        )
        actual = []
        for batch_path in (data_dir / "by-chapter" / slug).glob("*.csv"):
            with batch_path.open(encoding="utf-8-sig", newline="") as stream:
                actual.extend(csv.DictReader(stream))
        actual_counter = Counter(
            (
                row["subject_slug"],
                row["subcategory_slug"],
                row["chapter_slug"],
                row["question_text"],
                row["option_a"],
                row["option_b"],
                row["option_c"],
                row["option_d"],
                row["correct_option"],
                row.get("explanation", ""),
                row["difficulty"],
                row["is_pyq"].casefold(),
                row.get("pyq_year", "") or "",
                row.get("pyq_exam_name", "") or "",
                source_key(row, importer_row=True),
            )
            for row in actual
        )
        assert actual_counter == expected, slug


def test_source_page_supplement_batches_pass_dry_run_without_database_writes(
    db_session: Session,
) -> None:
    assert seed_database(db_session) == []
    batch_dir = (
        Path(__file__).resolve().parents[1]
        / "data/imports/science/by-chapter/source-page-supplement"
    )
    batch_paths = sorted(batch_dir.rglob("*.csv"))
    assert len(batch_paths) == 15
    row_count = 0
    for batch_path in batch_paths:
        with batch_path.open(encoding="utf-8-sig", newline="") as stream:
            row_count += sum(1 for _ in csv.DictReader(stream))
    assert row_count == 18

    for batch_path in batch_paths:
        result = import_questions(
            db_session,
            batch_path.read_bytes(),
            "text/csv",
            batch_path.name,
            dry_run=True,
        )
        assert result.total_records >= 1
        assert result.would_import == result.total_records
        assert result.imported == 0
        assert result.rejected == 0
        assert result.duplicates == 0
        assert result.aborted is False
        assert result.errors == []
        assert db_session.scalar(select(func.count(Question.id))) == 0


def test_disease_review_export_has_only_verified_nonduplicate_import_rows() -> None:
    import csv

    data_dir = Path(__file__).resolve().parents[1] / "data/imports/science"
    review_path = data_dir / "review-datasets/disease/disease_review.csv"
    with review_path.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 25
    assert sum(row["review_status"] == "VERIFIED" for row in rows) == 11
    assert sum(row["review_status"] == "NEEDS_REVIEW" for row in rows) == 14
    assert sum(row["review_status"] == "REJECTED" for row in rows) == 0
    assert sum(row["review_status"] == "DUPLICATE" for row in rows) == 0
    assert all(row["chapter_slug"] == "disease" for row in rows)
    eligible = [row for row in rows if row["import_eligible"] == "true"]
    assert len(eligible) == 11
    assert all(row["review_status"] == "VERIFIED" for row in eligible)
    assert all(row["explanation"].strip() for row in eligible)

    imported = 0
    for filename in ("disease_ordinary.csv", "disease_pyq.csv"):
        with (data_dir / "by-chapter/disease" / filename).open(
            encoding="utf-8-sig", newline=""
        ) as stream:
            imported += sum(1 for _ in csv.DictReader(stream))
    assert imported == len(eligible)


def test_disease_source_questions_are_routed_by_content_and_prior_decisions_remain() -> None:
    import csv

    data_dir = Path(__file__).resolve().parents[1] / "data/imports/science"
    with (data_dir / "SCIENCE_OCR_REVIEW_QUEUE.csv").open(
        encoding="utf-8-sig", newline=""
    ) as stream:
        queue = list(csv.DictReader(stream))
    disease_source = {
        int(row["source_page"]): row
        for row in queue
        if row["source_pdf"] == "Disease.pdf" and 2 <= int(row["source_page"]) <= 21
    }
    assert set(disease_source) == set(range(2, 22))
    assert {
        page for page, row in disease_source.items() if row["chapter_slug"] == "disease"
    } == {4, 5, 6, 7, 9}
    assert {
        page for page, row in disease_source.items() if row["chapter_slug"] == "glands"
    } == {2, 3, 8, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21}
    assert disease_source[15]["chapter_slug"] == "brain-and-nervous-system"

    with (data_dir / "SCIENCE_REVIEW_DECISIONS.csv").open(
        encoding="utf-8-sig", newline=""
    ) as stream:
        decisions = list(csv.DictReader(stream))
    for page, new_status in (("18", "VERIFIED"), ("20", "NEEDS_REVIEW"), ("21", "VERIFIED")):
        source_rows = [
            row for row in decisions
            if row["source_pdf"] == "nutrition - science.pdf"
            and row["source_page"] == page
            and row["chapter_slug"] == "disease"
        ]
        assert any(row["review_status"] == "REJECTED" for row in source_rows)
        assert any(row["review_status"] == new_status for row in source_rows)


def test_sound_verified_batches_pass_dry_run_and_exclude_unverified_pages(
    db_session: Session,
) -> None:
    import csv

    assert seed_database(db_session) == []
    data_dir = Path(__file__).resolve().parents[1] / "data/imports/science"
    review_path = data_dir / "review-datasets/sound/sound_review.csv"
    with review_path.open(encoding="utf-8-sig", newline="") as stream:
        review_rows = list(csv.DictReader(stream))
    assert len(review_rows) == 11
    eligible = [row for row in review_rows if row["import_eligible"] == "true"]
    assert len(eligible) == 5
    assert {row["source_page"] for row in eligible} == {"4", "9", "10", "11", "12"}
    assert all(row["review_status"] == "VERIFIED" for row in eligible)
    assert all(row["chapter_slug"] == "sound" for row in eligible)
    assert all(row["catalog_chapter_id"] == "d12ea943-a2eb-4ba5-b71b-6b8865b7cb9a" for row in eligible)
    assert all(row["explanation"].strip() for row in eligible)
    assert next(row for row in review_rows if row["source_page"] == "3")["review_status"] == "DUPLICATE"
    assert all(
        next(row for row in review_rows if row["source_page"] == page)["import_eligible"] == "false"
        for page in ("2", "3", "5", "6", "7", "8")
    )

    expected_status = {
        "2": "NEEDS_REVIEW", "3": "DUPLICATE", "4": "VERIFIED",
        "5": "NEEDS_REVIEW", "6": "NEEDS_REVIEW", "7": "NEEDS_REVIEW",
        "8": "NEEDS_REVIEW", "9": "VERIFIED", "10": "VERIFIED",
        "11": "VERIFIED", "12": "VERIFIED",
    }
    with (data_dir / "SCIENCE_OCR_REVIEW_QUEUE.csv").open(
        encoding="utf-8-sig", newline=""
    ) as stream:
        queue = list(csv.DictReader(stream))
    assert {
        row["source_page"]: row["review_status"] for row in queue
        if row["source_pdf"] == "optics and human eye.pdf"
    } == expected_status
    with (data_dir / "SCIENCE_REVIEW_DECISIONS.csv").open(
        encoding="utf-8-sig", newline=""
    ) as stream:
        decisions = list(csv.DictReader(stream))
    last_decision = {}
    for row in decisions:
        if row["source_pdf"] == "optics and human eye.pdf":
            last_decision[row["source_page"]] = row["review_status"]
    assert last_decision == expected_status

    imported = []
    for filename, expected in (("sound_ordinary.csv", 2), ("sound_pyq.csv", 3)):
        batch_path = data_dir / "by-chapter/sound" / filename
        with batch_path.open(encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.DictReader(stream))
        assert len(rows) == expected
        imported.extend(rows)
        result = import_questions(
            db_session,
            batch_path.read_bytes(),
            "text/csv",
            batch_path.name,
            dry_run=True,
        )
        assert result.total_records == expected
        assert result.would_import == expected
        assert result.imported == 0
        assert result.rejected == 0
        assert result.duplicates == 0
        assert result.aborted is False
        assert result.errors == []
        assert db_session.scalar(select(func.count(Question.id))) == 0

    assert {row["source"].rsplit(" ", 1)[-1] for row in imported} == {"4", "9", "10", "11", "12"}


def test_acid_base_salt_candidates_reconcile_and_pass_dry_run_without_writes(
    db_session: Session,
) -> None:
    import csv

    assert seed_database(db_session) == []
    data_dir = Path(__file__).resolve().parents[1] / "data/imports/science"
    review_path = data_dir / "review-datasets/acid-base-and-salt/acid-base-and-salt_review.csv"
    with review_path.open(encoding="utf-8-sig", newline="") as stream:
        review_rows = list(csv.DictReader(stream))
    eligible = [row for row in review_rows if row["import_eligible"] == "true"]
    assert len(eligible) == 2
    assert {row["source_page"] for row in eligible} == {"10", "15"}
    assert all(row["review_status"] == "VERIFIED" for row in eligible)
    assert all(row["chapter_slug"] == "acid-base-and-salt" for row in eligible)
    assert all(row["catalog_chapter_id"] == "8ce267a1-1920-4aff-a043-48fa730e76af" for row in eligible)
    assert all(row["explanation"].strip() for row in eligible)

    batch_path = data_dir / "by-chapter/acid-base-and-salt/acid_base_salt_ordinary.csv"
    with batch_path.open(encoding="utf-8-sig", newline="") as stream:
        batch_rows = list(csv.DictReader(stream))
    assert len(batch_rows) == len(eligible)
    assert {row["source"] for row in batch_rows} == {
        "chemical reactions.pdf p. 10",
        "matter and atoms.pdf p. 15",
    }

    result = import_questions(
        db_session,
        batch_path.read_bytes(),
        "text/csv",
        batch_path.name,
        dry_run=True,
    )
    assert result.total_records == 2
    assert result.would_import == 2
    assert result.imported == 0
    assert result.rejected == 0
    assert result.duplicates == 0
    assert result.aborted is False
    assert result.errors == []
    assert db_session.scalar(select(func.count(Question.id))) == 0
