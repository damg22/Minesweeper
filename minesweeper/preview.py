"""
A fake, hard-coded board that shows every tile type. Run: python main.py --preview
It uses the same Cell/CellState/GameStatus types as game.py, but has no rules at all.
"""

from .game import Cell, CellState, GameStatus

# Legend:
#   0-8  revealed number      .  hidden
#   F    flag on a mine       W  flag on a non-mine (shown crossed out)
#   ?    question mark        M  hidden mine (shown because the game is LOST)
#   X    exploded mine
LAYOUT = [
    "012345678",
    "1.......M",
    "F?W.....?",
    "1....M...",
    "2..X.....",
    "M...F....",
    "...W....F",
    "?........",
    "M...M...M",
]


class PreviewGame:
    def __init__(self, *_ignored):
        self.rows, self.cols = len(LAYOUT), len(LAYOUT[0])
        self.status = GameStatus.LOST
        self.grid = []
        for line in LAYOUT:
            row = []
            for ch in line:
                cell = Cell()
                if ch.isdigit():
                    cell.state, cell.adjacent_mines = CellState.REVEALED, int(ch)
                elif ch == "F":
                    cell.state, cell.is_mine = CellState.FLAGGED, True
                elif ch == "W":
                    cell.state = CellState.FLAGGED
                elif ch == "?":
                    cell.state = CellState.QUESTION
                elif ch == "M":
                    cell.is_mine = True
                elif ch == "X":
                    cell.is_mine = cell.exploded = True
                    cell.state = CellState.REVEALED
                row.append(cell)
            self.grid.append(row)
        self.mines = sum(c.is_mine for row in self.grid for c in row)

    def cell(self, r, c):
        return self.grid[r][c]

    def flags_remaining(self):
        return self.mines - sum(c.state == CellState.FLAGGED for row in self.grid for c in row)

    def reveal(self, r, c):
        pass

    def toggle_flag(self, r, c):
        pass

    def chord(self, r, c):
        pass
