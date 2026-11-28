# -*- coding: utf-8 -*-
"""Independent verifier formulas for the two Set 7 Partnership chapters.

The lambdas consume only the JSON-serializable ``inputs`` stored by each
builder and never import either builder module.
"""

from __future__ import annotations

from .formula_helpers import F, fmt, dec, pct, money, ratio


def _deduct(amount, tax, cess):
    """Remove tax and a cess on that tax from an amount."""
    tax_amt = F(amount * tax, 100)
    return amount - tax_amt - F(tax_amt * cess, 100)


def _part(amount, weight, total_weight):
    return F(amount * weight, total_weight)


FORMULAS = {
    "pm_timeline_add_withdraw": lambda d: money(
        _part(d["P"], d["cA"] * 12 + d["add"] * (13 - d["am"]),
              d["cA"] * 12 + d["add"] * (13 - d["am"]) + d["cB"] * 12 - d["wd"] * (13 - d["wm"]))
    ),
    "pm_late_join_withdraw_diff": lambda d: money(abs(
        _part(d["P"], d["cA"] * 12 - d["wd"] * (13 - d["wm"]),
              d["cA"] * 12 - d["wd"] * (13 - d["wm"]) + d["cB"] * (13 - d["jm"]))
        - _part(d["P"], d["cB"] * (13 - d["jm"]),
                d["cA"] * 12 - d["wd"] * (13 - d["wm"]) + d["cB"] * (13 - d["jm"]))
    )),
    "pm_working_salary_commission": lambda d: money(_part(
        d["P"] - (
            d["sal"] * d["months"] if d["basis"] == "monthly"
            else F(d["P"] * d["rate"], 100) if d["basis"] == "profit_pct"
            else F(max(0, d["P"] - d["threshold"]) * d["rate"], 100)
        ), d["cB"], d["cA"] + d["cB"]
    )),
    "pm_guaranteed_min_deficiency": lambda d: money(
        _part(d["P"], d["b"], d["a"] + d["b"] + d["c"])
        - (
            max(F(0), F(d["guar"]) - _part(d["P"], d["a"], d["a"] + d["b"] + d["c"]))
            if d["bearer"] == "B_only"
            else F(max(F(0), F(d["guar"]) - _part(d["P"], d["a"], d["a"] + d["b"] + d["c"])) * d["b"], d["b"] + d["c"])
        )
    ),
    "pm_admission_new_ratio": lambda d: money(_part(
        F(d["P"] * (100 - d["new_share"]), 100), d["na"], d["na"] + d["nb"]
    )),
    "pm_retirement_split_share": lambda d: money(
        _part(d["P"], d["a"], d["a"] + d["b"] + d["c"])
        + F(_part(d["P"], d["b"] if d["retire"] == "B" else d["c"],
                  d["a"] + d["b"] + d["c"]) * d["to_a"], d["to_a"] + d["to_other"])
    ),
    "pm_fractional_time_interest": lambda d: money(
        F(d["cB"] * d["rate"] * d["bn"], 100 * d["bd"])
        + _part(d["P"] - F(d["cA"] * d["rate"] * d["an"], 100 * d["ad"])
                - F(d["cB"] * d["rate"] * d["bn"], 100 * d["bd"]),
                F(d["cB"] * d["bn"], d["bd"]),
                F(d["cA"] * d["an"], d["ad"]) + F(d["cB"] * d["bn"], d["bd"]))
    ),
    "pm_loan_interest_tax_cess": lambda d: money(
        _part(d["P"] - _deduct(F(d["loan"] * d["rate"], 100), d["tax"], d["cess"]),
              d["cA"], d["cA"] + d["cB"])
        + (_deduct(F(d["loan"] * d["rate"], 100), d["tax"], d["cess"])
           if d["lender"] == "A" else 0)
    ),
    "pm_reinvest_different_rates": lambda d: money(abs(
        _part(d["P1"], d["ra"], d["ra"] + d["rb"])
        * ((1 + F(d["rateA"] * d["years"], 100)) if d["basis"] == "simple"
           else (1 + F(d["rateA"], 100)) ** d["years"])
        - _part(d["P1"], d["rb"], d["ra"] + d["rb"])
        * ((1 + F(d["rateB"] * d["years"], 100)) if d["basis"] == "simple"
           else (1 + F(d["rateB"], 100)) ** d["years"])
    )),
    "pm_target_bonus": lambda d: money(_part(
        d["P"] - (
            F(max(0, d["P"] - d["target"]) * d["bonus"], 100) if d["basis"] == "excess_pct"
            else F(d["P"] * d["bonus"], 100) if d["basis"] == "total_pct"
            else F(d["bonus"])
        ), d["b"], d["a"] + d["b"]
    )),
    "pm_three_overlapping": lambda d: money(_part(
        d["P"], d["cC"] * (13 - d["jc"]),
        d["cA"] * 12 - d["wd"] * (13 - d["wa_month"])
        + d["cB"] * (13 - d["jb"]) + d["cC"] * (13 - d["jc"])
    )),
    "pm_reverse_total_share": lambda d: money(
        F(d["S"] * (d["cA"] * 12 + d["add"] * (13 - d["am"]) + d["cB"] * (13 - d["jm"])),
          d["cA"] * 12 + d["add"] * (13 - d["am"]) if d["given"] == "A"
          else d["cB"] * (13 - d["jm"]))
    ),
    "pm_reverse_unknown_capital": lambda d: money(
        F(d["d"] * d["months"] * (d["P"] - d["S"]),
          d["S"] * (12 + d["months"]) - d["P"] * d["months"])
        if d["given"] == "B"
        else F(d["S"] * d["months"] * d["d"], 12 * d["P"] - d["S"] * (12 + d["months"]))
    ),
    "pm_equal_share_join_month": lambda d: fmt(
        12 - F(12 * d["cA"], d["cB"]) if d["mode"] == "equal"
        else 12 - F(12 * d["cA"], 2 * d["cB"]) if d["mode"] == "A_twice"
        else 12 - F(24 * d["cA"], d["cB"])
    ),
    "pm_interest_capital_final_ratio": lambda d: ratio(
        F(d["cA"] * d["rate"] * d["an"], 100 * d["ad"])
        + (_part(d["P"] - F(d["cA"] * d["rate"] * d["an"], 100 * d["ad"])
                 - F(d["cB"] * d["rate"] * d["bn"], 100 * d["bd"]),
                 F(d["cA"] * d["an"], d["ad"]),
                 F(d["cA"] * d["an"], d["ad"]) + F(d["cB"] * d["bn"], d["bd"]))
           if d["basis"] == "weighted"
           else _part(d["P"] - F(d["cA"] * d["rate"] * d["an"], 100 * d["ad"])
                      - F(d["cB"] * d["rate"] * d["bn"], 100 * d["bd"]),
                      d["cA"], d["cA"] + d["cB"])),
        F(d["cB"] * d["rate"] * d["bn"], 100 * d["bd"])
        + (_part(d["P"] - F(d["cA"] * d["rate"] * d["an"], 100 * d["ad"])
                 - F(d["cB"] * d["rate"] * d["bn"], 100 * d["bd"]),
                 F(d["cB"] * d["bn"], d["bd"]),
                 F(d["cA"] * d["an"], d["ad"]) + F(d["cB"] * d["bn"], d["bd"]))
           if d["basis"] == "weighted"
           else _part(d["P"] - F(d["cA"] * d["rate"] * d["an"], 100 * d["ad"])
                      - F(d["cB"] * d["rate"] * d["bn"], 100 * d["bd"]),
                      d["cB"], d["cA"] + d["cB"]))
    ),
    "pm_manager_commission_three": lambda d: money(
        _part(d["P"] - (F(d["P"] * d["rate"], 100) if d["basis"] == "gross"
                         else F(max(0, d["P"] - d["threshold"]) * d["rate"], 100)),
              {"A": d["cA"] * d["mA"], "B": d["cB"] * d["mB"],
               "C": d["cC"] * d["mC"]}[d["manager"]],
              d["cA"] * d["mA"] + d["cB"] * d["mB"] + d["cC"] * d["mC"])
        + (F(d["P"] * d["rate"], 100) if d["basis"] == "gross"
           else F(max(0, d["P"] - d["threshold"]) * d["rate"], 100))
    ),
    "pm_successive_ratio_amendment": lambda d: money(
        F(d["P"], 12) * (F(d["oa"], d["oa"] + d["ob"]) * d["change_month"]
                         + F(d["na"], d["na"] + d["nb"]) * (12 - d["change_month"]))
    ),
    "pm_partner_replacement": lambda d: money(_part(
        d["P"], d["cC"] * (13 - d["month"]),
        d["cA"] * 12 + d["cB"] * (d["month"] - 1)
        + (d["cB"] - F(d["cB"] * d["fn"], d["fd"])) * (13 - d["month"])
        + d["cC"] * (13 - d["month"])
    )),
    "pm_salary_commission_net": lambda d: money(_part(
        d["P"] - d["salary"] - (
            F(d["P"] * d["rate"], 100) if d["basis"] == "before_salary"
            else F((d["P"] - d["salary"]) * d["rate"], 100) if d["basis"] == "after_salary"
            else F(max(0, d["P"] - d["threshold"]) * d["rate"], 100)
        ), d["cB"], d["cA"] + d["cB"]
    )),
    "pm_three_share_spread": lambda d: money(
        max(_part(d["P"], w,
                  d["cA"] * 12 - d["wd"] * (13 - d["wd_month"])
                  + d["cB"] * (13 - d["jB"]) + d["cC"] * (13 - d["jC"]))
            for w in (d["cA"] * 12 - d["wd"] * (13 - d["wd_month"]),
                      d["cB"] * (13 - d["jB"]), d["cC"] * (13 - d["jC"])))
        - min(_part(d["P"], w,
                    d["cA"] * 12 - d["wd"] * (13 - d["wd_month"])
                    + d["cB"] * (13 - d["jB"]) + d["cC"] * (13 - d["jC"]))
              for w in (d["cA"] * 12 - d["wd"] * (13 - d["wd_month"]),
                        d["cB"] * (13 - d["jB"]), d["cC"] * (13 - d["jC"])))
    ),
    "pm_guarantee_time_weighted": lambda d: money(
        _part(d["P"], d["cB"] * (13 - d["jB"]),
              d["cA"] * 12 + d["cB"] * (13 - d["jB"]) + d["cC"] * (13 - d["jC"]))
        - (
            max(F(0), F(d["guar"]) - _part(d["P"], d["cA"] * 12,
                d["cA"] * 12 + d["cB"] * (13 - d["jB"]) + d["cC"] * (13 - d["jC"]))) / 2
            if d["bearer"] == "equal"
            else F(max(F(0), F(d["guar"]) - _part(d["P"], d["cA"] * 12,
                    d["cA"] * 12 + d["cB"] * (13 - d["jB"]) + d["cC"] * (13 - d["jC"])))
                   * d["cB"] * (13 - d["jB"]),
                   d["cB"] * (13 - d["jB"]) + d["cC"] * (13 - d["jC"]))
        )
    ),
    "pm_tax_cess_profit_split": lambda d: money(
        _part(_deduct(d["P"], d["tax"], d["cess"]), d["cA"] * 12,
              d["cA"] * 12 + d["cB"] * (13 - d["jB"]))
        if d["basis"] == "gross_profit"
        else _deduct(_part(d["P"], d["cA"] * 12,
                           d["cA"] * 12 + d["cB"] * (13 - d["jB"])),
                     d["tax"], d["cess"])
    ),
    "pm_reverse_total_difference": lambda d: money(F(
        d["S"] * (d["cA"] * 12 - d["wd"] * (13 - d["wm"]) + d["cB"] * (13 - d["jB"])),
        abs(d["cA"] * 12 - d["wd"] * (13 - d["wm"]) - d["cB"] * (13 - d["jB"]))
    )),
    "pm_capstone_guarantee_bonus": lambda d: money(
        _part(d["P"] - d["salary"] - (
            F((d["P"] - d["salary"]) * d["rate"], 100) if d["basis"] == "net"
            else F(max(0, d["P"] - d["target"]) * d["rate"], 100)
        ), d["cB"] * (13 - d["jB"]),
              d["cA"] * 12 + d["cB"] * (13 - d["jB"]) + d["cC"] * (13 - d["jC"]))
        - F(max(F(0), F(d["guar"]) - _part(d["P"] - d["salary"] - (
                F((d["P"] - d["salary"]) * d["rate"], 100) if d["basis"] == "net"
                else F(max(0, d["P"] - d["target"]) * d["rate"], 100)
            ), d["cC"] * (13 - d["jC"]),
               d["cA"] * 12 + d["cB"] * (13 - d["jB"]) + d["cC"] * (13 - d["jC"])))
            * d["cB"] * (13 - d["jB"]),
            d["cA"] * 12 + d["cB"] * (13 - d["jB"]))
    ),
    "pd_total_capital": lambda d: money(d["a"] + d["b"]),
    "pd_simple_ratio": lambda d: ratio(d["a"], d["b"]),
    "pd_one_share": lambda d: money(F(d["P"] * d["a"], d["a"] + d["b"])),
    "pd_share_difference": lambda d: money(F(d["P"] * abs(d["a"] - d["b"]), d["a"] + d["b"])),
    "pd_share_percent": lambda d: pct(F(d["a"] * 100, d["a"] + d["b"] + d["c"])),
    "pd_joining_months": lambda d: money(d["cap"] * d["months"]),
    "pd_profit_from_ratio": lambda d: money(F(d["share_a"] * (d["a"] + d["b"]), d["a"])),
    "pd_capital_missing": lambda d: money(F(d["cap_b"] * d["a"], d["b"])),
    "pd_avg_capital": lambda d: money(F(d["a"] + d["b"] + d["c"], 3)),
    "pd_yearwise_total": lambda d: money(d["p1"] + d["p2"] + d["p3"]),
    "pd_yearwise_growth": lambda d: pct(F((d["p2"] - d["p1"]) * 100, d["p1"])),
    "pd_yearwise_avg": lambda d: money(F(d["p1"] + d["p2"] + d["p3"], 3)),
    "pd_share_from_percent": lambda d: money(F(d["P"] * d["percent"], 100)),
    "pd_ratio_three": lambda d: f'{d["a"]}:{d["b"]}:{d["c"]}',
    "pd_time_weighted_ratio": lambda d: ratio(d["ca"] * d["ma"], d["cb"] * d["mb"]),
    "pd_share_with_time": lambda d: money(F(d["P"] * d["ca"] * d["ma"],
                                            d["ca"] * d["ma"] + d["cb"] * d["mb"])),
    "pd_partner_comparison": lambda d: money(d["s2a"] - d["s1a"]),
    "pd_total_investment_trend": lambda d: money(
        (d["y2a"] + d["y2b"]) - (d["y1a"] + d["y1b"])
    ),
    "pd_highest_share": lambda d: money(max(d["a"], d["b"], d["c"])),
    "pd_lowest_share": lambda d: money(min(d["a"], d["b"], d["c"])),
    "pd_missing_profit": lambda d: money(d["P"] - d["a"] - d["b"]),
    "pd_capital_percent": lambda d: pct(F(d["a"] * 100, d["a"] + d["b"])),
    "pd_avg_monthly_profit": lambda d: money(F(d["P"], d["months"])),
    "pd_two_year_ratio": lambda d: ratio(d["p1"], d["p2"]),
}
