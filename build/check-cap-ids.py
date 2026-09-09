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

Extended 2026-09-02, round 4 RB1, after A.1 grew from 354 to 360 rows (CAP-361 to CAP-366)
and A.5 was never updated to match: for four straight rounds this exact class of defect —
one appendix's register drifting out from under its siblings — escaped review because every
fix before this one patched only the file the finding named, never the whole contract A.1,
A.5 and A.7 make with each other and with their own stated counts. The checks below assert
that whole contract, not just the one hole (missing reverse-direction coverage) that let RB1
through:
  3. Every A.1 formal CAP-### row's ID is either a formal row in A.5, or named in A.5's own
     prose as a documented exclusion (the "covers all of them except **CAP-NNN" sentences).
     A.5's exclusion list must also not go stale in the other direction: an ID it claims to
     exclude must actually be absent from its matrix, or the exclusion note itself is wrong.
  4. A.1's frontmatter states how many rows it verified. That number must equal the actual
     count of CAP-### rows in A.1.
  5. A.5's own prose states how many rows its matrix carries. That number must equal the
     actual row count.
  6. A.7's main per-command table and its own ownership-audit table must agree on which
     chapter owns a command: no "No owning chapter" text may survive in the main table for
     a command the audit table assigns a chapter to, and the two chapters named must match.
  7. A.7's shared-prefix-contract arithmetic (how many of its command rows carry the common
     authorization prefix, how many do not, and how the index's own total splits between the
     cross-platform tree and the one Windows-only row) must equal the rows actually counted
     from its own tables, not just be internally consistent on paper.

Extended 2026-09-03, round 5 T1, after MJ2 found seven current a.1 capabilities silently
absent from a.2 and m8/m9 found a.5's own prose counts drifted from its matrix. The
a.1-to-a.5 sync check (3 above) held, but the same drift class had simply moved: to a.2,
which the contract never checked in reverse, and to a.5's internal arithmetic, which no
check recomputed. Two more assertions close both:
  8. Every formal a.1 CAP-### row is carried by a.2, as a platform-matrix row, a
     not-platform-scoped bullet, a lettered split row (CAP-244a/b/c, CAP-341a/b), or an id
     a.2's own prose names as a deliberate exclusion (CAP-342, CAP-048). An exclusion note
     for an id that is in fact present as a row is flagged as stale in the other direction.
  9. a.5's five-value-by-four-interface count table equals the tally recomputed from its
     matrix, and its prose cross-counts (rows with no supported interface and how many are
     readable, rows `Full` in all four columns, rows with all four columns agreeing) equal
     the matrix too. This makes m9's GitOps `Unsupported` figure and every sibling count a
     checked invariant rather than a hand-transcribed one.

A.4 is not checked here. Its 152 administrator intents are a coarser grouping than A.1's
360 outcomes (see a.1's "How to read a row"), so it carries no CAP-ID column and nothing
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


def a5_documented_exclusions(a5_text):
    """CAP-IDs a.5's own prose names as deliberately outside its matrix, e.g. "this index
    covers all of them except **CAP-354, connecting an AI assistant**". A row named here is
    a claim, not a fact; callers reconcile it against what the matrix actually contains."""
    return {"CAP-" + m.group(1) for m in re.finditer(r"except \*\*CAP-(\d+)", a5_text)}


def check_reverse_coverage(a1_rows, a5_rows, a5_text, problems):
    """The direction round 3's check never took: every formal a.1 row must land somewhere
    in a.5, either as a row or as a named exclusion. This is exactly the hole RB1 escaped
    through — CAP-361 to CAP-366 were new a.1 rows that a.5 silently never projected, and
    the old check only ever asked whether a.5's IDs existed in a.1, never the reverse."""
    missing = set(a1_rows) - set(a5_rows)
    excluded = a5_documented_exclusions(a5_text)

    undocumented = missing - excluded
    if undocumented:
        problems.append(
            "a.5: missing these a.1 IDs with no documented exclusion (either add a row or "
            "name the exclusion in a.5's sibling-differences prose): "
            + ", ".join(sorted(undocumented, key=lambda c: int(c.split("-")[1])))
        )

    stale = excluded - missing
    if stale:
        problems.append(
            "a.5: prose excludes these IDs but they are actually present as formal rows "
            "(stale exclusion note): " + ", ".join(sorted(stale, key=lambda c: int(c.split("-")[1])))
        )


def check_a1_frontmatter_count(a1_path, a1_rows, problems):
    text = a1_path.read_text()
    m = re.search(r"verified_source:.*?all (\d+) rows", text)
    if not m:
        problems.append("a.1: could not find the frontmatter's stated row count ('all N rows')")
        return
    stated, actual = int(m.group(1)), len(a1_rows)
    if stated != actual:
        problems.append(
            f"a.1: frontmatter's verified_source says {stated} rows but {actual} formal "
            f"CAP-### rows actually exist"
        )


def check_a5_prose_count(a5_path, a5_rows, problems):
    text = a5_path.read_text()
    m = re.search(r"This appendix carries (\d+) rows", text)
    if not m:
        problems.append("a.5: could not find the 'This appendix carries N rows' claim")
        return
    stated, actual = int(m.group(1)), len(a5_rows)
    if stated != actual:
        problems.append(
            f"a.5: prose says this appendix carries {stated} rows but its matrix actually "
            f"has {actual}"
        )
    # The two other headline row-count mentions must agree with the same actual count too.
    for label, pattern in (
        ("'carries N of them, against all four'", r"capability register, (\d+) of them, against"),
        ("'All N register rows'", r"All (\d+) register rows, grouped"),
        ("'N rows, 1,'", r"\*\*(\d+) rows, [\d,]+ cells"),
    ):
        m2 = re.search(pattern, text)
        if not m2:
            problems.append(f"a.5: could not find the {label} row-count mention")
            continue
        if int(m2.group(1)) != actual:
            problems.append(
                f"a.5: the {label} mention says {m2.group(1)} rows but the matrix has {actual}"
            )


def a7_index_segment(text):
    start = text.index("### Top-level commands")
    end = text.index("### The seventeen rows")
    return text[start:end]


def a7_command_rows(text):
    """(command_name, chapter_cell_or_None) for every row in the main per-command index, in
    the macOS/Linux tree. The Windows-only `updates` entry is deliberately not matched here:
    its row is `**\\`updates\\` on Windows**`, which this pattern (closing backtick flush
    against `**`) does not catch, mirroring how the index's own prose counts it separately.

    Split on "|" rather than a single greedy regex: the tables are not uniform width. Most
    rows carry five content columns (Command, Access contract, Effect, Result contract,
    Chapter); the `debug` family's table carries only four (no Chapter column at all, since
    that family is covered by its own paragraph rather than per-row links)."""
    out = []
    for line in a7_index_segment(text).split("\n"):
        m = re.match(r"^\|\s*\*\*`([^`]+)`\*\*", line)
        if not m:
            continue
        fields = [f.strip() for f in line.split("|")]
        # fields[0] and fields[-1] are the empty strings outside the leading/trailing pipes.
        content = fields[1:-1]
        chapter = content[4] if len(content) >= 5 else None
        out.append((m.group(1), chapter))
    return out


def a7_audit_table(text):
    """command name -> chapter citation, from 'Which commands have an owning chapter'."""
    start = text.index("### Which commands have an owning chapter")
    end = text.index("###", start + 1)
    segment = text[start:end]
    out = {}
    for line in segment.split("\n"):
        m = re.match(r"^\|\s*\*\*[^*]+\*\*\s*\|\s*(.+?)\s*\|\s*(\[[\d.]+\].*?)\s*\|\s*$", line)
        if not m:
            continue
        chapter_cite = m.group(2)
        for cmd in re.findall(r"`([^`]+)`", m.group(1)):
            out[cmd] = chapter_cite
    return out


def check_a7_chapter_agreement(a7_path, problems):
    text = a7_path.read_text()

    if "No owning chapter" in text:
        problems.append(
            "a.7: the literal string 'No owning chapter' still appears in the file, but the "
            "prose claims every row has an owning chapter"
        )

    main_rows = dict(a7_command_rows(text))
    audit = a7_audit_table(text)
    for cmd, audit_cite in audit.items():
        if cmd not in main_rows:
            problems.append(f"a.7: audit table names `{cmd}` but it has no row in the main index")
            continue
        main_cell = main_rows[cmd] or ""
        audit_chapter = re.match(r"\[([\d.]+)\]", audit_cite)
        main_chapter = re.match(r"\[([\d.]+)\]", main_cell)
        if not main_chapter:
            problems.append(
                f"a.7: main index's Chapter cell for `{cmd}` is \"{main_cell}\", which names no "
                f"chapter, but the audit table assigns it {audit_cite}"
            )
        elif audit_chapter and main_chapter.group(1) != audit_chapter.group(1):
            problems.append(
                f"a.7: main index sends `{cmd}` to [{main_chapter.group(1)}] but the audit "
                f"table sends it to [{audit_chapter.group(1)}]"
            )


def check_a7_prefix_arithmetic(a7_path, problems):
    text = a7_path.read_text()

    actual_rows = len(a7_command_rows(text))

    m = re.search(r"(\d+) rows, grouped by top-level family: the (\d+) behaviours", text)
    if not m:
        problems.append("a.7: could not find the '70 rows ... 69 behaviours' total-count sentence")
        return
    stated_total, stated_tree = int(m.group(1)), int(m.group(2))

    if stated_tree != actual_rows:
        problems.append(
            f"a.7: says {stated_tree} behavioural rows in the macOS/Linux tree, but the main "
            f"index actually has {actual_rows} rows"
        )
    if stated_total != stated_tree + 1:
        problems.append(
            f"a.7: says {stated_total} rows total but {stated_tree} (the tree) + 1 (the "
            f"Windows-only row) is {stated_tree + 1}"
        )

    m2 = re.search(r"for the (\d+) rows that carry it", text)
    m3 = re.search(r"Eighteen of the (\d+) rows do not carry the prefix", text)
    if not (m2 and m3):
        problems.append("a.7: could not find both halves of the shared-prefix-contract count")
        return
    carry, prefix_universe = int(m2.group(1)), int(m3.group(1))
    without_prefix = 18  # the sentence's own word, cross-checked against `carry` below
    if prefix_universe != stated_tree:
        problems.append(
            f"a.7: the shared-prefix discussion's universe is {prefix_universe} rows, but the "
            f"index says the macOS/Linux tree has {stated_tree}"
        )
    if carry + without_prefix != prefix_universe:
        problems.append(
            f"a.7: {carry} rows carrying the shared prefix plus {without_prefix} that do not "
            f"should equal the {prefix_universe}-row universe, but {carry} + {without_prefix} "
            f"= {carry + without_prefix}"
        )


def a2_covered_ids(a2_text):
    """Every CAP-ID a.2 actually carries as a row: a platform-matrix row, a
    not-platform-scoped bullet, or one of the lettered split rows (CAP-244a/b/c,
    CAP-341a/b), normalised back to its base id. Prose mentions do not count."""
    return {
        "CAP-" + m.group(1)
        for m in re.finditer(r"(?:^\||^-)\s*\*\*CAP-(\d+)[a-z]?\*\*", a2_text, re.M)
    }


def a2_documented_exclusions(a2_text):
    """CAP-IDs a.2's own prose names as deliberately not given a row: CAP-342 (not a Fleet
    capability at all) and CAP-048 (merged into another row because it is platform-identical).
    Both are written as a bold '**CAP-NNN, <verb phrase>**' lead, distinct from a table row's
    '**CAP-NNN**' which is immediately closed."""
    return {"CAP-" + m.group(1) for m in re.finditer(r"\*\*CAP-(\d+),\s", a2_text)}


def check_a2_reverse_coverage(a1_rows, a2_text, problems):
    """The direction round 4's check took into a.5, now taken into a.2 as well: every formal
    a.1 row must land somewhere in a.2, as a row or as a named exclusion. This is exactly the
    hole round 5's MJ2 escaped through, where seven current a.1 capabilities (CAP-349, 350,
    351, 352, 354, 372, 373) were silently absent from a.2's projection."""
    covered = a2_covered_ids(a2_text)
    excluded = a2_documented_exclusions(a2_text)

    undocumented = set(a1_rows) - covered - excluded
    if undocumented:
        problems.append(
            "a.2: missing these a.1 IDs with no documented exclusion (either add a row or "
            "name the exclusion in a.2's prose): "
            + ", ".join(sorted(undocumented, key=lambda c: int(c.split("-")[1])))
        )

    stale = excluded & covered
    if stale:
        problems.append(
            "a.2: prose documents these IDs as excluded but they are present as rows "
            "(stale exclusion note): "
            + ", ".join(sorted(stale, key=lambda c: int(c.split("-")[1])))
        )


A5_CELL_ROW = re.compile(
    r"^\|\s*\*\*CAP-\d+[a-z]?\*\*\s*\|[^|]*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|",
    re.M,
)


def a5_cell_rows(a5_text):
    """Every a.5 matrix row as its four interface cells (UI, REST API, fleetctl, GitOps),
    stopping before the self-initiation table, which answers a different question in the same
    column shape."""
    body = a5_text.split(STOP_HEADING)[0]
    return [
        tuple(m.group(i).strip() for i in (1, 2, 3, 4))
        for m in A5_CELL_ROW.finditer(body)
    ]


_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
_TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def _words(n):
    """English words for 0..999, lower-case and hyphenated ('forty-eight'), matching how a.5
    spells the counts it also states in prose."""
    if n < 20:
        return _ONES[n]
    if n < 100:
        t, o = divmod(n, 10)
        return _TENS[t] + ("-" + _ONES[o] if o else "")
    h, r = divmod(n, 100)
    return _ONES[h] + " hundred" + (" and " + _words(r) if r else "")


def check_a5_count_table(cells, a5_text, problems):
    """a.5 prints a five-value by four-interface count table. Every cell in it must equal the
    tally recomputed from the matrix, which makes m9's GitOps `Unsupported` figure (203) and
    every other per-interface count a checked invariant rather than a hand-transcribed one."""
    values = ["Full", "Partial", "Read only", "Unsupported", "Not established"]
    actual = {v: [0, 0, 0, 0] for v in values}
    for row in cells:
        for i in range(4):
            if row[i] in actual:
                actual[row[i]][i] += 1
    for v in values:
        m = re.search(
            r"^\|\s*\*\*" + re.escape(v) + r"\*\*\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|",
            a5_text, re.M,
        )
        if not m:
            problems.append(f"a.5: count table has no '{v}' row to check")
            continue
        stated = [int(m.group(i)) for i in (1, 2, 3, 4)]
        if stated != actual[v]:
            problems.append(
                f"a.5: count table '{v}' row says {stated} but the matrix has {actual[v]}"
            )


def check_a5_total_row(cells, a5_text, problems):
    """The count table's **Total** row. Added 2026-09-08 (overnight step 7, round 3) after
    CAP-395 was scored into the matrix and the five value rows were recomputed while the
    Total row below them kept the old 381 in all four columns. check_a5_count_table walks a
    fixed list of the five values and never looked at Total, so nothing caught it."""
    actual = len(cells)
    m = re.search(r"^\|\s*\*\*Total\*\*\s*\|\s*\*\*(\d+)\*\*\s*\|\s*\*\*(\d+)\*\*\s*\|"
                  r"\s*\*\*(\d+)\*\*\s*\|\s*\*\*(\d+)\*\*\s*\|", a5_text, re.M)
    if not m:
        problems.append("a.5: count table has no **Total** row to check")
        return
    stated = [int(m.group(i)) for i in (1, 2, 3, 4)]
    if stated != [actual] * 4:
        problems.append(
            f"a.5: count table Total row says {stated} but the matrix has {actual} rows in "
            f"every column"
        )


def check_a5_reach_figures(cells, a5_text, problems):
    """a.5's two reach sentences, both recomputed from the matrix. Added 2026-09-08 with the
    Total row check and for the same reason: CAP-395 moved both and neither had a check.

      1. "N at `Full` or `Partial` against N for the UI, N for `fleetctl` and N for GitOps".
      2. "GitOps is `Unsupported` on N rows the UI and the REST API can both perform."
    """
    can = ("Full", "Partial")
    reach = [sum(1 for r in cells if r[i] in can) for i in range(4)]  # UI, REST, fleetctl, GitOps
    m = re.search(
        r"(\d+) at `Full` or `Partial` against (\d+) for the UI, (\d+) for `fleetctl` and "
        r"(\d+) for GitOps", a5_text)
    if not m:
        problems.append("a.5: could not find the 'N at `Full` or `Partial` against ...' reach sentence")
    else:
        stated = [int(m.group(i)) for i in (2, 1, 3, 4)]  # sentence order is REST, UI, fleetctl, GitOps
        if stated != reach:
            problems.append(
                f"a.5: the reach sentence says UI {stated[0]}, REST {stated[1]}, fleetctl "
                f"{stated[2]}, GitOps {stated[3]} at Full or Partial but the matrix has "
                f"UI {reach[0]}, REST {reach[1]}, fleetctl {reach[2]}, GitOps {reach[3]}"
            )

    both = sum(1 for r in cells if r[3] == "Unsupported" and r[0] in can and r[1] in can)
    m = re.search(r"GitOps is `Unsupported` on (\d+) rows the UI and the REST API can both perform", a5_text)
    if not m:
        problems.append("a.5: could not find the 'GitOps is `Unsupported` on N rows' sentence")
    elif int(m.group(1)) != both:
        problems.append(
            f"a.5: says GitOps is Unsupported on {m.group(1)} rows the UI and REST can both "
            f"perform but the matrix has {both}"
        )


def check_a1_outcome_counts(a1_path, a1_rows, problems):
    """a.1 states its own size twice in prose and once inside "How to read a row", and states
    a subtotal under each of its eight group headings. Added 2026-09-08 (overnight step 7,
    round 3): CAP-395 left all three headline figures at 383 and group 4's subtotal at 62,
    and the only count this file had a check behind was the one in its frontmatter.

    Every "N outcomes" figure written in digits is checked: inside a group section it must
    equal that group's own formal rows, outside one it must equal the register total. The
    no-capability-row register spells its counts as words ("nine outcomes to ten"), which is
    what keeps those out of scope here rather than an exemption list."""
    text = a1_path.read_text()
    total = len(a1_rows)
    # Group headings ("### 5. Changing a device") and, inside three of them, the lane
    # headings that carry a subtotal of their own ("#### Settings that persist"). A figure
    # is checked against the innermost heading above it.
    heads = [(m.start(), m.group(1).count("#"), m.group(2).strip())
             for m in re.finditer(r"^(#{3,4}) (\d+\. .+|.+)$", text, re.M)]
    groups = [(pos, name) for pos, level, name in heads if level == 3 and re.match(r"\d+\. ", name)]
    if len(groups) != 8:
        problems.append(f"a.1: expected eight numbered group headings, found {len(groups)}")

    def section_of(pos, level):
        """The last heading at or above `level` before `pos`, as (start, name)."""
        out = None
        for start, lvl, name in heads:
            if start < pos and lvl <= level:
                out = (start, name)
        return out

    counts = {}
    for m in re.finditer(r"^\|\s*\*\*CAP-\d+\*\*\s*\|", text, re.M):
        for level in (3, 4):
            sec = section_of(m.start(), level)
            if sec:
                counts[(level, sec[0])] = counts.get((level, sec[0]), 0) + 1
    in_groups = sum(counts.get((3, pos), 0) for pos, _ in groups)
    if in_groups != total:
        problems.append(
            f"a.1: the eight group sections hold {in_groups} formal rows but the file has {total}"
        )
    for m in re.finditer(r"(\d+) outcomes", text):
        stated = int(m.group(1))
        sec4 = section_of(m.start(), 4)
        sec3 = section_of(m.start(), 3)
        if sec4 and sec4 != sec3:
            expected, where = counts.get((4, sec4[0]), 0), f"the '{sec4[1]}' lane"
        elif sec3:
            expected, where = counts.get((3, sec3[0]), 0), f"'{sec3[1]}'"
        else:
            expected, where = total, "the register total"
        if stated != expected:
            problems.append(
                f"a.1: a '{stated} outcomes' figure describing {where} should be {expected}"
            )


def check_a1_group_table(a1_path, a1_rows, problems):
    """The group-summary table under "Why the eight groups are not the table of contents".
    Added 2026-09-09 (overnight step 7, round 4): CAP-395 took group 4 to 63 and round 3
    corrected the group heading above while this table's cell kept 62, so the Outcomes
    column summed to 383 against a 384-row register and both count checks stayed green.
    check_a1_outcome_counts matches the phrase "N outcomes" and a bare table cell has no
    phrase to match, which is the third round running that a figure went stale for want of
    a check that names it. Each cell is checked against its own group section and the
    column is checked against the register total, so neither can drift alone."""
    text = a1_path.read_text()
    total = len(a1_rows)
    heads = [(m.start(), m.group(1)) for m in re.finditer(r"^### (\d+\. .+)$", text, re.M)]
    row_pos = [m.start() for m in re.finditer(r"^\|\s*\*\*CAP-\d+\*\*\s*\|", text, re.M)]
    by_num = {}
    for i, (pos, name) in enumerate(heads):
        end = heads[i + 1][0] if i + 1 < len(heads) else len(text)
        num, _, label = name.partition(". ")
        by_num[num] = (label.strip(), sum(1 for r in row_pos if pos < r < end))

    sec = re.search(r"^## Why the eight groups are not the table of contents$(.*?)^## ",
                    text, re.M | re.S)
    if not sec:
        problems.append("a.1: could not find the 'Why the eight groups' section to check its table")
        return
    table = re.findall(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*[^|]*?\s*\|\s*(\d+)\s*\|\s*$",
                       sec.group(1), re.M)
    if len(table) != 8:
        problems.append(
            f"a.1: expected an eight-row group-summary table, found {len(table)} countable rows"
        )
        return
    for num, label, stated in table:
        if num not in by_num:
            problems.append(f"a.1: group-summary table has a group {num} with no matching heading")
            continue
        head_label, actual = by_num[num]
        if label != head_label:
            problems.append(
                f"a.1: group-summary row {num} is named '{label}' but its heading is '{head_label}'"
            )
        if int(stated) != actual:
            problems.append(
                f"a.1: the group-summary table says group {num} holds {stated} outcomes but "
                f"that section holds {actual}"
            )
    stated_sum = sum(int(t[2]) for t in table)
    if stated_sum != total:
        problems.append(
            f"a.1: the group-summary table's Outcomes column sums to {stated_sum} but the "
            f"register has {total} rows"
        )


def check_a5_fleetctl_api_figures(cells, a5_text, problems):
    """a.5's `fleetctl api` boundary figures, the last hand-maintained numbers in that section.
    Added 2026-09-09 (overnight step 7, round 4) with the a.1 group table and for the same
    reason. Round 3 replaced three underivable figures here with 122/85; round 4 found that
    "`fleetctl api` would reach the 85" overreaches, because ten of the 85 read `Not
    established` under REST, which is the appendix declining to say. All four figures are
    recomputed from the matrix, and the split is asserted so 85 and 75 cannot drift apart."""
    unsup = [r for r in cells if r[2] == "Unsupported"]            # fleetctl column
    not_unsup = [r for r in unsup if r[1] != "Unsupported"]        # REST column
    settled = [r for r in not_unsup if r[1] != "Not established"]
    n122, n85, n75 = len(unsup), len(not_unsup), len(settled)

    m = re.search(r"the (\d+) rows no specification file reaches and `fleetctl api` "
                  r"demonstrably could", a5_text)
    if not m:
        problems.append("a.5: could not find the 'N rows no specification file reaches' sentence")
    elif int(m.group(1)) != n75:
        problems.append(
            f"a.5: says the boundary decides {m.group(1)} rows `fleetctl api` demonstrably "
            f"could reach but the matrix has {n75} with a settled REST answer"
        )

    m = re.search(r"(\d+) rows do, and on (\d+) of them the REST API column is not "
                  r"`Unsupported`\. On (\d+) of those the REST answer is settled", a5_text)
    if not m:
        problems.append("a.5: could not find the '122 rows do, and on 85 of them ...' sentence")
    else:
        stated = [int(m.group(i)) for i in (1, 2, 3)]
        if stated != [n122, n85, n75]:
            problems.append(
                f"a.5: the `fleetctl api` sentence says {stated[0]} fleetctl-Unsupported rows, "
                f"{stated[1]} with REST not Unsupported and {stated[2]} of those settled, but "
                f"the matrix has {n122}, {n85} and {n75}"
            )

    m = re.search(r"The other ([A-Za-z-]+) read `Not established` under REST", a5_text)
    if not m:
        problems.append("a.5: could not find the 'The other N read `Not established`' sentence")
    elif m.group(1) != _words(n85 - n75):
        problems.append(
            f"a.5: says {m.group(1)} of those rows read `Not established` under REST but the "
            f"matrix has {_words(n85 - n75)}"
        )


def check_a2_prose_count(a2_path, problems):
    """a.2's own headline row count, the a.2 half of the same 2026-09-08 gap: CAP-395 was
    added to the matrix and the "N rows" sentence above it kept 291. a.2 counts lettered
    split rows (CAP-244a and friends) as rows of its own, so this counts them too."""
    text = a2_path.read_text()
    actual = len(re.findall(r"^\|\s*\*\*CAP-\d+[a-z]?\*\*\s*\|", text, re.M))
    m = re.search(r"Grouped as a reader would look for a capability, (\d+) rows", text)
    if not m:
        problems.append("a.2: could not find the 'Grouped as a reader would look ..., N rows' claim")
        return
    if int(m.group(1)) != actual:
        problems.append(
            f"a.2: prose says the matrix carries {m.group(1)} rows but it actually has {actual}"
        )


def check_a5_prose_cross_counts(cells, a5_text, problems):
    """m8, plus the two all-column figures round 5 had to resync when CAP-372 moved from Full
    to Partial: the number of rows with no supported interface (no `Full` and no `Partial`
    anywhere) and how many of those are still readable, the count of rows `Full` in all four
    columns, and the count with all four columns agreeing. Each is recomputed and matched
    against the figure a.5 states, spelled or in digits."""
    no_iface = [r for r in cells if not any(x in ("Full", "Partial") for x in r)]
    readable = sum(1 for r in no_iface if "Read only" in r)
    n = len(no_iface)

    checks = [
        (r"([A-Za-z-]+) rows have no supported interface", _words(n), "rows with no supported interface"),
        (r"([A-Za-z-]+) rows have no `Full` and no `Partial`", _words(n), "rows with no Full and no Partial"),
        (r"([A-Za-z-]+) rows are `Full` in all four columns", _words(sum(1 for r in cells if set(r) == {"Full"})), "rows Full in all four columns"),
    ]
    for pattern, expected_word, label in checks:
        m = re.search(pattern, a5_text)
        if not m:
            problems.append(f"a.5: could not find the '{label}' figure to check")
        elif m.group(1).lower() != expected_word:
            problems.append(
                f"a.5: prose says '{m.group(1)}' {label} but the matrix has {expected_word}"
            )

    m = re.search(r"([A-Za-z]+) of the (\d+) are readable", a5_text)
    if not m:
        problems.append("a.5: could not find the 'N of the M are readable' figure")
    else:
        if int(m.group(2)) != n:
            problems.append(
                f"a.5: 'of the {m.group(2)} are readable' but the matrix has {n} no-interface rows"
            )
        if m.group(1).lower() != _words(readable):
            problems.append(
                f"a.5: '{m.group(1)} of the {n} are readable' but the matrix has {readable} readable"
            )

    m = re.search(r"(\d+) rows have all four columns agreeing", a5_text)
    agree = sum(1 for r in cells if len(set(r)) == 1)
    if not m:
        problems.append("a.5: could not find the 'N rows have all four columns agreeing' figure")
    elif int(m.group(1)) != agree:
        problems.append(
            f"a.5: prose says {m.group(1)} rows have all four columns agreeing but the matrix has {agree}"
        )


def main():
    a1 = APPENDICES / "a.1-capability-index.md"
    a2 = APPENDICES / "a.2-platform-capability-matrix.md"
    a5 = APPENDICES / "a.5-interface-index.md"
    a7 = APPENDICES / "a.7-fleetctl-command-reference.md"
    for p in (a1, a2, a5, a7):
        if not p.exists():
            print(f"skipped: {p} not found")
            return 0

    a1_rows, a2_rows, a5_rows = rows(a1), rows(a2), rows(a5)
    a5_text = a5.read_text()
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

    # The whole-contract checks added for round 4 RB1.
    check_reverse_coverage(a1_rows, a5_rows, a5_text, problems)
    check_a1_frontmatter_count(a1, a1_rows, problems)
    check_a5_prose_count(a5, a5_rows, problems)
    check_a7_chapter_agreement(a7, problems)
    check_a7_prefix_arithmetic(a7, problems)

    # Round 5 T1: a.2 reverse-coverage and a.5's own prose cross-counts (m8/m9), the two
    # drift classes round 5 caught after the a.1-to-a.5 sync check already held.
    a2_text = a2.read_text()
    a5_cells = a5_cell_rows(a5_text)
    check_a2_reverse_coverage(a1_rows, a2_text, problems)
    check_a5_count_table(a5_cells, a5_text, problems)
    check_a5_prose_cross_counts(a5_cells, a5_text, problems)

    # Round 3 of the 4.91 overnight campaign: the count table's Total row, a.5's two reach
    # sentences, a.1's headline and per-group outcome counts and a.2's headline row count.
    # Every one of them went stale when CAP-395 was minted and every check above stayed green.
    check_a5_total_row(a5_cells, a5_text, problems)
    check_a5_reach_figures(a5_cells, a5_text, problems)
    check_a1_outcome_counts(a1, a1_rows, problems)
    check_a2_prose_count(a2, problems)

    # Round 4 of the same campaign: the two figures round 3's checks still could not see —
    # a.1's group-summary table, whose cells carry no "N outcomes" phrase to match, and
    # a.5's `fleetctl api` split, where 85 and 75 mean different things and can drift apart.
    check_a1_group_table(a1, a1_rows, problems)
    check_a5_fleetctl_api_figures(a5_cells, a5_text, problems)

    if problems:
        print(f"{len(problems)} CAP-ID problem(s):\n")
        for p in problems:
            print(f"  {p}")
        return 1

    print(
        f"CAP-ID register: {len(a1_ids)} IDs in a.1; a.2 ({len(a2_rows)}) and a.5 "
        f"({len(a5_rows)}) are both subsets with {len(shared)} matching labels checked; "
        f"reverse coverage into a.5 and a.2, frontmatter/prose row counts, a.5's count table "
        f"and cross-counts, and a.7's chapter agreement and prefix arithmetic all hold"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
