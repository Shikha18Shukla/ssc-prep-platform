# -*- coding: utf-8 -*-
"""Speed, Time and Distance - 120 verified questions for the fourth Maths batch."""

from __future__ import annotations

import math
from fractions import Fraction

from .bank import fmt, fmt_dec
from .common import build_specs, pair, q, third

SOURCE = "Speed, Time and Distance topic-wise mains sets (local PDFs)"
PAGES = {
    1: "Mains_Topic_wise_Time,_Speed_and_Distance_Set_-1_(Mains).pdf, pp. 1-7",
    2: "Mains_Topic_wise_Time,_Speed_and_Distance_Set_-2_(Mains).pdf, pp. 1-13",
    3: "Mains_Topic_wise_Time,_Speed_and_Distance_Set_-3_(Mains).pdf, pp. 1-7",
    4: "Mains_Topic_wise_Time,_Speed_and_Distance_Set_-4_(Mains).pdf, pp. 1-6",
    5: "Mains_Topic_wise_Application_Based_DI_Time,_Speed_and_Distance_Set.pdf, pp. 1-11",
}

LEADS = ("Find", "Calculate", "Work out", "Determine", "Compute")


def F(value, denominator=None):
    if denominator is None:
        return Fraction(value)
    return Fraction(value, denominator)


def dec(value, places=2):
    return fmt_dec(float(value), places)


def rat(a, b):
    a, b = Fraction(a), Fraction(b)
    scale = math.lcm(a.denominator, b.denominator)
    first = a.numerator * (scale // a.denominator)
    second = b.numerator * (scale // b.denominator)
    divisor = math.gcd(abs(first), abs(second)) or 1
    return f"{first // divisor}:{second // divisor}"


def pick3(correct, *candidates):
    answer = fmt(correct)
    values = []
    for candidate in candidates:
        text = fmt(candidate)
        if text != answer and text not in values:
            values.append(text)
            if len(values) == 3:
                return values
    try:
        base = Fraction(correct)
    except (ValueError, ZeroDivisionError):
        return values
    step = 1
    while len(values) < 3:
        for candidate in (base + step, base - step, base + 2 * step, base - 2 * step):
            text = fmt(candidate)
            if text != answer and text not in values:
                values.append(text)
                if len(values) == 3:
                    return values
        step += 1
    return values


def lead(v):
    return LEADS[v % len(LEADS)]


def sd_basic_speed(r, v):
    person, _ = pair(v, 0)
    d, t = [(120, 2), (180, 3), (220, 4), (315, 5), (360, 4)][v]
    speed = F(d, t)
    return q(
        "sd_basic_speed", v,
        f"{lead(v)} the average speed of {person}, who covers {d} km in {t} hours. "
        "Give the answer in km/h.",
        speed,
        pick3(speed, F(d, t + 1), F(d + 10, t), F(d * 2, t)),
        f"Speed = distance / time = {d}/{t} = {fmt(speed)} km/h.",
        {"D": d, "T": t},
    )


def sd_basic_time(r, v):
    traveller, _ = pair(v, 1)
    d, s = [(150, 50), (240, 60), (180, 45), (210, 30), (360, 72)][v]
    time_taken = F(d, s)
    return q(
        "sd_basic_time", v,
        f"{lead(v)} how many hours {traveller} needs to walk {d} km at a steady "
        f"{s} km/h.",
        time_taken,
        pick3(time_taken, F(d + 10, s), F(d, s + 10), F(d, 2 * s)),
        f"Time = distance / speed = {d}/{s} = {fmt(time_taken)} hours.",
        {"D": d, "S": s},
    )


def sd_basic_distance(r, v):
    walker, _ = pair(v, 2)
    s, t = [(45, 3), (60, 4), (72, 2), (55, 6), (80, 5)][v]
    distance = F(s * t)
    return q(
        "sd_basic_distance", v,
        f"{lead(v)} the distance travelled by {walker} in {t} hours at "
        f"{s} km/h.",
        distance,
        pick3(distance, F(s * (t + 1)), F((s + 5) * t), F(s + 10 * t)),
        f"Distance = speed x time = {s} x {t} = {fmt(distance)} km.",
        {"S": s, "T": t},
    )


def sd_kmph_to_mps(r, v):
    runner, _ = pair(v, 3)
    k = [72, 45, 108, 63, 54][v]
    mps = F(k) * F(5, 18)
    return q(
        "sd_kmph_to_mps", v,
        f"{lead(v)} the speed of {runner} in m/s if it is {k} km/h.",
        mps,
        pick3(mps, F(k) * F(5, 9), F(k, 2), F(k) * F(18, 5)),
        f"km/h to m/s: {k} x 5/18 = {fmt(mps)} m/s.",
        {"K": k},
    )


def sd_mps_to_kmph(r, v):
    cyclist, _ = pair(v, 4)
    m = [20, 15, 30, 25, 12][v]
    kmph = F(m) * F(18, 5)
    return q(
        "sd_mps_to_kmph", v,
        f"{lead(v)} the speed in km/h of {cyclist}, who moves at "
        f"{dec(F(m))} m/s.",
        kmph,
        pick3(kmph, F(m) * F(5, 18), F(m) * F(9, 5), F(m) * F(36, 5)),
        f"m/s to km/h: {dec(F(m))} x 18/5 = {fmt(kmph)} km/h.",
        {"M": m},
    )


def sd_average_two_legs(r, v):
    driver, _ = pair(v, 5)
    a, b = [(40, 60), (30, 60), (50, 75), (20, 30), (60, 90)][v]
    average = F(2) * F(a) * F(b) / (F(a) + F(b))
    return q(
        "sd_average_two_legs", v,
        f"{lead(v)} the average speed of {driver}, who covers equal halves of "
        f"a trip at {a} km/h and {b} km/h.",
        average,
        pick3(average, F(a + b, 2), F(a + b), F(a * b, a + b)),
        f"Equal distances: average speed = 2ab/(a+b) = "
        f"2 x {a} x {b}/({a}+{b}) = {fmt(average)} km/h.",
        {"A": a, "B": b},
    )


def sd_same_direction(r, v):
    first, second = pair(v, 6)
    a, b, t = [(14, 10, 3), (20, 12, 4), (25, 15, 2), (18, 10, 5), (30, 24, 6)][v]
    gap = (F(a) - F(b)) * F(t)
    return q(
        "sd_same_direction", v,
        f"{first} and {second} start together from the same point and move in the "
        f"same direction at {a} km/h and {b} km/h. {lead(v)} the distance between "
        f"them after {t} hours.",
        gap,
        pick3(gap, (F(a) + F(b)) * F(t), F(a) * F(t), F(b) * F(t)),
        f"Relative speed = {a} - {b} = {a - b} km/h; gap = {a - b} x {t} = "
        f"{fmt(gap)} km.",
        {"A": a, "B": b, "T": t},
    )


def sd_opposite_direction(r, v):
    first, second = pair(v, 7)
    d, a, b = [(120, 25, 35), (240, 30, 50), (210, 25, 45), (330, 50, 60), (400, 30, 70)][v]
    meet_time = F(d, a + b)
    return q(
        "sd_opposite_direction", v,
        f"{first} starts from one town and {second} from another, {d} km apart. "
        f"They walk towards each other at {a} km/h and {b} km/h. "
        f"{lead(v)} the time until they meet, in hours.",
        meet_time,
        pick3(meet_time, F(d, abs(a - b)), F(d, a), F(d, b)),
        f"Closing speed = {a} + {b} = {a + b} km/h; time = {d}/{a + b} = "
        f"{fmt(meet_time)} hours.",
        {"D": d, "A": a, "B": b},
    )


def sd_meeting(r, v):
    first, second = pair(v, 8)
    d, a, b = [(200, 30, 20), (180, 40, 50), (240, 20, 60), (300, 45, 30), (360, 50, 40)][v]
    from_first = F(d) * F(a) / (F(a) + F(b))
    return q(
        "sd_meeting", v,
        f"{first} and {second} start from towns {d} km apart and walk towards each "
        f"other at {a} km/h and {b} km/h. {lead(v)} the distance from "
        f"{first}'s town to the meeting point.",
        from_first,
        pick3(from_first, F(d) * F(b) / (F(a) + F(b)), F(d, a + b), F(d) * F(a) / F(b)),
        f"Distances are in the ratio {a}:{b}; distance from {first}'s town = "
        f"{d} x {a}/({a}+{b}) = {fmt(from_first)} km.",
        {"D": d, "A": a, "B": b},
    )


def sd_chase(r, v):
    chaser, target = pair(v, 9)
    a, b, gap_km = [(20, 12, 32), (30, 18, 36), (25, 15, 50), (18, 12, 27), (45, 30, 60)][v]
    catch_time = F(gap_km, a - b)
    return q(
        "sd_chase", v,
        f"{target} has a {gap_km} km head start over {chaser}. They begin moving "
        f"together in the same direction at {b} km/h and {a} km/h. "
        f"{lead(v)} how long {chaser} takes to catch {target}, in hours.",
        catch_time,
        pick3(catch_time, F(gap_km, a + b), F(gap_km, a), F(gap_km, b)),
        f"Gain per hour = {a} - {b} = {a - b} km; catch time = {gap_km}/{a - b} = "
        f"{fmt(catch_time)} hours.",
        {"A": a, "B": b, "G": gap_km},
    )


def sd_head_start(r, v):
    faster, slower = pair(v, 10)
    h, a, b = [(12, 18, 12), (20, 25, 15), (9, 15, 12), (30, 40, 30), (24, 20, 14)][v]
    meeting_distance = F(a) * F(h) / (F(a) - F(b))
    return q(
        "sd_head_start", v,
        f"In a long race, {slower} is given a {h} km head start over {faster}. "
        f"Their speeds are {b} km/h and {a} km/h. {lead(v)} the distance from the "
        f"start at which {faster} catches {slower}.",
        meeting_distance,
        pick3(meeting_distance, F(b) * F(h) / (F(a) - F(b)), F(h, a - b), F(h)),
        f"Closing speed = {a} - {b} = {a - b} km/h; catch time = {h}/{a - b} hours; "
        f"distance run by {faster} = {a} x {h}/{a - b} = {fmt(meeting_distance)} km.",
        {"H": h, "A": a, "B": b},
    )


def sd_two_legs_time(r, v):
    person, _ = pair(v, 11)
    d1, s1, d2, s2 = [
        (60, 30, 120, 40), (90, 45, 60, 30), (100, 25, 150, 50),
        (80, 40, 90, 30), (120, 60, 180, 45),
    ][v]
    total = F(d1, s1) + F(d2, s2)
    return q(
        "sd_two_legs_time", v,
        f"{person} travels {d1} km at {s1} km/h and then another {d2} km at "
        f"{s2} km/h. {lead(v)} the total travel time in hours.",
        total,
        pick3(total, F(d1 + d2, s1), F(d1 + d2, s2), F(d1, s2) + F(d2, s1)),
        f"Time = {d1}/{s1} + {d2}/{s2} = {fmt(F(d1, s1))} + {fmt(F(d2, s2))} = "
        f"{fmt(total)} hours.",
        {"D1": d1, "S1": s1, "D2": d2, "S2": s2},
    )


def sd_distance_ratio(r, v):
    first, second = pair(v, 12)
    a, b = [(3, 2), (5, 3), (4, 3), (7, 5), (5, 4)][v]
    answer = rat(a, b)
    return q(
        "sd_distance_ratio", v,
        f"{first} and {second} travel for the same length of time at {a} km/h and "
        f"{b} km/h. {lead(v)} the ratio of the distances they cover.",
        answer,
        pick3(answer, rat(b, a), rat(a + 1, b), rat(a, b + 1), rat(a + 1, b + 1)),
        f"With equal time, distance is proportional to speed: {a}:{b} = {answer}.",
        {"A": a, "B": b},
    )


def sd_time_ratio(r, v):
    first, second = pair(v, 13)
    a, b = [(2, 3), (3, 5), (5, 7), (4, 9), (5, 8)][v]
    answer = rat(b, a)
    return q(
        "sd_time_ratio", v,
        f"{first} and {second} cover the same distance at {a} km/h and {b} km/h. "
        f"{lead(v)} the ratio of their travel times (first to second).",
        answer,
        pick3(answer, rat(a, b), rat(a + 5, b), rat(a, b + 5), rat(a + 1, b + 1)),
        f"For a fixed distance, time is inversely proportional to speed: "
        f"{b}:{a} = {answer}.",
        {"A": a, "B": b},
    )


def sd_speed_ratio(r, v):
    first, second = pair(v, 14)
    t1, t2 = [(2, 3), (3, 5), (5, 7), (4, 9), (5, 8)][v]
    answer = rat(t2, t1)
    return q(
        "sd_speed_ratio", v,
        f"{first} and {second} cover one identical journey in {t1} hours and "
        f"{t2} hours. {lead(v)} the ratio of their speeds (first to second).",
        answer,
        pick3(answer, rat(t1, t2), rat(t1 + 1, t2), rat(t1, t2 + 1), rat(t1 + 2, t2)),
        f"For the same distance, speed varies inversely with time: "
        f"{t2}:{t1} = {answer}.",
        {"T1": t1, "T2": t2},
    )


def sd_early_late(r, v):
    person, _ = pair(v, 15)
    s1, s2, late, early = [
        (4, 5, 15, 15), (5, 6, 12, 18), (3, 4, 20, 10),
        (6, 8, 10, 20), (3, 5, 24, 16),
    ][v]
    distance = F(s1) * F(s2) * F(late + early) / (F(60) * (F(s2) - F(s1)))
    return q(
        "sd_early_late", v,
        f"{person} is {late} minutes late when walking at {s1} km/h and "
        f"{early} minutes early when walking at {s2} km/h. "
        f"{lead(v)} the distance to the destination, in km.",
        distance,
        pick3(
            distance,
            F(s1 * (late + early), 60),
            F(s2 * (late + early), 60),
            F(s1) * F(s2) * F(late) / (F(60) * (F(s2) - F(s1))),
            F(s1 * s2, late + early),
        ),
        f"Time difference = ({late}+{early})/60 hours. Distance = "
        f"({late}+{early}) x {s1} x {s2}/(60 x ({s2}-{s1})) = {fmt(distance)} km.",
        {"S1": s1, "S2": s2, "Late": late, "Early": early},
    )


def sd_stoppage(r, v):
    person, _ = pair(v, 16)
    s, a = [(60, 48), (80, 50), (75, 60), (90, 60), (40, 30)][v]
    stoppage = F(60) * (F(1) - F(a) / F(s))
    return q(
        "sd_stoppage", v,
        f"{person} can travel at {s} km/h without stopping, but the average falls "
        f"to {a} km/h with stoppages. {lead(v)} the stoppage time per hour, in minutes.",
        stoppage,
        pick3(stoppage, F(60) * F(s - a, a), F(60) * F(a, s), F(3 * (s - a))),
        f"Moving time in an hour = {a}/{s} hour, so stoppage = 60 x "
        f"(1 - {a}/{s}) = {fmt(stoppage)} minutes.",
        {"S": s, "A": a},
    )


def sd_round_trip(r, v):
    traveller, _ = pair(v, 17)
    d, a, b = [(120, 40, 60), (180, 60, 90), (200, 50, 40), (150, 30, 50), (240, 60, 40)][v]
    total = F(d, a) + F(d, b)
    return q(
        "sd_round_trip", v,
        f"{traveller} goes {d} km at {a} km/h and returns the same way at "
        f"{b} km/h. {lead(v)} the total time for the round trip, in hours.",
        total,
        pick3(total, F(2 * d, a + b), F(2 * d, a), F(2 * d, b)),
        f"Outward time = {d}/{a}, return time = {d}/{b}; total = "
        f"{fmt(F(d, a))} + {fmt(F(d, b))} = {fmt(total)} hours.",
        {"D": d, "A": a, "B": b},
    )


def sd_average_three(r, v):
    runner, _ = pair(v, 18)
    a, b, c = [(20, 30, 60), (30, 60, 90), (40, 60, 120), (15, 30, 90), (25, 50, 100)][v]
    average = F(3) / (F(1) / F(a) + F(1) / F(b) + F(1) / F(c))
    return q(
        "sd_average_three", v,
        f"{runner} covers three equal stretches at {a} km/h, {b} km/h and "
        f"{c} km/h. {lead(v)} the average speed for the whole journey.",
        average,
        pick3(average, F(a + b + c, 3), F(a + b + c), F(3) / (F(1) / F(a) + F(1) / F(b))),
        f"Equal distances: average = 3/(1/{a} + 1/{b} + 1/{c}) = "
        f"{fmt(average)} km/h.",
        {"A": a, "B": b, "C": c},
    )


def sd_meet_three(r, v):
    first, second = pair(v, 19)
    third_person = third(v, 4)
    d, a, b, c = [
        (180, 30, 20, 10), (240, 40, 20, 15), (300, 50, 25, 20),
        (150, 30, 20, 10), (360, 60, 30, 15),
    ][v]
    gap_from_second = F(d) * (F(a) + F(b) - F(c)) / (F(a) + F(b))
    return q(
        "sd_meet_three", v,
        f"On a {d} km road, {first} starts from one end at {a} km/h and "
        f"{second} starts from the other end at {b} km/h, moving towards each "
        f"other. At the same moment {third_person} leaves {first}'s end at "
        f"{c} km/h towards {second}. {lead(v)} how far {third_person} is from "
        f"{second} when {first} and {second} meet.",
        gap_from_second,
        pick3(
            gap_from_second,
            F(d) * F(c) / (F(a) + F(b)),
            F(d, a + b),
            F(d) * (F(a) + F(b) + F(c)) / (F(a) + F(b)),
        ),
        f"{first} and {second} meet after {d}/{a + b} hours. By then "
        f"{third_person} has covered {c} x {d}/{a + b} km, so the remaining gap "
        f"is {fmt(gap_from_second)} km.",
        {"D": d, "A": a, "B": b, "C": c},
    )


def sd_cross_each_other(r, v):
    first, second = pair(v, 20)
    lap, a, b = [(12, 8, 2), (18, 9, 6), (24, 10, 4), (15, 7, 5), (20, 12, 8)][v]
    cross_time = F(lap, a - b)
    return q(
        "sd_cross_each_other", v,
        f"On a circular track of {lap} km, {first} and {second} start together "
        f"from the same point and run in the same direction at {a} km/h and "
        f"{b} km/h. {lead(v)} the time until {first} first crosses {second}, "
        "in hours.",
        cross_time,
        pick3(cross_time, F(lap, a + b), F(lap, a), F(lap, b)),
        f"Relative speed = {a} - {b} = {a - b} km/h; one lap is gained in "
        f"{lap}/{a - b} = {fmt(cross_time)} hours.",
        {"L": lap, "A": a, "B": b},
    )


def sd_diff_distance(r, v):
    first, second = pair(v, 21)
    a, t1, b, t2 = [(30, 2, 20, 2), (40, 3, 25, 4), (50, 2, 30, 3), (45, 4, 35, 5), (75, 2, 40, 3)][v]
    difference = abs(F(a) * F(t1) - F(b) * F(t2))
    return q(
        "sd_diff_distance", v,
        f"{first} travels at {a} km/h for {t1} hours while {second} travels at "
        f"{b} km/h for {t2} hours. {lead(v)} the difference between the distances "
        "they cover, in km.",
        difference,
        pick3(difference, F(a * t1 + b * t2), F(a * t1), F(b * t2)),
        f"Distances are {a} x {t1} = {a * t1} km and {b} x {t2} = {b * t2} km; "
        f"difference = {fmt(difference)} km.",
        {"A": a, "T1": t1, "B": b, "T2": t2},
    )


def sd_unit_conversion_mix(r, v):
    person, _ = pair(v, 22)
    metres, seconds = [(300, 30), (450, 30), (600, 40), (800, 50), (500, 25)][v]
    kmph = F(metres) * F(18) / F(5) / F(seconds)
    return q(
        "sd_unit_conversion_mix", v,
        f"{person} covers {metres} metres in {seconds} seconds. "
        f"{lead(v)} the speed in km/h.",
        kmph,
        pick3(kmph, F(metres, seconds), F(metres, seconds) * 3, F(metres) * F(18, 5)),
        f"Speed = {metres}/{seconds} = {fmt(F(metres, seconds))} m/s; "
        f"x 18/5 gives {fmt(kmph)} km/h.",
        {"Metres": metres, "Seconds": seconds},
    )


def sd_compare(r, v):
    first, second = pair(v, 23)
    a, b = [(35, 5), (49, 10), (25, 5), (55, 15), (65, 20)][v]
    b_kmph = F(b) * F(18, 5)
    assert b_kmph.denominator == 1
    answer = rat(a, int(b_kmph))
    return q(
        "sd_compare", v,
        f"{first} moves at {a} km/h while {second} moves at {b} m/s. "
        f"{lead(v)} the ratio of their speeds (first to second), with both "
        "speeds in km/h.",
        answer,
        pick3(
            answer,
            rat(int(b_kmph), a),
            rat(a, int(b_kmph) + 5),
            rat(a + 5, int(b_kmph)),
            rat(a, int(b_kmph) + 1),
        ),
        f"{b} m/s = {b} x 18/5 = {fmt(b_kmph)} km/h, so the ratio is "
        f"{a}:{fmt(b_kmph)} = {answer}.",
        {"A": a, "B": b},
    )


FAMILIES = (
    sd_basic_speed,
    sd_basic_time,
    sd_basic_distance,
    sd_kmph_to_mps,
    sd_mps_to_kmph,
    sd_average_two_legs,
    sd_same_direction,
    sd_opposite_direction,
    sd_meeting,
    sd_chase,
    sd_head_start,
    sd_two_legs_time,
    sd_distance_ratio,
    sd_time_ratio,
    sd_speed_ratio,
    sd_early_late,
    sd_stoppage,
    sd_round_trip,
    sd_average_three,
    sd_meet_three,
    sd_cross_each_other,
    sd_diff_distance,
    sd_unit_conversion_mix,
    sd_compare,
)


def build_speed_time_distance():
    return build_specs(FAMILIES)
