"""Validate the authored Hard Ratio & Proportion questions against independent arithmetic."""
import json
import re
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARD = ROOT / "data" / "ratio_proportion_hard_batch.json"
EASY = ROOT / "data" / "ratio_proportion_easy_batch.json"
MEDIUM = ROOT / "data" / "ratio_proportion_medium_batch.json"

# Values independently solved from each stem (ratio equations, alligation,
# weighted capital, or direct part arithmetic), without reading the answer keys.
EXPECTED = [
 "800", "252", "₹1,650", "9 years", "572", "10:22:43", "25:1", "54 L",
 "2,652", "24:20:21", "5,760", "40:32:55", "20 years", "₹2,880", "126 ha",
 "2:3", "12.8 L", "30", "28 4/7%", "640", "18:15:25", "42 years", "3:4",
 "3:2", "₹4,250", "77", "451", "₹18,000", "4:9:17", "648",
]

def norm(s):
    return " ".join(s.casefold().split())

def masked(s):
    return re.sub(r"\d+(?:,\d{3})*(?:\.\d+)?", "<n>", norm(s))

def test_hard_data_count_metadata_options_and_answers():
    questions = json.loads(HARD.read_text(encoding="utf-8"))["questions"]
    assert len(questions) == 30
    assert Counter(q["difficulty"] for q in questions) == {"HARD": 30}
    assert len(EXPECTED) == len(questions)
    for q, answer in zip(questions, EXPECTED):
        assert q["chapter_slug"] == "ratio-and-proportion"
        assert q["is_pyq"] is False
        assert q["source"] == "Original SSC-style practice question"
        assert set(q["options"]) == {"A", "B", "C", "D"}
        assert len({v.casefold().strip() for v in q["options"].values()}) == 4
        assert q["options"][q["correct_option"]] == answer, q["question_text"]
        assert sum(v == answer for v in q["options"].values()) == 1
        assert q["explanation"].strip()

def test_hard_stems_have_no_exact_masked_or_high_lexical_duplicates_across_batches():
    batches = [("easy", EASY), ("medium", MEDIUM), ("hard", HARD)]
    stems = [(name, q["question_text"]) for name, path in batches
             for q in json.loads(path.read_text(encoding="utf-8"))["questions"]]
    assert len({norm(stem) for name, stem in stems if name == "hard"}) == 30
    for i, (kind_a, a) in enumerate(stems):
        for kind_b, b in stems[:i]:
            if kind_a == kind_b == "easy" or kind_a == kind_b == "medium":
                continue
            assert masked(a) != masked(b), f"number-masked duplicate: {a!r} / {b!r}"
            assert SequenceMatcher(None, norm(a), norm(b)).ratio() < 0.92, f"near duplicate: {a!r} / {b!r}"
