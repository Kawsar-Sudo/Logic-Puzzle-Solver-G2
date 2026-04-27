"""Simple Streamlit UI for the Sudoku CSP Solver.

This file is intentionally kept small. It reuses the existing solver logic
from sudoku_solver.py and only adds a user-friendly interface.
"""

from __future__ import annotations

from typing import List

import streamlit as st

from puzzles import PUZZLES
from sudoku_solver import Board, SudokuSolver
from utils import board_from_string


st.set_page_config(
    page_title="Sudoku CSP Solver",
    page_icon="🧩",
    layout="centered",
)


def board_to_html(board: Board) -> str:
    """Converts a Sudoku board to a simple HTML table."""
    html = """
    <style>
        .sudoku-table {
            border-collapse: collapse;
            margin: 10px 0 20px 0;
            font-family: Arial, sans-serif;
        }
        .sudoku-table td {
            width: 42px;
            height: 42px;
            text-align: center;
            vertical-align: middle;
            border: 1px solid #999;
            font-size: 20px;
            font-weight: 600;
        }
        .sudoku-table tr:nth-child(3n) td {
            border-bottom: 3px solid #333;
        }
        .sudoku-table tr:first-child td {
            border-top: 3px solid #333;
        }
        .sudoku-table td:nth-child(3n) {
            border-right: 3px solid #333;
        }
        .sudoku-table td:first-child {
            border-left: 3px solid #333;
        }
        .empty-cell {
            color: #aaa;
        }
    </style>
    <table class="sudoku-table">
    """

    for row in board:
        html += "<tr>"
        for value in row:
            if value == 0:
                html += '<td class="empty-cell">.</td>'
            else:
                html += f"<td>{value}</td>"
        html += "</tr>"

    html += "</table>"
    return html


def show_board(title: str, board: Board) -> None:
    """Displays a board with a heading."""
    st.subheader(title)
    st.markdown(board_to_html(board), unsafe_allow_html=True)


def stats_to_dict(result) -> dict:
    """Converts solver statistics into a display-friendly dictionary."""
    stats = result.stats
    return {
        "Algorithm": stats.algorithm,
        "Solved": stats.solved,
        "Steps": stats.steps,
        "Assignments": stats.assignments,
        "Backtracks": stats.backtracks,
        "Time (seconds)": round(stats.elapsed_time, 6),
    }


def get_selected_board() -> Board | None:
    """Reads the selected puzzle from the sidebar."""
    puzzle_source = st.sidebar.radio(
        "Puzzle input method",
        ["Use sample puzzle", "Enter custom puzzle string"],
    )

    if puzzle_source == "Use sample puzzle":
        puzzle_name = st.sidebar.selectbox("Choose sample puzzle", list(PUZZLES.keys()))
        return [row[:] for row in PUZZLES[puzzle_name]]

    custom_string = st.sidebar.text_area(
        "Custom puzzle string",
        placeholder="Use 81 characters. Use 0 or . for empty cells.",
        height=120,
    )

    if not custom_string.strip():
        st.info("Enter a custom 81-character Sudoku string or choose a sample puzzle.")
        return None

    try:
        return board_from_string(custom_string)
    except ValueError as error:
        st.error(str(error))
        return None


def main() -> None:
    st.title("🧩 Sudoku Logic Puzzle Solver")
    st.write(
        "This AI system solves Sudoku using Constraint Satisfaction Problem techniques: "
        "Backtracking, MRV, Forward Checking, and LCV."
    )

    board = get_selected_board()

    solver_choice = st.sidebar.selectbox(
        "Solver mode",
        ["Optimized CSP", "Basic Backtracking", "Compare Both"],
    )

    if board is None:
        return

    show_board("Input Puzzle", board)

    if st.button("Solve Puzzle"):
        if solver_choice == "Basic Backtracking":
            solver = SudokuSolver(board)
            result = solver.solve_basic_backtracking()
            show_board("Solved Puzzle", result.board)
            st.subheader("Performance")
            st.table([stats_to_dict(result)])

        elif solver_choice == "Optimized CSP":
            solver = SudokuSolver(board)
            result = solver.solve_optimized_csp()
            show_board("Solved Puzzle", result.board)
            st.subheader("Performance")
            st.table([stats_to_dict(result)])

        else:
            basic_solver = SudokuSolver(board)
            optimized_solver = SudokuSolver(board)

            basic_result = basic_solver.solve_basic_backtracking()
            optimized_result = optimized_solver.solve_optimized_csp()

            show_board("Solved Puzzle", optimized_result.board)
            st.subheader("Performance Comparison")
            st.table([
                stats_to_dict(basic_result),
                stats_to_dict(optimized_result),
            ])

            if basic_result.stats.solved and optimized_result.stats.solved:
                st.success(
                    "Both solvers found a solution. The optimized CSP solver usually needs fewer steps "
                    "because it uses MRV, Forward Checking, and LCV."
                )
            elif not optimized_result.stats.solved:
                st.warning("The puzzle could not be solved or the input puzzle is invalid.")


if __name__ == "__main__":
    main()
