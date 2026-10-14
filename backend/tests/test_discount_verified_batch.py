"""Independent arithmetic, schema, provenance and duplicate checks for Discount."""
import json
import re
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BATCH = Path(__file__).resolve().parents[1] / "data" / "discount_verified_batch.json"

# Recomputed from the numerical relationships in each stem, independent of the
# answer key and explanations stored in the batch.
CALCULATED = [
    2400*.875, (3600-3060)/3600*100, 144/960*100, 2500*.82,
    5000*.8*.9, (1.4*.85-1)*100, (((3600-360)*.95)-2400)/2400*100,
    (1.2/.9-1)*100, (5000-5000*.9*.875+300)/5000*100,
    (1-3468/(4800*.85))*100, 20, (.9*1.25-.9)/.9*100,
    (1.8*.75-1)*100, (.9-.75)/.75*100, (1-.4/(.7*.8))*100,
    (1980*.95-1800)/1800*100, (1.3*.9*.95-1)*100,
    (1.25*.9*.96-1)*100, (1-1.0125/(1.25*.9))*100,
    (.9/.75-1)*100, ((3700*.75-2400)/2400)*100, 3200*.85,
    (1-.75*.92)*100, (4400-4000)/4000*100, 216, 3360/.84,
    2200*1.1/.88, (.95/.75-1)*100, 7500*.9*.96,
    (1.5*.9*.9-1)*100, 260/(1.4*.9-1), (1.6*.75-.03-1)*100,
    (.9-.85)/.85*100,
    # PDF-derived: pages 5, 6, 7, 8, 13, 18, 20, 23, 24, 25.
    (3600-3132)/3600*100, (1-.95*.90*.80)*100, 2000*.70*.80*.90,
    1800*.90*.80, 50000*(.20-(1-.84*.96)), 85*1.20/.85,
    (1.066/.82-1)*100, 4/7*100, (1-2/3)*100,
    (1-(12/15)*.75)*100,
    # Original Easy additions.
    800*.85, (1250-1000)/1250*100, 96/640*100, 765/.85,
    2500*.88, (480-408)/480*100, 400/3200*100, 225/1500*100,
    1350/.75, (2400-2040)/2400*100, 960*.125, 3500*.08,
    (1800-1530)/1800*100, (680-612)/680*100, 2400*.8,
    720/3600*100, 540/.9, 900*.7, (1600-1360)/1600*100,
    (2250-2025)/2250*100, 480*.75, 1760*.9375,
    # Original Medium additions.
    4000*.9*.95, (1-.8*.85)*100, 2448/(.85*.8),
    (5000-(5000*.9-350))/5000*100, (2640-2400)/2400*100,
    abs(4800*.75-4800*.85*.88), 3528/.84, 6400*.875-200,
    (1-.9*.8)*100, 1530/.85,
    # Original Hard additions.
    (1.4*.9*.95-1)*100, 300/(1.25*.9-1),
    (1.6*.8-.04-1)*100, (1-.8*.9)*100,
    (1-.60/.75)*100, 120/(1.50*.80-1.05),
    (1-.7*.95)*100, (1.8*.75-1)*100, 11/10,
    (1-1.2*.8)*100, (2700+300)/.9, (1.19/.85-1)*100,
    (1-.6/(.875*.8))*100, 60/(1.3*.9-1.08),
    6000*.75*1.10,
]


def normalized(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def number_masked(value):
    value = normalized(value)
    value = re.sub(r"\d[\d,]*(?:\.\d+)?%?", " <n> ", value)
    return " ".join(re.sub(r"[^a-z<> ]", " ", value).split())


def answer_number(text):
    text = text.replace(",", "")
    ratio = re.search(r"(-?\d+(?:\.\d+)?):(-?\d+(?:\.\d+)?)", text)
    if ratio:
        return float(ratio.group(1)) / float(ratio.group(2))
    mixed = re.search(r"(-?\d+)\s+(\d+)/(\d+)", text)
    if mixed:
        sign = -1 if mixed.group(1).startswith("-") else 1
        return sign * (abs(int(mixed.group(1))) + int(mixed.group(2))/int(mixed.group(3)))
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    assert match, f"No numeric answer found in {text!r}"
    return float(match.group())


def test_batch_schema_provenance_difficulty_and_unique_options():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    assert len(rows) == len(CALCULATED) == 90
    assert Counter(q["difficulty"] for q in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert sum(q["source"].startswith("Verified from supplied Discount PDF") for q in rows) == 10
    assert sum(q["source"].startswith("Original SSC-style practice question") for q in rows) == 80
    for row in rows:
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == (
            "maths", "arithmetic-maths", "discount"
        )
        assert row["is_pyq"] is False and row.get("pyq_year") is None and row.get("pyq_exam_name") is None
        assert row["question_text"].strip() and row["explanation"].strip()
        assert set(row["options"]) == set("ABCD")
        assert len({normalized(v) for v in row["options"].values()}) == 4
        assert row["correct_option"] in row["options"]


def test_answers_match_independent_calculations():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    for index, (row, expected) in enumerate(zip(rows, CALCULATED)):
        chosen = row["options"][row["correct_option"]]
        actual = answer_number(chosen)
        tolerance = max(0.011, abs(expected)*0.0001)
        assert abs(actual - expected) <= tolerance, (index + 1, row["question_text"], chosen, expected)
        if index == 24:  # The answer combines a named offer with a rupee difference.
            assert chosen == "Offer A, by Rs 216"
        else:
            assert sum(abs(answer_number(value) - expected) <= tolerance for value in row["options"].values()) == 1


def test_no_exact_number_masked_or_high_lexical_duplicates():
    stems = [q["question_text"] for q in json.loads(BATCH.read_text(encoding="utf-8"))["questions"]]
    assert len({normalized(stem) for stem in stems}) == len(stems)
    for i, stem in enumerate(stems):
        for prior in stems[:i]:
            assert number_masked(stem) != number_masked(prior), (stem, prior)
            assert SequenceMatcher(None, normalized(stem), normalized(prior)).ratio() < .92, (stem, prior)
