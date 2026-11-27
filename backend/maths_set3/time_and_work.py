# -*- coding: utf-8 -*-
"""Time and Work - 120 verified questions for the third Maths batch."""

from __future__ import annotations

import math
from fractions import Fraction

from .bank import fmt, fmt_dec, near_ints, near_values

SOURCE = "Time and Work class notes and topic-wise sets (local PDFs)"
PAGES = {
    1: "Time and Work 01 Class Notes, pp. 1-19",
    2: "Time and Work 02 Class Notes, pp. 1-15",
    3: "Time and Work 03_Class Notes, pp. 1-13",
    4: "Time and Work (VArdaan 3.0) 45 Questions, pp. 1-13",
}

NAMES = [
    ("Rohit", "Mohit"), ("Neha", "Divya"), ("Karan", "Aman"),
    ("Pooja", "Sneha"), ("Vivek", "Sachin"), ("Riya", "Tara"),
    ("Akash", "Deepak"), ("Meera", "Isha"), ("Nikhil", "Gaurav"),
    ("Swati", "Anjali"),
]


def pair(v):
    return NAMES[v % len(NAMES)]


def ratio_str(a, b):
    x, y = Fraction(a), Fraction(b)
    scale = math.lcm(x.denominator, y.denominator)
    first = x.numerator * (scale // x.denominator)
    second = y.numerator * (scale // y.denominator)
    g = math.gcd(abs(first), abs(second)) or 1
    return f"{first // g}:{second // g}"


def dec(value):
    return fmt_dec(float(value), 2)


def frac_str(value):
    value = Fraction(value)
    return fmt(value)


def q(family, variant, text, answer, distractors, explanation, inputs):
    return {
        "text": text,
        "correct": str(answer),
        "distractors": [str(d) for d in distractors],
        "explanation": explanation,
        "verification_data": {"family": family, "variant": variant, "inputs": inputs},
    }


def days_together(x, y):
    return Fraction(x * y, x + y)


def tw_basic_days(r, v):
    a, b = pair(v)
    presets = [(12, 24), (10, 15), (20, 30), (6, 12), (15, 30)]
    x, y = presets[v % len(presets)]
    answer = days_together(x, y)
    assert answer.denominator == 1
    return q(
        "tw_basic_days", v,
        f"{a} finishes a piece of work in {x} days and {b} in {y} days. "
        "How many days will they take working together?",
        answer.numerator, near_ints(answer.numerator, r, 4),
        f"Combined one-day work = 1/{x} + 1/{y}; time = {x}x{y}/({x}+{y}) = {answer.numerator} days.",
        {"X": x, "Y": y, "Days": answer.numerator},
    )


def tw_one_day_work(r, v):
    a, _ = pair(v + 1)
    x = [5, 8, 10, 12, 15][v % 5]
    answer = frac_str(Fraction(1, x))
    return q(
        "tw_one_day_work", v,
        f"{a} can finish a job in {x} days. What fraction of the job is done in one day?",
        answer, [frac_str(Fraction(1, x + 1)), frac_str(Fraction(1, x - 1)), frac_str(Fraction(1, 2 * x))],
        f"One day's work = 1/{x} of the whole job.",
        {"X": x, "Fraction": answer},
    )


def tw_combine_three(r, v):
    presets = [(6, 12, 12), (10, 15, 30), (8, 12, 24), (5, 10, 10), (12, 18, 36)]
    x, y, z = presets[v % len(presets)]
    rate = Fraction(1, x) + Fraction(1, y) + Fraction(1, z)
    answer = dec(1 / rate)
    first, second = pair(v + 1)
    third = pair(v + 2)[1]
    return q(
        "tw_combine_three", v,
        f"{first}, {second} and {third} can finish a task alone in {x}, {y} and "
        f"{z} days. How long do they take together?",
        answer, near_values(answer, r, 2),
        f"Combined rate = 1/{x} + 1/{y} + 1/{z} = {rate}; time = {answer} days.",
        {"X": x, "Y": y, "Z": z, "Days": answer},
    )


def tw_efficiency_ratio(r, v):
    a, b = pair(v + 2)
    presets = [(2, 1, 24), (3, 1, 30), (3, 2, 20), (4, 1, 28), (5, 2, 30)]
    ea, eb, bdays = presets[v % len(presets)]
    adays = Fraction(bdays * eb, ea)
    answer = dec(adays)
    return q(
        "tw_efficiency_ratio", v,
        f"{a} is {ea} times as efficient as {b}. If {b} alone takes {bdays} days, "
        f"how long does {a} take alone?",
        answer, near_values(answer, r, 2),
        f"Time is inversely proportional to efficiency: {bdays} x {eb}/{ea} = {answer} days.",
        {"Ea": ea, "Eb": eb, "BDays": bdays, "ADays": answer},
    )


def tw_leave_after(r, v):
    a, b = pair(v + 3)
    presets = [(12, 18, 6), (10, 15, 4), (20, 30, 5), (15, 10, 6), (24, 36, 8)]
    x, y, n = presets[v % len(presets)]
    total = Fraction(n) + (1 - Fraction(n, x)) * y
    answer = dec(total)
    return q(
        "tw_leave_after", v,
        f"{a} can complete a job in {x} days and {b} in {y} days. {a} works for "
        f"{n} days and leaves. How many days in total does the work take?",
        answer, near_values(answer, r, 2),
        f"Work done by {a} = {n}/{x}; remaining = {frac_str(1 - Fraction(n, x))}; "
        f"{b} needs {frac_str(1 - Fraction(n, x))} x {y} = {dec((1 - Fraction(n, x)) * y)} days; total = {answer}.",
        {"X": x, "Y": y, "N": n, "Total": answer},
    )


def tw_alternate_days(r, v):
    a, b = pair(v + 4)
    presets = [(6, 12), (10, 15), (8, 8), (12, 24), (5, 20)]
    x, y = presets[v % len(presets)]
    done = Fraction(0)
    day = 0
    while done < 1:
        day += 1
        done += Fraction(1, x) if day % 2 == 1 else Fraction(1, y)
    return q(
        "tw_alternate_days", v,
        f"{a} and {b} work on alternate days, {a} starting first. Alone they take "
        f"{x} and {y} days respectively. In how many days is the work completed?",
        day, near_ints(day, r, 3),
        f"Two-day cycle completes 1/{x} + 1/{y} = {frac_str(Fraction(1, x) + Fraction(1, y))}; "
        f"the work is finished on day {day}.",
        {"X": x, "Y": y, "Days": day},
    )


def tw_man_days(r, v):
    presets = [(12, 10, 15), (20, 12, 30), (15, 18, 27), (24, 15, 40), (10, 24, 16)]
    men, days, new_men = presets[v % len(presets)]
    answer = Fraction(men * days, new_men)
    assert answer.denominator == 1
    supervisor = pair(v + 2)[0]
    return q(
        "tw_man_days", v,
        f"Under {supervisor}, {men} workers complete a job in {days} days. "
        f"How many days will {new_men} workers take at the same rate?",
        answer.numerator, near_ints(answer.numerator, r, 4),
        f"Total work = {men} x {days} = {men * days} worker-days; time = {men * days}/{new_men} = {answer.numerator} days.",
        {"Men": men, "Days": days, "NewMen": new_men, "Answer": answer.numerator},
    )


def tw_men_women(r, v):
    presets = [(3, 5, 12, 6, 10), (4, 6, 10, 8, 9), (2, 3, 18, 4, 6),
               (5, 8, 20, 10, 16), (6, 9, 12, 12, 18)]
    m, w, days, men, women = presets[v % len(presets)]
    rate = Fraction(men, m * days) + Fraction(women, w * days)
    answer = dec(1 / rate)
    foreman, helper = pair(v + 3)
    return q(
        "tw_men_women", v,
        f"{foreman} notes that {m} men or {w} women can finish a task in {days} "
        f"days. How long will {men} men and {women} women working with {helper} "
        "take together?",
        answer, near_values(answer, r, 1),
        f"One man's rate = 1/({m}x{days}), one woman's = 1/({w}x{days}); combined rate = {rate}; time = {answer} days.",
        {"M": m, "W": w, "Days": days, "Men": men, "Women": women, "Answer": answer},
    )


def tw_partial_work(r, v):
    a, b = pair(v)
    presets = [(Fraction(1, 3), 4, 12), (Fraction(1, 4), 5, 20),
               (Fraction(2, 5), 6, 15), (Fraction(1, 2), 7, 14),
               (Fraction(3, 8), 9, 16)]
    frac, da, ydays = presets[v % len(presets)]
    answer = (1 - frac) * ydays
    text_answer = dec(answer)
    return q(
        "tw_partial_work", v,
        f"{a} completes {frac} of a task in {da} days and leaves. {b} alone takes "
        f"{ydays} days for the whole task. How long will {b} need to finish the rest?",
        text_answer, near_values(text_answer, r, 2),
        f"Remaining work = 1 - {frac} = {frac_str(1 - frac)}; time = {frac_str(1 - frac)} x {ydays} = {text_answer} days.",
        {"Frac": str(frac), "DA": da, "YDays": ydays, "Answer": text_answer},
    )


def tw_inverse_men(r, v):
    presets = [(8, 15, 12), (18, 20, 24), (14, 12, 21), (25, 16, 20), (9, 30, 15)]
    men, days, new_men = presets[v % len(presets)]
    answer = Fraction(men * days, new_men)
    assert answer.denominator == 1
    contractor = pair(v + 4)[0]
    return q(
        "tw_inverse_men", v,
        f"The contractor {contractor} estimates {days} days for {men} labourers. "
        f"If {new_men} labourers are deployed instead, how many days will the work take?",
        answer.numerator, near_ints(answer.numerator, r, 4),
        f"Work = {men} x {days} labourer-days; time = {men * days}/{new_men} = {answer.numerator} days.",
        {"Men": men, "Days": days, "NewMen": new_men, "Answer": answer.numerator},
    )


def tw_work_wages(r, v):
    a, b = pair(v + 1)
    presets = [(6, 12, 900), (10, 15, 1000), (8, 12, 1200), (5, 15, 800), (12, 18, 1500)]
    x, y, wage = presets[v % len(presets)]
    share = Fraction(wage * y, x + y)
    assert share.denominator == 1
    return q(
        "tw_work_wages", v,
        f"{a} takes {x} days and {b} takes {y} days to do a job. They work together "
        f"and earn Rs.{wage}. What is {a}'s share of the wages?",
        share.numerator, near_ints(share.numerator, r, 10),
        f"Wages are divided in the ratio of work done, {y}:{x}; {a}'s share = {wage} x {y}/({x}+{y}) = {share.numerator}.",
        {"X": x, "Y": y, "Wage": wage, "Share": share.numerator},
    )


def tw_pipes(r, v):
    presets = [(6, 3), (4, 6), (10, 15), (8, 12), (5, 20)]
    x, y = presets[v % len(presets)]
    answer = 1 / (Fraction(1, x) + Fraction(1, y))
    text = dec(answer)
    operator = pair(v + 5)[0]
    return q(
        "tw_pipes", v,
        f"For {operator}, two pipes can fill a tank in {x} hours and {y} hours "
        "separately. How long will they take together?",
        text, near_values(text, r, 1),
        f"Combined rate = 1/{x} + 1/{y}; time = {text} hours.",
        {"X": x, "Y": y, "Hours": text},
    )


def tw_leak(r, v):
    presets = [(10, 30), (12, 24), (8, 12), (6, 18), (15, 45)]
    x, y = presets[v % len(presets)]
    answer = 1 / (Fraction(1, x) - Fraction(1, y))
    text = dec(answer)
    operator = pair(v + 6)[0]
    return q(
        "tw_leak", v,
        f"In {operator}'s tank, a pipe fills it in {x} hours, but a leak empties "
        f"the full tank in {y} hours. With the leak open, how long does it take to "
        "fill the tank?",
        text, near_values(text, r, 2),
        f"Net rate = 1/{x} - 1/{y}; time = {text} hours.",
        {"X": x, "Y": y, "Hours": text},
    )


def tw_outlet(r, v):
    presets = [(10, 15, 30), (12, 18, 36), (8, 12, 24), (6, 12, 18), (20, 30, 60)]
    x, y, z = presets[v % len(presets)]
    rate = Fraction(1, x) + Fraction(1, y) - Fraction(1, z)
    answer = dec(1 / rate)
    operator = pair(v + 7)[0]
    return q(
        "tw_outlet", v,
        f"For {operator}, two inlet pipes fill a tank in {x} and {y} hours, while "
        f"an outlet empties it in {z} hours. With all three open, how long is the "
        "tank filled?",
        answer, near_values(answer, r, 1),
        f"Net rate = 1/{x} + 1/{y} - 1/{z} = {rate}; time = {answer} hours.",
        {"X": x, "Y": y, "Z": z, "Hours": answer},
    )


def tw_efficiency_percent(r, v):
    a, b = pair(v + 2)
    presets = [(25, 20), (50, 18), (20, 30), (60, 32), (100, 24)]
    percent, bdays = presets[v % len(presets)]
    adays = Fraction(bdays * 100, 100 + percent)
    answer = dec(adays)
    return q(
        "tw_efficiency_percent", v,
        f"{a} is {percent}% more efficient than {b}. If {b} takes {bdays} days "
        f"for a task, how long does {a} take?",
        answer, near_values(answer, r, 2),
        f"Efficiency ratio = {100 + percent}:100; time = {bdays} x 100/{100 + percent} = {answer} days.",
        {"Percent": percent, "BDays": bdays, "ADays": answer},
    )


def tw_half_work(r, v):
    a, _ = pair(v + 3)
    x = [4, 6, 8, 10, 12][v % 5]
    answer = 2 * x
    return q(
        "tw_half_work", v,
        f"{a} finishes half of a job in {x} days. How many days does the full job take?",
        answer, near_ints(answer, r, 4),
        f"Full work = 2 x {x} = {answer} days at the same rate.",
        {"X": x, "Answer": answer},
    )


def tw_time_fraction(r, v):
    a, _ = pair(v + 4)
    presets = [(12, 3), (15, 5), (20, 8), (18, 6), (24, 9)]
    x, n = presets[v % len(presets)]
    answer = frac_str(Fraction(n, x))
    return q(
        "tw_time_fraction", v,
        f"{a} can finish a task in {x} days. What fraction of the task is "
        f"completed in {n} days?",
        answer, [frac_str(Fraction(n + 1, x)), frac_str(Fraction(n, x + 1)), "1/2"],
        f"Fraction done = {n}/{x} = {answer}.",
        {"X": x, "N": n, "Fraction": answer},
    )


def tw_group_work(r, v):
    presets = [(10, 20, 5, 5), (12, 18, 6, 6), (15, 15, 5, 10), (8, 24, 6, 4), (20, 12, 3, 5)]
    men, days, worked, left = presets[v % len(presets)]
    answer = Fraction((days - worked) * men, men - left)
    assert answer.denominator == 1
    contractor = pair(v + 8)[0]
    return q(
        "tw_group_work", v,
        f"{contractor} allots {men} workers {days} days for a job. After {worked} "
        f"days {left} workers leave. How many more days will the remaining workers need?",
        answer.numerator, near_ints(answer.numerator, r, 5),
        f"Work left = ({days}-{worked}) x {men} worker-days; remaining workers = {men}-{left}; "
        f"days = {answer.numerator}.",
        {"Men": men, "Days": days, "Worked": worked, "Left": left, "Answer": answer.numerator},
    )


def tw_remaining_work(r, v):
    a, b = pair(v)
    presets = [(6, 10), (8, 12), (10, 15), (12, 20), (9, 12)]
    together, alone = presets[v % len(presets)]
    answer = Fraction(together * alone, alone - together)
    assert answer.denominator == 1
    return q(
        "tw_remaining_work", v,
        f"{a} and {b} together finish a task in {together} days. {a} alone takes "
        f"{alone} days. How long does {b} take alone?",
        answer.numerator, near_ints(answer.numerator, r, 5),
        f"{b}'s rate = 1/{together} - 1/{alone}; time = {together}x{alone}/({alone}-{together}) = {answer.numerator} days.",
        {"Together": together, "Alone": alone, "Answer": answer.numerator},
    )


def tw_combined_three(r, v):
    presets = [(6, 12, 12, 2), (10, 15, 30, 3), (8, 12, 24, 4), (5, 10, 10, 2), (12, 18, 36, 6)]
    x, y, z, n = presets[v % len(presets)]
    work = n * (Fraction(1, x) + Fraction(1, y) + Fraction(1, z))
    answer = frac_str(work)
    first, second = pair(v + 9)
    third = pair(v + 11)[1]
    return q(
        "tw_combined_three", v,
        f"{first}, {second} and {third}, who alone need {x}, {y} and {z} days, "
        f"work together for {n} days. What fraction of the task do they finish?",
        answer, [frac_str(Fraction(1) - work), frac_str(work / 2), "1/2"],
        f"Combined rate = 1/{x} + 1/{y} + 1/{z}; work in {n} days = {answer}.",
        {"X": x, "Y": y, "Z": z, "N": n, "Fraction": answer},
    )


def tw_alternate_group(r, v):
    a, b = pair(v + 1)
    presets = [(6, 12, 12), (10, 15, 30), (8, 8, 8), (12, 24, 24), (5, 10, 10)]
    x, y, z = presets[v % len(presets)]
    names = [x, y, z]
    done = Fraction(0)
    day = 0
    while done < 1:
        done += Fraction(1, names[day % 3])
        day += 1
    return q(
        "tw_alternate_group", v,
        f"{a}, {b} and a third worker take {x}, {y} and {z} days alone. They work "
        "one after another for one day each, starting with the first. In how many "
        "days is the work completed?",
        day, near_ints(day, r, 3),
        f"A three-day cycle completes 1/{x} + 1/{y} + 1/{z}; the work ends on day {day}.",
        {"X": x, "Y": y, "Z": z, "Days": day},
    )


def tw_wage_share(r, v):
    a, b = pair(v + 2)
    presets = [(10, 15, 5, 9, 1200), (6, 12, 3, 4, 900), (8, 12, 4, 6, 1200),
               (20, 30, 10, 15, 1500), (12, 18, 6, 9, 1800)]
    x, y, n1, n2, wage = presets[v % len(presets)]
    wa, wb = Fraction(n1, x), Fraction(n2, y)
    share = Fraction(wage * wa, wa + wb)
    answer = dec(share)
    return q(
        "tw_wage_share", v,
        f"{a} (who needs {x} days alone) works {n1} days and {b} (who needs {y} "
        f"days alone) works {n2} days on the same job. They receive Rs.{wage} in "
        f"total. What does {a} get?",
        answer, near_values(answer, r, 25),
        f"Work done is {frac_str(wa)} and {frac_str(wb)}; {a}'s wage = {wage} x {frac_str(wa)}/({frac_str(wa)}+{frac_str(wb)}) = {answer}.",
        {"X": x, "Y": y, "N1": n1, "N2": n2, "Wage": wage, "Share": answer},
    )


def tw_capacity_ratio(r, v):
    presets = [(2, 1, 6), (3, 2, 10), (1, 1, 8), (4, 1, 10), (3, 1, 9)]
    ra, rb, together = presets[v % len(presets)]
    answer = Fraction(together * (ra + rb), rb)
    assert answer.denominator == 1
    first, second = pair(v + 11)
    return q(
        "tw_capacity_ratio", v,
        f"{first} and {second} have efficiencies in the ratio {ra}:{rb}. Together "
        f"they complete a job in {together} days. How many days does the slower "
        "worker need alone?",
        answer.numerator, near_ints(answer.numerator, r, 5),
        f"Combined efficiency = {ra}+{rb}; slower worker's time = {together} x {ra+rb}/{rb} = {answer.numerator} days.",
        {"RA": ra, "RB": rb, "Together": together, "Answer": answer.numerator},
    )


def tw_compare(r, v):
    a, b = pair(v + 3)
    presets = [(6, 9), (12, 8), (15, 15), (10, 14), (20, 18)]
    x, y = presets[v % len(presets)]
    answer = a if x < y else b if y < x else "Both are equal"
    options = [a, b, "Both are equal", "Cannot be determined"]
    return {
        "text": (
            f"{a} completes a task in {x} days and {b} in {y} days. Who works faster?"
        ),
        "correct": answer,
        "distractors": [o for o in options if o != answer],
        "explanation": f"Smaller time means faster work; comparing {x} and {y} gives {answer}.",
        "verification_data": {
            "family": "tw_compare", "variant": v,
            "inputs": {"X": x, "Y": y, "Answer": answer},
        },
    }


FAMILIES = [
    tw_basic_days, tw_one_day_work, tw_combine_three, tw_efficiency_ratio,
    tw_leave_after, tw_alternate_days, tw_man_days, tw_men_women,
    tw_partial_work, tw_inverse_men, tw_work_wages, tw_pipes, tw_leak,
    tw_outlet, tw_efficiency_percent, tw_half_work, tw_time_fraction,
    tw_group_work, tw_remaining_work, tw_combined_three, tw_alternate_group,
    tw_wage_share, tw_capacity_ratio, tw_compare,
]


def build_time_and_work():
    spec = []
    for index, fn in enumerate(FAMILIES):
        part = 1 if index < 3 else 2 if index < 7 else 3 if index < 13 else 4
        difficulty = "EASY" if index < 7 else "MEDIUM" if index < 19 else "HARD"
        for variant in range(5):
            spec.append((part, difficulty, lambda r, f=fn, v=variant: f(r, v), (index % 4) + 1))
    return spec
