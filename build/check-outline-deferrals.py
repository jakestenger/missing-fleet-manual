#!/usr/bin/env python3
"""Report prose that defers detail to a chapter which is still an outline stub.

`check-links.py` proves the target file exists. It cannot tell that the target is a 50-word
placeholder, so "exact flags are in a.7" reads as a promise and delivers a heading list. Four
chapters deferred to a.7 that way, and a reviewer found it before any reader did.

Advisory rather than a gate: a forward reference to a chapter that is genuinely planned is
legitimate, and the fix is to say so rather than to delete the pointer. This lists them so the
choice is deliberate.
"""
import io, re, sys, pathlib

MANUAL = pathlib.Path("manual")

outline = {}
for path in MANUAL.rglob("*.md"):
    parts = path.read_text().split("---")
    if len(parts) < 3:
        continue
    if re.search(r"^status:\s*outline\s*$", parts[1], re.M):
        outline[path.name] = path

hits = []
LINK = re.compile(r"\[[^\]]+\]\(([^)]+\.md)(?:#[^)]*)?\)")
for path in sorted(MANUAL.rglob("*.md")):
    if path.name in outline:
        continue
    for i, line in enumerate(path.read_text().split("\n"), 1):
        for m in LINK.finditer(line):
            target = pathlib.PurePath(m.group(1)).name
            if target in outline:
                hits.append((path, i, target, line.strip()[:120]))

if hits:
    print(f"{len(hits)} reference(s) into a chapter that is still an outline stub:\n")
    for path, i, target, line in hits:
        print(f"  {path}:{i}  -> {target}\n    {line}")
    print("\nAdvisory. Either say the target is not written yet, or point somewhere that answers today.")
else:
    print("outline deferrals: none")
sys.exit(0)
