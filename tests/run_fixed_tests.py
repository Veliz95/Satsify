#!/usr/bin/env python3
"""
Script to run all test cases with the fixed solver.
"""

import os
from sat_solver.fixed_goal_oriented_solver import solve_3sat_fixed
from sat_solver.test_cases import ALL_TEST_CASES

def main():
    """Run the fixed solver on all test cases."""
    print("Running Fixed Solver tests...")
    
    # Ensure results directory exists
    os.makedirs("results", exist_ok=True)
    
    # Run fixed solver on all test cases
    for tc in ALL_TEST_CASES:
        print(f"Testing {tc['name']}...")
        output_path = f"results/fixed_{tc['name'].lower().replace(' ', '_')}.md"
        
        solution = solve_3sat_fixed(
            num_variables=tc['vars'],
            clauses=tc['clauses'],
            test_case_name=tc['name'],
            output_md_file_path=output_path
        )
        
        status = "SATISFIABLE" if solution else "UNSATISFIABLE"
        expected = tc['expected']
        match = "✓" if status == expected else "✗"
        
        print(f"  Result: {status} (Expected: {expected}) {match}")
    
    print("\nAll tests completed. Results saved to the 'results/' directory.")

if __name__ == "__main__":
    main() 