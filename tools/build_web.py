"""
Build the browser version of the game with pygbag (pygame compiled to WebAssembly).

    .venv/bin/pip install pygbag==0.9.3
    .venv/bin/python tools/build_web.py            # writes dist/web/
    .venv/bin/python tools/build_web.py --serve    # build, then test at http://localhost:8000

GitHub Actions runs this on every push to main and publishes the result at
https://damg22.github.io/Minesweeper/play/ (see .github/workflows/pages.yml).

Note: open the local test through --serve, not a plain web server. On localhost
pygbag expects its own server on port 8000 to provide the Python runtime.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PYGBAG_ARGS = ["--ume_block", "0", "--title", "Minesweeper"]   # ume_block 0: start without a click
DESCRIPTION = ("Play classic Minesweeper in your browser, free. Written in Python with pygame "
               "and running on WebAssembly. Beginner, Intermediate and Expert boards.")


def make_icon(path: Path) -> None:
    """Favicon: the game's own mine tile."""
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    sys.path.insert(0, str(ROOT))
    import pygame
    from minesweeper import graphics as gfx

    pygame.init()
    pygame.display.set_mode((1, 1))
    pygame.image.save(gfx.build_tiles(64)["mine"], str(path))
    pygame.quit()


def stage(dst: Path) -> None:
    """Copy only what the game needs: pygbag packages everything in the folder."""
    (dst / "minesweeper").mkdir(parents=True)
    shutil.copy2(ROOT / "main.py", dst / "main.py")
    for f in (ROOT / "minesweeper").glob("*.py"):
        shutil.copy2(f, dst / "minesweeper" / f.name)
    make_icon(dst / "favicon.png")


def polish_page(index: Path) -> None:
    html = index.read_text()
    html = html.replace(
        "<title>Minesweeper</title>",
        "<title>Play Minesweeper Online – Python + pygame</title>\n"
        f'    <meta name="description" content="{DESCRIPTION}">\n'
        '    <link rel="canonical" href="https://damg22.github.io/Minesweeper/play/">',
        1,
    )
    html = html.replace("Loading, please wait ...", "Loading Minesweeper… (the first visit takes a few seconds)")
    index.write_text(html)


def build(out: Path) -> Path:
    with tempfile.TemporaryDirectory() as tmp:
        app = Path(tmp) / "minesweeper-web"
        stage(app)
        subprocess.run([sys.executable, "-m", "pygbag", "--build", *PYGBAG_ARGS,
                        "--icon", str(app / "favicon.png"), str(app)], check=True)
        web = app / "build" / "web"
        polish_page(web / "index.html")
        if out.exists():
            shutil.rmtree(out)
        shutil.copytree(web, out)
    return out


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out = build(Path(args[0]) if args else ROOT / "dist" / "web")
    print(f"Browser build ready: {out}")
    if "--serve" in sys.argv:
        with tempfile.TemporaryDirectory() as tmp:
            app = Path(tmp) / "minesweeper-web"
            stage(app)
            subprocess.run([sys.executable, "-m", "pygbag", *PYGBAG_ARGS, str(app)])
