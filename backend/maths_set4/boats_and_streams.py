# -*- coding: utf-8 -*-
"""Boats and Streams - 120 verified questions for the fourth Maths batch."""

from __future__ import annotations

import math
from fractions import Fraction

from .bank import fmt
from .common import build_specs, pair, q, third

SOURCE = "Boats and Streams topic-wise mains sets (local PDFs)"
PAGES = {
    1: "Mains_Topic_wise_Boats_and_Stream_Set_-1_(Mains).pdf, pp. 1-9",
    2: "Mains_Topic_wise_Boats_and_Stream_Set_-2_(Mains).pdf, pp. 1-12",
    3: "Mains_Topic_wise_Boats_and_Stream_Set_-3_(Mains).pdf, pp. 1-8",
    4: "Mains_Topic_wise_Boats_and_Stream_Set_-4_(Mains).pdf, pp. 1-7",
}

ASK = ("What is", "Find", "Determine", "Calculate", "Work out")


F = Fraction


def rat(a, b):
    """Return a reduced integer ratio string from two exact values."""
    x, y = F(a), F(b)
    scale = math.lcm(x.denominator, y.denominator)
    first = x.numerator * (scale // x.denominator)
    second = y.numerator * (scale // y.denominator)
    g = math.gcd(abs(first), abs(second)) or 1
    return f"{first // g}:{second // g}"


# ---------------------------------------------------------------------------
# 24 families, five preset input tuples each.
# ---------------------------------------------------------------------------

def bs_downstream(rng, variant):
    a, _ = pair(variant, 0)
    presets = [(12, 3), (15, 4), (18, 2), (20, 5), (24, 4)]
    still, stream = presets[variant]
    answer = F(still + stream)
    return q(
        "bs_downstream", variant,
        f"{a} rows a boat with a still-water speed of {still} km/h while the "
        f"stream runs at {stream} km/h. {ASK[variant]} the downstream speed?",
        answer,
        [F(still - stream), F(still), F(still + 2 * stream)],
        f"Downstream speed = still-water speed + stream speed = "
        f"{still} + {stream} = {fmt(answer)} km/h.",
        {"Still": still, "Stream": stream},
    )


def bs_upstream(rng, variant):
    _, b = pair(variant, 1)
    presets = [(14, 3), (16, 4), (21, 5), (25, 6), (30, 7)]
    still, stream = presets[variant]
    answer = F(still - stream)
    return q(
        "bs_upstream", variant,
        f"A launch with still-water speed {still} km/h is rowed by {b} against "
        f"a current of {stream} km/h. {ASK[variant]} its upstream speed?",
        answer,
        [F(still + stream), F(still), F(still - 2 * stream)],
        f"Upstream speed = still-water speed - stream speed = "
        f"{still} - {stream} = {fmt(answer)} km/h.",
        {"Still": still, "Stream": stream},
    )


def bs_still_from_speeds(rng, variant):
    a, _ = pair(variant, 2)
    presets = [(15, 9), (18, 12), (20, 14), (24, 16), (30, 20)]
    down, up = presets[variant]
    answer = F(down + up, 2)
    return q(
        "bs_still_from_speeds", variant,
        f"Travelling with the current, {a}'s boat is timed at {down} km/h; "
        f"returning against it, the speed is {up} km/h. "
        f"{ASK[variant]} the speed in still water?",
        answer,
        [F(down - up, 2), F(down), F(up)],
        f"Still-water speed = (downstream + upstream)/2 = "
        f"({down} + {up})/2 = {fmt(answer)} km/h.",
        {"Down": down, "Up": up},
    )


def bs_stream_from_speeds(rng, variant):
    _, b = pair(variant, 3)
    presets = [(15, 9), (18, 10), (22, 14), (25, 15), (28, 18)]
    down, up = presets[variant]
    answer = F(down - up, 2)
    return q(
        "bs_stream_from_speeds", variant,
        f"The downstream and upstream speeds of {b}'s launch are {down} km/h "
        f"and {up} km/h respectively. {ASK[variant]} the speed of the current?",
        answer,
        [F(down + up, 2), F(down - up), F(down, 2)],
        f"Stream speed = (downstream - upstream)/2 = "
        f"({down} - {up})/2 = {fmt(answer)} km/h.",
        {"Down": down, "Up": up},
    )


def bs_down_distance(rng, variant):
    a, _ = pair(variant, 4)
    presets = [(12, 3, 4), (15, 4, 3), (18, 2, 5), (20, 5, 2), (24, 4, 6)]
    still, stream, hours = presets[variant]
    answer = F((still + stream) * hours)
    return q(
        "bs_down_distance", variant,
        f"With a still-water speed of {still} km/h and a following current of "
        f"{stream} km/h, how far does {a}'s boat travel downstream in "
        f"{hours} hours?",
        answer,
        [F((still - stream) * hours), F(still * hours), F(still * hours + stream)],
        f"Downstream speed = {still} + {stream} = {still + stream} km/h; "
        f"distance = {still + stream} x {hours} = {fmt(answer)} km.",
        {"Still": still, "Stream": stream, "Time": hours},
    )


def bs_up_time(rng, variant):
    _, b = pair(variant, 5)
    presets = [(42, 12, 3), (40, 15, 5), (50, 18, 3), (44, 20, 6), (70, 24, 4)]
    distance, still, stream = presets[variant]
    answer = F(distance, still - stream)
    return q(
        "bs_up_time", variant,
        f"{b} must cover {distance} km upstream. If the boat's still-water "
        f"speed is {still} km/h and the current is {stream} km/h, how many "
        f"hours does the journey take?",
        answer,
        [
            F(distance, still + stream),
            F(distance, still),
            F(distance, still - stream + 1),
        ],
        f"Upstream speed = {still} - {stream} = {still - stream} km/h; "
        f"time = {distance}/{still - stream} = {fmt(answer)} hours.",
        {"Distance": distance, "Still": still, "Stream": stream},
    )


def bs_round_trip(rng, variant):
    a, _ = pair(variant, 6)
    presets = [(12, 3, 36), (15, 5, 40), (18, 2, 40), (20, 4, 48), (24, 6, 54)]
    still, stream, distance = presets[variant]
    answer = F(distance, still + stream) + F(distance, still - stream)
    return q(
        "bs_round_trip", variant,
        f"{a}'s launch goes {distance} km with the stream and then returns "
        f"the same {distance} km against it. With still-water speed {still} "
        f"km/h and current {stream} km/h, {ASK[variant]} the total travel time?",
        answer,
        [
            F(2 * distance, still),
            F(distance, still + stream),
            F(distance, still - stream),
        ],
        f"Downstream time = {distance}/{still + stream} and upstream time = "
        f"{distance}/{still - stream}; total = {fmt(answer)} hours.",
        {"Distance": distance, "Still": still, "Stream": stream},
    )


def bs_still_from_round(rng, variant):
    _, b = pair(variant, 7)
    presets = [(12, 3, 45, 8), (15, 5, 40, 6), (18, 2, 80, 9),
               (20, 4, 48, 5), (24, 6, 45, 4)]
    still, stream, distance, hours = presets[variant]
    answer = F(still)
    return q(
        "bs_still_from_round", variant,
        f"A boat covers {distance} km downstream and the same distance back. "
        f"The whole round trip takes {hours} hours in a current of {stream} "
        f"km/h. {ASK[variant]} the still-water speed, as timed by {b}?",
        answer,
        [F(still - stream), F(still + stream), F(distance, hours)],
        f"With still speed s, {distance}/(s+{stream}) + "
        f"{distance}/(s-{stream}) = {hours}; solving gives s = "
        f"({distance} + sqrt({distance}^2 + {hours}^2 x {stream}^2))/{hours} "
        f"= {fmt(answer)} km/h.",
        {"Distance": distance, "Time": hours, "Stream": stream},
    )


def bs_stream_from_round(rng, variant):
    a, _ = pair(variant, 8)
    presets = [(12, 3, 45, 8), (15, 5, 40, 6), (18, 2, 80, 9),
               (20, 4, 48, 5), (24, 6, 45, 4)]
    still, stream, distance, hours = presets[variant]
    answer = F(stream)
    return q(
        "bs_stream_from_round", variant,
        f"Over a journey of {distance} km each way, {a} records a total of "
        f"{hours} hours. The boat's still-water speed is {still} km/h. "
        f"{ASK[variant]} the speed of the stream?",
        answer,
        [F(still, 2), F(still), F(distance, hours)],
        f"The round trip gives {hours} = 2 x {distance} x {still}/"
        f"({still}^2 - c^2); hence c = sqrt({still}^2 - "
        f"2 x {distance} x {still}/{hours}) = {fmt(answer)} km/h.",
        {"Distance": distance, "Time": hours, "Still": still},
    )


def bs_ratio_up_down(rng, variant):
    _, b = pair(variant, 9)
    presets = [(1, 2), (2, 3), (3, 5), (1, 3), (2, 5)]
    up, down = presets[variant]
    answer = rat(down + up, down - up)
    return q(
        "bs_ratio_up_down", variant,
        f"For {b}'s boat the upstream and downstream speeds are in the ratio "
        f"{up}:{down}. {ASK[variant]} the ratio of the still-water speed to "
        f"the speed of the current?",
        answer,
        [rat(down - up, down + up), rat(down, up), rat(up, down)],
        f"Still speed = (down + up)/2 and stream speed = (down - up)/2, so "
        f"the ratio is ({down} + {up}):({down} - {up}) = {answer}.",
        {"Up": up, "Down": down},
    )


def bs_between_points(rng, variant):
    a, _ = pair(variant, 10)
    place = third(variant, 12)
    presets = [(3, 2, 3), (4, 2, 4), (2, 3, 6), (5, 2, 5), (3, 4, 8)]
    stream, down_time, up_time = presets[variant]
    answer = F(2 * stream * down_time * up_time, up_time - down_time)
    return q(
        "bs_between_points", variant,
        f"{a} rows from a jetty to {place}'s landing. The downstream trip "
        f"takes {down_time} hours and the return upstream takes {up_time} "
        f"hours. If the current runs at {stream} km/h, {ASK[variant]} the "
        f"distance between the two landings?",
        answer,
        [
            F(stream * (down_time + up_time)),
            F(2 * stream * down_time * up_time, down_time + up_time),
            F(stream * (up_time - down_time)),
        ],
        f"Equating distances gives distance = 2 x {stream} x {down_time} x "
        f"{up_time}/({up_time} - {down_time}) = {fmt(answer)} km.",
        {"Stream": stream, "DownTime": down_time, "UpTime": up_time},
    )


def bs_two_boats(rng, variant):
    a, _ = pair(variant, 11)
    c, _ = pair(variant, 14)
    presets = [(18, 12, 3, 4), (20, 14, 4, 3), (25, 15, 2, 5),
               (16, 11, 5, 6), (22, 17, 3, 2)]
    first, second, stream, hours = presets[variant]
    answer = F(abs(first - second) * hours)
    return q(
        "bs_two_boats", variant,
        f"{a} and {c} start together in the same current of {stream} km/h. "
        f"Their still-water speeds are {first} km/h and {second} km/h. "
        f"How far apart are they after {hours} hours if both go downstream?",
        answer,
        [
            F((first + second) * hours),
            F((first - second + 2 * stream) * hours),
            F(abs(first - second) * hours, 2),
        ],
        f"Both boats gain the same current speed, so their separation grows "
        f"at |{first} - {second}| = {abs(first - second)} km/h; gap = "
        f"{fmt(answer)} km.",
        {"Still1": first, "Still2": second, "Stream": stream, "Time": hours},
    )


def bs_row_against(rng, variant):
    a, _ = pair(variant, 12)
    presets = [(12, 20, 2), (15, 36, 3), (18, 28, 2), (20, 42, 3), (25, 88, 4)]
    still, distance, hours = presets[variant]
    answer = F(still) - F(distance, hours)
    return q(
        "bs_row_against", variant,
        f"Rowing against the current, {a} covers {distance} km in {hours} "
        f"hours. If the still-water speed is {still} km/h, {ASK[variant]} "
        f"the speed of the current?",
        answer,
        [
            F(distance, hours),
            F(still) + F(distance, hours),
            F(still) - F(distance, 2 * hours),
        ],
        f"Upstream speed = {distance}/{hours}; current = {still} - "
        f"{distance}/{hours} = {fmt(answer)} km/h.",
        {"Still": still, "Distance": distance, "Time": hours},
    )


def bs_current_effect(rng, variant):
    a, _ = pair(variant, 13)
    presets = [(12, 3), (15, 4), (18, 2), (20, 5), (24, 6)]
    still, stream = presets[variant]
    answer = F(2 * stream)
    return q(
        "bs_current_effect", variant,
        f"For {a}'s launch the still-water speed is {still} km/h and the "
        f"stream speed is {stream} km/h. By how many km/h does the downstream "
        f"speed exceed the upstream speed?",
        answer,
        [F(stream), F(still + stream), F(still - stream)],
        f"Downstream - upstream = ({still} + {stream}) - ({still} - "
        f"{stream}) = 2 x {stream} = {fmt(answer)} km/h.",
        {"Still": still, "Stream": stream},
    )


def bs_speed_diff(rng, variant):
    a, _ = pair(variant, 14)
    b, _ = pair(variant, 17)
    presets = [(12, 3, 4), (15, 4, 3), (18, 2, 5), (20, 5, 2), (24, 6, 6)]
    still, stream, hours = presets[variant]
    answer = F(2 * stream * hours)
    return q(
        "bs_speed_diff", variant,
        f"{a} travels downstream and {b} travels upstream, both starting "
        f"together with still-water speed {still} km/h in a current of "
        f"{stream} km/h. How far apart are they after {hours} hours?",
        answer,
        [F(stream * hours), F(still * hours), F(2 * still * hours)],
        f"Relative speed = (still + current) - (still - current) = 2 x "
        f"{stream} = {2 * stream} km/h; gap = {fmt(answer)} km.",
        {"Still": still, "Stream": stream, "Time": hours},
    )


def bs_time_diff(rng, variant):
    a, _ = pair(variant, 15)
    presets = [(12, 3, 36), (15, 5, 40), (18, 2, 40), (20, 4, 48), (24, 6, 54)]
    still, stream, distance = presets[variant]
    answer = F(distance, still - stream) - F(distance, still + stream)
    return q(
        "bs_time_diff", variant,
        f"{a}'s boat travels {distance} km downstream and the same {distance} "
        f"km upstream. With still-water speed {still} km/h and current "
        f"{stream} km/h, how much longer is the upstream leg?",
        answer,
        [F(2 * distance, still), F(distance, still - stream), F(distance, 2 * still)],
        f"Difference = {distance}/({still} - {stream}) - {distance}/"
        f"({still} + {stream}) = {fmt(answer)} hours.",
        {"Distance": distance, "Still": still, "Stream": stream},
    )


def bs_man_row(rng, variant):
    a, _ = pair(variant, 16)
    observer = third(variant, 18)
    presets = [(30, 2, 18, 3), (36, 3, 20, 4), (40, 4, 24, 6),
               (45, 3, 28, 4), (50, 5, 30, 6)]
    down_distance, down_time, up_distance, up_time = presets[variant]
    answer = (F(down_distance, down_time) - F(up_distance, up_time)) / 2
    return q(
        "bs_man_row", variant,
        f"As {observer} times the trips, {a} rows {down_distance} km "
        f"downstream in {down_time} hours and {up_distance} km upstream in "
        f"{up_time} hours. {ASK[variant]} the speed of the current?",
        answer,
        [
            F(down_distance, down_time) - F(up_distance, up_time),
            F(down_distance, down_time),
            (F(down_distance, down_time) + F(up_distance, up_time)) / 2,
        ],
        f"Downstream speed = {down_distance}/{down_time}, upstream speed = "
        f"{up_distance}/{up_time}; current = (down - up)/2 = "
        f"{fmt(answer)} km/h.",
        {
            "DownDist": down_distance,
            "DownTime": down_time,
            "UpDist": up_distance,
            "UpTime": up_time,
        },
    )


def bs_float(rng, variant):
    a, _ = pair(variant, 17)
    presets = [(12, 3, 5), (15, 4, 6), (18, 2, 7), (20, 5, 4), (24, 6, 8)]
    still, stream, hours = presets[variant]
    answer = F(stream * hours)
    return q(
        "bs_float", variant,
        f"{a} rows upstream with still-water speed {still} km/h in a current "
        f"of {stream} km/h. After {hours} hours a cork dropped at the starting "
        f"point is noticed. How far has the cork drifted from that point?",
        answer,
        [
            F((still + stream) * hours),
            F((still - stream) * hours),
            F(stream * hours, 2),
        ],
        f"A floating cork moves with the current alone, so drift = "
        f"{stream} x {hours} = {fmt(answer)} km.",
        {"Still": still, "Stream": stream, "Time": hours},
    )


def bs_average_round(rng, variant):
    a, _ = pair(variant, 18)
    presets = [(12, 3), (15, 5), (18, 2), (20, 4), (24, 6)]
    still, stream = presets[variant]
    answer = F(still ** 2 - stream ** 2, still)
    return q(
        "bs_average_round", variant,
        f"{a}'s boat makes a round trip over equal distances. Its "
        f"still-water speed is {still} km/h and the stream runs at {stream} "
        f"km/h. {ASK[variant]} the average speed for the whole journey?",
        answer,
        [F(still), F(still - stream), F(still + stream)],
        f"Average speed over equal distances = 2(s+c)(s-c)/((s+c)+(s-c)) = "
        f"(s^2 - c^2)/s = ({still}^2 - {stream}^2)/{still} = "
        f"{fmt(answer)} km/h.",
        {"Still": still, "Stream": stream},
    )


def bs_return_time(rng, variant):
    a, _ = pair(variant, 19)
    landing = third(variant, 0)
    presets = [(12, 3, 2), (15, 5, 3), (18, 2, 4), (20, 4, 2), (24, 6, 5)]
    still, stream, down_time = presets[variant]
    answer = F(down_time * (still + stream), still - stream)
    return q(
        "bs_return_time", variant,
        f"Rowing downstream to {landing} Ghat, {a} takes {down_time} hours. "
        f"With still-water speed {still} km/h and current {stream} km/h, how "
        f"long will the return journey upstream take?",
        answer,
        [
            F(down_time * (still - stream), still + stream),
            F(down_time),
            F(down_time * (still + 2 * stream), still - stream),
        ],
        f"The distance is the same both ways, so return time = {down_time} x "
        f"({still} + {stream})/({still} - {stream}) = {fmt(answer)} hours.",
        {"Still": still, "Stream": stream, "DownTime": down_time},
    )


def bs_kmph_conversion(rng, variant):
    a, _ = pair(variant, 0)
    observer = third(variant, 2)
    presets = [(4, 1), (5, 2), (6, 3), (8, 2), (10, 4)]
    still_ms, stream_ms = presets[variant]
    answer = F((still_ms + stream_ms) * 18, 5)
    return q(
        "bs_kmph_conversion", variant,
        f"The launch monitored by {observer} has still-water speed "
        f"{still_ms} m/s and {a} reports a current of {stream_ms} m/s. "
        f"{ASK[variant]} the downstream speed in km/h?",
        answer,
        [
            F((still_ms - stream_ms) * 18, 5),
            F(still_ms + stream_ms),
            F(still_ms * 18, 5),
        ],
        f"Downstream speed = {still_ms} + {stream_ms} = "
        f"{still_ms + stream_ms} m/s; x 18/5 gives {fmt(answer)} km/h.",
        {"StillMs": still_ms, "StreamMs": stream_ms},
    )


def bs_distance_time_diff(rng, variant):
    a, _ = pair(variant, 2)
    presets = [(12, 3, 45, 2), (15, 5, 40, 2), (18, 2, 80, 1),
               (20, 4, 48, 1), (24, 6, 45, 1)]
    still, stream, distance, time_diff = presets[variant]
    answer = F(stream)
    return q(
        "bs_distance_time_diff", variant,
        f"{a} rows {distance} km downstream and the same distance upstream. "
        f"The upstream leg takes {time_diff} hours longer, and the "
        f"still-water speed is {still} km/h. {ASK[variant]} the speed of the "
        f"current?",
        answer,
        [F(still), F(2 * distance, time_diff), F(distance, 2 * time_diff)],
        f"From {distance}/(s-c) - {distance}/(s+c) = {time_diff}, "
        f"c = (sqrt({distance}^2 + {time_diff}^2 x {still}^2) - "
        f"{distance})/{time_diff} = {fmt(answer)} km/h.",
        {"Distance": distance, "Still": still, "TimeDiff": time_diff},
    )


def bs_relative_boats(rng, variant):
    a, _ = pair(variant, 3)
    b, _ = pair(variant, 6)
    presets = [(12, 18, 3, 2), (15, 20, 4, 3), (18, 24, 2, 4),
               (20, 28, 5, 2), (24, 30, 6, 5)]
    first, second, stream, hours = presets[variant]
    answer = F((first + second) * hours)
    return q(
        "bs_relative_boats", variant,
        f"{a} heads downstream and {b} heads upstream from the same point in "
        f"a stream of {stream} km/h. Their still-water speeds are {first} "
        f"km/h and {second} km/h. How far apart are they after {hours} hours?",
        answer,
        [
            F((first + second + 2 * stream) * hours),
            F((first + second - stream) * hours),
            F((first + second) * hours, 2),
        ],
        f"Relative speed = ({first} + {stream}) + ({second} - {stream}) = "
        f"{first + second} km/h; separation = {fmt(answer)} km.",
        {"Still1": first, "Still2": second, "Stream": stream, "Time": hours},
    )


def bs_compare(rng, variant):
    name1, _ = pair(variant, 4)
    _, name2 = pair(variant, 7)
    presets = [(12, 3, 20), (15, 4, 18), (10, 5, 22), (18, 2, 16), (14, 3, 20)]
    first, stream, second = presets[variant]
    speed1, speed2 = F(first + stream), F(second - stream)
    answer = name1 if speed1 > speed2 else name2 if speed2 > speed1 else "Both are equal"
    distractors = [name2, name1, "Both are equal", "Cannot be determined"]
    distractors = [item for item in distractors if item != answer][:3]
    return q(
        "bs_compare", variant,
        f"{name1} has still-water speed {first} km/h and {name2} has "
        f"{second} km/h. In a current of {stream} km/h, {name1} travels "
        f"downstream while {name2} travels upstream. Whose actual speed is "
        f"greater?",
        answer,
        distractors,
        f"Actual speeds are {fmt(speed1)} km/h and {fmt(speed2)} km/h; "
        f"comparison gives {answer}.",
        {
            "Still1": first,
            "Still2": second,
            "Stream": stream,
            "Name1": name1,
            "Name2": name2,
        },
    )


FAMILIES = [
    bs_downstream,
    bs_upstream,
    bs_still_from_speeds,
    bs_stream_from_speeds,
    bs_down_distance,
    bs_up_time,
    bs_round_trip,
    bs_still_from_round,
    bs_stream_from_round,
    bs_ratio_up_down,
    bs_between_points,
    bs_two_boats,
    bs_row_against,
    bs_current_effect,
    bs_speed_diff,
    bs_time_diff,
    bs_man_row,
    bs_float,
    bs_average_round,
    bs_return_time,
    bs_kmph_conversion,
    bs_distance_time_diff,
    bs_relative_boats,
    bs_compare,
]


def build_boats_and_streams():
    return build_specs(FAMILIES)
