# Benchmark Results Directory

This directory contains the results from running the CNF transformation and benchmarking framework. Each JSON file represents performance data for different benchmark categories.

## Results Structure

### Summary Files
- **`overall_summary.json`**: Complete performance overview across all benchmark categories
- **`benchmarks.md`**: Detailed documentation of all benchmark categories and their characteristics

### Benchmark Category Results

#### **uf_uuf_results.json** - Uniform Random 3-SAT
- **Type**: Uniform Random 3-SAT instances
- **Instances**: 
  - `uf20-*`: 20 variables, ~91 clauses (satisfiable instances)
  - `uf50-*`: 50 variables, ~218 clauses (satisfiable instances)  
  - `uuf50-*`: 50 variables, ~218 clauses (unsatisfiable instances)
- **Purpose**: Standard benchmark for testing SAT solver performance on random instances
- **Characteristics**: Well-balanced between satisfiable and unsatisfiable instances

#### **cbs_results.json** - Constraint-Based Synthesis
- **Type**: Structured constraint problems
- **Instances**: Larger, more complex instances with structured constraints
- **Purpose**: Testing scalability and performance on real-world-like problems
- **Characteristics**: More complex structure than random instances

#### **dimacs_aim_results.json** - DIMACS AIM Instances
- **Type**: Artificially generated instances from DIMACS competitions
- **Purpose**: Benchmark against competition-standard instances
- **Characteristics**: Designed to be challenging for SAT solvers

#### **dimacs_dubois_results.json** - DIMACS Dubois Instances  
- **Type**: Dubois instances (known unsatisfiable)
- **Purpose**: Testing performance on specifically constructed unsatisfiable instances
- **Characteristics**: Proven to be unsatisfiable, good for testing solver correctness

#### **dimacs_phole_results.json** - DIMACS Pigeonhole Instances
- **Type**: Pigeonhole principle instances (known unsatisfiable)
- **Purpose**: Testing on mathematically proven unsatisfiable instances
- **Characteristics**: Based on the pigeonhole principle, inherently unsatisfiable

## JSON File Format

Each results file contains:

```json
{
  "summary": {
    "total_instances": 5,
    "successful_instances": 5,
    "average_total_time_ms": 2.68,
    "median_total_time_ms": 2.16,
    "min_time_ms": 1.45,
    "max_time_ms": 4.32
  },
  "results": [
    {
      "instance_name": "uf20-01.cnf",
      "parsing_time_ms": 0.45,
      "transformation_time_ms": 1.72,
      "total_time_ms": 2.16,
      "success": true,
      "variables": 20,
      "clauses": 91
    }
  ]
}
```

## Performance Metrics Explained

- **`parsing_time_ms`**: Time to read and parse the CNF file
- **`transformation_time_ms`**: Time to extract features and perform transformations
- **`total_time_ms`**: End-to-end processing time
- **`success`**: Whether the processing completed without errors
- **`variables`**: Number of variables in the CNF instance
- **`clauses`**: Number of clauses in the CNF instance

## Using the Results

### Performance Analysis
Compare timing results across different benchmark categories to understand:
- Which types of instances are more challenging to process
- How processing time scales with instance size
- Framework overhead for different problem types

### Method Comparison
When developing your custom SAT solving method:
1. Run benchmarks before and after changes
2. Compare results across different instance types
3. Use the JSON data for statistical analysis
4. Focus on categories where your method shows improvement

### Research Applications
- Use timing data for algorithm comparison papers
- Analyze scaling behavior across different problem sizes
- Compare preprocessing overhead vs. solving time
- Identify problem characteristics that affect performance

## Generating New Results

To regenerate or update results:

```bash
# Run complete benchmark suite
python cnf_transformer.py

# Run specific category analysis  
python run_tests.py benchmarks/uf_uuf/

# Generate comparison between methods
python your_custom_method_template.py
```

Results are automatically timestamped and can be compared across different runs or algorithm versions. 