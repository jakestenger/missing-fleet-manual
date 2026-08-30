#!/usr/bin/env python3
"""Check that every Fleet cron schedule name the manual prints actually exists.

Written 2026-08-25, the same day two invented schedule names were found:
`software_checksum_migration` and `windows_maintained_app_titles`, neither of which appears
anywhere in Fleet's source. Both sat in a list a reader would use with `fleetctl trigger --name`,
so the failure mode was a command that could never work against a schedule that never existed.

This is the third checker built from an observed fabrication rather than an imagined risk, after
check-activity-names.py and check-crossrefs.py. The shape is the same: read the canonical
identifiers from Fleet's own source so the check tracks the release, then report names the manual
prints alongside verified ones that the source does not define.

Advisory by default; --strict exits 1.
"""
import os, re, sys, pathlib

SRC = pathlib.Path(os.environ.get("FLEET_SRC", os.path.expanduser(
    "~/Source/Fleet/fleet-public"))) / "server/fleet/cron_schedules.go"
if not SRC.exists():
    print(f"skipped: no Fleet source at {SRC}")
    sys.exit(0)

real = set(re.findall(r'CronScheduleName\s*=\s*"([a-z0-9_]+)"', SRC.read_text()))
# One schedule is registered by string literal rather than a CronScheduleName constant
# (service discovery, cmd/fleet/cron.go), so the constants list under-counts by one.
real.add("mdm_service_discovery")
if not real:
    print("skipped: no schedule names found in source; the declaration shape may have changed")
    sys.exit(0)

# Table and column names sit beside schedule names legitimately, as cron_stats does. Read them
# from the schema and use them only to suppress a flag, never to decide whether a line is a
# schedule list; counting them the other way made every SQL example look like one when this was
# first tried for activity names.
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
        known = [t for t in toks if t in real]
        # A line is a schedule list only when most of its identifiers are known schedule names.
        if len(known) >= 2 and len(known) >= len(toks) * 0.6:
            bad += [(path.name, n, t) for t in toks
                    if t not in real and t not in identifiers]

if bad:
    print(f"{len(bad)} name(s) printed alongside real schedules but absent from the source:\n")
    for name, n, tok in bad:
        print(f"  {name}:{n}  {tok}")
    sys.exit(1 if "--strict" in sys.argv else 0)
print(f"schedule names: all {len(real)} verified against {SRC.name}")
sys.exit(0)
