# Minesweeper

A classic-style Minesweeper in Python + pygame.

**[▶ Play it in your browser](https://damg22.github.io/Minesweeper/play/)** · or download it for
Windows and Mac, no Python needed · **[Website](https://damg22.github.io/Minesweeper/)**

<img src="docs/images/demo.gif" width="296" alt="Minesweeper being played: the first click opens an area, then flags are placed until the board is cleared.">

## Download and play (no Python needed)

Grab the latest build from the **[Releases page](https://github.com/damg22/Minesweeper/releases/latest)**:

| System                               | File                                  |
| ------------------------------------ | ------------------------------------- |
| Windows                              | `Minesweeper-windows.exe`             |
| Mac with Apple Silicon (M1 or newer) | `Minesweeper-macos-apple-silicon.zip` |
| Intel Mac                            | `Minesweeper-macos-intel.zip`         |

The apps aren't code-signed, so the first launch shows a warning:

- **Windows:** on the "Windows protected your PC" screen, click **More info → Run anyway**.
- **Mac:** unzip, then right-click `Minesweeper.app` → **Open** → **Open**. If macOS still
  blocks it, go to **System Settings → Privacy & Security** and click **Open Anyway**.

## For teachers: use it as an assignment / fun learning project

Minesweeper makes a great CS1/CS2 project: grids, flood fill (graph search),
state machines and testing, in a game students want to finish. The
**[starter kit](https://github.com/damg22/Minesweeper/releases/latest/download/minesweeper-starter.zip)**
gives students this complete UI with an empty `game.py` to fill in, guided by
four milestones and 32 automated tests (also usable for autograding).

- **[Instructor guide](education/README.md):** learning goals, how to hand it out
  (zip or GitHub Classroom), grading, and how to customise it
- **[Student handout](education/STUDENT_README.md):** setup, rules, milestones and tips

Free to use and adapt under the MIT license.

## Run from source

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Then:

```bash
.venv/bin/python main.py                       # beginner 9x9, 10 mines
.venv/bin/python main.py -d expert             # beginner | intermediate | expert
.venv/bin/python main.py --custom 20 24 80     # rows cols mines
.venv/bin/python main.py --preview             # sample board showing every tile type
```

## Controls

| Input                                 | Action                           |
| ------------------------------------- | -------------------------------- |
| Left click                            | reveal                           |
| Right click / Ctrl+click / Cmd+click  | flag / question mark             |
| Left+Right, middle click, Shift+click | chord                            |
| Smiley, `F2`, `N`                     | new game                         |
| `1` / `2` / `3` or the menu bar       | beginner / intermediate / expert |
| `Esc`                                 | quit                             |

## Layout

```
main.py                  entry point / CLI flags
minesweeper/
  game.py                game rules: Cell, CellState, GameStatus, Game
  ui.py                  window, input, rendering (reads Game state, calls Game actions)
  graphics.py            tile / mine / flag / LED / smiley drawing
  settings.py            sizes, colours, difficulty presets
  preview.py             hard-coded demo board used by --preview
education/
  README.md              instructor guide
  STUDENT_README.md      student handout (becomes the kit's README)
  game_stub.py           the empty game.py students start from
  tests/                 milestone tests (pytest)
  build_starter.py       builds dist/minesweeper-starter.zip
docs/                    GitHub Pages website
tools/make_screenshots.py  regenerates the website images from real games
tools/build_web.py       builds the browser version with pygbag (WebAssembly)
```

## What the UI expects from `Game`

- `Game(rows, cols, mines)`
- attributes: `rows`, `cols`, `mines`, `status` (a `GameStatus`)
- `cell(r, c)` returns a `Cell` with `is_mine`, `adjacent_mines`, `state`, `exploded`
- `flags_remaining()` returns the number for the left counter
- `reveal(r, c)`, `toggle_flag(r, c)`, `chord(r, c)` change the state

The timer starts when `status` becomes `PLAYING` and stops on `WON` or `LOST`.
On `LOST` the UI shows all mines and crosses out wrong flags. On `WON` it shows
every mine as a flag. The logic only needs to set the state.

## The website and browser version

`.github/workflows/pages.yml` publishes the site on every push to `main`: the
pages in `docs/`, plus the browser build of the game at `/play/`. It's made by
[pygbag](https://pypi.org/project/pygbag/), which runs pygame on WebAssembly.
One-time setup: **Settings → Pages → Source: GitHub Actions**.

To try the browser version locally:

```bash
.venv/bin/pip install pygbag==0.9.3
.venv/bin/python tools/build_web.py --serve      # then open http://localhost:8000
```

Two things the browser build relies on: `main.py` runs an async loop
(`App.run_async`) so the page stays responsive, and it imports `pygame` directly,
which is how pygbag knows to load it.

## Publishing a new release

GitHub Actions (`.github/workflows/build.yml`) builds the Windows and Mac apps and the
classroom starter kit on every push; the files show up under each run's **Artifacts**
on the Actions tab.

To publish a release that anyone can download, push a version tag:

```bash
git tag v1.0.0
git push origin v1.0.0
```

About 5 minutes later the Releases page has all four downloads attached: the three apps
and `minesweeper-starter.zip`.
