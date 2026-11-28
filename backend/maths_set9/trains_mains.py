# -*- coding: utf-8 -*-
"""Trains (Mains): 24 HARD original five-variant families."""

from __future__ import annotations

from .common import build_specs, ef, near_pct, ratio_distractors

SOURCE_PDF = "Trains Mains 01 Class Notes.pdf"
PAGES = {1: f"{SOURCE_PDF}, pp. 2-4", 2: f"{SOURCE_PDF}, pp. 5-8",
         3: f"{SOURCE_PDF}, pp. 9-12", 4: f"{SOURCE_PDF}, pp. 13-14"}


def R1(a):
    return [(a + 2 * i, i + 1) for i in range(5)]


def R2(a, b):
    return [(a + 2 * i, b + i, i + 1) for i in range(5)]


def R3(a, b, c):
    return [(a + 2 * i, b + i, c + i, i + 1) for i in range(5)]


FAMILIES = [
    ef("tm_cross_pole", ("l", "t", "q"), R2(180, 12),
       "F(l*18,5*t)",
       lambda d: f"Case {d['q']}: A train of length {d['l']} m crosses a pole in {d['t']} s. Find its speed in km/h.",
       "Speed = length/time = {l}/{t} m/s = {c} km/h.", unit=" km/h"),
    ef("tm_cross_platform", ("l", "p", "t", "q"), R3(180, 120, 20),
       "F((l+p)*18,5*t)",
       lambda d: f"Case {d['q']}: A {d['l']} m train clears a {d['p']} m platform in {d['t']} s. Find the train's speed in km/h.",
       "Total distance is {l} + {p} = {c} when converted from m/s to km/h.", unit=" km/h"),
    ef("tm_opposite_trains", ("l1", "l2", "s1", "s2", "q"),
       [(120 + 10*i, 150 + 10*i, 45 + i, 36 + i, i+1) for i in range(5)],
       "F((l1+l2)*18,5*(s1+s2))",
       lambda d: f"Case {d['q']}: Two trains of lengths {d['l1']} m and {d['l2']} m run towards each other at {d['s1']} km/h and {d['s2']} km/h. Find the crossing time.",
       "Relative speed is {s1}+{s2} km/h, so crossing time is {c} s.", unit=" s"),
    ef("tm_same_direction", ("l1", "l2", "s1", "s2", "q"),
       [(120 + 10*i, 150 + 10*i, 72 + i, 54 + i, i+1) for i in range(5)],
       "F((l1+l2)*18,5*(s1-s2))",
       lambda d: f"Case {d['q']}: Trains of lengths {d['l1']} m and {d['l2']} m move in the same direction at {d['s1']} km/h and {d['s2']} km/h. Find the time for the faster to clear the slower.",
       "Relative speed is {s1}-{s2} km/h, giving {c} s.", unit=" s"),
    ef("tm_gap_closure", ("gap", "s1", "s2", "q"), R3(60, 50, 30),
       "F(gap,s1-s2)",
       lambda d: f"Case {d['q']}: Two trains start {d['gap']} km apart and move in the same direction at {d['s1']} km/h and {d['s2']} km/h. How long until they meet?",
       "Closure speed is {s1}-{s2} km/h, so time is {c} hours.", unit=" h"),
    ef("tm_platform_ratio", ("l", "t", "q"), R2(200, 15),
       "F(l*18,5*t)",
       lambda d: f"Case {d['q']}: A train crosses a pole in {d['t']} s and its length is {d['l']} m. What is its speed in km/h?",
       "Pole crossing uses only the train length: {l}/{t} m/s = {c} km/h.", unit=" km/h"),
    ef("tm_bridge_cross", ("l", "b", "t", "q"), R3(160, 240, 24),
       "F((l+b)*18,5*t)",
       lambda d: f"Case {d['q']}: A {d['l']} m train takes {d['t']} s to cross a {d['b']} m bridge. Find its speed in km/h.",
       "Distance covered is {l}+{b} m; converting m/s to km/h gives {c}.", unit=" km/h"),
    ef("tm_tunnel_cross", ("l", "tun", "t", "q"), R3(240, 160, 30),
       "F((l+tun)*18,5*t)",
       lambda d: f"Case {d['q']}: A {d['l']} m train enters a {d['tun']} m tunnel and clears it in {d['t']} s. Find the speed in km/h.",
       "The engine travels {l}+{tun} m, so the speed is {c} km/h.", unit=" km/h"),
    ef("tm_delay_meet", ("gap", "s1", "s2", "d", "q"),
       [(80 + 10*i, 50 + i, 40 + i, 1 + i, i+1) for i in range(5)],
       "F(gap+s2*d,s1+s2)",
       lambda d: f"Case {d['q']}: Two stations are {d['gap']} km apart. A train leaves one at {d['s1']} km/h; {d['d']} h later another leaves the other at {d['s2']} km/h. When do they meet, measured from the first departure?",
       "The first train gains {s2}×{d} km before the second starts, so meeting time is {c} h.", unit=" h"),
    ef("tm_stoppage_loss", ("v", "stop", "q"), R2(80, 12),
       "F(v*(60-stop),60)",
       lambda d: f"Case {d['q']}: A train's running speed is {d['v']} km/h, but it stops for {d['stop']} minutes each hour. Find its average speed including stops.",
       "Only 60-{stop} minutes per hour are moving, giving {c} km/h.", unit=" km/h"),
    ef("tm_speed_conversion", ("v", "q"), R1(18),
       "F(v*18,5)",
       lambda d: f"Case {d['q']}: A train moves at {d['v']} m/s. Convert this speed to km/h.",
       "Multiplying m/s by 18/5 gives {c} km/h.", unit=" km/h"),
    ef("tm_length_from_two", ("v", "t1", "t2", "q"), R3(72, 10, 14),
       "F(v*5*(t2-t1),18)",
       lambda d: f"Case {d['q']}: A train running at {d['v']} km/h passes a pole in {d['t1']} s and a platform in {d['t2']} s. Find the platform length.",
       "Extra time {t2}-{t1} at {v} km/h corresponds to {c} m.", unit=" m"),
    ef("tm_goods_passenger", ("lg", "lp", "sg", "sp", "q"),
       [(200 + 10*i, 160 + 10*i, 60 + i, 42 + i, i+1) for i in range(5)],
       "F((lg+lp)*18,5*(sg-sp))",
       lambda d: f"Case {d['q']}: A goods train of length {d['lg']} m at {d['sg']} km/h overtakes a {d['lp']} m passenger train at {d['sp']} km/h. How long does the overtaking take?",
       "Relative speed is {sg}-{sp} km/h and distance is {lg}+{lp} m, so time is {c} s.", unit=" s"),
    ef("tm_overtake_time", ("gap", "f", "s", "q"), R3(30, 90, 60),
       "F(gap,f-s)",
       lambda d: f"Case {d['q']}: A faster train is {d['gap']} km behind a slower one and travels at {d['f']} km/h versus {d['s']} km/h. How many hours until it catches up?",
       "The gap closes at {f}-{s} km/h, giving {c} h.", unit=" h"),
    ef("tm_telegraph_poles", ("n", "d", "v", "q"),
       [(12 + i, 40 + 5*i, 60 + i, i+1) for i in range(5)],
       "F((n-1)*d*18,5*v)",
       lambda d: f"Case {d['q']}: Telegraph poles are {d['d']} m apart. A train at {d['v']} km/h passes {d['n']} consecutive poles. How many seconds elapse from the first to the last?",
       "There are {n}-1 intervals, so the elapsed time is {c} s.", unit=" s"),
    ef("tm_meeting_point", ("D", "s1", "s2", "q"), R3(180, 60, 48),
       "F(D*s1,s1+s2)",
       lambda d: f"Case {d['q']}: Two cities are {d['D']} km apart. Trains leave simultaneously towards each other at {d['s1']} km/h and {d['s2']} km/h. How far from the first city do they meet?",
       "The first train covers {s1}/({s1}+{s2}) of {D} km, i.e. {c} km.", unit=" km"),
    ef("tm_crossing_difference", ("l1", "l2", "s1", "s2", "q"),
       [(180 + 10*i, 220 + 10*i, 72 + i, 54 + i, i+1) for i in range(5)],
       "F((l1+l2)*18,5*(s1-s2))-F((l1+l2)*18,5*(s1+s2))",
       lambda d: f"Case {d['q']}: Two trains of lengths {d['l1']} m and {d['l2']} m have speeds {d['s1']} km/h and {d['s2']} km/h. Find the difference between their same-direction and opposite-direction crossing times.",
       "The reciprocal relative-speed difference is {c} s.", unit=" s"),
    ef("tm_early_late", ("v1", "v2", "dt", "q"), R3(60, 75, 1),
       "F(v1*v2*dt,v2-v1)",
       lambda d: f"Case {d['q']}: A train travelling at {d['v1']} km/h arrives {d['dt']} h later than one travelling at {d['v2']} km/h over the same route. Find the route length.",
       "Equal-distance relation gives length = {v1}×{v2}×{dt}/({v2}-{v1}) = {c} km.", unit=" km"),
    ef("tm_relative_speed", ("s1", "s2", "q"), R2(60, 48),
       "F((s1+s2)*5,18)",
       lambda d: f"Case {d['q']}: Two trains move towards each other at {d['s1']} km/h and {d['s2']} km/h. Find their relative speed in m/s.",
       "Relative speed {s1}+{s2} km/h converts to {c} m/s.", unit=" m/s"),
    ef("tm_half_journey", ("v1", "v2", "q"), R2(40, 60),
       "F(2*v1*v2,v1+v2)",
       lambda d: f"Case {d['q']}: A train covers the first half of a journey at {d['v1']} km/h and the second half at {d['v2']} km/h. Find the average speed for the whole journey.",
       "For equal distances the harmonic mean is {c} km/h.", unit=" km/h"),
    ef("tm_platform_speed", ("l", "p", "t", "q"), R3(180, 120, 20),
       "F((l+p)*18,10*t)",
       lambda d: f"Case {d['q']}: After doubling its speed, a {d['l']} m train clears a {d['p']} m platform in {d['t']} s. Find the original speed in km/h.",
       "Doubled speed equals ({l}+{p})/{t} m/s, so the original speed is {c} km/h.", unit=" km/h"),
    ef("tm_signal_gap", ("d", "l", "v", "q"), R3(500, 180, 72),
       "F((d-l)*18,5*v)",
       lambda d: f"Case {d['q']}: Signals are {d['d']} m apart. A {d['l']} m train travels at {d['v']} km/h. How long after the engine passes the first signal does the guard clear the second?",
       "The guard travels {d}-{l} m at {v} km/h, taking {c} s.", unit=" s"),
    ef("tm_two_bridge", ("l1", "l2", "t1", "t2", "q"),
       [(120 + 5*i, 200 + 5*i, 12 + i, 18 + i, i+1) for i in range(5)],
       "F((l2-l1)*18,5*(t2-t1))",
       lambda d: f"Case {d['q']}: A train takes {d['t1']} s to cross a {d['l1']} m bridge and {d['t2']} s to cross a {d['l2']} m bridge. Find its speed in km/h.",
       "The extra {l2}-{l1} m is covered in {t2}-{t1} s, giving {c} km/h.", unit=" km/h"),
    ef("tm_time_ratio", ("s1", "s2", "q"), R2(40, 60),
       "ratio(s2,s1)",
       lambda d: f"Case {d['q']}: Two trains cover the same distance at {d['s1']} km/h and {d['s2']} km/h. Find the ratio of the first journey's time to the second's.",
       "Times are inversely proportional to speeds, so the ratio is {s2}:{s1} = {c}.",
       distract=lambda c, d: ratio_distractors(c)),
]


def build_trains_mains():
    return build_specs(FAMILIES, mains=True)
