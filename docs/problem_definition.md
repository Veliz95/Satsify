# 3-SAT Problem Definition for Experimental Solver

## 1. Introduction to 3-SAT

The **3-Satisfiability Problem (3-SAT)** is a classic decision problem in computational complexity theory. It is a specific instance of the Boolean Satisfiability Problem (SAT). A 3-SAT problem asks whether a given Boolean formula, written in a specific structure called **3-Conjunctive Normal Form (3-CNF)**, can be made true by assigning truth values (True/False) to its variables.

3-SAT is fundamentally important because it was the first problem proven to be **NP-complete**. This means that many other complex problems can be translated into 3-SAT, and an efficient algorithm for 3-SAT would imply efficient algorithms for many other hard problems (potentially P=NP).

## 2. Goal

The objective is to determine if there exists an assignment of truth values (True/False, or equivalently 1/0) to the variables in a given 3-CNF Boolean formula such that the entire formula evaluates to **True**. If such an assignment exists, the formula is "satisfiable," and one such assignment should be provided. Otherwise, the formula is "unsatisfiable."

## 3. Input Format (for Python implementation)

The problem will be represented in Python using the following structure:

* **`num_variables`**: An integer ($N$) representing the total number of distinct Boolean variables in the formula. Variables are typically numbered from 1 to $N$.
* **`clauses`**: A list of lists. Each inner list represents a single **clause**. Each clause, in turn, is a list containing exactly three integers, called **literals**.
    * A **positive integer `v`** (where `1 <= v <= num_variables`) represents the variable $x_v$ (e.g., `1` represents $x_1$).
    * A **negative integer `-v`** (where `1 <= v <= num_variables`) represents the negated variable $\neg x_v$ (e.g., `-1` represents $\neg x_1$).

Each clause is a disjunction (OR) of its three literals. The entire formula is a conjunction (AND) of all its clauses.

## 4. Example Instance

* **`num_variables = 5`**
* **`clauses = [[1, -2, 3], [-1, 2, -4], [2, 3, 5], [-3, 4, -5]]`**

This corresponds to the Boolean formula:
$(x_1 \lor \neg x_2 \lor x_3) \land (\neg x_1 \lor x_2 \lor \neg x_4) \land (x_2 \lor x_3 \lor x_5) \land (\neg x_3 \lor x_4 \lor \neg x_5)$

## 5. Output Format

The Python function solving the problem should return:

* **If a satisfying assignment is found:** A dictionary where keys are variable numbers (integers from 1 to `num_variables`) and values are their assigned Boolean values (`True` or `False`).
    * _Example (format only, not necessarily the solution to the instance above):_
        `{1: True, 2: False, 3: True, 4: False, 5: True}`
* **If the formula is unsatisfiable:** The function should return `None`.

## 6. Success Criterion

A solution is considered successful if the returned variable assignment, when applied to the input formula, causes **every clause** to evaluate to True, thereby making the entire formula True.