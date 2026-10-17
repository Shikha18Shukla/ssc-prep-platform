"""Batch shape, calculation-ledger alignment, MCQ and duplicate checks."""
import json
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "geometry_verified_batch.json"
LEDGER = BASE / "data" / "geometry_answer_ledger.json"


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def test_batch_rows_match_independent_answer_ledger_and_mcq_invariants():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    assert len(rows) == len(ledger) == 90
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert sum(row["source"] == "Original SSC-style practice question" for row in rows) == 76
    assert sum(row["source"].startswith("Geometry ") for row in rows) == 14
    for i, (row, audit) in enumerate(zip(rows, ledger), start=1):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == ("maths", "advanced-maths", "geometry")
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
        if row["source"] != "Original SSC-style practice question":
            assert ", PDF page " in row["source"] and "exam/year not stated" in row["source"]


def test_stems_are_unique_and_not_near_verbatim_duplicates():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    stems = [norm(row["question_text"]) for row in rows]
    assert len(set(stems)) == 90
    for i, stem in enumerate(stems):
        assert all(SequenceMatcher(None, stem, previous).ratio() < .97 for previous in stems[:i])


def test_independently_recomputed_answer_samples_cover_geometry_theorems():
    rows = {r["question_text"]: r for r in json.loads(BATCH.read_text(encoding="utf-8"))["questions"]}
    cases = {
        "Two parallel chords of a circle have lengths 10 cm and 4 cm, lie on the same side of the centre, and are 3 cm apart. Find the circle's diameter.": "2√29 cm",
        "A chord of a circle is 10 cm long and is 12 cm from the centre. Find the circle's diameter.": "26 cm",
        "Two concentric circles have radii 5 cm and 3 cm. A chord of the larger circle is tangent to the smaller circle. Find the chord length.": "8 cm",
        "From an external point P, PT is a tangent of length 12 cm, and a secant meets the circle at A then B. If PA=x cm and AB=7 cm, find x.": "9 cm",
        "O is the circumcentre of △PQR. If ∠QOR=110° and ∠OPR=25°, find ∠PRQ.": "60°",
        "A right triangle has altitude from the right angle to its hypotenuse, splitting the hypotenuse into 9 cm and 16 cm segments. Find the altitude.": "12 cm",
        "In triangle ABC, D is midpoint of BC. If AB²+AC²=250 cm² and BC=10 cm, find AD.": "10 cm",
        "The sides of a triangle are 9 cm, 10 cm, and 17 cm. Find the median to the side of length 17 cm.": "√73/2 cm",
    }
    for stem, expected in cases.items():
        row = rows[stem]
        assert row["options"][row["correct_option"]] == expected
