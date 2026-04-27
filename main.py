"""Main runner for the Sudoku Logic Puzzle Solver project."""

from __future__ import annotations

import argparse
from support.sudoku_solver import SudokuSolver
from support.puzzles import PUZZLES
from support.utils import board_from_string, print_board, print_stats


def run_basic(board):
    solver = SudokuSolver(board)
    result = solver.solve_basic_backtracking()

    print("\nSolved Board:")
    print_board(result.board)
    print("\nPerformance:")
    print_stats(result.stats)

    return result


def run_optimized(board):
    solver = SudokuSolver(board)
    result = solver.solve_optimized_csp()

    print("\nSolved Board:")
    print_board(result.board)
    print("\nPerformance:")
    print_stats(result.stats)

    return result


def compare_solvers(board):
    print("\n========== Basic Backtracking ==========")
    basic_result = run_basic(board)

    print("\n========== Optimized CSP Solver ==========")
    optimized_result = run_optimized(board)

    print("\n========== Comparison ==========")
    print(f"{'Algorithm':35} {'Solved':8} {'Steps':10} {'Backtracks':12} {'Time (s)':10}")
    print("-" * 80)
    print(
        f"{basic_result.stats.algorithm:35} "
        f"{str(basic_result.stats.solved):8} "
        f"{basic_result.stats.steps:<10} "
        f"{basic_result.stats.backtracks:<12} "
        f"{basic_result.stats.elapsed_time:.6f}"
    )
    print(
        f"{optimized_result.stats.algorithm:35} "
        f"{str(optimized_result.stats.solved):8} "
        f"{optimized_result.stats.steps:<10} "
        f"{optimized_result.stats.backtracks:<12} "
        f"{optimized_result.stats.elapsed_time:.6f}"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Sudoku Logic Puzzle Solver using CSP techniques."
    )

    parser.add_argument(
        "--puzzle",
        choices=list(PUZZLES.keys()),
        default="easy",
        help="Choose a sample puzzle."
    )

    parser.add_argument(
        "--solver",
        choices=["basic", "optimized", "compare"],
        default="compare",
        help="Choose which solver to run."
    )

    parser.add_argument(
        "--custom",
        type=str,
        default=None,
        help="Optional 81-character custom puzzle string using 0 or . for empty cells."
    )

    args = parser.parse_args()

    if args.custom:
        board = board_from_string(args.custom)
        puzzle_name = "custom"
    else:
        board = PUZZLES[args.puzzle]
        puzzle_name = args.puzzle

    print("Logic Puzzle Solver: Sudoku using Constraint Satisfaction")
    print(f"Selected puzzle: {puzzle_name}")
    print(f"Selected solver: {args.solver}")

    print("\nInput Board:")
    print_board(board)

    if args.solver == "basic":
        print("\n========== Basic Backtracking ==========")
        run_basic(board)
    elif args.solver == "optimized":
        print("\n========== Optimized CSP Solver ==========")
        run_optimized(board)
    else:
        compare_solvers(board)


if __name__ == "__main__":
    main()
