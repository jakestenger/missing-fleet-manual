#!/usr/bin/env python3
"""Check that attributive cross-references are plausible.

check-links.py verifies that a link target exists. It cannot tell whether a sentence like
"as [2.9](...) notes, escrowed Linux disk encryption data" is true of 2.9. That defect class
shipped undetected and was found by an external reviewer, so this closes the gap.

The check is deliberately fuzzy and advisory. For every cross-reference whose sentence
attributes content to the target ("notes", "covers", "explains" ...), it collects the
distinctive words of that sentence and warns when the target file contains none of them.
Zero overlap is a strong signal; partial overlap is not, so only zero is reported.

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

if warnings:
    print(f"{len(warnings)} cross-reference(s) with no term overlap in the target:\n")
    for src, tgt, sent, terms in warnings:
        print(f"  {src}")
        print(f"    -> {tgt.relative_to(pathlib.Path.cwd())}")
        print(f"    {sent}")
        print(f"    looked for: {', '.join(terms)}\n")
else:
    print("cross-references: no zero-overlap attributions found")
sys.exit(0)
