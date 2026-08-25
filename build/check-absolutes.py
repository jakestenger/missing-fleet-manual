#!/usr/bin/env python3
"""Flag absolute and universal claims for re-verification.

Written 2026-08-25 after an external review found a material defect in all twelve Part II
chapters. Five of them shared one shape: a universal or absolute claim built from a partial
reading. "Neither survives the second one." "Nothing else." "Fleet instances never get bigger."
"Nothing is replayed." "Every published configuration."

None of those was a sourcing failure. Each cited a real source that said something narrower.
The absolute was added in composition and never re-examined, because by verification time it had
become the author's belief about what the source said.

This does not judge correctness. It surfaces the sentences where the gap between "what I checked"
and "what I wrote" is most likely to have opened, so they can be re-read against the source with
the specific question: did I verify the universal, or sample and generalize?

Backtested against the twelve Part II chapters as they stood before the 2026-08-25 review, a
tree containing seven defects of a shape these two scripts could in principle detect. Together
with check-headings.py this found five of six absolute-shaped ones and both heading-shaped ones,
across thirty flags in twelve chapters. Roughly two to three flags per chapter, one in four of
them real.

The miss is instructive: "changes almost nothing about how it runs, and exactly one thing about
how you deploy a new version" was suppressed because the sentence hedges its first half. A
sentence can hedge one clause and overreach in the next, and this check cannot see that.

It also cannot see the other five defects at all. Two were chapters contradicting themselves and
three were inferences that read as verified fact. Neither shape has a signature.

Advisory. Always exits 0.
"""
import re, sys, pathlib

# Strongest signals first. These rarely appear in a correctly hedged factual sentence.
STRONG = [
    # Absolutes that close an enumeration the author just made.
    r"\bnothing (?:else|but|more)\b", r"\bno other\b", r"\bnone of (?:them|these|those)\b",
    r"\bneither (?:survives|works|applies|is|does|of)\b", r"\ball of them\b",
    r"\bthe only (?:one|thing|way|setting|component)\b",
    # Counts asserted about a set.
    r"\bexactly (?:one|two|three|four|\d+) (?:thing|way|of|reason)", r"\bonly (?:one|two) (?:thing|way)",
    # Universals over a set that was sampled rather than enumerated.
    r"\bevery (?:published|single|sized|documented|one of)\b", r"\bin every (?:case|configuration|row)\b",
    r"\b(?:never|always) (?:get|gets|grow|grows|the answer|happens|applies)\b",
    # Blanket denials of a whole capability.
    r"\bnothing is (?:replayed|retried|logged|reported|kept)\b",
]
# Weaker: common in legitimate prose, reported separately.
WEAK = [r"\bevery\b", r"\ball \w+ (?:are|is|have|has)\b", r"\bcannot\b", r"\bmust always\b"]

# A sentence that already limits itself is not the failure mode this looks for.
HEDGE = re.compile(
    r"\b(almost|usually|typically|generally|mostly|often|in most|by default|at this release|"
    r"unless|except|only when|only if|on \w+ hosts|for \w+ hosts|personally|when you)\b", re.I)

MANUAL = pathlib.Path("manual")

def sentences(text):
    return re.split(r"(?<=[.!?])\s+(?=[A-Z*`\[])", text)

def scan(patterns):
    out = []
    for path in sorted(MANUAL.rglob("*.md")):
        body = re.sub(r"<!--.*?-->", " ", path.read_text(), flags=re.S)   # image briefs are specs
        body = re.sub(r"```.*?```", " ", body, flags=re.S)                # code is not prose
        incode = False
        for para in body.split("\n"):
            s = para.strip()
            if not s or s.startswith(("#", ">")):
                continue
            for sent in sentences(s):
                if HEDGE.search(sent):
                    continue
                for pat in patterns:
                    if re.search(pat, sent, re.I):
                        out.append((path, re.search(pat, sent, re.I).group(0), sent.strip()[:155]))
                        break
    return out

strong = scan(STRONG)
weak = [w for w in scan(WEAK) if w[2] not in {s[2] for s in strong}]

print(f"{len(strong)} unhedged absolute claim(s) to re-verify:\n")
for path, hit, sent in strong:
    print(f"  {path.name}")
    print(f"    [{hit}] {sent}\n")
print(f"({len(weak)} weaker universal(s) not listed; run with --all to see them)")
if "--all" in sys.argv:
    print()
    for path, hit, sent in weak:
        print(f"  {path.name}\n    [{hit}] {sent}\n")
sys.exit(0)
