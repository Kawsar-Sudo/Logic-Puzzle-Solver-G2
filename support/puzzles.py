"""Loads sample Sudoku puzzle data for the CSP solver.

The actual puzzle dataset is stored in data/sudoku_puzzles.json so that
project data stays separate from source code.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

Board = List[List[int]]

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "sudoku_puzzles.json"


def load_puzzles() -> Dict[str, Board]:
    """Loads sample Sudoku puzzles from the data folder."""
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


PUZZLES = load_puzzles()
