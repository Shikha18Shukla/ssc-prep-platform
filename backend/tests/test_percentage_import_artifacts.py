"""Reviewable percentage import files use the existing question import schema."""

import csv
from pathlib import Path


IMPORT_DIR = Path(__file__).parents[1] / "data" / "imports" / "percentage"
EXPECTED = {
    "percentage_easy.csv": ("EASY", 12),
    "percentage_medium.csv": ("MEDIUM", 11),
    "percentage_hard.csv": ("HARD", 3),
}
REQUIRED_COLUMNS = {
    "subject_slug",
    "subcategory_slug",
    "chapter_slug",
    "question_text",
    "option_a",
    "option_b",
    "option_c",
    "option_d",
    "correct_option",
    "explanation",
    "difficulty",
    "is_pyq",
    "pyq_year",
    "pyq_exam_name",
    "source",
}


def test_percentage_csvs_match_importer_contract_and_source_mapping():
    for filename, (difficulty, expected_count) in EXPECTED.items():
        with (IMPORT_DIR / filename).open(encoding="utf-8-sig", newline="") as source:
            reader = csv.DictReader(source)
            assert set(reader.fieldnames or ()) == REQUIRED_COLUMNS
            rows = list(reader)

        assert len(rows) == expected_count
        for row in rows:
            assert row["subject_slug"] == "maths"
            assert row["subcategory_slug"] == "arithmetic-maths"
            assert row["chapter_slug"] == "percentage"
            assert row["difficulty"] == difficulty
            assert row["is_pyq"] == "false"
            assert not row["pyq_year"]
            assert not row["pyq_exam_name"]
            assert row["correct_option"] in {"A", "B", "C", "D"}
            assert all(row[f"option_{key.lower()}"] for key in "ABCD")
            assert row["source"].startswith(filename.removeprefix("percentage_").removesuffix(".csv") + " percentage questions.pdf, p. ")
            assert row["explanation"].startswith("Calculated")
