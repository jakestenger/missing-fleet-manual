#!/usr/bin/env python3
"""How many review rounds each chapter has had, and which ones have hit the cap.

The owner set the policy on 2026-08-27: a chapter gets rounds until it comes back
clean or until it has had five, whichever happens first. A capped chapter stays at
`drafting` rather than being stamped, and a later full-part review is the safety net.

Counting rounds from memory is exactly the kind of bookkeeping this project has already
got wrong once, so count them from the review directories instead. Each round lives in
its own directory under the private reviews tree, and a chapter's rounds are the
directories containing a non-empty `<chapter>-sol.out`.

This reads the private repository, which is not part of the manual. It prints nothing
identifying and is safe to run anywhere; if the directory is absent it says so and exits
cleanly, because a checkout of the public manual alone should not fail here.
"""

import re
import sys
from pathlib import Path

REVIEWS = Path.home() / "Source/Personal/missing-fleet-manual-private/reviews"
MANUAL = Path(__file__).resolve().parent.parent / "manual"
CAP = 5

VERDICT = re.compile(r"^##\s*Verdict\s*$(.*?)(?=^##\s|\Z)", re.M | re.S)


def verdict_of(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return "unreadable"
    match = VERDICT.search(text)
    body = match.group(1) if match else text[:400]
    for candidate in ("READY WITH MINOR CHANGES", "NOT READY", "READY"):
        if candidate in body:
            return candidate
    return "no verdict found"


def main() -> int:
    if not REVIEWS.is_dir():
        print(f"no review directory at {REVIEWS}; nothing to count")
        return 0

    rounds: dict[str, list[tuple[str, str]]] = {}
    for out in sorted(REVIEWS.rglob("*-sol.out")):
        if out.stat().st_size == 0:
            continue
        chapter = out.name[: -len("-sol.out")]
        where = out.parent.relative_to(REVIEWS)
        rounds.setdefault(chapter, []).append((str(where), verdict_of(out)))

    if not rounds:
        print("no completed reviews found")
        return 0

    statuses = {}
    for md in MANUAL.rglob("*.md"):
        m = re.search(r'^section:\s*"?([\d.]+)"?\s*$', md.read_text(encoding="utf-8"), re.M)
        s = re.search(r"^status:\s*(\S+)\s*$", md.read_text(encoding="utf-8"), re.M)
        if m:
            statuses[m.group(1)] = s.group(1) if s else "?"

    def sort_key(chapter: str):
        try:
            return tuple(int(part) for part in chapter.split("."))
        except ValueError:
            return (999,)

    capped, clean, open_ = [], [], []
    for chapter in sorted(rounds, key=sort_key):
        history = rounds[chapter]
        last = history[-1][1]
        n = len(history)
        status = statuses.get(chapter, "?")
        row = (chapter, n, last, status)
        if last in ("READY", "READY WITH MINOR CHANGES"):
            clean.append(row)
        elif n >= CAP:
            capped.append(row)
        else:
            open_.append(row)

    def show(title: str, rows, note: str) -> None:
        if not rows:
            return
        print(f"\n{title}")
        for chapter, n, last, status in rows:
            print(f"  {chapter:<5} {n} round(s)  [{status}]  last: {last}")
        print(f"  {note}")

    total = sum(len(v) for v in rounds.values())
    print(f"{len(rounds)} chapter(s) reviewed, {total} round(s) in total. Cap is {CAP}.")

    show(
        "Last verdict was clean:",
        clean,
        "Stampable IF nothing has changed since that verdict. Check the ledger, not your memory.",
    )
    show(
        "At or past the cap:",
        capped,
        "Leave at drafting. Record the cap in the ledger and move on; the full-part review is the net.",
    )
    show(
        "Still under the cap and not yet clean:",
        open_,
        "These are the ones another round is for.",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
