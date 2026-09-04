# Contributing

The manual lives in `manual/`, one folder per part, one markdown file per section. Edit the
markdown, open a pull request, and the build check runs automatically. On merge to `main`
the site rebuilds and deploys.

## Read this first

`STYLE.md` is short and it carries the rules that do the real work. The four that come up
most:

- **§1, the airplane test.** The book is self-contained. A reader with the PDF and no
  network should be able to operate Fleet. Overlapping with fleetdm.com/docs is not a defect.
- **§12, two registers.** Parts 0 to VII lead with the administrator's model and the
  decision they face. Part VIII and the appendices lead with the artifact, because you read
  those mid-incident.
- **§17, reference goes to the appendices.** Exhaustive command listings, endpoint tables and
  flag enumerations live in Part 09 and get linked. The test: would removing this command
  break the explanation? If not, it belongs in an appendix.
- **§20, one paragraph, one line.** Do not hand-wrap prose. Your editor wraps it, the
  reader's browser wraps it, and hand-wrapping makes every diff noisier than the change.

`_template.md` is the section shape. `OUTLINE.md` holds the binding filename registry, since
sections forward-link to sections nobody has written yet.

## Claims about Fleet get verified

Anything the manual asserts about how Fleet behaves is checked against a **release tag**,
never a branch and never `CHANGELOG.md`, and the check is written down in
`research/section-notes/`.

A section carries the `verified_*` fields only when that check actually happened and its
notes file exists. If you are unsure, write:

```yaml
verified_source: "unverified: drafted from prior work, not checked at a tag"
```

An honest unverified stamp is worth more than a confident wrong one. Sections have twice
shipped here claiming verification that never ran.

**Point releases are not new book versions.** The book tracks a Fleet minor line (4.90,
4.91); a point release (4.90.1) is flagged inline as a footnote or parenthetical, not
re-stamped as its own version. `STYLE.md` §9 has the rule and the flag forms.

### Read the schema, not the migration that created the table

A migration tells you what a table looked like on the day it was added. It does not tell you what
the table looks like at the tag, because a later migration may have altered it.

This produced a wrong claim in the Part V structure proposal. Migration
`20250127162751_AddUnifiedQueueTable.go` creates `upcoming_activities` with an `activity_type`
enum of four values, and that count was carried into the proposal as the number of activity types
Fleet supports. It is five: `20251028140300_AddInHouseAppsToUnifiedQueue.go` adds
`in_house_app_install`. The reviewer caught it.

**For the current shape of any table, read `server/datastore/mysql/schema.sql`.** Use migrations to
learn *when* and *why* something changed, and to read their comments, which are often the best
statement of intent available. Never treat one as the authority on the present.

The same reasoning applies to anything generated or accumulated: prefer the file describing the
current state over the file describing a transition into it.

## What "complete" means here

**Jake's decision, 2026-08-25.** The manual is meant to be complete and correct, and length is
not a target in either direction. The test is whether someone who has never used Fleet can work
through this book and come out close to expert, as close as anyone gets without operating a real
estate.

That resolves a question the appendices kept raising. **Completeness is about the reader's path,
not about matching Fleet's reference page for page.**

An appendix is complete when it carries the things that make someone competent and that are not
collected anywhere else: how a surface is organized, how authentication and scoping work, what is
reachable from where, what the precedence rules are, and how one interface maps onto another.
Those are conceptual, they are durable across releases, and assembling them is genuine work no
existing document does.

An appendix does not become more complete by reproducing per-endpoint field lists or per-flag
tables from Fleet's own reference. That material is lookup rather than learning, Fleet maintains
it correctly and continuously, and a copy here would be stale within a release and wrong in a way
this manual could not detect. Point at it instead, precisely.

Applied to the appendix with the most inbound references: a.8 should teach the shape of Fleet's
API, its authentication and scoping model, and the matrix of what must be reachable from where,
which is real and uncollected. It should not restate every endpoint's parameters.

The same test settles a recurring question in the chapters. Where a reader needs to *understand*,
the manual explains. Where a reader needs to *look something up mid-task*, the manual sends them
somewhere that is maintained.

Deployment is the standing exception. The self-hosting chapters (2.2 on architecture and capacity,
and the deployment chapters 2.3 and 2.4) teach the model and the reference paths rather than every
self-hosted topology, so pointing at Fleet's reference architectures and Terraform repos there is
expected, not an unfinished chapter (STYLE §1).

## Verification is necessary and not sufficient

**Established 2026-08-25.** All twelve Part II chapters carried `status: verified`, a citation
ledger, and a check performed against the tag. An independent review then found a material defect
in every one. Five were correct readings of a source followed by a conclusion the source did not
support; two were chapters contradicting themselves; two were headings asserting more than the
paragraph beneath them.

None of those is a sourcing failure, which is why checking sources did not find them. An author
cannot reliably audit the distance between what a source said and what they concluded from it,
because by the time they check, the conclusion has become their belief about the source.

**So the book's readiness now requires an independent review pass as well as a source check**,
with the findings resolved or explicitly declined in the notes file. Per-chapter `verified`
stamps and the `reviewed_by` / `reviewed_on` frontmatter were retired on 2026-09-03: the book is
versioned and reviewed as a whole, so this review pass applies to the whole book rather than
being recorded chapter by chapter.

The review must not work from `STYLE.md`. A reviewer following our own rules returns our own
opinion with more steps. See `review/BRIEFING.md`, which was written by the reviewer from its own
context for exactly that reason.

Two things follow that are easy to get wrong. The review happens **before** the book is called
ready, not as a later audit of chapters already published. And where the reviewer disagrees with a rule in
`STYLE.md`, surface the disagreement rather than applying the rule silently: the rules are ours,
they are not evidence, and one of them has already turned out to be wrong.

## Visuals

Mark every place a screenshot or diagram would help, even if you cannot make the image
(`STYLE.md` §16). Write the brief as an HTML comment, specific enough that an image model
produces something usable:

```markdown
<!-- DIAGRAM: ...what is in frame, the labels verbatim, what to emphasise... -->
```

**Do not commit placeholder artwork.** A file at the target path reads as a finished
decision. Until the real image exists, park the image line inside the comment; the build
fails on a reference to a missing file.

Each image comment starts with a state marker: `IMAGE-TODO:` for one that does not exist yet,
`IMAGE-REDO:` for one that needs replacing (with a `WHY:` line saying what is wrong), and
`IMAGE-OK:` for one that has been reviewed and kept. **Do not delete an `IMAGE-OK` comment.**
It renders as nothing, and it is the only record of what the picture is meant to show.

```sh
grep -rn "IMAGE-REDO:\|IMAGE-TODO:" manual/     # what still needs artwork
python3 build/check-image-redo.py                # and what an IMAGE-REDO is blocking
```

**An `IMAGE-OK` is accepted against the prose as it stood, and a correction can invalidate it.**
This is not hypothetical. On 2026-08-27 three Part I diagrams were found asserting claims their
chapters had withdrawn hours earlier: the five-channel picture still captioned "They fail
independently" with a cadence of "every 10 to 30 seconds", the access-gates picture still labelling
scope "which devices?" and drawing the interface as an authorization gate, and the service state
model still summarising Redis as "loss costs a retry". Every prose checker passed the whole time,
because none of them can read a `.webp`.

So **when a correction touches something a picture shows, change the marker to `IMAGE-REDO:` in the
same commit**, write the `WHY:` line saying what the picture now asserts that the prose does not,
and correct the `PROMPT:` block while the reason is fresh. `build/check-image-redo.py` makes an
outstanding `IMAGE-REDO` block a `verified` stamp and rejects one with no `WHY:` line.

**Diagrams are the independent reviewer's to write, screenshots are the owner's.** The prompt for a
diagram gets the same treatment as prose: drafted against the chapter as it currently reads,
verified at the tag, and checked for the claims it makes. `scratchpad/imageprompts.sh` is the shape
of that request. Do not hand-edit a prompt and consider it done; a hand-edited prompt is a new claim
like any other correction, and this project's whole record says those need checking.

Use the Fleet brand palette, in hex, and Cloud City for illustration. Both are in
`STYLE.md` §13.

New artwork arrives as PNG and gets converted before commit:

```sh
python3 build/optimize-images.py apply    # ~1MB PNG -> ~80KB WebP, repoints the markdown
```

## Running it locally

```sh
cd website
npm ci
npm start          # http://localhost:3000, reads ../manual directly, hot reloads
```

Two things worth knowing when the site misbehaves:

- **A renamed heading silently breaks every anchor pointing into it.** Run
  `python3 build/check-links.py`, which is also what CI runs.
- **A missing image is a hard build failure**, not a warning, regardless of the
  `onBrokenMarkdownImages` setting. Webpack resolves images as modules.

If the browser shows something that contradicts what is on disk, restart the dev server
before assuming a real inconsistency. Renames in particular confuse its watcher.

## Deploying

`main` deploys automatically. The infrastructure behind it is created once by
`build/aws-setup.sh`, which is idempotent and safe to re-run: a private S3 bucket, a
CloudFront distribution in front of it, and an IAM role GitHub Actions assumes through OIDC
so no long-lived AWS keys are stored in GitHub.

Two things bit us standing this up, both worth knowing if you ever rebuild it.

**Docusaurus emits `some/path/index.html`,** and the S3 REST origin that origin access
control requires does not serve index documents for subdirectories. A CloudFront function
appends `index.html`. Its file-versus-directory test checks the last path segment for a real
extension, **not** whether the URL contains a dot, because every section slug here has one:
`1.1-what-fleet-is`, `8.14-degradation`, `a.6-glossary`. With the naive dot check, the
homepage works and every section returns 403.

**GitHub issues an immutable OIDC subject claim** that embeds numeric owner and repository
ids, `repo:owner@1234/name@5678:ref:refs/heads/main`. Published AWS trust-policy examples all
use the plain `repo:owner/name:ref:...` form, which silently fails to match and produces
`Not authorized to perform sts:AssumeRoleWithWebIdentity`. The setup script derives the real
value from the GitHub API.

## What not to put in this repository

- Customer names, account names, or any detail that would identify a customer from an
  anecdote. Anonymous operational detail is welcome and is much of what makes the book
  useful; the identifying part is not.
- Host identifiers: serial numbers, UUIDs, host IDs.
- Infrastructure access details, addresses, or credentials.
- Anything from Fleet's private repositories or internal systems.

## The checks, and where each came from

Every script in `build/` exists because a specific defect shipped. None was written from imagining
what might go wrong, and that has turned out to matter: the rules written from imagination in
`STYLE.md` have twice failed on their own author within hours of being written, while the checks
have caught something on nearly every run.

| Script | Gates CI | Built after |
|---|---|---|
| `check-links.py` | Yes | A renamed heading silently broke every anchor into it |
| `check-verified.py` | Yes | Per-chapter `status` / `reviewed_by` / `reviewed_on` stamps were retired 2026-09-03; now fails if one drifts back into frontmatter |
| `check-crossrefs.py` | Advisory | "As 2.2 notes, escrowed Linux disk encryption data", where 2.2 said no such thing. Also carries the §8 and eaten-code-span checks |
| `check-activity-names.py` | Advisory | `user_mfa_requested`, documented in two chapters, exists nowhere in Fleet |
| `check-schedule-names.py` | Advisory | `software_checksum_migration`, given an interval and a description, exists nowhere in Fleet |
| `check-column-names.py` | Advisory | Part VIII prints column inventories for ~20 tables; `check-table-names.py` covered table names and nothing covered columns |
| `check-absolutes.py` | Advisory | Five defects that were universal claims built from a partial reading |
| `check-headings.py` | Advisory | Headings asserting more than the paragraph beneath them |
| `check-em-dashes.py` | Yes | Eleven accumulated in one session in a manual whose STYLE forbids them, which is what a rule with no check behind it looks like |
| `check-pinned-links.py` | Yes | Sixteen links to `blob/main` in a manual that states what one release does. A moving link looks like a citation and behaves like a guess |
| `check-shell-placeholders.py` | Yes | `--enroll-secret=<secret>` in the primary macOS install command: unquoted, the shell reads `<` as redirection and it fails before Fleet is contacted. Twelve commands had it |
| `check-frequency-claims.py` | Advisory | Correcting "X is the cause" to "X is *usually* the cause" reads as a hedge and invents a triage order the source does not supply. Flagged by reviewers in seven chapters |
| `check-outline-deferrals.py` | Advisory | "The full action-by-action breakdown is in a.4", where a.4 is a stub. `check-links.py` passes because the file exists |
| `claims.py` | Run by hand | Two chapters contradicting each other while each was internally consistent |

`claims.py` is the odd one and the most useful when writing. It takes a term and prints every
sentence in the manual that mentions it, grouped by chapter:

```sh
python3 build/claims.py cooldown
python3 build/claims.py "enroll secret"
```

Run it before writing about a mechanism another chapter probably already covers. §27 says to read
a new chapter against the book, and nobody does that reliably from memory across seventy files.
Its first run found the same setting spelled two ways in three chapters.

**The pattern worth continuing.** When a defect is found, ask whether its class is detectable. If
it is, write the check before fixing the instance, and read the canonical values from Fleet's own
source so the check tracks the release rather than a snapshot.

**Correct the ledger row, not just the chapter.** When a review overturns a claim, the fix has two
halves and the second gets skipped: the chapter gets corrected, and an "applied" section gets
appended to the ledger describing what changed, while the original **Stated** row still asserts the
superseded claim with its original citation. A reviewer reading the ledger then finds two
incompatible accounts and no way to tell which is current, and the next writer citing that row
reintroduces the error.

This was found in 3.3's ledger on 2026-08-27, where four rows still carried a coupling model the
chapter had abandoned, an hourly-retry claim that was wrong in both directions, a grace period
described backwards, and three external claims sourced to a neighbouring chapter. **Edit the row in
place**, say what it now claims and that it was corrected, and keep the original error visible in
the row rather than only in the appended section. The ledger is a record of what is believed and
why, not a changelog.

**One operational hazard, recorded because it cost a file.** Bulk edits in this repository are
usually done with a throwaway Python script. `io.open(path, "w")` **truncates immediately**, so a
script shaped like

```python
io.open(p, "w").write(s.replace(a, b, 1))
```

destroys the file if anything in the expression raises. That happened to `HANDOFF.md` on
2026-08-27, from a typo in the replacement variable; git had it, so nothing was lost. Build the
new text into a variable first, then open and write, and the failure mode disappears.

### One that did not work, and why it was dropped

8.13's worked escalation example named `nano_command_queue`. No such table exists; the real one is
`nano_enrollment_queue`. `check-table-names.py` could not see it, because the name was in a prose
blockquote rather than in a SQL block, so the obvious move was to extend the checker to backticked
snake_case identifiers in prose.

It was written and it does not work. Fleet legitimately spells config keys, MDM asset names,
webhook names, activity types, and column names in exactly that shape, in exactly that position,
in the same paragraphs. Suppressing every known one of those still left **37 false positives and
zero true positives** across the manual. Similarity scoring against the real table names does not
separate them either: the genuine error scores 0.774 against its nearest real table, while
`vpp_token`, a correct reference to an MDM asset, scores 0.947.

There is no signal here to tune toward, and tuning until the one known answer appears is fitting
the test set, which §27 already warns against. A checker with that ratio teaches you to skip its
output, which costs more than the single catch is worth. It was reverted rather than shipped.

**So: not every defect class is checkable.** When the honest answer is that a rule would fire on
correct prose more often than on wrong prose, say so and leave the check unwritten. Note it here
so nobody spends the afternoon rediscovering it.

### And one that does work, for the reason the other one failed

`check-column-names.py`, written 2026-08-26, verifies column names rather than table names. It
succeeds where the prose experiment failed, and the difference is worth stating because it is the
rule for whether the next checker is worth writing.

It never reads prose. It reads only ` ```sql ` fenced blocks, and within them only `alias.column`
references where the alias is bound by a `FROM` or `JOIN` in the same block. **The binding is what
removes the ambiguity**: the table is not inferred from the identifier's shape, it is declared two
lines above. Unaliased columns are ignored on purpose, because attributing them in a multi-table
query needs real SQL scope analysis and guessing is what generates noise.

Current coverage is 146 distinct table-and-column pairs across 27 tables, from 99 SQL blocks, with
zero findings on the manual as it stands. Backtested by seeding three plausible wrong columns into
8.6: all three caught, correct line numbers, no false positives elsewhere.

What it does **not** cover, and what still needs a human: the column inventory *tables* in Part
VIII's prose, where columns are listed as backticked identifiers in a markdown table rather than
used in a query. That is the case CONTRIBUTING already says is unfixable by rule.

**The general lesson.** A checker is worth writing when the thing it needs to know is declared in
the text rather than guessed from it. `FROM upcoming_activities ua` declares it. A backtick in a
paragraph does not.

## A scripted edit can delete far more than you asked it to

This has now happened twice, in the same shape, and the second time no checker noticed.

**2026-08-25.** `io.open(p,'w').write(s.replace(a,b,1))` truncated `HANDOFF.md` to zero,
because `'w'` empties the file before the expression on the right is evaluated and that
expression raised. Recovered from git. Open for writing only after the new content exists.

**2026-08-27.** A `re.sub` with `re.S` and a non-greedy `.*?` deleted **131 lines and two
whole sections** from 1.2. The pattern was meant to remove a short note; its lookahead
matched a phrase 131 lines further down, and `.*?` cheerfully spanned everything between.

```python
# what was written                          # what it matched
r'\n\s+NOTE 2026-08-27:.*?'                # a note inside a SCREENSHOT comment
r'(?=\n\s+(?:IMAGE-OK-WAS:|Until it))'     # a phrase 131 lines later
```

**Every existing check passed afterwards.** Links resolved, because the deleted text held
no unique target. Anchors resolved. The frequency, em-dash, pinning and placeholder
checkers were all happy. An independent reviewer found it a round later, by noticing that
the chapter "jumps from the bundle introduction straight into a diagram whose terms are no
longer defined in visible prose". A reader would have hit the same wall.

So:

- **Prefer an exact `str.replace` with an asserted anchor** over a regex. Nearly every edit
  in this project is a known-string substitution and does not need one.
- **If a regex is genuinely needed, do not combine `re.S` with `.*?` and a lookahead.**
  Bound it: match within a single comment block, or capture and inspect the span first.
- **Run `python3 build/check-chapter-shrink.py` before committing a scripted edit.** It
  reports any chapter that lost more than 15 percent of its lines against a git ref, which
  is what a swallowed section looks like and what ordinary tightening does not.
- **When you do restore lost text, re-source-check it.** It is old text, not verified text,
  and the reviewer that found this loss said so explicitly: "do not blindly restore every
  sentence."

