"""Validate every curated Average question using separate arithmetic checks."""
import json
import re
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BATCH = Path(__file__).resolve().parents[1] / "data" / "average_verified_batch.json"

# These expressions are separate from the curation rows and their explanations.
# Each expression recomputes the result from the figures stated in its stem.
CALCULATED = [
 # Easy 1–30
 5*24-100, 9*38-8*35, (6*32+25)/7, (30*40-160+40)/30, (1+20)/2,
 4*18-12-17-19, (30*60+20*75)/50, 13*520-12*500, 6*70-5*68,
 (18+26)/2, (31+43)/2, (2*56+18)/2, (4*250+320)/5, 5*17-11-14-18-21,
 (12*64-72+60)/12, (68+76)/2, (4*32+42)/5, 9*45-8*43,
 (8*14+12+20)/10, (6+60)/2, (5*36+60)/6, 12+3, (4*20-44)/3,
 (5*120+150)/6, (15*28+48)/16, 3*30-62, (32+48)/2,
 (2*100+3*120)/5, (6*25-13)/5, 7*52-6*50,
 # Medium 31–60
 92-36*(68-67), 5*24/6, (24*72+16*63)/40, 7*72-6*70,
 (10*50-59)/9, 33*67-32*68, 11*25-(11*26-35), 5*78-296,
 8*4250-28700, (14+36)/2, (9*42+78)/10,
 (40*64-10*44)/30, 47-15, 68+(76-52)/8, (46-3)*(46+3),
 (40+50+60)/3, (12*84-5*78)/7, 36+(45-18)/9, (20*42+5*52)/25,
 13*38-12*35, 24, (40*32-8*42)/32, (1+29)/2,
 9*72-8*69, (6*27-2*48)/4, 10*1800-9*1720,
 31+(5*4-3*2)/8, 25*72+35*68-4000, 42+2*7, (10*70-8*66)/2,
 # Hard 61–90
 (700-6*25+4*30)/18, 24*52-(20*48+72+84+96),
 (40*65-5*91-5*39)/30, (8*29-44+2*2+9)/9,
 6*68+5*78-10*72, (30*36-12*42+8*32)/26,
 6*49+6*52-11*50, 6*52-6*48,
 5*72+4*82-8*76, 8*35+8*46-15*40,
 (50*34-10*46+6*28)/46,
 (25*42-(15*40+80+0+70+0+60))/5,
 3*(2*8/(5-3)), 10*44-9*42,
 3*76+4*83-6*80, (18*24-6*31-5*17)/7,
 7*22+7*29-12*25, (20*26-4*38-3*19+7*24)/20,
 7*60+6*70-12*64, (16*25-10*22)/6,
 13*44+13*53-25*48, 12*42_000-4*38_000-5*40_000,
 (45*68-40*66)/5, 10*21+10*28-18*24,
 (20*35-48-62+84+26)/20, (30*42-6*50+4*33)/28,
 5*70+5*80-9*74,
 (32*31-(40*29-8*24))/(35-31),
 (20*62+30*68+50*74)/100, (42+48+54+60)/4,
]


def normalized(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def masked(text):
    value = normalized(text)
    value = re.sub(r"\d[\d,]*(?:\.\d+)?%?", " <n> ", value)
    return " ".join(re.sub(r"[^a-z<> ]", " ", value).split())


def test_batch_has_exact_counts_valid_schema_options_and_original_provenance():
    questions = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    assert len(questions) == 90
    assert Counter(q["difficulty"] for q in questions) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert len(CALCULATED) == len(questions)
    for row, answer in zip(questions, CALCULATED):
        assert row["subject_slug"] == "maths"
        assert row["subcategory_slug"] == "arithmetic-maths"
        assert row["chapter_slug"] == "average"
        assert row["is_pyq"] is False
        assert row["source"] == "Original SSC-style practice question"
        assert row.get("pyq_year") is None and row.get("pyq_exam_name") is None
        assert row["difficulty"] in {"EASY", "MEDIUM", "HARD"}
        assert row["question_text"].strip() and row["explanation"].strip()
        assert set(row["options"]) == {"A", "B", "C", "D"}
        assert len({value.strip().casefold() for value in row["options"].values()}) == 4
        assert row["correct_option"] in row["options"]
        correct = float(row["options"][row["correct_option"]])
        assert correct == round(answer, 2), row["question_text"]
        assert sum(float(value) == correct for value in row["options"].values()) == 1


def test_no_exact_number_masked_or_high_lexical_duplicates():
    questions = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    stems = [row["question_text"] for row in questions]
    assert len({normalized(stem) for stem in stems}) == 90
    for index, stem in enumerate(stems):
        for prior in stems[:index]:
            assert masked(stem) != masked(prior), f"number-masked duplicate: {stem!r} / {prior!r}"
            similarity = SequenceMatcher(None, normalized(stem), normalized(prior)).ratio()
            assert similarity < 0.92, f"high lexical similarity ({similarity:.3f}): {stem!r} / {prior!r}"
