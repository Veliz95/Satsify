"""
3-SAT Test Cases

This module provides pre-defined test cases for the 3-SAT solvers.
"""

# Test Case 1: Original 5-Variable Example (Satisfiable)
# From the problem definition
TEST_CASE_ORIGINAL_5_VAR = {
    'name': 'Original 5-Var Example',
    'vars': 5,
    'clauses': [
        [1, -2, 3], [-1, 2, -4], [2, 3, 5], [-3, 4, -5]
    ],
    'expected': 'SATISFIABLE'
}

# Test Case 2: Small Unsatisfiable Example
# Contains all possible combinations of 3 variables, making it unsatisfiable
TEST_CASE_SMALL_UNSAT = {
    'name': 'Small Unsatisfiable Example',
    'vars': 3,
    'clauses': [
        [1, 2, 3], [1, 2, -3], [1, -2, 3], [1, -2, -3],
        [-1, 2, 3], [-1, 2, -3], [-1, -2, 3], [-1, -2, -3]
    ],
    'expected': 'UNSATISFIABLE'
}

# Test Case 3: Moderate Satisfiable Example
# A more complex example with 6 variables and 10 clauses
TEST_CASE_MODERATE_SAT = {
    'name': 'Moderate Satisfiable Example',
    'vars': 6,
    'clauses': [
        [1, 2, -3], [-1, -2, 4], [3, -4, 5], 
        [-3, 4, 6], [-5, -6, 1], [5, 6, -2],
        [1, 3, 5], [-2, -4, -6], [2, 4, 6], [3, -5, 6]
    ],
    'expected': 'SATISFIABLE'
}

# Test Case 4: Small Satisfiable Example
# A very simple satisfiable formula
TEST_CASE_SMALL_SAT = {
    'name': 'Small Satisfiable Example',
    'vars': 2,
    'clauses': [
        [1, 2, -1], [-1, -2, 2]
    ],
    'expected': 'SATISFIABLE'
}

# Collection of all test cases
ALL_TEST_CASES = [
    TEST_CASE_ORIGINAL_5_VAR, 
    TEST_CASE_SMALL_UNSAT, 
    TEST_CASE_MODERATE_SAT, 
    TEST_CASE_SMALL_SAT
]

# Function to get a test case by name
def get_test_case_by_name(name):
    """
    Get a test case by its name.
    
    Args:
        name: The name of the test case
        
    Returns:
        The test case dictionary or None if not found
    """
    for tc in ALL_TEST_CASES:
        if tc['name'] == name:
            return tc
    return None

# Function to run a solver on all test cases
def run_all_test_cases(solver_func, output_dir=None):
    """
    Run a solver function on all test cases.
    
    Args:
        solver_func: The solver function to use
        output_dir: Optional directory to write results to
        
    Returns:
        Dictionary of results by test case name
    """
    results = {}
    
    for tc in ALL_TEST_CASES:
        name = tc['name']
        
        # Define output path if directory provided
        output_path = None
        if output_dir:
            import os
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"{name.lower().replace(' ', '_')}.md")
        
        # Call the solver function with the appropriate signature
        # This assumes the solver function has a compatible interface
        result = solver_func(
            num_variables=tc['vars'],
            clauses=tc['clauses'],
            test_case_name=name,
            output_md_file_path=output_path
        )
        
        results[name] = result
        
    return results 