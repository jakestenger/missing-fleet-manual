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
