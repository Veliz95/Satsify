"""
Goal-Oriented 3-SAT Solver

This module implements a 3-SAT solver using a goal-oriented forced choice heuristic,
which intelligently reduces the search space for satisfiable instances.

The algorithm:
1. Evaluates both possible assignments (True/False) for each variable
2. Makes "forced choices" based on contradiction avoidance and clause satisfaction impact
3. Falls back to traditional backtracking when the heuristic cannot make a clear decision
"""

import time
import os
from typing import Dict, List, Tuple, Optional, Set
from .utils import is_clause_satisfied, write_results_to_md


def solve_3sat_goal_oriented(
    num_variables: int,
    clauses: List[List[int]],
    test_case_name: str = "Default Test Case",
    output_md_file_path: str = "solver_run_results.md"
) -> None:
    """
    Main function to solve a 3-SAT problem using a goal-oriented forced choice heuristic.
    
    Args:
        num_variables: Total number of distinct Boolean variables (1 to num_variables)
        clauses: List of clauses in 3-CNF form
        test_case_name: Descriptive name for the test run
        output_md_file_path: Path to the Markdown file for output
    """
    # Initialize execution stats
    stats = {
        'recursive_calls': 0,
        'backtracks_on_branch': 0,
        'heuristic_choices_count': 0,
        'branch_choices_count': 0,
        'defaulted_variables': []
    }
    
    # Record start time
    start_time = time.time()
    
    # Initialize unsatisfied clause indices (all clauses at the beginning)
    unsatisfied_clause_indices = list(range(len(clauses)))
    
    # Call the recursive helper function
    solution, assignment_types = _recursive_solve_with_heuristic(
        {}, {}, clauses, unsatisfied_clause_indices, stats, num_variables
    )
    
    # Record end time and calculate time taken
    end_time = time.time()
    time_taken_sec = end_time - start_time
    
    # Process the solution
    if solution is not None:
        status = "SATISFIABLE"
        
        # Ensure all variables are assigned (default unassigned to False)
        for var in range(1, num_variables + 1):
            if var not in solution:
                solution[var] = False
                assignment_types[var] = "Defaulted"
                stats['defaulted_variables'].append(var)
    else:
        status = "UNSATISFIABLE"
        solution = {}
        assignment_types = {}
    
    # Write results to the specified Markdown file
    algorithm_description = (
        "This problem was solved using the **Goal-Oriented Forced Choice Heuristic**, "
        "which makes intelligent variable assignments based on:\n\n"
        "1. Contradiction avoidance\n"
        "2. Maximizing the number of satisfied clauses\n"
        "3. Falling back to systematic backtracking when necessary\n"
    )
    
    write_results_to_md(
        test_case_name,
        num_variables,
        clauses,
        status,
        time_taken_sec,
        stats,
        solution,
        assignment_types,
        output_md_file_path,
        use_unicode=True,
        solver_name="Goal-Oriented 3-SAT Solver",
        algorithm_description=algorithm_description
    )


def _get_unsatisfied_clause_indices(
    clauses: List[List[int]], 
    assignments: Dict[int, bool], 
    current_unsatisfied: List[int]
) -> List[int]:
    """
    Update the list of unsatisfied clause indices based on current assignments.
    
    This optimized version only checks clauses that are currently unsatisfied.
    
    Args:
        clauses: List of all clauses
        assignments: Current variable assignments
        current_unsatisfied: Current list of unsatisfied clause indices
    
    Returns:
        Updated list of unsatisfied clause indices
    """
    # Efficiently filter only clauses that remain unsatisfied
    return [i for i in current_unsatisfied if not is_clause_satisfied(clauses[i], assignments)]


def _is_clause_contradiction(clause: List[int], assignments: Dict[int, bool]) -> bool:
    """
    Check if a clause becomes a contradiction with the given assignments.
    
    Args:
        clause: A list of literals
        assignments: Dictionary mapping variables to boolean values
    
    Returns:
        True if the clause is contradicted (all literals falsified), False otherwise
    """
    # If all literals in the clause are falsified, it's a contradiction
    for literal in clause:
        var = abs(literal)
        if var not in assignments:
            # If any variable is unassigned, no contradiction yet
            return False
        # Check if this literal is satisfied
        if (literal > 0 and assignments[var]) or (literal < 0 and not assignments[var]):
            # If any literal is satisfied, no contradiction
            return False
    # All literals are falsified
    return True


def _check_for_contradiction(clauses: List[List[int]], assignments: Dict[int, bool]) -> bool:
    """
    Check if any clause becomes a contradiction with the current assignments.
    
    Args:
        clauses: List of all clauses
        assignments: Current variable assignments
    
    Returns:
        True if any clause is contradicted, False otherwise
    """
    for clause in clauses:
        if _is_clause_contradiction(clause, assignments):
            return True
    return False


def _evaluate_variable_assignment(
    variable: int,
    value: bool, 
    current_assignments: Dict[int, bool],
    original_clauses: List[List[int]],
    unsatisfied_clause_indices: List[int]
) -> Tuple[bool, int, List[int]]:
    """
    Evaluate the impact of setting a variable to a specific value.
    
    Args:
        variable: The variable to assign
        value: The value to assign to the variable
        current_assignments: Current variable assignments
        original_clauses: List of all clauses
        unsatisfied_clause_indices: Indices of currently unsatisfied clauses
        
    Returns:
        Tuple containing:
        - Whether this assignment causes a contradiction
        - Number of clauses newly satisfied by this assignment
        - List of indices of clauses that remain unsatisfied after this assignment
    """
    # Create potential assignment
    potential_assignment = current_assignments.copy()
    potential_assignment[variable] = value
    
    # Calculate which clauses remain unsatisfied
    remaining_unsatisfied = _get_unsatisfied_clause_indices(
        original_clauses, potential_assignment, unsatisfied_clause_indices
    )
    
    # Calculate how many clauses are satisfied by this assignment
    newly_satisfied_count = len(unsatisfied_clause_indices) - len(remaining_unsatisfied)
    
    # Check for contradictions
    causes_contradiction = _check_for_contradiction(original_clauses, potential_assignment)
    
    return causes_contradiction, newly_satisfied_count, remaining_unsatisfied


def _make_heuristic_decision(
    variable: int,
    true_contradiction: bool,
    false_contradiction: bool,
    true_satisfied_count: int,
    false_satisfied_count: int,
    heuristic_factor: int
) -> Tuple[Optional[int], Optional[bool]]:
    """
    Make a heuristic decision for a variable assignment based on contradiction avoidance 
    and clause satisfaction impact.
    
    Args:
        variable: The variable under consideration
        true_contradiction: Whether setting the variable to True causes a contradiction
        false_contradiction: Whether setting the variable to False causes a contradiction
        true_satisfied_count: Number of clauses satisfied by setting the variable to True
        false_satisfied_count: Number of clauses satisfied by setting the variable to False
        heuristic_factor: Threshold for significant difference in clause satisfaction
        
    Returns:
        Tuple of (variable_to_force, value_to_force) if a decision is made, (None, None) otherwise
    """
    # Case 1: True doesn't cause contradiction but False does
    if not true_contradiction and false_contradiction:
        return variable, True
    
    # Case 2: False doesn't cause contradiction but True does
    if not false_contradiction and true_contradiction:
        return variable, False
    
    # Case 3: One choice satisfies significantly more clauses without contradiction
    if (not true_contradiction and not false_contradiction):
        if true_satisfied_count > false_satisfied_count + heuristic_factor:
            return variable, True
        elif false_satisfied_count > true_satisfied_count + heuristic_factor:
            return variable, False
    
    # No forced choice
    return None, None


def _apply_heuristic_for_variable(
    variable: int,
    current_assignments: Dict[int, bool],
    assignment_types: Dict[int, str],
    original_clauses: List[List[int]],
    unsatisfied_clause_indices: List[int],
    stats: Dict,
    num_variables: int,
    heuristic_factor: int
) -> Tuple[Optional[Dict[int, bool]], Optional[Dict[int, str]]]:
    """
    Apply the heuristic to a specific variable to determine if it should be forced.
    
    Args:
        variable: The variable to evaluate
        current_assignments: Current variable assignments
        assignment_types: Types of assignments (heuristic or branched)
        original_clauses: List of all original clauses
        unsatisfied_clause_indices: Indices of currently unsatisfied clauses
        stats: Statistics dictionary for tracking solver performance
        num_variables: Total number of variables
        heuristic_factor: Threshold for significant difference in clause satisfaction
        
    Returns:
        Tuple of (solution_assignments, assignment_types) if a solution is found through 
        this variable, (None, None) otherwise
    """
    # Skip if variable is already assigned
    if variable in current_assignments:
        return None, None
    
    # Evaluate setting the variable to True
    true_contradiction, true_satisfied_count, remaining_unsatisfied_true = _evaluate_variable_assignment(
        variable, True, current_assignments, original_clauses, unsatisfied_clause_indices
    )
    
    # Evaluate setting the variable to False
    false_contradiction, false_satisfied_count, remaining_unsatisfied_false = _evaluate_variable_assignment(
        variable, False, current_assignments, original_clauses, unsatisfied_clause_indices
    )
    
    # Make a heuristic decision
    variable_to_force, value_to_force = _make_heuristic_decision(
        variable, 
        true_contradiction, 
        false_contradiction, 
        true_satisfied_count, 
        false_satisfied_count,
        heuristic_factor
    )
    
    # If a forced choice was made
    if variable_to_force is not None:
        stats['heuristic_choices_count'] += 1
        
        new_assignments = current_assignments.copy()
        new_assignments[variable_to_force] = value_to_force
        
        new_assignment_types = assignment_types.copy()
        new_assignment_types[variable_to_force] = "Heuristic Set"
        
        # Determine which set of remaining unsatisfied clauses to use
        new_unsatisfied_indices = remaining_unsatisfied_true if value_to_force else remaining_unsatisfied_false
        
        # Recursive call with new state
        result, result_types = _recursive_solve_with_heuristic(
            new_assignments, new_assignment_types, original_clauses, 
            new_unsatisfied_indices, stats, num_variables
        )
        
        # If solution found, propagate it upwards
        return result, result_types
    
    # No forced choice was made for this variable
    return None, None


def _try_branch_on_target_clause(
    target_clause_idx: int,
    original_clauses: List[List[int]],
    current_assignments: Dict[int, bool],
    assignment_types: Dict[int, str],
    unsatisfied_clause_indices: List[int],
    stats: Dict,
    num_variables: int
) -> Tuple[Optional[Dict[int, bool]], Optional[Dict[int, str]]]:
    """
    Try to satisfy a target clause by branching on its variables.
    
    Args:
        target_clause_idx: Index of the target clause to satisfy
        original_clauses: List of all clauses
        current_assignments: Current variable assignments
        assignment_types: Types of assignments
        unsatisfied_clause_indices: Indices of currently unsatisfied clauses
        stats: Statistics dictionary
        num_variables: Total number of variables
        
    Returns:
        Tuple of (solution_assignments, assignment_types) if satisfiable, (None, None) otherwise
    """
    target_clause = original_clauses[target_clause_idx]
    
    # Try to satisfy the target clause by setting one of its literals to True
    for literal in target_clause:
        variable = abs(literal)
        
        # Skip if variable is already assigned
        if variable in current_assignments:
            continue
        
        # Set the variable to make this literal True
        new_assignments = current_assignments.copy()
        new_assignments[variable] = (literal > 0)  # True for positive literal, False for negative
        
        new_assignment_types = assignment_types.copy()
        new_assignment_types[variable] = "Branch Set"
        
        # Update unsatisfied clauses
        new_unsatisfied_indices = _get_unsatisfied_clause_indices(
            original_clauses, new_assignments, unsatisfied_clause_indices
        )
        
        # Check for immediate contradictions
        if _check_for_contradiction(original_clauses, new_assignments):
            stats['backtracks_on_branch'] += 1
            continue
        
        # Recursive call with new state
        result, result_types = _recursive_solve_with_heuristic(
            new_assignments, new_assignment_types, original_clauses, 
            new_unsatisfied_indices, stats, num_variables
        )
        
        # If solution found, propagate it upwards
        if result is not None:
            return result, result_types
    
    # Backtrack (all attempts failed)
    stats['backtracks_on_branch'] += 1
    return None, None


def _recursive_solve_with_heuristic(
    current_assignments: Dict[int, bool],
    assignment_types: Dict[int, str],
    original_clauses: List[List[int]],
    unsatisfied_clause_indices: List[int],
    stats: Dict,
    num_variables: int
) -> Tuple[Optional[Dict[int, bool]], Optional[Dict[int, str]]]:
    """
    Recursive helper function implementing the goal-oriented forced choice heuristic.
    
    Args:
        current_assignments: Current variable assignments
        assignment_types: Types of assignments (heuristic or branched)
        original_clauses: List of all original clauses
        unsatisfied_clause_indices: Indices of currently unsatisfied clauses
        stats: Statistics dictionary for tracking solver performance
        num_variables: Total number of variables
        
    Returns:
        Tuple of (solution_assignments, assignment_types) if satisfiable, (None, None) otherwise
    """
    # Increment recursive calls counter
    stats['recursive_calls'] += 1
    
    # Base case - Success: All clauses are satisfied
    if not unsatisfied_clause_indices:
        return current_assignments, assignment_types
    
    # Heuristic factor determines how much better one assignment must be to force a choice
    # Higher values make the heuristic more conservative, requiring larger differences
    # in satisfaction to force a variable assignment
    heuristic_factor = 1
    
    # Heuristic Forced Choice Step
    for variable in range(1, num_variables + 1):
        result, result_types = _apply_heuristic_for_variable(
            variable, 
            current_assignments, 
            assignment_types, 
            original_clauses, 
            unsatisfied_clause_indices, 
            stats,
            num_variables,
            heuristic_factor
        )
        
        if result is not None:
            return result, result_types
    
    # Branching Step (if no forced choice found by heuristic)
    stats['branch_choices_count'] += 1
    
    # Select a target clause (first unsatisfied clause)
    if not unsatisfied_clause_indices:
        # This should not happen, but just in case
        return current_assignments, assignment_types
    
    target_clause_idx = unsatisfied_clause_indices[0]
    
    return _try_branch_on_target_clause(
        target_clause_idx,
        original_clauses,
        current_assignments,
        assignment_types,
        unsatisfied_clause_indices,
        stats,
        num_variables
    )


if __name__ == "__main__":
    # Test Case 1 (from problem_definition.md)
    tc1_vars = 5
    tc1_clauses = [
        [1, -2, 3], [-1, 2, -4], [2, 3, 5], [-3, 4, -5]
    ]
    
    # Create results directory if it doesn't exist
    os.makedirs("results", exist_ok=True)
    
    # Run solver on test case 1
    solve_3sat_goal_oriented(
        tc1_vars, 
        tc1_clauses, 
        "Original 5-Var Example",
        "results/results_tc1.md"
    )
    
    # Test Case 2 (Small Unsatisfiable)
    tc2_vars = 3
    tc2_clauses = [
        [1, 2, 3], [1, 2, -3], [1, -2, 3], [1, -2, -3],
        [-1, 2, 3], [-1, 2, -3], [-1, -2, 3], [-1, -2, -3]
    ]
    
    # Run solver on test case 2
    solve_3sat_goal_oriented(
        tc2_vars, 
        tc2_clauses, 
        "Small Unsatisfiable Example",
        "results/results_tc2.md"
    )
    
    # Test Case 3 (Medium Satisfiable)
    tc3_vars = 6
    tc3_clauses = [
        [1, 2, -3], [-1, -2, 4], [3, -4, 5], 
        [-3, 4, 6], [-5, -6, 1], [5, 6, -2],
        [1, 3, 5], [-2, -4, -6], [2, 4, 6], [3, -5, 6]
    ]
    
    # Run solver on test case 3
    solve_3sat_goal_oriented(
        tc3_vars, 
        tc3_clauses, 
        "Moderate Satisfiable Example",
        "results/results_tc3.md"
    )
    
    print("All test cases completed. Results saved to the 'results/' directory.") 