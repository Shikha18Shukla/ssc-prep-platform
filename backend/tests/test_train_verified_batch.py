"""Train batch schema, source answer checks, and duplicate review."""
import json
from math import isclose
import re
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BATCH = Path(__file__).resolve().parents[1] / "data" / "train_verified_batch.json"
PDF_EXPECTED = {18: "125 m", 21: "52 and 26 km/h", 22: "7:5", 24: "108 km/h"}


def normalized(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def number_masked(value):
    value = normalized(value)
    value = re.sub(r"\b\d+(?:\.\d+)?(?:/\d+(?:\.\d+)?)?%?\b", " <n> ", value)
    return " ".join(re.sub(r"[^a-z<> ]", " ", value).split())


def test_batch_schema_pdf_answers_provenance_and_distribution():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    assert len(rows) == 90
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert sum(row["source"].startswith("Verified from supplied Train PDF") for row in rows) == 4
    assert sum(row["source"] == "Original SSC-style practice question" for row in rows) == 86
    pdf_rows = [row for row in rows if row["source"].startswith("Verified from supplied Train PDF")]
    assert [int(re.search(r"page (\d+);", row["source"]).group(1)) for row in pdf_rows] == [18, 21, 22, 24]
    for row in rows:
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == ("maths", "arithmetic-maths", "train")
        assert row["is_pyq"] is False and row.get("pyq_year") is None and row.get("pyq_exam_name") is None
        assert row["question_text"].strip() and row["explanation"].strip()
        assert set(row["options"]) == set("ABCD")
        assert len({normalized(v) for v in row["options"].values()}) == 4
        assert row["correct_option"] in row["options"]
    for row in pdf_rows:
        page = int(re.search(r"page (\d+);", row["source"]).group(1))
        assert row["options"][row["correct_option"]] == PDF_EXPECTED[page], row["question_text"]


def test_batch_stems_have_no_exact_normalized_number_masked_or_lexical_duplicates():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    stems = [row["question_text"] for row in rows]
    assert len({normalized(stem) for stem in stems}) == len(stems)
    for index, stem in enumerate(stems):
        for prior in stems[:index]:
            assert number_masked(stem) != number_masked(prior), f"number-masked duplicate: {stem!r} / {prior!r}"
            score = SequenceMatcher(None, normalized(stem), normalized(prior)).ratio()
            assert score < .92, f"lexical near duplicate {score:.3f}: {stem!r} / {prior!r}"


def test_semantic_review_replacements_match_independent_calculations():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    kmh_to_ms = 1000 / 3600
    round_trip_outward_speed = 60
    assert isclose(120 / round_trip_outward_speed + 120 / (1.25 * round_trip_outward_speed), 3.6)
    slower_equal_route_speed = 45
    assert isclose(180 / slower_equal_route_speed - 180 / (slower_equal_route_speed + 15), 1)
    expected = {
        10: f"{(12 * 16 + 11 * 2) / 20:.1f} s",
        11: f"{5 * 1000 / (72 * kmh_to_ms):.0f} s",
        14: f"{60 * (72 / 60 - 72 / 72):.0f} min",
        21: f"{540 - 54 * kmh_to_ms * 12:.0f} m",
        24: f"{72 * 25 / 60 + 60 * 35 / 60:.0f} km",
        35: f"{(90 - 15) / (30 / 60) - 72:.0f} km/h",
        36: f"{(2 * 600) / (30 + 10) * 3.6:.0f} km/h",
        48: f"{360 / 18 - 300 / 20:.0f} m/s",
        52: f"{120 / (240 / 72 - 120 / 60):.0f} km/h",
        58: f"{20 * 18 - 80:.0f} m",
        59: f"{(60 / 60 + 120 / 90) * 60:.0f} min",
        64: f"{(600 - 360) / (72 * kmh_to_ms):.0f} s",
        65: f"{((240 / 20 + 240 / 12) / 2) * 3.6:.1f} km/h",
        68: f"{(390 + 17 * 30) / 45:.0f} m/s",
        71: f"{(300 + 180) / (300 / 20 + 180 / 12):.0f} s",
        72: f"{round_trip_outward_speed:.0f} km/h",
        73: f"{(3 / 5) * (72 * kmh_to_ms * 25):.0f} m",
        76: f"{240 / 72 - 20 / 60:.0f} h",
        78: f"{slower_equal_route_speed:.0f} km/h",
        85: f"{((12 * 6 * kmh_to_ms + 20 * 9 * kmh_to_ms) / 8) * 3.6:.1f} km/h",
        87: f"{1 + (360 - 72 - 72) / (108 + 72):.1f} h",
        88: f"{(395 + 5) / (20 + 5):.0f} coaches",
        90: f"{(240 + 360) / abs(240 / 20 - 360 / 24):.0f} s",
    }
    for row_number, answer in expected.items():
        row = rows[row_number - 1]
        assert row["options"][row["correct_option"]] == answer, row["question_text"]
