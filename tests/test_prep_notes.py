import os, sys, subprocess, tempfile, unittest
from pathlib import Path

SCRIPT = str(Path(__file__).resolve().parent.parent / "scripts" / "prep_notes.py")


def run(md_text, slides_dir):
    src = Path(slides_dir) / "MASTER.md"
    src.write_text(md_text)
    r = subprocess.run(
        [sys.executable, SCRIPT, str(src)], capture_output=True, text=True
    )
    assert r.returncode == 0, r.stderr
    return r.stdout


class VisualTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        (Path(self.dir) / "assets").mkdir()
        (Path(self.dir) / "assets" / "real.png").write_bytes(b"x")

    def test_existing_asset_becomes_image(self):
        out = run("**Visual:** `assets/real.png` — A diagram\n", self.dir)
        self.assertIn("![A diagram](assets/real.png)", out)
        self.assertNotIn("**Visual:**", out)

    def test_stage_direction_becomes_italic_cue(self):
        out = run("**Visual:** (live demo) — run `ls`\n", self.dir)
        self.assertIn("*(live demo) — run `ls`*", out)
        self.assertNotIn("**Visual:**", out)

    def test_missing_asset_becomes_placeholder(self):
        out = run("**Visual:** assets/ghost.svg — Future art\n", self.dir)
        self.assertIn("*[visual pending: Future art]*", out)
        self.assertNotIn("**Visual:**", out)


if __name__ == "__main__":
    unittest.main()
