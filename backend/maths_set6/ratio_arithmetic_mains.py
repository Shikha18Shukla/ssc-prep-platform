# -*- coding: utf-8 -*-
"""Ratio Arithmetic (Mains) — 120 independently recomputed questions."""

from __future__ import annotations

from fractions import Fraction

from .bank import fmt
from .common import F, build_specs, money, near_num, near_pct, pct, q, ratio

SOURCE = "Ratio Arithmetic Mains class notes (local PDF)"
PAGES = {
    1: "c37283ae-286f-402f-90c5-fdba5737fd43.pdf, pp. 4-5",
    2: "c37283ae-286f-402f-90c5-fdba5737fd43.pdf, pp. 6-8",
    3: "c37283ae-286f-402f-90c5-fdba5737fd43.pdf, pp. 9-10",
    4: "c37283ae-286f-402f-90c5-fdba5737fd43.pdf, pp. 4-10",
}


def ratio_options(answer: str):
    first, second = answer.split(":")
    return [f"{second}:{first}", f"{int(first) + 1}:{second}", f"{first}:{int(second) + 1}"]


def ra_sum_adjust(r, v):
    a, b, total = ((3, 5, 160), (4, 7, 220), (5, 8, 260), (7, 9, 320), (8, 11, 380))[v]
    diff = F(total * (a - b), a + b)
    return q(
        "ra_sum_adjust", v,
        f"Two numbers are in the ratio {a}:{b} and their sum is {total}. Find the "
        f"difference between the larger and smaller number.",
        fmt(abs(diff)), near_num(abs(diff), 5),
        f"One part = {total}/{a + b} = {F(total, a + b)}; difference = "
        f"{abs(a - b)} parts = {fmt(abs(diff))}.",
        {"a": a, "b": b, "total": total},
    )


def ra_continuing(r, v):
    a, b, c, d, added = (
        (2, 3, 3, 4, 10), (3, 5, 4, 5, 15), (4, 7, 5, 7, 20),
        (5, 8, 6, 8, 25), (7, 9, 8, 10, 30),
    )[v]
    t = F(added * (c - d), a * d - b * c)
    first = a * t
    return q(
        "ra_continuing", v,
        f"Two numbers are in the ratio {a}:{b}. When {added} is added to each, "
        f"the ratio becomes {c}:{d}. Find the first number.",
        fmt(first), near_num(first, 5),
        f"Let the numbers be {a}t and {b}t. Then ({a}t+{added})/({b}t+{added}) = "
        f"{c}/{d}, giving t = {fmt(t)} and first number = {fmt(first)}.",
        {"a": a, "b": b, "c": c, "d": d, "added": added},
    )


def ra_income_savings(r, v):
    total_income, ia, ib, total_exp, ea, eb = (
        (120000, 3, 5, 80000, 2, 3), (180000, 4, 5, 120000, 3, 4),
        (240000, 5, 7, 160000, 4, 5), (300000, 7, 8, 210000, 5, 6),
        (360000, 2, 3, 240000, 3, 5),
    )[v]
    income_b = F(total_income * ib, ia + ib)
    exp_b = F(total_exp * eb, ea + eb)
    saving_b = income_b - exp_b
    return q(
        "ra_income_savings", v,
        f"Total incomes of A and B are in the ratio {ia}:{ib} and total ₹{total_income}. "
        f"Their expenditures are in the ratio {ea}:{eb} and total ₹{total_exp}. "
        f"Find B's savings.",
        money(saving_b), near_num(saving_b, 1000),
        f"B's income = ₹{fmt(income_b)}; B's expenditure = ₹{fmt(exp_b)}; "
        f"savings = ₹{fmt(saving_b)}.",
        {"total_income": total_income, "ia": ia, "ib": ib,
         "total_exp": total_exp, "ea": ea, "eb": eb},
    )


def ra_ages(r, v):
    a, b, years, c, d = (
        (3, 4, 5, 4, 5), (4, 7, 6, 5, 7), (5, 8, 10, 7, 10),
        (7, 9, 8, 8, 9), (8, 11, 12, 10, 12),
    )[v]
    t = F(years * (c - d), a * d - b * c)
    age = a * t
    return q(
        "ra_ages", v,
        f"Present ages are in the ratio {a}:{b}. After {years} years the ratio "
        f"will be {c}:{d}. Find the present age of the first person.",
        fmt(age), near_num(age, 2),
        f"Let ages be {a}t and {b}t. Solving ({a}t+{years})/({b}t+{years}) = "
        f"{c}/{d} gives t = {fmt(t)}, so the age is {fmt(age)}.",
        {"a": a, "b": b, "years": years, "c": c, "d": d},
    )


def ra_coins(r, v):
    d1, d2, a, b, value = (
        (1, 2, 3, 4, 110), (2, 5, 2, 3, 190), (5, 10, 4, 5, 600),
        (10, 20, 3, 7, 1700), (5, 20, 5, 2, 900),
    )[v]
    t = F(value, a * d1 + b * d2)
    count = a * t
    return q(
        "ra_coins", v,
        f"Coins of ₹{d1} and ₹{d2} are in the ratio {a}:{b}. Their total value "
        f"is ₹{value}. How many ₹{d1} coins are there?",
        fmt(count), near_num(count, 5),
        f"Value per ratio unit = {a}x{d1} + {b}x{d2} = {a * d1 + b * d2}; "
        f"t = {value}/{a * d1 + b * d2} = {fmt(t)}; count = {fmt(count)}.",
        {"d1": d1, "d2": d2, "a": a, "b": b, "value": value},
    )


def ra_mixture_replacement(r, v):
    a, b, total, removed = (
        (3, 2, 100, 20), (4, 3, 140, 28), (5, 3, 160, 32),
        (7, 5, 240, 48), (2, 3, 150, 30),
    )[v]
    first_left = F(a * (total - removed), a + b)
    return q(
        "ra_mixture_replacement", v,
        f"A mixture has milk:water = {a}:{b} and volume {total} L. {removed} L is "
        f"drawn off and replaced with water. How much milk remains?",
        fmt(first_left), near_num(first_left, 5),
        f"Initial milk = {a}/{a + b} x {total}; after removing {removed} L of "
        f"mixture, milk = initial x {(total - removed)}/{total} = {fmt(first_left)} L.",
        {"a": a, "b": b, "total": total, "removed": removed},
    )


def ra_partnership(r, v):
    a, b, t1, t2, profit = (
        (2, 3, 6, 4, 60000), (3, 4, 5, 6, 78000), (4, 5, 8, 6, 88000),
        (5, 7, 6, 9, 117000), (7, 8, 4, 7, 126000),
    )[v]
    share_a = F(profit * a * t1, a * t1 + b * t2)
    return q(
        "ra_partnership", v,
        f"A and B invest in the ratio {a}:{b} for {t1} and {t2} months. The annual "
        f"profit is ₹{profit}. Find A's share.",
        money(share_a), near_num(share_a, 1000),
        f"Profit ratio = {a}x{t1}:{b}x{t2} = {a * t1}:{b * t2}; A's share = "
        f"₹{fmt(share_a)}.",
        {"a": a, "b": b, "t1": t1, "t2": t2, "profit": profit},
    )


def ra_alloy_target(r, v):
    c1, c2, target = ((20, 45, 30), (25, 55, 40), (30, 60, 45), (35, 65, 50), (40, 70, 55))[v]
    answer = ratio(c2 - target, target - c1)
    return q(
        "ra_alloy_target", v,
        f"Alloy A has {c1}% copper and alloy B has {c2}% copper. In what ratio "
        f"should they be mixed to obtain {target}% copper?",
        answer, ratio_options(answer),
        f"Alligation ratio = ({c2}-{target}):({target}-{c1}) = "
        f"{c2 - target}:{target - c1} = {answer}.",
        {"c1": c1, "c2": c2, "target": target},
    )


def ra_students_admission(r, v):
    a, b, total, boys, girls = (
        (3, 2, 100, 20, 10), (4, 3, 140, 16, 14), (5, 4, 180, 25, 15),
        (7, 5, 240, 28, 22), (8, 7, 300, 32, 28),
    )[v]
    initial_boys = F(a * total, a + b)
    initial_girls = F(b * total, a + b)
    answer = ratio(initial_boys + boys, initial_girls + girls)
    return q(
        "ra_students_admission", v,
        f"Boys:girls = {a}:{b} among {total} students. After {boys} boys and "
        f"{girls} girls join, find the new boys:girls ratio.",
        answer, ratio_options(answer),
        f"Initial boys = {fmt(initial_boys)}, girls = {fmt(initial_girls)}; "
        f"new ratio = {fmt(initial_boys + boys)}:{fmt(initial_girls + girls)} = {answer}.",
        {"a": a, "b": b, "total": total, "boys": boys, "girls": girls},
    )


def ra_transfer(r, v):
    a, b, total, moved = ((5, 3, 160, 20), (4, 5, 180, 30), (7, 5, 240, 40),
                          (3, 8, 220, 25), (9, 7, 320, 50))[v]
    first = F(a * total, a + b) - moved
    second = F(b * total, a + b) + moved
    answer = ratio(first, second)
    return q(
        "ra_transfer", v,
        f"P:Q = {a}:{b} and their total is {total}. If {moved} is transferred from "
        f"P to Q, find the new ratio P:Q.",
        answer, ratio_options(answer),
        f"P = {fmt(first)}, Q = {fmt(second)}; new ratio = {answer}.",
        {"a": a, "b": b, "total": total, "moved": moved},
    )


def ra_two_vessels(r, v):
    a, b, c, d, volume = (
        (2, 3, 3, 1, 40), (3, 2, 1, 4, 60), (4, 5, 2, 7, 90),
        (5, 3, 3, 5, 120), (7, 5, 4, 8, 180),
    )[v]
    first = F(a * volume, a + b) + F(c * volume, c + d)
    second = F(b * volume, a + b) + F(d * volume, c + d)
    answer = ratio(first, second)
    return q(
        "ra_two_vessels", v,
        f"Two vessels each of {volume} L have milk:water = {a}:{b} and {c}:{d}. "
        f"Both are emptied into one container. Find the milk:water ratio.",
        answer, ratio_options(answer),
        f"Milk = {fmt(first)} L, water = {fmt(second)} L; ratio = {answer}.",
        {"a": a, "b": b, "c": c, "d": d, "volume": volume},
    )


def ra_speed_time(r, v):
    a, b = ((2, 3), (3, 5), (4, 7), (5, 8), (7, 10))[v]
    answer = ratio(b, a)
    return q(
        "ra_speed_time", v,
        f"Two vehicles have speeds in the ratio {a}:{b}. For the same distance, "
        f"find the ratio of their times.",
        answer, ratio_options(answer),
        f"Time is inversely proportional to speed, so ratio = {b}:{a} = {answer}.",
        {"a": a, "b": b},
    )


def ra_efficiency(r, v):
    a, b, days = ((2, 3, 12), (3, 4, 14), (4, 5, 18), (5, 7, 21), (7, 8, 24))[v]
    alone = F(days * (a + b), a)
    return q(
        "ra_efficiency", v,
        f"A and B's efficiencies are in the ratio {a}:{b}. Together they finish "
        f"a work in {days} days. How many days does A alone take?",
        fmt(alone), near_num(alone, 1),
        f"A's share of work per day = {a}/{a + b}; A alone takes "
        f"{days} x {(a + b)}/{a} = {fmt(alone)} days.",
        {"a": a, "b": b, "days": days},
    )


def ra_denomination_value(r, v):
    d1, d2, a, b, value = ((10, 50, 4, 3, 1900), (20, 100, 5, 2, 2000),
                           (50, 200, 3, 4, 9500), (100, 500, 2, 5, 27000),
                           (500, 2000, 5, 3, 85000))[v]
    count = F(value * a, a * d1 + b * d2)
    return q(
        "ra_denomination_value", v,
        f"Notes of ₹{d1} and ₹{d2} are in the ratio {a}:{b}. Their total value is "
        f"₹{value}. How many ₹{d1} notes are there?",
        fmt(count), near_num(count, 5),
        f"Value per ratio unit = {a}x{d1} + {b}x{d2}; count = "
        f"{value}x{a}/({a * d1 + b * d2}) = {fmt(count)}.",
        {"d1": d1, "d2": d2, "a": a, "b": b, "value": value},
    )


def ra_profit_share_salary(r, v):
    profit, salary, a, b = (
        (180000, 30000, 2, 3), (240000, 40000, 3, 5), (300000, 50000, 4, 6),
        (360000, 60000, 5, 7), (420000, 75000, 7, 8),
    )[v]
    share = salary + F((profit - salary) * a, a + b)
    return q(
        "ra_profit_share_salary", v,
        f"A partnership profit is ₹{profit}. A first gets a salary of ₹{salary} "
        f"and the balance is shared in the ratio {a}:{b}. Find A's total receipt.",
        money(share), near_num(share, 2000),
        f"Balance = ₹{profit - salary}; A's share of balance = "
        f"₹{fmt(F((profit - salary) * a, a + b))}; total = ₹{fmt(share)}.",
        {"profit": profit, "salary": salary, "a": a, "b": b},
    )


def ra_lcm_hcf(r, v):
    a, b, hcf = ((3, 5, 12), (4, 7, 15), (5, 9, 20), (7, 11, 25), (8, 13, 30))[v]
    lcm = hcf * a * b
    return q(
        "ra_lcm_hcf", v,
        f"Two numbers are in the ratio {a}:{b} and their HCF is {hcf}. Find their LCM.",
        fmt(lcm), near_num(lcm, 100),
        f"Numbers are {a}x{hcf} and {b}x{hcf}; LCM = {hcf}x{a}x{b} = {lcm}.",
        {"a": a, "b": b, "hcf": hcf},
    )


def ra_unit_price(r, v):
    total, x, y, p, qty = ((4800, 10, 20, 2, 3), (7200, 15, 25, 3, 4),
                           (9600, 20, 30, 4, 5), (12000, 25, 40, 3, 7),
                           (15000, 30, 50, 5, 8))[v]
    unit = F(total * p, x * p + y * qty)
    return q(
        "ra_unit_price", v,
        f"{x} units of A and {y} units of B cost ₹{total} together. Their unit "
        f"price ratio is {p}:{qty}. Find the price per unit of A.",
        money(unit), near_num(unit, 5),
        f"Let prices be {p}t and {qty}t; t = {total}/({x}x{p} + {y}x{qty}) = "
        f"{fmt(F(total, x * p + y * qty))}; price of A = ₹{fmt(unit)}.",
        {"total": total, "x": x, "y": y, "p": p, "qty": qty},
    )


def ra_remove_quantity(r, v):
    a, b, total, removed = ((5, 4, 180, 36), (3, 7, 200, 40), (4, 6, 250, 50),
                            (7, 8, 300, 60), (2, 9, 220, 44))[v]
    left = F(a * (total - removed), a + b)
    return q(
        "ra_remove_quantity", v,
        f"A mixture in ratio {a}:{b} has volume {total} L. If {removed} L of the "
        f"mixture is removed, how much of the first component remains?",
        fmt(left), near_num(left, 5),
        f"First component initially = {a}/{a + b} x {total}; after removal = "
        f"initial x {(total - removed)}/{total} = {fmt(left)} L.",
        {"a": a, "b": b, "total": total, "removed": removed},
    )


def ra_three_part(r, v):
    a, b, c, total = ((2, 3, 5, 200), (3, 4, 7, 280), (4, 5, 9, 360),
                      (5, 7, 8, 400), (6, 11, 13, 600))[v]
    share = F(b * total, a + b + c)
    return q(
        "ra_three_part", v,
        f"Three quantities are in the ratio {a}:{b}:{c} with total {total}. "
        f"Find the second quantity.",
        fmt(share), near_num(share, 5),
        f"Second quantity = {b}x{total}/({a + b + c}) = {fmt(share)}.",
        {"a": a, "b": b, "c": c, "total": total},
    )


def ra_after_percentage(r, v):
    a, b, pa, pb = ((3, 4, 20, 25), (5, 7, 10, 30), (4, 9, 25, 15),
                    (7, 8, 20, 40), (2, 5, 50, 20))[v]
    answer = ratio(F(a * (100 + pa)), F(b * (100 + pb)))
    return q(
        "ra_after_percentage", v,
        f"A:B = {a}:{b}. A increases by {pa}% and B by {pb}%. Find the new ratio A:B.",
        answer, ratio_options(answer),
        f"New amounts are {a}x{(100 + pa)} and {b}x{(100 + pb)}; ratio = {answer}.",
        {"a": a, "b": b, "pa": pa, "pb": pb},
    )


def ra_distance(r, v):
    a, b, t1, t2 = ((40, 60, 3, 2), (30, 45, 4, 3), (50, 75, 5, 4),
                    (20, 35, 6, 5), (60, 90, 7, 6))[v]
    answer = ratio(a * t1, b * t2)
    return q(
        "ra_distance", v,
        f"Two vehicles travel at {a} km/h and {b} km/h for {t1} h and {t2} h. "
        f"Find the ratio of distances covered.",
        answer, ratio_options(answer),
        f"Distances = {a}x{t1} and {b}x{t2}; ratio = {answer}.",
        {"a": a, "b": b, "t1": t1, "t2": t2},
    )


def ra_wages(r, v):
    a, b, c, d, t1, t2 = ((2, 3, 100, 120, 5, 4), (3, 4, 120, 150, 6, 5),
                          (4, 5, 150, 180, 7, 6), (5, 7, 180, 200, 8, 7),
                          (6, 8, 200, 250, 9, 8))[v]
    answer = ratio(a * c * t1, b * d * t2)
    return q(
        "ra_wages", v,
        f"Worker groups A:B have counts {a}:{b}, daily wages ₹{c}:₹{d} and work "
        f"for {t1}:{t2} days. Find the ratio of their total wages.",
        answer, ratio_options(answer),
        f"Total wages ratio = {a}x{c}x{t1}:{b}x{d}x{t2} = {answer}.",
        {"a": a, "b": b, "c": c, "d": d, "t1": t1, "t2": t2},
    )


def ra_dilution(r, v):
    a, b, total, added = ((4, 1, 100, 20), (5, 2, 140, 28), (3, 2, 150, 30),
                          (7, 3, 200, 40), (8, 5, 260, 52))[v]
    milk = F(a * total, a + b)
    water = F(b * total, a + b) + added
    answer = ratio(milk, water)
    return q(
        "ra_dilution", v,
        f"Milk:water = {a}:{b} in {total} L. If {added} L of water is added, find "
        f"the new milk:water ratio.",
        answer, ratio_options(answer),
        f"Milk = {fmt(milk)} L; water = {fmt(water)} L; ratio = {answer}.",
        {"a": a, "b": b, "total": total, "added": added},
    )


def ra_inverse(r, v):
    a, b = ((6, 9), (8, 12), (10, 15), (12, 18), (15, 25))[v]
    answer = ratio(b, a)
    return q(
        "ra_inverse", v,
        f"A alone finishes a work in {a} days and B alone in {b} days. Find the "
        f"ratio of work done by A and B in the same time.",
        answer, ratio_options(answer),
        f"Work done is inversely proportional to time, so ratio = {b}:{a} = {answer}.",
        {"a": a, "b": b},
    )


FAMILIES = [
    ra_sum_adjust, ra_continuing, ra_income_savings, ra_ages, ra_coins,
    ra_mixture_replacement, ra_partnership, ra_alloy_target, ra_students_admission,
    ra_transfer, ra_two_vessels, ra_speed_time, ra_efficiency, ra_denomination_value,
    ra_profit_share_salary, ra_lcm_hcf, ra_unit_price, ra_remove_quantity,
    ra_three_part, ra_after_percentage, ra_distance, ra_wages, ra_dilution, ra_inverse,
]


def build_ratio_arithmetic_mains():
    specs = build_specs(FAMILIES)
    return [(part, "HARD", fn, page) for part, _difficulty, fn, page in specs]
