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
        rid = rel.get("Id")
        tgt = rel.get("Target")
        if rid is None or tgt is None:
            continue
        if rel.get("TargetMode") == "External":
            resolved = tgt
        else:
            resolved = posixpath.normpath(posixpath.join(base, tgt))
        out[rid] = {"target": resolved, "type": rel.get("Type", "")}
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
