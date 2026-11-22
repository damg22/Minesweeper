"""Shared test helpers. Boards are drawn as text: '*' is a mine, '.' is safe."""

import pytest

from minesweeper.game import Game


def build(*rows: str) -> Game:
    """build("*..", "...", "..*") -> a 3x3 Game with mines at (0,0) and (2,2)."""
    positions = [(r, c) for r, line in enumerate(rows) for c, ch in enumerate(line) if ch == "*"]
    game = Game(len(rows), len(rows[0]), len(positions))
    game.set_mines(positions)
    return game


@pytest.fixture
def board():
    return build
