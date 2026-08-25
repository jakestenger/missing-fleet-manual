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

A section may only carry `status: verified` and the `verified_*` fields when that check
actually happened and its notes file exists. If you are unsure, write:

```yaml
verified_source: "unverified: drafted from prior work, not checked at a tag"
```

An honest unverified stamp is worth more than a confident wrong one. Sections have twice
shipped here claiming verification that never ran.

## Verification is necessary and not sufficient

**Established 2026-08-25.** All twelve Part II chapters carried `status: verified`, a citation
ledger, and a check performed against the tag. An independent review then found a material defect
in every one. Five were correct readings of a source followed by a conclusion the source did not
support; two were chapters contradicting themselves; two were headings asserting more than the
paragraph beneath them.

None of those is a sourcing failure, which is why checking sources did not find them. An author
cannot reliably audit the distance between what a source said and what they concluded from it,
because by the time they check, the conclusion has become their belief about the source.

**So `verified` now requires an independent review pass as well as a source check.** Both, with
the findings resolved or explicitly declined in the notes file. Add to the frontmatter:

```yaml
reviewed_by:            # e.g. codex gpt-5.6-sol
reviewed_on:            # YYYY-MM-DD
```

`build/check-verified.py` reports any section stamped `verified` without them.

The review must not work from `STYLE.md`. A reviewer following our own rules returns our own
opinion with more steps. See `review/BRIEFING.md`, which was written by the reviewer from its own
context for exactly that reason.

Two things follow that are easy to get wrong. The review happens **before** the stamp, not as a
later audit of chapters already published. And where the reviewer disagrees with a rule in
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
```

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
