# Handoff: The Missing Fleet Manual

Written 2026-08-26. Current as of commit `f620ec8`.

Read this, then `CONTRIBUTING.md`, then `STYLE.md`. This file says where the project is and how
the work is done. Those two say what the work has to satisfy.

---

## 1. What this is

A complete, self-contained technical reference for **Fleet 4.90.1**, deep enough to explain how
Fleet actually works underneath rather than restating the product documentation.

The standard the project owner set, verbatim:

> I want complete AND correct. I don't care about length as its own metric, but I do care about
> having a complete guide that can help someone completely unfamiliar with Fleet become an expert
> in it... or as close as someone can without actual experience.

Length is not a metric. The novice-to-expert path is. When you are deciding whether something
belongs, ask whether its absence would leave a reader unable to do the thing, not whether the
chapter is long enough.

**Site:** https://d4ch3x2jqqmix.cloudfront.net (public, deploys from `main` on push)
**Repo:** https://github.com/jakestenger/missing-fleet-manual (**public**)

---

## 2. Where the work actually stands

**36 chapters written, 42 still outline stubs.** The stubs are 50 to 90 words each: a title, a
frontmatter block, and a sentence of intent. Do not mistake the file count for progress.

| Part | Chapters | State |
|---|---|---|
| 0. Introduction | 1 | Written |
| I. Foundations | 6 | Written, reviewed, corrected. Stamped `drafting` |
| II. Administer and deploy | 12 | **Complete. All 12 `verified`** |
| III. Connect devices | 7 | 3.1 and 3.7 written and reviewed. **3.2 to 3.6 are stubs** |
| IV. Know your devices | 7 | **All stubs** |
| V. Manage devices | 8 | **All stubs** |
| VI. Automate Fleet | 5 | **All stubs** |
| VII. Operate Fleet | 6 | **All stubs** |
| VIII. Troubleshooting | 14 | Written, all 14 reviewed and corrected. Stamped `drafting` |
| IX. Appendices | 8 | a.8 partial. **a.1 to a.7 are stubs** |

So: Part II is finished, Parts I and VIII are written and reviewed but not stamped, and roughly
half the book has not been written at all.

### The status ladder

`outline` → `drafting` → `verified`. `check-verified.py` gates the top rung and will fail CI if a
chapter claims `verified` without all of:

- `verified_against`, `verified_on`, `verified_source`
- `reviewed_by`, `reviewed_on`
- a notes file at `research/section-notes/<section>-notes.md`

**Parts I and VIII are stuck on the bookkeeping, not the substance.** They have been reviewed and
corrected; they lack `reviewed_by`/`reviewed_on`, and Part VIII has notes files for only 8.11
through 8.14. Promoting them is a real task with a real gate, not a formality: adding the fields
without writing the ledgers would be exactly the overclaim the gate exists to stop.

### The other outstanding item on Part VIII

Only 8.11 through 8.14 carry a `verified_against: Fleet 4.90.1` stamp. **8.1 through 8.10 still
say 4.90.0 with `NOT tag-verified`.** That is accurate rather than stale: their review findings
were applied, but the chapters were never swept against the tag as a whole. Ten chapters.

---

## 3. How a chapter gets made

This loop is the method. It was arrived at by getting things wrong, and each step exists because
skipping it shipped a defect.

**1. Read the outline stub and the neighbouring chapters.** Every chapter defers work to other
chapters. Find out what has already been claimed about your subject before you claim anything.

**2. Run `claims.py` on the mechanism you are about to describe.**

```sh
python3 build/claims.py "enroll secret"
```

It prints every sentence in the manual mentioning a term, grouped by chapter. **Do this before
writing, not after.** The single largest defect class in this project is cross-chapter
contradiction: the book already contains the right answer, in a different chapter, and the new
chapter contradicts it. Eight of the fourteen findings in the last session were exactly that.

**3. Verify every product claim against the tag**, in `~/Source/Fleet/fleet-public` at
`fleet-v4.90.1` (commit `dd0200f062`). Not against memory, not against fleetdm.com, and not
against `main`. Fleet's published documentation is wrong often enough to matter: six documentation
bugs found so far, including a config default documented as `1h` that the server registers as
`2m`, and an audit-log reference that omits 34 of 191 activity types.

**4. Write the chapter.** `STYLE.md` is 28 sections and non-negotiable. The ones most often
violated: no em-dashes; never cite a Fleet source file in prose (§8); if you state a count, make
the items findable (§26); no claims about the reader's organization (§25); delete the lesson
sentence and the definition-by-denial (§24).

**5. Write the citation ledger** at `research/section-notes/<section>-notes.md`, separating
`stated` (in Fleet's source or docs) from `derived` (the book's reasoning over verified facts)
from `unverified` (carried forward, and marked as such in the text too). §27 governs this. Two
amendments worth internalising: *"stated" is a claim about scope, not just content*, and *read it
against the book, not only against itself*.

**6. Send it for independent review.** See section 4.

**7. Apply the review, then verify the reviewer.** The reviewer is right often but not always.
In the last session it correctly caught an inverted conclusion in 8.11 and missed four timing
errors in the same table; it also recommended deleting an `[!internal]` callout convention it had
no way to know was manual-wide. Check its source citations. Record what you rejected and why, in
the ledger.

**8. Run every checker.**

```sh
python3 build/check-links.py          # CI gate, must report 0 problems
python3 build/check-verified.py       # CI gate
python3 build/check-crossrefs.py
python3 build/check-absolutes.py
python3 build/check-headings.py
python3 build/check-activity-names.py
python3 build/check-schedule-names.py
python3 build/check-table-names.py
```

**9. Unwrap, build, commit, push, confirm the deploy.**

```sh
python3 build/unwrap.py apply
cd website && npm run build
git add -A && git commit && git push origin main
gh run list --limit 1
```

`main` deploys directly. There are no feature branches and nothing to merge.

---

## 4. The independent reviewer

The project owner's arrangement, in his words: *"I'd keep you as the project lead, CGPT as the
reviewer and second opinion and myself as the final arbiter."*

Reviews run through ChatGPT's Codex CLI, invoked directly, with no human relaying anything.

```sh
/Applications/ChatGPT.app/Contents/Resources/codex exec \
  -m gpt-5.6-sol \
  -c model_reasoning_effort="high" \
  -s read-only \
  -c 'sandbox_permissions=["disk-full-read-access"]' \
  -C ~/Source/Personal/missing-fleet-manual \
  - < prompt.txt
```

Four things that trip people up:

- **`codex` is not on `PATH`.** It lives inside the ChatGPT desktop app bundle at the path above.
- **It bills the ChatGPT Pro subscription, not the API.** `~/.codex/auth.json` shows
  `auth_mode: chatgpt`, `chatgpt_plan_type: pro`, `OPENAI_API_KEY: null`. No key needed. Each
  review costs roughly 100k to 350k tokens of that quota, so **do not re-run a review that already
  exists on disk.**
- **The sandbox flags are load-bearing.** The local config defaults to `danger-full-access`;
  `-s read-only` with `disk-full-read-access` scopes it to what a reviewer needs.
- **Do not hand it `STYLE.md` or `CONTRIBUTING.md`.** This is deliberate. The owner's reasoning:
  *"I don't trust that I've steered you clearly enough to trust both you and ChatGPT to use them,
  I prefer only you use them."* And the practical reason: if the reviewer shares your rules, you
  get the same opinion twice. Its briefing is at `review/BRIEFING.md` and it wrote that itself.

Models available locally: `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`, `gpt-5.4-mini`. Sol on
high reasoning is what finds the real defects. Terra is the cheaper tier that still source-checks.

### Where the reviews live, and why that is fragile

`~/Source/Personal/missing-fleet-manual-private/reviews/2026-08-25/` holds 16 completed reviews
and a README indexing them. **That directory is not a git repository.** It is local files on one
machine. It does not sync, and re-running its contents would cost most of a day's quota.

If you are on a different machine, those files do not exist and you cannot get them back cheaply.
Say so rather than silently re-running reviews.

---

## 5. Hard constraints

These are not preferences.

- **Never read or cite `~/Source/Fleet/fleet-confidential`.** The Fleet checkout has two halves;
  only `fleet-public` is in scope.
- **No commits to any Fleet repository and nothing touching Fleet's AWS.** Findings about Fleet
  get recorded in the manual's own notes. Six Fleet documentation bugs have been found and **none
  filed**. That is the owner's call, not yours.
- **Host identifiers** (serial numbers, UUIDs, host IDs) travel on a private channel and are never
  put in a public repository. This repo is public.
- **`op` CLI** is a service account limited to the vaults "Claude Code" and "Home Network".
- **No placeholder images.** They confuse the image-generation model. IMAGE-TODO / IMAGE-OK
  markers carry a verbatim PALETTE block copied between chapters; keep it byte-identical.

---

## 6. What the last two sessions actually taught

Worth reading before you write, because these are expensive lessons.

**Verification runs downstream of belief formation.** By the time you check a citation, your
inference has already become your belief about what the source says. This is why the independent
reviewer finds things you cannot: it arrives with no prior belief. Running total across the
project: **34 chapters reviewed, 33 with material defects.** Assume your chapter has one.

**Cross-chapter contradiction is the dominant defect class, and the most dangerous.** In the last
session: 8.11 contradicted 8.1 on log ordering and contradicted *itself* three sections later;
8.12 contradicted 1.5 on retention and 2.5 on stream lag and itself on actor names; 8.13
contradicted 8.7 on what a live report proves and 8.11 on a command name. In every case the book
already held the right answer. That is what `claims.py` is for.

**Backtests reward a checker for finding what it was built to find.** The checkers scored 7/12 on
the Part II defects they were built from and **0 of 7** on fresh Part I chapters. They are useful
and they are not a review.

**Not every defect class is checkable.** Extending `check-table-names.py` into prose produced 37
false positives and 0 true positives. It was reverted and the reasoning written into
`CONTRIBUTING.md`. When a rule would fire on correct prose more often than wrong prose, do not
ship it. Tuning until the one known answer appears is fitting the test set.

**The most dangerous defects are the confident, copyable ones.** 8.10 recommended deleting an
Android enterprise as general remediation, which would have destroyed every work profile in an
estate. 8.13's worked example, presented as *the model of a good ticket*, named a table that does
not exist. 8.14 gave a runnable command that deletes data one way with no warning. Prose that
reads as authoritative and is wrong does more damage than prose that is merely thin.

---

## 7. What to do next

In the order I would take them.

1. **Re-verify 8.1 through 8.10 at `fleet-v4.90.1`.** Ten chapters whose stamps currently
   understate them. Cheapest real progress available, and it closes out Part VIII's correctness.
2. **Part VIII structural pass.** The reviewer made the same recommendation for 8.11, 8.12, 8.13
   and 8.14 independently: lead with the incident workflow, move schema and command catalogs
   behind it, stop duplicating 8.5 and 2.5. Deferred four times on purpose, because it is one
   decision about the part's shape and should be taken once, across the part.
3. **Promote Parts I and VIII to `verified`** by writing the missing ledgers and adding
   `reviewed_by`/`reviewed_on`. Do not add the fields without the ledgers.
4. **a.4, the roles and permissions matrix.** Highest-demand remaining appendix, and
   `check-crossrefs.py` still reports 2.3's deferral to it as reaching nothing.
5. **Finish Part III** (3.2 to 3.6), then Parts IV through VII, with review in the loop per
   chapter. This is the bulk of the remaining book.

### Backlog, unchanged

- 12 SCREENSHOT briefs await real console captures. Those are the owner's to take.
- 1.1's lifecycle diagram needs regenerating; em-dashes are baked into the rendered asset.
- Apple Business Manager vs ABM terminology is inconsistent across chapters.
- `STYLE.md` still contains 20 pre-existing em-dashes, in a file that forbids them.

---

## 8. Repository map

```
missing-fleet-manual/            (public, git, deploys from main)
├── manual/                      78 chapter files, 36 written
├── research/section-notes/      citation ledgers, one per chapter
├── review/BRIEFING.md           the reviewer's own briefing, written by it
├── build/                       8 checkers, unwrap.py, claims.py
├── website/                     Docusaurus; root .md files are NOT published
├── STYLE.md                     28 sections, non-negotiable
├── CONTRIBUTING.md              the review gate and checker provenance
├── OUTLINE.md  PLATFORM.md
└── HANDOFF.md                   this file

missing-fleet-manual-private/    (NOT a git repo, local only, does not sync)
├── PROJECT_STATUS.md            dated session log
└── reviews/2026-08-25/          16 completed reviews + README

~/Source/Fleet/fleet-public      at tag fleet-v4.90.1: the source of truth
~/Source/Fleet/fleet-confidential OFF LIMITS
```
