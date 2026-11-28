# -*- coding: utf-8 -*-
"""Canonical family names shared by Set 9 builders and the independent verifier."""

FAMILY_NAMES = {
    "pipe_and_cistern_data_interpretation": [
        "pdi_flow_share", "pdi_rate_table", "pdi_two_pipe_fill", "pdi_leak_effect",
        "pdi_capacity_ratio", "pdi_cycle_output", "pdi_cost_fill", "pdi_waste_loss",
        "pdi_alternate_hours", "pdi_partial_level", "pdi_combined_time", "pdi_efficiency",
        "pdi_tank_dimensions", "pdi_multiple_tanks", "pdi_inlet_outlet", "pdi_intermittent",
        "pdi_flow_increase", "pdi_fill_levels", "pdi_pump_rate", "pdi_time_ratio",
        "pdi_metered_fill", "pdi_average_rate", "pdi_fraction_full", "pdi_joint_delay",
    ],
    "trains_mains": [
        "tm_cross_pole", "tm_cross_platform", "tm_opposite_trains", "tm_same_direction",
        "tm_gap_closure", "tm_platform_ratio", "tm_bridge_cross", "tm_tunnel_cross",
        "tm_delay_meet", "tm_stoppage_loss", "tm_speed_conversion", "tm_length_from_two",
        "tm_goods_passenger", "tm_overtake_time", "tm_telegraph_poles", "tm_meeting_point",
        "tm_crossing_difference", "tm_early_late", "tm_relative_speed", "tm_half_journey",
        "tm_platform_speed", "tm_signal_gap", "tm_two_bridge", "tm_time_ratio",
    ],
    "trains_data_interpretation": [
        "tdi_speed_table", "tdi_length_table", "tdi_cross_pole", "tdi_platform_time",
        "tdi_opposite_meet", "tdi_same_overtake", "tdi_distance_table", "tdi_stoppage_table",
        "tdi_gap_table", "tdi_time_table", "tdi_average_speed", "tdi_rel_speed",
        "tdi_platform_length", "tdi_two_trains", "tdi_frequency", "tdi_delay_table",
        "tdi_bridge_table", "tdi_ratio_table", "tdi_meet_point", "tdi_cost_per_km",
        "tdi_headway", "tdi_platform_count", "tdi_speed_gap", "tdi_crossing_order",
    ],
    "boats_and_streams_mains": [
        "bm_up_down_time", "bm_stream_speed", "bm_boat_speed", "bm_two_boats",
        "bm_upstream_meet", "bm_round_trip", "bm_delay_start", "bm_current_change",
        "bm_time_difference", "bm_speed_ratio", "bm_relative_drift", "bm_distance_split",
        "bm_current_from_times", "bm_stop_in_stream", "bm_trip_average", "bm_two_legs",
        "bm_half_current", "bm_downstream_first", "bm_upstream_first", "bm_meet_return",
        "bm_ratio_times", "bm_walk_replace", "bm_stream_ratio", "bm_multi_leg",
    ],
    "boats_and_streams_data_interpretation": [
        "bdi_speed_table", "bdi_time_table", "bdi_upstream_time", "bdi_downstream_time",
        "bdi_stream_speed", "bdi_round_trip", "bdi_distance_table", "bdi_ratio_table",
        "bdi_meeting_point", "bdi_average_speed", "bdi_current_effect", "bdi_two_boats",
        "bdi_stop_time", "bdi_leg_distance", "bdi_cost_table", "bdi_frequency",
        "bdi_current_ratio", "bdi_delay_table", "bdi_speed_sum", "bdi_speed_diff",
        "bdi_stream_table", "bdi_trip_table", "bdi_boat_table", "bdi_up_down_table",
    ],
    "probability_mains": [
        "pm_two_cards", "pm_without_replacement", "pm_with_replacement", "pm_dice_sum",
        "pm_dice_condition", "pm_at_least_one", "pm_complement", "pm_conditional",
        "pm_bayes_box", "pm_permutation_word", "pm_combination_group", "pm_committee",
        "pm_independent_events", "pm_mutually_exclusive", "pm_odds_conversion", "pm_expected_value",
        "pm_binomial", "pm_urn_transfer", "pm_card_suit", "pm_divisible_number",
        "pm_ball_sequence", "pm_dice_product", "pm_arrangement", "pm_hypergeometric",
    ],
    "probability_data_interpretation": [
        "pdi_class_table", "pdi_dice_frequency", "pdi_card_draw", "pdi_bag_composition",
        "pdi_defective_batch", "pdi_survey_table", "pdi_at_least_table", "pdi_conditional_table",
        "pdi_complement_table", "pdi_expected_count", "pdi_two_draw_table", "pdi_ratio_prob",
        "pdi_good_bad", "pdi_team_table", "pdi_favourable_count", "pdi_two_bags",
        "pdi_colour_table", "pdi_pass_fail", "pdi_game_table", "pdi_sample_space",
        "pdi_mark_table", "pdi_draw_table", "pdi_selection_table", "pdi_success_table",
    ],
}

ALL_NAMES = [name for names in FAMILY_NAMES.values() for name in names]
