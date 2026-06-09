import os, sys, zipfile, tempfile, unittest
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


if __name__ == "__main__":
    unittest.main()
