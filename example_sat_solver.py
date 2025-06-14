from cnf_transformer import CNFInstance, CNFParser, CNFTransformer, CNFBenchmark
import time
from typing import Dict, List, Set, Optional, Tuple

class SimpleDPLLSolver:
    """Example DPLL-based SAT solver to demonstrate the framework"""
    
    def __init__(self):
        self.statistics = {
            'decisions': 0,
            'unit_propagations': 0,
            'conflicts': 0,
            'backtracks': 0
        }
    
    def solve(self, cnf: CNFInstance) -> Tuple[bool, Optional[Dict[int, bool]], Dict]:
        """
        Solve CNF instance using DPLL algorithm
        Returns: (is_satisfiable, assignment, statistics)
        """
        self.statistics = {
            'decisions': 0,
            'unit_propagations': 0,
            'conflicts': 0,
            'backtracks': 0
        }
        
        # Initialize assignment
        assignment = {}
        
        # Start DPLL search
        result = self._dpll(cnf.clauses, assignment)
        
        return result, assignment if result else None, self.statistics
    
    def _dpll(self, clauses: List[List[int]], assignment: Dict[int, bool]) -> bool:
        """DPLL recursive search"""
        
        # Unit propagation
        while True:
            unit_clause = self._find_unit_clause(clauses, assignment)
            if unit_clause is None:
                break
            
            literal = unit_clause[0]
            var = abs(literal)
            value = literal > 0
            
            if var in assignment and assignment[var] != value:
                # Conflict
                self.statistics['conflicts'] += 1
                return False
            
            assignment[var] = value
            self.statistics['unit_propagations'] += 1
        
        # Check for conflicts
        if self._has_conflict(clauses, assignment):
            self.statistics['conflicts'] += 1
            return False
        
        # Check if all clauses are satisfied
        if self._all_satisfied(clauses, assignment):
            return True
        
        # Pure literal elimination
        pure_literal = self._find_pure_literal(clauses, assignment)
        if pure_literal is not None:
            var = abs(pure_literal)
            value = pure_literal > 0
            assignment[var] = value
            return self._dpll(clauses, assignment)
        
        # Choose next variable to branch on
        var = self._choose_variable(clauses, assignment)
        if var is None:
            return True  # All variables assigned
        
        # Try positive assignment
        self.statistics['decisions'] += 1
        assignment[var] = True
        if self._dpll(clauses, assignment.copy()):
            return True
        
        # Try negative assignment
        self.statistics['backtracks'] += 1
        assignment[var] = False
        if self._dpll(clauses, assignment.copy()):
            return True
        
        # Backtrack
        del assignment[var]
        return False
    
    def _find_unit_clause(self, clauses: List[List[int]], assignment: Dict[int, bool]) -> Optional[List[int]]:
        """Find a unit clause (clause with only one unassigned literal)"""
        for clause in clauses:
            if self._is_satisfied(clause, assignment):
                continue
            
            unassigned_literals = []
            for literal in clause:
                var = abs(literal)
                if var not in assignment:
                    unassigned_literals.append(literal)
            
            if len(unassigned_literals) == 1:
                return unassigned_literals
        
        return None
    
    def _find_pure_literal(self, clauses: List[List[int]], assignment: Dict[int, bool]) -> Optional[int]:
        """Find a pure literal (variable that appears only in positive or negative form)"""
        positive_vars = set()
        negative_vars = set()
        
        for clause in clauses:
            if self._is_satisfied(clause, assignment):
                continue
                
            for literal in clause:
                var = abs(literal)
                if var not in assignment:
                    if literal > 0:
                        positive_vars.add(var)
                    else:
                        negative_vars.add(var)
        
        # Find pure literals
        pure_positive = positive_vars - negative_vars
        pure_negative = negative_vars - positive_vars
        
        if pure_positive:
            return next(iter(pure_positive))
        if pure_negative:
            return -next(iter(pure_negative))
        
        return None
    
    def _choose_variable(self, clauses: List[List[int]], assignment: Dict[int, bool]) -> Optional[int]:
        """Choose next variable to branch on (simple heuristic)"""
        # Count frequency of unassigned variables
        var_count = {}
        
        for clause in clauses:
            if self._is_satisfied(clause, assignment):
                continue
                
            for literal in clause:
                var = abs(literal)
                if var not in assignment:
                    var_count[var] = var_count.get(var, 0) + 1
        
        if not var_count:
            return None
        
        # Choose most frequent variable
        return max(var_count.items(), key=lambda x: x[1])[0]
    
    def _is_satisfied(self, clause: List[int], assignment: Dict[int, bool]) -> bool:
        """Check if a clause is satisfied by current assignment"""
        for literal in clause:
            var = abs(literal)
            if var in assignment:
                value = assignment[var]
                if (literal > 0 and value) or (literal < 0 and not value):
                    return True
        return False
    
    def _has_conflict(self, clauses: List[List[int]], assignment: Dict[int, bool]) -> bool:
        """Check if any clause is unsatisfied (conflict)"""
        for clause in clauses:
            all_false = True
            has_unassigned = False
            
            for literal in clause:
                var = abs(literal)
                if var not in assignment:
                    has_unassigned = True
                    all_false = False
                    break
                else:
                    value = assignment[var]
                    if (literal > 0 and value) or (literal < 0 and not value):
                        all_false = False
                        break
            
            if all_false and not has_unassigned:
                return True
        
        return False
    
    def _all_satisfied(self, clauses: List[List[int]], assignment: Dict[int, bool]) -> bool:
        """Check if all clauses are satisfied"""
        for clause in clauses:
            if not self._is_satisfied(clause, assignment):
                return False
        return True

def custom_dpll_transformation(cnf: CNFInstance) -> Dict:
    """Custom transformation using DPLL solver"""
    solver = SimpleDPLLSolver()
    
    start_time = time.perf_counter()
    is_sat, assignment, stats = solver.solve(cnf)
    solve_time = time.perf_counter() - start_time
    
    # Extract additional features
    adjacency = CNFTransformer.to_adjacency_list(cnf)
    implications = CNFTransformer.to_implication_graph(cnf)
    backbone = CNFTransformer.extract_backbone(cnf)
    pure_literals = CNFTransformer.get_pure_literals(cnf)
    
    return {
        'satisfiable': is_sat,
        'assignment': assignment,
        'solve_time_ms': solve_time * 1000,
        'solver_statistics': stats,
        'structural_features': {
            'adjacency_graph_size': len(adjacency),
            'implication_graph_size': len(implications),
            'backbone_size': len(backbone),
            'pure_literals_count': len(pure_literals)
        },
        'cnf_properties': {
            'clause_variable_ratio': cnf.num_clauses / cnf.num_variables if cnf.num_variables > 0 else 0,
            'average_clause_length': sum(len(clause) for clause in cnf.clauses) / len(cnf.clauses) if cnf.clauses else 0,
            'clause_length_distribution': cnf.get_clause_length_distribution()
        }
    }

class SATBenchmark:
    """Extended benchmark specifically for SAT solving methods"""
    
    def __init__(self, results_dir: str = "results"):
        self.base_benchmark = CNFBenchmark(results_dir)
        self.results_dir = self.base_benchmark.results_dir
    
    def benchmark_sat_method(self, cnf_file: str, solver_func) -> Dict:
        """Benchmark a specific SAT solving method"""
        cnf_path = Path(cnf_file) if isinstance(cnf_file, str) else cnf_file
        
        try:
            # Parse CNF
            cnf = CNFParser.parse_cnf_file(str(cnf_path))
            
            # Run solver
            start_time = time.perf_counter()
            result = solver_func(cnf)
            total_time = time.perf_counter() - start_time
            
            return {
                'instance_name': cnf_path.name,
                'success': True,
                'total_benchmark_time_ms': total_time * 1000,
                'cnf_info': cnf.to_dict(),
                'solver_result': result
            }
            
        except Exception as e:
            return {
                'instance_name': cnf_path.name,
                'success': False,
                'error': str(e),
                'solver_result': None
            }
    
    def compare_methods(self, cnf_files: List[str], methods: Dict[str, callable]) -> Dict:
        """Compare multiple SAT solving methods"""
        comparison_results = {}
        
        for method_name, method_func in methods.items():
            print(f"\nTesting method: {method_name}")
            method_results = []
            
            for cnf_file in cnf_files:
                print(f"  Processing {Path(cnf_file).name}...")
                result = self.benchmark_sat_method(cnf_file, method_func)
                method_results.append(result)
                
                if result['success']:
                    print(f"    ✓ Time: {result['total_benchmark_time_ms']:.2f} ms")
                    if 'solver_result' in result and result['solver_result']:
                        sat_result = result['solver_result'].get('satisfiable', 'unknown')
                        print(f"    Result: {sat_result}")
                else:
                    print(f"    ✗ Error: {result['error']}")
            
            comparison_results[method_name] = method_results
        
        # Save comparison results
        comparison_file = self.results_dir / "method_comparison.json"
        with open(comparison_file, 'w') as f:
            import json
            json.dump(comparison_results, f, indent=2, default=str)
        
        print(f"\nComparison results saved to {comparison_file}")
        return comparison_results

if __name__ == "__main__":
    # Example usage: Test the DPLL solver on your CNF files
    
    print("Testing Simple DPLL Solver...")
    
    sat_benchmark = SATBenchmark()
    
    # Test files
    test_files = [
        "benchmarks/uf_uuf/uf20-01.cnf",
        "benchmarks/uf_uuf/uf20-02.cnf",
        "benchmarks/uf_uuf/uf20-03.cnf"
    ]
    
    # Available files check
    from pathlib import Path
    available_files = [f for f in test_files if Path(f).exists()]
    
    if not available_files:
        print("No test files found. Creating a simple test...")
        # Create a simple test case
        test_cnf = CNFInstance(
            filename="test.cnf",
            num_variables=3,
            num_clauses=3,
            clauses=[[1, 2], [-1, 3], [-2, -3]],
            comments=["Simple test case"]
        )
        
        solver = SimpleDPLLSolver()
        is_sat, assignment, stats = solver.solve(test_cnf)
        
        print(f"Test result: {'SAT' if is_sat else 'UNSAT'}")
        print(f"Assignment: {assignment}")
        print(f"Statistics: {stats}")
    else:
        print(f"Found {len(available_files)} test files")
        
        # Compare different methods
        methods = {
            'dpll_solver': custom_dpll_transformation,
            'basic_analysis': lambda cnf: {
                'backbone': CNFTransformer.extract_backbone(cnf),
                'pure_literals': CNFTransformer.get_pure_literals(cnf),
                'adjacency_size': len(CNFTransformer.to_adjacency_list(cnf))
            }
        }
        
        comparison_results = sat_benchmark.compare_methods(available_files[:3], methods)
        
        print("\nComparison Summary:")
        for method_name, results in comparison_results.items():
            successful = sum(1 for r in results if r['success'])
            print(f"  {method_name}: {successful}/{len(results)} successful")
    
    print("\nExample complete!") 