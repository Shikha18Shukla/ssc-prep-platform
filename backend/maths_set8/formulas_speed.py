# -*- coding: utf-8 -*-
"""Independent answer sheet for Time, Speed and Distance (Mains), Set 8.

The verifier passes each question's ``verification_data.inputs`` to the
matching formula below.  Nothing is imported from the chapter builder: every
relation is recomputed here from scratch with exact Fractions.
"""

from __future__ import annotations

from .formula_helpers import F, fmt, dec, pct, money, ratio

FORMULAS = {}

_K = F(5, 18)   # km/h -> m/s
_M = F(18, 5)   # m/s -> km/h


FORMULAS["tsd_train_platform"] = lambda d: fmt(
    (F(d["length"] + d["platform"]) / (F(d["speed_kmph"]) * F(5, 18)))
    if d["ask"] == "total_seconds" else
    (F(d["platform"]) / (F(d["speed_kmph"]) * F(5, 18)))
    if d["ask"] == "extra_seconds" else
    ratio(d["length"] + d["platform"], d["length"])
    if d["ask"] == "time_ratio" else
    fmt(F(d["platform"] + 2 * d["length"]))
    if d["ask"] == "distance_m" else
    fmt(F(100) / (F(d["speed_kmph"]) * F(5, 18)))
)


FORMULAS["tsd_opposite_trains"] = lambda d: fmt(
    F(d["l1"] + d["l2"]) / ((F(d["s1"]) + F(d["s2"])) * F(5, 18))
    if d["ask"] == "cross_seconds" else
    (F(d["l1"] + d["l2"]) / ((F(d["s1"]) - F(d["s2"])) * F(5, 18))
     - F(d["l1"] + d["l2"]) / ((F(d["s1"]) + F(d["s2"])) * F(5, 18)))
    if d["ask"] == "extra_seconds_vs_same" else
    F(d["s1"]) * F(5, 18) * (F(d["l1"] + d["l2"]) / ((F(d["s1"]) + F(d["s2"])) * F(5, 18)))
    if d["ask"] == "distance_l1_m" else
    (F(d["l1"] + d["l2"]) / ((F(d["s1"]) + F(d["s2"])) * F(5, 18))) / 60
)


FORMULAS["tsd_same_direction"] = lambda d: fmt(
    F(d["l1"] + d["l2"]) / ((F(d["s1"]) - F(d["s2"])) * F(5, 18))
    if d["ask"] == "overtake_seconds" else
    (F(d["l1"] + d["l2"]) / ((F(d["s1"]) - F(d["s2"])) * F(5, 18))
     - F(d["l1"] + d["l2"]) / ((F(d["s1"]) + F(d["s2"])) * F(5, 18)))
    if d["ask"] == "extra_seconds_vs_opposite" else
    F(d["s1"]) * F(5, 18) * (F(d["l1"] + d["l2"]) / ((F(d["s1"]) - F(d["s2"])) * F(5, 18)))
    if d["ask"] == "faster_distance_m" else
    F(d["s2"]) * F(5, 18) * (F(d["l1"] + d["l2"]) / ((F(d["s1"]) - F(d["s2"])) * F(5, 18)))
)


FORMULAS["tsd_boat_updown"] = lambda d: (
    fmt(F(d["one_way"]) / (F(d["boat"]) - F(d["stream"]))
        + F(d["one_way"]) / (F(d["boat"]) + F(d["stream"])))
    if d["ask"] == "round_trip_hours" else
    fmt(2 * F(d["one_way"]) /
        (F(d["one_way"]) / (F(d["boat"]) - F(d["stream"]))
         + F(d["one_way"]) / (F(d["boat"]) + F(d["stream"]))))
    if d["ask"] == "avg_speed_kmph" else
    fmt((F(d["one_way"]) / (F(d["boat"]) - F(d["stream"]))
         - F(d["one_way"]) / (F(d["boat"]) + F(d["stream"]))) * 60)
    if d["ask"] == "extra_minutes" else
    pct(((F(d["boat"]) + F(d["stream"])) / (F(d["boat"]) - F(d["stream"])) - 1) * 100)
    if d["ask"] == "down_pct_faster" else
    fmt(F(d["one_way"]) / (F(d["boat"]) - F(d["stream"])))
)


FORMULAS["tsd_average_halves"] = lambda d: (
    fmt(F(d["distance"]) /
        (F(d["distance"]) / (2 * F(d["s1"])) + F(d["distance"]) / (2 * F(d["s2"]))))
    if d["ask"] == "avg_speed_kmph" else
    fmt(F(d["distance"]) / (2 * F(d["s1"])) + F(d["distance"]) / (2 * F(d["s2"])))
    if d["ask"] == "total_hours" else
    fmt((F(d["distance"]) / (2 * F(d["s2"])) - F(d["distance"]) / (2 * F(d["s1"]))) * 60)
    if d["ask"] == "time_diff_minutes" else
    pct((F(d["distance"]) / (2 * F(d["s1"]))) /
        (F(d["distance"]) / (2 * F(d["s1"])) + F(d["distance"]) / (2 * F(d["s2"]))) * 100)
    if d["ask"] == "first_time_pct" else
    fmt(F(d["distance"]) /
        (F(d["distance"]) / (3 * F(d["s1"])) + 2 * F(d["distance"]) / (3 * F(d["s2"]))))
)


FORMULAS["tsd_speed_increase"] = lambda d: (
    fmt(F(d["n"]) * F(d["base"]) + F(d["gain"]) * F(F(d["n"]) * (F(d["n"]) - 1), 2))
    if d["ask"] == "total_distance_km" else
    fmt(F(d["base"]) + (F(d["n"]) - 1) * F(d["gain"]))
    if d["ask"] == "last_hour_distance_km" else
    fmt((F(d["n"]) * F(d["base"]) + F(d["gain"]) * F(F(d["n"]) * (F(d["n"]) - 1), 2)) / F(d["n"]))
    if d["ask"] == "avg_speed_kmph" else
    pct((F(d["n"]) - 1) * F(d["gain"]) / F(d["base"]) * 100)
    if d["ask"] == "pct_increase" else
    fmt(3 * F(d["base"]) + 3 * F(d["gain"]))
)


FORMULAS["tsd_meeting_point"] = lambda d: (
    fmt(F(d["s1"]) * (F(d["distance"]) / (F(d["s1"]) + F(d["s2"]))))
    if d["ask"] == "from_A_km" else
    fmt(abs(F(d["s1"]) - F(d["s2"])) * (F(d["distance"]) / (F(d["s1"]) + F(d["s2"]))))
    if d["ask"] == "extra_km" else
    fmt((F(d["distance"]) / (F(d["s1"]) + F(d["s2"]))) * 60)
    if d["ask"] == "minutes_to_meet" else
    pct(F(d["s1"]) / (F(d["s1"]) + F(d["s2"])) * 100)
    if d["ask"] == "pct_A" else
    fmt(F(d["s2"]) * (F(d["distance"]) / (F(d["s1"]) + F(d["s2"]))))
)


FORMULAS["tsd_delayed_start"] = lambda d: (
    fmt((F(d["gap"]) - F(d["v1"]) * F(d["delay"])) / (F(d["v2"]) - F(d["v1"])))
    if d["ask"] == "catch_hours_after_second" else
    fmt((F(d["gap"]) - F(d["v1"]) * F(d["delay"])) / (F(d["v2"]) - F(d["v1"])) + F(d["delay"]))
    if d["ask"] == "catch_hours_after_first" else
    fmt(F(d["v2"]) * ((F(d["gap"]) - F(d["v1"]) * F(d["delay"])) / (F(d["v2"]) - F(d["v1"]))))
    if d["ask"] == "distance_from_start_km" else
    fmt(((F(d["gap"]) - F(d["v1"]) * F(d["delay"])) / (F(d["v2"]) - F(d["v1"]))) * 60)
    if d["ask"] == "catch_minutes_after_second" else
    fmt(F(d["gap"]) - F(d["v1"]) * F(d["delay"]))
)


FORMULAS["tsd_stoppage"] = lambda d: (
    fmt((F(d["distance"]) / (F(d["speed"]) * F(d["run"]) / 60)) * (F(d["run"]) + F(d["halt"])) / 60)
    if d["ask"] == "total_hours" else
    fmt((F(d["distance"]) / (F(d["speed"]) * F(d["run"]) / 60)) * F(d["halt"]))
    if d["ask"] == "halt_minutes_total" else
    fmt(F(d["speed"]) * F(d["run"]) / (F(d["run"]) + F(d["halt"])))
    if d["ask"] == "effective_speed_kmph" else
    pct(F(d["halt"]) / (F(d["run"]) + F(d["halt"])) * 100)
    if d["ask"] == "halt_pct_of_time" else
    fmt(F(d["distance"]) / F(d["speed"]))
)


FORMULAS["tsd_speed_ratio_time"] = lambda d: (
    fmt(F(d["r2"]) * (F(d["time_diff"]) / (F(d["r2"]) - F(d["r1"]))))
    if d["ask"] == "slow_time_hours" else
    fmt((F(d["r2"]) + F(d["r1"])) * (F(d["time_diff"]) / (F(d["r2"]) - F(d["r1"]))))
    if d["ask"] == "sum_time_hours" else
    fmt(F(d["r1"]) * (F(d["time_diff"]) / (F(d["r2"]) - F(d["r1"]))))
    if d["ask"] == "fast_time_hours" else
    pct((F(d["r2"]) - F(d["r1"])) / F(d["r1"]) * 100)
    if d["ask"] == "slow_pct_more" else
    ratio(F(d["r2"]) * (F(d["time_diff"]) / (F(d["r2"]) - F(d["r1"]))),
          F(d["r1"]) * (F(d["time_diff"]) / (F(d["r2"]) - F(d["r1"]))))
)


FORMULAS["tsd_circular_meet"] = lambda d: (
    fmt(F(d["circumference"]) / ((F(d["s1"]) + F(d["s2"])) * F(5, 18)))
    if d["ask"] == "first_meet_seconds" else
    fmt(F(d["s1"]) * F(5, 18) * (F(d["circumference"]) / ((F(d["s1"]) + F(d["s2"])) * F(5, 18))))
    if d["ask"] == "distance_s1_m" else
    fmt(F(d["s2"]) * F(5, 18) * (F(d["circumference"]) / ((F(d["s1"]) + F(d["s2"])) * F(5, 18))))
    if d["ask"] == "distance_s2_m" else
    pct(F(d["s2"]) / (F(d["s1"]) + F(d["s2"])) * 100)
)


FORMULAS["tsd_cross_each_other"] = lambda d: (
    fmt(F(d["l1"] + d["l2"]) / ((F(d["s1"]) + F(d["s2"])) * F(5, 18)))
    if d["ask"] == "cross_seconds" else
    fmt(F(d["l1"]) / (F(d["s1"]) * F(5, 18)) + F(d["l2"]) / (F(d["s2"]) * F(5, 18)))
    if d["ask"] == "pole_times_sum_seconds" else
    ratio(F(d["l1"]) / (F(d["s1"]) * F(5, 18)), F(d["l2"]) / (F(d["s2"]) * F(5, 18)))
    if d["ask"] == "pole_time_ratio" else
    fmt(abs(F(d["l1"]) / (F(d["s1"]) * F(5, 18)) - F(d["l2"]) / (F(d["s2"]) * F(5, 18))))
    if d["ask"] == "pole_times_diff_seconds" else
    fmt((F(d["l1"] + d["l2"]) / ((F(d["s1"]) + F(d["s2"])) * F(5, 18))) / 60)
)


FORMULAS["tsd_bus_walker"] = lambda d: (
    fmt(F(d["interval"]) * (F(d["bus_speed"]) - F(d["walker_speed"])) / F(d["bus_speed"]))
    if d["ask"] == "stationary_interval_min" else
    fmt(F(d["interval"]) * (F(d["bus_speed"]) - F(d["walker_speed"])) / (F(d["bus_speed"]) + F(d["walker_speed"])))
    if d["ask"] == "opposite_interval_min" else
    fmt((F(d["bus_speed"]) - F(d["walker_speed"])) * F(d["interval"]) / 60)
    if d["ask"] == "bus_spacing_km" else
    pct(F(d["walker_speed"]) / F(d["bus_speed"]) * 100)
)


FORMULAS["tsd_stream_ratio"] = lambda d: (
    fmt(F(d["stream"]) * (F(d["up_time"]) + F(d["down_time"])) / (F(d["up_time"]) - F(d["down_time"])))
    if d["ask"] == "boat_speed_kmph" else
    fmt((F(d["stream"]) * (F(d["up_time"]) + F(d["down_time"])) / (F(d["up_time"]) - F(d["down_time"]))
         - F(d["stream"])) * F(d["up_time"]))
    if d["ask"] == "distance_km" else
    fmt(F(d["stream"]) * (F(d["up_time"]) + F(d["down_time"])) / (F(d["up_time"]) - F(d["down_time"])) + F(d["stream"]))
    if d["ask"] == "down_speed_kmph" else
    fmt(F(d["stream"]) * (F(d["up_time"]) + F(d["down_time"])) / (F(d["up_time"]) - F(d["down_time"])) - F(d["stream"]))
    if d["ask"] == "up_speed_kmph" else
    pct((F(d["up_time"]) - F(d["down_time"])) / F(d["down_time"]) * 100)
)


FORMULAS["tsd_speed_change_stop"] = lambda d: (
    fmt(F(d["d1"]) / F(d["s1"]) + F(d["stop_min"]) / 60 + F(d["d2"]) / F(d["s2"]))
    if d["ask"] == "total_hours" else
    fmt(F(d["d1"]) / F(d["s1"]) + F(d["d2"]) / F(d["s2"]))
    if d["ask"] == "moving_hours" else
    fmt(F(d["d1"] + d["d2"]) / (F(d["d1"]) / F(d["s1"]) + F(d["stop_min"]) / 60 + F(d["d2"]) / F(d["s2"])))
    if d["ask"] == "avg_speed_whole_kmph" else
    pct((F(d["stop_min"]) / 60) /
        (F(d["d1"]) / F(d["s1"]) + F(d["stop_min"]) / 60 + F(d["d2"]) / F(d["s2"])) * 100)
    if d["ask"] == "stop_pct_of_total" else
    pct((F(d["d2"]) / F(d["s2"])) /
        (F(d["d1"]) / F(d["s1"]) + F(d["stop_min"]) / 60 + F(d["d2"]) / F(d["s2"])) * 100)
)


FORMULAS["tsd_early_late"] = lambda d: (
    fmt(2 * F(d["diff"]) * F(d["slow"]) * F(d["fast"]) / (F(d["fast"]) - F(d["slow"])))
    if d["ask"] == "distance_km" else
    fmt(F(d["diff"]) * (F(d["slow"]) + F(d["fast"])) / (F(d["fast"]) - F(d["slow"])))
    if d["ask"] == "scheduled_hours" else
    fmt((2 * F(d["diff"]) * F(d["slow"]) * F(d["fast"]) / (F(d["fast"]) - F(d["slow"]))) / F(d["slow"]))
    if d["ask"] == "slow_travel_hours" else
    fmt((2 * F(d["diff"]) * F(d["slow"]) * F(d["fast"]) / (F(d["fast"]) - F(d["slow"]))) / F(d["fast"]))
    if d["ask"] == "fast_travel_hours" else
    pct((F(d["fast"]) - F(d["slow"])) / F(d["fast"]) * 100)
)


FORMULAS["tsd_two_vehicle_gap"] = lambda d: (
    fmt((F(d["lead"]) * F(d["v1"]) + F(d["start_gap"])) / (F(d["v2"]) - F(d["v1"])))
    if d["ask"] == "catch_hours_after_B" else
    fmt(F(d["v2"]) * ((F(d["lead"]) * F(d["v1"]) + F(d["start_gap"])) / (F(d["v2"]) - F(d["v1"]))))
    if d["ask"] == "distance_B_km" else
    fmt((F(d["lead"]) * F(d["v1"]) + F(d["start_gap"])) / (F(d["v2"]) - F(d["v1"])) + F(d["lead"]))
    if d["ask"] == "catch_hours_after_A" else
    fmt(F(d["lead"]) * F(d["v1"]) + F(d["start_gap"]))
    if d["ask"] == "gap_at_B_start_km" else
    pct((F(d["v2"]) - F(d["v1"])) / F(d["v1"]) * 100)
)


FORMULAS["tsd_tunnel"] = lambda d: (
    fmt(F(d["length"] + d["tunnel"]) / (F(d["speed_kmph"]) * F(5, 18)))
    if d["ask"] == "cross_seconds" else
    fmt(F(d["tunnel"] - d["length"]) / (F(d["speed_kmph"]) * F(5, 18)))
    if d["ask"] == "inside_seconds" else
    ratio(d["tunnel"] + d["length"], d["length"])
    if d["ask"] == "tunnel_to_pole_ratio" else
    fmt(F(d["speed_kmph"]) * 1000 / 60)
    if d["ask"] == "metres_per_minute" else
    fmt(F(d["length"]) / (F(d["speed_kmph"]) * F(5, 18)))
)


FORMULAS["tsd_walk_scale"] = lambda d: (
    fmt(F(d["length"]) / (F(d["walking_speed"]) + F(d["escalator_speed"])))
    if d["ask"] == "traverse_seconds" else
    fmt(F(d["length"]) / F(d["walking_speed"])
        - F(d["length"]) / (F(d["walking_speed"]) + F(d["escalator_speed"])))
    if d["ask"] == "seconds_saved" else
    fmt(F(d["length"]) / (F(d["walkers"]) + 1))
    if d["ask"] == "gap_m" else
    pct(F(d["escalator_speed"]) / (F(d["walking_speed"]) + F(d["escalator_speed"])) * 100)
    if d["ask"] == "pct_time_saved" else
    fmt(F(d["walkers"]) * F(d["length"]))
)


FORMULAS["tsd_circular_same"] = lambda d: (
    fmt(F(d["circumference"]) / ((F(d["s1"]) - F(d["s2"])) * F(5, 18)))
    if d["ask"] == "first_overtake_seconds" else
    fmt(F(d["s1"]) * F(5, 18) * (F(d["circumference"]) / ((F(d["s1"]) - F(d["s2"])) * F(5, 18))))
    if d["ask"] == "distance_fast_m" else
    pct(F(d["s1"]) / (F(d["s1"]) - F(d["s2"])) * 100)
    if d["ask"] == "pct_track_by_fast" else
    ratio(d["s1"], d["s2"])
)


FORMULAS["tsd_journey_stops"] = lambda d: (
    fmt(F(d["total_hours"]) - F(d["stops_min"]) / 60)
    if d["ask"] == "moving_time_hours" else
    fmt(F(d["distance"]) / F(d["total_hours"]))
    if d["ask"] == "effective_speed_kmph" else
    fmt(F(d["distance"]) / F(d["speed"]))
    if d["ask"] == "scheduled_without_stops_hours" else
    fmt((F(d["total_hours"]) - F(d["distance"]) / F(d["speed"]) - F(d["stops_min"]) / 60) * 60)
    if d["ask"] == "extra_delay_min" else
    pct((F(d["stops_min"]) / 60) / F(d["total_hours"]) * 100)
)


FORMULAS["tsd_kmph_ms"] = lambda d: (
    fmt(F(d["speed_kmph"]) * F(5, 18) * F(d["seconds"]))
    if d["ask"] == "distance_m" else
    fmt(F(d["speed_kmph"]) * F(5, 18) * F(d["seconds"]) / 1000)
    if d["ask"] == "distance_km" else
    pct(F(d["speed_kmph"]) * F(5, 18) * F(d["seconds"]) / 1000 * 100)
    if d["ask"] == "pct_of_km" else
    fmt(3600 / F(d["speed_kmph"]))
    if d["ask"] == "seconds_per_km" else
    fmt(F(d["speed_kmph"]) * F(5, 18) * F(d["seconds"]) * 100)
)


FORMULAS["tsd_two_boats"] = lambda d: (
    fmt(F(d["distance"]) / ((F(d["still"]) + F(d["stream"])) + (F(d["still"]) - F(d["stream"]))))
    if d["ask"] == "meet_hours" else
    fmt((F(d["still"]) + F(d["stream"]))
        * (F(d["distance"]) / ((F(d["still"]) + F(d["stream"])) + (F(d["still"]) - F(d["stream"])))))
    if d["ask"] == "meet_from_A_km" else
    fmt(F(d["distance"]) / (F(d["still"]) - F(d["stream"]))
        - F(d["distance"]) / (F(d["still"]) + F(d["stream"])))
    if d["ask"] == "time_diff_hours" else
    pct(((F(d["still"]) + F(d["stream"])) / (F(d["still"]) - F(d["stream"])) - 1) * 100)
    if d["ask"] == "down_pct_faster" else
    fmt(F(d["distance"]) / (F(d["still"]) + F(d["stream"]))
        + F(d["distance"]) / (F(d["still"]) - F(d["stream"])))
)


FORMULAS["tsd_chase_change"] = lambda d: (
    fmt(F(d["change_after"])
        + (F(d["gap"]) - (F(d["police"]) - F(d["thief"])) * F(d["change_after"]))
        / (F(d["police"]) + F(d["boost"]) - F(d["thief"])))
    if d["ask"] == "total_hours" else
    fmt((F(d["gap"]) - (F(d["police"]) - F(d["thief"])) * F(d["change_after"]))
        / (F(d["police"]) + F(d["boost"]) - F(d["thief"])))
    if d["ask"] == "hours_after_boost" else
    fmt(F(d["police"]) * F(d["change_after"])
        + (F(d["police"]) + F(d["boost"]))
        * ((F(d["gap"]) - (F(d["police"]) - F(d["thief"])) * F(d["change_after"]))
           / (F(d["police"]) + F(d["boost"]) - F(d["thief"]))))
    if d["ask"] == "police_distance_km" else
    fmt(F(d["thief"]) * (F(d["change_after"])
        + (F(d["gap"]) - (F(d["police"]) - F(d["thief"])) * F(d["change_after"]))
        / (F(d["police"]) + F(d["boost"]) - F(d["thief"]))))
    if d["ask"] == "thief_distance_km" else
    pct(F(d["boost"]) / F(d["police"]) * 100)
)
