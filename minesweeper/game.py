"""
Minesweeper game logic. THIS FILE IS YOURS TO WRITE.

The UI (ui.py) never changes game state itself. It only:
  1. reads state:   game.rows, game.cols, game.mines, game.status,
                    game.cell(row, col), game.flags_remaining()
  2. calls actions: game.reveal(r, c), game.toggle_flag(r, c), game.chord(r, c)
and redraws the board from whatever state you leave behind.

The data types below (CellState, GameStatus, Cell) are the "contract" the UI
renders from. You can add fields and helper methods anywhere you like, but keep
the names the UI uses (listed above) so the UI keeps working.

How the UI draws each cell:
  HIDDEN               -> raised grey tile
  FLAGGED              -> raised tile with a red flag
  QUESTION             -> raised tile with a "?"
  REVEALED, not mine   -> sunken tile showing adjacent_mines (blank when 0)
  REVEALED, mine       -> mine; on a red background if cell.exploded is True
When status is LOST, the UI also shows every un-flagged mine and draws a
red X over every flag that was wrong (a flag on a cell with no mine).
When status is WON, every mine is drawn as a flag.

The timer starts when status becomes PLAYING and stops on WON or LOST.
"""

import random
from collections import deque
from dataclasses import dataclass
from enum import Enum, auto
from sre_parse import State


class CellState(Enum):
    HIDDEN = auto()
    REVEALED = auto()
    FLAGGED = auto()
    QUESTION = auto()


class GameStatus(Enum):
    READY = auto()     # new board, no click yet (timer shows 000)
    PLAYING = auto()   # timer running
    WON = auto()
    LOST = auto()


@dataclass
class Cell:
    is_mine: bool = False
    adjacent_mines: int = 0           # 0-8, number of mines in the 8 neighbours
    state: CellState = CellState.HIDDEN
    exploded: bool = False            # True only for the mine the player clicked


class Game:
    def __init__(self, rows: int, cols: int, mines: int):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.flags = mines
        self.unflagged_mines: int = mines
        self.status = GameStatus.READY
        # An empty board, all hidden, no mines yet, so the UI has something to draw.
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]

        # Mines are placed lazily on the first reveal (see place_mines) so the
        # first click is always safe.

    # ------------------------------------------------------------ mine setup
    def place_mines(self, safe_row: int, safe_col: int) -> None:
        """Scatter mines randomly, keeping (safe_row, safe_col) and, when the
        board has room, its 8 neighbours mine-free so the first click opens
        an area. Then fill in adjacent_mines for every cell."""
        all_cells = [(r, c) for r in range(self.rows) for c in range(self.cols)]

        safe = {(r, c) for r, c in self._around(safe_row, safe_col)}
        candidates = [pos for pos in all_cells if pos not in safe]
        if len(candidates) < self.mines:
            # Board too crowded for a safe 3x3, so only guarantee the clicked cell.
            candidates = [pos for pos in all_cells if pos != (safe_row, safe_col)]

        for r, c in random.sample(candidates, self.mines):
            self.grid[r][c].is_mine = True

        for r, c in all_cells:
            self.grid[r][c].adjacent_mines = sum(
                self.grid[nr][nc].is_mine
                for nr, nc in self._around(r, c)
                if (nr, nc) != (r, c)
            )

    def _around(self, row: int, col: int):
        """Yield (row, col) itself and every in-bounds neighbour."""
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    yield nr, nc

    # ------------------------------------------------------------------ state
    def cell(self, row: int, col: int) -> Cell:
        """Return the Cell at (row, col). The UI calls this for every cell, every frame."""
        return self.grid[row][col]

    def flags_remaining(self) -> int:
        """Number shown on the left red counter (it can go negative)."""
        # TODO: mines minus the number of flags placed
        return self.flags

    # ---------------------------------------------------------------- actions
    def reveal(self, row: int, col: int) -> None:
        """Called on left-click release over a cell."""
        # TODO:
        #  - ignore clicks when the game is over, or the cell is flagged / already revealed
        #  - switch status from READY to PLAYING on the first click
        #  - mine -> mark it exploded, status = LOST
        #  - zero -> flood-reveal its neighbours
        #  - check for a win

        # Update game state
        if self.status == GameStatus.LOST:
            return
        if self.status == GameStatus.READY:
            self.place_mines(row, col)
            self.status = GameStatus.PLAYING

        cell: Cell = self.grid[row][col]

        # Manage cell state
        if cell.state != CellState.FLAGGED:
            if cell.is_mine:
                cell.exploded = True
                self.status = GameStatus.LOST
                return

            if cell.adjacent_mines == 0:
                self.flood_reveal(row, col)
            else:
                cell.state = CellState.REVEALED

        self.check_win()
        return

    def hidden_safe_cells(self) -> int:
        """Number of non-mine cells the player still hasn't revealed."""
        return sum(
            not cell.is_mine and cell.state != CellState.REVEALED
            for row in self.grid
            for cell in row
        )

    def check_win(self) -> None:
        """Win once every mine is flagged and no safe cell is left hidden."""
        if self.status != GameStatus.PLAYING:
            return
        if self.unflagged_mines == 0 and self.hidden_safe_cells() == 0:
            self.status = GameStatus.WON

    # reveal neighbhoring cells as long as int is 0
    def flood_reveal(self, row: int, col: int) -> None:
        neighbors: deque[tuple[int, int]] = deque()
        neighbors.append((row, col))
        visited: set[tuple[int,int]] = set()

        while len(neighbors) > 0:
            row_i, col_i = neighbors.pop()

            if not self.in_bounds(row_i, col_i) or (row_i, col_i) in visited:
                continue

            visited.add((row_i, col_i))
            cell: Cell = self.grid[row_i][col_i]

            if cell.is_mine == False and cell.state == CellState.HIDDEN:
                cell.state = CellState.REVEALED
            if cell.adjacent_mines == 0 and cell.state == CellState.REVEALED:
                neighbors.append((row_i, col_i + 1))
                neighbors.append((row_i, col_i - 1))
                neighbors.append((row_i - 1, col_i))
                neighbors.append((row_i + 1, col_i))

    def in_bounds(self, row: int, col: int) -> bool:
        return row >= 0 and row < len(self.grid) and col >= 0 and col < len(self.grid[row])
            

    def toggle_flag(self, row: int, col: int) -> None:
        """Called on right-click (or Ctrl/Cmd + left-click) over a cell."""
        # TODO: cycle HIDDEN -> FLAGGED -> QUESTION -> HIDDEN (or skip QUESTION).
        #       Ignore revealed cells.

        cell: Cell = self.grid[row][col]


        if cell.state == CellState.FLAGGED:
            cell.state = CellState.HIDDEN
            self.flags += 1
            if cell.is_mine:
                self.unflagged_mines += 1
        elif cell.state == CellState.HIDDEN and self.flags > 0:
            self.flags -= 1
            cell.state = CellState.FLAGGED
            if cell.is_mine:
                self.unflagged_mines -= 1

        # Flagging the last mine can be the winning move.
        self.check_win()
        return

    def chord(self, row: int, col: int) -> None:
        """Called on left+right, middle, or Shift + left-click release over a cell."""
        # TODO: if the cell is a revealed number and exactly that many flags
        #       surround it, reveal all of its other hidden neighbours.
        pass
