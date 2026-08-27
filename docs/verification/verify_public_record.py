#!/usr/bin/env python3
"""Verify the public research record — self-contained, no private inputs.

WHAT THIS IS
------------
An integrity checker for THIS repository. It runs with nothing but the files
committed here: no captured data, no derived statistics, no PRESAGE module.

It deliberately does NOT attempt what the private checker does. The production
checker re-derives every headline number in the note from the analysis
artifacts that produced them; those artifacts are not public, and publishing
them would disclose the exploratory feature set. Rather than ship a copy of
that checker with its inputs missing -- an assertion suite that cannot run,
which is the exact failure mode section 7 of the note is about -- this verifies
the properties a reader CAN check from the public record alone.

WHAT IT CHECKS
  1. Contract integrity — the public redacted editions hash to the values
     recorded in HASHES.txt, and the ratified hashes are preserved verbatim.
  2. Note assembly — research-note.md is exactly the concatenation of the
     section files, so the rendered page cannot drift from its sources.
  3. Figures — every figure referenced by the note exists, and every figure
     present is referenced.
  4. Completeness — no unresolved TODO or [NUMBER NOT FOUND] markers.
  5. Citation hygiene — every reference carries a DOI or arXiv id, preprints
     are labelled as unrefereed, and the one scanned source names the pages it
     was read from.
  6. Generic secret scan — no credential pattern or absolute path anywhere.

The full disclosure gate — which tests for private module names, withheld
feature names and capture configuration — deliberately does NOT run here. The
list of forbidden tokens IS the disclosure: naming what must not appear would
publish it. That gate runs privately, before anything is copied into this
repository.

Exit code 0 if every check passes, 1 otherwise.

    python verify_public_record.py
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOCS = HERE.parent
ROOT = DOCS.parent

checks: list[tuple[bool, str, str]] = []


def expect(name: str, ok: bool, detail: str = "") -> bool:
    checks.append((bool(ok), name, detail))
    return bool(ok)


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# --- 1. contract integrity -------------------------------------------------
hashes = DOCS / "contract" / "HASHES.txt"
if expect("HASHES.txt present", hashes.exists()):
    text = hashes.read_text(encoding="utf-8")
    for fname in ("EVALUATION_CONTRACT.public.md",
                  "EVALUATION_CONTRACT.v1.public.md"):
        p = DOCS / "contract" / fname
        if not expect(f"{fname} present", p.exists()):
            continue
        actual = sha256_file(p)
        expect(f"{fname} matches its published sha256",
               actual in text, actual[:16] + "...")
    # the ratified (unredacted, private) digests must still be published
    for ratified in ("937ce309d5c01f1f135a63dffa60507f3a4d9606cdffc9afdda32aa9411b4161",
                     "505b12d0999665230127fcc630aeabe40a83aefdb78f07359a1ecd176c291869"):
        expect(f"ratified digest {ratified[:12]}... preserved", ratified in text)

# --- 2. note assembly ------------------------------------------------------
sections = sorted((DOCS / "sections").glob("*.md"))
note = DOCS / "research-note.md"
if expect("section files present", len(sections) >= 10, f"{len(sections)} files") \
        and expect("research-note.md present", note.exists()):
    rebuilt = "\n\n".join(s.read_text(encoding="utf-8").strip()
                          for s in sections) + "\n"
    expect("research-note.md is exactly the concatenation of its sections",
           rebuilt == note.read_text(encoding="utf-8"),
           "regenerate with assemble_note.py")

# --- 3. figures ------------------------------------------------------------
if note.exists():
    body = note.read_text(encoding="utf-8")
    referenced = set(re.findall(r"figures/([A-Za-z0-9._-]+\.png)", body))
    present = {p.name for p in (DOCS / "figures").glob("*.png")}
    expect("every referenced figure exists", referenced <= present,
           ", ".join(sorted(referenced - present)))
    expect("every figure present is referenced", present <= referenced,
           ", ".join(sorted(present - referenced)))

# --- 4. completeness -------------------------------------------------------
    expect("no unresolved TODO markers", "[TODO" not in body)
    expect("no unresolved [NUMBER NOT FOUND] in the body",
           body.count("[NUMBER NOT FOUND]") <= 1,
           "more than the one definitional mention")

# --- 5. citation hygiene ---------------------------------------------------
sec2 = next((s for s in sections if s.name.startswith("02-")), None)
if sec2 is not None:
    t = sec2.read_text(encoding="utf-8")
    refs, cur = [], None
    for ln in t.splitlines():
        if ln.startswith("- "):
            if cur:
                refs.append(" ".join(cur.split()))
            cur = ln[2:]
        elif cur is not None and ln.startswith("  "):
            cur += " " + ln
        elif cur is not None:
            refs.append(" ".join(cur.split()))
            cur = None
    if cur:
        refs.append(" ".join(cur.split()))
    expect("reference list parsed", len(refs) >= 9, f"{len(refs)} entries")
    bad = [r[:40] for r in refs if "doi:" not in r and "arXiv:" not in r]
    expect("every reference carries a DOI or arXiv id", not bad, "; ".join(bad))
    for tag in ("arXiv:2607.27070", "arXiv:2212.06888"):
        i = t.find(tag)
        expect(f"{tag} labelled as a preprint",
               i > 0 and "not peer reviewed" in t[i:i + 260])
    if "Kyle" in t:
        expect("Kyle carries a DOI", "10.2307/1913210" in t)
        expect("Kyle names the pages it was read from", "1315–1316" in t)

# --- 6. generic secret scan -----------------------------------------------
# Only generic credential and absolute-path patterns live here. The full
# disclosure gate -- which tests for private module names, withheld feature
# names and capture configuration -- deliberately does NOT run in this
# repository, because the list of forbidden tokens IS the disclosure. Naming
# what must not appear would publish it. That gate runs privately, before
# anything is copied here.
GENERIC = (r"AKIA[0-9A-Z]{16}", r"ASIA[0-9A-Z]{16}", r"aws_secret_access_key",
           r"BEGIN [A-Z ]*PRIVATE KEY", r"xox[baprs]-",
           r"ghp_[A-Za-z0-9]{20,}", r"C:\\Users", r"/Users/[A-Za-z]")

offenders: list[str] = []
for p_ in sorted(ROOT.rglob("*")):
    if not p_.is_file() or ".git" in p_.parts:
        continue
    if p_.suffix.lower() in (".png", ".pdf"):
        continue
    if p_.resolve() == Path(__file__).resolve():
        continue
    try:
        t = p_.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue
    for pat in GENERIC:
        if re.search(pat, t):
            offenders.append(f"{p_.relative_to(ROOT).as_posix()}: /{pat}/")

expect("no credential or absolute-path pattern in the public tree",
       not offenders, "; ".join(offenders[:6]))

# --- report ----------------------------------------------------------------
fails = [c for c in checks if not c[0]]
for ok, name, detail in checks:
    print(f"  [{'ok  ' if ok else 'FAIL'}] {name}" + (f"   {detail}" if detail else ""))
print(f"\n{len(checks) - len(fails)}/{len(checks)} checks passed")
if fails:
    print("FAILED:")
    for _, name, detail in fails:
        print(f"  - {name}  {detail}")
sys.exit(1 if fails else 0)
