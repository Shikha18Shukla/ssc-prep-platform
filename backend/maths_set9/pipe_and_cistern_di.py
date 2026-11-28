# -*- coding: utf-8 -*-
"""Pipe and Cistern – Data Interpretation: 24 Prelims-level data families."""

from __future__ import annotations

from .common import F, build_specs, data, ef, near_pct, ratio_distractors

SOURCE_PDF = "Pipe and Cistern Data Interpretation 01  Class Notes.pdf"
PAGES = {1: SOURCE_PDF, 2: SOURCE_PDF, 3: SOURCE_PDF, 4: SOURCE_PDF}


def R2(a, b):
    return [(a + 2 * i, b + 3 * i, i + 1) for i in range(5)]


def R1(a):
    return [(a + 3 * i, i + 1) for i in range(5)]


def R3(a, b, c):
    return [(a + i, b + i, c, i + 1) for i in range(5)]


FAMILIES = [
    ef("pdi_flow_share", ("a", "b", "q"), R2(12, 18),
       "F(1,a)/(F(1,a)+F(1,b))*100",
       lambda d: data([("Case", d["q"]), ("A alone", f"{d['a']} h"), ("B alone", f"{d['b']} h")])
       + " What percentage of the combined filling work is done by pipe A?",
       "A's share is (1/{a}) / (1/{a} + 1/{b}) of the whole work, which is {c}.",
       unit="%", distract=lambda c, d: near_pct(c.rstrip('%'))),
    ef("pdi_rate_table", ("a", "b", "q"), R2(10, 15),
       "F(a*b,a+b)",
       lambda d: data([("Case", d["q"]), ("A alone", f"{d['a']} h"), ("B alone", f"{d['b']} h")])
       + " How many hours do both pipes take together to fill the tank?",
       "Combined rate is 1/{a} + 1/{b}, so the time is {c} hours.", unit=" h"),
    ef("pdi_two_pipe_fill", ("a", "b", "q"), R2(8, 12),
       "F(1, F(1,a)+F(1,b))",
       lambda d: data([("Case", d["q"]), ("inlet A", f"{d['a']} h"), ("inlet B", f"{d['b']} h")])
       + " Find the fraction of the tank filled in one hour when both inlets are open.",
       "One-hour combined work is 1/{a} + 1/{b} = {c} of the tank.", step=F(1, 10)),
    ef("pdi_leak_effect", ("a", "b", "q"), R2(12, 24),
       "F(a*b,b-a)",
       lambda d: data([("Case", d["q"]), ("inlet", f"{d['a']} h"), ("leak", f"{d['b']} h")])
       + " With the inlet and leak open together, how long does an empty tank take to fill?",
       "Net hourly work is 1/{a} - 1/{b}; its reciprocal is {c} hours.", unit=" h"),
    ef("pdi_capacity_ratio", ("a", "b", "q"), R2(9, 15),
       "ratio(b,a)",
       lambda d: data([("Case", d["q"]), ("small tank", f"{d['a']} L"), ("large tank", f"{d['b']} L")])
       + " What is the ratio of the large tank's capacity to the small tank's capacity?",
       "Comparing the stated capacities gives {b}:{a}, written as {c}.",
       distract=lambda c, d: ratio_distractors(c)),
    ef("pdi_cycle_output", ("a", "b", "q"), R2(20, 15),
       "F(b,a)",
       lambda d: data([("Case", d["q"]), ("pipe A output", f"{d['a']} L/min"), ("pipe B output", f"{d['b']} L/min")])
       + " How many minutes of A's output equal one minute of B's output?",
       "Equating output gives time = {b}/{a} = {c} minutes.", unit=" min"),
    ef("pdi_cost_fill", ("a", "b", "q"), R2(12, 360),
       "F(b,F(1,a)+1)",
       lambda d: data([("Case", d["q"]), ("tank capacity", f"{d['a']} L"), ("cost per litre", f"₹{d['b']/10}")])
       + " Find the total cost of filling the tank at the stated rate.",
       "Cost is {a} × ₹{b}/10 = ₹{c}.", step=50),
    ef("pdi_waste_loss", ("a", "b", "q"), R2(100, 8),
       "F(b,a)*100",
       lambda d: data([("Case", d["q"]), ("water supplied", f"{d['a']} L"), ("water wasted", f"{d['b']} L")])
       + " What percentage of the supplied water is wasted?",
       "Wasted percentage is {b}/{a} × 100 = {c}%.", unit="%",
       distract=lambda c, d: near_pct(c.rstrip('%'))),
    ef("pdi_alternate_hours", ("a", "b", "q"), R2(12, 18),
       "F(1,F(1,a)+F(1,b))*2",
       lambda d: data([("Case", d["q"]), ("A fills", f"{d['a']} h"), ("B fills", f"{d['b']} h")])
       + " A and B work alternately for one hour each. How many hours do they need for half the tank?",
       "In two hours they fill 1/{a} + 1/{b}; half the tank therefore takes {c} hours.", unit=" h"),
    ef("pdi_partial_level", ("a", "q"), R1(16),
       "F(3,4)*a",
       lambda d: data([("Case", d["q"]), ("full tank filling time", f"{d['a']} h")])
       + " How long does the inlet take to raise the tank from one-quarter to full?",
       "Three-quarters of {a} hours is needed, giving {c} hours.", unit=" h"),
    ef("pdi_combined_time", ("a", "b", "q"), R2(14, 21),
       "F(a*b,a+b)",
       lambda d: data([("Case", d["q"]), ("inlet A", f"{d['a']} h"), ("inlet B", f"{d['b']} h")])
       + " Find the time for both inlets to fill the tank together.",
       "The reciprocal of 1/{a} + 1/{b} is {c} hours.", unit=" h"),
    ef("pdi_efficiency", ("a", "b", "q"), R2(12, 25),
       "F(a*100,100-b)",
       lambda d: data([("Case", d["q"]), ("normal filling time", f"{d['a']} h"), ("efficiency drop", f"{d['b']}%")])
       + " After the stated efficiency drop, how many hours does the inlet take?",
       "Reduced efficiency is (100 - {b})% of normal, so time = {c} hours.", unit=" h"),
    ef("pdi_tank_dimensions", ("l", "w", "h", "q"), R3(8, 5, 3),
       "F(l*w*h,1000)",
       lambda d: data([("Case", d["q"]), ("length", f"{d['l']} m"), ("width", f"{d['w']} m"), ("height", f"{d['h']} m")])
       + " Find the tank capacity in kilolitres (1 m³ = 1000 L).",
       "Volume is {l} × {w} × {h} m³ = {c} kilolitres.", unit=" kL"),
    ef("pdi_multiple_tanks", ("a", "n", "q"), R2(12, 3),
       "F(a,n)",
       lambda d: data([("Case", d["q"]), ("one tank fill time", f"{d['a']} h"), ("identical tanks", str(d['n']))])
       + " One inlet fills each tank at the same rate. How long for all tanks if worked one after another?",
       "Sequential work is {n} × {a} hours = {c} hours.", unit=" h"),
    ef("pdi_inlet_outlet", ("a", "b", "q"), R2(10, 15),
       "F(a*b,b-a)",
       lambda d: data([("Case", d["q"]), ("inlet", f"{d['a']} h"), ("outlet", f"{d['b']} h")])
       + " Starting empty, how long until the tank is full with both pipes open?",
       "Net rate is 1/{a} - 1/{b}, so the fill time is {c} hours.", unit=" h"),
    ef("pdi_intermittent", ("a", "r", "q"), R2(12, 2),
       "F(a*3,r)",
       lambda d: data([("Case", d["q"]), ("inlet alone", f"{d['a']} h"), ("open hours per 3-hour cycle", str(d['r']))])
       + " The inlet follows the stated cycle. How many elapsed hours are needed to fill the tank?",
       "Each 3-hour cycle adds {r}/{a} of the tank; the required elapsed time is {c} hours.", unit=" h"),
    ef("pdi_flow_increase", ("a", "b", "q"), R2(12, 25),
       "F(a*100,100+b)",
       lambda d: data([("Case", d["q"]), ("old fill time", f"{d['a']} h"), ("flow increase", f"{d['b']}%")])
       + " After the stated flow increase, how long does filling take?",
       "New rate is (100 + {b})% of old, so time is {c} hours.", unit=" h"),
    ef("pdi_fill_levels", ("a", "q"), R1(20),
       "F(2,3)*a",
       lambda d: data([("Case", d["q"]), ("full tank time", f"{d['a']} h")])
       + " How long to fill the tank from one-third full to full?",
       "Two-thirds of {a} hours is needed, giving {c} hours.", unit=" h"),
    ef("pdi_pump_rate", ("a", "b", "q"), R2(15, 240),
       "F(b,a)",
       lambda d: data([("Case", d["q"]), ("fill time", f"{d['a']} h"), ("tank capacity", f"{d['b']} L")])
       + " Find the pump's hourly discharge in litres.",
       "Hourly discharge is {b}/{a} = {c} litres.", unit=" L/h"),
    ef("pdi_time_ratio", ("a", "b", "q"), R2(10, 15),
       "ratio(b,a)",
       lambda d: data([("Case", d["q"]), ("A alone", f"{d['a']} h"), ("B alone", f"{d['b']} h")])
       + " What is the ratio of B's filling time to A's filling time?",
       "The time ratio is {b}:{a}, i.e. {c}.", distract=lambda c, d: ratio_distractors(c)),
    ef("pdi_metered_fill", ("a", "b", "q"), R2(8, 125),
       "F(b,a)*60",
       lambda d: data([("Case", d["q"]), ("litres needed", str(d['b'])), ("rate", f"{d['a']} L/min")])
       + " How many seconds are required to deliver the stated volume?",
       "Minutes = {b}/{a}, so seconds = {c}.", unit=" s"),
    ef("pdi_average_rate", ("a", "b", "q"), R2(10, 15),
       "F(2*a*b,a+b)",
       lambda d: data([("Case", d["q"]), ("first pipe", f"{d['a']} h"), ("second pipe", f"{d['b']} h")])
       + " If each pipe works alone for an equal number of hours, what is the average effective filling time per pipe?",
       "The harmonic relation of {a} and {b} gives {c} hours.", unit=" h"),
    ef("pdi_fraction_full", ("a", "b", "q"), R2(18, 6),
       "F(a-b,a)",
       lambda d: data([("Case", d["q"]), ("inlet", f"{d['a']} h"), ("elapsed", f"{d['b']} h")])
       + " What fraction of the tank is full after the stated elapsed time?",
       "Filling for {b} of {a} hours gives {c} of the tank.", step=F(1, 12)),
    ef("pdi_joint_delay", ("a", "b", "q"), R2(12, 18),
       "F(2*a*b,3*(a+b))",
       lambda d: data([("Case", d["q"]), ("A alone", f"{d['a']} h"), ("B alone", f"{d['b']} h")])
       + " A works alone for one-third of its solo time, then both work. Find the extra time beyond A's solo start.",
       "The joint phase lasts {c} hours after A's initial work.", unit=" h"),
]


def build_pipe_and_cistern_di():
    return build_specs(FAMILIES)
