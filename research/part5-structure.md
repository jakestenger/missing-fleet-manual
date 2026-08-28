# Part V structure, agreed 2026-08-27

Negotiated with the independent reviewer before drafting, as Part IV's was. The reviewer verified
the checkout at `dd0200f062`, tagged `fleet-v4.90.1`.

## Outcome: nine chapters, not eight

The reviewer rejected the eight-chapter split. The subjects were mostly right; the organising model
was wrong in 5.1, 5.5 and 5.6, and 5.8 as outlined was not a chapter.

## Where I was wrong

**I proposed a two-mechanism spine: the unified activity queue against the MDM command channel.**
Half right and half wrong.

Right: configuration profiles really are outside `upcoming_activities`.

Wrong in two ways.

**First, the enum has five values, not four.** I read the creating migration
(`20250127162751_AddUnifiedQueueTable.go`) and stopped there. A later migration,
`20251028140300_AddInHouseAppsToUnifiedQueue.go`, adds `in_house_app_install`. Confirmed against
`server/datastore/mysql/schema.sql`, where the column reads
`enum('script','software_install','software_uninstall','vpp_app_install','in_house_app_install')`.
**Methodology lesson recorded in CONTRIBUTING: `schema.sql` is the authority on table shape, not the
migration that created the table.**

**Second, the queue is a scheduler, not a transport.** Two mechanisms is the wrong count because
queue membership and delivery channel are independent axes. A VPP install is both queue work and
Apple MDM work. An Android install is managed software that never enters the queue at all.

## The agreed spine

Three questions, in order:

1. Is this **desired state**, a **discrete activity**, or a **device action**?
2. Which channel carries it: **Orbit**, **Apple MDM/DDM**, **Windows OMA-DM**, or **Android AMAPI**?
3. Which lifecycle and status model tells you whether it converged, executed, or failed?

The reviewer's argument for this over my version: it explains why a VPP install is simultaneously
unified-queue work and Apple MDM work, which the two-mechanism model cannot.

## Queue facts 5.1 must teach, with the reviewer's citations to verify at drafting time

- Ordering is active work first, then higher priority, then earlier creation time.
- **Not perfectly serial**: Fleet may activate up to five consecutive same-priority VPP installs
  together. `server/datastore/mysql/activities.go`, ordering around line 1032, batching around 1087.
- Normal activities are priority `0`; setup-experience scripts and software are `100`.
  `server/fleet/scripts.go` and `server/fleet/software_installer.go`. **Do not present arbitrary
  priority as an administrator-facing rollout control.**
- An activity blocks later queue work until it reaches a final state.
- Upcoming work can be cancelled, but **activated lock and wipe are explicitly uncancellable**.
  `server/service/activities.go` around line 123.
- **Apple ADE re-enrollment cancels all upcoming activity for the host**, independently of whether
  past host activity is preserved. `server/datastore/mysql/apple_mdm.go`.
- Deleting a host deletes its queue rows. `server/datastore/mysql/hosts.go`.
- Cancellation is not a guarantee that already-dispatched host-side work can be recalled.

Every one of these is to be re-verified at the tag when 5.1 is drafted. The reviewer's citations are
a starting point, not a source: a reviewer's proposed wording is a claim, not a citation.

## Other rulings

**5.8 collision material moves to 5.1.** I wanted queue governance last. The reviewer's argument:
collision behaviour is prerequisite vocabulary, needed before running a script, choosing setup
software, attaching remediation or pressing wipe. Accepted.

**OS updates get their own chapter (5.6).** Previously buried inside configuration profiles.

**Encryption gets its own chapter (5.8),** separated from MDM commands, which become 5.7. The
reviewer was explicit that commands and encryption should not stay together merely to preserve a
chapter count.

**Policy automation moves to 5.9** and stays narrow: 4.3 owns what a policy is and how it
evaluates, 5.9 owns only what a failing policy triggers and the safety properties of that.

## The agreed chapters

| | Title | Sections |
|---|---|---|
| 5.1 | Plan, target, and govern device changes | Classify desired state, discrete activity, and device action; map the change to its channel and status model; rollout rings with fleets and labels; queue ordering, activation and priority; cancelling, re-enrollment and host deletion; collisions, repetition, rollback and ownership |
| 5.2 | Manage configuration profiles and declarative settings | Fleet settings, classic profiles or declarations; authoring for Apple, Windows and Android; scoping and reconciliation; secrets, Fleet variables, custom host vitals and assets; delivery, installation and removal status; editing, resending, replacing and removing |
| 5.3 | Run and manage scripts | Safe and repeatable design; supported platforms and interpreters; size, timeout, pending and output limits; upload, scope and run; secrets and host variables without leaking them; results and the script library |
| 5.4 | Manage software and applications | Custom packages, Fleet-maintained apps or store apps; installers, queries and lifecycle scripts; package variants and platform-specific applications; Orbit, Apple MDM and Android delivery; verify, retry and uninstall; versions, catalog refresh, automatic updates, pins and rollback |
| 5.5 | Design setup and self-service experiences | Enrollment-time setup against ongoing self-service; composing setup from profiles, software, scripts and account steps; per-platform setup capabilities; publishing and categorising self-service software; end-user installs, uninstall requests and device actions; completion, failure, skipped and cancelled status |
| 5.6 | Control operating system updates | Built-in enforcement or custom update profiles; macOS, iOS and iPadOS versions and deadlines; Windows deadlines and grace periods; Android system-update policy; the Linux boundary; rolling out, verifying, revising and withdrawing |
| 5.7 | Control devices and send MDM commands | Supported device actions and custom commands; lock, unlock, locate and wipe by platform; the transport behind each action; custom Apple and Windows commands; status, results and retry; cancellation and irreversible actions |
| 5.8 | Enforce disk encryption and manage recovery credentials | FileVault, BitLocker and LUKS as distinct things; enabling encryption or escrow by platform; prerequisites and end-user interaction; enforcement, encryption and escrow status; retrieving, verifying, rotating and recovering keys; re-enrollment, scope changes, archives and Recovery Lock |
| 5.9 | Automate remediation with policies | Starting from a failing policy result; software, App Store app or script remediation; transition-based against continuous automation; platform, fleet, label and agent compatibility; bounding duplicate work, cooldown and retries; automation history, resetting state, exceptions and rollback |

## Boundaries with drafted parts

Part VIII keeps implementation-level queue diagnosis, including the SQL already in 8.6. Part V
explains consequences. Part IV owns policy evaluation (4.3), software inventory reading (4.4) and
custom host vitals (4.1). Part II owns MDM server setup. Part VI owns GitOps.
