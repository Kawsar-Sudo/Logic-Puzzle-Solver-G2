"""Utility functions for the Sudoku CSP Solver."""

from __future__ import annotations

from typing import List

Board = List[List[int]]


def print_board(board: Board) -> None:
    """Prints a Sudoku board in a readable format."""
    for row in range(9):
        if row % 3 == 0 and row != 0:
            print("------+-------+------")

        row_values = []
        for col in range(9):
            if col % 3 == 0 and col != 0:
                row_values.append("|")

            value = board[row][col]
            row_values.append(str(value) if value != 0 else ".")

        print(" ".join(row_values))


def board_from_string(puzzle: str) -> Board:
    """
    Converts an 81-character string into a 9x9 Sudoku board.

    Accepted empty symbols:
    - 0
    - .
    """
    puzzle = puzzle.strip().replace("\n", "").replace(" ", "")

    if len(puzzle) != 81:
        raise ValueError("Puzzle string must contain exactly 81 characters.")

    board: Board = []
    for i in range(0, 81, 9):
        row = []
        for char in puzzle[i:i + 9]:
            if char in ("0", "."):
                row.append(0)
            elif char.isdigit() and char != "0":
                row.append(int(char))
            else:
                raise ValueError("Puzzle string can only contain digits 1-9, 0, or '.'.")
        board.append(row)

    return board


def board_to_string(board: Board) -> str:
    """Converts a 9x9 board into a compact 81-character string."""
    return "".join(str(cell) for row in board for cell in row)


def print_stats(stats) -> None:
    """Prints solver performance statistics."""
    print(f"Algorithm   : {stats.algorithm}")
    print(f"Solved      : {stats.solved}")
    print(f"Steps       : {stats.steps}")
    print(f"Assignments : {stats.assignments}")
    print(f"Backtracks  : {stats.backtracks}")
    print(f"Time        : {stats.elapsed_time:.6f} seconds")
