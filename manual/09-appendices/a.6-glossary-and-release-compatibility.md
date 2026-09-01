---
title: "Terminology and version boundaries"
chapter: "Appendices and indexes"
section: "A.6"
sidebar_position: 6
status: drafting
verified_against: Fleet 4.90.1
verified_on: 2026-08-29
verified_source: "drafted against fleet-v4.90.1 (dd0200f062). Boundaries that Fleet enforces were read from the gate; the version at which a capability was introduced is derived from release history rather than from the tag, and the ledger marks which is which. Citation ledger at research/section-notes/a.6-notes.md"
reviewed_by:
reviewed_on:
---

# Terminology and version boundaries

Two jobs, and they are the same job. **This appendix translates between the words for a thing and between the versions of a thing**, so that a reader who meets an unfamiliar name or an unexplained failure can find out which they are looking at.

What is **not** here: which capabilities your licence includes. That is collected in [a.2](a.2-platform-capability-matrix.md), where a claim is qualified by platform and scope, and where the licence is a column rather than a cell value. A version boundary and a licence gate can converge on the same symptom, a feature that is configured and does nothing, and keeping them in one table would make each harder to rule out. Many licence gates do refuse explicitly, so silence is not universal; it is common enough that the two are worth separating.

## Terminology

Entries are added as chapters need them. A term earns one when its competing meanings or names would otherwise make an administrator act or search incorrectly, which is why several entries below are pairs of words for one thing rather than definitions.

### fleetd, Orbit, osquery, Fleet Desktop

**fleetd is the bundle, and it has no version line of its own.** What ships to a host is several programs with separate version numbers. **What Fleet shows you as the fleetd or agent version is Orbit's**, which is why the boundaries later in this appendix name Orbit where they mean the supervisor and osquery where they mean the query engine. Knowing which one a number refers to is the difference between a useful check and upgrading the wrong thing.

| | What it is | Whose version |
|---|---|---|
| **Orbit** | The supervisor. It updates the others, runs scripts and software, and holds the config check-in | Its own, and the one usually meant by "the fleetd version" |
| **osquery** | The query engine. Reporting, live reports, the scheduled queries | osquery's, released separately by a separate project |
| **Fleet Desktop** | The menu-bar or tray application the end user sees | Its own |
| **Fleetd for Chrome** | A Chrome extension, on ChromeOS, with no osquery at all | Its own |

[1.2](../01-foundations/1.2-how-fleet-reaches-a-device.md) is the canonical explanation of how they divide the work.

### AB token, ABM token, and DEP token

**Three names for one credential**, and you will meet all three in one afternoon. The interface says **AB token**. Fleet's server code and most of its documentation say **ABM token**. The underlying library, and some database and log material, says **DEP**, for the same reason the [ADE and DEP](#ade-and-dep) entry below exists.

It is the token that authorises Fleet to talk to Apple Business Manager on your behalf, and it expires on its own schedule, separately from the push certificate and separately from the Apps and Books token ([7.6](../07-operate-fleet/7.6-maintain-credentials-certificates-and-access.md)).

### Unassigned, No team, and a null fleet

**Two vocabularies, and several storage representations.** Hosts that belong to no named fleet are shown as **Unassigned** in the interface. GitOps used to call the same thing **No team**, in a file named `no-team.yml`, now deprecated in favour of `unassigned.yml`.

**Underneath, how it is stored depends on what is being stored, and you cannot assume one shape.** A host carries a null fleet identifier. Some scoped resources pair a nullable identifier with a zero, and where a resource can also mean *all fleets*, a null can mean all fleets while an explicit zero means Unassigned. Read the table you are querying rather than carrying one rule between them.

**One consequence holds across all of them**: a fleet-scoped role is scoped to a *concrete* fleet, and the authorization rules reject both a null and a zero, so **fleet-scoped roles do not reach Unassigned at all** ([a.4](a.4-roles-and-permissions-matrix.md)).

### MDM enrollment status, on screen and in a filter

**The word on screen is not the word to search with.** Fleet renamed the displayed statuses and kept the API values for compatibility, so a filter written from what you read will not match:

| On screen | In the API and as a filter |
|---|---|
| On (company-owned) | `On (automatic)`, filtered as `automatic` |
| On (manual) | `On (manual)`, filtered as `manual` |
| Off | filtered as `unenrolled` |

That is three of five. The complete set also carries an enrolled personal state and a pending one, and the mapping for those is in Fleet's own interface definitions.

This is the strongest case in this appendix for looking a term up before using it. A value Fleet does not recognise is rejected with a `400`, so typing what you read on screen fails loudly, which is the good case. **The bad case is a value that is recognised and means something else than you meant.**

### MIA, and missing

**Identical, and one is deprecated.** Both name a host that has not communicated for thirty days, and Fleet's own source says they are the same thing with `mia` marked deprecated. Both work at this release. **Fleet has published no date and it has published a version**: the source says `mia` was deprecated in 4.15 and will be removed in **Fleet 5.0**. So `missing` is not merely the tidier name, it is the one that survives a major release.

### pack, and scheduled report

**A pack is the older container for scheduled queries**, and it still exists. Schedules were folded into saved queries, which this release calls reports, so current and older configuration describe overlapping objects in different words. **Meeting a pack does not prove you are looking at something old**: the pack specification endpoint still accepts new ones at this release. It does mean you are looking at the older of two ways to say the same thing.

### activity, which means two different things

**The audit stream and the work queue are both called activities**, and they are different tables with different lifetimes.

| You mean | Where it lives | What it is |
|---|---|---|
| What somebody did | The past-activity tables | The audit record, written after the fact ([1.5](../01-foundations/1.5-audit-and-activity.md)) |
| What is queued for a host | The upcoming-activity tables | Work Fleet has accepted and not yet completed ([8.6](../08-troubleshooting/8.6-server-state.md)) |

The distinction decides where you look. A script that has run is in the first and has left the second. A script that has not run yet is in the second, **and may already have left a trace in the first**, because scheduling something is itself an action somebody took and Fleet records batch scheduling as an activity. So the queue is the authority on what is pending; the audit stream is the authority on what was asked for.

### ADE, and DEP

**Automated Device Enrollment** is Apple's mechanism for a device enrolling into MDM during Setup Assistant, before anyone has logged in, because the device was bought into Apple Business and assigned to an MDM server there. It is what [3.2](../03-connect-devices/3.2-enroll-macos-devices.md) and [3.5](../03-connect-devices/3.5-enroll-ios-and-ipados-devices.md) call the company-owned path.

**DEP**, the Device Enrollment Program, is the same thing under its older name. Apple renamed the programme; the acronym did not go away, because it is still the word in Apple's own API and therefore in Fleet's code and database. You will meet ADE in the console and DEP in the tables: `host_dep_assignments`, `nano_dep_names`, `host_dep_assignments.profile_uuid`, the DEP sync cursor, and the `apple_mdm_dep_profile_assigner` schedule.

**Treat them as one concept with two vocabularies**, in the same way [8.6](../08-troubleshooting/8.6-server-state.md#one-status-three-vocabularies) treats MDM status. A query written from something you read on screen will not find a table called `ade_anything`.

### SCEP

**Simple Certificate Enrollment Protocol.** The protocol by which a device asks a server for a certificate, presenting a shared challenge as its proof of entitlement. Apple MDM uses it to give each enrolled device the identity certificate it authenticates its management sessions with, so Fleet runs a SCEP service as part of Apple MDM.

Two SCEPs are easy to confuse and the manual keeps them apart. **Fleet's own MDM SCEP** issues the device identity certificate at enrollment and is not optional. **Custom SCEP proxying**, where Fleet forwards certificate requests to a certificate authority you already run, is a separate feature for delivering your organisation's certificates to devices.

The Windows counterpart is WSTEP, which does the same job over Microsoft's protocol ([8.9](../08-troubleshooting/8.9-windows-mdm-diagnostics.md#898-wstep-device-identity-certificates)).

### MCP, and the Fleet MCP server

**Model Context Protocol.** An open standard for how an AI assistant discovers and calls external tools, so a client such as Claude operates a system through named, typed tools rather than raw API calls. **The Fleet MCP server** is Fleet's implementation: a small server that ships in the Fleet repository, holds one Fleet API token, and exposes selected Fleet reads and live osquery to an MCP-capable assistant. Keep five things apart, because the security model turns on the difference — the protocol, the MCP client inside the assistant, the model service the assistant runs on, the Fleet MCP server, and the Fleet REST API it proxies. [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md) is the chapter.

### VPP

**Apps and Books**, formerly the Volume Purchase Program. Apple's mechanism for an organisation buying app licences and assigning them to devices or to people. Fleet uses it to install App Store apps, which is why an App Store install has no installer and no download of Fleet's own: Fleet asks Apple to associate a licence and sends an `InstallApplication` command.

Like DEP, the retired name is the one in the code and the settings. The console says Apps and Books; the tokens, tables and configuration say VPP.

**Its token expires on its own schedule**, independent of the APNs certificate and the ABM token, so an estate can lose app installs while profiles keep working ([8.13](../08-troubleshooting/8.13-escalation.md)).

### node key

**The credential a host uses on the osquery and Orbit channels after enrollment.** The enroll secret authenticates the enrollment itself and nothing afterwards; what the host gets back is a node key, and that is what it presents from then on. **Not every request from a device uses one**: Fleet Desktop and the device page authenticate with a separate per-device token instead.

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

It is the **purpose-built** path for getting a file's contents off a host through osquery, which makes it both the answer to "I need to see that file" and a capability worth knowing is enabled. It is not the only such path: osquery can read a file line by line, and Fleet's own disk-encryption query does exactly that to ingest a key file. Blocks and their ceilings are configuration, and the per-carve size limit is in [8.14](../08-troubleshooting/8.14-degradation.md).

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

**Certain** renamed field names are deprecated rather than removed, so integrations written against those earlier names continue to work. The deprecation is per field rather than a blanket promise about every old name, so check the field you depend on. New work should use the current names.

**The rename covered the surfaces administrators touch, and stopped there.** Storage and internal naming kept the original words:

| Surface | Current | Notes |
|---|---|---|
| UI, API paths, CLI, GitOps | fleets, reports | `/api/v1/fleet/reports`, `fleetctl report` |
| API field names | fleets, reports | **Certain** old names deprecated and still accepted. Per field, not a blanket promise |
| MySQL tables | `teams`, `queries` | Schema unchanged |
| Redis key prefix | `livequery:` | Unchanged |
| osquery | query | osquery is a separate project and renamed nothing |

This is why documentation, forum posts, and scripts written before March 2026 use the older words for the same things, and why Fleet's own documentation still contains both.

A related change in the same release: `no-team.yml` in GitOps was deprecated in favour of `unassigned.yml`.


## What this book's version pin means

![Reference](../_assets/icons/reference.svg) Every chapter in this book was verified against **Fleet 4.90.1**, and the two generated catalogs, the configuration keys in [a.3](a.3-configuration-model-and-precedence.md#the-complete-configuration-key-catalog) and the routes in [a.8](a.8-api-action-and-endpoint-reference.md#the-complete-route-catalog), were read from that exact release. The pin is what lets the book be specific: a default, a route, an edition gate or a field name is stated as a fact about a named release rather than about Fleet in general.

Two signals tell you a claim may no longer match the release you run. The first is the version itself: if your server is not 4.90.1, treat commands, fields, defaults and gates as version-sensitive and read the chapter's version notes, because behaviour moves between releases. The second is more precise, and it is what the catalogs are for: if a configuration default you observe on your own server differs from the registered default in a.3's catalog, the book is describing a different binary from yours, and that key is where to look for what changed.

When this book is updated for a newer Fleet release, both catalogs are regenerated against that release's tag, so they keep describing the version each chapter names rather than a fixed snapshot.

## Version boundaries

![Reference](../_assets/icons/reference.svg) A **version boundary** is a version below which something behaves differently. They are not all floors and treating them as one list is how a diagnosis goes wrong, so each row below is one of these:

| | |
|---|---|
| **Hard floor** | Enforced, and the failure reaches an administrator through Fleet |
| **Silent floor** | **Nothing reaches an administrator through Fleet.** A line in the server's process log or in the agent's log on the host is still silent by this definition, and so is a notification shown to the end user of the device, because none of them appears in the console or raises an alert. Where such a signal exists the row says where |
| **Fallback or routing** | Both sides work. The version decides which path is taken |
| **Published baseline** | Fleet states it and nothing in the code enforces it |
| **Dependency constraint** | A floor or a ceiling on something Fleet runs on |

Only cross-cutting boundaries are collected here. One that a single chapter needs and no one would plan an estate around stays in that chapter.

### What Fleet enforces, and what it only negotiates

**Fleet 4.90.1 declares and enforces no global minimum agent version.** Neither enrollment path reads one, and the agent's enrollment record has no version field, so a version mismatch is never the reason an agent is refused.

What happens instead is not one mechanism but four, and telling them apart is what makes a symptom diagnosable:

| | What it means | What you see |
|---|---|---|
| **Negotiated** | Orbit and the device client declare named capabilities, and the server takes a different branch when one is absent | Usually a debug line. One capability fails **open**, and one is persisted |
| **Ungated** | No check of any kind. The server sends the block and an old agent ignores it | Nothing at all |
| **Chosen locally** | The agent decides from its own osquery version, or `fleetctl` decides while building a package | Nothing on the server |
| **Compared** | The server compares the reported agent version | An error the administrator can see. **There is exactly one of these** |

**The single comparison is the Linux passphrase escrow gate.** Everywhere else, an incompatibility degrades one feature rather than refusing anything, and most of that degradation is invisible from the console.

> **The negotiation is the Orbit and device protocols, not every Fleet request.** osquery's own protocol carries no capability header, so an osquery-side boundary is never negotiated: it is chosen locally or it is ungated.

**Fleet cannot tell you which hosts lack a capability.** Only one negotiated capability is persisted anywhere, the Windows on-demand sync flag, so for every other boundary the agent-version column on the hosts page is the practical proxy.

**Compatibility is asymmetric, and Fleet says so.** A new agent against an older server is a requirement its engineering process treats as a must. **An older agent against a new server is only a nice to have**, with a minimum named in the release notes when it breaks. That is a rollout rule: move the server first and the agents after, and read the release notes before assuming the reverse is safe.

**Upgrades follow semantic versioning with three stated exceptions**: experimental features, security fixes, and changes to default values. All three can break a minor or patch upgrade, and all three are called out in the version notes, which is the practical reason [7.3](../07-operate-fleet/7.3-upgrade-fleet-and-fleetd.md) asks you to read them rather than diff the version number.

### Agent floors

| Capability | Agent | Server | Kind |
|---|---|---|---|
| Linux LUKS **passphrase** escrow | Orbit 1.36.0 | 4.61.0 | **Hard floor.** The one version comparison in the server, and the only boundary whose failure reaches an administrator in Fleet, through the escrow error on the host record |
| Linux **snapd recovery-key** escrow, new agent against an older server | Orbit 1.58.0 | **4.90.0** | Silent to you, **not to the user**: the agent logs a warning and shows the device's user a one-shot notification. It gates itself rather than retrying, because retrying would churn the key slot |
| Linux **snapd recovery-key** escrow, older agent against a current server | Orbit 1.58.0 | 4.90.0 | Silent. The other direction of the same boundary, and **the only one in this table that runs both ways** |
| Remote channel configuration, `update_channels` | Orbit 1.20.0 | 4.43.0 | **Silent, and ungated.** Nothing checks anywhere. The server sends the block and an older agent ignores it |
| macOS FileVault key **rotation** | Orbit 1.30.0 | 4.56.0 | Silent. Negotiated, **no fallback**: the notification is simply not sent, with a debug line and nothing in the console |
| macOS ADE **setup experience** | Orbit 1.35.0 | 4.60.0 | **Fallback.** An older agent is released by the older worker-based path instead, which is a different mechanism rather than an absence |
| **Web setup experience, Linux** | Orbit 1.48.0 | 4.74.0 | Silent. **The agent refuses to start the flow** when the server does not declare the capability, which is the reverse of every other row |
| **Web setup experience, Windows** | Orbit 1.49.0 | 4.75.0 | Silent, as above. The two platforms arrived a release apart and are separate boundaries |
| **End-user authentication** at enrollment, Linux and Windows | Orbit 1.50.0 | 4.77.0 | **Silent, and it fails open.** Below it Fleet allows the enrollment unauthenticated. There is a warning in the server's process log and nothing in Fleet, so an unauthenticated enrollment looks like an ordinary one |
| Windows on-demand sync, the relaxed poll | Orbit 1.57.0 | 4.87.0 | Fallback. Negotiated, cadence only, and **the one capability flag Fleet persists** |
| `python_packages` in software inventory | osquery 5.16.0 | not applicable | Fallback, chosen locally. Two complementary queries, so both sides work, and the boundary changes whether packages in user directories are found |
| `END_USER_EMAIL` as an installer property | Orbit 1.28.0 **when the package is built** | not applicable | Fallback. Falls back to the service command line |
| `EUA_TOKEN` as an installer property | Orbit 1.55.0 **when the package is built** | not applicable | Silent floor. **No fallback branch** |
| Following an update channel to a current release | **Orbit 1.38.0 in the code, 1.38.1 as the bridge** | not applicable | Silent in Fleet. The failure is in the agent's own log on the host, and nothing in the console says the estate has stopped updating. See below |
| Enrolling and talking to a 4.90.1 server | **no minimum** | not applicable | **No boundary**, listed because its absence is the useful fact |

> **The update-server migration has two numbers and they answer different questions.** The rewrite to the new update server is in the code from **1.38.0**. **1.38.1** is what Fleet's own configuration reference names as the stepping stone, it shipped three days later, and Fleet also shipped a rollback with 1.38.0 in case one was needed. **Step through 1.38.1** ([3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md)).

> **`update_channels` is the one to know**, because it fails in the shape most likely to be misread. An agent below 1.20.0 ignores the channel you set. Fleet accepts the configuration, stores it, shows it back, and the host keeps running whatever it was running. There is no error and no log line, so the estate looks pinned and is not ([3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md)).

**The two packaging floors behave differently from the rest**, because they bind when the installer is built rather than when the host runs. An old `fleetctl` produces a package that cannot carry the property, and no later upgrade of the agent fixes it. Rebuild the package instead.

### Operating system boundaries

| Capability | Boundary | Platform | Enforced where | Kind |
|---|---|---|---|---|
| ACME device identity for Apple enrollment | **macOS 14.0, and Apple Silicon, and a DEP-assigned serial** | macOS | A server-side check before the profile is built | **Fallback.** Fleet issues the SCEP profile instead, with an info log and nothing in the console |
| Which OS-update mechanism is used | macOS 14.0.0 | macOS | A server-side version comparison | **Routing.** Both mechanisms exist and the version picks one |
| **Delivery** of the OS-update declaration | macOS 14 | macOS | A dynamic label computed from a report, not a version comparison | **Silent floor**, and a trap. See below |
| **Delivery** of the OS-update declaration | **iOS 17 and iPadOS 17** | iOS, iPadOS | **Nowhere.** The built-in labels carry no version predicate | **Published baseline only**, and a trap. See below |
| Manual, non-ADE migration eligibility | macOS **strictly above** 14.0.0 | macOS | A server-side comparison | **Silent floor** on the notification path. Loud only when a user triggers it themselves |
| Discovery request version | Protocol version 4.0 | Windows | A server-side check on the request | **Silent floor.** Fleet writes a debug line and returns a fault to the device; nothing reaches the console. The device reports the failure locally, so the evidence is on the machine rather than in Fleet |
| Full support for Windows 11 25H2 | **Fleet server 4.89.1** | Windows | Documented, and the enrollment fails | **Silent floor.** The enrollment fails outright rather than degrading, and the device reports error `80180006`; in Fleet it is a host that never appeared |
| Hardware-backed host identity | TPM 2.0 | Linux | Implicit. Fleet opens the TPM 2.0 resource-manager device node, so a kernel without it cannot serve this. **Which kernel that is, is Linux's fact rather than Fleet's**, and this appendix does not assert a number | **Silent floor** in Fleet |
| Enrolling an Apple device in MDM at all | **none** | Apple | Nothing checks | **No boundary**, listed because its absence is the useful fact |

> ### Two of these are traps rather than boundaries
>
> **The macOS 14 OS-update boundary is a dynamic label computed from report results**, so it depends on the agent rather than on the version. **A Mac that has never produced osquery results cannot enter that label**, and the older enforcement path needs the agent too, so a newly MDM-enrolled Mac with no fleetd receives neither the declaration nor the older mechanism.
>
> **Losing fleetd later is a different case.** Dynamic membership is removed only when a later result is definitively false, and an error leaves it alone, so a Mac that joined the label before its agent disappeared can keep its membership and keep receiving enforcement over MDM. Stale membership is the normal outcome there, not loss of enforcement.
>
> **The iOS and iPadOS 17 boundary is not enforced at all.** The built-in labels for those platforms are platform-only with an empty query, so they carry no version predicate and the declaration goes to every iPhone and iPad regardless. Fleet documents a baseline; nothing implements one.

### Published host baselines

**This is a snapshot of what Fleet published at 4.90.1, and it is the kind of list this appendix warns about.** It has moved before and it will move again, so read it as where the baseline stood at this release and check Fleet's own current table before planning against it.

**No global admission gate enforces this matrix.** Fleet does not refuse an enrollment for being below a line here. Individual features do have their own gates, several of them in the table above, so "unsupported" here means untested rather than blocked:

| Platform | Baseline |
|---|---|
| macOS | 14 and later |
| iOS and iPadOS | 17 and later |
| Windows | Pro and Enterprise 10 21H2 and later, Server 2012 and later |
| Linux | CentOS 7.1, Ubuntu 20.04, Fedora 38, Amazon Linux 2, Debian 11, RHEL 7, openSUSE 15.6, Arch, Omarchy |
| ChromeOS | 112.0.5615.134 and later |
| Android | 14 and later |

Fleet's own qualification is worth carrying: it may work partially or fully below these, and it does not test there or pursue bugs there. **Full Windows MDM on Windows 11 25H2 additionally needs Fleet server 4.89.1**, and that one does fail outright rather than silently.

### Server floors

These are the server side of the capabilities above, **including the two web setup rows, which run the other way**: there the agent refuses to start unless the server declares the capability. They matter when you are the one running the old version.

| Capability | Server floor |
|---|---|
| Remote channel configuration | 4.43.0 |
| macOS FileVault key rotation | 4.56.0 |
| macOS ADE setup experience | 4.60.0 |
| Linux LUKS passphrase escrow | 4.61.0 |
| End-user authentication at enrollment | 4.77.0 |
| Web setup experience, Linux | 4.74.0 |
| Web setup experience, Windows | 4.75.0 |
| Windows on-demand sync | 4.87.0 |
| Full Windows 11 25H2 support | 4.89.1 |
| Linux snapd recovery-key escrow | 4.90.0 |

**One floor runs in both directions**, and Fleet's own source says so where none of the others do. A current agent talking to a server without the snapd escrow capability has its payload rejected, so the agent gates on the capability rather than retrying, because retrying would churn the key slot on the device.

### Dependency floors

**MySQL 8.0.44.** Tested against 8.0.44, 8.4.8 and 9.5.0, with 9.6.0 currently incompatible. The floor moved from 8.0.36 during the 4.83 line ([2.2](../02-administer-and-deploy-fleet/2.2-self-hosting-architecture-and-capacity.md) has the operational consequence, which is that a newer MySQL is not automatically a safer one).

**Redis 6.2.** Required by the host-lookup cache on the agent authentication paths, which arrived in the 4.86 line. Fleet is actively tested against 6.2 and 7.

**Aurora MySQL 3.10.3**, where you are running Aurora rather than MySQL. It is the same class of constraint as the two above and is stated in the same place.

**`fleetctl` against the server: no enforced floor.** The client compares its version with the server's and, when they differ, **prints a warning and continues**. So a mismatched client is a caution rather than a refusal, and a command that behaves oddly against a server of a different version will not tell you that is why ([6.4](../06-automate-fleet/6.4-use-fleetctl.md) on pinning it in automation).

### Fleet publishes support scopes, and no dated end of life

**No dated end-of-life policy was found anywhere in the 4.90.1 repository.** What Fleet publishes there is two release-relative scopes:

| | Bug fixes | Troubleshooting help |
|---|---|---|
| **Free** | Latest version only | Current major version |
| **Premium** | Latest version only | All versions |

**There are no backports to either tier.** A fix lands in the latest release and nowhere else, so the only supported response to a bug that is hitting you is to upgrade.

**That is not the same as nothing being unsupported.** A release that is not the latest is outside the scope for fixes, and on Free a previous major version is outside the scope for troubleshooting too. Premium's all-versions troubleshooting promise is about help, not about fixes or indefinite compatibility.

So there are two planning questions rather than one. **Plan remediation around being on the latest release**, because that is what a fix requires. **Plan support access around the troubleshooting scope**, which depends on your tier and your major version. What you cannot plan around is a date, because none was found to plan against.

One practical note: **this policy lives in Fleet's company handbook rather than its documentation**, so a reader working through the product docs will not meet it.

**There is no constrained upgrade path within version 4.** Fleet's own guidance says skipping versions is fine and nothing in the server enforces an ordering. The exception is the agent, where the update server migration makes one release a stepping stone ([3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md)).

Fleet's cadence, for planning: one minor and one patch release every three weeks, with scheduled patches weekly in between and immediate patches for critical bugs. [7.3](../07-operate-fleet/7.3-upgrade-fleet-and-fleetd.md) turns that into a release-review rhythm.
