# Banking Maths Set 4 - Database Reconciliation

- Snapshot before: `2026-11-27T17:54:51.982051+00:00`
- Snapshot after: `2026-11-27T18:02:22.591444+00:00`

## Table count changes

| Table | Before | After | Delta |
| --- | ---: | ---: | ---: |
| question_options | 66813 | 72573 | +5760 |
| questions | 15172 | 16612 | +1440 |
| alembic_version | 1 | 1 | 0 |
| beta_capacity | 1 | 1 | 0 |
| beta_invitations | 0 | 0 | 0 |
| chapters | 598 | 598 | 0 |
| exams | 7 | 7 | 0 |
| rate_limit_windows | 9 | 9 | 0 |
| subcategories | 9 | 9 | 0 |
| subjects | 22 | 22 | 0 |
| test_attempts | 61 | 61 | 0 |
| test_questions | 2667 | 2667 | 0 |
| user_answers | 272 | 272 | 0 |
| user_chapter_rotations | 4 | 4 | 0 |
| user_question_history | 92 | 92 | 0 |
| users | 3 | 3 | 0 |

Only `question_options`, `questions` changed.

## Questions by exam and subject

| Exam / subject | Before | After | Delta |
| --- | ---: | ---: | ---: |
| banking-clerk/computer | 527 | 527 | +0 |
| banking-clerk/current-affairs | 500 | 500 | +0 |
| banking-clerk/english | 1120 | 1120 | +0 |
| banking-clerk/general-banking-awareness | 384 | 384 | +0 |
| banking-clerk/math-quant | 1920 | 2640 | +720 |
| banking-clerk/reasoning | 1546 | 1546 | +0 |
| banking-po/computer | 527 | 527 | +0 |
| banking-po/current-affairs | 503 | 503 | +0 |
| banking-po/english | 1120 | 1120 | +0 |
| banking-po/general-banking-awareness | 482 | 482 | +0 |
| banking-po/math-quant | 1920 | 2640 | +720 |
| ssc/gk-gs | 1107 | 1107 | +0 |
| ssc/maths | 2794 | 2794 | +0 |
| ssc/reasoning | 722 | 722 | +0 |

## Target chapters

| Exam / chapter | Before | After | Delta |
| --- | ---: | ---: | ---: |
| banking-clerk/average | 0 | 120 | +120 |
| banking-clerk/boats_and_streams | 0 | 120 | +120 |
| banking-clerk/mensuration_2d | 0 | 120 | +120 |
| banking-clerk/pipe_and_cistern | 0 | 120 | +120 |
| banking-clerk/problems_on_trains | 0 | 120 | +120 |
| banking-clerk/speed_time_distance | 0 | 120 | +120 |
| banking-po/average | 0 | 120 | +120 |
| banking-po/boats_and_streams | 0 | 120 | +120 |
| banking-po/mensuration_2d | 0 | 120 | +120 |
| banking-po/pipe_and_cistern | 0 | 120 | +120 |
| banking-po/problems_on_trains | 0 | 120 | +120 |
| banking-po/speed_time_distance | 0 | 120 | +120 |

## Maths section counts

| Section | Before | After | Expected after |
| --- | ---: | ---: | ---: |
| banking_clerk_maths_approximation_part_1 | 15 | 15 | 15 |
| banking_clerk_maths_approximation_part_2 | 20 | 20 | 20 |
| banking_clerk_maths_approximation_part_3 | 30 | 30 | 30 |
| banking_clerk_maths_approximation_part_4 | 55 | 55 | 55 |
| banking_clerk_maths_average_part_1 | 0 | 15 | 15 |
| banking_clerk_maths_average_part_2 | 0 | 20 | 20 |
| banking_clerk_maths_average_part_3 | 0 | 30 | 30 |
| banking_clerk_maths_average_part_4 | 0 | 55 | 55 |
| banking_clerk_maths_boats_and_streams_part_1 | 0 | 15 | 15 |
| banking_clerk_maths_boats_and_streams_part_2 | 0 | 20 | 20 |
| banking_clerk_maths_boats_and_streams_part_3 | 0 | 30 | 30 |
| banking_clerk_maths_boats_and_streams_part_4 | 0 | 55 | 55 |
| banking_clerk_maths_compound_interest_part_1 | 15 | 15 | 15 |
| banking_clerk_maths_compound_interest_part_2 | 20 | 20 | 20 |
| banking_clerk_maths_compound_interest_part_3 | 30 | 30 | 30 |
| banking_clerk_maths_compound_interest_part_4 | 55 | 55 | 55 |
| banking_clerk_maths_mensuration_2d_part_1 | 0 | 15 | 15 |
| banking_clerk_maths_mensuration_2d_part_2 | 0 | 20 | 20 |
| banking_clerk_maths_mensuration_2d_part_3 | 0 | 30 | 30 |
| banking_clerk_maths_mensuration_2d_part_4 | 0 | 55 | 55 |
| banking_clerk_maths_missing_series_part_1 | 15 | 15 | 15 |
| banking_clerk_maths_missing_series_part_2 | 20 | 20 | 20 |
| banking_clerk_maths_missing_series_part_3 | 30 | 30 | 30 |
| banking_clerk_maths_missing_series_part_4 | 55 | 55 | 55 |
| banking_clerk_maths_mixture_alligation_part_1 | 15 | 15 | 15 |
| banking_clerk_maths_mixture_alligation_part_2 | 20 | 20 | 20 |
| banking_clerk_maths_mixture_alligation_part_3 | 30 | 30 | 30 |
| banking_clerk_maths_mixture_alligation_part_4 | 55 | 55 | 55 |
| banking_clerk_maths_number_system_part_1 | 15 | 15 | 15 |
| banking_clerk_maths_number_system_part_2 | 20 | 20 | 20 |
| banking_clerk_maths_number_system_part_3 | 30 | 30 | 30 |
| banking_clerk_maths_number_system_part_4 | 55 | 55 | 55 |
| banking_clerk_maths_partnership_part_1 | 15 | 15 | 15 |
| banking_clerk_maths_partnership_part_2 | 20 | 20 | 20 |
| banking_clerk_maths_partnership_part_3 | 30 | 30 | 30 |
| banking_clerk_maths_partnership_part_4 | 55 | 55 | 55 |
| banking_clerk_maths_percentage_part_1 | 15 | 15 | 15 |
| banking_clerk_maths_percentage_part_2 | 20 | 20 | 20 |
| banking_clerk_maths_percentage_part_3 | 30 | 30 | 30 |
| banking_clerk_maths_percentage_part_4 | 55 | 55 | 55 |
| banking_clerk_maths_pipe_and_cistern_part_1 | 0 | 15 | 15 |
| banking_clerk_maths_pipe_and_cistern_part_2 | 0 | 20 | 20 |
| banking_clerk_maths_pipe_and_cistern_part_3 | 0 | 30 | 30 |
| banking_clerk_maths_pipe_and_cistern_part_4 | 0 | 55 | 55 |
| banking_clerk_maths_problems_on_age_part_1 | 15 | 15 | 15 |
| banking_clerk_maths_problems_on_age_part_2 | 20 | 20 | 20 |
| banking_clerk_maths_problems_on_age_part_3 | 30 | 30 | 30 |
| banking_clerk_maths_problems_on_age_part_4 | 55 | 55 | 55 |
| banking_clerk_maths_problems_on_trains_part_1 | 0 | 15 | 15 |
| banking_clerk_maths_problems_on_trains_part_2 | 0 | 20 | 20 |
| banking_clerk_maths_problems_on_trains_part_3 | 0 | 30 | 30 |
| banking_clerk_maths_problems_on_trains_part_4 | 0 | 55 | 55 |
| banking_clerk_maths_profit_loss_discount_part_1 | 15 | 15 | 15 |
| banking_clerk_maths_profit_loss_discount_part_2 | 20 | 20 | 20 |
| banking_clerk_maths_profit_loss_discount_part_3 | 30 | 30 | 30 |
| banking_clerk_maths_profit_loss_discount_part_4 | 55 | 55 | 55 |
| banking_clerk_maths_quadratic_equations_part_1 | 15 | 15 | 15 |
| banking_clerk_maths_quadratic_equations_part_2 | 20 | 20 | 20 |
| banking_clerk_maths_quadratic_equations_part_3 | 30 | 30 | 30 |
| banking_clerk_maths_quadratic_equations_part_4 | 55 | 55 | 55 |
| banking_clerk_maths_ratio_proportion_part_1 | 15 | 15 | 15 |
| banking_clerk_maths_ratio_proportion_part_2 | 20 | 20 | 20 |
| banking_clerk_maths_ratio_proportion_part_3 | 30 | 30 | 30 |
| banking_clerk_maths_ratio_proportion_part_4 | 55 | 55 | 55 |
| banking_clerk_maths_simple_interest_part_1 | 15 | 15 | 15 |
| banking_clerk_maths_simple_interest_part_2 | 20 | 20 | 20 |
| banking_clerk_maths_simple_interest_part_3 | 30 | 30 | 30 |
| banking_clerk_maths_simple_interest_part_4 | 55 | 55 | 55 |
| banking_clerk_maths_simplification_part_1 | 15 | 15 | 15 |
| banking_clerk_maths_simplification_part_2 | 20 | 20 | 20 |
| banking_clerk_maths_simplification_part_3 | 30 | 30 | 30 |
| banking_clerk_maths_simplification_part_4 | 55 | 55 | 55 |
| banking_clerk_maths_speed_time_distance_part_1 | 0 | 15 | 15 |
| banking_clerk_maths_speed_time_distance_part_2 | 0 | 20 | 20 |
| banking_clerk_maths_speed_time_distance_part_3 | 0 | 30 | 30 |
| banking_clerk_maths_speed_time_distance_part_4 | 0 | 55 | 55 |
| banking_clerk_maths_time_and_work_part_1 | 15 | 15 | 15 |
| banking_clerk_maths_time_and_work_part_2 | 20 | 20 | 20 |
| banking_clerk_maths_time_and_work_part_3 | 30 | 30 | 30 |
| banking_clerk_maths_time_and_work_part_4 | 55 | 55 | 55 |
| banking_clerk_maths_vedic_maths_part_1 | 15 | 15 | 15 |
| banking_clerk_maths_vedic_maths_part_2 | 20 | 20 | 20 |
| banking_clerk_maths_vedic_maths_part_3 | 30 | 30 | 30 |
| banking_clerk_maths_vedic_maths_part_4 | 55 | 55 | 55 |
| banking_clerk_maths_wrong_series_part_1 | 15 | 15 | 15 |
| banking_clerk_maths_wrong_series_part_2 | 20 | 20 | 20 |
| banking_clerk_maths_wrong_series_part_3 | 30 | 30 | 30 |
| banking_clerk_maths_wrong_series_part_4 | 55 | 55 | 55 |
| banking_po_maths_approximation_part_1 | 15 | 15 | 15 |
| banking_po_maths_approximation_part_2 | 20 | 20 | 20 |
| banking_po_maths_approximation_part_3 | 30 | 30 | 30 |
| banking_po_maths_approximation_part_4 | 55 | 55 | 55 |
| banking_po_maths_average_part_1 | 0 | 15 | 15 |
| banking_po_maths_average_part_2 | 0 | 20 | 20 |
| banking_po_maths_average_part_3 | 0 | 30 | 30 |
| banking_po_maths_average_part_4 | 0 | 55 | 55 |
| banking_po_maths_boats_and_streams_part_1 | 0 | 15 | 15 |
| banking_po_maths_boats_and_streams_part_2 | 0 | 20 | 20 |
| banking_po_maths_boats_and_streams_part_3 | 0 | 30 | 30 |
| banking_po_maths_boats_and_streams_part_4 | 0 | 55 | 55 |
| banking_po_maths_compound_interest_part_1 | 15 | 15 | 15 |
| banking_po_maths_compound_interest_part_2 | 20 | 20 | 20 |
| banking_po_maths_compound_interest_part_3 | 30 | 30 | 30 |
| banking_po_maths_compound_interest_part_4 | 55 | 55 | 55 |
| banking_po_maths_mensuration_2d_part_1 | 0 | 15 | 15 |
| banking_po_maths_mensuration_2d_part_2 | 0 | 20 | 20 |
| banking_po_maths_mensuration_2d_part_3 | 0 | 30 | 30 |
| banking_po_maths_mensuration_2d_part_4 | 0 | 55 | 55 |
| banking_po_maths_missing_series_part_1 | 15 | 15 | 15 |
| banking_po_maths_missing_series_part_2 | 20 | 20 | 20 |
| banking_po_maths_missing_series_part_3 | 30 | 30 | 30 |
| banking_po_maths_missing_series_part_4 | 55 | 55 | 55 |
| banking_po_maths_mixture_alligation_part_1 | 15 | 15 | 15 |
| banking_po_maths_mixture_alligation_part_2 | 20 | 20 | 20 |
| banking_po_maths_mixture_alligation_part_3 | 30 | 30 | 30 |
| banking_po_maths_mixture_alligation_part_4 | 55 | 55 | 55 |
| banking_po_maths_number_system_part_1 | 15 | 15 | 15 |
| banking_po_maths_number_system_part_2 | 20 | 20 | 20 |
| banking_po_maths_number_system_part_3 | 30 | 30 | 30 |
| banking_po_maths_number_system_part_4 | 55 | 55 | 55 |
| banking_po_maths_partnership_part_1 | 15 | 15 | 15 |
| banking_po_maths_partnership_part_2 | 20 | 20 | 20 |
| banking_po_maths_partnership_part_3 | 30 | 30 | 30 |
| banking_po_maths_partnership_part_4 | 55 | 55 | 55 |
| banking_po_maths_percentage_part_1 | 15 | 15 | 15 |
| banking_po_maths_percentage_part_2 | 20 | 20 | 20 |
| banking_po_maths_percentage_part_3 | 30 | 30 | 30 |
| banking_po_maths_percentage_part_4 | 55 | 55 | 55 |
| banking_po_maths_pipe_and_cistern_part_1 | 0 | 15 | 15 |
| banking_po_maths_pipe_and_cistern_part_2 | 0 | 20 | 20 |
| banking_po_maths_pipe_and_cistern_part_3 | 0 | 30 | 30 |
| banking_po_maths_pipe_and_cistern_part_4 | 0 | 55 | 55 |
| banking_po_maths_problems_on_age_part_1 | 15 | 15 | 15 |
| banking_po_maths_problems_on_age_part_2 | 20 | 20 | 20 |
| banking_po_maths_problems_on_age_part_3 | 30 | 30 | 30 |
| banking_po_maths_problems_on_age_part_4 | 55 | 55 | 55 |
| banking_po_maths_problems_on_trains_part_1 | 0 | 15 | 15 |
| banking_po_maths_problems_on_trains_part_2 | 0 | 20 | 20 |
| banking_po_maths_problems_on_trains_part_3 | 0 | 30 | 30 |
| banking_po_maths_problems_on_trains_part_4 | 0 | 55 | 55 |
| banking_po_maths_profit_loss_discount_part_1 | 15 | 15 | 15 |
| banking_po_maths_profit_loss_discount_part_2 | 20 | 20 | 20 |
| banking_po_maths_profit_loss_discount_part_3 | 30 | 30 | 30 |
| banking_po_maths_profit_loss_discount_part_4 | 55 | 55 | 55 |
| banking_po_maths_quadratic_equations_part_1 | 15 | 15 | 15 |
| banking_po_maths_quadratic_equations_part_2 | 20 | 20 | 20 |
| banking_po_maths_quadratic_equations_part_3 | 30 | 30 | 30 |
| banking_po_maths_quadratic_equations_part_4 | 55 | 55 | 55 |
| banking_po_maths_ratio_proportion_part_1 | 15 | 15 | 15 |
| banking_po_maths_ratio_proportion_part_2 | 20 | 20 | 20 |
| banking_po_maths_ratio_proportion_part_3 | 30 | 30 | 30 |
| banking_po_maths_ratio_proportion_part_4 | 55 | 55 | 55 |
| banking_po_maths_simple_interest_part_1 | 15 | 15 | 15 |
| banking_po_maths_simple_interest_part_2 | 20 | 20 | 20 |
| banking_po_maths_simple_interest_part_3 | 30 | 30 | 30 |
| banking_po_maths_simple_interest_part_4 | 55 | 55 | 55 |
| banking_po_maths_simplification_part_1 | 15 | 15 | 15 |
| banking_po_maths_simplification_part_2 | 20 | 20 | 20 |
| banking_po_maths_simplification_part_3 | 30 | 30 | 30 |
| banking_po_maths_simplification_part_4 | 55 | 55 | 55 |
| banking_po_maths_speed_time_distance_part_1 | 0 | 15 | 15 |
| banking_po_maths_speed_time_distance_part_2 | 0 | 20 | 20 |
| banking_po_maths_speed_time_distance_part_3 | 0 | 30 | 30 |
| banking_po_maths_speed_time_distance_part_4 | 0 | 55 | 55 |
| banking_po_maths_time_and_work_part_1 | 15 | 15 | 15 |
| banking_po_maths_time_and_work_part_2 | 20 | 20 | 20 |
| banking_po_maths_time_and_work_part_3 | 30 | 30 | 30 |
| banking_po_maths_time_and_work_part_4 | 55 | 55 | 55 |
| banking_po_maths_vedic_maths_part_1 | 15 | 15 | 15 |
| banking_po_maths_vedic_maths_part_2 | 20 | 20 | 20 |
| banking_po_maths_vedic_maths_part_3 | 30 | 30 | 30 |
| banking_po_maths_vedic_maths_part_4 | 55 | 55 | 55 |
| banking_po_maths_wrong_series_part_1 | 15 | 15 | 15 |
| banking_po_maths_wrong_series_part_2 | 20 | 20 | 20 |
| banking_po_maths_wrong_series_part_3 | 30 | 30 | 30 |
| banking_po_maths_wrong_series_part_4 | 55 | 55 | 55 |

## Target checks

- Set 4 section questions: 0 -> 1440 (+1440)
- Prior batch section questions: 3840 -> 3840 (unchanged)
- Banking Others maths questions: 0 -> 0 (unchanged)
- Maths sections: 128 -> 176 (+48)

## Result

The import added exactly 1,440 questions and 5,760 options across 48 new sections.
No attempts, answers, users, chapters, subjects, exams or other unrelated rows changed.
