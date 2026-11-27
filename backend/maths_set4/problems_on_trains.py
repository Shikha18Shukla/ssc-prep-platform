# -*- coding: utf-8 -*-
"""Problems on Trains - 120 verified questions for the fourth Maths batch."""

from __future__ import annotations

from fractions import Fraction

from .bank import fmt
from .common import build_specs, pair, q, third

SOURCE = "Problems on Trains topic-wise mains sets (local PDFs)"
PAGES = {
    1: "Mains_Topic_wise_Problems_on_Trains_Set_-1_(Mains).pdf, pp. 1-7",
    2: "Mains_Topic_wise_Problems_on_Trains_Set_-2_(Mains).pdf, pp. 1-3",
    3: "Mains_Topic_wise_Problems_on_Trains_Set_-3_(Mains).pdf, pp. 1-8",
    4: "Mains_Topic_wise_Problems_on_Trains_Set_-4_(Mains).pdf, pp. 1-7",
}

TRAIN_KINDS = (
    "goods train",
    "express train",
    "passenger train",
    "local train",
    "mail train",
)


def _mps(speed_kmph):
    """kmph -> m/s, exactly."""
    return Fraction(speed_kmph) * Fraction(5, 18)


def _kmph(speed_mps):
    """m/s -> kmph, exactly."""
    return Fraction(speed_mps) * Fraction(18, 5)


def _ratio(first, second):
    reduced = Fraction(first, second)
    return f"{reduced.numerator}:{reduced.denominator}"


def _distinct(correct, *candidates):
    """Three unique, plausible wrong answers as display strings."""
    seen = {fmt(correct)}
    out: list[str] = []
    for value in candidates:
        text = fmt(value)
        if text not in seen:
            seen.add(text)
            out.append(text)
        if len(out) == 3:
            break
    step = 1
    while len(out) < 3:
        try:
            base = Fraction(correct)
        except (ValueError, ZeroDivisionError):
            base = Fraction(len(seen) + step)
        for value in (base + step, base - step):
            text = fmt(value)
            if text not in seen:
                seen.add(text)
                out.append(text)
                if len(out) == 3:
                    break
        step += 1
    return out


def tr_cross_pole(rng, variant):
    presets = ((72, 360), (54, 300), (90, 450), (36, 240), (108, 480))
    speed, length = presets[variant % len(presets)]
    a, _ = pair(variant, 0)
    kind = TRAIN_KINDS[variant % len(TRAIN_KINDS)]
    speed_mps = _mps(speed)
    answer = Fraction(length) / speed_mps
    text = (
        f"A {length} m long {kind} passes a pole near {a}'s house at "
        f"{speed} kmph. In how many seconds does it cross the pole?"
    )
    explanation = (
        f"Speed = {speed} x 5/18 = {fmt(speed_mps)} m/s; time to cross a pole "
        f"= train length / speed = {length}/{fmt(speed_mps)} = {fmt(answer)} s."
    )
    return q(
        "tr_cross_pole", variant, text, answer,
        _distinct(
            answer,
            Fraction(length, speed),
            Fraction(length * 5, 18 * speed),
            Fraction(length, 2) / speed_mps,
        ),
        explanation,
        {"Speed": speed, "Length": length},
    )


def tr_cross_platform(rng, variant):
    presets = (
        (54, 180, 270), (60, 200, 300), (72, 150, 250),
        (90, 240, 360), (108, 300, 450),
    )
    speed, train_length, platform_length = presets[variant % len(presets)]
    a, b = pair(variant, 1)
    kind = TRAIN_KINDS[variant % len(TRAIN_KINDS)]
    speed_mps = _mps(speed)
    answer = Fraction(train_length + platform_length) / speed_mps
    text = (
        f"A {train_length} m {kind} starts from {a} and runs past the "
        f"{platform_length} m platform at {b} at {speed} kmph. How many "
        "seconds does it take to clear the platform completely?"
    )
    explanation = (
        f"Distance covered = {train_length} + {platform_length} = "
        f"{train_length + platform_length} m; speed = {fmt(speed_mps)} m/s; "
        f"time = {fmt(answer)} s."
    )
    return q(
        "tr_cross_platform", variant, text, answer,
        _distinct(
            answer,
            Fraction(train_length) / speed_mps,
            Fraction(platform_length) / speed_mps,
            Fraction(train_length + platform_length, speed),
        ),
        explanation,
        {
            "Speed": speed,
            "TrainLength": train_length,
            "PlatformLength": platform_length,
        },
    )


def tr_cross_bridge(rng, variant):
    presets = (
        (160, 240, 16), (120, 180, 18), (180, 270, 15),
        (200, 100, 12), (250, 350, 24),
    )
    train_length, bridge_length, time = presets[variant % len(presets)]
    a, b = pair(variant, 2)
    kind = TRAIN_KINDS[variant % len(TRAIN_KINDS)]
    answer = _kmph(Fraction(train_length + bridge_length, time))
    text = (
        f"A {kind} of length {train_length} m crosses the {bridge_length} m "
        f"bridge between {a} Nagar and {b} Nagar in {time} s. Find its speed "
        "in kmph."
    )
    explanation = (
        f"Total distance = {train_length} + {bridge_length} = "
        f"{train_length + bridge_length} m; speed = "
        f"{train_length + bridge_length}/{time} = "
        f"{fmt(Fraction(train_length + bridge_length, time))} m/s = "
        f"{fmt(answer)} kmph."
    )
    return q(
        "tr_cross_bridge", variant, text, answer,
        _distinct(
            answer,
            _kmph(Fraction(train_length, time)),
            _kmph(Fraction(bridge_length, time)),
            Fraction(train_length + bridge_length, time),
        ),
        explanation,
        {
            "TrainLength": train_length,
            "BridgeLength": bridge_length,
            "Time": time,
        },
    )


def tr_cross_man_same(rng, variant):
    presets = (
        (250, 72, 27), (225, 54, 9), (300, 90, 18),
        (350, 108, 18), (200, 60, 15),
    )
    train_length, train_speed, man_speed = presets[variant % len(presets)]
    a, b = pair(variant, 3)
    man = third(variant)
    kind = TRAIN_KINDS[variant % len(TRAIN_KINDS)]
    relative_mps = _mps(train_speed - man_speed)
    answer = Fraction(train_length) / relative_mps
    text = (
        f"{man} walks at {man_speed} kmph from {a} towards {b}. A "
        f"{train_length} m {kind} going the same way at {train_speed} kmph "
        "overtakes him. How long does the train take to pass him?"
    )
    explanation = (
        f"Same direction: relative speed = {train_speed} - {man_speed} = "
        f"{train_speed - man_speed} kmph = {fmt(relative_mps)} m/s; time = "
        f"{train_length}/{fmt(relative_mps)} = {fmt(answer)} s."
    )
    return q(
        "tr_cross_man_same", variant, text, answer,
        _distinct(
            answer,
            Fraction(train_length) / _mps(train_speed),
            Fraction(train_length) / _mps(man_speed),
            Fraction(train_length, train_speed - man_speed),
        ),
        explanation,
        {
            "TrainLength": train_length,
            "TrainSpeed": train_speed,
            "ManSpeed": man_speed,
        },
    )


def tr_cross_man_opposite(rng, variant):
    presets = (
        (200, 54, 18), (300, 72, 18), (240, 60, 12),
        (360, 90, 18), (280, 63, 9),
    )
    train_length, train_speed, man_speed = presets[variant % len(presets)]
    a, b = pair(variant, 4)
    man = third(variant)
    kind = TRAIN_KINDS[variant % len(TRAIN_KINDS)]
    relative_mps = _mps(train_speed + man_speed)
    answer = Fraction(train_length) / relative_mps
    text = (
        f"{man} walks from {b} to {a} at {man_speed} kmph while a "
        f"{train_length} m {kind} moves the other way at {train_speed} kmph. "
        "How many seconds does the train take to cross him?"
    )
    explanation = (
        f"Opposite directions: relative speed = {train_speed} + {man_speed} = "
        f"{train_speed + man_speed} kmph = {fmt(relative_mps)} m/s; time = "
        f"{train_length}/{fmt(relative_mps)} = {fmt(answer)} s."
    )
    return q(
        "tr_cross_man_opposite", variant, text, answer,
        _distinct(
            answer,
            Fraction(train_length) / _mps(train_speed),
            Fraction(train_length) / _mps(man_speed),
            Fraction(train_length, train_speed + man_speed),
        ),
        explanation,
        {
            "TrainLength": train_length,
            "TrainSpeed": train_speed,
            "ManSpeed": man_speed,
        },
    )


def tr_two_opposite(rng, variant):
    presets = (
        (120, 180, 36, 54), (150, 200, 45, 45), (100, 140, 36, 36),
        (200, 250, 54, 36), (160, 200, 63, 45),
    )
    length1, length2, speed1, speed2 = presets[variant % len(presets)]
    a, b = pair(variant, 5)
    kind1 = TRAIN_KINDS[variant % len(TRAIN_KINDS)]
    kind2 = TRAIN_KINDS[(variant + 2) % len(TRAIN_KINDS)]
    total_length = length1 + length2
    answer = Fraction(total_length) / _mps(speed1 + speed2)
    text = (
        f"The {length1} m {kind1} from {a} and the {length2} m {kind2} from "
        f"{b} run towards each other at {speed1} kmph and {speed2} kmph. "
        "How long do they take to cross each other?"
    )
    explanation = (
        f"Opposite directions: relative speed = {speed1} + {speed2} = "
        f"{speed1 + speed2} kmph = {fmt(_mps(speed1 + speed2))} m/s; total "
        f"length = {total_length} m; time = {fmt(answer)} s."
    )
    return q(
        "tr_two_opposite", variant, text, answer,
        _distinct(
            answer,
            Fraction(total_length) / _mps(speed1),
            Fraction(total_length) / _mps(speed2),
            Fraction(total_length, speed1 + speed2),
        ),
        explanation,
        {
            "Length1": length1,
            "Length2": length2,
            "Speed1": speed1,
            "Speed2": speed2,
        },
    )


def tr_two_same(rng, variant):
    presets = (
        (120, 180, 72, 54), (100, 150, 90, 54), (150, 200, 81, 45),
        (200, 250, 108, 72), (180, 220, 90, 54),
    )
    length1, length2, fast_speed, slow_speed = presets[variant % len(presets)]
    a, b = pair(variant, 6)
    kind1 = TRAIN_KINDS[variant % len(TRAIN_KINDS)]
    kind2 = TRAIN_KINDS[(variant + 3) % len(TRAIN_KINDS)]
    total_length = length1 + length2
    answer = Fraction(total_length) / _mps(fast_speed - slow_speed)
    text = (
        f"A {length1} m {kind1} at {fast_speed} kmph follows a {length2} m "
        f"{kind2} at {slow_speed} kmph from {a} towards {b}. How many "
        "seconds does the faster train take to overtake the slower one?"
    )
    explanation = (
        f"Same direction: relative speed = {fast_speed} - {slow_speed} = "
        f"{fast_speed - slow_speed} kmph = "
        f"{fmt(_mps(fast_speed - slow_speed))} m/s; total length = "
        f"{total_length} m; time = {fmt(answer)} s."
    )
    return q(
        "tr_two_same", variant, text, answer,
        _distinct(
            answer,
            Fraction(total_length) / _mps(fast_speed),
            Fraction(total_length) / _mps(slow_speed),
            Fraction(total_length, fast_speed - slow_speed),
        ),
        explanation,
        {
            "Length1": length1,
            "Length2": length2,
            "FastSpeed": fast_speed,
            "SlowSpeed": slow_speed,
        },
    )


def tr_length_from_time(rng, variant):
    presets = ((10, 16, 90), (12, 20, 120), (8, 14, 90), (9, 15, 100), (15, 25, 200))
    pole_time, platform_time, platform_length = presets[variant % len(presets)]
    a, b = pair(variant, 7)
    kind = TRAIN_KINDS[variant % len(TRAIN_KINDS)]
    speed_mps = Fraction(platform_length, platform_time - pole_time)
    answer = speed_mps * pole_time
    text = (
        f"The {kind} crossing {a}'s pole takes {pole_time} s, but it takes "
        f"{platform_time} s to cross the {platform_length} m platform at {b} "
        "at the same speed. Find the length of the train."
    )
    explanation = (
        f"Extra time = {platform_time} - {pole_time} = "
        f"{platform_time - pole_time} s covers the platform: speed = "
        f"{platform_length}/{platform_time - pole_time} = {fmt(speed_mps)} "
        f"m/s; train length = {fmt(speed_mps)} x {pole_time} = {fmt(answer)} m."
    )
    return q(
        "tr_length_from_time", variant, text, answer,
        _distinct(
            answer,
            Fraction(platform_length, pole_time),
            speed_mps,
            Fraction(platform_length * platform_time, platform_time - pole_time),
        ),
        explanation,
        {
            "PoleTime": pole_time,
            "PlatformTime": platform_time,
            "PlatformLength": platform_length,
        },
    )


def tr_platform_length(rng, variant):
    presets = (
        (150, 72, 20), (200, 54, 24), (120, 90, 16),
        (180, 60, 21), (240, 108, 18),
    )
    train_length, speed, time = presets[variant % len(presets)]
    a, b = pair(variant, 8)
    kind = TRAIN_KINDS[variant % len(TRAIN_KINDS)]
    speed_mps = _mps(speed)
    answer = speed_mps * time - train_length
    text = (
        f"A {train_length} m {kind} travelling at {speed} kmph takes {time} s "
        f"to pass the platform used by {a} and {b}. How long is the platform?"
    )
    explanation = (
        f"Distance in {time} s = {fmt(speed_mps)} x {time} = "
        f"{fmt(speed_mps * time)} m; platform length = "
        f"{fmt(speed_mps * time)} - {train_length} = {fmt(answer)} m."
    )
    return q(
        "tr_platform_length", variant, text, answer,
        _distinct(
            answer,
            speed_mps * time,
            speed_mps * (time - 1) - train_length,
            speed_mps * (time + 1) - train_length,
        ),
        explanation,
        {"TrainLength": train_length, "Speed": speed, "Time": time},
    )


def tr_speed_conversion(rng, variant):
    presets = ((72,), (90,), (108,), (36,), (54,))
    (speed,) = presets[variant % len(presets)]
    a, b = pair(variant, 9)
    kind = TRAIN_KINDS[variant % len(TRAIN_KINDS)]
    answer = _mps(speed)
    text = (
        f"The {kind} that {a} sees near {b}'s depot runs at {speed} kmph. "
        "Express its speed in m/s."
    )
    explanation = f"{speed} kmph = {speed} x 5/18 = {fmt(answer)} m/s."
    return q(
        "tr_speed_conversion", variant, text, answer,
        _distinct(
            answer,
            _kmph(speed),
            Fraction(speed, 2),
            Fraction(speed, 3),
        ),
        explanation,
        {"Speed": speed},
    )


def tr_tunnel(rng, variant):
    presets = (
        (180, 270, 54), (200, 300, 72), (150, 250, 60),
        (240, 360, 90), (120, 180, 36),
    )
    train_length, tunnel_length, speed = presets[variant % len(presets)]
    a, b = pair(variant, 10)
    kind = TRAIN_KINDS[variant % len(TRAIN_KINDS)]
    speed_mps = _mps(speed)
    answer = Fraction(train_length + tunnel_length) / speed_mps
    text = (
        f"A {train_length} m {kind} enters the {tunnel_length} m tunnel near "
        f"{a} and comes out near {b}. At {speed} kmph, how many seconds does "
        "it take to pass completely through the tunnel?"
    )
    explanation = (
        f"To clear the tunnel it covers {train_length} + {tunnel_length} = "
        f"{train_length + tunnel_length} m; speed = {fmt(speed_mps)} m/s; "
        f"time = {fmt(answer)} s."
    )
    return q(
        "tr_tunnel", variant, text, answer,
        _distinct(
            answer,
            Fraction(train_length) / speed_mps,
            Fraction(tunnel_length) / speed_mps,
            Fraction(train_length + tunnel_length, speed),
        ),
        explanation,
        {"TrainLength": train_length, "TunnelLength": tunnel_length, "Speed": speed},
    )


def tr_passes_point(rng, variant):
    presets = ((200, 10), (300, 12), (180, 9), (240, 16), (350, 14))
    length, time = presets[variant % len(presets)]
    a, b = pair(variant, 11)
    kind = TRAIN_KINDS[variant % len(TRAIN_KINDS)]
    answer = _kmph(Fraction(length, time))
    text = (
        f"A {length} m {kind} passes the point marked by {a} and {b} in "
        f"{time} s. What is its speed in kmph?"
    )
    explanation = (
        f"Speed = {length}/{time} = {fmt(Fraction(length, time))} m/s = "
        f"{fmt(answer)} kmph."
    )
    return q(
        "tr_passes_point", variant, text, answer,
        _distinct(
            answer,
            Fraction(length, time),
            _kmph(Fraction(length, time + 1)),
            _kmph(Fraction(length, time - 1)),
        ),
        explanation,
        {"Length": length, "Time": time},
    )


def tr_relative_speed(rng, variant):
    presets = (
        (54, 36, "opposite"), (72, 36, "opposite"), (90, 54, "opposite"),
        (63, 45, "same"), (108, 72, "same"),
    )
    speed1, speed2, direction = presets[variant % len(presets)]
    a, b = pair(variant, 12)
    kind1 = TRAIN_KINDS[variant % len(TRAIN_KINDS)]
    kind2 = TRAIN_KINDS[(variant + 1) % len(TRAIN_KINDS)]
    combined_kmph = speed1 + speed2 if direction == "opposite" else speed1 - speed2
    answer = _mps(combined_kmph)
    relation = "towards each other" if direction == "opposite" else "in the same direction"
    text = (
        f"The {kind1} from {a} and the {kind2} from {b} move {relation} at "
        f"{speed1} kmph and {speed2} kmph. What is their relative speed in m/s?"
    )
    explanation = (
        f"Relative speed = {fmt(combined_kmph)} kmph = "
        f"{fmt(combined_kmph)} x 5/18 = {fmt(answer)} m/s."
    )
    return q(
        "tr_relative_speed", variant, text, answer,
        _distinct(
            answer,
            Fraction(combined_kmph),
            _mps(speed1 + speed2 if direction == "same" else speed1 - speed2),
            _mps(speed1),
        ),
        explanation,
        {"Speed1": speed1, "Speed2": speed2, "Direction": direction},
    )


def tr_length_ratio(rng, variant):
    presets = ((10, 15), (12, 18), (9, 12), (14, 21), (16, 20))
    time1, time2 = presets[variant % len(presets)]
    a, b = pair(variant, 13)
    kind1 = TRAIN_KINDS[variant % len(TRAIN_KINDS)]
    kind2 = TRAIN_KINDS[(variant + 2) % len(TRAIN_KINDS)]
    answer = _ratio(time1, time2)
    text = (
        f"Two trains, the {kind1} at {a} station and the {kind2} at {b} "
        f"station, pass a pole in {time1} s and {time2} s respectively at the "
        "same speed. Find the ratio of their lengths."
    )
    explanation = (
        f"At the same speed, length is proportional to pole-crossing time; "
        f"ratio = {time1}:{time2} = {answer}."
    )
    return q(
        "tr_length_ratio", variant, text, answer,
        _distinct(
            answer,
            f"{time2}:{time1}",
            f"{time1}:{time2 + 1}",
            f"{time1 + 1}:{time2}",
        ),
        explanation,
        {"Time1": time1, "Time2": time2},
    )


def tr_meeting_time(rng, variant):
    presets = (
        (270, 50, 40), (360, 60, 60), (420, 70, 70),
        (300, 55, 45), (480, 80, 40),
    )
    distance, speed1, speed2 = presets[variant % len(presets)]
    a, b = pair(variant, 14)
    kind1 = TRAIN_KINDS[variant % len(TRAIN_KINDS)]
    kind2 = TRAIN_KINDS[(variant + 1) % len(TRAIN_KINDS)]
    answer = Fraction(distance, speed1 + speed2)
    text = (
        f"Stations {a}pur and {b}pur are {distance} km apart. A {kind1} and "
        f"a {kind2} start towards each other from them at {speed1} kmph and "
        f"{speed2} kmph. In how many hours do they meet?"
    )
    explanation = (
        f"Closing speed = {speed1} + {speed2} = {speed1 + speed2} kmph; "
        f"meeting time = {distance}/{speed1 + speed2} = {fmt(answer)} h."
    )
    return q(
        "tr_meeting_time", variant, text, answer,
        _distinct(
            answer,
            Fraction(distance, speed1),
            Fraction(distance, speed2 + 5),
            Fraction(distance, speed1 + speed2 + 10),
        ),
        explanation,
        {"Distance": distance, "Speed1": speed1, "Speed2": speed2},
    )


def tr_gap_catch(rng, variant):
    presets = (
        (60, 80, 60), (90, 90, 60), (100, 80, 55),
        (120, 100, 70), (75, 75, 50),
    )
    gap, fast_speed, slow_speed = presets[variant % len(presets)]
    a, b = pair(variant, 15)
    kind1 = TRAIN_KINDS[variant % len(TRAIN_KINDS)]
    kind2 = TRAIN_KINDS[(variant + 2) % len(TRAIN_KINDS)]
    answer = Fraction(gap, fast_speed - slow_speed)
    text = (
        f"A {kind1} leaves {a} at {fast_speed} kmph to chase a {kind2} that "
        f"had left {b} {gap} km ahead of it at {slow_speed} kmph. In how many "
        "hours does it catch up?"
    )
    explanation = (
        f"Gain per hour = {fast_speed} - {slow_speed} = "
        f"{fast_speed - slow_speed} km; time = {gap}/"
        f"{fast_speed - slow_speed} = {fmt(answer)} h."
    )
    return q(
        "tr_gap_catch", variant, text, answer,
        _distinct(
            answer,
            Fraction(gap, fast_speed),
            Fraction(gap, slow_speed),
            Fraction(gap, fast_speed - slow_speed + 5),
        ),
        explanation,
        {"Gap": gap, "FastSpeed": fast_speed, "SlowSpeed": slow_speed},
    )


def tr_cross_each_other(rng, variant):
    presets = (
        (120, 180, 12, 36), (150, 200, 14, 45), (200, 250, 18, 54),
        (160, 200, 12, 63), (100, 140, 8, 48),
    )
    length1, length2, time, speed1 = presets[variant % len(presets)]
    a, b = pair(variant, 16)
    kind1 = TRAIN_KINDS[variant % len(TRAIN_KINDS)]
    kind2 = TRAIN_KINDS[(variant + 3) % len(TRAIN_KINDS)]
    total_length = length1 + length2
    relative_kmph = _kmph(Fraction(total_length, time))
    answer = relative_kmph - speed1
    text = (
        f"A {length1} m {kind1} and a {length2} m {kind2} coming from "
        f"opposite sides cross each other in {time} s near {a} and {b}. If "
        f"the first train runs at {speed1} kmph, find the speed of the second "
        "train in kmph."
    )
    explanation = (
        f"Relative speed = {total_length}/{time} = "
        f"{fmt(Fraction(total_length, time))} m/s = {fmt(relative_kmph)} "
        f"kmph; second train = {fmt(relative_kmph)} - {speed1} = "
        f"{fmt(answer)} kmph."
    )
    return q(
        "tr_cross_each_other", variant, text, answer,
        _distinct(
            answer,
            relative_kmph,
            _kmph(Fraction(total_length, time + 1)) - speed1,
            _kmph(Fraction(total_length, time - 1)) - speed1,
        ),
        explanation,
        {
            "Length1": length1,
            "Length2": length2,
            "Time": time,
            "Speed1": speed1,
        },
    )


def tr_speed_after_cross(rng, variant):
    presets = ((10, 16, 90), (12, 20, 120), (8, 14, 90), (9, 15, 100), (15, 25, 200))
    pole_time, platform_time, platform_length = presets[variant % len(presets)]
    a, b = pair(variant, 17)
    man = third(variant)
    kind = TRAIN_KINDS[variant % len(TRAIN_KINDS)]
    speed_mps = Fraction(platform_length, platform_time - pole_time)
    answer = _kmph(speed_mps)
    text = (
        f"{man} notes that a {kind} crosses his pole in {pole_time} s and the "
        f"{platform_length} m platform at {a} and {b} in {platform_time} s. "
        "Find the speed of the train in kmph."
    )
    explanation = (
        f"Platform alone takes {platform_time} - {pole_time} = "
        f"{platform_time - pole_time} s; speed = {platform_length}/"
        f"{platform_time - pole_time} = {fmt(speed_mps)} m/s = {fmt(answer)} "
        "kmph."
    )
    return q(
        "tr_speed_after_cross", variant, text, answer,
        _distinct(
            answer,
            _kmph(Fraction(platform_length, platform_time)),
            _kmph(Fraction(platform_length, pole_time)),
            speed_mps,
        ),
        explanation,
        {
            "PoleTime": pole_time,
            "PlatformTime": platform_time,
            "PlatformLength": platform_length,
        },
    )


def tr_catch_up(rng, variant):
    presets = ((40, 60, 2), (50, 75, 2), (45, 60, 3), (30, 50, 4), (60, 90, 2))
    slow_speed, fast_speed, start_gap = presets[variant % len(presets)]
    a, b = pair(variant, 18)
    kind1 = TRAIN_KINDS[variant % len(TRAIN_KINDS)]
    kind2 = TRAIN_KINDS[(variant + 1) % len(TRAIN_KINDS)]
    head_start = slow_speed * start_gap
    answer = Fraction(head_start * fast_speed, fast_speed - slow_speed)
    text = (
        f"A {kind1} starts from {a} at {slow_speed} kmph. {start_gap} hours "
        f"later a {kind2} starts from the same place at {fast_speed} kmph. "
        "How far from the start does it catch the first train?"
    )
    explanation = (
        f"Head start = {slow_speed} x {start_gap} = {head_start} km; catch "
        f"time = {head_start}/{fast_speed - slow_speed} = "
        f"{fmt(Fraction(head_start, fast_speed - slow_speed))} h; distance = "
        f"{fmt(answer)} km."
    )
    return q(
        "tr_catch_up", variant, text, answer,
        _distinct(
            answer,
            Fraction(head_start),
            Fraction(fast_speed * start_gap),
            Fraction(head_start, fast_speed - slow_speed),
        ),
        explanation,
        {
            "SlowSpeed": slow_speed,
            "FastSpeed": fast_speed,
            "StartGapHours": start_gap,
        },
    )


def tr_signal(rng, variant):
    presets = ((72, 12), (54, 16), (90, 10), (36, 18), (108, 14))
    speed, time = presets[variant % len(presets)]
    a, b = pair(variant, 19)
    kind = TRAIN_KINDS[variant % len(TRAIN_KINDS)]
    speed_mps = _mps(speed)
    answer = speed_mps * time
    text = (
        f"A {kind} passes the signal near {a} and {b} in {time} s. If its "
        f"speed is {speed} kmph, what is its length in metres?"
    )
    explanation = (
        f"{speed} kmph = {fmt(speed_mps)} m/s; length = {fmt(speed_mps)} x "
        f"{time} = {fmt(answer)} m."
    )
    return q(
        "tr_signal", variant, text, answer,
        _distinct(
            answer,
            Fraction(speed * time),
            speed_mps * (time + 1),
            speed_mps * (time - 1),
        ),
        explanation,
        {"Speed": speed, "Time": time},
    )


def tr_distance_minutes(rng, variant):
    presets = ((72, 45), (90, 40), (60, 50), (120, 25), (48, 75))
    speed, minutes = presets[variant % len(presets)]
    a, b = pair(variant, 0)
    kind = TRAIN_KINDS[variant % len(TRAIN_KINDS)]
    answer = Fraction(speed * minutes, 60)
    text = (
        f"A {kind} from {a} to {b} maintains {speed} kmph. How many "
        f"kilometres does it cover in {minutes} minutes?"
    )
    explanation = (
        f"{minutes} minutes = {fmt(Fraction(minutes, 60))} h; distance = "
        f"{speed} x {fmt(Fraction(minutes, 60))} = {fmt(answer)} km."
    )
    return q(
        "tr_distance_minutes", variant, text, answer,
        _distinct(
            answer,
            Fraction(speed * minutes),
            Fraction(speed * minutes, 100),
            Fraction(speed * minutes, 3600),
        ),
        explanation,
        {"Speed": speed, "Minutes": minutes},
    )


def tr_journey_average(rng, variant):
    presets = ((40, 60), (30, 60), (50, 75), (45, 90), (36, 72))
    speed1, speed2 = presets[variant % len(presets)]
    a, b = pair(variant, 1)
    kind = TRAIN_KINDS[variant % len(TRAIN_KINDS)]
    answer = Fraction(2 * speed1 * speed2, speed1 + speed2)
    text = (
        f"A {kind} travels from {a} to {b} on the first half of the journey "
        f"at {speed1} kmph and the second half at {speed2} kmph. What is its "
        "average speed for the whole journey?"
    )
    explanation = (
        f"Equal distances: average speed = 2 x {speed1} x {speed2} / "
        f"({speed1} + {speed2}) = {fmt(answer)} kmph."
    )
    return q(
        "tr_journey_average", variant, text, answer,
        _distinct(
            answer,
            Fraction(speed1 + speed2, 2),
            Fraction(speed1),
            Fraction(speed2),
        ),
        explanation,
        {"Speed1": speed1, "Speed2": speed2},
    )


def tr_combined_length(rng, variant):
    presets = (
        (72, 8, 12), (54, 10, 14), (90, 9, 11),
        (36, 12, 18), (108, 7, 13),
    )
    speed, time1, time2 = presets[variant % len(presets)]
    a, b = pair(variant, 2)
    kind1 = TRAIN_KINDS[variant % len(TRAIN_KINDS)]
    kind2 = TRAIN_KINDS[(variant + 2) % len(TRAIN_KINDS)]
    speed_mps = _mps(speed)
    answer = speed_mps * (time1 + time2)
    text = (
        f"At {a} a {kind1} passes a pole in {time1} s, and at {b} a {kind2} "
        f"passes another pole in {time2} s. Both run at {speed} kmph. What is "
        "their combined length?"
    )
    explanation = (
        f"Speed = {fmt(speed_mps)} m/s; combined length = "
        f"{fmt(speed_mps)} x ({time1} + {time2}) = {fmt(answer)} m."
    )
    return q(
        "tr_combined_length", variant, text, answer,
        _distinct(
            answer,
            speed_mps * time1,
            speed_mps * time2,
            Fraction(speed * (time1 + time2)),
        ),
        explanation,
        {"Speed": speed, "Time1": time1, "Time2": time2},
    )


def tr_compare(rng, variant):
    presets = (
        (180, 3, 200, 4), (240, 4, 250, 5), (300, 5, 180, 4),
        (360, 6, 350, 5), (420, 7, 240, 5),
    )
    distance1, time1, distance2, time2 = presets[variant % len(presets)]
    a, b = pair(variant, 3)
    kind1 = TRAIN_KINDS[variant % len(TRAIN_KINDS)]
    kind2 = TRAIN_KINDS[(variant + 1) % len(TRAIN_KINDS)]
    speed1 = Fraction(distance1, time1)
    speed2 = Fraction(distance2, time2)
    answer = abs(speed1 - speed2)
    text = (
        f"The {kind1} from {a} covers {distance1} km in {time1} h, while the "
        f"{kind2} from {b} covers {distance2} km in {time2} h. By how many "
        "kmph is the faster train faster?"
    )
    explanation = (
        f"Speeds are {fmt(speed1)} kmph and {fmt(speed2)} kmph; difference = "
        f"{fmt(answer)} kmph."
    )
    return q(
        "tr_compare", variant, text, answer,
        _distinct(
            answer,
            speed1,
            speed2,
            Fraction(distance1 + distance2, time1 + time2),
        ),
        explanation,
        {
            "Distance1": distance1,
            "Time1": time1,
            "Distance2": distance2,
            "Time2": time2,
        },
    )


FAMILIES = (
    tr_cross_pole,
    tr_cross_platform,
    tr_cross_bridge,
    tr_cross_man_same,
    tr_cross_man_opposite,
    tr_two_opposite,
    tr_two_same,
    tr_length_from_time,
    tr_platform_length,
    tr_speed_conversion,
    tr_tunnel,
    tr_passes_point,
    tr_relative_speed,
    tr_length_ratio,
    tr_meeting_time,
    tr_gap_catch,
    tr_cross_each_other,
    tr_speed_after_cross,
    tr_catch_up,
    tr_signal,
    tr_distance_minutes,
    tr_journey_average,
    tr_combined_length,
    tr_compare,
)


def build_problems_on_trains():
    return build_specs(FAMILIES)
