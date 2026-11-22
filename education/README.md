# Minesweeper for the classroom

A ready-to-use programming assignment: students get a complete, working
Minesweeper interface (Python + pygame) and write the game logic themselves,
guided by milestones and an automated test suite.

**[Download the starter kit (`minesweeper-starter.zip`)](https://github.com/damg22/Minesweeper/releases/latest/download/minesweeper-starter.zip)**

Free to use, change and redistribute under the MIT license. No sign-up needed.

## Why this assignment

Students build something they actually want to play, and see every change
immediately. Meanwhile, the work covers core CS1/CS2 topics:

- **2D grids:** indexing, bounds checking, iterating over neighbours
- **Graph search:** the flood fill is breadth- or depth-first search, with a visited set
- **State machines:** game status (ready → playing → won/lost) and the cell cycle (hidden → flagged → question)
- **Randomness with constraints:** placing mines while keeping the first click safe
- **Separation of concerns:** the UI only reads state and calls methods, so the logic is pure and testable
- **Reading a spec and tests:** each milestone is defined by docstrings plus pytest tests
- **Python features:** classes, `Enum`, `@dataclass`, generators

**Level:** late CS1 or CS2. Students should know functions, loops, lists and
basic classes.
**Time:** roughly 4–8 hours of student work, depending on experience and how
many extensions they take on.

## What's in the kit

```
minesweeper-starter/
├── README.md               student handout: setup, rules, milestones, tips
├── main.py                 run the game:  python main.py   (--preview shows every tile type)
├── minesweeper/
│   ├── game.py             ← THE ASSIGNMENT: classes and empty methods with detailed docstrings
│   ├── ui.py               finished window, input and rendering
│   ├── graphics.py         finished tile, counter and smiley drawing
│   ├── settings.py         sizes, colours, difficulties
│   └── preview.py          hard-coded demo board
├── tests/
│   ├── conftest.py         board("*..", "...") helper for building known boards
│   ├── test_1_setup.py     milestone 1: placing mines, counting neighbours (9 tests)
│   ├── test_2_reveal.py    milestone 2: reveal and flood fill (10 tests)
│   ├── test_3_flags.py     milestone 3: flags, question marks, counter (6 tests)
│   └── test_4_win_chord.py milestone 4: winning and chording (7 tests)
├── requirements.txt        pygame, pytest
└── pytest.ini
```

The handout is the kit's `README.md`. You can also
[read it on GitHub](STUDENT_README.md).

## Running it in your course

**Option A: share the zip.** Post `minesweeper-starter.zip` on your LMS.
Students unzip it, follow the setup in the handout, and submit their
`minesweeper/game.py`.

**Option B: GitHub Classroom.** Unzip the kit into a new repository, mark it as
a *template repository*, and create an assignment from it. To add autograding,
create one test per milestone that runs, for example:

```
pip install -r requirements.txt && pytest tests/test_1_setup.py
```

The game window isn't needed for grading. All tests run headless.

## Grading

The tests check behaviour, not implementation details, so any reasonable
design passes. One possible split:

| Milestone | Tests | Points |
|---|---|---|
| 1. Setup | `test_1_setup.py` | 25 |
| 2. Reveal and flood fill | `test_2_reveal.py` | 35 |
| 3. Flags | `test_3_flags.py` | 15 |
| 4. Win and chord | `test_4_win_chord.py` | 25 |

Points per file can be scaled by the fraction of passing tests
(`pytest --tb=no -q` prints a summary). It's worth adding a few manual points
for code quality, e.g. a neighbours helper instead of eight copy-pasted
bounds checks.

## Making it yours

- **Change the rules:** edit the docstrings in `minesweeper/game.py` and the
  matching tests. For example, drop question marks, or require all mines to be
  flagged to win.
- **Make it easier:** give students a working neighbours helper, or provide
  `set_mines` and start at milestone 2.
- **Make it harder:** remove the docstrings and ask students to derive the
  rules from playing `--preview` and reading the tests, or assign the
  extensions listed in the handout.
- **Rebuild the zip** after editing: `python education/build_starter.py` from
  the repository root writes `dist/minesweeper-starter.zip`.

## Academic integrity

This repository's own `minesweeper/game.py` is a working implementation.
It's public, so students could find it, although its rules differ from the
assignment in a few places, so it won't pass the tests unchanged. If that
matters for your course, change the rules (see above) so that copied code
fails, and ask students to explain their flood fill in a short write-up or
code review.

## Feedback

Found a bug in the kit or the tests, or have a suggestion from using it in
class? [Open an issue](https://github.com/damg22/Minesweeper/issues).
