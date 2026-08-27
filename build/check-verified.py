#!/usr/bin/env python3
"""Report sections claiming verification they have not had.

`status: verified` means two things since 2026-08-25: claims were checked against a release tag,
and an independent review pass ran and its findings were resolved. Twelve chapters previously
carried the stamp on the first alone, and an external review found a material defect in every one.

Checks that a verified section has its `verified_*` fields, a notes file, and `reviewed_by` /
`reviewed_on`. Exits 1 on a section that overclaims, because this one is a gate rather than
advice.

**A freeze is in force from 2026-08-27, by the owner's decision: nothing carries `verified`
until every part is drafted and every chapter has had at least one review round.** The reason
is that the stamp kept going stale through no fault of the chapter carrying it. Writing a Part
III chapter found real errors in Part I; reviewing Part I found real errors in Part II. Twelve
chapters were demoted in one day, eight of them because a neighbour's review corrected them
hours after their own verdict. A stamp that a neighbour can invalidate is not measuring what it
claims to, and while whole parts are still outlines every chapter has neighbours that do not
exist yet.

Lift the freeze by deleting FREEZE below, once the condition it names is met.
"""
import re, sys, pathlib

MANUAL, NOTES = pathlib.Path("manual"), pathlib.Path("research/section-notes")
problems = []

# The ladder has exactly three rungs. A section reached `status: written` once, which is not a
# rung, so it sat outside every check here: it claimed nothing this file tests and nothing the
# ladder means. Anything that is not one of these three is a typo or an invention, and both
# are worth failing on.
LADDER = {"outline", "drafting", "verified"}
offladder = []

# See the module docstring. Set to False once every part is drafted and every chapter has had a
# review round; until then a `verified` stamp is premature by definition rather than by evidence.
FREEZE = True
frozen = []

for path in sorted(MANUAL.rglob("*.md")):
    head = path.read_text().split("---")
    if len(head) < 3:
        continue
    fm = head[1]
    m = re.search(r"^status:\s*(\S+)\s*$", fm, re.M)
    if not m:
        offladder.append((path, "no status field"))
    elif m.group(1) not in LADDER:
        offladder.append((path, m.group(1)))
    elif FREEZE and m.group(1) == "verified":
        frozen.append(path)
    if not re.search(r"^status:\s*verified\s*$", fm, re.M):
        continue
    def has(field):
        m = re.search(rf"^{field}:\s*(\S.*)$", fm, re.M)
        return bool(m and m.group(1).strip() not in {'""', "''", "~", "null"})
    missing = [f for f in ("verified_against", "verified_on", "verified_source",
                           "reviewed_by", "reviewed_on") if not has(f)]
    sec = re.search(r'^section:\s*"?([\d.a-z]+)"?', fm, re.M)
    note = None
    if sec:
        hits = list(NOTES.glob(f"{sec.group(1)}-*.md"))
        note = hits[0] if hits else None
        if not hits:
            missing.append("a notes file in research/section-notes/")
    if missing:
        problems.append((path, missing))

if offladder:
    print(f"{len(offladder)} section(s) with a status outside the ladder "
          "(outline, drafting, verified):\n")
    for path, got in offladder:
        print(f"  {path}: {got}")
    print()

if problems:
    print(f"{len(problems)} section(s) stamped verified without the evidence:\n")
    for path, missing in problems:
        print(f"  {path}")
        for m in missing:
            print(f"    missing: {m}")
        print()

if frozen:
    print(f"{len(frozen)} section(s) stamped verified while the freeze is in force:\n")
    for path in frozen:
        print(f"  {path}")
    print("\nNothing carries `verified` until every part is drafted and every chapter has had a\n"
          "review round. Set it to `drafting`, or lift the freeze in this file if the condition\n"
          "has actually been met.\n")

if problems or offladder or frozen:
    sys.exit(1)

if FREEZE:
    print("verified stamps: none, and none permitted while the freeze holds; "
          "every status is on the ladder")
else:
    print("verified stamps: all backed by a source check and a review pass; "
          "every status is on the ladder")
sys.exit(0)
