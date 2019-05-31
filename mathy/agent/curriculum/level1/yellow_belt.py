# coding: utf8
import random

from ....game_modes import MODE_SIMPLIFY_POLYNOMIAL
from ...training.lessons import LessonExercise, LessonPlan, build_lesson_plan
from ..problems import (
    get_rand_vars,
    maybe_int,
    maybe_power,
    rand_bool,
    rand_var,
    simplify_multiple_terms,
    combine_terms_after_commuting,
    combine_terms_in_place,
    move_around_blockers_one,
    move_around_blockers_two,
)

observations = 128
yellow_belt = build_lesson_plan(
    "yellow_belt",
    [
        LessonExercise(
            lesson_name="five_terms",
            problem_count=4,
            problem_fn=lambda: simplify_multiple_terms(5, powers_proability=0.85),
            problem_type=MODE_SIMPLIFY_POLYNOMIAL,
            mcts_sims=200,
            num_observations=observations,
        ),
        LessonExercise(
            lesson_name="six_terms",
            problem_count=1,
            problem_fn=lambda: simplify_multiple_terms(6, powers_proability=0.85),
            problem_type=MODE_SIMPLIFY_POLYNOMIAL,
            mcts_sims=200,
            num_observations=observations,
        ),
        LessonExercise(
            lesson_name="seven_terms",
            problem_count=1,
            problem_fn=lambda: simplify_multiple_terms(7, powers_proability=0.85),
            problem_type=MODE_SIMPLIFY_POLYNOMIAL,
            mcts_sims=200,
            num_observations=observations,
        ),
        LessonExercise(
            lesson_name="eight_terms",
            problem_count=1,
            problem_fn=lambda: simplify_multiple_terms(8, powers_proability=0.85),
            problem_type=MODE_SIMPLIFY_POLYNOMIAL,
            mcts_sims=200,
            num_observations=observations,
        ),
        LessonExercise(
            lesson_name="nine_terms",
            problem_count=1,
            problem_fn=lambda: simplify_multiple_terms(9, powers_proability=0.85),
            problem_type=MODE_SIMPLIFY_POLYNOMIAL,
            mcts_sims=200,
            num_observations=observations,
        ),
    ],
)

yellow_belt_practice = build_lesson_plan(
    "yellow_belt_practice",
    [
        LessonExercise(
            lesson_name="five_terms",
            problem_count=4,
            problem_fn=lambda: simplify_multiple_terms(5, powers_proability=0.85),
            problem_type=MODE_SIMPLIFY_POLYNOMIAL,
            mcts_sims=500,
            num_observations=observations,
        ),
        LessonExercise(
            lesson_name="six_terms",
            problem_count=1,
            problem_fn=lambda: simplify_multiple_terms(6, powers_proability=0.85),
            problem_type=MODE_SIMPLIFY_POLYNOMIAL,
            mcts_sims=500,
            num_observations=observations,
        ),
        LessonExercise(
            lesson_name="seven_terms",
            problem_count=1,
            problem_fn=lambda: simplify_multiple_terms(7, powers_proability=0.85),
            problem_type=MODE_SIMPLIFY_POLYNOMIAL,
            mcts_sims=500,
            num_observations=observations,
        ),
        LessonExercise(
            lesson_name="eight_terms",
            problem_count=1,
            problem_fn=lambda: simplify_multiple_terms(8, powers_proability=0.85),
            problem_type=MODE_SIMPLIFY_POLYNOMIAL,
            mcts_sims=500,
            num_observations=observations,
        ),
        LessonExercise(
            lesson_name="nine_terms",
            problem_count=1,
            problem_fn=lambda: simplify_multiple_terms(9, powers_proability=0.85),
            problem_type=MODE_SIMPLIFY_POLYNOMIAL,
            mcts_sims=500,
            num_observations=observations,
        ),
    ],
)
