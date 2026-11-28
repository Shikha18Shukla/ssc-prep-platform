# -*- coding: utf-8 -*-
"""Trains – Data Interpretation: 24 Prelims-level data families."""

from __future__ import annotations

from .common import build_specs, data, ef, near_pct, ratio_distractors

SOURCE_PDF = "Trains Data Interpretation 01 Class Notes.pdf"
PAGES = {1: SOURCE_PDF, 2: SOURCE_PDF, 3: SOURCE_PDF, 4: SOURCE_PDF}


def R1(a):
    return [(a + 2 * i, i + 1) for i in range(5)]


def R2(a, b):
    return [(a + 2 * i, b + i, i + 1) for i in range(5)]


def R3(a, b, c):
    return [(a + i, b + i, c + i, i + 1) for i in range(5)]


FAMILIES = [
    ef("tdi_speed_table", ("l", "t", "q"), R2(180, 12),
       "F(l*18,5*t)",
       lambda d: data([("Case", d["q"]), ("length", f"{d['l']} m"), ("pole time", f"{d['t']} s")])
       + " Find the train's speed in km/h.",
       "Length divided by pole time gives m/s; multiplying by 18/5 gives {c} km/h.", unit=" km/h"),
    ef("tdi_length_table", ("v", "t", "q"), R2(72, 10),
       "F(v*5*t,18)",
       lambda d: data([("Case", d["q"]), ("speed", f"{d['v']} km/h"), ("pole time", f"{d['t']} s")])
       + " Find the train length in metres.",
       "Length = speed × time = {c} m.", unit=" m"),
    ef("tdi_cross_pole", ("l", "v", "q"), R2(180, 60),
       "F(l*5,18*v)",
       lambda d: data([("Case", d["q"]), ("length", f"{d['l']} m"), ("speed", f"{d['v']} km/h")])
       + " How many seconds does the train take to cross a pole?",
       "Convert {v} km/h to m/s and divide {l} m by it: {c} s.", unit=" s"),
    ef("tdi_platform_time", ("l", "p", "v", "q"), R3(180, 120, 60),
       "F((l+p)*5,18*v)",
       lambda d: data([("Case", d["q"]), ("train length", f"{d['l']} m"), ("platform", f"{d['p']} m"), ("speed", f"{d['v']} km/h")])
       + " Find the time to clear the platform.",
       "Distance is {l}+{p} m at {v} km/h, so time is {c} s.", unit=" s"),
    ef("tdi_opposite_meet", ("l1", "l2", "s1", "s2", "q"),
       [(140 + 10*i, 160 + 10*i, 50 + i, 40 + i, i+1) for i in range(5)],
       "F((l1+l2)*5,18*(s1+s2))",
       lambda d: data([("Case", d["q"]), ("length A", f"{d['l1']} m"), ("length B", f"{d['l2']} m"),
                       ("speed A", f"{d['s1']} km/h"), ("speed B", f"{d['s2']} km/h")])
       + " Find the crossing time when they move towards each other.",
       "Opposite-direction relative speed is {s1}+{s2} km/h, giving {c} s.", unit=" s"),
    ef("tdi_same_overtake", ("l1", "l2", "s1", "s2", "q"),
       [(140 + 10*i, 160 + 10*i, 72 + i, 54 + i, i+1) for i in range(5)],
       "F((l1+l2)*5,18*(s1-s2))",
       lambda d: data([("Case", d["q"]), ("faster length", f"{d['l1']} m"), ("slower length", f"{d['l2']} m"),
                       ("faster speed", f"{d['s1']} km/h"), ("slower speed", f"{d['s2']} km/h")])
       + " Find the overtaking time in the same direction.",
       "Same-direction relative speed is {s1}-{s2} km/h, giving {c} s.", unit=" s"),
    ef("tdi_distance_table", ("v", "t", "q"), R2(60, 4),
       "F(v*t,1)",
       lambda d: data([("Case", d["q"]), ("speed", f"{d['v']} km/h"), ("time", f"{d['t']} h")])
       + " Find the distance travelled.",
       "Distance = speed × time = {c} km.", unit=" km"),
    ef("tdi_stoppage_table", ("v", "stop", "q"), R2(75, 10),
       "F(v*(60-stop),60)",
       lambda d: data([("Case", d["q"]), ("running speed", f"{d['v']} km/h"), ("stoppage", f"{d['stop']} min/h")])
       + " Find the effective average speed.",
       "Effective moving time is 60-{stop} minutes per hour, giving {c} km/h.", unit=" km/h"),
    ef("tdi_gap_table", ("D", "s1", "s2", "q"), R3(240, 70, 50),
       "F(D,s1-s2)",
       lambda d: data([("Case", d["q"]), ("initial gap", f"{d['D']} km"), ("chasing speed", f"{d['s1']} km/h"),
                       ("leading speed", f"{d['s2']} km/h")])
       + " How long until the gap closes?",
       "Using the stated leading and chasing speeds gives closure time {c} h.", unit=" h"),
    ef("tdi_time_table", ("D", "v", "q"), R2(300, 60),
       "F(D,v)",
       lambda d: data([("Case", d["q"]), ("distance", f"{d['D']} km"), ("speed", f"{d['v']} km/h")])
       + " Find the journey time.",
       "Time = distance / speed = {c} h.", unit=" h"),
    ef("tdi_average_speed", ("v1", "v2", "q"), R2(40, 60),
       "F(2*v1*v2,v1+v2)",
       lambda d: data([("Case", d["q"]), ("first-half speed", f"{d['v1']} km/h"), ("second-half speed", f"{d['v2']} km/h")])
       + " Find the average speed for equal halves.",
       "Equal distances give harmonic mean {c} km/h.", unit=" km/h"),
    ef("tdi_rel_speed", ("s1", "s2", "q"), R2(65, 55),
       "F(s1+s2,1)",
       lambda d: data([("Case", d["q"]), ("train A", f"{d['s1']} km/h"), ("train B", f"{d['s2']} km/h")])
       + " Find their relative speed when moving towards each other.",
       "Add the speeds to get {c} km/h.", unit=" km/h"),
    ef("tdi_platform_length", ("l", "v", "t", "q"), R3(150, 60, 18),
       "F(v*5*t,18)-l",
       lambda d: data([("Case", d["q"]), ("train length", f"{d['l']} m"), ("speed", f"{d['v']} km/h"),
                       ("platform time", f"{d['t']} s")])
       + " Find the platform length.",
       "Distance covered minus train length is {c} m.", unit=" m"),
    ef("tdi_two_trains", ("D", "s1", "s2", "q"), R3(360, 60, 45),
       "F(D,s1+s2)",
       lambda d: data([("Case", d["q"]), ("distance apart", f"{d['D']} km"), ("speed A", f"{d['s1']} km/h"),
                       ("speed B", f"{d['s2']} km/h")])
       + " Find the meeting time if they start together.",
       "Closing speed is {s1}+{s2} km/h, so they meet after {c} h.", unit=" h"),
    ef("tdi_frequency", ("T", "n", "q"), R2(48, 6),
       "F(T,n)",
       lambda d: data([("Case", d["q"]), ("total time", f"{d['T']} min"), ("trains observed", str(d['n']))])
       + " Find the average interval between trains.",
       "Dividing total time by count gives {c} minutes.", unit=" min"),
    ef("tdi_delay_table", ("v", "delay", "q"), R2(80, 15),
       "F(v*delay,60)",
       lambda d: data([("Case", d["q"]), ("speed", f"{d['v']} km/h"), ("delay", f"{d['delay']} min")])
       + " Find the distance lost due to the delay.",
       "Distance lost is speed × delay hours = {c} km.", unit=" km"),
    ef("tdi_bridge_table", ("l", "b", "v", "q"), R3(160, 240, 72),
       "F((l+b)*5,18*v)",
       lambda d: data([("Case", d["q"]), ("train length", f"{d['l']} m"), ("bridge", f"{d['b']} m"),
                       ("speed", f"{d['v']} km/h")])
       + " Find the bridge-crossing time.",
       "The train covers {l}+{b} m at {v} km/h, taking {c} s.", unit=" s"),
    ef("tdi_ratio_table", ("s1", "s2", "q"), R2(45, 60),
       "ratio(s2,s1)",
       lambda d: data([("Case", d["q"]), ("time A", f"{d['s1']} min"), ("time B", f"{d['s2']} min")])
       + " Find the ratio of speeds of A to B for the same route.",
       "Speeds are inverse to times, so the ratio is {s2}:{s1} = {c}.",
       distract=lambda c, d: ratio_distractors(c)),
    ef("tdi_meet_point", ("D", "s1", "s2", "q"), R3(180, 50, 40),
       "F(D*s1,s1+s2)",
       lambda d: data([("Case", d["q"]), ("route length", f"{d['D']} km"), ("speed A", f"{d['s1']} km/h"),
                       ("speed B", f"{d['s2']} km/h")])
       + " Find the distance from A's start where they meet.",
       "A covers {s1}/({s1}+{s2}) of the route, i.e. {c} km.", unit=" km"),
    ef("tdi_cost_per_km", ("fare", "D", "q"), R2(360, 240),
       "F(fare,D)",
       lambda d: data([("Case", d["q"]), ("total fare", f"₹{d['fare']}"), ("distance", f"{d['D']} km")])
       + " Find the fare per kilometre.",
       "Fare per kilometre is ₹{fare}/{D} = ₹{c}.", step=1),
    ef("tdi_headway", ("T", "n", "q"), R2(60, 5),
       "F(T,n)",
       lambda d: data([("Case", d["q"]), ("observation window", f"{d['T']} min"), ("departures", str(d['n']))])
       + " Find the average headway between departures.",
       "Average headway is {T}/{n} = {c} minutes.", unit=" min"),
    ef("tdi_platform_count", ("n", "p", "q"), R2(8, 180),
       "F(n*p,1000)",
       lambda d: data([("Case", d["q"]), ("platforms", str(d['n'])), ("average length", f"{d['p']} m")])
       + " Find the total platform length in kilometres.",
       "Total length is {n}×{p} m = {c} km.", unit=" km"),
    ef("tdi_speed_gap", ("l", "t1", "t2", "q"), R3(180, 12, 15),
       "F(l*18,5*t2)",
       lambda d: data([("Case", d["q"]), ("length", f"{d['l']} m"), ("old pole time", f"{d['t1']} s"),
                       ("new pole time", f"{d['t2']} s")])
       + " Find the new speed in km/h.",
       "Using the new pole time, speed = {l}/{t2} m/s = {c} km/h.", unit=" km/h"),
    ef("tdi_crossing_order", ("l", "v", "p", "q"), R3(160, 72, 140),
       "F((l+p)*5,18*v)",
       lambda d: data([("Case", d["q"]), ("length", f"{d['l']} m"), ("speed", f"{d['v']} km/h"),
                       ("crossing object", f"{d['p']} m")])
       + " Find the crossing time for the moving object.",
       "Relative distance is {l}+{p} m; at {v} km/h the time is {c} s.", unit=" s"),
]


def build_trains_di():
    return build_specs(FAMILIES)
