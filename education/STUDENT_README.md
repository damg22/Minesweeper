# Minesweeper: write the game logic

You're getting a complete, working Minesweeper interface: the window, the tiles,
the counters, the smiley and all the mouse handling. What's missing is the game
itself. Your job is to write the logic in **`minesweeper/game.py`** that makes it
a real game.

When you're done, you'll have a Minesweeper you can actually play, and a test
suite that proves it follows the rules.

## Setup

You need Python 3.9 to 3.13.

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell)**
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## See what you're building

```bash
python main.py --preview
```

This opens a fake, hard-coded board that shows every kind of tile: numbers,
flags, question marks, mines, the exploded mine, and wrong flags. Your code
will produce all of these.

```bash
python main.py
```

This runs the real game with your code. At first nothing happens when you click.
That's expected, because the methods in `game.py` are empty.

## How the code is organized

| File | What it does | Do you edit it? |
|---|---|---|
| `minesweeper/game.py` | The rules: mines, numbers, revealing, flags, winning | **Yes, this is the assignment** |
| `minesweeper/ui.py` | Window, mouse and keyboard, drawing the board | No |
| `minesweeper/graphics.py` | How each tile, the counters and the smiley look | No |
| `minesweeper/settings.py` | Sizes, colours, difficulty levels | Only if you want to |
| `tests/` | Automated checks for each milestone | No |

The UI and your code talk through a small "contract". The UI **reads**
`game.status`, `game.cell(r, c)` and `game.flags_remaining()`, and **calls**
`game.reveal(r, c)`, `game.toggle_flag(r, c)` and `game.chord(r, c)` when the
player clicks. It never changes the board itself; it just redraws whatever
state you leave behind. Keeping the rules separate from the display like this
is a common way to structure programs, and it's what makes the rules testable.

## The rules

- The board is a grid. Some cells hide mines.
- Every safe cell shows a number: how many of its **8 neighbours** (up, down,
  left, right and the 4 diagonals) are mines. Zero is shown as a blank.
- **Revealing** a mine loses the game. **The first click is always safe**: mines
  are placed only after it, avoiding the clicked cell.
- Revealing a **zero** automatically opens all of its neighbours. Any of those
  that are also zeros open theirs, and so on (a *flood fill*).
- **Right-click** cycles a hidden cell through flag → question mark → hidden.
  Flags protect a cell from being revealed by accident.
- **Chording:** clicking a revealed number whose neighbours already hold exactly
  that many flags reveals all of its other neighbours.
- You **win** when every safe cell is revealed. Flags aren't required.

Each method in `game.py` has a docstring with the exact behaviour expected.

## Milestones

Work through these in order. Each has its own test file, so you can check one
step before starting the next.

| # | Methods | Check with |
|---|---|---|
| 1 | `set_mines`, `place_mines` | `pytest tests/test_1_setup.py` |
| 2 | `reveal` (including the flood fill) | `pytest tests/test_2_reveal.py` |
| 3 | `toggle_flag`, `flags_remaining` | `pytest tests/test_3_flags.py` |
| 4 | winning, `chord` | `pytest tests/test_4_win_chord.py` |

Run everything with `pytest`. Play the game with `python main.py` after every
milestone. Seeing the board react is often the fastest way to spot a bug.

Useful pytest options:
- `pytest -x` stops at the first failure.
- `pytest -k diagonal` runs only the tests with "diagonal" in their name.
- Failure messages explain what was expected. Read them!

## Tips

- **Write a neighbours helper first.** Almost every method needs "the in-bounds
  cells around (r, c)". Writing it once (a generator with `yield` works nicely)
  saves you from repeating boundary checks everywhere. Corners have 3
  neighbours and edges have 5.
- **Flood fill** is graph search. Use a list as a stack (or `collections.deque`
  as a queue) of cells to visit, plus a set of cells already seen. Recursion
  also works, but large empty boards can hit Python's recursion limit.
- **Test on tiny boards.** The tests draw boards as text, like
  `board("*..", "...", "..*")`. Look at `tests/conftest.py` and write your own
  small cases when something confuses you.
- **Keep the state consistent.** If you track counts (flags placed, cells
  revealed), update them everywhere the state changes, or compute them from
  the grid when needed.

## Going further

Finished early? Some ideas, roughly easiest first:

1. **Bigger safe start:** keep the clicked cell *and its 8 neighbours* free of
   mines, so the first click always opens an area (fall back to just the cell
   on crowded boards).
2. **Best times:** save the fastest win per difficulty to a file and print it.
3. **Hint key:** add a method that returns a cell that is provably safe from
   the visible numbers (then wire up a key in `ui.py`).
4. **No-guess boards:** only generate boards that can be solved by logic alone.
   This is hard, and a great one for experimenting with solvers.

Some extensions change the rules the tests check. If so, explain what you
changed and why.

## Controls

| Input | Action |
|---|---|
| Left click | reveal |
| Right click / Ctrl+click / Cmd+click | flag / question mark |
| Left+Right, middle click, Shift+click | chord |
| Smiley, `F2`, `N` | new game |
| `1` / `2` / `3` | beginner / intermediate / expert |
| `Esc` | quit |
