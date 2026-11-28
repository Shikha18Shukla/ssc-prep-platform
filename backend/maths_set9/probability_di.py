# -*- coding: utf-8 -*-
"""Probability – Data Interpretation: 24 Prelims-level data families."""

from __future__ import annotations

from .common import F, build_specs, data, ef, near_pct

SOURCE_PDF = "Probability Data Interpretation 01 Class Notes.pdf"
PAGES = {1: SOURCE_PDF, 2: SOURCE_PDF, 3: SOURCE_PDF, 4: SOURCE_PDF}


def R1(a):
    return [(a + 2*i, i+1) for i in range(5)]


def R2(a, b):
    return [(a + i, b + i, i+1) for i in range(5)]


FAMILIES = [
    ef("pdi_class_table", ("boys", "girls", "q"), R2(18, 12),
       "F(girls,boys+girls)",
       lambda d: data([("Case", d["q"]), ("boys", str(d["boys"])), ("girls", str(d["girls"]))])
       + " A student is chosen at random. Find the probability that the student is a girl.",
       "P(girl) = girls/(boys+girls) = {c}.", step=F(1,20)),
    ef("pdi_dice_frequency", ("total", "sixes", "q"), R2(120, 20),
       "F(sixes,total)",
       lambda d: data([("Case", d["q"]), ("throws", str(d["total"])), ("sixes", str(d["sixes"]))])
       + " Find the empirical probability of getting a six.",
       "Empirical probability = sixes/throws = {c}.", step=F(1,20)),
    ef("pdi_card_draw", ("red", "black", "q"), R2(24, 24),
       "F(red,red+black)",
       lambda d: data([("Case", d["q"]), ("red cards", str(d["red"])), ("black cards", str(d["black"]))])
       + " Find the probability of drawing a red card.",
       "P(red) = red/(red+black) = {c}.", step=F(1,20)),
    ef("pdi_bag_composition", ("r", "b", "g", "q"),
       [(6 + i, 4 + i, 2 + i, i+1) for i in range(5)],
       "F(r,r+b+g)",
       lambda d: data([("Case", d["q"]), ("red", str(d["r"])), ("blue", str(d["b"])), ("green", str(d["g"]))])
       + " Find the probability of drawing a red ball.",
       "Red balls divided by total balls gives {c}.", step=F(1,20)),
    ef("pdi_defective_batch", ("good", "bad", "q"), R2(90, 10),
       "F(bad,good+bad)",
       lambda d: data([("Case", d["q"]), ("good units", str(d["good"])), ("defective units", str(d["bad"]))])
       + " Find the probability that a randomly chosen unit is defective.",
       "P(defective) = bad/(good+bad) = {c}.", step=F(1,20)),
    ef("pdi_survey_table", ("yes", "no", "q"), R2(60, 40),
       "F(yes,yes+no)",
       lambda d: data([("Case", d["q"]), ("yes responses", str(d["yes"])), ("no responses", str(d["no"]))])
       + " Find the probability of a randomly chosen respondent answering yes.",
       "P(yes) = yes/(yes+no) = {c}.", step=F(1,20)),
    ef("pdi_at_least_table", ("n", "success", "q"), R2(100, 25),
       "F(success,n)",
       lambda d: data([("Case", d["q"]), ("trials", str(d["n"])), ("successful trials", str(d["success"]))])
       + " Find the empirical probability of at least one success in a single trial.",
       "Relative frequency gives {c}.", step=F(1,20)),
    ef("pdi_conditional_table", ("both", "second", "q"), R2(30, 60),
       "F(both,second)",
       lambda d: data([("Case", d["q"]), ("favourable with condition", str(d["both"])), ("condition cases", str(d["second"]))])
       + " Find the conditional probability.",
       "Divide favourable conditioned cases by all conditioned cases: {c}.", step=F(1,20)),
    ef("pdi_complement_table", ("favour", "total", "q"), R2(30, 100),
       "F(total-favour,total)",
       lambda d: data([("Case", d["q"]), ("favourable cases", str(d["favour"])), ("total cases", str(d["total"]))])
       + " Find the probability of the complementary event.",
       "Complement count is total-favour, giving {c}.", step=F(1,20)),
    ef("pdi_expected_count", ("n", "p", "case"),
       [(100, F(1,5), 1), (200, F(1,4), 2), (150, F(1,3), 3), (80, F(1,2), 4), (120, F(2,5), 5)],
       "F(n)*p",
       lambda d: data([("Case", d["case"]), ("observations", str(d["n"])), ("probability", str(d["p"]))])
       + " Find the expected number of successes.",
       "Expected count = observations × probability = {c}.", step=1),
    ef("pdi_two_draw_table", ("good", "bad", "q"), R2(8, 4),
       "F(C(good,2),C(good+bad,2))",
       lambda d: data([("Case", d["q"]), ("good items", str(d["good"])), ("bad items", str(d["bad"]))])
       + " Two items are drawn without replacement. Find the probability that both are good.",
       "C(good,2)/C(good+bad,2) = {c}.", step=F(1,20)),
    ef("pdi_ratio_prob", ("a", "b", "q"), R2(3, 5),
       "F(a,a+b)",
       lambda d: data([("Case", d["q"]), ("favourable weight", str(d["a"])), ("unfavourable weight", str(d["b"]))])
       + " Find the probability corresponding to the stated ratio.",
       "Probability = a/(a+b) = {c}.", step=F(1,20)),
    ef("pdi_good_bad", ("good", "bad", "q"), R2(18, 6),
       "F(bad,good+bad)",
       lambda d: data([("Case", d["q"]), ("good outcomes", str(d["good"])), ("bad outcomes", str(d["bad"]))])
       + " Find the probability of a bad outcome.",
       "Bad outcomes over all outcomes gives {c}.", step=F(1,20)),
    ef("pdi_team_table", ("men", "women", "q"), R2(10, 8),
       "F(women,men+women)",
       lambda d: data([("Case", d["q"]), ("men", str(d["men"])), ("women", str(d["women"]))])
       + " A team member is chosen at random. Find the probability that the member is a woman.",
       "P(woman) = women/(men+women) = {c}.", step=F(1,20)),
    ef("pdi_favourable_count", ("favour", "total", "q"), R2(45, 180),
       "F(favour,total)",
       lambda d: data([("Case", d["q"]), ("favourable outcomes", str(d["favour"])), ("total outcomes", str(d["total"]))])
       + " Find the probability of a favourable outcome.",
       "Favourable divided by total = {c}.", step=F(1,20)),
    ef("pdi_two_bags", ("bag1", "bag2", "red1", "red2", "q"),
       [(10, 10, 6, 4, 1), (12, 8, 7, 3, 2), (15, 15, 9, 6, 3), (20, 10, 12, 4, 4), (18, 12, 10, 5, 5)],
       "F(red1+red2,bag1+bag2)",
       lambda d: data([("Case", d["q"]), ("bag1 size", str(d["bag1"])), ("bag1 red", str(d["red1"])),
                       ("bag2 size", str(d["bag2"])), ("bag2 red", str(d["red2"]))])
       + " The bags are emptied into one box. Find the probability of drawing a red ball.",
       "Total red balls divided by total balls gives {c}.", step=F(1,20)),
    ef("pdi_colour_table", ("blue", "yellow", "q"), R2(14, 6),
       "F(blue,blue+yellow)",
       lambda d: data([("Case", d["q"]), ("blue balls", str(d["blue"])), ("yellow balls", str(d["yellow"]))])
       + " Find the probability of drawing a blue ball.",
       "Blue balls over total balls = {c}.", step=F(1,20)),
    ef("pdi_pass_fail", ("passed", "failed", "q"), R2(80, 20),
       "F(failed,passed+failed)",
       lambda d: data([("Case", d["q"]), ("passed", str(d["passed"])), ("failed", str(d["failed"]))])
       + " Find the probability that a randomly chosen candidate failed.",
       "Failed candidates divided by all candidates gives {c}.", step=F(1,20)),
    ef("pdi_game_table", ("win", "lose", "q"), R2(12, 18),
       "F(win,win+lose)",
       lambda d: data([("Case", d["q"]), ("wins", str(d["win"])), ("losses", str(d["lose"]))])
       + " Find the probability that the player wins the next game based on relative frequency.",
       "Empirical win probability is win/(win+lose) = {c}.", step=F(1,20)),
    ef("pdi_sample_space", ("favour", "total", "q"), R2(15, 60),
       "F(favour,total)",
       lambda d: data([("Case", d["q"]), ("favourable cases", str(d["favour"])), ("sample space", str(d["total"]))])
       + " Find the probability of the event.",
       "Probability = favourable/sample space = {c}.", step=F(1,20)),
    ef("pdi_mark_table", ("scored", "attempted", "q"), R2(18, 30),
       "F(scored,attempted)",
       lambda d: data([("Case", d["q"]), ("correct marks", str(d["scored"])), ("attempted questions", str(d["attempted"]))])
       + " Find the fraction of attempted questions answered correctly.",
       "Correct attempts over total attempts gives {c}.", step=F(1,20)),
    ef("pdi_draw_table", ("target", "total", "q"), R2(8, 40),
       "F(target,total)",
       lambda d: data([("Case", d["q"]), ("target tickets", str(d["target"])), ("total tickets", str(d["total"]))])
       + " One ticket is drawn. Find the probability that it is a target ticket.",
       "Target tickets over total tickets = {c}.", step=F(1,20)),
    ef("pdi_selection_table", ("selected", "applied", "q"), R2(24, 120),
       "F(selected,applied)",
       lambda d: data([("Case", d["q"]), ("selected candidates", str(d["selected"])), ("applicants", str(d["applied"]))])
       + " Find the selection probability for a randomly chosen applicant.",
       "Selected over applicants gives {c}.", step=F(1,20)),
    ef("pdi_success_table", ("success", "trials", "q"), R2(36, 90),
       "F(success,trials)",
       lambda d: data([("Case", d["q"]), ("successful trials", str(d["success"])), ("total trials", str(d["trials"]))])
       + " Find the experimental probability of success.",
       "Successful trials divided by all trials = {c}.", step=F(1,20)),
]


def build_probability_di():
    return build_specs(FAMILIES)
