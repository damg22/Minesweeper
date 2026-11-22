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
crossed-out mine on every flag that was wrong.
When status is WON, every mine is drawn as a flag.

The timer starts when status becomes PLAYING and stops on WON or LOST.
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
    adjacent_mines: int = 0           # 0-8, number of mines in the 8 neighbours
    state: CellState = CellState.HIDDEN
    exploded: bool = False            # True only for the mine the player clicked


class Game:
    def __init__(self, rows: int, cols: int, mines: int):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.status = GameStatus.READY
        # An empty board, all hidden, no mines yet, so the UI has something to draw.
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]

        # TODO: decide when and how mines get placed (now, or on the first
        #       click so the first click is always safe), then compute
        #       adjacent_mines for every cell.

    # ------------------------------------------------------------------ state
    def cell(self, row: int, col: int) -> Cell:
        """Return the Cell at (row, col). The UI calls this for every cell, every frame."""
        return self.grid[row][col]

    def flags_remaining(self) -> int:
        """Number shown on the left red counter (it can go negative)."""
        # TODO: mines minus the number of flags placed
        return self.mines

    # ---------------------------------------------------------------- actions
    def reveal(self, row: int, col: int) -> None:
        """Called on left-click release over a cell."""
        # TODO:
        #  - ignore clicks when the game is over, or the cell is flagged / already revealed
        #  - switch status from READY to PLAYING on the first click
        #  - mine -> mark it exploded, status = LOST
        #  - zero -> flood-reveal its neighbours
        #  - check for a win
        pass

    def toggle_flag(self, row: int, col: int) -> None:
        """Called on right-click (or Ctrl/Cmd + left-click) over a cell."""
        # TODO: cycle HIDDEN -> FLAGGED -> QUESTION -> HIDDEN (or skip QUESTION).
        #       Ignore revealed cells.
        pass

    def chord(self, row: int, col: int) -> None:
        """Called on left+right, middle, or Shift + left-click release over a cell."""
        # TODO: if the cell is a revealed number and exactly that many flags
        #       surround it, reveal all of its other hidden neighbours.
        pass
