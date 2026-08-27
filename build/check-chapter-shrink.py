#!/usr/bin/env python3
"""Catch a chapter that lost a large amount of text without anyone meaning it to.

On 2026-08-27 a scripted edit to 1.2 deleted 131 lines, two whole sections, and every
existing check passed afterwards. Links resolved, because the deleted text contained no
unique link target. Anchors resolved. The frequency and em-dash checkers were happy. The
loss was found by an independent reviewer, a round later, who noticed the chapter now
"jumps from the bundle introduction straight into a diagram whose terms are no longer
defined in visible prose".

The cause is worth naming because it has now happened twice in this project, in the same
shape both times. A `re.sub` with `re.S` and a non-greedy `.*?` will happily run past
everything between its start pattern and a lookahead that appears much later in the file.
The first instance truncated `HANDOFF.md`; this one ate two sections of a chapter.

    # what was written                        # what it matched
    r'\\n\\s+NOTE 2026-08-27:.*?'              a note inside a SCREENSHOT comment
    r'(?=\\n\\s+(?:IMAGE-OK-WAS:|Until it))'   a phrase 131 lines further down

So: run this against a git ref before committing a scripted edit. It is advisory rather
than a gate, because a deliberate cut is legitimate; what it buys you is being told.

    python3 build/check-chapter-shrink.py              # against HEAD
    python3 build/check-chapter-shrink.py <ref>        # against any ref
"""

import subprocess
import sys
from pathlib import Path

MANUAL = Path("manual")
# A chapter losing more than this fraction of its lines is worth a second look. Chosen so
# that ordinary tightening passes quietly and a swallowed section does not.
THRESHOLD = 0.15
FLOOR = 25  # ignore small files and small absolute losses


def at_ref(ref: str, path: str) -> list[str] | None:
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"], capture_output=True, text=True
    )
    if result.returncode != 0:
        return None
    return result.stdout.splitlines()


def main() -> int:
    ref = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
    findings = []

    for path in sorted(MANUAL.rglob("*.md")):
        rel = str(path)
        before = at_ref(ref, rel)
        if before is None:
            continue  # new file
        now = path.read_text(encoding="utf-8").splitlines()
        lost = len(before) - len(now)
        if lost < FLOOR or not before:
            continue
        fraction = lost / len(before)
        if fraction >= THRESHOLD:
            findings.append((rel, len(before), len(now), lost, fraction))

    if not findings:
        print(f"chapter length against {ref}: no unexplained shrinkage")
        return 0

    print(f"{len(findings)} chapter(s) noticeably shorter than at {ref}:\n")
    for rel, was, now, lost, fraction in findings:
        print(f"  {rel}")
        print(f"    {was} -> {now} lines, {lost} lost ({fraction:.0%})")
    print(
        "\nIf you meant it, carry on. If you did not, the usual cause is a dot-all regex\n"
        "whose lookahead matched far later in the file than you expected. Recover with\n"
        f"  git diff {ref} -- <file> | grep '^-' | grep -v '^---' | sed 's/^-//'\n"
        "and re-source-check the restored text rather than trusting it because it is old."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
