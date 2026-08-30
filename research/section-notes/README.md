# Section notes

Two kinds of file live here, and only one of them is in this repository.

**Citation ledgers** (`5.4-notes.md`, `8.2-notes.md`, and so on) stay here. They record what a
chapter claims and on what basis, separating what was source-checked from what was derived and what
remains unverified, plus what was rejected and why.

**Working research notes** for Part V are **not here.** They are at
`missing-fleet-manual-private/research-sensitive/`.

## Why the working notes moved, 2026-08-28

This repository is public. While researching 5.8, whose subject is credentials that decrypt disks,
the independent reviewer set an explicit disclosure line and then found the research notes had
crossed it. A sweep found the same shape in Part V's other notes: several described, in actionable
detail, how to reach credentials or authorization gaps that are **unfixed at this release**.

The chapters themselves are written to the disclosure line and say what an administrator needs:
which roles can reach what, that certain reads are logged or state-changing, and how to handle
credential material. They do not describe the routes. Leaving the routes in the working notes, in a
public repository, would have defeated that with no benefit to any reader.

**No exposure occurred.** The notes were moved while the branch was unpushed, and the affected
commits were purged from history in the same pass.

## The rule

**Research notes inherit the disclosure line of the chapter they support.** They are the easier of
the two to forget, because nobody reviews them as prose. When a chapter's subject is sensitive, keep
its working notes out of this repository and cite them from the ledger instead.

## Renumber map, 2026-08-30

The P6 structural moves (owner-authorised whole-book reorganisation) renumbered the chapters
below. **A ledger follows its chapter**, so every `<section>-notes.md` in this directory is keyed
to the NEW number. **Pass-records and frozen research documents keep their old numbers**:
`2.1-2.5-topup-notes.md`, `de-ai-*.md`, `refocus-pass-notes.md`, `1.3-inheritance-verification.md`,
the dated `research/part*-structure.md` planning documents, and the review outputs in the private
sibling are records of work done against the numbering of their date, and renaming them would
falsify history. This map is the translation for reading any of them.

| Old | New | Chapter (current title) |
|---|---|---|
| 2.2 | 2.5 | Identity providers, SSO, SCIM, and role sync |
| 2.3 | 2.6 | User accounts, roles, and service identities |
| 2.4 | 2.7 | Organization and server settings |
| 2.5 | 2.8 | Activity, audit logs, and log delivery |
| 2.6 | 2.9 | MDM architecture and foundations |
| 2.7 | 2.10 | Apple MDM configuration |
| 2.8 | 2.11 and 2.12 | Split: Configure Windows management, and Bind Android Enterprise |
| 2.9 | 2.2 | Self-hosting architecture and capacity |
| 2.10 | 2.3 | Deploy on AWS or GCP |
| 2.11 | 2.4 | Deploy with containers or virtual machines |
| 2.12 | 7.7 | Production readiness checklist and handoff (moved to Part VII, retitled) |
| 3.6 | 3.6 and 3.7 | Split: Enroll Android devices (keeps 3.6), and Enroll ChromeOS devices |
| 3.7 | 3.8 | Manage fleetd, Orbit, and updates |
| 7.2 | 7.3 | Upgrade Fleet server and coordinate fleetd releases |
| 7.3 | 7.2 and 7.8 | Split: Back up and restore service state (keeps the body), and Retire a Fleet deployment |

4.5 kept its number; only its filename changed, to `4.5-monitor-fleet-wide-state.md`. Chapters not
listed did not move. The rule going forward is unchanged: a ledger tracks its chapter and renames
with it; a pass-record is immutable and reads in the numbering of its date, translated through
this map.
