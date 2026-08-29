# Part IX structure: what an appendix in this book is for

Agreed with the independent reviewer on 2026-08-28, in two rounds. Round one came back CHANGES
REQUIRED with five conditions; round two settled all five and returned AGREED. Both transcripts are
at `../missing-fleet-manual-private/reviews/2026-08-28/appendices/`.

This file governs all eight appendices. Read it before drafting any of them, and before accepting a
review finding that contradicts it.

## The rule that generates everything else

**Enumerate the manual's own stable synthesis. Model and link the volatile product surfaces Fleet
already enumerates.**

An appendix earns exhaustive treatment when its value comes from joining facts Fleet leaves
scattered. It does not earn it by copying a generated reference, which will be wrong at the next
release and which this project has already caught being wrong three times in one file.

a.8 was written to this rule before the rule existed, which is why it is the model: it carries the
authentication classes, the versioning scheme and the exposure matrix, and it refuses to reproduce
request bodies and response schemas.

## The eight, and what each one claims

| | Organising claim |
|---|---|
| **a.1 Capability index** | Every administrator outcome covered by the manual has one canonical home, even when several platforms and interfaces can achieve it |
| **a.2 Platform capability matrix** | Platform support is a per-capability contract, not a property of an operating system as a whole |
| **a.3 Configuration sources, scopes, and precedence** | Fleet configuration comes from several independently scoped authorities, so correctness depends on knowing which authority owns a value and how collisions are resolved |
| **a.4 Roles and permissions matrix** | Authorisation is the intersection of action, role and scope. Licensing, platform support and interface availability are separate gates |
| **a.5 Action-to-interface index** | Fleet's interfaces overlap but are not interchangeable, and each administrative action has a specific set of supported control surfaces |
| **a.6 Terminology and version boundaries** | Compatibility means translating between current names, legacy names and version floors, not maintaining a second feature catalogue |
| **a.7 fleetctl command index and behaviour** | `fleetctl` is a set of operator requests whose contract is what each command asks Fleet to do and what its result proves, not a transcription of `--help` |
| **a.8 API access, versioning, and exposure** | Fleet's request surface is a set of callers, not a list of endpoints: five that share a credential Fleet's authenticator understands, and a residue that must be read route by route |

Five were retitled on 2026-08-28 to match those claims. **Titles changed in frontmatter only.** The
filenames carry 28 live cross-references and renaming them buys nothing a title does not.

## Where the enumeration line falls, per appendix

| | Enumerate in full | Model and point at | Do not attempt |
|---|---|---|---|
| **a.1** | Every outcome the manual teaches, with the synonyms administrators actually search for, and one canonical chapter each | The outcome taxonomy, and links to a.2 and a.5 where platform or interface changes the answer | Capability support, licensing, procedures, or a prose duplicate of the table of contents |
| **a.2** | Every device-facing capability in the register, across separate platform columns, with plan gates and prerequisites where they change the cell | Delivery mechanism and exceptional conditions. Point to feature chapters for behaviour and a.6 for version floors | Every OS version, device subtype, setting or command. **Never infer one platform from another** |
| **a.3** | Every configuration authority, scope, ownership boundary, precedence rule, and every verified exception to those rules | Startup configuration against stored product configuration against delivered device configuration | Every setting and every default. Do not copy the configuration reference |
| **a.4** | Every administrator-visible action family against all six roles at both scopes, distinguishing read, change, execute, delete and secret-bearing access where those are separate decisions | The authorisation model and service-identity inheritance. Point to a.2 for plan and platform, a.5 for interfaces | Endpoint-by-endpoint authorisation, UI controls, or licensing folded into permission cells |
| **a.5** | Every action in the register against UI, REST API, `fleetctl` and GitOps, using full, partial, read-only, unsupported and not established rather than ticks | Why partial interfaces differ, and where their detailed reference lives | Every button, endpoint, flag or YAML field |
| **a.7** | Every public command and leaf subcommand in the 4.90.1 command tree, with purpose, authentication, scope, required permission, destructive character, synchronous or asynchronous behaviour, and the chapter that explains the workflow | Authentication and config resolution, output and exit semantics, high-risk option families. Point to the installed client's help for exact syntax | Full flag tables, exhaustive examples, or a command-to-API cross-reference |

## The shared capability register

**a.1, a.2, a.4 and a.5 are four projections of one register.** Authored independently they will
duplicate each other and then drift apart, which is this project's dominant defect class operating
at the scale of a whole part. The register lives at
`../missing-fleet-manual-private/research/capability-register.md` and is research infrastructure
rather than a ninth appendix.

**Granularity, which is the whole risk.** A row is the finest grain at which any declared dimension
gives a different answer: platform, role and scope, interface, licence, prerequisite, version.
**Split any candidate row the moment one of them disagrees within it.** Do not split one where they
all agree — with one refinement the reviewer added: never merge two semantically distinct
administrator intents just because their vectors happen to coincide. A row exists because it is a
distinct intent *or* a distinct contract.

The rule is not a preference. An early chapter said Linux has no lock and no wipe, because the row
was "lock and wipe" and the answer had been read off the MDM channel. Fleet does both on Linux, as
scripts, on Premium. **The coarse row produced a confident wrong cell that survived drafting and a
review.**

**The stopping condition is a fixed point, not a row count.** The register is finished for 4.90.1
when every administrator-visible action the manual teaches or promises is mapped; every product
action discovered in research is included, excluded with a recorded reason, or mapped as a synonym;
further research produces no row whose contents disagree on any declared dimension; and every row
has complete projections with no blank cells except an explicit `Not established`.

## The evidence rule for tables

Part VII is held to a four-class evidence rule because its claims are mostly operational. The
appendices need a different one, because **a table hides its evidence in a way prose does not**: a
cell saying "Premium" looks identical whether it was read out of a validator or assumed from a
neighbouring feature. Licence claims are the least reliable claim class in this project, seven wrong
in a single day, and a.2 and a.4 are largely licence and capability claims.

Every factual cell resolves to evidence in one of these classes:

| Class | Means |
|---|---|
| **Product contract, tag checked** | Tagged source: an authorisation check, a validator, a test, a registered configuration, a command declaration |
| **Published reference, release locked** | Documentation or release material where that is genuinely the contract. **It cannot overrule tagged implementation behaviour** |
| **Platform or vendor contract** | An exact vendor source with its version |
| **Manual navigation** | A link to the canonical chapter, making no new product claim |
| **Derived synthesis** | An explicit conclusion from cited facts |
| **Not established** | The sources do not settle it |

**A cell needs its own atomic claim when it is negative or exclusive, licence-gated, conditional or
partial, differs from its row's dominant answer, or introduces a distinct scope, prerequisite or
version boundary.** Everything else may ride a row-level claim, and only when the cited evidence
explicitly establishes every cell in that row. Proximity is not evidence and inference is not
evidence.

Claims are atomic and reusable: four facts in one cell need four claim identities, and those claims
may support other cells wherever their stated scope genuinely covers them.

Enforcement, all of it non-negotiable:

- **No blank cells.** `Not applicable` or `Not established`, and a `Not established` needs its own
  record of what was searched.
- **Negative and exclusive claims need positive evidence of the boundary.** Absence from one
  interface is not evidence of absence.
- **Every Free or Premium claim is checked against the validator or test for that exact capability,
  platform and scope.** No inheritance from a neighbouring feature.
- **Permission cells need the authorisation path or its tests**, not role documentation.
- **A correction creates a new claim** and inherits none of the original's checking.

**A ledger larger than the appendix it documents is an acceptable and likely outcome.** It signals
evidence density rather than too many rows. Reduce rows only where they lack a distinct intent or a
divergent behaviour, never to shorten the ledger.

## The three rounds do three different jobs

The owner set three review rounds per appendix on 2026-08-28, up from the single round the body
chapters got. They are not three passes of the same review:

1. **Coverage.** Taxonomy, boundaries, missing actions, and whether the appendix is answering its
   organising claim.
2. **A cell-by-cell evidence audit**, weighted to permissions, licence gates, defaults and every
   negative claim.
3. **A fresh whole-appendix read**, plus cross-appendix consistency against the register and against
   the promises live in the chapters.

**Every round reads the whole appendix, not the diff.** This project's evidence is that a correction
is the most reliable way to introduce the next defect, and the diff is exactly the view that hides
it.

## Writing order, and why

1. **a.3** establishes configuration ownership and precedence.
2. **a.4** is the authorisation projection of the register.
3. **a.7** establishes the command inventory and semantics.
4. **a.8** takes its retitle and its three rounds.
5. **a.6** is re-scoped and completed.
6. **a.2** uses the register and a.6's version boundaries.
7. **a.5** depends on a.3, a.4, a.7 and a.8 to classify an interface without guessing.
8. **a.1** is authored last, from the finished register and the final chapter anchors.

a.2 and a.5 do not depend on each other, but both must use identical capability IDs. a.1 depends on
both, because it is the reader-facing projection of what they establish.

## Four rulings worth keeping where they can be found

**a.1 is the synonym layer, and nothing else.** Held to "every outcome with its canonical chapter"
it would duplicate the table of contents. What it adds is translation: the table of contents exposes
only *this book's* vocabulary, and a.1 maps the reader's vocabulary onto it. The failure it prevents
is landing on an incidental mention, or finding nothing, because the administrator's word for a
thing is not the word this book chose. Keep it small and organised around what people search for.

**a.5 keeps four operator surfaces and gains a second table.** The reviewer's first position was to
drop automation as a catch-all column, which would have made a.5 wrong by omission: policy
automations, webhooks, schedules and integrations cause actions no operator invoked, and a reader
told there are four surfaces has a false inventory. It changed position. The matrix stays at UI,
REST API, `fleetctl` and GitOps, and **a separate short table answers a different question** —
which actions can be initiated by Fleet itself or by an external system — reusing the action IDs and
recording the initiator, the triggering mechanism, the resulting action and the material gates. Not
a fifth operator interface, and not a vendor catalogue.

**a.7's inventory comes from the tagged source command tree**, because no `fleetctl` binary
trustworthy as 4.90.1 was available. Follow the assembled root command tree rather than searching
command files, and account for aliases, hidden and deprecated status, generated registrations and
build constraints. **The appendix says plainly where the inventory came from and why.**

**a.6 loses two sections and gains one.** Feature availability moves to a.2, where a claim can be
qualified by platform and scope. Documentation maintenance leaves the published manual entirely; it
is contributor material and it was a third empty section in a chapter whose own introduction admits
to two. Version boundaries gets filled, with cross-cutting floors only. The glossary's selection
rule is already right and does not become a dictionary: include a term whose competing meanings or
names would otherwise make an administrator act or search incorrectly.
