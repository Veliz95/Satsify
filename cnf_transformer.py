import os
import time
import json
import statistics
from typing import List, Tuple, Dict, Set
from dataclasses import dataclass
from pathlib import Path
import shutil

@dataclass
class CNFInstance:
    """Represents a CNF instance with metadata"""
    filename: str
    num_variables: int
    num_clauses: int
    clauses: List[List[int]]
    comments: List[str]
    
    def get_variable_count(self) -> int:
        """Get the actual number of unique variables used"""
        variables = set()
        for clause in self.clauses:
            for literal in clause:
                variables.add(abs(literal))
        return len(variables)
    
    def get_clause_length_distribution(self) -> Dict[int, int]:
        """Get distribution of clause lengths"""
        distribution = {}
        for clause in self.clauses:
            length = len(clause)
            distribution[length] = distribution.get(length, 0) + 1
        return distribution
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'filename': self.filename,
            'num_variables': self.num_variables,
            'num_clauses': self.num_clauses,
            'actual_variables': self.get_variable_count(),
            'clause_length_distribution': self.get_clause_length_distribution(),
            'comments': self.comments
        }

class CNFParser:
    """Parser for DIMACS CNF format files"""
    
    @staticmethod
    def parse_cnf_file(filepath: str) -> CNFInstance:
        """Parse a DIMACS CNF file"""
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"CNF file not found: {filepath}")
        
        comments = []
        clauses = []
        num_variables = 0
        num_clauses = 0
        
        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()
                
                if not line:
                    continue
                
                if line.startswith('c'):
                    # Comment line
                    comments.append(line[1:].strip())
                elif line.startswith('p cnf'):
                    # Problem line: p cnf <variables> <clauses>
                    parts = line.split()
                    if len(parts) >= 4:
                        num_variables = int(parts[2])
                        num_clauses = int(parts[3])
                elif line.startswith('%'):
                    # End of clauses
                    break
                else:
                    # Clause line
                    literals = [int(x) for x in line.split() if x != '0']
                    if literals:  # Only add non-empty clauses
                        clauses.append(literals)
        
        return CNFInstance(
            filename=filepath.name,
            num_variables=num_variables,
            num_clauses=num_clauses,
            clauses=clauses,
            comments=comments
        )

class CNFTransformer:
    """Transform CNF instances for different solving approaches"""
    
    @staticmethod
    def to_adjacency_list(cnf: CNFInstance) -> Dict[int, Set[int]]:
        """Convert CNF to variable adjacency list representation"""
        adjacency = {}
        
        for clause in cnf.clauses:
            # Variables in the same clause are "adjacent"
            variables = [abs(lit) for lit in clause]
            
            for var in variables:
                if var not in adjacency:
                    adjacency[var] = set()
                
                # Add all other variables in the clause as neighbors
                for other_var in variables:
                    if other_var != var:
                        adjacency[var].add(other_var)
        
        return adjacency
    
    @staticmethod
    def to_implication_graph(cnf: CNFInstance) -> Dict[int, List[int]]:
        """Convert CNF to implication graph for unit propagation"""
        implications = {}
        
        for clause in cnf.clauses:
            if len(clause) == 2:  # Binary clause creates direct implication
                lit1, lit2 = clause
                # -lit1 -> lit2 and -lit2 -> lit1
                if -lit1 not in implications:
                    implications[-lit1] = []
                if -lit2 not in implications:
                    implications[-lit2] = []
                    
                implications[-lit1].append(lit2)
                implications[-lit2].append(lit1)
        
        return implications
    
    @staticmethod
    def to_matrix_representation(cnf: CNFInstance) -> Tuple[List[List[int]], int, int]:
        """Convert CNF to matrix representation for linear algebra approaches"""
        max_var = cnf.get_variable_count()
        matrix = []
        
        for clause in cnf.clauses:
            row = [0] * (2 * max_var)  # Positive and negative literals
            
            for literal in clause:
                if literal > 0:
                    row[literal - 1] = 1  # Positive literal
                else:
                    row[max_var + abs(literal) - 1] = 1  # Negative literal
            
            matrix.append(row)
        
        return matrix, len(cnf.clauses), 2 * max_var
    
    @staticmethod
    def extract_backbone(cnf: CNFInstance) -> Set[int]:
        """Extract unit clauses (backbone literals)"""
        backbone = set()
        
        for clause in cnf.clauses:
            if len(clause) == 1:
                backbone.add(clause[0])
        
        return backbone
    
    @staticmethod
    def get_pure_literals(cnf: CNFInstance) -> Set[int]:
        """Find pure literals (variables that appear only in positive or negative form)"""
        positive_vars = set()
        negative_vars = set()
        
        for clause in cnf.clauses:
            for literal in clause:
                if literal > 0:
                    positive_vars.add(literal)
                else:
                    negative_vars.add(abs(literal))
        
        # Pure literals appear only in one form
        pure_positive = positive_vars - negative_vars
        pure_negative = negative_vars - positive_vars
        
        pure_literals = set()
        pure_literals.update(pure_positive)
        pure_literals.update(-var for var in pure_negative)
        
        return pure_literals

@dataclass
class BenchmarkResult:
    """Result of a benchmark test"""
    instance_name: str
    parsing_time: float
    transformation_time: float
    total_time: float
    memory_usage: int  # in bytes
    success: bool
    error_message: str = ""
    
    def to_dict(self) -> Dict:
        return {
            'instance_name': self.instance_name,
            'parsing_time_ms': self.parsing_time * 1000,
            'transformation_time_ms': self.transformation_time * 1000,
            'total_time_ms': self.total_time * 1000,
            'memory_usage_bytes': self.memory_usage,
            'success': self.success,
            'error_message': self.error_message
        }

class CNFBenchmark:
    """Benchmark framework for CNF processing methods"""
    
    def __init__(self, results_dir: str = "results"):
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.results_dir / "uf_uuf").mkdir(exist_ok=True)
        (self.results_dir / "cbs").mkdir(exist_ok=True)
        (self.results_dir / "dimacs").mkdir(exist_ok=True)
        (self.results_dir / "dimacs" / "phole").mkdir(exist_ok=True)
        (self.results_dir / "dimacs" / "dubois").mkdir(exist_ok=True)
        (self.results_dir / "dimacs" / "aim").mkdir(exist_ok=True)
    
    def benchmark_single_file(self, cnf_file: str, transformation_func=None) -> BenchmarkResult:
        """Benchmark processing of a single CNF file"""
        cnf_path = Path(cnf_file)
        
        try:
            # Measure parsing time
            start_time = time.perf_counter()
            cnf_instance = CNFParser.parse_cnf_file(cnf_file)
            parsing_time = time.perf_counter() - start_time
            
            # Measure transformation time
            transformation_start = time.perf_counter()
            
            if transformation_func:
                transformation_func(cnf_instance)
            else:
                # Default transformations
                CNFTransformer.to_adjacency_list(cnf_instance)
                CNFTransformer.to_implication_graph(cnf_instance)
                CNFTransformer.extract_backbone(cnf_instance)
                CNFTransformer.get_pure_literals(cnf_instance)
            
            transformation_time = time.perf_counter() - transformation_start
            total_time = parsing_time + transformation_time
            
            # Estimate memory usage (rough approximation)
            memory_usage = len(str(cnf_instance.clauses).encode('utf-8'))
            
            return BenchmarkResult(
                instance_name=cnf_path.name,
                parsing_time=parsing_time,
                transformation_time=transformation_time,
                total_time=total_time,
                memory_usage=memory_usage,
                success=True
            )
            
        except Exception as e:
            return BenchmarkResult(
                instance_name=cnf_path.name,
                parsing_time=0,
                transformation_time=0,
                total_time=0,
                memory_usage=0,
                success=False,
                error_message=str(e)
            )
    
    def benchmark_directory(self, benchmark_dir: str, transformation_func=None) -> List[BenchmarkResult]:
        """Benchmark all CNF files in a directory"""
        benchmark_path = Path(benchmark_dir)
        results = []
        
        if not benchmark_path.exists():
            print(f"Warning: Directory {benchmark_dir} does not exist")
            return results
        
        cnf_files = list(benchmark_path.glob("*.cnf"))
        
        print(f"Found {len(cnf_files)} CNF files in {benchmark_dir}")
        
        for cnf_file in cnf_files:
            print(f"Processing {cnf_file.name}...")
            result = self.benchmark_single_file(str(cnf_file), transformation_func)
            results.append(result)
            
            if result.success:
                print(f"  ✓ Completed in {result.total_time:.3f}s")
            else:
                print(f"  ✗ Failed: {result.error_message}")
        
        return results
    
    def save_results(self, results: List[BenchmarkResult], output_file: str):
        """Save benchmark results to JSON file"""
        output_path = self.results_dir / output_file
        
        # Prepare summary statistics
        successful_results = [r for r in results if r.success]
        
        if successful_results:
            parsing_times = [r.parsing_time for r in successful_results]
            transformation_times = [r.transformation_time for r in successful_results]
            total_times = [r.total_time for r in successful_results]
            
            summary = {
                'total_instances': len(results),
                'successful_instances': len(successful_results),
                'failed_instances': len(results) - len(successful_results),
                'average_parsing_time_ms': statistics.mean(parsing_times) * 1000,
                'average_transformation_time_ms': statistics.mean(transformation_times) * 1000,
                'average_total_time_ms': statistics.mean(total_times) * 1000,
                'median_total_time_ms': statistics.median(total_times) * 1000,
                'min_total_time_ms': min(total_times) * 1000,
                'max_total_time_ms': max(total_times) * 1000
            }
        else:
            summary = {
                'total_instances': len(results),
                'successful_instances': 0,
                'failed_instances': len(results),
                'error': 'No successful processing'
            }
        
        output_data = {
            'summary': summary,
            'results': [result.to_dict() for result in results]
        }
        
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"Results saved to {output_path}")
        return summary
    
    def run_comprehensive_benchmark(self):
        """Run comprehensive benchmark across all benchmark directories"""
        benchmark_dirs = [
            "benchmarks/uf_uuf",
            "benchmarks/cbs",
            "benchmarks/dimacs/phole",
            "benchmarks/dimacs/dubois", 
            "benchmarks/dimacs/aim"
        ]
        
        all_results = {}
        
        for bench_dir in benchmark_dirs:
            if Path(bench_dir).exists():
                print(f"\n{'='*50}")
                print(f"Benchmarking {bench_dir}")
                print(f"{'='*50}")
                
                results = self.benchmark_directory(bench_dir)
                
                # Determine output filename
                dir_name = Path(bench_dir).name
                parent_name = Path(bench_dir).parent.name
                
                if parent_name == "dimacs":
                    output_file = f"dimacs_{dir_name}_results.json"
                else:
                    output_file = f"{dir_name}_results.json"
                
                summary = self.save_results(results, output_file)
                all_results[bench_dir] = summary
                
                print(f"\nSummary for {bench_dir}:")
                print(f"  Total instances: {summary.get('total_instances', 0)}")
                print(f"  Successful: {summary.get('successful_instances', 0)}")
                print(f"  Failed: {summary.get('failed_instances', 0)}")
                if 'average_total_time_ms' in summary:
                    print(f"  Average time: {summary['average_total_time_ms']:.2f} ms")
        
        # Save overall summary
        overall_summary_path = self.results_dir / "overall_summary.json"
        with open(overall_summary_path, 'w') as f:
            json.dump(all_results, f, indent=2)
        
        print(f"\n{'='*50}")
        print("OVERALL BENCHMARK COMPLETED")
        print(f"{'='*50}")
        print(f"Overall summary saved to {overall_summary_path}")
        
        return all_results

def custom_transformation_example(cnf: CNFInstance):
    """Example custom transformation - replace with your own method"""
    # Example: Your custom SAT solving preprocessing
    
    # 1. Extract structural features
    adjacency = CNFTransformer.to_adjacency_list(cnf)
    backbone = CNFTransformer.extract_backbone(cnf)
    pure_literals = CNFTransformer.get_pure_literals(cnf)
    
    # 2. Your custom analysis here
    # For example: variable ordering heuristics, conflict analysis, etc.
    
    # 3. Apply your transformations
    # This is where you would implement your specific method
    
    return {
        'adjacency_graph': adjacency,
        'backbone_literals': backbone,
        'pure_literals': pure_literals,
        'your_custom_data': "Add your specific transformations here"
    }

if __name__ == "__main__":
    # Create benchmark instance
    benchmark = CNFBenchmark()
    
    # Example: Test with a single file
    print("Testing with uf20-01.cnf...")
    result = benchmark.benchmark_single_file("benchmarks/uf_uuf/uf20-01.cnf", custom_transformation_example)
    
    if result.success:
        print(f"✓ Single file test successful!")
        print(f"  Parsing time: {result.parsing_time*1000:.2f} ms")
        print(f"  Transformation time: {result.transformation_time*1000:.2f} ms")
        print(f"  Total time: {result.total_time*1000:.2f} ms")
    else:
        print(f"✗ Single file test failed: {result.error_message}")
    
    # Run comprehensive benchmark
    print("\nStarting comprehensive benchmark...")
    all_results = benchmark.run_comprehensive_benchmark()
    
    print("\nBenchmark complete! Check the 'results' directory for detailed results.") 