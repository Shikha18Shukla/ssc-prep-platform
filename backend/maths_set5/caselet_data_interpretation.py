# -*- coding: utf-8 -*-
"""Caselet Data Interpretation — 120 verified questions for the fifth Maths batch."""

from __future__ import annotations

from fractions import Fraction

from .bank import fmt, fmt_dec
from .common import build_specs, pair, q, third

SOURCE = "Caselet Data Interpretation class notes (local PDFs)"
PAGES = {
    1: "e1183040-db37-4bf1-a5c1-ebac16ca3f1f.pdf, pp. 3-17",
    2: "e1183040-db37-4bf1-a5c1-ebac16ca3f1f.pdf, pp. 18-57",
}


def F(a, b=1):
    return Fraction(a, b)


def near(value, step=1):
    return [fmt(value + step), fmt(value - step), fmt(value * 2)]


def near_pct(value):
    return [fmt_dec(float(value) + 5) + "%", fmt_dec(float(value) - 5) + "%", fmt_dec(float(value) / 2) + "%"]


def cd_total(r, v):
    data = ((120, 180, 240), (150, 210, 270), (180, 240, 300), (210, 280, 350), (250, 320, 400))[v]
    who, friend = pair(v)
    helper = third(v, 3)
    total = sum(data)
    return q(
        "cd_total", v,
        f"A bank branch served {data[0]} savings, {data[1]} current and {data[2]} "
        f"fixed accounts in a month. {who}, {friend} and {helper} need the total "
        f"accounts. Find it.",
        fmt(total),
        near(F(total)),
        f"Total = {data[0]} + {data[1]} + {data[2]} = {total}.",
        {"a": data[0], "b": data[1], "c": data[2]},
    )


def cd_difference(r, v):
    data = ((360, 240), (420, 280), (480, 320), (540, 360), (600, 400))[v]
    who, friend = pair(v, 1)
    helper = third(v, 4)
    diff = data[0] - data[1]
    return q(
        "cd_difference", v,
        f"A shop's first-week sales were ₹{data[0]} thousand and second-week "
        f"sales were ₹{data[1]} thousand. {who}, {friend} and {helper} need the "
        f"excess of first week over second. Find it.",
        fmt(diff),
        near(F(diff)),
        f"Difference = {data[0]} - {data[1]} = {diff}.",
        {"a": data[0], "b": data[1]},
    )


def cd_ratio(r, v):
    data = ((24, 36), (30, 45), (36, 54), (42, 63), (48, 72))[v]
    from math import gcd
    g = gcd(*data)
    who, friend = pair(v, 2)
    helper = third(v, 5)
    return q(
        "cd_ratio", v,
        f"A production line made {data[0]} red and {data[1]} blue units. {who}, "
        f"{friend} and {helper} need the red:blue ratio in lowest terms. Find it.",
        f"{data[0] // g}:{data[1] // g}",
        [f"{data[1] // g}:{data[0] // g}", f"{data[0]}:{data[1]}", f"{data[0] // g + 1}:{data[1] // g}"],
        f"Divide both quantities by {g}: {data[0] // g}:{data[1] // g}.",
        {"a": data[0], "b": data[1]},
    )


def cd_pct_of_total(r, v):
    data = ((30, 120), (42, 168), (54, 216), (66, 264), (75, 300))[v]
    part, total = data
    who, friend = pair(v, 3)
    helper = third(v, 6)
    pct = F(part * 100, total)
    answer = fmt_dec(float(pct)) + "%"
    return q(
        "cd_pct_of_total", v,
        f"A caselet states that {part} of {total} applicants were shortlisted. "
        f"{who}, {friend} and {helper} need the shortlisted percentage. Find it.",
        answer,
        near_pct(pct),
        f"Percentage = {part}/{total} x 100 = {answer}.",
        {"a": part, "t": total},
    )


def cd_missing_value(r, v):
    data = ((45, 55, 150), (60, 70, 190), (75, 85, 240), (90, 100, 290), (110, 120, 350))[v]
    a, b, total = data
    missing = total - a - b
    who, friend = pair(v, 4)
    helper = third(v, 7)
    return q(
        "cd_missing_value", v,
        f"A three-part caselet has parts {a}, {b} and an unknown third part; the "
        f"total is {total}. {who}, {friend} and {helper} need the missing part. "
        f"Find it.",
        fmt(missing),
        near(F(missing)),
        f"Missing part = {total} - ({a} + {b}) = {missing}.",
        {"a": a, "b": b, "t": total},
    )


def cd_average(r, v):
    data = ((40, 50, 60), (55, 65, 75), (70, 80, 90), (85, 95, 105), (100, 110, 130))[v]
    who, friend = pair(v, 5)
    helper = third(v, 8)
    avg = F(sum(data), 3)
    return q(
        "cd_average", v,
        f"A firm's three quarterly profits were ₹{data[0]}, ₹{data[1]} and "
        f"₹{data[2]} lakh. {who}, {friend} and {helper} need the average quarterly "
        f"profit. Find it.",
        fmt(avg),
        near(avg),
        f"Average = ({sum(data)})/3 = {fmt(avg)}.",
        {"v": list(data)},
    )


def cd_percentage_change(r, v):
    data = ((80, 100), (100, 125), (120, 150), (160, 200), (200, 240))[v]
    old, new = data
    who, friend = pair(v, 6)
    helper = third(v, 9)
    pct = F(new - old, old) * 100
    answer = fmt_dec(float(pct)) + "%"
    return q(
        "cd_percentage_change", v,
        f"A village's annual income rose from ₹{old} thousand to ₹{new} thousand. "
        f"{who}, {friend} and {helper} need the percentage increase. Find it.",
        answer,
        near_pct(pct),
        f"Increase = {new - old}; percentage = ({new - old}/{old}) x 100 = {answer}.",
        {"a": old, "b": new},
    )


def cd_successive_change(r, v):
    data = ((100, 10, 20), (200, 10, 15), (300, 20, 10), (400, 25, 20), (500, 20, 25))[v]
    start, p1, p2 = data
    who, friend = pair(v, 7)
    helper = third(v, 10)
    final = F(start * (100 + p1) * (100 - p2), 10000)
    return q(
        "cd_successive_change", v,
        f"A stock index starts at {start}, rises {p1}% and then falls {p2}%. "
        f"{who}, {friend} and {helper} need the final index value. Find it.",
        fmt(final),
        near(final, 5),
        f"Final = {start} x (1 + {p1}/100) x (1 - {p2}/100) = {fmt(final)}.",
        {"s": start, "p": p1, "q": p2},
    )


def cd_weighted_avg(r, v):
    data = ((18, 62, 32, 84), (24, 68, 36, 88), (28, 74, 42, 92), (36, 82, 54, 96), (45, 86, 65, 94))[v]
    n1, a1, n2, a2 = data
    who, friend = pair(v, 8)
    helper = third(v, 11)
    avg = F(n1 * a1 + n2 * a2, n1 + n2)
    return q(
        "cd_weighted_avg", v,
        f"A caselet says {n1} workers earn ₹{a1} a day and {n2} workers earn "
        f"₹{a2} a day. {who}, {friend} and {helper} need the average daily wage. "
        f"Find it.",
        fmt(avg),
        near(avg),
        f"Average = ({n1}x{a1} + {n2}x{a2})/({n1} + {n2}) = {fmt(avg)}.",
        {"n1": n1, "a1": a1, "n2": n2, "a2": a2},
    )


def cd_ratio_split(r, v):
    data = ((240, 2, 3), (300, 3, 2), (360, 4, 5), (420, 5, 7), (480, 3, 5))[v]
    total, a, b = data
    who, friend = pair(v, 9)
    helper = third(v, 12)
    first = F(total * a, a + b)
    return q(
        "cd_ratio_split", v,
        f"A sum of ₹{total} lakh is split between two departments in the ratio "
        f"{a}:{b}. {who}, {friend} and {helper} need the first department's share. "
        f"Find it.",
        fmt(first),
        near(first, 5),
        f"First share = {total} x {a}/({a} + {b}) = {fmt(first)}.",
        {"t": total, "a": a, "b": b},
    )


def cd_ratio_difference(r, v):
    data = ((240, 2, 3), (300, 3, 2), (360, 4, 5), (420, 5, 7), (480, 3, 5))[v]
    total, a, b = data
    who, friend = pair(v, 10)
    helper = third(v, 13)
    diff = F(total * abs(a - b), a + b)
    return q(
        "cd_ratio_difference", v,
        f"A sum of ₹{total} lakh is divided in the ratio {a}:{b}. {who}, {friend} "
        f"and {helper} need the difference between the two shares. Find it.",
        fmt(diff),
        near(diff, 5),
        f"Difference = {total} x |{a} - {b}|/({a} + {b}) = {fmt(diff)}.",
        {"t": total, "a": a, "b": b},
    )


def cd_fraction_remaining(r, v):
    data = ((360, 3, 8), (420, 2, 7), (480, 5, 12), (540, 4, 9), (600, 3, 10))[v]
    total, numerator, denominator = data
    who, friend = pair(v, 11)
    helper = third(v, 14)
    remaining = F(total * (denominator - numerator), denominator)
    return q(
        "cd_fraction_remaining", v,
        f"A warehouse had {total} sacks and {numerator}/{denominator} of them were "
        f"shipped. {who}, {friend} and {helper} need the number remaining. Find it.",
        fmt(remaining),
        near(remaining, 5),
        f"Remaining fraction = ({denominator} - {numerator})/{denominator}; number = "
        f"{total} x {denominator - numerator}/{denominator} = {fmt(remaining)}.",
        {"t": total, "n": numerator, "d": denominator},
    )


def cd_cost_price(r, v):
    data = ((480, 20, 25), (600, 25, 20), (720, 30, 25), (840, 20, 30), (960, 25, 30))[v]
    cp, profit_pct, discount_pct = data
    who, friend = pair(v, 12)
    helper = third(v, 15)
    sp = F(cp * (100 + profit_pct) * (100 - discount_pct), 10000)
    return q(
        "cd_cost_price", v,
        f"A trader's cost is ₹{cp}, markup is {profit_pct}% and discount is "
        f"{discount_pct}%. {who}, {friend} and {helper} need the final selling price. "
        f"Find it.",
        fmt(sp),
        near(sp, 5),
        f"Selling price = {cp} x (1 + {profit_pct}/100) x (1 - {discount_pct}/100) "
        f"= {fmt(sp)}.",
        {"c": cp, "p": profit_pct, "d": discount_pct},
    )


def cd_population(r, v):
    data = ((20000, 10, 5), (24000, 15, 10), (30000, 20, 10), (36000, 25, 20), (40000, 10, 15))[v]
    start, growth, decline = data
    who, friend = pair(v, 13)
    helper = third(v, 16)
    result = F(start * (100 + growth) * (100 - decline), 10000)
    return q(
        "cd_population", v,
        f"A town has {start} residents. Population grows {growth}% in year one and "
        f"falls {decline}% in year two. {who}, {friend} and {helper} need the final "
        f"population. Find it.",
        fmt(result),
        near(result, 100),
        f"Final population = {start} x (1 + {growth}/100) x (1 - {decline}/100) = "
        f"{fmt(result)}.",
        {"p": start, "g": growth, "d": decline},
    )


def cd_average_missing(r, v):
    data = ((60, 70, 80, 75), (65, 75, 85, 80), (70, 80, 90, 85), (75, 85, 95, 90), (80, 90, 100, 95))[v]
    a, b, c, avg = data
    missing = 4 * avg - a - b - c
    who, friend = pair(v, 14)
    helper = third(v, 17)
    return q(
        "cd_average_missing", v,
        f"A caselet gives three readings {a}, {b}, {c} and an average {avg} over "
        f"four readings. {who}, {friend} and {helper} need the missing reading. "
        f"Find it.",
        fmt(missing),
        near(F(missing)),
        f"Missing reading = 4 x {avg} - ({a} + {b} + {c}) = {missing}.",
        {"a": a, "b": b, "c": c, "avg": avg},
    )


def cd_two_year_total(r, v):
    data = ((120, 150, 180, 210), (140, 170, 200, 230), (160, 190, 220, 250), (180, 210, 240, 270), (200, 230, 260, 290))[v]
    a1, a2, b1, b2 = data
    who, friend = pair(v, 15)
    helper = third(v, 18)
    total = a1 + a2 + b1 + b2
    return q(
        "cd_two_year_total", v,
        f"A company's two products had sales {a1}, {a2} and {b1}, {b2} lakh in "
        f"two years. {who}, {friend} and {helper} need the four-value total. Find it.",
        fmt(total),
        near(F(total), 5),
        f"Total = {a1} + {a2} + {b1} + {b2} = {total}.",
        {"a": a1, "b": a2, "c": b1, "d": b2},
    )


def cd_two_year_gap(r, v):
    data = ((120, 150, 180, 210), (140, 170, 200, 230), (160, 190, 220, 250), (180, 210, 240, 270), (200, 230, 260, 290))[v]
    a1, a2, b1, b2 = data
    who, friend = pair(v, 16)
    helper = third(v, 19)
    gap = (a2 + b2) - (a1 + b1)
    return q(
        "cd_two_year_gap", v,
        f"Product A sales: {a1} then {a2}; product B sales: {b1} then {b2}. "
        f"{who}, {friend} and {helper} need the increase in the combined total. "
        f"Find it.",
        fmt(gap),
        near(F(gap), 5),
        f"Combined second year minus combined first year = ({a2} + {b2}) - "
        f"({a1} + {b1}) = {gap}.",
        {"a": a1, "b": a2, "c": b1, "d": b2},
    )


def cd_share_after_add(r, v):
    data = ((40, 60, 20), (50, 70, 30), (60, 90, 40), (70, 105, 45), (80, 120, 50))[v]
    a, b, added = data
    who, friend = pair(v, 17)
    helper = third(v, 20)
    pct = F(a + added, a + b + added) * 100
    answer = fmt_dec(float(pct)) + "%"
    return q(
        "cd_share_after_add", v,
        f"A group has {a} members from section A and {b} from section B. {added} "
        f"new members, all from A, join. {who}, {friend} and {helper} need A's "
        f"percentage share afterwards. Find it.",
        answer,
        near_pct(pct),
        f"New A count = {a + added}; new total = {a + b + added}; share = "
        f"{a + added}/{a + b + added} x 100 = {answer}.",
        {"a": a, "b": b, "x": added},
    )


def cd_multi_tag(r, v):
    data = ((200, 40, 50, 20), (240, 48, 60, 24), (300, 60, 75, 30), (360, 72, 90, 36), (400, 80, 100, 40))[v]
    total, a, b, both = data
    who, friend = pair(v, 18)
    helper = third(v, 21)
    union = a + b - both
    pct = F(union, total) * 100
    answer = fmt_dec(float(pct)) + "%"
    return q(
        "cd_multi_tag", v,
        f"In a survey of {total} customers, {a} use mobile banking, {b} use net "
        f"banking and {both} use both. {who}, {friend} and {helper} need the "
        f"percentage using at least one. Find it.",
        answer,
        near_pct(pct),
        f"At least one = {a} + {b} - {both} = {union}; percentage = "
        f"{union}/{total} x 100 = {answer}.",
        {"t": total, "a": a, "b": b, "c": both},
    )


def cd_discount_ratio(r, v):
    data = ((600, 10, 540), (750, 20, 600), (900, 25, 675), (1200, 20, 960), (1500, 30, 1050))[v]
    marked, discount, final = data
    who, friend = pair(v, 19)
    helper = third(v, 22)
    ratio = F(final, marked - final)
    return q(
        "cd_discount_ratio", v,
        f"A caselet gives marked price ₹{marked}, discount {discount}% and selling "
        f"price ₹{final}. {who}, {friend} and {helper} need the ratio selling price "
        f"to discount amount. Find it.",
        fmt(ratio),
        near(ratio),
        f"Discount amount = {marked} - {final} = {marked - final}; ratio = "
        f"{final}/{marked - final} = {fmt(ratio)}.",
        {"m": marked, "f": final},
    )


def cd_target_actual(r, v):
    data = ((400, 480), (500, 600), (600, 720), (800, 960), (1000, 1200))[v]
    target, actual = data
    who, friend = pair(v, 20)
    helper = third(v, 23)
    pct = F(actual, target) * 100
    answer = fmt_dec(float(pct)) + "%"
    return q(
        "cd_target_actual", v,
        f"A branch target was ₹{target} lakh and actual sales were ₹{actual} lakh. "
        f"{who}, {friend} and {helper} need actual sales as a percentage of target. "
        f"Find it.",
        answer,
        near_pct(pct),
        f"Percentage = {actual}/{target} x 100 = {answer}.",
        {"t": target, "a": actual},
    )


def cd_expenditure_split(r, v):
    data = ((24000, 3, 5), (30000, 2, 5), (36000, 5, 8), (42000, 3, 7), (48000, 1, 4))[v]
    total, numerator, denominator = data
    who, friend = pair(v, 21)
    helper = third(v, 24)
    amount = F(total * numerator, denominator)
    return q(
        "cd_expenditure_split", v,
        f"A family's monthly expenditure is ₹{total} and {numerator}/{denominator} "
        f"of it is spent on food. {who}, {friend} and {helper} need the food "
        f"expenditure. Find it.",
        fmt(amount),
        near(amount, 100),
        f"Food expenditure = {total} x {numerator}/{denominator} = {fmt(amount)}.",
        {"t": total, "n": numerator, "d": denominator},
    )


def cd_growth_difference(r, v):
    data = ((100, 120, 200, 250), (120, 150, 240, 300), (150, 180, 300, 360), (180, 216, 360, 432), (200, 240, 400, 500))[v]
    a1, a2, b1, b2 = data
    who, friend = pair(v, 22)
    helper = third(v, 25)
    ga = F(a2 - a1, a1) * 100
    gb = F(b2 - b1, b1) * 100
    diff = abs(ga - gb)
    answer = fmt_dec(float(diff)) + " percentage points"
    return q(
        "cd_growth_difference", v,
        f"Series A goes from {a1} to {a2}; series B goes from {b1} to {b2}. "
        f"{who}, {friend} and {helper} need the positive difference in their growth "
        f"rates. Find it.",
        answer,
        [
            fmt_dec(float(diff) + 5) + " percentage points",
            fmt_dec(float(diff) - 5) + " percentage points",
            fmt_dec(float(diff) / 2) + " percentage points",
        ],
        f"Growth rates are {fmt(ga)}% and {fmt(gb)}%; the positive difference is "
        f"{answer}.",
        {"a": a1, "b": a2, "c": b1, "d": b2},
    )


def cd_stock_reorder(r, v):
    data = ((1200, 300, 150), (1500, 400, 200), (1800, 450, 250), (2100, 500, 300), (2400, 600, 350))[v]
    stock, sold, added = data
    who, friend = pair(v, 23)
    helper = third(v, 26)
    left = stock - sold + added
    return q(
        "cd_stock_reorder", v,
        f"A store began with {stock} units, sold {sold} units and then received "
        f"{added} new units. {who}, {friend} and {helper} need the closing stock. "
        f"Find it.",
        fmt(left),
        near(F(left), 10),
        f"Closing stock = {stock} - {sold} + {added} = {left}.",
        {"s": stock, "o": sold, "a": added},
    )


FAMILIES = (
    cd_total,
    cd_difference,
    cd_ratio,
    cd_pct_of_total,
    cd_missing_value,
    cd_average,
    cd_percentage_change,
    cd_successive_change,
    cd_weighted_avg,
    cd_ratio_split,
    cd_ratio_difference,
    cd_fraction_remaining,
    cd_cost_price,
    cd_population,
    cd_average_missing,
    cd_two_year_total,
    cd_two_year_gap,
    cd_share_after_add,
    cd_multi_tag,
    cd_discount_ratio,
    cd_target_actual,
    cd_expenditure_split,
    cd_growth_difference,
    cd_stock_reorder,
)


def build_caselet_data_interpretation():
    return build_specs(FAMILIES)
