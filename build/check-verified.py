#!/usr/bin/env python3
"""Report sections claiming verification they have not had.

`status: verified` means two things since 2026-08-25: claims were checked against a release tag,
and an independent review pass ran and its findings were resolved. Twelve chapters previously
carried the stamp on the first alone, and an external review found a material defect in every one.

Checks that a verified section has its `verified_*` fields, a notes file, and `reviewed_by` /
`reviewed_on`. Exits 1 on a section that overclaims, because this one is a gate rather than
advice.
"""
import re, sys, pathlib

MANUAL, NOTES = pathlib.Path("manual"), pathlib.Path("research/section-notes")
problems = []

for path in sorted(MANUAL.rglob("*.md")):
    head = path.read_text().split("---")
    if len(head) < 3:
        continue
    fm = head[1]
    if not re.search(r"^status:\s*verified\s*$", fm, re.M):
        continue
    def has(field):
        m = re.search(rf"^{field}:\s*(\S.*)$", fm, re.M)
        return bool(m and m.group(1).strip() not in {'""', "''", "~", "null"})
    missing = [f for f in ("verified_against", "verified_on", "verified_source",
                           "reviewed_by", "reviewed_on") if not has(f)]
    sec = re.search(r'^section:\s*"?([\d.a-z]+)"?', fm, re.M)
    note = None
    if sec:
        hits = list(NOTES.glob(f"{sec.group(1)}-*.md"))
        note = hits[0] if hits else None
        if not hits:
            missing.append("a notes file in research/section-notes/")
    if missing:
        problems.append((path, missing))

if problems:
    print(f"{len(problems)} section(s) stamped verified without the evidence:\n")
    for path, missing in problems:
        print(f"  {path}")
        for m in missing:
            print(f"    missing: {m}")
        print()
    sys.exit(1)
print("verified stamps: all backed by a source check and a review pass")
sys.exit(0)
