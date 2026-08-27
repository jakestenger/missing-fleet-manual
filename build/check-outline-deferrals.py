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

# A pointer and a promise are different failures. "See a.4" costs the reader one click into a
# stub. "The full action-by-action breakdown for all six roles is in a.4" tells them the answer
# exists and names it, which is the one that wastes their time and misrepresents the manual.
PROMISE = re.compile(
    r"\b(?:every|full|complete|exact|exhaustive|all (?:six|the)|action-by-action|per-action|"
    r"enumerat\w+|the detail|detailed)\b", re.I)

hits = []
LINK = re.compile(r"\[[^\]]+\]\(([^)]+\.md)(?:#[^)]*)?\)")
for path in sorted(MANUAL.rglob("*.md")):
    if path.name in outline:
        continue
    text = path.read_text()
    verified = bool(re.search(r"^status:\s*verified\s*$", text.split("---")[1], re.M)) \
        if len(text.split("---")) > 2 else False
    for i, line in enumerate(text.split("\n"), 1):
        for m in LINK.finditer(line):
            target = pathlib.PurePath(m.group(1)).name
            if target in outline:
                hits.append((path, i, target, line.strip()[:120],
                             bool(PROMISE.search(line)), verified))

if hits:
    promises = [h for h in hits if h[4]]
    in_verified = [h for h in hits if h[5]]
    print(f"{len(hits)} reference(s) into a chapter that is still an outline stub. "
          f"{len(promises)} promise specific content; {len(in_verified)} are in a chapter "
          f"stamped verified.\n")
    for path, i, target, line, promise, ver in hits:
        tags = "".join(t for t in ("  [PROMISE]" if promise else "",
                                   "  [IN VERIFIED CHAPTER]" if ver else ""))
        print(f"  {path}:{i}  -> {target}{tags}\n    {line}")
    print("\nAdvisory. A bare pointer into a planned chapter is legitimate. A [PROMISE] is not:\n"
          "either write the target, or stop naming content that does not exist. A [PROMISE] inside\n"
          "a verified chapter is a defect in a verified chapter.")
else:
    print("outline deferrals: none")
sys.exit(0)
