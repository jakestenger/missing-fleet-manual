---
title: "Terminology and version boundaries"
chapter: "Appendices and indexes"
section: "A.6"
sidebar_position: 6
status: drafting
verified_against: Fleet 4.90.1
verified_on: 2026-08-29
verified_source: "drafted against fleet-v4.90.1 (dd0200f062). Every version floor was read from the gate that enforces it, or recorded as unenforced where none exists. Citation ledger at research/section-notes/a.6-notes.md"
reviewed_by:
reviewed_on:
---

# Terminology and version boundaries

Two jobs, and they are the same job. **This appendix translates between the words for a thing and between the versions of a thing**, so that a reader who meets an unfamiliar name or an unexplained failure can find out which they are looking at.

What is **not** here: which capabilities your licence includes, which belongs in [a.2](a.2-platform-capability-matrix.md), where a claim can be qualified by platform and scope. A version floor and a licence gate produce the same symptom, a feature that is configured and does nothing, and keeping them in one table would make each harder to diagnose.

## Terminology

Entries are added as chapters need them. The terms below are the ones the manual's `[term]()` markers point at.

### ADE, and DEP

**Automated Device Enrollment** is Apple's mechanism for a device enrolling into MDM during Setup Assistant, before anyone has logged in, because the device was bought into Apple Business and assigned to an MDM server there. It is what [3.2](../03-connect-devices/3.2-enroll-macos-devices.md) and [3.5](../03-connect-devices/3.5-enroll-ios-and-ipados-devices.md) call the company-owned path.

**DEP**, the Device Enrollment Program, is the same thing under its older name. Apple renamed the programme; the acronym did not go away, because it is still the word in Apple's own API and therefore in Fleet's code and database. You will meet ADE in the console and DEP in the tables: `host_dep_assignments`, `nano_dep_names`, `host_dep_assignments.profile_uuid`, the DEP sync cursor, and the `apple_mdm_dep_profile_assigner` schedule.

**Treat them as one concept with two vocabularies**, in the same way [8.6](../08-troubleshooting/8.6-server-state.md#one-status-three-vocabularies) treats MDM status. A query written from something you read on screen will not find a table called `ade_anything`.

### SCEP

**Simple Certificate Enrollment Protocol.** The protocol by which a device asks a server for a certificate, presenting a shared challenge as its proof of entitlement. Apple MDM uses it to give each enrolled device the identity certificate it authenticates its management sessions with, so Fleet runs a SCEP service as part of Apple MDM.

Two SCEPs are easy to confuse and the manual keeps them apart. **Fleet's own MDM SCEP** issues the device identity certificate at enrollment and is not optional. **Custom SCEP proxying**, where Fleet forwards certificate requests to a certificate authority you already run, is a separate feature for delivering your organisation's certificates to devices.

The Windows counterpart is WSTEP, which does the same job over Microsoft's protocol ([8.9](../08-troubleshooting/8.9-windows-mdm-diagnostics.md#898-wstep-device-identity-certificates)).

### VPP

**Apps and Books**, formerly the Volume Purchase Program. Apple's mechanism for an organisation buying app licences and assigning them to devices or to people. Fleet uses it to install App Store apps, which is why an App Store install has no installer and no download of Fleet's own: Fleet asks Apple to associate a licence and sends an `InstallApplication` command.

Like DEP, the retired name is the one in the code and the settings. The console says Apps and Books; the tokens, tables and configuration say VPP.

**Its token expires on its own schedule**, independent of the APNs certificate and the ABM token, so an estate can lose app installs while profiles keep working ([8.13](../08-troubleshooting/8.13-escalation.md)).

### node key

**The credential a host uses for every request after enrollment.** The enroll secret authenticates the enrollment itself and nothing afterwards; what the host gets back is a node key, and that is what it presents from then on.

A fleetd host holds **two** of them, and confusing them costs time:

| Key | Used by | Stored on the host as |
|---|---|---|
| osquery node key | osquery, for the distributed and logging channels | Inside osquery's own database |
| Orbit node key | Orbit, for the config check-in and everything Orbit-driven | `secret-orbit-node-key.txt` in the Orbit root |

Fleet also treats the osquery node key as the unique identifier for a host row, which is why a duplicate one is a data problem rather than merely an authentication one ([3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md)).

### pprof

**Go's profiling format, and the endpoints that produce it.** A pprof profile is a sample of what a Go process was doing: CPU time, heap allocations, goroutines, blocking, mutex contention. Fleet exposes them because it is a Go program, and `fleetctl debug` fetches them ([8.5](../08-troubleshooting/8.5-fleetctl-debug.md)).

The output is not readable by eye. It is a binary file you open with `go tool pprof`, which is why the manual treats a profile as something you collect and attach rather than something you interpret in place.

### file carving

**osquery's mechanism for collecting whole files off a host**, rather than facts about them. You run a report against the `carves` table with a path, osquery reads the file, splits it into blocks, and uploads them; Fleet reassembles them and stores the result on disk or in object storage.

It is the only path in Fleet by which a file's **contents** leave a host through osquery, which makes it both the answer to "I need to see that file" and a capability worth knowing is enabled. Blocks and their ceilings are configuration, and the per-carve size limit is in [8.14](../08-troubleshooting/8.14-degradation.md).

### dead lettering

**What a message queue does with a message it could not deliver**: rather than dropping it or retrying forever, it moves it to a separate queue for inspection. The term belongs to the queueing systems Fleet delivers logs into rather than to Fleet, and it appears in this manual only where a log destination's own behaviour decides what happens to a record Fleet could not hand over ([8.2](../08-troubleshooting/8.2-log-surfaces.md)).

Fleet itself has no dead-letter queue. A record Fleet fails to write is gone, which is the point [8.2](../08-troubleshooting/8.2-log-surfaces.md) makes about which surfaces are durable.

### report, and query

**A report is Fleet's saved, runnable object.** You create it, target it, run it live, or put it on a schedule. Running one ad hoc is a **live report**.

**A query is osquery's mechanism**, and also plain SQL. osquery runs queries: on a schedule, or on demand through its distributed channel.

The two words describe different layers of the same action. Running a live report in Fleet causes osquery to execute a query on each targeted host. Both terms are correct, and which one is right depends on the layer you are talking about.

| You mean | Say | Because |
|---|---|---|
| The Fleet object you saved | report | Renamed in Fleet 4.82.0 |
| Running one ad hoc from Fleet | live report | Renamed in Fleet 4.82.0 |
| osquery's distributed channel | distributed query | osquery's own term, unchanged |
| An entry in `osquery_schedule` | scheduled query | osquery's own term, unchanged |
| The MySQL table | `queries` | The schema was not renamed |
| The Redis key prefix | `livequery:` | Internal naming was not renamed |
| SQL text | query | Generic |

Part VIII works at all of these layers at once, which is why both words appear there. Its opening section carries a note explaining the split in context.

## Deprecated names and APIs

### Fleet 4.82.0 renamed teams to fleets, and queries to reports

Released 11 March 2026. From the release notes:

> Renamed teams and queries to fleets and reports in the UI, API, CLI, and GitOps.
>
> Deprecated certain API field names to reflect the renaming of "teams" to "fleets" and "queries" to "reports".

The old field names are **deprecated rather than removed**, so integrations written against the earlier names continue to work. New work should use the current names.

**The rename covered the surfaces administrators touch, and stopped there.** Storage and internal naming kept the original words:

| Surface | Current | Notes |
|---|---|---|
| UI, API paths, CLI, GitOps | fleets, reports | `/api/v1/fleet/reports`, `fleetctl report` |
| API field names | fleets, reports | Old names deprecated, still accepted |
| MySQL tables | `teams`, `queries` | Schema unchanged |
| Redis key prefix | `livequery:` | Unchanged |
| osquery | query | osquery is a separate project and renamed nothing |

This is why documentation, forum posts, and scripts written before March 2026 use the older words for the same things, and why Fleet's own documentation still contains both.

A related change in the same release: `no-team.yml` in GitOps was deprecated in favour of `unassigned.yml`.


## Version boundaries

![Reference](../_assets/icons/reference.svg) A **floor** is the version below which a capability does not work. Three kinds meet here, and confusing them is how a diagnosis goes wrong: a minimum agent version, a minimum operating system version, and a minimum Fleet server version.

Only cross-cutting floors are collected here. A floor that one chapter needs and no other reader would plan around stays in that chapter.

### Fleet negotiates capabilities rather than versions, and that is why floors are quiet

**This is the fact the rest of the section rests on.** The agent and the server exchange a list of named capabilities on every request, each side declaring what it supports. When the server wants to do something the agent has not declared, it does something else and writes a debug line.

**There is exactly one place in the whole 4.90.1 server that compares an agent version number**, and it is the Linux disk-encryption passphrase escrow gate. Everything else is negotiated.

That mechanism is better than version comparison in most ways. It is bidirectional, it survives custom builds, and it does not break on an unexpected version string. **What it is not is observable.** There is no version number in the failure, no error in the console, and usually nothing above debug in the server log. What an administrator sees is a feature that is configured and does nothing.

Two consequences worth stating plainly:

- **There is no minimum agent version for talking to a 4.90.1 server at all.** Neither enrollment path reads a version; the agent's own enrollment record has no version field. A current server will enroll an arbitrarily old agent. The cost is per-feature degradation, and almost all of it is silent.
- **Fleet cannot tell you which hosts lack a capability.** Only one negotiated capability is written down anywhere, the Windows on-demand sync flag. For the rest there is no way to ask the question, which is why the agent-version column on the hosts page is the practical proxy.

### Agent floors

| Capability | Agent floor | Server floor | Enforced | Quiet |
|---|---|---|---|---|
| Linux LUKS **passphrase** escrow | fleetd 1.36.0 | 4.61.0 | **Yes**, the one version comparison | **No.** The only floor whose failure reaches an administrator, and only after a user acts |
| Linux **snapd recovery-key** escrow | fleetd 1.58.0 | **4.90.0** | Capability | Yes |
| Remote channel configuration, `update_channels` | fleetd 1.20.0 | 4.43.0 | **Nothing checks.** The server sends the block unconditionally | Yes, and this is the worst of the set |
| Following an update channel to a current release | orbit 1.38.1 | not applicable | Not enforced. A property of the update repository | Yes, and only in the agent's own log ([3.7](../03-connect-devices/3.7-manage-fleetd-orbit-and-updates.md)) |
| macOS FileVault key **rotation** | fleetd 1.30.0 | 4.56.0 | Capability. **No fallback**; the notification is simply not sent | Yes |
| macOS ADE **setup experience** | fleetd 1.35.0 | 4.60.0 | Capability, with a fallback path for older agents | Yes |
| **End-user authentication** at enrollment, Linux and Windows | fleetd 1.50.0 | 4.77.0 | Capability. **Below it Fleet allows the enrollment unauthenticated** | Effectively. A warning in the server log and nothing else |
| Windows on-demand sync, the relaxed poll | fleetd 1.57.0 | 4.87.0 | Capability, and the only one persisted | Yes. Cadence only |
| `python_packages` in software inventory | osquery 5.16.0 | not applicable | Two complementary queries, so both sides work | Yes, and gracefully |
| gzip-compressed osquery responses | osquery 5.21.0 | not applicable | A flag that is not passed below it | Yes. Bandwidth only |
| Per-certificate scope on Windows host details | osquery 5.23.1 | 4.90.0 | No gate found | Yes |
| `END_USER_EMAIL` as an installer property | orbit 1.28.0 **at packaging time** | not applicable | Falls back to the service command line | Yes |
| `EUA_TOKEN` as an installer property | orbit 1.55.0 **at packaging time** | not applicable | **No fallback branch** | Yes |
| Talking to a 4.90.1 server | **none** | not applicable | Nothing checks | Not applicable |

> **`update_channels` is the one to know**, because it fails in the shape most likely to be misread. An agent below 1.20.0 ignores the channel you set. Fleet accepts the configuration, stores it, shows it back, and the host keeps running whatever it was running. There is no error and no log line, so the estate looks pinned and is not ([3.7](../03-connect-devices/3.7-manage-fleetd-orbit-and-updates.md)).

**The two packaging floors behave differently from the rest**, because they bind when the installer is built rather than when the host runs. An old `fleetctl` produces a package that cannot carry the property, and no later upgrade of the agent fixes it. Rebuild the package instead.

### Operating system floors

| Capability | Floor | Platform | Enforced | Quiet |
|---|---|---|---|---|
| ACME device identity for Apple enrollment | **macOS 14.0, and Apple Silicon, and a DEP-assigned serial** | macOS | Yes | Yes. Fleet issues the SCEP profile instead and logs at info |
| Which OS-update mechanism is used | macOS 14.0.0 | macOS | Yes. A routing decision; both paths exist | Not applicable |
| **Delivery** of the OS-update declaration | macOS 14 | macOS | Yes, but **by a dynamic label computed from a report**, not by a version comparison | Yes, and see below |
| **Delivery** of the OS-update declaration | **iOS 17 and iPadOS 17: not enforced** | iOS, iPadOS | **No.** The built-in labels for these platforms carry no version predicate | Yes |
| Manual, non-ADE migration eligibility | macOS **strictly above** 14.0.0 | macOS | Yes | Yes on the notification path; loud only when a user triggers it |
| Discovery request version | protocol version 4.0 | Windows | Yes | **No.** The device reports a specific failure code |
| Full support for Windows 11 25H2 | **Fleet server 4.89.1** | Windows | Documented | **No.** Enrollment fails outright |
| Hardware-backed host identity | TPM 2.0, and so Linux kernel 4.12 | Linux | Implicitly, by opening a device node that older kernels do not have | No on the host, yes in Fleet |
| ChromeOS reporting | 112.0.5615.134, documented only | ChromeOS | Nothing enforces it | Yes |
| Android | **No minimum in code.** Fleet's documentation says Android 14 | Android | Nothing enforces it | Yes |
| Enrolling an Apple device in MDM at all | **none** | Apple | Nothing checks | Not applicable |

> ### Two of these are traps rather than floors
>
> **The macOS 14 OS-update floor is a dynamic label computed from report results.** A host that has not reported since enrollment is not in the label, so it receives nothing, and a Mac managed by MDM with no agent installed is never in it at all. **An MDM-enrolled Mac without fleetd gets no OS-update enforcement**, because both the label that selects it and the older enforcement path need the agent.
>
> **The iOS and iPadOS floor is not enforced at all.** The built-in labels for those platforms select by platform with no version predicate, so the update declaration goes to every iPhone and iPad regardless of version. Fleet's documentation states a floor; nothing implements one.

### Server floors

These are the server side of the capability list above. They matter when you are the one running the old version: an agent that is current against a server that is not.

| Capability | Server floor |
|---|---|
| Remote channel configuration | 4.43.0 |
| macOS FileVault key rotation | 4.56.0 |
| macOS ADE setup experience | 4.60.0 |
| Linux LUKS passphrase escrow | 4.61.0 |
| End-user authentication at enrollment | 4.77.0 |
| Windows on-demand sync | 4.87.0 |
| Full Windows 11 25H2 support | 4.89.1 |
| Linux snapd recovery-key escrow | 4.90.0 |

**One floor runs in both directions**, and Fleet's own source says so where none of the others do. A current agent talking to a server without the snapd escrow capability has its payload rejected, so the agent gates on the capability rather than retrying, because retrying would churn the key slot on the device.

### Dependency floors

**MySQL 8.0.44.** Tested against 8.0.44, 8.4.8 and 9.5.0, with 9.6.0 currently incompatible. The floor moved from 8.0.36 during the 4.83 line ([2.9](../02-administer-and-deploy-fleet/2.9-self-hosting-architecture-and-capacity.md) has the operational consequence, which is that a newer MySQL is not automatically a safer one).

**Redis 6.2.** Required by the host-lookup cache on the agent authentication paths, which arrived in the 4.86 line. Fleet is actively tested against 6.2 and 7.

### Fleet publishes a support policy, not a support window

**No Fleet release has a stated end of life, and no date is attached to any of them.** What Fleet publishes is release-relative:

| | Bug fixes | Troubleshooting help |
|---|---|---|
| **Free** | Latest version only | Current major version |
| **Premium** | Latest version only | All versions |

**There are no backports to either tier.** A fix lands in the latest release and nowhere else, so the only supported response to a bug you are hit by is to upgrade.

Two things about that policy are worth knowing before you plan against it. **It lives in Fleet's company handbook rather than in its documentation**, so a reader working through the product docs will not meet it. And **it is not a window**: nothing expires, and no version is ever declared unsupported, which means "supported" and "unsupported" are not the categories to plan in. The category that matters is whether you are on the latest release.

**There is no constrained upgrade path within version 4.** Fleet's own guidance says skipping versions is fine, and nothing in the server enforces an ordering. The exception is the agent, where the update repository move makes one release a stepping stone ([3.7](../03-connect-devices/3.7-manage-fleetd-orbit-and-updates.md)).

Fleet's cadence, for planning: one minor and one patch release every three weeks, with scheduled patches weekly in between and immediate patches for critical bugs. [7.2](../07-operate-fleet/7.2-upgrade-fleet-and-fleetd.md) is where that becomes a release-review rhythm.
