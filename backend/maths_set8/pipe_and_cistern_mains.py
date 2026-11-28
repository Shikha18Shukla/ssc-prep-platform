# -*- coding: utf-8 -*-
"""Pipe and Cistern (Mains) - 24 HARD original families, five variants each."""

from __future__ import annotations

from .common import (
    F,
    build_specs,
    data,
    dec,
    fmt,
    make_family,
    money,
    near_money,
    near_num,
    near_pct,
    pct,
    q,
    ratio,
    ratio_distractors,
)

SOURCE_PDF = "Pipe and Cistern Mains 01 _Class Notes.pdf"
PAGES = {
    1: f"{SOURCE_PDF}, pp. 2-4",
    2: f"{SOURCE_PDF}, pp. 5-8",
    3: f"{SOURCE_PDF}, pp. 9-12",
    4: f"{SOURCE_PDF}, pp. 13-14",
}


def _frac(value):
    """Parse a JSON-safe fraction string (or a number) exactly."""
    if isinstance(value, str):
        if "/" in value:
            num, den = value.split("/", 1)
            return F(int(num), int(den))
        return F(int(value))
    return F(value)


def _alt_finish(start, x, y):
    """Exact hours for x,y alternating one-hour turns (x next) to finish."""
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
    """Elapsed hours for an on/off inlet to fill an empty tank exactly."""
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
    """A,B alternate for ``hours`` hours, then A closes and B continues."""
    filled = F(0)
    for hour in range(hours):
        pipe = a if hour % 2 == 0 else b
        before = filled
        filled += F(1, pipe)
        if filled >= 1:
            return F(hour) + (1 - before) * pipe
    return F(hours) + (1 - filled) * b


def _alternate_three(a, b, c, hours):
    """A,B,C one-hour turns; after ``hours`` C closes and A,B alternate."""
    filled = F(0)
    pipes = (a, b, c)
    for hour in range(hours):
        pipe = pipes[hour % 3]
        before = filled
        filled += F(1, pipe)
        if filled >= 1:
            return F(hour) + (1 - before) * pipe
    return F(hours) + _alt_finish(filled, a, b)


# 1. Two inlets, lead time then joint working.
pcm_two_inlets = make_family(
    "pcm_two_inlets",
    ("a", "b", "ask"),
    [(12, 18, "total"), (10, 15, "total"), (8, 12, "total"), (6, 9, "total"), (20, 30, "total")],
    lambda d: (
        data([("A alone", f"{d['a']} h"), ("B alone", f"{d['b']} h")])
        + " A runs alone for one-third of its solo filling time; then B joins and both run until the tank is full. Find the total elapsed hours."
    ),
    lambda d: F(d["a"], 3) + F(2 * d["a"] * d["b"], 3 * (d["a"] + d["b"])),
    lambda r, d: [
        F(d["a"] * d["b"], d["a"] + d["b"]),
        F(d["a"], 3) + F(2 * d["b"], 3),
        2 * r,
    ],
    lambda d, c: (
        f"A alone fills 1/3 of the tank in {fmt(F(d['a'], 3))} h. The remaining 2/3 at combined rate "
        f"(a+b)/(ab) takes {fmt(F(2 * d['a'] * d['b'], 3 * (d['a'] + d['b'])))} h, so the total is {c} h."
    ),
)


# 2. Inlet/outlet on a partly filled tank.
pcm_inlet_outlet = make_family(
    "pcm_inlet_outlet",
    ("a", "b", "ask"),
    [(12, 18, "fill"), (10, 15, "fill"), (8, 14, "fill"), (9, 15, "fill"), (14, 35, "fill")],
    lambda d: (
        data([("inlet", f"{d['a']} h"), ("outlet", f"{d['b']} h"), ("initial", "1/3 full")])
        + " An inlet and an outlet are opened together on a tank that is one-third full. Find the hours until the tank is full."
    ),
    lambda d: F(2 * d["a"] * d["b"], 3 * (d["b"] - d["a"])),
    lambda r, d: [
        F(d["a"] * d["b"], d["b"] - d["a"]),
        F(d["a"] * d["b"], d["a"] + d["b"]),
        2 * r,
    ],
    lambda d, c: (
        f"Net hourly rate is 1/{d['a']} - 1/{d['b']} = {fmt(F(d['b'] - d['a'], d['a'] * d['b']))}. "
        f"Only 2/3 of the tank is needed, so time = (2/3)/net rate = {c} h."
    ),
)


# 3. Alternating pipes with a mid-process shut-off.
pcm_alternating_pipes = make_family(
    "pcm_alternating_pipes",
    ("a", "b", "hours", "ask"),
    [(12, 18, 4, "total"), (10, 15, 3, "total"), (8, 12, 5, "total"), (9, 15, 2, "total"), (20, 30, 6, "total")],
    lambda d: (
        data([("A", f"{d['a']} h"), ("B", f"{d['b']} h"), ("switch after", f"{d['hours']} h")])
        + " A and B are opened alternately for one hour each, A first. After the stated hours A is closed and B alone continues. Find the total hours to fill."
    ),
    lambda d: _alternating_then_b(d["a"], d["b"], d["hours"]),
    lambda r, d: [
        F(d["hours"]) + F(d["a"] + d["b"], 2),
        F(d["hours"]) + (1 - F(d["hours"], 2 * d["a"])) * d["a"],
        2 * r,
    ],
    lambda d, c: (
        f"In {d['hours']} alternating hours the tank gains "
        f"{fmt(F((d['hours'] + 1) // 2, d['a']) + F(d['hours'] // 2, d['b']))}; "
        f"B alone then supplies the balance, giving a total of {c} h."
    ),
)


# 4. Leak begins at half fill.
pcm_leakage = make_family(
    "pcm_leakage",
    ("inlet", "leak", "ask"),
    [(12, 24, "time"), (10, 15, "time"), (8, 12, "time"), (9, 18, "time"), (14, 21, "time")],
    lambda d: (
        data([("inlet", f"{d['inlet']} h"), ("leak", f"{d['leak']} h")])
        + " An inlet fills an empty tank; when the tank is half full a leak starts, which alone would empty a full tank in the leak time. Find the total hours to fill."
    ),
    lambda d: F(d["inlet"], 2) + F(d["inlet"] * d["leak"], 2 * (d["leak"] - d["inlet"])),
    lambda r, d: [
        F(d["inlet"] * d["leak"], d["leak"] - d["inlet"]),
        F(d["inlet"], 2) + F(d["leak"], 2),
        2 * r,
    ],
    lambda d, c: (
        f"The first half takes {fmt(F(d['inlet'], 2))} h. Thereafter net rate is 1/{d['inlet']} - 1/{d['leak']}, "
        f"so the second half takes {fmt(F(d['inlet'] * d['leak'], 2 * (d['leak'] - d['inlet'])))} h; total {c} h."
    ),
)


# 5. Partial fill, outlet closed midway, inlet refills.
pcm_partial_fill = make_family(
    "pcm_partial_fill",
    ("inlet", "outlet", "frac", "ask"),
    [
        (12, 8, "1/2", "total"),
        (10, 6, "2/3", "total"),
        (15, 10, "3/5", "total"),
        (18, 12, "1/3", "total"),
        (9, 6, "3/4", "total"),
    ],
    lambda d: (
        data([("inlet", f"{d['inlet']} h"), ("outlet", f"{d['outlet']} h"), ("initial", f"{d['frac']} full")])
        + " Both pipes run together until the tank holds half of its initial content; then the outlet is closed and the inlet alone fills the tank. Find the total hours."
    ),
    lambda d: (
        _frac(d["frac"]) * d["inlet"] * d["outlet"] / (2 * (d["inlet"] - d["outlet"]))
        + (1 - _frac(d["frac"]) / 2) * d["inlet"]
    ),
    lambda r, d: [
        _frac(d["frac"]) * d["inlet"] * d["outlet"] / (d["inlet"] - d["outlet"]),
        d["inlet"] * _frac(d["frac"]),
        2 * r,
    ],
    lambda d, c: (
        f"Starting at {d['frac']}, half of that amount is removed at net rate 1/{d['outlet']} - 1/{d['inlet']}; "
        f"then the inlet alone fills the remaining {fmt(1 - _frac(d['frac']) / 2)}. Total = {c} h."
    ),
)


# 6. Three pipes opened in sequence.
pcm_three_sequence = make_family(
    "pcm_three_sequence",
    ("a", "b", "c", "after_a", "after_b", "ask"),
    [
        (18, 12, 9, 3, 2, "total"),
        (24, 16, 12, 4, 3, "total"),
        (20, 15, 10, 2, 3, "total"),
        (30, 20, 15, 5, 4, "total"),
        (12, 8, 6, 1, 2, "total"),
    ],
    lambda d: (
        data([
            ("A", f"{d['a']} h"), ("B", f"{d['b']} h"), ("C", f"{d['c']} h"),
            ("A alone", f"{d['after_a']} h"), ("A+B", f"{d['after_b']} h"),
        ])
        + " A works alone, then B joins, then C joins and all three finish. Find the total hours to fill."
    ),
    lambda d: (
        d["after_a"] + d["after_b"]
        + (1 - F(d["after_a"], d["a"]) - d["after_b"] * (F(1, d["a"]) + F(1, d["b"])))
        / (F(1, d["a"]) + F(1, d["b"]) + F(1, d["c"]))
    ),
    lambda r, d: [
        F(d["after_a"] + d["after_b"]),
        F(1, F(1, d["a"]) + F(1, d["b"]) + F(1, d["c"])),
        2 * r,
    ],
    lambda d, c: (
        f"After A alone for {d['after_a']} h and A+B for {d['after_b']} h, the balance is filled at rate "
        f"1/{d['a']}+1/{d['b']}+1/{d['c']}; the elapsed total is {c} h."
    ),
)


# 7. Flow capacity increases at half full.
pcm_capacity_change = make_family(
    "pcm_capacity_change",
    ("inlet", "base", "extra", "ask"),
    [
        (12, 120, 20, "time"),
        (12, 120, 40, "time"),
        (18, 180, 30, "time"),
        (15, 150, 50, "time"),
        (10, 100, 25, "time"),
    ],
    lambda d: (
        data([("capacity", f"{d['base']} L"), ("solo fill", f"{d['inlet']} h"), ("already", f"{d['extra']} L")])
        + f" A pipe fills a {d['base']}-litre tank in {d['inlet']} hours. The tank already holds {d['extra']} litres; at half capacity the flow is raised by {d['extra']} litres/hour. Find the total hours to fill."
    ),
    lambda d: (
        F(d["inlet"]) * (F(d["base"], 2) - d["extra"]) / d["base"]
        + F(d["base"], 2) / (F(d["base"], d["inlet"]) + d["extra"])
    ),
    lambda r, d: [
        F(d["inlet"]) * (1 - F(d["extra"], d["base"])),
        F(d["base"], 2) / F(d["base"], d["inlet"]),
        2 * r,
    ],
    lambda d, c: (
        f"Original flow is {fmt(F(d['base'], d['inlet']))} L/h. Reaching half capacity takes "
        f"{fmt(F(d['inlet']) * (F(d['base'], 2) - d['extra']) / d['base'])} h; the last half at the "
        f"raised flow takes {fmt(F(d['base'], 2) / (F(d['base'], d['inlet']) + d['extra']))} h. Total {c} h."
    ),
)


# 8. Efficiency drops after a fixed run.
pcm_efficiency_drop = make_family(
    "pcm_efficiency_drop",
    ("inlet", "rate", "drop", "after", "ask"),
    [
        (12, 15, 25, 3, "total"),
        (10, 18, 20, 2, "total"),
        (15, 12, 40, 5, "total"),
        (8, 20, 25, 2, "total"),
        (18, 10, 10, 6, "total"),
    ],
    lambda d: (
        data([
            ("full fill", f"{d['inlet']} h"), ("flow", f"{d['rate']} L/h"),
            ("drop", f"{d['drop']}%"), ("full-flow run", f"{d['after']} h"),
        ])
        + " An inlet at full efficiency fills the tank in the full-fill time; after the full-flow run its efficiency falls by the stated percent. Find the total hours to fill."
    ),
    lambda d: d["after"] + (1 - F(d["after"], d["inlet"])) * F(d["inlet"] * 100, 100 - d["drop"]),
    lambda r, d: [
        d["inlet"] * F(100, 100 - d["drop"]),
        d["after"] + d["inlet"] - d["after"],
        2 * r,
    ],
    lambda d, c: (
        f"Full-flow work leaves {fmt(1 - F(d['after'], d['inlet']))} of the tank. With efficiency cut by "
        f"{d['drop']}%, a full tank would take {fmt(F(d['inlet'] * 100, 100 - d['drop']))} h, so the balance takes "
        f"its proportional share; total {c} h."
    ),
)


# 9. Waste tap opens at one-third fill.
pcm_tank_waste = make_family(
    "pcm_tank_waste",
    ("inlet", "waste", "capacity", "ask"),
    [
        (12, 4, 120, "time"),
        (15, 3, 180, "time"),
        (20, 2, 240, "time"),
        (10, 2, 100, "time"),
        (10, 5, 150, "time"),
    ],
    lambda d: (
        data([
            ("capacity", f"{d['capacity']} L"), ("solo fill", f"{d['inlet']} h"),
            ("waste", f"{d['waste']} L/h"),
        ])
        + " An inlet fills the tank in the solo-fill time; once the tank is one-third full a waste tap drains litres per hour. Find the total hours to fill."
    ),
    lambda d: F(d["inlet"], 3) + F(2 * d["capacity"], 3 * (F(d["capacity"], d["inlet"]) - d["waste"])),
    lambda r, d: [
        F(d["inlet"]),
        F(d["capacity"], F(d["capacity"], d["inlet"]) - d["waste"]),
        2 * r,
    ],
    lambda d, c: (
        f"The first third takes {fmt(F(d['inlet'], 3))} h. Inlet flow is {fmt(F(d['capacity'], d['inlet']))} L/h, "
        f"so after waste begins the net is {fmt(F(d['capacity'], d['inlet']) - d['waste'])} L/h; total {c} h."
    ),
)


# 10. Intermittent supply, exact hour-by-hour accounting.
pcm_intermittent = make_family(
    "pcm_intermittent",
    ("inlet", "run", "cycle", "ask"),
    [
        (12, 2, 3, "elapsed"),
        (10, 2, 5, "elapsed"),
        (9, 2, 4, "elapsed"),
        (15, 2, 3, "elapsed"),
        (8, 3, 5, "elapsed"),
    ],
    lambda d: (
        data([("solo fill", f"{d['inlet']} h"), ("on", f"{d['run']} h"), ("cycle", f"{d['cycle']} h")])
        + " The inlet runs for the on duration and stays closed for the rest of each cycle, starting with an on period on an empty tank. Find the elapsed hours until it is full."
    ),
    lambda d: _intermittent(d["inlet"], d["run"], d["cycle"]),
    lambda r, d: [
        F(d["inlet"]),
        F(d["run"] * d["cycle"]),
        2 * r,
    ],
    lambda d, c: (
        f"Each cycle contributes {fmt(F(d['run'], d['inlet']))} of the tank over {d['cycle']} elapsed hours. "
        f"Tracking the on-hours exactly gives {c} elapsed hours."
    ),
)


# 11. Two tanks with a catch-up or a both-full question.
pcm_two_tanks = make_family(
    "pcm_two_tanks",
    ("a", "b", "t1", "t2", "ask"),
    [
        (8, 12, "1/4", "1/2", "catch_up"),
        (10, 15, "1/5", "2/5", "both_full"),
        (6, 9, "1/6", "1/3", "catch_up"),
        (12, 18, "1/3", "5/6", "both_full"),
        (9, 12, "1/9", "1/3", "catch_up"),
    ],
    lambda d: (
        data([
            ("A solo", f"{d['a']} h"), ("B solo", f"{d['b']} h"),
            ("A initial", f"{d['t1']} full"), ("B initial", f"{d['t2']} full"),
            ("question", d["ask"]),
        ])
        + (
            " Both inlets are opened. Find the hours until the two tanks are equally full."
            if d["ask"] == "catch_up"
            else " Both inlets are opened. Find the hours until both tanks are full."
        )
    ),
    lambda d: (
        (_frac(d["t2"]) - _frac(d["t1"])) / (F(1, d["a"]) - F(1, d["b"]))
        if d["ask"] == "catch_up"
        else max((1 - _frac(d["t1"])) * d["a"], (1 - _frac(d["t2"])) * d["b"])
    ),
    lambda r, d: [
        (1 - _frac(d["t1"])) * d["a"],
        (1 - _frac(d["t2"])) * d["b"],
        2 * r,
    ],
    lambda d, c: (
        f"A gains at 1/{d['a']} per hour and B at 1/{d['b']} per hour from initial levels {d['t1']} and {d['t2']}. "
        f"The required comparison gives {c} h."
    ),
)


# 12. Outlet time expressed as a multiple of inlet time.
pcm_time_ratio = make_family(
    "pcm_time_ratio",
    ("inlet", "outlet_ratio", "ask"),
    [
        (12, "3/2", "fill"),
        (10, "5/4", "fill"),
        (8, "2", "fill"),
        (15, "5/3", "fill"),
        (9, "4/3", "fill"),
    ],
    lambda d: (
        data([("inlet", f"{d['inlet']} h"), ("outlet time", f"{d['outlet_ratio']} x inlet"), ("initial", "1/3 full")])
        + " A tank is one-third full. The inlet and outlet are opened together; find the hours until the tank is full."
    ),
    lambda d: F(2, 3) * d["inlet"] * _frac(d["outlet_ratio"]) / (_frac(d["outlet_ratio"]) - 1),
    lambda r, d: [
        F(2, 3) * d["inlet"] * _frac(d["outlet_ratio"]),
        d["inlet"] * _frac(d["outlet_ratio"]),
        2 * r,
    ],
    lambda d, c: (
        f"Outlet alone takes {fmt(d['inlet'] * _frac(d['outlet_ratio']))} h. Net fill rate is "
        f"1/{d['inlet']} - 1/{fmt(d['inlet'] * _frac(d['outlet_ratio']))}; filling the missing 2/3 takes {c} h."
    ),
)


# 13. Inlet, outlet, then inlet again.
pcm_fill_empty_cycle = make_family(
    "pcm_fill_empty_cycle",
    ("inlet", "outlet", "fill_hours", "empty_hours", "ask"),
    [
        (12, 18, 6, 3, "total"),
        (10, 15, 4, 3, "total"),
        (8, 12, 3, 2, "total"),
        (9, 6, 4, 2, "total"),
        (15, 10, 8, 3, "total"),
    ],
    lambda d: (
        data([
            ("inlet", f"{d['inlet']} h"), ("outlet", f"{d['outlet']} h"),
            ("inlet first", f"{d['fill_hours']} h"), ("outlet next", f"{d['empty_hours']} h"),
        ])
        + " Starting empty, the inlet runs for the first stated hours, the outlet alone runs for the next stated hours, and then the inlet alone finishes. Find the total hours."
    ),
    lambda d: (
        d["fill_hours"] + d["empty_hours"]
        + (1 - F(d["fill_hours"], d["inlet"]) + F(d["empty_hours"], d["outlet"])) * d["inlet"]
    ),
    lambda r, d: [
        d["fill_hours"] + d["empty_hours"],
        (1 - F(d["fill_hours"], d["inlet"])) * d["inlet"],
        2 * r,
    ],
    lambda d, c: (
        f"After filling {fmt(F(d['fill_hours'], d['inlet']))} and draining {fmt(F(d['empty_hours'], d['outlet']))}, "
        f"the remaining {fmt(1 - F(d['fill_hours'], d['inlet']) + F(d['empty_hours'], d['outlet']))} is filled by the inlet; total {c} h."
    ),
)


# 14. Identical inlets opened one per hour.
pcm_parallel_inlets = make_family(
    "pcm_parallel_inlets",
    ("a", "n", "ask"),
    [(30, 4, "total"), (42, 5, "total"), (24, 3, "total"), (40, 6, "total"), (56, 7, "total")],
    lambda d: (
        data([("solo fill", f"{d['a']} h"), ("inlets", d["n"]), ("gap", "1 h")])
        + " One inlet is opened at the start and one more at the end of every hour until all are open. Find the elapsed hours until an empty tank is full."
    ),
    lambda d: (
        d["n"] + (1 - F(d["n"] * (d["n"] + 1), 2 * d["a"])) * F(d["a"], d["n"])
    ),
    lambda r, d: [
        F(d["a"], d["n"]),
        d["n"],
        2 * r,
    ],
    lambda d, c: (
        f"During the first {d['n']} hours the tank gains 1+2+...+{d['n']} = {d['n'] * (d['n'] + 1) // 2} "
        f"pipe-hours, i.e. {fmt(F(d['n'] * (d['n'] + 1), 2 * d['a']))} of the tank. All n pipes then finish it; total {c} h."
    ),
)


# 15. Leak equal to a fraction of the inlet flow.
pcm_leak_fraction = make_family(
    "pcm_leak_fraction",
    ("inlet", "leak_frac", "ask"),
    [
        (12, "1/3", "time"),
        (10, "1/4", "time"),
        (8, "2/5", "time"),
        (15, "1/5", "time"),
        (18, "3/10", "time"),
    ],
    lambda d: (
        data([("inlet", f"{d['inlet']} h"), ("leak", f"{d['leak_frac']} of inflow")])
        + " An inlet starts filling an empty tank. When the tank is half full a leak develops that loses the stated fraction of the inlet flow. Find the total hours to fill."
    ),
    lambda d: F(d["inlet"], 2) + F(d["inlet"], 2) / (1 - _frac(d["leak_frac"])),
    lambda r, d: [
        d["inlet"],
        F(d["inlet"], 2) * (1 + _frac(d["leak_frac"])),
        2 * r,
    ],
    lambda d, c: (
        f"Half full takes {fmt(F(d['inlet'], 2))} h. The leak leaves a fraction {fmt(1 - _frac(d['leak_frac']))} "
        f"of the inflow effective, so the other half takes {fmt(F(d['inlet'], 2) / (1 - _frac(d['leak_frac'])))} h; total {c} h."
    ),
)


# 16. Taps of different cross-sections used one after another.
pcm_tap_sizes = make_family(
    "pcm_tap_sizes",
    ("base", "areas", "times", "ask"),
    [
        (24, [1, 2], [4, 3], "finish_time"),
        (30, [1, 2, 3], [3, 2, 1], "finish_time"),
        (20, [2, 3], [2, 2], "finish_time"),
        (36, [1, 1, 2], [6, 4, 3], "finish_time"),
        (48, [3, 1, 2], [4, 5, 3], "finish_time"),
    ],
    lambda d: (
        data([
            ("unit tap", f"{d['base']} h"), ("areas", ",".join(str(x) for x in d["areas"])),
            ("durations", ",".join(str(x) for x in d["times"]) + " h"),
        ])
        + " Taps whose flow rates are proportional to their areas are opened one at a time for the listed durations; then a unit-area tap alone finishes the tank. Find those extra hours."
    ),
    lambda d: d["base"] - sum(a * t for a, t in zip(d["areas"], d["times"])),
    lambda r, d: [
        sum(a * t for a, t in zip(d["areas"], d["times"])),
        d["base"] // 2,
        2 * r,
    ],
    lambda d, c: (
        f"Pipe-hours delivered are {sum(a * t for a, t in zip(d['areas'], d['times']))} against a "
        f"unit-tap requirement of {d['base']} pipe-hours, so the finishing tap needs {c} h."
    ),
)


# 17. Second inlet starts late.
pcm_start_delay = make_family(
    "pcm_start_delay",
    ("a", "b", "delay", "ask"),
    [
        (12, 18, 3, "total"),
        (10, 15, 2, "total"),
        (8, 12, 1, "total"),
        (9, 6, 2, "total"),
        (15, 10, 5, "total"),
    ],
    lambda d: (
        data([("A", f"{d['a']} h"), ("B", f"{d['b']} h"), ("B delay", f"{d['delay']} h")])
        + " A starts on an empty tank at once; B starts after the stated delay. Find the hours from A's start until the tank is full."
    ),
    lambda d: d["delay"] + (d["a"] - d["delay"]) * d["b"] / (d["a"] + d["b"]),
    lambda r, d: [
        F(d["a"] * d["b"], d["a"] + d["b"]),
        d["a"] + d["b"],
        2 * r,
    ],
    lambda d, c: (
        f"A alone fills {fmt(F(d['delay'], d['a']))} in {d['delay']} h. The balance is then filled at "
        f"1/{d['a']}+1/{d['b']}, making the total {c} h."
    ),
)


# 18. Overflow with a pre-existing level.
pcm_overflow = make_family(
    "pcm_overflow",
    ("inlet", "outlet", "capacity", "start", "ask"),
    [
        (12, 18, 120, 30, "overflow"),
        (15, 20, 180, 45, "overflow"),
        (16, 24, 240, 60, "overflow"),
        (10, 15, 100, 20, "overflow"),
        (12, 20, 150, 30, "overflow"),
    ],
    lambda d: (
        data([
            ("capacity", f"{d['capacity']} L"), ("inlet", f"{d['inlet']} h"),
            ("outlet", f"{d['outlet']} h"), ("initial", f"{d['start']} L"),
        ])
        + " Both pipes are opened on a tank holding the stated initial litres. Find the hours until the tank overflows."
    ),
    lambda d: F(d["inlet"] * d["outlet"] * (d["capacity"] - d["start"]), d["capacity"] * (d["outlet"] - d["inlet"])),
    lambda r, d: [
        d["inlet"] * (d["capacity"] - d["start"]) / d["capacity"],
        d["outlet"] * (d["capacity"] - d["start"]) / d["capacity"],
        2 * r,
    ],
    lambda d, c: (
        f"Inlet flow is {fmt(F(d['capacity'], d['inlet']))} L/h and outlet flow is "
        f"{fmt(F(d['capacity'], d['outlet']))} L/h. The net fills the missing {d['capacity'] - d['start']} L in {c} h."
    ),
)


# 19. Metered tariff changes part-way through the fill.
pcm_metered_fill = make_family(
    "pcm_metered_fill",
    ("inlet", "capacity", "rate_per_litre", "ask"),
    [
        (12, 120, 3, "cost"),
        (15, 180, 4, "cost"),
        (10, 150, 2, "cost"),
        (20, 240, 5, "cost"),
        (9, 90, 7, "cost"),
    ],
    lambda d: (
        data([
            ("capacity", f"{d['capacity']} L"), ("solo fill", f"{d['inlet']} h"),
            ("meter rate", money(d["rate_per_litre"]) + "/L"),
            ("surcharge", "1.5x after one-third of fill time"),
        ])
        + " Find the total metering cost of filling the tank."
    ),
    lambda d: money(F(4 * d["capacity"] * d["rate_per_litre"], 3)),
    lambda r, d: [
        money(F(d["capacity"] * d["rate_per_litre"])),
        money(F(3 * d["capacity"] * d["rate_per_litre"], 2)),
        money(F(2 * d["capacity"] * d["rate_per_litre"])),
    ],
    lambda d, c: (
        f"The first {fmt(F(d['capacity'], 3))} L is charged at {money(d['rate_per_litre'])}/L and the remaining "
        f"{fmt(F(2 * d['capacity'], 3))} L at 1.5 times that rate; total cost {c}."
    ),
)


# 20. Recover the outlet time from the observed net fill time.
pcm_reverse_outlet = make_family(
    "pcm_reverse_outlet",
    ("inlet", "net", "ask"),
    [(12, 18, "outlet_time"), (10, 15, "outlet_time"), (8, 12, "outlet_time"), (9, 15, "outlet_time"), (14, 21, "outlet_time")],
    lambda d: (
        data([("inlet alone", f"{d['inlet']} h"), ("inlet with outlet", f"{d['net']} h")])
        + " An inlet fills a tank in the inlet-alone time; with an outlet also open the tank fills in the slower observed time. Find the hours for the outlet alone to empty a full tank."
    ),
    lambda d: F(d["inlet"] * d["net"], d["net"] - d["inlet"]),
    lambda r, d: [
        F(d["net"] - d["inlet"]),
        d["inlet"] + d["net"],
        2 * r,
    ],
    lambda d, c: (
        f"The outlet rate is 1/{d['inlet']} - 1/{d['net']} = {fmt(F(d['net'] - d['inlet'], d['inlet'] * d['net']))}; "
        f"its emptying time is the reciprocal, {c} h."
    ),
)


# 21. Three-way alternation followed by a two-way alternation.
pcm_alternate_three = make_family(
    "pcm_alternate_three",
    ("a", "b", "c", "hours", "ask"),
    [
        (18, 12, 9, 3, "total"),
        (24, 16, 12, 3, "total"),
        (20, 15, 10, 6, "total"),
        (12, 8, 6, 3, "total"),
        (30, 20, 15, 6, "total"),
    ],
    lambda d: (
        data([
            ("A", f"{d['a']} h"), ("B", f"{d['b']} h"), ("C", f"{d['c']} h"),
            ("switch after", f"{d['hours']} h"),
        ])
        + " A, B and C take one-hour turns in that order. After the stated hours C is closed and A,B alternate one-hour turns with A taking the next turn. Find total hours to fill."
    ),
    lambda d: _alternate_three(d["a"], d["b"], d["c"], d["hours"]),
    lambda r, d: [
        F(d["hours"]),
        F(d["a"] + d["b"] + d["c"], 3),
        2 * r,
    ],
    lambda d, c: (
        f"The first {d['hours']} hours contribute one-hour shares of A,B,C; afterwards the balance is handled by "
        f"alternating A and B. Exact hour-slot accounting gives {c} h."
    ),
)


# 22. Leak changes part-way through pumping.
pcm_pump_leak = make_family(
    "pcm_pump_leak",
    ("pump", "leak", "change_after", "new_leak", "ask"),
    [
        (12, 24, 4, 18, "total"),
        (10, 20, 3, 15, "total"),
        (15, 30, 5, 20, "total"),
        (8, 16, 2, 12, "total"),
        (18, 36, 6, 27, "total"),
    ],
    lambda d: (
        data([
            ("pump", f"{d['pump']} h"), ("old leak", f"{d['leak']} h"),
            ("change after", f"{d['change_after']} h"), ("new leak", f"{d['new_leak']} h"),
        ])
        + " A pump and a leak run together; at the change time the old leak is replaced by the new leak. Find total hours to fill the tank."
    ),
    lambda d: (
        d["change_after"]
        + (1 - d["change_after"] * (F(1, d["pump"]) - F(1, d["leak"])))
        / (F(1, d["pump"]) - F(1, d["new_leak"]))
    ),
    lambda r, d: [
        d["change_after"] + F(d["pump"] * d["new_leak"], d["new_leak"] - d["pump"]),
        F(d["pump"] * d["leak"], d["leak"] - d["pump"]),
        2 * r,
    ],
    lambda d, c: (
        f"For the first {d['change_after']} h net rate is 1/{d['pump']} - 1/{d['leak']}; afterwards it is "
        f"1/{d['pump']} - 1/{d['new_leak']}. The exact remaining fill gives {c} h."
    ),
)


# 23. Drain to a fraction, then refill to three-fourths.
pcm_drain_refill = make_family(
    "pcm_drain_refill",
    ("drain", "refill", "frac", "ask"),
    [
        (12, 10, "1/4", "time"),
        (10, 15, "1/3", "time"),
        (8, 12, "1/2", "time"),
        (9, 18, "1/6", "time"),
        (15, 20, "2/5", "time"),
    ],
    lambda d: (
        data([("drain", f"{d['drain']} h"), ("refill", f"{d['refill']} h"), ("stop at", f"{d['frac']} full")])
        + " A full tank is drained until only the stated fraction remains; the drain is closed and the refill pipe runs until the tank is three-fourths full. Find total elapsed hours."
    ),
    lambda d: (1 - _frac(d["frac"])) * d["drain"] + (F(3, 4) - _frac(d["frac"])) * d["refill"],
    lambda r, d: [
        _frac(d["frac"]) * d["drain"],
        (1 - _frac(d["frac"])) * d["refill"],
        2 * r,
    ],
    lambda d, c: (
        f"Draining from full to {d['frac']} takes {fmt((1 - _frac(d['frac'])) * d['drain'])} h; refilling from "
        f"{d['frac']} to 3/4 takes {fmt((F(3, 4) - _frac(d['frac'])) * d['refill'])} h; total {c} h."
    ),
)


# 24. Rates given as a ratio; staged half-and-half working.
pcm_capacity_ratio = make_family(
    "pcm_capacity_ratio",
    ("ratio_a", "ratio_b", "time_a", "ask"),
    [(2, 3, 15, "total"), (3, 2, 12, "total"), (1, 2, 18, "total"), (3, 4, 20, "total"), (2, 5, 21, "total")],
    lambda d: (
        data([
            ("rate ratio A:B", f"{d['ratio_a']}:{d['ratio_b']}"),
            ("A alone", f"{d['time_a']} h"),
        ])
        + " Both pipes fill the tank together until it is half full; then A is closed and B alone finishes. Find the total hours."
    ),
    lambda d: (
        F(d["time_a"] * d["ratio_a"], 2 * (d["ratio_a"] + d["ratio_b"]))
        + F(d["time_a"] * d["ratio_a"], 2 * d["ratio_b"])
    ),
    lambda r, d: [
        F(d["time_a"], 2),
        F(d["time_a"] * d["ratio_a"], d["ratio_b"]),
        2 * r,
    ],
    lambda d, c: (
        f"A's rate is 1/{d['time_a']}; B's rate is {d['ratio_b']}/{d['ratio_a']} of A's. The first half takes "
        f"{fmt(F(d['time_a'] * d['ratio_a'], 2 * (d['ratio_a'] + d['ratio_b'])))} h and B's half takes "
        f"{fmt(F(d['time_a'] * d['ratio_a'], 2 * d['ratio_b']))} h; total {c} h."
    ),
)


FAMILIES = [
    pcm_two_inlets,
    pcm_inlet_outlet,
    pcm_alternating_pipes,
    pcm_leakage,
    pcm_partial_fill,
    pcm_three_sequence,
    pcm_capacity_change,
    pcm_efficiency_drop,
    pcm_tank_waste,
    pcm_intermittent,
    pcm_two_tanks,
    pcm_time_ratio,
    pcm_fill_empty_cycle,
    pcm_parallel_inlets,
    pcm_leak_fraction,
    pcm_tap_sizes,
    pcm_start_delay,
    pcm_overflow,
    pcm_metered_fill,
    pcm_reverse_outlet,
    pcm_alternate_three,
    pcm_pump_leak,
    pcm_drain_refill,
    pcm_capacity_ratio,
]


def build_pipe_and_cistern_mains():
    return build_specs(FAMILIES, mains=True)
