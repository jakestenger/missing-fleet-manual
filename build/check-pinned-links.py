#!/usr/bin/env python3
"""Fail on a link into Fleet's repository that points at a moving branch.

The manual states what Fleet does at one release. A link to `blob/main` promises the reader
a source for a claim and then hands them a file that has since changed, which is worse than
no link: it looks like a citation and behaves like a guess.

Every `github.com/fleetdm/fleet/blob/<ref>/` link must name the tag this manual is verified
against. Sixteen such links were found unpinned across seven chapters on 2026-08-27, five of
them in a chapter whose review had already asked for four of them to be pinned.
"""
import re, sys, pathlib

TAG = "fleet-v4.90.0"
PAT = re.compile(r"github\.com/fleetdm/fleet/blob/([^/\s)\]`]+)/")

problems = []
for path in sorted(pathlib.Path("manual").rglob("*.md")):
    for i, line in enumerate(path.read_text().splitlines(), 1):
        for m in PAT.finditer(line):
            if m.group(1) != TAG:
                problems.append((path, i, m.group(1)))

if problems:
    print(f"{len(problems)} repository link(s) not pinned to {TAG}:\n")
    for path, i, ref in problems:
        print(f"  {path}:{i}  points at '{ref}'")
    sys.exit(1)
print(f"repository links: all pinned to {TAG}")
sys.exit(0)
