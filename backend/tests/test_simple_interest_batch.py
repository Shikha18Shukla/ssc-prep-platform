"""Structural quality checks for the reviewed Simple Interest question batch."""
import json
from collections import Counter
from pathlib import Path


def test_simple_interest_batch_has_target_distribution_and_provenance():
    batch_path = Path(__file__).resolve().parents[1] / "data" / "simple_interest_verified_batch.json"
    questions = json.loads(batch_path.read_text(encoding="utf-8"))["questions"]

    assert len(questions) == 90
    assert Counter(question["difficulty"] for question in questions) == {
        "EASY": 30, "MEDIUM": 30, "HARD": 30,
    }
    assert sum("Source-derived practice question" in question["source"] for question in questions) == 1
    assert sum("Original SSC-style practice question" in question["source"] for question in questions) == 89
    assert all(question["is_pyq"] is False for question in questions)


def test_simple_interest_batch_has_four_distinct_options_and_one_answer_key():
    batch_path = Path(__file__).resolve().parents[1] / "data" / "simple_interest_verified_batch.json"
    questions = json.loads(batch_path.read_text(encoding="utf-8"))["questions"]

    for question in questions:
        options = question["options"]
        assert set(options) == {"A", "B", "C", "D"}
        assert len({value.strip().casefold() for value in options.values()}) == 4
        assert question["correct_option"] in options
        assert question["explanation"].strip()
        assert question["chapter_slug"] == "simple-interest"


def test_source_derived_simple_interest_answers_match_calculation():
    batch_path = Path(__file__).resolve().parents[1] / "data" / "simple_interest_verified_batch.json"
    questions = json.loads(batch_path.read_text(encoding="utf-8"))["questions"]
    sourced = [question for question in questions if "Source-derived practice question" in question["source"]]

    by_stem = {question["question_text"]: question for question in sourced}
    first = by_stem["Find the simple interest on Rs 750 at 8% per annum for 2 years."]
    assert first["options"][first["correct_option"]] == "Rs 120"
    assert 750 * 8 * 2 / 100 == 120


def test_hard_principal_comparison_answer_is_independently_calculated():
    batch_path = Path(__file__).resolve().parents[1] / "data" / "simple_interest_verified_batch.json"
    questions = json.loads(batch_path.read_text(encoding="utf-8"))["questions"]
    stem = (
        "A principal is lent at 8% simple interest for 3 years. If Rs 5,000 more had been "
        "invested at 2 percentage points less for the same duration, the interest would be "
        "Rs 180 less. Find the original principal."
    )
    question = next(item for item in questions if item["question_text"] == stem)
    answer = question["options"][question["correct_option"]]

    # 0.24P - 0.18(P + 5,000) = 180.
    assert answer == "Rs 18,000"
    assert 0.24 * 18_000 - 0.18 * (18_000 + 5_000) == 180

