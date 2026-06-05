#!/usr/bin/env python3
"""Slim a PowerPoint template: keep the slide master / layouts / theme, drop all
content slides (and their notes) and any media no longer referenced. Produces a
small .pptx usable as a Pandoc --reference-doc.

Usage: slim_template.py SRC.pptx DST.pptx
"""
import sys, re, zipfile

src, dst = sys.argv[1], sys.argv[2]
zin = zipfile.ZipFile(src)
names = zin.namelist()

def m(pat, n): return re.match(pat, n)
drop = {n for n in names if (
    m(r'ppt/slides/slide\d+\.xml$', n) or
    m(r'ppt/slides/_rels/slide\d+\.xml\.rels$', n) or
    m(r'ppt/notesSlides/notesSlide\d+\.xml$', n) or
    m(r'ppt/notesSlides/_rels/notesSlide\d+\.xml\.rels$', n)
)}

# media still referenced by surviving .rels (masters, layouts, theme, presentation)
ref_media = set()
for rn in (n for n in names if n.endswith('.rels') and n not in drop):
    for t in re.findall(r'Target="([^"]+)"', zin.read(rn).decode('utf-8', 'ignore')):
        if 'media/' in t:
            ref_media.add('ppt/media/' + t.split('media/')[-1])
drop |= {n for n in names if n.startswith('ppt/media/') and n not in ref_media}

# rewrite presentation (empty slide list), its rels (no slide rels), content types
pres = re.sub(r'<p:sldIdLst>.*?</p:sldIdLst>', '<p:sldIdLst/>',
              zin.read('ppt/presentation.xml').decode('utf-8'), flags=re.S)
presrels = re.sub(r'<Relationship[^>]+Type="[^"]*/slide"[^>]*/>', '',
                  zin.read('ppt/_rels/presentation.xml.rels').decode('utf-8'))
ct = zin.read('[Content_Types].xml').decode('utf-8')
ct = re.sub(r'<Override PartName="/ppt/slides/slide\d+\.xml"[^>]*/>', '', ct)
ct = re.sub(r'<Override PartName="/ppt/notesSlides/notesSlide\d+\.xml"[^>]*/>', '', ct)
edits = {'ppt/presentation.xml': pres,
         'ppt/_rels/presentation.xml.rels': presrels,
         '[Content_Types].xml': ct}

with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        n = item.filename
        if n in drop:
            continue
        zout.writestr(n, edits.get(n, zin.read(n)))
zin.close()
print('slimmed ->', dst)
