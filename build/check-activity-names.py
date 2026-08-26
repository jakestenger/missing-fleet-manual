#!/usr/bin/env python3
"""Check that every Fleet activity name the manual prints actually exists.

Written 2026-08-25. A review found `user_mfa_requested` documented in two chapters. No such
activity type exists at fleet-v4.90.1, and no MFA activity is emitted at all. Two more invented
names, `created_setup_experience_script` and `deleted_setup_experience_script`, and a third,
`released_from_ab`, were found by auditing the rest.

That is a different failure from the over-inference this week's other checks target. Nothing was
misread; the names were invented and then printed in a reference table, where a reader would
reasonably build monitoring on them.

Names are read from Fleet's own `activities.go`, so this stays correct across releases as long as
FLEET_SRC points at the tag the manual targets.

Advisory by default; pass --strict to exit 1, which is what CI should do once the path is stable.
"""
import os, re, sys, pathlib

SRC = pathlib.Path(os.environ.get("FLEET_SRC", os.path.expanduser(
    "~/Source/Fleet/fleet-public"))) / "server/fleet/activities.go"
if not SRC.exists():
    print(f"skipped: no Fleet source at {SRC}")
    sys.exit(0)

real = set(re.findall(r'return\s+"([a-z0-9_]+)"', SRC.read_text()))

# Table and column names appear in the same backticked style. They are used to suppress a
# flag, never to decide whether a line is an activity list, because widening that test makes
# every SQL example look like one.
schema = SRC.parent.parent / "datastore/mysql/schema.sql"
identifiers = set()
if schema.exists():
    s = schema.read_text()
    identifiers |= set(re.findall(r"CREATE TABLE `([a-z0-9_]+)`", s))
    identifiers |= set(re.findall(r"^\s+`([a-z0-9_]+)`", s, re.M))
bad = []
for path in sorted(pathlib.Path("manual").rglob("*.md")):
    for n, line in enumerate(path.read_text().split("\n"), 1):
        toks = re.findall(r"`([a-z][a-z0-9_]{4,})`", line)
        if len(toks) < 2:
            continue
        known = [t for t in toks if t in real]
        # Treat a line as an activity list only when most of its tokens are known activity names.
        if len(known) >= 2 and len(known) >= len(toks) * 0.6:
            bad += [(path.name, n, t) for t in toks
                    if t not in real and t not in identifiers]

if bad:
    print(f"{len(bad)} name(s) printed alongside real activity types but absent from the source:\n")
    for name, n, tok in bad:
        print(f"  {name}:{n}  {tok}")
    sys.exit(1 if "--strict" in sys.argv else 0)
print(f"activity names: all verified against {SRC.name}")
sys.exit(0)
