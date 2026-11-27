# -*- coding: utf-8 -*-
"""Percentage - 120 verified questions for the second Maths batch."""

from __future__ import annotations

from fractions import Fraction

from .bank import Bank, fill, fmt_dec

SOURCE = "PW Banking Wallah - Percentage Class Notes (local PDF)"
PAGES = {
    1: "Percentage 01, pp. 3-19",
    2: "Percentage 02, pp. 3-17",
    3: "Percentage 03, pp. 3-25",
    4: "Percentage 04, pp. 3-19",
    5: "Percentage 05, pp. 3-19",
    6: "Percentage 06, pp. 3-19",
    7: "Percentage 07, pp. 3-19",
    8: "Percentage 08, pp. 3-21",
}


def near_values(correct: float, rng, spread: float = 8, places: int = 2) -> list[str]:
    values: list[str] = []
    target = fmt_dec(correct, places)
    while len(values) < 3:
        delta = rng.choice([-1, 1]) * rng.choice([2, 4, 5, 8, 10, 12])
        text = fmt_dec(correct + delta, places)
        if text != target and text not in values:
            values.append(text)
    return values


def pct_of(rng):
    p = 5 * rng.randint(3, 19)
    n = 20 * rng.randint(6, 45)
    answer = p * n // 100
    return {
        "text": f"What is {p}% of {n}?",
        "correct": str(answer),
        "distractors": near_values(answer, rng, 12),
        "explanation": (
            f"{p}% of {n} = ({p}/100) x {n} = {p} x {n // 20} / 5 = {answer}."
        ),
        "verification_data": {"op": "pct_of", "p": p, "n": n},
    }


def pct_what(rng):
    b = 20 * rng.randint(5, 40)
    a = rng.randint(10, 350)
    answer = Fraction(a, b) * 100
    return {
        "text": f"{a} is what percent of {b}?",
        "correct": fmt_dec(float(answer), 2),
        "distractors": near_values(float(answer), rng, 8),
        "explanation": (
            f"Required percentage = ({a}/{b}) x 100 = {fmt_dec(float(answer), 2)}%."
        ),
        "verification_data": {"op": "pct_what", "a": a, "b": b},
    }


def pct_fraction(rng):
    num = rng.randint(1, 7)
    den = rng.choice([8, 16, 20, 25, 40, 50])
    value = Fraction(num, den) * 100
    return {
        "text": f"Express {num}/{den} as a percentage.",
        "correct": fmt_dec(float(value), 2) + "%",
        "distractors": [fmt_dec(float(value) + d, 2) + "%" for d in (5, 10, 12.5)],
        "explanation": (
            f"{num}/{den} x 100 = {fmt_dec(float(value), 2)}%."
        ),
        "verification_data": {"op": "pct_fraction", "num": num, "den": den},
    }


def pct_change(rng):
    old = 20 * rng.randint(5, 30)
    p = 5 * rng.randint(2, 16)
    new = old + old * p // 100
    return {
        "text": f"A quantity increases from {old} to {new}. Find the percentage increase.",
        "correct": str(p),
        "distractors": near_values(p, rng, 6),
        "explanation": (
            f"Increase = {new} - {old} = {new - old}. Percentage increase = "
            f"({new - old}/{old}) x 100 = {p}%."
        ),
        "verification_data": {"op": "pct_change", "old": old, "new": new},
    }


def pct_reverse(rng):
    p = 5 * rng.randint(3, 16)
    original = 20 * rng.randint(6, 40)
    result = original + original * p // 100
    return {
        "text": (
            f"After a {p}% increase, a number becomes {result}. Find the original number."
        ),
        "correct": str(original),
        "distractors": near_values(original, rng, 15),
        "explanation": (
            f"Let the original number be x. Then x(1 + {p}/100) = {result}, so "
            f"x = {result} x 100/{100 + p} = {original}."
        ),
        "verification_data": {"op": "pct_reverse", "p": p, "result": result},
    }


def pct_successive(rng):
    p = 5 * rng.randint(2, 12)
    q = 5 * rng.randint(2, 12)
    mode = rng.choice(["up_up", "up_down"])
    if mode == "up_up":
        net = Fraction(p) + Fraction(q) + Fraction(p * q, 100)
        second = "increased"
    else:
        net = Fraction(p) - Fraction(q) - Fraction(p * q, 100)
        second = "decreased"
    if net > 0:
        label = f"{fmt_dec(float(net), 2)}% increase"
    elif net < 0:
        label = f"{fmt_dec(float(-net), 2)}% decrease"
    else:
        label = "No change"
    naive = f"{p + q}% increase" if mode == "up_up" else f"{p - q}% change"
    return {
        "text": (
            f"A number is increased by {p}% and then {second} by {q}%. "
            f"Find the net percentage change."
        ),
        "correct": label,
        "distractors": [
            naive,
            f"{p + q}% decrease",
            f"{abs(p - q)}% increase",
        ],
        "explanation": (
            f"Net change = {p} {'+' if mode == 'up_up' else '-'} {q} "
            f"{'+' if mode == 'up_up' else '-'} ({p} x {q})/100 = "
            f"{fmt_dec(float(net), 2)}%, so the result is {label.lower()}."
        ),
        "verification_data": {
            "op": "pct_successive",
            "p": p,
            "q": q,
            "mode": mode,
        },
    }


def pct_more_less(rng):
    p = rng.choice([25, 50, 100, 150, 200, 300, 400])
    noun = rng.choice(
        ["salary", "marks", "population", "price", "weight", "area", "speed"]
    )
    answer = Fraction(100 * p, 100 + p)
    return {
        "text": (
            f"A's {noun} is {p}% more than B's {noun}. B's {noun} is what percent "
            f"less than A's {noun}?"
        ),
        "correct": fmt_dec(float(answer), 2) + "%",
        "distractors": [
            f"{p}%",
            f"{p + 10}%",
            f"{max(1, p - 10)}%",
        ],
        "explanation": (
            f"Let B = 100, then A = {100 + p}. B is less than A by {p}, so the "
            f"required percentage is ({p}/{100 + p}) x 100 = "
            f"{fmt_dec(float(answer), 2)}%."
        ),
        "verification_data": {"op": "pct_more_less", "p": p},
    }


def pct_exam(rng):
    total = 100 * rng.randint(4, 10)
    p1 = 5 * rng.randint(6, 9)
    p2 = 5 * rng.randint(11, 15)
    pass_marks = (total * p1 // 100 + total * p2 // 100) // 2
    fail = pass_marks - total * p1 // 100
    extra = total * p2 // 100 - pass_marks
    if fail <= 0 or extra <= 0:
        return None
    return {
        "text": (
            f"In an examination, a candidate who scores {p1}% fails by {fail} marks, "
            f"while a candidate who scores {p2}% gets {extra} marks more than the pass "
            f"mark. Find the maximum marks."
        ),
        "correct": str(total),
        "distractors": near_values(total, rng, 60),
        "explanation": (
            f"The gap of {p2}% - {p1}% = {p2 - p1}% equals {fail} + {extra} = "
            f"{fail + extra} marks. So 1% = {(fail + extra) / (p2 - p1):g} marks and "
            f"100% = {total} marks."
        ),
        "verification_data": {
            "op": "pct_exam",
            "p1": p1,
            "fail": fail,
            "p2": p2,
            "extra": extra,
        },
    }


def pct_consumption(rng):
    rise = rng.choice([True, False])
    p = rng.choice(
        [25, 50, 100, 150, 200, 300, 400] if rise else [25, 50, 150, 200, 300, 400]
    )
    item = rng.choice(["sugar", "rice", "petrol", "wheat", "cooking oil", "gas"])
    if rise:
        answer = Fraction(100 * p, 100 + p)
        text = (
            f"The price of {item} rises by {p}%. By what percent must a family "
            f"reduce its consumption so that its expenditure stays the same?"
        )
    else:
        answer = Fraction(100 * p, 100 - p)
        text = (
            f"The price of {item} falls by {p}%. By what percent can a family "
            f"increase its consumption so that its expenditure stays the same?"
        )
    return {
        "text": text,
        "correct": fmt_dec(float(answer), 2) + "%",
        "distractors": [
            f"{p}%",
            f"{p + 10}%",
            f"{max(1, p - 10)}%",
        ],
        "explanation": (
            f"Expenditure is fixed, so consumption changes in the inverse ratio of "
            f"price. The required percentage is "
            f"{'100 x ' + str(p) + '/(' + str(100 + p) + ')' if rise else '100 x ' + str(p) + '/(' + str(100 - p) + ')'} "
            f"= {fmt_dec(float(answer), 2)}%."
        ),
        "verification_data": {"op": "pct_consumption", "p": p, "rise": rise},
    }


def pct_population(rng):
    population = 100 * rng.randint(20, 90)
    p = 10 * rng.randint(1, 4)
    q = 10 * rng.randint(1, 4)
    final = population * (100 + p) // 100 * (100 + q) // 100
    return {
        "text": (
            f"The population of a town is {population}. It increases by {p}% in the "
            f"first year and by {q}% in the next year. Find the population after two years."
        ),
        "correct": str(final),
        "distractors": near_values(final, rng, 120),
        "explanation": (
            f"Population after two years = {population} x (1 + {p}/100) x "
            f"(1 + {q}/100) = {final}."
        ),
        "verification_data": {
            "op": "pct_population",
            "population": population,
            "p": p,
            "q": q,
        },
    }


def pct_income(rng):
    income = 100 * rng.randint(20, 90)
    p = 5 * rng.randint(4, 16)
    saving = income * (100 - p) // 100
    return {
        "text": (
            f"A person spends {p}% of his monthly income and saves Rs {saving}. "
            f"Find his monthly income."
        ),
        "correct": str(income),
        "distractors": near_values(income, rng, 150),
        "explanation": (
            f"He saves 100% - {p}% = {100 - p}% of his income. So "
            f"{100 - p}% of income = {saving}, giving income = "
            f"{saving} x 100/{100 - p} = {income}."
        ),
        "verification_data": {
            "op": "pct_income",
            "income": income,
            "p": p,
            "saving": saving,
        },
    }


def build_percentage() -> Bank:
    bank = Bank("Percentage", "percentage", seed=603)
    spec = [
        (1, "EASY", 6, pct_of, 1),
        (1, "EASY", 4, pct_what, 2),
        (1, "EASY", 3, pct_fraction, 3),
        (1, "EASY", 2, pct_change, 4),
        (2, "EASY", 4, pct_of, 5),
        (2, "MEDIUM", 4, pct_what, 6),
        (2, "MEDIUM", 4, pct_change, 7),
        (2, "MEDIUM", 4, pct_reverse, 8),
        (2, "MEDIUM", 4, pct_more_less, 5),
        (3, "MEDIUM", 6, pct_successive, 4),
        (3, "MEDIUM", 6, pct_consumption, 6),
        (3, "HARD", 6, pct_exam, 7),
        (3, "MEDIUM", 6, pct_income, 8),
        (3, "MEDIUM", 6, pct_population, 3),
        (4, "HARD", 10, pct_successive, 5),
        (4, "HARD", 10, pct_consumption, 7),
        (4, "HARD", 10, pct_exam, 8),
        (4, "HARD", 10, pct_population, 6),
        (4, "HARD", 10, pct_more_less, 4),
        (4, "HARD", 5, pct_reverse, 2),
    ]
    for part, difficulty, count, fn, page in spec:
        fill(bank, part, difficulty, count, fn, SOURCE, PAGES[page])
    return bank
