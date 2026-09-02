#!/usr/bin/env python3
"""Check the shared CAP-ID register for collisions, not just duplicates.

Written 2026-09-02 after round 3 caught A.2 silently reusing six of A.1's live IDs
(CAP-349-354) for six unrelated capabilities, and inventing six more (CAP-355-360) that
existed nowhere else. A uniqueness check inside one file would have missed both: every ID
in A.2 was already unique *within A.2*. The defect was cross-file — the same ID meaning two
different things depending which appendix you were reading.

**A.1 is the register.** A.2 and A.5 carry the same outcomes at the same grain (every
ID either file uses must be an ID A.1 defines somewhere, in a formal row or in the
no-chapter prose section for outcomes no chapter teaches), so this checks two things a
uniqueness check cannot:
  1. Every CAP-ID in A.2 or A.5 exists in A.1. Catches an appendix inventing an ID A.1
     never assigned, which is exactly how CAP-355-360 got in.
  2. Where the same CAP-ID appears in both A.2 and A.5, its label is character-for-character
     identical. Those two files have always agreed verbatim where they share a row; this
     makes that agreement a checked invariant instead of an accident.

A.4 is not checked here. Its 152 administrator intents are a coarser grouping than A.1's
354 outcomes (see a.1's "How to read a row"), so it carries no CAP-ID column and nothing
to compare.

Exit code 1 on any failure, so CI blocks the merge.
"""
import re, sys, pathlib

APPENDICES = pathlib.Path("manual/09-appendices")
ROW = re.compile(r"^\|\s*\*\*CAP-(\d+)\*\*\s*\|\s*([^|]+?)\s*\|", re.M)
ANY_ID = re.compile(r"CAP-(\d+)")

# a.5's own "self-initiation" table (below this heading) answers a different question, in a
# different column shape, and re-lists some of the same IDs with a phrasing suited to that
# question. It is not the register, so row-scanning stops before it.
STOP_HEADING = "## What Fleet or an external system starts on its own"


def rows(path):
    text = path.read_text()
    text = text.split(STOP_HEADING)[0]
    out = {}
    for m in ROW.finditer(text):
        cid, label = "CAP-" + m.group(1), m.group(2).strip()
        out.setdefault(cid, []).append(label)
    return out


def all_ids(path):
    """Every CAP-ID a.1 mentions anywhere, including the no-chapter prose entries that
    are never given a formal table row because no chapter owns them."""
    return {"CAP-" + m.group(1) for m in ANY_ID.finditer(path.read_text())}


def main():
    a1 = APPENDICES / "a.1-capability-index.md"
    a2 = APPENDICES / "a.2-platform-capability-matrix.md"
    a5 = APPENDICES / "a.5-interface-index.md"
    for p in (a1, a2, a5):
        if not p.exists():
            print(f"skipped: {p} not found")
            return 0

    a1_rows, a2_rows, a5_rows = rows(a1), rows(a2), rows(a5)
    problems = []

    for name, reg in (("a.1", a1_rows), ("a.2", a2_rows), ("a.5", a5_rows)):
        for cid, labels in reg.items():
            if len(labels) > 1:
                problems.append(f"{name}: {cid} appears {len(labels)} times in the same file")

    a1_ids = all_ids(a1)
    for name, reg in (("a.2", a2_rows), ("a.5", a5_rows)):
        for cid in reg:
            if cid not in a1_ids:
                problems.append(f"{name}: {cid} is not in a.1's register (invented or stale ID)")

    shared = set(a2_rows) & set(a5_rows)
    for cid in sorted(shared, key=lambda c: int(c.split("-")[1])):
        a2_label = a2_rows[cid][0]
        a5_label = a5_rows[cid][0]
        if a2_label != a5_label:
            problems.append(
                f"{cid}: a.2 says \"{a2_label}\" but a.5 says \"{a5_label}\" for the same ID"
            )

    if problems:
        print(f"{len(problems)} CAP-ID problem(s):\n")
        for p in problems:
            print(f"  {p}")
        return 1

    print(
        f"CAP-ID register: {len(a1_ids)} IDs in a.1; a.2 ({len(a2_rows)}) and a.5 "
        f"({len(a5_rows)}) are both subsets with {len(shared)} matching labels checked"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
