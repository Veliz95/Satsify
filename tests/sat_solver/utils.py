"""
Common Utilities for 3-SAT Solvers

This module provides shared utility functions used by both the goal-oriented and 
backward 3-SAT solvers.
"""

import os
from typing import Dict, List, Optional


def is_clause_satisfied(clause: List[int], assignments: Dict[int, bool]) -> bool:
    """
    Check if a clause is satisfied given the current variable assignments.
    
    Args:
        clause: A list of literals (positive or negative integers)
        assignments: Dictionary mapping variables to boolean values
    
    Returns:
        True if the clause is satisfied, False otherwise
    """
    for literal in clause:
        var = abs(literal)
        if var in assignments:
            # If literal is positive and var is True, or literal is negative and var is False
            if (literal > 0 and assignments[var]) or (literal < 0 and not assignments[var]):
                return True
    return False


def write_results_to_md(
    test_case_name: str,
    num_variables: int,
    clauses: List[List[int]],
    status: str,
    time_taken_sec: float,
    stats: Dict,
    solution: Optional[Dict[int, bool]],
    assignment_types: Optional[Dict[int, str]] = None,
    output_md_file_path: str = "solver_results.md",
    use_unicode: bool = True,
    solver_name: str = "3-SAT Solver",
    algorithm_description: str = ""
) -> None:
    """
    Write the solver execution results to a Markdown file.
    
    Args:
        test_case_name: Name of the test case
        num_variables: Number of variables in the problem
        clauses: List of clauses in the problem
        status: Solution status (SATISFIABLE/UNSATISFIABLE)
        time_taken_sec: Execution time in seconds
        stats: Dictionary of execution statistics
        solution: Dictionary of variable assignments or None if unsatisfiable
        assignment_types: Dictionary of assignment types (optional)
        output_md_file_path: Output file path
        use_unicode: Whether to use Unicode symbols (∧, ∨, ¬) or ASCII (AND, OR, NOT)
        solver_name: Name of the solver for the results header
        algorithm_description: Description of the algorithm used
    """
    try:
        # Ensure directory exists
        output_dir = os.path.dirname(output_md_file_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        with open(output_md_file_path, 'w', encoding='utf-8') as f:
            f.write(f"# {solver_name} Results: {test_case_name}\n\n")
            
            # Write Input Information
            f.write("## Input\n\n")
            f.write(f"- **Variables:** {num_variables}\n")
            f.write(f"- **Clauses:** {len(clauses)}\n")
            f.write("- **Formula:**\n")
            
            # Format the formula in CNF notation with Unicode or ASCII
            if use_unicode:
                conjunction_symbol = " ∧ "
                disjunction_symbol = " ∨ "
                negation_symbol = "¬"
            else:
                conjunction_symbol = " AND "
                disjunction_symbol = " OR "
                negation_symbol = "NOT "
            
            formula_str = conjunction_symbol.join([
                "(" + disjunction_symbol.join([
                    f"x{abs(lit)}" if lit > 0 else f"{negation_symbol}x{abs(lit)}" 
                    for lit in clause
                ]) + ")"
                for clause in clauses
            ])
            f.write(f"  - {formula_str}\n\n")
            
            # Write Execution Statistics
            f.write("## Execution Statistics\n\n")
            f.write(f"- **Status:** {status}\n")
            f.write(f"- **Time Taken:** {time_taken_sec:.6f} seconds\n")
            
            # Write stats based on which solver was used
            for key, value in stats.items():
                if key not in ['test_case_name', 'num_variables', 'num_clauses', 'time_taken_sec', 'status', 'solution', 'defaulted_variables']:
                    f.write(f"- **{key.replace('_', ' ').title()}:** {value}\n")
            
            # Write Solution (if satisfiable)
            if solution is not None and status == "SATISFIABLE":
                f.write("\n## Solution\n\n")
                
                if assignment_types:
                    f.write("| Variable | Value | Assignment Type |\n")
                    f.write("|----------|-------|----------------|\n")
                    
                    # Sort variables for consistent output
                    sorted_vars = sorted(solution.keys())
                    for var in sorted_vars:
                        var_value = "True" if solution[var] else "False"
                        
                        # Handle different assignment type naming between solvers
                        if var in stats.get('defaulted_variables', []):
                            assign_type = "Defaulted"
                        else:
                            assign_type = assignment_types.get(var, "Unknown")
                            
                        f.write(f"| x{var} | {var_value} | {assign_type} |\n")
                else:
                    f.write("| Variable | Value |\n")
                    f.write("|----------|-------|\n")
                    
                    # Sort variables for consistent output
                    sorted_vars = sorted(solution.keys())
                    for var in sorted_vars:
                        var_value = "True" if solution[var] else "False"
                        f.write(f"| x{var} | {var_value} |\n")
            
            # Write Algorithm Information
            if algorithm_description:
                f.write(f"\n## Algorithm\n\n{algorithm_description}\n")
    
    except (IOError, PermissionError) as e:
        print(f"Error writing results to {output_md_file_path}: {e}") 