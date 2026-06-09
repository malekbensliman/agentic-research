#!/usr/bin/env python3
"""Preprocess a workshop master deck for Pandoc pptx rendering.

- strips the YAML front-matter and HTML comments (our metadata, not Pandoc's)
- drops the literal "**On slide:**" labels (the bullets speak for themselves)
- converts each "**Notes:**" + blockquote into a Pandoc `::: notes` div so the
  speaker notes land in the slide's notes pane instead of on the slide.
"""
import sys, re, os
BASE = os.path.dirname(os.path.abspath(sys.argv[1]))
VISUAL = re.compile(r'^\*\*Visual:\*\*\s*(.*?)\s*—\s*(.*)$')

src = open(sys.argv[1]).read()
src = re.sub(r'^---\n.*?\n---\n', '', src, count=1, flags=re.S)   # front-matter
src = re.sub(r'<!--.*?-->', '', src, flags=re.S)                  # comments

lines = src.split('\n')
out, i = [], 0
while i < len(lines):
    line = lines[i]
    s = line.strip()
    if s == '**On slide:**':
        i += 1
        continue
    if re.match(r'^_~?\s*\d+\s*min_$', s):          # drop "_~10 min_" duration notes
        i += 1
        continue
    if line.startswith('### Slide — '):             # clean "Slide — X" titles to "X"
        out.append('### ' + line[len('### Slide — '):])
        i += 1
        continue
    if s == '**Notes:**':
        i += 1
        notes = []
        while i < len(lines) and lines[i].lstrip().startswith('>'):
            notes.append(lines[i].lstrip()[1:].strip())
            i += 1
        out += ['', '::: notes', ' '.join(notes), ':::', '']
        continue
    mv = VISUAL.match(s)
    if mv:
        target, desc = mv.group(1).strip('`'), mv.group(2).strip()
        if target.startswith('('):
            out.append(f'*{s[len("**Visual:**"):].strip()}*')
        elif os.path.isfile(os.path.join(BASE, target)):
            out.append(f'![{desc}]({target})')
        else:
            out.append(f'*[visual pending: {desc}]*')
        i += 1
        continue
    out.append(line)
    i += 1

print('\n'.join(out))
