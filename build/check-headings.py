#!/usr/bin/env python3
"""Flag headings that assert more than the section beneath them.

Written 2026-08-25. Two of the twelve Part II defects were correct prose under an incorrect
heading. Per-claim verification is structurally blind to this: the verified claim is the one in
the paragraph, and nothing ever re-reads the heading against it.

  "An Android host has no serial number"
      ... over a paragraph correctly scoped to "a personally owned Android device enrolled with
      a work profile". Company-owned enrollment was never checked.

  "Object storage becomes mandatory when you add the second instance"
      ... over a body explaining that carves fall back to MySQL, which is shared and survives
      multiple instances perfectly well.

Term overlap does not find these; the words match fine. What separates them is that the heading
states something unconditionally while the body qualifies it. A reader skimming headings gets the
unconditional version, which is exactly the reader most likely to act on it.

Advisory. Always exits 0.
"""
import re, sys, pathlib

ABSOLUTE = re.compile(
    r"\b(no|never|always|every|all|none|neither|nothing|only|must|cannot|mandatory|required|"
    r"any|exactly|impossible)\b", re.I)

# Scope limiters. If the body leans on these and the heading does not, the heading is broader
# than what it introduces.
QUALIFIER = re.compile(
    r"\b(personally|company-owned|unless|except|only if|only when|when you|if you|"
    r"provided|depends on|varies|in most|usually|typically|by default|at this release|"
    r"on macOS|on Windows|on Android|on Linux|for macOS|for Windows|self-hosted|managed cloud|"
    r"falls? back|fall back|conditional|assuming)\b", re.I)

MANUAL = pathlib.Path("manual")
flagged = []

for path in sorted(MANUAL.rglob("*.md")):
    text = re.sub(r"<!--.*?-->", " ", path.read_text(), flags=re.S)
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    parts = re.split(r"^(#{2,3} .+)$", text, flags=re.M)
    for i in range(1, len(parts), 2):
        heading = parts[i].lstrip("# ").strip()
        body = parts[i + 1] if i + 1 < len(parts) else ""
        if not ABSOLUTE.search(heading):
            continue
        quals = {q.group(0).lower() for q in QUALIFIER.finditer(body)}
        # Anything the heading itself already says is not a mismatch.
        quals = {q for q in quals if q not in heading.lower()}
        if len(quals) >= 1:
            flagged.append((path, heading, sorted(quals)[:6],
                            " ".join(body.split())[:150]))

if flagged:
    print(f"{len(flagged)} heading(s) asserting more than the section qualifies:\n")
    for path, heading, quals, opening in flagged:
        print(f"  {path.name}")
        print(f"    heading: {heading}")
        print(f"    body qualifies with: {', '.join(quals)}")
        print(f"    body opens: {opening}\n")
else:
    print("headings: none assert more than their section qualifies")
sys.exit(0)
