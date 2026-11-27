# -*- coding: utf-8 -*-
"""Percentage Arithmetic (Mains) — 120 independently recomputed questions."""

from __future__ import annotations

from fractions import Fraction

from .bank import fmt
from .common import (
    F, build_specs, dec, money, near_num, near_pct, pct, q, ratio,
)

SOURCE = "Percentage Arithmetic Mains class notes (local PDF)"
PAGES = {
    1: "ed99aa3d-eaea-44e4-b047-f1fdcba71c86.pdf, pp. 4-6",
    2: "ed99aa3d-eaea-44e4-b047-f1fdcba71c86.pdf, pp. 7-9",
    3: "ed99aa3d-eaea-44e4-b047-f1fdcba71c86.pdf, pp. 10-11",
    4: "ed99aa3d-eaea-44e4-b047-f1fdcba71c86.pdf, pp. 4-11",
}


def pa_successive_three(r, v):
    base, a, b, c = ((800, 10, 20, -15), (1200, 15, -10, 25), (1500, 20, 15, -20),
                     (2400, 25, -20, 10), (3600, 12, 18, -25))[v]
    final = F(base * (100 + a) * (100 + b) * (100 + c), 1000000)
    return q(
        "pa_successive_three", v,
        f"An investment of ₹{base} changes by {a}%, then {b}% and then {c}%. "
        f"What is its final value?",
        money(final), near_money(final, 100),
        f"Multiply successively: {base} x {(100 + a)}/100 x {(100 + b)}/100 x "
        f"{(100 + c)}/100 = {fmt(final)}.",
        {"base": base, "a": a, "b": b, "c": c},
    )


def near_money(value, step=100):
    value = F(value)
    return [money(value + step), money(value - step), money(value * 2)]


def pa_reverse_original(r, v):
    final, a, b = ((1540, 10, -20), (1728, 20, -10), (2025, 25, -20),
                   (1188, 10, -10), (2160, 20, -10))[v]
    original = F(final * 10000, (100 + a) * (100 + b))
    return q(
        "pa_reverse_original", v,
        f"A sum becomes ₹{final} after a {a}% increase followed by a {b}% change. "
        f"Find the original sum.",
        money(original), near_money(original, 100),
        f"Original = {final} x 10000 / ({(100 + a)} x {(100 + b)}) = {fmt(original)}.",
        {"final": final, "a": a, "b": b},
    )


def pa_population_net(r, v):
    pop, growth, migrants = ((12000, 15, 600), (18000, 12, 900), (24000, 8, -1200),
                             (30000, 10, 1500), (36000, 5, -900))[v]
    final = F(pop * (100 + growth), 100) + migrants
    return q(
        "pa_population_net", v,
        f"A town has {pop} residents. It grows by {growth}% and then gains "
        f"{migrants} net migrants. What is the new population?",
        fmt(final), near_num(final, 500),
        f"After growth: {pop} x {(100 + growth)}/100 = {fmt(F(pop * (100 + growth), 100))}; "
        f"then add {migrants} to get {fmt(final)}.",
        {"pop": pop, "growth": growth, "migrants": migrants},
    )


def pa_price_return(r, v):
    rise = (10, 20, 25, 50, 60)[v]
    fall = F(rise * 100, 100 + rise)
    return q(
        "pa_price_return", v,
        f"The price of an article rises by {rise}%. By what percent must it now "
        f"fall to return to the original price?",
        pct(fall), near_pct(fall, 5),
        f"Required fall = {rise}/{(100 + rise)} x 100 = {dec(fall)}%.",
        {"rise": rise},
    )


def pa_allocation_remaining(r, v):
    income, a, b, c = ((20000, 20, 25, 10), (30000, 15, 20, 25), (40000, 25, 10, 20),
                       (50000, 10, 30, 15), (60000, 20, 15, 30))[v]
    remaining = F(income * (100 - a) * (100 - b) * (100 - c), 1000000)
    return q(
        "pa_allocation_remaining", v,
        f"From a monthly income of ₹{income}, a person spends {a}% on rent, "
        f"{b}% of the remainder on food and {c}% of the new remainder on travel. "
        f"How much is left?",
        money(remaining), near_money(remaining, 500),
        f"Left = {income} x {(100 - a)}/100 x {(100 - b)}/100 x {(100 - c)}/100 "
        f"= {fmt(remaining)}.",
        {"income": income, "a": a, "b": b, "c": c},
    )


def pa_weighted_average(r, v):
    q1, c1, q2, c2 = ((20, 15, 30, 35), (30, 20, 50, 40), (40, 12, 60, 32),
                      (50, 18, 75, 30), (60, 25, 90, 45))[v]
    strength = F(q1 * c1 + q2 * c2, q1 + q2)
    return q(
        "pa_weighted_average", v,
        f"Two solutions of {q1} L at {c1}% strength and {q2} L at {c2}% strength "
        f"are mixed. Find the strength of the mixture.",
        pct(strength), near_pct(strength, 2),
        f"Strength = ({q1}x{c1} + {q2}x{c2})/{q1 + q2} = {dec(strength)}%.",
        {"q1": q1, "c1": c1, "q2": q2, "c2": c2},
    )


def pa_election_margin(r, v):
    total, invalid, winner = ((50000, 10, 55), (60000, 15, 60), (72000, 12, 58),
                              (84000, 20, 62), (96000, 25, 65))[v]
    valid = F(total * (100 - invalid), 100)
    margin = F(valid * (2 * winner - 100), 100)
    return q(
        "pa_election_margin", v,
        f"An election had {total} votes, of which {invalid}% were invalid. The "
        f"winner secured {winner}% of valid votes. Find the winning margin.",
        fmt(margin), near_num(margin, 1000),
        f"Valid votes = {fmt(valid)}; margin = {(2 * winner - 100)}% of valid votes "
        f"= {fmt(margin)}.",
        {"total": total, "invalid": invalid, "winner": winner},
    )


def pa_exam_pass(r, v):
    enrolled, absent, pass_pct = ((400, 10, 75), (500, 12, 80), (600, 15, 70),
                                  (800, 20, 85), (1000, 25, 72))[v]
    passed = F(enrolled * (100 - absent) * pass_pct, 10000)
    return q(
        "pa_exam_pass", v,
        f"Of {enrolled} students, {absent}% were absent. Of those who appeared, "
        f"{pass_pct}% passed. How many students passed?",
        fmt(passed), near_num(passed, 25),
        f"Appeared = {enrolled} x {(100 - absent)}/100; passed = appeared x "
        f"{pass_pct}/100 = {fmt(passed)}.",
        {"enrolled": enrolled, "absent": absent, "pass_pct": pass_pct},
    )


def pa_depreciation(r, v):
    value, d1, d2 = ((200000, 10, 15), (250000, 12, 20), (320000, 15, 10),
                     (400000, 20, 25), (500000, 8, 12))[v]
    final = F(value * (100 - d1) * (100 - d2), 10000)
    return q(
        "pa_depreciation", v,
        f"An asset worth ₹{value} depreciates by {d1}% in the first year and "
        f"{d2}% in the second year. Find its value after two years.",
        money(final), near_money(final, 5000),
        f"Value = {value} x {(100 - d1)}/100 x {(100 - d2)}/100 = {fmt(final)}.",
        {"value": value, "d1": d1, "d2": d2},
    )


def pa_tax_slab(r, v):
    income, free, rate, cess = ((800000, 300000, 10, 4), (1000000, 400000, 15, 3),
                                (1200000, 500000, 20, 2), (1500000, 600000, 20, 4),
                                (1800000, 700000, 25, 3))[v]
    tax = F((income - free) * rate, 100)
    total = F(tax * (100 + cess), 100)
    return q(
        "pa_tax_slab", v,
        f"Income is ₹{income}. The first ₹{free} is exempt, the balance is taxed "
        f"at {rate}% and a {cess}% cess is charged on the tax. Find the total tax.",
        money(total), near_money(total, 5000),
        f"Taxable = {income} - {free} = {income - free}; base tax = "
        f"{fmt(tax)}; with cess = {fmt(total)}.",
        {"income": income, "free": free, "rate": rate, "cess": cess},
    )


def pa_percentage_point(r, v):
    old_total, old_share, new_total, new_share = (
        (20000, 30, 30000, 25), (24000, 40, 36000, 35), (30000, 25, 45000, 30),
        (36000, 45, 48000, 40), (40000, 20, 60000, 25),
    )[v]
    old_part = F(old_total * old_share, 100)
    new_part = F(new_total * new_share, 100)
    change = new_part - old_part
    return q(
        "pa_percentage_point", v,
        f"A category was {old_share}% of {old_total} and later {new_share}% of "
        f"{new_total}. By how many units did its absolute value change?",
        fmt(change), near_num(change, 500),
        f"Old part = {fmt(old_part)}; new part = {fmt(new_part)}; change = "
        f"{fmt(change)}.",
        {"old_total": old_total, "old_share": old_share,
         "new_total": new_total, "new_share": new_share},
    )


def pa_ratio_from_percent(r, v):
    x, y = ((20, 50), (25, 40), (30, 60), (40, 25), (50, 20))[v]
    answer = ratio(F(x * y, 10000), 1)
    return q(
        "pa_ratio_from_percent", v,
        f"A is {x}% of B and B is {y}% of C. Find A:C in simplest form.",
        answer, [f"{x}:{y}", f"{100}:{y}", f"{100}:{x}"],
        f"A/C = {x}/100 x {y}/100 = {x * y}/10000 = {answer} after simplification.",
        {"x": x, "y": y},
    )


def pa_expenditure_change(r, v):
    price, consumption = ((20, 10), (25, 20), (10, 5), (30, 25), (40, 20))[v]
    change = F((100 + price) * (100 - consumption), 100) - 100
    return q(
        "pa_expenditure_change", v,
        f"The price of a commodity rises {price}% and its consumption falls "
        f"{consumption}%. What is the percentage change in expenditure?",
        pct(change), near_pct(change, 2),
        f"Expenditure factor = {(100 + price)}/100 x {(100 - consumption)}/100; "
        f"change = {dec(change)}%.",
        {"price": price, "consumption": consumption},
    )


def pa_overlap_pass(r, v):
    total, math_pct, eng_pct, both_pct = (
        (200, 70, 60, 40), (300, 65, 55, 30), (400, 75, 60, 45),
        (500, 80, 70, 55), (600, 72, 68, 40),
    )[v]
    at_least = F(total * (math_pct + eng_pct - both_pct), 100)
    return q(
        "pa_overlap_pass", v,
        f"In an exam of {total} students, {math_pct}% passed Maths, {eng_pct}% "
        f"passed English and {both_pct}% passed both. How many passed at least one?",
        fmt(at_least), near_num(at_least, 20),
        f"Inclusion-exclusion: {math_pct} + {eng_pct} - {both_pct} = "
        f"{math_pct + eng_pct - both_pct}% of {total} = {fmt(at_least)}.",
        {"total": total, "math_pct": math_pct, "eng_pct": eng_pct, "both_pct": both_pct},
    )


def pa_gender_literacy(r, v):
    pop, male_pct, male_lit, female_lit = (
        (20000, 55, 80, 60), (30000, 60, 75, 65), (40000, 52, 85, 70),
        (50000, 58, 78, 62), (60000, 62, 82, 68),
    )[v]
    literate = F(pop * (male_pct * male_lit + (100 - male_pct) * female_lit), 10000)
    return q(
        "pa_gender_literacy", v,
        f"A population is {pop}. Men are {male_pct}% of it, with {male_lit}% "
        f"literacy; female literacy is {female_lit}%. Find the literate population.",
        fmt(literate), near_num(literate, 500),
        f"Literate = {pop} x ({male_pct}x{male_lit} + "
        f"{100 - male_pct}x{female_lit})/10000 = {fmt(literate)}.",
        {"pop": pop, "male_pct": male_pct, "male_lit": male_lit, "female_lit": female_lit},
    )


def pa_investment_split(r, v):
    total, x, y, r1, r2 = ((120000, 2, 3, 8, 12), (180000, 3, 5, 6, 10),
                           (240000, 4, 5, 9, 15), (300000, 5, 7, 7, 11),
                           (360000, 3, 7, 8, 13))[v]
    interest = F(total * x * r1, (x + y) * 100) + F(total * y * r2, (x + y) * 100)
    return q(
        "pa_investment_split", v,
        f"₹{total} is split in the ratio {x}:{y}. The parts earn {r1}% and {r2}% "
        f"simple interest respectively. Find the total annual interest.",
        money(interest), near_money(interest, 1000),
        f"First part = ₹{fmt(F(total * x, x + y))}, second = "
        f"₹{fmt(F(total * y, x + y))}; interest = {fmt(interest)}.",
        {"total": total, "x": x, "y": y, "r1": r1, "r2": r2},
    )


def pa_discount_tax(r, v):
    mp, discount, tax = ((25000, 20, 8), (32000, 25, 5), (40000, 15, 12),
                         (48000, 30, 6), (60000, 20, 10))[v]
    net = F(mp * (100 - discount) * (100 + tax), 10000)
    return q(
        "pa_discount_tax", v,
        f"An article has marked price ₹{mp}. A {discount}% discount is given and "
        f"then {tax}% tax is added. What does the customer pay?",
        money(net), near_money(net, 1000),
        f"Net = {mp} x {(100 - discount)}/100 x {(100 + tax)}/100 = {fmt(net)}.",
        {"mp": mp, "discount": discount, "tax": tax},
    )


def pa_evaporation(r, v):
    total, solute_pct, evaporated = ((100, 20, 20), (150, 25, 30), (200, 15, 40),
                                     (250, 30, 50), (300, 24, 60))[v]
    solute = F(total * solute_pct, 100)
    strength = F(solute * 100, total - evaporated)
    return q(
        "pa_evaporation", v,
        f"{total} L of a {solute_pct}% solution has {evaporated} L of water "
        f"evaporated. Find the new concentration.",
        pct(strength), near_pct(strength, 2),
        f"Solute = {fmt(solute)} L; final volume = {total - evaporated} L; "
        f"strength = {dec(strength)}%.",
        {"total": total, "solute_pct": solute_pct, "evaporated": evaporated},
    )


def pa_alloy_mix(r, v):
    q1, c1, q2, c2 = ((18, 30, 12, 60), (24, 25, 16, 50), (30, 40, 20, 65),
                      (36, 35, 24, 55), (42, 45, 28, 70))[v]
    copper = F(q1 * c1 + q2 * c2, q1 + q2)
    return q(
        "pa_alloy_mix", v,
        f"Two alloys contain {c1}% and {c2}% copper. Quantities of {q1} kg and "
        f"{q2} kg are melted together. Find the copper percentage in the new alloy.",
        pct(copper), near_pct(copper, 2),
        f"Copper = ({q1}x{c1} + {q2}x{c2})/{q1 + q2} = {dec(copper)}%.",
        {"q1": q1, "c1": c1, "q2": q2, "c2": c2},
    )


def pa_time_allocation(r, v):
    hours, sleep, study, work = ((24, 25, 20, 30), (24, 30, 25, 20), (24, 20, 30, 25),
                                 (30, 25, 20, 40), (36, 30, 25, 30))[v]
    left = F(hours * (100 - sleep) * (100 - study) * (100 - work), 1000000)
    return q(
        "pa_time_allocation", v,
        f"Of {hours} hours, {sleep}% is spent sleeping, {study}% of the remainder "
        f"studying and {work}% of the next remainder working. How many hours remain?",
        fmt(left), near_num(left, 1),
        f"Remaining = {hours} x {(100 - sleep)}/100 x {(100 - study)}/100 x "
        f"{(100 - work)}/100 = {fmt(left)} hours.",
        {"hours": hours, "sleep": sleep, "study": study, "work": work},
    )


def pa_claim_settlement(r, v):
    claims, settled, reopened = ((10000, 60, 25), (12000, 65, 20), (15000, 70, 30),
                                 (18000, 75, 40), (20000, 80, 25))[v]
    pending = F(claims * (100 - settled) * (100 - reopened), 10000)
    return q(
        "pa_claim_settlement", v,
        f"An insurer received {claims} claims. {settled}% were settled and "
        f"{reopened}% of the unsettled ones were reopened. How many remain pending?",
        fmt(pending), near_num(pending, 50),
        f"Unsettled = {claims} x {(100 - settled)}/100; after reopening, pending = "
        f"{fmt(pending)}.",
        {"claims": claims, "settled": settled, "reopened": reopened},
    )


def pa_consecutive_discount(r, v):
    d1, d2 = ((10, 20), (15, 25), (20, 30), (25, 40), (30, 35))[v]
    single = F(d1 + d2) - F(d1 * d2, 100)
    return q(
        "pa_consecutive_discount", v,
        f"Find the single discount equivalent to successive discounts of {d1}% "
        f"and {d2}%.",
        pct(single), near_pct(single, 2),
        f"Equivalent discount = {d1} + {d2} - ({d1}x{d2})/100 = {dec(single)}%.",
        {"d1": d1, "d2": d2},
    )


def pa_area_change(r, v):
    length, breadth, a, b = ((20, 10, 20, -10), (30, 20, 15, 20), (40, 25, 25, -20),
                             (50, 30, 10, 10), (60, 40, 30, -25))[v]
    change = F((100 + a) * (100 + b), 100) - 100
    return q(
        "pa_area_change", v,
        f"A rectangle has length {length} cm and breadth {breadth} cm. Length "
        f"changes by {a}% and breadth by {b}%. Find the percentage change in area.",
        pct(change), near_pct(change, 2),
        f"Area factor = {(100 + a)}/100 x {(100 + b)}/100; change = {dec(change)}%.",
        {"length": length, "breadth": breadth, "a": a, "b": b},
    )


def pa_two_year_growth(r, v):
    pop, a, b = ((10000, 10, 20), (15000, 12, 15), (20000, 20, 25),
                 (25000, 8, 12), (30000, 15, 10))[v]
    final = F(pop * (100 + a) * (100 + b), 10000)
    return q(
        "pa_two_year_growth", v,
        f"A city's population grows {a}% in year one and {b}% in year two from "
        f"a base of {pop}. Find the population after two years.",
        fmt(final), near_num(final, 500),
        f"Population = {pop} x {(100 + a)}/100 x {(100 + b)}/100 = {fmt(final)}.",
        {"pop": pop, "a": a, "b": b},
    )


FAMILIES = [
    pa_successive_three, pa_reverse_original, pa_population_net, pa_price_return,
    pa_allocation_remaining, pa_weighted_average, pa_election_margin, pa_exam_pass,
    pa_depreciation, pa_tax_slab, pa_percentage_point, pa_ratio_from_percent,
    pa_expenditure_change, pa_overlap_pass, pa_gender_literacy, pa_investment_split,
    pa_discount_tax, pa_evaporation, pa_alloy_mix, pa_time_allocation,
    pa_claim_settlement, pa_consecutive_discount, pa_area_change, pa_two_year_growth,
]


def build_percentage_arithmetic_mains():
    specs = build_specs(FAMILIES)
    return [(part, "HARD", fn, page) for part, _difficulty, fn, page in specs]
