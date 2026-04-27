# Project Report Draft

## 1. Introduction
Logic puzzles are problems that require reasoning under constraints. Sudoku is one of the most popular examples of a logic puzzle. The objective is to fill a 9x9 grid with numbers from 1 to 9 while satisfying row, column, and 3x3 box constraints.

This project develops an AI-based Sudoku solver using Constraint Satisfaction Problem techniques. Instead of using brute force only, the system applies backtracking, MRV, forward checking, and LCV to search efficiently.

## 2. Problem Statement
The goal of this project is to develop an AI system that can solve Sudoku puzzles automatically using constraint satisfaction techniques. The system should accept an incomplete Sudoku board and return a valid solved board if a solution exists.

## 3. CSP Formulation
Sudoku can be represented as a Constraint Satisfaction Problem:

- Variables: Empty cells in the Sudoku grid.
- Domains: Possible values from 1 to 9.
- Constraints:
  - Each row must contain unique numbers.
  - Each column must contain unique numbers.
  - Each 3x3 box must contain unique numbers.

## 4. Algorithms Used

### 4.1 Backtracking Search
Backtracking is a depth-first search technique. The solver chooses an empty cell, tries possible values, and recursively continues. If a wrong assignment leads to failure, the solver removes that value and tries another.

### 4.2 MRV Heuristic
MRV stands for Minimum Remaining Values. It selects the cell with the fewest legal values. This reduces unnecessary search because highly constrained cells are solved first.

### 4.3 Forward Checking
Forward checking is a constraint propagation method. After assigning a value to a cell, the value is removed from the domains of all related cells. If any related cell has no possible value left, the algorithm backtracks early.

### 4.4 LCV Heuristic
LCV stands for Least Constraining Value. It tries the value that removes the fewest options from neighboring cells first.

## 5. System Workflow
1. Input Sudoku puzzle.
2. Validate the puzzle.
3. Convert the puzzle into CSP representation.
4. Solve using either basic backtracking or optimized CSP solver.
5. Display solved board.
6. Show performance statistics.

## 6. Tools and Technologies
- Programming Language: Python
- Libraries: Built-in Python libraries only
- Development Environment: VS Code / PyCharm / Google Colab

## 7. Results
The system successfully solves valid Sudoku puzzles and detects invalid initial boards. The optimized CSP solver generally requires fewer search steps and backtracks compared to basic backtracking.

## 8. Limitations
The current system only supports standard 9x9 Sudoku puzzles. It does not support puzzle generation, Kakuro solving, image input, or graphical user interface.

## 9. Future Work
Future improvements may include adding a GUI, supporting Kakuro puzzles, implementing AC-3, and adding image recognition for Sudoku boards.

## 10. Conclusion
This project demonstrates how constraint satisfaction techniques can solve logic puzzles efficiently. By using MRV, forward checking, and LCV, the solver reduces unnecessary search and solves Sudoku puzzles more intelligently than basic brute-force backtracking.
