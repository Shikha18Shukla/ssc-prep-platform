# -*- coding: utf-8 -*-
"""Independently verify the fourth Banking Maths batch (6 x 120 questions).

This script never trusts ``correct_answer``.  Every result is recomputed from
``verification_data.inputs`` using the formula sheets embedded below, which
were written independently of the chapter builders.  The script also validates
the JSON structure, option uniqueness and part counts.

Run:
    python backend/verify_banking_maths_set4_questions.py
"""

from __future__ import annotations

import json
import math
import os
import sys
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

FILES = {
    "Pipe and Cistern": "banking_maths_pipe_and_cistern_questions.json",
    "Average": "banking_maths_average_questions.json",
    "Speed, Time and Distance": "banking_maths_speed_time_distance_questions.json",
    "Problems on Trains": "banking_maths_problems_on_trains_questions.json",
    "Boats and Streams": "banking_maths_boats_and_streams_questions.json",
    "Mensuration – 2D": "banking_maths_mensuration_2d_questions.json",
}

PART_SIZES = {1: 15, 2: 20, 3: 30, 4: 55}
DIFFICULTIES = {"EASY", "MEDIUM", "HARD"}
LETTERS = "ABCD"

F = Fraction
PI = F(22, 7)


def fmt(value) -> str:
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def dec(value, places: int = 2) -> str:
    text = f"{float(value):.{places}f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def rat(a, b) -> str:
    x, y = Fraction(a), Fraction(b)
    scale = math.lcm(x.denominator, y.denominator)
    first = x.numerator * (scale // x.denominator)
    second = y.numerator * (scale // y.denominator)
    divisor = math.gcd(abs(first), abs(second)) or 1
    return f"{first // divisor}:{second // divisor}"


FORMULAS: dict = {}
FORMULAS.update({
    "pc_two_inlets": lambda i: dec(1 / (F(1, i["X"]) + F(1, i["Y"]))),
    "pc_inlet_outlet": lambda i: fmt(F(i["X"] * i["Y"], i["Y"] - i["X"])),
    "pc_three_inlets": lambda i: dec(
        1 / (F(1, i["X"]) + F(1, i["Y"]) + F(1, i["Z"]))
    ),
    "pc_efficiency_ratio": lambda i: dec(F(i["T"], i["M"])),
    "pc_alternate_hours": lambda i: (lambda xh, yh, rx, ry, k, rem: dec(
        F(2 * k) if rem == 0 else (
            F(2 * k) + rem * xh if rem <= rx else F(2 * k + 1) + (rem - rx) * yh
        )
    ))(
        F(i["X"]), F(i["Y"]), F(1, i["X"]), F(1, i["Y"]),
        1 // (F(1, i["X"]) + F(1, i["Y"])),
        1 - (1 // (F(1, i["X"]) + F(1, i["Y"]))) * (F(1, i["X"]) + F(1, i["Y"])),
    ),
    "pc_leak": lambda i: dec(F(i["X"] * i["Y"], i["Y"] - i["X"])),
    "pc_partial_fill": lambda i: fmt(F(i["T"], i["X"])),
    "pc_capacity_litres": lambda i: fmt(
        F(i["C"]) * (F(1, i["X"]) + F(1, i["Y"]))
    ),
    "pc_time_fraction": lambda i: dec(F(i["N"] * i["X"], i["D"])),
    "pc_outlet_only": lambda i: dec(F(i["N"] * i["X"], i["D"])),
    "pc_two_outlets": lambda i: dec(1 / (F(1, i["X"]) + F(1, i["Y"]))),
    "pc_net_rate": lambda i: fmt(F(i["Y"] - i["X"], i["X"] * i["Y"])),
    "pc_large_small": lambda i: fmt(F(i["X"] * i["T"], i["X"] - i["T"])),
    "pc_fill_then_leak": lambda i: fmt(
        F(i["T"]) + (1 - F(i["T"], i["X"])) / (F(1, i["X"]) - F(1, i["Y"]))
    ),
    "pc_half_full": lambda i: dec(F(i["X"] * (i["D"] - i["N"]), i["D"])),
    "pc_three_with_outlet": lambda i: dec(
        1 / (F(1, i["X"]) + F(1, i["Y"]) - F(1, i["Z"]))
    ),
    "pc_rate_per_minute": lambda i: fmt(F(i["C"], i["X"])),
    "pc_remaining_work": lambda i: fmt(
        1 - F(i["T"]) * (F(1, i["X"]) + F(1, i["Y"]))
    ),
    "pc_staggered_start": lambda i: dec(
        F(i["T"]) + (1 - F(i["T"], i["X"])) / (F(1, i["X"]) + F(1, i["Y"]))
    ),
    "pc_outlet_after_hours": lambda i: fmt(
        F(i["T"]) + (1 - F(i["T"], i["X"])) / (F(1, i["X"]) - F(1, i["Y"]))
    ),
    "pc_relative_efficiency": lambda i: fmt(F(i["T"]) * (i["M"] + 1)),
    "pc_alternate_minutes": lambda i: (lambda xh, yh, rx, ry, k, rem: dec(
        F(2 * k) if rem == 0 else (
            F(2 * k) + rem * xh if rem <= rx else F(2 * k + 1) + (rem - rx) * yh
        )
    ))(
        F(i["X"]), F(i["Y"]), F(1, i["X"]), F(1, i["Y"]),
        1 // (F(1, i["X"]) + F(1, i["Y"])),
        1 - (1 // (F(1, i["X"]) + F(1, i["Y"]))) * (F(1, i["X"]) + F(1, i["Y"])),
    ),
    "pc_tank_fraction_rate": lambda i: dec(F(i["T"] * i["D"], i["N"])),
    "pc_compare": lambda i: (
        "Both are equal" if i["X"] == i["Y"] else (
            "First pipe" if i["X"] < i["Y"] else "Second pipe"
        )
    ),
})
FORMULAS.update({
    "av_basic": lambda i: fmt(F(sum(i["values"]), len(i["values"]))),
    "av_two_groups": lambda i: fmt(F(i["N1"] * i["A1"] + i["N2"] * i["A2"], i["N1"] + i["N2"])),
    "av_replacement": lambda i: fmt(F(i["Avg"]) + F(i["New"] - i["Old"], i["N"])),
    "av_added_member": lambda i: fmt(F(i["N"] * i["Avg"] + i["Added"], i["N"] + 1)),
    "av_removed_member": lambda i: fmt(F(i["N"] * i["Avg"] - i["Removed"], i["N"] - 1)),
    "av_missing_value": lambda i: fmt(F(i["N"] * i["Avg"] - sum(i["Known"]))),
    "av_weighted": lambda i: fmt(F(sum(w * m for w, m in i["Pairs"]), sum(w for w, m in i["Pairs"]))),
    "av_age_family": lambda i: fmt(F(i["Avg"]) + i["Years"]),
    "av_marks": lambda i: fmt(F(sum(sorted(i["Marks"])[-i["Top"]:]), i["Top"])),
    "av_consecutive": lambda i: fmt(F(2 * i["First"] + i["Count"] - 1, 2)),
    "av_ratio_split": lambda i: fmt(F(i["R1"] * i["A1"] + i["R2"] * i["A2"], i["R1"] + i["R2"])),
    "av_change_one": lambda i: fmt(F(i["New"] - i["Old"], i["N"])),
    "av_group_sizes": lambda i: rat(i["Combined"] - i["A2"], i["A1"] - i["Combined"]),
    "av_total_from_average": lambda i: fmt(F(i["N"] * i["Avg"])),
    "av_correction": lambda i: fmt(F(i["N"] * i["Avg"] - i["Wrong"] + i["Right"], i["N"])),
    "av_batting": lambda i: dec(F(sum(i["Runs"]), len(i["Runs"]) - i["NotOut"])),
    "av_temperature": lambda i: dec(F(sum(i["Temps"]), len(i["Temps"]))),
    "av_expenditure": lambda i: fmt(F(i["Avg"]) + F(i["Rent"], i["N"])),
    "av_three_groups": lambda i: fmt(F(i["N1"] * i["A1"] + i["N2"] * i["A2"] + i["N3"] * i["A3"], i["N1"] + i["N2"] + i["N3"])),
    "av_find_count": lambda i: fmt(F(i["Added"] - i["NewAvg"], i["NewAvg"] - i["Avg"])),
    "av_find_new_value": lambda i: fmt(F((i["N"] + 1) * i["Target"] - i["N"] * i["Avg"])),
    "av_percentage_marks": lambda i: dec(F(100 * sum(i["Marks"]), i["Max"] * len(i["Marks"]))),
    "av_mixed_series": lambda i: fmt(F(i["Scale"]) * F(sum(i["Values"]), len(i["Values"])) + i["Shift"]),
    "av_compare": lambda i: fmt(abs(F(i["N1"] * i["A1"]) - F(i["N2"] * i["A2"]))),
})
FORMULAS.update({
    "sd_basic_speed": lambda i: fmt(F(i["D"]) / F(i["T"])),
    "sd_basic_time": lambda i: fmt(F(i["D"]) / F(i["S"])),
    "sd_basic_distance": lambda i: fmt(F(i["S"]) * F(i["T"])),
    "sd_kmph_to_mps": lambda i: fmt(F(i["K"]) * F(5) / F(18)),
    "sd_mps_to_kmph": lambda i: fmt(F(i["M"]) * F(18) / F(5)),
    "sd_average_two_legs": lambda i: fmt(
        F(2) * F(i["A"]) * F(i["B"]) / (F(i["A"]) + F(i["B"]))
    ),
    "sd_same_direction": lambda i: fmt((F(i["A"]) - F(i["B"])) * F(i["T"])),
    "sd_opposite_direction": lambda i: fmt(F(i["D"]) / (F(i["A"]) + F(i["B"]))),
    "sd_meeting": lambda i: fmt(F(i["D"]) * F(i["A"]) / (F(i["A"]) + F(i["B"]))),
    "sd_chase": lambda i: fmt(F(i["G"]) / (F(i["A"]) - F(i["B"]))),
    "sd_head_start": lambda i: fmt(
        F(i["A"]) * F(i["H"]) / (F(i["A"]) - F(i["B"]))
    ),
    "sd_two_legs_time": lambda i: fmt(
        F(i["D1"]) / F(i["S1"]) + F(i["D2"]) / F(i["S2"])
    ),
    "sd_distance_ratio": lambda i: rat(i["A"], i["B"]),
    "sd_time_ratio": lambda i: rat(i["B"], i["A"]),
    "sd_speed_ratio": lambda i: rat(i["T2"], i["T1"]),
    "sd_early_late": lambda i: fmt(
        F(i["S1"]) * F(i["S2"]) * (F(i["Late"]) + F(i["Early"]))
        / (F(60) * (F(i["S2"]) - F(i["S1"])))
    ),
    "sd_stoppage": lambda i: fmt(F(60) * (F(1) - F(i["A"]) / F(i["S"]))),
    "sd_round_trip": lambda i: fmt(F(i["D"]) / F(i["A"]) + F(i["D"]) / F(i["B"])),
    "sd_average_three": lambda i: fmt(
        F(3) / (
            F(1) / F(i["A"]) + F(1) / F(i["B"]) + F(1) / F(i["C"])
        )
    ),
    "sd_meet_three": lambda i: fmt(
        F(i["D"]) * (F(i["A"]) + F(i["B"]) - F(i["C"]))
        / (F(i["A"]) + F(i["B"]))
    ),
    "sd_cross_each_other": lambda i: fmt(F(i["L"]) / (F(i["A"]) - F(i["B"]))),
    "sd_diff_distance": lambda i: fmt(
        abs(F(i["A"]) * F(i["T1"]) - F(i["B"]) * F(i["T2"]))
    ),
    "sd_unit_conversion_mix": lambda i: fmt(
        F(i["Metres"]) * F(18) / F(5) / F(i["Seconds"])
    ),
    "sd_compare": lambda i: rat(i["A"], i["B"] * 18 // 5),
})
FORMULAS.update({
    "tr_cross_pole": lambda d: fmt(
        F(d["Length"]) / (F(d["Speed"]) * F(5, 18))
    ),
    "tr_cross_platform": lambda d: fmt(
        F(d["TrainLength"] + d["PlatformLength"])
        / (F(d["Speed"]) * F(5, 18))
    ),
    "tr_cross_bridge": lambda d: fmt(
        F(d["TrainLength"] + d["BridgeLength"], d["Time"]) * F(18, 5)
    ),
    "tr_cross_man_same": lambda d: fmt(
        F(d["TrainLength"])
        / (F(d["TrainSpeed"] - d["ManSpeed"]) * F(5, 18))
    ),
    "tr_cross_man_opposite": lambda d: fmt(
        F(d["TrainLength"])
        / (F(d["TrainSpeed"] + d["ManSpeed"]) * F(5, 18))
    ),
    "tr_two_opposite": lambda d: fmt(
        F(d["Length1"] + d["Length2"])
        / (F(d["Speed1"] + d["Speed2"]) * F(5, 18))
    ),
    "tr_two_same": lambda d: fmt(
        F(d["Length1"] + d["Length2"])
        / (F(d["FastSpeed"] - d["SlowSpeed"]) * F(5, 18))
    ),
    "tr_length_from_time": lambda d: fmt(
        F(d["PlatformLength"], d["PlatformTime"] - d["PoleTime"])
        * F(d["PoleTime"])
    ),
    "tr_platform_length": lambda d: fmt(
        F(d["Speed"]) * F(5, 18) * F(d["Time"]) - F(d["TrainLength"])
    ),
    "tr_speed_conversion": lambda d: fmt(F(d["Speed"]) * F(5, 18)),
    "tr_tunnel": lambda d: fmt(
        F(d["TrainLength"] + d["TunnelLength"])
        / (F(d["Speed"]) * F(5, 18))
    ),
    "tr_passes_point": lambda d: fmt(
        F(d["Length"], d["Time"]) * F(18, 5)
    ),
    "tr_relative_speed": lambda d: fmt(
        F(
            (d["Speed1"] + d["Speed2"])
            if d["Direction"] == "opposite"
            else (d["Speed1"] - d["Speed2"])
        )
        * F(5, 18)
    ),
    "tr_length_ratio": lambda d: rat(d["Time1"], d["Time2"]),
    "tr_meeting_time": lambda d: fmt(
        F(d["Distance"], d["Speed1"] + d["Speed2"])
    ),
    "tr_gap_catch": lambda d: fmt(
        F(d["Gap"], d["FastSpeed"] - d["SlowSpeed"])
    ),
    "tr_cross_each_other": lambda d: fmt(
        F(d["Length1"] + d["Length2"], d["Time"]) * F(18, 5)
        - F(d["Speed1"])
    ),
    "tr_speed_after_cross": lambda d: fmt(
        F(d["PlatformLength"], d["PlatformTime"] - d["PoleTime"]) * F(18, 5)
    ),
    "tr_catch_up": lambda d: fmt(
        F(
            d["SlowSpeed"] * d["StartGapHours"] * d["FastSpeed"],
            d["FastSpeed"] - d["SlowSpeed"],
        )
    ),
    "tr_signal": lambda d: fmt(
        F(d["Speed"]) * F(5, 18) * F(d["Time"])
    ),
    "tr_distance_minutes": lambda d: fmt(
        F(d["Speed"] * d["Minutes"], 60)
    ),
    "tr_journey_average": lambda d: fmt(
        F(2 * d["Speed1"] * d["Speed2"], d["Speed1"] + d["Speed2"])
    ),
    "tr_combined_length": lambda d: fmt(
        F(d["Speed"]) * F(5, 18) * F(d["Time1"] + d["Time2"])
    ),
    "tr_compare": lambda d: fmt(
        abs(F(d["Distance1"], d["Time1"]) - F(d["Distance2"], d["Time2"]))
    ),
})
FORMULAS.update({
    "bs_downstream": lambda d: fmt(F(d["Still"]) + F(d["Stream"])),
    "bs_upstream": lambda d: fmt(F(d["Still"]) - F(d["Stream"])),
    "bs_still_from_speeds": lambda d: fmt((F(d["Down"]) + F(d["Up"])) / 2),
    "bs_stream_from_speeds": lambda d: fmt((F(d["Down"]) - F(d["Up"])) / 2),
    "bs_down_distance": lambda d: fmt((F(d["Still"]) + F(d["Stream"])) * F(d["Time"])),
    "bs_up_time": lambda d: fmt(F(d["Distance"]) / (F(d["Still"]) - F(d["Stream"]))),
    "bs_round_trip": lambda d: fmt(
        F(d["Distance"]) / (F(d["Still"]) + F(d["Stream"]))
        + F(d["Distance"]) / (F(d["Still"]) - F(d["Stream"]))
    ),
    "bs_still_from_round": lambda d: fmt(
        (
            F(d["Distance"])
            + (
                lambda disc: F(
                    math.isqrt(disc.numerator * disc.denominator), disc.denominator
                )
            )(
                F(d["Distance"]) ** 2
                + F(d["Time"]) ** 2 * F(d["Stream"]) ** 2
            )
        )
        / F(d["Time"])
    ),
    "bs_stream_from_round": lambda d: fmt(
        (
            lambda disc: F(
                math.isqrt(disc.numerator * disc.denominator), disc.denominator
            )
        )(
            F(d["Still"]) ** 2
            - 2 * F(d["Distance"]) * F(d["Still"]) / F(d["Time"])
        )
    ),
    "bs_ratio_up_down": lambda d: rat(
        F(d["Down"]) + F(d["Up"]), F(d["Down"]) - F(d["Up"])
    ),
    "bs_between_points": lambda d: fmt(
        2 * F(d["Stream"]) * F(d["DownTime"]) * F(d["UpTime"])
        / (F(d["UpTime"]) - F(d["DownTime"]))
    ),
    "bs_two_boats": lambda d: fmt(
        abs(F(d["Still1"]) - F(d["Still2"])) * F(d["Time"])
    ),
    "bs_row_against": lambda d: fmt(
        F(d["Still"]) - F(d["Distance"]) / F(d["Time"])
    ),
    "bs_current_effect": lambda d: fmt(2 * F(d["Stream"])),
    "bs_speed_diff": lambda d: fmt(2 * F(d["Stream"]) * F(d["Time"])),
    "bs_time_diff": lambda d: fmt(
        F(d["Distance"]) / (F(d["Still"]) - F(d["Stream"]))
        - F(d["Distance"]) / (F(d["Still"]) + F(d["Stream"]))
    ),
    "bs_man_row": lambda d: fmt(
        (
            F(d["DownDist"]) / F(d["DownTime"])
            - F(d["UpDist"]) / F(d["UpTime"])
        )
        / 2
    ),
    "bs_float": lambda d: fmt(F(d["Stream"]) * F(d["Time"])),
    "bs_average_round": lambda d: fmt(
        (F(d["Still"]) ** 2 - F(d["Stream"]) ** 2) / F(d["Still"])
    ),
    "bs_return_time": lambda d: fmt(
        F(d["DownTime"]) * (F(d["Still"]) + F(d["Stream"]))
        / (F(d["Still"]) - F(d["Stream"]))
    ),
    "bs_kmph_conversion": lambda d: fmt(
        (F(d["StillMs"]) + F(d["StreamMs"])) * F(18, 5)
    ),
    "bs_distance_time_diff": lambda d: fmt(
        (
            (
                lambda disc: F(
                    math.isqrt(disc.numerator * disc.denominator), disc.denominator
                )
            )(
                F(d["Distance"]) ** 2
                + F(d["TimeDiff"]) ** 2 * F(d["Still"]) ** 2
            )
            - F(d["Distance"])
        )
        / F(d["TimeDiff"])
    ),
    "bs_relative_boats": lambda d: fmt(
        (F(d["Still1"]) + F(d["Still2"])) * F(d["Time"])
    ),
    "bs_compare": lambda d: (
        lambda with_stream, against_stream: (
            d["Name1"]
            if with_stream > against_stream
            else d["Name2"]
            if against_stream > with_stream
            else "Both are equal"
        )
    )(F(d["Still1"]) + F(d["Stream"]), F(d["Still2"]) - F(d["Stream"])),
})
FORMULAS.update({
    "m2_square_area": lambda d: fmt(F(d["s"]) ** 2) + " sq m",
    "m2_square_perimeter": lambda d: fmt(4 * F(d["s"])) + " m",
    "m2_rectangle_area": lambda d: fmt(F(d["L"]) * F(d["W"])) + " sq m",
    "m2_rectangle_perimeter": lambda d: fmt(2 * (F(d["L"]) + F(d["W"]))) + " m",
    "m2_triangle_area": lambda d: fmt(F(d["b"] * d["h"], 2)) + " sq m",
    "m2_triangle_perimeter": lambda d: fmt(F(d["a"] + d["b"] + d["c"])) + " m",
    "m2_circle_area": lambda d: fmt(PI * F(d["r"]) ** 2) + " sq m",
    "m2_circle_circumference": lambda d: fmt(2 * PI * F(d["r"])) + " m",
    "m2_semicircle_area": lambda d: fmt(PI * F(d["r"]) ** 2 / 2) + " sq m",
    "m2_semicircle_perimeter": lambda d: fmt(PI * F(d["r"]) + 2 * F(d["r"])) + " m",
    "m2_parallelogram_area": lambda d: fmt(F(d["b"]) * F(d["h"])) + " sq m",
    "m2_parallelogram_perimeter": lambda d: fmt(2 * (F(d["a"]) + F(d["b"]))) + " m",
    "m2_rhombus_area": lambda d: fmt(F(d["d1"] * d["d2"], 2)) + " sq m",
    "m2_rhombus_perimeter": lambda d: fmt(4 * F(d["s"])) + " m",
    "m2_trapezium_area": lambda d: fmt(F(d["a"] + d["b"], 2) * F(d["h"])) + " sq m",
    "m2_trapezium_perimeter": lambda d: fmt(F(d["a"] + d["b"] + d["c"] + d["d"])) + " m",
    "m2_composite_rect_square": lambda d: fmt(
        F(d["L"]) * F(d["W"]) + F(d["s"]) ** 2
    ) + " sq m",
    "m2_composite_circle_square": lambda d: fmt(
        F(d["s"]) ** 2 - PI * F(d["r"]) ** 2
    ) + " sq m",
    "m2_path_area": lambda d: fmt(
        F((d["L"] + 2 * d["w"]) * (d["W"] + 2 * d["w"])) - F(d["L"] * d["W"])
    ) + " sq m",
    "m2_square_diagonal": lambda d: fmt(F(d["s"])) + "√2 m",
    "m2_rect_diagonal": lambda d: fmt(F(next(k for k in range(1, d["L"] + d["W"] + 1) if k * k == d["L"] ** 2 + d["W"] ** 2))) + " m",
    "m2_tiles_cost": lambda d: "₹" + fmt(
        F(d["L"] * d["W"] * 10000, d["tile_cm"] ** 2) * F(d["rate"])
    ),
    "m2_fencing_cost": lambda d: "₹" + fmt(
        2 * (F(d["L"]) + F(d["W"])) * F(d["rate"])
    ),
    "m2_compare": lambda d: fmt(F(d["s"]) ** 2 - F(d["L"] * d["W"])) + " sq m",
})


def expected_answer(item) -> str:
    meta = item.get("verification_data") or {}
    family = meta.get("family")
    if family not in FORMULAS:
        raise ValueError(f"unhandled verification family: {family}")
    return str(FORMULAS[family](meta.get("inputs") or {}))


def main() -> int:
    failures: list[str] = []
    total = 0
    seen_ids: set[str] = set()
    for chapter, filename in FILES.items():
        path = os.path.join(DATA, filename)
        with open(path, encoding="utf-8") as handle:
            items = json.load(handle)
        if len(items) != 120:
            failures.append(f"{chapter}: expected 120 items, found {len(items)}")
        parts = {part: 0 for part in PART_SIZES}
        for index, item in enumerate(items):
            total += 1
            tag = f"{chapter}#{index + 1} ({item.get('id')})"
            if item.get("id") in seen_ids:
                failures.append(f"{tag}: duplicate id")
            seen_ids.add(item.get("id"))
            if item.get("chapter") != chapter:
                failures.append(f"{tag}: chapter label mismatch")
            if item.get("difficulty") not in DIFFICULTIES:
                failures.append(f"{tag}: bad difficulty {item.get('difficulty')}")
            part = item.get("part")
            if part not in PART_SIZES:
                failures.append(f"{tag}: bad part {part}")
            else:
                parts[part] += 1
            options = item.get("options", [])
            if len(options) != 4 or len(set(map(str, options))) != 4:
                failures.append(f"{tag}: options are not four distinct strings")
                continue
            letter = item.get("correct_option")
            if letter not in LETTERS:
                failures.append(f"{tag}: bad correct_option {letter}")
                continue
            if str(options[LETTERS.index(letter)]) != str(item.get("correct_answer")):
                failures.append(f"{tag}: correct_option/correct_answer mismatch")
            matches = [option for option in options if str(option) == str(item.get("correct_answer"))]
            if len(matches) != 1:
                failures.append(f"{tag}: correct answer is not unique among options")
            if not str(item.get("explanation", "")).strip():
                failures.append(f"{tag}: missing explanation")
            if not item.get("verification_data"):
                failures.append(f"{tag}: missing verification_data")
                continue
            try:
                expected = expected_answer(item)
            except Exception as exc:  # noqa: BLE001
                failures.append(f"{tag}: recomputation error {exc}")
                continue
            if expected != str(item.get("correct_answer")):
                failures.append(
                    f"{tag}: recomputed {expected!r} != stored {item.get('correct_answer')!r}"
                )
        for part, size in PART_SIZES.items():
            if parts.get(part) != size:
                failures.append(f"{chapter}: part {part} has {parts.get(part)}, expected {size}")

    print(f"verified {total} questions across {len(FILES)} chapters")
    if failures:
        print(f"FAILED {len(failures)} checks:")
        for line in failures[:80]:
            print(" -", line)
        return 1
    print("all answers independently recomputed; structure and options valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
