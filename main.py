import argparse
import asyncio

import pygame  # noqa: F401  (imported here so the browser build, pygbag, knows to load pygame)

from minesweeper import settings as S
from minesweeper.game import Game
from minesweeper.ui import App


async def main():
    p = argparse.ArgumentParser(description="Minesweeper")
    p.add_argument("-d", "--difficulty", choices=S.DIFFICULTIES, default="beginner")
    p.add_argument("--custom", nargs=3, type=int, metavar=("ROWS", "COLS", "MINES"),
                   help="custom board, e.g. --custom 20 24 80")
    p.add_argument("--preview", action="store_true",
                   help="show a sample board with every tile type (no game logic needed)")
    args = p.parse_args()

    custom = None
    if args.custom:
        rows, cols, mines = args.custom
        rows = max(S.MIN_ROWS, min(S.MAX_ROWS, rows))
        cols = max(S.MIN_COLS, min(S.MAX_COLS, cols))
        mines = max(1, min(rows * cols - 1, mines))
        custom = (rows, cols, mines)

    factory = Game
    if args.preview:
        from minesweeper.preview import PreviewGame
        factory = PreviewGame

    await App(difficulty=args.difficulty, custom=custom, game_factory=factory).run_async()


# pygbag (the browser build) needs an async main() started with asyncio.run().
if __name__ == "__main__":
    asyncio.run(main())
