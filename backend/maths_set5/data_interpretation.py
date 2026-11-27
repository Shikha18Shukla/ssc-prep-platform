# -*- coding: utf-8 -*-
"""Data Interpretation — 120 verified questions for the fifth Maths batch."""

from __future__ import annotations

from fractions import Fraction

from .bank import fmt, fmt_dec
from .common import build_specs, pair, q, third

SOURCE = "Data Interpretation class notes (local PDFs)"
PAGES = {
    1: "DATA INTERPRETATION 01  Class Notes.pdf, pp. 4-22",
    2: "dd6dc577-2571-460b-952b-3b67ddf71c1c.pdf, pp. 4-17",
    3: "d0d52b32-a3ee-4287-a42c-a34734858e19.pdf, pp. 4-22",
}


def F(a, b=1):
    return Fraction(a, b)


def near(value: Fraction, step=1):
    return [fmt(value + step), fmt(value - step), fmt(value * 2)]


def near_pct(value: Fraction):
    return [fmt_dec(float(value) + 5) + "%", fmt_dec(float(value) - 5) + "%", fmt_dec(float(value) / 2) + "%"]


def table_text(rows):
    return "; ".join(f"{name}={value}" for name, value in rows)


def di_table_total(r, v):
    data = ((12, 18, 24, 30), (15, 21, 27, 33), (20, 25, 35, 40), (24, 30, 42, 48), (28, 36, 50, 56))[v]
    who, friend = pair(v)
    helper = third(v, 3)
    total = sum(data)
    return q(
        "di_table_total", v,
        f"Table of daily collections (₹ thousand): {table_text([('A', data[0]), ('B', data[1]), ('C', data[2]), ('D', data[3])])}. "
        f"{who}, {friend} and {helper} need the total. Find it.",
        fmt(total),
        near(F(total)),
        f"Add all four entries: {' + '.join(str(x) for x in data)} = {total}.",
        {"v": list(data)},
    )


def di_table_difference(r, v):
    data = ((48, 32), (56, 39), (64, 45), (72, 51), (84, 58))[v]
    who, friend = pair(v, 1)
    helper = third(v, 4)
    diff = data[0] - data[1]
    return q(
        "di_table_difference", v,
        f"Table of two branches (₹ lakh): Branch P={data[0]}, Branch Q={data[1]}. "
        f"{who}, {friend} and {helper} need P minus Q. Find it.",
        fmt(diff),
        near(F(diff)),
        f"Difference = {data[0]} - {data[1]} = {diff}.",
        {"x": data[0], "y": data[1]},
    )


def di_table_pct_change(r, v):
    data = ((40, 50), (50, 60), (60, 75), (80, 100), (90, 120))[v]
    old, new = data
    who, friend = pair(v, 2)
    helper = third(v, 5)
    pct = F(new - old, old) * 100
    answer = fmt_dec(float(pct)) + "%"
    return q(
        "di_table_pct_change", v,
        f"Table: old value={old}, new value={new}. {who}, {friend} and {helper} "
        f"calculate the percentage increase. Find it.",
        answer,
        near_pct(pct),
        f"Increase = {new} - {old} = {new - old}; percentage = "
        f"({new - old}/{old}) x 100 = {answer}.",
        {"old": old, "new": new},
    )


def di_table_ratio(r, v):
    data = ((18, 24), (21, 28), (27, 36), (33, 44), (39, 52))[v]
    a, b = data
    from math import gcd
    g = gcd(a, b)
    answer = f"{a // g}:{b // g}"
    who, friend = pair(v, 3)
    helper = third(v, 6)
    return q(
        "di_table_ratio", v,
        f"Table: section X={a} students, section Y={b} students. {who}, {friend} "
        f"and {helper} need the ratio X:Y in simplest form. Find it.",
        answer,
        [f"{b // g}:{a // g}", f"{a // g + 1}:{b // g}", f"{a}:{b}"],
        f"Divide both values by their greatest common divisor {g}: {answer}.",
        {"a": a, "b": b},
    )


def di_table_average(r, v):
    data = ((12, 18, 24), (15, 20, 25), (21, 27, 33), (24, 30, 42), (30, 36, 48))[v]
    who, friend = pair(v, 4)
    helper = third(v, 7)
    avg = F(sum(data), 3)
    return q(
        "di_table_average", v,
        f"Table of three monthly values: {table_text([('Jan', data[0]), ('Feb', data[1]), ('Mar', data[2])])}. "
        f"{who}, {friend} and {helper} need their average. Find it.",
        fmt(avg),
        near(avg),
        f"Average = ({' + '.join(str(x) for x in data)})/3 = {fmt(avg)}.",
        {"v": list(data)},
    )


def di_table_missing(r, v):
    data = ((20, 24, 28, 96), (25, 30, 35, 108), (30, 36, 42, 120), (35, 42, 49, 144), (40, 48, 56, 168))[v]
    a, b, c, total = data
    missing = total - a - b - c
    who, friend = pair(v, 5)
    helper = third(v, 8)
    return q(
        "di_table_missing", v,
        f"Incomplete table: P={a}, Q={b}, R={c}, S=?, total={total}. {who}, "
        f"{friend} and {helper} need the missing value S. Find it.",
        fmt(missing),
        near(F(missing)),
        f"S = total - (P + Q + R) = {total} - {a + b + c} = {missing}.",
        {"a": a, "b": b, "c": c, "t": total},
    )


def di_bar_max(r, v):
    data = ((32, 45, 28, 51), (38, 42, 55, 47), (44, 39, 58, 50), (53, 61, 48, 57), (66, 59, 72, 64))[v]
    who, friend = pair(v, 6)
    helper = third(v, 9)
    answer = ("P", "Q", "R", "S")[max(range(4), key=lambda i: data[i])]
    values = "; ".join(f"{name}={value}" for name, value in zip(("P", "Q", "R", "S"), data))
    choices = [name for name in ("P", "Q", "R", "S") if name != answer]
    return q(
        "di_bar_max", v,
        f"Bar chart values: {values}. {who}, {friend} and {helper} identify the "
        f"category with the highest value. Which is it?",
        answer,
        choices,
        f"Compare the four bars; the largest value is {max(data)}, belonging to {answer}.",
        {"v": list(data)},
    )


def di_bar_min(r, v):
    data = ((32, 45, 28, 51), (38, 42, 55, 47), (44, 39, 58, 50), (53, 61, 48, 57), (66, 59, 72, 64))[v]
    who, friend = pair(v, 7)
    helper = third(v, 10)
    answer = ("P", "Q", "R", "S")[min(range(4), key=lambda i: data[i])]
    values = "; ".join(f"{name}={value}" for name, value in zip(("P", "Q", "R", "S"), data))
    choices = [name for name in ("P", "Q", "R", "S") if name != answer]
    return q(
        "di_bar_min", v,
        f"Bar chart values: {values}. {who}, {friend} and {helper} identify the "
        f"category with the lowest value. Which is it?",
        answer,
        choices,
        f"The smallest bar value is {min(data)}, belonging to {answer}.",
        {"v": list(data)},
    )


def di_bar_sum_two(r, v):
    data = ((32, 45, 28, 51), (38, 42, 55, 47), (44, 39, 58, 50), (53, 61, 48, 57), (66, 59, 72, 64))[v]
    who, friend = pair(v, 8)
    helper = third(v, 11)
    answer = fmt(data[0] + data[2])
    values = "; ".join(f"{name}={value}" for name, value in zip(("P", "Q", "R", "S"), data))
    return q(
        "di_bar_sum_two", v,
        f"Bar chart values: {values}. {who}, {friend} and {helper} need the combined "
        f"value of P and R. Find it.",
        answer,
        near(F(data[0] + data[2])),
        f"P + R = {data[0]} + {data[2]} = {data[0] + data[2]}.",
        {"a": data[0], "c": data[2]},
    )


def di_bar_pct_total(r, v):
    data = ((20, 30, 25, 25), (15, 35, 20, 30), (24, 26, 30, 20), (18, 32, 22, 28), (25, 25, 30, 20))[v]
    who, friend = pair(v, 9)
    helper = third(v, 12)
    total = sum(data)
    pct = F(data[0] * 100, total)
    answer = fmt_dec(float(pct)) + "%"
    values = "; ".join(f"{name}={value}" for name, value in zip(("P", "Q", "R", "S"), data))
    return q(
        "di_bar_pct_total", v,
        f"Bar chart values: {values}. {who}, {friend} and {helper} need P as a "
        f"percentage of the total. Find it.",
        answer,
        near_pct(pct),
        f"Total = {total}; P's share = {data[0]}/{total} x 100 = {answer}.",
        {"a": data[0], "t": total},
    )


def di_line_increase(r, v):
    data = ((45, 60), (52, 65), (58, 72), (64, 80), (75, 90))[v]
    who, friend = pair(v, 10)
    helper = third(v, 13)
    diff = data[1] - data[0]
    return q(
        "di_line_increase", v,
        f"Line graph: 2021={data[0]}, 2022={data[1]}. {who}, {friend} and {helper} "
        f"need the absolute increase from 2021 to 2022. Find it.",
        fmt(diff),
        near(F(diff)),
        f"Increase = {data[1]} - {data[0]} = {diff}.",
        {"a": data[0], "b": data[1]},
    )


def di_line_decrease(r, v):
    data = ((80, 64), (90, 72), (100, 85), (120, 96), (150, 120))[v]
    who, friend = pair(v, 11)
    helper = third(v, 14)
    pct = F(data[0] - data[1], data[0]) * 100
    answer = fmt_dec(float(pct)) + "%"
    return q(
        "di_line_decrease", v,
        f"Line graph: original={data[0]}, later={data[1]}. {who}, {friend} and "
        f"{helper} need the percentage decrease. Find it.",
        answer,
        near_pct(pct),
        f"Decrease = {data[0] - data[1]}; percentage = ({data[0] - data[1]}/{data[0]}) "
        f"x 100 = {answer}.",
        {"a": data[0], "b": data[1]},
    )


def di_line_average(r, v):
    data = ((40, 50, 60), (45, 55, 65), (50, 65, 80), (60, 70, 95), (70, 80, 110))[v]
    who, friend = pair(v, 12)
    helper = third(v, 15)
    avg = F(sum(data), 3)
    return q(
        "di_line_average", v,
        f"Line graph values for 2022, 2023 and 2024: {data[0]}, {data[1]} and "
        f"{data[2]}. {who}, {friend} and {helper} need the three-year average. Find it.",
        fmt(avg),
        near(avg),
        f"Average = ({sum(data)})/3 = {fmt(avg)}.",
        {"v": list(data)},
    )


def di_line_growth(r, v):
    data = ((25, 30), (36, 45), (48, 60), (55, 66), (72, 90))[v]
    who, friend = pair(v, 13)
    helper = third(v, 16)
    pct = F(data[1] - data[0], data[0]) * 100
    answer = fmt_dec(float(pct)) + "%"
    return q(
        "di_line_growth", v,
        f"Line graph: first year={data[0]}, next year={data[1]}. {who}, {friend} and "
        f"{helper} need the year-on-year growth rate. Find it.",
        answer,
        near_pct(pct),
        f"Growth = ({data[1]} - {data[0]})/{data[0]} x 100 = {answer}.",
        {"a": data[0], "b": data[1]},
    )


def di_pie_angle(r, v):
    data = ((25, 360), (30, 360), (15, 360), (20, 360), (35, 360))[v]
    pct, total = data
    who, friend = pair(v, 14)
    helper = third(v, 17)
    angle = F(pct * total, 100)
    return q(
        "di_pie_angle", v,
        f"A pie chart has {pct}% in one sector and a full-circle total of {total} "
        f"degrees. {who}, {friend} and {helper} need the sector angle. Find it.",
        fmt(angle),
        near(angle, 10),
        f"Sector angle = {pct}/100 x {total} = {fmt(angle)} degrees.",
        {"p": pct, "d": total},
    )


def di_pie_value(r, v):
    data = ((90, 720), (72, 900), (108, 1080), (54, 1200), (144, 1440))[v]
    angle, total = data
    who, friend = pair(v, 15)
    helper = third(v, 18)
    value = F(angle * total, 360)
    return q(
        "di_pie_value", v,
        f"A pie chart sector is {angle} degrees and the total value is {total}. "
        f"{who}, {friend} and {helper} need the sector's value. Find it.",
        fmt(value),
        near(value, 5),
        f"Sector value = {angle}/360 x {total} = {fmt(value)}.",
        {"d": angle, "t": total},
    )


def di_pie_diff(r, v):
    data = ((90, 60, 720), (120, 45, 900), (108, 72, 1080), (135, 90, 1200), (144, 36, 1440))[v]
    a, b, total = data
    who, friend = pair(v, 16)
    helper = third(v, 19)
    diff = F((a - b) * total, 360)
    return q(
        "di_pie_diff", v,
        f"In a pie chart, sector A is {a} degrees and sector B is {b} degrees; "
        f"the total value is {total}. {who}, {friend} and {helper} need A's value "
        f"minus B's value. Find it.",
        fmt(diff),
        near(diff, 5),
        f"Difference in degrees = {a - b}; value difference = ({a - b}/360) x "
        f"{total} = {fmt(diff)}.",
        {"a": a, "b": b, "t": total},
    )


def di_mixed_sum(r, v):
    data = ((120, 80, 60, 40), (150, 90, 70, 50), (180, 110, 90, 60), (210, 130, 100, 80), (240, 150, 120, 90))[v]
    who, friend = pair(v, 17)
    helper = third(v, 20)
    total = sum(data)
    return q(
        "di_mixed_sum", v,
        f"Mixed chart: table value={data[0]}, bar value={data[1]}, line value="
        f"{data[2]}, pie-sector value={data[3]}. {who}, {friend} and {helper} need "
        f"the grand total. Find it.",
        fmt(total),
        near(F(total), 5),
        f"Grand total = {' + '.join(str(x) for x in data)} = {total}.",
        {"v": list(data)},
    )


def di_pct_point(r, v):
    data = ((45, 60), (50, 65), (55, 70), (62, 75), (68, 80))[v]
    who, friend = pair(v, 18)
    helper = third(v, 21)
    diff = data[1] - data[0]
    return q(
        "di_pct_point", v,
        f"Pass rates: Section A={data[0]}%, Section B={data[1]}%. {who}, {friend} "
        f"and {helper} need the difference in percentage points. Find it.",
        fmt(diff),
        near(F(diff)),
        f"Difference = {data[1]}% - {data[0]}% = {diff} percentage points.",
        {"a": data[0], "b": data[1]},
    )


def di_pass_percentage(r, v):
    data = ((200, 150), (250, 180), (300, 210), (400, 280), (500, 360))[v]
    appeared, passed = data
    who, friend = pair(v, 19)
    helper = third(v, 22)
    pct = F(passed * 100, appeared)
    answer = fmt_dec(float(pct)) + "%"
    return q(
        "di_pass_percentage", v,
        f"Exam table: {appeared} appeared and {passed} passed. {who}, {friend} and "
        f"{helper} need the pass percentage. Find it.",
        answer,
        near_pct(pct),
        f"Pass percentage = {passed}/{appeared} x 100 = {answer}.",
        {"a": appeared, "p": passed},
    )


def di_ratio_parts(r, v):
    data = ((24, 36, 60), (30, 45, 75), (36, 48, 84), (42, 56, 98), (54, 72, 126))[v]
    a, b, total = data
    from math import gcd
    g = gcd(a, b)
    who, friend = pair(v, 20)
    helper = third(v, 23)
    return q(
        "di_ratio_parts", v,
        f"A table shows part A={a}, part B={b} and total={total}. {who}, {friend} "
        f"and {helper} need the ratio A:B in lowest terms. Find it.",
        f"{a // g}:{b // g}",
        [f"{b // g}:{a // g}", f"{a}:{b}", f"{a // g + 1}:{b // g}"],
        f"Divide {a} and {b} by {g}: {a // g}:{b // g}.",
        {"a": a, "b": b},
    )


def di_two_table_multi(r, v):
    data = ((120, 80, 150, 100), (140, 90, 180, 120), (160, 110, 200, 140), (180, 130, 240, 160), (220, 150, 280, 180))[v]
    a, b, c, d = data
    who, friend = pair(v, 21)
    helper = third(v, 24)
    diff = (a + c) - (b + d)
    return q(
        "di_two_table_multi", v,
        f"Two tables: first has X={a}, Y={b}; second has X={c}, Y={d}. {who}, "
        f"{friend} and {helper} need total X minus total Y. Find it.",
        fmt(diff),
        near(F(diff), 5),
        f"Total X = {a + c}; total Y = {b + d}; difference = {diff}.",
        {"a": a, "b": b, "c": c, "d": d},
    )


def di_weighted_avg(r, v):
    data = ((20, 60, 30, 80), (25, 70, 35, 85), (30, 75, 40, 90), (40, 80, 60, 95), (50, 85, 70, 90))[v]
    n1, a1, n2, a2 = data
    who, friend = pair(v, 22)
    helper = third(v, 25)
    avg = F(n1 * a1 + n2 * a2, n1 + n2)
    return q(
        "di_weighted_avg", v,
        f"Table: group 1 has {n1} items averaging {a1}; group 2 has {n2} items "
        f"averaging {a2}. {who}, {friend} and {helper} need the combined average. "
        f"Find it.",
        fmt(avg),
        near(avg),
        f"Weighted average = ({n1}x{a1} + {n2}x{a2})/({n1} + {n2}) = {fmt(avg)}.",
        {"n1": n1, "a1": a1, "n2": n2, "a2": a2},
    )


def di_growth_compare(r, v):
    data = ((100, 120, 200, 230), (120, 150, 240, 276), (150, 180, 300, 330), (180, 216, 360, 396), (200, 250, 400, 440))[v]
    a1, a2, b1, b2 = data
    who, friend = pair(v, 23)
    helper = third(v, 26)
    ga = F(a2 - a1, a1) * 100
    gb = F(b2 - b1, b1) * 100
    answer = "A" if ga > gb else "B" if gb > ga else "Equal"
    choices = [name for name in ("A", "B", "Equal") if name != answer] + ["Neither"]
    return q(
        "di_growth_compare", v,
        f"Table: series A goes from {a1} to {a2}; series B goes from {b1} to "
        f"{b2}. {who}, {friend} and {helper} identify the series with the higher "
        f"percentage growth. Which is it?",
        answer,
        choices,
        f"Growth of A = {fmt(ga)}%, growth of B = {fmt(gb)}%; the higher is {answer}.",
        {"a1": a1, "a2": a2, "b1": b1, "b2": b2},
    )


FAMILIES = (
    di_table_total,
    di_table_difference,
    di_table_pct_change,
    di_table_ratio,
    di_table_average,
    di_table_missing,
    di_bar_max,
    di_bar_min,
    di_bar_sum_two,
    di_bar_pct_total,
    di_line_increase,
    di_line_decrease,
    di_line_average,
    di_line_growth,
    di_pie_angle,
    di_pie_value,
    di_pie_diff,
    di_mixed_sum,
    di_pct_point,
    di_pass_percentage,
    di_ratio_parts,
    di_two_table_multi,
    di_weighted_avg,
    di_growth_compare,
)


def build_data_interpretation():
    return build_specs(FAMILIES)
