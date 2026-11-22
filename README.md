# Minesweeper

A classic-style Minesweeper in Python + pygame. The UI is done; the game logic in
`minesweeper/game.py` is for you to write.

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Run

```bash
.venv/bin/python main.py                       # beginner 9x9, 10 mines
.venv/bin/python main.py -d expert             # beginner | intermediate | expert
.venv/bin/python main.py --custom 20 24 80     # rows cols mines
.venv/bin/python main.py --preview             # sample board showing every tile type
```

## Controls

| Input                                   | Action                         |
|-----------------------------------------|--------------------------------|
| Left click                              | reveal                         |
| Right click / Ctrl+click / Cmd+click    | flag / question mark           |
| Left+Right, middle click, Shift+click   | chord                          |
| Smiley, `F2`, `N`                       | new game                       |
| `1` / `2` / `3` or the menu bar         | beginner / intermediate / expert |
| `Esc`                                   | quit                           |

## Layout

```
main.py                  entry point / CLI flags
minesweeper/
  game.py                YOUR CODE: Cell, CellState, GameStatus, Game (stubs with TODOs)
  ui.py                  window, input, rendering (reads Game state, calls Game actions)
  graphics.py            tile / mine / flag / LED / smiley drawing
  settings.py            sizes, colours, difficulty presets
  preview.py             hard-coded demo board used by --preview
```

## What the UI expects from `Game`

- `Game(rows, cols, mines)`
- attributes: `rows`, `cols`, `mines`, `status` (a `GameStatus`)
- `cell(r, c)` returns a `Cell` with `is_mine`, `adjacent_mines`, `state`, `exploded`
- `flags_remaining()` returns the number for the left counter
- `reveal(r, c)`, `toggle_flag(r, c)`, `chord(r, c)` change the state

The timer starts when `status` becomes `PLAYING` and stops on `WON` or `LOST`.
On `LOST` the UI shows all mines and crosses out wrong flags. On `WON` it shows
every mine as a flag. Your logic only needs to set the state.
