"""Build a reviewed SSC HCF and LCM batch with a worked answer ledger.

Source-derived questions are transcribed from two scanned Physics Wallah
HCF and LCM lecture decks and independently re-solved. Only legible, well-posed
MCQs with four visible options were retained; title/contents pages, recaps,
concept-only slides, worked examples without options, a renumbered working
clone, a cross-deck duplicate and pages that merely repeated an earlier item
with changed numbers were excluded. Original SSC-style questions fill the
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
LCM1 = "HCF and LCM 01_.pdf"
LCM2 = "HCF and LCM 02_.pdf"
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
        "chapter_slug": "hcf-and-lcm", "question_text": stem,
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
# SOURCE-DERIVED QUESTIONS (19) — HCF and LCM 01 / 02 scanned decks
# ─────────────────────────────────────────────────────────────────────────

# --- HCF and LCM 01_.pdf (Lecture 1) ---
add("EASY", "Find the HCF of 35 and 30.",
    "5", ["6", "7", "8"],
    "35 = 5·7 and 30 = 2·3·5, so the common factor is 5.",
    src(LCM1, 4))
add("EASY", "Two numbers are in the ratio 15 : 11. If their HCF is 13, find the numbers.",
    "195 and 143", ["143 and 165", "175 and 190", "170 and 190"],
    "The numbers are 13·15 = 195 and 13·11 = 143, and gcd(195,143) = 13.",
    src(LCM1, 6))
add("EASY", "Find the HCF of 110, 180 and 540.",
    "10", ["20", "5", "30"],
    "110 = 2·5·11, 180 = 2²·3²·5, 540 = 2²·3³·5; the common part is 2·5 = 10.",
    src(LCM1, 9))
add("EASY", "Find the HCF of 240, 280 and 560.",
    "40", ["30", "20", "80"],
    "240 = 2⁴·3·5, 280 = 2³·5·7, 560 = 2⁴·5·7; the common part is 2³·5 = 40.",
    src(LCM1, 10))
add("EASY", "The least number which is exactly divisible by 5, 6, 8, 10 and 12 is:",
    "120", ["240", "180", "150"],
    "5, 6 = 2·3, 8 = 2³, 10 = 2·5, 12 = 2²·3; LCM = 2³·3·5 = 120.",
    src(LCM1, 11))
add("MEDIUM", "The HCF of two numbers is 5 and their LCM is 120. How many pairs of such numbers can be formed?",
    "2", ["3", "4", "5"],
    "Write the numbers as 5m and 5n with gcd(m,n) = 1 and mn = 120/5 = 24; the coprime factor pairs are (1,24) and (3,8), giving 2 pairs.",
    src(LCM1, 12))
add("MEDIUM", "The LCM of two numbers is 45 times their HCF. If one of the numbers is 125 and the sum of the HCF and the LCM is 1150, the other number is:",
    "225", ["235", "215", "250"],
    "L = 45H and H + L = 1150 ⇒ 46H = 1150 ⇒ H = 25, L = 1125; the other number is H·L/125 = 28125/125 = 225.",
    src(LCM1, 13))
add("MEDIUM", "The LCM of two numbers is 495 and their HCF is 5. If the sum of the numbers is 100, find the difference between the two numbers.",
    "10", ["5", "15", "20"],
    "Product = HCF·LCM = 2475; the numbers are the roots of t² − 100t + 2475 = 0, giving 55 and 45, so the difference is 10.",
    src(LCM1, 14))

# --- HCF and LCM 02_.pdf (Lecture 2) ---
add("MEDIUM", "Find the LCM of 15, 24, 32 and 45.",
    "1440", ["1436", "1435", "1448"],
    "15 = 3·5, 24 = 2³·3, 32 = 2⁵, 45 = 3²·5; LCM = 2⁵·3²·5 = 1440.",
    src(LCM2, 4))
add("MEDIUM", "Find the LCM of 48, 50, 98, 54 and 72.",
    "2⁴ × 3³ × 5² × 7²", ["2³ × 3³ × 5² × 7²", "2⁴ × 3² × 5² × 7²", "2³ × 3³ × 5 × 7"],
    "Taking the highest power of each prime: 2⁴·3³·5²·7².",
    src(LCM2, 6))
add("MEDIUM", "Find the LCM of 3⁴ × 5 × 7² × 11, 3³ × 5 × 11² and 3² × 5³ × 11⁴.",
    "3⁴ × 5³ × 7² × 11⁴", ["3² × 5 × 11", "3⁴ × 5 × 7 × 11⁴", "3⁴ × 5³ × 7² × 11"],
    "Highest powers are 3⁴, 5³, 7² and 11⁴, so LCM = 3⁴·5³·7²·11⁴.",
    src(LCM2, 7))
add("MEDIUM", "Find the HCF of 1/2, 3/4, 5/6, 7/8 and 9/10.",
    "1/120", ["1/7", "1/32", "1/40"],
    "HCF of fractions = HCF(numerators)/LCM(denominators) = 1/120.",
    src(LCM2, 10))
add("MEDIUM", "What is the HCF of 7/16, 21/32 and 49/8?",
    "7/32", ["7/64", "147/32", "147/8"],
    "HCF = HCF(7,21,49)/LCM(16,32,8) = 7/32.",
    src(LCM2, 11))
add("MEDIUM", "The LCM of 1/6, 7/27, 5/9, 4/15 and 8/3 is:",
    "280/3", ["3/280", "280/15", "15/280"],
    "LCM = LCM(1,7,5,4,8)/HCF(6,27,9,15,3) = 280/3.",
    src(LCM2, 12))
add("HARD", "Find the difference between the LCM and the HCF of 4/7, 5/14 and 9/35.",
    "25.7", ["19.5", "20.7", "22.3"],
    "LCM = LCM(4,5,9)/HCF(7,14,35) = 180/7 and HCF = HCF(4,5,9)/LCM(7,14,35) = 1/70; difference = 180/7 − 1/70 = 1799/70 = 25.7.",
    src(LCM2, 13))
add("HARD", "Find the least number which is divisible by 2, 3, 4, 5 and 6, leaves a remainder 1 in each case, and is completely divisible by 7.",
    "301", ["288", "360", "358"],
    "LCM(2,3,4,5,6) = 60; the least 60k + 1 divisible by 7 is 301 (301 = 7·43).",
    src(LCM2, 14))
add("HARD", "Find the least number which when divided by 5, 6, 7 and 8 leaves a remainder 3 in each case, but when divided by 9 leaves no remainder.",
    "1683", ["843", "2523", "3363"],
    "LCM(5,6,7,8) = 840; 840k + 3 is the first value divisible by 9 at k = 2, giving 1683.",
    src(LCM2, 16))
add("MEDIUM", "Three different containers contain 496 L, 403 L and 713 L of a milk-and-water mixture. What is the biggest measure of a container that can measure all three quantities exactly?",
    "31 L", ["41 L", "51 L", "52 L"],
    "496 = 2⁴·31, 403 = 13·31 and 713 = 23·31, so HCF = 31 L.",
    src(LCM2, 19))
add("MEDIUM", "Six bells ring after 2, 4, 6, 8, 10 and 12 seconds respectively. How many times will they ring simultaneously in 30 minutes?",
    "16", ["18", "20", "22"],
    "LCM(2,4,6,8,10,12) = 120 s = 2 min; in 30 min they ring together 30/2 = 15 times plus the initial toll = 16 times.",
    src(LCM2, 20))

# ─────────────────────────────────────────────────────────────────────────
# ORIGINAL SSC-STYLE QUESTIONS (71) filling the remaining per-level gaps
# ─────────────────────────────────────────────────────────────────────────

# EASY originals (25) — mixed phrasing and contexts so no two stems collide.
easy = [
    ("Find the HCF of 12 and 18.", "6", ["3", "4", "9"],
     "12 = 2²·3 and 18 = 2·3², so HCF = 2·3 = 6."),
    ("Find the LCM of 6 and 8.", "24", ["12", "48", "16"],
     "6 = 2·3 and 8 = 2³, so LCM = 2³·3 = 24."),
    ("What is the HCF of 45 and 75?", "15", ["5", "9", "25"],
     "45 = 3²·5 and 75 = 3·5², so HCF = 3·5 = 15."),
    ("What is the LCM of 12 and 15?", "60", ["30", "90", "180"],
     "12 = 2²·3 and 15 = 3·5, so LCM = 2²·3·5 = 60."),
    ("Find the HCF of 14, 28 and 42.", "14", ["7", "2", "21"],
     "14 = 2·7, 28 = 2²·7 and 42 = 2·3·7, so HCF = 2·7 = 14."),
    ("Find the LCM of 4, 6 and 8.", "24", ["12", "48", "96"],
     "LCM = 2³·3 = 24."),
    ("The product of two numbers is 216 and their HCF is 6. Find their LCM.", "36", ["30", "54", "1296"],
     "HCF·LCM = product, so LCM = 216/6 = 36."),
    ("The HCF of two numbers is 9 and their LCM is 108. If one number is 27, find the other.", "36", ["12", "27", "96"],
     "Other = HCF·LCM / 27 = 9·108/27 = 36."),
    ("Three bells toll at intervals of 4, 6 and 8 minutes respectively. If they start tolling together, after how many minutes will they next toll together?", "24", ["12", "18", "48"],
     "They toll together after LCM(4,6,8) = 24 minutes."),
    ("Find the greatest number that divides both 24 and 36 exactly.", "12", ["6", "8", "18"],
     "HCF(24,36) = 12."),
    ("Find the smallest number that is exactly divisible by 6, 9 and 12.", "36", ["72", "18", "108"],
     "LCM(6,9,12) = 2²·3² = 36."),
    ("Find the largest number that divides 70 and 125, leaving remainders 5 and 8 respectively.", "13", ["5", "8", "65"],
     "Required number = HCF(70−5, 125−8) = HCF(65,117) = 13."),
    ("Two numbers are in the ratio 3 : 4 and their HCF is 5. Find the numbers.", "15 and 20", ["12 and 16", "30 and 40", "9 and 12"],
     "The numbers are 5·3 = 15 and 5·4 = 20."),
    ("Find the HCF of two consecutive even numbers 8 and 10.", "2", ["4", "8", "1"],
     "Consecutive even numbers differ by 2, so their HCF is 2."),
    ("Find the HCF of 18, 24 and 30.", "6", ["3", "12", "2"],
     "18 = 2·3², 24 = 2³·3, 30 = 2·3·5, so HCF = 6."),
    ("Find the LCM of 9, 12 and 15.", "180", ["90", "360", "540"],
     "LCM = 2²·3²·5 = 180."),
    ("Find the HCF of 25 and 40.", "5", ["10", "25", "8"],
     "25 = 5² and 40 = 2³·5, so HCF = 5."),
    ("The LCM of two numbers is 180 and their HCF is 6. If one number is 36, find the other.", "30", ["24", "60", "90"],
     "Other = HCF·LCM / 36 = 6·180/36 = 30."),
    ("Find the greatest common divisor of 48, 72 and 120.", "24", ["12", "8", "36"],
     "48 = 2⁴·3, 72 = 2³·3², 120 = 2³·3·5, so GCD = 2³·3 = 24."),
    ("Find the smallest number divisible by 8, 10 and 12.", "120", ["240", "60", "480"],
     "8 = 2³, 10 = 2·5, 12 = 2²·3, so LCM = 2³·3·5 = 120."),
    ("What is the HCF of the two prime numbers 7 and 11?", "1", ["7", "11", "77"],
     "Distinct primes share no common factor, so HCF = 1."),
    ("Find the LCM of 6, 7 and 8.", "168", ["336", "84", "56"],
     "LCM = 2³·3·7 = 168."),
    ("Find the HCF of 36 and 84.", "12", ["6", "18", "24"],
     "36 = 2²·3² and 84 = 2²·3·7, so HCF = 2²·3 = 12."),
    ("Find the LCM of 16 and 20.", "80", ["40", "160", "320"],
     "16 = 2⁴ and 20 = 2²·5, so LCM = 2⁴·5 = 80."),
    ("Find the HCF of 22, 33 and 44.", "11", ["2", "3", "22"],
     "22 = 2·11, 33 = 3·11, 44 = 4·11, so HCF = 11."),
]
for stem, ans, wrongs, proof in easy:
    add("EASY", stem, ans, wrongs, proof)

# MEDIUM originals (19)
medium = [
    ("Find the largest 4-digit number that is exactly divisible by 12.", "9996", ["9999", "9984", "9960"],
     "12·833 = 9996, which is the largest multiple of 12 not exceeding 9999."),
    ("Find the smallest 4-digit number that is exactly divisible by 15.", "1005", ["1000", "1020", "1050"],
     "15·67 = 1005 is the first multiple of 15 at or above 1000."),
    ("Find the largest number that divides 245 and 1029, leaving a remainder 5 in each case.", "16", ["8", "32", "48"],
     "Required number = HCF(245−5, 1029−5) = HCF(240,1024) = 2⁴ = 16."),
    ("Find the smallest number which when divided by 12, 15 and 20 leaves a remainder 5.", "65", ["55", "60", "80"],
     "LCM(12,15,20) = 60, so the number is 60 + 5 = 65."),
    ("Find the greatest number that divides 615 and 963, leaving a remainder 6 in each case.", "87", ["29", "3", "174"],
     "Required number = HCF(615−6, 963−6) = HCF(609,957) = 87."),
    ("Two numbers are in the ratio 5 : 7 and their LCM is 210. Find their HCF.", "6", ["7", "5", "42"],
     "The numbers are 5k and 7k with LCM 35k = 210 ⇒ k = 6, so HCF = 6."),
    ("The HCF of two numbers is 12 and their product is 1728. Find their LCM.", "144", ["12", "288", "20736"],
     "LCM = product / HCF = 1728/12 = 144."),
    ("Find the greatest 4-digit number which when divided by 10, 12 and 15 leaves a remainder 3 in each case.", "9963", ["9993", "9903", "9843"],
     "LCM(10,12,15) = 60; the largest value ≤ 9999 with remainder 3 is 9963."),
    ("Find the least number which when divided by 6, 15 and 18 leaves a remainder 5 in each case.", "95", ["90", "85", "180"],
     "LCM(6,15,18) = 90, so the number is 90 + 5 = 95."),
    ("Reduce the fraction 161/207 to its lowest terms.", "7/9", ["8/9", "7/11", "9/11"],
     "HCF(161,207) = 23, so 161/207 = (161÷23)/(207÷23) = 7/9."),
    ("Find the HCF of 1.5 and 2.4.", "0.3", ["0.6", "1.2", "0.09"],
     "HCF(1.5,2.4) = HCF(15,24)/10 = 3/10 = 0.3."),
    ("Find the LCM of 0.6, 0.9 and 1.2.", "3.6", ["1.8", "0.36", "7.2"],
     "LCM(0.6,0.9,1.2) = LCM(6,9,12)/10 = 36/10 = 3.6."),
    ("The product of the HCF and the LCM of two numbers is 1200. If one number is 60, find the other.", "20", ["30", "40", "24"],
     "The product of the numbers = HCF·LCM = 1200, so the other number is 1200/60 = 20."),
    ("Three numbers are in the ratio 2 : 3 : 5 and their HCF is 8. Find their LCM.", "240", ["120", "30", "144"],
     "The numbers are 16, 24 and 40; their LCM is 2⁴·3·5 = 240."),
    ("Find the least number that must be added to 3000 so that the sum is exactly divisible by 12, 15 and 18.", "60", ["120", "180", "24"],
     "LCM(12,15,18) = 180; 3000 leaves remainder 120, so add 180 − 120 = 60."),
    ("A rectangular courtyard is 18 m 72 cm long and 13 m 20 cm broad. Find the side of the largest square tile that can pave it exactly.", "24 cm", ["12 cm", "36 cm", "18 cm"],
     "1872 cm and 1320 cm have HCF 2³·3 = 24 cm."),
    ("The circumferences of two circles are 88 cm and 132 cm. Find the greatest length of tape that can measure both exactly.", "44 cm", ["22 cm", "11 cm", "66 cm"],
     "HCF(88,132) = 44 cm."),
    ("In a school, students can be arranged exactly in rows of 12, 15 or 20. Find the minimum number of students.", "60", ["30", "120", "180"],
     "LCM(12,15,20) = 60."),
    ("What is the least number that leaves a remainder of 7 when divided by 12, 20 and 24?", "127", ["120", "137", "240"],
     "LCM(12,20,24) = 120, so the number is 120 + 7 = 127."),
]
for stem, ans, wrongs, proof in medium:
    add("MEDIUM", stem, ans, wrongs, proof)

# HARD originals (27)
hard = [
    ("Find the largest number that divides 2053 and 967, leaving remainders 5 and 7 respectively.", "64", ["32", "16", "128"],
     "Required number = HCF(2053−5, 967−7) = HCF(2048,960) = 2⁶ = 64."),
    ("Find the greatest 4-digit number that is exactly divisible by 15, 20 and 28.", "9660", ["9900", "9840", "9600"],
     "LCM(15,20,28) = 420; 420·23 = 9660 is the largest 4-digit multiple."),
    ("Find the least 5-digit number that is exactly divisible by 6, 8, 12 and 15.", "10080", ["10000", "10020", "10200"],
     "LCM(6,8,12,15) = 120; 120·84 = 10080 is the smallest 5-digit multiple."),
    ("The LCM and HCF of two numbers are 84 and 14 respectively. How many such pairs of numbers are possible?", "2", ["3", "4", "6"],
     "The numbers are 14m and 14n with gcd(m,n) = 1 and mn = 6, giving the coprime pairs (1,6) and (2,3) — 2 pairs."),
    ("Two numbers are in the ratio 5 : 6 and their LCM is 150. Find the sum of the numbers.", "55", ["60", "50", "66"],
     "The numbers are 5k and 6k with LCM 30k = 150 ⇒ k = 5; the numbers 25 and 30 sum to 55."),
    ("Find the smallest number which when divided by 6, 8, 10 and 12 leaves remainders 4, 6, 8 and 10 respectively.", "118", ["122", "120", "110"],
     "Each remainder is 2 less than its divisor, so the number is LCM(6,8,10,12) − 2 = 120 − 2 = 118."),
    ("Find the least number which when divided by 6, 8 and 10 leaves remainders 5, 7 and 9 respectively.", "119", ["120", "121", "109"],
     "Each remainder is 1 less than its divisor, so the number is LCM(6,8,10) − 1 = 120 − 1 = 119."),
    ("Find the least number of square tiles required to pave a floor 15 m 17 cm long and 9 m 2 cm broad.", "814", ["407", "1628", "74"],
     "1517 cm and 902 cm have HCF 41 cm; tiles needed = 37·22 = 814."),
    ("Find the greatest number that divides 1290, 4230 and 2835, leaving the same remainder in each case.", "15", ["5", "45", "30"],
     "Required number = HCF(4230−1290, 2835−1290, 4230−2835) = HCF(2940,1545,1395) = 15."),
    ("Three bells ring at intervals of 20, 25 and 30 minutes respectively. If they ring together at 8 a.m., when will they next ring together?", "1 p.m.", ["10 a.m.", "12 noon", "2 p.m."],
     "LCM(20,25,30) = 300 min = 5 h, so they next ring together at 8 a.m. + 5 h = 1 p.m."),
    ("Six bells start ringing together and then ring at intervals of 4, 8, 12, 16, 20 and 24 seconds respectively. In 60 minutes, how many times do they ring together?", "16", ["15", "20", "30"],
     "LCM(4,8,12,16,20,24) = 240 s = 4 min; in 60 min they coincide 60/4 = 15 times plus the start = 16 times."),
    ("The product of two numbers is 4104 and their HCF is 6. How many pairs of such numbers are possible?", "4", ["3", "6", "8"],
     "The numbers are 6m and 6n with gcd(m,n) = 1 and mn = 4104/(6·6) = 114, giving the coprime pairs (1,114), (2,57), (3,38) and (6,19) — 4 pairs."),
    ("Three runners complete one round of a circular track in 120, 150 and 180 seconds respectively. If they start together, after how many minutes will they meet again at the starting point?", "30", ["15", "60", "45"],
     "LCM(120,150,180) = 1800 s = 30 minutes."),
    ("Find the least number which when divided by 24, 30, 36 and 40 leaves a remainder 13.", "373", ["360", "353", "720"],
     "LCM(24,30,36,40) = 360, so the number is 360 + 13 = 373."),
    ("Find the greatest number that divides 1305, 4665 and 6905, leaving the same remainder in each case.", "1120", ["560", "280", "2240"],
     "Required number = HCF(4665−1305, 6905−4665, 6905−1305) = HCF(3360,2240,5600) = 1120."),
    ("The sum of two numbers is 512 and their HCF is 32. How many pairs of such numbers are possible?", "4", ["3", "5", "8"],
     "The numbers are 32m and 32n with gcd(m,n) = 1 and m + n = 16, giving the pairs (1,15), (3,13), (5,11) and (7,9) — 4 pairs."),
    ("Find the smallest number which is exactly divisible by 12, 16 and 18, and is also a perfect square.", "144", ["288", "72", "432"],
     "LCM(12,16,18) = 144 = 12², which is already a perfect square."),
    ("Find the least number that must be subtracted from 10000 so that the remainder is exactly divisible by 21, 28 and 36.", "172", ["252", "80", "328"],
     "LCM(21,28,36) = 252; 10000 = 252·39 + 172, so subtract 172."),
    ("Find the greatest 4-digit number that is exactly divisible by 6, 8, 9, 12 and 15.", "9720", ["9960", "9840", "9900"],
     "LCM = 360; 360·27 = 9720 is the largest 4-digit multiple."),
    ("Three men jog around a circular track and complete one round in 8, 12 and 15 minutes respectively. If they start together, after how long will they meet again at the starting point?", "2 hours", ["1 hour", "3 hours", "4 hours"],
     "LCM(8,12,15) = 120 min = 2 hours."),
    ("The HCF of two numbers is 24 and their LCM is 720. If one of the numbers lies between 100 and 150, find it.", "120", ["144", "96", "240"],
     "The numbers are 24m and 24n with gcd(m,n) = 1 and mn = 30; the pair (5,6) gives 120 and 144, and 120 lies between 100 and 150."),
    ("Find the least 4-digit number which when divided by 6, 8, 10 and 12 leaves a remainder 3 in each case.", "1083", ["1023", "1203", "1080"],
     "LCM(6,8,10,12) = 120; the least 4-digit value with remainder 3 is 1083."),
    ("The LCM of two numbers is six times their HCF. The sum of the HCF and the LCM is 350. If one number is 50, find the other number.", "300", ["250", "350", "150"],
     "L = 6H and H + L = 350 ⇒ 7H = 350 ⇒ H = 50, L = 300; the other number is H·L/50 = 15000/50 = 300."),
    ("A number when divided by 15, 20 and 25 leaves a remainder 8 in each case. Find the greatest such 3-digit number.", "908", ["608", "308", "1208"],
     "LCM(15,20,25) = 300; the largest 3-digit value with remainder 8 is 908."),
    ("Two numbers have an HCF of 15 and an LCM of 300. If both numbers are greater than 50, find their sum.", "135", ["120", "105", "150"],
     "The numbers are 15m and 15n with gcd(m,n) = 1 and mn = 20; both exceed 50 only for (4,5), giving 60 and 75 whose sum is 135."),
    ("Find the least number which when divided by 5, 7, 9 and 11 leaves a remainder 3 in each case.", "3468", ["3465", "3462", "6930"],
     "LCM(5,7,9,11) = 3465, so the number is 3465 + 3 = 3468."),
    ("Find the greatest number which on dividing 1657 and 2037 leaves remainders 6 and 5 respectively.", "127", ["13", "254", "31"],
     "Required number = HCF(1657−6, 2037−5) = HCF(1651,2032) = 127."),
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
    (BASE / "data/hcf_lcm_verified_batch.json").write_text(
        json.dumps({"questions": ROWS}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (BASE / "data/hcf_lcm_answer_ledger.json").write_text(
        json.dumps(LEDGER, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("WROTE", len(ROWS), dict(counts),
          "source", sum(r["source"] != ORIGINAL for r in ROWS),
          "original", sum(r["source"] == ORIGINAL for r in ROWS))


if __name__ == "__main__":
    main()
