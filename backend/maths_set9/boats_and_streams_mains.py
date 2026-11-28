# -*- coding: utf-8 -*-
"""Boats and Streams (Mains): 24 HARD original five-variant families."""

from __future__ import annotations

from .common import build_specs, ef, ratio_distractors

SOURCE_PDF = "Boats and Streams Mains 01 Class Notes.pdf"
PAGES = {1: f"{SOURCE_PDF}, pp. 2-4", 2: f"{SOURCE_PDF}, pp. 5-8",
         3: f"{SOURCE_PDF}, pp. 9-12", 4: f"{SOURCE_PDF}, pp. 13-14"}


def R2(a, b):
    return [(a + 2*i, b + i, i+1) for i in range(5)]


def R3(a, b, c):
    return [(a + 2*i, b + i, c + 2*i, i+1) for i in range(5)]


FAMILIES = [
    ef("bm_up_down_time", ("b", "s", "D", "q"), R3(20, 5, 24),
       "F(D,b-s)+F(D,b+s)",
       lambda d: f"Case {d['q']}: A boat's still-water speed is {d['b']} km/h and the stream is {d['s']} km/h. Find the total time for {d['D']} km upstream and back.",
       "Upstream speed is {b}-{s} and downstream speed is {b}+{s}; total time is {c} h.", unit=" h"),
    ef("bm_stream_speed", ("up", "down", "q"), R2(12, 20),
       "F(down-up,2)",
       lambda d: f"Case {d['q']}: A boat moves at {d['up']} km/h upstream and {d['down']} km/h downstream. Find the stream speed.",
       "Stream speed = (downstream - upstream)/2 = {c} km/h.", unit=" km/h"),
    ef("bm_boat_speed", ("up", "down", "q"), R2(12, 20),
       "F(down+up,2)",
       lambda d: f"Case {d['q']}: A boat's upstream speed is {d['up']} km/h and downstream speed is {d['down']} km/h. Find its still-water speed.",
       "Still-water speed = (downstream + upstream)/2 = {c} km/h.", unit=" km/h"),
    ef("bm_two_boats", ("D", "p", "q1", "q"),
       [(60 + 10*i, 18 + i, 12 + i, i+1) for i in range(5)],
       "F(D,p+q1)",
       lambda d: f"Case {d['q']}: Two boats start towards each other {d['D']} km apart with still-water speeds {d['p']} km/h and {d['q1']} km/h. Find the meeting time.",
       "The stream helps one and hinders the other equally, so closure speed is {p}+{q1} km/h and time is {c} h.", unit=" h"),
    ef("bm_upstream_meet", ("D", "u1", "u2", "q"),
       [(48 + 6*i, 18 + i, 14 + i, i+1) for i in range(5)],
       "F(D,u1+u2)",
       lambda d: f"Case {d['q']}: Two boats start {d['D']} km apart and travel towards each other with effective upstream speeds {d['u1']} km/h and {d['u2']} km/h. Find the meeting time.",
       "Effective speeds add while approaching, giving {c} h.", unit=" h"),
    ef("bm_round_trip", ("b", "s", "q"), R2(20, 5),
       "F(2*(b-s)*(b+s),2*b)",
       lambda d: f"Case {d['q']}: A boat has still-water speed {d['b']} km/h in a stream of {d['s']} km/h. Find its average speed for an equal-distance round trip.",
       "Average speed is 2uv/(u+v) with u={b}-{s} and v={b}+{s}, giving {c} km/h.", unit=" km/h"),
    ef("bm_delay_start", ("D", "b", "s", "d", "q"),
       [(60 + 5*i, 20 + i, 5, i+1, i+1) for i in range(5)],
       "F(D-(b+s)*d,2*b)",
       lambda d: f"Case {d['q']}: Two towns are {d['D']} km apart. A boat starts downstream at {d['b']} km/h in a {d['s']} km/h stream; {d['d']} h later another starts from the far end at the same still-water speed. Find the meeting time from the first start.",
       "The first boat covers {b}+{s} km/h before the second starts, so the remaining gap closes at 2×{b} km/h: {c} h.", unit=" h"),
    ef("bm_current_change", ("D", "b", "s1", "s2", "q"),
       [(60 + 5*i, 20 + i, 4 + i, 6 + i, i+1) for i in range(5)],
       "F(D,b-s2)-F(D,b-s1)",
       lambda d: f"Case {d['q']}: A {d['D']} km upstream trip is made when the stream is {d['s1']} km/h and again when it is {d['s2']} km/h. The boat's still-water speed is {d['b']} km/h. Find the increase in journey time.",
       "Compare upstream times at the two stream speeds: {c} h.", unit=" h"),
    ef("bm_time_difference", ("D", "b", "s", "q"), R3(60, 20, 5),
       "F(D,b-s)-F(D,b+s)",
       lambda d: f"Case {d['q']}: A boat with still-water speed {d['b']} km/h travels {d['D']} km in a {d['s']} km/h stream. Find how much longer the upstream journey takes than the downstream journey.",
       "Difference of upstream and downstream times is {c} h.", unit=" h"),
    ef("bm_speed_ratio", ("b", "s", "q"), R2(20, 5),
       "ratio(b+s,b-s)",
       lambda d: f"Case {d['q']}: A boat's still-water speed is {d['b']} km/h and the stream speed is {d['s']} km/h. Find the ratio of downstream to upstream speeds.",
       "The ratio is ({b}+{s}):({b}-{s}) = {c}.", distract=lambda c, d: ratio_distractors(c)),
    ef("bm_relative_drift", ("s", "q"), [(5 + i, i+1) for i in range(5)],
       "F(2*s,1)",
       lambda d: f"Case {d['q']}: A stream flows at {d['s']} km/h. Find the difference between a boat's downstream and upstream speeds in still water of the same value.",
       "Downstream minus upstream speed is 2×{s} = {c} km/h.", unit=" km/h"),
    ef("bm_distance_split", ("b", "s", "t", "T", "q"),
       [(20 + i, 5, 2 + i, 10 + i, i+1) for i in range(5)],
       "F((b-s)*t+(b+s)*(T-t),1)",
       lambda d: f"Case {d['q']}: A boat travels upstream for {d['t']} h and then downstream for the rest of a {d['T']} h journey. Its still-water speed is {d['b']} km/h in a {d['s']} km/h stream. Find the total distance.",
       "Upstream distance plus downstream distance equals {c} km.", unit=" km"),
    ef("bm_current_from_times", ("D", "t1", "t2", "q"),
       [(60 + 10*i, 6 + i, 3 + i//2, i+1) for i in range(5)],
       "F(D*(t1-t2),2*t1*t2)",
       lambda d: f"Case {d['q']}: A boat takes {d['t1']} h upstream and {d['t2']} h downstream for the same {d['D']} km stretch. Find the stream speed.",
       "Stream speed = D(t1-t2)/(2t1t2) = {c} km/h.", unit=" km/h"),
    ef("bm_stop_in_stream", ("s", "t", "q"), R2(6, 2),
       "F(s*t,1)",
       lambda d: f"Case {d['q']}: A boat switches off its engine for {d['t']} h in a stream flowing at {d['s']} km/h. How far does it drift?",
       "Drift = stream speed × time = {c} km.", unit=" km"),
    ef("bm_trip_average", ("b", "s", "q"), R2(18, 4),
       "F(2*(b-s)*(b+s),2*b)",
       lambda d: f"Case {d['q']}: A boat makes an equal-distance round trip with still-water speed {d['b']} km/h in a {d['s']} km/h stream. Find the average speed for the trip.",
       "The harmonic mean of upstream and downstream speeds is {c} km/h.", unit=" km/h"),
    ef("bm_two_legs", ("D1", "D2", "b", "s", "q"),
       [(30 + 5*i, 40 + 5*i, 20 + i, 5, i+1) for i in range(5)],
       "F(D1,b-s)+F(D2,b+s)",
       lambda d: f"Case {d['q']}: A boat covers {d['D1']} km upstream and then {d['D2']} km downstream with still-water speed {d['b']} km/h in a {d['s']} km/h stream. Find the total time.",
       "Add the two leg times using upstream {b}-{s} and downstream {b}+{s}: {c} h.", unit=" h"),
    ef("bm_half_current", ("D", "b", "s", "q"), R3(60, 20, 6),
       "F(D,b-F(s,2))",
       lambda d: f"Case {d['q']}: A river's current falls to half its usual {d['s']} km/h. A boat with still-water speed {d['b']} km/h travels {d['D']} km upstream. Find the new time.",
       "New upstream speed is {b}-{s}/2, so time is {c} h.", unit=" h"),
    ef("bm_downstream_first", ("D", "b", "s", "q"), R3(60, 20, 5),
       "F(D,b+s)+F(D,b-s)",
       lambda d: f"Case {d['q']}: A boat goes {d['D']} km downstream first and returns the same distance. Its still-water speed is {d['b']} km/h and the stream is {d['s']} km/h. Find the total time.",
       "Downstream and upstream times add to {c} h.", unit=" h"),
    ef("bm_upstream_first", ("D", "b", "s", "q"), R3(60, 20, 5),
       "F(D,b-s)-F(D,b+s)",
       lambda d: f"Case {d['q']}: A boat travels {d['D']} km upstream and then returns. With still-water speed {d['b']} km/h in a {d['s']} km/h stream, how much longer is the upstream leg?",
       "The time difference is {c} h.", unit=" h"),
    ef("bm_meet_return", ("T", "b", "s", "q"), R3(10, 20, 5),
       "F(T*(b-s)*(b+s),2*b)",
       lambda d: f"Case {d['q']}: A boat completes an upstream-and-back trip in {d['T']} h total. Its still-water speed is {d['b']} km/h in a {d['s']} km/h stream. Find the one-way distance.",
       "Distance = T×u×v/(u+v) = {c} km.", unit=" km"),
    ef("bm_ratio_times", ("b", "s", "q"), R2(20, 5),
       "ratio(b+s,b-s)",
       lambda d: f"Case {d['q']}: A boat's still-water speed is {d['b']} km/h and the stream is {d['s']} km/h. Find the ratio of upstream time to downstream time for the same distance.",
       "Time ratio is inverse of speed ratio: ({b}+{s}):({b}-{s}) = {c}.", distract=lambda c, d: ratio_distractors(c)),
    ef("bm_walk_replace", ("D", "b", "s", "q"), R3(60, 20, 5),
       "F(D,b-s)-F(D,b+s)",
       lambda d: f"Case {d['q']}: Replacing a {d['D']} km downstream leg with the same distance upstream adds how much time? The boat's still-water speed is {d['b']} km/h in a {d['s']} km/h stream.",
       "The added time is upstream minus downstream time = {c} h.", unit=" h"),
    ef("bm_stream_ratio", ("b", "s", "q"), R2(20, 5),
       "ratio(s,b)",
       lambda d: f"Case {d['q']}: A boat's still-water speed is {d['b']} km/h and the stream speed is {d['s']} km/h. Find the ratio of stream speed to still-water speed.",
       "The required ratio is {s}:{b} = {c}.", distract=lambda c, d: ratio_distractors(c)),
    ef("bm_multi_leg", ("D", "b", "s", "q"), R3(40, 20, 5),
       "F(2*D,b-s)+F(D,b+s)",
       lambda d: f"Case {d['q']}: A boat makes two {d['D']} km upstream legs and one {d['D']} km downstream leg with still-water speed {d['b']} km/h in a {d['s']} km/h stream. Find total time.",
       "Total time is 2D/(b-s) + D/(b+s) = {c} h.", unit=" h"),
]


def build_boats_and_streams_mains():
    return build_specs(FAMILIES, mains=True)
