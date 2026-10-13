"""Independent arithmetic and batch-quality checks for the 90-question bank."""
import json
import re
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from math import sqrt
from pathlib import Path

BATCH = Path(__file__).resolve().parents[1] / "data" / "speed_time_distance_verified_batch.json"

# Recomputed directly from the quantities and relations in each stem, separately
# from the answer values and explanations in the curation script.
VERIFIED_ANSWERS = [
    # Easy 1-30
    54*3, 180/4, 210/70, 72*5/18, 15*18/5, 48*2.5, 360/30, 42*90/60,
    180/2.5, 2*40*60/(40+60), (20*.5+60*1.5)/2,
    45*4/(4+.5), 12+2, 15-3, 48+36, 150/10, 180/(54*5/18), 1.5/.5,
    12/(40/60), 300/60*18/5, 240/80, 5*18/5, 30/(60-45), 220/(50+60),
    100-100*20/25, (120+180)/(72*5/18), (40+60)/2,
    90/45+90/60, 60/4, 60/(20/40+40/80),
    # Medium 31-60
    2*75*50/(75+50), (3*48+2*66)/5, 360/(240/60+120/40), 240/48-240/60,
    (20/60)/(1/30-1/40), 72*5/18*15, 54*5/18*40-200, (72+54)*5/18,
    (220+180)/((72-54)*5/18), (48/3-36/3)/2, (22-14)/2,
    72/12-72/18, 200-200*(175/200)*(180/200), 400/6-400/8,
    120/(120/40-1), (30+60)/(30/30+60/60),
    1/(1/3/30+2/3/60), 24/(1-48/60), 6/4+6/6,
    60*(40*.75/(60-40)), 300/(40+35), 400-7*(400/8),
    72*5/18*27.5-250, 12.5*8*60/1000, (18+14)/2, 88/(18+4),
    (20+30)/2, 90/45-90/60, 210/(210/70-.5), 1.2/3*60,
    # Hard 61-90
    360/(2+3+.5), 3/(1/30+1/40+1/60), .4/(1/50-1/75),
    40+40*((220-40)/(40+50)), ((300+400)/20)*18/5-72,
    72*5/18*30-240, (300/12-6*5/18)*18/5,
    (200+180)/((72-54)*5/18), (300/(24-12))*12,
    ((180+220)/16)*18/5-54, (90/3+90/5)/2,
    (72/3-60/5)/2, (72/3+72/4.5)/2,
    400-400*(360/400)*(370/400), 2*600/(6+4), 260/(2+3+.5),
    120/(360/60-120/40-120/60), 180/(4.5-90/45), 500/25*18/5,
    ((180+200)/10-72*5/18)*18/5,
    56*((320-40*.5)/(40+56)), 900/17, 240,
    (24-12)/2, 600/(240/60+240/80+120/100),
    1+1+(400-60-(60+40))/(60+60), 360/(180/45+180/60),
    180/(360/72-180/60-.5),
    1+(60-(90-60))/(90-80),
    # Opposite-direction meetings: solve 48/(v-4)+80/(v+4)=8;
    # the positive physical root of 8v^2-128v=0 is 16 km/h.
    (-(-128)+sqrt((-128)**2-4*8*0))/(2*8),
]


def normalized(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def number_masked(text):
    value = normalized(text)
    value = re.sub(r"\d[\d,]*(?:\.\d+)?%?", " <n> ", value)
    return " ".join(re.sub(r"[^a-z<> ]", " ", value).split())


def load_questions():
    return json.loads(BATCH.read_text(encoding="utf-8"))["questions"]


def test_batch_count_difficulty_schema_options_provenance_and_answers():
    questions = load_questions()
    assert len(questions) == 90
    assert Counter(q["difficulty"] for q in questions) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert len(VERIFIED_ANSWERS) == len(questions)
    for index, (row, independently_calculated) in enumerate(zip(questions, VERIFIED_ANSWERS), 1):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == (
            "maths", "arithmetic-maths", "speed-time-and-distance"
        )
        assert row["difficulty"] in {"EASY", "MEDIUM", "HARD"}
        assert row["is_pyq"] is False
        assert row["pyq_year"] is None and row["pyq_exam_name"] is None
        assert row["source"] == "Original SSC-style practice question"
        assert row["question_text"].strip() and row["explanation"].strip()
        assert set(row["options"]) == {"A", "B", "C", "D"}
        option_texts = [value.strip() for value in row["options"].values()]
        assert len({normalized(value) for value in option_texts}) == 4, row["question_text"]
        assert row["correct_option"] in row["options"]
        numeric_options = [float(value) for value in option_texts]
        expected = round(independently_calculated, 2)
        assert numeric_options.count(expected) == 1, (index, row["question_text"], independently_calculated)
        assert float(row["options"][row["correct_option"]]) == expected


def test_no_exact_number_masked_or_high_lexical_duplicate_questions():
    stems = [row["question_text"] for row in load_questions()]
    assert len({normalized(stem) for stem in stems}) == 90
    for index, stem in enumerate(stems):
        for prior in stems[:index]:
            assert number_masked(stem) != number_masked(prior), f"number-masked duplicate: {stem!r} / {prior!r}"
            similarity = SequenceMatcher(None, normalized(stem), normalized(prior)).ratio()
            assert similarity < 0.92, f"high lexical similarity {similarity:.3f}: {stem!r} / {prior!r}"
