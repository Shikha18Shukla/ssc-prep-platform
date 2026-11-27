# -*- coding: utf-8 -*-
"""Pipe and Cistern - 120 template-generated questions for the fourth Maths batch."""

from __future__ import annotations

from fractions import Fraction

from .bank import fmt, fmt_dec, near_ints, near_values
from .common import build_specs, pair, q, third

SOURCE = "Pipe and Cistern topic-wise mains sets (local PDFs)"
PAGES = {
    1: "Mains_Topic_wise_Time_and_Work_and_Pipes_and_Cistern_Set_1_Mains.pdf, pp. 1-8",
    2: "Mains_Topic_wise_Time_and_Work_and_Pipes_and_Cistern_Set_2_Mains.pdf, pp. 1-11",
    3: "Mains_Topic_wise_Time_and_Work_and_Pipes_and_Cistern_Set_3_Mains.pdf, pp. 1-8",
    4: "Mains_Topic_wise_Time_and_Work_and_Pipes_and_Cistern_Set_4_Mains.pdf, pp. 1-7",
}

LEADS = (
    "In a cistern drill,",
    "A water tank is being tested as follows:",
    "Consider this pipe-and-cistern setup.",
    "For a practice tank problem,",
    "While checking pipe rates,",
)


def dec(value, places=2):
    return fmt_dec(float(value), places)


def _alternate_total(x, y):
    """Exact finishing time when two inlets alternate for one unit each."""
    rate = Fraction(1, x) + Fraction(1, y)
    cycles = 1 // rate
    remaining = 1 - cycles * rate
    if remaining == 0:
        return Fraction(2 * cycles)
    if remaining <= Fraction(1, x):
        return Fraction(2 * cycles) + remaining * x
    return Fraction(2 * cycles + 1) + (remaining - Fraction(1, x)) * y


def pc_two_inlets(rng, variant):
    a, b = pair(variant, 0)
    x, y = [(12, 18), (10, 15), (8, 12), (6, 9), (20, 30)][variant % 5]
    answer = dec(1 / (Fraction(1, x) + Fraction(1, y)))
    text = (
        f"{LEADS[variant]} {a}'s inlet fills the cistern in {x} hours and "
        f"{b}'s inlet fills it in {y} hours. If both inlets are opened "
        "together, how many hours will they need to fill the cistern?"
    )
    return q(
        "pc_two_inlets", variant, text, answer,
        near_values(answer, rng, 1),
        f"Combined hourly rate = 1/{x} + 1/{y}; filling time = 1/rate = {answer} hours.",
        {"X": x, "Y": y},
    )


def pc_inlet_outlet(rng, variant):
    a, b = pair(variant, 1)
    x, y = [(12, 18), (10, 15), (8, 12), (6, 10), (20, 30)][variant % 5]
    value = Fraction(x * y, y - x)
    answer = fmt(value)
    text = (
        f"{LEADS[variant]} {a}'s inlet fills a tank in {x} hours, while "
        f"{b}'s drain empties the full tank in {y} hours. With both open from "
        "the start, how many hours does an empty tank take to fill?"
    )
    return q(
        "pc_inlet_outlet", variant, text, answer,
        near_ints(value.numerator, rng, 4),
        f"Net hourly rate = 1/{x} - 1/{y} = {fmt(Fraction(y - x, x * y))}; "
        f"time = {value.numerator} hours.",
        {"X": x, "Y": y},
    )


def pc_three_inlets(rng, variant):
    a, b = pair(variant, 2)
    c = third(variant, 4)
    x, y, z = [
        (6, 12, 12), (8, 12, 24), (10, 15, 30), (5, 10, 10), (12, 18, 36)
    ][variant % 5]
    answer = dec(1 / (Fraction(1, x) + Fraction(1, y) + Fraction(1, z)))
    text = (
        f"{LEADS[variant]} The inlets fitted by {a}, {b} and {c} fill a cistern "
        f"alone in {x}, {y} and {z} hours respectively. How many hours do all "
        "three need when opened together?"
    )
    return q(
        "pc_three_inlets", variant, text, answer,
        near_values(answer, rng, 1),
        f"Combined rate = 1/{x} + 1/{y} + 1/{z}; reciprocal gives {answer} hours.",
        {"X": x, "Y": y, "Z": z},
    )


def pc_efficiency_ratio(rng, variant):
    a, b = pair(variant, 3)
    m, t = [(2, 14), (3, 18), (4, 22), (5, 30), (3, 21)][variant % 5]
    answer = dec(Fraction(t, m))
    text = (
        f"{LEADS[variant]} {a}'s pipe is {m} times as efficient as {b}'s pipe. "
        f"{b}'s pipe alone fills the tank in {t} hours. How many hours does "
        f"{a}'s pipe alone need?"
    )
    return q(
        "pc_efficiency_ratio", variant, text, answer,
        near_values(answer, rng, 1),
        f"Filling time is inversely proportional to efficiency: {t}/{m} = {answer} hours.",
        {"M": m, "T": t},
    )


def pc_alternate_hours(rng, variant):
    a, b = pair(variant, 4)
    x, y = [(5, 10), (6, 9), (4, 6), (12, 18), (8, 12)][variant % 5]
    answer = dec(_alternate_total(x, y))
    text = (
        f"{LEADS[variant]} Inlets fitted by {a} and {b} are opened alternately "
        f"for one hour each, {a}'s inlet starting first. Alone they fill the "
        f"tank in {x} and {y} hours. How many hours from the start is the tank full?"
    )
    return q(
        "pc_alternate_hours", variant, text, answer,
        near_values(answer, rng, 1),
        f"Two-hour cycles complete 1/{x} + 1/{y} of the tank; the exact "
        f"finishing time with alternating one-hour slots is {answer} hours.",
        {"X": x, "Y": y},
    )


def pc_leak(rng, variant):
    a, b = pair(variant, 5)
    x, y = [(9, 18), (12, 20), (15, 25), (8, 24), (10, 14)][variant % 5]
    answer = dec(Fraction(x * y, y - x))
    text = (
        f"{LEADS[variant]} {a}'s inlet can fill the cistern in {x} hours, but a "
        f"leak logged by {b} drains a full cistern in {y} hours. How long does "
        "an empty cistern take to fill with the inlet open and the leak active?"
    )
    return q(
        "pc_leak", variant, text, answer,
        near_values(answer, rng, 1),
        f"Effective hourly rate = 1/{x} - 1/{y}; filling time = {answer} hours.",
        {"X": x, "Y": y},
    )


def pc_partial_fill(rng, variant):
    a, _ = pair(variant, 6)
    x, t = [(8, 3), (12, 5), (10, 4), (9, 6), (7, 2)][variant % 5]
    answer = fmt(Fraction(t, x))
    distractors = [
        fmt(Fraction(t, x + 1)),
        fmt(Fraction(t + 1, x)),
        fmt(Fraction(t, 2 * x)),
    ]
    text = (
        f"{LEADS[variant]} {a}'s pipe fills an empty tank in {x} hours. If it "
        f"is left open for {t} hours, what fraction of the tank is filled?"
    )
    return q(
        "pc_partial_fill", variant, text, answer, distractors,
        f"Fraction filled = {t} x (1/{x}) = {answer} of the tank.",
        {"X": x, "T": t},
    )


def pc_capacity_litres(rng, variant):
    a, b = pair(variant, 7)
    x, y, capacity = [
        (8, 12, 480), (6, 10, 360), (5, 15, 600), (4, 12, 240), (10, 15, 900)
    ][variant % 5]
    answer = fmt(capacity * (Fraction(1, x) + Fraction(1, y)))
    text = (
        f"{LEADS[variant]} {a}'s pipe fills a {capacity}-litre tank in {x} hours "
        f"and {b}'s pipe fills the same tank in {y} hours. How many litres per "
        "hour enter the tank when both pipes run together?"
    )
    return q(
        "pc_capacity_litres", variant, text, answer,
        near_ints(int(answer), rng, 5),
        f"Combined hourly rate = 1/{x} + 1/{y} = {fmt(Fraction(1, x) + Fraction(1, y))} "
        f"of the tank; {capacity} x that rate = {answer} litres per hour.",
        {"X": x, "Y": y, "C": capacity},
    )


def pc_time_fraction(rng, variant):
    a, _ = pair(variant, 8)
    x, n, d = [(12, 3, 5), (10, 2, 3), (8, 1, 4), (15, 4, 5), (9, 2, 3)][variant % 5]
    answer = dec(Fraction(n * x, d))
    text = (
        f"{LEADS[variant]} {a}'s pipe can fill a whole tank in {x} hours. "
        f"How many hours are needed to fill {n}/{d} of the tank?"
    )
    return q(
        "pc_time_fraction", variant, text, answer,
        near_values(answer, rng, 1),
        f"Time for {n}/{d} of the tank = ({n}/{d}) x {x} = {answer} hours.",
        {"X": x, "N": n, "D": d},
    )


def pc_outlet_only(rng, variant):
    a, _ = pair(variant, 9)
    x, n, d = [(12, 2, 3), (9, 1, 3), (15, 3, 5), (18, 4, 6), (10, 3, 4)][variant % 5]
    answer = dec(Fraction(n * x, d))
    text = (
        f"{LEADS[variant]} A full cistern drains through {a}'s outlet in {x} "
        f"hours. How long does it take to drain {n}/{d} of the full cistern?"
    )
    return q(
        "pc_outlet_only", variant, text, answer,
        near_values(answer, rng, 1),
        f"Draining {n}/{d} of a full cistern takes ({n}/{d}) x {x} = {answer} hours.",
        {"X": x, "N": n, "D": d},
    )


def pc_two_outlets(rng, variant):
    a, b = pair(variant, 10)
    x, y = [(6, 12), (8, 8), (10, 15), (9, 18), (12, 24)][variant % 5]
    answer = dec(1 / (Fraction(1, x) + Fraction(1, y)))
    text = (
        f"{LEADS[variant]} Two drains, one handled by {a} and one by {b}, empty "
        f"a full tank in {x} and {y} hours respectively. If both drains are "
        "opened on a full tank, how many hours until it is empty?"
    )
    return q(
        "pc_two_outlets", variant, text, answer,
        near_values(answer, rng, 1),
        f"Combined draining rate = 1/{x} + 1/{y}; emptying time = {answer} hours.",
        {"X": x, "Y": y},
    )


def pc_net_rate(rng, variant):
    a, b = pair(variant, 11)
    x, y = [(12, 18), (10, 15), (8, 12), (6, 9), (20, 30)][variant % 5]
    answer = fmt(Fraction(y - x, x * y))
    distractors = [
        fmt(Fraction(1, x + y)),
        fmt(Fraction(1, y - x)),
        fmt(Fraction(1, x) + Fraction(1, y)),
    ]
    text = (
        f"{LEADS[variant]} {a}'s inlet fills a tank in {x} hours while {b}'s "
        f"outlet empties a full tank in {y} hours. With both open, what "
        "fraction of the tank is filled in one hour?"
    )
    return q(
        "pc_net_rate", variant, text, answer, distractors,
        f"Net one-hour fill = 1/{x} - 1/{y} = {answer} of the tank.",
        {"X": x, "Y": y},
    )


def pc_large_small(rng, variant):
    a, b = pair(variant, 12)
    x, t = [(12, 8), (10, 6), (18, 12), (15, 10), (20, 16)][variant % 5]
    answer = fmt(Fraction(x * t, x - t))
    text = (
        f"{LEADS[variant]} The large pipe fitted by {a} fills a tank in {x} "
        f"hours. Together with the small pipe fitted by {b}, the tank fills in "
        f"{t} hours. How many hours does the small pipe alone need?"
    )
    return q(
        "pc_large_small", variant, text, answer,
        near_ints(int(answer), rng, 4),
        f"Small-pipe rate = 1/{t} - 1/{x}; its alone time = {x}x{t}/({x}-{t}) = {answer} hours.",
        {"X": x, "T": t},
    )


def pc_fill_then_leak(rng, variant):
    a, b = pair(variant, 13)
    x, y, t = [(10, 15, 4), (12, 18, 3), (8, 12, 2), (6, 9, 1), (15, 30, 5)][variant % 5]
    remaining = 1 - Fraction(t, x)
    net = Fraction(1, x) - Fraction(1, y)
    answer = fmt(t + remaining / net)
    text = (
        f"{LEADS[variant]} {a}'s inlet fills the cistern in {x} hours. It runs "
        f"alone for {t} hours, then a leak logged by {b} opens and drains a "
        f"full cistern in {y} hours while the inlet continues. How many hours "
        "in total from the start until the cistern is full?"
    )
    return q(
        "pc_fill_then_leak", variant, text, answer,
        near_ints(int(answer), rng, 4),
        f"After {t} hours, {fmt(remaining)} remains; net rate afterwards = "
        f"1/{x} - 1/{y}; extra time = {fmt(remaining / net)} hours; total = {answer} hours.",
        {"X": x, "Y": y, "T": t},
    )


def pc_half_full(rng, variant):
    a, _ = pair(variant, 14)
    x, n, d = [(10, 1, 2), (14, 1, 2), (9, 2, 3), (12, 3, 4), (15, 1, 3)][variant % 5]
    answer = dec(Fraction(x * (d - n), d))
    text = (
        f"{LEADS[variant]} {a}'s pipe fills an empty tank in {x} hours. The "
        f"tank is already {n}/{d} full. How many more hours does the same pipe "
        "need to fill it completely?"
    )
    return q(
        "pc_half_full", variant, text, answer,
        near_values(answer, rng, 1),
        f"Unfilled part = ({d}-{n})/{d}; extra time = {x} x ({d}-{n})/{d} = {answer} hours.",
        {"X": x, "N": n, "D": d},
    )


def pc_three_with_outlet(rng, variant):
    a, b = pair(variant, 15)
    c = third(variant, 17)
    x, y, z = [
        (12, 18, 36), (10, 15, 30), (8, 12, 24), (6, 9, 18), (20, 30, 60)
    ][variant % 5]
    answer = dec(1 / (Fraction(1, x) + Fraction(1, y) - Fraction(1, z)))
    text = (
        f"{LEADS[variant]} Inlets fitted by {a} and {b} fill a cistern in {x} "
        f"and {y} hours, while an outlet fitted by {c} drains a full cistern "
        f"in {z} hours. How long does an empty cistern take to fill with all "
        "three pipes open?"
    )
    return q(
        "pc_three_with_outlet", variant, text, answer,
        near_values(answer, rng, 1),
        f"Net rate = 1/{x} + 1/{y} - 1/{z}; filling time = {answer} hours.",
        {"X": x, "Y": y, "Z": z},
    )


def pc_rate_per_minute(rng, variant):
    a, _ = pair(variant, 16)
    x, capacity = [(20, 600), (15, 450), (24, 720), (18, 900), (25, 500)][variant % 5]
    answer = fmt(Fraction(capacity, x))
    text = (
        f"{LEADS[variant]} {a}'s pipe fills a {capacity}-litre tank in {x} "
        "minutes. At a constant rate, how many litres of water enter the tank "
        "each minute?"
    )
    return q(
        "pc_rate_per_minute", variant, text, answer,
        near_ints(int(answer), rng, 4),
        f"Flow rate = {capacity} litres / {x} minutes = {answer} litres per minute.",
        {"X": x, "C": capacity},
    )


def pc_remaining_work(rng, variant):
    a, b = pair(variant, 17)
    x, y, t = [
        (12, 18, 4), (10, 15, 3), (8, 12, 2), (6, 9, 2), (20, 30, 6)
    ][variant % 5]
    rate = Fraction(1, x) + Fraction(1, y)
    answer = fmt(1 - t * rate)
    distractors = [
        fmt(1 - (t + 1) * rate),
        fmt(1 - Fraction(t, x)),
        fmt(Fraction(t, x * y)),
    ]
    text = (
        f"{LEADS[variant]} The inlets of {a} and {b} fill a tank in {x} and "
        f"{y} hours alone. Both are opened together for {t} hours. What "
        "fraction of the tank is still empty?"
    )
    return q(
        "pc_remaining_work", variant, text, answer, distractors,
        f"Filled = {t}(1/{x} + 1/{y}) = {fmt(t * rate)}; still empty = {answer}.",
        {"X": x, "Y": y, "T": t},
    )


def pc_staggered_start(rng, variant):
    a, b = pair(variant, 18)
    x, y, t = [
        (12, 18, 3), (10, 15, 2), (8, 12, 2), (6, 9, 1), (20, 30, 5)
    ][variant % 5]
    answer = dec(t + (1 - Fraction(t, x)) / (Fraction(1, x) + Fraction(1, y)))
    text = (
        f"{LEADS[variant]} {a}'s inlet starts filling an empty tank and, {t} "
        f"hours later, {b}'s inlet is also opened. Alone they fill the tank in "
        f"{x} and {y} hours. How many hours after {a}'s start is the tank full?"
    )
    return q(
        "pc_staggered_start", variant, text, answer,
        near_values(answer, rng, 1),
        f"After {t} hours, {fmt(1 - Fraction(t, x))} remains; joint rate = "
        f"1/{x} + 1/{y}; total time = {answer} hours.",
        {"X": x, "Y": y, "T": t},
    )


def pc_outlet_after_hours(rng, variant):
    a, b = pair(variant, 19)
    x, y, t = [
        (10, 15, 5), (12, 18, 4), (8, 12, 3), (6, 9, 2), (15, 30, 6)
    ][variant % 5]
    answer = fmt(t + (1 - Fraction(t, x)) / (Fraction(1, x) - Fraction(1, y)))
    text = (
        f"{LEADS[variant]} {a}'s inlet fills a tank in {x} hours and runs alone "
        f"for {t} hours. Then {b}'s outlet, which drains a full tank in {y} "
        "hours, is opened while the inlet stays open. How many hours from the "
        "start is the tank full?"
    )
    return q(
        "pc_outlet_after_hours", variant, text, answer,
        near_ints(int(answer), rng, 4),
        f"Remaining after {t} hours = {fmt(1 - Fraction(t, x))}; net rate = "
        f"1/{x} - 1/{y}; total = {answer} hours.",
        {"X": x, "Y": y, "T": t},
    )


def pc_relative_efficiency(rng, variant):
    a, b = pair(variant, 0)
    m, t = [(2, 9), (3, 8), (4, 6), (5, 5), (1, 12)][variant % 5]
    answer = fmt(t * (m + 1))
    text = (
        f"{LEADS[variant]} {a}'s pipe is {m} times as efficient as {b}'s pipe. "
        f"Working together they fill the tank in {t} hours. How many hours "
        f"would {b}'s pipe alone take?"
    )
    return q(
        "pc_relative_efficiency", variant, text, answer,
        near_ints(int(answer), rng, 4),
        f"If {b}'s rate is 1 unit, combined rate is {m}+1 = {m + 1} units; "
        f"{b} alone takes {t} x {m + 1} = {answer} hours.",
        {"M": m, "T": t},
    )


def pc_alternate_minutes(rng, variant):
    a, b = pair(variant, 1)
    x, y = [(6, 12), (5, 10), (4, 4), (9, 18), (8, 12)][variant % 5]
    answer = dec(_alternate_total(x, y))
    text = (
        f"{LEADS[variant]} Two inlets, attached to {a} and {b}, are opened "
        f"alternately for one minute each with {a}'s inlet first. Alone they "
        f"fill the tank in {x} and {y} minutes. How many minutes from the start "
        "is the tank full?"
    )
    return q(
        "pc_alternate_minutes", variant, text, answer,
        near_values(answer, rng, 1),
        f"Alternating one-minute slots of 1/{x} and 1/{y} finish the tank in "
        f"exactly {answer} minutes.",
        {"X": x, "Y": y},
    )


def pc_tank_fraction_rate(rng, variant):
    a, _ = pair(variant, 2)
    t, n, d = [(6, 2, 5), (8, 3, 4), (9, 3, 5), (10, 4, 5), (12, 2, 3)][variant % 5]
    answer = dec(Fraction(t * d, n))
    text = (
        f"{LEADS[variant]} {a}'s pipe fills {n}/{d} of a tank in {t} hours. At "
        "that constant rate, how many hours does it take to fill the entire tank?"
    )
    return q(
        "pc_tank_fraction_rate", variant, text, answer,
        near_values(answer, rng, 1),
        f"{n}/{d} of the tank takes {t} hours; the whole tank takes "
        f"{t} x {d}/{n} = {answer} hours.",
        {"T": t, "N": n, "D": d},
    )


def pc_compare(rng, variant):
    a, b = pair(variant, 3)
    x, y = [(12, 18), (20, 15), (9, 14), (24, 16), (12, 12)][variant % 5]
    options = ("First pipe", "Second pipe", "Both are equal", "Cannot be determined")
    answer = "Both are equal" if x == y else ("First pipe" if x < y else "Second pipe")
    distractors = [option for option in options if option != answer]
    text = (
        f"{LEADS[variant]} {a}'s pipe fills a tank in {x} hours and {b}'s pipe "
        "fills the same tank in another time. Which pipe has the greater "
        f"filling rate if {b}'s pipe takes {y} hours?"
    )
    return q(
        "pc_compare", variant, text, answer, distractors,
        f"Smaller filling time means larger rate: {x} versus {y} hours, so the "
        f"answer is {answer}.",
        {"X": x, "Y": y},
    )


FAMILIES = [
    pc_two_inlets,
    pc_inlet_outlet,
    pc_three_inlets,
    pc_efficiency_ratio,
    pc_alternate_hours,
    pc_leak,
    pc_partial_fill,
    pc_capacity_litres,
    pc_time_fraction,
    pc_outlet_only,
    pc_two_outlets,
    pc_net_rate,
    pc_large_small,
    pc_fill_then_leak,
    pc_half_full,
    pc_three_with_outlet,
    pc_rate_per_minute,
    pc_remaining_work,
    pc_staggered_start,
    pc_outlet_after_hours,
    pc_relative_efficiency,
    pc_alternate_minutes,
    pc_tank_fraction_rate,
    pc_compare,
]


def build_pipe_and_cistern():
    return build_specs(FAMILIES)
