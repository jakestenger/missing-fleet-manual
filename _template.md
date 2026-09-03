---
title: ""               # quote it; unquoted values with a colon break the build
chapter: ""             # e.g. "V. Manage devices"
section: ""             # e.g. "5.2" — quoted, or YAML reads it as a float
sidebar_position:       # integer, position within the part
verified_against:       # e.g. Fleet 4.90.1 — see the rule below
verified_on:            # YYYY-MM-DD
verified_source:        # e.g. git tag fleet-v4.90.1
further_reading:        # official docs URLs — NOT load-bearing; the section stands alone
feature_requests:       # drives the website's open-FR widget; see PLATFORM.md
  labels: []            #   e.g. [":product", "#g-apple-at-work"]
  match: []             #   e.g. ["VPP", "App Store", "Apps and Books"]
  exclude: []
---

<!--
This template is for the narrative chapters, Parts 0 through VII. Part VIII is a
reference chapter with its own established shape; follow the existing 8.x sections
there, and STYLE.md §12 (reference register).

STATUS VOCABULARY, and the rule that matters:

  outline    headings only, no prose
  drafting   prose started, incomplete
  written    complete prose, reads start to finish, not yet verified
  verified   written AND checked against a release tag, with a citation ledger
             in research/section-notes/<section>.md

The three verified_* fields may be filled ONLY when status is `verified` and that
notes file exists. Do not inherit them from a neighbouring section, and never derive
a version from CHANGELOG.md (STYLE.md §9). The book targets Fleet 4.90.1; that is
the target, not a claim that this section was checked against it.

If the section is unverified, say so rather than leaving the field blank and looking
verified by omission:

  verified_source: unverified — drafted from prior work, not checked at a tag

Sections have twice shipped carrying stamps for verification that never happened.
-->

# {{title}}

> Headings are prompts, not a form. Rename them for the topic, drop what doesn't
> apply, add what does (`STYLE.md` §11). What is **not** optional is the set of
> elements in `STYLE.md` §19.
>
> Read before writing: **§18** (this feature has one canonical home, so is it here or are
> you linking to it?), **§17** (reference material goes to an appendix), **§12** (narrative
> register: model and decision first, not a table first), **§22** (headings name a subject,
> not a conclusion).
>
> Every section opens with a category badge, at the start of its first paragraph:
> `![Explanation](../_assets/icons/explanation.svg)` and likewise `howto`, `reference`,
> `troubleshooting`. See §16.

## Purpose and scope

What this chapter covers and what it deliberately leaves to another chapter. Two or
three sentences.

A reader may have arrived here cold from a search rather than from the previous
chapter, so orient them: what is this, and are they in the right place.

## Vocabulary

Only if this chapter uses a term in a **narrower** sense than the general one, or where
Fleet's word differs from the industry's. `STYLE.md` §14, layer 2.

A term that just means the ordinary thing gets an inline gloss and a link to
`../09-appendices/a.6-glossary-and-release-compatibility.md`. Never define the same term
in two places.

| Term | In this chapter it means |
|---|---|
|  |  |

## The model

**Start here, not with an artifact.** What the administrator needs to hold in their head
before any of the procedure makes sense: what the thing is, what it relates to, and how
Fleet was designed for it to work.

Prose and scenarios, not a grid. A reader cannot learn a relationship from a table
(`STYLE.md` §12).

<!-- DIAGRAM: if the model is a lifecycle, a scope boundary, or an architecture, this is
     where it earns its place. Name every box and arrow label verbatim. STYLE.md §13, §16 -->

## The decision

Rename to fit: "Choosing between X and Y", "Before you start", "Prerequisites".

The choice the administrator actually faces, what each option costs, and what becomes
hard to reverse. If there is no choice, state the prerequisites instead: what must
already be true.

This is the element that makes the chapter useful rather than descriptive.

## How to do it

The procedure. Prefer the GitOps and API surface over UI click-paths (`STYLE.md` §6);
where UI steps are needed, mark them volatile.

**Keep the commands minimal.** The test: would removing this command break the
explanation? If not, it belongs in `a.7` or `a.8` and gets linked from here
(`STYLE.md` §17).

<!-- SCREENSHOT: if this involves the Fleet console, mark the shot here. Name the page,
     the state it should be in, what to crop to, what to highlight. STYLE.md §16 -->

## Platform differences

**Only where they change the administrator's decision.** A difference that changes
nothing they do is trivia; leave it out or send it to `a.2`.

Where the platforms genuinely diverge in what is supported, that is a true comparison and
a table is right.

## Verification and ownership

**The most-skipped element, and the one administrators most need** (`STYLE.md` §19).

How to confirm it actually worked: what to look at, what "good" looks like, and how long
to wait before the absence of a result means something. Then who owns it once it is
running, and what they should watch.

## Edge cases and precedence

The most-asked, least-documented category (`STYLE.md` §4). Where applicable: conflicts and
what wins, ordering guarantees, offline hosts (queued, replayed, or dropped), retry and
idempotency, interruption partway, empty or malformed values, limits and what happens at
the boundary.

Say "not documented; unverified" rather than guessing.

Precedence that spans features belongs in
`../09-appendices/a.3-configuration-model-and-precedence.md`. Keep the rule governing
*this* feature here, and link there for the full model.

## Reference and troubleshooting

Where the exact detail lives, and where to go when it misbehaves. Name what the reader
will find, not just the destination (`STYLE.md` §18).

- Commands: `../09-appendices/a.7-fleetctl-command-reference.md`
- Endpoints: `../09-appendices/a.8-api-action-and-endpoint-reference.md`
- Diagnosis: the relevant Part VIII section, and why that one

**Short. A pointer, not a procedure.** Part VIII owns troubleshooting, both the how-to and
the reference tables (`STYLE.md` §5). Do not reproduce their material.

## Version notes

What changed and in which release. Source: release notes at the tag, not `CHANGELOG.md` on
a branch (`STYLE.md` §9). Record agent versions separately when they differ; Orbit ships on
its own cadence.

<!--
BEFORE MARKING THIS CHAPTER DONE

  - All seven elements of §19 present, including verification and ownership
  - This feature's canonical home is correct: explained here, or linked there   §18
  - Reference material routed to an appendix and linked from here               §17
  - Opens with the model and the decision, not with a table                     §12
  - Diagrams limited to lifecycle, scope, architecture, platform comparison     §13
  - A SCREENSHOT or DIAGRAM brief wherever one helps, with real alt text        §16
  - Unfamiliar terms glossed inline or in Vocabulary, glossary linked           §14
  - No code-level references: no file paths, package names, Go identifiers      §8
  - Positive voice; boundaries framed as design, not as missing features        §15
  - Cross-part links resolve (see the check in OUTLINE.md)
  - No "See also" section; links live in the prose that needs them      §21
  - Every section opens with a category badge                          §16
  - Headings name a subject, not a conclusion                          §22
  - No meta-commentary about the document itself                       §23
  - status: and verified_*: honest, per the rule at the top                     §9
-->
