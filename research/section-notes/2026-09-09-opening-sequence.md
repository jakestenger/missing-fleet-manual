# Opening sequence revision, 2026-09-09

## Editorial decision and scope

Jake asked for a warmer, benefits-led introduction to Fleet, moved ahead of the reading
guide, plus a company introduction explaining its ethos and values. This pass is on
`review/1.1-warmer-voice`, based on the earlier warmer sample at `b6ebcf4`. It is for
review before integration into main.

Both the living 4.91 edition and the frozen 4.90 edition receive this structure:

| Chapter | Responsibility |
|---|---|
| 0.1 Who Fleet is | Company background, values, openness, and participation |
| 0.2 What Fleet is | Everyday administrator and operator outcomes, with light technical context |
| 0.3 How to use this manual | Reading paths, task-to-chapter guidance, indexes, and local preview |
| 0.4 What changed, by release | Existing release ledger, renumbered without changing release facts |
| 1.1 How Fleet works | Existing component, observation, delivery, platform, and system-boundary explanations |

The public STYLE.md now records the opening chapters' purpose and the warmer voice.
Technical completeness still applies across the manual; it does not require every
technical condition to appear in the product overview.

## Public sources for company context

These pages were read on 2026-09-09. This is a dated company profile, shared by both
editions, not a claim about what Fleet's website said at either software release.
The chapter cites public sources directly and paraphrases them concisely.

| Claims | Public source | Treatment |
|---|---|---|
| Company purpose, history, remote staff and contributors, names and meaning of the five values | https://fleetdm.com/handbook/company | Stated company context; no headcounts, customer counts, funding totals, or current executive titles |
| Open-core model, inspectable Premium code, public work and contributions | https://fleetdm.com/handbook/company/why-this-way | Stated approach; source availability is not presented as an open-source licence for every feature |
| Transparency toward people using managed devices | https://fleetdm.com/docs/get-started/why-fleet | Stated intent; no claim that scripts or administrators are technically unable to collect other data |
| Bringing questions to an evaluation and explaining an organization's device-management practices | Editorial guidance | Practical application, not a company service guarantee |

## Product overview evidence

The new overview distills the existing reviewed material at `b6ebcf4`. It adds no new
API, timing, entitlement, automation guarantee, or platform-parity claim. These are
editorial examples and ownership checks, not fresh source-level verification of every
feature. Existing release-specific ledgers remain the evidence for those features.

| Overview subject | Existing technical home |
|---|---|
| Host inventory and freshness | 4.1; retained freshness explanation in 1.1 |
| Queries and reporting | 4.2; report-storage model retained in 1.1 |
| Policies and compliance checks | 4.3 |
| Software inventory and vulnerabilities | 4.4 |
| Targeting a rollout and following its results | 5.1 and Part V feature chapters |
| Software delivery and self-service | 5.4; Fleet Desktop component explanation in 1.1 |
| Scripts and profiles | 5.3 and 5.2 |
| GitOps, API, fleetctl, and integrations | Part VI |
| Hosting and other systems | 2.1; environment-boundary explanation retained in 1.1 |
| Supported platforms and licence limits | Platform paths retained in 1.1; a.2 |

The new-colleague and application-update scenarios are illustrative combinations of
those features. The overview names platform and Free/Premium variation without
reproducing the capability matrix. It does not promise automatic remediation or that
queuing a change proves completion.

The preview procedure moved verbatim from the warmer 1.1 to 0.3 in each edition.
Its existing evidence is in `research/section-notes/1.1-notes.md` and a.7's preview
contract. The 4.91 command keeps `--tag v4.91.0 --preview-config fleet-v4.91.0`; the
4.90 command keeps the corresponding 4.90.0 pins. Both retain `--no-hosts`, the
client-configuration warning, context choice, and separate stop/reset semantics.
The reading guide's suggestion to reset and repeat now makes clear that reset keeps
stored data, matching the procedure it links to.

## One inherited factual inconsistency corrected

During relocation, 1.1's forwarding explanation was found to be broader than 4.2 and
its own a.1 ownership row: it said a query with Automations off sends nothing to the
log destination. This is only the ordinary recognized-query filtering path while
server-wide report storage is enabled.

**Stated in source:** at both `fleet-v4.90.0` (`7c428c6e467d4dd642b0375350eecca7138746d1`)
and `fleet-v4.91.0` (`35fc1c0244907c157a64d05d4ec291c0a3a20e32`),
`server/service/osquery.go:3146-3226`, `SubmitResultLogs` forwards parsed received
results without the Automations filter when query reporting is disabled, and also
forwards unrecognized queries. The ordinary path checks `AutomationsEnabled`.
The revised table, following paragraph, and environment paragraph agree on this.
These are rules for received results; no new claim is made about scheduling queries.

**Inference:** none needed for the filter condition; no live deployment experiment
was performed. This correction was source-checked for both tags; the rest of 1.1
retains its prior release evidence rather than receiving a fabricated full-review stamp.

## Paths, assets, and retained content

- The company introduction becomes `/` (and `/4.90/`), with the reading guide now at
  `/Introduction/0.3-how-to-use-this-manual` in its edition. Existing root bookmarks
  now open the company introduction; the sidebar and chapter navigation expose the guide.
- `1.1-what-fleet-is.md` remains the filename and published path for the technical
  primer, now titled *How Fleet works*. Its former `what-does-fleet-do` anchor remains
  as an HTML alias. Its old preview heading links to the procedure's new home.
- The changelog keeps its published `/Introduction/0.2-changelog` URL through an
  explicit slug, despite its new chapter number and filename.
- The lifecycle figure and accepted prompt move from Foundations into the product
  overview. The asset name stays `1.1-fleet-management-lifecycle.webp` for provenance.
- The accepted Cloud City welcome illustration and brief move from the guide into
  the company introduction. The existing asset filename stays unchanged.
- The guide keeps the reader-route and manual-map figures; neither encodes the changed
  individual Part 0 chapter numbers. The technical primer keeps the environment diagram.
- The authentic Hosts screenshot request moves into the product overview. No screenshot
  was invented or marked accepted.
- The guide, release ledger, capability/command/subject indexes, device-control scope
  reference, outline, current visual briefs manifest, and visual-opportunity inventory
  are updated. Historical research citations retain their original paths and dates.
- Feature explanations, platform table, report-storage conditions, and the component
  definitions remain available in 1.1. Repeated opening summaries and the four-question
  list were replaced by the new overview's concrete narrative.

## Validation

- `npm ci --no-audit --no-fund` and the full two-edition `npm run build` completed successfully.
- All 13 Python checks invoked by the PR workflow returned zero. Source-name/schema
  checks used a local extract of the 4.91 release, not the moving Fleet checkout.
- Link, anchor, and image checks passed for all 85 chapters in each edition.
- Additional heading, outline-deferral, and shrink advisories were reviewed. The
  1.1 shrink is intentional: its preview, lifecycle image/brief, screenshot request,
  and product introduction have new homes. Existing frontmatter source citations
  account for the changed chapters' cross-reference checker flags.
- Compared old and new preview sections byte-for-byte in both editions: unchanged,
  including release pins and fenced commands. The moved lifecycle image is also
  byte-for-byte unchanged in each edition.
- Inspected generated Docusaurus metadata: both editions navigate Who → What → How
  to use → Changelog → How Fleet works. The homepage and preserved technical and
  changelog paths resolve to their intended chapters.
- Checked the standalone review preview's internal chapter and heading links.
- `git diff --check` passed. No new dependencies or website configuration changes.
