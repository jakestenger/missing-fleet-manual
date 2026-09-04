# Outline — The Missing Fleet Manual

**Table of contents and the binding filename registry.**

**The 2026-08-23 design is authoritative.** Where it and the older metadata disagree on
structure, organization, or voice, the design wins. It does **not** override source
verification: product claims are still checked against the release, and corrected where the
product disagrees (Jake's call, 2026-08-23).

Restructured 2026-08-23 to the ten-part shape. Sections get added when a question has no home; nothing gets cut for being
covered by the official docs, because of the airplane test (`STYLE.md` §1).

## Status legend

Judge status by **evidence, not by frontmatter**. The reorganization rewrote every
`status:` field, so a fully written and source-verified Part VIII section currently reads
`status: drafting` alongside a 29-line stub. Until that is repaired, use this:

| Mark | Meaning | Evidence |
|---|---|---|
| ○ | outline | headings only, roughly 29 lines, no prose |
| ◐ | drafting | prose started, incomplete |
| ● | written | complete prose, reads start to finish |
| ✔ | verified | written **and** checked against a release tag, with a citation ledger in `research/section-notes/` |

**Current state, 2026-08-24.** Part I and the Part II chapters now numbered 2.1 and 2.5 to 2.8 are ✔ verified against tag
`fleet-v4.90.1`, each with a ledger in `research/section-notes/`. Part VIII is ● written and
was checked against Fleet 4.90.0, so its re-verification at the tag is still outstanding and
it does not yet qualify. Everything else is ○ or ◐. See `STYLE.md` §9.

**Priority** is based on **hidden machinery** — how much Fleet does behind the scenes, how
many edge cases and precedence rules there are, and how often customers ask "but how does
it actually work?"

★★★ deep machinery, rich edge cases · ★★ moderate · ★ mostly surface, still written

---

## Part 0 — Introduction

`manual/00-Introduction/`

| # | Section | File | Pri | Status |
|---|---|---|---|---|
| 0.1 | How to use this manual | `0.1-how-to-use-this-manual.md` | ★ | ◐ |

## Part I — Foundations

`manual/01-foundations/`

How Fleet is put together, and the vocabulary the rest of the book assumes.

| # | Section | File | Pri | Status |
|---|---|---|---|---|
| 1.1 | What Fleet is | `1.1-what-fleet-is.md` | ★★★ | ◐ |
| 1.2 | How Fleet reaches a device | `1.2-how-fleet-reaches-a-device.md` | ★★★ | ◐ **salvage available** |
| 1.3 | Hosts, fleets, labels, and targeting | `1.3-hosts-fleets-labels.md` | ★★★ | ◐ **salvage available** |
| 1.4 | Identity and roles | `1.4-identity-and-roles.md` | ★★ | ◐ |
| 1.5 | Audit and activity | `1.5-audit-and-activity.md` | ★★ | ◐ |
| 1.6 | The Fleet server | `1.6-the-fleet-server.md` | ★★ | ◐ **salvage available** |

### Foundations decisions (2026-08-23, authoritative)

Concepts to keep separate. Blurring these is the specific failure this chapter split
exists to prevent.

- **Fleets are durable configuration and administrative boundaries.**
- **Labels are flexible selections.** Global labels can cross fleets; fleet labels stay
  within their fleet. *(Verify at 4.90.0 before writing — see the note on verification at
  the top of this file.)*
- **Global and fleet-scoped configuration work together**, rather than one overriding the
  other as a blanket rule. The precedence detail belongs in `a.3`.
- **Fleet-level roles** let a team, such as computer-lab staff, administer only its own
  fleet without reaching others.
- **Identity/roles (1.4) and audit/activity (1.5) are separate chapters.** They were
  previously entangled.
- **1.6 explains relationships**, not internals: the Fleet server, administrators and
  automation, fleetd hosts, MDM-managed devices, MySQL, Redis, and object storage.

Per `STYLE.md` §18, Part I owns the *mental model* for each of these. Organization-wide
setup lives in Part II, and targeting in practice lives in 5.1. Those chapters link here
rather than restating.

**Salvage, resolved.** Three Part I chapters were overwritten during the 2026-08-23
reorganization and recovered from the rendered site. All three were merged back on
2026-08-24 and the recovered copies are no longer needed.


## Part II — Administer and deploy Fleet

`manual/02-administer-and-deploy-fleet/`

Standing up and configuring the server itself. Everything here is done once, by an
administrator, before devices arrive.

| # | Section | File | Pri | Status |
|---|---|---|---|---|
| 2.1 | Administration model and deployment choices | `2.1-administration-model-and-deployment-choices.md` | ★★ | ◐ |
| 2.2 | Self-hosting architecture and capacity | `2.2-self-hosting-architecture-and-capacity.md` | ★★ | ○ |
| 2.3 | Deploy on AWS or GCP | `2.3-deploy-on-aws-or-gcp.md` | ★★ | ○ |
| 2.4 | Deploy with containers or virtual machines | `2.4-deploy-with-containers-or-virtual-machines.md` | ★★ | ○ |
| 2.5 | Identity providers, SSO, SCIM, and role sync | `2.5-identity-providers-sso-scim-and-role-sync.md` | ★★★ | ◐ |
| 2.6 | User accounts, roles, and service identities | `2.6-user-accounts-roles-and-service-identities.md` | ★★ | ◐ |
| 2.7 | Organization and server settings | `2.7-organization-and-server-settings.md` | ★★ | ◐ |
| 2.8 | Activity, audit logs, and log delivery | `2.8-activity-audit-logs-and-log-delivery.md` | ★★ | ◐ |
| 2.9 | MDM architecture and foundations | `2.9-mdm-architecture-and-foundations.md` | ★★★ | ◐ |
| 2.10 | Apple MDM configuration | `2.10-apple-mdm-configuration.md` | ★★★ | ○ |
| 2.11 | Configure Windows management | `2.11-configure-windows-management.md` | ★★★ | ○ |
| 2.12 | Bind Android Enterprise | `2.12-bind-android-enterprise.md` | ★★★ | ○ |
| 2.13 | Connect certificate authorities | `2.13-connect-certificate-authorities.md` | ★★★ | ◐ |

## Part III — Connect devices

`manual/03-connect-devices/`

| # | Section | File | Pri | Status |
|---|---|---|---|---|
| 3.1 | Enrollment design and host lifecycle | `3.1-enrollment-design-and-host-lifecycle.md` | ★★★ | ○ |
| 3.2 | Enroll macOS devices | `3.2-enroll-macos-devices.md` | ★★★ | ○ |
| 3.3 | Enroll Windows devices | `3.3-enroll-windows-devices.md` | ★★★ | ○ |
| 3.4 | Enroll Linux devices | `3.4-enroll-linux-devices.md` | ★★ | ○ |
| 3.5 | Enroll iOS and iPadOS devices | `3.5-enroll-ios-and-ipados-devices.md` | ★★ | ○ |
| 3.6 | Enroll Android devices | `3.6-enroll-android-devices.md` | ★★ | ○ |
| 3.7 | Enroll ChromeOS devices | `3.7-enroll-chromeos-devices.md` | ★★ | ○ |
| 3.8 | Manage fleetd, Orbit, and updates | `3.8-manage-fleetd-orbit-and-updates.md` | ★★★ | ○ |

## Part IV — Know your devices

`manual/04-know-your-devices/`

Reading state off devices: inventory, queries, policies, vulnerabilities.

| # | Section | File | Pri | Status |
|---|---|---|---|---|
| 4.1 | Understand hosts, vitals, and inventory | `4.1-understand-hosts-vitals-and-inventory.md` | ★★ | ○ |
| 4.2 | Run queries and reports | `4.2-run-queries-and-reports.md` | ★★★ | ○ |
| 4.3 | Use policies for compliance | `4.3-use-policies-for-compliance.md` | ★★★ | ○ |
| 4.4 | Understand software and vulnerabilities | `4.4-understand-software-and-vulnerabilities.md` | ★★★ | ○ |
| 4.5 | Monitor fleet-wide state | `4.5-monitor-fleet-wide-state.md` | ★★ | ○ |
| 4.6 | Advanced osquery: queries and tables | `4.6-advanced-osquery-queries-and-tables.md` | ★★ | ○ |
| 4.7 | Advanced osquery: custom tables and plugins | `4.7-extend-osquery-with-custom-tables-and-plugins.md` | ★ | ○ |

## Part V — Manage devices

`manual/05-manage-devices/`

Changing state on devices: profiles, scripts, software, remediation.

| # | Section | File | Pri | Status |
|---|---|---|---|---|
| 5.1 | Plan, target, and govern device changes | `5.1-plan-target-and-govern-device-changes.md` | ★★★ | ○ |
| 5.2 | Manage configuration profiles and declarative settings | `5.2-manage-configuration-profiles-and-declarative-settings.md` | ★★★ | ○ |
| 5.3 | Run and manage scripts | `5.3-run-and-manage-scripts.md` | ★★ | ○ |
| 5.4 | Manage software and applications | `5.4-manage-software-and-applications.md` | ★★★ | ○ |
| 5.5 | Design setup and self-service experiences | `5.5-design-setup-and-self-service-experiences.md` | ★★★ | ○ |
| 5.6 | Control operating system updates | `5.6-control-operating-system-updates.md` | ★★★ | ○ |
| 5.7 | Control devices and send custom MDM commands | `5.7-control-devices-and-send-mdm-commands.md` | ★★★ | ○ |
| 5.8 | Enforce disk encryption and manage recovery credentials | `5.8-enforce-disk-encryption-and-manage-recovery-credentials.md` | ★★★ | ○ |
| 5.9 | Automate responses to policy failures | `5.9-automate-remediation-with-policies.md` | ★★★ | ○ |

## Part VI — Automate Fleet

`manual/06-automate-fleet/`

| # | Section | File | Pri | Status |
|---|---|---|---|---|
| 6.1 | Automation design and change control | `6.1-automation-design-and-change-control.md` | ★★ | ○ |
| 6.2 | Manage Fleet with GitOps | `6.2-manage-fleet-with-gitops.md` | ★★★ | ○ |
| 6.3 | Use the Fleet REST API | `6.3-use-the-fleet-rest-api.md` | ★★ | ○ |
| 6.4 | Use fleetctl | `6.4-use-fleetctl.md` | ★★ | ○ |
| 6.5 | Integrations, webhooks, and external workflows | `6.5-integrations-webhooks-and-external-workflows.md` | ★★ | ○ |
| 6.6 | Connect an AI assistant to Fleet | `6.6-connect-fleet-to-an-ai-assistant.md` | ★★ | ◐ |

Exhaustive command and endpoint listings belong in `a.7` and `a.8`, not in these sections
(`STYLE.md` §17).

6.6 covers the Fleet MCP server (`cmd/fleet-mcp`), the assistant-facing sibling of 6.5: it exposes
the same REST API 6.3 documents as typed MCP tools. Added 2026-09-01.

## Part VII — Operate Fleet

`manual/07-operate-fleet/`

| # | Section | File | Pri | Status |
|---|---|---|---|---|
| 7.1 | Day-two operations | `7.1-day-two-operations.md` | ★★ | ○ |
| 7.2 | Back up and restore service state | `7.2-back-up-and-restore-service-state.md` | ★★★ | ○ |
| 7.3 | Upgrade Fleet and fleetd | `7.3-upgrade-fleet-and-fleetd.md` | ★★★ | ○ |
| 7.4 | Scale and maintain availability | `7.4-scale-and-maintain-availability.md` | ★★★ | ○ |
| 7.5 | Observe performance and service health | `7.5-observe-performance-and-service-health.md` | ★★★ | ○ |
| 7.6 | Operational security and release maintenance | `7.6-operational-security-and-release-maintenance.md` | ★★ | ○ |
| 7.7 | Production readiness checklist and handoff | `7.7-production-readiness-checklist-and-handoff.md` | ★★ | ○ |
| 7.8 | Retire a Fleet deployment | `7.8-retire-a-fleet-deployment.md` | ★ | ○ |

## Part VIII — Troubleshooting Fleet

`manual/08-troubleshooting/`

The reference chapter, and the only complete part of the book. Every feature chapter's own
troubleshooting section cross-references *into* here by section ID rather than repeating
the material. **Keep these IDs stable** — the cross-references depend on them, and 8.1
links to 8.2 through 8.14.

`STYLE.md` §17 routes reference material to the appendices. **Part VIII is exempt.** It is
a reference chapter, so its tables stay where they are (`STYLE.md` §5).

| # | Section | File | Pri | Status |
|---|---|---|---|---|
| 8.1 | The diagnostic method | `8.1-diagnostic-method.md` | ★★★ | ● |
| 8.2 | The log surfaces | `8.2-log-surfaces.md` | ★★★ | ● |
| 8.3 | Fleet server logs | `8.3-server-logs.md` | ★★★ | ● |
| 8.4 | Host-side investigation | `8.4-host-side-investigation.md` | ★★★ | ● |
| 8.5 | `fleetctl debug` and the debug archive | `8.5-fleetctl-debug.md` | ★★★ | ● |
| 8.6 | Inspecting server state: MySQL and Redis | `8.6-server-state.md` | ★★★ | ● |
| 8.7 | Live query as an introspection tool | `8.7-live-query-introspection.md` | ★★ | ● |
| 8.8 | Apple MDM diagnostics | `8.8-apple-mdm-diagnostics.md` | ★★★ | ● |
| 8.9 | Windows MDM diagnostics | `8.9-windows-mdm-diagnostics.md` | ★★★ | ● |
| 8.10 | Android and AMAPI diagnostics | `8.10-android-diagnostics.md` | ★★ | ● |
| 8.11 | Reproducing and isolating | `8.11-reproducing-and-isolating.md` | ★★★ | ● |
| 8.12 | Audit logs: who did what, when | `8.12-audit-logs.md` | ★★ | ● |
| 8.13 | What to collect before escalating | `8.13-escalation.md` | ★★★ | ● |
| 8.14 | Diagnosing degradation | `8.14-degradation.md` | ★★★ | ● |

Section IDs here are **append-only**. Never renumber.

## Appendices

`manual/09-appendices/`

`STYLE.md` §17 makes these load-bearing rather than optional. Reference material pulled out
of the narrative chapters lands here, so these get written alongside the chapters that feed
them, not at the end.

| # | Section | File | Pri | Status |
|---|---|---|---|---|
| A.1 | Capability index | `a.1-capability-index.md` | ★★ | ○ |
| A.2 | Platform capability matrix | `a.2-platform-capability-matrix.md` | ★★★ | ○ |
| A.3 | Configuration model and precedence | `a.3-configuration-model-and-precedence.md` | ★★★ | ○ |
| A.4 | Roles and permissions matrix | `a.4-roles-and-permissions-matrix.md` | ★★ | ○ |
| A.5 | Interface index (UI, fleetctl, API, GitOps) | `a.5-interface-index.md` | ★★ | ○ |
| A.6 | Glossary and release compatibility | `a.6-glossary-and-release-compatibility.md` | ★★★ | ○ |
| A.7 | fleetctl command reference | `a.7-fleetctl-command-reference.md` | ★★ | ○ |
| A.8 | API action and endpoint reference | `a.8-api-action-and-endpoint-reference.md` | ★★ | ○ |
| A.10 | Subject index (A-Z of concepts and nouns) | `a.10-subject-index.md` | ★★ | ○ |
| A.11 | Fleet MCP tool reference | `a.11-mcp-tool-reference.md` | ★★ | ◐ |

**A.11 (Fleet MCP tool reference) added 2026-09-01** — the argument-level reference for the MCP tools that 6.6 teaches.

**A.9 (Hands-on labs) was removed 2026-09-01** on owner decision to keep this book explanation/reference-only and build a separate labs & exercises compendium later. The ten labs are preserved (with the Lab 6 GitOps dry-run defect corrected) in the private companion repo at `future-labs-book/`. The A.9 slot is left vacant rather than renumbering A.10, pending an owner call on whether to renumber the subject index to close the gap (which would change its published URL).

A.6 is the third layer of the definitions model in `STYLE.md` §14, so every section that
glosses a term inline should be linking to it.

---

## Filename registry (binding)

Sections forward-link to unwritten sections, so paths must be predictable or the links rot.
**These paths are canonical.** A worker writing a section MUST use its registered path, and
may only add to this list, never rename. The renumber of 2026-08-30 was executed under owner
authorisation (whole-book review, P6 structural moves); the registry now reflects the new
numbering, and the no-rename rule resumes from that baseline.

Convention: `manual/NN-part-slug/N.N-section-slug.md`, lowercase, hyphenated. Appendices use
a lowercase `a.N-` prefix. `00-Introduction` is capitalised, inconsistently with the rest;
left alone because renaming it would break links for no reader benefit.

| Part | Directory |
|---|---|
| 0 Introduction | `manual/00-Introduction/` |
| I Foundations | `manual/01-foundations/` |
| II Administer and deploy Fleet | `manual/02-administer-and-deploy-fleet/` |
| III Connect devices | `manual/03-connect-devices/` |
| IV Know your devices | `manual/04-know-your-devices/` |
| V Manage devices | `manual/05-manage-devices/` |
| VI Automate Fleet | `manual/06-automate-fleet/` |
| VII Operate Fleet | `manual/07-operate-fleet/` |
| VIII Troubleshooting | `manual/08-troubleshooting/` |
| Appendices | `manual/09-appendices/` |

Every section file listed in the tables above exists on disk. The registry is the tables;
there is no separate claim list, because there are no unclaimed forward links.

Verify before declaring a section done, from `manual/`:

```sh
grep -rhoE '\]\(\.\./[^)]+\.md\)' . | sed 's/](\.\.\///; s/)$//' | sort -u |
  while read p; do [ -f "$p" ] || echo "BROKEN: $p"; done
```

Last run 2026-08-23: 20 distinct cross-part links, all resolving.

## Structure history

**2026-08-23 — reorganized from eight parts to ten.** The previous shape was
Foundations / Getting devices in / Managing devices / Software / Orchestration and posture /
Identity and integrations / Operating Fleet / Troubleshooting.

What changed and why it was kept:

- **Server administration got its own part (II).** Standing up Fleet was previously
  scattered across old 1.5, old Part VI and old Part VII. It is a distinct audience task.
- **Read and write were separated** into "Know your devices" (IV) and "Manage devices" (V).
  The old Parts III, IV and V mixed reading state with changing it.
- **Software stopped being its own part.** Delivery folded into 5.4 and 5.5, inventory and
  vulnerabilities into 4.4. Software delivery is a way of changing a device, not a category
  beside it.
- **Appendices went from 3 to 8** and became the destination for reference material under
  `STYLE.md` §17.
- **Part VIII was left completely untouched**, including its section IDs.

The reorganization also **rewrote every cross-part link correctly** and added `section:` and
`sidebar_position:` to frontmatter. Both are kept.

What it cost, recorded so the same trade is not made blindly again: it **overwrote the prose
of the three written Part I sections** with outlines, and reset `status:` on all 14 Part VIII
sections. The prose was recovered and is held outside this repository; the status damage is repaired by the evidence-based
legend at the top of this file.

## Prioritisation signal

Keyword mentions across the **entire** `CHANGELOG.md` history. This is churn, not bug
density — it conflates feature development with fixes — so treat it as a rough ordering
hint, not evidence.

| Area | Mentions | Now lives in |
|---|---|---|
| Software / installers / packages | 752 | 5.4, 5.5, 4.4 |
| Queries | 620 | 4.2, 4.6 |
| Enrollment (ADE / Autopilot / DEP) | 457 | 3.1 to 3.7 |
| Policies | 319 | 4.3, 5.7 |
| Profiles / DDM / CSPs | 314 | 5.2 |
| Vulnerabilities / CVEs | 272 | 4.4 |
| GitOps | 240 | 6.2 |
| Scripts | 233 | 5.3 |
| Labels | 199 | 1.3, 5.1 |
| SSO / SCIM / IdP | 165 | 2.5, 1.4 |
| Certificates / SCEP | 146 | 2.10, 5.8 |
| VPP / App Store | 119 | 5.4 |
| Self Service / Fleet Desktop | 115 | 5.5 |
| Webhooks / integrations | 100 | 6.5 |
| Android | 80 | 3.6, 2.12 |
| Disk encryption | 78 | 5.6 |
| Host vitals / inventory | 68 | 4.1 |
| OS updates / patching | 51 | 5.5, 3.8 |

This heuristic is a placeholder. Once the weekly support sweep has a few weeks
of data, hits-per-section replaces it with something real.

## Write order

1. ~~Merge the salvage into 1.2, 1.3 and 1.6.~~ **Done 2026-08-24.**
2. ~~Finish Part I.~~ **Done.** All six chapters written and verified.
3. **Finish Part II.** The chapters now numbered 2.1 and 2.5 to 2.8 are verified; the rest of the part are outlines. In progress on an
   hourly schedule, one chapter per run, each verified at the tag with its own ledger.
4. **Re-verify Part VIII** against tag `fleet-v4.90.1` and move it from ● to ✔. This is the
   largest outstanding debt in the book: fourteen written sections carrying a 4.90.0 stamp.
5. Then by reader demand and the churn table below: 5.4, 4.2, 3.1, 5.2, 6.2.

Appendices are written as their feeder chapters are written, never batched at the end.

## Open outline questions

- ~~Is ~65 sections the right granularity?~~ **Closed 2026-08-23.** The structure is
  authoritative as designed. Revisit only if a chapter proves unwritable at that size.
- ~~Does Part I earn its place?~~ **Resolved 2026-08-19: yes.** A self-contained book that
  survives the airplane test needs its own foundations.
- ~~Do diagnostic methodologies belong inside each section, or in one chapter?~~
  **Resolved 2026-08-19: both.** Part VIII is the reference chapter; each feature chapter
  carries a short pointer into it by section ID.
- ~~Should there be a Part 0?~~ **Resolved 2026-08-23: yes**, it exists as
  `00-Introduction`. Still open: whether 0.1 should be joined by a "decisions that are
  expensive to reverse" section, which was the original motivation.
- ~~Does Part II want splitting?~~ **Closed 2026-08-23.** Part II covers identity, roles,
  organization configuration, audit logs, MDM foundations and self-hosting as one part, by
  design.
- What is N for the version dropdown — how many releases stay live? (`PLATFORM.md`)
