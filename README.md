# Satsify: CNF Transformation and Benchmarking Framework

A comprehensive Python framework for parsing, transforming, and benchmarking CNF (Conjunctive Normal Form) files for SAT solving research and development.

## Overview

This framework provides tools to:
- Parse DIMACS CNF format files
- Transform CNF instances into various representations
- Benchmark your custom SAT solving methods
- Compare different approaches with detailed performance metrics
- Organize results in a structured format similar to your benchmarks directory

## Project Philosophy & Motivation

This project was born out of a deep curiosity about one of the most profound questions in computer science: the P versus NP problem. As an enthusiast rather than a professional coder, I embarked on this journey to explore complex problems like 3-SAT not just theoretically, but with hands-on experimentation. The initial foundations of this framework were laid in a single night, driven by a passion for understanding how different algorithmic approaches tackle NP-complete challenges.

The core idea is not just to build another SAT solver, but to create an intuitive and extensible **benchmarking framework**. This platform is designed for researchers, students, and fellow enthusiasts who want to rapidly prototype, test, and compare their own unique heuristics and methods without getting bogged down in boilerplate code.

## Directory Structure

```
pnp/
├── benchmarks/              # Your test instances
│   ├── uf_uuf/             # Uniform random 3-SAT instances
│   ├── cbs/                # CBS benchmark instances  
│   └── dimacs/             # DIMACS competition instances
│       ├── phole/
│       ├── dubois/
│       └── aim/
├── results/                # Generated results (mirrors benchmarks structure)
│   ├── uf_uuf/
│   ├── cbs/
│   └── dimacs/
│       ├── phole/
│       ├── dubois/
│       └── aim/
├── cnf_transformer.py      # Core CNF parsing and transformation
├── example_sat_solver.py   # Example DPLL SAT solver
├── run_tests.py           # Comprehensive test runner
└── your_custom_method_template.py  # Template for your method
```

## Key Components

### 1. CNF Parser (`CNFParser`)
Parses standard DIMACS CNF format files:
```python
cnf = CNFParser.parse_cnf_file("benchmarks/uf_uuf/uf20-01.cnf")
print(f"Variables: {cnf.num_variables}, Clauses: {cnf.num_clauses}")
```

### 2. CNF Transformer (`CNFTransformer`)
Converts CNF instances to different representations:
- **Adjacency List**: Variable interaction graph
- **Implication Graph**: Binary clause implications
- **Matrix Representation**: Linear algebra format
- **Backbone Extraction**: Unit clauses
- **Pure Literals**: Variables appearing only positive/negative

```python
adjacency = CNFTransformer.to_adjacency_list(cnf)
backbone = CNFTransformer.extract_backbone(cnf)
pure_literals = CNFTransformer.get_pure_literals(cnf)
```

### 3. Benchmark Framework (`CNFBenchmark`)
Performance testing and comparison:
```python
benchmark = CNFBenchmark()
result = benchmark.benchmark_single_file("test.cnf", your_custom_method)
```

## Quick Start

Choose the right script for your needs:

### 1. Run Complete Benchmark Suite (Recommended)
```bash
python cnf_transformer.py
```
**Purpose**: Main benchmark script that processes all CNF files in your benchmarks directory  
**What it does**: 
- Runs comprehensive benchmarks on all benchmark categories (uf_uuf, cbs, dimacs)
- Generates detailed JSON results for each category
- Creates performance summaries and comparisons
- Best for: Getting complete performance overview of the framework

### 2. Analyze Specific Files or Run Demo
```bash
python run_tests.py benchmarks/uf_uuf/uf20-01.cnf
```
**Purpose**: Analysis and demo script for specific files or examples  
**What it does**:
- Analyzes individual CNF files with detailed output
- Demonstrates the example DPLL solver in action
- Shows transformation features (adjacency lists, backbone extraction, etc.)
- Best for: Understanding how the framework works on specific instances

### 3. Run Framework Tests
```bash
python run_tests.py
```
**Purpose**: When run without arguments, runs internal framework tests  
**What it does**:
- Tests the framework components
- Validates parsing and transformation functions
- Runs example solver on sample instances
- Best for: Verifying the framework installation and basic functionality

### 4. Develop Your Custom Method
```bash
python your_custom_method_template.py
```
**Purpose**: Template and starting point for implementing your own SAT solving method  
**What it does**:
- Provides boilerplate code for your custom solver
- Shows how to integrate with the benchmark framework
- Includes example feature extraction and result formatting
- Best for: Building and testing your own SAT solving approach

## Implementing Your Custom Method

1. **Edit the Template**: Modify `your_custom_method_template.py`
2. **Implement Your Logic**: Add your SAT solving approach
3. **Test Your Method**: Use the benchmark framework

### Template Structure
```python
def your_custom_method(cnf: CNFInstance) -> Dict:
    # Extract features
    adjacency = CNFTransformer.to_adjacency_list(cnf)
    
    # Your custom logic here
    # - Variable ordering heuristics
    # - Conflict-driven clause learning  
    # - Neural network inference
    # - Quantum-inspired algorithms
    
    return {
        'satisfiable': True/False/None,
        'assignment': {...},  # Variable assignments
        'solve_time_ms': elapsed_time,
        'your_custom_metrics': {...}
    }
```

## Benchmark Results Format

Results are saved as JSON files with detailed statistics:

```json
{
  "summary": {
    "total_instances": 5,
    "successful_instances": 5,
    "average_total_time_ms": 2.68,
    "median_total_time_ms": 2.16
  },
  "results": [
    {
      "instance_name": "uf20-01.cnf",
      "parsing_time_ms": 0.45,
      "transformation_time_ms": 1.72,
      "total_time_ms": 2.16,
      "success": true
    }
  ]
}
```

## Example: Testing uf20-01.cnf

Your `uf20-01.cnf` file analysis shows:
- **Variables**: 20
- **Clauses**: 91 (all length 3)
- **Type**: Uniform random 3-SAT
- **Adjacency Graph**: 20 nodes (all variables connected)
- **Structure**: No backbone literals, no pure literals
- **Solvability**: SATISFIABLE (verified with DPLL)

## Advanced Usage

### Compare Multiple Methods
```python
methods = {
    'your_method': your_custom_method,
    'dpll_baseline': custom_dpll_transformation,
    'preprocessing_only': basic_preprocessing
}

sat_benchmark = SATBenchmark()
comparison = sat_benchmark.compare_methods(test_files, methods)
```

### Batch Processing
```python
benchmark = CNFBenchmark()
all_results = benchmark.run_comprehensive_benchmark()
```

### Custom Transformations
```python
def your_transformation(cnf):
    # Custom feature extraction
    matrix, rows, cols = CNFTransformer.to_matrix_representation(cnf)
    
    # Your analysis
    return custom_analysis_result
```

## Performance Metrics

The framework automatically tracks:
- **Parsing Time**: CNF file reading and processing
- **Transformation Time**: Feature extraction and preprocessing  
- **Total Time**: End-to-end processing
- **Memory Usage**: Approximate memory consumption
- **Success Rate**: Percentage of successful processing
- **Custom Metrics**: Your method-specific measurements

## Benchmark Categories

### uf_uuf (Uniform Random 3-SAT)
- `uf20-*`: 20 variables, ~91 clauses (satisfiable)
- `uf50-*`: 50 variables, ~218 clauses (satisfiable)
- `uuf50-*`: 50 variables, ~218 clauses (unsatisfiable)

### CBS (Constraint-Based Synthesis)
- Larger instances with structured constraints
- Good for testing scalability

### DIMACS Competition Instances
- **phole**: Pigeonhole principle (unsatisfiable)
- **dubois**: Dubois instances (unsatisfiable)
- **aim**: Artificially generated instances

## Tips for Your Method

1. **Start Small**: Test on uf20-* instances first
2. **Profile Performance**: Use the timing metrics to identify bottlenecks
3. **Validate Results**: Compare against known satisfiable/unsatisfiable instances
4. **Extract Features**: Use the provided transformations as starting points
5. **Iterate**: Use the benchmark framework to compare improvements

## Extending the Framework

### Add New Transformations
```python
@staticmethod
def your_new_transformation(cnf: CNFInstance):
    # Your custom transformation
    return transformed_data
```

### Custom Metrics
```python
def your_custom_benchmark(cnf_file, solver_func):
    # Custom benchmarking logic
    return detailed_metrics
```

## Results Analysis

Check the `results/` directory for:
- Individual test results (JSON)
- Overall summaries
- Performance comparisons
- Method-specific analyses

## Future Directions & How to Contribute

This framework is a living project, and the journey is just beginning. My next major goal is to implement and test a **hybrid SAT solving method**.

### The Hybrid Method Vision

The plan is to combine the "Goal-Oriented" heuristics developed in this project with **Survey Propagation (SP)**, an algorithm inspired by statistical physics that has shown great success on random k-SAT instances. The hypothesis is that a hybrid approach—using heuristics to simplify the problem space before applying the statistical power of SP—could yield robust performance across both structured and random problems.

### You Can Contribute!

This is an open invitation to anyone interested in SAT, algorithms, or computational complexity. Whether you are a seasoned researcher, a student, or a curious mind like myself, your contribution is welcome. Here are a few ways you can help:

-   **Implement New Heuristics:** Have an idea for a variable ordering or clause selection heuristic? Use the template to implement and benchmark it!
-   **Integrate Solvers:** Help integrate Survey Propagation or other advanced solvers into the framework.
-   **Expand Benchmarks:** Add new and challenging CNF instances to the `benchmarks/` directory.
-   **Improve Documentation:** If you find a section unclear, feel free to submit a pull request to improve it.
-   **Find and Report Bugs:** Test the framework and help make it more robust.

Let's explore the fascinating landscape of computational complexity together!

## Next Steps

1. **Implement Your Method**: Edit the template file
2. **Test on Small Instances**: Start with uf20-* files
3. **Scale Up**: Move to larger instances as your method improves
4. **Compare and Iterate**: Use benchmark results to guide improvements
5. **Document Results**: Save your findings in the results directory

The framework is designed to be flexible and extensible. Feel free to modify the transformations, add new metrics, or integrate with other SAT solving tools as needed for your research.

## Requirements

- Python 3.7+
- Standard library only (no external dependencies)
- CNF files in DIMACS format

Happy SAT solving! 🧠⚡ 