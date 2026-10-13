"""Validate Medium Ratio & Proportion data and distinguish it from Easy items."""
import json
import math
import re
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MEDIUM_PATH = ROOT / "data" / "ratio_proportion_medium_batch.json"
EASY_PATH = ROOT / "data" / "ratio_proportion_easy_batch.json"


def reduced_ratio(a, b):
    divisor = math.gcd(a, b)
    return f"{a // divisor}:{b // divisor}"


def independently_calculated_answers():
    # These calculations are deliberately expressed independently of the
    # batch options and explanations; every stem must have one calculation.
    return {
        "A:B=3:5 and B:C=10:7. If A+B+C=₹920, how much is B?": f"₹{920 * 10 // 23}",
        "A 1,080 m cable is cut into two sections in the ratio 2:7. The shorter section is then cut in the ratio 3:5. What is the length of the shortest final piece?": f"{1_080 * 2 // 9 * 3 // 8} m",
        "A and B hold amounts in the ratio 2:7. If ₹80 is transferred from B to A, their ratio becomes 4:5. What was their original total?": f"₹{(80 * (4 + 5) // (4 * 7 - 5 * 2)) * (2 + 7):,}",
        "A prize of ₹2,400 is divided between P and Q in the ratio 3:5. P gives 20% of her share to Q. What is their final ratio P:Q?": reduced_ratio(2_400 * 3 // 8 * 80 // 100, 2_400 * 5 // 8 + 2_400 * 3 // 8 * 20 // 100),
        "P:Q=4:7. P's quantity rises by 25% while Q's falls by 20%. What is the new ratio P:Q?": reduced_ratio(4 * 125, 7 * 80),
        "The number of boys and girls is in the ratio 5:4. After 8 boys leave, the ratio is 3:4. How many students were there initially?": str((5 + 4) * 4),
        "A parent's and child's present ages are in the ratio 5:3. In 8 years, their ages will be in the ratio 7:5. What is their present combined age?": f"{(5 + 3) * 4} years",
        "A father is three times his son's age. Five years ago, the father was four times his son's age. How old is the father now?": f"{3 * 15} years",
        "A 3:2 milk-water mixture has 12 litres of water added, making the ratio 3:4. What was the original mixture volume?": f"{(3 + 2) * 6} L",
        "A 40 L mixture contains milk and water in the ratio 3:1. Ten litres of mixture are removed and replaced with water. What is the final milk:water ratio?": reduced_ratio((40 - 10) * 3, (40 - 10) * 1 + 10 * 4),
        "A and B have total monthly incomes of ₹60,000 in the ratio 7:5. Their total monthly expenditure is ₹35,000 in the ratio 4:3. What is their savings ratio A:B?": reduced_ratio(60_000 * 7 // 12 - 35_000 * 4 // 7, 60_000 * 5 // 12 - 35_000 * 3 // 7),
        "A:B incomes are in the ratio 4:5. A saves 25% of income and B saves 40%. What is the ratio of their savings?": reduced_ratio(4 * 25, 5 * 40),
        "Three-fifths of A's amount equals two-sevenths of B's amount. Find A:B.": reduced_ratio(2 * 5, 3 * 7),
        "Two numbers are in the ratio 4:7. Adding 6 to the smaller and subtracting 3 from the larger makes their ratio 2:3. Find the original larger number.": str(7 * 12),
        "A:B=5:8. If 12 is added to A and 8 is subtracted from B, the new ratio is 3:4. Find A+B originally.": str((5 + 8) * 18),
        "If 3x:5y=9:20 and x+y=49, find x.": str(49 * 3 // 7),
        "Three amounts are in the ratio 2:3:5. The largest exceeds the smallest by ₹540. What is the middle amount?": f"₹{540 * 3 // (5 - 2)}",
        "The sides of a triangle are in the ratio 4:5:6. If its perimeter is 180 cm, what is the length of the longest side?": f"{180 * 6 // (4 + 5 + 6)} cm",
        "A recipe uses rice and lentils in the ratio 5:2. A cook has 1.2 kg of rice and wants to keep the same ratio. How many grams of lentils are needed?": f"{1_200 * 2 // 5} g",
        "A map scale is 1:50,000. A road measures 6 cm on the map. If 1 cm is mistakenly measured as 1.2 cm during copying, what length will that road appear to have on the copy?": f"{6 * 1.2:.1f} cm",
        "A and B divide an amount in the ratio 3:5. If A receives ₹240 less than B, what is the total amount?": f"₹{240 * (3 + 5) // (5 - 3)}",
        "The present ages of two siblings are in the ratio 4:3. After 6 years their ages will total 54 years. How old is the older sibling now?": f"{(54 - 12) * 4 // 7} years",
        "A container has 54 L of juice and water in the ratio 7:2. How much water must be added to make the ratio 7:5?": f"{54 * 5 // 9 - 54 * 2 // 9} L",
        "A sum is divided between X and Y in the ratio 7:9. If X's share is increased by ₹120 and Y's share is reduced by ₹120, the shares become equal. What is the original total?": f"₹{120 * (7 + 9):,}",
        "The ratio of two numbers is 9:13. If their difference is 52, what is their average?": str(52 * (9 + 13) // (2 * (13 - 9))),
        "A worker's pay for 5 days is in the ratio 3:4 to another worker's pay for 6 days. If the first earns ₹900 per day, what does the second earn per day?": f"₹{900 * 5 * 4 // 3 // 6:,}",
        "Three quantities are in the ratio 7:9:12. The first two together equal 128. How much greater is the third quantity than the first?": str(128 * (12 - 7) // (7 + 9)),
        "If a:b=3:4 and b:c=6:7, and a+b+c=350, find c.": str(350 * 14 // (9 + 12 + 14)),
        "R and S make monthly deposits in the ratio 3:4. In one month, R deposits ₹250 extra, making that month's amounts 4:5. What is S's regular deposit?": f"₹{250 * 20:,}",
        "The ratio of two positive quantities is 2:3. Their product is 864. What is their sum?": str(5 * 12),
    }


def normalize(text):
    return " ".join(text.casefold().split())


def number_mask(text):
    return re.sub(r"\d+(?:,\d+)*(?:\.\d+)?", "<n>", normalize(text))


def test_medium_batch_has_thirty_original_medium_questions_and_valid_options():
    questions = json.loads(MEDIUM_PATH.read_text(encoding="utf-8"))["questions"]
    assert len(questions) == 30
    assert Counter(q["difficulty"] for q in questions) == {"MEDIUM": 30}
    for question in questions:
        assert question["chapter_slug"] == "ratio-and-proportion"
        assert question["is_pyq"] is False
        assert question["source"] == "Original SSC-style practice question"
        assert set(question["options"]) == {"A", "B", "C", "D"}
        assert len({value.strip().casefold() for value in question["options"].values()}) == 4
        assert question["correct_option"] in question["options"]
        assert question["explanation"].strip()


def test_every_medium_answer_is_independently_calculated_and_unique():
    questions = json.loads(MEDIUM_PATH.read_text(encoding="utf-8"))["questions"]
    answers = independently_calculated_answers()
    assert len(answers) == len(questions)
    for question in questions:
        computed = answers[question["question_text"]]
        options = question["options"]
        assert options[question["correct_option"]] == computed, question["question_text"]
        assert sum(value == computed for value in options.values()) == 1


def test_medium_has_no_exact_masked_or_near_duplicate_with_either_batch():
    medium = json.loads(MEDIUM_PATH.read_text(encoding="utf-8"))["questions"]
    easy = json.loads(EASY_PATH.read_text(encoding="utf-8"))["questions"]
    medium_stems = [q["question_text"] for q in medium]
    easy_stems = [q["question_text"] for q in easy]
    assert len({normalize(stem) for stem in medium_stems}) == 30

    all_stems = [("medium", stem) for stem in medium_stems] + [("easy", stem) for stem in easy_stems]
    for index, (kind_a, stem_a) in enumerate(all_stems):
        for kind_b, stem_b in all_stems[:index]:
            if kind_a == kind_b == "easy":
                continue
            assert number_mask(stem_a) != number_mask(stem_b), f"number-masked duplicate: {stem_a!r} / {stem_b!r}"
            assert SequenceMatcher(None, normalize(stem_a), normalize(stem_b)).ratio() < 0.92, f"near duplicate: {stem_a!r} / {stem_b!r}"
