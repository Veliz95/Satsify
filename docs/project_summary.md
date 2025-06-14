# Advanced 3-SAT Solver Project Summary

## Project Overview

This project implements an advanced 3-SAT solver using a goal-oriented approach with a forced choice heuristic. The 3-SAT problem is a classic NP-complete problem in computer science, and this implementation explores a novel approach to finding satisfying assignments for Boolean formulas in 3-CNF form.

The main motivation is experimental exploration of algorithms for tackling P vs NP problems through a backward decision-making perspective.

## Project Structure

```
3sat_solver/
├── goal_oriented_sat_solver.py  # Main implementation of the 3-SAT solver
├── project_summary.md           # This file (overview of project implementation)
└── results/                     # Directory containing test results
    ├── results_tc1.md           # Results for Moderate Satisfiable Example
    ├── results_tc2.md           # Results for Small Unsatisfiable Example
    ├── results_tc3.md           # Results for Original 5-Var Example
    └── summary.md               # Analysis of test results and performance metrics
```

## Implementation Details

### Core Algorithm Components

1. **Goal-Oriented Forced Choice Heuristic**:
   - Evaluates both possible assignments (True/False) for each variable
   - Makes "forced choices" based on contradiction avoidance and clause satisfaction impact
   - Intelligently reduces the search space for satisfiable instances

2. **Backtracking Strategy**:
   - Falls back to traditional backtracking when the heuristic cannot make a clear decision
   - Systematically explores the search space to find satisfying assignments or prove unsatisfiability

3. **Execution Tracking**:
   - Records comprehensive metrics including recursive calls, backtracks, and heuristic choices
   - Categorizes variable assignments by source (heuristic, branching, or default)

### Key Functions

- `solve_3sat_goal_oriented`: Main entry point that handles initialization and result reporting
- `_recursive_solve_with_heuristic`: Core recursive algorithm implementing the heuristic approach
- `_get_unsatisfied_clause_indices`: Efficiently tracks unsatisfied clauses during search
- `_is_clause_contradiction`: Detects contradictions that would invalidate the solution
- `_write_results_to_md`: Formats and outputs detailed execution results

## Usage

The solver can be used in two ways:

### 1. Standalone Script

```bash
python goal_oriented_sat_solver.py
```

This executes the solver on predefined test cases and writes results to Markdown files in the `results/` directory.

### 2. Library Import

```python
from goal_oriented_sat_solver import solve_3sat_goal_oriented

# Define your 3-SAT problem
num_variables = 5
clauses = [
    [1, -2, 3],   # Each integer represents a literal
    [-1, 2, -4],  # Positive for variable, negative for negated variable
    [2, 3, 5],
    [-3, 4, -5]
]
test_case_name = "My Test Case"
output_file = "my_results.md"

# Solve the problem
solve_3sat_goal_oriented(num_variables, clauses, test_case_name, output_file)
```

## Performance Analysis

Initial testing on small to moderate problem instances shows:

- Efficient performance on satisfiable instances with minimal backtracking
- Correct identification of unsatisfiable instances, though with more extensive search
- Execution times under 0.002 seconds for test cases with up to 6 variables and 10 clauses

The detailed performance metrics can be found in `results/summary.md`.

## Future Development Opportunities

1. **Algorithm Enhancements**:
   - Improved heuristics for unsatisfiable instances
   - Dynamic variable ordering strategies

2. **Scalability Testing**:
   - Evaluation on larger problem instances
   - Benchmarking against established 3-SAT solvers

3. **Implementation Optimizations**:
   - Memory usage improvements
   - Potential parallelization of search space exploration 