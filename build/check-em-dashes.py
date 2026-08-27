#!/usr/bin/env python3
"""Fail on an em-dash in the manual.

STYLE forbids them. Eleven had accumulated by 2026-08-27, ten of them written that day, which
is what a rule with no check behind it looks like after one long session. Rendered assets are a
separate problem: an em-dash baked into a generated image cannot be caught here.

An en-dash in a numeric range is left alone; this checks the em-dash only.
"""
import io, sys, pathlib

hits = []
for path in sorted(pathlib.Path("manual").rglob("*.md")):
    for i, line in enumerate(io.open(path, encoding="utf-8").read().split("\n"), 1):
        if "—" in line:
            hits.append((path, i, line.strip()[:140]))

if hits:
    print(f"{len(hits)} line(s) containing an em-dash, which STYLE forbids:\n")
    for path, i, line in hits:
        print(f"  {path}:{i}\n    {line}")
    sys.exit(1)
print("em-dashes: none in manual/")
sys.exit(0)
