# -*- coding: utf-8 -*-
"""Compound Interest - 120 verified questions for the third Maths batch."""

from __future__ import annotations

from fractions import Fraction

from .bank import fmt_dec, near_ints, near_values

SOURCE = "Compound Interest class notes and mains topic-wise sets (local PDFs)"
PAGES = {
    1: "Compound Interest 01_Class Notes, pp. 1-14",
    2: "Compound Interest 02_Class Notes, pp. 1-18",
    3: "Compound Interest 03_ Class Notes, pp. 1-15",
    4: "Mains Topic wise Simple Interest and Compound Interest Set 1, pp. 1-8",
    5: "Mains Topic wise Simple Interest and Compound Interest Set 2, pp. 1-9",
    6: "Mains Topic wise Application Based DI Simple Interest And Compound, pp. 1-15",
}

WHO = [
    ("Isha", "a recurring deposit"), ("Dev", "a term deposit"),
    ("Riya", "a capital scheme"), ("Nikhil", "a savings plan"),
    ("Sneha", "a business deposit"), ("Aditya", "an investment"),
    ("Tara", "a bank deposit"), ("Manav", "a fixed deposit"),
    ("Pooja", "a wealth scheme"), ("Aman", "a compound scheme"),
]


def who(v, offset=0):
    return WHO[(v * 2 + offset) % len(WHO)]


def factor(rate, periods):
    per = Fraction(rate) if isinstance(rate, (int, Fraction)) else Fraction(str(rate))
    return (1 + per / 100) ** periods


def amount(p, rate, periods):
    return Fraction(p) * factor(rate, periods)


def dec(value):
    return fmt_dec(float(value), 2)


def q(family, variant, text, answer, distractors, explanation, inputs):
    return {
        "text": text,
        "correct": str(answer),
        "distractors": [str(d) for d in distractors],
        "explanation": explanation,
        "verification_data": {"family": family, "variant": variant, "inputs": inputs},
    }


def ci_amount_annual(r, v):
    name, scheme = who(v)
    p = r.choice([8000, 10000, 12000, 15000, 20000])
    rate = r.choice([5, 8, 10, 12])
    t = r.choice([2, 3])
    a = amount(p, rate, t)
    answer = dec(a)
    return q(
        "ci_amount_annual", v,
        f"Find the amount when {name} invests Rs.{p} in {scheme} at {rate}% "
        f"compounded annually for {t} years.",
        answer, near_values(answer, r, 15),
        f"A = P(1 + R/100)^T = {p}(1 + {rate}/100)^{t} = {answer}.",
        {"P": p, "R": rate, "T": t, "A": answer},
    )


def ci_interest_annual(r, v):
    name, scheme = who(v, 1)
    p = r.choice([8000, 10000, 12000, 15000])
    rate = r.choice([5, 8, 10])
    t = r.choice([2, 3])
    a = amount(p, rate, t)
    ci = a - p
    answer = dec(ci)
    return q(
        "ci_interest_annual", v,
        f"{name} puts Rs.{p} into {scheme} at {rate}% compound interest for {t} "
        "years, compounded yearly. What interest is earned?",
        answer, near_values(answer, r, 12),
        f"A = {dec(a)}; compound interest = {dec(a)} - {p} = {answer}.",
        {"P": p, "R": rate, "T": t, "CI": answer},
    )


def ci_half_amount(r, v):
    name, scheme = who(v, 2)
    p = r.choice([8000, 12000, 16000, 20000])
    rate = r.choice([8, 10, 12])
    t = r.choice([1, 2])
    periods = 2 * t
    half_rate = Fraction(rate, 2)
    a = amount(p, half_rate, periods)
    answer = dec(a)
    return q(
        "ci_half_amount", v,
        f"{name} deposits Rs.{p} in {scheme} at {rate}% per annum compounded "
        f"half-yearly for {t} year(s). Find the maturity amount.",
        answer, near_values(answer, r, 15),
        f"Rate per half-year = {rate}/2 percent; periods = {periods}; A = {answer}.",
        {"P": p, "R": rate, "T": t, "A": answer},
    )


def ci_half_interest(r, v):
    name, scheme = who(v, 3)
    p = r.choice([10000, 12000, 16000])
    rate = r.choice([8, 10, 12])
    a = amount(p, Fraction(rate, 2), 2)
    answer = dec(a - p)
    return q(
        "ci_half_interest", v,
        f"Calculate the compound interest for {name} on Rs.{p} in {scheme} at "
        f"{rate}% per annum compounded half-yearly for one year.",
        answer, near_values(answer, r, 12),
        f"Half-yearly rate = {Fraction(rate, 2)}% for 2 periods; A = {dec(a)}, CI = {answer}.",
        {"P": p, "R": rate, "T": 1, "CI": answer},
    )


def ci_quarter_amount(r, v):
    name, scheme = who(v, 4)
    p = r.choice([12000, 16000, 20000])
    rate = r.choice([8, 10, 12])
    a = amount(p, Fraction(rate, 4), 4)
    answer = dec(a)
    return q(
        "ci_quarter_amount", v,
        f"{name} invests Rs.{p} in {scheme} at {rate}% per annum compounded "
        "quarterly for one year. What amount is received?",
        answer, near_values(answer, r, 15),
        f"Quarterly rate = {Fraction(rate, 4)}%; 4 periods; A = {answer}.",
        {"P": p, "R": rate, "T": 1, "A": answer},
    )


def ci_quarter_interest(r, v):
    name, scheme = who(v, 5)
    p = r.choice([12000, 16000, 20000])
    rate = r.choice([8, 10, 12])
    a = amount(p, Fraction(rate, 4), 4)
    answer = dec(a - p)
    return q(
        "ci_quarter_interest", v,
        f"Find the quarterly-compounded interest on Rs.{p} for {name}'s {scheme} "
        f"at {rate}% per annum for one year.",
        answer, near_values(answer, r, 12),
        f"Quarterly rate = {Fraction(rate, 4)}% for 4 periods; A = {dec(a)}; CI = {answer}.",
        {"P": p, "R": rate, "T": 1, "CI": answer},
    )


def ci_principal(r, v):
    presets = [(12100, 10, 2, 10000), (11236, 6, 2, 10000), (13310, 10, 3, 10000)]
    a, rate, t, p = presets[v % len(presets)]
    name, scheme = who(v, 6)
    return q(
        "ci_principal", v,
        f"{name}'s {scheme} matured to Rs.{a} after {t} years at {rate}% "
        "compounded annually. Find the original sum.",
        p, near_ints(p, r, 8),
        f"P = A / (1 + R/100)^T = {a} / (1 + {rate}/100)^{t} = {p}.",
        {"A": a, "R": rate, "T": t, "P": p},
    )


def ci_find_rate(r, v):
    presets = [(10000, 12100, 2, 10), (8000, 9261, 3, 5), (12000, 14520, 2, 10)]
    p, a, t, rate = presets[v % len(presets)]
    name, scheme = who(v, 7)
    return q(
        "ci_find_rate", v,
        f"Rs.{p} in {scheme} became Rs.{a} for {name} in {t} years with annual "
        "compounding. What was the yearly rate?",
        rate, near_ints(rate, r, 3),
        f"Since {a}/{p} = (1 + R/100)^{t}, the annual rate is {rate}%.",
        {"P": p, "A": a, "T": t, "R": rate},
    )


def ci_find_time(r, v):
    presets = [(10000, 12100, 2, 10), (8000, 9261, 3, 5), (10000, 14400, 2, 20)]
    p, a, t, rate = presets[v % len(presets)]
    name, scheme = who(v, 8)
    return q(
        "ci_find_time", v,
        f"At {rate}% compounded annually, how many years did {name}'s Rs.{p} "
        f"take to become Rs.{a} in {scheme}?",
        t, near_ints(t, r, 2),
        f"(1 + {rate}/100)^T = {a}/{p}, so T = {t} years.",
        {"P": p, "A": a, "R": rate, "T": t},
    )


def ci_si_ci_diff2(r, v):
    presets = [(8000, 5), (12000, 10), (20000, 5), (16000, 12), (10000, 10)]
    p, rate = presets[v % len(presets)]
    diff = Fraction(p) * Fraction(rate, 100) ** 2
    answer = dec(diff)
    name, scheme = who(v, 9)
    return q(
        "ci_si_ci_diff2", v,
        f"For Rs.{p} at {rate}% for 2 years, how much more is compound interest "
        f"than simple interest in {name}'s {scheme}?",
        answer, near_values(answer, r, 10),
        f"For 2 years, CI - SI = P(R/100)^2 = {p} x ({rate}/100)^2 = {answer}.",
        {"P": p, "R": rate, "T": 2, "D": answer},
    )


def ci_si_ci_diff3(r, v):
    presets = [(10000, 10), (8000, 5), (12000, 10), (16000, 5), (20000, 10)]
    p, rate = presets[v % len(presets)]
    rr = Fraction(rate, 100)
    diff = Fraction(p) * rr * rr * (3 + rr)
    answer = dec(diff)
    name, scheme = who(v, 1)
    return q(
        "ci_si_ci_diff3", v,
        f"{name} compares CI and SI on Rs.{p} in {scheme} at {rate}% for 3 years. "
        "What is the difference?",
        answer, near_values(answer, r, 12),
        f"For 3 years, CI - SI = P(R/100)^2(3 + R/100) = {answer}.",
        {"P": p, "R": rate, "T": 3, "D": answer},
    )


def ci_growth(r, v):
    place = ["a town", "a village", "a colony", "a city", "a campus"][v]
    start = r.choice([4000, 5000, 8000, 10000])
    rate = r.choice([5, 10, 20])
    a = amount(start, rate, 2)
    answer = dec(a)
    return q(
        "ci_growth", v,
        f"The population of {place} is {start} and grows at {rate}% per year "
        "compounded annually. What will it be after two years?",
        answer, near_values(answer, r, 15),
        f"Population = {start}(1 + {rate}/100)^2 = {answer}.",
        {"P": start, "R": rate, "T": 2, "A": answer},
    )


def ci_depreciation(r, v):
    item = ["a machine", "a laptop", "a vehicle", "a device", "an instrument"][v]
    p = r.choice([10000, 20000, 25000, 30000])
    rate = r.choice([5, 10, 20])
    a = amount(p, -rate, 2)
    answer = dec(a)
    return q(
        "ci_depreciation", v,
        f"The value of {item} is Rs.{p}. It depreciates at {rate}% per year. "
        "What is its value after two years?",
        answer, near_values(answer, r, 15),
        f"Value = {p}(1 - {rate}/100)^2 = {answer}.",
        {"P": p, "R": rate, "T": 2, "A": answer},
    )


def ci_variable_rates(r, v):
    presets = [(10000, 5, 8, 11340), (8000, 10, 5, 9240), (12000, 5, 10, 13860)]
    p, r1, r2, a = presets[v % len(presets)]
    name, scheme = who(v, 2)
    return q(
        "ci_variable_rates", v,
        f"{name} invests Rs.{p} in {scheme} at {r1}% in the first year and "
        f"{r2}% in the second year, compounded annually. Find the amount.",
        a, near_ints(a, r, 8),
        f"Amount = {p} x (1 + {r1}/100) x (1 + {r2}/100) = {a}.",
        {"P": p, "R1": r1, "R2": r2, "A": a},
    )


def ci_amount_ratio(r, v):
    name, scheme = who(v, 3)
    p = r.choice([10000, 12000, 15000])
    r1, r2 = r.sample([5, 8, 10, 12], 2)
    t = 2
    a1 = dec(amount(p, r1, t))
    a2 = dec(amount(p, r2, t))
    answer = f"{a1}:{a2}"
    distractors = [f"{a2}:{a1}", f"{p}:{p}", f"{float(a1)+100:.2f}:{a2}"]
    return q(
        "ci_amount_ratio", v,
        f"Equal sums of Rs.{p} are invested in {scheme} by {name} at {r1}% and "
        f"{r2}% for {t} years with annual compounding. Find the ratio of the amounts.",
        answer, distractors,
        f"Amounts are {a1} and {a2}, so the ratio is {answer}.",
        {"P": p, "R1": r1, "R2": r2, "T": t, "A1": a1, "A2": a2},
    )


def ci_half_annual_diff(r, v):
    presets = [(20000, 10), (12000, 10), (10000, 20), (16000, 10), (24000, 10)]
    p, rate = presets[v % len(presets)]
    annual = amount(p, rate, 1)
    half = amount(p, Fraction(rate, 2), 2)
    answer = dec(half - annual)
    name, scheme = who(v, 4)
    return q(
        "ci_half_annual_diff", v,
        f"How much more interest does {name} earn from {scheme} on Rs.{p} at "
        f"{rate}% compounded half-yearly rather than yearly for one year?",
        answer, near_values(answer, r, 10),
        f"Half-yearly amount = {dec(half)}, yearly amount = {dec(annual)}; difference = {answer}.",
        {"P": p, "R": rate, "T": 1, "D": answer},
    )


def ci_quarter_annual_diff(r, v):
    presets = [(20000, 8), (16000, 12), (12000, 8), (10000, 20), (24000, 8)]
    p, rate = presets[v % len(presets)]
    annual = amount(p, rate, 1)
    quarter = amount(p, Fraction(rate, 4), 4)
    answer = dec(quarter - annual)
    name, scheme = who(v, 5)
    return q(
        "ci_quarter_annual_diff", v,
        f"For Rs.{p} in {scheme} at {rate}% for one year, find the extra interest "
        f"from quarterly compounding over annual compounding for {name}.",
        answer, near_values(answer, r, 10),
        f"Quarterly amount = {dec(quarter)}, annual amount = {dec(annual)}; extra = {answer}.",
        {"P": p, "R": rate, "T": 1, "D": answer},
    )


def ci_fractional_rate(r, v):
    presets = [(8000, Fraction(5, 2)), (16000, Fraction(15, 2)), (16000, Fraction(5, 2))]
    p, rate = presets[v % len(presets)]
    a = amount(p, rate, 2)
    answer = dec(a)
    name, scheme = who(v, 6)
    return q(
        "ci_fractional_rate", v,
        f"{name} earns compound interest on Rs.{p} in {scheme} at {rate}% "
        "per annum for 2 years. Find the amount.",
        answer, near_values(answer, r, 15),
        f"A = {p}(1 + {rate}/100)^2 = {answer}.",
        {"P": p, "R": str(rate), "T": 2, "A": answer},
    )


def ci_interest_year_ratio(r, v):
    presets = [(10000, 10), (8000, 5), (12000, 10), (16000, 5), (18000, 10)]
    p, rate = presets[v % len(presets)]
    rr = Fraction(rate, 100)
    first = Fraction(p) * rr
    second = first * (1 + rr)
    answer = f"{dec(second)}:{dec(first)}"
    name, scheme = who(v, 7)
    return q(
        "ci_interest_year_ratio", v,
        f"For {name}'s Rs.{p} in {scheme} at {rate}% compound interest, find the "
        "ratio of the interest earned in year 2 to the interest earned in year 1.",
        answer, [f"{dec(first)}:{dec(second)}", "1:1", f"{rate}:1"],
        f"First-year interest = {dec(first)}; second-year interest = {dec(second)}; ratio = {answer}.",
        {"P": p, "R": rate, "I1": dec(first), "I2": dec(second)},
    )


def ci_principal_from_ci(r, v):
    presets = [(2100, 10, 2, 10000), (1230, 5, 2, 12000), (3310, 10, 3, 10000)]
    ci, rate, t, p = presets[v % len(presets)]
    name, scheme = who(v, 8)
    return q(
        "ci_principal_from_ci", v,
        f"{name} received Rs.{ci} as compound interest from {scheme} at {rate}% "
        f"for {t} years. What sum was invested?",
        p, near_ints(p, r, 8),
        f"A = P + CI = {p + ci}; P = A/(1 + R/100)^T = {p}.",
        {"CI": ci, "R": rate, "T": t, "P": p, "A": p + ci},
    )


def ci_three_year_amount(r, v):
    name, scheme = who(v, 9)
    p = r.choice([8000, 10000, 12000])
    rate = r.choice([5, 10])
    a = amount(p, rate, 3)
    answer = dec(a)
    return q(
        "ci_three_year_amount", v,
        f"Calculate the amount after 3 years for Rs.{p} in {scheme} at {rate}% "
        f"compounded annually for {name}.",
        answer, near_values(answer, r, 15),
        f"A = {p}(1 + {rate}/100)^3 = {answer}.",
        {"P": p, "R": rate, "T": 3, "A": answer},
    )


def ci_half_rate(r, v):
    presets = [(10000, 10, 2), (8000, 5, 2), (12000, 10, 2), (16000, 8, 1), (20000, 12, 1)]
    p, rate, t = presets[v % len(presets)]
    a = dec(amount(p, Fraction(rate, 2), 2 * t))
    name, scheme = who(v, 1)
    return q(
        "ci_half_rate", v,
        f"Rs.{p} in {name}'s {scheme} became Rs.{a} in {t} years with "
        f"{2 * t} half-year periods. What was the annual rate, compounded half-yearly?",
        rate, near_ints(rate, r, 3),
        f"The half-yearly rate is {rate}/2 percent; over {2*t} periods the amount is {a}, so the annual rate is {rate}%.",
        {"P": p, "A": a, "T": t, "R": rate},
    )


def ci_compare(r, v):
    presets = [
        (10000, 10, 1, 10000, 12, 1),
        (8000, 5, 2, 9000, 10, 2),
        (10000, 20, 1, 11000, 10, 1),
        (12000, 5, 2, 10000, 12, 2),
        (15000, 10, 1, 14000, 15, 1),
    ]
    p1, r1, t1, p2, r2, t2 = presets[v % len(presets)]
    a1 = amount(p1, r1, t1)
    a2 = amount(p2, r2, t2)
    answer = "Scheme A" if a1 > a2 else "Scheme B" if a2 > a1 else "Both are equal"
    name = who(v, 2)[0]
    options = ["Scheme A", "Scheme B", "Both are equal", "Cannot be determined"]
    return {
        "text": (
            f"{name} compares two deposits: A has Rs.{p1} at {r1}% for {t1} year(s), "
            f"B has Rs.{p2} at {r2}% for {t2} years, both compounded yearly. "
            "Which gives the larger amount?"
        ),
        "correct": answer,
        "distractors": [o for o in options if o != answer],
        "explanation": f"A gives {dec(a1)} and B gives {dec(a2)}; hence {answer}.",
        "verification_data": {
            "family": "ci_compare", "variant": v,
            "inputs": {"P1": p1, "R1": r1, "T1": t1, "P2": p2, "R2": r2, "T2": t2, "A1": dec(a1), "A2": dec(a2)},
        },
    }


def ci_two_scheme_diff(r, v):
    presets = [
        (10000, 10, 8000, 15, 2, 480),
        (12000, 5, 10000, 8, 2, 434),
        (8000, 10, 12000, 5, 2, 450),
        (15000, 8, 10000, 10, 2, 396),
        (20000, 5, 16000, 10, 2, 1310),
    ]
    p1, r1, p2, r2, t, diff = presets[v % len(presets)]
    ci1 = amount(p1, r1, t).numerator - p1
    ci2 = amount(p2, r2, t).numerator - p2
    name, scheme = who(v, 3)
    return q(
        "ci_two_scheme_diff", v,
        f"{name} compares Rs.{p1} in {scheme} at {r1}% with Rs.{p2} at {r2}% "
        f"for {t} years, both compounded yearly. What is the difference between "
        "the two compound interests?",
        diff, near_ints(diff, r, 8),
        f"Interests are {ci1} and {ci2}; the difference is {diff}.",
        {"P1": p1, "R1": r1, "P2": p2, "R2": r2, "T": t, "CI1": ci1, "CI2": ci2},
    )


FAMILIES = [
    ci_amount_annual, ci_interest_annual, ci_half_amount, ci_half_interest,
    ci_quarter_amount, ci_quarter_interest, ci_principal, ci_find_rate,
    ci_find_time, ci_si_ci_diff2, ci_si_ci_diff3, ci_growth,
    ci_depreciation, ci_variable_rates, ci_amount_ratio, ci_half_annual_diff,
    ci_quarter_annual_diff, ci_fractional_rate, ci_interest_year_ratio,
    ci_principal_from_ci, ci_three_year_amount, ci_half_rate, ci_compare,
    ci_two_scheme_diff,
]


def build_compound_interest():
    spec = []
    page_sets = [1, 2, 3, 4, 5, 6]
    for index, fn in enumerate(FAMILIES):
        part = 1 if index < 3 else 2 if index < 7 else 3 if index < 13 else 4
        difficulty = "EASY" if index < 7 else "MEDIUM" if index < 19 else "HARD"
        for variant in range(5):
            spec.append((part, difficulty, lambda r, f=fn, v=variant: f(r, v), page_sets[index % len(page_sets)]))
    return spec
