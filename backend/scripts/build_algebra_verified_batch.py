"""Build a reviewed SSC Algebra batch with a calculation/reasoning ledger.

Source-derived questions are transcribed from five scanned Physics Wallah
Algebra lecture decks and independently re-solved. Only legible, well-posed
MCQs with four visible options were retained; short-answer drills, concept
slides, titles/recaps and summary pages were excluded. Original SSC-style
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
        "chapter_slug": "algebra", "question_text": stem,
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
# SOURCE-DERIVED QUESTIONS (49) — Algebra 02 / 03 / 05 / 06 / 07 scanned decks
# ─────────────────────────────────────────────────────────────────────────

# --- Algebra 02_ (Lecture 2: x + 1/x powers) ---
add("MEDIUM", "If 3y − 3/y = 5, find the value of y² + 1/y².", "43/9",
    ["47/9", "49/9", "41/9"],
    "3(y−1/y)=5 so y−1/y=5/3; y²+1/y²=(5/3)²+2=25/9+18/9=43/9.",
    src("Algebra 02_.pdf", 9))
add("MEDIUM", "If √x − 1/√x = √6, then x² + 1/x² is equal to:", "62",
    ["40", "54", "66"],
    "Squaring: x+1/x−2=6 so x+1/x=8; x²+1/x²=64−2=62.",
    src("Algebra 02_.pdf", 10))
add("HARD", "If x² + 3x + 1 = 0, then the value of x⁶ + 1/x⁶ is:", "322",
    ["324", "318", "327"],
    "Divide by x: x+1/x=−3; x²+1/x²=9−2=7; x³+1/x³=(−3)³−3(−3)=−18; x⁶+1/x⁶=(−18)²−2=322.",
    src("Algebra 02_.pdf", 11))
add("MEDIUM", "If 5x + 1/(3x) = 5, find the value of 9x² + 1/(25x²).", "7.8",
    ["0", "5", "4"],
    "3x+1/(5x)=3; 9x²+1/(25x²)=(3x+1/(5x))²−2·3x·1/(5x)=9−6/5=7.8.",
    src("Algebra 02_.pdf", 13))
add("HARD", "If x + 1/x = 5, find the value of x⁵ + 1/x⁵.", "2525",
    ["2530", "2125", "2150"],
    "x²+1/x²=23, x³+1/x³=110; x⁵+1/x⁵=(x²+1/x²)(x³+1/x³)−(x+1/x)=23·110−5=2525.",
    src("Algebra 02_.pdf", 14))
add("HARD", "If x + 1/x = 3, then the value of x⁷ + 1/x⁷ is:", "843",
    ["846", "845", "850"],
    "x²+1/x²=7, x³+1/x³=18, x⁴+1/x⁴=47; x⁷+1/x⁷=(x⁴+1/x⁴)(x³+1/x³)−(x+1/x)=47·18−3=843.",
    src("Algebra 02_.pdf", 15))

# --- Algebra 03_ (Lecture 3: symmetric rational expressions) ---
add("HARD", "If x² − 5x + 1 = 0, then the value of (x⁶ + x⁴ + x² + 1)/(5x³) is:", "23",
    ["30", "25", "28"],
    "x+1/x=5; x³+1/x³=125−15=110; (x⁶+x⁴+x²+1)/(5x³)=(1/5)(x³+x+1/x+1/x³)=(1/5)(110+5)=23.",
    src("Algebra 03_.pdf", 4))
add("HARD", "If x + 1/x = 5, x ≠ 0, then the value of (x⁴ + 1/x²)/(x² − 3x + 1) is:", "55",
    ["60", "65", "50"],
    "Divide numerator and denominator by x: (x³+1/x³)/(x−3+1/x)=110/(5−3)=110/2=55.",
    src("Algebra 03_.pdf", 5))
add("HARD", "If x − 1/x = 5, x ≠ 0, then the value of (x⁶ + 3x³ − 1)/(x⁶ − 8x³ − 1) is:", "13/12",
    ["11/13", "3/8", "4/9"],
    "Divide by x³: (x³+3−1/x³)/(x³−8−1/x³). x³−1/x³=5³+3·5=140; (140+3)/(140−8)=143/132=13/12.",
    src("Algebra 03_.pdf", 6))
add("HARD", "If x + 1/x = 5 then the value of (x⁴ + 3x³ + 5x² + 3x + 1)/(x⁴ + 1) is:", "43/23",
    ["47/21", "41/23", "45/21"],
    "Divide by x²: (x²+1/x²+3(x+1/x)+5)/(x²+1/x²)=(23+15+5)/23=43/23.",
    src("Algebra 03_.pdf", 7))
add("HARD", "If x² − 3x + 1 = 0, then the value of (x⁴ + 1/x²)/(x² + 5x + 1) is:", "9/4",
    ["27/8", "5/2", "2"],
    "x+1/x=3; divide by x: (x³+1/x³)/(x+5+1/x)=18/8=9/4.",
    src("Algebra 03_.pdf", 8))
add("HARD", "If x + 1/x = 8, then the value of x³ − 1/x³ is:", "63√60",
    ["60√63", "57√63", "60√57"],
    "x−1/x=√(64−4)=√60; x³−1/x³=(x−1/x)³+3(x−1/x)=60√60+3√60=63√60.",
    src("Algebra 03_.pdf", 9))
add("MEDIUM", "If (x + 1/x)² = 3, then the value of x³ + 1/x³ is:", "0",
    ["2√3", "2", "3√3"],
    "x+1/x=√3; x³+1/x³=(√3)³−3√3=3√3−3√3=0.",
    src("Algebra 03_.pdf", 12))
add("HARD", "If x + 1/x = √3, then the value of x¹³ + x¹⁹ + x¹⁰⁰ + x⁹⁴ is:", "0",
    ["1", "−1", "2"],
    "x⁶=−1, so x⁶ᵏ=−1. x¹³+x¹⁹=x¹³(1+x⁶)=0 and x¹⁰⁰+x⁹⁴=x⁹⁴(x⁶+1)=0; total 0.",
    src("Algebra 03_.pdf", 13))
add("HARD", "If (a + 1/a)² = 3, then the value of a³⁰ + a²⁴ + a¹⁸ + a¹² + a⁶ + 1 is:", "0",
    ["27", "1", "−1"],
    "a⁶=−1. Group: a²⁴(a⁶+1)+a¹²(a⁶+1)+(a⁶+1)=0.",
    src("Algebra 03_.pdf", 14))

# --- _Algebra 05_ (Lecture 5: perfect squares & sum of squares) ---
add("MEDIUM", "If m + 1/(m − 3) = 5, then (m − 3)⁸ + 1/(m − 3)⁸ is:", "2",
    ["0", "−2", "15"],
    "(m−3)+1/(m−3)=5−3=2; if t+1/t=2 then t=1, so t⁸+1/t⁸=2.",
    src("_Algebra 05_.pdf", 7))
add("MEDIUM", "If x + 1/(x + 1) = 1, then (x + 1)⁵ + 1/(x + 1)⁵ is:", "2",
    ["1", "4", "8"],
    "(x+1)+1/(x+1)=1+1=2; t+1/t=2 ⇒ t=1, so t⁵+1/t⁵=2.",
    src("_Algebra 05_.pdf", 8))
add("HARD", "If x + 1/(x − 9) = 11, then (x − 11)¹² + 1/(x − 11)¹³ is:", "0",
    ["2", "−2", "1"],
    "(x−9)+1/(x−9)=11−9=2 ⇒ x=10; (x−11)¹²+1/(x−11)¹³=(−1)¹²+1/(−1)¹³=1−1=0.",
    src("_Algebra 05_.pdf", 9))
add("EASY", "If (a − 3)² + (b − 4)² + (c − 9)² = 0, then √(a + b + c) is:", "4",
    ["−4", "±4", "±2"],
    "Each square is 0: a=3, b=4, c=9; √(3+4+9)=√16=4.",
    src("_Algebra 05_.pdf", 10))
add("EASY", "If (a − 1)² + (b + 2)² + (c + 1)² = 0, then 2a − 3b + 7c equals:", "1",
    ["12", "−11", "3"],
    "a=1, b=−2, c=−1; 2(1)−3(−2)+7(−1)=2+6−7=1.",
    src("_Algebra 05_.pdf", 12))
add("EASY", "If (a − 4)² + (b − 5)² + (c − 3)² = 0, then (a + b)/c is:", "3",
    ["0", "1", "−3"],
    "a=4, b=5, c=3; (4+5)/3=3.",
    src("_Algebra 05_.pdf", 13))
add("MEDIUM", "If a² + b² + c² = 2(a − b − c) − 3, then 4a − 3b + 5c is:", "2",
    ["3", "5", "6"],
    "Rearrange: (a−1)²+(b+1)²+(c+1)²=0 ⇒ a=1, b=−1, c=−1; 4(1)−3(−1)+5(−1)=2.",
    src("_Algebra 05_.pdf", 14))
add("HARD", "If a² + b² + c² + 84 = 4(a − 2b + 4c), then √(ab − bc + ca) is:", "2√10",
    ["4√10", "√10", "5√10"],
    "(a−2)²+(b+4)²+(c−8)²=0 ⇒ a=2, b=−4, c=8; ab−bc+ca=−8+32+16=40; √40=2√10.",
    src("_Algebra 05_.pdf", 16))
add("HARD", "If a² + b² + 49c² + 18 = 2(b − 28c − a), then (a + b − 7c) is:", "4",
    ["3", "2", "1"],
    "(a+1)²+(b−1)²+(7c+4)²=0 ⇒ a=−1, b=1, c=−4/7; a+b−7c=−1+1+4=4.",
    src("_Algebra 05_.pdf", 17))
add("MEDIUM", "If a + b + c = 16 and a² + b² + c² = 90, find ab + bc + ca.", "83",
    ["84", "82", "81"],
    "(a+b+c)²=a²+b²+c²+2(ab+bc+ca); 256=90+2S ⇒ S=83.",
    src("_Algebra 05_.pdf", 19))
add("MEDIUM", "If a + b − c = 5 and ab − bc − ca = 10, then a² + b² + c² is:", "5",
    ["15", "45", "40"],
    "(a+b−c)²=a²+b²+c²+2(ab−bc−ca); 25=a²+b²+c²+20 ⇒ a²+b²+c²=5.",
    src("_Algebra 05_.pdf", 20))
add("MEDIUM", "If a² + b² + c² = 6.25 and ab + bc + ca = 0.52, find (a + b + c) if (a + b + c) < 0.", "−2.7",
    ["±2.7", "−2.8", "±2.8"],
    "(a+b+c)²=6.25+2(0.52)=7.29, so a+b+c=±2.7; with a+b+c<0 the value is −2.7.",
    src("_Algebra 05_.pdf", 21))

# --- _Algebra 06_ (Lecture 6: special products) ---
add("MEDIUM", "If a⁴ + a²b² + b⁴ = 8 and a² + ab + b² = 4, then the value of ab is:", "1",
    ["−1", "0", "2"],
    "(a²+ab+b²)(a²−ab+b²)=a⁴+a²b²+b⁴; 4(a²−ab+b²)=8 ⇒ a²−ab+b²=2. Subtract: 2ab=4−2=2 ⇒ ab=1.",
    src("_Algebra 06_.pdf", 5))
add("HARD", "If x + y = ±√(7 + xy) and x − y = ±√(3 − xy), find x⁴ + x²y² + y⁴.", "21",
    ["58", "441", "10"],
    "(x+y)²=7+xy ⇒ x²+y²+xy=7; (x−y)²=3−xy ⇒ x²+y²−xy=3. Product (x²+y²+xy)(x²+y²−xy)=x⁴+x²y²+y⁴=7·3=21.",
    src("_Algebra 06_.pdf", 6))
add("HARD", "If x⁴ + y⁴ + x²y² = 21 and x² + y² − xy = 7, then x/y + y/x is:", "−5/2",
    ["3/4", "−3/2", "5/4"],
    "(x²+y²+xy)(x²+y²−xy)=21 ⇒ x²+y²+xy=3; with x²+y²−xy=7 ⇒ xy=−2, x²+y²=5; x/y+y/x=(x²+y²)/(xy)=5/(−2)=−5/2.",
    src("_Algebra 06_.pdf", 7))
add("MEDIUM", "If 8x³ − 27y³ = (Ax + By)(Cx² − Dy² + 6xy), then (A + B + C − D) is:", "12",
    ["−12", "9", "15"],
    "8x³−27y³=(2x−3y)(4x²+6xy+9y²); A=2, B=−3, C=4, D=−9; A+B+C−D=2−3+4+9=12.",
    src("_Algebra 06_.pdf", 8))
add("HARD", "If (x − a)(x − b) = 1 and a − b + 5 = 0, then (x − a)³ − 1/(x − a)³ is:", "140",
    ["−125", "1", "125"],
    "x−b=1/(x−a) and (x−a)−(x−b)=b−a=5, so (x−a)−1/(x−a)=5; cube: 5³+3·5=140.",
    src("_Algebra 06_.pdf", 9))
add("EASY", "Simplify (x − y + z)² − (x − y − z)².", "4xz − 4yz",
    ["2xz + 2yz", "4yz − 4xz", "4xz + 4yz"],
    "Let a=x−y. (a+z)²−(a−z)²=4az=4(x−y)z=4xz−4yz.",
    src("_Algebra 06_.pdf", 10))
add("MEDIUM", "If (2a + 3/a − 1) = 11, what is the value of (4a² + 9/a² − 1)?", "131",
    ["110", "132", "121"],
    "2a+3/a=12; 4a²+9/a²=(2a+3/a)²−2·2a·(3/a)=144−12=132; minus 1 gives 131.",
    src("_Algebra 06_.pdf", 11))
add("MEDIUM", "If 16x² + y² = 48 and xy = 2 with x, y > 0, then (64x³ + y³) is:", "320",
    ["340", "300", "240"],
    "(4x+y)²=48+16=64 ⇒ 4x+y=8; 64x³+y³=(4x+y)³−3(4x)(y)(4x+y)=512−12·2·8=320.",
    src("_Algebra 06_.pdf", 12))
add("HARD", "If 1/(x + 1/(y + 1/z)) = 67/16, then the value of xy + z is:", "23",
    ["20", "21", "22"],
    "67/16=4+3/16 ⇒ x=4; y+1/z=16/3=5+1/3 ⇒ y=5, z=3; xy+z=20+3=23.",
    src("_Algebra 06_.pdf", 13))
add("HARD", "If 13/37 = 1/(x + 1/(y + 1/z)), find the values of x, y, z respectively.", "2, 1, 11/2",
    ["11/2, 1, 2", "11/2, 2, 1", "2, 11/2, 1"],
    "37/13=2+11/13 ⇒ x=2; 13/11=1+2/11 ⇒ y=1, z=11/2.",
    src("_Algebra 06_.pdf", 14))
add("MEDIUM", "If (11 − 13x)/x + (11 − 13y)/y + (11 − 13z)/z = 5, then 1/x + 1/y + 1/z is:", "4",
    ["5", "13/11", "13/5"],
    "Each term = 11/x − 13. Sum = 11(1/x+1/y+1/z) − 39 = 5 ⇒ 11S=44 ⇒ S=4.",
    src("_Algebra 06_.pdf", 15))
add("HARD", "If x + 4√3/x = 5, then (x² + 7x + 4√3)/(x²(5 − x)) is:", "√3",
    ["2√3", "3√3", "2"],
    "x²+4√3=5x ⇒ 5x−x²=4√3. Numerator x²+7x+4√3=x²+7x+5x−x²=12x; denominator x²(5−x)=x²·4√3/x=4√3x; ratio=12x/(4√3x)=3/√3=√3.",
    src("_Algebra 06_.pdf", 16))

# --- _Algebra 07_ (Lecture 7: a³ + b³ + c³ − 3abc) ---
add("HARD", "If a = 7 + 4√3 and b = 7 − 4√3, then 1/(a⁵ + 1) + 1/(b⁵ + 1) is:", "1",
    ["4", "3", "7"],
    "ab=49−48=1 ⇒ b=1/a; 1/(a⁵+1)+a⁵/(1+a⁵)=(1+a⁵)/(1+a⁵)=1.",
    src("_Algebra 07_.pdf", 4))
add("HARD", "If x = √(19 + √13)/√(19 − √13) and y = √(19 − √13)/√(19 + √13), then 1/(x³ + 1) + 1/(y³ + 1) is:", "1",
    ["8", "4", "2"],
    "xy=1 ⇒ y=1/x; 1/(x³+1)+x³/(1+x³)=(1+x³)/(1+x³)=1.",
    src("_Algebra 07_.pdf", 5))
add("EASY", "If xᵃ · xᵇ · xᶜ = 1, then the value of a³ + b³ + c³ is:", "3abc",
    ["9", "abc", "a + b + c"],
    "x^(a+b+c)=1 ⇒ a+b+c=0 (for x≠1); then a³+b³+c³=3abc.",
    src("_Algebra 07_.pdf", 8))
add("MEDIUM", "If a = 25, b = 15, c = −10, then the value of (a³ + b³ + c³ − 3abc)/((a − b)² + (b − c)² + (c − a)²) is:", "15",
    ["30", "−15", "−30"],
    "Numerator=(a+b+c)(a²+b²+c²−ab−bc−ca); denominator=2(a²+b²+c²−ab−bc−ca); ratio=(a+b+c)/2=(25+15−10)/2=15.",
    src("_Algebra 07_.pdf", 9))
add("MEDIUM", "If a + b + c = 6, a² + b² + c² = 14 and a³ + b³ + c³ = 36, then the value of abc is:", "6",
    ["3", "9", "12"],
    "a³+b³+c³−3abc=(1/2)(a+b+c)[3(a²+b²+c²)−(a+b+c)²]=(1/2)(6)(42−36)=18; 36−3abc=18 ⇒ abc=6.",
    src("_Algebra 07_.pdf", 10))
add("MEDIUM", "If x = y = 333 and z = 334, then x³ + y³ + z³ − 3xyz is:", "1000",
    ["0", "667", "2334"],
    "=(1/2)(x+y+z)[(x−y)²+(y−z)²+(z−x)²]=(1/2)(1000)(0+1+1)=1000.",
    src("_Algebra 07_.pdf", 11))
add("HARD", "The value of [(1.2)³ + (0.8)³ + (0.7)³ − 2.016] / {(1.35)[(1.2)² + (0.8)² + (0.7)² − 0.96 − 0.84 − 0.56]} is:", "2",
    ["1/4", "1/2", "1"],
    "Numerator=a³+b³+c³−3abc with a=1.2, b=0.8, c=0.7 (3abc=2.016), so =(a+b+c)(a²+b²+c²−ab−bc−ca)=2.7·D; denominator=1.35·D; ratio=2.7/1.35=2.",
    src("_Algebra 07_.pdf", 12))
add("MEDIUM", "If x + y + z = 2 and xy + yz + zx = −11, then x³ + y³ + z³ − 3xyz is:", "74",
    ["78", "69", "71"],
    "=(x+y+z)[(x+y+z)²−3(xy+yz+zx)]=2[4−3(−11)]=2·37=74.",
    src("_Algebra 07_.pdf", 13))
add("HARD", "If (x + 6)³ + (2x + 3)³ + (3x + 5)³ = (3x + 18)(2x + 3)(3x + 5), then the value of x is:", "−7/3",
    ["7/3", "−5/3", "5/3"],
    "RHS=3(x+6)(2x+3)(3x+5), so a³+b³+c³=3abc ⇒ a+b+c=0; (x+6)+(2x+3)+(3x+5)=0 ⇒ 6x+14=0 ⇒ x=−7/3.",
    src("_Algebra 07_.pdf", 14))
add("HARD", "If x + y + z = 7, x² + y² + z² = 85 and x³ + y³ + z³ = 913, then the value of ∛(xyz) is:", "4",
    ["2", "1", "8"],
    "x³+y³+z³−3xyz=(1/2)(x+y+z)[3(x²+y²+z²)−(x+y+z)²]=(1/2)(7)(255−49)=721; 913−3xyz=721 ⇒ xyz=64; ∛64=4.",
    src("_Algebra 07_.pdf", 15))

# ─────────────────────────────────────────────────────────────────────────
# ORIGINAL SSC-STYLE QUESTIONS (41) filling the remaining per-level gaps
# ─────────────────────────────────────────────────────────────────────────

# EASY originals (25) — deliberately varied wording so no two stems collide.
easy = [
    ("If x + 1/x = 2, find x² + 1/x².", "2", ["0", "4", "6"],
     "x²+1/x²=(x+1/x)²−2=4−2=2."),
    ("The sum of two numbers is 10, and their product is 21. Find the sum of their squares.", "58", ["100", "42", "79"],
     "a²+b²=(a+b)²−2ab=100−42=58."),
    ("Two numbers differ by 4, and their product is 12. Find the sum of their squares.", "40", ["16", "24", "28"],
     "a²+b²=(a−b)²+2ab=16+24=40."),
    ("If a + b = 12 and a − b = 4, evaluate a² − b².", "48", ["96", "56", "144"],
     "a²−b²=(a+b)(a−b)=12·4=48."),
    ("Given x − 1/x = 3, compute x² + 1/x².", "11", ["9", "7", "13"],
     "x²+1/x²=(x−1/x)²+2=9+2=11."),
    ("Three numbers add to zero, and the sum of their pairwise products is −5. Find the sum of their squares.", "10", ["−10", "5", "25"],
     "(a+b+c)²=a²+b²+c²+2(ab+bc+ca); 0=a²+b²+c²−10 ⇒ a²+b²+c²=10."),
    ("For x > 0 with x² + 1/x² = 14, determine x + 1/x.", "4", ["8", "16", "12"],
     "(x+1/x)²=x²+1/x²+2=16 ⇒ x+1/x=4 (positive)."),
    ("If a³ + b³ = 35 and a + b = 5, find ab.", "6", ["5", "7", "10"],
     "a³+b³=(a+b)³−3ab(a+b); 35=125−15ab ⇒ ab=6."),
    ("If x + 1/x = 4, what is x³ + 1/x³?", "52", ["64", "48", "60"],
     "x³+1/x³=(x+1/x)³−3(x+1/x)=64−12=52."),
    ("Given a + b = 5 and ab = 6, compute a³ + b³.", "35", ["125", "65", "90"],
     "a³+b³=(a+b)³−3ab(a+b)=125−90=35."),
    ("If p + q = 7 and pq = 10, find p² + q².", "29", ["49", "20", "39"],
     "p²+q²=(p+q)²−2pq=49−20=29."),
    ("The squares of two numbers add to 25, and their product is 12. Find the square of their difference.", "1", ["25", "24", "49"],
     "(a−b)²=a²+b²−2ab=25−24=1."),
    ("If a − b = 5 and a² + b² = 37, find ab.", "6", ["12", "10", "8"],
     "(a−b)²=a²+b²−2ab; 25=37−2ab ⇒ ab=6."),
    ("Evaluate (a + b)² − (a − b)², given a + b = 10 and a − b = 6.", "64", ["36", "100", "136"],
     "(a+b)²−(a−b)²=4ab; a=8, b=2, ab=16, so 4·16=64."),
    ("Three numbers sum to 9, and the sum of their squares is 35. Find the sum of their pairwise products.", "23", ["46", "54", "17"],
     "(a+b+c)²=a²+b²+c²+2(ab+bc+ca); 81=35+2S ⇒ S=23."),
    ("If a + b + c = 0, what does a³ + b³ + c³ equal?", "3abc", ["abc", "0", "a² + b² + c²"],
     "When a+b+c=0, a³+b³+c³=3abc."),
    ("Given x = 2 + √3 and y = 2 − √3, find xy.", "1", ["4", "7", "−1"],
     "xy=(2+√3)(2−√3)=4−3=1."),
    ("If x = 3 + 2√2, find x + 1/x.", "6", ["3", "4√2", "5"],
     "(3+2√2)(3−2√2)=9−8=1, so 1/x=3−2√2 and x+1/x=6."),
    ("Two numbers sum to 8 and differ by 2. Find their product.", "15", ["16", "12", "10"],
     "ab=((a+b)²−(a−b)²)/4=(64−4)/4=15."),
    ("What is the sum of the roots of x² − 5x + 6 = 0?", "5", ["6", "−5", "1"],
     "For x²−5x+6=0, sum of roots = −(−5)/1 = 5."),
    ("What is the product of the roots of x² − 7x + 12 = 0?", "12", ["7", "−12", "−7"],
     "For x²−7x+12=0, product of roots = 12/1 = 12."),
    ("Simplify (a + b)² − (a − b)².", "4ab", ["2ab", "a² − b²", "a² + b²"],
     "(a+b)²−(a−b)²=(a²+2ab+b²)−(a²−2ab+b²)=4ab."),
    ("Expand (x + 5)².", "x² + 10x + 25", ["x² + 25", "x² − 10x + 25", "x² + 5x + 25"],
     "(x+5)²=x²+2·5·x+5²=x²+10x+25."),
    ("If x + 1/x = 6, find (x − 1/x)².", "32", ["36", "34", "40"],
     "(x−1/x)²=(x+1/x)²−4=36−4=32."),
    ("When the sum of a number and its reciprocal is 5, what is the sum of their squares?", "23", ["25", "27", "21"],
     "x²+1/x²=(x+1/x)²−2=25−2=23."),
]
for stem, ans, wrongs, proof in easy:
    add("EASY", stem, ans, wrongs, proof)

# MEDIUM originals (11)
medium = [
    ("If x + 1/x = 5, find x⁴ + 1/x⁴.", "527", ["529", "523", "625"],
     "x²+1/x²=23; x⁴+1/x⁴=23²−2=529−2=527."),
    ("If a and b satisfy a + b = 6 with ab = 8, determine a³ + b³.", "72", ["216", "144", "36"],
     "a³+b³=(a+b)³−3ab(a+b)=216−144=72."),
    ("Given x − 1/x = 4, find x³ − 1/x³.", "76", ["64", "52", "68"],
     "x³−1/x³=(x−1/x)³+3(x−1/x)=64+12=76."),
    ("Given a² + b² + c² = 29 with a + b + c = 9, find ab + bc + ca.", "26", ["52", "23", "34"],
     "(a+b+c)²=a²+b²+c²+2(ab+bc+ca); 81=29+2S ⇒ S=26."),
    ("Given that a number plus its reciprocal equals 7, find the sum of the fourth powers of the number and its reciprocal.", "2207", ["2209", "2401", "2205"],
     "x²+1/x²=49−2=47; x⁴+1/x⁴=47²−2=2209−2=2207."),
    ("If a + b = 4 and a³ + b³ = 28, find ab.", "3", ["1", "6", "9"],
     "a³+b³=(a+b)³−3ab(a+b); 28=64−12ab ⇒ ab=3."),
    ("The sum of two numbers is 10 and the sum of their squares is 58. Find their product.", "21", ["42", "29", "16"],
     "xy=((x+y)²−(x²+y²))/2=(100−58)/2=21."),
    ("When a + 1/a = 3, find a³ + 1/a³.", "18", ["27", "9", "21"],
     "a³+1/a³=(a+1/a)³−3(a+1/a)=27−9=18."),
    ("Three numbers sum to 12, and their pairwise products sum to 47. Find the sum of their squares.", "50", ["94", "38", "97"],
     "a²+b²+c²=(a+b+c)²−2(ab+bc+ca)=144−94=50."),
    ("The difference between a number and its reciprocal is 5. Find the sum of their squares.", "27", ["25", "23", "29"],
     "x²+1/x²=(x−1/x)²+2=25+2=27."),
    ("The sum of the squares of two positive numbers is 34 and their product is 15. Find their sum.", "8", ["64", "4", "6"],
     "(a+b)²=a²+b²+2ab=34+30=64 ⇒ a+b=8 (positive)."),
]
for stem, ans, wrongs, proof in medium:
    add("MEDIUM", stem, ans, wrongs, proof)

# HARD originals (5)
hard = [
    ("For a number t with t + 1/t = 4, find t⁵ + 1/t⁵.", "724", ["720", "728", "512"],
     "t²+1/t²=14, t³+1/t³=64−12=52; t⁵+1/t⁵=(t²+1/t²)(t³+1/t³)−(t+1/t)=14·52−4=728−4=724."),
    ("Given x + 1/x = 6, determine x⁶ + 1/x⁶.", "39202", ["39204", "39200", "46656"],
     "x²+1/x²=34, x³+1/x³=216−18=198; x⁶+1/x⁶=198²−2=39204−2=39202."),
    ("If a + b + c = 8, a² + b² + c² = 30 and ab + bc + ca = 17, find a³ + b³ + c³ − 3abc.", "104", ["52", "1040", "136"],
     "=(a+b+c)(a²+b²+c²−ab−bc−ca)=8(30−17)=8·13=104."),
    ("If x − 1/x = √5, find x³ − 1/x³.", "8√5", ["5√5", "2√5", "4√5"],
     "x³−1/x³=(x−1/x)³+3(x−1/x)=(√5)³+3√5=5√5+3√5=8√5."),
    ("Two numbers have sum 12 and the sum of their cubes is 936. Find their product.", "22", ["20", "24", "26"],
     "a³+b³=(a+b)³−3ab(a+b); 936=1728−36ab ⇒ ab=22."),
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
            if a == b or ratio >= .93:
                collisions.append((round(ratio, 4), other["question_text"], r["question_text"]))
    if collisions:
        for ratio, a, b in collisions:
            print(f"COLLISION {ratio}\n  A: {a}\n  B: {b}")
        raise SystemExit(f"{len(collisions)} near duplicate pair(s)")
    (BASE / "data/algebra_verified_batch.json").write_text(
        json.dumps({"questions": ROWS}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (BASE / "data/algebra_answer_ledger.json").write_text(
        json.dumps(LEDGER, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("WROTE", len(ROWS), dict(counts),
          "source", sum(r["source"] != ORIGINAL for r in ROWS),
          "original", sum(r["source"] == ORIGINAL for r in ROWS))


if __name__ == "__main__":
    main()
