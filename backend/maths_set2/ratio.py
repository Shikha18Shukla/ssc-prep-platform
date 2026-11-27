# -*- coding: utf-8 -*-
"""Ratio and Proportion - 120 verified questions for the second Maths batch."""

from __future__ import annotations

import math

from .bank import Bank, fill

SOURCE = "Guidely Topic-Wise Bundle - Ratio and Proportion Sets 1-4 (Mains) (local PDF)"
PAGES = {
    1: "Ratio and Proportion Set-1 (Mains), pp. 1-7",
    2: "Ratio and Proportion Set-2 (Mains), pp. 1-8",
    3: "Ratio and Proportion Set-3 (Mains), pp. 1-7",
    4: "Ratio and Proportion Set-4 (Mains), pp. 1-7",
}


def ratio_str(a: int, b: int) -> str:
    g = math.gcd(a, b)
    return f"{a // g}:{b // g}"


def triple_str(a: int, b: int, c: int) -> str:
    g = math.gcd(math.gcd(a, b), c)
    return f"{a // g}:{b // g}:{c // g}"


def near_ints(correct: int, rng, spread: int = 8) -> list[str]:
    values: list[str] = []
    while len(values) < 3:
        delta = rng.choice([-1, 1]) * rng.randint(1, spread)
        text = str(correct + delta)
        if text != str(correct) and text not in values:
            values.append(text)
    return values


def r_divide(rng):
    a, b, c = rng.randint(1, 6), rng.randint(1, 7), rng.randint(1, 8)
    total = (a + b + c) * rng.randint(8, 60)
    which = rng.choice(["A", "B", "C"])
    share = {"A": a, "B": b, "C": c}[which]
    answer = total * share // (a + b + c)
    return {
        "text": (
            f"An amount of Rs {total} is divided among A, B and C in the ratio "
            f"{a}:{b}:{c}. What is {which}'s share?"
        ),
        "correct": str(answer),
        "distractors": near_ints(answer, rng, 40),
        "explanation": (
            f"Total parts = {a} + {b} + {c} = {a + b + c}. One part = "
            f"{total}/{a + b + c} = {total // (a + b + c)}. {which}'s share = "
            f"{share} x {total // (a + b + c)} = {answer}."
        ),
        "verification_data": {
            "op": "r_divide",
            "total": total,
            "ratio": [a, b, c],
            "index": "ABC".index(which),
        },
    }


def r_prop(rng):
    a = rng.randint(2, 9)
    b = rng.randint(2, 12)
    c = rng.randint(2, 12)
    product = b * c
    while product % a:
        a = rng.randint(2, 9)
    answer = product // a
    return {
        "text": f"Find x if {a}:{b} = {c}:x.",
        "correct": str(answer),
        "distractors": near_ints(answer, rng, 8),
        "explanation": (
            f"For a proportion, the product of the means equals the product of the "
            f"extremes: {b} x {c} = {a} x x, so x = {product}/{a} = {answer}."
        ),
        "verification_data": {"op": "r_prop", "a": a, "b": b, "c": c},
    }


def r_boys(rng):
    a, b = rng.randint(2, 7), rng.randint(2, 7)
    total = (a + b) * rng.randint(4, 15)
    answer = total * a // (a + b)
    return {
        "text": (
            f"In a class of {total} students, the ratio of boys to girls is {a}:{b}. "
            f"How many boys are there?"
        ),
        "correct": str(answer),
        "distractors": near_ints(answer, rng, 10),
        "explanation": (
            f"Total parts = {a + b}, and each part is {total}/{a + b} = "
            f"{total // (a + b)}. Boys = {a} x {total // (a + b)} = {answer}."
        ),
        "verification_data": {"op": "r_boys", "total": total, "a": a, "b": b},
    }


def r_share(rng):
    a, b = rng.randint(2, 9), rng.randint(2, 9)
    while a == b:
        b = rng.randint(2, 9)
    total = (a + b) * rng.randint(6, 30)
    larger = max(a, b)
    answer = total * larger // (a + b)
    return {
        "text": (
            f"Two numbers are in the ratio {a}:{b} and their sum is {total}. "
            f"Find the larger number."
        ),
        "correct": str(answer),
        "distractors": near_ints(answer, rng, 15),
        "explanation": (
            f"The larger share corresponds to {larger} parts out of {a + b}. So the "
            f"larger number is {total} x {larger}/{a + b} = {answer}."
        ),
        "verification_data": {"op": "r_share", "a": a, "b": b, "total": total},
    }


def r_combine(rng):
    a1, b1 = rng.randint(2, 9), rng.randint(2, 9)
    while math.gcd(a1, b1) != 1:
        a1, b1 = rng.randint(2, 9), rng.randint(2, 9)
    b2, c1 = rng.randint(2, 9), rng.randint(2, 9)
    while math.gcd(b2, c1) != 1:
        b2, c1 = rng.randint(2, 9), rng.randint(2, 9)
    common = math.lcm(b1, b2)
    a = a1 * (common // b1)
    b = common
    c = c1 * (common // b2)
    answer = triple_str(a, b, c)
    return {
        "text": f"If A:B = {a1}:{b1} and B:C = {b2}:{c1}, find A:B:C.",
        "correct": answer,
        "distractors": [
            triple_str(a1, b1, c1),
            triple_str(a1 * b2, b1 * b2, b2 * c1),
            triple_str(b1, a1, c1),
        ],
        "explanation": (
            f"Make the B term common. The LCM of {b1} and {b2} is {common}, so "
            f"A:B = {a}:{common} and B:C = {common}:{c}. Hence A:B:C = {answer}."
        ),
        "verification_data": {"op": "r_combine", "a1": a1, "b1": b1, "b2": b2, "c1": c1},
    }


def r_mean(rng):
    u = rng.randint(2, 9)
    v = rng.randint(2, 9)
    a, b = u * u, v * v
    answer = u * v
    return {
        "text": f"Find the mean proportional between {a} and {b}.",
        "correct": str(answer),
        "distractors": near_ints(answer, rng, 6),
        "explanation": (
            f"The mean proportional m satisfies m^2 = {a} x {b} = {a * b}, so "
            f"m = sqrt({a * b}) = {answer}."
        ),
        "verification_data": {"op": "r_mean", "a": a, "b": b},
    }


def r_third(rng):
    a = rng.randint(2, 8)
    b = a * rng.randint(2, 9)
    answer = b * b // a
    return {
        "text": f"Find x such that {a}:{b} = {b}:x.",
        "correct": str(answer),
        "distractors": near_ints(answer, rng, 12),
        "explanation": (
            f"If x is the third proportional, then {a}:{b} = {b}:x, so "
            f"x = {b} x {b}/{a} = {answer}."
        ),
        "verification_data": {"op": "r_third", "a": a, "b": b},
    }


def r_inverse(rng):
    m, n = rng.randint(2, 9), rng.randint(2, 9)
    p, q = rng.randint(1, 5), rng.randint(1, 5)
    answer = ratio_str(p * m, q * n)
    return {
        "text": f"If a:b = {m}:{n}, find ({p}a):({q}b).",
        "correct": answer,
        "distractors": [
            ratio_str(m, n),
            ratio_str(q * m, p * n),
            ratio_str(p * n, q * m),
        ],
        "explanation": (
            f"Substitute a = {m}k and b = {n}k. Then {p}a : {q}b = "
            f"{p * m}k : {q * n}k = {answer}."
        ),
        "verification_data": {"op": "r_inverse", "m": m, "n": n, "p": p, "q": q},
    }


def r_ages(rng):
    a, b = rng.randint(2, 7), rng.randint(2, 7)
    while math.gcd(a, b) != 1 or a == b:
        a, b = rng.randint(2, 7), rng.randint(2, 7)
    k = rng.randint(3, 12)
    t = rng.randint(2, 12)
    now_a, now_b = a * k, b * k
    later_a, later_b = now_a + t, now_b + t
    g = math.gcd(later_a, later_b)
    c, d = later_a // g, later_b // g
    which = rng.choice(["A", "B"])
    answer = now_a if which == "A" else now_b
    return {
        "text": (
            f"The present ages of A and B are in the ratio {a}:{b}. After {t} years, "
            f"the ratio becomes {c}:{d}. Find the present age of {which}."
        ),
        "correct": str(answer),
        "distractors": near_ints(answer, rng, 6),
        "explanation": (
            f"Let the ages be {a}k and {b}k. Then ({a}k + {t})/({b}k + {t}) = "
            f"{c}/{d}, which gives k = {k}. So A = {now_a} and B = {now_b}; "
            f"{which}'s present age is {answer}."
        ),
        "verification_data": {
            "op": "r_ages",
            "a": a,
            "b": b,
            "t": t,
            "c": c,
            "d": d,
            "which": which,
        },
    }


def r_income(rng):
    a, b = rng.randint(3, 7), rng.randint(4, 9)
    c, d = rng.randint(2, 6), rng.randint(3, 8)
    while b <= a or d <= c or a * d - b * c <= 0:
        a, b = rng.randint(3, 7), rng.randint(4, 9)
        c, d = rng.randint(2, 6), rng.randint(3, 8)
    j = rng.randint(3, 10)
    k = (d - c) * j
    saving = j * (a * d - b * c)
    income_a = a * k
    return {
        "text": (
            f"The monthly incomes of A and B are in the ratio {a}:{b}, and their "
            f"expenditures are in the ratio {c}:{d}. If each saves Rs {saving}, find "
            f"A's monthly income."
        ),
        "correct": str(income_a),
        "distractors": near_ints(income_a, rng, 400),
        "explanation": (
            f"Let incomes be {a}k and {b}k, and expenditures be {c}m and {d}m. "
            f"Savings give {a}k - {c}m = {saving} and {b}k - {d}m = {saving}. "
            f"Solving gives k = {k}, so A's income = {a} x {k} = {income_a}."
        ),
        "verification_data": {
            "op": "r_income",
            "a": a,
            "b": b,
            "c": c,
            "d": d,
            "saving": saving,
        },
    }


def r_coins(rng):
    a, b, c = rng.randint(1, 4), rng.randint(1, 4), rng.randint(1, 4)
    values = [1, 2, 5]
    k = rng.randint(4, 20)
    total = k * (a * values[0] + b * values[1] + c * values[2])
    answer = b * k
    return {
        "text": (
            f"A bag contains Re 1, Rs 2 and Rs 5 coins in the ratio {a}:{b}:{c}. "
            f"If the total value of the coins is Rs {total}, how many Rs 2 coins are there?"
        ),
        "correct": str(answer),
        "distractors": near_ints(answer, rng, 8),
        "explanation": (
            f"Let the counts be {a}k, {b}k and {c}k. Then {a}k + 2 x {b}k + "
            f"5 x {c}k = {total}, so k = {k}. The number of Rs 2 coins is "
            f"{b} x {k} = {answer}."
        ),
        "verification_data": {
            "op": "r_coins",
            "a": a,
            "b": b,
            "c": c,
            "total": total,
        },
    }


def r_mixture(rng):
    a, b = rng.randint(1, 5), rng.randint(1, 5)
    c, d = rng.randint(1, 5), rng.randint(1, 5)
    milk = a * (c + d) + c * (a + b)
    water = b * (c + d) + d * (a + b)
    answer = ratio_str(milk, water)
    return {
        "text": (
            f"Two vessels contain milk and water in the ratios {a}:{b} and {c}:{d}. "
            f"Equal quantities from both vessels are mixed. Find the ratio of milk to "
            f"water in the mixture."
        ),
        "correct": answer,
        "distractors": [
            ratio_str(a + c, b + d),
            ratio_str(a * c, b * d),
            ratio_str(b, a),
        ],
        "explanation": (
            f"Take one litre from each vessel. Milk = {a}/{a + b} + {c}/{c + d}, "
            f"water = {b}/{a + b} + {d}/{c + d}. Multiplying by "
            f"{a + b}({c + d}) gives milk:water = {milk}:{water} = {answer}."
        ),
        "verification_data": {"op": "r_mixture", "a": a, "b": b, "c": c, "d": d},
    }


def r_partnership(rng):
    c1, c2 = rng.randint(2, 9), rng.randint(2, 9)
    t1, t2 = rng.randint(4, 12), rng.randint(4, 12)
    unit = c1 * t1 + c2 * t2
    total = unit * rng.randint(5, 30)
    answer = total * c1 * t1 // unit
    return {
        "text": (
            f"A invests Rs {c1 * 1000} for {t1} months and B invests Rs {c2 * 1000} "
            f"for {t2} months. If the total profit is Rs {total}, find A's share."
        ),
        "correct": str(answer),
        "distractors": near_ints(answer, rng, 60),
        "explanation": (
            f"Profit is shared in the ratio of capital x time: "
            f"{c1} x {t1} : {c2} x {t2} = {c1 * t1}:{c2 * t2}. A's share = "
            f"{total} x {c1 * t1}/{unit} = {answer}."
        ),
        "verification_data": {
            "op": "r_partnership",
            "c1": c1,
            "t1": t1,
            "c2": c2,
            "t2": t2,
            "total": total,
        },
    }


def build_ratio() -> Bank:
    bank = Bank("Ratio and Proportion", "ratio_proportion", seed=604)
    spec = [
        (1, "EASY", 5, r_divide, 1),
        (1, "EASY", 4, r_prop, 1),
        (1, "EASY", 3, r_boys, 2),
        (1, "EASY", 3, r_share, 2),
        (2, "EASY", 4, r_divide, 3),
        (2, "MEDIUM", 4, r_prop, 2),
        (2, "MEDIUM", 4, r_combine, 3),
        (2, "MEDIUM", 4, r_mean, 4),
        (2, "MEDIUM", 4, r_inverse, 4),
        (3, "MEDIUM", 5, r_combine, 1),
        (3, "MEDIUM", 5, r_mean, 2),
        (3, "MEDIUM", 5, r_third, 3),
        (3, "HARD", 5, r_ages, 4),
        (3, "MEDIUM", 5, r_coins, 1),
        (3, "HARD", 5, r_partnership, 2),
        (4, "HARD", 10, r_ages, 1),
        (4, "HARD", 10, r_income, 2),
        (4, "HARD", 10, r_coins, 3),
        (4, "HARD", 10, r_partnership, 4),
        (4, "HARD", 10, r_mixture, 1),
        (4, "HARD", 5, r_third, 2),
    ]
    for part, difficulty, count, fn, page in spec:
        fill(bank, part, difficulty, count, fn, SOURCE, PAGES[page])
    return bank
