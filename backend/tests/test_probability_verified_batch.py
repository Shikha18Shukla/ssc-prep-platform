"""Independent outcome-count, option, provenance, and duplicate checks."""
import json
import re
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from fractions import Fraction
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "probability_verified_batch.json"
LEDGER = BASE / "data" / "probability_answer_ledger.json"


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def masked(value):
    value = norm(value)
    value = re.sub(r"\d[\d,]*(?:\.\d+)?%?", " <n> ", value)
    return " ".join(re.sub(r"[^a-z<> ]", " ", value).split())


def test_every_answer_is_supported_by_outcome_count_ledger():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    assert len(rows) == len(ledger) == 90
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert sum(row["source"].startswith("Probability ") for row in rows) == 8
    assert sum(row["source"] == "Original SSC-style practice question" for row in rows) == 82
    for index, (row, audit) in enumerate(zip(rows, ledger), 1):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == (
            "maths", "advanced-maths", "probability")
        assert row["is_pyq"] is False
        assert row.get("pyq_year") is None and row.get("pyq_exam_name") is None
        assert row["question_text"].strip() and row["explanation"].strip()
        assert set(row["options"]) == set("ABCD")
        assert len({norm(value) for value in row["options"].values()}) == 4
        expected = Fraction(audit["favourable_outcomes"], audit["total_equally_likely_outcomes"])
        assert 0 <= expected <= 1
        assert fmt(expected) == audit["expected_answer"]
        assert row["options"][row["correct_option"]] == audit["expected_answer"]
        assert row["question_text"] == audit["question"]
        assert row["difficulty"] == audit["difficulty"]


def fmt(value):
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def test_batch_has_no_exact_number_masked_or_lexical_duplicates():
    stems = [row["question_text"] for row in json.loads(BATCH.read_text(encoding="utf-8"))["questions"]]
    assert len({norm(stem) for stem in stems}) == 90
    for index, stem in enumerate(stems):
        for prior in stems[:index]:
            assert masked(stem) != masked(prior), f"number-masked duplicate: {stem!r} / {prior!r}"
            assert SequenceMatcher(None, norm(stem), norm(prior)).ratio() < .92, f"near duplicate: {stem!r} / {prior!r}"


def test_pdf_source_answers_rechecked_against_visible_slide_calculations():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    source_answers = {
        "Two fair coins are tossed together. What is the probability of getting at most one head?": "3/4",
        "A coin is tossed three times. What is the probability that heads and tails alternate on every toss?": "1/4",
        "A die is rolled twice and the sum is known to be 10. Given this, what is the probability that at least one roll is 5?": "1/3",
        "Two fair dice are thrown. What is the probability that their sum is 5?": "1/9",
        "One card is drawn from a 52-card pack. What is the probability of drawing a face card?": "3/13",
        "A single card is taken from a shuffled standard deck. What is the probability that it is a red king?": "1/26",
        "A playing card is picked blindly from a full deck. What is the probability of a red card?": "1/2",
    }
    by_stem = {row["question_text"]: row for row in rows}
    # The eighth source question is the visible three-coin result on slide 10.
    source_answers["Three unbiased coins are tossed. What is the probability of getting at most two heads?"] = "7/8"
    assert len(source_answers) == 8
    for stem, expected in source_answers.items():
        row = by_stem[stem]
        assert row["options"][row["correct_option"]] == expected

