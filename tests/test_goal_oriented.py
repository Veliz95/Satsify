#!/usr/bin/env python3
"""
Direct test for the goal-oriented solver with debug information.
"""

import os
import sys
import traceback
from sat_solver.goal_oriented_sat_solver import solve_3sat_goal_oriented
from sat_solver.test_cases import TC1

def main():
    """Run the goal-oriented solver on a single test case with debug information."""
    print("Testing goal-oriented solver on Original 5-Var Example...")
    
    # Ensure results directory exists
    os.makedirs("results", exist_ok=True)
    
    # Extract test case details
    test_name = TC1['name']
    num_vars = TC1['vars']
    clauses = TC1['clauses']
    expected = TC1['expected']
    
    print(f"Test name: {test_name}")
    print(f"Variables: {num_vars}")
    print(f"Clauses: {len(clauses)}")
    print(f"Expected: {expected}")
    
    # Set output path
    output_path = "results/test_result.md"
    
    # Run the solver with exception handling
    print("\nRunning solver...")
    try:
        solve_3sat_goal_oriented(
            num_variables=num_vars,
            clauses=clauses,
            test_case_name=test_name,
            output_md_file_path=output_path
        )
        print("Solver completed successfully!")
    except Exception as e:
        print(f"ERROR: Solver failed with exception: {e}")
        print("\nTraceback:")
        traceback.print_exc(file=sys.stdout)
    
    # Check if the output file was created
    print(f"\nChecking if output file was created: {output_path}")
    if os.path.exists(output_path):
        print("Output file created successfully!")
        
        # Print first few lines of the output file
        print("\nFirst 10 lines of output file:")
        with open(output_path, 'r') as f:
            for i, line in enumerate(f):
                if i < 10:
                    print(f"  {line.strip()}")
                else:
                    break
    else:
        print("Output file was not created.")
    
    print("\nTest completed.")

if __name__ == "__main__":
    main() 