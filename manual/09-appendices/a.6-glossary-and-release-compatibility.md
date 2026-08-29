---
title: "Terminology and version boundaries"
chapter: "Appendices and indexes"
section: "A.6"
sidebar_position: 6
status: drafting
verified_against: Fleet 4.90.1
verified_on: 2026-08-24
verified_source: "partial: the terminology section and the 4.82.0 rename are verified at git tag fleet-v4.90.1; feature availability and version boundaries are still outline"
---

# Terminology and version boundaries

**Two of the five sections below are written and three are not.** Terminology and the deprecated-names section carry verified content; **Feature availability** and **Version boundaries** are headings with nothing under them, and a chapter that sends you to this appendix for either is sending you nowhere yet.

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

## Feature availability

**Not written.** Which capabilities are Fleet Free and which are Fleet Premium is currently stated per chapter, where each was verified, rather than gathered here.

## Version boundaries

**Not written.** Minimum supported OS versions, minimum fleetd versions per feature, and Fleet's own version support window belong here. Several chapters state a specific floor they verified, such as fleetd 1.36.0 for Linux disk-encryption escrow; none of that is collected.

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

## Documentation maintenance
