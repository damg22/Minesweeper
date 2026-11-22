"""
Build the student starter kit: dist/minesweeper-starter.zip

    python education/build_starter.py

The kit is the finished UI from this repo, with minesweeper/game.py swapped for
the empty stub in education/game_stub.py, plus the tests and the student
handout. It's rebuilt from the current UI every time, so the two never drift apart.
"""

import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EDU = ROOT / "education"
KIT = "minesweeper-starter"

# (source, path inside the kit)
FILES = [
    (ROOT / "main.py", "main.py"),
    (ROOT / "LICENSE", "LICENSE"),
    (ROOT / "minesweeper" / "__init__.py", "minesweeper/__init__.py"),
    (ROOT / "minesweeper" / "settings.py", "minesweeper/settings.py"),
    (ROOT / "minesweeper" / "graphics.py", "minesweeper/graphics.py"),
    (ROOT / "minesweeper" / "ui.py", "minesweeper/ui.py"),
    (ROOT / "minesweeper" / "preview.py", "minesweeper/preview.py"),
    (EDU / "game_stub.py", "minesweeper/game.py"),
    (EDU / "STUDENT_README.md", "README.md"),
    *[(p, f"tests/{p.name}") for p in sorted((EDU / "tests").glob("*.py"))],
]

GENERATED = {
    "requirements.txt": "pygame==2.6.1\npytest\n",
    "pytest.ini": "[pytest]\npythonpath = .\ntestpaths = tests\n",
    ".gitignore": ".venv/\n__pycache__/\n*.pyc\n.DS_Store\n.pytest_cache/\n",
}


def build(out_dir: Path = ROOT / "dist") -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        kit = Path(tmp) / KIT
        for src, rel in FILES:
            dst = kit / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        for rel, text in GENERATED.items():
            (kit / rel).write_text(text)

        zip_path = out_dir / f"{KIT}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in sorted(kit.rglob("*")):
                if f.is_file():
                    zf.write(f, f.relative_to(kit.parent))
    return zip_path


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "dist"
    print(build(out))
