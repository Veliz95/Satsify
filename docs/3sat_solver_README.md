# Advanced 3-SAT Solver with Goal-Oriented Forced Choice Heuristic

This project implements an advanced 3-SAT solver using a goal-oriented approach with a forced choice heuristic. The solver is designed to efficiently find satisfiable assignments for Boolean formulas in 3-CNF form or prove that no satisfying assignment exists.

## Overview

The 3-SAT problem is a classic NP-complete problem in computer science. Given a Boolean formula in conjunctive normal form (CNF) where each clause has exactly 3 literals, the goal is to determine if there exists an assignment of truth values to the variables that makes the entire formula true.

This solver implements a "Goal-Oriented Forced Choice Heuristic" which:

1. Tries to make intelligent decisions about variable assignments when possible
2. Falls back to traditional backtracking when the heuristic cannot make a clear choice
3. Tracks detailed execution statistics and results for analysis

## Features

- **Goal-Oriented Forced Choice Heuristic**: Makes smart decisions based on clause satisfaction
- **Backtracking Capability**: Falls back to branching when heuristic doesn't yield a clear choice
- **Detailed Execution Tracking**: Records metrics like recursive calls, backtracks, heuristic choices
- **Markdown Output**: Writes detailed execution results to Markdown files for analysis
- **Variable Assignment Types**: Tracks how each variable was assigned (heuristic, branching, or default)

## Implementation Details

The main components of the solver are:

- `solve_3sat_goal_oriented`: Main function that orchestrates the solving process
- `_recursive_solve_with_heuristic`: Core recursive function implementing the solving algorithm
- `_is_clause_satisfied`: Helper function to check if a clause is satisfied
- `_check_for_contradiction`: Helper function to check for contradictions
- `_write_results_to_md`: Function to write results to Markdown files

## Usage

```python
from goal_oriented_sat_solver import solve_3sat_goal_oriented

# Example usage
num_variables = 5
clauses = [
    [1, -2, 3], 
    [-1, 2, -4], 
    [2, 3, 5], 
    [-3, 4, -5]
]
test_case_name = "Example Test"
output_file = "results.md"

solve_3sat_goal_oriented(num_variables, clauses, test_case_name, output_file)
```

## Test Cases

The implementation includes three test cases:

1. **Moderate Satisfiable Example**: A moderately complex example with 6 variables and 10 clauses
2. **Small Unsatisfiable Example**: A small example that is unsatisfiable
3. **Original 5-Var Example**: A simple example with 5 variables and 4 clauses

## Output Format

The solver writes detailed results to Markdown files with the following sections:

- Input Configuration
- Execution Summary
- Solution Assignment (if satisfiable)

## Running the Tests

To run the included test cases:

```
python goal_oriented_sat_solver.py
```

This will execute all three test cases and write the results to separate Markdown files in the project directory. 