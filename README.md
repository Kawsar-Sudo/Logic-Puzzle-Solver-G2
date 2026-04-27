# Logic Puzzle Solver using Constraint Satisfaction Techniques

## Course
CSE440 - Artificial Intelligence

## Project Title
Logic Puzzle Solver: Sudoku Solver using Constraint Satisfaction Problem Techniques

## Project Overview
This project implements an AI system that solves Sudoku puzzles using Constraint Satisfaction Problem (CSP) techniques. Sudoku is modeled as a CSP where each empty cell is a variable, possible numbers from 1 to 9 are the domains, and Sudoku rules are the constraints.

## Dataset / Data Folder
This project does not use a large external dataset such as images, CSV files, or training data. However, the sample Sudoku puzzles used for testing are considered project data, so they are stored in:

```text
data/sudoku_puzzles.json
```

The solver loads those puzzles through:

```text
support/puzzles.py
```

## AI Techniques Used
- Constraint Satisfaction Problem formulation
- Backtracking Search
- Constraint Propagation through Forward Checking
- MRV heuristic: Minimum Remaining Values
- LCV heuristic: Least Constraining Value
- Performance comparison between basic and optimized search

## CSP Formulation

| CSP Component | Sudoku Representation |
|---|---|
| Variables | Empty cells in the 9x9 grid |
| Domains | Numbers 1 to 9 |
| Constraints | No repeated number in any row, column, or 3x3 box |
| Assignment | Placing a number in an empty cell |
| Solution | A complete valid Sudoku board |

## Folder Structure

```text
logic-puzzle-solver/
│
├── main.py
├── README.md
├── requirements.txt
│
├── data/
│   └── sudoku_puzzles.json
│
└── support/
    ├── app.py
    ├── sudoku_solver.py
    ├── puzzles.py
    ├── utils.py
    ├── report_draft.md
    └── __init__.py
```

## How to Run Console Version

### 1. Run default comparison on easy puzzle

```bash
python main.py
```

### 2. Run optimized CSP solver only

```bash
python main.py --solver optimized --puzzle easy
```

### 3. Run basic backtracking solver only

```bash
python main.py --solver basic --puzzle easy
```

### 4. Compare solvers on hard puzzle

```bash
python main.py --solver compare --puzzle hard
```

### 5. Run a custom puzzle

Use an 81-character string. Use `0` or `.` for empty cells.

```bash
python main.py --custom "530070000600195000098000060800060003400803001700020006060000280000419005000080079" --solver compare
```

## How to Run Streamlit UI

Install requirements first:

```bash
pip install -r requirements.txt
```

Because `app.py` is inside the `support/` folder, run:

```bash
streamlit run support/app.py
```

The UI allows you to:
- choose a sample Sudoku puzzle,
- enter a custom 81-character puzzle string,
- run the basic backtracking solver,
- run the optimized CSP solver,
- compare both solvers using steps, assignments, backtracks, and time.

## Sample Output

The program prints:
- input Sudoku board,
- solved Sudoku board,
- solving algorithm used,
- number of search steps,
- number of assignments,
- number of backtracks,
- execution time.

## Limitations
- Solves standard 9x9 Sudoku puzzles only.
- Does not generate new Sudoku puzzles.
- Does not solve Kakuro yet.
- Does not include image-based Sudoku input.

## Future Work
- Add Kakuro puzzle support.
- Add AC-3 constraint propagation.
- Add Sudoku puzzle generator.
- Add image-based Sudoku input.
- Improve the web interface with editable Sudoku cells.
