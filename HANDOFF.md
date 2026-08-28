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
**Status artifact:** https://claude.ai/code/artifact/8b5267d3-3e77-4867-8ed9-5a6bdf9119f6
**Fleet defect queue:** `~/Vault/Claude Cowork/Work/General/Fleet bugs to file.md`

### Where Fleet defects go

Researching this manual finds real Fleet bugs, and the standing instruction is that this project
files nothing and commits nothing to any Fleet repo. **Record them in the defect queue above**, which
deliberately sits in the vault outside every git repo: this repo is public, and some findings should
not be published before Fleet can fix them. It is shared with other sessions, so take the next free
number in your class (C code defect, D documentation error, S security-shaped) rather than renumbering.

Note the file is not version controlled. Do not assume you can recover a bad edit.

### Resolved 2026-08-28: sensitive research purged from history

While researching 5.8, disk encryption, the research notes crossed the disclosure line the reviewer
had set for that chapter. A sweep found the same shape across Part V: several working notes
described, in actionable detail, how to reach credentials or authorization gaps that are **unfixed at
this release**. This repository is public.

**Resolved, and verified.** All Part V working notes moved to
`missing-fleet-manual-private/research-sensitive/`, and the affected paths were purged from this
repository's history with `git filter-branch`, followed by dropping the backup ref, clearing
`refs/original`, expiring the reflog and garbage collecting. Verified afterwards: zero scratch files
anywhere in history, zero blobs containing the extraction prose, zero dangling objects holding it,
and the link checker clean.

**No exposure occurred at any point.** The branch was never pushed; it was over a hundred commits
ahead of `origin/main` throughout.

**What stays in the repo:** the chapters, and the citation ledgers, both written to the disclosure
line. `research/section-notes/README.md` records the policy.

**The rule, now general:** research notes inherit the disclosure line of the chapter they support.
They are the easier of the two to forget, because nobody reviews them as prose. When a chapter's
subject is sensitive, keep its working notes out of this repository and cite them from the ledger.

### Standing rule: refresh the status artifact after every step

The project owner asked (2026-08-27) that the status artifact be updated **after every step**,
not once at the end of a session. A step is any unit of work that changes what the table says: a
chapter drafted, a review applied, a part finished, a checker added.

Source file is `build/manual-status.html`. Regenerate it, then republish **to the URL above** by
passing that URL to the publish call. Publishing without it creates a second artifact and breaks
the link the owner already has.

The purpose is that the owner can look at any moment and see where things stand without asking.
Treat a stale artifact as an unfinished step.

---

## 2. Where the work actually stands

**49 chapters written, 26 still outline stubs.** The stubs are 50 to 90 words each: a title, a
frontmatter block, and section headings. Do not mistake the file count for progress.

| Part | Chapters | State |
|---|---|---|
| 0. Introduction | 1 | Written. Stamped `drafting` |
| I. Foundations | 6 | Written, reviewed to the five-round cap, corrected. `drafting` |
| II. Administer and deploy | 12 | Written. Was `verified`; **demoted to `drafting` under the freeze** |
| III. Connect devices | 7 | Written, reviewed to the cap, corrected. `drafting` |
| IV. Know your devices | 7 | **All 7 written 2026-08-27**, each with one review round applied and a ledger. `drafting` |
| V. Manage devices | 9 | **In progress.** 5.1, 5.2, 5.3 drafted 2026-08-27, one review round each, `drafting`. 5.4 to 5.9 still stubs. Structure agreed with the reviewer, at `research/part5-structure.md` |
| VI. Automate Fleet | 5 | **All stubs** |
| VII. Operate Fleet | 6 | **All stubs** |
| VIII. Troubleshooting | 14 | Written, reviewed to the cap, corrected. `drafting` |
| IX. Appendices | 8 | a.6 and a.8 partial. **a.1 to a.5 and a.7 are stubs** |

So: Parts 0, I, II, III, IV and VIII are drafted; Parts V, VI, VII and most appendices are not.

**The verification freeze is in force.** `check-verified.py` carries `FREEZE = True`, and nothing
may carry `verified` until every part is drafted and every chapter has had a review round. Part II
was demoted from `verified` under it. Lifting the freeze is a deliberate act, not a formality.

**No chapter has yet passed a review round without a material finding.** Across every part
reviewed so far, every first round came back NOT READY, and the finding was usually the chapter's
organising claim rather than a detail.

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

### Addendum, agreed 2026-08-28: the loop for drafting the rest of Part V (5.4 to 5.9)

The owner asked for this exact sequence per chapter, tighter than the general loop above on two
points: an explicit outline-agreement step before research, and only **one** review round per
chapter for now (not the five-round cap) — a full extra review pass happens later, at the same
point the whole book gets its final round.

**The asymmetry is deliberate and the owner stated it explicitly (2026-08-28). Steps 1 and 2 run to
consensus: loop back and forth with the reviewer as many times as it takes until you genuinely
agree. Step 4 is a single pass: one review, apply, move on.** Do not spend rounds polishing prose
now; spend them getting the outline and the facts right, because those are what later rounds cannot
cheaply undo. A wrong organising claim survives five prose rounds — that is the record of this
project — whereas a clumsy sentence does not survive one.

1. **Pull the outline stub and check it with the independent reviewer.** Send the chapter's row
   from `research/part5-structure.md` plus its stub file. Ask directly: is this a good base for a
   chapter that takes an administrator to expert level on this subject, and does it capture every
   concept it needs to? Apply whatever changes it recommends to the outline before researching.
   (Part V's spine was already negotiated at the part level on 2026-08-27 — this step re-confirms
   the one chapter's slice of it, not the whole structure again.)
2. **Research the chapter's subject** the normal way: `claims.py` on every mechanism first, then
   verify every claim against `~/Source/Fleet/fleet-public` at tag `fleet-v4.90.1` (commit
   `dd0200f062`), never `main`, never the published docs as a primary source. Write the findings as
   normal notes, then send them to the reviewer and ask if the research looks correct and complete.
   Iterate — more research, back to the reviewer — until you agree. Do this **before** drafting
   prose, not after.
3. **Draft the chapter** to `STYLE.md`, citation ledger and all. Include HTML-comment diagram,
   artwork, or screenshot markers wherever a picture would materially help, in the same
   `IMAGE-TODO` / `IMAGE-REDO`-with-`PROMPT` shape used in Part II — Part II is the model to match
   for how many markers and what they cover. Screenshots are the owner's to shoot; diagrams and
   artwork prompts are the reviewer's to write (next step).
4. **One review-and-edit round.** Send it to the reviewer once, apply what's accepted, record
   rejections and why in the ledger, re-run `claims.py` on changed terms, run the checker list.
   Do not chase a clean verdict or run further rounds this pass — that happens later, part-wide.
5. **Kick off the image-prompt job in the background and move on** — do not wait on it. This is
   `scratchpad/imageprompts.sh`'s shape: the reviewer reads the finished chapter and writes/refines
   the `PROMPT:` block for each `IMAGE-TODO`/`IMAGE-REDO` marker, verified against the tag, in the
   same style-rule voice as existing accepted prompts. It does **not** render pixels — the owner
   generates the actual images himself afterward, separately and on his own schedule. Launch with
   `nohup ... &`, note the job, then start the next chapter without waiting for it to finish.
6. **Move to the next stub chapter and repeat from step 1.**

**Refresh the status artifact after every step** (see the standing rule above) — after the outline
is agreed, after research is agreed, after the draft lands, after the review is applied, and after
each chapter closes out. Republish to the same URL recorded there; do not create a second one.

**Only a review OF A DRAFT counts as a round.** Set by the owner on 2026-08-28, after the status page
counted 5.4's outline and research reviews toward the five-round cap. Those are real reviews and
their findings are applied, but they read a plan rather than prose, so counting them would retire a
chapter's review budget before it had been written. `build/status-artifact.py` enforces this with
`NON_DRAFT_REVIEW`, which excludes any review file whose name contains `outline`, `research`,
`imageprompt` or `structure` from both the count and the displayed verdict. **Keep naming review
outputs accordingly** — a draft review of 5.5 should be `5.5-sol.out` or similar, and anything that
is not a draft review should say so in its filename.

---

## 4. The independent reviewer

The project owner's arrangement, in his words: *"I'd keep you as the project lead, CGPT as the
reviewer and second opinion and myself as the final arbiter."*

Reviews run through ChatGPT's Codex CLI, invoked directly, with no human relaying anything.

### The verification freeze

**Set by the owner on 2026-08-27:**

> Let's demote anything listed as "verified" to drafting until we've completed drafting all the
> parts and have done at least one round of review on every chapter.

So **nothing carries `verified` right now**, and `build/check-verified.py` enforces that with a
`FREEZE` flag rather than leaving it to discipline. Twelve chapters were demoted on the day the
freeze was set: eight because a neighbour's review had corrected them hours after their own verdict,
and four because the stamp no longer meant anything once the other eight had gone.

The reasoning is worth keeping, because it is the clearest lesson of the whole session. **A stamp
that a neighbour can invalidate is not measuring what it claims to.** Writing a Part III chapter
found real errors in Part I. Reviewing Part I found real errors in Part II. Reviewing Part I again
found errors in Part VIII. While whole parts are still outlines, every chapter has neighbours that
do not exist yet, and a chapter cannot be finished before the chapters that contradict it have been
written.

Lift the freeze by deleting the flag in `check-verified.py`, once every part is drafted and every
chapter has had at least one review round. Not before, and not chapter by chapter.

### How many rounds a chapter gets

**Set by the owner on 2026-08-27, after Part I failed two full rounds and Part VIII four.**

> Keep running rounds until a chapter comes back clean or until it hits 5 rounds, then cap it for
> now and keep it in `drafting`. We'll run another full review again at the end of completing the
> initial draft of every chapter in a part.

So the rule is: **clean verdict, or five rounds, whichever comes first.** A capped chapter stays at
`drafting` and is not a failure; it is a chapter whose remaining defects cost more to find than the
next unwritten chapter costs to draft. Record the cap in the chapter's ledger with the round count
and the last verdict, so a later reader knows the difference between *not reviewed* and *reviewed
five times and still imperfect*.

**"Clean" means READY, or READY WITH MINOR CHANGES where the minors are applied and nothing else
has changed since.** That second clause is what has blocked every stamp so far: chapters keep
taking corrections from a neighbour's review after their own verdict.

The point of the cap is that this loop does not converge to zero, and the evidence is now
substantial. Round three of 1.2 still produced eight items. What changed was their **character**:
rounds one and two found fabricated claims, round three found mostly *propagation* failures, the
same claim surviving in a table or a neighbouring chapter after the prose was fixed. That class is
cheaper to attack with `claims.py` and a grep than with another review, which is a large part of
why five is a sensible ceiling rather than an arbitrary one.

The full-review-per-part at the end of drafting is the real safety net. A part reviewed once its
chapters all exist gets something no per-chapter round can give: reviewers who can see every
cross-reference land somewhere real.

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
project: **56 chapters reviewed, 55 with material defects.** Part I contributed six for six on
2026-08-27, on the chapters the rest of the book inherits from. Assume your chapter has one.

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

**A new chapter's organising claim is the most likely thing in it to be wrong, and writing one is the
best test the neighbours ever get.** Four of Part III's five first reviews came back NOT READY on the
sentence the chapter is built around, not on a detail:

| Chapter | Said | Actually |
|---|---|---|
| 3.2 | Fleet delivers the agent on ADE; manual enrollments need a package by hand | It delivers on **both**. Only ADE has an opt-out |
| 3.3 | Windows MDM brings disk-encryption enforcement | It is set in the **Orbit** config response; MDM is a gate, and it never appears in the MDM queue |
| 3.4 | Linux has one channel, and no lock or wipe | It has no *MDM* channel and three others, and Premium **can** lock and wipe Linux, as scripts |
| 3.5 | ADE's licensing on Free is undocumented | ADE is **Premium**, because Apple Business tokens are, which 2.7 had said all along |

Every one is the natural inference from a true adjacent fact, which is why it survived drafting: no MDM
therefore no lock; ADE installs the agent therefore only ADE does; MDM does disk encryption elsewhere
therefore it does here.

3.6 and 3.7 completed the set at six for six. 3.6 said Android has no agent and everything arrives
unsolicited; Fleet ships a narrow force-installed app that reports certificate results, and polls Google
hourly. **1.2, 2.8 and 8.10 all had that right.** 3.7 said Orbit checks for updates at startup; it starts
a timer and waits, so a channel change reaches the host in under a minute and changes the version fifteen
to twenty-five minutes later.

**And each correction rippled.** Writing and reviewing these chapters produced corrections in **thirteen
places in already-reviewed chapters**: 1.2 four separate times, plus 2.7, 2.8, 3.1, 3.2, 8.1, 8.2, 8.4,
8.8, and 8.10 twice. A reviewed chapter is not a verified one, and the cheapest way to find what a
reviewed chapter got wrong turns out to be writing its neighbour.

**So, before drafting a chapter: write its organising sentence down and check that one sentence against
Fleet's source directly.** Not against a neighbouring chapter, not against the inference that makes it
plausible. Doing exactly that to 3.4 and 3.6 before their reviews found a wrong claim in each, and in
3.4's case the same wrong claim sitting in 1.2.

**Correcting a chapter is the most reliable way to introduce the next defect in it.** This is the
strongest evidence the project has produced, and it is not the same thing as half-application. Across
Part VIII's four review rounds and Part III's two, **the dominant remaining finding at every stage
after the first was introduced by the previous round's correction.** Not left behind: written.

The shape is consistent and recognisable:

| The correction | What it became | Where |
|---|---|---|
| A wrong universal | The opposite universal | 3.2 "Fleet installs on every enrollment"; 3.4 "settled when the image is built" |
| A wrong universal | A frequency claim | 8.4 "usually permissions"; 3.6 "almost everything Fleet knows" |
| A missing caveat | A new absolute nearby | 8.8's DDM bypass added above a sentence denying it |
| A new section | A sentence contradicting the section it introduces | 8.13, three rounds running |

**Why it happens is worth understanding, because it predicts where to look.** A correction is written
with the finding in hand and the rest of the chapter out of mind. The new sentence is checked against
the source and not against its neighbours, and the reviewer's finding gives a false sense that this
passage is now the settled one. A hedge feels safer than an absolute, so "X is the cause" becomes "X
is usually the cause", which is a *new* claim about frequency that the source almost never supports.

**A reviewer's proposed wording is a claim, not a citation, and adopting it unchecked is its own
defect class.** Added 2026-08-27 after 1.1's third round, where three of eight findings were the
reviewer retracting round-two claims that had gone into the chapter verbatim on its authority: that
the report row cap "freezes" storage, that Apple gates profile variables individually while Windows
gates them wholesale, and that FileVault escrow is Orbit's work. All three were wrong, and all three
would have been caught by opening the file the review cited. The same happened twice in 1.5. The
reviewer retracting its own findings is the system working; paying for a whole extra round to
discover it is not. **Treat a suggested replacement exactly like your own draft sentence: source it
before it lands.**

**The countermeasure is to re-read the whole chapter after applying, as if reviewing it fresh, rather
than reading the diff.** The diff is exactly the view that hides this. And before writing a
replacement sentence, ask what it now asserts that the old one did not: a proportion, a ranking, an
exhaustive list, a direction. If the source does not establish that new thing, say what the reading
is *consistent with* instead.

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

**Part I's foundations chapters failed in a shape the later parts do not.** Both 1.1 and 1.2 came
back NOT READY on 2026-08-27 with seven and ten factual defects respectively, and almost none of
them were details. In 1.2, nearly every defect was **a true statement about a fully enrolled Mac
promoted to a universal**: five channels, query work belongs to osquery, online means queries work,
hardware migration recovers itself, if Orbit is down osquery is down. Each holds on the host the
author was picturing and fails on Linux, on mobile, on ChromeOS, or on Windows. In 1.1 the defects
were **tidy framings that survived because they sounded quotable**: the reading half and the writing
half, expected state over there and actual state over here, a missing capability means the platform
offers no mechanism.

Two things follow for anyone writing foundations material. A sentence that generalises is making a
claim about every platform in the book, and it needs checking against the *worst* case rather than
the typical one; the applicability matrix now in 1.2 exists because no amount of hedging replaces
enumerating. And a framing that sounds like a principle should be suspected precisely because it
sounds like one, since a reader will carry it into chapters that were never checked against it.

**Licence claims are the least reliable claim class in the project and no checker catches them.**
**Seven wrong on 2026-08-27 alone**, in both directions and in every part of the book: 3.5 said ADE's licensing was undocumented when ADE is
Premium, then said owner mapping was free when end-user authentication is Premium; 2.8 gated
company-owned Android when it is not gated; 1.2's rollout table listed lock, wipe and LUKS escrow
with no gate at all when every lock is Premium, every wipe except company-owned Android is Premium,
and disk encryption is Premium; and 1.1 presented a platform table that read as an edition promise.
1.3 described named fleets, fleet-scoped labels and label targeting as generally available when all
are gated; 1.4 split one licence claim into two gates and left two more out, including the one that
refuses an API-only user *any* fleet role regardless of which role it is; 8.9 stated the BitLocker
reserved-LocURI exception without saying that enabling custom disk encryption is Premium; 8.11 told
readers to scope a profile or installer to a one-host label, in a chapter whose own throwaway recipe
ships a blank licence key; and 1.6 presented a fallback table for three artifact types that Free
cannot create at all.

**One caveat on that, added after 1.1's second review corrected me on it.** The validators are
mostly explicit: they return a licence error rather than failing obscurely, so a licence gate is
usually cheap to confirm by trying the operation. What makes these claims unreliable is not that
Fleet hides them, it is that the manual asserts them from memory of how a product this shape
*usually* gates things instead of reading the validation. **Check every licence claim against its own validation in the source. There is no
single rule to infer from: Fleet gates feature by feature, and scope by scope within a feature.**
Two of the seven were *omissions* rather than assertions, which is the harder kind: there is no
sentence to check, so the only way to find them is to ask, of every capability a passage tells a
reader to use, which licence it needs.

**The strongest single instance of the correction-introduces-the-next-defect pattern, for the
record.** On 2026-08-27 the author corrected 1.2 to say lock and wipe are MDM commands on macOS and
Windows and scripts on Linux, generalising correctly from a Linux finding to a two-way split that
does not exist: **Windows lock is a script**, gated on scripts being enabled, and only Windows wipe
is an MDM command. The wrong version went into the chapter *and into the ledger row justifying it*,
where it would have outlived the prose. Separately, correcting 8.4's hardware-migration finding into
8.2 produced a fresh false claim, that `hardware-uuid.txt` is written on Windows and Linux and merely
not acted on, within an hour of reading the `darwin` branch that disproves it. **A correction is a
new claim. It inherits none of the original's checking, and it needs all of it.**

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
3. **Promote Part VIII to `verified`, or decide deliberately not to yet.** This is a judgement
   call and it is the owner's, so here are the facts rather than a recommendation dressed as one.

   **Part VIII has had four review rounds.** A full re-review at the tagged text (11 of 14 NOT
   READY), a confirming round, a second over the six still failing, and a third over the six
   corrected after that. **Every finding from every round is applied.** The loop demonstrably
   terminates: 8.9 carried more findings than any chapter in the part, was NOT READY three rounds
   running, and came back on the fourth with everything resolved and one leftover positional word.

   **What blocks a clean stamp is that no chapter's exact current text has been reviewed**, and
   that is true of all fourteen rather than of a stubborn few. The cross-cutting sweeps done on
   2026-08-27, pinning repository links, quoting shell placeholders, linking the glossary, and
   clearing frequency claims, touched almost every chapter after its verdict. So did the
   corrections that Part III's reviews forced back into Part VIII.

   The chapters differ in **what kind** of change landed after their last verdict, which is what
   the decision should turn on:

   | State | Chapters | What changed since the verdict |
   |---|---|---|
   | Verdict was clean and nothing has changed since | **8.5** | Nothing. Its confirming minors were applied in the same commit |
   | Verdict was READY WITH MINOR, those exact minors applied, nothing else | **8.9, 8.13** | One word and one sentence respectively, both named in the verdict as the acceptance condition |
   | Clean verdict, then editorial-only sweeps | **8.3, 8.7, 8.12, 8.14** | Link pinning, glossary links, frequency-claim rewording |
   | Clean verdict, then a **factual** correction from elsewhere | **8.1, 8.2, 8.6, 8.10** | Part III's reviews found real errors in these: the half-enrolled framing, `secret.txt`, `Failed profile`, and two Android diagnostics |
   | Last verdict was NOT READY, findings applied since | **8.4, 8.8, 8.11** | Substantive. These are the ones a reviewer has genuinely not seen |

   **The defensible reading:** 8.5, 8.9 and 8.13 meet the standard now. 8.3, 8.7, 8.12 and 8.14
   meet it unless you hold that any edit invalidates a verdict, which the project has not held
   before. 8.1, 8.2, 8.6 and 8.10 took real corrections and should be re-read at minimum. 8.4, 8.8
   and 8.11 need a fourth round.

   ~~**The cheap option** is a fourth round over the seven in the bottom two rows.~~ **Done
   2026-08-27, over six of them** (8.2, 8.4, 8.8, 8.9, 8.11, 8.13), at `confirm4/`. Three came back
   READY WITH MINOR CHANGES and three NOT READY, and **all six were then corrected**, so Part VIII
   is back in the same position one rung higher: every finding applied, no chapter reviewed at its
   current text. A fifth round over those six is what would settle it.

   What the fourth round found is the reason it was worth running. **Round three's own corrections
   were the largest source of new defects**, and the reviewer said so in as many words twice: "the
   fourth review's one-hour-retention conclusion was wrong", and "the fourth review was wrong to
   call the SCEP wording fully correct". Concretely: 8.8's new `skipNotNow` passage confused one
   response cycle with persistent queue state; 8.9's queue retention became "one hour" when the
   cleanup makes a row *eligible* at one hour on an hourly schedule, so nearly two; 8.9's
   certificate-lifetime fix over-corrected into "enrollment age is useless as a proxy" while the
   chapter relied on enrollment age three paragraphs later; and three frequency claims in 8.8 had
   replaced universals during earlier rounds.

   **8.11's Compose blocker is closed.** The recipe had never been executed; it has now been run end
   to end and torn down. Docker creates `certs/fleet.crt` and `certs/fleet.key` as **empty
   directories** when they are absent, the stack comes up perfectly healthy with TLS off so nothing
   warns you, and switching TLS on later gives `read /fleet/fleet.crt: is a directory` in a restart
   loop. Also measured: healthy in about a minute rather than the fifteen the chapter guessed, the
   Compose file pins no Fleet version (`image: fleetdm/fleet`, so `latest`, which happened to be
   4.90.1 that day), and **a Free instance starts 21 of the 34 cron schedules**, which is a useful
   diagnostic and corroborates the Premium gating from the running product.

   Full record at `reviews/2026-08-27/README.md`, `confirm/`, `confirm2/`, `confirm3/` and
   `confirm4/`.

   **Part I was further from `verified` than its bookkeeping suggested, and a round on 2026-08-27
   proved it: all six chapters came back NOT READY, with six to ten factual defects each.** That is
   a worse result than Part VIII's first full re-review, on chapters that everything else in the
   book inherits from. Every finding is applied and a second round is running at `part1b/`.

   The two failure shapes were distinct and both worth recognising elsewhere:

   - **1.2, 1.3, 1.5 and 1.6 promoted a true statement about one configuration into a universal.**
     Five channels (a fully enrolled Mac or Windows machine only); query work belongs to osquery
     (fleetd hosts only); one targeting model (four items, no two agreeing); a fleet duplicates
     everything (profiles and software only, while policies, reports and labels inherit from
     global); activities record what Fleet did (device-originated rows are routine and carry no
     actor); losing Redis costs a retry (pending failing-policy notifications are not
     reconstructed).
   - **1.1 and 1.4 stated tidy framings that survived because they sounded quotable.** The reading
     half and the writing half; the asset system holds expected state and Fleet holds actual;
     a missing capability means the platform offers no mechanism; the IdP is the directory so Fleet
     keeps no accounts; two questions decide authorization.

   The most useful single addition to come out of it is **the four-way capability check in 1.1**:
   when something is missing for a platform, the reason is the OS, or Fleet's implementation at this
   release, or your edition, or an unmet prerequisite, and earlier drafts assumed the first by
   default. That framing is worth applying anywhere the manual says a platform cannot do something.

   **The second round returned NOT READY on all six again**, at `part1b/`, and this is the single
   most useful number the project has produced. Round one's findings were almost all confirmed
   resolved. What failed the chapters a second time was **the corrections themselves**: seven new
   defects in 1.2, seven in 1.3, eight in 1.5, eight in 1.6, six in 1.4, seven in 1.1. The reviewer
   named the shapes without being told them, and they are the four already tabulated above.

   Some of the worst were operationally dangerous rather than merely wrong. 1.2 gained a table row
   telling readers to pin osquery by naming only the `osqueryd` key, which silently moves Orbit and
   Desktop to `stable`. 1.3 said an exclusion withholds an item from everybody until hosts report,
   when the guard is evaluated **per host**, so a rollout stalls raggedly rather than uniformly, and
   said software is uninstalled when a host leaves scope, which it is not. 1.6 conflated Redis being
   unreachable with Redis losing what it held, across three passages.

   **Three of Part I's images were found asserting claims the prose had withdrawn**, which nothing
   checked for. `build/check-image-regeneration.py` now exists, and an `IMAGE-REGENERATE` marker
   blocks a `verified` stamp. An accepted image is accepted against the prose as it stood.

   **Eight Part II chapters were demoted from `verified` to `drafting`**, having taken factual
   corrections today from the Part I and Part III work. The clearest case: 2.2, whose whole subject
   is identity, stated that SCIM deprovisioning does not require Premium. It does, and Fleet only
   registers the SCIM routes when the server starts with a Premium licence.

   Full record at `reviews/2026-08-27/part1/` and `part1b/`. Tasks 21 and 25, both complete. A third
   round is the open question, and the honest expectation from two data points is that it will find
   fewer defects but not none.

4. **Part III has had two review rounds and every finding applied.** Five first reviews, five
   confirming reviews, and a first review of 3.7, which had never had one. All twelve verdicts and
   their findings are at `reviews/2026-08-27/part3/` and `part3-confirm/`.

   It is in exactly the position Part VIII is: **every chapter was corrected after its last
   verdict**, so nothing is stampable without one more round. 3.3 is the only chapter whose
   confirming verdict was READY WITH MINOR CHANGES.

   **What the second round found is the reason to read those files rather than the verdicts.**
   Almost nothing was left behind from the first round; almost everything was written during the
   corrections. §6 above has the shapes.

5. **a.4, the roles and permissions matrix.** Highest-demand remaining appendix, and
   `check-crossrefs.py` still reports 2.3's deferral to it as reaching nothing.
6. **Part V, chapters 5.4 through 5.9**, using the addendum loop in §3 above (agreed 2026-08-28).
   5.1 to 5.3 are drafted with one review round each. Then **Parts VI and VII**, still unstarted:
   11 chapters, all stubs.

### Backlog

- **Licence claims are the least reliable class of claim in this manual, and there is no check for
  them.** Part III's confirming reviews found one chapter asserting a capability was Premium and
  then, forty lines later, asserting a related one was free; both were wrong, in opposite
  directions. Sweeping the rest found two more: 8.6's schedule table omitted Premium on
  `send_recovery_lock_commands` and `google_workspace_sync`, and **2.8, a `verified` chapter, called
  company-owned Android enrollment Premium when nothing in Fleet's Android module checks a licence
  at all.**

  Each licence gate lives in its own validation, so none is checkable from any other, and a wrong
  one is expensive in both directions: it either tells a Free deployment it cannot do something it
  can, or has it plan around a capability it does not have. **Check every new licence claim against
  the specific validation that enforces it**, and treat "X is Premium" in an existing chapter as
  unverified until you have found that validation. A checker is not obviously possible here, which
  is why this is a habit rather than a script.


- **`8.11:47` publishes a timeout claim that traces back to a stale Fleet code comment.** Found
  2026-08-28 while researching 5.4, before drafting rather than after, which is the only reason it
  did not get reinforced in a second chapter. The table row says the 1-hour software timeout covers
  "every step … and an explicit uninstall", and adds that the `script_execution_timeout` agent option
  "does not apply to this path". The explicit uninstall appears to be the one step it does **not**
  cover, which would make the agent-option sentence wrong in the same row.

  The chain, at the tag: an uninstall queues as `activity_type = 'software_uninstall'` and activates
  into `host_script_results` with `is_internal = 1`; `listUpcomingHostScriptExecutions`
  (`server/datastore/mysql/scripts.go:322,347,352`) selects
  `activity_type IN ('script','software_uninstall')`, commented "software_uninstalls are implicitly
  internal"; that pipeline's runner times out on `r.ScriptExecutionTimeout`
  (`orbit/pkg/scripts/scripts.go:121`), set from `MaxHostExecutionTime`, 5 minutes, at
  `orbit/pkg/update/notifications.go:425-428`. `orbit/pkg/installer/installer.go` is the sole consumer
  of the 1-hour constant and mentions uninstall only inside the post-install rollback block at
  532-541. **Fleet's own comment at `pkg/scripts/scripts.go:17-23` asserts the opposite**, which is
  where both Fleet's docs and this manual appear to have taken it from.

  Sent to the independent reviewer for a ruling on 2026-08-28 (`reviews/2026-08-28/part5/`), because
  the reviewer asserted the same stale claim from the same comment when reviewing 5.4's outline.
  **Fix 8.11 once that ruling lands; do not fix it from this note alone.** If confirmed it is the
  eleventh Fleet documentation error and the first found in a code comment rather than generated
  reference output, which extends the standing rule: read the executed path, not the comment above it.

- ~~13 frequency claims rank a cause without a source.~~ **Cleared 2026-08-27** in one pass across
  nine chapters, and `build/check-frequency-claims.py` now reports none. Keep it that way: the
  checker is deliberately narrow, so anything it flags is a real candidate. The fix is almost never
  a weaker hedge. It is to say what the reading is *consistent with*, or to name the candidates
  without ordering them, or to say why one is worth testing first on grounds of cost rather than
  frequency, which is a claim you can actually support.
- **45 references point into chapters that are still outline stubs**, and `check-links.py` passes
  every one because the file exists. `build/check-outline-deferrals.py` lists them and now
  separates the two failures, which are not equally serious:

  - ~~10 are promises~~ **All closed 2026-08-27.** They named content that does not exist: "the
    full action-by-action breakdown for all six roles at both scopes", "every setting, what it
    defaults to, and what wins when two levels disagree". Each now says the target is not written
    yet and names what answers the question today, which for a.4 is 2.3 itself and for a.3 is
    Fleet's configuration reference read with 8.14's caveat about its defaults. The checker
    suppresses a promise that disclaims itself, so it reports zero and will report any new one.
  - **19 still sit in chapters stamped `verified`**, now as bare pointers rather than promises.
    Tolerable, and worth watching: a verified chapter that points into a stub is one edit away
    from promising again.

  Also on 2026-08-27, **a.6 moved from `outline` to `drafting`**, because its terminology section
  is written and linked from seventeen places in Part VIII. Its two genuinely empty sections,
  Feature availability and Version boundaries, now say so in the file rather than presenting as
  headings with content on the way.

  **a.3 and a.4 are the most-referenced by a wide margin**, which is the answer to which appendix
  to write next.
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
├── build/                       14 checkers, unwrap.py, claims.py
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
