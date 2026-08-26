#!/usr/bin/env python3
"""Check that every MySQL table the manual names actually exists.

Written 2026-08-25, after a review of 8.9 reported that its database reference "names objects that
do not exist". Part VIII prints SQL a reader runs during an incident, so a table that was renamed,
never existed, or belongs to a different release sends someone to an error at the worst moment.

Fourth checker built from an observed fabrication, after activity names, schedule names, and
cross-reference targets. Same shape: read the canonical set from Fleet's own schema so the check
tracks the release rather than a snapshot.

**Two SQL dialects appear in this manual and only one is in scope.** Part VIII prints osquery
queries, run against a host, alongside MySQL queries run against Fleet's database. `os_version`
and `processes` are real osquery tables and would be false positives against a MySQL schema. So a
block is judged only when it already names at least one real Fleet table, which is what marks it
as a Fleet-database query; unknown names in that block are then genuinely suspicious.

That heuristic is the same one used by the activity and schedule checkers, and it was learned by
getting it wrong: the first version of this check reported twenty-five osquery tables as missing.

Advisory by default; --strict exits 1.
"""
import os, re, sys, pathlib

SRC = pathlib.Path(os.environ.get("FLEET_SRC", os.path.expanduser(
    "~/Source/Fleet/fleet-public"))) / "server/datastore/mysql/schema.sql"
if not SRC.exists():
    print(f"skipped: no Fleet schema at {SRC}")
    sys.exit(0)

schema = SRC.read_text()
tables = set(re.findall(r"CREATE TABLE `([a-z0-9_]+)`", schema))
tables |= set(re.findall(r"CREATE(?:\s+ALGORITHM=\S+)?.*?VIEW `([a-z0-9_]+)`", schema))
if not tables:
    print("skipped: no tables found; the schema dump format may have changed")
    sys.exit(0)

# Names that legitimately appear in FROM/JOIN position without being Fleet tables.
ALLOW = {"dual"}

bad = []
for path in sorted(pathlib.Path("manual").rglob("*.md")):
    text = path.read_text()
    # Only look inside fenced blocks that are actually SQL.
    for block in re.findall(r"```[a-z]*\n(.*?)```", text, re.S):
        if not re.search(r"\b(FROM|JOIN)\b", block, re.I):
            continue
        # Judge only blocks that query Fleet's database, identified by naming a Fleet table.
        named = {m.group(1).lower() for m in
                 re.finditer(r"\b(?:FROM|JOIN)\s+`?([a-z][a-z0-9_]*)`?", block, re.I)}
        if not (named & tables):
            continue
        for m in re.finditer(r"\b(?:FROM|JOIN)\s+`?([a-z][a-z0-9_]*)`?", block, re.I):
            name = m.group(1).lower()
            if name in tables or name in ALLOW:
                continue
            # Subquery aliases and CTEs are defined in the block itself.
            if re.search(rf"\bAS\s+{re.escape(name)}\b|\b{re.escape(name)}\s+AS\s*\(", block, re.I):
                continue
            line = path.read_text()[:text.index(block)].count("\n") + 1
            bad.append((path.name, line, name))

if bad:
    seen = set()
    uniq = [b for b in bad if not (b[2] in seen or seen.add(b[2]))]
    print(f"{len(uniq)} table name(s) queried in the manual but absent from Fleet's schema:\n")
    for name, line, tok in uniq:
        print(f"  {name}: near line {line}  ->  {tok}")
    sys.exit(1 if "--strict" in sys.argv else 0)
print(f"table names: all queried tables exist among the {len(tables)} in schema.sql")
sys.exit(0)
