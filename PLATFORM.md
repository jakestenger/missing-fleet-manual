# Platform plan — from markdown to website

**Status (2026-08-23): built and running locally.** Docusaurus serves the vault
markdown in place at `http://localhost:3000`. Versioning and the feature-request
widget are still design-only. Nothing is published publicly.

Markdown in the vault remains the format of record. The site reads it; it does not
own it.

The requirements below come from Jake (2026-08-19).

## What is actually built

| Piece | State |
|---|---|
| Docusaurus site | Running locally, `~/Source/Personal/fleet-manual-site` |
| Docs source | Reads the vault directly, no copy step |
| Sidebar | Generated from the directory tree |
| Mermaid | Enabled (`@docusaurus/theme-mermaid`) |
| Versioning | Not cut yet, no `versioned_docs/` |
| Feature-request widget | Not built |
| Public hosting | None |

The site config points `path` at the vault folder and sets `routeBasePath: '/'`, so
editing a section in Obsidian hot-reloads the browser. That is the whole reason it
was set up this way, and it is worth preserving through any future move.

### Two settings that are load-bearing

**`markdown.format: 'md'`** — CommonMark, not MDX. Sections are full of angle-bracket
placeholders like `<schedule>` and `<your-server-url>`, which MDX parses as JSX and
fails on. This is a deliberate trade: it costs us React components in pages, which is
why the definition-tooltip idea in `STYLE.md` §14 is currently off the table, and why
the feature-request widget will need MDX confined to specific files if it is ever built.

**`onBrokenMarkdownImages: 'warn'`** — added 2026-08-24. **It does less than it looks like
it does, and this was miscorded here at first.** The setting stops the MDX loader from
throwing, but webpack still resolves each image as a module, so a reference to a file that
does not exist is **still a hard build failure**.

The working method is therefore not to rely on this setting. A brief written before its
image exists parks the markdown image line inside an HTML comment, and the comment markers
come off when the file lands. See `STYLE.md` §16.

**`onBrokenLinks: 'warn'`** — set to warn rather than throw because the book is full of
forward links to sections that exist as outlines. Once the book is complete this should
become `throw`, and the check in `OUTLINE.md` should move into CI.

### Where images go

`STYLE.md` §16 marks every place a screenshot or diagram would help. When those images
get generated, they go in an `assets/` folder inside the part directory, referenced
relatively. `01-foundations/assets/` and `02-administer-and-deploy-fleet/assets/`
already exist. Docusaurus resolves relative image paths from the markdown file, and
Obsidian previews them, so both surfaces work from one path.

### Stray file to clean up

`manual/08-troubleshooting/sidebars.js` does not belong in the docs tree. The real
sidebar config is site-local. It is harmless but confusing, and it will end up in a
version snapshot if left.

## Requirements

1. **Version-pinned documentation.** A customer on an older Fleet release picks
   their version from a dropdown and reads the manual as it existed at that release.
2. **Open feature requests per feature.** Each chapter shows the currently-open FRs
   relating to it — what's already been identified as missing, and what customers
   want it to do.
3. Markdown source, git-tracked, still editable in Obsidian.

## Recommendation: Docusaurus

| Option | Versioning | Custom components | Verdict |
|---|---|---|---|
| **Docusaurus** | First-class. `docs:version` snapshots the tree; dropdown built in. | MDX → React components embed directly in a page. | **Recommended** |
| MkDocs + Material + `mike` | Good, via the `mike` plugin. | Awkward — build-time macros, no real component model. | Fallback if we want to avoid a Node toolchain |
| Starlight (Astro) | Not built in; needs a plugin or manual trees. | Excellent. | Rejected on versioning |
| VitePress | Not built in. | Good. | Rejected on versioning |
| GitBook / Mintlify / ReadMe | Included. | Limited; hosted. | Rejected — less control, recurring cost |

Docusaurus wins because requirement 2 needs a real component and requirement 1 needs
native versioning. It's the only option strong at both. Output is static, so hosting
is trivial and cheap.

## Versioning strategy — the part that bites people

Docusaurus versioning **snapshots the entire docs tree** per version. At Fleet's
~3-week cadence that's roughly 17 snapshots a year. Naively turning it on produces
a repo and a build that degrade fast.

Three decisions make it work:

**1. Cut the snapshot in CI at release tag, not by hand.** When Fleet tags a
release, CI runs the version command and commits the snapshot. Zero manual effort,
and the snapshot genuinely is "the manual as it existed at 4.89.2."

**2. Freeze old versions. Do not backport.** This is the correct semantic, not a
compromise — the reader asked for the docs *as they were*. The only exception is a
factual correction to something that was wrong at the time, and it should be marked
as a correction. This eliminates the maintenance burden that usually kills doc
versioning.

**3. Prune to a supported window.** Keep the last N releases live in the dropdown
(pick N from what customers actually run, not a round number). Older snapshots stay
in git history and can be served as static archives if anyone needs them.

## Feature-request widget

### How Fleet's issues are actually labelled

Verified from `~/Source/Fleet/fleet-public/.github/ISSUE_TEMPLATE/` and
`handbook/company/product-groups.md`:

- Feature requests carry the **`:product`** label (`feature-request.md` template).
- User stories carry **`story`**.
- Bugs carry **`bug`**.
- Six product-group labels route ownership:
  `#g-orchestration`, `#g-apple-at-work`, `#g-power-to-pc`, `#g-auto-patching`,
  `#g-supply-chain`, `#g-byod`.

**The problem:** six product groups is far coarser than ~40 manual sections.
`#g-apple-at-work` alone covers ADE, ADUE, profiles, DDM, VPP, Platform SSO, and
more. Labels alone can't drive the widget.

### Design

Each section declares its own query in frontmatter:

```yaml
feature_requests:
  labels: [":product", "#g-apple-at-work"]
  match: ["VPP", "App Store", "volume purchase", "Apps and Books"]
  exclude: ["Android"]
```

**Fetch at build time, not in the browser.** Reasons: no API token in client-side
code, no CORS, no rate limiting against the reader, and — most importantly — the
list gets frozen into the version snapshot, which is semantically correct. A reader
on the 4.86 docs should see the FRs that were open at 4.86.

Build step: query the GitHub API once per section query → write a static JSON blob →
an MDX `<FeatureRequests />` component renders it with title, number, link, and
upvote/reaction count.

**Open question:** `match` is keyword matching against issue titles/bodies, which
will be imprecise. Alternative is maintaining an explicit issue-number list per
section — accurate but manual. Probably: keyword match to *surface candidates*, plus
a per-section pin/exclude list for the ones that matter. Decide when we build it.

## What this means for the markdown we write now

Cheap to do now, expensive to retrofit:

- **Frontmatter is the contract.** Keep `title`, `verified_against`, `verified_on`,
  `further_reading`, `feature_requests` in every section even while unused.
- **One folder per chapter, one file per section**, numbered — that maps cleanly to
  a Docusaurus sidebar.
- **Relative links between sections**, never absolute vault paths.
- **Stable section IDs** (e.g. `8.2`) that other sections reference — the
  troubleshooting cross-references depend on these surviving the move.
- Don't use Obsidian-only syntax (`[[wikilinks]]`, embeds) in manual content. Plain
  markdown links only. Obsidian callouts (`> [!internal]`) are fine — they degrade to
  blockquotes and we strip them on export anyway.
