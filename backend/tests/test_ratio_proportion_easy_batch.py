"""Validation tests for the first original Ratio & Proportion batch."""
import json
import math
from collections import Counter
from pathlib import Path


BATCH = Path(__file__).resolve().parents[1] / "data" / "ratio_proportion_easy_batch.json"


def _independently_calculated_answers():
    # Keep calculations separate from the JSON explanations and answer keys.
    gcd = math.gcd
    return {
        "Simplify the ratio 84:126 to its lowest terms.": f"{84 // gcd(84, 126)}:{126 // gcd(84, 126)}",
        "₹840 is divided between A and B in the ratio 3:4. How much does A receive?": f"₹{840 * 3 // (3 + 4)}",
        "Find the fourth proportional to 6, 9 and 10.": str(9 * 10 // 6),
        "What is the mean proportional between 12 and 27?": str(math.isqrt(12 * 27)),
        "Find the third proportional to 8 and 12.": str(12 * 12 // 8),
        "Given A:B=2:3 and B:C=4:5, what is A:B:C in its simplest whole-number form?": "8:12:15",
        "The ratio of boys to girls in a class is 7:9. If there are 45 girls, how many boys are there?": str(45 * 7 // 9),
        "Two numbers are in the ratio 5:7 and have a sum of 144. What is the smaller number?": str(144 * 5 // (5 + 7)),
        "Two quantities are in the ratio 2:5. If 12 is added to each, their ratio becomes 1:2. What was the smaller quantity originally?": str(2 * 12),
        "What is the ratio of 3 hours 30 minutes to 2 hours 20 minutes in simplest form?": "3:2",
        "If 9:15 = x:40, what is x?": str(9 * 40 // 15),
        "A and B share ₹260 in the ratio 5:8. How much does B receive?": f"₹{260 * 8 // 13}",
        "A prize of ₹840 is divided among three students in the ratio 2:3:7. What is the second student's share?": f"₹{840 * 3 // 12}",
        "Find x if 7:x = 21:45.": str(7 * 45 // 21),
        "A father's age and his daughter's age are in the ratio 4:1. If the daughter is 9 years old, how old is her father?": f"{4 * 9} years",
        "On a map with scale 1:25,000, two places are 8 cm apart. What is their actual distance?": f"{8 * 25_000 // 100_000} km",
        "In a group, the ratio of tea drinkers to coffee drinkers is 3:4. If there are 42 people in these two groups altogether, how many drink tea?": str(42 * 3 // 7),
        "A drink is made with flour and sugar in the ratio 5:2 by weight. In 1.4 kg of this mixture, how much sugar is there?": f"{1_400 * 2 // 7} g",
        "A 60 m ribbon is cut into three pieces in the ratio 2:3:5. What is the length of the middle-sized piece?": f"{60 * 3 // 10} m",
        "A cyclist covers 45 km in 2 hours and a car covers 120 km in 3 hours. What is the ratio of their average speeds, cyclist to car?": "9:16",
        "The ratio of pens owned by Rina to those owned by Salim is 4:9. If Rina has 32 pens, how many pens do they own altogether?": str(32 * 13 // 4),
        "A shopkeeper combines 0.75 kg of one grain with 1.25 kg of another. What is the ratio of the first grain to the second in simplest form?": "3:5",
        "A 315 cm wire is cut into two pieces in the ratio 2:5. What is the length of the shorter piece?": f"{315 * 2 // 7} cm",
        "The length and width of a rectangular field are in the ratio 4:7. Its perimeter is 66 m. What is its width?": f"{66 // (2 * (4 + 7)) * 7} m",
        "The ratio of green to yellow tiles in a display is 4:9. If there are 36 green tiles, how many tiles are in the display?": str(36 * (4 + 9) // 4),
        "A car travels 150 km in 3 hours. At the same speed, how far will it travel in 5 hours?": f"{150 * 5 // 3} km",
        "A school assigns science and art books to its library in the ratio 5:8. If 520 books are assigned altogether, how many are art books?": str(520 * 8 // 13),
        "A 3.6 m board is cut into two pieces whose lengths are in the ratio 5:7. What is the length of the longer piece?": f"{3.6 * 7 / 12:.1f} m",
        "If 4:7 = 20:x, what is x?": str(7 * 20 // 4),
        "A bag contains 2.5 kg of rice and 750 g of lentils. What is the ratio of rice to lentils by weight in simplest form?": f"{2_500 // 250}:{750 // 250}",
    }


def test_easy_batch_structure_options_and_provenance():
    questions = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    assert len(questions) == 30
    assert Counter(q["difficulty"] for q in questions) == {"EASY": 30}
    assert all(q["chapter_slug"] == "ratio-and-proportion" for q in questions)
    assert all(q["is_pyq"] is False for q in questions)
    assert all(q["source"] == "Original SSC-style practice question" for q in questions)
    for question in questions:
        options = question["options"]
        assert set(options) == {"A", "B", "C", "D"}
        assert len({option.strip().casefold() for option in options.values()}) == 4
        assert question["correct_option"] in options
        assert question["explanation"].strip()


def test_each_answer_matches_an_independent_calculation_and_is_unique():
    questions = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    expected = _independently_calculated_answers()
    assert len(expected) == len(questions)
    for question in questions:
        correct = question["options"][question["correct_option"]]
        calculated = expected[question["question_text"]]
        assert correct == calculated, question["question_text"]
        assert sum(option == calculated for option in question["options"].values()) == 1


def test_batch_has_no_exact_or_number_masked_template_duplicates():
    questions = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    stems = [" ".join(q["question_text"].casefold().split()) for q in questions]
    assert len(stems) == len(set(stems))
    import re
    masked = [re.sub(r"\d+(?:,\d+)*(?:\.\d+)?", "<n>", stem) for stem in stems]
    assert len(masked) == len(set(masked))
