#!/usr/bin/env python3
"""Show every claim the manual already makes about a term.

Two defects this week were chapters contradicting each other while each was internally consistent:
3.1 said an enroll secret decides where a host lands, which 2.7 had already qualified for Apple
enrollment; 3.7 described the update cooldown in a way 8.4 already had right. In both cases the
book contained the correct claim and the new chapter did not consult it.

STYLE §27 says to read a chapter against the book as well as against itself. That is hard to do
from memory across seventy files, so this collects the raw material: every sentence in the manual
mentioning a term, grouped by chapter, ordered so the oldest treatment reads first.

It decides nothing. A human reads the output and notices the disagreement.

    python3 build/claims.py cooldown
    python3 build/claims.py "enroll secret" --context

Run it before writing about a mechanism another chapter probably already covers.
"""
import re, sys, pathlib

def sentences(text):
    return re.split(r"(?<=[.!?])\s+(?=[A-Z*`\[])", text)

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__.strip().split("\n\n")[-1])
        return 2
    term = args[0].lower()
    show_file_context = "--context" in sys.argv

    hits = []
    for path in sorted(pathlib.Path("manual").rglob("*.md")):
        body = path.read_text()
        body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)      # image briefs are specs
        body = re.sub(r"```.*?```", " ", body, flags=re.S)        # code is not a claim
        for para in body.split("\n"):
            s = para.strip()
            if not s or s.startswith(("|", "#")) and not show_file_context:
                if not (s.startswith("|") and term in s.lower()):
                    continue
            for sent in sentences(s):
                if term in sent.lower():
                    hits.append((path, " ".join(sent.split())))

    if not hits:
        print(f'nothing in the manual mentions "{term}"')
        return 0

    print(f'{len(hits)} claim(s) about "{term}", oldest chapter first:\n')
    current = None
    for path, sent in hits:
        if path != current:
            print(f"  {path}")
            current = path
        print(f"    {sent[:300]}")
    print(f"\n  Read these together before adding another. Disagreement between two chapters is")
    print(f"  invisible to every other check in build/.")
    return 0

sys.exit(main())
