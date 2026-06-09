import os, sys, zipfile, tempfile, unittest
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import harvest_pptx as H


def _z(zf, name, text):
    zf.writestr(name, text.strip() + "\n")


def make_fixture(path):
    """Minimal pptx with only the parts the harvester reads.

    Two slides; presentation lists slide2 BEFORE slide1 to prove ordering
    follows sldIdLst, not filename. slide1 (2nd in order) carries a title,
    two nested bullets, an image (used twice -> dedup), and notes.
    """
    REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    with zipfile.ZipFile(path, "w") as z:
        _z(z, "ppt/presentation.xml", f'''
<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
  xmlns:r="{REL}">
  <p:sldIdLst>
    <p:sldId id="256" r:id="rId2"/>
    <p:sldId id="257" r:id="rId1"/>
  </p:sldIdLst>
</p:presentation>''')
        _z(z, "ppt/_rels/presentation.xml.rels", '''
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="x/slide" Target="slides/slide1.xml"/>
  <Relationship Id="rId2" Type="x/slide" Target="slides/slide2.xml"/>
</Relationships>''')
        _z(z, "ppt/slides/slide2.xml", '''
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
  xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
  <p:cSld><p:spTree>
    <p:sp><p:nvSpPr><p:nvPr><p:ph type="title"/></p:nvPr></p:nvSpPr>
      <p:txBody><a:p><a:r><a:t>First In Order</a:t></a:r></a:p></p:txBody></p:sp>
  </p:spTree></p:cSld>
</p:sld>''')
        _z(z, "ppt/slides/slide1.xml", f'''
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
  xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
  xmlns:r="{REL}">
  <p:cSld><p:spTree>
    <p:sp><p:nvSpPr><p:nvPr><p:ph type="title"/></p:nvPr></p:nvSpPr>
      <p:txBody><a:p><a:r><a:t>Second In Order</a:t></a:r></a:p></p:txBody></p:sp>
    <p:sp><p:nvSpPr><p:nvPr><p:ph type="body"/></p:nvPr></p:nvSpPr>
      <p:txBody>
        <a:p><a:r><a:t>Top bullet</a:t></a:r></a:p>
        <a:p><a:pPr lvl="1"/><a:r><a:t>Nested bullet</a:t></a:r></a:p>
      </p:txBody></p:sp>
    <p:pic><p:blipFill><a:blip r:embed="rIdImg"/></p:blipFill></p:pic>
    <p:pic><p:blipFill><a:blip r:embed="rIdImg"/></p:blipFill></p:pic>
  </p:spTree></p:cSld>
</p:sld>''')
        _z(z, "ppt/slides/_rels/slide1.xml.rels", '''
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdImg" Type="x/image" Target="../media/image1.png"/>
  <Relationship Id="rIdNote" Type="x/notesSlide" Target="../notesSlides/notesSlide1.xml"/>
</Relationships>''')
        _z(z, "ppt/notesSlides/notesSlide1.xml", '''
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
  xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
  <p:cSld><p:spTree>
    <p:sp><p:nvSpPr><p:nvPr><p:ph type="sldNum"/></p:nvPr></p:nvSpPr>
      <p:txBody><a:p><a:r><a:t>7</a:t></a:r></a:p></p:txBody></p:sp>
    <p:sp><p:nvSpPr><p:nvPr><p:ph type="body"/></p:nvPr></p:nvSpPr>
      <p:txBody><a:p><a:r><a:t>Remember to breathe.</a:t></a:r></a:p></p:txBody></p:sp>
  </p:spTree></p:cSld>
</p:sld>''')
        z.writestr("ppt/media/image1.png", b"\x89PNG\r\n\x1a\nFAKE")


class HarvestTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.pptx = os.path.join(self.tmp, "draft.pptx")
        make_fixture(self.pptx)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_slide_order_follows_sldidlst_not_filename(self):
        with zipfile.ZipFile(self.pptx) as z:
            parts = H.slide_parts(z)
        self.assertEqual(
            parts, ["ppt/slides/slide2.xml", "ppt/slides/slide1.xml"]
        )

    def test_rejects_dtd_bearing_part(self):
        bad = os.path.join(self.tmp, "bad.pptx")
        with zipfile.ZipFile(bad, "w") as z:
            z.writestr(
                "ppt/presentation.xml",
                '<!DOCTYPE x [<!ENTITY a "boom">]>'
                '<p:presentation xmlns:p="%s"/>' % H.P,
            )
        with zipfile.ZipFile(bad) as z:
            with self.assertRaises(ValueError):
                H._xml(z, "ppt/presentation.xml")

    def test_title_and_nested_bullets(self):
        with zipfile.ZipFile(self.pptx) as z:
            el = H._xml(z, "ppt/slides/slide1.xml")
            title, bullets = H.title_and_bullets(el)
        self.assertEqual(title, "Second In Order")
        self.assertEqual(bullets, [(0, "Top bullet"), (1, "Nested bullet")])

    def test_untitled_when_no_title_placeholder(self):
        with zipfile.ZipFile(self.pptx) as z:
            # slide2 has only a title; craft a titleless element
            el = ET.fromstring(
                '<p:sld xmlns:p="%s" xmlns:a="%s"><p:cSld><p:spTree>'
                '<p:sp><p:txBody><a:p><a:r><a:t>Lonely</a:t></a:r></a:p>'
                "</p:txBody></p:sp></p:spTree></p:cSld></p:sld>" % (H.P, H.A)
            )
            title, bullets = H.title_and_bullets(el)
        self.assertIsNone(title)
        self.assertEqual(bullets, [(0, "Lonely")])

    def test_notes_skips_slide_number(self):
        with zipfile.ZipFile(self.pptx) as z:
            notes = H.notes_text(z, "ppt/slides/slide1.xml")
        self.assertEqual(notes, "Remember to breathe.")

    def test_notes_empty_when_absent(self):
        with zipfile.ZipFile(self.pptx) as z:
            notes = H.notes_text(z, "ppt/slides/slide2.xml")
        self.assertEqual(notes, "")

    def test_images_written_once_and_referenced(self):
        out_assets = Path(self.tmp) / "assets"
        seen = {}
        with zipfile.ZipFile(self.pptx) as z:
            refs = H.extract_images(
                z, "ppt/slides/slide1.xml", 2, "draft", out_assets, seen
            )
        # slide1 uses the same media twice -> one file, two references
        files = sorted(p.name for p in out_assets.iterdir())
        self.assertEqual(files, ["draft-slide02-img1.png"])
        self.assertEqual(
            refs, [("assets/draft-slide02-img1.png", 2),
                   ("assets/draft-slide02-img1.png", 2)]
        )

    def test_harvest_emits_dsl_in_order(self):
        out_assets = Path(self.tmp) / "assets"
        with zipfile.ZipFile(self.pptx) as z:
            md = H.harvest(z, stem="draft", assets_dir=out_assets)
        # slide2 ("First In Order") must appear before slide1 ("Second In Order")
        self.assertLess(md.index("First In Order"), md.index("Second In Order"))
        self.assertIn("### Slide — Second In Order", md)
        self.assertIn("**On slide:**", md)
        self.assertIn("- Top bullet", md)
        self.assertIn("  - Nested bullet", md)
        self.assertIn("**Visual:** assets/draft-slide02-img1.png — imported from slide 2", md)
        self.assertIn("**Notes:**", md)
        self.assertIn("> Remember to breathe.", md)


if __name__ == "__main__":
    unittest.main()
