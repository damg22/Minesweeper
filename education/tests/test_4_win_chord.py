"""Milestone 4: winning and chording."""

from minesweeper.game import CellState, GameStatus


def test_win_when_every_safe_cell_is_revealed(board):
    g = board("*..",
              "...",
              "...")
    g.reveal(2, 2)                 # flood fill opens everything except the mine
    assert g.status == GameStatus.WON, "flags aren't needed to win"


def test_not_won_while_safe_cells_remain(board):
    g = board("*.*",
              "...",
              "*.*")
    g.reveal(1, 1)
    assert g.status == GameStatus.PLAYING


def test_win_by_single_reveals(board):
    g = board("*.",
              "..")
    g.reveal(0, 1)
    g.reveal(1, 0)
    assert g.status == GameStatus.PLAYING
    g.reveal(1, 1)
    assert g.status == GameStatus.WON


def test_chord_opens_neighbours_when_flags_match(board):
    g = board("*...",
              "....",
              "...*")
    g.reveal(1, 1)                 # a "1"
    g.toggle_flag(0, 0)
    g.chord(1, 1)
    for r, c in [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]:
        assert g.cell(r, c).state == CellState.REVEALED, f"{(r, c)} should be opened by the chord"
    assert g.cell(0, 0).state == CellState.FLAGGED


def test_chord_does_nothing_without_enough_flags(board):
    g = board("*...",
              "....",
              "...*")
    g.reveal(1, 1)
    assert g.cell(1, 1).state == CellState.REVEALED
    g.chord(1, 1)                  # no flags placed, so nothing happens
    assert g.cell(0, 1).state == CellState.HIDDEN


def test_chord_with_wrong_flag_hits_mine(board):
    g = board("*...",
              "....",
              "...*")
    g.reveal(1, 1)
    g.toggle_flag(0, 1)            # wrong flag; the mine is at (0,0)
    g.chord(1, 1)
    assert g.status == GameStatus.LOST
    assert g.cell(0, 0).exploded


def test_chord_on_hidden_cell_does_nothing(board):
    g = board("*...",
              "....",
              "...*")
    g.reveal(0, 1)                 # a "1", opens only itself
    g.toggle_flag(0, 0)
    assert g.cell(0, 1).state == CellState.REVEALED
    g.chord(1, 1)                  # (1,1) is still hidden
    assert g.cell(1, 1).state == CellState.HIDDEN
