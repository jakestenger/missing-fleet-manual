# Handoff: The Missing Fleet Manual

Written 2026-08-26, updated 2026-08-27.

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

**41 chapters written, 33 still outline stubs.** The stubs are 50 to 90 words each: a title, a
frontmatter block, and a sentence of intent. Do not mistake the file count for progress.

| Part | Chapters | State |
|---|---|---|
| 0. Introduction | 1 | Written. Stamped `drafting` |
| I. Foundations | 6 | Written, reviewed, corrected. Stamped `drafting` |
| II. Administer and deploy | 12 | **Complete. All 12 `verified`** |
| III. Connect devices | 7 | **All 7 written.** 3.1 and 3.7 reviewed; 3.2 to 3.6 written 2026-08-27 with ledgers and **no independent review yet**. All `drafting` |
| IV. Know your devices | 7 | **All stubs** |
| V. Manage devices | 8 | **All stubs** |
| VI. Automate Fleet | 5 | **All stubs** |
| VII. Operate Fleet | 6 | **All stubs** |
| VIII. Troubleshooting | 14 | Written, tag-verified at 4.90.1, restructured, and re-reviewed twice. **Every chapter now has its findings applied at current text.** Stamped `drafting` |
| IX. Appendices | 8 | a.6's terminology section written 2026-08-27; a.8 partial. **a.1 to a.5 and a.7 are stubs** |

So: Part II is finished, Parts I, III and VIII are written but not stamped, and Parts IV to VII
have not been started.

### The status ladder

`outline` → `drafting` → `verified`. `check-verified.py` gates the top rung and will fail CI if a
chapter claims `verified` without all of:

- `verified_against`, `verified_on`, `verified_source`
- `reviewed_by`, `reviewed_on`
- a notes file at `research/section-notes/<section>-notes.md`

**Part I is stuck on the bookkeeping, not the substance.** It has been reviewed and corrected; it
lacks `reviewed_by`/`reviewed_on`. Promoting it is a real task with a real gate, not a formality:
adding the fields without writing the ledgers would be exactly the overclaim the gate exists to
stop.

**Part VIII has all fourteen ledgers and both review fields, has now been through three review
rounds, and is still deliberately `drafting`.** The rounds were: a full re-review at the tagged
text (eleven of fourteen NOT READY), a confirming round asking whether the corrections landed,
and a second confirming round over the six that were still NOT READY. **Every chapter's findings
are applied at the current text.**

What remains before it can be stamped is narrow but real: **8.2, 8.4, 8.8, 8.9, 8.11 and 8.13 have
corrections applied since their last verdict, so their last verdict again describes older text.**
Three chapters (8.1, 8.5, 8.12) have a clean confirming verdict at text that has not changed since.
Stamping the rest now would repeat the mistake `check-verified.py` exists to prevent. See section 7
and `reviews/2026-08-27/README.md`.

**The dominant defect across all three rounds was not wrong facts, it was half-applied
corrections.** Every finding was applied correctly at the passage it cited, and the same claim was
left standing elsewhere in the chapter — which leaves the chapter arguing with itself, a worse
state than the original error. If you take one working rule from this file, take this one: after
applying a finding, grep the chapter for every phrasing of the claim you just changed, then run
`claims.py` on it for the neighbours.

### Part VIII's version debt is closed

All fourteen chapters carry `verified_against: Fleet 4.90.1` and `verified_source: git tag
fleet-v4.90.1`. 8.1 through 8.10 were swept on 2026-08-26; nine of the ten had material defects,
and three of those existed only because the check ran at 4.90.1 rather than at the `main` checkout
the chapters were first verified against. A further round on 2026-08-27 found more, including seven
errors in prose written during that sweep. Details in `PROJECT_STATUS.md`.

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
bugs found so far, including three separate settings where the generated reference disagrees with
what the server registers: a default documented as `1h` that registers as `2m`, an Android batch
size documented as 1,000 that registers as 100, and `app_enable_report_stats`, which the server
does not bind at all. **Read configuration defaults out of `config.go`, never out of the
reference.**

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

**7. Apply the review, then verify the reviewer, then run `claims.py` again.** The second `claims.py`
pass is not optional and it is new: on 2026-08-27, correcting three chapters generated three fresh
cross-chapter contradictions, because a fix that is right for one chapter contradicts a neighbour
that still says the old thing. `claims.py` found all three in seconds. Run it on every term you
changed, not only on the terms you were about to write about.

The reviewer is right often but not always.
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
python3 build/check-column-names.py
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
project: **44 chapters reviewed, 43 with material defects.** Assume your chapter has one.

**A review round is not a formality either, and "applied" is a claim worth checking.** The
2026-08-25 index said 8.1 through 8.10 were processed and applied. Spot-checking that before
spending quota found it was not: a corrected string had never made it into 8.5. Check the
instance, not the index.

**Re-verifying at a new tag is not bookkeeping.** The 2026-08-26 sweep of ten already-reviewed,
already-corrected chapters found defects in nine, and three of those were only visible at the new
tag: a bug fixed in the patch release had been live and undocumented when the chapter was written,
so the chapter documented a world that no longer existed and gave the wrong cause for a symptom
that still occurs. A stamp that says 4.90.0 on a chapter checked against `main` is not a small
inaccuracy; it is a claim about which release's behaviour is described.

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

**Half-applied corrections are the project's signature defect, across four sessions now.** Not
wrong facts: every finding was applied correctly at the passage it cited. What was left behind was
the same claim in a table two sections up, in a summary paragraph, in a start-here row. That is a
worse state than the original error, because the chapter now argues with itself and the reader
cannot tell which half to believe. Concrete instances from 2026-08-27 alone: an osqueryd path that
exists on no platform, left in 8.2's inventory table after the command below it was fixed; 8.4's
Orbit-root shape still called proof in the summary after the table said it was evidence; 8.8's DDM
absolute standing two lines above the bypass that contradicts it; and 8.9 with three at once.

The countermeasure is mechanical and cheap. **After applying a finding, grep the chapter for every
phrasing of the claim you changed — not the sentence, the claim — and then run `claims.py` on it
for the neighbours.** The second half matters as much as the first: correcting `secret.txt` in one
chapter while another still says it exists on Linux is the same defect at a larger scale.

**The most dangerous defects are the confident, copyable ones.** 8.10 recommended deleting an
Android enterprise as general remediation, which would have destroyed every work profile in an
estate. 8.13's worked example, presented as *the model of a good ticket*, named a table that does
not exist. 8.14 gave a runnable command that deletes data one way with no warning. Prose that
reads as authoritative and is wrong does more damage than prose that is merely thin.

---

## 7. What to do next

In the order I would take them. Item 1 was done on 2026-08-26 and is left here with its outcome,
because what it found changes how to weigh the rest.

1. ~~**Re-verify 8.1 through 8.10 at `fleet-v4.90.1`.**~~ **Done 2026-08-26.** Nine of ten had
   material defects. Three were version drift invisible at the old ref, including a 4.90.0 Apple
   reconciler bug that silently stopped considering a fixed set of hosts. Ten ledgers written, one
   new checker, one `unwrap.py` bug that had eaten a code block and passed its own safety check.
2. ~~**Part VIII structural pass.**~~ **Done 2026-08-27, additively.** Fourteen independent
   reviews made the same recommendation, so the decision was taken once across the part: each
   chapter that needed one got a short `8.x.0 Start here` routing a symptom to the section that
   answers it. No existing section moved, so no anchor broke. Both contradictions noted here are
   also closed: 8.9 and 8.6 now agree on `cleanup_windows_mdm_command_queue`.
3. **Promote Parts I and VIII to `verified`.** Part VIII has now had three rounds: a full
   re-review at the tagged text (eleven of fourteen NOT READY), a confirming round, and a second
   confirming round over the six still NOT READY. **All fourteen have their findings applied at
   the current text.**

   The loop demonstrably terminates. Three chapters reached a clean confirming verdict at text
   that has not changed since (8.12 `READY`, 8.1 and 8.5 `READY WITH MINOR CHANGES`, applied), and
   8.2 went NOT READY → READY WITH MINOR CHANGES on its second confirm, with those minors applied.

   **The gate is the six chapters corrected since their last verdict: 8.2, 8.4, 8.8, 8.9, 8.11,
   8.13.** One more confirming round over those six, at roughly 190k tokens each, is what stands
   between here and a defensible stamp. Everything else is done.
   Full record at `reviews/2026-08-27/README.md` and `reviews/2026-08-27/confirm2/`. Part I still
   needs its `reviewed_by`/`reviewed_on`, and 1.2 carries a correction recorded only in 8.1's
   ledger.
4. **Finish reviewing Part III.** 3.2 and 3.3 have been reviewed and corrected; **3.4, 3.5 and
   3.6 have not been reviewed at all.** Reviews run at `reviews/2026-08-27/part3/`.

   Both completed reviews came back NOT READY **on the chapter's organising claim**, not on
   details, and both corrections rippled into chapters that were already reviewed:

   - 3.2 said Fleet delivers the agent on ADE and not on manual macOS enrollment. It delivers on
     both; only ADE has an opt-out. That made the half-enrolled state look ADE-specific in 8.1,
     8.4 and 8.8 as well.
   - 3.3 said Windows MDM brings BitLocker enforcement. Enforcement is set in the **Orbit**
     configuration response with MDM enrollment as a gate, so it never appears in the MDM command
     queue, and 1.2 had it right all along.

   **The lesson for the remaining three is specific and worth acting on before the reviews land:**
   take each chapter's organising sentence and check it against Fleet's source directly, not
   against what a neighbouring chapter says. Doing exactly that to 3.4 before its review found its
   escrow prerequisites wrong in both directions, and found the same error sitting in 1.2, a
   chapter already reviewed once.

   3.1 and 3.7 were reviewed earlier and are `drafting` on the same bookkeeping gap as Part I.
5. **a.4, the roles and permissions matrix.** Highest-demand remaining appendix, and
   `check-crossrefs.py` still reports 2.3's deferral to it as reaching nothing.
6. **Parts IV through VII**, with review in the loop per chapter. This is the bulk of the
   remaining book: 26 chapters, none started.

### Backlog

- **45 references point into chapters that are still outline stubs**, and `check-links.py` passes
  every one of them because the file exists. "Exact flags are in a.7" reads as a promise and
  delivers a heading list. `build/check-outline-deferrals.py` lists them; it is advisory rather
  than a gate, because a forward reference to a planned chapter is legitimate and the fix is to
  say so rather than to delete the pointer. Four a.7 deferrals were fixed on 2026-08-27 by
  pointing at `fleetctl package --help` instead; the other 41 are outstanding. **a.4 and a.3 are
  the most-referenced**, which is a signal about which appendix to write next.
- 12 SCREENSHOT briefs await real console captures. Those are the owner's to take.
- 1.1's lifecycle diagram needs regenerating; em-dashes are baked into the rendered asset.
- Apple Business Manager vs ABM terminology is inconsistent across chapters.
- `STYLE.md` still contains 20 pre-existing em-dashes, in a file that forbids them.
- **`further_reading` reaches no reader.** 35 chapters carry it, roughly 70 URLs, and the site has
  no code referencing the field. §21 permits it on the understanding that "the site can render
  them separately", which is not true today, so every one of those links fails the airplane test.
  A website change rather than a content one, and the cheapest reader-facing win on this list.

---

## 8. Repository map

```
missing-fleet-manual/            (public, git, deploys from main)
├── manual/                      78 chapter files, 41 written
├── research/section-notes/      citation ledgers, one per chapter
├── review/BRIEFING.md           the reviewer's own briefing, written by it
├── build/                       10 checkers, unwrap.py, claims.py
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
