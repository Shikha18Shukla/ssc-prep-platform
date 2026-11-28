# -*- coding: utf-8 -*-
"""Independent answer sheet for Ages Set 7 (Mains + DI).

The verifier passes the exact ``verification_data.inputs`` dictionary from a
question to the lambda stored here; no builder module is imported.
"""

from __future__ import annotations

from .formula_helpers import F, fmt, dec, pct, money, ratio

FORMULAS = {}

# ---- Ages (Mains) -------------------------------------------------------

FORMULAS["am_three_shift_pair"] = lambda d: fmt(
    sum(c * k for c, k in zip(d["coefs"], [d["a"] * d["u"], d["b"] * d["u"], d["c"] * d["u"]]))
)

FORMULAS["am_fraction_sum_diff"] = lambda d: fmt(
    sum(c * val for c, val in zip(
        d["coefs"],
        [
            F(d["fn1"] * ((d["p"] * d["u"] + d["shift"]) + (d["q"] * d["u"] + d["shift"])), d["fd1"]),
            d["p"] * d["u"] + d["shift"],
            d["q"] * d["u"] + d["shift"],
        ],
    ))
)

FORMULAS["am_replacement_average"] = lambda d: fmt(
    F(d["n"] * d["avg"] + d["n"] * d["k"] - d["extra_leave"] * (d["leave_age"] + d["k"]) + d["join_age"], d["n"] - d["extra_leave"] + 1)
    if d["ask"] == "new_avg" else
    (d["target"] * (d["n"] - d["extra_leave"] + 1) - (d["n"] * d["avg"] + d["n"] * d["k"] - d["extra_leave"] * (d["leave_age"] + d["k"])))
    if d["ask"] == "join_age" else
    (F(d["n"] * d["avg"] + d["n"] * d["k"] - (d["target"] * (d["n"] - d["extra_leave"] + 1) - d["join_age"]), d["extra_leave"]) - d["k"])
    if d["ask"] == "leave_age" else
    (d["n"] * d["avg"])
)

FORMULAS["am_new_birth_average"] = lambda d: fmt(
    F(d["n"] * (d["avg0"] + d["k1"] + d["k2"]) + d["k2"], d["n"] + 2)
    if d["ask"] == "avg" else
    (d["n"] * (d["avg0"] + d["k1"] + d["k2"]) + d["k2"])
    if d["ask"] == "total" else
    d["k2"]
)

FORMULAS["am_reciprocal_product"] = lambda d: fmt(
    d["coefs"][0] * (d["p"] * d["u"]) + d["coefs"][1] * (d["q"] * d["u"])
)

FORMULAS["am_admission_service"] = lambda d: fmt(
    d["coefs"][0] * (d["r"] * d["t"]) + d["coefs"][1] * (d["s"] * d["t"])
    + d["coefs"][2] * (d["p"] * d["u"]) + d["coefs"][3] * (d["q"] * d["u"])
)

FORMULAS["am_unequal_gaps_ratio"] = lambda d: fmt(
    d["coefs"][0] * (d["a"] * d["u"] + d["k"]) + d["coefs"][1] * (d["b"] * d["u"] + d["k"])
    + (2 * d["m"] if d["ask"] == "future_sum" else 0)
)

FORMULAS["am_hidden_multiple_family"] = lambda d: fmt(
    d["coefs"][0] * d["x"] + d["coefs"][1] * (d["m1"] * d["x"] + d["a1"]) + d["coefs"][2] * (d["m2"] * d["x"] + d["a2"])
)

FORMULAS["am_group_avg_exit_entry"] = lambda d: fmt(
    F(d["n"] * d["avg"] - d["leave_n"] * d["leave_avg"] + d["join_n"] * d["join_avg"] + (d["n"] - d["leave_n"] + d["join_n"]) * d["k"], d["n"] - d["leave_n"] + d["join_n"])
    if d["ask"] == "avg_after_k" else
    (d["n"] * d["avg"] - d["leave_n"] * d["leave_avg"] + d["join_n"] * d["join_avg"] + (d["n"] - d["leave_n"] + d["join_n"]) * d["k"])
    if d["ask"] == "total_after_k" else
    (d["n"] - d["leave_n"] + d["join_n"])
)

FORMULAS["am_future_different_pair"] = lambda d: fmt(
    d["coefs"][0] * (d["a"] * d["u"]) + d["coefs"][1] * (d["b"] * d["u"])
    + d["coefs"][2] * ((d["a"] * d["u"] if d["base"] == "A" else d["b"] * d["u"]) + d["e"])
)

FORMULAS["am_percentage_ages"] = lambda d: fmt(
    d["coefs"][0] * (F(d["p"] * d["u"], 100) if d["anchor"] == "A_of_B" else d["u"])
    + d["coefs"][1] * (d["u"] if d["anchor"] == "A_of_B" else F(d["p"] * d["u"], 100))
)

FORMULAS["am_simultaneous_linear"] = lambda d: fmt(
    d["coefs"][0] * F(d["rhs1"] * d["d2"] - d["rhs2"] * d["d1"], d["c1"] * d["d2"] - d["c2"] * d["d1"])
    + d["coefs"][1] * F(d["c1"] * d["rhs2"] - d["c2"] * d["rhs1"], d["c1"] * d["d2"] - d["c2"] * d["d1"])
)

FORMULAS["am_three_time_chain"] = lambda d: fmt(
    (d["a"] * d["u"] + d["k"]) if d["ask"] == "A" else
    (d["b"] * d["u"] + d["k"] + d["gap"]) if d["ask"] == "C" else
    ((d["a"] * d["u"] + d["k"]) + (d["b"] * d["u"] + d["k"]) + (d["b"] * d["u"] + d["k"] + d["gap"])) if d["ask"] == "sum" else
    ((d["b"] * d["u"] + d["k"]) - (d["b"] * d["u"] + d["k"] + d["gap"])) if d["ask"] == "gapBC" else
    ((d["b"] * d["u"] + d["k"] + d["gap"]) + d["m"])
)

FORMULAS["am_average_subset"] = lambda d: fmt(
    (d["n"] * d["avg"] - d["t"] * d["old"] - d["s"] * d["young"]) if d["ask"] == "middle" else
    (d["n"] * d["avg"] - d["t"] * d["old"] - d["s"] * d["young"] + d["rem_count"] * d["k"]) if d["ask"] == "middle_future" else
    (d["t"] * d["old"] + d["s"] * d["young"]) if d["ask"] == "extremes_total" else
    F(d["n"] * d["avg"] - d["t"] * d["old"] - d["s"] * d["young"], d["rem_count"]) if d["ask"] == "avg_remaining" else
    (d["n"] * d["avg"] + d["n"] * d["k"])
)

FORMULAS["am_ratio_change_find_time"] = lambda d: (
    lambda A, B, k: fmt(
        k if d["ask"] == "years" else
        (A + k if d["direction"] == "future" else A - k) if d["ask"] == "age" else
        (A + B + 2 * k) if d["ask"] == "sum_after" else (A - k)
    )
)(F(d["p"] * d["total"], d["p"] + d["q"]), F(d["q"] * d["total"], d["p"] + d["q"]),
  F(d["s"] * F(d["p"] * d["total"], d["p"] + d["q"]) - d["r"] * F(d["q"] * d["total"], d["p"] + d["q"]),
    (d["r"] - d["s"]) if d["direction"] == "future" else (d["s"] - d["r"])))

FORMULAS["am_two_future_conditions"] = lambda d: (
    lambda A, B, C: fmt(d["coefs"][0] * A + d["coefs"][1] * B + d["coefs"][2] * C)
)(F(d["u"]), F(d["b"] * (d["u"] + d["m"]), d["a"]) - d["m"],
  F(d["d2"] * ((d["u"] if d["mode"] == "AC" else F(d["b"] * (d["u"] + d["m"]), d["a"]) - d["m"]) + d["n"]), d["c2"]) - d["n"])

FORMULAS["am_joining_service_two"] = lambda d: (
    lambda A, joinB: fmt(
        d["coefs"][0] * d["x"] + d["coefs"][1] * joinB
        + d["coefs"][2] * (A - d["x"]) + d["coefs"][3] * (F(d["gap"] * d["q"], d["p"] - d["q"]) - joinB)
        + d["coefs"][4] * A
    )
)(F(d["gap"] * d["p"], d["p"] - d["q"]), d["x"] + d["lag"] - d["gap"])

FORMULAS["am_fraction_two_conditions"] = lambda d: (
    lambda A, B, C: fmt(ratio(A, B)) if d["ask"] == "ratio" else fmt({"A": A, "B": B, "C": C, "total": A + B + C}[d["ask"]])
)(*(((d["m"] + 1) * d["t"], (d["k"] + 1) * d["t"], (d["k"] * d["m"] - 1) * d["t"]) if d["mode"] == "sum" else
    ((d["m"] - 1) * d["t"], (d["k"] - 1) * d["t"], (d["k"] * d["m"] - 1) * d["t"])))

FORMULAS["am_percentage_change_average"] = lambda d: (
    lambda total, count: fmt(d["t"] if d["ask"] == "count" else count if d["ask"] == "remaining" else total if d["ask"] == "total" else F(total, count))
)(d["n"] * (d["avg"] + d["k"]) - d["t"] * d["x_avg"] if d["mode"] == "leave" else d["n"] * (d["avg"] + d["k"]) + d["t"] * d["x_avg"],
  d["n"] - d["t"] if d["mode"] == "leave" else d["n"] + d["t"])

FORMULAS["am_reciprocal_sum_diff"] = lambda d: (
    lambda elder, younger: fmt(
        elder if d["ask"] == "elder" else younger if d["ask"] == "younger" else
        (elder + younger + 2 * d["k"]) if d["ask"] == "sum_after" else
        (elder * younger) if d["ask"] == "product" else ratio(elder + d["k"], younger + d["k"])
    )
)(F(d["s"] + d["d"], 2), F(d["s"] - d["d"], 2))

FORMULAS["am_exam_eligibility"] = lambda d: (
    lambda A, B: fmt(max(0, d["limit"] - min(A, B)) if d["ask"] == "years" else min(A, B))
)(d["p"] * d["u"] + d["k"], d["q"] * d["u"] + d["k"])

FORMULAS["am_time_triple_ratio"] = lambda d: (
    lambda A, B, C: fmt(
        A if d["ask"] == "A" else B if d["ask"] == "B" else C if d["ask"] == "C" else
        (A + B + C) if d["ask"] == "total" else (A + B + C + 3 * d["k"])
    )
)(d["a"] * d["t"], d["b"] * d["t"], F(d["d"] * d["b"] * d["t"], d["c"]))

FORMULAS["am_future_family_average"] = lambda d: (
    lambda total, count: fmt(F(total, count) if d["ask"] == "avg" else total if d["ask"] == "total" else count)
)(d["n"] * (d["avg"] + d["k"]) - d["leaving"] * (d["leave_age"] + d["k"]), d["n"] + d["born"] - d["leaving"])

FORMULAS["am_linear_combo_ratio"] = lambda d: fmt(
    d["coefs"][0] * (d["p"] * d["u"] + d["k"]) + d["coefs"][1] * (d["q"] * d["u"] + d["k"])
)

# ---- Ages – Data Interpretation ----------------------------------------

FORMULAS["ad_table_lookup"] = lambda d: fmt(
    [d["ages"][0], d["ages"][1], d["ages"][2], sum(d["ages"]),
     abs(d["ages"][0] - d["ages"][1])][d["ask"]]
)

FORMULAS["ad_table_difference"] = lambda d: fmt(
    abs(d["ages"][d["pair"][0]] - d["ages"][d["pair"][1]])
)

FORMULAS["ad_table_sum"] = lambda d: fmt(sum(d["ages"]))

FORMULAS["ad_table_average"] = lambda d: fmt(F(sum(d["ages"]), len(d["ages"])))

FORMULAS["ad_table_future"] = lambda d: fmt(
    d["ages"][d["idx"]] + (d["k"] if d["future"] else -d["k"])
)

FORMULAS["ad_table_ratio"] = lambda d: fmt(
    ratio(d["a"], d["b"]) if d["order"] == 0 else ratio(d["b"], d["a"])
)

FORMULAS["ad_family_caselet"] = lambda d: fmt(
    [d["father"], d["mother"], d["child"], d["father"] + d["mother"],
     d["father"] + d["mother"] + d["child"]][d["ask"]]
)

FORMULAS["ad_yearwise"] = lambda d: fmt(
    d["vals"][d["idx"]] if d["mode"] == "lookup" else
    (abs(d["vals"][1] - d["vals"][0]) if d["mode"] == "change" else
     d["vals"][0] + d["vals"][1])
)

FORMULAS["ad_average_compare"] = lambda d: fmt(
    F(sum(d["a"]), len(d["a"])) if d["ask"] == "A" else
    (F(sum(d["b"]), len(d["b"])) if d["ask"] == "B" else
     abs(F(sum(d["a"]), len(d["a"])) - F(sum(d["b"]), len(d["b"]))))
)

FORMULAS["ad_percentage_of_age"] = lambda d: fmt(
    F(d["ages"][d["idx"]] * d["percent"], 100)
)

FORMULAS["ad_future_ratio"] = lambda d: fmt(ratio(d["a"] + d["k"], d["b"] + d["k"]))

FORMULAS["ad_past_ratio"] = lambda d: fmt(ratio(d["a"] - d["k"], d["b"] - d["k"]))

FORMULAS["ad_join_average"] = lambda d: fmt(
    d["n"] * d["avg"] + d["new"] if d["ask"] == "total" else
    F(d["n"] * d["avg"] + d["new"], d["n"] + 1)
)

FORMULAS["ad_leave_average"] = lambda d: fmt(
    d["n"] * d["avg"] - d["leaving"] if d["ask"] == "total" else
    F(d["n"] * d["avg"] - d["leaving"], d["n"] - 1)
)

FORMULAS["ad_bar_pairs"] = lambda d: fmt(
    d["pairs"][d["idx"]][0] + d["pairs"][d["idx"]][1]
    if d["mode"] == "sum_at" else
    (d["pairs"][d["idx"]][0] - d["pairs"][d["idx"]][1]
     if d["mode"] == "diff_at" else
     sum(pair[0] for pair in d["pairs"]))
)

FORMULAS["ad_two_groups_combined"] = lambda d: fmt(
    d["n1"] * d["a1"] + d["n2"] * d["a2"] if d["ask"] == "total" else
    F(d["n1"] * d["a1"] + d["n2"] * d["a2"], d["n1"] + d["n2"])
)

FORMULAS["ad_age_multiples"] = lambda d: fmt(
    [d["k"] * d["a"], d["a"] + d["k"] * d["a"], d["k"] * d["a"] - d["a"]][d["ask"]]
)

FORMULAS["ad_fraction_age"] = lambda d: fmt(
    [F(d["a"], d["k"]), d["a"] + F(d["a"], d["k"]), d["a"] - F(d["a"], d["k"])][d["ask"]]
)

FORMULAS["ad_ratio_missing"] = lambda d: fmt(
    F(d["first"] * d["q"], d["p"]) if d["ask"] == 0 else
    d["first"] + F(d["first"] * d["q"], d["p"])
)

FORMULAS["ad_older_count"] = lambda d: fmt(
    sum(1 for age in d["ages"] if age > d["threshold"])
    if d["mode"] == "older" else
    sum(1 for age in d["ages"] if age < d["threshold"])
)

FORMULAS["ad_median_range"] = lambda d: fmt(
    (d["ages"][len(d["ages"]) // 2] if len(d["ages"]) % 2 else
     F(d["ages"][len(d["ages"]) // 2 - 1] + d["ages"][len(d["ages"]) // 2], 2))
    if d["mode"] == "median" else d["ages"][-1] - d["ages"][0]
)

FORMULAS["ad_two_year_growth"] = lambda d: fmt(
    [d["vals"][1] - d["vals"][0], d["vals"][2] - d["vals"][1],
     d["vals"][2] - d["vals"][0], F(sum(d["vals"]), 3)][d["ask"]]
)

FORMULAS["ad_caselet_future_sum"] = lambda d: fmt(
    sum(d["ages"]) + d["k"] * len(d["ages"]) if d["ask"] == "sum" else
    F(sum(d["ages"]) + d["k"] * len(d["ages"]), len(d["ages"]))
)

FORMULAS["ad_average_after_birth"] = lambda d: fmt(
    d["p1"] + d["p2"] + d["child"] + 3 * d["k"] if d["ask"] == "total" else
    (d["child"] + d["k"] if d["ask"] == "child" else
     F(d["p1"] + d["p2"] + d["child"] + 3 * d["k"], 3))
)
