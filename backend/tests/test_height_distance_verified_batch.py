"""Batch shape, calculation-ledger alignment, MCQ and duplicate checks."""
import json
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "height_distance_verified_batch.json"
LEDGER = BASE / "data" / "height_distance_answer_ledger.json"
ORIGINAL = "Original SSC-style practice question"


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def test_batch_rows_match_independent_answer_ledger_and_mcq_invariants():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    assert len(rows) == len(ledger) == 90
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert sum(row["source"] == ORIGINAL for row in rows) == 69
    assert sum(row["source"].startswith(("Height and Distance ", "_Height and Distance ")) for row in rows) == 21
    for i, (row, audit) in enumerate(zip(rows, ledger), start=1):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == ("maths", "advanced-maths", "height-and-distance")
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


def test_independently_recomputed_answer_samples_cover_height_and_distance_cases():
    rows = {r["question_text"]: r for r in json.loads(BATCH.read_text(encoding="utf-8"))["questions"]}
    cases = {
        "The angle of elevation of the top of a tower from a point 50 m away from its foot is 30°. The height of the tower is:": "50/√3 m",
        "The elevation of the top of a tower from a point on the ground is 45°. On travelling 60 m towards the tower, the elevation becomes 60°. The height of the tower is:": "30(3+√3) m",
        "A man on the top of a 50 m high tower sees a car moving towards the tower at an angle of depression of 30°. After some time the angle of depression becomes 60°. The distance travelled by the car during this time is:": "100√3/3 m",
        "A vertical pole and a vertical tower stand on the same level ground. The pole is 10 m high. From the top of the pole, the angle of elevation of the top of the tower is 60° and the angle of depression of the foot of the tower is 30°. The height of the tower is:": "40 m",
        "Two poles of equal height stand opposite to each other on either side of a road 100 m wide. From a point between them on the road, the angles of elevation of their tops are 30° and 60°. The height of each pole is:": "25√3 m",
        "The angle of elevation of the top of a tower from the bottom of a building is twice that from its top. If the tower is 75 m high and the angle of elevation of the top of the tower from the bottom of the building is 60°, the height of the building is:": "50 m",
        "At the foot of a mountain the elevation of its summit is 45°. After ascending 3 km towards the mountain up a slope of 30° inclination, the elevation is found to be 60°. The height of the mountain is:": "(3/2)(√3+1) km",
        "A tower standing on a horizontal plane subtends a certain angle at a point 160 m from its foot. On advancing 100 m towards it, the tower subtends an angle twice as before. The height of the tower is:": "80 m",
        "From a point P, the tangent of the angle of elevation of a tower is 3/4. On walking 560 m towards the tower, the tangent of the angle of elevation becomes 4/3. The height of the tower is:": "960 m",
        "The angle of elevation of a cloud from a point 60 m above a lake is 30° and the angle of depression of its reflection in the lake is 60°. Find the height of the cloud above the lake.": "120 m",
        "A ladder 25 m long reaches a window 20 m above the ground on one side of a street. Keeping its foot fixed, the ladder is turned to the other side to reach a window 7 m high. Find the width of the street.": "39 m",
        "A tree is broken by the wind so that its top touches the ground 8 m from the foot, making an angle of 30° with the ground. Find the original height of the tree.": "8√3 m",
        "A man on the top of a tower observes a car approaching the tower at a uniform speed. If the angle of depression changes from 30° to 45° in 12 minutes, how much longer will the car take to reach the foot of the tower?": "6(√3+1) minutes",
        "The angle of elevation of the top of a tower from a point A on the ground is 60°. From a point B, 40 m vertically above A, the angle of elevation is 30°. Find the height of the tower.": "60 m",
        "Two poles of equal height stand on either side of a road 80 m wide. From a point between them on the road, the angles of elevation of their tops are 60° and 30°. Find the height of the poles.": "20√3 m",
    }
    for stem, expected in cases.items():
        row = rows[stem]
        assert row["options"][row["correct_option"]] == expected
