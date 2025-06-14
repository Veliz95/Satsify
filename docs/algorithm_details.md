# Goal-Oriented 3-SAT Solver Algorithm Details

This document provides a detailed explanation of the "Goal-Oriented Forced Choice Heuristic" and "Backward Decision-Making" approaches implemented in this project.

## Core Algorithm Concepts

### 1. Backward Decision-Making Approach

Traditional SAT solvers typically use a "forward" approach, assigning variables in a predefined order and then checking if clauses are satisfied. Our approach inverts this paradigm:

1. **Clause-First Focus**: The algorithm targets unsatisfied clauses directly
2. **Variable Assignment for Clause Satisfaction**: Variables are assigned specifically to satisfy target clauses
3. **Incremental Clause Satisfaction**: The algorithm works to satisfy one clause at a time

This backward approach is particularly intuitive as it mimics how humans might tackle a satisfiability problem: identify what needs to be satisfied and then make assignments to achieve that goal.

### 2. Goal-Oriented Forced Choice Heuristic

The enhanced version of the solver implements a sophisticated heuristic that guides variable selection:

1. **Dual Assignment Evaluation**: For each unassigned variable, both True and False assignments are evaluated
2. **Contradiction Detection**: Assignments that lead to immediate contradictions are avoided
3. **Satisfaction Impact Measurement**: The number of clauses that would be satisfied by each assignment is calculated
4. **Forced Choice Criteria**:
   - If one assignment causes a contradiction but the other doesn't, choose the non-contradicting assignment
   - If one assignment satisfies significantly more clauses than the other, choose that assignment
5. **Heuristic Threshold**: A configurable "heuristic_factor" determines what constitutes a "significant" difference

When the heuristic cannot make a forced choice, the algorithm falls back to a systematic backtracking approach.

## Algorithm Workflow

### Initialization
1. Begin with empty variable assignments
2. All clauses are initially unsatisfied

### Main Recursive Function
1. **Base Case**: If all clauses are satisfied, return the current assignment
2. **Heuristic Step**:
   - For each unassigned variable:
     - Try assigning True and False
     - Calculate how many clauses each assignment would satisfy
     - Check if either assignment leads to contradictions
     - Make a "forced choice" if criteria are met
3. **Branching Step** (if heuristic makes no choice):
   - Select an unsatisfied clause
   - Try assigning variables to satisfy it
   - If a contradiction is found, backtrack
4. **Backtracking**:
   - If all attempts for a branch fail, revert and try alternatives

### Completion
1. Ensure all variables have assignments (default to False for unassigned variables)
2. Return the complete solution or indicate unsatisfiability

## Implementation Details

### Key Functions

1. **`_recursive_solve_with_heuristic`**: The core recursive algorithm
   - Implements the heuristic decision logic
   - Handles branching and backtracking
   - Tracks statistics on solver performance

2. **`_is_clause_satisfied`**: Determines if a clause is satisfied given current assignments
   - A clause is satisfied if at least one of its literals evaluates to True

3. **`_check_for_contradiction`**: Detects if any clause becomes a contradiction
   - A contradiction occurs when all literals in a clause are falsified

4. **`_get_unsatisfied_clause_indices`**: Efficiently tracks which clauses remain unsatisfied

### Optimization Techniques

1. **Efficient Tracking of Unsatisfied Clauses**:
   - Only update clauses that might be affected by new assignments
   - Avoid rechecking already satisfied clauses

2. **Early Contradiction Detection**:
   - Detect and avoid assignments that lead to contradictions before deeper recursion
   - Significant pruning of the search space

3. **Heuristic-Guided Search**:
   - Prioritize variables and assignments that maximize clause satisfaction
   - Reduce the need for extensive backtracking

## Performance Characteristics

### Satisfiable Instances
- The heuristic often makes effective early choices
- Minimal backtracking is typically required
- Solution is found in fewer recursive calls

### Unsatisfiable Instances
- More extensive search is required
- Complete backtracking is necessary to prove unsatisfiability
- The heuristic may be less effective at reducing the search space

## Theoretical Considerations

While this approach shows promising results on the test cases, it's important to note that 3-SAT remains NP-complete. This implementation is an experimental exploration for the P vs NP problem, not a polynomial-time solution. In the worst case, the algorithm may still require exponential time to determine unsatisfiability for certain problem instances. 