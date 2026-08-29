#!/usr/bin/env python3
"""Advisory prose-integrity checks.

Two checks, both advisory. Neither gates CI; both print for a human to judge.

1. Attributive cross-references.

check-links.py verifies that a link target exists. It cannot tell whether a sentence like
"as [2.9](...) notes, escrowed Linux disk encryption data" is true of 2.9. That defect class
shipped undetected and was found by an external reviewer, so this closes the gap.

The check is deliberately fuzzy and advisory. For every cross-reference whose sentence
attributes content to the target ("notes", "covers", "explains" ...), it collects the
distinctive words of that sentence and warns when the target file contains none of them.
Zero overlap is a strong signal; partial overlap is not, so only zero is reported.

2. Source-file citations in prose. STYLE §8 keeps them in the ledger, where a reader can check
   the verification, and out of the chapter, where they date the text and help nobody. Seven had
   accumulated in two chapters before an external review prompted a look.

3. Eaten code spans. Writing a chapter through an unquoted heredoc lets the shell
   consume a `backticked` span via command substitution, leaving a double space where the
   code used to be. That happened once, shipped, and stayed live until an external review
   read the sentence. The signature is a double space mid-sentence outside code and tables.

Exits 0 always. This informs a human, it does not gate CI.
"""
import re, sys, pathlib

ATTRIBUTIVE = re.compile(
    r"\b(notes?|covers?|describes?|explains?|establishes?|records?|shows?|sets out|"
    r"documents?|lists?|gives?|has|carries|owns?|discusses|details?)\b", re.I)

STOP = set("""the a an and or but if then that this these those there here it its it's is are was
were be been being of in on at to from by for with without into over under about across as than
so such not no nor only own same too very can will just don should now what which who whom whose
when where why how all any both each few more most other some own also each every either neither
you your yours we our ours they their theirs he she his her them us me my i chapter section part
manual fleet page above below covered covers cover see read reads reading first second third
things thing way ways make makes made take takes taken give gives given get gets got come comes
one two three four five six seven eight nine ten""".split())

MANUAL = pathlib.Path("manual")
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+\.md)(?:#[^)]*)?\)")

def sentences(text):
    # Split on sentence enders followed by space+capital, keeping it crude but adequate.
    return re.split(r"(?<=[.!?])\s+(?=[A-Z*`\[])", text)

def words(s):
    s = re.sub(r"\[[^\]]*\]\([^)]*\)", " ", s)          # drop link syntax
    s = re.sub(r"`[^`]*`", " ", s)                       # drop code spans
    out = set()
    for w in re.findall(r"[A-Za-z][A-Za-z'-]{4,}", s):
        lw = w.lower().strip("'-")
        if lw and lw not in STOP:
            out.add(lw)
    return out

warnings = []
for path in sorted(MANUAL.rglob("*.md")):
    body = path.read_text()
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)   # image briefs are not prose
    for sent in sentences(body):
        for m in LINK.finditer(sent):
            if not ATTRIBUTIVE.search(sent):
                continue
            target = (path.parent / m.group(2)).resolve()
            if not target.exists():
                continue                                   # check-links.py owns that
            terms = words(sent)
            if len(terms) < 2:
                continue
            hay = target.read_text().lower()
            hits = {t for t in terms if t in hay}
            if not hits:
                warnings.append((path, target, sent.strip()[:150], sorted(terms)[:8]))

# --- check 2: source files cited in prose (STYLE §8) ---
sources = []
# A citation is still a citation with a line number on it, and STYLE forbids both. The first
# version of this pattern required the backtick to close straight after the extension, so
# `policy.rego:47` passed and `policy.rego` did not; 49 of 50 citations in a.4 were invisible.
SRC_RE = re.compile(r"`([a-z][a-z0-9_/-]*\.(?:go|tsx|ts|rego|sql|py))(?::[0-9,:-]+)?`")
for path in sorted(MANUAL.rglob("*.md")):
    body = re.sub(r"<!--.*?-->", " ", path.read_text(), flags=re.S)
    body = re.sub(r"```.*?```", " ", body, flags=re.S)
    for n, line in enumerate(body.split("\n"), 1):
        s = line.strip()
        # Headings are structural. Table rows are NOT exempt: a table is reader-facing content
        # and STYLE section 8 applies to it exactly as it applies to a paragraph. Skipping them
        # is what let a.4 ship 40 citations inside its matrix.
        if s.startswith("#"):
            continue
        for m in SRC_RE.finditer(line):
            sources.append((path.name, n, m.group(1)))

if sources:
    print(f"{len(sources)} source-file citation(s) in prose, which belong in the ledger:\n")
    for name, n, f in sources:
        print(f"  {name}:{n}  {f}")
    print()
else:
    print("prose: no source files cited outside the ledger")

# --- check 3: double space mid-sentence, the signature of a shell-eaten code span ---
spans = []
for path in sorted(MANUAL.rglob("*.md")):
    incode = False
    for n, line in enumerate(path.read_text().split("\n"), 1):
        s = line.strip()
        if s.startswith("```"):
            incode = not incode
            continue
        if incode or s.startswith(("|", "<!--", "#", ">")):
            continue
        if re.search(r"\S  +\S", line.lstrip()):
            spans.append((path, n, s[:120]))

if spans:
    print(f"{len(spans)} internal double-space(s), possible eaten code span:\n")
    for path, n, s in spans:
        print(f"  {path}:{n}\n    {s}\n")
else:
    print("prose: no suspicious internal double spaces")

if warnings:
    print(f"\n{len(warnings)} cross-reference(s) with no term overlap in the target:\n")
    for src, tgt, sent, terms in warnings:
        print(f"  {src}")
        print(f"    -> {tgt.relative_to(pathlib.Path.cwd())}")
        print(f"    {sent}")
        print(f"    looked for: {', '.join(terms)}\n")
else:
    print("cross-references: no zero-overlap attributions found")
sys.exit(0)
