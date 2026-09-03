# Style guide

Short on purpose. Read before writing any prose.

## 0. Who this is for

**Enterprise infrastructure and endpoint administrators running Fleet, and the Fleet
employees who support them.** Not developers, and not Fleet engineers.

That single fact settles most questions of depth and register. The reader wants to know what
Fleet does, why it behaves the way it does, and what to do about it. They are not going to
read the source, and they should never need to.

### The book is read two ways

It is **a guided administration manual and a reference manual at once.** Parts 0 through
VIII are a coherent read front to back. An experienced administrator also drops in cold to
find one setting, command, permission, or platform behaviour.

Four entry points, and every one of them has to work:

| The reader arrives asking | They land on |
|---|---|
| What outcome do I need? | The capability index, `a.1` |
| What platform do I manage? | The platform matrix `a.2`, then the platform chapter |
| What interface am I using? | GitOps, REST API and fleetctl chapters, then `a.7` and `a.8` |
| What is unexpected? | The troubleshooting index, Part VIII |

Design every section so a cold arrival works: say what the section covers up front, and
link outward rather than assuming the reader came through the previous chapter.

## 1. Completeness — the airplane test

**A reader with a PDF of this book, on a plane, with no network, should be able to
understand and operate Fleet.**

That is the acceptance criterion. It overrides everything else. If a section
requires the reader to go read fleetdm.com/docs to make sense, the section is
unfinished.

This means we **do** reproduce procedure, config reference, payload shapes, and
command syntax when the reader needs them. Overlapping with the official docs is
not a defect.

The official docs are a **floor, not a boundary**: we cover at least what they
cover, then keep going into the mechanism they stop short of. Links to docs are
*further reading*, never load-bearing.

## 2. A customer question is a documentation gap

If someone had to ask, the information wasn't findable. So the job isn't to answer
the question — it's to **put the answer where the next person will find it without
asking.**

Practically: absorb the answer into the body of the relevant section, at the
heading where a reader would look for it. A question that survives as a standalone
FAQ entry usually means we failed to place it. Keep an FAQ only as a staging area
or a pointer index into the body.

## 3. Mechanism is the main event

Customers overwhelmingly ask **"how does Fleet actually do this?"** and **"what
happens when…?"** — not "which button." So "How it works" is the largest part of
most sections, and it should go deeper than feels necessary.

Write the mechanism as an **ordered pipeline**:

- Name every component in the path and what each one does.
- State the protocol or transport at each hop.
- State **where state lands** — which table, file, cache, or queue.
- State what is **observable** at each stage, and how to observe it.
- State the timing: what's synchronous, what's a cron, what's on next check-in.

That last set of points isn't decoration. It's what makes §5 possible — a
mechanism written as an observable pipeline *is* the diagnostic scaffold, and
troubleshooting falls out of it nearly for free.

## 4. Edge cases and precedence get their own heading

This is the most-asked and least-documented category in all of Fleet. Every
section should answer, where applicable:

- What happens when two things **conflict** or target the same host? What wins?
- What's the **ordering** guarantee, if any?
- What happens if the host is **offline** — is it queued, replayed, or dropped?
- What happens on **retry**? Is the operation idempotent?
- What happens if it's **interrupted** halfway?
- What happens when a value is **empty, missing, or malformed**?
- What are the **limits** — size, count, rate — and what happens at the boundary?

If you don't know, say "not documented; unverified" rather than guessing. An
honest gap is useful; a confident wrong answer is not.

## 5. Troubleshooting is a methodology, not a symptom table

**Do not write a `Symptom | Cause | Fix` table.** It only helps someone whose
problem you already anticipated, and it goes stale.

Write a **narrowing procedure** — how a competent engineer reasons from "something
is wrong" to a specific stage. The parts:

1. **Enumerate the stages.** You can't diagnose what you can't enumerate. Reuse the
   pipeline from §3.
2. **Give the observation point for each stage** — the exact log, table, command,
   or endpoint that says whether that stage is healthy.
3. **Give the narrowing logic** — bisect the pipeline rather than walking it
   linearly, and state **what each observation rules in or out**. This is the part
   that makes it methodology instead of a checklist.
4. **Say how to reproduce it on demand**, and how to shrink to a minimal case.

A symptom index is fine, but it should *point into* the procedure, not replace it.

### Where troubleshooting content lives

**Chapter VIII owns all of it.** Both the how-to procedures and the reference material:
log-surface tables, state-table column lists, command references, query listings. If a
reader is debugging, everything they need is in Part VIII.

**Feature chapters are about design and use.** How Fleet was designed to work, why it is
shaped that way, and what the feature is used for. A feature section's troubleshooting
heading is a three or four line pointer into Part VIII, never a procedure and never a
duplicate of its tables.

The test: if content answers "what do I run when this breaks", it belongs in Part VIII. If
it answers "why is it built like this" or "what would I use this for", it belongs in the
feature chapter.

### Worked example of the shape

> *Illustrative — teaching the shape, not a verified chapter.*
>
> **"Our SIEM is ingesting query results timestamped three months ago."**
>
> Stages: osquery on the host runs the scheduled query → buffers results locally
> if it can't reach Fleet → ships on the next logger period (`logger_tls_period`)
> → Fleet's server receives them → Fleet writes to the configured
> `osquery_result_log_plugin` destination → the destination's own pipeline →
> the SIEM indexes them.
>
> The narrowing question is **which timestamp is old** — the one *inside* the log
> record, or the one the destination stamped on arrival. Those two answers point at
> opposite ends of the pipeline:
>
> - Record timestamp old, arrival timestamp recent → the data was generated long
>   ago and is only now arriving. Look **left**: hosts that were offline or
>   couldn't reach Fleet are draining their local osquery buffer, replaying old
>   results with their original timestamps. Confirm by checking whether the
>   affected hosts share a recent return-to-service.
> - Both timestamps old → the data isn't new at all. Look **right**: the SIEM is
>   re-reading or re-processing an existing bucket/stream, not receiving anything
>   new from Fleet. Confirm by checking whether Fleet is emitting at all.
>
> One observation cuts the search space in half. *Then* you go looking at specific
> logs — and you know which end to look at.

Note that the example needs the buffering behavior from §3 to work. Without the
mechanism, there's no procedure — only guessing.

## 6. Prefer the durable surface

Completeness has a cost: duplicated procedure goes stale when Fleet changes.

That cost is **managed, not existential** — Fleet ships roughly every three weeks and
documents product changes per release, so we get a written changelog on a schedule
(see the intake process). Staleness is a maintenance loop, not a slow leak.

It's still worth describing things at the level that survives:

- Prefer **GitOps YAML and API shapes** over UI click-paths — they change more slowly
  and they're what the reader automates against anyway.
- When UI steps are genuinely needed, keep them terse and mark them as volatile.
- Mechanism outlives interface. Weight the section accordingly.

## 7. Generic core, internal annotations

Core prose is publishable to a customer as-is: no customer names, no people, no
internal URLs or hostnames, no Fleet-internal process. Anything that can't meet
that bar goes in a callout, stripped on external export:

```markdown
> [!internal]
> A customer hit this when their ABM token expired mid-migration — the symptom was
> silent, not an error.
```

Genericise in prose ("a customer", "the customer's Fleet server") rather than using
fake placeholders. Keep all Fleet-technical content exact.

## 8. Claims are grounded, but never cite code

**Verify against source. Do not show the source to the reader.**

Reader-facing prose describes expected behaviour and process. It does not name Go files,
paths, line numbers, functions, or internal identifiers. `resolveFirstAddedInstallersForHost`
means nothing to an administrator; "when a host matches more than one package, Fleet installs
the one that fits the host's platform" means everything.

| Instead of | Write |
|---|---|
| "confirmed in `server/service/schedule/schedule.go:484`" | "a trigger is ignored when a run is already pending" |
| "`MaxPackagesPerTitle = 10` (`server/fleet/software_installer.go:1281`)" | "a title holds at most 10 packages" |
| "the `instanceID` in `cmd/fleet/serve.go`" | "the instance identifier Fleet logs at startup" |

**The verification trail still matters, it just lives elsewhere.** Put file paths and line
numbers in the section's notes file under `research/section-notes/`. That is where a future
editor checks the work. The published section carries the behaviour.

Keep citing things the reader can actually use: fleetdm.com documentation, guides, GitHub
issue numbers, release notes, and configuration or API reference pages.

Honesty rules are unchanged. When something is undocumented or you could not confirm it, say
so in plain terms ("not documented; unverified"), without pointing at code.

## 9. Currency

Every section carries `verified_against` (a Fleet release), `verified_on` (a date), and
`verified_source` (the ref you checked). Update all three whenever you touch a section. A
section several releases behind is suspect, not wrong. Flag it, do not auto-delete it.

### Verify against a release tag, never a branch and never a commit

The book is versioned per Fleet release (see `PLATFORM.md`), so verification pins to a
release too. Work from a local branch cut at the release tag:

```sh
cd ~/Source/Fleet/fleet-public
git fetch --tags --quiet
git tag -l "fleet-v4.9*" --sort=-v:refname | head -3       # find the current release
git checkout -b manual-verify-<version> fleet-v<version>    # e.g. fleet-v4.90.1
git rev-parse --abbrev-ref HEAD                             # confirm before writing
```

Frontmatter records the tag:

```yaml
verified_against: Fleet 4.90.1
verified_source: git tag fleet-v4.90.1
```

A commit hash pins to something no reader can install. A release tag pins to what they
are actually running, which is the only comparison that helps them.

**Agent versions ship separately.** fleetd and Orbit carry their own tags
(`orbit-v1.59.0`), independent of the Fleet server release. When a claim depends on agent
behaviour rather than server behaviour, say which agent version you checked.

### Two traps that produced a wrong stamp on every Part VIII section

**Never derive the version from `CHANGELOG.md`.** In `fleet-public` that file is assembled
at release time from the `changes/` directory, so on `main` it lags by up to a release. On
2026-08-19 it read 4.89.2 while the code already contained 4.90.0 features, and every Part
VIII section got stamped 4.89.2 as a result. At a release tag the file is accurate, which
is a second reason to work from tags.

**Check what ref you are on before verifying anything.** Part VIII was verified against a
feature branch sitting 425 commits behind `main`. Confirm the ref first, every time.

## 10. Voice

Direct, second person, no marketing register. Assume a competent platform engineer
who is short on time and has already tried the obvious thing.

Avoid "simply", "just", "easy", "seamless", "powerful", "robust". If a thing is
finicky, say it's finicky. Short declarative sentences. Tables for anything
enumerable. Real runnable commands — never pseudo-commands.

## 11. Don't slot-fill the template

`_template.md` is a checklist of things worth considering, not a form. Drop
headings that don't apply to the topic and add ones that do. A section where every
heading is present but three are one thin line each is worse than a shorter
section that says real things.

## 12. Two registers, and which one you are writing in

**Revised 2026-08-23.** This section previously said "lead with the artifact, and if a
section can open with a table, it should." That is right for a reference chapter and wrong
for a narrative one. Which register applies depends on where you are writing.

### Reference register — Part VIII and the appendices

Consulted mid-incident, not read through.

- **Lead with the artifact.** Table, command, path, or query first; explanation after.
- **One idea per heading**, findable by scanning. A reader under pressure reads headings
  and tables, not paragraphs.
- **Cut the justification.** Say what to do and what it tells you. Why it works is one
  sentence, not a paragraph.
- Prose earns its place only where the reader needs reasoning: a narrowing procedure, a
  mechanism, a judgement call.

### Narrative register — Parts 0 through VII

Read in order by someone learning the system, and dropped into cold by someone who already
knows it.

- **Lead with the administrator's model and the decision they face**, not with an artifact.
  What is this for, what are you choosing between, what does the choice cost you.
- **Then** procedure, platform differences, and verification.
- **Prose and scenarios carry mechanics that need a mental model.** Do not compress a
  concept into a table to look tidy; a reader cannot learn a relationship from a grid.
- Still no throat-clearing. Drop "it's worth noting", "the reason for this is", and any
  sentence announcing what the next sentence will say. That rule is register-independent.

### When a table is right, in either register

True comparisons, mappings, settings, permissions, platform support, and command or
endpoint reference. If what you are tabulating is a *concept*, write it as prose or draw it
(§13).

### Prose is the default in narrative chapters

**Jake's rule, 2026-08-23, after reading Part I.** The strong preference is prose for
conveying how Fleet works. Tables have real value, and a reader should be *led into* one by
explanation rather than dropped on top of it.

Three tests, applied to any table in Parts 0 to VII:

1. **Could a reader learn this from the grid alone?** A comparison of six platforms, yes. A
   mental model of how two ideas relate, no. The second one is prose.
2. **Does it repeat what is already said?** Part I had a chapter stating the same three
   facts in a table, a diagram, and a paragraph. One of the three is enough.
3. **Is it a two-row table?** Then it is two sentences wearing a grid.

When a table survives all three, write the paragraph that walks the reader through it first,
then present the table as the precise version. "With that story in mind, the reference
version:" is a perfectly good way to hand off.

### Not all prose has to be load-bearing

This is the part that cuts against the reflex to compress. **Orientation, metaphor, and
plain conversational framing earn their place**, because they ground a reader before the
technical content arrives. A reader who has been told that a fleet is like an address and a
label is like a mailing list will make far fewer scoping mistakes than one handed a correct
definition of both.

What this does **not** license is padding: restating the previous paragraph, safe truths
that carry no information ("consistency is important"), or throat-clearing that announces
what the next sentence will say. Those still go (§10).

The distinction is whether the sentence changes what the reader can do or understand. A
metaphor that makes a distinction stick does. A sentence that summarises the section they
just read does not.

8.1 is the hardest case in the book (it *is* about method), is knowingly over-long, and
gets a tightening pass later.

## 13. Diagrams in explanatory chapters, tables in reference chapters

**Reference material (Part VIII and the appendices):** tables are right. A reader
mid-incident scans a table, and in an appendix the table is the thing they came for. Keep
them.

**Explanatory chapters (Parts 0 to VII):** use a diagram when it makes a relationship
easier to understand than prose would. Not everything with a shape earns one, and a diagram
that restates a paragraph costs the reader time.

Four kinds earn their place:

| Kind | Use it for |
|---|---|
| Lifecycle or sequence | Setup flow, operational flow, anything with ordered stages |
| Scope | Global versus fleet configuration, label reach, role boundaries |
| Architecture | Fleet server, devices and infrastructure, and what connects them |
| Platform comparison | Only where a picture simplifies a real decision the reader faces |

If a candidate diagram fits none of these, write the prose instead.

### You do not draw the diagram. You write the brief for it.

Jake generates the images separately. Your job is to mark the spot and specify the picture
precisely enough that an image model produces something usable without further context.

**Use the HTML comment from §16:** `<!-- DIAGRAM: ... -->`.

An earlier version of this section put a `> **DIAGRAM PLACEHOLDER**` blockquote in the text.
That is superseded. A blockquote renders on the site, so the reader sees our scaffolding; an
HTML comment does not render, which is what we want. §16 is the single mechanism for both
diagrams and screenshots.

Rules for the brief:

- **Describe the picture, not the concept.** Name the boxes, the arrows, the labels, the
  layout, and the reading order. An image model cannot infer what matters.
- **Specify the words that must appear**, verbatim. Diagrams fail most often on wrong or
  invented labels.
- **State the style** once: flat vector, clean, generous whitespace, legible at half width.
- **One idea per diagram.** Two diagrams beat one crowded one.
- Keep the surrounding prose complete on its own. The diagram is an aid, not a dependency,
  and the airplane test still applies if the image is missing.

### Use the Fleet brand palette, and no other colours

**Verified against Fleet's handbook, 2026-08-24.** Every brief specifies colours as hex
values rather than colour names, because an image model asked for "teal" will invent one.

| Name | Hex | Use it for |
|---|---|---|
| Fleet Black 100 | `#192147` | Headings, key linework |
| Fleet Black 75 | `#515774` | Labels, body text |
| Fleet Black 50 | `#8B8FA2` | Lines and strokes |
| Fleet Black 25 | `#C5C7D1` | Lighter lines and strokes |
| Fleet Black 10 | `#E2E4EA` | Lightest strokes, subtle fills |
| Off-white | `#F9FAFC` | Backgrounds |
| Light blue | `#D3E8F3` | Backgrounds, fills |
| Lighter blue | `#E8F1F6` | Backgrounds, fills |
| Fleet Green | `#009A7D` | **One** accent. Fleet reserves it for calls to action and links |

The palette has two halves, and the second one was missing from this guide until
2026-08-24, which is why the first pass of Part I artwork came back drawn almost entirely in
`#192147` hairlines on `#F9FAFC`.

### The structure set

The Fleet Black ramp and the neutrals above. All text lives here. Use the whole ramp rather
than only its extremes: `#515774` for ordinary labels, `#8B8FA2` and `#C5C7D1` for secondary
structure, `#E2E4EA` for grouping bands. **`#D3E8F3` reads as a fill; `#E8F1F6` reads as
white.** Pick accordingly.

### The Fleet dots

Fleet's logo mark is six coloured dots, and those six are brand colours as much as the navy
is. Extracted from the brand asset:

| Dot | Hex |
|---|---|
| Sky blue | `#5CABDF` |
| Mint | `#3AEFC4` |
| Green | `#63C740` |
| Lavender | `#C98DEF` |
| Apricot | `#FAA669` |
| Rose | `#D66C7B` |

They are soft enough to take `#192147` text on top, so they work as fills rather than only
as strokes. Fleet Green `#009A7D` sits alongside them as the CTA colour.

**Match strength to area.** Full saturation is for small marks: an arrow, a chip, a filled
icon. Over a large panel, use the dot at roughly a 20 to 25 percent tint. The first attempt
at this put five dots at full strength across five large panels and the result looked like a
children's infographic. The same colours as thin arrows, in the five-channels diagram, work
perfectly. Area is the variable, not the colour.

**Do not colour an empty container.** One diagram came back with three large saturated
panels, two of which had nothing inside them. Colour has to carry meaning; an empty coloured
box is noise.

**Use them for categories, not decoration.** One colour per thing a reader has to tell apart,
used consistently within the image, and only as many as there are categories. Five channels
gets five dots. Four items do not get six colours to look lively. If nothing in the picture
needs distinguishing, use none and let the structure set carry it.

This is the correction to an earlier over-reaction. A diagram once came back using eight
invented hues, and the response here was "exactly one accent, no other hues at all", which
produced flat pictures. **The sin was inventing colours, not colour-coding.** Colour-coding
from the dots is on-brand and is often exactly what a diagram needs.

### Give it weight

At least one element per diagram should be a solid filled shape rather than an outline, so
the composition has an anchor. Vary stroke weight so the primary flow reads heavier than the
scaffolding.

Paste this into every brief:

> Fleet brand palette only: off-white `#F9FAFC` background; `#192147` headings and key
> linework; `#515774` labels; `#8B8FA2` and `#C5C7D1` secondary strokes; optional pale blue
> fills `#E8F1F6` or `#D3E8F3`; at most one `#009A7D` Fleet Green accent. Flat vector,
> generous whitespace, no gradients or drop shadows, no logo or watermark, legible at half
> page width.

### Cloud City, for illustration rather than diagrams

Fleet's illustration system is **Cloud City**: floating islands, glass-like structures, wide
open skies, waterfalls, and swans. Fleet describes it as a symbol of openness and clarity,
with each island independent yet interoperable.

Use it for hero and section-opening imagery where the job is tone rather than information.
Do not use it inside an explanatory diagram, where it would compete with the content.

Fleet's handbook also says plainly: **do not use graphics as decoration without purpose**,
do not mix flat and photorealistic styles, and do not introduce visual styles outside the
existing system. A picture on a page needs a reason beyond filling space.

Fleet's own **Graphics and Icons** brand guidance is marked TODO in the handbook, so
anything we invent in that space should stay simple, palette-correct, and easy to replace
when Fleet defines its system.

Mermaid is enabled on the site, so a ```mermaid fence renders if a diagram is genuinely
structural and trivial to express. Prefer the comment and a brief for anything that
wants real visual design.

## 14. Define the unfamiliar: three layers

Readers arrive with uneven background, and a term can mean something narrower inside one
chapter than it does generally. Three layers, each with a job:

**1. Inline gloss, on first substantial use in a section.** A clause, not a footnote. "the
node key, the per-host credential Fleet issues at enrollment". Costs the reader nothing and
keeps them in the flow.

**2. A Vocabulary table near the top of the section**, for terms this chapter uses in a
specific sense. Section 1.4 already does this well: it defines primary, read replica,
instance, campaign, cron schedule, bounded context and reconciler as *this chapter* means
them. Use it when the chapter-local meaning is narrower than the general one.

**3. The glossary appendix** (`09-appendices/a.6-glossary-and-release-compatibility.md`),
the canonical definition, one entry per term. Sections link to it rather than redefining. Terms already flagged for it: VPP, ADE, DEP, SCEP, node key,
pprof, file carving, dead lettering.

Which layer to use: if the term is unfamiliar but means the ordinary thing, gloss inline and
link to the glossary. If the chapter uses it in a narrower sense, put it in the Vocabulary
table and say how it differs. Do not repeat a full definition in more than one place.

**Flagging a gap:** an empty markdown link, `[term]()`, means "needs a definition and does not
have one". Jake marks these while reading. Find them with:

```sh
grep -rnoE '\[[^]]+\]\(\)' manual/
```

*Not currently possible:* hover tooltips. The site is configured for CommonMark rather than
MDX, because our sections are full of angle brackets like `<schedule>` that MDX parses as
JSX. Revisiting that would enable a definition component, at the cost of escaping work
across every section.

## 15. Write in a positive voice

Say what a thing is, not what it is not. Say what happens, not what fails to happen.

| Negative | Positive |
|---|---|
| "determined by the osquery channel only" | "determined by the osquery channel" |
| "Nothing about the Orbit API or the MDM channel enters that calculation." | (cut it) |
| "This does not mean the host is offline." | "The host is still reachable over MDM." |

Two specific habits to avoid:

**Dropping "only" and "just".** They usually add nothing, and when they do add something it is
a defensive tone rather than information.

**Answering questions nobody asked.** Pre-empting a misunderstanding by naming it plants the
misunderstanding. If a distinction genuinely matters, state the correct version positively and
move on. Reserve explicit contrast for cases where readers demonstrably get it wrong, and even
then, one sentence.

## 16. Mark every place a visual would help

**Do this by default, in new writing and when editing existing sections.** Jake reads
visually and finds walls of technical prose hard going. A section that could use a picture
and does not have one is unfinished.

Two kinds, both left as HTML comments so they do not render:

**Screenshots**, for anything the reader does in the Fleet UI. These carry more weight than
diagrams for procedures: they show the actual surface, and they make the manual look like
something a person made.

```markdown
<!-- SCREENSHOT: Host details page, Activity tab, with the "Show MDM commands" toggle
     switched on and one command row expanded to show its result. Crop to the activity
     panel. Highlight the toggle. -->
```

**Diagrams**, for relationships prose handles badly: a pipeline, a decision, a lifecycle, a
scope boundary, an architecture.

```markdown
<!-- DIAGRAM: Three stores and what survives a restart. Fleet server in the centre, MySQL,
     Redis and object storage around it. Label each arrow with what it carries. Mark Redis
     "lost on restart, by design". Flat vector, generous whitespace. -->
```

Write the comment as a usable brief: name what is in frame, the labels verbatim, and what to
emphasise. Jake generates the images separately, so a vague note means a wrong picture.

Diagram briefs should describe one of the four kinds in §13. Screenshot briefs are for the
Fleet UI and have no such restriction: any procedure the reader performs in the console is
a candidate.

### The comment outlives the image

Once an image exists, **the brief stays, directly above the image**, so the prompt remains
editable and regenerable without appearing in the rendered page:

```markdown
<!-- DIAGRAM: Three stores and what survives a restart. Fleet server in the centre, MySQL,
     Redis and object storage around it. Label each arrow with what it carries. Mark Redis
     "lost on restart, by design". Flat vector, generous whitespace. -->
![Fleet server, MySQL, Redis and object storage, and what each one holds](assets/1.6-state-stores.png)
```

Images live in the part's own `assets/` directory, referenced relatively. Both the site and
Obsidian resolve that path, so one form works in each.

Write a real alt text describing what the image shows. A reader with the PDF and no images
rendered still gets the sentence, and the airplane test still applies.

Find them with:

```sh
grep -rn "SCREENSHOT:\|DIAGRAM:" manual/
```

### Category icons on every section, Parts 0 to VII

Each section carries a small icon marking which of the four kinds of material it holds
(§19): explanation, how-to, reference, or troubleshooting. They live in
`manual/_assets/icons/` and are referenced as `../_assets/icons/<kind>.svg`.

Place the badge at the **start of the section's first paragraph**, never in the heading,
because heading text generates the anchor. Where a section opens with a list rather than a
paragraph, put the badge on its own line above the list.

**Part VIII is excluded.** It is a reference chapter whose sections are all diagnostic, so
every badge would say the same thing.

Do not force an even spread. Foundations chapters come out almost entirely explanation, and
that is the correct signal: it tells a skimmer there are no procedures in them.

### Every image comment carries a state marker

**Added 2026-08-24.** Jake feeds these comments to an image model, so each one has to say
what it wants done. Three markers, all greppable:

| Marker | Means |
|---|---|
| `IMAGE-TODO:` | No image exists yet. Generate one from the prompt below |
| `IMAGE-REDO:` | An image exists and should be replaced. A `WHY:` line says what is wrong with it, then the corrected prompt |
| `IMAGE-OK:` | Reviewed and kept. **Do not delete this comment**; the prompt is retained so the image can be regenerated later |

Format:

```markdown
<!-- IMAGE-REDO: assets/1.2-five-channels.webp
     WHY: uses eight saturated hues and a photorealistic server icon.
     PROMPT: ...the corrected brief...
     PALETTE, strictly: ...the palette block from §13... -->
![Alt text](assets/1.2-five-channels.webp)
```

Find outstanding work with `grep -rn "IMAGE-REDO:\|IMAGE-TODO:" manual/`.

**`IMAGE-OK` exists because these comments keep getting deleted.** They render as nothing,
so an edit pass loses them silently, and the 1.6 prompts were removed three separate times
while their images stayed. A marker that says "keep me" is easier to respect than a
convention someone has to remember.

### Two standing instructions every prompt needs

Both learned the hard way, both cheap to include:

- **"Fleet" is a software product, not vehicles.** An image model asked to draw a box
  labelled Fleet produced a laptop displaying cars, vans and trucks. Say it explicitly.
- **No em-dashes in rendered text.** The manual does not use them, and text inside an image
  cannot be fixed by a later editing pass.

### Never commit a placeholder image

**Jake's rule, 2026-08-24.** Do not generate stand-in artwork, not even neat stand-in
artwork in the brand palette.

The reason is specific and worth remembering: Jake feeds these briefs to an image model to
generate the real picture. A placeholder file sitting at the target path made the model
insist the image already existed, and it argued rather than drawing. A file that exists is
taken as a finished decision.

### How to write a brief before the image exists

A missing image file is a **hard build failure**. `onBrokenMarkdownImages: 'warn'` does not
prevent it, because webpack still resolves the image as a module.

So park the image line inside a comment until the file arrives:

```markdown
<!-- DIAGRAM: ...the full brief... -->
<!-- IMAGE PENDING. Drop the generated file at assets/1.4-scope.png, then delete this
     comment's opening and closing markers to make the image live.
![Alt text describing what the diagram shows](assets/1.4-scope.png)
-->
```

The brief stays visible, the alt text is written once and waits with it, the site builds,
and there is no file at the target path to mislead an image model. Making it live is
deleting two lines.

**Do not delete or "resolve" these comments.** They are content, not review notes. Review
notes are plain `<!-- ... -->` comments without the `SCREENSHOT:` or `DIAGRAM:` prefix, and
those do get resolved and removed.

## 17. Narrative sections, reference appendices

**Jake's rule, 2026-08-23.** Keep reference material out of the narrative flow: exhaustive
command listings, endpoint tables, flag enumerations, exit codes, deep technical minutiae.
Put them in an appendix and link to them from the section.

A section explains how Fleet was designed to work and what you would use it for. It is read
start to finish. An appendix answers "what is the exact syntax," and it is scanned, never
read. Interleaving the two makes the section hard to read and the reference hard to find.

### Where things go

| Material | Home |
|---|---|
| How a mechanism works, and why it was built that way | The section |
| What you would use it for, and the decision points | The section |
| The one or two commands needed to follow the narrative | The section, inline |
| Every flag, subcommand and option of a tool | `a.7-fleetctl-command-reference.md` |
| Endpoint and API action listings | `a.8-api-action-and-endpoint-reference.md` |
| Which setting wins when two disagree | `a.3-configuration-model-and-precedence.md` |
| Role and permission matrices | `a.4-roles-and-permissions-matrix.md` |
| Per-platform capability tables | `a.2-platform-capability-matrix.md` |
| Which UI, CLI or API surface can do a given thing | `a.5-interface-index.md` |
| Term definitions | `a.6-glossary-and-release-compatibility.md` |
| Diagnostic procedures, and the tables that serve them | Part VIII |

Part VIII is the exception that proves the rule: it is a reference chapter, so its tables
stay put. §5 already says Chapter VIII owns both the how-to and the reference for
troubleshooting. Do not route Part VIII tables into the appendices.

### This does not weaken the airplane test

§1 says the book is self-contained. The **book**, not each section. Appendices ship in the
same PDF, so a reader offline still has all of it. What changes is where it sits.

The test for whether a command belongs in a section: **would removing it break the
explanation?** A command that demonstrates the mechanism being described stays. A command
listed for completeness moves to the appendix.

### When you move something, link to it

A section that drops a table without a pointer has lost information from the reader's point
of view, even though the book still contains it. Name the appendix and say what is in it.

### Appendices are written, not dumped

An appendix entry gets a sentence of context saying what the thing is for. A bare table with
no framing is a data dump, and §12 applies to appendices too.

## 18. One canonical home per feature

**Every feature is fully explained in exactly one place.** Every other chapter that touches
it links there instead of re-explaining it. Without this rule a feature like disk encryption
gets a partial, slightly different treatment in five chapters, and the reader cannot tell
which one is authoritative.

### Which layer owns what

| Layer | Owns |
|---|---|
| Foundations (I) | The mental model. What the concept is and how it relates to the others |
| Administration (II) | Organization-wide setup and ownership. Standing the service up |
| Platform (III) | Prerequisites, enrollment, and per-platform differences |
| Feature (IV, V) | The capability itself and how to use it |
| Automation (VI) | The GitOps, API and fleetctl equivalents of the above |
| Appendices | Exact commands, endpoints, permissions, precedence |
| Troubleshooting (VIII) | Diagnosis, once the reader already understands the feature |

Worked examples:

- **MDM service setup** is Part II. **Enrolling a Mac or a Windows device** is Part III.
  **Profiles and MDM commands** are Part V. **The exact API endpoints and fleetctl
  invocations** are appendices.
- **Labels** get their model in 1.3 and their use in targeting in 5.1. 5.1 links back; it
  does not restate the scoping rules.

### Linking is not a completeness failure

§1 says the book is self-contained. Cross-linking within the book satisfies that, because
the linked chapter ships in the same PDF. What §1 forbids is depending on **fleetdm.com**,
not depending on chapter 5.

When you link, say what the reader will find there. "Targeting is covered in 1.3" is weaker
than "1.3 explains why a global label can cross fleets and a fleet label cannot."

### When two chapters both seem to own something

The more specific layer wins for *how*, the more general layer wins for *why*. If that
still leaves it ambiguous, pick one, write it there, link from the other, and record the
choice in `OUTLINE.md` so it does not get re-litigated.

## 19. What every chapter contains

From the 2026-08-23 design. These are the elements, not the headings; name the headings for
the topic (§11).

| Element | What it does |
|---|---|
| **Purpose and scope** | What this chapter covers, and what it does not. Makes a cold arrival work |
| **Decision model or prerequisites** | The choice the administrator faces, or what must be true first |
| **How-to guidance** | The procedure |
| **Verification and operational ownership** | How to confirm it worked, and who owns it afterwards |
| **Platform differences** | Only where they change the administrator's decision |
| **Links out** | To the canonical reference (appendix) and to the Part VIII diagnosis |
| **Release metadata** | `verified_against`, `verified_on`, `verified_source` in frontmatter |

**Verification and operational ownership is the one most likely to be skipped**, and it is
the one administrators most need. A procedure that ends at "apply the profile" leaves the
reader without knowing whether it worked or who watches it next week.

Start with the model and the decision. Procedure, platform differences, and verification
follow (§12, narrative register).

## 20. One paragraph, one line

**Jake's rule, 2026-08-24.** Do not hand-wrap prose. Write each paragraph as a single line
and let the reader's software wrap it.

Manual wrapping looks tidy in a text editor and costs everywhere else. It makes editing
harder, because changing a word means rewrapping the paragraph. It makes diffs noisier than
the change deserves. And it does nothing for the reader, since the browser, Obsidian, and a
PDF renderer all wrap to their own width anyway.

This applies to prose, list items, and blockquote paragraphs.

**Leave these alone.** They are line-structured and wrapping is meaningful:

- Fenced code blocks, and their contents
- Table rows, one per line
- Headings
- YAML frontmatter
- HTML comments carrying screenshot and diagram briefs. They do not render, and their
  structure makes them easier to read and edit as a spec.
- Any line ending in two spaces, which is a deliberate markdown hard break

`build/unwrap.py` performs the transformation and verifies it. It compares a
whitespace-normalised signature of every file before and after, so a change that would alter
the rendered output fails loudly rather than silently. Run it as
`python3 build/unwrap.py dryrun` first, then `apply`.
## 21. No "See also" sections

**Jake's rule, 2026-08-24.** Do not end a chapter with a list of adjacent chapters. The
sidebar already does that job, and better, because it shows where the reader is.

A link earns its place **inside** the prose, at the moment the reader would want it, with a
sentence saying what they will find there. "1.3 explains why a global label can cross fleets
and a fleet label cannot" is worth following. A bare link under a "See also" heading is not,
and 70 chapters carrying one was 192 lines of navigation nobody needed.

Two things this does **not** cover, and both stay:

- **The troubleshooting handoff.** A short pointer into Part VIII naming which sections apply
  and why is required by §19, and it is content rather than navigation.
- **`further_reading` in frontmatter.** Those are external documentation URLs, not internal
  navigation, and the site can render them separately.

## 22. Headings say what the section contains

**Jake's rule, 2026-08-24.** A heading is a navigation aid before it is anything else. Someone
skimming should be able to tell from it whether this section holds what they came for.

That rules out headings that state a conclusion instead of naming a subject. "Three
questions", "A useful mental model", "Two records describe one piece of work" all read well
in sequence and tell a skimmer nothing. Compare:

| Instead of | Write |
|---|---|
| Three questions | What does Fleet do? |
| A useful mental model | The five components, and what each one does |
| Two records describe one piece of work | Activity records and host results |
| The two flows administrators operate | Desired state out, observed state in |
| Terms you will encounter | Fleets and teams, reports and queries |
| Three ways to get at it | Reading the record: in Fleet, by webhook, or streamed |

The test: read the heading with no surrounding text and ask what the section is about. If the
answer is "something to do with the chapter", rewrite it.

A heading that states a finding is fine when the finding **is** the subject, as in "Read-only
is not the same as harmless" or "Fleet supports exactly one database writer". The failure is
abstraction, not assertion.

**Renaming a heading breaks every anchor into it.** Run `python3 build/check-links.py` after
any heading change.

## 23. No meta-commentary about the writing

The reader does not need to be told why a table is a table, that a comparison deserves one, or
that the prose is about to hand off to a diagram. Cut anything that describes the document
rather than the product: "this is a genuine comparison, so it earns a table", "with that story
in mind, the reference version", "one caption is enough here".

The same goes for announcing what is coming. **One exception**, and it is a real one: say so
when you are deliberately holding something back, so the reader knows the gap is intentional
and where it gets filled. "The exact flag list is in `a.7`" is useful. "We will look at
identity later" is not.

## 24. Two sentence patterns to delete on sight

**Jake's rule, 2026-08-25.** Both of these are conspicuous machine-writing tells. Both survive
review easily because each individual instance reads fine. The damage is cumulative.

### The lesson sentence

A sentence whose only job is to tell the reader that the fact next to it was important.

> That order is the point.
> The distinction worth internalising is that ...
> That last item is the one people skip, and it is the one that matters most.
> This deserves reading twice.

Delete it and let the fact stand. If the fact needs an announcement to register, the fact is
underwritten and the fix is upstream. If it does not, the announcement is padding that also
sounds automated.

**Test.** Cover the sentence. Does the paragraph lose any information? If not, it goes.

### Definition by denial

Defining something by first denying an adjacent thing the reader never proposed.

> This is an operational choice, not a feature choice.
> This is not a rehearsal. It is the first real deployment.
> Not a server. A set of standing obligations.
> This sounds like bureaucracy and is not.
> It is not a criticism of the module.

The tell is that the "not B" half carries no information. B was invented to give A something to
push against, and the reader was never going to think B in the first place. Say A.

**This is not a ban on contrast.** A contrast is legitimate when both halves name real things
the reader could actually encounter or choose between, and the denied half carries information:

> Fleet sends the wipe command rather than the delete command, because delete expires after
> thirty days.
> Linux hosts encrypt escrowed data with the server private key; Windows hosts use the WSTEP
> certificate.

Both of those lose something real if you cut the second half. "This is not a rehearsal" loses
nothing.

**Test.** Ask whether a reasonable reader would have believed B before you denied it. If not,
B is a foil. Cut it and keep A.

### Related forms worth catching in the same pass

- "It is worth stating plainly that ..." leading into an ordinary statement
- "not just B, but A", where B is a strawman
- "This is not X, it is Y" as a section's opening move
- Any paragraph that opens by characterising the sentence it is about to deliver

## 25. Claims about the reader's organization

**Jake's rule, 2026-08-25.** The manual can state what Fleet does, because that is verifiable at
the tag. It cannot state what your company is like, what most companies are like, or what will
happen to you eighteen months from now. When it does, it is inventing field experience it does
not have, and the invention is audible.

> Both are cheap to settle now and awkward to unpick once a few thousand devices are enrolled
> and a support team has built habits around them.
> There are two ways to run Fleet, and for most organizations the choice is made for them.
> Your identity provider was almost certainly chosen years ago by someone else.
> That is the destination most organizations want.
> A consequence people miss.
> The failure mode this prevents is the common one where ...

None of that is checkable. "A few thousand devices" is a number with no source. "Most
organizations" has no survey behind it. The reader's support team may not exist.

**Test.** Ask what would have to be true for the sentence to be verified, and whether this book
could verify it. A statement about Fleet can be checked against the release. A statement about
what most teams do cannot be checked against anything.

### What to write instead

Replace the assumed experience with the verified consequence, which is almost always both
shorter and stronger:

> ~~Changing this later is painful once you are at scale.~~
> Changing the server URL after Apple devices have MDM turned on requires an end user to turn
> MDM off and back on, per device, by hand.

The second sentence does everything the first was reaching for, and it is true.

### The exception, and it is a real one

**Jake has this experience and the book is his.** A claim drawn from actual field work is
legitimate and is often the most valuable thing on the page. The rule is about who is speaking.
Write those claims so they own their source, and do not manufacture new ones to match the tone:

> In deployments I have seen, the renewal calendar is the first thing to lapse.

If a passage needs a claim like that and Jake has not made it, leave the gap and flag it rather
than filling it with a plausible-sounding generalization.

### Related forms

- "in practice", "in the real world", "more often than not", used to introduce an unsourced claim
- Invented failure scenes: "usually at 2am", "you will find out on a Tuesday"
- "nobody", "everyone", "people", used as a demographic rather than about a specific mechanism.
  "A Fleet with no global admin has nobody who can create one" is a product fact and is fine.
  "A layer nobody on the team wants to operate" is a guess about the reader's team.

## 26. If you state a count, make the items findable

**Jake's rule, 2026-08-25.** Announcing "Fleet has six roles" or "three named exceptions" is a
promise that the reader can locate each one. Deliver on it.

A numbered list is the right answer when the items are a closed set of named things the reader
will refer to individually, as with Fleet's six roles. Bold lead-in paragraphs are equally good
when each item needs a few sentences of its own, as with the three reasons for external log
delivery. Either satisfies the rule, because either makes item three findable at a glance.

What fails is announcing a count and then running the items together in a paragraph:

> ... with three named exceptions.
>
> Experimental features can change, and they are tagged as such in the API documentation.
> Security fixes may break compatibility when there is no alternative. And default values
> occasionally change ...

The reader now has to parse the count back out of the prose. Enumerate, or drop the count and
write the paragraph as ordinary prose.

**This does not reopen §12.** A numbered list of named things is not a table, and this rule is
not a licence to fragment explanation into bullets. The de-tabling pass was about data that
should have been prose; a catalogue with a stated count is a list.

### The same discipline applies to a stated path

**Added 2026-08-27, after one table row was wrong in three different ways across three review
rounds.**

8.2's Orbit-root inventory gave the osqueryd binary as `bin/osqueryd/<os>/<channel>/osqueryd`.
That path exists on no platform. Corrected once, it still said "the last two segments differ by
platform" when the platform token itself differs. Corrected again, it omitted the ARM64 variants,
so two of the five real paths were unaccounted for.

The failure is not carelessness about osqueryd. **A path in a table reads as a fact and is
actually a template**, and a template is wrong until every variable in it is enumerated. The
reader cannot tell which parts are literal, so a path with an unstated variable sends them looking
for a directory that is not there, in the middle of whatever went wrong.

**So: if a path contains a placeholder, enumerate every value it takes, or give the real paths
instead of the template.** The same goes for a command with a platform-dependent flag and a table
name with a suffix. If the list is too long to enumerate, that is a signal the table cell is the
wrong home for it.

## 27. What a citation ledger has to separate

**Written 2026-08-25, after an external review found a material defect in every one of the twelve
Part II chapters.** Each chapter had a citation ledger and had been verified against the release
tag. The process was followed and it did not work. This section records why.

### The ledgers recorded sourcing and could not record reasoning

A row saying "claim X, source `file.go:123`, confidence high" is true and insufficient. It does
not say whether X is *what the source states* or *what was concluded from it*, and the majority of
the defects were the second kind:

| Written | Source said | Gap |
|---|---|---|
| GCP is not highly available | The sizing table lists `Nodes: 1` | One HA instance is one node |
| Neither carves nor installers survive a second instance | Carves fall back to MySQL, installers to local disk | MySQL is shared |
| Technician can do this and nothing else | The role's *write* permissions | Its read permissions are much wider |
| Nothing is replayed | Plugins drop oversized records | Write failures are retried |

Every one is a correct reading followed by a wrong inference. Confidence was recorded as high
because the source really did say what it was quoted as saying.

**Every ledger row now carries one of three bases.** Borrowed from an external reviewer that
caught what this process missed:

- **Stated** — the source says this. Quote or cite it precisely.
- **Derived** — the book concluded this from what the source says. Give the reasoning, not just
  the source, so a reader can check the step and not just the citation.
- **Unverified** — could not be established at the tag. Say so in the chapter too (§8).

A derived row is not weaker than a stated one. Some of the best material in this book is derived.
But it is a different kind of claim and it fails in a different way, so it has to be visible as
one.

### Headings and tables are claims, and were never checked

Two defects had correct prose under an incorrect heading, or correct prose beside a table cell
that overstated it. Per-claim verification is structurally blind to this, because the verified
claim is the one in the paragraph.

**Check every heading, table cell and summary line against the text it summarises**, as a
separate pass. Ask what the heading asserts on its own, to someone skimming, and whether the
paragraph supports exactly that.

### "Stated" is a claim about scope, not just about content

**Added 2026-08-25, after the rule above failed on the chapter written to test it.**

A ledger row read: *the retry is limited to three consecutive attempts followed by a 24 hour
cooldown*, filed as **stated**, citing `retry.NewLimitedWithCooldown(3, 24*time.Hour)`.

That line does say three, and it does say 24 hours. What it does not say is **per what**. The
retries turned out to be tracked per artifact hash, one file away, which changes the operational
meaning completely: a host failing on one download is not silenced for everything else, and a
corrected build is not held by the old one's cooldown.

The row was cited correctly and was still wrong, because citing a line establishes its content
and not its scope.

**So a row is only `stated` when the cited source establishes the claim's boundaries as well as
its substance.** Ask what the claim quietly asserts about *when*, *where*, *to whom* and *per
what*, and whether the citation covers each. If it covers the number but not the unit, the row is
**derived**, and the derivation is the part worth writing down.

### A `stated` row cites Fleet, not this manual

**Added 2026-08-27, after a first review found a chapter's organising claim inverted.**

3.2 said Fleet delivers fleetd on the ADE path and that manual enrollments need a package
delivered by hand. Fleet sends the same agent-install command after **both**, and only ADE has an
opt-out. The chapter had it backwards on both halves, and its decision table was built on it.

The ledger shows how it got in. The row sat under **stated**, and its source column read: *"Re-verified with 8.1, 8.4 and 8.8, and `fleetdm/fleet#47793`."* That is not a source. It cites this
manual's own prior belief, held in three chapters that had all inherited the same assumption, plus
an issue title. A claim can be re-verified across four documents that never checked it and end up
looking better cited than one read straight out of the server's source.

**A `stated` row cites Fleet's source at the tag, and nothing else.** Not another chapter, not a
ledger, not an issue, not this manual at an earlier date. Agreement with a neighbouring chapter is
worth recording, but it is consistency and not verification, and it belongs in the prose or under
**derived** where the reasoning is visible.

The asymmetry is the point. `claims.py` finds chapters that **disagree**. Nothing finds chapters
that agree with each other and are all wrong together, and that is precisely what a chain of
"re-verified with" citations manufactures.

The same failure has a ledger-scale version. That ledger also asserted *"No claim in this chapter
is unverified."* Asserting completeness is itself a claim, and it required having read the
adjacent material, which had not happened. **A ledger can overstate its own coverage exactly as a
chapter can overstate a fact.** Say what was checked; do not certify what was not.

### Nothing checked a chapter against itself

Two chapters contradicted themselves: one said a setting was per-token and later per-platform
"not per token"; another told the same reader both to verify a domain and that they need not.
Both halves had been verified in isolation. Consistency is not a property of any single claim, so
no per-claim process can see it.

**Read the finished chapter once, whole, looking only for passages that disagree with each
other.** This is the cheapest of the three checks and it caught nothing for twelve chapters
because it was never performed.

**And read it against the book, not only against itself.** Added 2026-08-25: a chapter written
under this rule still contradicted a different chapter of the same manual. 3.1 stated that an
enroll secret determines where a host lands, which is true on the fleetd path; 2.10 had already
documented that automatic Apple enrollment places hosts by a default fleet on the Apple Business
token instead. Both chapters were internally consistent and the book was not.

A within-chapter read cannot see this by construction. Any chapter that generalizes, and any
chapter whose scope line says words like *any*, *every*, *all* or *common to*, needs its general
claims checked against what the book already says elsewhere. `build/check-crossrefs.py` catches
the case where a reference names a target that does not support it; it does not catch two
chapters quietly disagreeing, and nothing mechanical currently does.

### And a note on where these came from

An independent reviewer found all of it, working from its own briefing and explicitly not from
this style guide. The lesson is not that review is useful, which is obvious. It is that a
verification process can be followed correctly and still be blind in a specific, describable
direction, and that the blindness is invisible from inside the process. Build the checks that
look where you do not.

## 28. The announce-then-correct rhythm, and qualification stacks

**Jake's rule, 2026-09-03. The systemic one.** Across five review rounds the most consistent
machine-writing tell in this book was not a phrase, as in §24, but a rhythm, repeated until the
page had a texture. Each instance passes review because each instance is defensible. The damage
is cumulative: a reader feels the pattern well before they can name it, and what they feel is
"written by a model." The two shapes below are the dominant ones, and this rule names them so a
pass can be run against them directly.

### The bold-led announce-then-correct paragraph

A paragraph that opens with a bold claim, states it, then immediately swerves into a corrective
contrast that qualifies or reverses it. The bold lead announces; the clause after it walks the
announcement back, which is the tell: the bold sentence was written in order to be corrected, so
the correction is the real content and the announcement is scaffolding.

> **X is not the same as Y.** In most cases it only does A, but ...
> **Both of them work.** What is genuinely missing is narrower than it looks ...
> **This one path is the exception.** That is the platform's constraint rather than Fleet's ...

One is fine. As the default shape for section after section it becomes a tic, and it is
measurable in this book: bold lead-ins run at about one visible line in seven, and the word
*worth* ("worth knowing", "worth being precise about") appears in the hundreds, standing in for a
claim the sentence does not otherwise carry.

Write the load-bearing sentence first. If the correction is the point, lead with it and drop the
setup. Keep a bold lead-in only where it labels a real list item (§26) or a branch the reader
chooses between, never as a way to pre-announce the sentence you are about to deliver (see §24's
related forms, which catch the same move at sentence scale).

**Test.** Over a run of paragraphs, count how many open with bold text and how many of those
openers are then qualified by the sentence after them. If most of a section is this shape, most
of it is rhythm rather than structure. Rewrite until each bold marks something a reader navigates
by, not something the paragraph immediately takes back.

### The qualification stack

A single sentence, or an unbroken paragraph, that hangs qualifier on qualifier until the thing
the reader came to decide is buried among the clauses.

> The binary carries an embedded schema and serves it immediately, then attempts a background
> refresh about two seconds after startup and every 24 hours thereafter by default, replacing the
> in-memory copy only on a successful fetch and keeping the previous one when a fetch fails.

Every clause is true and the whole is exhausting, because several facts arrive in one breath with
no ranking. The reader cannot tell which clause they act on and which is reassurance they can
skim.

Find the one thing the reader does with the paragraph and lead with it. Promote the qualifiers
that survive into their own sentences, and cut the ones that were only there for completeness
(§20). A fact that needs three subordinate clauses to be stated safely is usually two facts
wearing one sentence.

**Test.** Read the sentence aloud. If you run out of breath before the main verb reaches its
object, or you cannot say in one clause what the reader is meant to do, it is a stack. Break it.
