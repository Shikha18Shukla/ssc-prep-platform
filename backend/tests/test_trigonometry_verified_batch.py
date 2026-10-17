"""Batch shape, independently worked solutions, provenance, and MCQ checks."""
import json
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "trigonometry_verified_batch.json"
LEDGER = BASE / "data" / "trigonometry_answer_ledger.json"


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def test_rows_align_with_ledger_and_have_one_keyed_answer_and_four_options():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    assert len(rows) == len(ledger) == 90
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert sum(row["source"] == "Original SSC-style practice question" for row in rows) == 83
    assert sum(row["source"].startswith("Trigonometry ") for row in rows) == 7
    for i, (row, audit) in enumerate(zip(rows, ledger), start=1):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == ("maths", "advanced-maths", "trigonometry")
        assert row["is_pyq"] is False and row.get("pyq_year") is None and row.get("pyq_exam_name") is None
        assert row["question_text"].strip() and row["explanation"].strip()
        assert set(row["options"]) == set("ABCD")
        assert all(isinstance(value, str) and value.strip() for value in row["options"].values())
        assert len({norm(value) for value in row["options"].values()}) == 4
        assert row["correct_option"] in row["options"]
        assert sum(norm(value) == norm(row["options"][row["correct_option"]]) for value in row["options"].values()) == 1
        assert row["options"][row["correct_option"]] == audit["expected_answer"]
        assert row["question_text"] == audit["question"] and row["difficulty"] == audit["difficulty"]
        assert audit["row"] == i and audit["independent_reasoning"].strip()
        if row["source"] != "Original SSC-style practice question":
            assert ", PDF page " in row["source"] and "exam/year not stated" in row["source"]


def test_stems_are_unique_and_not_near_verbatim_duplicates():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    stems = [norm(row["question_text"]) for row in rows]
    assert len(set(stems)) == 90
    for i, stem in enumerate(stems):
        assert all(SequenceMatcher(None, stem, previous).ratio() < .97 for previous in stems[:i])


def test_selected_trigonometric_calculations_are_independently_recomputed():
    rows = {row["question_text"]: row for row in json.loads(BATCH.read_text(encoding="utf-8"))["questions"]}
    expected = {
        "Evaluate (cos²20° + cos²70°)/sin²90° − tan²45°.": "0",
        "If sin(A+B)=1 and cos(A−B)=1/2 for acute A and B, find A.": "75°",
        "Evaluate sin²5° + sin²25° + sin²45° + sin²65° + sin²85°.": "2.5",
        "Evaluate sin²5° + sin²6° + … + sin²84° + sin²85°.": "40.5",
        "Evaluate 2(sin1°·sec89°)+3(cos11°·cosec79°)+5(tan21°·tan69°).": "10",
        "In right △ABC, ∠B=90°, AC=2√5 cm and AB−BC=2 cm. Find cos²A−cos²C.": "3/5",
        "If cosec53°=a/b (with a>b>0), find tan37°.": "√(a²−b²)/b",
        "If secθ=13/12 for acute θ, find tanθ.": "5/12",
        "If tanθ+cotθ=10/3 for acute θ, find sin2θ.": "3/5",
        "If sinθ+cosθ=7/5 for acute θ, find sin2θ.": "24/25",
        "If sinθ=3/5 for acute θ, evaluate 1/(1+cosθ)+1/(1−cosθ).": "50/9",
    }
    for stem, answer in expected.items():
        row = rows[stem]
        assert row["options"][row["correct_option"]] == answer

