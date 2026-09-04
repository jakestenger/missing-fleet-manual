#!/usr/bin/env python3
"""Recompute a.5's derived register tallies from its matrix and fail on drift.

Written 2026-09-04 (round 9 prep) after round 8 caught a.5's narrative counts drifting from
its own matrix once more: two cells were rescored against the tag and five derived figures had
to be recounted by hand (rows-with-any-`Not established` 72 to 70, the UI `Not established` total
70 to 69, the `Partial` total 252 to 253, the more-than-one-column group 14 to 13, and section N
22 to 23 rows). Every one of those is a number a reader trusts and none had a check behind it, so
the same recount-drift class had surfaced in some form every round a cell moved.

`check-cap-ids.py` already recomputes a.5's five-value-by-four-interface count table, its total
row count, and the no-supported-interface / all-four-agree / readable cross-counts. This check
does NOT repeat those. It covers the derived tallies that one leaves untouched, each recomputed
from the same matrix cells and asserted against the figure a.5 states in prose:

  1. The `Partial` total across all four columns ("appears N times across the four columns").
  2. The "Where exactly one interface can do it" table: for each interface, the count of rows
     where it is the only column that can act (`Full` or `Partial`), the rest cannot.
  3. Rows carrying at least one `Not established` cell, and the claim that no row carries four.
  4. Rows unsettled in more than one column (two or more `Not established` cells).
  5. The UI column's `Not established` figure as stated in the closing prose.
  6. Section N's row count and the claim that GitOps can act on none of those rows, plus a
     structural check that every matrix row falls under exactly one lettered section (the
     per-section counts sum to the matrix total).

Each figure is parsed from prose as either digits or the English words a.5 spells them in
(`Seventy`, `Thirteen`, `twenty-three`), so a reworded number is caught rather than skipped, and
a missing anchor sentence is itself a failure so quietly deleting the prose cannot disable a check.

The matrix cell parser mirrors `check-cap-ids.py` exactly: the four interface cells per CAP row,
stopping before the self-initiation table (a different question in the same column shape).

Exit code 1 on any failure, so CI blocks the merge.
"""
import re, sys, pathlib

A5_PATH = pathlib.Path("manual/09-appendices/a.5-interface-index.md")

# a.5's self-initiation table re-lists some IDs in the same column shape to answer a different
# question, so the matrix scan stops before it — the same boundary check-cap-ids.py uses.
STOP_HEADING = "## What Fleet or an external system starts on its own"

# Four interface cells (UI, REST API, fleetctl, GitOps) per CAP row, including lettered split
# rows (CAP-244a/b/c, CAP-341a/b). Identical to check-cap-ids.py's A5_CELL_ROW.
CELL_ROW = re.compile(
    r"^\|\s*\*\*CAP-\d+[a-z]?\*\*\s*\|[^|]*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|",
    re.M,
)
SECTION_HEADER = re.compile(r"^\|\s*\*\*([A-Z])\.\s")

CAN = {"Full", "Partial"}  # "can act"; Read only / Unsupported / Not established are "cannot"
INTERFACES = ("UI", "REST API", "fleetctl", "GitOps")  # matrix column order

# English number words, spelled the way a.5 spells its counts (matches check-cap-ids.py's _words).
_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
_TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def _words(n):
    if n < 20:
        return _ONES[n]
    if n < 100:
        t, o = divmod(n, 10)
        return _TENS[t] + ("-" + _ONES[o] if o else "")
    h, r = divmod(n, 100)
    return _ONES[h] + " hundred" + (" and " + _words(r) if r else "")


WORD2NUM = {_words(n): n for n in range(1000)}


def parse_count(token):
    """A prose count token to an int: '253' or 'Thirteen' or 'twenty-three'. Returns None when
    the token is neither, so the caller can report an unrecognised figure rather than crash."""
    token = token.strip()
    if token.isdigit():
        return int(token)
    return WORD2NUM.get(token.lower())


def lineno(text, idx):
    return text.count("\n", 0, idx) + 1


def matrix_cells(text):
    """Every matrix row as its four interface-cell values, before the self-initiation table."""
    body = text.split(STOP_HEADING)[0]
    return [tuple(m.group(i).strip() for i in (1, 2, 3, 4)) for m in CELL_ROW.finditer(body)]


def section_rows(text):
    """Ordered list of (letter, [row-cells...]) for each lettered matrix section, before the
    self-initiation table. Section-header rows carry no cells and only open a section."""
    body = text.split(STOP_HEADING)[0]
    sections, cur = [], None
    for line in body.split("\n"):
        ms = SECTION_HEADER.match(line)
        if ms:
            cur = (ms.group(1), [])
            sections.append(cur)
            continue
        mc = CELL_ROW.match(line)
        if mc and cur is not None:
            cur[1].append(tuple(mc.group(i).strip() for i in (1, 2, 3, 4)))
    return sections


def _check_stated(text, pattern, expected, label, problems, group=1):
    """Find `pattern` (whose capture `group` is a digits-or-words count), parse it, and assert it
    equals `expected`. A missing anchor or an unparseable token is itself a reported failure."""
    m = re.search(pattern, text)
    if not m:
        problems.append(f"a.5: could not find the {label} figure to check (anchor sentence gone or reworded)")
        return
    stated = parse_count(m.group(group))
    if stated is None:
        problems.append(f"a.5:{lineno(text, m.start())}: {label} figure {m.group(group)!r} is not a recognised number")
    elif stated != expected:
        problems.append(
            f"a.5:{lineno(text, m.start())}: {label} — prose says {m.group(group)} ({stated}) but the matrix has {expected}"
        )


def check_partial_total(cells, text, problems):
    total = sum(c == "Partial" for row in cells for c in row)
    _check_stated(text, r"appears (\d+|[A-Za-z-]+) times across the four columns",
                  total, "`Partial` total across the four columns", problems)


def check_exactly_one_interface(cells, text, problems):
    """The 'Where exactly one interface can do it' table: rows where a single column can act."""
    exclusive = {name: 0 for name in INTERFACES}
    for row in cells:
        can = [i for i, c in enumerate(row) if c in CAN]
        if len(can) == 1:
            exclusive[INTERFACES[can[0]]] += 1

    start = text.find("## Where exactly one interface can do it")
    if start == -1:
        problems.append("a.5: could not find the 'Where exactly one interface can do it' section")
        return
    end = text.find("\n## ", start + 1)
    segment = text[start: end if end != -1 else len(text)]

    # Rows read '| **REST API** | 16 | ...' / '| **`fleetctl`** | 10 | ...'.
    seen = set()
    for m in re.finditer(r"^\|\s*\*\*`?([^`*]+?)`?\*\*\s*\|\s*(\d+)\s*\|", segment, re.M):
        name = m.group(1).strip()
        if name not in exclusive:
            continue
        seen.add(name)
        stated = int(m.group(2))
        if stated != exclusive[name]:
            problems.append(
                f"a.5:{lineno(text, start + m.start())}: exactly-one-interface table — {name} row says "
                f"{stated} but the matrix has {exclusive[name]}"
            )
    for name in INTERFACES:
        if name not in seen:
            problems.append(f"a.5: exactly-one-interface table has no {name} row to check")


def check_not_established_rows(cells, text, problems):
    ge1 = sum(any(c == "Not established" for c in row) for row in cells)
    ge2 = sum(sum(c == "Not established" for c in row) >= 2 for row in cells)
    all4 = sum(all(c == "Not established" for c in row) for row in cells)

    _check_stated(text, r"([A-Za-z-]+) rows carry at least one `Not established` cell",
                  ge1, "rows with at least one `Not established` cell", problems)
    if "and no row carries four" not in text:
        problems.append("a.5: could not find the 'no row carries four' claim to check")
    elif all4 != 0:
        problems.append(
            f"a.5: prose says no row carries four `Not established` cells but the matrix has {all4}"
        )
    _check_stated(text, r"([A-Za-z-]+) rows are unsettled in more than one column",
                  ge2, "rows unsettled in more than one column", problems)


def check_ui_not_established(cells, text, problems):
    ui_ne = sum(row[0] == "Not established" for row in cells)
    _check_stated(text, r"UI column's (\d+|[A-Za-z-]+) cells",
                  ui_ne, "UI column's `Not established` cell count", problems)


def check_section_n(text, problems):
    sections = section_rows(text)
    by_letter = {letter: rows for letter, rows in sections}

    total_in_sections = sum(len(rows) for _, rows in sections)
    matrix_total = len(matrix_cells(text))
    if total_in_sections != matrix_total:
        problems.append(
            f"a.5: the lettered sections hold {total_in_sections} rows but the matrix has "
            f"{matrix_total} — a section header is mis-parsed or a row sits outside every section"
        )

    n_rows = by_letter.get("N", [])
    _check_stated(text, r"section N, where GitOps supports none of the (\d+|[A-Za-z-]+) rows",
                  len(n_rows), "section N row count", problems)
    gitops_can = sum(1 for row in n_rows if row[3] in CAN)
    if gitops_can != 0:
        problems.append(
            f"a.5: prose says GitOps supports none of section N's rows but {gitops_can} carry a "
            f"`Full`/`Partial` GitOps cell"
        )


def main():
    if not A5_PATH.exists():
        print(f"skipped: {A5_PATH} not found")
        return 0

    text = A5_PATH.read_text()
    cells = matrix_cells(text)
    problems = []

    check_partial_total(cells, text, problems)
    check_exactly_one_interface(cells, text, problems)
    check_not_established_rows(cells, text, problems)
    check_ui_not_established(cells, text, problems)
    check_section_n(text, problems)

    if problems:
        print(f"{len(problems)} register-count problem(s):\n")
        for p in problems:
            print(f"  {p}")
        return 1

    partial = sum(c == "Partial" for row in cells for c in row)
    print(
        f"register counts: recomputed from a.5's {len(cells)} matrix rows — `Partial` total ({partial}), "
        f"the exactly-one-interface table, at-least-one/more-than-one `Not established` (rows), the UI "
        f"`Not established` figure, and section N's count and GitOps-none claim all match the prose"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
