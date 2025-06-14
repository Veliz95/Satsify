"""
Goal-Oriented 3-SAT Solver Package

This package contains implementations of 3-SAT solvers using:
1. Goal-oriented forced choice heuristic
2. Backward decision-making approach
3. Simplified fixed solver (for testing only)

It also includes shared utilities and predefined test cases.
"""

from .goal_oriented_sat_solver import solve_3sat_goal_oriented
from .backward_3sat_solver import solve_3sat_backward
from .fixed_goal_oriented_solver import solve_3sat_fixed
from .utils import is_clause_satisfied, write_results_to_md
from .test_cases import ALL_TEST_CASES, get_test_case_by_name, run_all_test_cases

__version__ = "1.1.0" 