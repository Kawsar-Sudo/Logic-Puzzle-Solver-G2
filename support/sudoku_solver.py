"""
Sudoku Solver using Constraint Satisfaction Problem (CSP) techniques.

Algorithms implemented:
1. Basic Backtracking
2. Backtracking with MRV + Forward Checking + optional LCV ordering

This module is designed for a CSE440 Artificial Intelligence project.
"""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Dict, List, Optional, Set, Tuple
import copy


Board = List[List[int]]
Cell = Tuple[int, int]
Domains = Dict[Cell, Set[int]]


@dataclass
class SolverStats:
    """Stores performance statistics for a solver run."""
    algorithm: str
    solved: bool
    steps: int
    assignments: int
    backtracks: int
    elapsed_time: float


@dataclass
class SolverResult:
    """Stores the final result of a solver run."""
    board: Board
    stats: SolverStats


class SudokuSolver:
    """Solves 9x9 Sudoku puzzles using CSP-based algorithms."""

    SIZE = 9
    BOX_SIZE = 3
    VALUES = set(range(1, 10))

    def __init__(self, board: Board):
        self.original_board = self.copy_board(board)
        self.steps = 0
        self.assignments = 0
        self.backtracks = 0

    @staticmethod
    def copy_board(board: Board) -> Board:
        """Returns a deep copy of the Sudoku board."""
        return [row[:] for row in board]

    @staticmethod
    def is_complete(board: Board) -> bool:
        """Returns True if the board has no empty cells."""
        return all(cell != 0 for row in board for cell in row)

    def reset_stats(self) -> None:
        """Resets solver statistics before a new run."""
        self.steps = 0
        self.assignments = 0
        self.backtracks = 0

    def validate_board_shape(self, board: Board) -> bool:
        """Checks whether the board is a valid 9x9 grid containing numbers 0-9."""
        if len(board) != self.SIZE:
            return False
        for row in board:
            if len(row) != self.SIZE:
                return False
            for value in row:
                if not isinstance(value, int) or value < 0 or value > 9:
                    return False
        return True

    def is_initial_board_valid(self, board: Board) -> bool:
        """
        Checks whether the initial Sudoku board violates any Sudoku rule.
        Empty cells are represented by 0 and are ignored.
        """
        if not self.validate_board_shape(board):
            return False

        # Check rows
        for row in range(self.SIZE):
            values = [board[row][col] for col in range(self.SIZE) if board[row][col] != 0]
            if len(values) != len(set(values)):
                return False

        # Check columns
        for col in range(self.SIZE):
            values = [board[row][col] for row in range(self.SIZE) if board[row][col] != 0]
            if len(values) != len(set(values)):
                return False

        # Check 3x3 boxes
        for box_row in range(0, self.SIZE, self.BOX_SIZE):
            for box_col in range(0, self.SIZE, self.BOX_SIZE):
                values = []
                for row in range(box_row, box_row + self.BOX_SIZE):
                    for col in range(box_col, box_col + self.BOX_SIZE):
                        if board[row][col] != 0:
                            values.append(board[row][col])
                if len(values) != len(set(values)):
                    return False

        return True

    def is_valid_assignment(self, board: Board, row: int, col: int, value: int) -> bool:
        """Checks whether a value can be placed at board[row][col]."""
        # Row constraint
        if value in board[row]:
            return False

        # Column constraint
        for r in range(self.SIZE):
            if board[r][col] == value:
                return False

        # 3x3 box constraint
        start_row = (row // self.BOX_SIZE) * self.BOX_SIZE
        start_col = (col // self.BOX_SIZE) * self.BOX_SIZE

        for r in range(start_row, start_row + self.BOX_SIZE):
            for c in range(start_col, start_col + self.BOX_SIZE):
                if board[r][c] == value:
                    return False

        return True

    def find_first_empty_cell(self, board: Board) -> Optional[Cell]:
        """Finds the first empty cell in row-major order."""
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                if board[row][col] == 0:
                    return row, col
        return None

    def solve_basic_backtracking(self) -> SolverResult:
        """
        Solves Sudoku using simple backtracking.
        This version always chooses the first empty cell.
        """
        board = self.copy_board(self.original_board)
        self.reset_stats()
        start = perf_counter()

        if not self.is_initial_board_valid(board):
            elapsed = perf_counter() - start
            return SolverResult(
                board,
                SolverStats("Basic Backtracking", False, self.steps, self.assignments, self.backtracks, elapsed),
            )

        solved = self._basic_backtracking(board)
        elapsed = perf_counter() - start

        return SolverResult(
            board,
            SolverStats("Basic Backtracking", solved, self.steps, self.assignments, self.backtracks, elapsed),
        )

    def _basic_backtracking(self, board: Board) -> bool:
        """Recursive helper for basic backtracking."""
        self.steps += 1

        empty_cell = self.find_first_empty_cell(board)
        if empty_cell is None:
            return True

        row, col = empty_cell

        for value in range(1, 10):
            if self.is_valid_assignment(board, row, col, value):
                board[row][col] = value
                self.assignments += 1

                if self._basic_backtracking(board):
                    return True

                board[row][col] = 0
                self.backtracks += 1

        return False

    def get_peers(self, row: int, col: int) -> Set[Cell]:
        """
        Returns all cells that share a row, column, or 3x3 box with the given cell.
        These cells are constrained by the same Sudoku rules.
        """
        peers: Set[Cell] = set()

        # Same row and same column
        for i in range(self.SIZE):
            if i != col:
                peers.add((row, i))
            if i != row:
                peers.add((i, col))

        # Same 3x3 box
        start_row = (row // self.BOX_SIZE) * self.BOX_SIZE
        start_col = (col // self.BOX_SIZE) * self.BOX_SIZE

        for r in range(start_row, start_row + self.BOX_SIZE):
            for c in range(start_col, start_col + self.BOX_SIZE):
                if (r, c) != (row, col):
                    peers.add((r, c))

        return peers

    def get_possible_values(self, board: Board, row: int, col: int) -> Set[int]:
        """Returns all legal values for an empty cell."""
        if board[row][col] != 0:
            return {board[row][col]}

        possible = set(self.VALUES)

        # Remove row values
        possible -= set(board[row])

        # Remove column values
        possible -= {board[r][col] for r in range(self.SIZE)}

        # Remove 3x3 box values
        start_row = (row // self.BOX_SIZE) * self.BOX_SIZE
        start_col = (col // self.BOX_SIZE) * self.BOX_SIZE
        box_values = {
            board[r][c]
            for r in range(start_row, start_row + self.BOX_SIZE)
            for c in range(start_col, start_col + self.BOX_SIZE)
        }
        possible -= box_values

        # 0 is not a valid Sudoku value
        possible.discard(0)
        return possible

    def initialize_domains(self, board: Board) -> Optional[Domains]:
        """
        Creates initial domains for all empty cells.
        If any empty cell has no possible value, the puzzle is unsolvable.
        """
        domains: Domains = {}

        for row in range(self.SIZE):
            for col in range(self.SIZE):
                if board[row][col] == 0:
                    values = self.get_possible_values(board, row, col)
                    if not values:
                        return None
                    domains[(row, col)] = values

        return domains

    def select_mrv_cell(self, domains: Domains) -> Cell:
        """
        MRV heuristic: selects the empty cell with the fewest remaining legal values.
        This reduces the branching factor of the search.
        """
        return min(domains, key=lambda cell: len(domains[cell]))

    def order_values_lcv(self, cell: Cell, domains: Domains) -> List[int]:
        """
        LCV heuristic: tries values that eliminate the fewest options for neighboring cells first.
        This is optional but improves the optimized solver.
        """
        row, col = cell

        def elimination_count(value: int) -> int:
            count = 0
            for peer in self.get_peers(row, col):
                if peer in domains and value in domains[peer]:
                    count += 1
            return count

        return sorted(domains[cell], key=elimination_count)

    def forward_check(self, domains: Domains, cell: Cell, value: int) -> Optional[Domains]:
        """
        Performs forward checking after assigning a value to a cell.

        The assigned value is removed from all peer domains.
        If any peer domain becomes empty, this assignment leads to failure.
        """
        row, col = cell
        new_domains: Domains = copy.deepcopy(domains)

        # The assigned cell is no longer unassigned
        new_domains.pop(cell, None)

        for peer in self.get_peers(row, col):
            if peer in new_domains and value in new_domains[peer]:
                new_domains[peer].remove(value)

                # Failure detected early
                if len(new_domains[peer]) == 0:
                    return None

        return new_domains

    def solve_optimized_csp(self) -> SolverResult:
        """
        Solves Sudoku using:
        - Backtracking
        - MRV heuristic
        - Forward checking
        - LCV value ordering
        """
        board = self.copy_board(self.original_board)
        self.reset_stats()
        start = perf_counter()

        if not self.is_initial_board_valid(board):
            elapsed = perf_counter() - start
            return SolverResult(
                board,
                SolverStats("CSP: MRV + Forward Checking + LCV", False, self.steps, self.assignments, self.backtracks, elapsed),
            )

        domains = self.initialize_domains(board)
        if domains is None:
            elapsed = perf_counter() - start
            return SolverResult(
                board,
                SolverStats("CSP: MRV + Forward Checking + LCV", False, self.steps, self.assignments, self.backtracks, elapsed),
            )

        solved = self._optimized_backtracking(board, domains)
        elapsed = perf_counter() - start

        return SolverResult(
            board,
            SolverStats("CSP: MRV + Forward Checking + LCV", solved, self.steps, self.assignments, self.backtracks, elapsed),
        )

    def _optimized_backtracking(self, board: Board, domains: Domains) -> bool:
        """Recursive helper for optimized CSP backtracking."""
        self.steps += 1

        if not domains:
            return True

        cell = self.select_mrv_cell(domains)
        row, col = cell

        for value in self.order_values_lcv(cell, domains):
            if self.is_valid_assignment(board, row, col, value):
                board[row][col] = value
                self.assignments += 1

                updated_domains = self.forward_check(domains, cell, value)

                if updated_domains is not None and self._optimized_backtracking(board, updated_domains):
                    return True

                board[row][col] = 0
                self.backtracks += 1

        return False
