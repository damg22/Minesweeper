"""Milestone 3: flags, question marks and the mine counter."""

from minesweeper.game import CellState, GameStatus


def test_flag_cycle(board):
    g = board("*..",
              "...",
              "...")
    g.toggle_flag(1, 1)
    assert g.cell(1, 1).state == CellState.FLAGGED
    g.toggle_flag(1, 1)
    assert g.cell(1, 1).state == CellState.QUESTION
    g.toggle_flag(1, 1)
    assert g.cell(1, 1).state == CellState.HIDDEN


def test_cannot_flag_revealed_cell(board):
    g = board("*..",
              "...",
              "...")
    g.reveal(0, 1)
    g.toggle_flag(0, 1)
    assert g.cell(0, 1).state == CellState.REVEALED


def test_flags_remaining_counts_down_and_can_go_negative(board):
    g = board("*..",
              "...",
              "...")
    assert g.flags_remaining() == 1
    g.toggle_flag(0, 0)
    assert g.flags_remaining() == 0
    g.toggle_flag(2, 2)
    assert g.flags_remaining() == -1, "too many flags makes the counter negative"


def test_question_marks_do_not_count_as_flags(board):
    g = board("*..",
              "...",
              "...")
    g.toggle_flag(0, 0)
    g.toggle_flag(0, 0)
    assert g.cell(0, 0).state == CellState.QUESTION
    assert g.flags_remaining() == 1


def test_question_mark_can_be_revealed(board):
    g = board("*..",
              "...",
              "...")
    g.toggle_flag(0, 1)
    g.toggle_flag(0, 1)            # QUESTION
    g.reveal(0, 1)
    assert g.cell(0, 1).state == CellState.REVEALED


def test_no_flagging_after_game_over(board):
    g = board("*..",
              "...",
              "...")
    g.reveal(0, 0)
    assert g.status == GameStatus.LOST
    g.toggle_flag(0, 2)
    assert g.cell(0, 2).state != CellState.FLAGGED
