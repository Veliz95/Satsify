"""
Backward 3-SAT Solver

This module implements a 3-SAT solver using a backward decision-making approach
that focuses on satisfying individual clauses first rather than assigning
variables in a predefined order.

The algorithm:
1. Selects an unsatisfied clause as the target
2. Attempts to satisfy it by assigning values to its variables
3. Backtracks when inconsistencies are found or when a branch doesn't lead to a solution
4. Continues this process until either a solution is found or all possibilities are exhausted
"""

import time
import os
from typing import Dict, List, Tuple, Set, Optional, Union
from .utils import is_clause_satisfied, write_results_to_md


def _find_solution_recursive(
    current_assignments: Dict[int, bool],
    original_clauses: List[List[int]],
    unsatisfied_clause_indices: List[int],
    stats: Dict
) -> Optional[Dict[int, bool]]:
    """
    Recursive helper function that attempts to find a satisfying assignment.
    
    This function implements a backward decision-making approach by:
    1. Selecting an unsatisfied clause
    2. Trying to satisfy it by assigning values to its variables
    3. Recursively continuing with the updated assignment
    4. Backtracking if the current branch doesn't lead to a solution
    
    The backtracking mechanism works as follows:
    - If we try all possible assignments for a clause's variables and none lead to a solution,
      we backtrack to the previous decision point
    - This allows the algorithm to systematically explore the search space until either
      a solution is found or all possibilities are exhausted
    
    Args:
        current_assignments: Current variable assignments
        original_clauses: List of all clauses in the formula
        unsatisfied_clause_indices: Indices of clauses that are not yet satisfied
        stats: Dictionary to track execution statistics
        
    Returns:
        Dictionary of variable assignments if satisfiable, None otherwise
    """
    # Increment recursive call counter
    stats['recursive_calls'] += 1
    
    # Base Case - Success: All clauses are satisfied
    if not unsatisfied_clause_indices:
        return current_assignments
    
    # Select target unsatisfied clause (first one in the list)
    target_clause_index = unsatisfied_clause_indices[0]
    target_clause = original_clauses[target_clause_index]
    
    # Attempt to satisfy the target clause by trying each literal
    for literal in target_clause:
        variable_to_assign = abs(literal)
        value_to_assign = (literal > 0)
        
        # Consistency Check
        if variable_to_assign in current_assignments:
            # If there's a conflict with existing assignment, try next literal
            if current_assignments[variable_to_assign] != value_to_assign:
                continue
            # If already assigned consistently, this literal alone isn't enough to satisfy
            # (since the clause is in unsatisfied_clause_indices)
            else:
                continue
        
        # Make Assignment & Recurse
        new_assignments = current_assignments.copy()
        new_assignments[variable_to_assign] = value_to_assign
        
        # Update unsatisfied clauses list
        new_unsatisfied_indices = []
        for idx in unsatisfied_clause_indices:
            if not is_clause_satisfied(original_clauses[idx], new_assignments):
                new_unsatisfied_indices.append(idx)
        
        # Recursive call with new state
        result = _find_solution_recursive(
            new_assignments, 
            original_clauses, 
            new_unsatisfied_indices,
            stats
        )
        
        # If solution found, propagate it upwards
        if result is not None:
            # Record that this was a branch choice
            stats['branch_choices_count'] += 1
            return result
    
    # Backtrack (all literals tried, none led to solution)
    stats['backtracks'] += 1
    return None


def solve_3sat_backward(
    num_variables: int, 
    clauses: List[List[int]], 
    test_case_name: str = "Test Case",
    output_md_file_path: Optional[str] = None
) -> Tuple[Optional[Dict[int, bool]], Dict]:
    """
    Solves the 3-SAT problem using a backward decision-making approach.
    
    This backward approach differs from traditional 3-SAT solvers by:
    1. Focusing on unsatisfied clauses first rather than variables
    2. Making assignments based on what would satisfy specific clauses
    3. Backtracking when inconsistencies are found or when a branch doesn't lead to a solution
    
    Args:
        num_variables: Total number of distinct Boolean variables in the formula
        clauses: List of clauses, where each clause is a list of integers representing literals
                 (positive for variables, negative for negated variables)
        test_case_name: Name for the test case (used in statistics)
        output_md_file_path: Optional path to write results in Markdown format
        
    Returns:
        Tuple containing:
            - solution_assignment: Dictionary mapping variables to boolean values, or None if unsatisfiable
            - execution_stats: Dictionary containing execution statistics (calls, time, status)
    """
    # Initialize execution statistics
    execution_stats = {
        'test_case_name': test_case_name,
        'num_variables': num_variables,
        'num_clauses': len(clauses),
        'recursive_calls': 0,
        'backtracks': 0,
        'branch_choices_count': 0,  # Added to match goal-oriented solver
        'defaulted_variables': []
    }
    
    # Record start time
    start_time = time.time()
    
    # Initial state: all clauses are unsatisfied
    unsatisfied_clause_indices = list(range(len(clauses)))
    
    # Call recursive helper function
    solution = _find_solution_recursive(
        current_assignments={}, 
        original_clauses=clauses,
        unsatisfied_clause_indices=unsatisfied_clause_indices,
        stats=execution_stats
    )
    
    # Record end time and calculate duration
    end_time = time.time()
    execution_stats['time_taken_sec'] = end_time - start_time
    
    # Process solution for output
    if solution is not None:
        execution_stats['status'] = "SATISFIABLE"
        
        # Ensure all variables have assignments (default = False for unassigned)
        complete_solution = {}
        assignment_types = {}  # Track assignment types
        for var in range(1, num_variables + 1):
            if var in solution:
                complete_solution[var] = solution[var]
                assignment_types[var] = "Branch Set"
            else:
                complete_solution[var] = False  # Default value
                assignment_types[var] = "Defaulted"
                execution_stats['defaulted_variables'].append(var)
        
        # Store solution in stats
        execution_stats['solution'] = complete_solution
        
        # Write results to markdown if path provided
        if output_md_file_path:
            algorithm_description = (
                "This problem was solved using the **Backward Decision-Making Approach**, "
                "which focuses on satisfying individual clauses by:\n\n"
                "1. Selecting an unsatisfied clause as the target\n"
                "2. Assigning values to its variables to make it satisfied\n"
                "3. Backtracking when inconsistencies are found or when a branch doesn't lead to a solution\n"
            )
            
            write_results_to_md(
                test_case_name,
                num_variables,
                clauses,
                "SATISFIABLE",
                execution_stats['time_taken_sec'],
                execution_stats,
                complete_solution,
                assignment_types,
                output_md_file_path,
                use_unicode=True,
                solver_name="Backward 3-SAT Solver",
                algorithm_description=algorithm_description
            )
            
        return complete_solution, execution_stats
    else:
        execution_stats['status'] = "UNSATISFIABLE"
        execution_stats['solution'] = None
        
        # Write results to markdown if path provided
        if output_md_file_path:
            algorithm_description = (
                "This problem was solved using the **Backward Decision-Making Approach**, "
                "which focuses on satisfying individual clauses by:\n\n"
                "1. Selecting an unsatisfied clause as the target\n"
                "2. Assigning values to its variables to make it satisfied\n"
                "3. Backtracking when inconsistencies are found or when a branch doesn't lead to a solution\n"
            )
            
            write_results_to_md(
                test_case_name,
                num_variables,
                clauses,
                "UNSATISFIABLE",
                execution_stats['time_taken_sec'],
                execution_stats,
                None,
                None,
                output_md_file_path,
                use_unicode=True,
                solver_name="Backward 3-SAT Solver",
                algorithm_description=algorithm_description
            )
            
        return None, execution_stats


if __name__ == "__main__":
    # Test Case 1 (from problem_definition.md)
    tc1_vars = 5
    tc1_clauses = [
        [1, -2, 3], [-1, 2, -4], [2, 3, 5], [-3, 4, -5]
    ]
    
    # Create results directory if it doesn't exist
    os.makedirs("results", exist_ok=True)
    
    # Run solver on test case 1
    solution1, stats1 = solve_3sat_backward(
        tc1_vars, 
        tc1_clauses, 
        "Original 5-Var Example",
        "results/backward_tc1.md"
    )

    print(f"Test Case 1: {stats1['status']} in {stats1['time_taken_sec']:.6f} seconds")
    
    # Test Case 2 (Small Unsatisfiable)
    tc2_vars = 3
    tc2_clauses = [
        [1, 2, 3], [1, 2, -3], [1, -2, 3], [1, -2, -3],
        [-1, 2, 3], [-1, 2, -3], [-1, -2, 3], [-1, -2, -3]
    ]
    
    # Run solver on test case 2
    solution2, stats2 = solve_3sat_backward(
        tc2_vars, 
        tc2_clauses, 
        "Small Unsatisfiable Example",
        "results/backward_tc2.md"
    )
    
    print(f"Test Case 2: {stats2['status']} in {stats2['time_taken_sec']:.6f} seconds")
    
    # Test Case 3 (Medium Satisfiable)
    tc3_vars = 6
    tc3_clauses = [
        [1, 2, -3], [-1, -2, 4], [3, -4, 5], 
        [-3, 4, 6], [-5, -6, 1], [5, 6, -2],
        [1, 3, 5], [-2, -4, -6], [2, 4, 6], [3, -5, 6]
    ]
    
    # Run solver on test case 3
    solution3, stats3 = solve_3sat_backward(
        tc3_vars, 
        tc3_clauses, 
        "Moderate Satisfiable Example",
        "results/backward_tc3.md"
    )
    
    print(f"Test Case 3: {stats3['status']} in {stats3['time_taken_sec']:.6f} seconds")
    print("\nAll test cases completed. Results saved to the 'results/' directory.") 