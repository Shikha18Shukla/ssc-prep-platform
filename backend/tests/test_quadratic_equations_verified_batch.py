"""Batch shape, calculation-ledger alignment, MCQ and duplicate checks."""
import json
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "quadratic_equations_verified_batch.json"
LEDGER = BASE / "data" / "quadratic_equations_answer_ledger.json"
ORIGINAL = "Original SSC-style practice question"


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def test_batch_rows_match_independent_answer_ledger_and_mcq_invariants():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    assert len(rows) == len(ledger) == 90
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert sum(row["source"] == ORIGINAL for row in rows) == 75
    assert sum(row["source"].startswith("Quadratic Equations ") for row in rows) == 15
    for i, (row, audit) in enumerate(zip(rows, ledger), start=1):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == ("maths", "advanced-maths", "quadratic-equations")
        assert row["is_pyq"] is False and row.get("pyq_year") is None and row.get("pyq_exam_name") is None
        assert row["question_text"].strip() and row["explanation"].strip()
        assert set(row["options"]) == set("ABCD")
        assert all(isinstance(v, str) and v.strip() for v in row["options"].values())
        assert len({norm(v) for v in row["options"].values()}) == 4
        assert row["correct_option"] in row["options"]
        assert row["options"][row["correct_option"]] == audit["expected_answer"]
        assert row["question_text"] == audit["question"]
        assert row["difficulty"] == audit["difficulty"]
        assert audit["row"] == i and audit["independent_reasoning"].strip()
        if row["source"] != ORIGINAL:
            assert ", PDF page " in row["source"] and "exam/year not stated" in row["source"]


def test_stems_are_unique_and_not_near_verbatim_duplicates():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    stems = [norm(row["question_text"]) for row in rows]
    assert len(set(stems)) == 90
    for i, stem in enumerate(stems):
        assert all(SequenceMatcher(None, stem, previous).ratio() < .97 for previous in stems[:i])


def test_independently_recomputed_answer_samples_cover_quadratic_cases():
    rows = {r["question_text"]: r for r in json.loads(BATCH.read_text(encoding="utf-8"))["questions"]}
    cases = {
        "If α and β are the roots of 4x² + 3x + 7 = 0, then the value of 1/α + 1/β is:": "−3/7",
        "If α and β are the roots of x² − x + 1 = 0, then the value of α² + β² is:": "−1",
        "If the equation 2x² − 7x + 12 = 0 has roots α and β, then the value of α/β + β/α is:": "1/24",
        "One root of the quadratic equation x² − kx + 27 = 0 is 3; find the value of k.": "12",
        "Find k if one root of the equation x² − 9x + k = 0 is twice the other root.": "18",
        "Find k so that the sum of the roots of 3x² + (2k + 1)x − k − 5 = 0 equals their product.": "4",
        "If the sum of the roots of a quadratic equation is 1 and the product of the roots is −20, the equation is:": "x² − x − 20 = 0",
        "Which of the following quadratic equations has roots −3 and −5?": "x² + 8x + 15 = 0",
        "When (x⁴ − 3x³ + 2x² − 5x + 7) is divided by (x − 2), the remainder is:": "−3",
        "When f(x) = 15x³ − 14x² − 4x + 1 is divided by (3x + 2), the remainder is:": "−7",
        "The roots of the equation x² − 8x + 15 = 0 are:": "3, 5",
        "For what value(s) of k does the quadratic equation 9x² + 3kx + 4 = 0 have equal roots?": "±4",
        "If the roots of ax² + bx + c = 0 are equal, then c equals:": "b²/(4a)",
        "For what values of k does the equation x² + 2(k − 4)x + 2k = 0 have equal roots?": "8, 2",
        "If the product of the roots of x² − (k + 7)x + 2(2k − 2) = 0 is three times their sum, then k equals:": "25",
        "Solve: x² − 5x + 6 = 0.": "2, 3",
        "The positive root of the equation x² − 49 = 0 is:": "7",
        "Find the discriminant of x² − 4x + 4 = 0.": "0",
        "The nature of the roots of x² + 2x + 5 = 0 is:": "No real roots",
        "Form the quadratic equation whose roots are 2 and 3.": "x² − 5x + 6 = 0",
        "If one root of x² + px + 8 = 0 is 2, then p equals:": "−6",
        "For the equation 2x² − 5x + 3 = 0 with roots α and β, 1/α + 1/β equals:": "5/3",
        "α and β are the roots of x² − 4x + 1 = 0. Find α² + β².": "14",
        "The roots of x² − 5x + 6 = 0 are α and β; determine (α − β)².": "1",
        "Determine k such that 2x² + 3x + k = 0 has equal roots.": "9/8",
        "If α and β satisfy x² − 3x + 1 = 0, then α³ + β³ = ?": "18",
        "Let α and β be the roots of x² − 6x + 4 = 0. Evaluate α/β + β/α.": "7",
        "The length of a rectangle is 3 m more than its breadth and its area is 180 m². The length is:": "15 m",
        "The product of two consecutive positive integers is 30. The integers are:": "5 and 6",
    }
    for stem, expected in cases.items():
        row = rows[stem]
        assert row["options"][row["correct_option"]] == expected
