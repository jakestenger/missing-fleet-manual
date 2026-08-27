#!/usr/bin/env python3
"""An image whose rendered content contradicts the prose is a defect in the chapter.

Assets are marked `IMAGE-OK` once a human has looked at the rendered result and
accepted it. That acceptance is against the prose as it stood, so a correction to
the prose can invalidate it: on 2026-08-27 the five-channel diagram in 1.2 still
read "Five channels. They fail independently" and "every 10 to 30 seconds" after
the chapter had retracted both claims. The reviewer that had originally said to
leave the asset alone retracted that advice once the text changed.

`CONTRIBUTING.md` already had the marker for this: `IMAGE-REDO:` with a `WHY:` line.
What was missing was anything that made it bite. This checker makes the debt block a
`verified` stamp, in the same way `check-verified.py` gates the ladder, so an image
cannot quietly stay wrong because regenerating it is inconvenient.

It also insists on the `WHY:` line, because an `IMAGE-REDO` with no stated reason is
a marker nobody can act on later.

A chapter at `outline` or `drafting` may carry one. A chapter at `verified` may not.
"""

import re
import sys
from pathlib import Path

MANUAL = Path(__file__).resolve().parent.parent / "manual"

MARKER = re.compile(r"<!--\s*IMAGE-REDO:\s*(\S+)\n(.*?)(?=\n\s*(?:PROMPT|NOTE|Caption)\b)", re.S)
STATUS = re.compile(r"^status:\s*(\S+)\s*$", re.M)


def main() -> int:
    pending: list[tuple[Path, str, str]] = []
    for path in sorted(MANUAL.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        marks = MARKER.findall(text)
        if not marks:
            continue
        status_match = STATUS.search(text)
        status = status_match.group(1) if status_match else "unknown"
        for asset, body in marks:
            has_why = "WHY:" in body
            pending.append((path, status, asset, has_why))

    if not pending:
        print("IMAGE-REDO: nothing outstanding")
        return 0

    blocking = [row for row in pending if row[1] == "verified"]
    unexplained = [row for row in pending if not row[3]]

    print(f"{len(pending)} asset(s) marked IMAGE-REDO:\n")
    for path, status, asset, has_why in pending:
        rel = path.relative_to(MANUAL.parent)
        flag = "  BLOCKS VERIFIED" if status == "verified" else ""
        why = "" if has_why else "  NO WHY: LINE"
        print(f"  {rel}  [{status}]{flag}{why}")
        print(f"    {asset}")

    if unexplained:
        print(
            "\nAn IMAGE-REDO with no WHY: line is a marker nobody can act on. Say what the\n"
            "rendered picture asserts that the prose no longer does."
        )
        return 1

    if blocking:
        print(
            "\nA verified chapter may not carry an IMAGE-REDO marker. The rendered image is\n"
            "part of what the stamp vouches for. Regenerate it from the prompt in the comment,\n"
            "look at the result, and change the marker back to IMAGE-OK."
        )
        return 1

    print(
        "\nNone of these is in a verified chapter, so none blocks. Each is still a claim\n"
        "the chapter makes in a picture and no longer makes in words."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
