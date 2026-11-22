"""Milestone 2: revealing cells and flood fill."""

from minesweeper.game import CellState, Game, GameStatus

H, R = CellState.HIDDEN, CellState.REVEALED


def states(g):
    return [[g.cell(r, c).state for c in range(g.cols)] for r in range(g.rows)]


def test_first_reveal_places_mines_and_starts_playing():
    g = Game(9, 9, 10)
    g.reveal(4, 4)
    assert g.mines_placed, "the first reveal should place the mines"
    assert g.status == GameStatus.PLAYING
    assert g.cell(4, 4).state == R
    assert not g.cell(4, 4).is_mine


def test_first_reveal_keeps_mines_already_set(board):
    g = board("*....",
              ".....",
              ".....")
    g.reveal(2, 4)
    assert g.cell(0, 0).is_mine, "don't re-place mines if set_mines() was already called"
    assert sum(g.cell(r, c).is_mine for r in range(3) for c in range(5)) == 1


def test_reveal_number_opens_only_that_cell(board):
    g = board("*..",
              "...",
              "...")
    g.reveal(0, 1)
    assert g.cell(0, 1).state == R
    revealed = sum(s == R for row in states(g) for s in row)
    assert revealed == 1


def test_reveal_mine_loses_and_explodes(board):
    g = board("*..",
              "...",
              "...")
    g.reveal(0, 0)          # set_mines() already ran, so this click can hit a mine
    assert g.status == GameStatus.LOST
    assert g.cell(0, 0).exploded


def test_flood_fill_opens_zeros_and_their_border(board):
    g = board(".....",
              ".....",
              ".....",
              "....*")
    g.reveal(0, 0)
    for r in range(4):
        for c in range(5):
            if (r, c) != (3, 4):
                assert g.cell(r, c).state == R, f"{(r, c)} should be opened by the flood fill"
    assert g.cell(3, 4).state == H


def test_flood_fill_goes_diagonally(board):
    # (0,0) is a zero. Its diagonal neighbour (1,1) is a number that can only
    # be reached diagonally, so a 4-direction flood fill would miss it.
    g = board("..*",
              "...",
              "*..")
    g.reveal(0, 0)
    assert g.cell(1, 1).state == R, "a zero opens all 8 neighbours, including diagonals"


def test_flood_fill_stops_at_numbers(board):
    g = board("....",
              "....",
              "**.*",
              "....")
    g.reveal(0, 0)
    assert g.cell(1, 3).state == R, "numbers bordering the zeros are opened"
    assert g.cell(2, 2).state == H, "flood fill must not continue past numbered cells"
    assert g.cell(3, 0).state == H


def test_flood_fill_skips_flags(board):
    g = board("....",
              "....",
              "...*")
    g.toggle_flag(0, 3)
    g.reveal(0, 0)
    assert g.cell(0, 3).state == CellState.FLAGGED, "flagged cells stay flagged"


def test_reveal_flagged_cell_does_nothing(board):
    g = board("*..",
              "...",
              "...")
    g.toggle_flag(0, 0)
    g.reveal(0, 0)
    assert g.status != GameStatus.LOST
    assert g.cell(0, 0).state == CellState.FLAGGED


def test_no_reveals_after_game_over(board):
    g = board("*..",
              "...",
              "...")
    g.reveal(0, 0)
    assert g.status == GameStatus.LOST
    before = states(g)
    g.reveal(0, 2)
    assert states(g) == before
