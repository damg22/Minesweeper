"""
Minesweeper game logic. THIS FILE IS YOURS TO WRITE.

The UI (ui.py) never changes game state itself. It only:
  1. reads state:   game.rows, game.cols, game.mines, game.status,
                    game.cell(row, col), game.flags_remaining()
  2. calls actions: game.reveal(r, c), game.toggle_flag(r, c), game.chord(r, c)
and redraws the board from whatever state you leave behind.

The data types below (CellState, GameStatus, Cell) are the "contract" the UI
renders from. Add any fields and helper methods you like, but keep the names
the UI and the tests use.

How the UI draws each cell:
  HIDDEN               -> raised grey tile
  FLAGGED              -> raised tile with a red flag
  QUESTION             -> raised tile with a "?"
  REVEALED, not mine   -> sunken tile showing adjacent_mines (blank when 0)
  REVEALED, mine       -> mine; on a red background if cell.exploded is True
When status is LOST, the UI also shows every un-flagged mine and puts a red X
over every wrong flag. When status is WON, every mine is drawn as a flag.
The timer starts when status becomes PLAYING and stops on WON or LOST.

Run the tests for each milestone with:  pytest tests/test_1_setup.py  (etc.)
"""

from dataclasses import dataclass
from enum import Enum, auto


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
    adjacent_mines: int = 0           # 0-8: mines in the 8 surrounding cells
    state: CellState = CellState.HIDDEN
    exploded: bool = False            # True only for the mine the player clicked


class Game:
    def __init__(self, rows: int, cols: int, mines: int):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.status = GameStatus.READY
        self.mines_placed = False
        # An empty board, all hidden, no mines yet, so the UI has something to draw.
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]

    def cell(self, row: int, col: int) -> Cell:
        """Return the Cell at (row, col). The UI calls this for every cell, every frame."""
        return self.grid[row][col]

    # ===================================================== Milestone 1: setup
    def set_mines(self, positions) -> None:
        """Put a mine on every (row, col) in `positions`, then compute
        adjacent_mines for EVERY cell: the number of mines among its 8
        neighbours (diagonals included). Finally set self.mines_placed = True.

        The tests call this directly to build known boards."""
        # TODO
        pass

    def place_mines(self, safe_row: int, safe_col: int) -> None:
        """Choose self.mines random, distinct positions that never include
        (safe_row, safe_col), then hand them to set_mines().
        Hint: random.sample() picks distinct items from a list."""
        # TODO
        pass

    # ==================================================== Milestone 2: reveal
    def reveal(self, row: int, col: int) -> None:
        """Called on left-click release over a cell.

        - Do nothing if the game is WON or LOST, or the cell is FLAGGED or
          already REVEALED. (A QUESTION cell can be revealed.)
        - On the first reveal: if mines aren't placed yet, call
          place_mines(row, col), then set status to PLAYING.
        - A mine: mark it exploded, status becomes LOST.
        - A number: reveal just that cell.
        - A zero: flood-reveal. Open every connected zero and the numbers
          bordering them, in all 8 directions. Never open flagged cells.
        - After revealing, check for a win (Milestone 4)."""
        # TODO
        pass

    # ===================================================== Milestone 3: flags
    def toggle_flag(self, row: int, col: int) -> None:
        """Called on right-click. Cycle HIDDEN -> FLAGGED -> QUESTION -> HIDDEN.
        Do nothing on REVEALED cells or when the game is over."""
        # TODO
        pass

    def flags_remaining(self) -> int:
        """Shown on the left red counter: mines minus flags placed.
        It goes negative if the player places too many flags."""
        # TODO
        return self.mines

    # ============================================ Milestone 4: win and chord
    def chord(self, row: int, col: int) -> None:
        """Called on left+right click. If (row, col) is a REVEALED number and
        exactly that many neighbours are FLAGGED, reveal every other
        non-flagged neighbour (which can hit a mine if a flag was wrong).
        Otherwise do nothing."""
        # TODO
        pass

    # Win rule: the game is WON as soon as every non-mine cell is REVEALED.
    # Flags are not required. Where you check it is up to you.
