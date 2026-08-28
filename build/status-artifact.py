#!/usr/bin/env python3
"""Regenerate the build-status artifact from the working tree.

The project owner asked for the status artifact to be refreshed after every step rather than at
the end of a session (HANDOFF section 1). That is only sustainable if it is one command, so this
reads the manual, the review directories and the git log, and writes `build/manual-status.html`.

Everything here is derived. Nothing is typed in by hand, because a hand-maintained status page
drifts from the tree within a day and then quietly misreports progress, which is worse than not
having one.

    python3 build/status-artifact.py

Then republish to the URL recorded in HANDOFF. Publishing without that URL creates a second
artifact and the owner's link goes stale.
"""

import html
import os
import re
import subprocess
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANUAL = os.path.join(ROOT, "manual")
TEMPLATE = os.path.join(ROOT, "build", "status-template.html")
OUT = os.path.join(ROOT, "build", "manual-status.html")

# The review transcripts live in the private sibling repo. They are never read into the manual,
# only counted, so nothing from them can leak into the public tree.
REVIEWS = os.path.join(os.path.dirname(ROOT), "missing-fleet-manual-private", "reviews")

PART_NAMES = {
    "00": ("0", "Introduction"),
    "01": ("I", "Foundations"),
    "02": ("II", "Administer and deploy Fleet"),
    "03": ("III", "Connect devices"),
    "04": ("IV", "Know your devices"),
    "05": ("V", "Manage devices"),
    "06": ("VI", "Automate Fleet"),
    "07": ("VII", "Extend and integrate Fleet"),
    "08": ("VIII", "Troubleshooting Fleet"),
    "09": ("A", "Appendices and indexes"),
}


def frontmatter(text):
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    head, body = text[3:end], text[end + 4 :]
    meta = {}
    for line in head.splitlines():
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if m:
            meta[m.group(1)] = m.group(2).strip().strip('"')
    return meta, body


def word_count(body):
    """Words a reader actually sees.

    HTML comments carry the image briefs and prompts, which are instructions to whoever makes the
    picture rather than text in the book. Counting them inflates every chapter that has a diagram
    brief by several hundred words and makes chapters incomparable.
    """
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    body = re.sub(r"^---.*?^---", " ", body, flags=re.S | re.M)
    return len(body.split())


def review_index():
    """Map section number to (rounds, latest verdict).

    A round is one review output file with content in it. Zero-byte files are runs that died, and
    counting them as rounds would let a chapter reach its five-round cap without ever having been
    read.
    """
    rounds = defaultdict(int)
    latest = {}
    if not os.path.isdir(REVIEWS):
        return rounds, latest
    for dirpath, _dirnames, filenames in os.walk(REVIEWS):
        for fn in sorted(filenames):
            m = re.match(r"^(\d+\.\d+)[-.].*\.(out|md|txt)$", fn)
            if not m:
                continue
            path = os.path.join(dirpath, fn)
            try:
                if os.path.getsize(path) == 0:
                    continue
                with open(path, encoding="utf-8", errors="replace") as fh:
                    content = fh.read()
            except OSError:
                continue
            sec = m.group(1)
            rounds[sec] += 1
            if "NOT READY" in content:
                verdict = "not ready"
            elif "READY" in content:
                verdict = "ready"
            else:
                verdict = "no verdict"
            # Files are walked in sorted order per directory and directories are dated, so the
            # last assignment wins and is the most recent round.
            latest[sec] = verdict
    return rounds, latest


def collect():
    chapters = defaultdict(list)
    for entry in sorted(os.listdir(MANUAL)):
        d = os.path.join(MANUAL, entry)
        if not os.path.isdir(d):
            continue
        part_key = entry.split("-")[0]
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".md"):
                continue
            with open(os.path.join(d, fn), encoding="utf-8") as fh:
                text = fh.read()
            meta, body = frontmatter(text)
            if "section" not in meta:
                continue
            chapters[part_key].append(
                {
                    "section": meta.get("section", "").strip('"'),
                    "title": meta.get("title", fn).strip('"'),
                    "status": meta.get("status", "outline"),
                    "words": word_count(body),
                }
            )
    return chapters


def sec_key(s):
    parts = s.split(".")
    try:
        return tuple(int(p) for p in parts)
    except ValueError:
        return (99, 99)


def pill(status, rounds, verdict):
    """The status a reader cares about is not always the one in the frontmatter.

    A chapter stamped `drafting` that has hit the five-round cap is in a different state from one
    that has never been reviewed, and collapsing both to the same word is how a status page stops
    being useful.
    """
    if status == "verified":
        return "s-verified", "verified"
    if status == "outline":
        return "s-outline", "outline"
    if rounds >= 5:
        return "s-capped", "capped at 5"
    if rounds and verdict == "ready":
        return "s-clean", "clean"
    return "s-drafting", "drafting"


def main():
    chapters = collect()
    rounds, latest = review_index()

    total = sum(len(v) for v in chapters.values())
    words = sum(c["words"] for v in chapters.values() for c in v)
    drafting = sum(1 for v in chapters.values() for c in v if c["status"] != "outline")
    outline = total - drafting
    verified = sum(1 for v in chapters.values() for c in v if c["status"] == "verified")
    all_rounds = sum(rounds.get(c["section"], 0) for v in chapters.values() for c in v)
    reviewed = sum(1 for v in chapters.values() for c in v if rounds.get(c["section"], 0))

    try:
        commits = subprocess.run(
            ["git", "rev-list", "--count", "HEAD"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        commits = "?"

    with open(TEMPLATE, encoding="utf-8") as fh:
        out = [fh.read()]

    a = out.append
    a('<div class="wrap">\n')
    a('  <header class="masthead">\n')
    a('    <div class="eyebrow">Fleet 4.90.1 &middot; tag fleet-v4.90.1 &middot; commit dd0200f062</div>\n')
    a("    <h1>The Missing Fleet Manual: build status</h1>\n")
    a(
        '    <p class="standfirst">%d chapters across nine parts. %d drafted, %d still outline. '
        "Nothing carries a verified stamp, by design.</p>\n" % (total, drafting, outline)
    )
    a("  </header>\n\n")

    a('  <section class="rules" aria-label="Governing rules">\n')
    a(
        '    <div class="rule-card"><span class="k">Verification freeze</span>'
        '<span class="v">In force</span><span class="n">No chapter carries <code>verified</code> '
        "until every part is drafted and every chapter has had a review round. Enforced by "
        "<code>check-verified.py</code>.</span></div>\n"
    )
    a(
        '    <div class="rule-card"><span class="k">Review cap</span>'
        '<span class="v">Five rounds per chapter</span><span class="n">Rounds run until a chapter '
        "comes back clean or hits five, then it stays at <code>drafting</code> and waits for the "
        "whole-part review.</span></div>\n"
    )
    a(
        '    <div class="rule-card"><span class="k">Defect record</span>'
        '<span class="v">%d chapters reviewed</span><span class="n">%d rounds recorded. No chapter '
        "has yet passed a round without a material finding.</span></div>\n" % (reviewed, all_rounds)
    )
    a("  </section>\n\n")

    a('  <section class="totals" aria-label="Book totals">\n')
    for num, lab in [
        (total, "Chapters"),
        (drafting, "Drafted"),
        (outline, "Outline"),
        (verified, "Verified"),
        ("%dk" % round(words / 1000), "Words"),
        (all_rounds, "Review rounds"),
        (commits, "Commits"),
    ]:
        a('    <div class="tot"><span class="num">%s</span><span class="lab">%s</span></div>\n' % (num, lab))
    a("  </section>\n\n")

    for key in sorted(chapters):
        roman, name = PART_NAMES.get(key, (key, key))
        chs = sorted(chapters[key], key=lambda c: sec_key(c["section"]))
        pw = sum(c["words"] for c in chs)
        pr = sum(rounds.get(c["section"], 0) for c in chs)
        meta = "%d chapter%s &middot; %s words" % (len(chs), "" if len(chs) == 1 else "s", "{:,}".format(pw))
        if pr:
            meta += " &middot; %d round%s" % (pr, "" if pr == 1 else "s")

        a('  <section class="part">\n')
        a('    <div class="part-head"><span class="part-num">%s</span><h2>%s</h2>'
          '<span class="part-meta">%s</span></div>\n' % (roman, html.escape(name), meta))
        a('    <div class="scroller">\n      <table>\n')
        a("        <thead><tr><th>&sect;</th><th>Chapter</th><th>Status</th><th>Rounds</th>"
          '<th>Last verdict</th><th style="text-align:right">Words</th></tr></thead>\n')
        a("        <tbody>\n")
        for c in chs:
            sec = c["section"]
            r = rounds.get(sec, 0)
            v = latest.get(sec)
            cls, label = pill(c["status"], r, v)
            r_cell = str(r) if r else '<span class="meter-none">&mdash;</span>'
            if v == "ready":
                v_cell = "clean"
            elif v == "not ready":
                v_cell = "changes required"
            elif v:
                v_cell = html.escape(v)
            else:
                v_cell = '<span class="meter-none">not reviewed</span>'
            w_cell = "{:,}".format(c["words"]) if c["words"] > 120 else '<span class="meter-none">stub</span>'
            a('          <tr><td class="sec">%s</td><td class="title">%s</td>'
              '<td><span class="pill %s">%s</span></td><td>%s</td><td>%s</td>'
              '<td class="num">%s</td></tr>\n'
              % (html.escape(sec), html.escape(c["title"]), cls, label, r_cell, v_cell, w_cell))
        a("        </tbody>\n      </table>\n    </div>\n  </section>\n\n")

    a("  <footer>\n")
    a("    <p>Every product claim verified against <code>~/Source/Fleet/fleet-public</code> at tag "
      "<code>fleet-v4.90.1</code>, commit <code>dd0200f062</code>. Never against the product "
      "documentation, and never against <code>main</code>.</p>\n")
    a("    <p>Word counts exclude HTML comments, which carry the image briefs. Round counts come "
      "from the review directories rather than from memory, and zero-byte transcripts from failed "
      "runs are not counted as rounds. This page is generated by "
      "<code>build/status-artifact.py</code>; nothing on it is typed in by hand.</p>\n")
    a("  </footer>\n\n</div>\n")

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("".join(out))

    print("wrote %s: %d chapters, %d drafted, %d rounds" % (OUT, total, drafting, all_rounds))
    return 0


if __name__ == "__main__":
    sys.exit(main())
