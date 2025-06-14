#!/usr/bin/env python3
"""
Test runner for CNF transformation and benchmarking framework
This script demonstrates how to use the framework with your own CNF files
"""

import sys
import json
from pathlib import Path
from cnf_transformer import CNFParser, CNFTransformer, CNFBenchmark, CNFInstance
from example_sat_solver import SimpleDPLLSolver, custom_dpll_transformation, SATBenchmark

def analyze_cnf_file(filepath: str):
    """Analyze a single CNF file and print detailed information"""
    print(f"\n{'='*60}")
    print(f"ANALYZING: {filepath}")
    print(f"{'='*60}")
    
    try:
        # Parse the CNF file
        cnf = CNFParser.parse_cnf_file(filepath)
        
        # Basic information
        print(f"Filename: {cnf.filename}")
        print(f"Variables: {cnf.num_variables}")
        print(f"Clauses: {cnf.num_clauses}")
        print(f"Actual variables used: {cnf.get_variable_count()}")
        
        # Clause analysis
        clause_dist = cnf.get_clause_length_distribution()
        print(f"Clause length distribution: {clause_dist}")
        
        avg_clause_length = sum(len(clause) for clause in cnf.clauses) / len(cnf.clauses) if cnf.clauses else 0
        print(f"Average clause length: {avg_clause_length:.2f}")
        
        # Structural analysis
        print(f"\nStructural Analysis:")
        print(f"-" * 20)
        
        # Adjacency graph
        adjacency = CNFTransformer.to_adjacency_list(cnf)
        print(f"Variable adjacency graph nodes: {len(adjacency)}")
        
        # Implication graph
        implications = CNFTransformer.to_implication_graph(cnf)
        print(f"Implication graph edges: {sum(len(v) for v in implications.values())}")
        
        # Backbone literals
        backbone = CNFTransformer.extract_backbone(cnf)
        print(f"Backbone literals: {len(backbone)} -> {backbone}")
        
        # Pure literals
        pure_literals = CNFTransformer.get_pure_literals(cnf)
        print(f"Pure literals: {len(pure_literals)} -> {pure_literals}")
        
        # Matrix representation
        matrix, rows, cols = CNFTransformer.to_matrix_representation(cnf)
        print(f"Matrix representation: {rows}x{cols}")
        
        # Comments
        if cnf.comments:
            print(f"\nComments:")
            for comment in cnf.comments[:5]:  # Show first 5 comments
                print(f"  {comment}")
            if len(cnf.comments) > 5:
                print(f"  ... and {len(cnf.comments) - 5} more comments")
        
        return cnf
        
    except Exception as e:
        print(f"ERROR analyzing {filepath}: {e}")
        return None

def test_solver_on_file(filepath: str):
    """Test the DPLL solver on a CNF file"""
    print(f"\n{'='*60}")
    print(f"SOLVING: {filepath}")
    print(f"{'='*60}")
    
    try:
        cnf = CNFParser.parse_cnf_file(filepath)
        solver = SimpleDPLLSolver()
        
        print("Running DPLL solver...")
        is_sat, assignment, stats = solver.solve(cnf)
        
        print(f"Result: {'SATISFIABLE' if is_sat else 'UNSATISFIABLE'}")
        print(f"Statistics: {stats}")
        
        if is_sat and assignment:
            print(f"Sample assignment (first 10 variables):")
            for var in sorted(assignment.keys())[:10]:
                print(f"  x{var} = {assignment[var]}")
            if len(assignment) > 10:
                print(f"  ... and {len(assignment) - 10} more variables")
        
        return is_sat, stats
        
    except Exception as e:
        print(f"ERROR solving {filepath}: {e}")
        return None, None

def run_comprehensive_test():
    """Run comprehensive tests on available CNF files"""
    print("="*80)
    print("COMPREHENSIVE CNF ANALYSIS AND BENCHMARKING")
    print("="*80)
    
    # Find available CNF files
    test_files = []
    search_paths = [
        "benchmarks/uf_uuf/*.cnf",
        "benchmarks/cbs/*.cnf",
        "benchmarks/dimacs/*/*.cnf"
    ]
    
    for pattern in search_paths:
        test_files.extend(Path(".").glob(pattern))
    
    if not test_files:
        print("No CNF files found in benchmarks directory!")
        print("Creating a simple test case...")
        
        # Create a simple satisfiable test case
        test_cnf = CNFInstance(
            filename="simple_test.cnf",
            num_variables=4,
            num_clauses=5,
            clauses=[
                [1, 2],      # x1 OR x2
                [-1, 3],     # NOT x1 OR x3  
                [-2, 4],     # NOT x2 OR x4
                [-3, -4],    # NOT x3 OR NOT x4
                [1, -2, 3]   # x1 OR NOT x2 OR x3
            ],
            comments=["Simple test case", "Should be satisfiable"]
        )
        
        print("\nAnalyzing simple test case...")
        solver = SimpleDPLLSolver()
        is_sat, assignment, stats = solver.solve(test_cnf)
        print(f"Result: {'SAT' if is_sat else 'UNSAT'}")
        print(f"Assignment: {assignment}")
        print(f"Statistics: {stats}")
        return
    
    print(f"Found {len(test_files)} CNF files")
    
    # Analyze first few files in detail
    analysis_files = test_files[:3]  # Analyze first 3 files in detail
    
    print(f"\nDetailed analysis of {len(analysis_files)} files:")
    analyzed_cnfs = []
    
    for cnf_file in analysis_files:
        cnf = analyze_cnf_file(str(cnf_file))
        if cnf:
            analyzed_cnfs.append((str(cnf_file), cnf))
    
    # Test solver on small instances
    small_instances = [f for f in test_files if "uf20" in f.name][:2]
    
    if small_instances:
        print(f"\nTesting solver on {len(small_instances)} small instances:")
        for cnf_file in small_instances:
            test_solver_on_file(str(cnf_file))
    
    # Run benchmark
    print(f"\nRunning benchmark framework...")
    benchmark = CNFBenchmark()
    
    # Test with a subset of files
    test_subset = [str(f) for f in test_files[:5]]  # First 5 files
    
    print("Testing benchmark framework...")
    results = []
    for cnf_file in test_subset:
        result = benchmark.benchmark_single_file(cnf_file, custom_dpll_transformation)
        results.append(result)
        
        if result.success:
            print(f"✓ {Path(cnf_file).name}: {result.total_time*1000:.2f} ms")
        else:
            print(f"✗ {Path(cnf_file).name}: {result.error_message}")
    
    # Save results
    summary = benchmark.save_results(results, "sample_test_results.json")
    
    print(f"\nBenchmark Summary:")
    print(f"  Total instances: {summary.get('total_instances', 0)}")
    print(f"  Successful: {summary.get('successful_instances', 0)}")
    print(f"  Failed: {summary.get('failed_instances', 0)}")
    if 'average_total_time_ms' in summary:
        print(f"  Average time: {summary['average_total_time_ms']:.2f} ms")
    
    print(f"\nResults saved to: results/sample_test_results.json")

def create_custom_method_template():
    """Create a template for implementing your custom method"""
    template_code = '''
def your_custom_method(cnf: CNFInstance) -> Dict:
    """
    Template for your custom SAT solving method
    
    Args:
        cnf: CNFInstance containing the problem
        
    Returns:
        Dict containing your method's results
    """
    import time
    
    start_time = time.perf_counter()
    
    # 1. Extract features you need
    adjacency = CNFTransformer.to_adjacency_list(cnf)
    backbone = CNFTransformer.extract_backbone(cnf)
    pure_literals = CNFTransformer.get_pure_literals(cnf)
    
    # 2. Implement your custom logic here
    # For example:
    # - Variable ordering heuristics
    # - Conflict-driven clause learning
    # - Preprocessing techniques
    # - Neural network inference
    # - Quantum-inspired algorithms
    # - etc.
    
    # Placeholder for your method
    your_result = {
        'method_name': 'YourMethodName',
        'satisfiable': None,  # True/False/None for unknown
        'assignment': None,   # Variable assignment if SAT
        'confidence': 0.0,    # Confidence in result (0-1)
        'custom_features': {
            'adjacency_graph_density': len(adjacency) / cnf.num_variables if cnf.num_variables > 0 else 0,
            'backbone_ratio': len(backbone) / cnf.num_variables if cnf.num_variables > 0 else 0,
            'pure_literal_ratio': len(pure_literals) / cnf.num_variables if cnf.num_variables > 0 else 0,
            # Add your custom features here
        }
    }
    
    solve_time = time.perf_counter() - start_time
    your_result['solve_time_ms'] = solve_time * 1000
    
    return your_result

# Example usage:
# benchmark = CNFBenchmark()
# result = benchmark.benchmark_single_file("your_file.cnf", your_custom_method)
'''
    
    template_file = Path("your_custom_method_template.py")
    with open(template_file, 'w') as f:
        f.write(template_code)
    
    print(f"Custom method template created: {template_file}")
    print("Edit this file to implement your specific method!")

def main():
    """Main function to run tests"""
    print("CNF Transformation and Benchmarking Framework")
    print("="*50)
    
    if len(sys.argv) > 1:
        # Test specific file
        cnf_file = sys.argv[1]
        if Path(cnf_file).exists():
            analyze_cnf_file(cnf_file)
            test_solver_on_file(cnf_file)
        else:
            print(f"File not found: {cnf_file}")
    else:
        # Run comprehensive tests
        run_comprehensive_test()
        
        # Create template for custom method
        create_custom_method_template()
        
        print("\n" + "="*80)
        print("NEXT STEPS:")
        print("="*80)
        print("1. Edit 'your_custom_method_template.py' to implement your method")
        print("2. Run: python run_tests.py <your_cnf_file.cnf> to test specific files")
        print("3. Use the benchmark framework to compare methods")
        print("4. Check the 'results' directory for detailed benchmark results")
        print("5. Modify the transformation functions in cnf_transformer.py as needed")

if __name__ == "__main__":
    main() 