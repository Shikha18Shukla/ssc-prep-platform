# -*- coding: utf-8 -*-
"""Boats and Streams – Data Interpretation: 24 Prelims-level data families."""

from __future__ import annotations

from .common import build_specs, data, ef, near_pct, ratio_distractors

SOURCE_PDF = "Boats and Streams Data Interpretation 01 Class Notes.pdf"
PAGES = {1: SOURCE_PDF, 2: SOURCE_PDF, 3: SOURCE_PDF, 4: SOURCE_PDF}


def R1(a):
    return [(a + 2*i, i+1) for i in range(5)]


def R2(a, b):
    return [(a + 2*i, b + i, i+1) for i in range(5)]


def R3(a, b, c):
    return [(a + i, b + i, c + i, i+1) for i in range(5)]


FAMILIES = [
    ef("bdi_speed_table", ("up", "down", "q"), R2(12, 20),
       "F(down-up,2)",
       lambda d: data([("Case", d["q"]), ("upstream speed", f"{d['up']} km/h"), ("downstream speed", f"{d['down']} km/h")])
       + " Find the stream speed.",
       "Stream speed = (down - up)/2 = {c} km/h.", unit=" km/h"),
    ef("bdi_time_table", ("D", "v", "q"), R2(60, 20),
       "F(D,v)",
       lambda d: data([("Case", d["q"]), ("distance", f"{d['D']} km"), ("effective speed", f"{d['v']} km/h")])
       + " Find the travel time.",
       "Time = distance / speed = {c} h.", unit=" h"),
    ef("bdi_upstream_time", ("D", "b", "s", "q"), R3(60, 20, 5),
       "F(D,b-s)",
       lambda d: data([("Case", d["q"]), ("distance", f"{d['D']} km"), ("boat speed", f"{d['b']} km/h"), ("stream", f"{d['s']} km/h")])
       + " Find the upstream time.",
       "Upstream speed is {b}-{s}; time is {c} h.", unit=" h"),
    ef("bdi_downstream_time", ("D", "b", "s", "q"), R3(60, 20, 5),
       "F(D,b+s)",
       lambda d: data([("Case", d["q"]), ("distance", f"{d['D']} km"), ("boat speed", f"{d['b']} km/h"), ("stream", f"{d['s']} km/h")])
       + " Find the downstream time.",
       "Downstream speed is {b}+{s}; time is {c} h.", unit=" h"),
    ef("bdi_stream_speed", ("b", "up", "q"), R2(20, 15),
       "F(b-up,1)",
       lambda d: data([("Case", d["q"]), ("still-water speed", f"{d['b']} km/h"), ("upstream speed", f"{d['up']} km/h")])
       + " Find the stream speed.",
       "Stream speed = still-water minus upstream speed = {c} km/h.", unit=" km/h"),
    ef("bdi_round_trip", ("D", "u", "v", "q"), R3(60, 12, 20),
       "F(2*D*u*v,D*(u+v))",
       lambda d: data([("Case", d["q"]), ("one-way distance", f"{d['D']} km"), ("upstream speed", f"{d['u']} km/h"),
                       ("downstream speed", f"{d['v']} km/h")])
       + " Find the average speed for the round trip.",
       "Average speed = 2uv/(u+v) = {c} km/h.", unit=" km/h"),
    ef("bdi_distance_table", ("v", "t", "q"), R2(18, 4),
       "F(v*t,1)",
       lambda d: data([("Case", d["q"]), ("effective speed", f"{d['v']} km/h"), ("time", f"{d['t']} h")])
       + " Find the distance travelled.",
       "Distance = speed × time = {c} km.", unit=" km"),
    ef("bdi_ratio_table", ("b", "s", "q"), R2(20, 5),
       "ratio(b+s,b-s)",
       lambda d: data([("Case", d["q"]), ("boat speed", f"{d['b']} km/h"), ("stream", f"{d['s']} km/h")])
       + " Find the ratio of downstream to upstream speeds.",
       "The ratio is ({b}+{s}):({b}-{s}) = {c}.", distract=lambda c, d: ratio_distractors(c)),
    ef("bdi_meeting_point", ("D", "d1", "d2", "q"), R3(240, 20, 28),
       "F(D*d1,d1+d2)",
       lambda d: data([("Case", d["q"]), ("distance apart", f"{d['D']} km"), ("boat A effective speed", f"{d['d1']} km/h"),
                       ("boat B effective speed", f"{d['d2']} km/h")])
       + " Find the meeting distance from A's start.",
       "A covers d1/(d1+d2) of the route, i.e. {c} km.", unit=" km"),
    ef("bdi_average_speed", ("u", "v", "q"), R2(12, 20),
       "F(2*u*v,u+v)",
       lambda d: data([("Case", d["q"]), ("upstream speed", f"{d['u']} km/h"), ("downstream speed", f"{d['v']} km/h")])
       + " Find the average speed over an equal-distance round trip.",
       "Harmonic mean of the two speeds is {c} km/h.", unit=" km/h"),
    ef("bdi_current_effect", ("D", "b", "s", "q"), R3(60, 20, 5),
       "F(D,b-s)-F(D,b+s)",
       lambda d: data([("Case", d["q"]), ("distance", f"{d['D']} km"), ("boat speed", f"{d['b']} km/h"), ("stream", f"{d['s']} km/h")])
       + " Find the extra time caused by the current on the upstream leg.",
       "Upstream minus downstream time is {c} h.", unit=" h"),
    ef("bdi_two_boats", ("D", "v1", "v2", "q"), R3(200, 25, 20),
       "F(D,v1+v2)",
       lambda d: data([("Case", d["q"]), ("distance apart", f"{d['D']} km"), ("effective speed A", f"{d['v1']} km/h"),
                       ("effective speed B", f"{d['v2']} km/h")])
       + " Find the meeting time.",
       "Effective speeds add while approaching, giving {c} h.", unit=" h"),
    ef("bdi_stop_time", ("s", "t", "q"), R2(6, 2),
       "F(s*t,1)",
       lambda d: data([("Case", d["q"]), ("stream speed", f"{d['s']} km/h"), ("engine-off time", f"{d['t']} h")])
       + " Find the drift distance.",
       "Drift = stream speed × time = {c} km.", unit=" km"),
    ef("bdi_leg_distance", ("v", "t", "q"), R2(18, 3),
       "F(v*t,1)",
       lambda d: data([("Case", d["q"]), ("leg speed", f"{d['v']} km/h"), ("leg time", f"{d['t']} h")])
       + " Find the leg distance.",
       "Distance = speed × time = {c} km.", unit=" km"),
    ef("bdi_cost_table", ("trip", "fare", "other", "q"),
       [(4 + i, 250 + 25*i, 100 + 10*i, i+1) for i in range(5)],
       "F(trip*fare+other,1)",
       lambda d: data([("Case", d["q"]), ("trips", str(d["trip"])), ("fare per trip", f"₹{d['fare']}"), ("other charge", f"₹{d['other']}")])
       + " Find the total charge.",
       "Total charge is {trip}×₹{fare}+₹{other} = ₹{c}.", step=100),
    ef("bdi_frequency", ("interval", "window", "q"), R2(30, 6),
       "F(window*60,interval)",
       lambda d: data([("Case", d["q"]), ("service interval", f"{d['interval']} min"), ("observation window", f"{d['window']} h")])
       + " Find the number of services in the window.",
       "Window has 60×{window} minutes, so services = {c}.", unit=" trips"),
    ef("bdi_current_ratio", ("b", "s", "q"), R2(20, 5),
       "ratio(s,b)",
       lambda d: data([("Case", d["q"]), ("boat speed", f"{d['b']} km/h"), ("stream", f"{d['s']} km/h")])
       + " Find the ratio of stream speed to boat speed.",
       "The ratio is {s}:{b} = {c}.", distract=lambda c, d: ratio_distractors(c)),
    ef("bdi_delay_table", ("v", "delay", "q"), R2(80, 15),
       "F(v*delay,60)",
       lambda d: data([("Case", d["q"]), ("speed", f"{d['v']} km/h"), ("delay", f"{d['delay']} min")])
       + " Find the distance lost to the delay.",
       "Lost distance = speed × delay hours = {c} km.", unit=" km"),
    ef("bdi_speed_sum", ("up", "down", "q"), R2(12, 20),
       "F(up+down,1)",
       lambda d: data([("Case", d["q"]), ("upstream speed", f"{d['up']} km/h"), ("downstream speed", f"{d['down']} km/h")])
       + " Find the sum of the two speeds.",
       "Add the given speeds to get {c} km/h.", unit=" km/h"),
    ef("bdi_speed_diff", ("up", "down", "q"), R2(12, 20),
       "F(down-up,1)",
       lambda d: data([("Case", d["q"]), ("upstream speed", f"{d['up']} km/h"), ("downstream speed", f"{d['down']} km/h")])
       + " Find the difference between the two speeds.",
       "Subtract upstream from downstream: {c} km/h.", unit=" km/h"),
    ef("bdi_stream_table", ("b", "s", "q"), R2(18, 4),
       "F(b+s,1)",
       lambda d: data([("Case", d["q"]), ("still-water speed", f"{d['b']} km/h"), ("stream", f"{d['s']} km/h")])
       + " Find the downstream speed.",
       "Downstream speed is {b}+{s} = {c} km/h.", unit=" km/h"),
    ef("bdi_trip_table", ("D", "u", "v", "q"), R3(60, 12, 20),
       "F(D,u)+F(D,v)",
       lambda d: data([("Case", d["q"]), ("one-way distance", f"{d['D']} km"), ("upstream speed", f"{d['u']} km/h"),
                       ("downstream speed", f"{d['v']} km/h")])
       + " Find the total round-trip time.",
       "Add the two leg times: {c} h.", unit=" h"),
    ef("bdi_boat_table", ("b", "s", "q"), R2(20, 5),
       "F(b-s,1)",
       lambda d: data([("Case", d["q"]), ("still-water speed", f"{d['b']} km/h"), ("stream", f"{d['s']} km/h")])
       + " Find the upstream speed.",
       "Upstream speed is {b}-{s} = {c} km/h.", unit=" km/h"),
    ef("bdi_up_down_table", ("D", "b", "s", "q"), R3(60, 20, 5),
       "F(D,b+s)-F(D,b-s)",
       lambda d: data([("Case", d["q"]), ("distance", f"{d['D']} km"), ("boat speed", f"{d['b']} km/h"), ("stream", f"{d['s']} km/h")])
       + " Find how much less time the downstream journey takes.",
       "Downstream time subtracted from upstream time is {c} h.", unit=" h"),
]


def build_boats_and_streams_di():
    return build_specs(FAMILIES)
