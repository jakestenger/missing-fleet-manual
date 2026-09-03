#!/usr/bin/env python3
"""Guard the retired per-chapter verification stamps.

Per-chapter status tracking was retired on 2026-09-03 by the owner's decision. The book is now
versioned as a whole, per minor release (4.90.x, 4.91.x, ...), selectable from a nav-bar
dropdown, so a per-chapter `status:` field tracks nothing the reader can use. The
reviewer-attribution pair `reviewed_by:` / `reviewed_on:` went with it: no reviewer should feel
obligated to sign a chapter and carry the blame for a later-found mistake.

What remains is the release-provenance triple, which every chapter keeps:
`verified_against` (the release the content was checked against), `verified_on`, and
`verified_source`. That records what the content was written against; it never claimed a review
pass, so nothing is lost by dropping the retired stamps.

This check used to enforce the status ladder and the `verified` stamp. Its job now is the
inverse: make sure none of the three retired keys drift back into a chapter's frontmatter. It is
a gate rather than advice, because a reintroduced `status:` would quietly resurrect a model the
book no longer runs. Exits 1 on any retired key found; otherwise reports clean.
"""
import re, sys, pathlib

MANUAL = pathlib.Path("manual")

# The exact top-level keys retired on 2026-09-03. Anchored so `verified_on` (kept) is never
# matched by `reviewed_on`, and indented list children (e.g. under further_reading) are ignored.
RETIRED = ("status", "reviewed_by", "reviewed_on")
RETIRED_RE = re.compile(rf"^({'|'.join(RETIRED)}):", re.M)

offenders = []
for path in sorted(MANUAL.rglob("*.md")):
    parts = path.read_text(encoding="utf-8").split("---")
    if len(parts) < 3:
        continue
    fm = parts[1]
    found = sorted({m.group(1) for m in RETIRED_RE.finditer(fm)})
    if found:
        offenders.append((path, found))

if offenders:
    print(f"{len(offenders)} chapter(s) carry a retired per-chapter verification key "
          "(status / reviewed_by / reviewed_on):\n")
    for path, found in offenders:
        print(f"  {path}: {', '.join(found)}")
    print("\nThese were retired 2026-09-03; the book is versioned as a whole now. Remove the key\n"
          "and keep only verified_against / verified_on / verified_source.")
    sys.exit(1)

print("verification stamps: no retired per-chapter status/reviewed keys; "
      "every chapter carries only whole-book release provenance")
sys.exit(0)
