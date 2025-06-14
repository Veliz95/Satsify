# Goal-Oriented 3-SAT Solver Project Overview

## Project Motivation

The Boolean Satisfiability Problem (SAT) is one of the most studied NP-complete problems in computer science. This project explores an alternative approach to solving 3-SAT, a restricted version where each clause contains exactly three literals.

Most traditional SAT solvers use a "forward" approach, where variables are assigned values in some order, and the consequences of these assignments are propagated. This project explores a different paradigm:

1. A "backward decision-making" approach that focuses on satisfying specific clauses directly
2. A "goal-oriented forced choice heuristic" that makes intelligent variable assignments

The motivation for this project is experimental exploration for P vs NP problems. While we don't claim to solve the P vs NP problem (3-SAT remains NP-complete), this approach offers an interesting perspective on how different heuristics affect performance on satisfiable vs. unsatisfiable instances.

## Project Components

### Core Solvers

1. **Goal-Oriented Solver** (`sat_solver/goal_oriented_sat_solver.py`):
   - Implements the advanced "forced choice" heuristic
   - Evaluates multiple possible assignments and makes intelligent choices
   - Falls back to systematic backtracking when necessary

2. **Backward Solver** (`sat_solver/backward_3sat_solver.py`):
   - Implements the basic backward decision-making approach
   - Focuses on satisfying one clause at a time
   - Provides a baseline for comparison with the goal-oriented approach

### Documentation

1. **Problem Definition** (`sat_solver/problem_definition.md`):
   - Formal definition of the 3-SAT problem
   - Input and output formats
   - Success criteria

2. **Algorithm Details** (`docs/algorithm_details.md`):
   - In-depth explanation of the goal-oriented and backward approaches
   - Key functions and their purposes
   - Performance characteristics and theoretical considerations

3. **Results Analysis** (`results/summary.md`):
   - Performance metrics across test cases
   - Analysis of solver behavior on satisfiable vs. unsatisfiable instances
   - Observations and future research directions

### Test Cases

The project includes several pre-defined test cases (`sat_solver/test_cases.py`):

1. **Original 5-Variable Example**: A satisfiable instance from the problem definition
2. **Small Unsatisfiable Example**: Specifically constructed to be unsatisfiable
3. **Moderate Satisfiable Example**: A more complex example with 6 variables and 10 clauses
4. **Small Satisfiable Example**: A simple satisfiable formula with 2 variables

## Key Features

### Solver Capabilities

- Determines satisfiability of 3-CNF Boolean formulas
- Provides a satisfying assignment when one exists
- Records detailed performance metrics
- Generates formatted Markdown reports of results

### Algorithm Innovations

- Goal-oriented forced choice heuristic for intelligent variable assignment
- Clause-first approach (backward decision-making)
- Efficient tracking of unsatisfied clauses
- Early contradiction detection

### Technical Implementation

- Pure Python implementation with no external dependencies
- Well-documented, modular code structure
- Dockerized for cross-platform compatibility
- Comprehensive test cases for verification

## Usage Scenarios

This project can be used for:

1. **Educational Purposes**: Understanding SAT algorithms and NP-complete problems
2. **Research Exploration**: Examining alternative approaches to SAT solving
3. **Algorithm Comparison**: Benchmarking against other SAT solving strategies
4. **Problem Solving**: Solving actual 3-SAT instances

## Future Directions

1. **Scalability Testing**: Evaluating performance on larger problem instances
2. **Algorithm Refinements**: Improving the heuristic for unsatisfiable instances
3. **Parallelization**: Exploring multi-threaded approaches for larger problems
4. **Hybrid Approaches**: Combining with other SAT solving techniques