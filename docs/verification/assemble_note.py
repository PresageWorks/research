#!/usr/bin/env python3
"""Assemble research-note.md from the section files. No private inputs.

Sections are ordered by filename. verify_public_record.py asserts that
research-note.md is exactly this concatenation, so the rendered page cannot
drift from its sources.
"""
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent
sections = sorted((DOCS / "sections").glob("*.md"))
out = "\n\n".join(s.read_text(encoding="utf-8").strip() for s in sections) + "\n"
(DOCS / "research-note.md").write_text(out, encoding="utf-8")
print(f"wrote research-note.md ({len(sections)} sections, {len(out.split()):,} words)")
