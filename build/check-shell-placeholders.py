#!/usr/bin/env python3
"""Fail on a copyable shell command whose placeholder the shell would read as redirection.

`--enroll-secret=<secret>` inside a code fence looks like a placeholder and behaves like input
redirection: the shell tries to open a file named `secret` and the command fails before Fleet is
contacted. An independent review found it in this manual's primary macOS installation command,
and a sweep found it in five commands across five chapters.

Angle-bracket placeholders are the house convention and are fine. They just have to be quoted
when they sit inside a fenced block a reader will copy.
"""
import io, re, sys, pathlib

FENCE = re.compile(r"^\s*```(\w*)")
# Only shell fences. A YAML list item, a SQL predicate and a sample log line all contain
# angle brackets harmlessly; only a shell reads '<' as redirection.
SHELL = {"sh", "bash", "zsh", "shell", "console", "powershell", "ps1"}
# An unquoted <placeholder> immediately after '=' or after whitespace, inside a fence.
BAD = re.compile(r"(?<![\"'\w])<[a-z][a-z0-9._-]*>(?![\"'])")

problems = []
for path in sorted(pathlib.Path("manual").rglob("*.md")):
    infence = False
    for i, line in enumerate(io.open(path, encoding="utf-8").read().split("\n"), 1):
        m = FENCE.match(line)
        if m:
            infence = (m.group(1).lower() in SHELL) if not infence else False
            continue
        if not infence:
            continue
        # Comments and continuation text are not commands.
        if re.match(r"^\s*(#|//)", line):
            continue
        for m in BAD.finditer(line):
            # '<' preceded by whitespace or '=' is where the shell redirects.
            j = m.start()
            if j == 0 or line[j - 1] in "= \t":
                problems.append((path, i, line.strip()))
                break

if problems:
    print(f"{len(problems)} fenced command(s) with an unquoted <placeholder> "
          "the shell would read as redirection:\n")
    for path, i, line in problems:
        print(f"  {path}:{i}\n    {line}")
    print("\nQuote the placeholder: --flag=\"<value>\".")
    sys.exit(1)
print("fenced commands: no unquoted angle-bracket placeholders")
sys.exit(0)
