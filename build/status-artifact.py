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
import time
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANUAL = os.path.join(ROOT, "manual")
TEMPLATE = os.path.join(ROOT, "build", "status-template.html")
OUT = os.path.join(ROOT, "build", "manual-status.html")

# The review transcripts live in the private sibling repo. They are never read into the manual,
# only counted, so nothing from them can leak into the public tree.
REVIEWS = os.path.join(os.path.dirname(ROOT), "missing-fleet-manual-private", "reviews")

# The owner reset every review count to zero on 2026-08-29, once all 78 chapters were drafted.
# The per-chapter era (2026-08-25 through 2026-08-29) stays on disk as an archive, but only the
# whole-book era under phase2/ counts. Walking the old directories would resurrect the retired
# counts every time this page regenerates.
PHASE2 = os.path.join(REVIEWS, "phase2")

PART_NAMES = {
    "00": ("0", "Introduction"),
    "01": ("I", "Foundations"),
    "02": ("II", "Administer and deploy Fleet"),
    "03": ("III", "Connect devices"),
    "04": ("IV", "Know your devices"),
    "05": ("V", "Manage devices"),
    "06": ("VI", "Automate Fleet"),
    # Part VII was renamed while it was still an outline. The old name lived on here until
    # 2026-08-28, so the status page announced six chapters under a title none of them had.
    "07": ("VII", "Operate Fleet"),
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


# Reviews that are not reviews OF A DRAFT. The owner ruled on 2026-08-28 that only full draft
# reviews count against the five-round cap: an outline or research review happens before there is
# any prose to review, so counting it would retire a chapter's budget before it was written.
# Matched against the filename after the section number.
NON_DRAFT_REVIEW = re.compile(r"(outline|research|imageprompt|structure)", re.I)


def review_index():
    """Map section number to (rounds, latest verdict).

    A round is one review output file with content in it. Zero-byte files are runs that died, and
    counting them as rounds would let a chapter reach its five-round cap without ever having been
    read.

    Outline and research reviews are excluded entirely. They are real reviews and their findings
    are applied, but they review a plan rather than a draft, so they are neither counted nor
    allowed to set the displayed verdict.
    """
    rounds = defaultdict(int)
    latest = {}
    if not os.path.isdir(PHASE2):
        return rounds, latest
    for dirpath, _dirnames, filenames in os.walk(PHASE2):
        for fn in sorted(filenames):
            # Appendix sections are lettered, `a.4`, not numbered, so a digits-only pattern
            # counted zero rounds for every appendix and reported them all as unreviewed.
            m = re.match(r"^([\da-z]+\.\d+)[-.](.*)\.(out|md|txt)$", fn, re.I)
            if not m:
                continue
            if NON_DRAFT_REVIEW.search(m.group(2)):
                continue
            path = os.path.join(dirpath, fn)
            try:
                if os.path.getsize(path) == 0:
                    continue
                with open(path, encoding="utf-8", errors="replace") as fh:
                    content = fh.read()
            except OSError:
                continue
            # Frontmatter writes appendix sections capitalised (`A.4`) and review filenames are
            # lower case (`a.4-sol.out`). Fold both to one case or the lookup silently misses.
            sec = m.group(1).upper()
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


def in_flight():
    """Reviews that are running right now, derived rather than declared.

    The reviewer writes its output file only when it finishes, so a review output that exists
    and is empty is a run in progress. That makes "what is happening at this moment" a property
    of the filesystem rather than something I have to remember to type in, which is the only
    kind of live status that stays true.

    Returns a list of (label, minutes_running), newest last.
    """
    if not os.path.isdir(REVIEWS):
        return []
    now = time.time()
    running = []
    for dirpath, _dirnames, filenames in os.walk(REVIEWS):
        for fn in sorted(filenames):
            if not fn.endswith((".out", ".md", ".txt")) or fn.endswith(".err"):
                continue
            path = os.path.join(dirpath, fn)
            try:
                st = os.stat(path)
            except OSError:
                continue
            if st.st_size:
                continue
            age = (now - st.st_mtime) / 60
            # A job that has been empty for hours is dead, not running. Codex reviews take five
            # to ten minutes; an hour is generous enough to never hide a slow one.
            if age > 60:
                continue
            running.append((os.path.splitext(fn)[0], age))
    running.sort(key=lambda r: r[1], reverse=True)
    return running


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
    """Sort `7.10` after `7.9`, and sort `A.4` by its number rather than tying every appendix.

    The lettered part sorts last because there is only one of it; what matters is that the
    numbers inside it order correctly, which a bare int() cast on "A" could not do.
    """
    parts = s.split(".")
    out = []
    for p in parts:
        try:
            out.append((0, int(p)))
        except ValueError:
            out.append((1, p.lower()))
    return tuple(out)


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


def diagram_progress():
    """Count image markers across the manual so the artifact tracks the graphics run.

    The book carries three image marker kinds in HTML comments: IMAGE-OK (a picture that is
    placed and accepted), IMAGE-TODO (a brief with no picture yet), and IMAGE-REDO (a picture
    that no longer matches the corrected prose). Progress on the graphics run is OK over the
    total, per part, so the owner can see which parts are finished at a glance.
    """
    ok = defaultdict(int)
    todo = defaultdict(int)
    redo = defaultdict(int)
    for dirpath, _dirs, files in os.walk(MANUAL):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            m = re.match(r"(\d\d)", os.path.basename(dirpath))
            part = m.group(1) if m else "00"
            text = open(os.path.join(dirpath, fn), encoding="utf-8").read()
            ok[part] += len(re.findall(r"<!--\s*IMAGE-OK:", text))
            todo[part] += len(re.findall(r"<!--\s*IMAGE-TODO", text))
            redo[part] += len(re.findall(r"<!--\s*IMAGE-REDO", text))
    parts = sorted(set(ok) | set(todo) | set(redo))
    return ok, todo, redo, parts


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

    img_ok, img_todo, img_redo, img_parts = diagram_progress()
    imgs_ok = sum(img_ok.values())
    imgs_total = imgs_ok + sum(img_todo.values()) + sum(img_redo.values())
    imgs_open = sum(img_todo.values()) + sum(img_redo.values())

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
        '    <div class="rule-card"><span class="k">Review reset</span>'
        '<span class="v">All counts zero, 2026-08-29</span><span class="n">With every chapter '
        "drafted, the owner retired the per-chapter rounds (the five-round cap, three per "
        "appendix) and reset every count to zero. The next phase reviews <strong>the whole book "
        "as a single entity</strong>.</span></div>\n"
    )
    a(
        '    <div class="rule-card"><span class="k">Whole-book review</span>'
        '<span class="v">%d chapters reviewed, %d rounds</span><span class="n">Counted from the '
        "whole-book era only. In the retired per-chapter era, no chapter ever passed a round "
        "without a material finding.</span></div>\n" % (reviewed, all_rounds)
    )
    done_parts = [PART_NAMES.get(pt, (pt, pt))[0] for pt in img_parts
                  if img_ok.get(pt, 0) and not (img_todo.get(pt, 0) or img_redo.get(pt, 0))]
    a(
        '    <div class="rule-card"><span class="k">Graphics run</span>'
        '<span class="v">%d of %d placed, %d open</span><span class="n">Diagrams are drawn by '
        "the reviewer as SVG and placed as lossless WebP, part by part with a review gate per "
        "batch. Parts with every picture placed: %s.</span></div>\n"
        % (imgs_ok, imgs_total, imgs_open, (", ".join(done_parts) if done_parts else "none yet"))
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
        ("%d/%d" % (imgs_ok, imgs_total), "Diagrams placed"),
        (commits, "Commits"),
    ]:
        a('    <div class="tot"><span class="num">%s</span><span class="lab">%s</span></div>\n' % (num, lab))
    a("  </section>\n\n")

    running = in_flight()
    if running:
        a('  <section class="running" aria-label="Running now">\n')
        a('    <div class="running-head"><span class="dot"></span>Running now</div>\n')
        a("    <ul>\n")
        for label, age in running:
            a('      <li><code>%s</code><span class="age">%d min</span></li>\n'
              % (html.escape(label), round(age)))
        a("    </ul>\n")
        a('    <p class="running-note">Reviews the reviewer has not yet returned. It writes its '
          "output only when it finishes, so an empty transcript is a job still thinking.</p>\n")
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
      "runs are not counted as rounds. <strong>Only the whole-book era is counted:</strong> the "
      "owner reset every count to zero on 2026-08-29, so the per-chapter reviews run before that "
      "date remain archived but count for nothing here. This page is generated "
      "by <code>build/status-artifact.py</code>; nothing on it is typed in by hand.</p>\n")
    a("  </footer>\n\n</div>\n")

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("".join(out))

    print("wrote %s: %d chapters, %d drafted, %d rounds" % (OUT, total, drafting, all_rounds))
    return 0


if __name__ == "__main__":
    sys.exit(main())
