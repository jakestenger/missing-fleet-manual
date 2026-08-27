#!/usr/bin/env python3
"""Flag unsupported frequency claims in diagnostic prose.

A distinct defect from the absolutes `check-absolutes.py` looks for, and the one that has
survived the most review rounds on this project. It appears when a universal is corrected:
"X is the cause" becomes "X is usually the cause", which reads as hedged and is a new claim about
frequency that the source almost never establishes. Reviewers have flagged it in 8.4 three rounds
running, and in 8.8, 8.9, 3.3, 3.4, 3.5 and 3.6.

It matters because it silently reorders an incident. "Usually permissions" sends someone to
permissions first; if the tag does not rank the causes, the manual has invented a triage order.

The fix is nearly always to name the candidates without ranking them, or to say what the reading
is *consistent with*. Where a frequency really is established, say by a Fleet issue reporting a
rate, cite it in the sentence and this check's flag is answered.

Advisory. Always exits 0, because a legitimately sourced frequency claim is a real thing.
"""
import io, re, sys, pathlib

# Narrow deliberately. A frequency word describing a *mechanism* ("openssl is usually
# LibreSSL on macOS") is a fact about the world. The defect is a frequency word ranking a
# *cause*, because that invents a triage order the source does not supply. So the patterns
# require the frequency word to sit next to diagnostic vocabulary.
CAUSE = r"(?:cause|causes|reason|reasons|culprit|suspect|suspects|explanation|means|meaning|points? at|indicates?|is the answer)"
PATTERNS = [
    rf"\b(?:usually|typically|normally|generally|most often|nearly always|almost always|"
    rf"in most cases|more often than not|rarely|seldom)\b[^.]{{0,60}}\b{CAUSE}\b",
    rf"\b{CAUSE}\b[^.]{{0,60}}\b(?:usually|typically|normally|generally|most often|"
    rf"nearly always|almost always|in most cases|more often than not|rarely|seldom)\b",
    r"\bthe usual (?:cause|causes|reason|reasons|suspect|suspects)\b",
    r"\bthe most common (?:cause|reason|failure|misdiagnosis|shape)\b",
]
RX = re.compile("|".join(PATTERNS), re.I)

# A sentence that cites something alongside the claim has answered the question.
CITED = re.compile(r"fleetdm/fleet#|`cron_stats`|release notes|changelog|Fleet's own (?:notes|guide|documentation|checklist)", re.I)

hits = []
for path in sorted(pathlib.Path("manual").rglob("*.md")):
    infence = False
    for i, line in enumerate(io.open(path, encoding="utf-8").read().split("\n"), 1):
        if re.match(r"^\s*```", line):
            infence = not infence
            continue
        if infence:
            continue
        m = RX.search(line)
        if m and not CITED.search(line):
            hits.append((path, i, m.group(0), line.strip()[:130]))

if hits:
    print(f"{len(hits)} frequency claim(s) to check against the source:\n")
    for path, i, word, line in hits:
        print(f"  {path}:{i}  [{word}]\n    {line}")
    print("\nAsk of each: does the tag establish this ranking, or was a universal hedged into a\n"
          "frequency? If the latter, name the candidates without ordering them.")
else:
    print("frequency claims: none unsourced")
sys.exit(0)
