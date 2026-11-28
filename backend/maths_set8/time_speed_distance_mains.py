# -*- coding: utf-8 -*-
"""Time, Speed and Distance (Mains) - 120 original HARD multi-step questions.

All arithmetic is done with exact Fractions.  Speeds quoted in km/h are
converted with 5/18 for m/s (and 18/5 for the reverse conversion).
"""

from __future__ import annotations

from fractions import Fraction as _Fraction

from .common import (
    F,
    build_specs,
    fmt,
    make_family,
    near_num,
    near_pct,
    pct,
    ratio,
    ratio_distractors,
)

SOURCE_PDF = "0da2c67a-4985-4a86-9772-b0c4b826b42f.pdf"
PAGES = {
    1: f"{SOURCE_PDF}, pp. 3-5",
    2: f"{SOURCE_PDF}, pp. 6-8",
    3: f"{SOURCE_PDF}, pp. 9-11",
    4: f"{SOURCE_PDF}, pp. 12-14",
}

KMS_TO_MS = F(5, 18)
MS_TO_KMS = F(18, 5)


# ---------------------------------------------------------------------------
# Generic option and explanation helpers.
# ---------------------------------------------------------------------------

def _dn(result, inputs, step=3):
    """Numeric distractors for an exact Fraction/int answer."""
    return near_num(F(result), step)


def _dp(result, inputs, step=5):
    """Percentage distractors; ``result`` is a formatted '..%' string."""
    return near_pct(_Fraction(str(result).rstrip("%")), step)


def _dr(result, inputs):
    """Ratio distractors; ``result`` is a formatted 'a:b' string."""
    return ratio_distractors(str(result))


def _dsmart(result, inputs):
    """Pick distractors matching the answer type (number, ratio or percent)."""
    text = str(result)
    if text.endswith("%"):
        return _dp(text, inputs)
    if ":" in text:
        return _dr(text, inputs)
    return _dn(result, inputs)


def _explain(d, correct, note):
    return " ".join(
        f"Using the stated values in exact arithmetic, {note} "
        f"Therefore the required value is {correct}.".split()
    )


# ---------------------------------------------------------------------------
# 1. Train crossing a platform.
# ---------------------------------------------------------------------------

def _a_train_platform(d):
    length, platform, speed, ask = d["length"], d["platform"], d["speed_kmph"], d["ask"]
    ms = F(speed) * KMS_TO_MS
    if ask == "total_seconds":
        return F(length + platform) / ms
    if ask == "extra_seconds":
        return F(platform) / ms
    if ask == "time_ratio":
        return ratio(length + platform, length)
    if ask == "distance_m":
        return F(platform + 2 * length)
    if ask == "seconds_per_100m":
        return F(100) / ms
    raise ValueError(ask)


def _t_train_platform(d):
    head = (
        f"A train {fmt(d['length'])} m long is approaching a platform "
        f"{fmt(d['platform'])} m long, running throughout at a constant "
        f"{fmt(d['speed_kmph'])} km/h. "
    )
    tail = {
        "total_seconds": (
            "Counting from the instant the engine reaches the near end of the "
            "platform until the guard clears the far end, how many seconds does "
            "the complete crossing take?"
        ),
        "extra_seconds": (
            "How many more seconds does the train need to clear the platform "
            "than it needs to pass a single pole at the same speed?"
        ),
        "time_ratio": (
            "Find, in lowest terms, the ratio of the time taken to clear the "
            "platform to the time taken to pass a single pole."
        ),
        "distance_m": (
            "From the instant the engine enters the platform until the train "
            "has gone one further train-length after fully clearing it, how "
            "many metres has the engine travelled?"
        ),
        "seconds_per_100m": "How many seconds does the train take to cover 100 m at this speed?",
    }
    return head + tail[d["ask"]]


# ---------------------------------------------------------------------------
# 2. Opposite-direction trains.
# ---------------------------------------------------------------------------

def _a_opposite(d):
    s1, s2 = F(d["s1"]), F(d["s2"])
    total_len = F(d["l1"] + d["l2"])
    same = total_len / ((s1 - s2) * KMS_TO_MS)
    opposite = total_len / ((s1 + s2) * KMS_TO_MS)
    ask = d["ask"]
    if ask == "cross_seconds":
        return opposite
    if ask == "extra_seconds_vs_same":
        return same - opposite
    if ask == "distance_l1_m":
        return s1 * KMS_TO_MS * opposite
    if ask == "cross_minutes":
        return opposite / 60
    raise ValueError(ask)


def _t_opposite(d):
    head = (
        f"Two trains of length {fmt(d['l1'])} m and {fmt(d['l2'])} m run on "
        f"parallel tracks towards each other at {fmt(d['s1'])} km/h and "
        f"{fmt(d['s2'])} km/h respectively. "
    )
    tail = {
        "cross_seconds": (
            "How many seconds pass from the moment their engines meet until "
            "their guards have completely cleared one another?"
        ),
        "extra_seconds_vs_same": (
            "Had the faster train instead overtaken the slower one from behind "
            "at the same two speeds, how many additional seconds would the "
            "complete crossing have taken compared with the opposite-direction case?"
        ),
        "distance_l1_m": (
            "In the opposite-direction crossing, how many metres does the "
            f"{fmt(d['s1'])} km/h train travel between the engines meeting and "
            "the guards clearing each other?"
        ),
        "cross_minutes": (
            "How many minutes (as an exact fraction) elapse between the engines "
            "meeting and the guards clearing each other?"
        ),
    }
    return head + tail[d["ask"]]


# ---------------------------------------------------------------------------
# 3. Same-direction trains.
# ---------------------------------------------------------------------------

def _a_same_direction(d):
    s1, s2 = F(d["s1"]), F(d["s2"])
    total_len = F(d["l1"] + d["l2"])
    same = total_len / ((s1 - s2) * KMS_TO_MS)
    opposite = total_len / ((s1 + s2) * KMS_TO_MS)
    ask = d["ask"]
    if ask == "overtake_seconds":
        return same
    if ask == "extra_seconds_vs_opposite":
        return same - opposite
    if ask == "faster_distance_m":
        return s1 * KMS_TO_MS * same
    if ask == "slower_distance_m":
        return s2 * KMS_TO_MS * same
    raise ValueError(ask)


def _t_same_direction(d):
    head = (
        f"A {fmt(d['l1'])} m train travelling at {fmt(d['s1'])} km/h is behind "
        f"a {fmt(d['l2'])} m train travelling in the same direction at "
        f"{fmt(d['s2'])} km/h on a parallel track, with engines initially "
        "alongside each other. "
    )
    tail = {
        "overtake_seconds": (
            "How many seconds elapse until the faster train has completely "
            "overtaken the slower one (its guard level with the slower engine)?"
        ),
        "extra_seconds_vs_opposite": (
            "How many more seconds does this complete overtaking take than a "
            "complete crossing would take if the two trains travelled towards "
            "each other at the same two speeds?"
        ),
        "faster_distance_m": (
            "How many metres does the faster train cover from the engines "
            "coming level until the overtaking is complete?"
        ),
        "slower_distance_m": (
            "How many metres does the slower train cover from the engines "
            "coming level until the overtaking is complete?"
        ),
    }
    return head + tail[d["ask"]]


# ---------------------------------------------------------------------------
# 4. Boat going upstream and downstream.
# ---------------------------------------------------------------------------

def _a_boat_updown(d):
    boat, stream, one_way = F(d["boat"]), F(d["stream"]), F(d["one_way"])
    upstream, downstream = boat - stream, boat + stream
    up_t, down_t = one_way / upstream, one_way / downstream
    total_t = up_t + down_t
    ask = d["ask"]
    if ask == "round_trip_hours":
        return total_t
    if ask == "avg_speed_kmph":
        return 2 * one_way / total_t
    if ask == "extra_minutes":
        return (up_t - down_t) * 60
    if ask == "down_pct_faster":
        return pct((downstream / upstream - 1) * 100)
    if ask == "upstream_hours":
        return up_t
    raise ValueError(ask)


def _t_boat_updown(d):
    head = (
        f"A boat's speed in still water is {fmt(d['boat'])} km/h and the stream "
        f"runs at {fmt(d['stream'])} km/h. Two points A and B are "
        f"{fmt(d['one_way'])} km apart along the stream. "
    )
    tail = {
        "round_trip_hours": "How many hours does the return journey A to B and back to A take?",
        "avg_speed_kmph": "Find the average speed for the whole return journey, in km/h.",
        "extra_minutes": (
            "How many minutes longer is the upstream leg than the downstream leg?"
        ),
        "down_pct_faster": (
            "By what percentage is the downstream speed greater than the upstream speed?"
        ),
        "upstream_hours": "How many hours does the upstream leg alone take?",
    }
    return head + tail[d["ask"]]


# ---------------------------------------------------------------------------
# 5. Average speed over equal halves.
# ---------------------------------------------------------------------------

def _a_average_halves(d):
    s1, s2, distance = F(d["s1"]), F(d["s2"]), F(d["distance"])
    t1, t2 = distance / (2 * s1), distance / (2 * s2)
    ask = d["ask"]
    if ask == "avg_speed_kmph":
        return distance / (t1 + t2)
    if ask == "total_hours":
        return t1 + t2
    if ask == "time_diff_minutes":
        return (t2 - t1) * 60
    if ask == "first_time_pct":
        return pct(t1 / (t1 + t2) * 100)
    if ask == "thirds_avg_kmph":
        return distance / (distance / (3 * s1) + 2 * distance / (3 * s2))
    raise ValueError(ask)


def _t_average_halves(d):
    head = (
        f"A journey covers {fmt(d['distance'])} km. The first part is covered "
        f"at {fmt(d['s1'])} km/h and the remaining part at {fmt(d['s2'])} km/h. "
    )
    tail = {
        "avg_speed_kmph": (
            "If the two parts are equal halves of the distance, find the "
            "average speed for the whole journey in km/h."
        ),
        "total_hours": (
            "If the two parts are equal halves of the distance, find the "
            "total journey time in hours."
        ),
        "time_diff_minutes": (
            "If the journey is split into equal halves, how many more minutes "
            "is spent on the slower half than on the faster half?"
        ),
        "first_time_pct": (
            "With equal halves, what percentage of the total travel time is "
            "spent on the first part?"
        ),
        "thirds_avg_kmph": (
            "Suppose instead the first third of the distance is covered at "
            f"{fmt(d['s1'])} km/h and the remaining two-thirds at "
            f"{fmt(d['s2'])} km/h. Find the average speed for the journey in km/h."
        ),
    }
    return head + tail[d["ask"]]


# ---------------------------------------------------------------------------
# 6. Speed increasing in equal time intervals.
# ---------------------------------------------------------------------------

def _a_speed_increase(d):
    base, gain, n = F(d["base"]), F(d["gain"]), F(d["n"])
    total = n * base + gain * F(n * (n - 1), 2)
    ask = d["ask"]
    if ask == "total_distance_km":
        return total
    if ask == "last_hour_distance_km":
        return base + (n - 1) * gain
    if ask == "avg_speed_kmph":
        return total / n
    if ask == "pct_increase":
        return pct((n - 1) * gain / base * 100)
    if ask == "first_three_hours_km":
        return 3 * base + 3 * gain
    raise ValueError(ask)


def _t_speed_increase(d):
    head = (
        f"A vehicle starts at {fmt(d['base'])} km/h. At the end of every one-hour "
        f"interval it increases its speed by {fmt(d['gain'])} km/h and holds the "
        f"new speed for the next hour, for a total of {fmt(d['n'])} hours. "
    )
    tail = {
        "total_distance_km": "How many kilometres does it cover in all?",
        "last_hour_distance_km": "How many kilometres does it cover in the final hour?",
        "avg_speed_kmph": "What is its average speed over the whole period, in km/h?",
        "pct_increase": (
            "By what percentage is the speed in the final hour greater than "
            "the starting speed?"
        ),
        "first_three_hours_km": "How many kilometres does it cover in the first three hours?",
    }
    return head + tail[d["ask"]]


# ---------------------------------------------------------------------------
# 7. Meeting point between two starters.
# ---------------------------------------------------------------------------

def _a_meeting_point(d):
    distance, s1, s2 = F(d["distance"]), F(d["s1"]), F(d["s2"])
    meet_t = distance / (s1 + s2)
    ask = d["ask"]
    if ask == "from_A_km":
        return s1 * meet_t
    if ask == "extra_km":
        return abs(s1 - s2) * meet_t
    if ask == "minutes_to_meet":
        return meet_t * 60
    if ask == "pct_A":
        return pct(s1 / (s1 + s2) * 100)
    if ask == "from_B_km":
        return s2 * meet_t
    raise ValueError(ask)


def _t_meeting_point(d):
    head = (
        f"Two towns P and Q are {fmt(d['distance'])} km apart. A starts from P "
        f"towards Q at {fmt(d['s1'])} km/h while B starts from Q towards P at "
        f"{fmt(d['s2'])} km/h, at the same instant. "
    )
    tail = {
        "from_A_km": "How far from P do they meet, in kilometres?",
        "extra_km": (
            "How many kilometres more has the faster traveller covered than "
            "the slower traveller by the meeting instant?"
        ),
        "minutes_to_meet": "How many minutes after starting do they meet?",
        "pct_A": "What percentage of the total distance has A covered at the meeting point?",
        "from_B_km": "How far from Q do they meet, in kilometres?",
    }
    return head + tail[d["ask"]]


# ---------------------------------------------------------------------------
# 8. Delayed start and catch-up.
# ---------------------------------------------------------------------------

def _a_delayed_start(d):
    gap, v1, v2, delay = F(d["gap"]), F(d["v1"]), F(d["v2"]), F(d["delay"])
    remaining = gap - v1 * delay
    catch = remaining / (v2 - v1)
    ask = d["ask"]
    if ask == "catch_hours_after_second":
        return catch
    if ask == "catch_hours_after_first":
        return catch + delay
    if ask == "distance_from_start_km":
        return v2 * catch
    if ask == "catch_minutes_after_second":
        return catch * 60
    if ask == "gap_at_second_start_km":
        return remaining
    raise ValueError(ask)


def _t_delayed_start(d):
    head = (
        f"A is already {fmt(d['gap'])} km ahead of B. A continues at "
        f"{fmt(d['v1'])} km/h. B waits {fmt(d['delay'])} hour(s) and then "
        f"starts from the same origin in pursuit at {fmt(d['v2'])} km/h. "
    )
    tail = {
        "catch_hours_after_second": (
            "How many hours after B starts does B catch A?"
        ),
        "catch_hours_after_first": (
            "How many hours after A originally started does the catch occur?"
        ),
        "distance_from_start_km": (
            "How many kilometres does B travel from its own starting point "
            "before catching A?"
        ),
        "catch_minutes_after_second": "How many minutes after B starts is A caught?",
        "gap_at_second_start_km": (
            "At the instant B starts, how many kilometres separate the two?"
        ),
    }
    return head + tail[d["ask"]]


# ---------------------------------------------------------------------------
# 9. Stoppage during a journey.
# ---------------------------------------------------------------------------

def _a_stoppage(d):
    speed, run, halt = F(d["speed"]), F(d["run"]), F(d["halt"])
    distance = F(d["distance"])
    cycles = distance / (speed * run / 60)
    ask = d["ask"]
    if ask == "total_hours":
        return cycles * (run + halt) / 60
    if ask == "halt_minutes_total":
        return cycles * halt
    if ask == "effective_speed_kmph":
        return speed * run / (run + halt)
    if ask == "halt_pct_of_time":
        return pct(halt / (run + halt) * 100)
    if ask == "moving_hours":
        return distance / speed
    raise ValueError(ask)


def _t_stoppage(d):
    head = (
        f"A vehicle runs at {fmt(d['speed'])} km/h for {fmt(d['run'])} minutes "
        f"and then halts for {fmt(d['halt'])} minutes, repeating this cycle "
        f"until it has covered {fmt(d['distance'])} km. The distance is an "
        "exact number of running segments. "
    )
    tail = {
        "total_hours": (
            "Counting every halt after a completed running segment, how many "
            "hours does the whole journey take?"
        ),
        "halt_minutes_total": "How many minutes does it spend halted in total?",
        "effective_speed_kmph": "Find its effective average speed in km/h over a full cycle.",
        "halt_pct_of_time": "What percentage of a full cycle is spent halted?",
        "moving_hours": "How many hours does it actually spend in motion?",
    }
    return head + tail[d["ask"]]


# ---------------------------------------------------------------------------
# 10. Speed ratio and time difference.
# ---------------------------------------------------------------------------

def _a_speed_ratio_time(d):
    r1, r2, time_diff = F(d["r1"]), F(d["r2"]), F(d["time_diff"])
    k = time_diff / (r2 - r1)
    slow, fast = r2 * k, r1 * k
    ask = d["ask"]
    if ask == "slow_time_hours":
        return slow
    if ask == "sum_time_hours":
        return slow + fast
    if ask == "fast_time_hours":
        return fast
    if ask == "slow_pct_more":
        return pct((r2 - r1) / r1 * 100)
    if ask == "time_ratio":
        return ratio(slow, fast)
    raise ValueError(ask)


def _t_speed_ratio_time(d):
    head = (
        f"Two vehicles cover the same distance at speeds in the ratio "
        f"{fmt(d['r1'])}:{fmt(d['r2'])} (the second is faster). The slower "
        f"vehicle takes {fmt(d['time_diff'])} hour(s) more than the faster one. "
    )
    tail = {
        "slow_time_hours": "How many hours does the slower vehicle take?",
        "sum_time_hours": "What is the sum of their travel times, in hours?",
        "fast_time_hours": "How many hours does the faster vehicle take?",
        "slow_pct_more": (
            "By what percentage is the slower vehicle's time greater than the "
            "faster vehicle's time?"
        ),
        "time_ratio": "Find the ratio of the slower time to the faster time, in lowest terms.",
    }
    return head + tail[d["ask"]]


# ---------------------------------------------------------------------------
# 11. Circular track, opposite directions.
# ---------------------------------------------------------------------------

def _a_circular_meet(d):
    circumference = F(d["circumference"])
    s1, s2 = F(d["s1"]), F(d["s2"])
    meet_t = circumference / ((s1 + s2) * KMS_TO_MS)
    ask = d["ask"]
    if ask == "first_meet_seconds":
        return meet_t
    if ask == "distance_s1_m":
        return s1 * KMS_TO_MS * meet_t
    if ask == "distance_s2_m":
        return s2 * KMS_TO_MS * meet_t
    if ask == "pct_s2":
        return pct(s2 / (s1 + s2) * 100)
    raise ValueError(ask)


def _t_circular_meet(d):
    head = (
        f"On a circular track of circumference {fmt(d['circumference'])} m, "
        f"two runners start together from the same point and run in opposite "
        f"directions at {fmt(d['s1'])} km/h and {fmt(d['s2'])} km/h. "
    )
    tail = {
        "first_meet_seconds": "How many seconds elapse before they first meet?",
        "distance_s1_m": (
            "How many metres has the first runner covered when they meet for "
            "the first time?"
        ),
        "distance_s2_m": (
            "How many metres has the second runner covered when they meet for "
            "the first time?"
        ),
        "pct_s2": (
            "What percentage of the combined distance covered up to the first "
            "meeting is covered by the second runner?"
        ),
    }
    return head + tail[d["ask"]]


# ---------------------------------------------------------------------------
# 12. Two trains crossing each other, plus pole-crossing comparisons.
# ---------------------------------------------------------------------------

def _a_cross_each_other(d):
    s1, s2 = F(d["s1"]), F(d["s2"])
    pole1 = F(d["l1"]) / (s1 * KMS_TO_MS)
    pole2 = F(d["l2"]) / (s2 * KMS_TO_MS)
    cross = F(d["l1"] + d["l2"]) / ((s1 + s2) * KMS_TO_MS)
    ask = d["ask"]
    if ask == "cross_seconds":
        return cross
    if ask == "pole_times_sum_seconds":
        return pole1 + pole2
    if ask == "pole_time_ratio":
        return ratio(pole1, pole2)
    if ask == "pole_times_diff_seconds":
        return abs(pole1 - pole2)
    if ask == "cross_minutes":
        return cross / 60
    raise ValueError(ask)


def _t_cross_each_other(d):
    head = (
        f"Two trains are {fmt(d['l1'])} m and {fmt(d['l2'])} m long and run at "
        f"{fmt(d['s1'])} km/h and {fmt(d['s2'])} km/h respectively on parallel "
        "tracks in opposite directions. "
    )
    tail = {
        "cross_seconds": (
            "How many seconds do they take to cross each other completely?"
        ),
        "pole_times_sum_seconds": (
            "Find the sum of the times, in seconds, that each train takes to "
            "pass a single pole at its own speed."
        ),
        "pole_time_ratio": (
            "Find, in lowest terms, the ratio of the time the first train takes "
            "to pass a pole to the time the second train takes to pass a pole."
        ),
        "pole_times_diff_seconds": (
            "How many seconds differ between the times the two trains take to "
            "pass a pole at their own speeds?"
        ),
        "cross_minutes": (
            "How many minutes, as an exact fraction, do the two trains take to "
            "cross each other completely?"
        ),
    }
    return head + tail[d["ask"]]


# ---------------------------------------------------------------------------
# 13. Buses overtaking a walker.
# ---------------------------------------------------------------------------

def _a_bus_walker(d):
    bus, walker, interval = F(d["bus_speed"]), F(d["walker_speed"]), F(d["interval"])
    ask = d["ask"]
    if ask == "stationary_interval_min":
        return interval * (bus - walker) / bus
    if ask == "opposite_interval_min":
        return interval * (bus - walker) / (bus + walker)
    if ask == "bus_spacing_km":
        return (bus - walker) * interval / 60
    if ask == "pct_reduction":
        return pct(walker / bus * 100)
    raise ValueError(ask)


def _t_bus_walker(d):
    head = (
        f"Buses run in a stream at a uniform spacing and at "
        f"{fmt(d['bus_speed'])} km/h. A walker moving in the same direction at "
        f"{fmt(d['walker_speed'])} km/h is passed by a bus every "
        f"{fmt(d['interval'])} minutes. "
    )
    tail = {
        "stationary_interval_min": (
            "At what interval, in minutes, would a person standing still be "
            "passed by successive buses?"
        ),
        "opposite_interval_min": (
            "At what interval, in minutes, would buses pass a person walking "
            "in the opposite direction at the same speed?"
        ),
        "bus_spacing_km": "What is the distance between consecutive buses, in kilometres?",
        "pct_reduction": (
            "By what percentage is the observed passing interval shorter than "
            "it would be for a stationary observer?"
        ),
    }
    return head + tail[d["ask"]]


# ---------------------------------------------------------------------------
# 14. Boat speed inferred from upstream/downstream times.
# ---------------------------------------------------------------------------

def _a_stream_ratio(d):
    up_time, down_time = F(d["up_time"]), F(d["down_time"])
    stream = F(d["stream"])
    boat = stream * (up_time + down_time) / (up_time - down_time)
    upstream, downstream = boat - stream, boat + stream
    ask = d["ask"]
    if ask == "boat_speed_kmph":
        return boat
    if ask == "distance_km":
        return upstream * up_time
    if ask == "down_speed_kmph":
        return downstream
    if ask == "up_speed_kmph":
        return upstream
    if ask == "pct_up_slower":
        return pct((up_time - down_time) / down_time * 100)
    raise ValueError(ask)


def _t_stream_ratio(d):
    head = (
        f"A boat takes {fmt(d['up_time'])} hours to travel a certain distance "
        f"upstream and {fmt(d['down_time'])} hours for the same distance "
        f"downstream. The stream runs at {fmt(d['stream'])} km/h. "
    )
    tail = {
        "boat_speed_kmph": "Find the boat's speed in still water, in km/h.",
        "distance_km": "Find the one-way distance, in kilometres.",
        "down_speed_kmph": "Find the downstream speed, in km/h.",
        "up_speed_kmph": "Find the upstream speed, in km/h.",
        "pct_up_slower": (
            "By what percentage is the upstream travel time greater than the "
            "downstream travel time?"
        ),
    }
    return head + tail[d["ask"]]


# ---------------------------------------------------------------------------
# 15. Two legs with a stop in between.
# ---------------------------------------------------------------------------

def _a_speed_change_stop(d):
    t1 = F(d["d1"]) / F(d["s1"])
    stop = F(d["stop_min"]) / 60
    t2 = F(d["d2"]) / F(d["s2"])
    total = t1 + stop + t2
    ask = d["ask"]
    if ask == "total_hours":
        return total
    if ask == "moving_hours":
        return t1 + t2
    if ask == "avg_speed_whole_kmph":
        return F(d["d1"] + d["d2"]) / total
    if ask == "stop_pct_of_total":
        return pct(stop / total * 100)
    if ask == "second_leg_pct_of_time":
        return pct(t2 / total * 100)
    raise ValueError(ask)


def _t_speed_change_stop(d):
    head = (
        f"A traveller covers {fmt(d['d1'])} km at {fmt(d['s1'])} km/h, rests for "
        f"{fmt(d['stop_min'])} minutes, then covers {fmt(d['d2'])} km at "
        f"{fmt(d['s2'])} km/h. "
    )
    tail = {
        "total_hours": "Find the total elapsed time, in hours.",
        "moving_hours": "Find the total time actually spent moving, in hours.",
        "avg_speed_whole_kmph": (
            "Find the average speed for the entire journey including the rest, "
            "in km/h."
        ),
        "stop_pct_of_total": "What percentage of the total elapsed time is the rest?",
        "second_leg_pct_of_time": (
            "What percentage of the total elapsed time is spent on the second leg?"
        ),
    }
    return head + tail[d["ask"]]


# ---------------------------------------------------------------------------
# 16. Late at one speed, early at another.
# ---------------------------------------------------------------------------

def _a_early_late(d):
    slow, fast, diff = F(d["slow"]), F(d["fast"]), F(d["diff"])
    distance = 2 * diff * slow * fast / (fast - slow)
    scheduled = diff * (slow + fast) / (fast - slow)
    ask = d["ask"]
    if ask == "distance_km":
        return distance
    if ask == "scheduled_hours":
        return scheduled
    if ask == "slow_travel_hours":
        return distance / slow
    if ask == "fast_travel_hours":
        return distance / fast
    if ask == "pct_time_saved":
        return pct((fast - slow) / fast * 100)
    raise ValueError(ask)


def _t_early_late(d):
    head = (
        f"For a fixed journey, travelling at {fmt(d['slow'])} km/h arrives "
        f"{fmt(d['diff'])} hour(s) late, while travelling at "
        f"{fmt(d['fast'])} km/h arrives {fmt(d['diff'])} hour(s) early. "
    )
    tail = {
        "distance_km": "Find the length of the journey, in kilometres.",
        "scheduled_hours": "Find the scheduled travel time, in hours.",
        "slow_travel_hours": "How many hours does the slow journey actually take?",
        "fast_travel_hours": "How many hours does the fast journey actually take?",
        "pct_time_saved": (
            "By what percentage is the fast travel time less than the slow "
            "travel time?"
        ),
    }
    return head + tail[d["ask"]]


# ---------------------------------------------------------------------------
# 17. Two vehicles with both a time lead and a distance gap.
# ---------------------------------------------------------------------------

def _a_two_vehicle_gap(d):
    lead = F(d["lead"])
    v1, v2 = F(d["v1"]), F(d["v2"])
    start_gap = F(d["start_gap"])
    gap_at_start = lead * v1 + start_gap
    catch = gap_at_start / (v2 - v1)
    ask = d["ask"]
    if ask == "catch_hours_after_B":
        return catch
    if ask == "distance_B_km":
        return v2 * catch
    if ask == "catch_hours_after_A":
        return catch + lead
    if ask == "gap_at_B_start_km":
        return gap_at_start
    if ask == "pct_gap_closed_per_hour":
        return pct((v2 - v1) / v1 * 100)
    raise ValueError(ask)


def _t_two_vehicle_gap(d):
    head = (
        f"Vehicle A leaves point P and travels at {fmt(d['v1'])} km/h. "
        f"{fmt(d['lead'])} hour(s) later, vehicle B leaves point Q, which is "
        f"{fmt(d['start_gap'])} km behind P, and travels in the same direction "
        f"at {fmt(d['v2'])} km/h. "
    )
    tail = {
        "catch_hours_after_B": "How many hours after B starts does B catch A?",
        "distance_B_km": "How many kilometres does B travel before catching A?",
        "catch_hours_after_A": "How many hours after A started does the catch occur?",
        "gap_at_B_start_km": (
            "At the moment B starts, how many kilometres ahead is A?"
        ),
        "pct_gap_closed_per_hour": (
            "By what percentage of A's speed does B close the gap each hour?"
        ),
    }
    return head + tail[d["ask"]]


# ---------------------------------------------------------------------------
# 18. Train through a tunnel.
# ---------------------------------------------------------------------------

def _a_tunnel(d):
    ms = F(d["speed_kmph"]) * KMS_TO_MS
    ask = d["ask"]
    if ask == "cross_seconds":
        return F(d["length"] + d["tunnel"]) / ms
    if ask == "inside_seconds":
        return F(d["tunnel"] - d["length"]) / ms
    if ask == "tunnel_to_pole_ratio":
        return ratio(d["tunnel"] + d["length"], d["length"])
    if ask == "metres_per_minute":
        return F(d["speed_kmph"]) * 1000 / 60
    if ask == "pole_seconds":
        return F(d["length"]) / ms
    raise ValueError(ask)


def _t_tunnel(d):
    head = (
        f"A train {fmt(d['length'])} m long passes through a tunnel "
        f"{fmt(d['tunnel'])} m long at a steady {fmt(d['speed_kmph'])} km/h. "
    )
    tail = {
        "cross_seconds": (
            "How many seconds pass from the engine entering the tunnel until "
            "the guard leaves it?"
        ),
        "inside_seconds": (
            "How many seconds is the whole train completely inside the tunnel?"
        ),
        "tunnel_to_pole_ratio": (
            "Find, in lowest terms, the ratio of the time to pass completely "
            "through the tunnel to the time to pass a pole."
        ),
        "metres_per_minute": "How many metres does the train cover in one minute?",
        "pole_seconds": "How many seconds does the train take to pass a pole?",
    }
    return head + tail[d["ask"]]


# ---------------------------------------------------------------------------
# 19. Walking on a moving walkway.
# ---------------------------------------------------------------------------

def _a_walk_scale(d):
    walkers, length = F(d["walkers"]), F(d["length"])
    walking, escalator = F(d["walking_speed"]), F(d["escalator_speed"])
    traverse = length / (walking + escalator)
    ask = d["ask"]
    if ask == "traverse_seconds":
        return traverse
    if ask == "seconds_saved":
        return length / walking - traverse
    if ask == "gap_m":
        return length / (walkers + 1)
    if ask == "pct_time_saved":
        return pct(escalator / (walking + escalator) * 100)
    if ask == "all_walkers_total_m":
        return walkers * length
    raise ValueError(ask)


def _t_walk_scale(d):
    head = (
        f"A moving walkway is {fmt(d['length'])} m long and itself advances at "
        f"{fmt(d['escalator_speed'])} m/s. {fmt(d['walkers'])} walkers are on it, "
        f"equally spaced from one end to the other, each walking at "
        f"{fmt(d['walking_speed'])} m/s relative to the walkway. "
    )
    tail = {
        "traverse_seconds": (
            "How many seconds does one walking person need to go from one end "
            "to the other?"
        ),
        "seconds_saved": (
            "How many seconds does a walker save compared with walking the "
            "same length on stationary ground at the same walking speed?"
        ),
        "gap_m": "What is the gap between consecutive walkers, in metres?",
        "pct_time_saved": (
            "What percentage of the time on stationary ground is saved by the "
            "motion of the walkway?"
        ),
        "all_walkers_total_m": (
            "What is the total distance, in metres, covered by all the walkers "
            "together if each walks the full length?"
        ),
    }
    return head + tail[d["ask"]]


# ---------------------------------------------------------------------------
# 20. Circular track, same direction.
# ---------------------------------------------------------------------------

def _a_circular_same(d):
    circumference = F(d["circumference"])
    s1, s2 = F(d["s1"]), F(d["s2"])
    lap = circumference / ((s1 - s2) * KMS_TO_MS)
    ask = d["ask"]
    if ask == "first_overtake_seconds":
        return lap
    if ask == "distance_fast_m":
        return s1 * KMS_TO_MS * lap
    if ask == "pct_track_by_fast":
        return pct(s1 / (s1 - s2) * 100)
    if ask == "lap_ratio":
        return ratio(s1, s2)
    raise ValueError(ask)


def _t_circular_same(d):
    head = (
        f"On a circular track of circumference {fmt(d['circumference'])} m, "
        f"two runners start together from the same point and run in the same "
        f"direction at {fmt(d['s1'])} km/h and {fmt(d['s2'])} km/h, the first "
        "being faster. "
    )
    tail = {
        "first_overtake_seconds": (
            "How many seconds elapse before the faster runner first overtakes "
            "the slower one?"
        ),
        "distance_fast_m": (
            "How many metres has the faster runner covered at that first "
            "overtaking?"
        ),
        "pct_track_by_fast": (
            "The distance covered by the faster runner up to the first overtaking "
            "is what percentage of one lap?"
        ),
        "lap_ratio": (
            "Find, in lowest terms, the ratio of the numbers of laps completed "
            "per unit time by the two runners."
        ),
    }
    return head + tail[d["ask"]]


# ---------------------------------------------------------------------------
# 21. Journey with a known total time and unaccounted stops.
# ---------------------------------------------------------------------------

def _a_journey_stops(d):
    distance, speed = F(d["distance"]), F(d["speed"])
    stops, total = F(d["stops_min"]) / 60, F(d["total_hours"])
    ask = d["ask"]
    if ask == "moving_time_hours":
        return total - stops
    if ask == "effective_speed_kmph":
        return distance / total
    if ask == "scheduled_without_stops_hours":
        return distance / speed
    if ask == "extra_delay_min":
        return (total - distance / speed - stops) * 60
    if ask == "pct_time_stopped":
        return pct(stops / total * 100)
    raise ValueError(ask)


def _t_journey_stops(d):
    head = (
        f"A journey of {fmt(d['distance'])} km is nominally run at "
        f"{fmt(d['speed'])} km/h. Named stops account for {fmt(d['stops_min'])} "
        f"minutes, yet the whole journey takes {fmt(d['total_hours'])} hours. "
    )
    tail = {
        "moving_time_hours": "How many hours are actually spent in motion?",
        "effective_speed_kmph": (
            "Find the effective average speed for the whole elapsed time, in km/h."
        ),
        "scheduled_without_stops_hours": (
            "How many hours would the journey take with no stopping at all?"
        ),
        "extra_delay_min": (
            "How many minutes of delay remain unexplained by the named stops?"
        ),
        "pct_time_stopped": (
            "What percentage of the total elapsed time is taken by the named stops?"
        ),
    }
    return head + tail[d["ask"]]


# ---------------------------------------------------------------------------
# 22. km/h to m/s conversions over a short time.
# ---------------------------------------------------------------------------

def _a_kmph_ms(d):
    speed, seconds = F(d["speed_kmph"]), F(d["seconds"])
    metres = speed * KMS_TO_MS * seconds
    ask = d["ask"]
    if ask == "distance_m":
        return metres
    if ask == "distance_km":
        return metres / 1000
    if ask == "pct_of_km":
        return pct(metres / 1000 * 100)
    if ask == "seconds_per_km":
        return 3600 / speed
    if ask == "distance_cm":
        return metres * 100
    raise ValueError(ask)


def _t_kmph_ms(d):
    head = (
        f"A body moves at a constant {fmt(d['speed_kmph'])} km/h for "
        f"{fmt(d['seconds'])} seconds. "
    )
    tail = {
        "distance_m": "How many metres does it cover?",
        "distance_km": "How many kilometres does it cover?",
        "pct_of_km": "The distance covered is what percentage of one kilometre?",
        "seconds_per_km": "How many seconds would it take to cover one kilometre?",
        "distance_cm": "How many centimetres does it cover?",
    }
    return head + tail[d["ask"]]


# ---------------------------------------------------------------------------
# 23. Two boats in a stream.
# ---------------------------------------------------------------------------

def _a_two_boats(d):
    still, stream, distance = F(d["still"]), F(d["stream"]), F(d["distance"])
    downstream, upstream = still + stream, still - stream
    meet_t = distance / (downstream + upstream)
    ask = d["ask"]
    if ask == "meet_hours":
        return meet_t
    if ask == "meet_from_A_km":
        return downstream * meet_t
    if ask == "time_diff_hours":
        return distance / upstream - distance / downstream
    if ask == "down_pct_faster":
        return pct((downstream / upstream - 1) * 100)
    if ask == "round_trip_hours":
        return distance / downstream + distance / upstream
    raise ValueError(ask)


def _t_two_boats(d):
    head = (
        f"Two points A and B are {fmt(d['distance'])} km apart along a river "
        f"flowing at {fmt(d['stream'])} km/h. Both boats have a still-water "
        f"speed of {fmt(d['still'])} km/h. Boat 1 starts from A towards B while "
        "boat 2 starts from B towards A at the same instant. "
    )
    tail = {
        "meet_hours": "How many hours elapse before the boats meet?",
        "meet_from_A_km": "How far from A is the meeting point, in kilometres?",
        "time_diff_hours": (
            "A single boat going only downstream between A and B takes how many "
            "hours less than one going only upstream?"
        ),
        "down_pct_faster": (
            "By what percentage is the downstream speed greater than the "
            "upstream speed?"
        ),
        "round_trip_hours": (
            "How many hours does one boat take to go from A to B and back to A?"
        ),
    }
    return head + tail[d["ask"]]


# ---------------------------------------------------------------------------
# 24. Chase with a speed boost after a delay.
# ---------------------------------------------------------------------------

def _a_chase_change(d):
    gap = F(d["gap"])
    thief, police = F(d["thief"]), F(d["police"])
    boost, change_after = F(d["boost"]), F(d["change_after"])
    remaining = gap - (police - thief) * change_after
    after = remaining / (police + boost - thief)
    total = change_after + after
    ask = d["ask"]
    if ask == "total_hours":
        return total
    if ask == "hours_after_boost":
        return after
    if ask == "police_distance_km":
        return police * change_after + (police + boost) * after
    if ask == "thief_distance_km":
        return thief * total
    if ask == "pct_speed_boost":
        return pct(boost / police * 100)
    raise ValueError(ask)


def _t_chase_change(d):
    head = (
        f"A thief is {fmt(d['gap'])} km ahead of a policeman and runs at "
        f"{fmt(d['thief'])} km/h. The policeman initially chases at "
        f"{fmt(d['police'])} km/h but, after {fmt(d['change_after'])} hour(s), "
        f"increases his speed by {fmt(d['boost'])} km/h and keeps the new speed. "
    )
    tail = {
        "total_hours": "How many hours from the start does the capture take?",
        "hours_after_boost": "How many hours after the speed increase is the thief caught?",
        "police_distance_km": "How many kilometres does the policeman run before the capture?",
        "thief_distance_km": "How many kilometres does the thief run before capture?",
        "pct_speed_boost": "By what percentage does the policeman raise his speed?",
    }
    return head + tail[d["ask"]]


# ---------------------------------------------------------------------------
# Family declarations: exactly 24 families, five variants each.
# ---------------------------------------------------------------------------

FAMILIES = [
    make_family(
        "tsd_train_platform",
        ("length", "platform", "speed_kmph", "ask"),
        [
            (180, 270, 54, "total_seconds"),
            (240, 360, 72, "extra_seconds"),
            (150, 250, 45, "time_ratio"),
            (200, 300, 60, "distance_m"),
            (160, 200, 48, "total_seconds"),
        ],
        _t_train_platform,
        _a_train_platform,
        _dsmart,
        lambda d, c: _explain(
            d, c,
            f"{fmt(F(d['speed_kmph']) * KMS_TO_MS)} m/s is the speed; the "
            f"relevant length combination is handled with that conversion.",
        ),
    ),
    make_family(
        "tsd_opposite_trains",
        ("l1", "l2", "s1", "s2", "ask"),
        [
            (180, 270, 54, 36, "cross_seconds"),
            (200, 250, 72, 48, "extra_seconds_vs_same"),
            (120, 280, 54, 36, "cross_seconds"),
            (300, 600, 60, 30, "distance_l1_m"),
            (120, 180, 72, 36, "extra_seconds_vs_same"),
        ],
        _t_opposite,
        _a_opposite,
        _dsmart,
        lambda d, c: _explain(
            d, c,
            f"relative speeds are {fmt((F(d['s1']) + F(d['s2'])) * KMS_TO_MS)} m/s "
            f"towards and {fmt((F(d['s1']) - F(d['s2'])) * KMS_TO_MS)} m/s apart.",
        ),
    ),
    make_family(
        "tsd_same_direction",
        ("l1", "l2", "s1", "s2", "ask"),
        [
            (150, 210, 72, 36, "overtake_seconds"),
            (180, 220, 90, 54, "overtake_seconds"),
            (120, 180, 72, 36, "extra_seconds_vs_opposite"),
            (200, 250, 108, 72, "faster_distance_m"),
            (150, 300, 72, 45, "overtake_seconds"),
        ],
        _t_same_direction,
        _a_same_direction,
        _dsmart,
        lambda d, c: _explain(
            d, c,
            f"the closing speed behind is "
            f"{fmt((F(d['s1']) - F(d['s2'])) * KMS_TO_MS)} m/s while the "
            f"approach speed would be "
            f"{fmt((F(d['s1']) + F(d['s2'])) * KMS_TO_MS)} m/s.",
        ),
    ),
    make_family(
        "tsd_boat_updown",
        ("boat", "stream", "one_way", "ask"),
        [
            (18, 6, 24, "round_trip_hours"),
            (16, 4, 24, "avg_speed_kmph"),
            (10, 2, 24, "extra_minutes"),
            (14, 7, 28, "down_pct_faster"),
            (20, 4, 48, "round_trip_hours"),
        ],
        _t_boat_updown,
        _a_boat_updown,
        _dsmart,
        lambda d, c: _explain(
            d, c,
            f"upstream {fmt(F(d['boat']) - F(d['stream']))} km/h and downstream "
            f"{fmt(F(d['boat']) + F(d['stream']))} km/h over "
            f"{fmt(d['one_way'])} km each way.",
        ),
    ),
    make_family(
        "tsd_average_halves",
        ("s1", "s2", "distance", "ask"),
        [
            (40, 60, 120, "avg_speed_kmph"),
            (30, 60, 120, "total_hours"),
            (60, 40, 240, "time_diff_minutes"),
            (50, 75, 150, "first_time_pct"),
            (30, 60, 180, "thirds_avg_kmph"),
        ],
        _t_average_halves,
        _a_average_halves,
        _dsmart,
        lambda d, c: _explain(
            d, c,
            "time on each segment is found separately from distance divided by "
            "that segment's speed before combining the times.",
        ),
    ),
    make_family(
        "tsd_speed_increase",
        ("base", "gain", "n", "ask"),
        [
            (30, 5, 6, "total_distance_km"),
            (20, 4, 5, "last_hour_distance_km"),
            (40, 8, 5, "avg_speed_kmph"),
            (25, 5, 5, "pct_increase"),
            (36, 6, 7, "total_distance_km"),
        ],
        _t_speed_increase,
        _a_speed_increase,
        _dsmart,
        lambda d, c: _explain(
            d, c,
            "the hourly distances form an arithmetic progression starting at "
            f"{fmt(d['base'])} with step {fmt(d['gain'])} over {fmt(d['n'])} hours.",
        ),
    ),
    make_family(
        "tsd_meeting_point",
        ("distance", "s1", "s2", "ask"),
        [
            (180, 40, 50, "from_A_km"),
            (240, 60, 40, "extra_km"),
            (120, 30, 90, "minutes_to_meet"),
            (200, 45, 55, "pct_A"),
            (360, 50, 40, "from_B_km"),
        ],
        _t_meeting_point,
        _a_meeting_point,
        _dsmart,
        lambda d, c: _explain(
            d, c,
            f"meeting time is {fmt(d['distance'])}/({fmt(d['s1'])}+{fmt(d['s2'])}) "
            "hours, then each traveller's share follows from that time.",
        ),
    ),
    make_family(
        "tsd_delayed_start",
        ("gap", "v1", "v2", "delay", "ask"),
        [
            (120, 40, 60, 1, "catch_hours_after_second"),
            (200, 30, 50, 2, "catch_hours_after_first"),
            (150, 30, 60, 1, "distance_from_start_km"),
            (100, 24, 36, 1, "catch_minutes_after_second"),
            (180, 45, 75, 2, "gap_at_second_start_km"),
        ],
        _t_delayed_start,
        _a_delayed_start,
        _dsmart,
        lambda d, c: _explain(
            d, c,
            f"the gap at the later start is "
            f"{fmt(F(d['gap']) - F(d['v1']) * F(d['delay']))} km, closed at "
            f"{fmt(F(d['v2']) - F(d['v1']))} km/h.",
        ),
    ),
    make_family(
        "tsd_stoppage",
        ("speed", "run", "halt", "distance", "ask"),
        [
            (60, 45, 15, 45, "total_hours"),
            (45, 40, 20, 30, "halt_minutes_total"),
            (72, 50, 10, 90, "effective_speed_kmph"),
            (50, 36, 24, 60, "halt_pct_of_time"),
            (30, 40, 20, 60, "total_hours"),
        ],
        _t_stoppage,
        _a_stoppage,
        _dsmart,
        lambda d, c: _explain(
            d, c,
            f"one {fmt(d['run'])}-minute run covers "
            f"{fmt(F(d['speed']) * F(d['run']) / 60)} km before the "
            f"{fmt(d['halt'])}-minute halt.",
        ),
    ),
    make_family(
        "tsd_speed_ratio_time",
        ("r1", "r2", "time_diff", "ask"),
        [
            (2, 3, 2, "slow_time_hours"),
            (3, 5, 4, "sum_time_hours"),
            (4, 5, 1, "fast_time_hours"),
            (4, 7, 3, "slow_pct_more"),
            (5, 8, 6, "slow_time_hours"),
        ],
        _t_speed_ratio_time,
        _a_speed_ratio_time,
        _dsmart,
        lambda d, c: _explain(
            d, c,
            f"times invert the speed ratio to {fmt(d['r2'])}:{fmt(d['r1'])} and "
            f"the time gap is {fmt(d['time_diff'])} hour(s).",
        ),
    ),
    make_family(
        "tsd_circular_meet",
        ("circumference", "s1", "s2", "ask"),
        [
            (600, 30, 18, "first_meet_seconds"),
            (900, 36, 24, "distance_s1_m"),
            (1200, 45, 27, "pct_s2"),
            (400, 54, 36, "first_meet_seconds"),
            (900, 48, 42, "distance_s1_m"),
        ],
        _t_circular_meet,
        _a_circular_meet,
        _dsmart,
        lambda d, c: _explain(
            d, c,
            f"opposite-direction relative speed is "
            f"{fmt((F(d['s1']) + F(d['s2'])) * KMS_TO_MS)} m/s over one lap of "
            f"{fmt(d['circumference'])} m.",
        ),
    ),
    make_family(
        "tsd_cross_each_other",
        ("l1", "l2", "s1", "s2", "ask"),
        [
            (180, 270, 54, 36, "cross_seconds"),
            (120, 180, 54, 36, "pole_times_sum_seconds"),
            (150, 200, 45, 36, "pole_time_ratio"),
            (300, 180, 72, 54, "pole_times_diff_seconds"),
            (160, 240, 60, 30, "cross_seconds"),
        ],
        _t_cross_each_other,
        _a_cross_each_other,
        _dsmart,
        lambda d, c: _explain(
            d, c,
            "each pole time is length divided by that train's own speed in m/s; "
            "the mutual crossing uses the sum of the two speeds.",
        ),
    ),
    make_family(
        "tsd_bus_walker",
        ("bus_speed", "walker_speed", "interval", "ask"),
        [
            (60, 10, 12, "stationary_interval_min"),
            (50, 10, 18, "opposite_interval_min"),
            (45, 9, 20, "bus_spacing_km"),
            (60, 12, 15, "pct_reduction"),
            (60, 15, 20, "stationary_interval_min"),
        ],
        _t_bus_walker,
        _a_bus_walker,
        _dsmart,
        lambda d, c: _explain(
            d, c,
            f"the spacing fixed by the passing interval is "
            f"{fmt((F(d['bus_speed']) - F(d['walker_speed'])) * F(d['interval']) / 60)} km.",
        ),
    ),
    make_family(
        "tsd_stream_ratio",
        ("up_time", "down_time", "stream", "ask"),
        [
            (3, 2, 4, "boat_speed_kmph"),
            (4, 3, 3, "distance_km"),
            (5, 3, 6, "down_speed_kmph"),
            (3, 2, 10, "pct_up_slower"),
            (6, 4, 5, "up_speed_kmph"),
        ],
        _t_stream_ratio,
        _a_stream_ratio,
        _dsmart,
        lambda d, c: _explain(
            d, c,
            "equal distances give (boat - stream) times up-time equals "
            "(boat + stream) times down-time, which fixes the still-water speed.",
        ),
    ),
    make_family(
        "tsd_speed_change_stop",
        ("d1", "s1", "stop_min", "d2", "s2", "ask"),
        [
            (80, 40, 30, 60, 60, "total_hours"),
            (120, 60, 20, 90, 45, "moving_hours"),
            (80, 40, 60, 160, 80, "avg_speed_whole_kmph"),
            (60, 60, 30, 60, 60, "stop_pct_of_total"),
            (60, 60, 60, 120, 60, "second_leg_pct_of_time"),
        ],
        _t_speed_change_stop,
        _a_speed_change_stop,
        _dsmart,
        lambda d, c: _explain(
            d, c,
            f"leg times are {fmt(F(d['d1']) / F(d['s1']))} h and "
            f"{fmt(F(d['d2']) / F(d['s2']))} h with a "
            f"{fmt(F(d['stop_min']) / 60)} h rest between them.",
        ),
    ),
    make_family(
        "tsd_early_late",
        ("slow", "fast", "diff", "ask"),
        [
            (30, 50, 1, "distance_km"),
            (40, 60, 2, "scheduled_hours"),
            (20, 30, 1, "slow_travel_hours"),
            (30, 40, 2, "pct_time_saved"),
            (25, 50, 1, "fast_travel_hours"),
        ],
        _t_early_late,
        _a_early_late,
        _dsmart,
        lambda d, c: _explain(
            d, c,
            "the two travel times differ by twice the stated early/late gap; "
            "their ratio is the inverse ratio of the two speeds.",
        ),
    ),
    make_family(
        "tsd_two_vehicle_gap",
        ("lead", "v1", "v2", "start_gap", "ask"),
        [
            (1, 40, 60, 20, "catch_hours_after_B"),
            (2, 30, 50, 40, "distance_B_km"),
            (1, 45, 75, 30, "catch_hours_after_A"),
            (3, 20, 30, 10, "gap_at_B_start_km"),
            (1, 25, 40, 15, "pct_gap_closed_per_hour"),
        ],
        _t_two_vehicle_gap,
        _a_two_vehicle_gap,
        _dsmart,
        lambda d, c: _explain(
            d, c,
            f"the lead alone contributes "
            f"{fmt(F(d['lead']) * F(d['v1']))} km, added to the "
            f"{fmt(d['start_gap'])} km station gap.",
        ),
    ),
    make_family(
        "tsd_tunnel",
        ("length", "tunnel", "speed_kmph", "ask"),
        [
            (180, 420, 54, "cross_seconds"),
            (150, 400, 45, "inside_seconds"),
            (200, 300, 72, "tunnel_to_pole_ratio"),
            (120, 480, 36, "metres_per_minute"),
            (240, 360, 54, "inside_seconds"),
        ],
        _t_tunnel,
        _a_tunnel,
        _dsmart,
        lambda d, c: _explain(
            d, c,
            f"the speed is {fmt(F(d['speed_kmph']) * KMS_TO_MS)} m/s; crossing "
            "uses the sum of train and tunnel lengths, being fully inside uses "
            "their difference.",
        ),
    ),
    make_family(
        "tsd_walk_scale",
        ("walkers", "length", "walking_speed", "escalator_speed", "ask"),
        [
            (4, 120, 1, 1, "traverse_seconds"),
            (5, 180, 2, 1, "seconds_saved"),
            (3, 100, 2, 1, "gap_m"),
            (6, 200, 3, 1, "pct_time_saved"),
            (8, 240, 2, 1, "traverse_seconds"),
        ],
        _t_walk_scale,
        _a_walk_scale,
        _dsmart,
        lambda d, c: _explain(
            d, c,
            f"ground speed is "
            f"{fmt(F(d['walking_speed']) + F(d['escalator_speed']))} m/s, so "
            f"the traverse takes {fmt(F(d['length']) / (F(d['walking_speed']) + F(d['escalator_speed'])))} s.",
        ),
    ),
    make_family(
        "tsd_circular_same",
        ("circumference", "s1", "s2", "ask"),
        [
            (400, 36, 24, "first_overtake_seconds"),
            (600, 45, 30, "distance_fast_m"),
            (900, 60, 45, "pct_track_by_fast"),
            (300, 54, 36, "first_overtake_seconds"),
            (480, 42, 30, "lap_ratio"),
        ],
        _t_circular_same,
        _a_circular_same,
        _dsmart,
        lambda d, c: _explain(
            d, c,
            f"the relative speed is "
            f"{fmt((F(d['s1']) - F(d['s2'])) * KMS_TO_MS)} m/s over one lap of "
            f"{fmt(d['circumference'])} m.",
        ),
    ),
    make_family(
        "tsd_journey_stops",
        ("distance", "speed", "stops_min", "total_hours", "ask"),
        [
            (240, 60, 30, 5, "extra_delay_min"),
            (180, 45, 20, 5, "effective_speed_kmph"),
            (300, 60, 30, 6, "moving_time_hours"),
            (120, 40, 30, 4, "pct_time_stopped"),
            (200, 50, 20, 5, "extra_delay_min"),
        ],
        _t_journey_stops,
        _a_journey_stops,
        _dsmart,
        lambda d, c: _explain(
            d, c,
            f"pure running time would be "
            f"{fmt(F(d['distance']) / F(d['speed']))} h, while named stops "
            f"take {fmt(F(d['stops_min']) / 60)} h.",
        ),
    ),
    make_family(
        "tsd_kmph_ms",
        ("speed_kmph", "seconds", "ask"),
        [
            (54, 20, "distance_m"),
            (36, 100, "distance_km"),
            (45, 40, "pct_of_km"),
            (60, 45, "seconds_per_km"),
            (90, 12, "distance_cm"),
        ],
        _t_kmph_ms,
        _a_kmph_ms,
        _dsmart,
        lambda d, c: _explain(
            d, c,
            f"{fmt(d['speed_kmph'])} km/h equals "
            f"{fmt(F(d['speed_kmph']) * KMS_TO_MS)} m/s using the 5/18 factor.",
        ),
    ),
    make_family(
        "tsd_two_boats",
        ("still", "stream", "distance", "ask"),
        [
            (12, 4, 24, "meet_hours"),
            (15, 5, 30, "meet_from_A_km"),
            (10, 2, 24, "time_diff_hours"),
            (14, 7, 28, "down_pct_faster"),
            (18, 6, 48, "round_trip_hours"),
        ],
        _t_two_boats,
        _a_two_boats,
        _dsmart,
        lambda d, c: _explain(
            d, c,
            f"downstream is {fmt(F(d['still']) + F(d['stream']))} km/h and "
            f"upstream {fmt(F(d['still']) - F(d['stream']))} km/h, so their "
            "approach speeds add while the stream cancels.",
        ),
    ),
    make_family(
        "tsd_chase_change",
        ("gap", "thief", "police", "change_after", "boost", "ask"),
        [
            (40, 30, 40, 1, 20, "total_hours"),
            (60, 25, 35, 2, 10, "hours_after_boost"),
            (50, 20, 30, 1, 10, "police_distance_km"),
            (80, 15, 25, 2, 5, "thief_distance_km"),
            (20, 40, 50, 1, 10, "pct_speed_boost"),
        ],
        _t_chase_change,
        _a_chase_change,
        _dsmart,
        lambda d, c: _explain(
            d, c,
            f"the first {fmt(d['change_after'])} hour(s) close "
            f"{fmt((F(d['police']) - F(d['thief'])) * F(d['change_after']))} km, "
            "then the boosted closing speed is used for the remainder.",
        ),
    ),
]


def build_time_speed_distance_mains():
    """Return the 120 HARD Mains specs (24 families x 5 variants)."""
    return build_specs(FAMILIES, mains=True)
