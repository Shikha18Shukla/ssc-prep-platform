"""Build and validate the Maximum & Minimum Value question batch and ledger."""
import json
import random
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "maximum_and_minimum_value_verified_batch.json"
LEDGER = BASE / "data" / "maximum_and_minimum_value_answer_ledger.json"
ORIGINAL = "Original SSC-style practice question"
PDF = "Maximum and  Minimum Value.pdf"
ROWS, AUDIT = [], []


def add(level, stem, answer, wrong, proof, page=None):
    vals = list(dict.fromkeys([str(answer), *map(str, wrong)]))
    if len(vals) != 4:
        raise ValueError(f"Need four distinct options: {stem}")
    random.Random(len(ROWS) * 97 + len(stem)).shuffle(vals)
    source = ORIGINAL if page is None else f"{PDF}, PDF page {page}; exam/year not stated (PYQ status unverified)"
    ROWS.append({
        "subject_slug": "maths", "subcategory_slug": "advanced-maths",
        "chapter_slug": "maximum-and-minimum-value", "question_text": stem,
        "options": dict(zip("ABCD", vals)), "correct_option": "ABCD"[vals.index(str(answer))],
        "explanation": proof, "difficulty": level, "is_pyq": False,
        "pyq_year": None, "pyq_exam_name": None, "source": source,
    })
    AUDIT.append({"row": len(ROWS), "question": stem, "difficulty": level,
                  "expected_answer": str(answer), "independent_reasoning": proof, "source": source})


# PDF MCQs: legible question and answer choices reviewed from the indicated slide.
add("EASY", "For 15 sin²θ + 10 cos²θ, what is the maximum value for real θ?", "15", ["10", "25", "5"], "Write 10 + 5sin²θ. Since 0 ≤ sin²θ ≤ 1, the maximum is 15.", 13)
add("EASY", "For 15 sin²θ + 10 cos²θ, what is the minimum value?", "10", ["5", "15", "25"], "Write 10 + 5sin²θ; its minimum occurs at sin²θ=0 and is 10.", 13)
add("EASY", "Find the greatest value of 65 sin²θ + 43 cos²θ.", "65", ["43", "108", "22"], "This is 43 + 22sin²θ; the maximum occurs at sin²θ=1 and equals 65.", 14)
add("EASY", "Find the least value of 65 sin²θ + 43 cos²θ.", "43", ["22", "65", "108"], "This is a weighted average of 65 and 43, so its minimum is 43.", 14)
add("EASY", "What is the maximum of 4sin²θ + 7cos²θ + 5?", "12", ["9", "16", "7"], "Let u=sin²θ∈[0,1]. The expression is 12−3u, whose maximum is 12.", 15)
add("EASY", "What is the minimum of 4sin²θ + 7cos²θ + 5?", "9", ["12", "5", "16"], "The expression is 12−3sin²θ; its minimum is attained at sin²θ=1 and equals 9.", 15)
add("MEDIUM", "The minimum of 4sinθ + 3cosθ over real θ is:", "−5", ["−7", "−1", "5"], "A sinθ+B cosθ ranges from −√(A²+B²) to +√(A²+B²); here √(16+9)=5.", 18)
add("MEDIUM", "The maximum of 7cosθ + 3sinθ over real θ is:", "√58", ["10", "√10", "−√58"], "The maximum is the amplitude √(7²+3²)=√58.", 19)
add("MEDIUM", "Find the difference between maximum and minimum of 15cosθ − 8sinθ + 5.", "34", ["17", "22", "12"], "The sinusoidal amplitude is √(15²+8²)=17; the constant shift cancels, so range width is 34.", 20)
add("MEDIUM", "For x in [0,π/2], the greatest value of 81^(sin x)·27^(cos x) is:", "3⁵", ["3⁴", "3³", "3⁷"], "Rewrite as 3^(4sin x+3cos x). The exponent maximum is √(4²+3²)=5 on this interval.", 21)
add("HARD", "For real x, the maximum of sin x cos x is:", "1/2", ["1", "1/4", "0"], "sin x cos x=½sin2x, whose maximum is ½.", 24)
add("HARD", "For real x, the minimum of sin x cos x is:", "−1/2", ["−1", "0", "1/2"], "sin x cos x=½sin2x, whose minimum is −½.", 24)
add("HARD", "The maximum value of sin⁴θ cos⁴θ is:", "1/16", ["1/256", "1/64", "1/8"], "Let t=sin²θcos²θ≤1/4. Then sin⁴θcos⁴θ=t²≤1/16, attained when sin²θ=cos²θ=1/2.", 25)
add("HARD", "The minimum value of sin⁴θ cos⁴θ is:", "0", ["1/256", "1/16", "1/4"], "At θ=0 (or π/2), one factor is zero; the product is nonnegative, so minimum 0.", 25)
add("HARD", "For positive θ where tanθ is defined, the least value of tan²θ + cot²θ is:", "2", ["1", "4", "0"], "For u=tan²θ>0, u+1/u≥2, with equality u=1.", 31)
add("HARD", "Find the least value of 16tan²θ + 9cot²θ where tanθ≠0.", "24", ["12", "25", "7"], "Set u=tan²θ>0. By AM-GM, 16u+9/u≥2√144=24, attained at u=3/4.", 30)

# Original easy questions: completing squares, weighted averages and AM-GM.
add("EASY", "For real x, the minimum of x² − 8x + 19 is:", "3", ["−3", "4", "19"], "Complete the square: (x−4)²+3, so the minimum is 3.")
add("EASY", "What is the greatest value of −2x² + 12x − 17 for real x?", "1", ["−1", "17", "0"], "The vertex is at x=3; substitution gives −18+36−17=1.")
add("EASY", "The least value of 3x² + 12x + 14 over the reals is:", "2", ["−2", "14", "6"], "3x²+12x+14=3(x+2)²+2, hence the minimum is 2.")
add("EASY", "Find the maximum of −4(x+1)² + 9.", "9", ["5", "−4", "13"], "The squared term is nonnegative, so −4(x+1)²≤0; equality at x=−1.")
add("EASY", "If x>0, the minimum value of 2x + 8/x is:", "8", ["4", "10", "6"], "AM-GM gives 2x+8/x≥2√16=8, with equality at x=2.")
add("EASY", "For positive t, the least value of 5t + 20/t is:", "20", ["10", "25", "15"], "AM-GM gives 5t+20/t≥2√100=20, attained at t=2.")
add("EASY", "The minimum of y² + 10y + 29 for real y equals:", "4", ["−4", "9", "29"], "y²+10y+29=(y+5)²+4.")
add("EASY", "For real u, what is the maximum of −3u² − 6u + 2?", "5", ["2", "−1", "8"], "Rewrite as −3(u+1)²+5; the maximum is 5.")
add("EASY", "Given sin²θ+cos²θ=1, the maximum of 8sin²θ+2cos²θ is:", "8", ["10", "6", "2"], "The expression is 2+6sin²θ, whose maximum is 8.")
add("EASY", "For every real θ, the minimum of 11cos²θ + 6sin²θ is:", "6", ["5", "11", "17"], "This is a weighted average of 11 and 6; it reaches 6 when cosθ=0.")
add("EASY", "What is the minimum value of (3x−2)² + 7?", "7", ["5", "9", "0"], "The square is at least zero and vanishes at x=2/3.")
add("EASY", "For x>0, find the least value of x + 16/x.", "8", ["4", "16", "17"], "AM-GM gives x+16/x≥2√16=8, equality at x=4.")
add("EASY", "The maximum of 6 − (x−5)² for real x is:", "6", ["5", "11", "−6"], "Subtracting a nonnegative square gives a value at most 6, attained at x=5.")
add("EASY", "For real x, the least value of 2x² − 4x + 7 is:", "5", ["3", "7", "−5"], "2x²−4x+7=2(x−1)²+5.")
add("EASY", "For positive a, the minimum of 3a + 12/a is:", "12", ["6", "15", "9"], "AM-GM gives 3a+12/a≥2√36=12, with equality at a=2.")
add("EASY", "Find the greatest value of −(2x+1)² + 4.", "4", ["3", "5", "−1"], "The negative square is at most zero, attained when x=−1/2.")
add("EASY", "The minimum value of x² + 2x + 8 over real x is:", "7", ["6", "8", "9"], "x²+2x+8=(x+1)²+7.")
add("EASY", "For 0≤θ≤π/2, what is the greatest value of 3sin²θ+9cos²θ?", "9", ["12", "6", "3"], "The expression is 3+6cos²θ≤9, with equality at θ=0.")
add("EASY", "If x>0, the least possible value of 7x + 28/x is:", "28", ["14", "35", "21"], "AM-GM yields a lower bound 2√(196)=28, attained at x=2.")
add("EASY", "For real x, the maximum of −5x² + 20x − 16 is:", "4", ["−4", "16", "0"], "The vertex is x=2; the value is −20+40−16=4.")
add("EASY", "What is the minimum of 4(x−3)² − 2?", "−2", ["2", "−6", "0"], "The square is nonnegative and can be zero, so the minimum is −2.")
add("EASY", "For x>0, determine the least value of 9x + 1/x.", "6", ["3", "10", "9"], "By AM-GM, 9x+1/x≥2√9=6, with equality at x=1/3.")
add("EASY", "The minimum of 5x² + 10x + 8 over all real x is:", "3", ["−3", "5", "8"], "5x²+10x+8=5(x+1)²+3.")
add("EASY", "For real θ, the least value of 4sin²θ + 13cos²θ is:", "4", ["9", "13", "17"], "It equals 4+9cos²θ, so the minimum 4 occurs when cosθ=0.")

# Original medium questions: amplitude, products and constrained quadratic forms.
add("MEDIUM", "The range of 5sinθ − 12cosθ, for real θ, is:", "[−13, 13]", "[−12,12] [−17,17] [−5,5]".split(), "The amplitude is √(25+144)=13, so the range is [−13,13].")
add("MEDIUM", "Find the least value of 6x + 24/x for x>0.", "24", ["12", "30", "18"], "AM-GM gives 2√(6·24)=24, with equality at x=2.")
add("MEDIUM", "For x>0, the minimum of 3x + 5/x is:", "2√15", ["√15", "8", "15"], "AM-GM gives 3x+5/x≥2√15; equality when 3x=5/x.")
add("MEDIUM", "If x+y=12 for real x,y, the minimum of x²+y² is:", "72", ["36", "144", "24"], "For fixed sum, x²+y²≥(x+y)²/2=72, equality at x=y=6.")
add("MEDIUM", "For real x,y with x+y=10, what is the least value of 2x²+2y²?", "100", ["50", "200", "20"], "x²+y²≥(x+y)²/2=50; doubling gives the minimum 100 at x=y=5.")
add("MEDIUM", "The minimum value of 4sin²θ + 9cos²θ is:", "4", ["5", "9", "13"], "It is 4+5cos²θ, whose minimum 4 is attained when cosθ=0.")
add("MEDIUM", "The greatest value of 2sinθ + 5cosθ over real θ equals:", "√29", ["7", "√21", "−√29"], "The maximum amplitude is √(2²+5²)=√29.")
add("MEDIUM", "For real θ, what is the minimum of 8cosθ − 15sinθ?", "−17", ["−7", "17", "−15"], "The amplitude is √(64+225)=17, so the minimum is −17.")
add("MEDIUM", "For x>0, find the least value of 10x + 40/x.", "40", ["20", "50", "30"], "AM-GM gives 2√400=40, attained at x=2.")
add("MEDIUM", "Given x−y=8, the minimum of x²+y² over real x,y is:", "32", ["16", "64", "8"], "For fixed difference, the sum of squares is least at x=4,y=−4, giving 32.")
add("MEDIUM", "For real θ, the maximum of 9sin²θ + 4cos²θ is:", "9", ["13", "5", "4"], "Since sin²θ+cos²θ=1, the expression is 4+5sin²θ≤9.")
add("MEDIUM", "The maximum of 12sinθ + 5cosθ over all real θ is:", "13", ["17", "7", "−13"], "Its amplitude is √(12²+5²)=13.")
add("MEDIUM", "Determine the lower bound of 2x + 18/x when x is positive.", "12", ["6", "20", "10"], "AM-GM gives 2√36=12, attained at x=3.")
add("MEDIUM", "If a+b=14, the least possible value of a²+b² is:", "98", ["49", "196", "28"], "a²+b²≥(a+b)²/2=98, equality at a=b=7.")
add("MEDIUM", "For real θ, the range of 9cosθ + 12sinθ is:", "[−15, 15]", ["[−21,21]", "[−12,12]", "[0,15]"], "Amplitude √(81+144)=15, so the range is [−15,15].")
add("MEDIUM", "If x>0, the minimum of 7x + 3/x is:", "2√21", ["√21", "10", "21"], "AM-GM gives 2√(7·3)=2√21, equality when 7x=3/x.")
add("MEDIUM", "For real θ, the least value of 5sin²θ + 11cos²θ is:", "5", ["6", "11", "16"], "The expression is 5+6cos²θ, with minimum 5.")
add("MEDIUM", "For positive x, what is the minimum of 4x + 25/x?", "20", ["10", "29", "15"], "By AM-GM it is at least 2√100=20, attained at x=5/2.")
add("MEDIUM", "With p+q=6, the minimum of 3p²+3q² is:", "54", ["27", "108", "18"], "p²+q²≥36/2=18; multiplying by 3 gives 54.")
add("MEDIUM", "The maximum value of 20sinθ − 21cosθ is:", "29", ["41", "1", "−29"], "The amplitude is √(400+441)=29.")
add("MEDIUM", "For x>0, the least value of 12x + 3/x equals:", "12", ["6", "15", "9"], "AM-GM gives 2√36=12, reached when x=1/2.")
add("MEDIUM", "If u+v=18, determine the smallest value of u²+v².", "162", ["81", "324", "36"], "u²+v²≥(u+v)²/2=162, attained at u=v=9.")
add("MEDIUM", "For real θ, what is the minimum of 7cosθ + 24sinθ?", "−25", ["−17", "25", "−24"], "Amplitude √(49+576)=25; the minimum is −25.")
add("MEDIUM", "Find the greatest value of 3sinθ − 4cosθ for real θ.", "5", ["7", "−5", "1"], "The amplitude is √(9+16)=5.")
add("MEDIUM", "For x>0, the minimum of 5x+45/x is:", "30", ["15", "50", "25"], "AM-GM gives 2√225=30, attained at x=3.")
add("MEDIUM", "For real θ, the least value of 16sin²θ + 25cos²θ equals:", "16", ["9", "25", "41"], "The expression is 16+9cos²θ and reaches 16 at cosθ=0.")

# Original hard questions: domain-sensitive forms and nontrivial identities.
add("HARD", "For x>0, the minimum of (x+4)²/x is:", "16", ["8", "12", "4"], "Expand to x+8+16/x. AM-GM gives x+16/x≥8, hence the minimum 16, at x=4.")
add("HARD", "For x>0, the least value of (x²+9)/x is:", "6", ["3", "9", "12"], "The expression is x+9/x≥2√9=6, attained at x=3.")
add("HARD", "If x+y=8 and x,y are real, the minimum of x²+2y² is:", "128/3", ["32", "64", "16"], "Set y=8−x; differentiating 3x²−32x+128 gives x=16/3,y=8/3 and value 128/3.")
add("HARD", "For x>0, the least value of 2x² + 8/x is:", "6·2^(2/3)", ["6·2^(1/3)", "8", "4·2^(2/3)"], "Differentiate: 4x−8/x²=0 gives x³=2. At this point 8/x=4x², so the minimum is 6x²=6·2^(2/3). The expression tends to infinity at both domain ends.")
add("HARD", "For real θ, the maximum of sinθ+cosθ+sinθcosθ is:", "(1+2√2)/2", ["5/4", "3/2", "2"], "Let u=sinθ+cosθ∈[−√2,√2]; then sc=(u²−1)/2 and the expression is (u²+2u−1)/2. It is convex, so the maximum is at an endpoint; u=√2 gives (1+2√2)/2.")
add("HARD", "For real θ, the minimum of 3sin²θ+4cos²θ−2sinθcosθ is:", "(7−√5)/2", ["1", "(7+√5)/2", "2"], "The quadratic form matrix has eigenvalues (7±√5)/2; the minimum eigenvalue is attained by a unit vector (sinθ,cosθ).")
add("HARD", "For real θ, the minimum of 5sin²θ+5cos²θ+6sinθcosθ is:", "2", ["5", "8", "−1"], "Use sin²+cos²=1 and |sinθcosθ|≤1/2; the minimum is 5−3=2, attained when sinθcosθ=−1/2.")
add("HARD", "For x>0, find the minimum of x² + 4/x² + 4.", "8", ["4", "6", "9"], "Let t=x²>0. t+4/t≥4, so the expression is at least 8, attained at t=2.")
add("HARD", "For real x, the maximum of (2x+3)/(x²+1) is:", "(3+√13)/2", ["3", "2", "√13"], "The symmetric matrix for the numerator is [[0,1],[1,3]] and the denominator is the identity. Its largest eigenvalue solves λ²−3λ−1=0, giving (3+√13)/2.")
add("HARD", "For x>0, what is the least value of (x²+16)/x?", "8", ["4", "16", "12"], "This equals x+16/x≥2√16=8, attained at x=4.")
add("HARD", "Given x+y=5, what is the least possible value of x²+4y²?", "20", ["5", "25/4", "4"], "Cauchy gives (x+y)²≤(1+1/4)(x²+4y²), so x²+4y²≥25/(5/4)=20, attained when x=4y.")
add("HARD", "For real θ, find the maximum of sin²θ+2sinθcosθ+3cos²θ.", "2+√2", ["3", "2−√2", "4"], "The symmetric matrix [[1,1],[1,3]] has eigenvalues 2±√2; the maximum is 2+√2.")
add("HARD", "For real x, determine the minimum of (x²+1)/(x²−2x+2).", "(3−√5)/2", ["1/2", "1", "(3+√5)/2"], "The generalized eigenvalue equation det([[1,0],[0,1]]−λ[[1,−1],[-1,2]])=0 gives λ²−3λ+1=0; the smaller root is (3−√5)/2.")
add("HARD", "For x>0, the smallest value of 3x² + 12/x² is:", "12", ["6", "15", "9"], "Let t=x²>0. 3t+12/t≥2√36=12, equality at t=2.")
add("HARD", "If x,y>0 and xy=16, the least value of x+4y is:", "16", ["8", "20", "12"], "Substitute y=16/x: minimize x+64/x≥2√64=16, attained at x=8,y=2.")
add("HARD", "For real θ, the minimum of 2sin²θ+2cos²θ+3sinθcosθ is:", "1/2", ["2", "−1/2", "3/2"], "The first two terms total 2; since sinθcosθ≥−1/2, the minimum is 2−3/2=1/2.")
add("HARD", "For x>0, find the minimum of (x²+1)(1+1/x²).", "4", ["2", "3", "1"], "Expand to x²+2+1/x²; since x²+1/x²≥2, the minimum is 4 at x=1.")
add("HARD", "For real θ, the maximum of 2sinθcosθ−cos²θ is:", "(√5−1)/2", ["1", "0", "(√5+1)/2"], "This quadratic form has matrix [[0,1],[1,−1]], whose largest eigenvalue solves λ²+λ−1=0, namely (√5−1)/2.")
add("HARD", "For x>0, the least value of (x+1)(x+9)/x is:", "16", ["12", "18", "10"], "Expand to x+10+9/x; AM-GM gives x+9/x≥6, so the minimum is 16 at x=3.")
add("HARD", "For real x, the maximum value of (3x²+2x+1)/(x²+1) is:", "2+√2", ["3", "2−√2", "4"], "The generalized eigenvalues satisfy det([[3−λ,1],[1,1−λ]])=0, or λ²−4λ+2=0; largest is 2+√2.")
add("HARD", "For x,y>0 with x+y=10, the minimum of 1/x+1/y is:", "2/5", ["1/5", "1/2", "4/5"], "1/x+1/y=(x+y)/(xy); xy≤25, hence the minimum is 10/25=2/5 at x=y=5.")
add("HARD", "For positive x, determine the minimum of x² + 9/x.", "3·(9/2)^(2/3)", ["6", "3·∛3", "9/2"], "Differentiate: 2x−9/x²=0 gives x³=9/2. At the stationary point 9/x=2x², so the value is 3x²=3·(9/2)^(2/3); the expression diverges at 0+ and infinity.")
add("HARD", "For real θ, what is the minimum of 4sin²θ+4cos²θ+4sinθcosθ?", "2", ["0", "4", "6"], "The first two terms total 4; since sinθcosθ≥−1/2, the minimum is 4−2=2.")
add("HARD", "For x>0, the minimum of x² + 25/x² is:", "10", ["5", "25", "12"], "Let t=x²>0; t+25/t≥2√25=10, equality at t=5.")


def norm(s):
    return " ".join(unicodedata.normalize("NFKC", s).casefold().split())


def main():
    if len(ROWS) != 90:
        raise SystemExit(f"Builder currently contains {len(ROWS)} questions; expected 90")
    if Counter(r["difficulty"] for r in ROWS) != {"EASY": 30, "MEDIUM": 30, "HARD": 30}:
        raise SystemExit("Difficulty targets are not 30/30/30")
    stems = [norm(r["question_text"]) for r in ROWS]
    if len(set(stems)) != 90 or any(SequenceMatcher(None, a, b).ratio() >= .97 for i, a in enumerate(stems) for b in stems[:i]):
        raise SystemExit("Duplicate or near-duplicate question stems")
    for row, audit in zip(ROWS, AUDIT):
        if row["options"][row["correct_option"]] != audit["expected_answer"] or len(set(row["options"].values())) != 4:
            raise SystemExit(f"Invalid options or answer key: {row['question_text']}")
    BATCH.write_text(json.dumps({"questions": ROWS}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    LEDGER.write_text(json.dumps(AUDIT, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("WROTE", len(ROWS), dict(Counter(r["difficulty"] for r in ROWS)))


if __name__ == "__main__":
    main()
