#!/usr/bin/env python3
"""Generate a source-pinned catalog of every HTTP route the Fleet server registers.

Written 2026-08-30 for order-of-attack step 6 (reference layer), alongside
gen-config-catalog.py. The book's API appendix must not delegate per-endpoint
facts to a reference that drifts; this reads the registrations themselves --
the endpointer verb calls (ue.GET(...) and friends) in server/service/handler.go
and the feature-module handler files serve.go mounts, the WithAltPaths aliases,
the declarative deprecated-path alias table, and the raw ServeMux Handle calls
for the MDM protocol endpoints -- so the catalog can only say what the server
actually routes.

Authentication class is derived mechanically from the endpointer constructor a
route is registered on (newUserAuthenticatedEndpointer -> user, and so on; the
legend in the output names the constructor for each label). Raw mux routes are
labeled by the registering function, which is the registration group.

Mechanical extraction only. A registration that resists extraction (unresolvable
path constant, unrecognized receiver) goes to an UNPARSED section verbatim --
never guessed, never dropped. Two loud-failure checks back that up: an
independent dumb count of verb-shaped call sites per scanned file, and a
repo-wide sweep for route-registering files outside the scanned list.
Counts print to stderr and are embedded in the output header.

Usage:  python3 build/gen-api-catalog.py [--out FILE]        # Markdown to stdout by default
        FLEET_SRC=/path/to/fleet python3 build/gen-api-catalog.py
"""
import os
import pathlib
import re
import subprocess
import sys

SRC_ROOT = pathlib.Path(os.environ.get("FLEET_SRC", os.path.expanduser("~/Source/Fleet/fleet-public")))
HANDLER_GO = SRC_ROOT / "server/service/handler.go"
ALIASES_GO = SRC_ROOT / "server/service/handler_deprecated_paths.go"
if not HANDLER_GO.exists():
    print(f"skipped: no Fleet source at {HANDLER_GO}")
    sys.exit(0)

# All files that register routes on the server's router: the main handler plus
# the feature modules serve.go passes to MakeHandler as HandlerRoutesFunc
# (android MDM, activity, ACME, chart at this tag). The repo-wide sweep at the
# bottom fails loudly if a new module starts registering routes outside this list.
HANDLER_FILES = [
    "server/service/handler.go",
    "server/mdm/android/service/handler.go",
    "server/activity/internal/service/handler.go",
    "server/mdm/acme/internal/service/handler.go",
    "server/chart/internal/service/handler.go",
]

CONSTRUCTOR_CLASS = {
    "newUserAuthenticatedEndpointer": "user (session or API token)",
    # The chart module builds its own middleware wrapping auth.AuthenticatedUser,
    # so its one route authenticates as an ordinary user (verified at the tag).
    "newChartEndpointer": "user (session or API token)",
    "newDeviceAuthenticatedEndpointer": "device (device token)",
    "newHostAuthenticatedEndpointer": "host (osquery node key)",
    "newOrbitAuthenticatedEndpointer": "orbit (orbit node key)",
    "androidAuthenticatedEndpointer": "android (orbit node key)",
    "newNoAuthEndpointer": "none",
    "newOrbitNoAuthEndpointer": "none (orbit enroll)",
    # ACME protocol endpoints authenticate inside the handlers (JWS); the
    # endpointer itself installs no auth, which is what the constructor name says.
    "newEndpointerWithNoAuth": "none (protocol auth in handler)",
}
VERBS = ("GET", "POST", "PUT", "PATCH", "DELETE", "HEAD")


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


def strip_file(path):
    return "\n".join(strip_comments(l) for l in path.read_text().split("\n"))


def find_call_args(text, start):
    """Given index of '(' opening a call, return (args_text, index_after_close)."""
    depth, i, n = 0, start, len(text)
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
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return text[start + 1:i], i + 1
        i += 1
    return None, n


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


def chain_head(text, dot_pos):
    """Walk left from the '.' before a verb through a method chain (possibly
    multi-line, dot at end of line) to the receiver identifier. Returns
    (head_identifier, head_start_index) or (None, dot_pos)."""
    i = dot_pos - 1
    while True:
        while i >= 0 and text[i] in " \t\n":
            i -= 1
        if i >= 0 and text[i] == ")":
            depth = 0
            while i >= 0:
                if text[i] == ")":
                    depth += 1
                elif text[i] == "(":
                    depth -= 1
                    if depth == 0:
                        break
                i -= 1
            if i < 0:
                return None, dot_pos
            i -= 1  # left of '('
        end = i
        while i >= 0 and (text[i].isalnum() or text[i] == "_"):
            i -= 1
        if end == i:  # no identifier where one was expected
            return None, dot_pos
        ident_start = i + 1
        j = i
        while j >= 0 and text[j] in " \t\n":
            j -= 1
        if j >= 0 and text[j] == ".":
            i = j - 1
            continue
        return text[ident_start:end + 1], ident_start


def balanced_brace_span(t, open_pos):
    """Index just past the '}' matching the '{' at open_pos, quote-aware.
    Needed because deprecated paths themselves contain braces ({fleet_id},
    {id:[0-9]+}), which break any regex that stops at the first '}'."""
    depth, i, n = 0, open_pos, len(t)
    quote = None
    while i < n:
        c = t[i]
        if quote:
            if c == "\\" and quote == '"':
                i += 2
                continue
            if c == quote:
                quote = None
        elif c in ('"', "`"):
            quote = c
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return n


# --- constant path resolution -------------------------------------------------
module_prefix = None
gomod = SRC_ROOT / "go.mod"
if gomod.exists():
    m = re.search(r"^module\s+(\S+)", gomod.read_text(), re.M)
    if m:
        module_prefix = m.group(1)

const_cache = {}


def resolve_in_dir(search_dir, ident, depth):
    """Find `ident = "..."` or `ident = OtherIdent + "..."` in a package dir.
    Follows same-package concatenation one identifier deep per level, bounded."""
    if depth > 3:
        return None
    values = set()
    for f in sorted(search_dir.glob("*.go")):
        if f.name.endswith("_test.go"):
            continue
        ftext = strip_file(f)
        # covers both const-block entries (`Ident = "..."`) and single-line
        # declarations (`const ident = "..."`)
        for dm in re.finditer(r"^\s*(?:const\s+)?" + re.escape(ident) + r'\s*=\s*"([^"]*)"\s*$', ftext, re.M):
            values.add(dm.group(1))
        for dm in re.finditer(r"^\s*(?:const\s+)?" + re.escape(ident) + r'\s*=\s*(\w+)\s*\+\s*"([^"]*)"\s*$', ftext, re.M):
            base = resolve_in_dir(search_dir, dm.group(1), depth + 1)
            if base is not None:
                values.add(base + dm.group(2))
    return values.pop() if len(values) == 1 else None


def resolve_const(expr, imports, local_dir):
    """Resolve `pkg.Ident` or a package-local `ident` to its string value by
    scanning the defining package's files for a single consistent declaration.
    Returns None when not found or ambiguous."""
    m = re.match(r"^(\w+)\.(\w+)$", expr)
    if m:
        alias, ident = m.group(1), m.group(2)
        search_dir = SRC_ROOT / imports[alias] if alias in imports else None
    elif re.match(r"^[a-zA-Z_]\w*$", expr):
        ident = expr
        search_dir = local_dir
    else:
        return None
    if not (search_dir and search_dir.is_dir()):
        return None
    key = (str(search_dir), ident)
    if key not in const_cache:
        const_cache[key] = resolve_in_dir(search_dir, ident, 0)
    return const_cache[key]


def handler_name(expr):
    expr = " ".join(expr.split())
    m = re.match(r"^([\w.]+)", expr)
    return m.group(1) if m else expr


# --- per-file scan ------------------------------------------------------------
found = 0
rows = []       # (method, path, auth, handler, rel, lineno, note)
raw_rows = []   # same shape; auth column carries the registration group
unparsed = []   # (rel, lineno, fragment, reason)
verb_sites_attributed = 0
verb_sites_independent = 0

# \s* after the dot: chained registrations often put the verb on a continuation
# line (`ne.WithAltPaths("...").` newline `POST(...)`)
verb_re = re.compile(r"\.\s*(" + "|".join(VERBS) + r"|PathHandler)\(")
independent_re = re.compile(r"(?<![A-Za-z0-9_])(?:" + "|".join(VERBS) + r"|PathHandler)\(")
ctor_re = re.compile(
    r"^\s*(\w+)\s*:?=\s*(new\w*Endpointer\w*|\w+AuthenticatedEndpointer)\(", re.M)


def scan_file(rel):
    global found, verb_sites_attributed, verb_sites_independent
    path = SRC_ROOT / rel
    if not path.exists():
        unparsed.append((rel, 0, rel, "listed handler file missing; the module may have moved"))
        return
    raw_src = path.read_text()
    text = strip_file(path)

    def line_of(offset):
        return text.count("\n", 0, offset) + 1

    func_starts = [(m.start(), m.group(1)) for m in re.finditer(r"^func (?:\([^)]*\) )?(\w+)", text, re.M)]

    def func_of(offset):
        name = "?"
        for start, fname in func_starts:
            if start <= offset:
                name = fname
            else:
                break
        return name

    imports = {}
    for m in re.finditer(r'^\t(?:(\w+) )?"([^"]+)"', raw_src, re.M):
        alias, ipath = m.group(1), m.group(2)
        if module_prefix and ipath.startswith(module_prefix + "/"):
            imports[alias or ipath.rsplit("/", 1)[-1]] = ipath[len(module_prefix) + 1:]

    def parse_path(expr):
        expr = expr.strip()
        pm = re.match(r'^"([^"]*)"$', expr)
        if pm:
            return pm.group(1)
        return resolve_const(expr, imports, path.parent)

    # endpointer variable tracking: constructor calls, then derived/tuple/reassigned vars
    env_vars = {}
    for m in ctor_re.finditer(text):
        ctor = m.group(2)
        env_vars[m.group(1)] = (CONSTRUCTOR_CLASS.get(ctor, f"constructor {ctor}"), ctor)
    changed = True
    while changed:
        changed = False
        for m in re.finditer(r"^\s*(\w+)\s*,?\s*(\w*)\s*:?=\s*(\w+)(?:\.|,|\s*$)", text, re.M):
            lhs1, lhs2, rhs = m.group(1), m.group(2), m.group(3)
            if rhs in env_vars:
                for lhs in (lhs1, lhs2):
                    if lhs and lhs not in env_vars and lhs not in ("if", "for", "return", "var"):
                        env_vars[lhs] = (env_vars[rhs][0], f"derived from {rhs}")
                        changed = True

    verb_sites_independent += len(independent_re.findall(text))

    for m in verb_re.finditer(text):
        verb = m.group(1)
        args_text, _ = find_call_args(text, m.end() - 1)
        args = split_args(args_text) if args_text is not None else []
        lineno = line_of(m.start(1))  # line of the verb, not of a trailing dot on the previous line
        head, head_start = chain_head(text, m.start())
        found += 1
        verb_sites_attributed += 1
        if head is None or head not in env_vars:
            unparsed.append((rel, lineno, " ".join(text[m.start():m.start() + 120].split()),
                             f"receiver {head!r} is not a recognized endpointer"))
            continue
        auth = env_vars[head][0]
        chain = text[head_start:m.start()]
        if verb == "PathHandler":
            method = args[0].strip('"') if args else "?"
            path_expr = args[1] if len(args) > 1 else ""
            h_expr = args[2] if len(args) > 2 else ""
        else:
            method = verb
            path_expr = args[0] if args else ""
            h_expr = args[1] if len(args) > 1 else ""
        route_path = parse_path(path_expr)
        if route_path is None:
            unparsed.append((rel, lineno, " ".join(text[head_start:m.start() + 40].split()),
                             f"path expression {path_expr!r} did not resolve to a single string"))
            continue
        notes = []
        for vm in re.finditer(r"\.\s*(StartingAtVersion|EndingAtVersion)\(\s*\"([^\"]+)\"\s*\)", chain):
            notes.append(f"{vm.group(1)}({vm.group(2)})")
        if "UsePathPrefix()" in chain.replace(" ", ""):
            notes.append("path prefix, not exact match")
        hname = handler_name(h_expr)
        rows.append((method, route_path, auth, hname, rel, lineno, "; ".join(notes)))
        # WithAltPaths aliases are real registered routes
        for am in re.finditer(r"\.\s*WithAltPaths\(", chain):
            alt_args, _ = find_call_args(chain, am.end() - 1)
            for alt in split_args(alt_args or ""):
                alt_path = parse_path(alt)
                found += 1
                if alt_path is None:
                    unparsed.append((rel, lineno, alt.strip()[:120], "WithAltPaths argument did not resolve"))
                else:
                    rows.append((method, alt_path, auth, hname, rel, lineno, f"alt path of {route_path}"))

    # raw ServeMux / router Handle calls
    for m in re.finditer(r"\b(\w+)\.Handle\(", text):
        found += 1
        lineno = line_of(m.start())
        args_text, _ = find_call_args(text, m.end() - 1)
        args = split_args(args_text) if args_text is not None else []
        route_path = parse_path(args[0]) if args else None
        group = func_of(m.start())
        if route_path is None:
            unparsed.append((rel, lineno, " ".join(text[m.start():m.start() + 120].split()),
                             f"path expression {(args[0] if args else '')!r} did not resolve"))
            continue
        h_expr = handler_name(args[1]) if len(args) > 1 else "?"
        raw_rows.append(("ANY", route_path, f"raw: {group}", h_expr, rel, lineno, ""))


for rel in HANDLER_FILES:
    scan_file(rel)

# --- deprecated path aliases --------------------------------------------------
alias_rows = []
route_index = {(r[0], r[1]): r for r in rows}
if ALIASES_GO.exists():
    arel = str(ALIASES_GO.relative_to(SRC_ROOT))
    atext = strip_file(ALIASES_GO)
    alias_entries_found = len(re.findall(r"\bMethod:", atext))
    matched = 0
    for am in re.finditer(
            r'\{\s*Method:\s*"(\w+)",\s*PrimaryPath:\s*"([^"]+)",\s*DeprecatedPaths:\s*\[\]string\{',
            atext, re.S):
        matched += 1
        method, primary = am.group(1), am.group(2)
        dep_blob = atext[am.end() - 1:balanced_brace_span(atext, am.end() - 1)]
        lineno = atext.count("\n", 0, am.start()) + 1
        primary_row = route_index.get((method, primary))
        auth = primary_row[2] if primary_row else None
        deps = re.findall(r'"([^"]+)"', dep_blob)
        if not deps:
            found += 1
            unparsed.append((arel, lineno, f"{method} {primary}",
                             "alias entry with no readable deprecated paths"))
        for dep in deps:
            found += 1
            if auth is None:
                unparsed.append((arel, lineno, f"{method} {dep} -> {primary}",
                                 "primary route not found among parsed registrations"))
            else:
                alias_rows.append((method, dep, auth, primary, arel, lineno, ""))
    if matched != alias_entries_found:
        unparsed.append((arel, 0, f"{alias_entries_found - matched} alias entries",
                         "entry shape did not match the Method/PrimaryPath/DeprecatedPaths pattern"))
else:
    unparsed.append((str(ALIASES_GO), 0, "", "deprecated-alias table file missing"))

# --- repo-wide sweep: route registrations outside the scanned files -----------
# Any non-test .go file under server/ that both constructs an endpointer and
# makes a verb call on one is a handler file; if it is not in HANDLER_FILES the
# catalog is incomplete and must say so.
sweep_hits = []
for f in sorted((SRC_ROOT / "server").rglob("*.go")):
    rel = str(f.relative_to(SRC_ROOT))
    if f.name.endswith("_test.go") or rel in HANDLER_FILES:
        continue
    try:
        t = strip_file(f)
    except UnicodeDecodeError:
        continue
    if ctor_re.search(t) and verb_re.search(t):
        sweep_hits.append(rel)
for rel in sweep_hits:
    unparsed.append((rel, 0, rel,
                     "file registers routes but is not in this generator's HANDLER_FILES list"))

parsed = len(rows) + len(raw_rows) + len(alias_rows)
commit = src_commit()

out = []
out.append("<!-- GENERATED by build/gen-api-catalog.py; do not edit by hand.")
out.append(f"     source: {', '.join(HANDLER_FILES)} + handler_deprecated_paths.go @ {commit}")
out.append(f"     registrations found: {found}; routes parsed: {parsed} "
           f"({len(rows)} endpointer incl. alt paths, {len(alias_rows)} deprecated aliases, "
           f"{len(raw_rows)} raw mux); unparsed: {len(unparsed)} -->")
out.append("")
out.append("# HTTP routes as registered by the server")
out.append("")
out.append("Every row is a route the server binds: the endpointer registrations in")
out.append("`server/service/handler.go` and the feature-module handler files mounted by")
out.append("`cmd/fleet/serve.go`, the declarative alias table in `handler_deprecated_paths.go`,")
out.append("and the raw mux registrations for the MDM protocol services. `_version_` stands")
out.append("for the supported API versions (`v1`, `2022-04`) unless a note constrains it.")
out.append("The Auth column names what a caller must present. The classes are:")
out.append("")
for label in sorted(set(CONSTRUCTOR_CLASS.values())):
    out.append(f"- {label}")
out.append("- route-local or protocol (registered directly on the router; see the raw mux section)")
out.append("")
out.append("The handler function and, for raw routes, the registration group are kept in each")
out.append("row's HTML comment beside the source line, not in a reader-facing column.")
out.append("")
out.append("## API endpoints")
out.append("")
out.append("| Method | Path | Auth |")
out.append("|---|---|---|")
for method, path, auth, hname, rel, lineno, note in rows:
    comment = f"<!-- {rel}:{lineno}{'; ' + note if note else ''}; handler {hname} -->"
    out.append(f"| {method} | `{path}` | {auth} {comment}|")
out.append("")
out.append("## Deprecated path aliases")
out.append("")
out.append("Old paths still served, mapped onto the same handler as their current path by the")
out.append("server's declarative alias table.")
out.append("")
out.append("| Method | Deprecated path | Auth | Serves |")
out.append("|---|---|---|---|")
for method, path, auth, target, rel, lineno, _ in alias_rows:
    comment = f"<!-- {rel}:{lineno} -->"
    out.append(f"| {method} | `{path}` | {auth} | alias of `{target}` {comment}|")
out.append("")
out.append("## Raw mux routes (MDM protocol and setup)")
out.append("")
out.append("Registered directly on the router rather than through an endpointer. Each of these")
out.append("carries its own protocol authentication (a device-management certificate, a SCEP")
out.append("challenge, or pre-setup state) rather than a Fleet credential.")
out.append("")
out.append("| Method | Path | Auth |")
out.append("|---|---|---|")
for method, path, group, hname, rel, lineno, _ in raw_rows:
    comment = f"<!-- {rel}:{lineno}; {group}; handler {hname} -->"
    out.append(f"| {method} | `{path}` | route-local or protocol {comment}|")
out.append("")
if unparsed:
    out.append("## UNPARSED registrations")
    out.append("")
    out.append("These look like route registrations but resisted mechanical extraction.")
    out.append("They are listed verbatim rather than guessed at; read the cited line.")
    out.append("")
    for rel, lineno, frag, reason in unparsed:
        out.append(f"- `{rel}:{lineno}` -- {reason}: `{frag}`")
    out.append("")

md = "\n".join(out)
args = sys.argv[1:]
if "--out" in args:
    pathlib.Path(args[args.index("--out") + 1]).write_text(md + "\n")
else:
    print(md)

print(f"api catalog: {found} registrations found, {parsed} routes parsed "
      f"({len(rows)} endpointer incl. alt paths, {len(alias_rows)} deprecated aliases, "
      f"{len(raw_rows)} raw mux), {len(unparsed)} unparsed, source commit {commit[:12]}",
      file=sys.stderr)
# no-silent-drop check: an independent, dumber count of verb-shaped call sites in
# the scanned files must equal the verb sites this parser attributed (to a row or
# an UNPARSED entry). A mismatch means the registration shape changed and
# something was skipped without being surfaced.
if verb_sites_independent != verb_sites_attributed:
    print(f"WARNING: {verb_sites_independent} verb-shaped call sites in scanned files but "
          f"{verb_sites_attributed} attributed; the registration shape may have changed",
          file=sys.stderr)
    sys.exit(1)
if sweep_hits:
    print(f"WARNING: route registrations outside HANDLER_FILES: {', '.join(sweep_hits)}",
          file=sys.stderr)
    sys.exit(1)
sys.exit(1 if unparsed and "--strict" in args else 0)
