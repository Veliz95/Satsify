#!/usr/bin/env python3
"""
Simple test script to verify module imports and basic functionality.
"""

import sys
print(f"Python version: {sys.version}")
print(f"Python path: {sys.path}")

try:
    import sat_solver
    print(f"sat_solver module found: {sat_solver}")
    print(f"sat_solver path: {sat_solver.__file__}")
    
    from sat_solver.test_cases import TC1
    print(f"Test case loaded: {TC1['name']}")
    
    print("\nAll imports successful!")
except ImportError as e:
    print(f"Import error: {e}")

print("\nDone.") 