# -*- coding: utf-8 -*-
"""Number System - 120 verified questions for the second Maths batch."""

from __future__ import annotations

import math
from fractions import Fraction

from .bank import Bank, fill

SOURCE = "PW Banking Wallah - Number System Class Notes (local PDF)"
PAGES = {
    1: "Number System 01, pp. 3-27",
    2: "Number System 02, pp. 3-16",
    3: "Number System 03, pp. 3-12",
}


def near_ints(correct: int, rng, spread: int = 5) -> list[str]:
    values: list[str] = []
    while len(values) < 3:
        delta = rng.choice([-1, 1]) * rng.randint(1, spread)
        text = str(correct + delta)
        if text != str(correct) and text not in values:
            values.append(text)
    return values


def factorise(n: int) -> dict[int, int]:
    factors: dict[int, int] = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def divisor_count(n: int) -> int:
    total = 1
    for exponent in factorise(n).values():
        total *= exponent + 1
    return total


def divisor_sum(n: int) -> int:
    total = 1
    for prime, exponent in factorise(n).items():
        total *= (prime ** (exponent + 1) - 1) // (prime - 1)
    return total


def trailing_zeros(n: int) -> int:
    total, power = 0, 5
    while power <= n:
        total += n // power
        power *= 5
    return total


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def ns_mod(rng):
    b = rng.randint(7, 19)
    a = rng.randint(1000, 9999)
    answer = a % b
    quotient = a // b
    pool = [value for value in range(b) if value != answer]
    distractors = [str(value) for value in rng.sample(pool, 3)]
    return {
        "text": f"What remainder is left when {a} is divided by {b}?",
        "correct": str(answer),
        "distractors": distractors,
        "explanation": (
            f"{b} x {quotient} = {b * quotient}, so the remainder is "
            f"{a} - {b * quotient} = {answer}."
        ),
        "verification_data": {"op": "ns_mod", "a": a, "b": b},
    }


def ns_unit(rng):
    a = rng.randint(2, 9)
    b = rng.randint(3, 60)
    answer = pow(a, b, 10)
    cycle = [pow(a, i, 10) for i in range(1, 5)]
    position = b % 4 or 4
    return {
        "text": f"Find the unit digit of {a}^{b}.",
        "correct": str(answer),
        "distractors": [str((answer + d) % 10) for d in (1, 2, 3)],
        "explanation": (
            f"The unit digits of successive powers of {a} follow the cycle "
            f"{cycle}. Position {position} in that cycle gives the unit digit "
            f"{answer}."
        ),
        "verification_data": {"op": "ns_unit", "a": a, "b": b},
    }


def ns_gcd(rng):
    g = rng.randint(3, 18)
    picks: list[int] = []
    while len(picks) < 3:
        m = rng.randint(2, 12)
        if all(math.gcd(m, p) == 1 for p in picks):
            picks.append(m)
    nums = [g * m for m in picks]
    return {
        "text": (
            f"Find the greatest number that divides {nums[0]}, {nums[1]} and "
            f"{nums[2]} exactly."
        ),
        "correct": str(g),
        "distractors": near_ints(g, rng, 6),
        "explanation": (
            f"Write each number as a multiple: {nums[0]} = {g} x {picks[0]}, "
            f"{nums[1]} = {g} x {picks[1]}, {nums[2]} = {g} x {picks[2]}. The "
            f"multipliers are pairwise coprime, so the HCF is {g}."
        ),
        "verification_data": {"op": "ns_gcd", "nums": nums},
    }


def ns_lcm(rng):
    picks: list[int] = []
    while len(picks) < 3:
        m = rng.randint(2, 11)
        if all(math.gcd(m, p) == 1 for p in picks):
            picks.append(m)
    nums = picks
    answer = math.lcm(*nums)
    return {
        "text": (
            f"Find the least number that is exactly divisible by {nums[0]}, "
            f"{nums[1]} and {nums[2]}."
        ),
        "correct": str(answer),
        "distractors": near_ints(answer, rng, 10),
        "explanation": (
            f"The three numbers are pairwise coprime, so their LCM is their "
            f"product: {nums[0]} x {nums[1]} x {nums[2]} = {answer}."
        ),
        "verification_data": {"op": "ns_lcm", "nums": nums},
    }


def ns_divcount(rng):
    primes = [2, 3, 5, 7]
    chosen = sorted(rng.sample(primes, rng.randint(2, 3)))
    exponents = [rng.randint(1, 3) for _ in chosen]
    n = 1
    for p, e in zip(chosen, exponents):
        n *= p ** e
    answer = 1
    for e in exponents:
        answer *= e + 1
    factor_text = " x ".join(f"{p}^{e}" for p, e in zip(chosen, exponents))
    return {
        "text": f"Find the number of positive divisors of {n}.",
        "correct": str(answer),
        "distractors": near_ints(answer, rng, 4),
        "explanation": (
            f"{n} = {factor_text}. The number of factors is "
            + " x ".join(str(e + 1) for e in exponents)
            + f" = {answer}."
        ),
        "verification_data": {"op": "ns_divcount", "n": n},
    }


def ns_divsum(rng):
    primes = [2, 3, 5, 7]
    chosen = sorted(rng.sample(primes, rng.randint(2, 3)))
    exponents = [rng.randint(1, 2) for _ in chosen]
    n = 1
    for p, e in zip(chosen, exponents):
        n *= p ** e
    answer = divisor_sum(n)
    return {
        "text": f"Find the sum of all positive factors of {n}.",
        "correct": str(answer),
        "distractors": near_ints(answer, rng, 8),
        "explanation": (
            f"{n} = "
            + " x ".join(f"{p}^{e}" for p, e in zip(chosen, exponents))
            + ". Sum of factors = "
            + " x ".join(f"({p}^{e + 1} - 1)/({p} - 1)" for p, e in zip(chosen, exponents))
            + f" = {answer}."
        ),
        "verification_data": {"op": "ns_divsum", "n": n},
    }


def ns_zeros(rng):
    n = rng.randint(20, 180)
    answer = trailing_zeros(n)
    return {
        "text": f"How many trailing zeros are there in {n}! ?",
        "correct": str(answer),
        "distractors": near_ints(answer, rng, 4),
        "explanation": (
            f"Each trailing zero needs a factor 10. Count factors of 5 in {n}! "
            f"using floor division: {n}//5 + {n}//25 + ... = {answer}."
        ),
        "verification_data": {"op": "ns_zeros", "n": n},
    }


def ns_powmod(rng):
    a = rng.randint(2, 12)
    b = rng.randint(3, 20)
    m = rng.choice([7, 9, 11, 13, 17])
    answer = pow(a, b, m)
    return {
        "text": f"Find the remainder when {a}^{b} is divided by {m}.",
        "correct": str(answer),
        "distractors": near_ints(answer, rng, m - 1),
        "explanation": (
            f"Reduce step by step modulo {m}: the remainder of {a}^{b} is "
            f"{answer}. (Repeated squaring gives the same value.)"
        ),
        "verification_data": {"op": "ns_powmod", "a": a, "b": b, "m": m},
    }


def ns_pick_divisible(rng):
    d = rng.choice([4, 6, 7, 8, 9, 11, 12, 13])
    correct = d * rng.randint(12, 90)
    offsets = rng.sample(range(1, d), 3)
    options = [correct] + [correct + off for off in offsets]
    return {
        "text": (
            f"Which of the numbers {options[0]}, {options[1]}, {options[2]} and "
            f"{options[3]} is divisible by {d}?"
        ),
        "correct": str(correct),
        "distractors": [str(x) for x in options[1:]],
        "explanation": (
            f"{correct} = {d} x {correct // d}, so it is exactly divisible by {d}. "
            f"The other three leave non-zero remainders."
        ),
        "verification_data": {
            "op": "ns_pick_divisible",
            "divisor": d,
            "options": [str(x) for x in options],
        },
    }


def ns_missing_digit(rng):
    digits = [rng.randint(1, 9)] + [rng.randint(0, 9) for _ in range(5)]
    pos = rng.randint(0, 5)
    divisor = rng.choice([9, 11])
    known = [d for i, d in enumerate(digits) if i != pos]
    solution = None
    for x in range(10):
        trial = digits[:]
        trial[pos] = x
        number = int("".join(str(d) for d in trial))
        if number % divisor == 0:
            if solution is not None:
                return None
            solution = x
    if solution is None:
        return None
    shown = "".join("x" if i == pos else str(d) for i, d in enumerate(digits))
    if divisor == 9:
        why = (
            f"A number is divisible by 9 when its digit sum is a multiple of 9. "
            f"The known digits sum to {sum(known)}, so x must be {solution}."
        )
    else:
        why = (
            f"For divisibility by 11, the difference of the alternating digit sums "
            f"must be a multiple of 11; this forces x = {solution}."
        )
    return {
        "text": f"If the number {shown} is divisible by {divisor}, find the digit x.",
        "correct": str(solution),
        "distractors": [str((solution + d) % 10) for d in (1, 2, 3)],
        "explanation": why,
        "verification_data": {
            "op": "ns_missing_digit",
            "digits": digits,
            "pos": pos,
            "divisor": divisor,
        },
    }


def ns_frac_max(rng):
    dens = rng.sample([3, 4, 5, 6, 7, 8, 9, 11], 4)
    fracs = []
    for den in dens:
        num = rng.randint(1, den - 1)
        fracs.append(Fraction(num, den))
    if len(set(fracs)) != 4:
        return None
    best = max(fracs)
    labels = [f"{f.numerator}/{f.denominator}" for f in fracs]
    return {
        "text": (
            f"Which of the fractions {labels[0]}, {labels[1]}, {labels[2]} and "
            f"{labels[3]} is the largest?"
        ),
        "correct": labels[fracs.index(best)],
        "distractors": [lab for f, lab in zip(fracs, labels) if f != best],
        "explanation": (
            "Compare the fractions by cross-multiplication or by converting to "
            f"decimals: {labels[fracs.index(best)]} is the largest."
        ),
        "verification_data": {"op": "ns_frac_max", "fractions": labels},
    }


def ns_prime_pick(rng):
    while True:
        nums = [rng.randint(21, 99) for _ in range(4)]
        if len(set(nums)) != 4:
            continue
        primes = [n for n in nums if is_prime(n)]
        if len(primes) == 1:
            break
    correct = str(primes[0])
    return {
        "text": (
            f"Which of the numbers {nums[0]}, {nums[1]}, {nums[2]} and {nums[3]} "
            f"is a prime number?"
        ),
        "correct": correct,
        "distractors": [str(n) for n in nums if str(n) != correct],
        "explanation": (
            f"{correct} has no divisor other than 1 and itself. The other options "
            f"are composite."
        ),
        "verification_data": {"op": "ns_prime_pick", "options": [str(n) for n in nums]},
    }


def ns_hcf_lcm(rng):
    h = rng.randint(4, 20)
    a = h * rng.randint(2, 9)
    b = h * rng.randint(2, 9)
    product = a * b
    answer = product // h
    return {
        "text": (
            f"Two numbers have HCF {h} and product {product}. What is their LCM?"
        ),
        "correct": str(answer),
        "distractors": near_ints(answer, rng, 12),
        "explanation": (
            f"For two numbers, HCF x LCM = product. So LCM = {product}/{h} = {answer}."
        ),
        "verification_data": {"op": "ns_hcf_lcm", "a": a, "b": b, "h": h},
    }


def ns_even_divcount(rng):
    power = rng.randint(1, 4)
    odd = rng.choice([3, 5, 7, 9, 15, 21, 25, 27])
    n = (2 ** power) * odd
    answer = power * divisor_count(odd)
    return {
        "text": f"How many even factors does {n} have?",
        "correct": str(answer),
        "distractors": near_ints(answer, rng, 4),
        "explanation": (
            f"{n} = 2^{power} x {odd}. An even factor must contain at least one 2, "
            f"so there are {power} choices for the power of 2 and {divisor_count(odd)} "
            f"choices from {odd}: {power} x {divisor_count(odd)} = {answer}."
        ),
        "verification_data": {"op": "ns_even_divcount", "n": n},
    }


def ns_exp(rng):
    base = rng.randint(2, 5)
    e1, e2, e3 = rng.randint(2, 5), rng.randint(2, 5), rng.randint(1, 4)
    answer = base ** (e1 + e2 - e3)
    return {
        "text": f"Simplify: ({base}^{e1} x {base}^{e2}) / {base}^{e3}.",
        "correct": str(answer),
        "distractors": near_ints(answer, rng, 8),
        "explanation": (
            f"Add the exponents in the numerator and subtract the divisor's "
            f"exponent: {e1} + {e2} - {e3} = {e1 + e2 - e3}, so the value is "
            f"{base}^{e1 + e2 - e3} = {answer}."
        ),
        "verification_data": {
            "op": "ns_exp",
            "base": base,
            "e1": e1,
            "e2": e2,
            "e3": e3,
        },
    }


def build_number_system() -> Bank:
    bank = Bank("Number System", "number_system", seed=602)
    spec = [
        (1, "EASY", 4, ns_mod, 1),
        (1, "EASY", 3, ns_unit, 2),
        (1, "EASY", 3, ns_gcd, 1),
        (1, "EASY", 3, ns_lcm, 2),
        (1, "EASY", 2, ns_pick_divisible, 1),
        (2, "EASY", 3, ns_mod, 1),
        (2, "MEDIUM", 3, ns_unit, 3),
        (2, "MEDIUM", 2, ns_gcd, 2),
        (2, "MEDIUM", 2, ns_lcm, 3),
        (2, "MEDIUM", 4, ns_divcount, 2),
        (2, "EASY", 3, ns_pick_divisible, 2),
        (2, "MEDIUM", 3, ns_prime_pick, 3),
        (3, "MEDIUM", 5, ns_divcount, 3),
        (3, "MEDIUM", 4, ns_divsum, 2),
        (3, "MEDIUM", 4, ns_zeros, 3),
        (3, "HARD", 5, ns_powmod, 3),
        (3, "MEDIUM", 4, ns_missing_digit, 2),
        (3, "MEDIUM", 4, ns_frac_max, 1),
        (3, "HARD", 4, ns_hcf_lcm, 2),
        (4, "HARD", 8, ns_divsum, 3),
        (4, "HARD", 8, ns_zeros, 3),
        (4, "HARD", 10, ns_powmod, 3),
        (4, "HARD", 8, ns_missing_digit, 3),
        (4, "HARD", 7, ns_frac_max, 2),
        (4, "HARD", 7, ns_even_divcount, 3),
        (4, "HARD", 7, ns_exp, 3),
    ]
    for part, difficulty, count, fn, page in spec:
        fill(bank, part, difficulty, count, fn, SOURCE, PAGES[page])
    return bank
