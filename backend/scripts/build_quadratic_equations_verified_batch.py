"""Build a reviewed SSC Quadratic Equations batch with a worked answer ledger.

Source-derived questions are transcribed from one scanned Physics Wallah
Quadratic Equation lecture deck and independently re-solved. Only legible,
well-posed MCQs with four visible options were retained; title/recap/contents,
concept-only, summary and thank-you pages were excluded. Original SSC-style
questions fill the remaining per-difficulty gaps. PYQ status is not asserted.
"""
from __future__ import annotations

import json
import random
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
ORIGINAL = "Original SSC-style practice question"
QE1 = "Quadratic Equations 01_.pdf"
ROWS = []
LEDGER = []


def src(page):
    return f"{QE1}, PDF page {page}; exam/year not stated per item (PYQ status unverified)"


def add(level, stem, correct, wrongs, proof, source=ORIGINAL):
    correct = str(correct)
    vals = [correct]
    for w in wrongs:
        w = str(w)
        if w not in vals:
            vals.append(w)
    if len(vals) != 4:
        raise ValueError(f"Expected four distinct options for {stem!r}: {vals}")
    random.Random(len(ROWS) * 37 + len(stem)).shuffle(vals)
    key = "ABCD"[vals.index(correct)]
    ROWS.append({
        "subject_slug": "maths", "subcategory_slug": "advanced-maths",
        "chapter_slug": "quadratic-equations", "question_text": stem,
        "options": dict(zip("ABCD", vals)), "correct_option": key,
        "explanation": proof, "difficulty": level, "is_pyq": False,
        "pyq_year": None, "pyq_exam_name": None, "source": source,
    })
    LEDGER.append({
        "row": len(ROWS), "question": stem, "difficulty": level,
        "expected_answer": correct, "independent_reasoning": proof,
        "source": source,
    })


# ─────────────────────────────────────────────────────────────────────────
# SOURCE-DERIVED QUESTIONS (15) — Quadratic Equations 01_.pdf
# ─────────────────────────────────────────────────────────────────────────
add("MEDIUM", "If α and β are the roots of 4x² + 3x + 7 = 0, then the value of 1/α + 1/β is:",
    "−3/7", ["4/7", "3/7", "−3/4"],
    "α+β = −3/4 and αβ = 7/4, so 1/α + 1/β = (α+β)/αβ = (−3/4)/(7/4) = −3/7.",
    src(6))
add("MEDIUM", "If α and β are the roots of x² − x + 1 = 0, then the value of α² + β² is:",
    "−1", ["1", "0", "−2"],
    "α+β = 1 and αβ = 1, so α² + β² = (α+β)² − 2αβ = 1 − 2 = −1.",
    src(7))
add("MEDIUM", "If the equation 2x² − 7x + 12 = 0 has roots α and β, then the value of α/β + β/α is:",
    "1/24", ["97/24", "7/2", "7/24"],
    "α+β = 7/2 and αβ = 6, so α/β + β/α = (α²+β²)/αβ = ((49/4) − 12)/6 = (1/4)/6 = 1/24.",
    src(8))
add("EASY", "One root of the quadratic equation x² − kx + 27 = 0 is 3; find the value of k.",
    "12", ["10", "−12", "16"],
    "Substituting x = 3: 9 − 3k + 27 = 0 ⇒ 36 = 3k ⇒ k = 12.",
    src(9))
add("MEDIUM", "Find k if one root of the equation x² − 9x + k = 0 is twice the other root.",
    "18", ["16", "12", "9"],
    "Roots are m and 2m; sum = 3m = 9 ⇒ m = 3, so k = αβ = 3·6 = 18.",
    src(10))
add("MEDIUM", "Find k so that the sum of the roots of 3x² + (2k + 1)x − k − 5 = 0 equals their product.",
    "4", ["−4", "2", "8"],
    "Sum = −(2k+1)/3 and product = (−k−5)/3; equating gives −(2k+1) = −k−5 ⇒ k = 4.",
    src(11))
add("EASY", "If the sum of the roots of a quadratic equation is 1 and the product of the roots is −20, the equation is:",
    "x² − x − 20 = 0", ["x² + x + 20 = 0", "x² + x − 20 = 0", "x² − x + 20 = 0"],
    "x² − (sum)x + (product) = 0 ⇒ x² − x − 20 = 0.",
    src(13))
add("EASY", "Which of the following quadratic equations has roots −3 and −5?",
    "x² + 8x + 15 = 0", ["x² − 8x + 15 = 0", "x² − 8x − 15 = 0", "x² + 8x − 15 = 0"],
    "Sum = −8 and product = 15, so the equation is x² + 8x + 15 = 0.",
    src(14))
add("MEDIUM", "When (x⁴ − 3x³ + 2x² − 5x + 7) is divided by (x − 2), the remainder is:",
    "−3", ["3", "2", "0"],
    "By the remainder theorem, p(2) = 16 − 24 + 8 − 10 + 7 = −3.",
    src(15))
add("HARD", "When f(x) = 15x³ − 14x² − 4x + 1 is divided by (3x + 2), the remainder is:",
    "−7", ["1", "−2", "2"],
    "Put x = −2/3: f(−2/3) = −40/9 − 56/9 + 8/3 + 1 = (−40 − 56 + 24 + 9)/9 = −63/9 = −7.",
    src(16))
add("EASY", "The roots of the equation x² − 8x + 15 = 0 are:",
    "3, 5", ["2, 3", "8, 15", "6, 5"],
    "x² − 8x + 15 = (x − 3)(x − 5), so the roots are 3 and 5.",
    src(17))
add("MEDIUM", "For what value(s) of k does the quadratic equation 9x² + 3kx + 4 = 0 have equal roots?",
    "±4", ["±2", "±3", "±6"],
    "Equal roots ⇒ b² = 4ac ⇒ 9k² = 4·9·4 = 144 ⇒ k² = 16 ⇒ k = ±4. (The source slide phrases this as the positive value, 4, with options 2/4/3/None.)",
    src(18))
add("MEDIUM", "If the roots of ax² + bx + c = 0 are equal, then c equals:",
    "b²/(4a)", ["b/(2a)", "−b/(2a)", "−b²/(4a)"],
    "Equal roots ⇒ b² = 4ac ⇒ c = b²/(4a).",
    src(19))
add("HARD", "For what values of k does the equation x² + 2(k − 4)x + 2k = 0 have equal roots?",
    "8, 2", ["6, 4", "12, 2", "None of these"],
    "Equal roots ⇒ [2(k−4)]² = 4(1)(2k) ⇒ k² − 8k + 16 = 2k ⇒ k² − 10k + 16 = 0 ⇒ k = 8 or 2.",
    src(20))
add("HARD", "If the product of the roots of x² − (k + 7)x + 2(2k − 2) = 0 is three times their sum, then k equals:",
    "25", ["20", "23", "30"],
    "Sum = k+7 and product = 2(2k−2); 4k − 4 = 3(k+7) ⇒ k = 25.",
    src(21))

# ─────────────────────────────────────────────────────────────────────────
# ORIGINAL SSC-STYLE QUESTIONS (75)
# ─────────────────────────────────────────────────────────────────────────

# EASY originals (26)
easy = [
    ("Solve: x² − 5x + 6 = 0.", "2, 3", ["−2, −3", "1, 6", "−1, −6"],
     "x² − 5x + 6 = (x − 2)(x − 3) = 0 ⇒ x = 2 or 3."),
    ("Find the roots of x² + 7x + 10 = 0.", "−2, −5", ["2, 5", "1, 10", "−1, −10"],
     "x² + 7x + 10 = (x + 2)(x + 5) = 0 ⇒ x = −2 or −5."),
    ("Solve for x: x² − 9 = 0.", "3, −3", ["9, −9", "3, 9", "0, 9"],
     "x² = 9 ⇒ x = 3 or −3."),
    ("Find the roots of the equation x² − 4x = 0.", "0, 4", ["0, −4", "2, 2", "4, −4"],
     "x(x − 4) = 0 ⇒ x = 0 or 4."),
    ("Solve: x² − x − 12 = 0.", "4, −3", ["−4, 3", "6, −2", "12, −1"],
     "x² − x − 12 = (x − 4)(x + 3) = 0 ⇒ x = 4 or −3."),
    ("Find the roots of 2x² − 8 = 0.", "2, −2", ["4, −4", "8, −8", "2, 8"],
     "2x² = 8 ⇒ x² = 4 ⇒ x = 2 or −2."),
    ("Find the sum of the roots of x² − 6x + 5 = 0.", "6", ["5", "−6", "−5"],
     "Sum of roots = −b/a = 6."),
    ("Find the product of the roots of x² + 7x + 12 = 0.", "12", ["7", "−12", "−7"],
     "Product of roots = c/a = 12."),
    ("Find the sum of the roots of 2x² − 7x + 3 = 0.", "7/2", ["−7/2", "3/2", "2/7"],
     "Sum of roots = −b/a = 7/2."),
    ("Find the product of the roots of 3x² + 5x − 2 = 0.", "−2/3", ["2/3", "5/3", "−5/3"],
     "Product of roots = c/a = −2/3."),
    ("The positive root of the equation x² − 49 = 0 is:", "7", ["−7", "49", "24.5"],
     "x² = 49 ⇒ x = 7 or −7, so the positive root is 7."),
    ("Find the discriminant of x² − 4x + 4 = 0.", "0", ["4", "8", "16"],
     "D = b² − 4ac = 16 − 16 = 0."),
    ("The discriminant of the equation x² + 3x + 2 = 0 is:", "1", ["17", "−1", "9"],
     "D = b² − 4ac = 9 − 8 = 1."),
    ("The nature of the roots of x² + 2x + 5 = 0 is:", "No real roots",
     ["Two distinct real roots", "Two equal real roots", "Exactly one real root"],
     "D = 4 − 20 = −16 < 0, so the equation has no real roots."),
    ("For the equation x² − 6x + 9 = 0, the roots are:", "Two equal real roots",
     ["Two distinct real roots", "No real roots", "Zero real roots"],
     "D = 36 − 36 = 0, so the roots are real and equal."),
    ("Form the quadratic equation whose roots are 2 and 3.", "x² − 5x + 6 = 0",
     ["x² + 5x + 6 = 0", "x² − 5x − 6 = 0", "x² + 5x − 6 = 0"],
     "Sum = 5, product = 6 ⇒ x² − 5x + 6 = 0."),
    ("The quadratic equation with roots −1 and 4 is:", "x² − 3x − 4 = 0",
     ["x² + 3x − 4 = 0", "x² − 3x + 4 = 0", "x² + 3x + 4 = 0"],
     "Sum = 3, product = −4 ⇒ x² − 3x − 4 = 0."),
    ("If the sum of the roots is 7 and the product is 12, the quadratic equation is:",
     "x² − 7x + 12 = 0", ["x² + 7x + 12 = 0", "x² − 7x − 12 = 0", "x² + 7x − 12 = 0"],
     "x² − (sum)x + (product) = x² − 7x + 12 = 0."),
    ("The quadratic equation whose roots are 0 and 5 is:", "x² − 5x = 0",
     ["x² + 5x = 0", "x² − 5 = 0", "x² + 5 = 0"],
     "Sum = 5, product = 0 ⇒ x² − 5x + 0 = 0, i.e. x² − 5x = 0."),
    ("If one root of x² + px + 8 = 0 is 2, then p equals:", "−6", ["6", "−4", "4"],
     "Put x = 2: 4 + 2p + 8 = 0 ⇒ 2p = −12 ⇒ p = −6."),
    ("The value of k for which x = 3 is a root of x² − kx + 6 = 0 is:", "5", ["−5", "3", "6"],
     "Put x = 3: 9 − 3k + 6 = 0 ⇒ 3k = 15 ⇒ k = 5."),
    ("Which of the following is a root of x² − 4x − 12 = 0?", "6", ["3", "4", "12"],
     "x² − 4x − 12 = (x − 6)(x + 2), so 6 is a root."),
    ("Solve: (x − 2)(x + 3) = 0.", "2, −3", ["−2, 3", "2, 3", "−2, −3"],
     "A product is zero when a factor is zero ⇒ x = 2 or −3."),
    ("The sum of the roots of x² + 8x + 15 = 0 is:", "−8", ["8", "15", "−15"],
     "Sum of roots = −b/a = −8."),
    ("The product of the roots of x² − 7x + 10 = 0 is:", "10", ["7", "−10", "−7"],
     "Product of roots = c/a = 10."),
    ("The roots of x² − 2x − 15 = 0 are:", "5, −3", ["−5, 3", "3, 5", "−3, −5"],
     "x² − 2x − 15 = (x − 5)(x + 3) = 0 ⇒ x = 5 or −3."),
]

# MEDIUM originals (22)
medium = [
    ("For the equation 2x² − 5x + 3 = 0 with roots α and β, 1/α + 1/β equals:", "5/3",
     ["3/5", "−5/3", "2/3"],
     "α+β = 5/2 and αβ = 3/2, so 1/α + 1/β = (5/2)/(3/2) = 5/3."),
    ("α and β are the roots of x² − 4x + 1 = 0. Find α² + β².", "14", ["16", "12", "10"],
     "α² + β² = (α+β)² − 2αβ = 16 − 2 = 14."),
    ("The roots of x² − 5x + 6 = 0 are α and β; determine (α − β)².", "1", ["25", "24", "0"],
     "(α − β)² = (α+β)² − 4αβ = 25 − 24 = 1."),
    ("If one root of x² − 7x + k = 0 is 2, then k equals:", "10", ["7", "5", "14"],
     "Put x = 2: 4 − 14 + k = 0 ⇒ k = 10."),
    ("If the roots of x² − 5x + k = 0 are in the ratio 2 : 3, then k equals:", "6", ["5", "10", "12"],
     "Roots 2m and 3m give sum 5m = 5 ⇒ m = 1, so k = 2m·3m = 6."),
    ("Find the value of k for which x² − 8x + k = 0 has equal roots.", "16", ["8", "64", "−16"],
     "Equal roots ⇒ 64 − 4k = 0 ⇒ k = 16."),
    ("Find the positive value of k for which 4x² + kx + 9 = 0 has equal roots.", "12",
     ["6", "9", "36"],
     "Equal roots ⇒ k² = 4·4·9 = 144 ⇒ k = ±12, so the positive value is 12."),
    ("If the roots of x² + kx + 9 = 0 are equal, the positive value of k is:", "6", ["3", "9", "18"],
     "Equal roots ⇒ k² = 36 ⇒ k = ±6, so the positive value is 6."),
    ("Determine k such that 2x² + 3x + k = 0 has equal roots.", "9/8", ["8/9", "−9/8", "9/4"],
     "Equal roots ⇒ 9 − 8k = 0 ⇒ k = 9/8."),
    ("The quadratic equation x² − 4x + k = 0 has real roots. The largest integer value of k is:",
     "4", ["3", "5", "16"],
     "Real roots ⇒ 16 − 4k ≥ 0 ⇒ k ≤ 4, so the largest integer is 4."),
    ("The quadratic equation having 1/2 and 1/3 as its roots is:", "6x² − 5x + 1 = 0",
     ["6x² + 5x + 1 = 0", "x² − 5x + 6 = 0", "5x² − 6x + 1 = 0"],
     "Sum = 5/6, product = 1/6 ⇒ x² − (5/6)x + 1/6 = 0 ⇒ 6x² − 5x + 1 = 0."),
    ("If the roots of 2x² − 5x + 3 = 0 are α and β, the equation whose roots are 1/α and 1/β is:",
     "3x² − 5x + 2 = 0", ["3x² + 5x + 2 = 0", "2x² − 5x + 3 = 0", "x² − 5x + 6 = 0"],
     "Roots of the given equation are 3/2 and 1; their reciprocals 2/3 and 1 have sum 5/3 and product 2/3, giving 3x² − 5x + 2 = 0."),
    ("Form the quadratic equation whose roots are the squares of the roots of x² − 5x + 6 = 0.",
     "x² − 13x + 36 = 0", ["x² + 13x + 36 = 0", "x² − 13x − 36 = 0", "x² − 36x + 13 = 0"],
     "Roots 2 and 3 have squares 4 and 9; sum = 13, product = 36 ⇒ x² − 13x + 36 = 0."),
    ("Solve: 2x² − 7x + 3 = 0.", "3, 1/2", ["−3, −1/2", "3, −1/2", "1, 3"],
     "2x² − 7x + 3 = (2x − 1)(x − 3) = 0 ⇒ x = 1/2 or 3."),
    ("Find the roots of 6x² − x − 2 = 0.", "2/3, −1/2", ["−2/3, 1/2", "2, −1/2", "3/2, −2"],
     "6x² − x − 2 = (3x − 2)(2x + 1) = 0 ⇒ x = 2/3 or −1/2."),
    ("Solve for x: 3x² + 10x + 8 = 0.", "−2, −4/3", ["2, 4/3", "−2, 4/3", "−4, −2/3"],
     "3x² + 10x + 8 = (3x + 4)(x + 2) = 0 ⇒ x = −4/3 or −2."),
    ("The product of two consecutive positive integers is 30. The integers are:", "5 and 6",
     ["4 and 5", "6 and 7", "3 and 10"],
     "n(n + 1) = 30 ⇒ n² + n − 30 = 0 ⇒ n = 5, giving 5 and 6."),
    ("The sum of the squares of two consecutive positive integers is 25. The integers are:",
     "3 and 4", ["2 and 3", "4 and 5", "1 and 2"],
     "n² + (n + 1)² = 25 ⇒ 2n² + 2n − 24 = 0 ⇒ n = 3, giving 3 and 4."),
    ("Find the roots of the equation x² − 3x − 10 = 0.", "5, −2", ["−5, 2", "2, 5", "−2, −5"],
     "x² − 3x − 10 = (x − 5)(x + 2) = 0 ⇒ x = 5 or −2."),
    ("The sum of the roots of 2x² − 8x + 6 = 0 is:", "4", ["8", "3", "−4"],
     "Sum of roots = −b/a = 8/2 = 4."),
    ("The roots of 2x² + x − 6 = 0 are:", "3/2, −2", ["−3/2, 2", "3, −2", "2/3, −2"],
     "2x² + x − 6 = (2x − 3)(x + 2) = 0 ⇒ x = 3/2 or −2."),
    ("If one root of x² − 6x + k = 0 is twice the other, then k equals:", "8", ["6", "9", "12"],
     "Roots m and 2m give 3m = 6 ⇒ m = 2, so k = 2m² = 8."),
]

# HARD originals (27)
hard = [
    ("If α and β satisfy x² − 3x + 1 = 0, then α³ + β³ = ?", "18", ["9", "27", "12"],
     "α+β = 3, αβ = 1; α³+β³ = (α+β)³ − 3αβ(α+β) = 27 − 9 = 18."),
    ("The quadratic equation whose roots are 3 + √2 and 3 − √2 is:", "x² − 6x + 7 = 0",
     ["x² + 6x + 7 = 0", "x² − 6x − 7 = 0", "x² − 7x + 6 = 0"],
     "Sum = 6 and product = 9 − 2 = 7, so the equation is x² − 6x + 7 = 0."),
    ("Two numbers differ by 5 and their product is 84. The larger number is:", "12",
     ["7", "14", "9"],
     "n(n − 5) = 84 ⇒ n² − 5n − 84 = 0 ⇒ n = 12, so the larger number is 12."),
    ("Let α and β be the roots of x² − 6x + 4 = 0. Evaluate α/β + β/α.", "7", ["5", "9", "36"],
     "α/β + β/α = (α²+β²)/αβ = (36 − 8)/4 = 28/4 = 7."),
    ("How many real roots does the equation x² − 2x + 2 = 0 have?", "None",
     ["One", "Two", "Three"],
     "D = 4 − 8 = −4 < 0, so there are no real roots."),
    ("If the roots of x² − px + q = 0 differ by 1, then p² − 4q equals:", "1", ["0", "2", "4"],
     "The difference of roots satisfies (α−β)² = p² − 4q; a difference of 1 gives p² − 4q = 1."),
    ("For what value of k does x² − 2(k + 1)x + k² = 0 have equal roots?", "−1/2", ["1/2", "−1", "1"],
     "Equal roots ⇒ 4(k+1)² − 4k² = 0 ⇒ 4(2k + 1) = 0 ⇒ k = −1/2."),
    ("Find the value of m for which 3x² + mx + 12 = 0 has equal roots.", "±12",
     ["±6", "±4", "±24"],
     "Equal roots ⇒ m² = 4·3·12 = 144 ⇒ m = ±12."),
    ("For what values of k does (k − 2)x² + 2(2k − 3)x + (5k − 6) = 0 have equal roots?",
     "1, 3", ["2, 3", "1, 2", "−1, −3"],
     "Setting D = 0 gives (2k−3)² = (k−2)(5k−6) ⇒ k² − 4k + 3 = 0 ⇒ k = 1 or 3."),
    ("If the roots of (b − c)x² + (c − a)x + (a − b) = 0 are equal, then:", "2b = a + c",
     ["2a = b + c", "2c = a + b", "a = b = c"],
     "x = 1 is a root, so equal roots mean a double root at 1, giving sum 2 = −(c−a)/(b−c) ⇒ 2b = a + c."),
    ("A positive number is such that its square diminished by 15 equals twice the number. The number is:",
     "5", ["3", "6", "8"],
     "x² − 15 = 2x ⇒ x² − 2x − 15 = 0 ⇒ x = 5 (positive)."),
    ("The product of a positive number and the number decreased by 4 is 21. The number is:", "7",
     ["3", "9", "11"],
     "x(x − 4) = 21 ⇒ x² − 4x − 21 = 0 ⇒ x = 7 (positive)."),
    ("The length of a rectangle is 3 m more than its breadth and its area is 180 m². The length is:",
     "15 m", ["12 m", "18 m", "20 m"],
     "b(b + 3) = 180 ⇒ b² + 3b − 180 = 0 ⇒ b = 12, so the length is 15 m."),
    ("The sum of the reciprocals of two consecutive even positive integers is 5/12. The smaller integer is:",
     "4", ["2", "6", "8"],
     "1/x + 1/(x+2) = 5/12 ⇒ 12(2x + 2) = 5(x² + 2x) ⇒ 5x² − 14x − 24 = 0 ⇒ x = 4."),
    ("A train travels 360 km at a uniform speed. If its speed were 5 km/h more, it would take 1 hour less. The speed is:",
     "40 km/h", ["36 km/h", "45 km/h", "30 km/h"],
     "360/x − 360/(x+5) = 1 ⇒ x² + 5x − 1800 = 0 ⇒ x = 40."),
    ("α and β being the roots of x² − 2x + 3 = 0, compute α³β + αβ³.", "−6", ["6", "−12", "12"],
     "α³β + αβ³ = αβ(α²+β²) = 3·((4) − 6) = 3·(−2) = −6."),
    ("The sum of the roots of a quadratic equation is 5 and the sum of their squares is 13. The equation is:",
     "x² − 5x + 6 = 0", ["x² + 5x + 6 = 0", "x² − 5x − 6 = 0", "x² − 13x + 5 = 0"],
     "αβ = (25 − 13)/2 = 6, so the equation is x² − 5x + 6 = 0."),
    ("If α and β are the roots of x² − px + 3 = 0 and α − β = 2, then p (p > 0) equals:", "4",
     ["2", "8", "16"],
     "(α−β)² = 4 = p² − 12 ⇒ p² = 16 ⇒ p = 4."),
    ("If one root of x² − 8x + k = 0 is three times the other, then k equals:", "12", ["16", "15", "8"],
     "Roots m and 3m give 4m = 8 ⇒ m = 2, so k = 3m² = 12."),
    ("If the roots of 2x² − 7x + k = 0 are reciprocals of each other, then k equals:", "2",
     ["7", "−2", "1"],
     "Reciprocal roots give product = 1 ⇒ k/2 = 1 ⇒ k = 2."),
    ("Two numbers are in the ratio 3 : 4 and their product is 48. The larger number is:", "8",
     ["6", "12", "4"],
     "The numbers are 3k and 4k; 12k² = 48 ⇒ k² = 4 ⇒ k = 2, so the larger number is 8."),
    ("The product of the digits of a two-digit number is 24 and their sum is 10. The digits are:",
     "4 and 6", ["3 and 8", "2 and 12", "5 and 5"],
     "The digits are roots of t² − 10t + 24 = 0 ⇒ t = 4 and 6."),
    ("A number when added to its square gives 132. The number is:", "11", ["12", "10", "9"],
     "x² + x = 132 ⇒ x² + x − 132 = 0 ⇒ x = 11."),
    ("The age of a man is the square of the age of his son. After 5 years the man will be three times as old as his son. The son's present age is:",
     "5 years", ["4 years", "6 years", "3 years"],
     "x² + 5 = 3(x + 5) ⇒ x² − 3x − 10 = 0 ⇒ x = 5."),
    ("The perimeter of a rectangle is 34 cm and its area is 60 cm². Its length is:", "12 cm",
     ["10 cm", "15 cm", "17 cm"],
     "l + b = 17 and lb = 60 ⇒ t² − 17t + 60 = 0 ⇒ t = 12 or 5, so the length is 12 cm."),
    ("The product of two consecutive odd positive integers is 143. The larger integer is:", "13",
     ["11", "15", "12"],
     "n(n + 2) = 143 ⇒ n² + 2n − 143 = 0 ⇒ n = 11, so the larger is 13."),
    ("For x² − 4x + 2 = 0 whose roots are α and β, find α⁴ + β⁴.", "136", ["144", "128", "120"],
     "α²+β² = 16 − 4 = 12, α²β² = 4; α⁴+β⁴ = 12² − 2·4 = 144 − 8 = 136."),
]

for stem, ans, wrongs, proof in easy:
    add("EASY", stem, ans, wrongs, proof)
for stem, ans, wrongs, proof in medium:
    add("MEDIUM", stem, ans, wrongs, proof)
for stem, ans, wrongs, proof in hard:
    add("HARD", stem, ans, wrongs, proof)


def norm(s):
    return " ".join(unicodedata.normalize("NFKC", s).casefold().split())


def main():
    counts = Counter(r["difficulty"] for r in ROWS)
    if len(ROWS) != 90 or counts != {"EASY": 30, "MEDIUM": 30, "HARD": 30}:
        raise SystemExit(f"bad batch count {len(ROWS)} {counts}")
    for i, r in enumerate(ROWS):
        if len(set(norm(v) for v in r["options"].values())) != 4:
            raise SystemExit(f"option collision row {i+1}: {r['options']}")
        if r["options"][r["correct_option"]] != LEDGER[i]["expected_answer"]:
            raise SystemExit(f"key/ledger mismatch row {i+1}")
    collisions = []
    for i, r in enumerate(ROWS):
        for other in ROWS[:i]:
            a, b = norm(other["question_text"]), norm(r["question_text"])
            ratio = SequenceMatcher(None, a, b).ratio()
            if a == b or ratio >= .95:
                collisions.append((round(ratio, 4), other["question_text"], r["question_text"]))
    if collisions:
        for ratio, a, b in collisions:
            print(f"COLLISION {ratio}\n  A: {a}\n  B: {b}")
        raise SystemExit(f"{len(collisions)} near duplicate pair(s)")
    (BASE / "data/quadratic_equations_verified_batch.json").write_text(
        json.dumps({"questions": ROWS}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (BASE / "data/quadratic_equations_answer_ledger.json").write_text(
        json.dumps(LEDGER, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("WROTE", len(ROWS), dict(counts),
          "source", sum(r["source"] != ORIGINAL for r in ROWS),
          "original", sum(r["source"] == ORIGINAL for r in ROWS))


if __name__ == "__main__":
    main()
