#!/usr/bin/env python3
"""Generate a source-pinned catalog of every server config key Fleet actually binds.

Written 2026-08-30 for order-of-attack step 6 (reference layer). The whole-book review
verified that Fleet's own generated configuration reference disagrees with what the
server registers: a default documented as 1h that registers as 2m, an Android batch
size documented 1000 that registers 100, and app_enable_report_stats which the server
never binds at all. Hand-maintained tables inherit those errors; this generator reads
the registration calls themselves (Manager.addConfigs in server/config/config.go), so
the table can only say what the binary does.

Mechanical extraction only. A registration call whose key or default cannot be read
mechanically goes to an UNPARSED section verbatim -- never guessed, never dropped.
Counts (found/parsed/unparsed) print to stderr and are embedded in the output header.

Usage:  python3 build/gen-config-catalog.py [--out FILE]     # Markdown to stdout by default
        FLEET_SRC=/path/to/fleet python3 build/gen-config-catalog.py
"""
import os
import pathlib
import re
import subprocess
import sys

SRC_ROOT = pathlib.Path(os.environ.get("FLEET_SRC", os.path.expanduser("~/Source/Fleet/fleet-public")))
CONFIG_GO = SRC_ROOT / "server/config/config.go"
if not CONFIG_GO.exists():
    print(f"skipped: no Fleet source at {CONFIG_GO}")
    sys.exit(0)

ENV_PREFIX = "FLEET"
TYPES = {"String": "string", "Int": "int", "Bool": "bool", "Duration": "duration", "ByteSize": "bytes"}
DUR_UNITS = {"Nanosecond": "ns", "Microsecond": "us", "Millisecond": "ms",
             "Second": "s", "Minute": "m", "Hour": "h"}


def src_commit():
    try:
        out = subprocess.run(["git", "-C", str(SRC_ROOT), "rev-parse", "HEAD"],
                             capture_output=True, text=True, timeout=10)
        if out.returncode == 0:
            return out.stdout.strip()
    except Exception:
        pass
    return "unknown"


def strip_comments(line):
    """Remove a // comment, respecting double-quoted strings and backticks."""
    out, i, n = [], 0, len(line)
    quote = None
    while i < n:
        c = line[i]
        if quote:
            out.append(c)
            if c == "\\" and quote == '"' and i + 1 < n:
                out.append(line[i + 1])
                i += 2
                continue
            if c == quote:
                quote = None
            i += 1
            continue
        if c in ('"', "`"):
            quote = c
            out.append(c)
            i += 1
            continue
        if c == "/" and i + 1 < n and line[i + 1] == "/":
            break
        out.append(c)
        i += 1
    return "".join(out)


def depth_delta(text):
    """Net change in bracket depth, ignoring brackets inside strings."""
    d, i, n = 0, 0, len(text)
    quote = None
    while i < n:
        c = text[i]
        if quote:
            if c == "\\" and quote == '"':
                i += 2
                continue
            if c == quote:
                quote = None
        elif c in ('"', "`"):
            quote = c
        elif c in "([{":
            d += 1
        elif c in ")]}":
            d -= 1
        i += 1
    return d


def split_args(text):
    """Split an argument list on top-level commas, respecting nesting and strings."""
    args, buf, depth, i, n = [], [], 0, 0, len(text)
    quote = None
    while i < n:
        c = text[i]
        if quote:
            buf.append(c)
            if c == "\\" and quote == '"' and i + 1 < n:
                buf.append(text[i + 1])
                i += 2
                continue
            if c == quote:
                quote = None
            i += 1
            continue
        if c in ('"', "`"):
            quote = c
            buf.append(c)
        elif c in "([{":
            depth += 1
            buf.append(c)
        elif c in ")]}":
            depth -= 1
            buf.append(c)
        elif c == "," and depth == 0:
            args.append("".join(buf).strip())
            buf = []
        else:
            buf.append(c)
        i += 1
    tail = "".join(buf).strip()
    if tail:
        args.append(tail)
    return args


def split_on_plus(text):
    """Split a Go string-concatenation expression on top-level '+', respecting
    quoted strings so a literal '+' inside a usage string isn't mistaken for
    concatenation."""
    parts, buf, depth, i, n = [], [], 0, 0, len(text)
    quote = None
    while i < n:
        c = text[i]
        if quote:
            buf.append(c)
            if c == "\\" and quote == '"' and i + 1 < n:
                buf.append(text[i + 1])
                i += 2
                continue
            if c == quote:
                quote = None
            i += 1
            continue
        if c in ('"', "`"):
            quote = c
            buf.append(c)
        elif c in "([{":
            depth += 1
            buf.append(c)
        elif c in ")]}":
            depth -= 1
            buf.append(c)
        elif c == "+" and depth == 0:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(c)
        i += 1
    parts.append("".join(buf))
    return parts


def find_call_args(stmt, start):
    """Given index of '(' opening a call, return (args_text, index_after_close)."""
    depth, i, n = 0, start, len(stmt)
    quote = None
    while i < n:
        c = stmt[i]
        if quote:
            if c == "\\" and quote == '"':
                i += 2
                continue
            if c == quote:
                quote = None
        elif c in ('"', "`"):
            quote = c
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return stmt[start + 1:i], i + 1
        i += 1
    return None, n


lines = CONFIG_GO.read_text().split("\n")
stripped_file = "\n".join(strip_comments(l) for l in lines)

# Constants declared in config.go, for keys/defaults given by identifier
# (e.g. TLSProfileKey = "server.tls_compatibility").
consts = {}
for m in re.finditer(r'^\s*(\w+)\s*=\s*"([^"]*)"\s*$', stripped_file, re.M):
    consts[m.group(1)] = m.group(2)

# Extract the addConfigs() body with real line numbers.
body_start = None
for idx, line in enumerate(lines):
    if re.match(r"^func \(man Manager\) addConfigs\(\) \{", line):
        body_start = idx
        break
if body_start is None:
    print("skipped: Manager.addConfigs not found; the registration shape may have changed")
    sys.exit(0)

body = []  # (lineno, text-without-comments)
depth = 0
for idx in range(body_start, len(lines)):
    text = strip_comments(lines[idx])
    depth += depth_delta(text)
    body.append((idx + 1, text))
    if depth == 0 and idx > body_start:
        break

# Join into statements on bracket balance, preserving line breaks so any
# match offset inside a statement maps back to a real source line.
statements = []  # (first_lineno, text-with-newlines)
buf, buf_line, d = [], None, 0
for lineno, text in body[1:-1]:  # skip "func ... {" and closing "}"
    if not text.strip() and not buf:
        continue
    if buf_line is None:
        buf_line = lineno
    buf.append(text.strip())
    d += depth_delta(text)
    if d <= 0:
        statements.append((buf_line, "\n".join(buf)))
        buf, buf_line, d = [], None, 0
if buf:
    statements.append((buf_line, "\n".join(buf)))


def line_at(first_lineno, text, offset):
    return first_lineno + text.count("\n", 0, offset)

CALL_RE = re.compile(r"\bman\.addConfig(String|Int|Bool|Duration|ByteSize)\(")
HIDE_RE = re.compile(r'\bman\.hideConfig\("([^"]+)"\)')


def norm_duration(expr):
    expr = expr.strip()
    if expr == "0":
        return "0s"
    m = re.match(r"^time\.(\w+)$", expr)
    if m and m.group(1) in DUR_UNITS:
        return "1" + DUR_UNITS[m.group(1)]
    m = re.match(r"^([\d*\s]+)\*\s*time\.(\w+)$", expr)
    if m and m.group(2) in DUR_UNITS:
        factors = [int(x) for x in m.group(1).replace(" ", "").rstrip("*").split("*")]
        n = 1
        for f in factors:
            n *= f
        return f"{n}{DUR_UNITS[m.group(2)]}"
    return None


NS = {"ns": 1, "us": 10**3, "ms": 10**6, "s": 10**9, "m": 60 * 10**9, "h": 3600 * 10**9}


def go_duration_string(norm):
    """Reproduce Go's time.Duration.String() for a normalized '<n><unit>' value,
    so a default registered as (1*time.Minute).String() prints exactly what the
    binary registers ('1m0s', not '1m')."""
    m = re.match(r"^(\d+)(ns|us|ms|s|m|h)$", norm)
    if not m:
        return None
    ns = int(m.group(1)) * NS[m.group(2)]
    if ns == 0:
        return "0s"
    if ns < 10**9:  # sub-second: Go uses a single unit with fractional digits
        for unit, size in (("ns", 1), ("us", 10**3), ("ms", 10**6)):
            if ns < size * 1000:
                v = ns / size
                s = f"{v:.9f}".rstrip("0").rstrip(".")
                return s + ("µs" if unit == "us" else unit)
    secs, frac = divmod(ns, 10**9)
    h, rem = divmod(secs, 3600)
    mnt, sec = divmod(rem, 60)
    sec_s = str(sec) if frac == 0 else f"{sec + frac / 10**9:.9f}".rstrip("0").rstrip(".")
    if h:
        return f"{h}h{mnt}m{sec_s}s"
    if mnt:
        return f"{mnt}m{sec_s}s"
    return f"{sec_s}s"


def parse_default(kind, expr):
    """Return (display, computed) for a registered default, or None if unreadable.
    computed=True means the default is a source expression evaluated at runtime,
    shown verbatim rather than as a value."""
    expr = expr.strip()
    if kind == "Duration":
        d = norm_duration(expr)
        return (d, False) if d is not None else (expr, True)
    if kind in ("String", "ByteSize"):
        m = re.match(r'^"((?:[^"\\]|\\.)*)"$', expr)
        if m:
            return ('"' + m.group(1) + '"', False)
        if expr in consts:
            return ('"' + consts[expr] + '"', False)
        # (N*time.Unit).String() -- registered as the exact Go rendering
        m = re.match(r"^\((.+)\)\.String\(\)$", expr)
        if m:
            d = norm_duration(m.group(1))
            g = go_duration_string(d) if d else None
            if g is not None:
                return ('"' + g + '"', False)
        return (expr, True)
    if kind == "Int":
        return (expr, False) if re.match(r"^-?\d+$", expr) else (expr, True)
    if kind == "Bool":
        return (expr, False) if expr in ("true", "false") else (expr, True)
    return None


def parse_key(expr, closure_params=None):
    expr = expr.strip()
    m = re.match(r'^"([a-z0-9_.]+)"$', expr)
    if m:
        return m.group(1)
    if expr in consts and re.match(r"^[a-z0-9_.]+$", consts[expr]):
        return consts[expr]
    return None


def parse_usage(expr, binding=None):
    """Return the registered usage string for a config key, or None if the
    third addConfig* argument isn't a chain of string literals and/or bound
    closure parameters (e.g. "a"+usageSuffix, or "a"+"b"+"c"). Never guessed:
    an unreadable segment (fmt.Sprintf, an unbound identifier) yields None
    for the whole string rather than a fabricated or partial one."""
    if expr is None:
        return None
    expr = expr.strip()
    if not expr:
        return None
    segments = [s.strip() for s in split_on_plus(expr)]
    parts = []
    for seg in segments:
        m = re.match(r'^"((?:[^"\\]|\\.)*)"$', seg)
        if m:
            parts.append(m.group(1))
            continue
        if binding is not None and seg in binding:
            bm = re.match(r'^"((?:[^"\\]|\\.)*)"$', binding[seg].strip())
            if bm:
                parts.append(bm.group(1))
                continue
        return None
    return "".join(parts)


# --- reader-facing rendering of computed defaults -----------------------------
# A computed default is a source expression evaluated at runtime. Shown verbatim
# it would put Go identifiers in a reader-facing cell (STYLE forbids that), so the
# recognised forms are translated to a reader term and the raw expression is kept
# only in the row's HTML comment. An unrecognised computed form falls back to a
# neutral marker, again with the expression in the comment alone.
SIZE_UNITS = {"KB": 10**3, "MB": 10**6, "GB": 10**9, "TB": 10**12,
              "KiB": 1 << 10, "MiB": 1 << 20, "GiB": 1 << 30, "TiB": 1 << 40}
_size_cache = {}


def _resolve_size_const(ident):
    """Resolve a Go size constant (possibly package-qualified) to a display form
    like '10 GiB' by reading its single declaration from the Fleet source. The
    unit and multiplier come straight from the source, so a change to the constant
    flows through on regeneration. Returns None if it cannot be resolved uniquely."""
    if ident in _size_cache:
        return _size_cache[ident]
    name = ident.split(".")[-1]
    decl_re = re.compile(r"^\s*(?:const\s+|var\s+)?" + re.escape(name) + r"\b[^\n=]*=\s*(.+?)\s*$", re.M)
    unit_re = re.compile(r"^\s*(?:(\d+)\s*\*\s*)?units\.(\w+)\b")
    found = set()
    server_dir = SRC_ROOT / "server"
    for f in server_dir.rglob("*.go"):
        if f.name.endswith("_test.go"):
            continue
        try:
            txt = f.read_text()
        except Exception:
            continue
        if name not in txt:
            continue
        for m in decl_re.finditer(txt):
            um = unit_re.match(m.group(1))
            if um and um.group(2) in SIZE_UNITS:
                mult = int(um.group(1)) if um.group(1) else 1
                found.add(f"{mult} {um.group(2)}")
    result = found.pop() if len(found) == 1 else None
    _size_cache[ident] = result
    return result


def render_computed(expr):
    """Return a reader-facing string for a computed default, or None to fall back
    to a neutral marker. Never returns Go identifiers."""
    expr = expr.strip()
    m = re.match(r'^filepath\.Join\(os\.TempDir\(\),\s*"([^"]+)"\)$', expr)
    if m:
        return "<system temp dir>/" + m.group(1)
    m = re.match(r"^installersize\.Human\((.+)\)$", expr)
    if m:
        return _resolve_size_const(m.group(1).strip())
    return None


found_calls = 0       # registration call sites seen in addConfigs (closure bodies count once)
rows = []             # (key, kind, default_display, lineno, via) in registration order
unparsed = []         # (lineno, raw_stmt_or_call, reason)
hidden = set()
closures = {}         # name -> {"params": [...], "calls": [(lineno, kind, key_expr, def_expr)]}

# Pass 1: closure definitions (helper funcs registering keys under a prefix).
for lineno, stmt in statements:
    m = re.match(r"^(\w+)\s*:=\s*func\(([^)]*)\)\s*\{", stmt)
    if not m or "addConfig" not in stmt:
        continue
    params = [p.strip().split(" ")[0] for p in m.group(2).split(",") if p.strip()]
    calls = []
    pos = 0
    while True:
        cm = CALL_RE.search(stmt, pos)
        if not cm:
            break
        call_line = line_at(lineno, stmt, cm.start())
        args_text, pos = find_call_args(stmt, cm.end() - 1)
        args = split_args(args_text) if args_text is not None else []
        calls.append((call_line, cm.group(1), args[0] if args else "", args[1] if len(args) > 1 else "",
                     args[2] if len(args) > 2 else ""))
    closures[m.group(1)] = {"params": params, "calls": calls}
    found_calls += len(calls)

# Pass 2: everything else, in order.
for lineno, stmt in statements:
    if re.match(r"^\w+\s*:=\s*func\(", stmt) and "addConfig" in stmt:
        continue  # closure definition, handled above; expansion happens at call sites
    # hideConfig, direct or via a range over a []string literal
    for hm in HIDE_RE.finditer(stmt):
        hidden.add(hm.group(1))
    if "hideConfig(" in stmt and not HIDE_RE.search(stmt) and "range" in stmt:
        lit = re.search(r"\[\]string\{(.*?)\}", stmt, re.S)
        if lit:
            hidden.update(re.findall(r'"([a-z0-9_.]+)"', lit.group(1)))
        else:
            unparsed.append((lineno, stmt[:160], "hideConfig loop without a readable []string literal"))
    # closure invocations
    cim = re.match(r"^(\w+)\(", stmt)
    if cim and cim.group(1) in closures:
        cl = closures[cim.group(1)]
        args_text, _ = find_call_args(stmt, len(cim.group(1)))
        if args_text is not None:
            args_text = " ".join(args_text.split())
        cargs = split_args(args_text) if args_text is not None else []
        binding = dict(zip(cl["params"], cargs))
        for c_line, kind, key_expr, def_expr, usage_expr in cl["calls"]:
            key_expr_b, def_expr_b = key_expr.strip(), def_expr.strip()
            pm = re.match(r'^(\w+)\s*\+\s*"([a-z0-9_.]+)"$', key_expr_b)
            if pm and pm.group(1) in binding and re.match(r'^"[a-z0-9_.]+"$', binding[pm.group(1)].strip()):
                key = binding[pm.group(1)].strip().strip('"') + pm.group(2)
            else:
                key = parse_key(key_expr_b)
            if def_expr_b in binding:
                def_expr_b = binding[def_expr_b].strip()
            default = parse_default(kind, def_expr_b) if def_expr_b else None
            usage = parse_usage(usage_expr, binding)
            if key is None or default is None:
                unparsed.append((c_line, f"{cim.group(1)}({args_text}) -> addConfig{kind}({key_expr}, {def_expr})",
                                 "key not mechanically readable through helper expansion"))
            else:
                rows.append((key, kind, default[0], default[1], c_line, f"via {cim.group(1)}({args_text})" if args_text else f"via {cim.group(1)}", usage))
        continue
    # direct registrations
    pos = 0
    while True:
        cm = CALL_RE.search(stmt, pos)
        if not cm:
            break
        found_calls += 1
        kind = cm.group(1)
        call_line = line_at(lineno, stmt, cm.start())
        args_text, pos = find_call_args(stmt, cm.end() - 1)
        if args_text is not None:
            args_text = " ".join(args_text.split())
        args = split_args(args_text) if args_text is not None else []
        key = parse_key(args[0]) if args else None
        default = parse_default(kind, args[1]) if len(args) > 1 else None
        usage = parse_usage(args[2]) if len(args) > 2 else None
        if key is None or default is None:
            unparsed.append((call_line, f"addConfig{kind}({args_text[:140] if args_text else ''})",
                             "key not mechanically readable"))
        else:
            rows.append((key, kind, default[0], default[1], call_line, "", usage))

# Registration order is source order; keep it (deterministic, matches config.go grouping).
dupes = len(rows) - len({r[0] for r in rows})
parsed_keys = len(rows)
computed = sum(1 for r in rows if r[3])
commit = src_commit()

out = []
out.append("<!-- GENERATED by build/gen-config-catalog.py; do not edit by hand.")
out.append(f"     source: server/config/config.go @ {commit}")
out.append(f"     registration calls found: {found_calls}; keys parsed: {parsed_keys} "
           f"(of which {computed} computed defaults); unparsed: {len(unparsed)}; duplicate keys: {dupes} -->")
out.append("")
out.append("# Server configuration keys as registered at startup")
out.append("")
out.append("Every key below is bound by `Manager.addConfigs` in `server/config/config.go` --")
out.append("these are the defaults the binary registers, which is not always what Fleet's")
out.append("generated reference documents. A key absent from this table is not bound by the")
out.append("server, whatever the documentation says. Keys marked *hidden* are bound and")
out.append("functional but suppressed from `fleet serve --help`. A default marked *computed*")
out.append("is evaluated at runtime; the cell shows the exact source expression, not a value.")
out.append("The \"What it's for\" column is the registration's own usage string -- the same")
out.append("text `fleet serve --help` prints for that flag -- read mechanically, not summarised.")
out.append("A blank cell means the usage argument wasn't a plain string the generator could")
out.append("read; that is a generator gap, not a claim the server has no description.")
out.append("")
out.append("| Key | Environment variable | Type | Registered default | What it's for |")
out.append("|---|---|---|---|---|")
for key, kind, default, is_computed, lineno, via, usage in rows:
    env = ENV_PREFIX + "_" + key.replace(".", "_").upper()
    marker = " *(hidden)*" if key in hidden else ""
    note = f"; {via}" if via else ""
    if is_computed:
        # Never put the raw Go expression in a reader-facing cell; keep it in the
        # comment. Show a resolved reader term where the form is recognised.
        note += f"; expr {default}"
        human = render_computed(default)
        default_cell = f"`{human}` *(computed)*" if human else "*(computed at runtime)*"
    else:
        escaped = default.replace("|", "\\|")  # keep table cells intact
        default_cell = f"`{escaped}`"
    usage_cell = usage.replace("|", "\\|").replace("`", "'") if usage else ""
    anchor = f"<!-- server/config/config.go:{lineno}{note} -->"
    out.append(f"| `{key}`{marker} | `{env}` | {TYPES[kind]} | {default_cell} | {usage_cell} {anchor}|")
out.append("")
if unparsed:
    out.append("## UNPARSED registrations")
    out.append("")
    out.append("These call sites register configuration but resisted mechanical extraction.")
    out.append("They are listed verbatim rather than guessed at; read the cited line.")
    out.append("")
    for lineno, frag, reason in unparsed:
        out.append(f"- `server/config/config.go:{lineno}` -- {reason}: `{frag}`")
    out.append("")
hidden_unbound = sorted(h for h in hidden if h not in {r[0] for r in rows})
if hidden_unbound:
    out.append(f"<!-- hideConfig called for keys with no parsed registration: {', '.join(hidden_unbound)} -->")
    out.append("")

text = "\n".join(out)
args = sys.argv[1:]
if "--out" in args:
    dest = pathlib.Path(args[args.index("--out") + 1])
    dest.write_text(text + "\n")
else:
    print(text)

print(f"config catalog: {found_calls} registration calls found, "
      f"{parsed_keys} keys parsed ({len(hidden & {r[0] for r in rows})} hidden, "
      f"{computed} computed defaults), "
      f"{len(unparsed)} unparsed, {dupes} duplicate keys, source commit {commit[:12]}",
      file=sys.stderr)
# no-silent-drop check: every addConfig call in the whole file should be accounted for
total_in_file = len(CALL_RE.findall(stripped_file))
if total_in_file != found_calls:
    print(f"WARNING: {total_in_file} addConfig* calls in config.go but {found_calls} "
          f"seen inside addConfigs(); registrations may live outside the parsed function",
          file=sys.stderr)
    sys.exit(1)
sys.exit(1 if unparsed and "--strict" in args else 0)
