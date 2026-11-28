# -*- coding: utf-8 -*-
"""Independent answer sheet for Pipe and Cistern Set 8 (Mains).

The verifier passes the exact ``verification_data.inputs`` dictionary from a
question to the lambda stored here; no builder, common or bank logic is used.
"""

from __future__ import annotations

from .formula_helpers import F, fmt, money

FORMULAS = {}


def _frac(value):
    """Parse a JSON-safe fraction string (or a number) exactly."""
    if isinstance(value, str):
        if "/" in value:
            num, den = value.split("/", 1)
            return F(int(num), int(den))
        return F(int(value))
    return F(value)


def _alt_finish(start, x, y):
    filled = F(start)
    hour = 0
    while filled < 1:
        pipe = x if hour % 2 == 0 else y
        before = filled
        filled += F(1, pipe)
        if filled >= 1:
            return F(hour) + (1 - before) * pipe
        hour += 1
    return F(hour)


def _intermittent(inlet, run, cycle):
    filled = F(0)
    hour = 0
    while True:
        if hour % cycle < run:
            before = filled
            filled += F(1, inlet)
            if filled >= 1:
                return F(hour) + (1 - before) * inlet
        hour += 1


def _alternating_then_b(a, b, hours):
    filled = F(0)
    for hour in range(hours):
        pipe = a if hour % 2 == 0 else b
        before = filled
        filled += F(1, pipe)
        if filled >= 1:
            return F(hour) + (1 - before) * pipe
    return F(hours) + (1 - filled) * b


def _alternate_three(a, b, c, hours):
    filled = F(0)
    pipes = (a, b, c)
    for hour in range(hours):
        pipe = pipes[hour % 3]
        before = filled
        filled += F(1, pipe)
        if filled >= 1:
            return F(hour) + (1 - before) * pipe
    return F(hours) + _alt_finish(filled, a, b)


FORMULAS["pcm_two_inlets"] = lambda d: fmt(
    F(d["a"], 3) + F(2 * d["a"] * d["b"], 3 * (d["a"] + d["b"]))
)

FORMULAS["pcm_inlet_outlet"] = lambda d: fmt(
    F(2 * d["a"] * d["b"], 3 * (d["b"] - d["a"]))
)

FORMULAS["pcm_alternating_pipes"] = lambda d: fmt(
    _alternating_then_b(d["a"], d["b"], d["hours"])
)

FORMULAS["pcm_leakage"] = lambda d: fmt(
    F(d["inlet"], 2) + F(d["inlet"] * d["leak"], 2 * (d["leak"] - d["inlet"]))
)

FORMULAS["pcm_partial_fill"] = lambda d: fmt(
    _frac(d["frac"]) * d["inlet"] * d["outlet"] / (2 * (d["inlet"] - d["outlet"]))
    + (1 - _frac(d["frac"]) / 2) * d["inlet"]
)

FORMULAS["pcm_three_sequence"] = lambda d: fmt(
    d["after_a"]
    + d["after_b"]
    + (
        1
        - F(d["after_a"], d["a"])
        - d["after_b"] * (F(1, d["a"]) + F(1, d["b"]))
    )
    / (F(1, d["a"]) + F(1, d["b"]) + F(1, d["c"]))
)

FORMULAS["pcm_capacity_change"] = lambda d: fmt(
    F(d["inlet"]) * (F(d["base"], 2) - d["extra"]) / d["base"]
    + F(d["base"], 2) / (F(d["base"], d["inlet"]) + d["extra"])
)

FORMULAS["pcm_efficiency_drop"] = lambda d: fmt(
    d["after"]
    + (1 - F(d["after"], d["inlet"])) * F(d["inlet"] * 100, 100 - d["drop"])
)

FORMULAS["pcm_tank_waste"] = lambda d: fmt(
    F(d["inlet"], 3)
    + F(2 * d["capacity"], 3 * (F(d["capacity"], d["inlet"]) - d["waste"]))
)

FORMULAS["pcm_intermittent"] = lambda d: fmt(
    _intermittent(d["inlet"], d["run"], d["cycle"])
)

FORMULAS["pcm_two_tanks"] = lambda d: fmt(
    (_frac(d["t2"]) - _frac(d["t1"])) / (F(1, d["a"]) - F(1, d["b"]))
    if d["ask"] == "catch_up"
    else max((1 - _frac(d["t1"])) * d["a"], (1 - _frac(d["t2"])) * d["b"])
)

FORMULAS["pcm_time_ratio"] = lambda d: fmt(
    F(2, 3) * d["inlet"] * _frac(d["outlet_ratio"]) / (_frac(d["outlet_ratio"]) - 1)
)

FORMULAS["pcm_fill_empty_cycle"] = lambda d: fmt(
    d["fill_hours"]
    + d["empty_hours"]
    + (1 - F(d["fill_hours"], d["inlet"]) + F(d["empty_hours"], d["outlet"]))
    * d["inlet"]
)

FORMULAS["pcm_parallel_inlets"] = lambda d: fmt(
    d["n"] + (1 - F(d["n"] * (d["n"] + 1), 2 * d["a"])) * F(d["a"], d["n"])
)

FORMULAS["pcm_leak_fraction"] = lambda d: fmt(
    F(d["inlet"], 2) + F(d["inlet"], 2) / (1 - _frac(d["leak_frac"]))
)

FORMULAS["pcm_tap_sizes"] = lambda d: fmt(
    d["base"] - sum(a * t for a, t in zip(d["areas"], d["times"]))
)

FORMULAS["pcm_start_delay"] = lambda d: fmt(
    d["delay"] + (d["a"] - d["delay"]) * d["b"] / (d["a"] + d["b"])
)

FORMULAS["pcm_overflow"] = lambda d: fmt(
    F(
        d["inlet"] * d["outlet"] * (d["capacity"] - d["start"]),
        d["capacity"] * (d["outlet"] - d["inlet"]),
    )
)

FORMULAS["pcm_metered_fill"] = lambda d: money(
    F(4 * d["capacity"] * d["rate_per_litre"], 3)
)

FORMULAS["pcm_reverse_outlet"] = lambda d: fmt(
    F(d["inlet"] * d["net"], d["net"] - d["inlet"])
)

FORMULAS["pcm_alternate_three"] = lambda d: fmt(
    _alternate_three(d["a"], d["b"], d["c"], d["hours"])
)

FORMULAS["pcm_pump_leak"] = lambda d: fmt(
    d["change_after"]
    + (
        1
        - d["change_after"] * (F(1, d["pump"]) - F(1, d["leak"]))
    )
    / (F(1, d["pump"]) - F(1, d["new_leak"]))
)

FORMULAS["pcm_drain_refill"] = lambda d: fmt(
    (1 - _frac(d["frac"])) * d["drain"]
    + (F(3, 4) - _frac(d["frac"])) * d["refill"]
)

FORMULAS["pcm_capacity_ratio"] = lambda d: fmt(
    F(d["time_a"] * d["ratio_a"], 2 * (d["ratio_a"] + d["ratio_b"]))
    + F(d["time_a"] * d["ratio_a"], 2 * d["ratio_b"])
)
