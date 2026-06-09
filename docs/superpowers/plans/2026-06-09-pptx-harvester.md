# PowerPoint Harvester Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a stdlib-only tool that extracts a PowerPoint deck into this repo's slide-DSL markdown (writing embedded images to `slides/assets/`), and wire the render pipeline so those images appear in the CBS-branded `.pptx`.

**Architecture:** `scripts/harvest_pptx.py` reads a `.pptx` as a zip, resolves slide order via `presentation.xml`, extracts titles/bullets/notes/images per slide, and prints DSL markdown to stdout (never touching `MASTER.md`). `scripts/prep_notes.py` gains one rule that turns `**Visual:**` lines into Pandoc image embeds or italic cues. The three render scripts get `--resource-path=slides` so relative `assets/…` paths resolve.

**Tech Stack:** Python 3 stdlib only (`zipfile`, `xml.etree.ElementTree`, `posixpath`, `pathlib`, `unittest`) — matching the repo's no-dependency convention (`scripts/slim_template.py` already reads pptx via `zipfile`). Pandoc for rendering. **XML hardening:** since stdlib XML is XXE/billion-laughs-prone and `defusedxml` would add a dependency, the `_xml` reader rejects any part containing a DTD/entity declaration (which a legitimate `.pptx` never has) — see Task 1.

---

## File Structure

- Create: `scripts/harvest_pptx.py` — the harvester (pptx → DSL markdown + extracted assets).
- Create: `tests/test_harvest_pptx.py` — unittest suite with an in-test minimal-pptx fixture builder.
- Modify: `scripts/prep_notes.py` — add `**Visual:**` line handling.
- Create: `tests/test_prep_notes.py` — unittest suite for the new Visual handling.
- Modify: `scripts/build.sh`, `scripts/preview.sh`, `scripts/watch.sh` — add `--resource-path=slides`.

Tests run from repo root with: `python3 -m unittest discover -s tests -v`

---

## Task 1: Scaffold module + fixture builder + slide ordering

**Files:**
- Create: `scripts/harvest_pptx.py`
- Test: `tests/test_harvest_pptx.py`

- [ ] **Step 1: Write the failing test (fixture builder + ordering)**

Create `tests/test_harvest_pptx.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_harvest_pptx -v`
Expected: FAIL — `AttributeError: module 'harvest_pptx' has no attribute 'slide_parts'`

- [ ] **Step 3: Write minimal implementation**

Create `scripts/harvest_pptx.py`:

```python
#!/usr/bin/env python3
"""Harvest a .pptx into this repo's slide DSL (stdout) + images to slides/assets/.

Stdlib only (zipfile + ElementTree), matching scripts/slim_template.py. The pptx
is an INPUT you harvest from, never a source of truth: output goes to stdout for a
human to merge into slides/MASTER.md. See
docs/superpowers/specs/2026-06-09-pptx-harvester-design.md.
"""
import sys, posixpath
import xml.etree.ElementTree as ET
from pathlib import Path

P = "http://schemas.openxmlformats.org/presentationml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"p": P, "a": A, "r": R, "pkg": PKG}


def _xml(zf, part):
    # Security: .pptx parts never contain a DTD. Refusing one blocks XXE and
    # billion-laughs entity-expansion attacks without a defusedxml dependency
    # (the repo is intentionally stdlib-only).
    data = zf.read(part)
    if b"<!DOCTYPE" in data or b"<!ENTITY" in data:
        raise ValueError(f"refusing to parse {part}: DTD/entity declarations are not allowed in pptx")
    return ET.fromstring(data)


def rels(zf, owner):
    """Map rId -> {'target': resolved_part, 'type': type} for an owner part."""
    relpart = posixpath.join(
        posixpath.dirname(owner), "_rels", posixpath.basename(owner) + ".rels"
    )
    out = {}
    try:
        root = _xml(zf, relpart)
    except KeyError:
        return out
    base = posixpath.dirname(owner)
    for rel in root.findall("pkg:Relationship", NS):
        tgt = rel.get("Target")
        if rel.get("TargetMode") == "External":
            resolved = tgt
        else:
            resolved = posixpath.normpath(posixpath.join(base, tgt))
        out[rel.get("Id")] = {"target": resolved, "type": rel.get("Type", "")}
    return out


def slide_parts(zf):
    """Ordered list of slide part names, per presentation.xml sldIdLst."""
    pres = _xml(zf, "ppt/presentation.xml")
    rmap = rels(zf, "ppt/presentation.xml")
    parts = []
    for sld in pres.findall(".//p:sldIdLst/p:sldId", NS):
        rid = sld.get(f"{{{R}}}id")
        if rid in rmap:
            parts.append(rmap[rid]["target"])
    return parts
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_harvest_pptx -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/harvest_pptx.py tests/test_harvest_pptx.py
git commit -m "Add pptx harvester scaffold + slide-ordering"
```

---

## Task 2: Extract title and nested bullets

**Files:**
- Modify: `scripts/harvest_pptx.py`
- Test: `tests/test_harvest_pptx.py`

- [ ] **Step 1: Write the failing test**

Add to `class HarvestTest`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_harvest_pptx -v`
Expected: FAIL — `module 'harvest_pptx' has no attribute 'title_and_bullets'`

- [ ] **Step 3: Write minimal implementation**

Add to `scripts/harvest_pptx.py`:

```python
def _para_text(p):
    return "".join(t.text or "" for t in p.findall(".//a:t", NS)).strip()


def title_and_bullets(slide_el):
    """Return (title or None, [(level, text), ...]) for a slide element."""
    title = None
    bullets = []
    for sp in slide_el.findall(".//p:spTree/p:sp", NS):
        ph = sp.find(".//p:ph", NS)
        ph_type = ph.get("type") if ph is not None else None
        is_title = ph_type in ("title", "ctrTitle")
        paras = [p for p in sp.findall(".//p:txBody/a:p", NS)]
        texts = [(p, _para_text(p)) for p in paras]
        texts = [(p, t) for p, t in texts if t]
        if not texts:
            continue
        if is_title and title is None:
            title = " ".join(t for _, t in texts)
            continue
        for p, t in texts:
            pPr = p.find("a:pPr", NS)
            lvl = int(pPr.get("lvl", "0")) if pPr is not None else 0
            bullets.append((lvl, t))
    return title, bullets
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_harvest_pptx -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Commit**

```bash
git add scripts/harvest_pptx.py tests/test_harvest_pptx.py
git commit -m "Add title + nested bullet extraction to harvester"
```

---

## Task 3: Extract speaker notes

**Files:**
- Modify: `scripts/harvest_pptx.py`
- Test: `tests/test_harvest_pptx.py`

- [ ] **Step 1: Write the failing test**

Add to `class HarvestTest`:

```python
    def test_notes_skips_slide_number(self):
        with zipfile.ZipFile(self.pptx) as z:
            notes = H.notes_text(z, "ppt/slides/slide1.xml")
        self.assertEqual(notes, "Remember to breathe.")

    def test_notes_empty_when_absent(self):
        with zipfile.ZipFile(self.pptx) as z:
            notes = H.notes_text(z, "ppt/slides/slide2.xml")
        self.assertEqual(notes, "")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_harvest_pptx -v`
Expected: FAIL — `module 'harvest_pptx' has no attribute 'notes_text'`

- [ ] **Step 3: Write minimal implementation**

Add to `scripts/harvest_pptx.py`:

```python
def notes_text(zf, slide_part):
    """Body text of the slide's notesSlide, skipping the slide-number placeholder."""
    rmap = rels(zf, slide_part)
    note_part = None
    for info in rmap.values():
        if info["type"].endswith("notesSlide"):
            note_part = info["target"]
            break
    if not note_part:
        return ""
    el = _xml(zf, note_part)
    chunks = []
    for sp in el.findall(".//p:spTree/p:sp", NS):
        ph = sp.find(".//p:ph", NS)
        if ph is not None and ph.get("type") == "sldNum":
            continue
        for p in sp.findall(".//p:txBody/a:p", NS):
            t = _para_text(p)
            if t:
                chunks.append(t)
    return " ".join(chunks)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_harvest_pptx -v`
Expected: PASS (5 tests)

- [ ] **Step 5: Commit**

```bash
git add scripts/harvest_pptx.py tests/test_harvest_pptx.py
git commit -m "Add speaker-notes extraction to harvester"
```

---

## Task 4: Extract images to assets with dedup

**Files:**
- Modify: `scripts/harvest_pptx.py`
- Test: `tests/test_harvest_pptx.py`

- [ ] **Step 1: Write the failing test**

Add to `class HarvestTest`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_harvest_pptx -v`
Expected: FAIL — `module 'harvest_pptx' has no attribute 'extract_images'`

- [ ] **Step 3: Write minimal implementation**

Add to `scripts/harvest_pptx.py`:

```python
def extract_images(zf, slide_part, slide_no, stem, assets_dir, seen):
    """Write each referenced image once into assets_dir; return [(ref, slide_no)].

    `seen` maps a media part -> 'assets/<name>' so a logo reused across slides is
    written a single time and every reference points at it.
    """
    assets_dir = Path(assets_dir)
    assets_dir.mkdir(parents=True, exist_ok=True)
    rmap = rels(zf, slide_part)
    el = _xml(zf, slide_part)
    refs, m = [], 0
    for blip in el.findall(".//a:blip", NS):
        rid = blip.get(f"{{{R}}}embed")
        info = rmap.get(rid)
        if not info:
            continue
        media = info["target"]
        if media in seen:
            refs.append((seen[media], slide_no))
            continue
        m += 1
        ext = media.rsplit(".", 1)[-1] if "." in media else "png"
        name = f"{stem}-slide{slide_no:02d}-img{m}.{ext}"
        (assets_dir / name).write_bytes(zf.read(media))
        ref = f"assets/{name}"
        seen[media] = ref
        refs.append((ref, slide_no))
    return refs
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_harvest_pptx -v`
Expected: PASS (6 tests)

- [ ] **Step 5: Commit**

```bash
git add scripts/harvest_pptx.py tests/test_harvest_pptx.py
git commit -m "Add image extraction with dedup to harvester"
```

---

## Task 5: Assemble DSL markdown + non-text flag

**Files:**
- Modify: `scripts/harvest_pptx.py`
- Test: `tests/test_harvest_pptx.py`

- [ ] **Step 1: Write the failing test**

Add to `class HarvestTest`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_harvest_pptx -v`
Expected: FAIL — `module 'harvest_pptx' has no attribute 'harvest'`

- [ ] **Step 3: Write minimal implementation**

Add to `scripts/harvest_pptx.py`:

```python
def harvest(zf, stem, assets_dir):
    """Return DSL markdown for the whole deck; write images to assets_dir."""
    seen = {}
    blocks = []
    for n, part in enumerate(slide_parts(zf), start=1):
        el = _xml(zf, part)
        title, bullets = title_and_bullets(el)
        lines = [f"### Slide — {title or f'(untitled {n})'}"]
        if bullets:
            lines.append("**On slide:**")
            for lvl, text in bullets:
                lines.append("  " * lvl + f"- {text}")
            lines.append("")
        for ref, sn in extract_images(zf, part, n, stem, assets_dir, seen):
            lines.append(f"**Visual:** {ref} — imported from slide {sn}")
        if el.findall(".//p:graphicFrame", NS):
            lines.append(
                f"**Visual:** (imported from slide {n}: table/chart — needs manual handling)"
            )
        notes = notes_text(zf, part)
        if notes:
            lines += ["", "**Notes:**", f"> {notes}"]
        blocks.append("\n".join(lines).rstrip())
    return "\n\n".join(blocks) + "\n"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_harvest_pptx -v`
Expected: PASS (7 tests)

- [ ] **Step 5: Commit**

```bash
git add scripts/harvest_pptx.py tests/test_harvest_pptx.py
git commit -m "Add DSL assembly + non-text flagging to harvester"
```

---

## Task 6: CLI entry point

**Files:**
- Modify: `scripts/harvest_pptx.py`
- Test: `tests/test_harvest_pptx.py`

- [ ] **Step 1: Write the failing test**

Add to `tests/test_harvest_pptx.py` (top-level, runs the script as a subprocess):

```python
import subprocess

class CliTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.pptx = os.path.join(self.tmp, "draft.pptx")
        make_fixture(self.pptx)
        self.script = str(
            Path(__file__).resolve().parent.parent / "scripts" / "harvest_pptx.py"
        )

    def test_cli_prints_dsl(self):
        r = subprocess.run(
            [sys.executable, self.script, self.pptx],
            capture_output=True, text=True, cwd=self.tmp
        )
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("### Slide — First In Order", r.stdout)

    def test_cli_errors_on_missing_file(self):
        r = subprocess.run(
            [sys.executable, self.script, "/no/such.pptx"],
            capture_output=True, text=True
        )
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("not found", r.stderr.lower())
```

Note: the CLI must resolve `assets_dir` to the repo's `slides/assets`, independent of `cwd`. The `cwd=self.tmp` above proves images land in the repo, not the caller's directory.

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_harvest_pptx -v`
Expected: FAIL — no `__main__` handling yet (`test_cli_prints_dsl` gets empty stdout / nonzero).

- [ ] **Step 3: Write minimal implementation**

Append to `scripts/harvest_pptx.py`:

```python
import zipfile

REPO = Path(__file__).resolve().parent.parent
ASSETS = REPO / "slides" / "assets"


def main(argv):
    if len(argv) != 2:
        print("usage: harvest_pptx.py <deck.pptx>", file=sys.stderr)
        return 2
    src = Path(argv[1])
    if not src.is_file():
        print(f"error: file not found: {src}", file=sys.stderr)
        return 1
    try:
        with zipfile.ZipFile(src) as zf:
            md = harvest(zf, stem=src.stem, assets_dir=ASSETS)
    except zipfile.BadZipFile:
        print(f"error: not a .pptx (bad zip): {src}", file=sys.stderr)
        return 1
    sys.stdout.write(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_harvest_pptx -v`
Expected: PASS (9 tests)

- [ ] **Step 5: Make executable and commit**

```bash
chmod +x scripts/harvest_pptx.py
git add scripts/harvest_pptx.py tests/test_harvest_pptx.py
git commit -m "Add harvester CLI entry point"
```

---

## Task 7: Teach prep_notes.py to render `**Visual:**` lines

**Files:**
- Modify: `scripts/prep_notes.py`
- Test: `tests/test_prep_notes.py`

**Behavior (deterministic, refines the spec's stage-direction rule to an italic cue):**
- `**Visual:** <path> — <desc>` where `<path>` (backticks stripped) exists relative to `slides/` → `![<desc>](<path>)`.
- `**Visual:** (<cue>) — <desc>` (target starts with `(`) → `*(<cue>) — <desc>*` (italic on-slide cue).
- `**Visual:** <path> — <desc>` where `<path>` does NOT exist → `*[visual pending: <desc>]*`.

- [ ] **Step 1: Write the failing test**

Create `tests/test_prep_notes.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_prep_notes -v`
Expected: FAIL — output still contains literal `**Visual:**`.

- [ ] **Step 3: Write minimal implementation**

In `scripts/prep_notes.py`, after the existing `import sys, re` line, add the
base-directory capture and a Visual regex:

```python
import os
BASE = os.path.dirname(os.path.abspath(sys.argv[1]))
VISUAL = re.compile(r'^\*\*Visual:\*\*\s*`?([^`\s]+)`?\s*—\s*(.*)$')
```

Then inside the `while i < len(lines)` loop in `prep_notes.py`, add this branch
**before** the final `out.append(line)`:

```python
    mv = VISUAL.match(s)
    if mv:
        target, desc = mv.group(1), mv.group(2).strip()
        if target.startswith('('):
            out.append(f'*{s[len("**Visual:**"):].strip()}*')
        elif os.path.isfile(os.path.join(BASE, target)):
            out.append(f'![{desc}]({target})')
        else:
            out.append(f'*[visual pending: {desc}]*')
        i += 1
        continue
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_prep_notes -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Verify the existing build still works**

Run: `python3 -m unittest discover -s tests -v && scripts/build.sh`
Expected: all tests PASS; `Rendered -> build/MASTER.pptx`. The 6 existing
`Visual:` lines now render as italic cues (the 4 SVG specs as `*[visual pending: …]*`,
the 2 demo lines as italic cues) instead of literal `**Visual:**` text.

- [ ] **Step 6: Commit**

```bash
git add scripts/prep_notes.py tests/test_prep_notes.py
git commit -m "Render **Visual:** lines as images / italic cues in prep_notes"
```

---

## Task 8: Add `--resource-path=slides` so image embeds resolve

**Files:**
- Modify: `scripts/build.sh:19`, `scripts/preview.sh:16`, `scripts/watch.sh:12`

- [ ] **Step 1: Write the failing test (end-to-end render check)**

Create `tests/test_render_assets.py`:

```python
import subprocess, zipfile, unittest, shutil
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_render_assets -v`
Expected: FAIL — without `--resource-path` Pandoc can't find `assets/_rendertest.png`, so no `ppt/media/*` is embedded (Pandoc emits a warning and drops the image). *(This step proves the flag is load-bearing; the test command itself already includes the flag, so if it passes here, temporarily remove `--resource-path=slides` from the test to confirm it fails, then restore it.)*

- [ ] **Step 3: Add the flag to the three render scripts**

In `scripts/build.sh`, change the pandoc line (line 19) to:

```bash
pandoc "$TMP" -f markdown -o "$OUT" --slide-level=3 --resource-path=slides --reference-doc="$REF"
```

In `scripts/preview.sh`, add `--resource-path=slides \` after the `--slide-level=3 \` line (line 17).

In `scripts/watch.sh`, add `--resource-path=slides` to the pandoc invocation (line 12-15), e.g. on the `--slide-level=3 ...` continuation line.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_render_assets -v`
Expected: PASS — `ppt/media/*` present in the rendered pptx.

- [ ] **Step 5: Full suite + real build**

Run: `python3 -m unittest discover -s tests -v && scripts/build.sh`
Expected: all tests PASS; `Rendered -> build/MASTER.pptx`.

- [ ] **Step 6: Commit**

```bash
git add scripts/build.sh scripts/preview.sh scripts/watch.sh tests/test_render_assets.py
git commit -m "Resolve slides/assets image paths in render scripts (--resource-path)"
```

---

## Self-Review

**1. Spec coverage:**
- Harvest-inbox model, stdout-only, no MASTER.md writes → Tasks 5, 6. ✓
- Stdlib only (zipfile + ElementTree) → Task 1. ✓
- Slide ordering via sldIdLst → Task 1. ✓
- Title / nested bullets / notes (skip sldNum) → Tasks 2, 3. ✓
- Images → assets, positional names, dedup → Task 4. ✓
- Non-text flagged not dropped → Task 5 (graphicFrame branch). ✓
- Option A image convention + `prep_notes` rendering → Task 7. ✓
- Image paths resolve at render → Task 8 (companion to Option A; not in original spec, added because embeds fail without it). ✓
- Out of scope (bespoke SVGs, auto-merge, python-pptx) → respected; SVG specs render as `*[visual pending]*`. ✓

**2. Placeholder scan:** No TBD/TODO/"handle edge cases" — every code step is complete. The only literal "pending" is the intended `*[visual pending: …]*` output. ✓

**3. Type consistency:** `slide_parts`, `title_and_bullets`, `notes_text`, `extract_images(zf, slide_part, slide_no, stem, assets_dir, seen)`, `harvest(zf, stem, assets_dir)`, `main(argv)` — names and signatures match across tasks and tests. `seen` dict and `assets/<name>` reference format are consistent between Task 4 and Task 5. ✓
