# -*- coding: utf-8 -*-
"""Simple Interest - 120 verified questions for the third Maths batch."""

from __future__ import annotations

from fractions import Fraction

from .bank import fmt, near_ints, near_values

SOURCE = "Simple Interest class notes and mains topic-wise sets (local PDFs)"
PAGES = {
    1: "Simple Interest 01_Class Notes, pp. 1-28",
    2: "Simple Interest 02_Class Notes, pp. 1-18",
    3: "Simple Interest 03_Class Notes, pp. 1-13",
    4: "Mains Topic wise Simple Interest and Compound Interest Set 1, pp. 1-8",
    5: "Mains Topic wise Simple Interest and Compound Interest Set 2, pp. 1-9",
    6: "Mains Topic wise Simple Interest and Compound Interest Set 4, pp. 1-6",
}

WHO = [
    ("Meera", "a fixed deposit"), ("Arjun", "a savings scheme"),
    ("Priya", "a small-business loan"), ("Karan", "a recurring deposit"),
    ("Neha", "an investment scheme"), ("Rohan", "a deposit"),
    ("Sita", "a bank scheme"), ("Vikram", "a term deposit"),
    ("Anita", "a personal loan"), ("Deepak", "a finance plan"),
]


def q(family, variant, text, answer, distractors, explanation, inputs):
    return {
        "text": text,
        "correct": str(answer),
        "distractors": [str(d) for d in distractors],
        "explanation": explanation,
        "verification_data": {
            "family": family,
            "variant": variant,
            "inputs": inputs,
        },
    }


def who(v, offset=0):
    return WHO[(v * 2 + offset) % len(WHO)]


def si_interest(r, v):
    name, scheme = who(v)
    p = r.choice([4000, 6000, 8000, 12000, 15000, 18000, 24000])
    rate = r.choice([4, 5, 6, 8, 10, 12])
    t = r.choice([2, 3, 4, 5])
    interest = Fraction(p * rate * t, 100)
    assert interest.denominator == 1
    answer = interest.numerator
    text = (
        f"{name} puts Rs.{p} into {scheme} at {rate}% simple interest for {t} years. "
        "How much interest is earned?"
    )
    return q(
        "si_interest", v, text, answer, near_ints(answer, r),
        f"Simple interest = P x R x T / 100 = {p} x {rate} x {t} / 100 = {answer}.",
        {"P": p, "R": rate, "T": t},
    )


def si_amount(r, v):
    name, scheme = who(v, 1)
    p = r.choice([5000, 7500, 9000, 12500, 16000, 20000])
    rate = r.choice([5, 6, 8, 10, 12])
    t = r.choice([2, 3, 4])
    interest = Fraction(p * rate * t, 100)
    assert interest.denominator == 1
    answer = p + interest.numerator
    text = (
        f"Find the maturity amount when {name} deposits Rs.{p} in {scheme} "
        f"for {t} years at {rate}% per annum simple interest."
    )
    return q(
        "si_amount", v, text, answer, near_ints(answer, r, 7),
        f"Interest = {p} x {rate} x {t} / 100 = {interest.numerator}; amount = {p} + {interest.numerator} = {answer}.",
        {"P": p, "R": rate, "T": t},
    )


def si_principal(r, v):
    name, scheme = who(v, 2)
    rate = r.choice([5, 6, 8, 10, 12])
    t = r.choice([2, 3, 4])
    p = r.choice([5000, 8000, 10000, 12000, 15000])
    interest = Fraction(p * rate * t, 100)
    assert interest.denominator == 1
    answer = p
    text = (
        f"{name} earned Rs.{interest.numerator} as simple interest from {scheme} "
        f"in {t} years at {rate}% per annum. What sum was deposited?"
    )
    return q(
        "si_principal", v, text, answer, near_ints(answer, r, 8),
        f"P = (SI x 100) / (R x T) = ({interest.numerator} x 100) / ({rate} x {t}) = {answer}.",
        {"I": interest.numerator, "R": rate, "T": t},
    )


def si_rate(r, v):
    name, scheme = who(v, 3)
    p = r.choice([6000, 8000, 10000, 12000, 16000])
    t = r.choice([2, 3, 4])
    rate = r.choice([4, 5, 6, 8, 10])
    interest = Fraction(p * rate * t, 100)
    assert interest.denominator == 1
    text = (
        f"A deposit of Rs.{p} in {scheme} for {name} grew by "
        f"Rs.{interest.numerator} in {t} years. Find the annual simple interest rate."
    )
    return q(
        "si_rate", v, text, rate, near_ints(rate, r, 3),
        f"R = (SI x 100) / (P x T) = ({interest.numerator} x 100) / ({p} x {t}) = {rate}%.",
        {"I": interest.numerator, "P": p, "T": t},
    )


def si_time(r, v):
    name, scheme = who(v, 4)
    p = r.choice([5000, 8000, 10000, 12000])
    rate = r.choice([5, 8, 10, 12])
    t = r.choice([2, 3, 4])
    interest = Fraction(p * rate * t, 100)
    assert interest.denominator == 1
    text = (
        f"For how many years must {name} keep Rs.{p} in {scheme} at {rate}% "
        f"simple interest to earn Rs.{interest.numerator}?"
    )
    return q(
        "si_time", v, text, t, near_ints(t, r, 2),
        f"T = (SI x 100) / (P x R) = ({interest.numerator} x 100) / ({p} x {rate}) = {t} years.",
        {"I": interest.numerator, "P": p, "R": rate},
    )


def si_amount_principal(r, v):
    name, scheme = who(v, 5)
    rate = r.choice([5, 8, 10, 12])
    t = r.choice([2, 3])
    p = r.choice([4000, 6000, 8000, 10000])
    amount = p + Fraction(p * rate * t, 100).numerator
    text = (
        f"The amount in {name}'s {scheme} after {t} years at {rate}% simple "
        f"interest is Rs.{amount}. What was the original principal?"
    )
    return q(
        "si_amount_principal", v, text, p, near_ints(p, r, 8),
        f"A = P(1 + RT/100), so P = A x 100 / (100 + RT) = {amount} x 100 / (100 + {rate * t}) = {p}.",
        {"A": amount, "R": rate, "T": t},
    )


def si_amount_rate(r, v):
    name, scheme = who(v, 6)
    p = r.choice([5000, 8000, 10000, 12000])
    t = r.choice([2, 3, 4])
    rate = r.choice([5, 6, 8, 10])
    amount = p + Fraction(p * rate * t, 100).numerator
    text = (
        f"{name} deposited Rs.{p} in {scheme}; after {t} years the amount was "
        f"Rs.{amount}. Find the simple interest rate applied each year."
    )
    return q(
        "si_amount_rate", v, text, rate, near_ints(rate, r, 3),
        f"Interest = {amount} - {p} = {amount - p}; R = (I x 100)/(P x T) = {rate}%.",
        {"A": amount, "P": p, "T": t},
    )


def si_amount_time(r, v):
    name, scheme = who(v, 7)
    p = r.choice([6000, 8000, 10000])
    rate = r.choice([5, 8, 10])
    t = r.choice([2, 3, 4])
    amount = p + Fraction(p * rate * t, 100).numerator
    text = (
        f"Rs.{p} placed in {scheme} by {name} became Rs.{amount} at {rate}% "
        "per annum simple interest. For how long was it invested?"
    )
    return q(
        "si_amount_time", v, text, t, near_ints(t, r, 2),
        f"Interest = {amount - p}; T = (I x 100)/(P x R) = {t} years.",
        {"A": amount, "P": p, "R": rate},
    )


def si_months(r, v):
    name, scheme = who(v, 8)
    p = r.choice([6000, 9000, 12000, 18000])
    rate = r.choice([6, 8, 9, 12])
    months = r.choice([6, 9, 15, 18, 24])
    interest = Fraction(p * rate * months, 1200)
    if interest.denominator != 1:
        return None
    text = (
        f"{name} lent Rs.{p} under {scheme} at {rate}% simple interest for "
        f"{months} months. Compute the interest payable."
    )
    return q(
        "si_months", v, text, interest.numerator, near_ints(interest.numerator, r),
        f"Convert months to years: T = {months}/12. SI = {p} x {rate} x {months}/12 / 100 = {interest.numerator}.",
        {"P": p, "R": rate, "M": months},
    )


def si_days365(r, v):
    presets = [(20000, 5, 73), (36500, 4, 45), (15000, 6, 73), (24000, 5, 73)]
    p, rate, days = presets[v % len(presets)]
    name, scheme = who(v, 9)
    interest = Fraction(p * rate * days, 36500)
    assert interest.denominator == 1
    text = (
        f"{name} kept Rs.{p} in {scheme} for {days} days at {rate}% simple "
        "interest, using a 365-day year. Find the interest."
    )
    return q(
        "si_days365", v, text, interest.numerator, near_ints(interest.numerator, r),
        f"SI = {p} x {rate} x {days} / (365 x 100) = {interest.numerator}.",
        {"P": p, "R": rate, "D": days},
    )


def si_days360(r, v):
    presets = [(18000, 5, 72), (24000, 6, 60), (12000, 8, 90), (30000, 4, 72)]
    p, rate, days = presets[v % len(presets)]
    name, scheme = who(v, 1)
    interest = Fraction(p * rate * days, 36000)
    assert interest.denominator == 1
    text = (
        f"Using a 360-day year, what interest does {name} get on Rs.{p} from "
        f"{scheme} at {rate}% for {days} days?"
    )
    return q(
        "si_days360", v, text, interest.numerator, near_ints(interest.numerator, r),
        f"SI = {p} x {rate} x {days} / (360 x 100) = {interest.numerator}.",
        {"P": p, "R": rate, "D": days},
    )


def si_double(r, v):
    name, scheme = who(v, 2)
    rate = r.choice([4, 5, 8, 10, 12, 16, 20])
    years = Fraction(100, rate)
    answer = fmt(years)
    text = (
        f"At {rate}% per annum simple interest, in how many years will the "
        f"money in {name}'s {scheme} double itself?"
    )
    distractors = near_values(answer, r, 1)
    return q(
        "si_double", v, text, answer, distractors,
        f"To double, SI = P, so T = 100/R = 100/{rate} = {answer} years.",
        {"R": rate},
    )


def si_triple(r, v):
    name, scheme = who(v, 3)
    rate = r.choice([5, 8, 10, 12, 16, 20])
    years = Fraction(200, rate)
    answer = fmt(years)
    text = (
        f"{name} wants the deposit in {scheme} to become three times the "
        f"principal at {rate}% simple interest. How long will it take?"
    )
    return q(
        "si_triple", v, text, answer, near_values(answer, r, 1),
        f"To triple, SI = 2P, so T = 200/R = 200/{rate} = {answer} years.",
        {"R": rate},
    )


def si_rate_double(r, v):
    name, scheme = who(v, 4)
    years = r.choice([4, 5, 8, 10, 12, 16, 20])
    rate = Fraction(100, years)
    answer = fmt(rate)
    text = (
        f"What annual simple interest rate will make {name}'s {scheme} "
        f"amount double in {years} years?"
    )
    return q(
        "si_rate_double", v, text, answer, near_values(answer, r, 1),
        f"For doubling, R = 100/T = 100/{years} = {answer}%.",
        {"T": years},
    )


def si_split_equal(r, v):
    name, scheme = who(v, 5)
    r1, r2 = r.sample([5, 6, 8, 10, 12, 15], 2)
    total = r.choice([12000, 18000, 24000, 30000])
    p1 = Fraction(total * r2, r1 + r2)
    if p1.denominator != 1:
        return None
    answer = p1.numerator
    text = (
        f"{name} splits Rs.{total} between two deposits in {scheme}, one at "
        f"{r1}% and the other at {r2}% simple interest. The yearly interest is "
        "equal. How much is placed at the first rate?"
    )
    return q(
        "si_split_equal", v, text, answer, near_ints(answer, r, 8),
        f"Equal interest gives P1:P2 = {r2}:{r1}, so P1 = {total} x {r2}/({r1}+{r2}) = {answer}.",
        {"Total": total, "R1": r1, "R2": r2},
    )


def si_split_total_interest(r, v):
    name, scheme = who(v, 6)
    r1, r2 = r.sample([5, 6, 8, 10, 12], 2)
    total = r.choice([10000, 15000, 20000])
    t = 2
    p1 = r.choice([4000, 6000, 8000])
    p2 = total - p1
    interest = Fraction(p1 * r1 * t + p2 * r2 * t, 100)
    if interest.denominator != 1:
        return None
    text = (
        f"{name} invests Rs.{total} in two parts under {scheme}, at {r1}% and "
        f"{r2}% for {t} years. Total simple interest is Rs.{interest.numerator}. "
        "What amount was invested at the first rate?"
    )
    return q(
        "si_split_total_interest", v, text, p1, near_ints(p1, r, 8),
        f"Solve x x {r1} x {t}/100 + ({total}-x) x {r2} x {t}/100 = {interest.numerator}, giving x = {p1}.",
        {"Total": total, "R1": r1, "R2": r2, "T": t, "I": interest.numerator},
    )


def si_rate_diff(r, v):
    name, scheme = who(v, 7)
    p = r.choice([8000, 10000, 12000, 16000, 20000])
    t = r.choice([2, 3, 4])
    r1, r2 = r.sample([5, 7, 8, 10, 12, 15], 2)
    hi, lo = max(r1, r2), min(r1, r2)
    diff = Fraction(p * t * (hi - lo), 100)
    assert diff.denominator == 1
    text = (
        f"The same Rs.{p} could be placed in {scheme} at {hi}% or {lo}% for "
        f"{t} years. For {name}, how much more interest does the better option give?"
    )
    return q(
        "si_rate_diff", v, text, diff.numerator, near_ints(diff.numerator, r),
        f"Difference = P x T x (R1-R2)/100 = {p} x {t} x {hi-lo}/100 = {diff.numerator}.",
        {"P": p, "T": t, "R1": hi, "R2": lo},
    )


def si_time_ratio(r, v):
    name, scheme = who(v, 8)
    p, rate = r.choice([(8000, 5), (10000, 8), (12000, 10)])
    t1, t2 = r.sample([2, 3, 4, 5, 6], 2)
    answer = f"{t1}:{t2}"
    text = (
        f"For the same principal and rate in {scheme}, {name} compares interest "
        f"over {t1} years with interest over {t2} years. What is the ratio?"
    )
    distractors = [f"{t2}:{t1}", f"{t1 + 1}:{t2}", f"{t1}:{t2 + 1}"]
    return q(
        "si_time_ratio", v, text, answer, distractors,
        f"With P and R fixed, SI is proportional to T, so the ratio is {t1}:{t2}.",
        {"T1": t1, "T2": t2},
    )


def si_rate_ratio(r, v):
    name, scheme = who(v, 9)
    p, t = r.choice([(8000, 2), (10000, 3), (12000, 4)])
    r1, r2 = r.sample([5, 8, 10, 12], 2)
    answer = f"{r1}:{r2}"
    text = (
        f"{name} puts equal sums in {scheme} for {t} years at {r1}% and {r2}%. "
        "What is the ratio of the two simple interests?"
    )
    distractors = [f"{r2}:{r1}", f"{r1 + 1}:{r2}", f"{r1}:{r2 + 1}"]
    return q(
        "si_rate_ratio", v, text, answer, distractors,
        f"With P and T fixed, SI is proportional to R, so the ratio is {r1}:{r2}.",
        {"R1": r1, "R2": r2},
    )


def si_principal_ratio(r, v):
    name, scheme = who(v, 1)
    t, rate = r.choice([(2, 5), (3, 8), (4, 10)])
    p1, p2 = r.sample([5000, 8000, 10000, 12000], 2)
    answer = f"{p1}:{p2}"
    text = (
        f"Two deposits in {scheme}, one of Rs.{p1} and one of Rs.{p2}, earn "
        f"simple interest for {t} years at {rate}%. For {name}, find the ratio "
        "of their interests."
    )
    distractors = [f"{p2}:{p1}", f"{p1 + 1000}:{p2}", f"{p1}:{p2 + 1000}"]
    return q(
        "si_principal_ratio", v, text, answer, distractors,
        f"With R and T fixed, SI is proportional to P, so the ratio is {p1}:{p2}.",
        {"P1": p1, "P2": p2},
    )


def si_successive_rate(r, v):
    name, scheme = who(v, 2)
    p = r.choice([10000, 12000, 15000, 20000])
    t1, t2 = r.sample([1, 2, 3], 2)
    r1, r2 = r.sample([5, 6, 8, 10, 12], 2)
    interest = Fraction(p * (t1 * r1 + t2 * r2), 100)
    if interest.denominator != 1:
        return None
    text = (
        f"{name} invests Rs.{p} in {scheme} for {t1} year(s) at {r1}% and then "
        f"for {t2} year(s) at {r2}%, both at simple interest. Find the total interest."
    )
    return q(
        "si_successive_rate", v, text, interest.numerator,
        near_ints(interest.numerator, r, 7),
        f"Interest = {p} x ({t1}x{r1} + {t2}x{r2})/100 = {interest.numerator}.",
        {"P": p, "T1": t1, "T2": t2, "R1": r1, "R2": r2},
    )


def si_partial_withdrawal(r, v):
    name, scheme = who(v, 3)
    presets = [(20000, 5000, 2, 3, 5), (24000, 4000, 1, 4, 6), (18000, 3000, 2, 2, 8)]
    p, w, t1, t2, rate = presets[v % len(presets)]
    interest = Fraction(p * rate * t1 + (p - w) * rate * t2, 100)
    assert interest.denominator == 1
    text = (
        f"{name} deposits Rs.{p} in {scheme} at {rate}% simple interest. After "
        f"{t1} years, Rs.{w} is withdrawn; the rest stays for another {t2} years. "
        "What is the total interest?"
    )
    return q(
        "si_partial_withdrawal", v, text, interest.numerator,
        near_ints(interest.numerator, r, 7),
        f"Interest = {p}x{rate}x{t1}/100 + ({p}-{w})x{rate}x{t2}/100 = {interest.numerator}.",
        {"P": p, "W": w, "T1": t1, "T2": t2, "R": rate},
    )


def si_extra_deposit(r, v):
    name, scheme = who(v, 4)
    presets = [(10000, 5000, 2, 3, 6), (12000, 3000, 1, 4, 5), (15000, 5000, 2, 2, 8)]
    p, extra, t1, t2, rate = presets[v % len(presets)]
    amount = p + Fraction(p * rate * t1, 100).numerator + (p + extra) + Fraction((p + extra) * rate * t2, 100).numerator
    text = (
        f"{name} starts {scheme} with Rs.{p} at {rate}% simple interest. After "
        f"{t1} years, another Rs.{extra} is added, and the full amount is kept "
        f"for {t2} more years. What is the final amount?"
    )
    return q(
        "si_extra_deposit", v, text, amount, near_ints(amount, r, 9),
        f"First amount = {p} + {p}x{rate}x{t1}/100; second amount = {p+extra} + {p+extra}x{rate}x{t2}/100; total = {amount}.",
        {"P": p, "E": extra, "T1": t1, "T2": t2, "R": rate},
    )


def si_compare(r, v):
    name, scheme = who(v, 5)
    p = r.choice([8000, 10000, 12000])
    r1, r2 = r.sample([5, 8, 10, 12], 2)
    t = r.choice([2, 3, 4])
    i1 = Fraction(p * r1 * t, 100)
    i2 = Fraction(p * r2 * t, 100)
    answer = "Second option" if i2 > i1 else "First option"
    text = (
        f"{name} can choose {scheme} option A at {r1}% or option B at {r2}% "
        f"for {t} years on Rs.{p}. Which option pays more simple interest?"
    )
    distractors = [o for o in ["First option", "Second option", "Both pay equally", "Cannot be determined"] if o != answer]
    return {
        "text": text,
        "correct": answer,
        "distractors": distractors,
        "explanation": f"Option A gives {i1.numerator} and option B gives {i2.numerator}; hence {answer.lower()} pays more.",
        "verification_data": {"family": "si_compare", "variant": v, "inputs": {"P": p, "R1": r1, "R2": r2, "T": t}},
    }


FAMILIES = [
    si_interest, si_amount, si_principal, si_rate, si_time, si_amount_principal,
    si_amount_rate, si_amount_time, si_months, si_days365, si_days360,
    si_double, si_triple, si_rate_double, si_split_equal, si_split_total_interest,
    si_rate_diff, si_time_ratio, si_rate_ratio, si_principal_ratio,
    si_successive_rate, si_partial_withdrawal, si_extra_deposit, si_compare,
]


def build_simple_interest() -> list[tuple[int, str, object, int]]:
    """Return part, difficulty, generator, page-set number for 120 items."""
    spec: list[tuple[int, str, object, int]] = []
    page_sets = [1, 2, 3, 4, 5]
    for index, fn in enumerate(FAMILIES):
        part = 1 if index < 3 else 2 if index < 7 else 3 if index < 13 else 4
        difficulty = "EASY" if index < 7 else "MEDIUM" if index < 21 else "HARD"
        for variant in range(5):
            spec.append((part, difficulty, lambda r, f=fn, v=variant: f(r, v), page_sets[index % len(page_sets)]))
    return spec
