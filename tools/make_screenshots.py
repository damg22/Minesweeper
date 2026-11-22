"""
Regenerate the images in docs/images/ by playing real games with the real code.

    .venv/bin/pip install pillow
    .venv/bin/python tools/make_screenshots.py

Runs headless (no window). Games are played by a simple bot that only clicks
cells next to what is already open, so the boards look like real play.
"""

import os
import random
import sys
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import pygame  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

from minesweeper.game import CellState, GameStatus  # noqa: E402
from minesweeper.ui import App  # noqa: E402

OUT = ROOT / "docs" / "images"
SCALE = 2  # crisp pixel-art upscale


# ----------------------------------------------------------------- helpers
def capture(app: App, timer: int | None = None) -> Image.Image:
    if timer == 0:  # timer not started yet: shows 000
        app.start_time = app.end_time = None
    elif timer is not None:  # show a fixed time on the timer
        app.start_time, app.end_time = 0.0, timer - 0.5
    app.render()
    surf = app.screen
    img = Image.frombytes("RGB", surf.get_size(), pygame.image.tobytes(surf, "RGB"))
    return img.resize((img.width * SCALE, img.height * SCALE), Image.NEAREST)


def neighbours(g, r, c):
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            rr, cc = r + dr, c + dc
            if (dr or dc) and 0 <= rr < g.rows and 0 <= cc < g.cols:
                yield rr, cc


def frontier(g):
    """Hidden cells touching an opened number: what a human would click next."""
    out = []
    for r in range(g.rows):
        for c in range(g.cols):
            if g.cell(r, c).state == CellState.HIDDEN and any(
                g.cell(rr, cc).state == CellState.REVEALED for rr, cc in neighbours(g, r, c)
            ):
                out.append((r, c))
    return out


def bot_move(g, rng):
    """Flag a mine or open a safe cell on the frontier (falls back to any hidden cell)."""
    options = frontier(g) or [
        (r, c) for r in range(g.rows) for c in range(g.cols) if g.cell(r, c).state == CellState.HIDDEN
    ]
    if not options:
        return False
    r, c = rng.choice(options)
    (g.toggle_flag if g.cell(r, c).is_mine else g.reveal)(r, c)
    return True


def new_app(difficulty, seed):
    random.seed(seed)  # mine placement uses the global random module
    app = App(difficulty=difficulty)
    return app, random.Random(seed)


# ----------------------------------------------------------------- scenes
def demo_gif():
    app, rng = new_app("beginner", 7)
    g = app.game
    frames, durations = [capture(app, 0)], [900]
    g.reveal(g.rows // 2, g.cols // 2)
    t = 1
    while g.status == GameStatus.PLAYING and bot_move(g, rng):
        t += 1
        frames.append(capture(app, t))
        durations.append(260)
    frames.append(capture(app, t))
    durations.append(2500)
    frames[0].save(OUT / "demo.gif", save_all=True, append_images=frames[1:],
                   duration=durations, loop=0, optimize=True)
    return frames[len(frames) // 2]


def intermediate_midgame():
    app, rng = new_app("intermediate", 11)
    g = app.game
    g.reveal(8, 8)
    for _ in range(70):
        bot_move(g, rng)
    img = capture(app, 74)
    img.save(OUT / "playing.png", optimize=True)
    return img


def beginner_win():
    app, rng = new_app("beginner", 3)
    g = app.game
    g.reveal(4, 4)
    while g.status == GameStatus.PLAYING and bot_move(g, rng):
        pass
    assert g.status == GameStatus.WON, g.status
    capture(app, 23).save(OUT / "win.png", optimize=True)


def expert_loss():
    app, rng = new_app("expert", 5)
    g = app.game
    g.reveal(8, 15)
    for _ in range(120):
        bot_move(g, rng)
    # a couple of wrong flags, then an unlucky guess
    safe = [p for p in frontier(g) if not g.cell(*p).is_mine]
    for p in rng.sample(safe, 2):
        g.toggle_flag(*p)
    mine = next(p for p in frontier(g) if g.cell(*p).is_mine)
    g.reveal(*mine)
    assert g.status == GameStatus.LOST
    capture(app, 211).save(OUT / "loss.png", optimize=True)


def social_card(shot: Image.Image):
    """1200x630 preview image used when the page link is shared."""
    W, H = 1200, 630
    card = Image.new("RGB", (W, H), (30, 32, 38))
    font_path = os.path.join(os.path.dirname(pygame.__file__), "freesansbold.ttf")
    d = ImageDraw.Draw(card)
    d.text((70, 200), "Minesweeper", font=ImageFont.truetype(font_path, 88), fill=(255, 255, 255))
    d.text((74, 315), "The classic puzzle game,", font=ImageFont.truetype(font_path, 36), fill=(200, 204, 212))
    d.text((74, 362), "written in Python + pygame.", font=ImageFont.truetype(font_path, 36), fill=(200, 204, 212))
    d.text((74, 450), "Free for Windows & Mac", font=ImageFont.truetype(font_path, 30), fill=(255, 90, 90))
    s = shot.copy()
    s.thumbnail((470, 560), Image.NEAREST)
    card.paste(s, (W - s.width - 70, (H - s.height) // 2))
    card.save(OUT / "og.png", optimize=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    demo_gif()
    shot = intermediate_midgame()
    beginner_win()
    expert_loss()
    social_card(shot)
    for f in sorted(OUT.iterdir()):
        print(f"{f.relative_to(ROOT)}  {f.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
