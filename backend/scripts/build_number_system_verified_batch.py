"""Build the reviewed SSC Number System bank and calculation ledger."""
from __future__ import annotations

import json
import random
import re
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from fractions import Fraction
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
ORIGINAL = "Original SSC-style practice question"
ROWS: list[dict] = []
LEDGER: list[dict] = []


def source(pdf: str, page: int) -> str:
    return f"{pdf}, PDF page {page}; exam/year not stated per item (PYQ status unverified)"


def text_number(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def numeric_distractors(answer: str) -> list[str] | None:
    try:
        value = Fraction(answer)
    except (ValueError, ZeroDivisionError):
        return None
    if value.denominator == 1:
        n = value.numerator
        candidates = [n + 1, n - 1, n + 2, n - 2, n + 3, n - 3]
        return [str(x) for x in candidates if x != n]
    step = Fraction(1, value.denominator)
    return [text_number(value + step), text_number(value - step), text_number(value + 2 * step), text_number(value - 2 * step)]


def q(level: str, stem: str, answer: str, proof: str, src: str = ORIGINAL, wrong=()):
    answer = str(answer)
    distractors = list(wrong) if wrong else (numeric_distractors(answer) or ["0", "1", "2", "3"])
    options = [answer]
    parsed_answer = None
    try:
        parsed_answer = Fraction(answer)
    except (ValueError, ZeroDivisionError):
        pass
    seen_numeric = {parsed_answer} if parsed_answer is not None else set()
    for candidate in distractors:
        candidate = str(candidate)
        if candidate in options:
            continue
        try:
            numeric = Fraction(candidate)
        except (ValueError, ZeroDivisionError):
            numeric = None
        if numeric is not None:
            if numeric in seen_numeric:
                continue
            seen_numeric.add(numeric)
        options.append(candidate)
        if len(options) == 4:
            break
    fallback = ["1/2", "2/3", "3/4", "4/5", "5/6", "7/8", "9/10", "11/12", "13/15", "17/20"]
    for candidate in fallback:
        if len(options) == 4:
            break
        if candidate not in options:
            try:
                numeric = Fraction(candidate)
            except ValueError:
                numeric = None
            if numeric is None or numeric not in seen_numeric:
                options.append(candidate)
                if numeric is not None:
                    seen_numeric.add(numeric)
    if len(options) != 4:
        raise ValueError(f"Need four distinct options for {stem!r}: {options}")
    random.Random(len(ROWS) * 43 + len(stem)).shuffle(options)
    key = "ABCD"[options.index(answer)]
    row = {
        "subject_slug": "maths", "subcategory_slug": "advanced-maths", "chapter_slug": "number-system",
        "question_text": stem, "options": dict(zip("ABCD", options)), "correct_option": key,
        "explanation": proof, "difficulty": level, "is_pyq": False, "pyq_year": None,
        "pyq_exam_name": None, "source": src,
    }
    ROWS.append(row)
    LEDGER.append({"row": len(ROWS), "question": stem, "difficulty": level,
                   "expected_answer": answer, "independent_reasoning": proof, "source": src})


def add(level, items):
    for item in items:
        q(level, *item)


# Source-derived questions: selected from legible scanned question slides. The
# displayed keys were independently recalculated; individual PYQ attribution
# is absent, so source provenance is retained without verified-PYQ flags.
EASY_SOURCE = [
    ("Evaluate 1/(4·5) + 1/(5·6) + … + 1/(11·12).", "1/6", "Use 1/[n(n+1)]=1/n−1/(n+1). The terms telescope from 1/4 through −1/12, giving 1/6.", source("Number System 1.pdf", 9), ["1/5", "1/4", "1/12"]),
    ("Simplify 1+2+3+…+99+100+99+…+2+1.", "10000", "The sum is (1+…+100)+(1+…+99)=100·101/2+99·100/2=5,050+4,950=10,000.", source("Number System 1.pdf", 13), ["9990", "9999", "9900"]),
    ("Evaluate (1+1/2)(1+1/3)(1+1/4)…(1+1/29).", "15", "Each factor is (n+1)/n for n=2,…,29, so the product telescopes to 30/2=15.", source("Number System 1.pdf", 15), ["13", "14", "16"]),
    ("How many trailing zeroes are in 5²×2⁶?", "2", "A trailing zero needs one factor 2 and one factor 5. The product contains min(6,2)=2 such pairs.", source("Number System 2_.pdf", 5), ["1", "3", "4"]),
    ("How many trailing zeroes are in 100!?", "24", "Count factors of 5: ⌊100/5⌋+⌊100/25⌋=20+4=24. There are more factors of 2.", source("Number System 2_.pdf", 12), ["20", "25", "28"]),
    ("How many trailing zeroes are in 1·3·5·7·…·99?", "0", "Every factor is odd, so the product has no factor 2 and therefore no factor 10.", source("Number System 2_.pdf", 15), ["1", "10", "24"]),
]
MEDIUM_SOURCE = [
    ("Evaluate 1/(2·3)+1/(3·4)+…+1/(19·20).", "9/20", "Apply 1/[n(n+1)]=1/n−1/(n+1) for n=2,…,19. The sum is 1/2−1/20=9/20.", source("Number System 1.pdf", 6), ["3/20", "2/19", "9/19"]),
    ("Evaluate 1/(2·5)+1/(5·8)+1/(8·11)+…+1/(23·26).", "2/13", "Each term 1/[a(a+3)]=(1/3)(1/a−1/(a+3)). The intermediate terms cancel, leaving (1/3)(1/2−1/26)=2/13.", source("Number System 1.pdf", 7), ["1/11", "3/11", "4/13"]),
    ("If x=1+1/(1+1/(1+1/(1+1/2))), find 2x+7/4.", "5", "Evaluate inward: 1+1/2=3/2; then 5/3, 8/5, and x=13/8. Thus 2x+7/4=13/4+7/4=5.", source("Number System 1.pdf", 22), ["4", "13/8", "7/8"]),
    ("How many trailing zeroes are in 55¹¹×22³³?", "11", "55¹¹ contributes 11 factors of 5; 22³³ contributes 33 factors of 2. The number of complete (2,5) pairs is 11.", source("Number System 2_.pdf", 7), ["22", "33", "44"]),
    ("How many trailing zeroes are in 5·10·25·40·50·55·65·125·80?", "9", "Count prime factors: the product has 13 factors of 5 and 9 factors of 2, so it has min(13,9)=9 trailing zeroes.", source("Number System 2_.pdf", 10), ["4", "5", "13"]),
    ("Evaluate 1/(3·7)+1/(7·11)+…+1/(31·35).", "8/105", "For terms with n=3,7,…,31, 1/[n(n+4)]=(1/4)(1/n−1/(n+4)). The sum telescopes to (1/4)(1/3−1/35)=8/105.", source("Number System 1.pdf", 8), ["1/14", "4/105", "8/35"]),
    ("Evaluate 9½+99½+999½+9999½.", "11108", "The integer parts sum to 9+99+999+9999=11,106; four halves total 2, giving 11,108.", source("Number System 2_.pdf", 18), ["11106", "11107", "11109"]),
]
HARD_SOURCE = [
    ("Evaluate 5/(2²·3²)+7/(3²·4²)+9/(4²·5²)+…+39/(19²·20²).", "99/400", "For each n=2,…,19, (2n+1)/(n²(n+1)²)=1/n²−1/(n+1)². The sum telescopes to 1/4−1/400=99/400.", source("Number System 1.pdf", 12), ["99/300", "299/200", "399/100"]),
    ("Evaluate (1−1/2²)(1−1/3²)…(1−1/90²).", "91/180", "Factor each term as ((n−1)(n+1))/n²=((n−1)/n)((n+1)/n). Products telescope to (1/90)(91/2)=91/180.", source("Number System 1.pdf", 18), ["90/91", "91/91", "1/90"]),
    ("Evaluate 1−1/(1−1/(1−1/(1−2/3))).", "1/3", "Evaluate from the innermost layer: 1−2/3=1/3; then 1−3=−2; then 1−(−1/2)=3/2; finally 1−2/3=1/3.", source("Number System 1.pdf", 23), ["2/3", "−1/3", "−2/3"]),
    ("Evaluate 1+1/(2+1/(3+1/(4+1/5))).", "225/157", "From inside out: 4+1/5=21/5; 3+5/21=68/21; 2+21/68=157/68; hence the whole expression is 1+68/157=225/157.", source("Number System 1.pdf", 25), ["411/719", "157/225", "205/157"]),
    ("How many trailing zeroes are in (3¹²³−3¹²²−3¹²¹)(2¹²¹−2¹²⁰−2¹¹⁹)?", "1", "Factor to 3¹²¹(9−3−1)·2¹¹⁹(4−2−1)=5·3¹²¹·2¹¹⁹. Exactly one factor 5 is available, and at least one factor 2.", source("Number System 2_.pdf", 8), ["0", "2", "3"]),
    ("Evaluate (1−1/2)(1−1/3)(1−1/4)…(1−1/40).", "1/40", "Each factor is (n−1)/n. The product telescopes from n=2 through 40 to 1/40.", source("Number System 1.pdf", 16), ["39/40", "1/39", "2/40"]),
]

add("EASY", EASY_SOURCE)
add("MEDIUM", MEDIUM_SOURCE)
add("HARD", HARD_SOURCE)

# Original SSC-style items fill the remaining level slots, with broad coverage
# beyond the PDFs' emphasis on logical series and trailing-zero counts.
EASY_ORIGINAL = [
 ("Which set contains 0 but not −1?", "Whole numbers", "Whole numbers are 0,1,2,…; integers include −1 and natural numbers do not include 0 under the usual SSC convention.", ORIGINAL, ["Natural numbers", "Negative integers", "Irrational numbers"]),
 ("Which of the following is irrational?", "√7", "7 is not a perfect square, so √7 cannot be written as a ratio of integers.", ORIGINAL, ["0.25", "3/8", "√49"]),
 ("How many positive factors does 36 have?", "9", "36=2²·3², so the divisor count is (2+1)(2+1)=9.", ORIGINAL, ["6", "8", "12"]),
 ("Which number is prime?", "53", "53 has no prime divisor at most √53: it is not divisible by 2, 3, 5, or 7.", ORIGINAL, ["51", "55", "57"]),
 ("What is the remainder when 347 is divided by 9?", "5", "The digit sum is 3+4+7=14, whose remainder modulo 9 is 5.", ORIGINAL, ["3", "4", "6"]),
 ("What is the units digit of 7⁴?", "1", "The units digits of powers of 7 cycle 7,9,3,1 with period 4; exponent 4 gives 1.", ORIGINAL, ["3", "7", "9"]),
 ("Which fraction has a terminating decimal expansion?", "7/40", "In lowest terms, a rational has a terminating decimal exactly when its denominator has only prime factors 2 and 5; 40=2³·5.", ORIGINAL, ["2/21", "5/12", "7/30"]),
 ("What is the smallest prime factor of 91?", "7", "91=7·13, so its smallest prime factor is 7.", ORIGINAL, ["3", "5", "11"]),
 ("Which is the greatest 3-digit number divisible by 8?", "992", "The greatest 3-digit integer is 999; 999 leaves remainder 7 modulo 8, so subtract 7 to get 992.", ORIGINAL, ["984", "996", "998"]),
 ("How many integers lie strictly between −3 and 4?", "6", "They are −2,−1,0,1,2,3: six integers.", ORIGINAL, ["5", "7", "8"]),
 ("What is the prime factorization of 84?", "2²·3·7", "84=4·21=2²·3·7.", ORIGINAL, ["2·3·14", "2²·21", "3·28"]),
 ("Which number is divisible by 11?", "2,739", "For 2,739, alternating digit sums differ by (9+7)−(3+2)=11, which is divisible by 11.", ORIGINAL, ["2,738", "2,740", "2,741"]),
 ("What is the units digit of 3⁵?", "3", "Powers of 3 have units digits 3,9,7,1 repeating every four powers. Since 5≡1 mod 4, the units digit is 3.", ORIGINAL, ["1", "7", "9"]),
 ("Which number is a perfect square?", "1,296", "1296=36².", ORIGINAL, ["1,250", "1,300", "1,350"]),
 ("Express 0.375 as a fraction in lowest terms.", "3/8", "0.375=375/1000; divide numerator and denominator by 125 to get 3/8.", ORIGINAL, ["5/12", "7/16", "3/10"]),
 ("What is the least positive integer divisible by 2, 3, and 5?", "30", "The least common multiple of pairwise coprime 2,3,5 is their product 30.", ORIGINAL, ["15", "20", "60"]),
 ("A number leaves remainder 2 when divided by 5. Which could it be?", "37", "37=5·7+2, whereas the other choices are not congruent to 2 modulo 5.", ORIGINAL, ["35", "38", "40"]),
 ("How many distinct prime factors does 210 have?", "4", "210=2·3·5·7, which has four distinct prime factors.", ORIGINAL, ["2", "3", "5"]),
 ("Which decimal is equal to 2/3?", "0.666…", "Long division of 2 by 3 repeats remainder 2, producing the recurring digit 6.", ORIGINAL, ["0.23", "0.636…", "0.6"]),
 ("What is the smallest integer greater than 20 that is a perfect cube?", "27", "3³=27 is the first cube greater than 20; 2³=8 is smaller.", ORIGINAL, ["24", "25", "32"]),
 ("Which statement about the integer 1 is correct?", "It is neither prime nor composite", "A prime has exactly two positive divisors and a composite has more than two; 1 has only one positive divisor.", ORIGINAL, ["It is prime", "It is composite", "It is neither an integer nor rational"]),
 ("What is the remainder when 5,432 is divided by 10?", "2", "Division by 10 leaves the units digit as the remainder, which is 2.", ORIGINAL, ["0", "3", "4"]),
 ("How many positive divisors does the prime number 29 have?", "2", "A prime has exactly two positive divisors: 1 and itself.", ORIGINAL, ["1", "3", "29"]),
 ("What is the remainder when 1²+2²+…+10² is divided by 11?", "0", "The sum of the first ten squares is 10·11·21/6=385=35·11, so the remainder is 0.", ORIGINAL, ["1", "5", "10"]),
]
MEDIUM_ORIGINAL = [
 ("Find the least positive integer that must be added to 1,247 to make the result divisible by 9.", "4", "The digit sum is 14, so 1,247≡5 (mod 9). Adding 4 makes 1,251, divisible by 9.", ORIGINAL, ["1", "2", "3"]),
 ("Find the remainder when 2⁵⁰ is divided by 7.", "4", "Powers of 2 modulo 7 cycle 2,4,1 with period 3. Since 50≡2 mod 3, the remainder is 4.", ORIGINAL, ["1", "2", "3"]),
 ("How many positive divisors does 360 have?", "24", "360=2³·3²·5, so its divisor count is (3+1)(2+1)(1+1)=24.", ORIGINAL, ["18", "20", "30"]),
 ("Convert 0.2̅7̅ (that is, 0.272727…) to a fraction in lowest terms.", "3/11", "Let x=0.272727…; then 100x−x=27, so 99x=27 and x=27/99=3/11.", ORIGINAL, ["27/100", "27/90", "2/7"]),
 ("What is the units digit of 13⁴⁷?", "7", "Only the base's units digit matters. Powers of 3 cycle 3,9,7,1 every four; 47≡3 mod 4, so the units digit is 7.", ORIGINAL, ["1", "3", "9"]),
 ("Find the greatest integer that divides 83 and 125 leaving the same remainder in each case.", "42", "The common remainder r means the divisor divides both differences 83−r and 125−r, hence divides 42. The greatest possible divisor is 42; both leave remainder 41.", ORIGINAL, ["21", "41", "83"]),
 ("What is the smallest number by which 540 must be multiplied to make a perfect square?", "15", "540=2²·3³·5. Odd exponents of 3 and 5 need one more each, so multiply by 15.", ORIGINAL, ["3", "5", "30"]),
 ("How many trailing zeroes are in 250!?", "62", "⌊250/5⌋+⌊250/25⌋+⌊250/125⌋=50+10+2=62.", ORIGINAL, ["50", "60", "64"]),
 ("A number is divisible by 6 and 15. What is the least possible positive value?", "30", "A common multiple must be divisible by lcm(6,15)=30; 30 itself works.", ORIGINAL, ["15", "45", "60"]),
 ("Find the remainder when 7³⁰ is divided by 10.", "9", "Units digits of powers of 7 cycle 7,9,3,1 every four. 30≡2 mod 4, so the units digit and remainder are 9.", ORIGINAL, ["1", "3", "7"]),
 ("How many factors does 2⁴·3²·7 have?", "30", "The independent exponent choices give (4+1)(2+1)(1+1)=30 divisors.", ORIGINAL, ["24", "28", "36"]),
 ("Find the smallest positive integer n such that 3n is a perfect cube and n is a perfect square.", "9", "For n=3ᵉ to be a square, e is even; for 3n to be a cube, e+1 is divisible by 3. The least nonnegative even e satisfying this is 2, so n=9.", ORIGINAL, ["1", "6", "18"]),
 ("If N leaves remainder 4 when divided by 7, what remainder does 3N+5 leave when divided by 7?", "3", "Modulo 7, 3N+5≡3·4+5=17≡3.", ORIGINAL, ["1", "2", "4"]),
 ("What is the least digit x such that 47x2 is divisible by 3?", "2", "The digit sum is 13+x. Divisibility by 3 requires x≡2 (mod 3), whose least digit solution is 2.", ORIGINAL, ["0", "1", "5"]),
 ("How many trailing zeroes are in 75!?", "18", "⌊75/5⌋+⌊75/25⌋=15+3=18.", ORIGINAL, ["15", "17", "20"]),
 ("If a number leaves remainder 5 when divided by 8, what remainder does its square leave when divided by 8?", "1", "Write n≡5 mod 8; n²≡25≡1 mod 8.", ORIGINAL, ["3", "5", "7"]),
 ("Find the smallest number greater than 1,000 that is divisible by 12 and 18.", "1008", "lcm(12,18)=36. The first multiple of 36 above 1,000 is 36·28=1,008.", ORIGINAL, ["1002", "1016", "1036"]),
 ("Which is the least integer x for which 2, 3, and 5 all divide x+1 and x is positive?", "29", "x+1 must be a positive multiple of lcm(2,3,5)=30. The least positive x is 29.", ORIGINAL, ["30", "31", "59"]),
 ("What is the remainder when 1+2+…+50 is divided by 7?", "1", "The sum is 50·51/2=1,275; 1,275=7·182+1.", ORIGINAL, ["0", "2", "6"]),
 ("Find the units digit of 2¹⁰¹+3¹⁰¹.", "5", "2^n has cycle 2,4,8,6; 101≡1 gives 2. 3^n has cycle 3,9,7,1; 101≡1 gives 3. Sum units digit=5.", ORIGINAL, ["1", "3", "7"]),
 ("A positive integer has prime factorization 2³·5². How many of its divisors are multiples of 10?", "6", "A divisor multiple of 10 needs exponent at least one for both primes. There are 3 choices for the exponent of 2 and 2 for 5, hence 6.", ORIGINAL, ["4", "8", "10"]),
 ("What is the least number that must be subtracted from 1,003 to get a multiple of 17?", "0", "1,003=17·59 exactly, so it is already divisible by 17 and the least subtraction is zero.", ORIGINAL, ["1", "2", "14"]),
 ("If 4,5a2 is divisible by 9, find digit a.", "7", "The digit sum is 4+5+a+2=11+a; the only digit a making this a multiple of 9 is 7.", ORIGINAL, ["5", "6", "8"]),
]
HARD_ORIGINAL = [
 ("Find the remainder when 3¹⁰⁰ is divided by 13.", "3", "3³=27≡1 (mod 13), so 3¹⁰⁰=(3³)³³·3≡3 (mod 13).", ORIGINAL, ["4", "9", "12"]),
 ("How many positive divisors of 2⁵·3⁴·5² are perfect squares?", "18", "A square divisor uses even exponents: choices are 0,2,4 for 2 (3 choices), 0,2,4 for 3 (3), and 0,2 for 5 (2). Total 18.", ORIGINAL, ["15", "20", "24"]),
 ("Find the smallest positive integer k such that 2,520k is a perfect cube.", "3675", "2520=2³·3²·5·7. Complete all prime exponents to multiples of 3 by multiplying by 3·5²·7²=3,675.", ORIGINAL, ["105", "147", "735"]),
 ("How many trailing zeroes are in 1,000! when written in base 12?", "497", "A base-12 zero requires 2²·3. In 1000!, v₂=994 and v₃=498. The count is min(⌊994/2⌋,498)=497.", ORIGINAL, ["249", "498", "499"]),
 ("Find the remainder when 1!+2!+3!+…+10! is divided by 10.", "3", "For n≥5, n! ends in 0 and contributes remainder 0 mod 10. The units digits of 1! through 4! sum to 1+2+6+4=13, remainder 3.", ORIGINAL, ["0", "1", "4"]),
 ("How many positive integers less than 1,000 are divisible by 6 or 10, but not both?", "199", "There are 166 multiples of 6 and 99 of 10 below 1000; 33 are multiples of both (30). Exclusive count=(166−33)+(99−33)=199.", ORIGINAL, ["166", "198", "232"]),
 ("Find the last two digits of 7¹⁰⁰.", "01", "Modulo 100, 7⁴=2401≡1. Since 100 is divisible by 4, 7¹⁰⁰=(7⁴)²⁵≡1, so the last two digits are 01.", ORIGINAL, ["07", "21", "49"]),
 ("A number N is the least positive integer satisfying N≡2 (mod 5), N≡3 (mod 7), and N≡4 (mod 9). Find N.", "157", "Numbers congruent to 2 mod 5 and 3 mod 7 are 17+35t. Modulo 9, 17+35t≡8+8t≡4, so 8t≡5 (mod 9), giving t≡4. The least positive solution is 157.", ORIGINAL, ["122", "147", "192"]),
 ("How many positive divisors of 2⁶·3⁵·7² are divisible by 84?", "50", "84=2²·3·7. Divisor exponents have 5 choices for 2 (2–6), 5 for 3 (1–5), and 2 for 7 (1–2), giving 5·5·2=50.", ORIGINAL, ["40", "48", "60"]),
 ("Find the smallest positive integer n for which n! has at least 100 factors of 5.", "405", "For 405!, v₅=81+16+3=100; for every n≤404 the count is at most 80+16+3=99. Thus 405 is the least such n.", ORIGINAL, ["400", "404", "410"]),
 ("Find the least positive integer m such that 2m is a perfect square and 3m is a perfect cube.", "72", "For prime exponents e₂,e₃: e₂+1 is even, e₂ is 0 mod 3; e₃ is even and e₃+1 is 0 mod 3. Least exponents are e₂=3,e₃=2, so m=2³·3²=72.", ORIGINAL, ["36", "48", "144"]),
 ("Find the remainder when 10¹⁰⁰+10⁵⁰+1 is divided by 9.", "3", "10≡1 (mod 9), so the expression is congruent to 1+1+1=3 modulo 9.", ORIGINAL, ["1", "2", "4"]),
 ("How many positive divisors of 2⁴·3³·5² are not divisible by 15?", "30", "Total divisors=(5)(4)(3)=60. Divisors divisible by 15 require positive exponents of both 3 and 5: 5·3·2=30. Hence 60−30=30.", ORIGINAL, ["24", "36", "40"]),
 ("Find the smallest positive integer x such that 7x leaves remainder 1 when divided by 30.", "13", "7·13=91≡1 (mod 30); checking residues modulo 30 gives 13 as the least positive inverse of 7.", ORIGINAL, ["7", "17", "23"]),
 ("Find the remainder when 2¹⁰⁰+3¹⁰⁰ is divided by 5.", "2", "Modulo 5, 2⁴≡1 and 100≡0 mod 4, so 2¹⁰⁰≡1. Also 3⁴≡1, so 3¹⁰⁰≡1. Sum≡2.", ORIGINAL, ["0", "1", "4"]),
 ("How many integers from 1 through 500 are divisible by neither 2 nor 3?", "167", "By inclusion-exclusion, 500−⌊500/2⌋−⌊500/3⌋+⌊500/6⌋=500−250−166+83=167.", ORIGINAL, ["166", "168", "250"]),
 ("Find the units digit of 1!+2!+3!+…+25!.", "3", "Every n! for n≥5 ends in 0. The units digits of 1!+2!+3!+4! are 1+2+6+4=13, so the sum ends in 3.", ORIGINAL, ["0", "1", "4"]),
 ("How many positive divisors of 2⁵·3⁴·5³ are perfect cubes?", "8", "A cube divisor uses exponents divisible by 3. For each prime the allowed exponents are 0 or 3, giving 2·2·2=8 divisors.", ORIGINAL, ["12", "16", "24"]),
 ("Find the least positive integer n such that n is divisible by 18 and n² is divisible by 1,000.", "900", "18 requires n to contain 2·3². Since 1000=2³·5³ divides n², n needs at least 2²·5². Thus the least n is 2²·3²·5²=900.", ORIGINAL, ["180", "450", "1,800"]),
 ("Find the remainder when 4¹⁰⁰ is divided by 15.", "1", "4²=16≡1 (mod 15); 100 is even, so 4¹⁰⁰=(4²)⁵⁰≡1.", ORIGINAL, ["4", "9", "14"]),
 ("How many trailing zeroes are in 200! when represented in base 8?", "65", "A base-8 zero needs three factors of 2. v₂(200!)=100+50+25+12+6+3+1=197; ⌊197/3⌋=65.", ORIGINAL, ["49", "64", "66"]),
 ("Find the least positive integer N that leaves remainder 1 when divided by 2, 3, 4, 5, and 6, and is greater than 1.", "61", "N−1 must be divisible by lcm(2,3,4,5,6)=60. The least N>1 is 61.", ORIGINAL, ["31", "60", "121"]),
 ("How many divisors of 3⁶·5⁴ are divisible by 45?", "20", "45=3²·5. Exponents in a divisor must have 3-exponent 2–6 (5 choices) and 5-exponent 1–4 (4 choices), so 20.", ORIGINAL, ["16", "24", "25"]),
 ("Find the least positive integer whose square is divisible by 2⁶·3⁴·5³.", "1800", "For n² to contain the required prime powers, n needs exponents at least ⌈6/2⌉=3 for 2, ⌈4/2⌉=2 for 3, and ⌈3/2⌉=2 for 5. Thus n=2³·3²·5²=1,800.", ORIGINAL, ["900", "1200", "3600"]),
]

add("EASY", EASY_ORIGINAL)
add("MEDIUM", MEDIUM_ORIGINAL)
add("HARD", HARD_ORIGINAL)


def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def validate_generation():
    if len(ROWS) != 90 or Counter(row["difficulty"] for row in ROWS) != {"EASY":30,"MEDIUM":30,"HARD":30}:
        raise ValueError(f"Bad row count/distribution: {len(ROWS)}, {Counter(row['difficulty'] for row in ROWS)}")
    stems = [normalized(row["question_text"]) for row in ROWS]
    for i, stem in enumerate(stems):
        for prior in stems[:i]:
            if stem == prior or SequenceMatcher(None, stem, prior).ratio() >= .97:
                raise ValueError(f"Duplicate or near-verbatim stems: {stem!r} / {prior!r}")


validate_generation()
(BASE / "data" / "number_system_verified_batch.json").write_text(json.dumps({"questions":ROWS}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
(BASE / "data" / "number_system_answer_ledger.json").write_text(json.dumps(LEDGER, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print("Wrote", len(ROWS), "questions", dict(Counter(row["difficulty"] for row in ROWS)),
      "sources", sum(row["source"] != ORIGINAL for row in ROWS), "original", sum(row["source"] == ORIGINAL for row in ROWS))
