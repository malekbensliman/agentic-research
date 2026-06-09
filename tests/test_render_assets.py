import subprocess, zipfile, unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


class RenderAssetTest(unittest.TestCase):
    def test_existing_asset_is_embedded_in_pptx(self):
        # a real asset + a one-slide deck that references it
        asset = REPO / "slides" / "assets" / "_rendertest.png"
        asset.write_bytes(b"\x89PNG\r\n\x1a\nFAKE")
        deck = REPO / "slides" / "_rendertest.md"
        deck.write_text(
            "### Slide — Render Test\n"
            "**On slide:**\n- hi\n\n"
            "**Visual:** `assets/_rendertest.png` — caption\n"
        )
        out = REPO / "build" / "_rendertest.pptx"
        try:
            tmp = REPO / "build" / "_rendertest.prep.md"
            tmp.parent.mkdir(exist_ok=True)
            prepped = subprocess.run(
                ["python3", "scripts/prep_notes.py", "slides/_rendertest.md"],
                cwd=REPO, capture_output=True, text=True, check=True
            ).stdout
            tmp.write_text(prepped)
            subprocess.run(
                ["pandoc", str(tmp), "-o", str(out), "--slide-level=3",
                 "--reference-doc=templates/cbs-template.pptx",
                 "--resource-path=slides"],
                cwd=REPO, check=True
            )
            with zipfile.ZipFile(out) as z:
                media = [n for n in z.namelist() if n.startswith("ppt/media/")]
            self.assertTrue(media, "no media embedded — resource-path missing?")
        finally:
            for f in (asset, deck, out, REPO / "build" / "_rendertest.prep.md"):
                f.exists() and f.unlink()


if __name__ == "__main__":
    unittest.main()
