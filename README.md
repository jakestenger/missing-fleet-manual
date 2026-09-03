# The Missing Fleet Manual

A hand-written guide to every Fleet feature — **complete enough to read on a plane,
and deep enough to explain how Fleet actually works underneath.**

## The premise

**Complete, self-contained, and deeper than the docs.**

The acceptance criterion is the airplane test: a reader with a PDF of this book, on
a plane, with no network, should be able to understand and operate Fleet. That means
we reproduce procedure, config, and payload shapes wherever the reader needs them —
overlapping with fleetdm.com/docs is not a defect.

The one deliberate exception is deployment. The self-hosting chapters teach the model
and the reference paths rather than every possible topology, and there they point at
Fleet's reference architectures and Terraform repos by design. Everything else aims
for the airplane test.

The official docs are a **floor, not a boundary.** We cover what they cover, then
keep going into the mechanism they stop short of: how Fleet actually does the thing,
where state lands, and how the edge cases resolve. That's what customers ask about,
and it's where the book earns its place.

Two working stances follow from this:

- **A customer question is a documentation gap.** The job isn't to answer it — it's
  to put the answer where the next person finds it without asking.
- **Troubleshooting is a methodology, not a symptom table.** Sections teach a
  narrowing procedure — how to reason from "something is wrong" to a specific stage
  of a specific pipeline — not a list of anticipated failures.

## Audience

Two readers, one book:

- **Core prose is generic** — written for a competent IT/platform engineer running
  Fleet. No customer names, no internal process, no Fleet-internal context.
- **Internal annotations** live in `> [!internal]` callout blocks. Customer-specific
  war stories, competitive notes, engagement context. These are stripped on any
  external export.

This means every section is publishable to a customer at any time, minus the callouts.

## How it's built

Manual. There is no pipeline, no database, and no scheduled job.

Jake writes it section by section with Claude. Claude researches from primary
sources; Jake directs, corrects, and edits. Sections are plain markdown files in
this vault, browsable in Obsidian.

A Docusaurus site reads those files in place and serves them at
`http://localhost:3000` for reading in a browser. It is a view, not a build step:
the markdown in this vault is the format of record. See `PLATFORM.md`.

## Primary sources

In priority order. Everything asserted in a section should trace to one of these.

| Source | Location | What it's good for |
|---|---|---|
| Fleet docs | `~/Source/Fleet/fleet-public/docs/` | Official behavior, config reference |
| Fleet guides | `~/Source/Fleet/fleet-public/articles/` (491 files) | Task walkthroughs, real scenarios |
| Handbook | `~/Source/Fleet/fleet-public/handbook/` | Pricing/feature tiers, process |
| Source code | `~/Source/Fleet/fleet-public/server/`, `ee/`, `orbit/` | Ground truth when docs are vague. Research only — never cited in prose (`STYLE.md` §8) |
| Release notes | GitHub releases, at the tag | **Authoritative for what shipped.** Beats the build files when they disagree |
| CHANGELOG | `~/Source/Fleet/fleet-public/CHANGELOG.md` | Failure modes. **Never derive a version from it** (`STYLE.md` §9) |
| GitHub issues | `github.com/fleetdm/fleet/issues` | Open bugs, known limitations |
| Jake | — | Field experience; the whole point of the book |
| Support conversations | ongoing | Customer questions reveal documentation gaps |

Never index or cite Fleet's private repositories.

## Working on it

The manual is a git repository with a Docusaurus site in `website/` that reads `manual/`
directly. Open a pull request; CI builds it and checks every link, anchor, and image. Merging
to `main` deploys.

See `CONTRIBUTING.md` before your first edit.

```sh
cd website && npm ci && npm start     # http://localhost:3000
```

> Some working material is kept outside this repository: the session log, the intake
> process, the phase research that produced Part VIII, and the pre-reorganization
> salvage. It is either derived from private customer support data or is internal
> working detail with no value to a contributor. The verification trail that backs
> every `status: verified` claim **is** here, in `research/section-notes/`.

## Layout

```
missing-fleet-manual/
├── README.md            ← this file
├── OUTLINE.md           ← the table of contents (living plan)
├── STYLE.md             ← the writing rules; read before any prose
├── PLATFORM.md          ← eventual website: versioning + feature-request widget
├── CONTRIBUTING.md      ← read before your first edit
├── _template.md         ← copy this to start a section
├── build/               ← check-links, optimize-images, unwrap
├── website/             ← Docusaurus site; reads ../manual, deployed on merge
├── .github/workflows/   ← PR build check, and deploy to S3 + CloudFront
├── research/
│   └── section-notes/   ← the audit trail; a section is not `verified` without one
└── manual/
    ├── 00-Introduction/ … 08-troubleshooting/   ← one folder per part
    └── 09-appendices/   ← reference material lives here, not in the chapters
```

Ten parts. `OUTLINE.md` holds the binding filename registry; paths there are
canonical because sections forward-link to sections that aren't written yet.

## Working on it

Pick a section from `OUTLINE.md`, copy `_template.md`, and write it. Read `STYLE.md`
first. Four rules do most of the work:

- **The airplane test (§1)** — the book is self-contained.
- **Troubleshooting is a methodology (§5)** — Part VIII owns it; chapters point into it.
- **Narrative sections, reference appendices (§17)** — commands, endpoint tables and
  flag listings go to Part 09 and get linked, not into the flow of a section.
- **Mark every place a visual would help (§16)** — leave a `<!-- SCREENSHOT: -->` or
  `<!-- DIAGRAM: -->` brief. These are content; they don't get resolved away.

Two things that have gone wrong before and are worth naming: only stamp
`verified_against` when the check actually happened and a ledger exists in
`research/section-notes/`, and never cite a source file in prose (`STYLE.md` §8) even
though source code is a legitimate thing to research from.

Record decisions in `OUTLINE.md` so they do not get re-litigated.
