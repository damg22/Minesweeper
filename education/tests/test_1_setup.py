"""Milestone 1: placing mines and counting neighbours."""

from minesweeper.game import CellState, Game, GameStatus


def test_new_game_starts_ready_and_hidden():
    g = Game(9, 9, 10)
    assert g.status == GameStatus.READY
    assert all(g.cell(r, c).state == CellState.HIDDEN for r in range(9) for c in range(9))


def test_set_mines_marks_exactly_those_cells(board):
    g = board("*..",
              "...",
              "..*")
    mines = {(r, c) for r in range(3) for c in range(3) if g.cell(r, c).is_mine}
    assert mines == {(0, 0), (2, 2)}
    assert g.mines_placed


def test_counts_include_diagonals(board):
    g = board("*.*",
              "...",
              "*.*")
    assert g.cell(1, 1).adjacent_mines == 4, "the centre touches all four corner mines diagonally"


def test_counts_orthogonal_and_diagonal_mix(board):
    g = board(".*.",
              "*.*",
              ".*.")
    assert g.cell(1, 1).adjacent_mines == 4
    assert g.cell(0, 0).adjacent_mines == 2
    assert g.cell(2, 2).adjacent_mines == 2


def test_counts_at_edges_and_corners(board):
    g = board("....",
              ".**.",
              "....")
    assert g.cell(0, 0).adjacent_mines == 1, "corner cells have only 3 neighbours"
    assert g.cell(0, 1).adjacent_mines == 2
    assert g.cell(0, 3).adjacent_mines == 1
    assert g.cell(1, 0).adjacent_mines == 1, "edge cells have only 5 neighbours"
    assert g.cell(2, 2).adjacent_mines == 2


def test_full_board_of_eights(board):
    g = board("***",
              "*.*",
              "***")
    assert g.cell(1, 1).adjacent_mines == 8


def test_place_mines_count_and_safe_cell():
    for _ in range(200):
        g = Game(9, 9, 10)
        g.place_mines(4, 4)
        mines = [(r, c) for r in range(9) for c in range(9) if g.cell(r, c).is_mine]
        assert len(mines) == 10, "place exactly game.mines mines"
        assert (4, 4) not in mines, "the first-clicked cell must never be a mine"
        assert g.mines_placed


def test_place_mines_on_a_crowded_board():
    for _ in range(50):
        g = Game(3, 3, 8)
        g.place_mines(0, 0)
        assert not g.cell(0, 0).is_mine
        assert sum(g.cell(r, c).is_mine for r in range(3) for c in range(3)) == 8


def test_place_mines_also_computes_counts():
    g = Game(5, 5, 6)
    g.place_mines(2, 2)
    assert sum(g.cell(r, c).is_mine for r in range(5) for c in range(5)) == 6
    for r in range(5):
        for c in range(5):
            expected = sum(
                g.cell(rr, cc).is_mine
                for rr in range(r - 1, r + 2)
                for cc in range(c - 1, c + 2)
                if (rr, cc) != (r, c) and 0 <= rr < 5 and 0 <= cc < 5
            )
            assert g.cell(r, c).adjacent_mines == expected, f"wrong count at {(r, c)}"
