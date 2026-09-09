---
title: "Terminology and version boundaries"
chapter: "Appendices and indexes"
section: "A.6"
sidebar_position: 6
verified_against: Fleet 4.91.0
verified_on: 2026-09-08
verified_source: "drafted against fleet-v4.90.0 (7c428c6e46). Boundaries that Fleet enforces were read from the gate; the version at which a capability was introduced is derived from release history rather than from the tag, and the ledger marks which is which. Citation ledger at research/section-notes/a.6-notes.md. The end-user-authentication agent-floor row was amended 2026-09-08 for the 4.91 `mdm.allow_orbit_end_user_auth_bypass` setting, verified against fleet-v4.91.0 (35fc1c0244). Corrected 2026-09-08 (overnight campaign step 7), verified at fleet-v4.91.0 (35fc1c0244): the end-user authentication floor read Orbit 1.50.0, a release that appears nowhere in `orbit/CHANGELOG.md`. The entry that added end-user authentication before enrolling Windows and Linux devices is 1.50.1 (Nov 27, 2025), so the row now says 1.50.1. Found while checking a different version claim; the code citation at `server/service/orbit.go` was unaffected and unchanged. Amended again 2026-09-08 (overnight campaign step 7, round-3 review finding 2), verified at the orbit release tags in the same checkout: the 1.50.1 correction above was itself wrong and is reverted. `orbit-v1.50.0` exists as a tag (`b3ca45564a`, 2025-11-12), `CapabilityEndUserAuth` is absent from `orbit-v1.49.1:server/fleet/capabilities.go` and present at `orbit-v1.50.0:server/fleet/capabilities.go:99` where `GetOrbitClientCapabilities()` advertises it unconditionally, and the entire `orbit-v1.50.0..orbit-v1.50.1` diff is one file refactoring how Orbit opens a browser window. `orbit/CHANGELOG.md` files the feature under 1.50.1 only because the pending entry `orbit/changes/34528-support-end-user-auth`, present in the 1.50.0 tree, was folded in at the next cut. An absent changelog section is not evidence that a release does not exist, so the agent-floors row reads Orbit 1.50.0 again; the row's evidence kind is a tag reading rather than the release history this frontmatter warns about, and the `server/service/orbit.go` citation is again unaffected"
---

# Terminology and version boundaries

![Reference](../_assets/icons/reference-light.svg) Use this appendix to translate unfamiliar names and check version requirements. It connects the terms you see in the UI with those used in code, APIs, and older documentation, then lists the version changes that can affect a deployment.

For licence requirements, see [a.2](a.2-platform-capability-matrix.md). Version and licence restrictions can produce similar symptoms, so check both when a configured feature does not work. Some restrictions return explicit errors; others leave only a log message or no visible indication.

## Terminology

These entries explain names that can affect a search or an administrative decision. Several map current product terms to older names still used in storage or integrations.

### fleetd, Orbit, osquery, Fleet Desktop

fleetd bundles programs with separate version numbers. The fleetd or agent version displayed by Fleet is Orbit’s version. The tables below name Orbit for the supervisor and osquery for the query engine so you can check or upgrade the relevant component.

| | What it is | Whose version |
|---|---|---|
| **Orbit** | The supervisor. It updates the others, runs scripts and software, and holds the config check-in | Its own, and the one usually meant by "the fleetd version" |
| **osquery** | The query engine. Reporting, live reports, the scheduled queries | osquery's, released separately by a separate project |
| **Fleet Desktop** | The menu-bar or tray application the end user sees | Its own |
| **Fleetd for Chrome** | A Chrome extension, on ChromeOS, with no osquery at all | Its own |

[1.2](../01-foundations/1.2-how-fleet-reaches-a-device.md) explains how these components divide the work.

### AB token, ABM token, and DEP token

These names refer to the same credential. The interface uses **AB token**; server code and much of the documentation use **ABM token**. The underlying library and some database and log entries use **DEP token**, reflecting Apple’s older terminology ([ADE and DEP](#ade-and-dep)).

It is the token that authorises Fleet to talk to Apple Business Manager on your behalf, and it expires on its own schedule, separately from the push certificate and separately from the Apps and Books token ([7.6](../07-operate-fleet/7.6-maintain-credentials-certificates-and-access.md)).

### Unassigned, No team, and a null fleet

Hosts outside a named fleet appear as **Unassigned** in the interface. GitOps formerly called this **No team**, using `no-team.yml`; that filename is deprecated in favor of `unassigned.yml`.

Storage representation varies by resource. A host uses a null fleet identifier. Other scoped resources distinguish null from zero; where a resource can cover all fleets, null may mean all fleets and zero may mean Unassigned. Check the table’s meaning before writing a query.

Most fleet-scoped authorization rules require a concrete fleet identifier and reject Unassigned objects. Host listing has a broader rule, so visibility in a list does not establish permission to open or act on the host ([a.4](a.4-roles-and-permissions-matrix.md)).

### MDM enrollment status, on screen and in a filter

Fleet renamed some displayed enrollment statuses while retaining API values for compatibility. Use the API value when filtering:

| On screen | In the API and as a filter |
|---|---|
| On (company-owned) | `On (automatic)`, filtered as `automatic` |
| On (manual) | `On (manual)`, filtered as `manual` |
| Off | filtered as `unenrolled` |

The full set also includes enrolled-personal and pending states. Fleet’s interface definitions provide those mappings.

Check the accepted filter value before using a displayed label. Unknown values return `400`; a recognized value with a different meaning can instead return an unexpected set of hosts.

### MIA, and missing

Both names mean a host that has not communicated for thirty days. At this release, both work, but `mia` is deprecated. Fleet’s source records deprecation in 4.15 and planned removal in Fleet 5.0, without a calendar date. Use `missing` in new filters.

### pack, and scheduled report

A pack is the older container for scheduled queries. Current reports include scheduling directly, but the pack specification endpoint still accepts new packs at this release. Older and current configuration can therefore describe overlapping scheduling workflows.

### activity, which means two different things

Fleet uses “activity” for both audit records and queued host work. They live in different tables and have different lifetimes:

| You mean | Where it lives | What it is |
|---|---|---|
| What somebody did | The past-activity tables | The audit record, written after the fact ([1.5](../01-foundations/1.5-audit-and-activity.md)) |
| What is queued for a host | The upcoming-activity tables | Work Fleet has accepted and not yet completed ([8.6](../08-troubleshooting/8.6-server-state.md)) |

Use the upcoming-activity queue to check what is pending. An audit entry may already exist for work that has not run, since Fleet records actions such as batch scheduling. Completed scripts leave the queue and appear in past activity records.

### ADE, and DEP

**Automated Device Enrollment** is Apple's mechanism for a device enrolling into MDM during Setup Assistant, before anyone has logged in, because the device was bought into Apple Business and assigned to an MDM server there. It is what [3.2](../03-connect-devices/3.2-enroll-macos-devices.md) and [3.5](../03-connect-devices/3.5-enroll-ios-and-ipados-devices.md) call the company-owned path.

DEP, the Device Enrollment Program, is the older name for ADE. The acronym remains in Apple’s API and Fleet’s storage and code: `host_dep_assignments`, `nano_dep_names`, `host_dep_assignments.profile_uuid`, the DEP sync cursor, and the `apple_mdm_dep_profile_assigner` schedule.

Use ADE when describing the workflow and the literal DEP identifiers when querying storage. [8.6](../08-troubleshooting/8.6-server-state.md#enrolment-values-in-storage-display-and-filters) covers similar differences between displayed and stored MDM status.

### SCEP

**Simple Certificate Enrollment Protocol.** The protocol by which a device asks a server for a certificate, presenting a shared challenge as its proof of entitlement. Apple MDM uses it to give each enrolled device the identity certificate it authenticates its management sessions with, so Fleet runs a SCEP service as part of Apple MDM.

Fleet’s built-in MDM SCEP service issues the device identity certificate at enrollment and is required for Apple MDM. Custom SCEP proxying is a separate feature that forwards requests to your own certificate authority to deliver organisational certificates.

The Windows counterpart is WSTEP, which does the same job over Microsoft's protocol ([8.9](../08-troubleshooting/8.9-windows-mdm-diagnostics.md#898-wstep-device-identity-certificates)).

### MCP, and the Fleet MCP server

**Model Context Protocol** is an open standard through which an AI assistant discovers and calls named, typed tools. The Fleet MCP server ships in Fleet’s repository, holds one API token, and exposes selected reads and live osquery operations. Its security model involves five components: the protocol, the assistant’s MCP client, the model service, the Fleet MCP server, and the REST API it calls. [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md) explains their roles and setup.

### VPP

**Apps and Books**, formerly the Volume Purchase Program. Apple's mechanism for an organisation buying app licences and assigning them to devices or to people. Fleet uses it to install App Store apps, which is why an App Store install has no installer and no download of Fleet's own: Fleet asks Apple to associate a licence and sends an `InstallApplication` command.

Like DEP, the retired name is the one in the code and the settings. The console says Apps and Books; the tokens, tables and configuration say VPP.

**Its token expires on its own schedule**, independent of the APNs certificate and the ABM token, so an estate can lose app installs while profiles keep working ([8.13](../08-troubleshooting/8.13-escalation.md)).

### node key

A node key authenticates a host on the osquery or Orbit channel after enrollment. The enroll secret authenticates enrollment, which returns the node key for subsequent requests. Fleet Desktop and the device page use a separate per-device token.

A fleetd host holds two node keys:

| Key | Used by | Stored on the host as |
|---|---|---|
| osquery node key | osquery, for the distributed and logging channels | Inside osquery's own database |
| Orbit node key | Orbit, for the config check-in and everything Orbit-driven | `secret-orbit-node-key.txt` in the Orbit root |

Fleet also treats the osquery node key as the unique identifier for a host row, which is why a duplicate one is a data problem rather than merely an authentication one ([3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md)).

### pprof

**Go's profiling format, and the endpoints that produce it.** A pprof profile is a sample of what a Go process was doing: CPU time, heap allocations, goroutines, blocking, mutex contention. Fleet exposes them because it is a Go program, and `fleetctl debug` fetches them ([8.5](../08-troubleshooting/8.5-fleetctl-debug.md)).

Open the binary profile with `go tool pprof`, or attach it to a support investigation. It cannot be interpreted as an ordinary text log.

### file carving

File carving collects whole files through osquery. A report against the `carves` table supplies a path; osquery reads the file, splits it into blocks, and uploads them. Fleet reassembles the blocks and stores metadata in MySQL. Block data also uses MySQL by default, or S3/GCS when a carves bucket is configured.

Use carving when you need a file’s contents. It is one of several ways osquery can read file data; Fleet’s disk-encryption query, for example, reads a key file line by line. [8.14](../08-troubleshooting/8.14-degradation.md) covers the per-carve size limit and related configuration.

### dead lettering

Dead lettering moves an undeliverable message to a separate queue for inspection. In this manual, the term describes behavior of external log destinations. Their queueing rules determine what happens after Fleet hands over a record ([8.2](../08-troubleshooting/8.2-log-surfaces.md)).

Fleet has no dead-letter queue of its own. A failed log write has no such recovery path; [8.2](../08-troubleshooting/8.2-log-surfaces.md) describes the durability of each log surface.

### report, and query

**A report is Fleet's saved, runnable object.** You create it, target it, run it live, or put it on a schedule. Running one ad hoc is a **live report**.

**A query is osquery's mechanism**, and also plain SQL. osquery runs queries: on a schedule, or on demand through its distributed channel.

Running a live report in Fleet causes osquery to execute a query on each targeted host. Use the term that matches the layer you are describing.

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

### Terms the manual uses across chapters

These terms appear across the manual. The linked chapters explain their practical use.

**Blast radius.** The scope affected by an action or failure, such as the hosts reached by a command or data exposed through a credential. [8.1](../08-troubleshooting/8.1-diagnostic-method.md) uses this idea when choosing a diagnostic step.

**Estate.** All devices managed by one Fleet deployment. The term is used for capacity, rollout, and policy decisions that concern the whole population.

**Idempotency.** Repeating an operation produces the same result as performing it once. This matters when scripts, installations, or remediation may be retried. Design that behavior into the work you send; Fleet does not provide a general idempotency guarantee ([6.1](../06-automate-fleet/6.1-automation-design-and-change-control.md)).

**Fan-out.** One request expands into many, such as a live query sent to hundreds of hosts or an assistant making one API call per fleet. Account for the combined cost and possible partial failures ([1.6](../01-foundations/1.6-the-fleet-server.md), [a.11](a.11-mcp-tool-reference.md)).

**JSON-RPC.** The request and response protocol the Model Context Protocol speaks: named methods with typed parameters, carried over the Fleet MCP server's stdio or SSE transport ([6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md)).

**IRSA.** IAM Roles for Service Accounts, AWS's mechanism for giving a Kubernetes pod an IAM role without static keys. Fleet on EKS uses it, alongside ECS task roles, for token-based access to AWS APIs ([2.3](../02-administer-and-deploy-fleet/2.3-deploy-on-aws-or-gcp.md)).

**TUF.** The Update Framework, the signed-metadata update system fleetd's updater uses to decide which version to run and to verify what it fetched ([3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md)). Fleetd for Chrome does not use it; Chrome updates that extension instead.

## Deprecated names and APIs

### Fleet 4.82.0 renamed teams to fleets, and queries to reports

Released 11 March 2026. From the release notes:

> Renamed teams and queries to fleets and reports in the UI, API, CLI, and GitOps.
>
> Deprecated certain API field names to reflect the renaming of "teams" to "fleets" and "queries" to "reports".

Some renamed API fields remain accepted under their deprecated names. Check each field your integration uses; this is not a blanket compatibility promise for every old name. Use current names for new work.

Administrator-facing names changed, while storage and internal identifiers retained older terms:

| Surface | Current | Notes |
|---|---|---|
| UI, API paths, CLI, GitOps | fleets, reports | `/api/v1/fleet/reports`, `fleetctl report` |
| API field names | fleets, reports | **Certain** old names deprecated and still accepted. Per field, not a blanket promise |
| MySQL tables | `teams`, `queries` | Schema unchanged |
| Redis key prefix | `livequery:` | Unchanged |
| osquery | query | osquery is a separate project and renamed nothing |

This is why documentation, forum posts, and scripts written before March 2026 use the older words for the same things, and why Fleet's own documentation still contains both.

A related change in the same release: `no-team.yml` in GitOps was deprecated in favour of `unassigned.yml`.


## What this manual's version pin means

![Reference](../_assets/icons/reference-light.svg) This edition covers Fleet 4.91.0. Most chapters were verified at 4.90.0 and carried forward; sections affected by 4.91 were checked against 4.91.0. The generated [configuration catalog](a.3-configuration-model-and-precedence.md#the-complete-configuration-key-catalog) and [route catalog](a.8-api-action-and-endpoint-reference.md#the-complete-route-catalog) come from 4.91.0. Each chapter’s `verified_against` frontmatter records its verification version.

If your server is outside this edition’s release line, review the chapter’s version notes before relying on commands, fields, defaults, or licence gates. A difference in a registered default is a useful clue to a version change; first distinguish that default from an explicitly configured value using [a.3](a.3-configuration-model-and-precedence.md).

When this manual is updated for a newer Fleet release, both catalogs are regenerated against that release's tag, so they keep describing the version each chapter names rather than a fixed snapshot.

## Version boundaries

![Reference](../_assets/icons/reference-light.svg) A version boundary marks a change in availability, behavior, or dependency support. The tables distinguish six kinds:

| | |
|---|---|
| **Hard floor** | Enforced, and the failure reaches an administrator through Fleet |
| **Silent floor** | **Nothing reaches an administrator through Fleet.** A line in the server's process log or in the agent's log on the host is still silent by this definition, and so is a notification shown to the end user of the device, because none of them appears in the console or raises an alert. Where such a signal exists the row says where |
| **Fallback or routing** | Both sides work. The version decides which path is taken |
| **Published baseline** | Fleet states it and nothing in the code enforces it |
| **Dependency constraint** | A floor or a ceiling on something Fleet runs on |
| **Runtime-fetched** | The binary is pinned to a release, but a specific input inside it is re-fetched on a schedule from somewhere that is not that release, so what it validates against can drift while the version number does not move |

This appendix collects boundaries that affect deployment planning across chapters. Feature-specific limits also appear in their owning chapters.

<a id="what-fleet-enforces-and-what-it-only-negotiates"></a>

### Enforced requirements and capability negotiation

Fleet 4.90.0 has no global minimum agent version enforced at enrollment. Neither enrollment path checks one, and the agent’s enrollment record has no version field. Individual features can still have version requirements.

Feature compatibility follows four mechanisms:

| | What it means | What you see |
|---|---|---|
| **Negotiated** | Orbit and the device client declare named capabilities, and the server takes a different branch when one is absent | Usually a debug line. One capability fails **open**, and one is persisted |
| **Ungated** | No check of any kind. The server sends the block and an old agent ignores it | Nothing at all |
| **Chosen locally** | The agent decides from its own osquery version, or `fleetctl` decides while building a package | Nothing on the server |
| **Compared** | The server compares the reported agent version | An error the administrator can see. **There is exactly one of these** |

The explicit agent-version comparison covers Linux passphrase escrow. Other compatibility checks can limit individual features without rejecting enrollment, often without a console-visible error.

> Capability negotiation belongs to the Orbit and device protocols. osquery’s protocol has no capability header; its version-dependent behavior is chosen locally or left ungated.

Fleet persists only one negotiated capability, the Windows on-demand sync flag. For the others, use reported agent versions as a practical proxy when identifying hosts that may lack support.

Fleet’s engineering guidance requires newer agents to work with older servers. Support for older agents against newer servers is a weaker expectation, with minimums called out in release notes when compatibility breaks. Check those notes and the rollout procedure in [7.3](../07-operate-fleet/7.3-upgrade-fleet-and-fleetd.md) before choosing an upgrade order.

Fleet follows semantic versioning with three exceptions: experimental features, security fixes, and changed defaults can introduce breaking changes in minor or patch releases. Review the version notes for those changes as part of the upgrade procedure ([7.3](../07-operate-fleet/7.3-upgrade-fleet-and-fleetd.md)).


<!-- IMAGE-TODO: assets/a.6-agent-feature-compatibility.webp
     QUESTION: Why can an agent enroll successfully and still lack one feature?
     PROMPT: DIAGRAM: Separate Enrollment accepted from four feature paths. Named capability
     advertised → server selects branch; Ungated setting sent → older agent may ignore it;
     Agent/tool local decision → feature choice; Explicit version comparison → Linux passphrase
     escrow gate. Do not place a universal Minimum agent version gate before enrollment. Keep the
     lanes independent, and note osquery protocol has no capability header. The single persisted
     Windows sync capability can be a small storage tag on the negotiated lane, not a universal
     capability inventory.
     TERMINOLOGY: Fleet is the company, product, or server. Host groups are lowercase
     fleet/fleets, including headings and labels. Do not call these groups teams. Preserve
     exact code/API identifiers. These instructions are not text to render.
     DESIGN: Flat vector technical diagram. Fleet is software for managing computers; draw no
     vehicles. Use Inter labels and Roboto Mono identifiers. At 1400 px source width use 48 px
     titles, 36 px body labels, and at least 28 px secondary text; scale proportionally. Check at
     720 px reading width and intended print size. Use a 32 px spacing grid, at least 24 px node
     padding, and consistent corner radii. Center short node names; left-align multiline
     explanations. Never shrink text to fit. Use #F9FAFC background, #192147 headings and primary
     connectors, #515774 text, #8B8FA2 secondary connectors, #C5C7D1 borders, and #D3E8F3 or #E8F1F6
     quiet fills. Use #5CABDF and #C98DEF for named categories, #3AEFC4 for labelled positive
     outcomes, #D66C7B for labelled failures, and #FAA669 for labelled cautions. Tint large panels
     to 20 to 25 percent; full strength is for small marks. Keep text navy or slate, or off-white on
     a navy anchor. Never rely on colour alone. Use one arrowhead shape, consistent stroke weights,
     box-edge termination, and labelled branches and return paths. Keep connectors clear of text. No
     gradients, shadows, decorative icons, logo, watermark, em-dashes, or slogan footer. Render only
     the specified reader-facing labels. Choose orientation to fit the relationship, not a default
     poster. Keep captions outside the artwork. If labels crowd, split the figure before shrinking
     them. Keep editable SVG when the production method supports it.
     NOTE: Proposed 2026-09-08; editorial brief, not technical re-verification. Reduce the paragraph
     introducing compatibility mechanisms. Retain all version floors, exact feature exceptions,
     direction-of-compatibility qualifications, and the native mechanism table. Keep current prose
     and this TODO until the actual image is reviewed. Then check alt text against the artwork and
     retain an accessible summary plus all required technical qualifications.
     CANDIDATE: ../../research/visual-reviews/appendices/assets/a.6-agent-feature-compatibility.webp
     Rendered and inspected for the overnight batch; awaiting final joint review.
-->

<!-- IMAGE PENDING. Install reviewed artwork, then activate the image line below.
![Enrollment acceptance is separate from feature negotiation, ignored settings, local decisions, and the explicit Linux escrow version check.](assets/a.6-agent-feature-compatibility.webp)
-->

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
| **End-user authentication** at enrollment, Linux and Windows | Orbit 1.50.0 | 4.77.0 | **Silent, and it fails open by default.** Below it Fleet allows the enrollment unauthenticated. There is a warning in the server's process log and nothing in Fleet, so an unauthenticated enrollment looks like an ordinary one. **From server 4.91.0 this is a choice**: `mdm.allow_orbit_end_user_auth_bypass` defaults to true, preserving the fail-open, and set to false it refuses these hosts instead ([5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md#end-user-authentication)) |
| Windows on-demand sync, the relaxed poll | Orbit 1.57.0 | 4.87.0 | Fallback. Negotiated, cadence only, and **the one capability flag Fleet persists** |
| `python_packages` in software inventory | osquery 5.16.0 | not applicable | Fallback, chosen locally. Two complementary queries, so both sides work, and the boundary changes whether packages in user directories are found |
| `END_USER_EMAIL` as an installer property | Orbit 1.28.0 **when the package is built** | not applicable | Fallback. Falls back to the service command line |
| `EUA_TOKEN` as an installer property | Orbit 1.55.0 **when the package is built** | not applicable | Silent floor. **No fallback branch** |
| Following an update channel to a current release | **Orbit 1.38.0 in the code, 1.38.1 as the bridge** | not applicable | Silent in Fleet. The failure is in the agent's own log on the host, and nothing in the console says the estate has stopped updating. See below |
| Enrolling and talking to a 4.90.0 server | **no minimum** | not applicable | **No boundary**, listed because its absence is the useful fact |

> The update-server migration uses two relevant versions. The rewrite arrived in Orbit 1.38.0; Fleet’s configuration reference specifies 1.38.1, released three days later, as the bridge release. A rollback also shipped with 1.38.0. Use 1.38.1 as the stepping stone ([3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md)).

> Agents below Orbit 1.20.0 ignore `update_channels`. Fleet can accept and display the configuration while those hosts continue using their previous channels, without an error or log line. Confirm agent versions before relying on remote channel control ([3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md)).

The two installer-property floors apply when the package is built. Upgrading an already-installed agent does not add a property that an older `fleetctl` omitted from the installer; rebuild the package.

### Operating system boundaries

| Capability | Boundary | Platform | Enforced where | Kind |
|---|---|---|---|---|
| ACME device identity for Apple enrollment | **macOS 14.0, and Apple Silicon, and a DEP-assigned serial** | macOS | A server-side check before the profile is built | **Fallback.** Fleet issues the SCEP profile instead, with an info log and nothing in the console |
| Which OS-update mechanism is used | macOS 14.0.0 | macOS | A server-side version comparison | **Routing.** Both mechanisms exist and the version picks one |
| **Delivery** of the OS-update declaration | macOS 14 | macOS | A dynamic label computed from a report, not a version comparison | **Silent floor.** Delivery also depends on the label behavior below |
| **Delivery** of the OS-update declaration | **iOS 17 and iPadOS 17** | iOS, iPadOS | **Nowhere.** The built-in labels carry no version predicate | **Published baseline only.** See the targeting behavior below |
| Manual, non-ADE migration eligibility | macOS **strictly above** 14.0.0 | macOS | A server-side comparison | **Silent floor** on the notification path. Loud only when a user triggers it themselves |
| Discovery request version | Protocol version 4.0 | Windows | A server-side check on the request | **Silent floor.** Fleet writes a debug line and returns a fault to the device; nothing reaches the console. The device reports the failure locally, so the evidence is on the machine rather than in Fleet |
| Full support for Windows 11 25H2 | **Fleet server 4.89.1** | Windows | Documented, and the enrollment fails | **Silent floor.** The enrollment fails outright rather than degrading, and the device reports error `80180006`; in Fleet it is a host that never appeared |
| Hardware-backed host identity | TPM 2.0 | Linux | Implicit. Fleet opens the TPM 2.0 resource-manager device node, so a kernel without it cannot serve this. No minimum kernel version is established here | **Silent floor** in Fleet |
| Enrolling an Apple device in MDM at all | **none** | Apple | Nothing checks | **No boundary**, listed because its absence is the useful fact |

> ### OS-update delivery also depends on targeting
>
> The macOS 14 update label is computed from osquery results. A newly MDM-enrolled Mac that has never reported through fleetd cannot join it, and the older enforcement path also needs the agent. It therefore receives neither mechanism until the required agent data is available.
>
> A Mac that loses fleetd after joining the label can retain membership and continue receiving MDM enforcement. Dynamic membership is removed by a later false result; an error preserves it.
>
> The built-in iOS and iPadOS labels have no version predicate. They target all devices on those platforms, so the published iOS/iPadOS 17 baseline does not gate declaration delivery.

### Published host baselines

These are Fleet’s published host baselines at 4.90.0. Check the current supported-platform table before planning a deployment on a later release.

Fleet has no global enrollment gate enforcing this table. It describes the tested support baseline, while individual features have their own checks, including those listed above.

| Platform | Baseline |
|---|---|
| macOS | 14 and later |
| iOS and iPadOS | 17 and later |
| Windows | Pro and Enterprise 10 21H2 and later, Server 2012 and later |
| Linux | CentOS 7.1, Ubuntu 20.04, Fedora 38, Amazon Linux 2, Debian 11, RHEL 7, openSUSE 15.6, Arch, Omarchy |
| ChromeOS | 112.0.5615.134 and later |
| Android | 14 and later |

Below these baselines, Fleet may work partially or fully, but Fleet does not test or pursue bugs there. Windows 11 25H2 MDM additionally requires server 4.89.1; an older server can fail enrollment outright.

### Server floors

These server floors complement the agent requirements above. For Linux and Windows web setup, the agent checks that the server declares the capability before starting the flow.

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

Snapd recovery-key escrow requires compatibility in both directions. A current agent checks for the server capability before sending an escrow payload; repeatedly trying an unsupported server would churn the device’s key slot.

### Dependency floors

**MySQL 8.0.44.** Tested against 8.0.44, 8.4.8, and 9.5.0; 9.6.0 is incompatible at the reviewed release. The minimum moved from 8.0.36 during the 4.83 line. Check the supported versions before upgrading the database ([2.2](../02-administer-and-deploy-fleet/2.2-self-hosting-architecture-and-capacity.md)).

**Redis 6.2.** Required by the host-lookup cache on the agent authentication paths, which arrived in the 4.86 line. Fleet is actively tested against 6.2 and 7.

**Aurora MySQL 3.10.3.** This is the published minimum when using Aurora.

**`fleetctl` has no enforced server-version floor.** A mismatch produces a warning and the client continues. Pin the client version in automation and check compatibility when a command behaves unexpectedly ([6.4](../06-automate-fleet/6.4-use-fleetctl.md)).

<a id="runtime-fetched-moving-inputs"></a>

### Inputs refreshed at runtime

A pinned binary can still fetch newer runtime data. The Fleet MCP server built from 4.90.0 initially uses its embedded osquery schema, then attempts a refresh from Fleet’s `main` branch about two seconds after startup and every 24 hours by default. A successful fetch replaces the in-memory schema; failure retains the current copy ([6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md)).

| | |
|---|---|
| **Source** | Fleet's `main` branch, not the 4.90.0 tag |
| **Refresh interval** | 24 hours by default; set with `FLEET_MCP_SCHEMA_REFRESH_INTERVAL` (a Go duration such as `12h`) |
| **Failure behavior** | An unset or unparseable interval falls back to the 24-hour default rather than failing startup; the variable is read once at startup, so a change needs a restart |
| **Inspection** | Compare a column or table you rely on against the schema shipped in the 4.90.0 tag if you need to know whether it moved |
| **Pin the automatic refresh** | Set `FLEET_MCP_SCHEMA_REFRESH_DISABLE` to any non-empty value to stop the startup/periodic fetch and serve only the embedded snapshot, for a strictly release-pinned deployment |
| **Manual refresh still reaches out** | The variable above does not cover the `refresh_osquery_schema` tool: it calls the same GitHub fetch unconditionally whenever the assistant invokes it. To prevent all schema fetches, also block outbound access to `raw.githubusercontent.com` |

Track the MCP schema separately when reproducing a query-validation result. Fleet and the MCP server can share a release tag while the MCP server uses a newer schema.

<a id="fleet-publishes-support-scopes-and-no-dated-end-of-life"></a>

### Published support scopes

The 4.90.0 repository review found these release-relative support scopes and no dated end-of-life policy:

| | Bug fixes | Troubleshooting help |
|---|---|---|
| **Free** | Latest version only | Current major version |
| **Premium** | Latest version only | All versions |

Bug fixes are delivered in the latest release for both tiers, without backports. Applying a fix therefore requires an upgrade to the release containing it.

Older releases are outside the scope for fixes. On Free, previous major versions are also outside the troubleshooting scope. Premium’s all-version troubleshooting coverage provides help without promising backports or indefinite compatibility.

Plan remediation around the latest release and support access around your tier’s troubleshooting coverage. The reviewed policy provides no retirement date to schedule against.

This policy is published in Fleet’s company handbook.

Fleet’s guidance permits skipping server versions within version 4, and the server enforces no intermediate-release sequence. Agent updates have a separate exception: the update-server migration requires a bridge release ([3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md)).

Fleet's cadence, for planning: one minor and one patch release every three weeks, with scheduled patches weekly in between and immediate patches for critical bugs. [7.3](../07-operate-fleet/7.3-upgrade-fleet-and-fleetd.md) turns that into a release-review rhythm.
