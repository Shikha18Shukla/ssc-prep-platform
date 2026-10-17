"""Build a reviewed SSC Simplification batch with a worked answer ledger.

Source-derived questions are transcribed from two scanned Physics Wallah
Simplification lecture decks and independently re-solved. Only legible,
well-posed MCQs with four visible options were retained; title/contents pages,
recaps, concept-only slides, promo/summary/thank-you pages, worked examples
without options and one ambiguously-notated nested-fraction item were excluded,
and a cross-deck repeat was counted once. Original SSC-style questions fill the
remaining per-difficulty gaps. PYQ status is not asserted for any item.
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
SIM1 = "Simplification 01_.pdf"
SIM2 = "Simplification 02_.pdf"
ROWS = []
LEDGER = []


def src(pdf, page):
    return f"{pdf}, PDF page {page}; exam/year not stated per item (PYQ status unverified)"


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
        "chapter_slug": "simplification", "question_text": stem,
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
# SOURCE-DERIVED QUESTIONS (22) — Simplification 01 / 02 scanned decks
# ─────────────────────────────────────────────────────────────────────────

# --- Simplification 01_.pdf ---
add("HARD", "Find the value of 1 + 1/(1 + 1/(1 + 1/(1 + 1/(1 + 2/3)))).",
    "34/21", ["21/13", "17/2", "8/5"],
    "Evaluating from the inner fraction: 1+2/3 = 5/3 → 3/5 → 8/5 → 5/8 → 13/8 → 8/13 → 21/13 → 13/21 → 34/21.",
    src(SIM1, 5))
add("MEDIUM", "If x = 1 + 1/(1 + 1/(1 + 1/(1 + 1/2))), then the value of 2x + 7/4 is:",
    "5", ["13/8", "4", "7/8"],
    "x = 13/8, so 2x + 7/4 = 13/4 + 7/4 = 20/4 = 5.",
    src(SIM1, 6))
add("HARD", "Find the value of 1 − 1/(1 − 1/(1 − 1/(1 − 2/3))).",
    "1/3", ["2/3", "−1/3", "−2/3"],
    "Evaluating from the inner fraction: 1−2/3 = 1/3 → 3 → −2 → −1/2 → 3/2 → 2/3 → 1/3.",
    src(SIM1, 7))
add("HARD", "If a, b, c and d are integers such that 1/(a + 1/(b + 1/(c + 1/d))) = 29/154, then a + b + c + d = ?",
    "14", ["12", "13", "15"],
    "154/29 = 5 + 9/29 ⇒ a = 5; 29/9 = 3 + 2/9 ⇒ b = 3; 9/2 = 4 + 1/2 ⇒ c = 4 and d = 2; sum = 5+3+4+2 = 14.",
    src(SIM1, 9))
add("MEDIUM", "The value of [ (3 1/5 − 3/5) ÷ 8/5 ] ÷ [ 1 1/7 ÷ { 6/7 − (1/7 ÷ 1/5) } ] is:",
    "13/64", ["13/16", "13/8", "13/7"],
    "Numerator: (16/5 − 3/5) ÷ 8/5 = (13/5)·(5/8) = 13/8. Denominator: (8/7) ÷ (6/7 − 5/7) = (8/7) ÷ (1/7) = 8. Result = (13/8)/8 = 13/64.",
    src(SIM1, 19))
add("MEDIUM", "Simplify: [∛(⁶√(5⁹))]⁴ × [∛(⁶√(5⁹))]⁴",
    "5⁴", ["5²", "5⁸", "5¹²"],
    "∛(⁶√(5⁹)) = 5^(9/6·1/3) = 5^(1/2); each fourth power is 5² and the product is 5⁴.",
    src(SIM1, 12))
add("MEDIUM", "The value of 3/7 ÷ 9/21 + 2 − 4/3 + 1/2 of 12/5 × 25/18 ÷ 5/9 is:",
    "14/3", ["2", "17/3", "4"],
    "3/7 ÷ 9/21 = 1; (1/2 of 12/5) = 6/5; 6/5 × 25/18 ÷ 5/9 = (5/3)·(9/5) = 3; total = 1 + 2 − 4/3 + 3 = 6 − 4/3 = 14/3.",
    src(SIM1, 14))
add("MEDIUM", "What is the value of 90 × 3 ÷ 9 + 4 ÷ 2 × 3 of 4 × 8 ÷ (18 × 2 − 4)?",
    "36", ["48", "40", "42"],
    "(18×2−4) = 32; 3 of 4 = 12; 4÷2×12×8÷32 = 6; 90×3÷9 = 30; total = 30 + 6 = 36.",
    src(SIM1, 15))
add("MEDIUM", "Find the value of 36 ÷ 8 × 4 + 2 ÷ 4 − 1 + 5 of 3 ÷ (4 × 2 − 3) − 3.",
    "35/2", ["18", "16", "31/2"],
    "5 of 3 = 15; (4×2−3) = 5, so 15÷5 = 3; 36÷8×4 = 18 and 2÷4 = 1/2; total = 18 + 1/2 − 1 + 3 − 3 = 35/2.",
    src(SIM1, 16))
add("HARD", "The value of 5 ÷ 5 of 5 × 2 + 2 ÷ 2 of 2 × 5 − (5 − 2) ÷ 6 × 2 is:",
    "19/10", ["9/5", "19", "23/2"],
    "5÷(5 of 5)×2 = 5÷25×2 = 2/5; 2÷(2 of 2)×5 = 2÷4×5 = 5/2; (5−2)÷6×2 = 1; total = 2/5 + 5/2 − 1 = 19/10.",
    src(SIM1, 17))
add("HARD", "The value of 16 ÷ 4 of 4 × [3 ÷ 4 of {4 × 3 ÷ (3 + 3)}] ÷ (2 ÷ 4 of 8) is:",
    "6", ["9", "48", "16"],
    "4 of 4 = 16, so 16÷16 = 1; {4×3÷6} = 2 and 4 of 2 = 8, so 3÷8 = 3/8; 4 of 8 = 32, so 2÷32 = 1/16; total = 1 × 3/8 ÷ 1/16 = 6.",
    src(SIM1, 18))

# --- Simplification 02_.pdf ---
add("EASY", "Find the number of factors of 2³ × 3⁴ × 5⁶.",
    "140", ["120", "125", "130"],
    "Number of factors = (3+1)(4+1)(6+1) = 4·5·7 = 140.",
    src(SIM2, 7))
add("EASY", "Find the number of factors of 720.",
    "30", ["25", "35", "40"],
    "720 = 2⁴·3²·5, so the number of factors is (4+1)(2+1)(1+1) = 5·3·2 = 30.",
    src(SIM2, 8))
add("MEDIUM", "Find the number of even factors of 2³ × 3⁴ × 5⁶.",
    "105", ["104", "110", "115"],
    "An even factor needs at least one 2: 3 choices for the power of 2, then 5 and 7 choices for 3 and 5, giving 3·5·7 = 105.",
    src(SIM2, 16))
add("MEDIUM", "The value of 1/(2×3) + 1/(3×4) + 1/(4×5) + ... + 1/(19×20) is:",
    "9/20", ["3/20", "2/19", "3/19"],
    "Telescoping: (1/2 − 1/3) + (1/3 − 1/4) + ... + (1/19 − 1/20) = 1/2 − 1/20 = 9/20.",
    src(SIM2, 19))
add("HARD", "The value of 1/(2×5) + 1/(5×8) + 1/(8×11) + ... + 1/(23×26) is:",
    "2/13", ["1/11", "3/11", "4/13"],
    "Each term is (1/3)(1/k − 1/(k+3)); the sum telescopes to (1/3)(1/2 − 1/26) = (1/3)(12/26) = 2/13.",
    src(SIM2, 20))
add("MEDIUM", "The value of 1/20 + 1/30 + 1/42 + ... + 1/132 is:",
    "1/6", ["2/5", "3/4", "4/5"],
    "Terms are 1/(4×5) + 1/(5×6) + ... + 1/(11×12) = 1/4 − 1/12 = 2/12 = 1/6.",
    src(SIM2, 22))
add("HARD", "The value of 5/(2²×3²) + 7/(3²×4²) + 9/(4²×5²) + ... + 39/(19²×20²) is:",
    "99/400", ["299/300", "299/200", "399/100"],
    "Each term is 1/k² − 1/(k+1)² for k = 2..19; the sum telescopes to 1/4 − 1/400 = 99/400.",
    src(SIM2, 25))
add("MEDIUM", "Simplify: 1 + 2 + 3 + ... + 99 + 100 + 99 + ... + 2 + 1",
    "10000", ["9990", "9999", "9900"],
    "A symmetric sum up to the middle term n equals n²; here n = 100, so the sum is 100² = 10000.",
    src(SIM2, 26))
add("MEDIUM", "Simplify: √(1 + 2 + 3 + ... + 78 + 79 + 78 + ... + 2 + 1)",
    "79", ["78", "6084", "6241"],
    "The sum equals 79² = 6241, so its square root is 79.",
    src(SIM2, 27))
add("HARD", "Find the number of even factors of 842.",
    "2", ["4", "6", "8"],
    "842 = 2·421; an even factor must contain one factor of 2, and 421 is prime, giving 1·2 = 2 even factors.",
    src(SIM2, 15))
add("MEDIUM", "The value of 1/9 + 1/6 + 1/12 + 1/20 + ... + 1/72 is:",
    "0.5", ["0.33", "0.66", "0.77"],
    "Apart from 1/9 the terms are 1/(2×3)+1/(3×4)+...+1/(8×9) = 1/2 − 1/9; adding 1/9 gives exactly 1/2 = 0.5.",
    src(SIM2, 23))

# ─────────────────────────────────────────────────────────────────────────
# ORIGINAL SSC-STYLE QUESTIONS (68) filling the remaining per-level gaps
# ─────────────────────────────────────────────────────────────────────────

# EASY originals (28)
easy = [
    ("Find the value of 12 + 8 ÷ 4.", "14", ["5", "20", "11"],
     "Division first: 8÷4 = 2, so 12 + 2 = 14."),
    ("Find the value of 15 − 3 × 4.", "3", ["48", "−3", "7"],
     "Multiplication first: 3×4 = 12, so 15 − 12 = 3."),
    ("Find the value of (7 + 5) × 2.", "24", ["19", "14", "26"],
     "Bracket first: 12 × 2 = 24."),
    ("Find the value of 36 ÷ 6 + 5 × 2.", "16", ["17", "22", "6"],
     "36÷6 = 6 and 5×2 = 10, so 6 + 10 = 16."),
    ("What is the value of 1/2 + 1/4?", "3/4", ["2/6", "1/6", "2/8"],
     "1/2 = 2/4, so 2/4 + 1/4 = 3/4."),
    ("What is the value of 2/3 − 1/6?", "1/2", ["1/3", "1/6", "2/9"],
     "2/3 = 4/6, so 4/6 − 1/6 = 3/6 = 1/2."),
    ("What is the value of 3/5 × 10/9?", "2/3", ["30/45", "1/3", "3/2"],
     "(3×10)/(5×9) = 30/45 = 2/3."),
    ("What is the value of 3/4 ÷ 9/8?", "2/3", ["27/32", "3/2", "1/2"],
     "3/4 × 8/9 = 24/36 = 2/3."),
    ("Find the value of 0.5 + 0.25.", "0.75", ["0.30", "0.125", "0.55"],
     "0.50 + 0.25 = 0.75."),
    ("Find the value of 1.2 × 0.5.", "0.6", ["0.06", "6", "1.7"],
     "1.2 × 0.5 = 0.6."),
    ("Find the value of 2³ + 3².", "17", ["13", "25", "36"],
     "2³ = 8 and 3² = 9, so 8 + 9 = 17."),
    ("Find the value of √144 + √81.", "21", ["15", "225", "12"],
     "√144 = 12 and √81 = 9, so 12 + 9 = 21."),
    ("Find the value of 5 + 3 × 2 − 4.", "7", ["12", "4", "16"],
     "3×2 = 6, so 5 + 6 − 4 = 7."),
    ("Find the value of 10 − 2 × 3 + 8 ÷ 4.", "6", ["4", "0", "12"],
     "2×3 = 6 and 8÷4 = 2, so 10 − 6 + 2 = 6."),
    ("Find the value of (12 + 18) ÷ 5.", "6", ["30", "5", "10"],
     "12 + 18 = 30 and 30 ÷ 5 = 6."),
    ("What is the value of 7/8 − 3/8?", "1/2", ["4/16", "1/4", "3/8"],
     "7/8 − 3/8 = 4/8 = 1/2."),
    ("What is the value of 2/5 + 3/10?", "7/10", ["5/15", "1/2", "3/5"],
     "2/5 = 4/10, so 4/10 + 3/10 = 7/10."),
    ("Find the value of 4² − 2³.", "8", ["4", "16", "0"],
     "4² = 16 and 2³ = 8, so 16 − 8 = 8."),
    ("Find the value of 2.5 + 1.75.", "4.25", ["3.25", "4.75", "3.75"],
     "2.50 + 1.75 = 4.25."),
    ("Find the value of 0.6 ÷ 0.2.", "3", ["0.3", "0.03", "12"],
     "0.6 ÷ 0.2 = 3."),
    ("Find the value of 3/4 of 20.", "15", ["60", "5", "12"],
     "3/4 × 20 = 15."),
    ("Find the value of 25% of 80.", "20", ["40", "25", "16"],
     "25% of 80 = 80/4 = 20."),
    ("Find the value of 18 ÷ 3 × 2.", "12", ["3", "27", "6"],
     "18÷3 = 6 and 6 × 2 = 12."),
    ("Find the value of 8 + 2 × (5 − 3).", "12", ["20", "17", "10"],
     "(5−3) = 2, 2×2 = 4, so 8 + 4 = 12."),
    ("What is the value of 1/3 + 1/6 + 1/2?", "1", ["1/2", "3/11", "2/3"],
     "Using sixths: 2/6 + 1/6 + 3/6 = 6/6 = 1."),
    ("Find the value of 9² − 8².", "17", ["1", "81", "145"],
     "9² − 8² = 81 − 64 = 17."),
    ("Find the value of 1.5 × 4 − 2.", "4", ["6", "8", "10"],
     "1.5 × 4 = 6, so 6 − 2 = 4."),
    ("Find the value of 100 ÷ 4 + 6 × 3.", "43", ["48", "25", "39"],
     "100÷4 = 25 and 6×3 = 18, so 25 + 18 = 43."),
]
for stem, ans, wrongs, proof in easy:
    add("EASY", stem, ans, wrongs, proof)

# MEDIUM originals (18)
medium = [
    ("Find the value of 12 ÷ 3 + 4 × 2 − 6.", "6", ["2", "14", "8"],
     "12÷3 = 4 and 4×2 = 8, so 4 + 8 − 6 = 6."),
    ("Find the value of 24 ÷ (8 − 4) × 3.", "18", ["2", "24", "6"],
     "24÷4 = 6 and 6 × 3 = 18."),
    ("What is the value of 2/3 + 3/4 − 5/6?", "7/12", ["1/12", "5/12", "1"],
     "Using twelfths: 8/12 + 9/12 − 10/12 = 7/12."),
    ("What is the value of 5/6 × 3/10 ÷ 1/4?", "1", ["1/4", "4", "1/8"],
     "5/6 × 3/10 = 1/4, and 1/4 ÷ 1/4 = 1."),
    ("Find the value of 0.75 × 1.6.", "1.2", ["0.12", "12", "1.35"],
     "0.75 × 1.6 = 1.2."),
    ("Find the value of √2.25.", "1.5", ["1.25", "0.15", "15"],
     "1.5 × 1.5 = 2.25, so √2.25 = 1.5."),
    ("Find the value of 40% of 250.", "100", ["62.5", "10", "625"],
     "40% of 250 = 0.4 × 250 = 100."),
    ("Find the value of 15% of 480 + 25% of 240.", "132", ["120", "168", "144"],
     "15% of 480 = 72 and 25% of 240 = 60, so the sum is 132."),
    ("Find the value of 3⁴ ÷ 3² × 3.", "27", ["9", "3", "81"],
     "3⁴÷3² = 9 and 9 × 3 = 27."),
    ("Find the value of (0.2)³.", "0.008", ["0.6", "0.08", "0.0008"],
     "0.2 × 0.2 × 0.2 = 0.008."),
    ("What is the value of 5/8 ÷ 15/16?", "2/3", ["3/2", "75/128", "1/2"],
     "5/8 × 16/15 = 80/120 = 2/3."),
    ("What is the value of 7/12 + 5/18 − 1/4?", "11/18", ["1/2", "13/18", "5/9"],
     "Using thirty-sixths: 21/36 + 10/36 − 9/36 = 22/36 = 11/18."),
    ("Find the value of 1.25 × 0.8 + 0.2.", "1.2", ["1.0", "1.25", "0.3"],
     "1.25 × 0.8 = 1.0, so 1.0 + 0.2 = 1.2."),
    ("Find the value of 16 ÷ 4 + 3 × (7 − 5)².", "16", ["22", "28", "10"],
     "(7−5)² = 4 and 3×4 = 12, so 16÷4 + 12 = 4 + 12 = 16."),
    ("What is the value of (3/7) × (14/9) ÷ (2/3)?", "1", ["2/3", "3/2", "1/3"],
     "3/7 × 14/9 = 2/3, and 2/3 ÷ 2/3 = 1."),
    ("Find the value of √1296.", "36", ["24", "32", "1296"],
     "36 × 36 = 1296, so √1296 = 36."),
    ("Find the value of 20% of 15% of 400.", "12", ["60", "1.2", "120"],
     "15% of 400 = 60 and 20% of 60 = 12."),
    ("Find the value of 3/4 of 1/2 + 1/8.", "1/2", ["3/8", "5/8", "7/8"],
     "3/4 × 1/2 = 3/8 and 3/8 + 1/8 = 4/8 = 1/2."),
]
for stem, ans, wrongs, proof in medium:
    add("MEDIUM", stem, ans, wrongs, proof)

# HARD originals (22)
hard = [
    ("The value of 1/(1×2) + 1/(2×3) + ... + 1/(9×10) is:", "9/10", ["10/11", "1/90", "9/100"],
     "Telescoping: (1 − 1/2) + (1/2 − 1/3) + ... + (1/9 − 1/10) = 1 − 1/10 = 9/10."),
    ("The value of 1/(1×3) + 1/(3×5) + 1/(5×7) + 1/(7×9) is:", "4/9", ["1/9", "8/9", "1/3"],
     "Each term is (1/2)(1/k − 1/(k+2)); the sum is (1/2)(1 − 1/9) = (1/2)(8/9) = 4/9."),
    ("The value of 1/(2×4) + 1/(4×6) + 1/(6×8) + 1/(8×10) is:", "1/5", ["1/10", "2/5", "1/4"],
     "Each term is (1/2)(1/k − 1/(k+2)); the sum is (1/2)(1/2 − 1/10) = (1/2)(2/5) = 1/5."),
    ("The value of 1/6 + 1/12 + 1/20 + 1/30 is:", "1/3", ["1/2", "2/25", "1/4"],
     "Terms are 1/(2×3)+1/(3×4)+1/(4×5)+1/(5×6) = 1/2 − 1/6 = 1/3."),
    ("The value of 1 + 1/(2 + 1/(3 + 1/4)) is:", "43/30", ["30/43", "7/4", "4/3"],
     "Inner: 3+1/4 = 13/4 → 4/13 → 2+4/13 = 30/13 → 13/30 → 1 + 13/30 = 43/30."),
    ("The value of (3/8 + 5/12) ÷ (7/8 − 3/4) is:", "19/3", ["3/19", "19/24", "1/8"],
     "(9/24 + 10/24) = 19/24 and (7/8 − 3/4) = 1/8, so 19/24 × 8 = 19/3."),
    ("The value of [(0.9)² − (0.8)²] ÷ (0.9 − 0.8) is:", "1.7", ["0.17", "17", "0.017"],
     "(0.81 − 0.64) ÷ 0.1 = 0.17 ÷ 0.1 = 1.7."),
    ("The value of √0.0004 + ³√0.008 is:", "0.22", ["0.06", "0.42", "0.6"],
     "√0.0004 = 0.02 and ³√0.008 = 0.2, so the sum is 0.22."),
    ("The value of √1.44 × ³√0.027 is:", "0.36", ["0.036", "3.6", "0.12"],
     "√1.44 = 1.2 and ³√0.027 = 0.3, so the product is 0.36."),
    ("The value of (³√8 + ⁴√16) × √25 is:", "20", ["10", "14", "40"],
     "³√8 = 2, ⁴√16 = 2 and √25 = 5, so (2 + 2) × 5 = 20."),
    ("The value of (√2)⁴ × (³√2)⁶ is:", "16", ["4", "8", "32"],
     "(√2)⁴ = 2² = 4 and (³√2)⁶ = 2² = 4, so the product is 16."),
    ("Simplify: √12 × √27.", "18", ["9", "324", "39"],
     "√12 × √27 = √324 = 18."),
    ("Simplify: (√5 + √3)(√5 − √3).", "2", ["8", "15", "√2"],
     "Using (a+b)(a−b) = a²−b²: 5 − 3 = 2."),
    ("Find the total number of factors of 360.", "24", ["12", "18", "36"],
     "360 = 2³·3²·5, so the number of factors is 4·3·2 = 24."),
    ("Find the number of prime factors in 12³ (counting repetition).", "9", ["6", "3", "12"],
     "12³ = (2²·3)³ = 2⁶·3³, so the number of prime factors is 6 + 3 = 9."),
    ("Simplify: (√7 + √3)² − 2√21.", "10", ["4", "14", "2√21"],
     "Expanding: (√7)² + (√3)² + 2√21 − 2√21 = 7 + 3 = 10."),
    ("Simplify: (16/81)^(3/4).", "8/27", ["27/8", "2/3", "64/729"],
     "16^(3/4) = 8 and 81^(3/4) = 27, so the value is 8/27."),
    ("Simplify: √(7 + 4√3) + √(7 − 4√3).", "4", ["2√3", "4√3", "7"],
     "7 + 4√3 = (2 + √3)² and 7 − 4√3 = (2 − √3)², so the sum is (2 + √3) + (2 − √3) = 4."),
    ("Simplify: 2/3 of 3/4 of 4/5 of 100.", "40", ["50", "80", "45"],
     "(2/3)(3/4) = 1/2, (1/2)(4/5) = 2/5 and (2/5)(100) = 40."),
    ("Simplify: (1/2 + 1/3) ÷ (1/2 − 1/3).", "5", ["1", "1/5", "5/6"],
     "(5/6) ÷ (1/6) = 5."),
    ("Simplify: 0.008 × 0.5 ÷ 0.002.", "2", ["0.2", "20", "0.02"],
     "0.008 × 0.5 = 0.004 and 0.004 ÷ 0.002 = 2."),
    ("Simplify: 5² × 5³ ÷ 5⁴.", "5", ["25", "125", "1"],
     "5² × 5³ = 5⁵ and 5⁵ ÷ 5⁴ = 5."),
]
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
    (BASE / "data/simplification_verified_batch.json").write_text(
        json.dumps({"questions": ROWS}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (BASE / "data/simplification_answer_ledger.json").write_text(
        json.dumps(LEDGER, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("WROTE", len(ROWS), dict(counts),
          "source", sum(r["source"] != ORIGINAL for r in ROWS),
          "original", sum(r["source"] == ORIGINAL for r in ROWS))


if __name__ == "__main__":
    main()
