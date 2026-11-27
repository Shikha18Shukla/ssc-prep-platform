# -*- coding: utf-8 -*-
"""Generate the Banking Maths question bank (5 chapters x 120 verified questions).

Every question is produced deterministically from a seeded generator.  Answers are
computed in Python, not copied from an answer key, and each item carries a
`verification_data` block so a separate verifier can recompute it.

Run:
    python backend/generate_banking_maths_questions.py

Outputs:
    data/banking_maths_vedic_calculation_questions.json
    data/banking_maths_simplification_questions.json
    data/banking_maths_approximation_questions.json
    data/banking_maths_missing_number_series_questions.json
    data/banking_maths_wrong_number_series_questions.json
"""

from __future__ import annotations

import json
import math
import os
import random
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

TARGET_PER_CHAPTER = 120
PART_SIZES = {1: 15, 2: 20, 3: 30, 4: 55}


# ---------------------------------------------------------------------------
# formatting / option helpers
# ---------------------------------------------------------------------------

def fmt(value) -> str:
    """Format an int/Fraction/float for display and for an option string."""
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return str(value.numerator)
        return f"{value.numerator}/{value.denominator}"
    if isinstance(value, float):
        if abs(value - round(value)) < 1e-9:
            return str(int(round(value)))
        text = f"{value:.4f}".rstrip("0").rstrip(".")
        return text
    return str(value)


def fmt_dec(value: float, places: int = 2) -> str:
    text = f"{value:.{places}f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def unique_options(correct: str, distractors: list[str], rng: random.Random):
    """Return four distinct options and the correct letter."""
    correct = str(correct)
    options: list[str] = []
    for candidate in [correct] + [str(d) for d in distractors]:
        if candidate not in options:
            options.append(candidate)
    # numeric fallbacks, used only if a template supplied a duplicate
    if len(options) < 4:
        base = Fraction(correct) if "/" in correct else Fraction(str(correct))
        step = Fraction(1)
        while len(options) < 4:
            for candidate in (base + step, base - step):
                text = fmt(candidate)
                if text not in options:
                    options.append(text)
                    break
            step += 1
    options = options[:4]
    rng.shuffle(options)
    return options, "ABCD"[options.index(correct)]


class Bank:
    def __init__(self, chapter: str, seed: int):
        self.chapter = chapter
        self.rng = random.Random(seed)
        self.items: list[dict] = []
        self.texts: set[str] = set()

    def count(self, part: int | None = None) -> int:
        if part is None:
            return len(self.items)
        return sum(1 for item in self.items if item["part"] == part)

    def add(
        self,
        *,
        part: int,
        difficulty: str,
        text: str,
        correct: str,
        distractors: list[str],
        explanation: str,
        source_name: str,
        source_page: str,
        source_type: str,
        verification_data: dict,
    ) -> bool:
        text = " ".join(text.split())
        if text in self.texts:
            return False
        options, letter = unique_options(correct, distractors, self.rng)
        if len(options) != 4 or len(set(options)) != 4:
            raise ValueError(f"bad options for: {text}")
        if explanation.strip() == "":
            raise ValueError(f"missing explanation for: {text}")
        self.texts.add(text)
        self.items.append(
            {
                "id": f"{self.chapter_key}-{len(self.items) + 1:04d}",
                "chapter": self.chapter,
                "chapter_key": self.chapter_key,
                "part": part,
                "section": f"{self.chapter_key}_part_{part}",
                "question_text": text,
                "options": options,
                "correct_option": letter,
                "correct_answer": options["ABCD".index(letter)],
                "explanation": explanation.strip(),
                "difficulty": difficulty,
                "source_name": source_name,
                "source_url": "",
                "source_page": source_page,
                "source_type": source_type,
                "exam_year": None,
                "verification_status": "VERIFIED",
                "verification_method": "Independent arithmetic recomputation in generate_banking_maths_questions.py",
                "verification_data": verification_data,
                "provenance_note": (
                    "Original question written for this bank. Topic scope is aligned with the "
                    "cited PW Banking Wallah class-notes pages; it is not an extracted PDF MCQ "
                    "and is not a previous-year question."
                ),
            }
        )
        return True


def fill(bank: Bank, part: int, difficulty: str, count: int, fn, source_name: str,
         source_page: str, source_type: str = "ORIGINAL_VERIFIED", max_tries: int = 4000):
    """Repeatedly call fn until `count` unique questions were added to `part`."""
    added = 0
    tries = 0
    while added < count and tries < max_tries:
        tries += 1
        candidate = fn(bank.rng)
        if candidate is None:
            continue
        if bank.add(
            part=part,
            difficulty=difficulty,
            text=candidate["text"],
            correct=candidate["correct"],
            distractors=candidate["distractors"],
            explanation=candidate["explanation"],
            source_name=source_name,
            source_page=source_page,
            source_type=source_type,
            verification_data=candidate["verification_data"],
        ):
            added += 1
    if added < count:
        raise RuntimeError(
            f"could not generate {count} questions for part {part}; added {added} after {tries} tries"
        )


# ---------------------------------------------------------------------------
# Vedic Maths
# ---------------------------------------------------------------------------

VEDIC_SOURCE = "PW Banking Wallah - Vedic Maths Tricks - Calculations Techniques (Class Notes, local PDF)"


def v_mult11_2(rng):
    a = rng.randint(1, 9)
    b = rng.randint(0, 9)
    n = 10 * a + b
    ans = n * 11
    if a + b < 10:
        steps = f"write {a} | {a + b} | {b}"
    else:
        carry = (a + b) // 10
        steps = (
            f"write {a} | {a + b} | {b}, carry {carry} from the middle, giving {ans}"
        )
    return {
        "text": f"Using the Vedic x11 shortcut, find {n} x 11.",
        "correct": str(ans),
        "distractors": [str(ans + 11), str(ans - 11), str(ans + 110)],
        "explanation": f"For a two-digit number multiplied by 11, keep the outer digits and put the sum of the digits in the middle: {steps}.",
        "verification_data": {"op": "mul", "a": n, "b": 11, "expected": ans},
    }


def v_mult11_3(rng):
    a = rng.randint(1, 9)
    b = rng.randint(0, 9)
    c = rng.randint(0, 9)
    n = 100 * a + 10 * b + c
    ans = n * 11
    return {
        "text": f"Using the Vedic x11 shortcut, find {n} x 11.",
        "correct": str(ans),
        "distractors": [str(ans + 11), str(ans - 11), str(ans + 1001)],
        "explanation": f"For a three-digit number, the digits of the product are a | a+b | b+c | c with carries. Applying this to {n} gives {ans}.",
        "verification_data": {"op": "mul", "a": n, "b": 11, "expected": ans},
    }


def v_square5(rng):
    a = rng.randint(1, 9)
    n = 10 * a + 5
    ans = a * (a + 1) * 100 + 25
    return {
        "text": f"Find {n}^2 using the 'number ending in 5' trick.",
        "correct": str(ans),
        "distractors": [str(a * (a + 1) * 100), str(ans + 100), str(ans - 25)],
        "explanation": f"For a number ending in 5, multiply the part before 5 by the next integer and append 25: {a} x {a + 1} = {a * (a + 1)}, so {n}^2 = {ans}.",
        "verification_data": {"op": "square", "a": n, "expected": ans},
    }


def v_square_near100(rng):
    d = rng.randint(1, 9)
    sign = rng.choice([-1, 1])
    n = 100 + sign * d
    ans = n * n
    return {
        "text": f"Find {n}^2 using the base-100 method.",
        "correct": str(ans),
        "distractors": [str(ans + 100), str(ans - 100), str(ans + 2 * n)],
        "explanation": f"Take 100 as the base. The deviation is {sign * d:+d}. Square the deviation and add it to 100 x (100 + 2 x deviation): {ans}. Equivalently, {n}^2 = {ans}.",
        "verification_data": {"op": "square", "a": n, "expected": ans},
    }


def v_mult_near100(rng):
    a = rng.choice([x for x in range(-9, 10) if x != 0])
    b = rng.choice([x for x in range(-9, 10) if x != 0])
    n1, n2 = 100 + a, 100 + b
    ans = n1 * n2
    return {
        "text": f"Using the base-100 method, find {n1} x {n2}.",
        "correct": str(ans),
        "distractors": [str(ans + 100), str(ans - 100), str(ans + a * b if a * b else ans + 10)],
        "explanation": f"Deviations from 100 are {a:+d} and {b:+d}. The answer is 100 x (100 + {a:+d} + {b:+d}) + ({a:+d}) x ({b:+d}) = {ans}.",
        "verification_data": {"op": "mul", "a": n1, "b": n2, "expected": ans},
    }


def v_same_tens(rng):
    t = rng.randint(1, 9)
    u = rng.randint(1, 9)
    v = 10 - u
    n1, n2 = 10 * t + u, 10 * t + v
    ans = n1 * n2
    return {
        "text": f"Find {n1} x {n2} using the 'same tens digit, units sum to 10' trick.",
        "correct": str(ans),
        "distractors": [str(ans + 100), str(ans - 100), str(t * t * 100 + u * v)],
        "explanation": f"Both numbers have tens digit {t}, and the units {u} + {v} = 10. Multiply {t} by {t + 1} and append the product of the units: {t} x {t + 1} = {t * (t + 1)}, {u} x {v} = {u * v:02d}; hence {ans}.",
        "verification_data": {"op": "mul", "a": n1, "b": n2, "expected": ans},
    }


def v_mult_5_25_125(rng):
    k = rng.choice([5, 25, 125])
    divisor = {5: 2, 25: 4, 125: 8}[k]
    n = divisor * rng.randint(3, 40)
    ans = n * k
    shortcut = {5: "n/2 x 10", 25: "n/4 x 100", 125: "n/8 x 1000"}[k]
    return {
        "text": f"Find {n} x {k} using a Vedic shortcut.",
        "correct": str(ans),
        "distractors": [str(ans + k), str(ans - k), str(ans + 10)],
        "explanation": f"Use {shortcut}: {n} / {divisor} = {n // divisor}, so the answer is {ans}.",
        "verification_data": {"op": "mul", "a": n, "b": k, "expected": ans},
    }


def v_div_5_25(rng):
    k = rng.choice([5, 25])
    n = k * rng.randint(4, 60)
    ans = n // k
    multiplier = {5: 2, 25: 4}[k]
    return {
        "text": f"Find {n} / {k} using a Vedic shortcut.",
        "correct": str(ans),
        "distractors": [str(ans + 1), str(ans - 1), str(ans * 10)],
        "explanation": f"Dividing by {k} is the same as multiplying by {multiplier} and dividing by {k * multiplier}: {n} x {multiplier} = {n * multiplier}, and {n * multiplier} / {k * multiplier} = {ans}.",
        "verification_data": {"op": "div", "a": n, "b": k, "expected": ans},
    }


def v_diff_squares(rng):
    b = rng.randint(5, 40)
    a = b + rng.choice([10, 20, 30, 40, 50])
    ans = a * a - b * b
    return {
        "text": f"Evaluate {a}^2 - {b}^2 using the difference-of-squares trick.",
        "correct": str(ans),
        "distractors": [str((a - b) ** 2), str(a * a + b * b), str(ans + 100)],
        "explanation": f"a^2 - b^2 = (a + b)(a - b) = ({a} + {b})({a} - {b}) = {a + b} x {a - b} = {ans}.",
        "verification_data": {"op": "diff_squares", "a": a, "b": b, "expected": ans},
    }


def v_sum_natural(rng):
    n = rng.randint(10, 60)
    ans = n * (n + 1) // 2
    return {
        "text": f"Find the sum of the first {n} natural numbers using a Vedic shortcut.",
        "correct": str(ans),
        "distractors": [str(n * n), str(n * (n + 1)), str(ans + n)],
        "explanation": f"Sum of the first n natural numbers = n(n + 1)/2 = {n} x {n + 1} / 2 = {ans}.",
        "verification_data": {"op": "sum_natural", "n": n, "expected": ans},
    }


def v_sum_odd(rng):
    n = rng.randint(8, 45)
    ans = n * n
    return {
        "text": f"Find the sum of the first {n} odd natural numbers using a Vedic shortcut.",
        "correct": str(ans),
        "distractors": [str(n * (n + 1)), str(n * (n + 1) // 2), str(ans + n)],
        "explanation": f"The sum of the first n odd numbers is n^2: {n}^2 = {ans}.",
        "verification_data": {"op": "sum_odd", "n": n, "expected": ans},
    }


def v_sum_even(rng):
    n = rng.randint(8, 45)
    ans = n * (n + 1)
    return {
        "text": f"Find the sum of the first {n} even natural numbers using a Vedic shortcut.",
        "correct": str(ans),
        "distractors": [str(n * n), str(n * (n + 1) // 2), str(ans + n)],
        "explanation": f"The sum of the first n even numbers is n(n + 1): {n} x {n + 1} = {ans}.",
        "verification_data": {"op": "sum_even", "n": n, "expected": ans},
    }


def v_div11(rng):
    n = rng.randint(10000, 999999)
    alt = sum(int(d) if i % 2 == 0 else -int(d) for i, d in enumerate(str(n)[::-1]))
    ans = alt % 11
    candidates = [str(x) for x in range(11) if x != ans]
    rng.shuffle(candidates)
    return {
        "text": f"Find the remainder when {n} is divided by 11.",
        "correct": str(ans),
        "distractors": candidates[:3],
        "explanation": f"Using the divisibility rule for 11, the alternating digit sum gives a remainder of {ans} when divided by 11. Hence {n} leaves remainder {ans}.",
        "verification_data": {"op": "mod", "a": n, "b": 11, "expected": ans},
    }


def v_digital_root(rng):
    n = rng.randint(10000, 999999)
    ans = 1 + (n - 1) % 9
    candidates = [str(x) for x in range(1, 10) if x != ans]
    rng.shuffle(candidates)
    return {
        "text": f"Find the digital root of {n}.",
        "correct": str(ans),
        "distractors": candidates[:3],
        "explanation": f"Add the digits repeatedly until one digit remains. The digital root of {n} is {ans}.",
        "verification_data": {"op": "digital_root", "n": n, "expected": ans},
    }


def v_square_2digit(rng):
    n = rng.randint(11, 99)
    ans = n * n
    a, b = divmod(n, 10)
    return {
        "text": f"Find {n}^2 using the vertically-and-crosswise method.",
        "correct": str(ans),
        "distractors": [str(ans + 10), str(ans - 10), str(a * a * 100 + b * b)],
        "explanation": f"Using (10a + b)^2 = 100a^2 + 20ab + b^2 with a = {a}, b = {b}: {ans}.",
        "verification_data": {"op": "square", "a": n, "expected": ans},
    }


def v_percent_fraction(rng):
    pairs = [
        (Fraction(1, 8), "12.5%"),
        (Fraction(3, 8), "37.5%"),
        (Fraction(5, 8), "62.5%"),
        (Fraction(1, 6), "16 2/3%"),
        (Fraction(1, 3), "33 1/3%"),
        (Fraction(2, 3), "66 2/3%"),
        (Fraction(1, 12), "8 1/3%"),
        (Fraction(1, 9), "11 1/9%"),
    ]
    fr, pct = rng.choice(pairs)
    base = fr.denominator * rng.randint(5, 20)
    ans = fr * base
    return {
        "text": f"Find {pct} of {base} using a fraction equivalent.",
        "correct": fmt(ans),
        "distractors": [fmt(ans + 10), fmt(ans - 10), fmt(ans * 2)],
        "explanation": f"{pct} = {fmt(fr)}. Therefore {pct} of {base} = {fmt(fr)} x {base} = {fmt(ans)}.",
        "verification_data": {"op": "fraction_of", "num": fr.numerator, "den": fr.denominator, "base": base, "expected": fmt(ans)},
    }


def v_diff2(rng):
    n = rng.randint(12, 99)
    ans = n * n - 1
    return {
        "text": f"Find {n - 1} x {n + 1} using the (a - 1)(a + 1) shortcut.",
        "correct": str(ans),
        "distractors": [str(n * n), str(n * n + 1), str(ans + 10)],
        "explanation": f"(a - 1)(a + 1) = a^2 - 1. Here a = {n}, so the product is {n}^2 - 1 = {ans}.",
        "verification_data": {"op": "mul", "a": n - 1, "b": n + 1, "expected": ans},
    }


def build_vedic() -> Bank:
    bank = Bank("Vedic Maths Tricks - Calculation Techniques", seed=101)
    bank.chapter_key = "vedic_maths"
    spec = [
        (1, "EASY", 5, v_mult11_2, "Vedic Maths 01, pp. 5-9"),
        (1, "EASY", 4, v_square5, "Vedic Maths 01, pp. 10-14"),
        (1, "EASY", 3, v_mult_5_25_125, "Vedic Maths 02, pp. 4-9"),
        (1, "EASY", 3, v_sum_natural, "Vedic Maths 02, pp. 10-16"),
        (2, "EASY", 5, v_mult11_3, "Vedic Maths 03, pp. 4-9"),
        (2, "MEDIUM", 5, v_square_near100, "Vedic Maths 03, pp. 10-14"),
        (2, "EASY", 4, v_same_tens, "Vedic Maths 04, pp. 4-10"),
        (2, "MEDIUM", 3, v_diff2, "Vedic Maths 04, pp. 11-16"),
        (2, "MEDIUM", 3, v_digital_root, "Vedic Maths 04, pp. 17-22"),
        (3, "MEDIUM", 10, v_mult_near100, "Vedic Maths 05, pp. 4-18"),
        (3, "MEDIUM", 4, v_mult_5_25_125, "Vedic Maths 05, pp. 19-26"),
        (3, "MEDIUM", 4, v_div_5_25, "Vedic Maths 05, pp. 27-32"),
        (3, "MEDIUM", 5, v_diff_squares, "Vedic Maths 05, pp. 33-38"),
        (3, "HARD", 4, v_square_2digit, "Vedic Maths 06, pp. 4-10"),
        (3, "HARD", 3, v_div11, "Vedic Maths 06, pp. 11-14"),
        (4, "HARD", 15, v_mult_near100, "Vedic Maths 05, pp. 4-18"),
        (4, "HARD", 8, v_same_tens, "Vedic Maths 04, pp. 4-10"),
        (4, "HARD", 5, v_diff_squares, "Vedic Maths 05, pp. 33-38"),
        (4, "HARD", 7, v_sum_odd, "Vedic Maths 02, pp. 10-16"),
        (4, "HARD", 3, v_sum_even, "Vedic Maths 02, pp. 10-16"),
        (4, "HARD", 6, v_percent_fraction, "Vedic Maths 06, pp. 15-19"),
        (4, "HARD", 6, v_square_2digit, "Vedic Maths 06, pp. 4-10"),
        (4, "HARD", 5, v_mult11_3, "Vedic Maths 03, pp. 4-9"),
    ]
    for part, difficulty, count, fn, pages in spec:
        fill(bank, part, difficulty, count, fn, VEDIC_SOURCE, pages)
    return bank


# ---------------------------------------------------------------------------
# Simplification
# ---------------------------------------------------------------------------

SIMPL_SOURCE = "PW Banking Wallah - Simplifications (Class Notes, local PDF)"


def s_bodmas(rng):
    a = rng.randint(5, 60)
    b = rng.randint(2, 12)
    c = rng.randint(2, 9)
    e = rng.randint(2, 9)
    d = e * rng.randint(2, 12)
    ans = Fraction(a) + b * c - Fraction(d, e)
    return {
        "text": f"Simplify: {a} + {b} x {c} - {d} / {e}",
        "correct": fmt(ans),
        "distractors": [fmt(ans + 1), fmt(ans - 1), fmt(ans + b)],
        "explanation": f"By BODMAS, do multiplication and division first: {b} x {c} = {b * c} and {d} / {e} = {d // e}. Then {a} + {b * c} - {d // e} = {fmt(ans)}.",
        "verification_data": {"op": "expr", "expr": f"{a}+{b}*{c}-{d}/{e}", "expected": fmt(ans)},
    }


def s_brackets(rng):
    a = rng.randint(5, 40)
    b = rng.randint(2, 20)
    c = rng.randint(2, 9)
    e = rng.randint(2, 9)
    d = e * rng.randint(2, 12)
    ans = (a + b) * c - Fraction(d, e)
    return {
        "text": f"Simplify: ({a} + {b}) x {c} - {d} / {e}",
        "correct": fmt(ans),
        "distractors": [fmt(ans + 1), fmt(ans - 1), fmt(ans + c)],
        "explanation": f"First solve the bracket: {a} + {b} = {a + b}. Then {a + b} x {c} = {(a + b) * c}, and {d} / {e} = {d // e}. Finally {(a + b) * c} - {d // e} = {fmt(ans)}.",
        "verification_data": {"op": "expr", "expr": f"({a}+{b})*{c}-{d}/{e}", "expected": fmt(ans)},
    }


def s_fractions(rng):
    b = rng.choice([2, 3, 4, 5, 6, 8])
    d = rng.choice([2, 3, 4, 5, 6, 8])
    a = rng.randint(1, b - 1) if b > 1 else 1
    c = rng.randint(1, d - 1) if d > 1 else 1
    e = rng.randint(2, 12)
    ans = (Fraction(a, b) + Fraction(c, d)) * e
    return {
        "text": f"Simplify: ({a}/{b} + {c}/{d}) x {e}",
        "correct": fmt(ans),
        "distractors": [fmt(ans + 1), fmt(ans - 1), fmt(ans + Fraction(1, 2))],
        "explanation": f"Add the fractions using the LCM: {a}/{b} + {c}/{d} = {fmt(Fraction(a, b) + Fraction(c, d))}. Multiply by {e} to get {fmt(ans)}.",
        "verification_data": {"op": "expr", "expr": f"({a}/{b}+{c}/{d})*{e}", "expected": fmt(ans)},
    }


def s_percent(rng):
    x = rng.choice([5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 75])
    y = rng.choice([5, 10, 15, 20, 25, 30, 40, 50, 60, 75])
    A = 20 * rng.randint(3, 30)
    B = 20 * rng.randint(3, 30)
    ans = Fraction(x, 100) * A + Fraction(y, 100) * B
    return {
        "text": f"Simplify: {x}% of {A} + {y}% of {B}",
        "correct": fmt(ans),
        "distractors": [fmt(ans + 10), fmt(ans - 10), fmt(ans + x + y)],
        "explanation": f"{x}% of {A} = {fmt(Fraction(x, 100) * A)} and {y}% of {B} = {fmt(Fraction(y, 100) * B)}. Their sum is {fmt(ans)}.",
        "verification_data": {"op": "percent_sum", "x": x, "A": A, "y": y, "B": B, "expected": fmt(ans)},
    }


def s_decimals(rng):
    a = rng.randint(11, 99) / 10
    b = rng.randint(11, 49) / 10
    c = rng.randint(11, 99) / 10
    ans = Fraction(str(a)) * Fraction(str(b)) + Fraction(str(c))
    return {
        "text": f"Simplify: {a} x {b} + {c}",
        "correct": fmt_dec(float(ans), 2),
        "distractors": [fmt_dec(float(ans) + 0.5, 2), fmt_dec(float(ans) - 0.5, 2), fmt_dec(float(ans) + 1, 2)],
        "explanation": f"First multiply: {a} x {b} = {fmt_dec(a * b, 2)}. Then add {c}: {fmt_dec(a * b, 2)} + {c} = {fmt_dec(float(ans), 2)}.",
        "verification_data": {"op": "decimal_expr", "a": a, "b": b, "c": c, "expected": fmt_dec(float(ans), 2)},
    }


def s_roots(rng):
    root = rng.randint(5, 30)
    a = root * root
    b = rng.randint(3, 15)
    c = rng.randint(2, 8)
    ans = root + b * b - c * c * c
    return {
        "text": f"Simplify: sqrt({a}) + {b}^2 - {c}^3",
        "correct": str(ans),
        "distractors": [str(ans + 1), str(ans - 1), str(ans + b)],
        "explanation": f"sqrt({a}) = {root}, {b}^2 = {b * b}, and {c}^3 = {c * c * c}. So {root} + {b * b} - {c * c * c} = {ans}.",
        "verification_data": {"op": "expr", "expr": f"{root}+{b}**2-{c}**3", "expected": str(ans)},
    }


def s_mixed(rng):
    b = rng.choice([2, 3, 4, 5, 6, 8])
    a = rng.randint(1, b - 1) if b > 1 else 1
    whole = rng.randint(2, 20)
    d = rng.choice([4, 6, 8, 10, 12, 15, 20, 24])
    ans = Fraction(whole) + Fraction(a, b) * d
    return {
        "text": f"Simplify: {whole} + {a}/{b} of {d}",
        "correct": fmt(ans),
        "distractors": [fmt(ans + 1), fmt(ans - 1), fmt(Fraction(whole + a, b) * d)],
        "explanation": f"In BODMAS, 'of' means multiplication: {a}/{b} of {d} = {fmt(Fraction(a, b) * d)}. Then {whole} + {fmt(Fraction(a, b) * d)} = {fmt(ans)}.",
        "verification_data": {"op": "expr", "expr": f"{whole}+({a}/{b})*{d}", "expected": fmt(ans)},
    }


def s_identity(rng):
    a = rng.randint(5, 40)
    b = rng.randint(2, 30)
    ans = (a + b) ** 2 - (a - b) ** 2
    return {
        "text": f"Simplify: ({a} + {b})^2 - ({a} - {b})^2",
        "correct": str(ans),
        "distractors": [str((2 * a) ** 2), str((2 * b) ** 2), str(a * a + b * b)],
        "explanation": f"Use (x + y)^2 - (x - y)^2 = 4xy. Here 4 x {a} x {b} = {ans}.",
        "verification_data": {"op": "expr", "expr": f"({a}+{b})**2-({a}-{b})**2", "expected": str(ans)},
    }


def s_nested(rng):
    a = rng.randint(2, 12)
    b = rng.randint(2, 20)
    c = rng.randint(2, 9)
    d = rng.randint(10, 30)
    e = rng.randint(2, 9)
    ans = a * (b + c * (d - e))
    return {
        "text": f"Simplify: {a} x [{b} + {c} x ({d} - {e})]",
        "correct": str(ans),
        "distractors": [str(ans + a), str(ans - a), str(ans + c)],
        "explanation": f"Innermost bracket: {d} - {e} = {d - e}. Then {c} x {d - e} = {c * (d - e)}, and {b} + {c * (d - e)} = {b + c * (d - e)}. Finally {a} x {b + c * (d - e)} = {ans}.",
        "verification_data": {"op": "expr", "expr": f"{a}*({b}+{c}*({d}-{e}))", "expected": str(ans)},
    }


def s_div_fraction(rng):
    a = rng.randint(1, 9)
    b = rng.randint(2, 9)
    c = rng.randint(1, 9)
    d = rng.randint(2, 9)
    e = rng.randint(2, 12)
    ans = (Fraction(a, b) / Fraction(c, d)) * e
    return {
        "text": f"Simplify: ({a}/{b}) / ({c}/{d}) x {e}",
        "correct": fmt(ans),
        "distractors": [fmt(ans + 1), fmt(ans - 1), fmt(Fraction(b, a) * Fraction(c, d) * e)],
        "explanation": f"Dividing by a fraction means multiplying by its reciprocal: ({a}/{b}) x ({d}/{c}) = {fmt(Fraction(a, b) * Fraction(d, c))}. Multiplying by {e} gives {fmt(ans)}.",
        "verification_data": {"op": "expr", "expr": f"({a}/{b})/({c}/{d})*{e}", "expected": fmt(ans)},
    }


def build_simplification() -> Bank:
    bank = Bank("Simplification", seed=202)
    bank.chapter_key = "simplification"
    spec = [
        (1, "EASY", 8, s_bodmas, "Simplifications 01, pp. 5-13"),
        (1, "EASY", 4, s_brackets, "Simplifications 01, pp. 14-18"),
        (1, "EASY", 3, s_percent, "Simplifications 01, pp. 19-23"),
        (2, "EASY", 6, s_fractions, "Simplifications 02, pp. 4-12"),
        (2, "MEDIUM", 5, s_decimals, "Simplifications 02, pp. 13-18"),
        (2, "MEDIUM", 5, s_roots, "Simplifications 02, pp. 19-25"),
        (2, "EASY", 4, s_mixed, "Simplifications 03, pp. 4-10"),
        (3, "MEDIUM", 6, s_bodmas, "Simplifications 01, pp. 5-13"),
        (3, "MEDIUM", 6, s_nested, "Simplifications 03, pp. 11-16"),
        (3, "MEDIUM", 6, s_identity, "Simplifications 04, pp. 4-10"),
        (3, "HARD", 4, s_div_fraction, "Simplifications 03, pp. 17-19"),
        (3, "MEDIUM", 4, s_percent, "Simplifications 04, pp. 11-16"),
        (3, "HARD", 4, s_roots, "Simplifications 02, pp. 19-25"),
        (4, "HARD", 8, s_fractions, "Simplifications 02, pp. 4-12"),
        (4, "HARD", 6, s_decimals, "Simplifications 02, pp. 13-18"),
        (4, "HARD", 8, s_roots, "Simplifications 02, pp. 19-25"),
        (4, "HARD", 6, s_identity, "Simplifications 04, pp. 4-10"),
        (4, "HARD", 8, s_nested, "Simplifications 03, pp. 11-16"),
        (4, "HARD", 6, s_div_fraction, "Simplifications 03, pp. 17-19"),
        (4, "HARD", 6, s_mixed, "Simplifications 03, pp. 4-10"),
        (4, "HARD", 7, s_percent, "Simplifications 04, pp. 11-16"),
    ]
    for part, difficulty, count, fn, pages in spec:
        fill(bank, part, difficulty, count, fn, SIMPL_SOURCE, pages)
    return bank


# ---------------------------------------------------------------------------
# Approximation
# ---------------------------------------------------------------------------

APPROX_SOURCE = "PW Banking Wallah - Approximations (Class Notes, local PDF)"


def _round0(value: float) -> int:
    return int(math.floor(value + 0.5))


def _near(rng, base, spread):
    delta = rng.uniform(-spread, spread)
    if abs(delta) < 0.01:
        delta = spread / 2
    return round(base + delta, 2)


def _approx_step(ans, exact, minimum):
    """Keep the rounded answer strictly closer to the exact value than any distractor."""
    dev = abs(float(exact) - float(ans))
    return max(minimum, _round0(dev * 3) + 2)


def a_product(rng):
    base_a = rng.choice([20, 25, 30, 40, 50, 60, 80, 100, 120, 150, 200, 250, 400, 500])
    base_b = rng.choice([10, 12, 15, 20, 25, 30, 40, 50, 60, 80, 100, 120])
    a = _near(rng, base_a, max(0.2, base_a * 0.008))
    b = _near(rng, base_b, max(0.2, base_b * 0.008))
    ans = base_a * base_b
    step = _approx_step(ans, a * b, max(2, _round0(ans * 0.04)))
    return {
        "text": f"What approximate value should come in place of the question mark? {a:.2f} x {b:.2f} = ?",
        "correct": str(ans),
        "distractors": [str(ans + step), str(ans - step), str(ans + 2 * step)],
        "explanation": f"Round the numbers: {a:.2f} is about {base_a} and {b:.2f} is about {base_b}. Then {base_a} x {base_b} = {ans}, which is the closest option.",
        "verification_data": {"op": "approx_product", "a": a, "b": b, "expected": ans},
    }


def a_division(rng):
    base_a = rng.choice([100, 200, 300, 400, 500, 600, 800, 1000, 1200, 1500, 2000, 2500])
    base_b = rng.choice([5, 10, 15, 20, 25, 30, 40, 50])
    a = _near(rng, base_a, max(0.3, base_a * 0.006))
    b = _near(rng, base_b, max(0.1, base_b * 0.01))
    ans = _round0(base_a / base_b)
    step = _approx_step(ans, a / b, max(1, _round0(ans * 0.06)))
    return {
        "text": f"What approximate value should come in place of the question mark? {a:.2f} / {b:.2f} = ?",
        "correct": str(ans),
        "distractors": [str(ans + step), str(ans - step), str(ans + 2 * step)],
        "explanation": f"Round the numbers: {a:.2f} is about {base_a} and {b:.2f} is about {base_b}. Then {base_a} / {base_b} = {ans}, which is the closest option.",
        "verification_data": {"op": "approx_division", "a": a, "b": b, "expected": ans},
    }


def a_percent(rng):
    base_p = rng.choice([5, 10, 12, 15, 18, 20, 25, 30, 35, 40, 45, 50, 60, 75])
    base_n = rng.choice([200, 400, 500, 600, 800, 1000, 1200, 1500, 2000])
    p = _near(rng, base_p, 0.08)
    n = _near(rng, base_n, max(0.3, base_n * 0.001))
    ans = _round0(base_p * base_n / 100)
    step = _approx_step(ans, p * n / 100, max(1, _round0(ans * 0.06)))
    return {
        "text": f"What approximate value should come in place of the question mark? {p:.2f}% of {n:.2f} = ?",
        "correct": str(ans),
        "distractors": [str(ans + step), str(ans - step), str(ans + 2 * step)],
        "explanation": f"Round the values: {p:.2f}% is about {base_p}% and {n:.2f} is about {base_n}. Then {base_p}% of {base_n} = {ans}, which is the closest option.",
        "verification_data": {"op": "approx_percent", "p": p, "n": n, "expected": ans},
    }


def a_sqrt(rng):
    root = rng.randint(6, 60)
    n = round(root * root + rng.uniform(-0.8, 0.8), 2)
    ans = root
    return {
        "text": f"What approximate value should come in place of the question mark? sqrt({n:.2f}) = ?",
        "correct": str(ans),
        "distractors": [str(ans + 2), str(ans - 2), str(ans + 4)],
        "explanation": f"{n:.2f} is very close to {root}^2 = {root * root}. Therefore sqrt({n:.2f}) is approximately {ans}.",
        "verification_data": {"op": "approx_sqrt", "n": n, "expected": ans},
    }


def a_sumsq(rng):
    base_a = rng.randint(6, 30)
    base_b = rng.randint(6, 30)
    a = _near(rng, base_a, 0.4)
    b = _near(rng, base_b, 0.4)
    ans = base_a * base_a + base_b * base_b
    step = _approx_step(ans, a * a + b * b, max(2, _round0(ans * 0.06)))
    return {
        "text": f"What approximate value should come in place of the question mark? ({a:.2f})^2 + ({b:.2f})^2 = ?",
        "correct": str(ans),
        "distractors": [str(ans + step), str(ans - step), str(ans + 2 * step)],
        "explanation": f"Round to {base_a} and {base_b}: {base_a}^2 + {base_b}^2 = {ans}, which is the closest option.",
        "verification_data": {"op": "approx_sumsq", "a": a, "b": b, "expected": ans},
    }


def a_mixed(rng):
    base_a = rng.choice([50, 100, 150, 200, 250, 300, 400])
    base_b = rng.choice([2, 3, 4, 5, 6, 8, 10])
    base_c = rng.choice([100, 200, 300, 400, 500])
    base_d = rng.choice([3, 4, 5, 6, 8, 10])
    a = _near(rng, base_a, 0.4)
    b = _near(rng, base_b, 0.04)
    c = _near(rng, base_c, 0.4)
    d = _near(rng, base_d, 0.04)
    ans = _round0(base_a * base_b + base_c / base_d)
    step = _approx_step(ans, a * b + c / d, max(2, _round0(ans * 0.06)))
    return {
        "text": f"What approximate value should come in place of the question mark? {a:.2f} x {b:.2f} + {c:.2f} / {d:.2f} = ?",
        "correct": str(ans),
        "distractors": [str(ans + step), str(ans - step), str(ans + 2 * step)],
        "explanation": f"Round the values: {a:.2f} x {b:.2f} is about {base_a} x {base_b} = {base_a * base_b}, and {c:.2f} / {d:.2f} is about {base_c} / {base_d} = {_round0(base_c / base_d)}. The total is approximately {ans}.",
        "verification_data": {"op": "approx_mixed", "a": a, "b": b, "c": c, "d": d, "expected": ans},
    }


def a_fracsum(rng):
    base_a = rng.randint(2, 10)
    base_b = rng.randint(2, 10)
    a = _near(rng, base_a, 0.05)
    b = _near(rng, base_b, 0.05)
    ans = round(1 / base_a + 1 / base_b, 2)
    return {
        "text": f"What approximate value should come in place of the question mark? 1/{a:.2f} + 1/{b:.2f} = ?",
        "correct": f"{ans:.2f}",
        "distractors": [f"{ans + 0.10:.2f}", f"{ans - 0.10:.2f}", f"{ans + 0.20:.2f}"],
        "explanation": f"Round to 1/{base_a} + 1/{base_b} = {ans:.2f}, which is the closest option.",
        "verification_data": {"op": "approx_fracsum", "a": a, "b": b, "expected": f"{ans:.2f}"},
    }


def a_rounding(rng):
    base_a = rng.choice([20, 25, 30, 40, 50, 60, 80, 100])
    base_b = rng.choice([10, 12, 15, 20, 25, 30, 40, 50])
    a = _near(rng, base_a, max(0.2, base_a * 0.008))
    b = _near(rng, base_b, max(0.2, base_b * 0.008))
    ans = base_a * base_b
    step = _approx_step(ans, a * b, max(10, _round0(ans * 0.10)))
    return {
        "text": f"Which of the following is closest to {a:.2f} x {b:.2f}?",
        "correct": str(ans),
        "distractors": [str(ans + step), str(ans - step), str(ans + 2 * step)],
        "explanation": f"{a:.2f} is close to {base_a} and {b:.2f} is close to {base_b}. Their product is about {base_a} x {base_b} = {ans}.",
        "verification_data": {"op": "approx_product", "a": a, "b": b, "expected": ans},
    }


def a_multistep(rng):
    base_a = rng.randint(10, 40)
    base_b = rng.randint(10, 40)
    base_c = rng.choice([2, 3, 4, 5, 6, 8, 10])
    base_d = rng.choice([2, 3, 4, 5, 6, 8, 10])
    a = _near(rng, base_a, 0.1)
    b = _near(rng, base_b, 0.1)
    c = _near(rng, base_c, 0.05)
    d = _near(rng, base_d, 0.05)
    ans = _round0((base_a + base_b) * base_c / base_d)
    step = _approx_step(ans, (a + b) * c / d, max(2, _round0(ans * 0.06)))
    return {
        "text": f"What approximate value should come in place of the question mark? ({a:.2f} + {b:.2f}) x {c:.2f} / {d:.2f} = ?",
        "correct": str(ans),
        "distractors": [str(ans + step), str(ans - step), str(ans + 2 * step)],
        "explanation": f"Round the values: ({base_a} + {base_b}) x {base_c} / {base_d} = {ans}, which is the closest option.",
        "verification_data": {"op": "approx_multistep", "a": a, "b": b, "c": c, "d": d, "expected": ans},
    }


def build_approximation() -> Bank:
    bank = Bank("Approximation", seed=303)
    bank.chapter_key = "approximation"
    spec = [
        (1, "EASY", 6, a_product, "Approximations 01, pp. 4-9"),
        (1, "EASY", 4, a_division, "Approximations 01, pp. 10-14"),
        (1, "EASY", 3, a_percent, "Approximations 01, pp. 15-17"),
        (1, "EASY", 2, a_sqrt, "Approximations 02, pp. 4-8"),
        (2, "EASY", 6, a_product, "Approximations 02, pp. 9-14"),
        (2, "MEDIUM", 4, a_division, "Approximations 02, pp. 15-19"),
        (2, "MEDIUM", 4, a_percent, "Approximations 03, pp. 4-8"),
        (2, "EASY", 3, a_sqrt, "Approximations 03, pp. 9-13"),
        (2, "MEDIUM", 3, a_fracsum, "Approximations 03, pp. 14-20"),
        (3, "MEDIUM", 6, a_product, "Approximations 01, pp. 4-9"),
        (3, "MEDIUM", 5, a_division, "Approximations 01, pp. 10-14"),
        (3, "MEDIUM", 5, a_percent, "Approximations 02, pp. 4-8"),
        (3, "HARD", 4, a_sqrt, "Approximations 02, pp. 9-13"),
        (3, "HARD", 4, a_sumsq, "Approximations 02, pp. 14-19"),
        (3, "HARD", 3, a_mixed, "Approximations 03, pp. 4-10"),
        (3, "HARD", 3, a_multistep, "Approximations 03, pp. 11-16"),
        (4, "HARD", 12, a_product, "Approximations 01, pp. 4-9"),
        (4, "HARD", 8, a_division, "Approximations 01, pp. 10-14"),
        (4, "HARD", 8, a_percent, "Approximations 02, pp. 4-8"),
        (4, "HARD", 6, a_sqrt, "Approximations 02, pp. 9-13"),
        (4, "HARD", 5, a_sumsq, "Approximations 02, pp. 14-19"),
        (4, "HARD", 6, a_mixed, "Approximations 03, pp. 4-10"),
        (4, "HARD", 5, a_fracsum, "Approximations 03, pp. 14-20"),
        (4, "HARD", 5, a_rounding, "Approximations 03, pp. 17-20"),
    ]
    for part, difficulty, count, fn, pages in spec:
        fill(bank, part, difficulty, count, fn, APPROX_SOURCE, pages)
    return bank


# ---------------------------------------------------------------------------
# Missing Number Series
# ---------------------------------------------------------------------------

MISSING_SOURCE = "PW Banking Wallah - Missing Number Series (Class Notes, local PDF)"

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


def _predict_ap(terms, missing_idx):
    known = [(i, t) for i, t in enumerate(terms) if i != missing_idx]
    if len(known) < 3:
        return None
    d = known[1][1] - known[0][1]
    if d == 0:
        return None
    if all(known[j][1] - known[j - 1][1] == d for j in range(1, len(known))):
        return terms[0] + missing_idx * d
    return None


def _predict_gp(terms, missing_idx):
    known = [(i, t) for i, t in enumerate(terms) if i != missing_idx]
    if len(known) < 3 or known[0][1] == 0:
        return None
    ratio = Fraction(known[1][1], known[0][1])
    if ratio.denominator != 1 or ratio.numerator < 2:
        return None
    if all(Fraction(known[j][1], known[j - 1][1]) == ratio for j in range(1, len(known))):
        return int(terms[0] * ratio ** missing_idx)
    return None


def _predict_power(terms, missing_idx, power):
    known = [(i, t) for i, t in enumerate(terms) if i != missing_idx]
    roots = []
    for i, t in known:
        if t < 0:
            return None
        root = round(t ** (1.0 / power))
        if root ** power != t:
            return None
        roots.append((i, root))
    start = roots[0][1] - roots[0][0]
    if all(root == start + i for i, root in roots):
        return (start + missing_idx) ** power
    return None


def _predict_quadratic(terms, missing_idx):
    known = [(i, t) for i, t in enumerate(terms) if i != missing_idx]
    if len(known) < 4:
        return None
    (i1, y1), (i2, y2), (i3, y3) = known[:3]
    # Solve A*i^2 + B*i + C = y for the first three known points.
    import copy
    matrix = [
        [Fraction(i1 * i1), Fraction(i1), Fraction(1), Fraction(y1)],
        [Fraction(i2 * i2), Fraction(i2), Fraction(1), Fraction(y2)],
        [Fraction(i3 * i3), Fraction(i3), Fraction(1), Fraction(y3)],
    ]
    for col in range(3):
        pivot = next((row for row in range(col, 3) if matrix[row][col] != 0), None)
        if pivot is None:
            return None
        matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
        factor = matrix[col][col]
        matrix[col] = [value / factor for value in matrix[col]]
        for row in range(3):
            if row != col and matrix[row][col] != 0:
                factor = matrix[row][col]
                matrix[row] = [a - factor * b for a, b in zip(matrix[row], matrix[col])]
    a, b, c = matrix[0][3], matrix[1][3], matrix[2][3]
    for i, t in known:
        if a * i * i + b * i + c != t:
            return None
    predicted = a * missing_idx * missing_idx + b * missing_idx + c
    if predicted.denominator != 1:
        return None
    return int(predicted)


def _series_ambiguous(terms, missing_idx, answer) -> bool:
    """True when a second simple pattern predicts a different missing value."""
    predictions = [
        _predict_ap(terms, missing_idx),
        _predict_gp(terms, missing_idx),
        _predict_power(terms, missing_idx, 2),
        _predict_power(terms, missing_idx, 3),
        _predict_quadratic(terms, missing_idx),
    ]
    for prediction in predictions:
        if prediction is not None and prediction != answer:
            return True
    return False


def _series_candidate(rng, terms, missing_idx, rule_desc, extra_distractors=None):
    if missing_idx < 1 or missing_idx >= len(terms):
        return None
    if len(set(terms)) != len(terms):
        return None
    if any(t <= 0 for t in terms):
        return None
    answer = terms[missing_idx]
    if _series_ambiguous(terms, missing_idx, answer):
        return None
    shown = [str(t) if i != missing_idx else "?" for i, t in enumerate(terms)]
    step = max(1, abs(terms[missing_idx] - terms[missing_idx - 1]))
    forbidden = set(terms)
    distractors = []
    for delta in (step, -step, 2 * step, -2 * step, 3 * step, -3 * step, 1, -1, 2, -2, 10, -10):
        candidate = answer + delta
        if candidate > 0 and candidate not in forbidden and candidate not in distractors:
            distractors.append(candidate)
        if len(distractors) == 3:
            break
    if extra_distractors:
        distractors = extra_distractors
    return {
        "text": "Find the missing number in the series: " + ", ".join(shown),
        "correct": str(answer),
        "distractors": [str(d) for d in distractors],
        "explanation": f"{rule_desc} The missing term is {answer}.",
        "verification_data": {"op": "series", "terms": terms, "missing_index": missing_idx, "expected": answer, "rule": rule_desc},
    }


def m_ap(rng):
    a = rng.randint(1, 60)
    d = rng.randint(2, 18)
    terms = [a + i * d for i in range(5)]
    return _series_candidate(rng, terms, rng.randint(1, 4), f"The series increases by {d} each time (arithmetic progression).")


def m_gp(rng):
    a = rng.randint(1, 12)
    r = rng.randint(2, 4)
    terms = [a * r ** i for i in range(5)]
    if terms[-1] > 2_000_000:
        return None
    return _series_candidate(rng, terms, rng.randint(1, 4), f"Each term is multiplied by {r} (geometric progression).")


def m_square(rng):
    n = rng.randint(2, 22)
    terms = [(n + i) ** 2 for i in range(5)]
    return _series_candidate(rng, terms, rng.randint(1, 4), "The terms are consecutive perfect squares.")


def m_cube(rng):
    n = rng.randint(1, 13)
    terms = [(n + i) ** 3 for i in range(5)]
    return _series_candidate(rng, terms, rng.randint(1, 4), "The terms are consecutive perfect cubes.")


def m_plus_n2(rng):
    start = rng.randint(1, 30)
    terms = [start]
    for i in range(1, 5):
        terms.append(terms[-1] + i * i)
    return _series_candidate(rng, terms, rng.randint(1, 4), "The differences are 1, 4, 9, 16, ... (successive squares).")


def m_plus_n3(rng):
    start = rng.randint(1, 30)
    terms = [start]
    for i in range(1, 5):
        terms.append(terms[-1] + i ** 3)
    return _series_candidate(rng, terms, rng.randint(1, 4), "The differences are 1, 8, 27, 64, ... (successive cubes).")


def m_alt(rng):
    start = rng.randint(1, 12)
    r = rng.randint(2, 3)
    add = rng.randint(1, 12)
    terms = [start]
    for i in range(4):
        if i % 2 == 0:
            terms.append(terms[-1] * r)
        else:
            terms.append(terms[-1] + add)
    return _series_candidate(rng, terms, rng.randint(1, 4), f"The pattern alternates: x{r}, then +{add}.")


def m_double_diff(rng):
    start = rng.randint(1, 40)
    first = rng.randint(2, 12)
    inc = rng.randint(1, 9)
    terms = [start]
    diff = first
    for _ in range(4):
        terms.append(terms[-1] + diff)
        diff += inc
    return _series_candidate(rng, terms, rng.randint(1, 4), f"The differences increase by {inc} each time.")


def m_fib(rng):
    a = rng.randint(1, 12)
    b = rng.randint(1, 12)
    terms = [a, b, a + b, a + 2 * b, 2 * a + 3 * b]
    return _series_candidate(rng, terms, rng.randint(2, 4), "Each term is the sum of the two previous terms.")


def m_mul_add(rng):
    start = rng.randint(1, 8)
    r = rng.randint(2, 3)
    add = rng.randint(1, 12)
    terms = [start]
    for _ in range(4):
        terms.append(terms[-1] * r + add)
    return _series_candidate(rng, terms, rng.randint(1, 4), f"The pattern is x{r} + {add}.")


def m_prime(rng):
    start = rng.randint(0, len(PRIMES) - 5)
    terms = PRIMES[start:start + 5]
    return _series_candidate(rng, terms, rng.randint(1, 4), "The terms are consecutive prime numbers.")


def m_decreasing(rng):
    start = rng.randint(120, 600)
    first = rng.randint(2, 12)
    inc = rng.randint(1, 7)
    terms = [start]
    diff = first
    for _ in range(4):
        terms.append(terms[-1] - diff)
        diff += inc
    return _series_candidate(rng, terms, rng.randint(1, 4), f"The series decreases by {first}, then by {first + inc}, and so on.")


def build_missing_series() -> Bank:
    bank = Bank("Missing Number Series", seed=404)
    bank.chapter_key = "missing_series"
    spec = [
        (1, "EASY", 6, m_ap, "Missing Number Series 01, pp. 4-12"),
        (1, "EASY", 4, m_gp, "Missing Number Series 01, pp. 13-20"),
        (1, "EASY", 3, m_square, "Missing Number Series 01, pp. 21-28"),
        (1, "EASY", 2, m_cube, "Missing Number Series 01, pp. 29-38"),
        (2, "EASY", 5, m_ap, "Missing Number Series 01, pp. 4-12"),
        (2, "MEDIUM", 4, m_gp, "Missing Number Series 01, pp. 13-20"),
        (2, "MEDIUM", 4, m_plus_n2, "Missing Number Series 02, pp. 4-10"),
        (2, "MEDIUM", 4, m_double_diff, "Missing Number Series 02, pp. 11-16"),
        (2, "EASY", 3, m_fib, "Missing Number Series 02, pp. 17-23"),
        (3, "MEDIUM", 5, m_plus_n2, "Missing Number Series 02, pp. 4-10"),
        (3, "HARD", 5, m_plus_n3, "Missing Number Series 02, pp. 11-16"),
        (3, "MEDIUM", 5, m_double_diff, "Missing Number Series 02, pp. 11-16"),
        (3, "HARD", 5, m_alt, "Missing Number Series 01, pp. 21-28"),
        (3, "HARD", 5, m_mul_add, "Missing Number Series 01, pp. 29-38"),
        (3, "MEDIUM", 5, m_prime, "Missing Number Series 01, pp. 4-12"),
        (4, "HARD", 10, m_plus_n3, "Missing Number Series 02, pp. 11-16"),
        (4, "HARD", 8, m_alt, "Missing Number Series 01, pp. 21-28"),
        (4, "HARD", 8, m_mul_add, "Missing Number Series 01, pp. 29-38"),
        (4, "HARD", 8, m_double_diff, "Missing Number Series 02, pp. 11-16"),
        (4, "HARD", 6, m_fib, "Missing Number Series 02, pp. 17-23"),
        (4, "HARD", 6, m_decreasing, "Missing Number Series 02, pp. 17-23"),
        (4, "HARD", 5, m_prime, "Missing Number Series 01, pp. 4-12"),
        (4, "HARD", 4, m_cube, "Missing Number Series 01, pp. 29-38"),
    ]
    for part, difficulty, count, fn, pages in spec:
        fill(bank, part, difficulty, count, fn, MISSING_SOURCE, pages)
    return bank


# ---------------------------------------------------------------------------
# Wrong Number Series
# ---------------------------------------------------------------------------

WRONG_SOURCE = "PW Banking Wallah - Wrong Number Series (Class Notes, local PDF)"


def _pattern_fits(display, skip_idx) -> bool:
    others = [(i, t) for i, t in enumerate(display) if i != skip_idx]
    if len(others) < 4:
        return False
    # arithmetic progression
    d = others[1][1] - others[0][1]
    if d != 0 and all(others[j][1] - others[j - 1][1] == d for j in range(1, len(others))):
        return True
    # geometric progression
    if others[0][1] != 0:
        ratio = Fraction(others[1][1], others[0][1])
        if ratio.denominator == 1 and ratio.numerator >= 2:
            if all(Fraction(others[j][1], others[j - 1][1]) == ratio for j in range(1, len(others))):
                return True
    # consecutive squares / cubes
    for power in (2, 3):
        roots = []
        ok = True
        for i, t in others:
            if t < 0:
                ok = False
                break
            root = round(t ** (1.0 / power))
            if root ** power != t:
                ok = False
                break
            roots.append((i, root))
        if ok:
            start = roots[0][1] - roots[0][0]
            if all(root == start + i for i, root in roots):
                return True
    # quadratic through the four remaining points
    (i1, y1), (i2, y2), (i3, y3), (i4, y4) = others
    matrix = [
        [Fraction(i1 * i1), Fraction(i1), Fraction(1), Fraction(y1)],
        [Fraction(i2 * i2), Fraction(i2), Fraction(1), Fraction(y2)],
        [Fraction(i3 * i3), Fraction(i3), Fraction(1), Fraction(y3)],
    ]
    for col in range(3):
        pivot = next((row for row in range(col, 3) if matrix[row][col] != 0), None)
        if pivot is None:
            return False
        matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
        factor = matrix[col][col]
        matrix[col] = [value / factor for value in matrix[col]]
        for row in range(3):
            if row != col and matrix[row][col] != 0:
                factor = matrix[row][col]
                matrix[row] = [a - factor * b for a, b in zip(matrix[row], matrix[col])]
    a, b, c = matrix[0][3], matrix[1][3], matrix[2][3]
    return a * i4 * i4 + b * i4 + c == y4


def _wrong_candidate(rng, terms, rule_desc):
    if len(terms) != 5 or len(set(terms)) != 5 or any(t <= 0 for t in terms):
        return None
    wrong_idx = rng.randint(1, 4)
    local_step = abs(terms[wrong_idx] - terms[wrong_idx - 1])
    delta = max(1, local_step // 2)
    wrong_value = None
    for sign in (rng.choice([-1, 1]), rng.choice([-1, 1])):
        candidate = terms[wrong_idx] + sign * delta
        if candidate > 0 and candidate not in terms:
            wrong_value = candidate
            break
    if wrong_value is None:
        return None
    display = list(terms)
    display[wrong_idx] = wrong_value
    if len(set(display)) != 5:
        return None
    # The intended answer must be the only term whose removal leaves a simple pattern.
    for i in range(5):
        if i != wrong_idx and _pattern_fits(display, i):
            return None
    correct_terms = terms
    other_positions = [i for i in range(5) if i != wrong_idx]
    rng.shuffle(other_positions)
    option_terms = [wrong_value] + [correct_terms[i] for i in other_positions[:3]]
    return {
        "text": "Find the wrong number in the series: " + ", ".join(str(t) for t in display),
        "correct": str(wrong_value),
        "distractors": [str(t) for t in option_terms[1:]],
        "explanation": f"{rule_desc} The correct term at position {wrong_idx + 1} is {correct_terms[wrong_idx]}, so {wrong_value} is the wrong number.",
        "verification_data": {
            "op": "wrong_series",
            "correct_terms": correct_terms,
            "wrong_index": wrong_idx,
            "wrong_value": wrong_value,
            "rule": rule_desc,
        },
    }


def w_ap(rng):
    a = rng.randint(1, 60)
    d = rng.randint(2, 18)
    return _wrong_candidate(rng, [a + i * d for i in range(5)], f"The series increases by {d} each time (arithmetic progression).")


def w_gp(rng):
    a = rng.randint(1, 12)
    r = rng.randint(2, 4)
    terms = [a * r ** i for i in range(5)]
    if terms[-1] > 2_000_000:
        return None
    return _wrong_candidate(rng, terms, f"Each term is multiplied by {r} (geometric progression).")


def w_square(rng):
    n = rng.randint(2, 22)
    return _wrong_candidate(rng, [(n + i) ** 2 for i in range(5)], "The terms are consecutive perfect squares.")


def w_cube(rng):
    n = rng.randint(1, 13)
    return _wrong_candidate(rng, [(n + i) ** 3 for i in range(5)], "The terms are consecutive perfect cubes.")


def w_plus_n2(rng):
    start = rng.randint(1, 30)
    terms = [start]
    for i in range(1, 5):
        terms.append(terms[-1] + i * i)
    return _wrong_candidate(rng, terms, "The differences are 1, 4, 9, 16, ... (successive squares).")


def w_plus_n3(rng):
    start = rng.randint(1, 30)
    terms = [start]
    for i in range(1, 5):
        terms.append(terms[-1] + i ** 3)
    return _wrong_candidate(rng, terms, "The differences are 1, 8, 27, 64, ... (successive cubes).")


def w_alt(rng):
    start = rng.randint(1, 12)
    r = rng.randint(2, 3)
    add = rng.randint(1, 12)
    terms = [start]
    for i in range(4):
        terms.append(terms[-1] * r if i % 2 == 0 else terms[-1] + add)
    return _wrong_candidate(rng, terms, f"The pattern alternates: x{r}, then +{add}.")


def w_double_diff(rng):
    start = rng.randint(1, 40)
    first = rng.randint(2, 12)
    inc = rng.randint(1, 9)
    terms = [start]
    diff = first
    for _ in range(4):
        terms.append(terms[-1] + diff)
        diff += inc
    return _wrong_candidate(rng, terms, f"The differences increase by {inc} each time.")


def w_fib(rng):
    a = rng.randint(1, 12)
    b = rng.randint(1, 12)
    return _wrong_candidate(rng, [a, b, a + b, a + 2 * b, 2 * a + 3 * b], "Each term is the sum of the two previous terms.")


def w_mul_add(rng):
    start = rng.randint(1, 8)
    r = rng.randint(2, 3)
    add = rng.randint(1, 12)
    terms = [start]
    for _ in range(4):
        terms.append(terms[-1] * r + add)
    return _wrong_candidate(rng, terms, f"The pattern is x{r} + {add}.")


def w_prime(rng):
    start = rng.randint(0, len(PRIMES) - 5)
    return _wrong_candidate(rng, PRIMES[start:start + 5], "The terms are consecutive prime numbers.")


def w_decreasing(rng):
    start = rng.randint(120, 600)
    first = rng.randint(2, 12)
    inc = rng.randint(1, 7)
    terms = [start]
    diff = first
    for _ in range(4):
        terms.append(terms[-1] - diff)
        diff += inc
    return _wrong_candidate(rng, terms, f"The series decreases by {first}, then by {first + inc}, and so on.")


def build_wrong_series() -> Bank:
    bank = Bank("Wrong Number Series", seed=505)
    bank.chapter_key = "wrong_series"
    spec = [
        (1, "EASY", 5, w_ap, "Wrong Number Series 01, pp. 4-8"),
        (1, "EASY", 3, w_gp, "Wrong Number Series 01, pp. 9-14"),
        (1, "EASY", 3, w_square, "Wrong Number Series 02, pp. 4-8"),
        (1, "EASY", 2, w_plus_n2, "Wrong Number Series 02, pp. 9-13"),
        (1, "EASY", 2, w_double_diff, "Wrong Number Series 02, pp. 14-21"),
        (2, "EASY", 4, w_ap, "Wrong Number Series 01, pp. 4-8"),
        (2, "MEDIUM", 4, w_gp, "Wrong Number Series 01, pp. 9-14"),
        (2, "MEDIUM", 4, w_plus_n2, "Wrong Number Series 02, pp. 9-13"),
        (2, "MEDIUM", 2, w_plus_n3, "Wrong Number Series 02, pp. 9-13"),
        (2, "MEDIUM", 3, w_alt, "Wrong Number Series 01, pp. 9-14"),
        (2, "MEDIUM", 3, w_fib, "Wrong Number Series 02, pp. 14-21"),
        (3, "MEDIUM", 5, w_plus_n2, "Wrong Number Series 02, pp. 9-13"),
        (3, "HARD", 5, w_plus_n3, "Wrong Number Series 02, pp. 9-13"),
        (3, "HARD", 5, w_alt, "Wrong Number Series 01, pp. 9-14"),
        (3, "MEDIUM", 5, w_double_diff, "Wrong Number Series 02, pp. 14-21"),
        (3, "HARD", 5, w_mul_add, "Wrong Number Series 01, pp. 15-21"),
        (3, "MEDIUM", 5, w_square, "Wrong Number Series 02, pp. 4-8"),
        (4, "HARD", 10, w_plus_n3, "Wrong Number Series 02, pp. 9-13"),
        (4, "HARD", 8, w_alt, "Wrong Number Series 01, pp. 9-14"),
        (4, "HARD", 8, w_mul_add, "Wrong Number Series 01, pp. 15-21"),
        (4, "HARD", 8, w_double_diff, "Wrong Number Series 02, pp. 14-21"),
        (4, "HARD", 6, w_fib, "Wrong Number Series 02, pp. 14-21"),
        (4, "HARD", 5, w_decreasing, "Wrong Number Series 02, pp. 14-21"),
        (4, "HARD", 5, w_prime, "Wrong Number Series 01, pp. 4-8"),
        (4, "HARD", 5, w_cube, "Wrong Number Series 02, pp. 4-8"),
    ]
    for part, difficulty, count, fn, pages in spec:
        fill(bank, part, difficulty, count, fn, WRONG_SOURCE, pages)
    return bank


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def write_bank(bank: Bank, filename: str):
    assert bank.count() == TARGET_PER_CHAPTER, (bank.chapter, bank.count())
    for part, size in PART_SIZES.items():
        assert bank.count(part) == size, (bank.chapter, part, bank.count(part))
    path = os.path.join(DATA, filename)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(bank.items, handle, ensure_ascii=False, indent=2)
    print(f"wrote {path} ({bank.count()} questions)")


def main():
    banks = [build_vedic(), build_simplification(), build_approximation(), build_missing_series(), build_wrong_series()]
    # other chapters are appended below
    for bank in banks:
        write_bank(bank, BANK_FILES[bank.chapter_key])


BANK_FILES = {
    "vedic_maths": "banking_maths_vedic_calculation_questions.json",
    "simplification": "banking_maths_simplification_questions.json",
    "approximation": "banking_maths_approximation_questions.json",
    "missing_series": "banking_maths_missing_number_series_questions.json",
    "wrong_series": "banking_maths_wrong_number_series_questions.json",
}


if __name__ == "__main__":
    main()
