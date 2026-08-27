#!/usr/bin/env python3
"""Check that every aliased column reference in the manual's SQL exists in Fleet's schema.

Written 2026-08-26, during the 8.1-8.10 re-verification at fleet-v4.90.1. That sweep found
that Part VIII prints column inventories for roughly twenty tables, that `check-table-names.py`
covers table *names* and nothing covers columns, and that a human comparing twenty column lists
against a 221-table schema will not stay accurate. A wrong column name in a runnable query is
the same defect class as 8.13's `nano_command_queue`: it looks authoritative and it does not run.

**Why this one works where the prose checker did not.** `check-table-names.py` was extended into
prose once and produced 37 false positives and 0 true positives, because Fleet legitimately spells
config keys, MDM asset names and activity types as backticked snake_case in the same paragraphs
(see CONTRIBUTING.md). This checker never looks at prose. It reads only ```sql fenced blocks, and
only `alias.column` references where the alias is bound by a FROM or JOIN in the same block. That
binding is what removes the ambiguity: the table is not guessed, it is declared two lines up.

Unaliased columns are deliberately ignored. In a multi-table query they cannot be attributed
without parsing SQL scope, and guessing is how a checker earns a reputation for noise.

Advisory by default; --strict exits 1.
"""
import os, re, sys, pathlib

SRC = pathlib.Path(os.environ.get("FLEET_SRC", os.path.expanduser(
    "~/Source/Fleet/fleet-public"))) / "server/datastore/mysql/schema.sql"
if not SRC.exists():
    print(f"skipped: no Fleet schema at {SRC}")
    sys.exit(0)

# table -> set(columns), read from Fleet's own schema so the check tracks the release.
schema, table = {}, None
for line in SRC.read_text().split("\n"):
    m = re.match(r"CREATE TABLE `([a-z0-9_]+)`", line)
    if m:
        table = m.group(1)
        schema[table] = set()
        continue
    if table:
        c = re.match(r"\s+`([a-z0-9_]+)`\s+\S", line)
        if c:
            schema[table].add(c.group(1))
        elif line.startswith(")"):
            table = None

if not schema:
    print("skipped: no tables parsed; the schema dump's shape may have changed")
    sys.exit(0)

# Views are real objects the manual queries (nano_view_queue) but carry no CREATE TABLE, so any
# alias bound to an unknown name is skipped rather than reported. Same for derived tables.
FENCE = re.compile(r"```sql\n(.*?)```", re.S)
BIND = re.compile(r"\b(?:FROM|JOIN)\s+([a-z0-9_]+)\s+(?:AS\s+)?([a-z][a-z0-9_]*)\b", re.I)
REF = re.compile(r"\b([a-z][a-z0-9_]*)\.([a-z][a-z0-9_]*)\b")
# SQL keywords that can follow FROM/JOIN and are not aliases.
NOT_ALIAS = {"on", "where", "order", "group", "left", "right", "inner", "outer", "join",
             "using", "as", "union", "limit", "having", "set", "select"}

bad = []
for path in sorted(pathlib.Path("manual").rglob("*.md")):
    text = path.read_text()
    for block in FENCE.finditer(text):
        sql = block.group(1)
        line0 = text[:block.start()].count("\n") + 1
        aliases = {a.lower(): t for t, a in BIND.findall(sql) if a.lower() not in NOT_ALIAS}
        if not aliases:
            continue
        for alias, col in REF.findall(sql):
            t = aliases.get(alias.lower())
            if t is None or t not in schema:      # unbound alias, or a view
                continue
            if col not in schema[t]:
                n = line0 + sql[:sql.find(f"{alias}.{col}")].count("\n")
                bad.append((path.name, n, f"{alias}.{col}", t))

if bad:
    print(f"{len(bad)} column reference(s) not present in the aliased table:\n")
    for name, n, ref, t in bad:
        print(f"  {name}:{n}  {ref}  (no column `{ref.split('.')[1]}` in `{t}`)")
    sys.exit(1 if "--strict" in sys.argv else 0)

checked = sum(len(v) for v in schema.values())
print(f"column names: aliased references all exist, against {len(schema)} tables "
      f"({checked} columns) in {SRC.name}")
sys.exit(0)
