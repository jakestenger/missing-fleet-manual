---
title: "Action-to-interface index"
chapter: "Appendices and indexes"
section: "A.5"
sidebar_position: 5
verified_against: Fleet 4.90.0
verified_on: 2026-09-02
verified_source: "drafted against fleet-v4.90.0 (7c428c6e46) from four independently built research columns, one per interface, each covering the register rows as they stood at first drafting. Every column was read at the tag; Fleet's documentation was used for leads only, never as evidence. The columns disagreed on 17 rows and those were reconciled against source before drafting. Reconciled 2026-09-01 to the then-current 354-capability register: six rows the index had not yet projected were added: CAP-048 restored as a distinct interface action, and the newer CAP-349 to CAP-353, with cells verified at the tag, CAP-354 (MCP) left as a documented exclusion, and the counts recounted from the table. Reconciled again 2026-09-02 to a.1's 360-capability register: CAP-361, CAP-362, CAP-363, CAP-364, CAP-365 and CAP-366, labelled from a.2's existing platform research, were added as Unsupported in every column, each for the reason its own row states; CAP-354 remains the sole documented exclusion, and the counts were recounted from the table again. Reconciled a third time 2026-09-02 (round4 RB3) to a.1's 361-capability register: CAP-372, provisioning a Mac's local account and syncing its password with the identity provider, was added scored Full and later corrected to Partial in every column, because setting the OAuth IdP through the UI's Account provisioning page, the REST API, `fleetctl` and GitOps only arms an outcome the Mac itself performs; the counts were recounted from the table again. Reconciled a fourth time 2026-09-02 (round4 RM9) to a.1's 362-capability register: CAP-373, requiring ACME/Managed Device Attestation for eligible Macs, was added scored Full in every column, because the checkbox, `mdm.apple_require_hardware_attestation` on the REST API's config endpoint, the same field via classic `fleetctl get/apply config`, and `controls.apple_require_hardware_attestation` in GitOps all read and write the one boolean identically, confirmed against fleetctl's own testdata fixtures; the counts and the derived narrative figures (Full/Partial totals, all-four-agree rows) were recounted from the table again. Reconciled a fifth time 2026-09-04 (round8) after two cells were rescored against the tag: CAP-279 (Windows enrollment prompt) `fleetctl` and GitOps moved from Not established to Full, because GitOps writes `controls.enable_turn_on_windows_mdm_manually` (pkg/spec/gitops.go) and classic `fleetctl apply` writes the same `mdm` key (server/service/client.go), and CAP-181 (keep the library's catalogue apps current) UI moved from Not established to Partial, because the UI arms the no-pin auto-update through the software title's Versions control the same way the other three interfaces do; the rows-with-any-Not-established total fell 72 to 70, the UI Not-established total 70 to 69, the Partial total rose 252 to 253, the more-than-one-column group 14 to 13, and section N was corrected 22 to 23 rows. Reconciled a sixth time 2026-09-05 (round11) after one cell pair was rescored against the tag: CAP-179 (ship different builds of one title to different hosts) `fleetctl` and GitOps moved from Not established to Full, because at fleet-v4.90.0 a title holds several content-hash-deduped packages (the `20260723181411_MultipleCustomPackagesPerTitle` migration and the `software_installers.dedup_token` unique key) and both classic `fleetctl apply` (`server/service/client.go` extractTmSpecsSoftwarePackages) and GitOps (`pkg/spec/gitops.go` Packages list) route that packages list, each package independently label-scoped, to the same `software/batch` handler the UI and REST API use; the rows-with-any-Not-established total fell 70 to 69, the more-than-one-column group 13 to 12, the `fleetctl` Full total rose 180 to 181 and GitOps Full 123 to 124 (Full-or-Partial reach 237 to 238 and 158 to 159), and the all-four-Full rows rose 84 to 85 with all-four-agree 105 to 106; the counts were recounted from the table again. Citation ledger at research/section-notes/a.5-notes.md"
further_reading:
  - https://fleetdm.com/docs/configuration/yaml-files
  - https://fleetdm.com/docs/rest-api/rest-api
feature_requests:
  labels: [":product"]
  match: ["GitOps", "fleetctl", "API", "UI"]
  exclude: []
---

# Action-to-interface index

![Reference](../_assets/icons/reference-light.svg) Use this index when choosing how to perform an action in Fleet. The UI, REST API, `fleetctl`, and GitOps cover much of the same work, with some practical differences: activity-feed reads need an interface other than a native `fleetctl` command, GitOps can manage a script library but cannot run scripts, and installer builds require `fleetctl`.

Find the action in the matrix, then check any limits described below before building it into a runbook or automation.

<a id="what-this-appendix-carries"></a>

## Coverage and related references

![Reference](../_assets/icons/reference-light.svg) The matrix maps 362 administrator actions from the capability register to the Fleet UI, REST API, `fleetctl`, and GitOps. A second table covers administrative actions initiated by Fleet, a device user, or an external system.

For commands and exit-status behavior, see [a.7](a.7-fleetctl-command-reference.md). Use [a.8](a.8-api-action-and-endpoint-reference.md) for API callers and access requirements, [a.3](a.3-configuration-model-and-precedence.md) for configuration precedence, [a.4](a.4-roles-and-permissions-matrix.md) for permissions, and [a.2](a.2-platform-capability-matrix.md) for platform support.

A `Full` cell means the interface can perform the action. Your account still needs the required permission.

This index focuses on each interface’s reach. Use the command and endpoint references for exact syntax, and check the version notes before applying an answer to a different Fleet release.

## How to read it

![Reference](../_assets/icons/reference-light.svg) The cells use these five values:

| Value | What it means |
|---|---|
| **Full** | The interface performs the action. |
| **Partial** | The interface performs part of the action and a stated boundary stops it. The boundary is either predictable from the interface model below or named in this appendix. |
| **Read only** | The interface can show you the current value and cannot change it. **This is a claim about the interface, not about Fleet.** Some of these values can be changed elsewhere and some cannot be changed anywhere. |
| **Unsupported** | The interface refuses or has no surface, and a positive boundary was found: a rendered refusal, a closed command tree, a closed request surface, a closed key vocabulary, or a route behind a credential an administrator does not hold. |
| **Not established** | The sources do not settle it. The record of what was searched is in the appendix's notes. |

These four conventions explain how the values apply:

For an action that consists entirely of reading, a complete response earns `Full`. `Read only` applies when the action includes a change that the interface cannot make, although it can display the current state.

A `Read only` cell does not guarantee another interface can make the change. Forty-eight rows have no `Full` or `Partial` cell, including seven that can be read somewhere. For example, changing log destinations or the two exposed host-freshness intervals requires a server restart with new process configuration ([a.3](a.3-configuration-model-and-precedence.md)).

An interface that enables an action but cannot perform it receives `Partial`. Examples include just-in-time account creation, attaching an end user’s identity to devices, and allowing a one-time conditional-access bypass. Fleet or the device user completes the action.

Device-owner pages use the device’s token rather than an administrator’s account. An action available only there is `Unsupported` in all four administrator columns. Installing all offered software and initiating Linux escrow are examples, even though both use a web page.

<a id="what-each-interface-is-and-the-boundary-that-decides-its-column"></a>

## How each interface is assessed

![Explanation](../_assets/icons/explanation-light.svg) These rules define what counts as support in each column.

<a id="fleetctl-api-is-not-fleetctl-support-gitops-apply-and-delete-are"></a>

### Native `fleetctl` commands and specification files

The `fleetctl` column includes commands that understand Fleet operations or specification files. Generic HTTP requests through `fleetctl api` are assessed under the REST API column.

`fleetctl api` builds an HTTP request from a URI you supply. It can reach endpoints without a corresponding native command, but you must provide the request and interpret the response. Forty-seven rows are reachable only this way through the client and remain `Unsupported` in its native-command column.

`fleetctl gitops`, `fleetctl apply`, and `fleetctl delete` count as native support. The client parses specifications and calls ordinary endpoints; there is no server-side GitOps engine. `apply` also supports two specification kinds outside the GitOps vocabulary. One hundred and one rows depend on one of these three commands.

For an API-backed operation, the native command handles Fleet-specific request construction. With `fleetctl api`, that work remains with the operator.

A `Full` cell under `fleetctl` may therefore require a YAML specification file. See [6.4](../06-automate-fleet/6.4-use-fleetctl.md) for client usage and [6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md) for repository workflows.

<a id="the-rest-api-column-counts-a-route-only-if-it-sits-behind-fleets-shared-user-authenticator"></a>

### REST routes available to an administrator token

The REST API column covers routes registered behind Fleet’s shared user authenticator, which checks the token belonging to a Fleet account. A route’s existence alone does not establish that an administrator can call it.

That authenticator has five registration sites in the server, plus a route family outside the versioned tree that also requires global administrator access. Other routes authenticate devices, agents, identity providers, or vendor callbacks, or require no authentication. [a.8](a.8-api-action-and-endpoint-reference.md) describes the six caller classes and their paths.

This caller boundary accounts for eighteen `Partial` answers where another caller performs part of the action, and fifteen `Unsupported` answers where only that caller can perform it. Examples include Linux escrow, self-service installation, conditional-access bypass, and enrollment protocols. An `Unsupported` REST cell can still have an HTTP route that requires a device or protocol credential.

<a id="the-ui-column-is-what-is-rendered-not-what-the-browser-received"></a>

### Controls and values rendered in the UI

The UI assessment checks both the endpoints requested by the browser and the components rendered at the pinned release.

Data returned to the browser counts only if a page displays it. Of the three log destinations in the configuration response, one is rendered in four places; the audit and osquery status destinations are not rendered. You can read those two through REST or `fleetctl`, but their UI cells are `Unsupported`.

<a id="gitops-has-no-read-direction-at-all"></a>

### GitOps writes declared state

`fleetctl gitops` produces an apply log and two status lines. It has no read, export, or report command, so this column has no `Read only` cells.

Of the eighteen rows with a `Read only` cell elsewhere, twelve are unsupported in GitOps because the underlying data has no declarative form.

The other six have writable GitOps configuration: local-account collection (CAP-088), software inventory and its fleet-level toggle (CAP-122, CAP-123), fleet-scoped labels (CAP-143), and update prompts on older Macs (CAP-206) are `Full` in GitOps despite a `Read only` UI cell. App Store purchasing and distribution (CAP-275) is `Partial` in GitOps and `Read only` in `fleetctl`. Assess each column independently.

GitOps accepts ten top-level keys and validates nested keys against its schema. Unknown keys fail with spelling suggestions. `--allow-unknown-keys` changes those errors to warnings but still drops the keys. The schema defines which configuration GitOps can express.

GitOps cannot perform reads or immediate actions such as locking a device, running a script, wiping a phone, or signing in. All 23 rows in section N fall outside its supported operations.

<a id="the-mcp-server-is-not-a-column-here"></a>

### MCP tools use a separate reference

The Fleet MCP server lets an AI assistant call a fixed subset of REST operations. See [A.11](a.11-mcp-tool-reference.md) for its twenty tools across hosts, queries, policies and vulnerabilities, and inventory. The token’s role further limits their access. MCP has no separate column here; [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md) covers setup.

The MCP server has no delete-host tool, generic REST passthrough, or configuration-writing tool. Use A.11 to check the exact tool list and 6.6 for the proxy and destructive-tool controls.

<a id="five-boundaries-worth-knowing-before-you-plan"></a>

## Limits to check before planning a workflow

![Troubleshooting](../_assets/icons/troubleshooting-light.svg) These five cases often affect how a workflow needs to be built.

> ### Check omission behavior before applying GitOps changes
>
> Removing a YAML key can clear settings, enable a default, preserve a value, or reject the file. The rule depends on the key and scope; [a.3](a.3-configuration-model-and-precedence.md) describes the configuration paths.
>
> Omitting `policies:`, `reports:`, or `org_settings.yara_rules` deletes those objects in scope. Omitting `controls:` from a named fleet file resets controls, including profile removal and disabling disk encryption. Across global and unassigned files, exactly one must define `controls`; both or neither is an error. When only the unassigned file defines it, those controls apply globally.
>
> Omitted `features.enable_software_inventory`, `enable_host_users`, and historical-data keys default to `true` on each apply. Re-enabling vulnerability history restarts collection but does not restore rows scrubbed while it was disabled. An omitted `controls.macos_updates.update_new_hosts` is derived as enabled when both a minimum version and deadline are set.
>
> Other omitted `org_settings` keys retain stored values unless the client supplies a replacement block. Four additional cases need care:
>
> - `labels[].hosts` distinguishes absence, which preserves membership, from explicit null, which clears it.
> - `$FLEET_SECRET_` values are upsert-only. Removing a reference leaves the stored secret, and values are transmitted even during a dry run.
> - A global file without an unassigned-scope file causes the client to apply an empty configuration to the unassigned scope.
> - `agent_options` is required in global and named-fleet files. In an unassigned-scope file it is unsupported: a supplied value is ignored with a warning, and omission changes nothing.
>
> A dry run does not validate reports, labels, packs, policies, or user roles. Review those changes separately before applying.

> ### Packaging and local setup require `fleetctl`
>
> Native client workflows cover installer builds, enabling scripts at packaging time, hardware-backed host identity certificates, Windows install-time URL and secret inputs, local update channels, disabling agent updates, macOS packages without credentials, a self-hosted agent update repository, and GitOps CI scaffolding. These build and setup actions have no matching UI, REST, or GitOps surface.
>
> An agent packaged with updates disabled or certificate verification skipped retains that behavior until its package is replaced on the host.
>
> The Docker Compose command is more limited: it starts an evaluation sandbox at a fixed local address. It is not a general deployment-management command.

> ### UI controls with limited reach
>
> The UI runs scripts from the library, including across multiple hosts. It cannot accept pasted script contents for an ad-hoc run; Fleet directs that input to the command line.
>
> Software inventory can be enabled or disabled through REST, `fleetctl`, or GitOps. The UI reads the setting to choose what to display but has no toggle at either scope.
>
> The UI’s disk-encryption switch sends one value for FileVault and BitLocker together. Plan for both platforms when using it during a staged rollout.

> ### Plan an interactive enrollment step for Android and ChromeOS
>
> The UI is the only supported administrator interface in four enrollment rows: Android personal work profiles, company-owned Android QR enrollment, the single-use Android token, and Chromebook enrollment.
>
> Include that interactive step in your rollout plan before automating later management. See [3.6](../03-connect-devices/3.6-enroll-android-devices.md) and [3.7](../03-connect-devices/3.7-enroll-chromeos-devices.md) for the workflows.

> ### Apple credential renewal spans several interfaces
>
> `fleetctl` can request an Apple push-certificate signing request and Apple Business public key. It cannot upload their renewed counterparts or a Volume Purchasing token. Include Apple’s browser-based steps and the Fleet upload step in your renewal procedure.
>
> GitOps can assign default fleets to an uploaded token, but cannot upload, renew, or delete it. The matrix scores renewal `Full` in the UI and REST API and `Read only` in `fleetctl`. [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) covers the complete workflow.

## What decides a `Partial` cell

![Explanation](../_assets/icons/explanation-light.svg) The matrix has 253 `Partial` cells. The limits tend to follow these patterns:

For REST, part of the action usually requires a device, agent, or protocol caller. An administrator can configure or initiate the workflow without performing its device-side steps.

For `fleetctl`, common limits are build-time settings that cannot be changed later, one-sided credential workflows, fixed page sizes, and omitted default-output fields. For example, the MDM queue command returns twenty entries, and default account output leaves fleet-scoped roles blank. Check the command reference before treating either output as a complete review.

For GitOps, configuration and execution are separate. It can manage scripts without running them, define custom host vitals without setting per-host values, and configure a fleet without assigning its administrators. Ticketing integrations can be defined globally, but the server rejects attempts to enable them per fleet.

For the UI, `Partial` usually reflects a platform subset, a licence-hidden control, or a workflow split between administrator and device-owner pages.

## Where exactly one interface can do it

![Reference](../_assets/icons/reference-light.svg) These counts include `Full` and `Partial` as support. They exclude `Read only`, `Unsupported`, and unresolved answers.

| Interface | Rows where it is the only one | What they are |
|---|---|---|
| **REST API** | 16 | Identity-provider driven removal, several diagnostic and introspection reads, re-arming a policy's automations, and the Linux escrow surfaces |
| **`fleetctl`** | 10 | Packaging, the self-hosted update repository, and repository scaffolding. See the build and setup workflows above |
| **UI** | 4 | Android and ChromeOS enrollment |
| **GitOps** | 0 | All supported actions are also available through another interface |

Forty-eight rows have no `Full` or `Partial` interface. Most concern server process configuration or deployment infrastructure; six concern device-owner pages or local host operations. Seven of the forty-eight can be read through an interface even though none of the four can perform the change.

## The matrix

![Reference](../_assets/icons/reference-light.svg) The 362 rows below are grouped by administrative task. Bold section rows separate the groups; counts follow the matrix.

| ID | Action | UI | REST API | `fleetctl` | GitOps |
|---|---|---|---|---|---|
| **A. Identity, access, and governance** | | | | | |
| **CAP-001** | Sign in to Fleet with a Fleet password | Full | Unsupported | Full | Unsupported |
| **CAP-002** | Sign in through the organisation's identity provider | Full | Partial | Partial | Partial |
| **CAP-003** | Have Fleet create the account on first IdP sign-in | Partial | Partial | Partial | Partial |
| **CAP-004** | Remove Fleet accounts when people leave, from the IdP | Read only | Full | Unsupported | Unsupported |
| **CAP-005** | Have SCIM skip accounts it must not delete | Not established | Full | Unsupported | Unsupported |
| **CAP-006** | Challenge a sign-in with an emailed second factor | Full | Partial | Partial | Unsupported |
| **CAP-007** | Create or modify a user and give it a global role | Full | Full | Full | Unsupported |
| **CAP-008** | Give a user the Technician, Observer+ or GitOps role | Partial | Full | Full | Unsupported |
| **CAP-009** | Give a user a role scoped to one or more fleets | Full | Full | Full | Unsupported |
| **CAP-010** | Create an API-only identity for automation | Full | Full | Full | Unsupported |
| **CAP-011** | Give an API-only identity a fleet role | Full | Full | Full | Unsupported |
| **CAP-012** | Restrict an API-only identity to named API endpoints | Full | Partial | Unsupported | Unsupported |
| **CAP-013** | Add or remove a member of a fleet | Full | Full | Full | Unsupported |
| **CAP-014** | Make managed settings read-only in the interface | Full | Full | Full | Full |
| **CAP-015** | Read the organisation-wide activity feed | Full | Full | Unsupported | Unsupported |
| **CAP-016** | Read one host's activity feed | Full | Full | Unsupported | Unsupported |
| **CAP-017** | Read the work still queued for a host | Partial | Full | Unsupported | Unsupported |
| **CAP-018** | POST every activity to a URL as it happens | Full | Full | Full | Full |
| **CAP-019** | Stream activities to an audit-log destination | Unsupported | Read only | Read only | Unsupported |
| **CAP-020** | Know which activities never reach a streamed destination | Not established | Partial | Unsupported | Unsupported |
| **CAP-021** | Set how long Fleet keeps activity records | Full | Full | Full | Full |
| **CAP-022** | Keep a host's activity history across an Apple ADE re-enrollment | Full | Full | Full | Full |
| **CAP-023** | Read a disk-encryption recovery key | Full | Full | Unsupported | Unsupported |
| **CAP-024** | Have the read of a secret recorded as an event | Read only | Full | Unsupported | Unsupported |
| **CAP-349** | Connect a certificate authority | Full | Full | Full | Full |
| **B. Enrollment and host lifecycle** | | | | | |
| **CAP-025** | Create and hold enroll secrets for a scope | Full | Full | Full | Full |
| **CAP-026** | Rotate an enroll secret without a flag day | Full | Full | Full | Full |
| **CAP-027** | Enroll a Mac in MDM automatically during Setup Assistant | Full | Partial | Partial | Partial |
| **CAP-028** | Enroll a Mac in MDM from a link, company-owned | Full | Partial | Unsupported | Unsupported |
| **CAP-029** | Enroll a personally owned device from a link | Full | Partial | Unsupported | Unsupported |
| **CAP-030** | Download an unsigned manual macOS enrollment profile | Partial | Full | Unsupported | Unsupported |
| **CAP-031** | Download the default Setup Assistant profile | Full | Full | Read only | Unsupported |
| **CAP-032** | Have Fleet install the agent on a Mac it enrolls | Not established | Unsupported | Full | Full |
| **CAP-033** | Suppress Fleet's ADE agent install so a bootstrap package delivers it | Full | Full | Full | Full |
| **CAP-034** | Attach the end user's identity at enrollment | Full | Full | Full | Full |
| **CAP-035** | Enroll a Windows host by installing the agent | Partial | Partial | Partial | Unsupported |
| **CAP-036** | Enroll a Windows host at first boot through Autopilot | Partial | Partial | Partial | Partial |
| **CAP-037** | Let a person enroll a Windows host from Settings | Full | Partial | Partial | Partial |
| **CAP-038** | Stop Fleet enrolling Windows hosts unasked | Full | Full | Full | Full |
| **CAP-039** | Move Windows hosts off another MDM with no user interaction | Full | Full | Full | Full |
| **CAP-040** | Prompt a Mac's user to migrate from another MDM | Full | Unsupported | Full | Full |
| **CAP-041** | Have Fleet push the agent to an Entra-enrolled Windows host | Not established | Unsupported | Unsupported | Unsupported |
| **CAP-042** | Enroll a Linux host | Partial | Unsupported | Partial | Unsupported |
| **CAP-043** | Re-point or reconfigure a deployed Linux agent without rebuilding | Not established | Partial | Unsupported | Unsupported |
| **CAP-044** | Build a macOS package that carries no URL or secret | Not established | Unsupported | Full | Unsupported |
| **CAP-045** | Supply a Windows host's URL, secret and flags at install time | Not established | Unsupported | Partial | Unsupported |
| **CAP-046** | Enroll an iPhone or iPad automatically | Full | Partial | Partial | Partial |
| **CAP-047** | Enroll an iPhone or iPad from a link, company-owned | Full | Partial | Unsupported | Unsupported |
| **CAP-048** | Enroll a personally owned iPhone or iPad | Full | Partial | Unsupported | Unsupported |
| **CAP-049** | Have a person enroll their own device with a Managed Apple Account | Partial | Partial | Partial | Partial |
| **CAP-050** | Register Fleet's Apple service-discovery URL | Not established | Partial | Unsupported | Unsupported |
| **CAP-051** | Place an ADE device in a fleet by platform | Full | Full | Full | Full |
| **CAP-052** | Enroll an Android device as a personal work profile | Full | Unsupported | Unsupported | Unsupported |
| **CAP-053** | Enroll a company-owned Android device by QR at first boot | Partial | Unsupported | Unsupported | Unsupported |
| **CAP-054** | Issue a single-use Android enrollment token | Partial | Unsupported | Unsupported | Unsupported |
| **CAP-055** | Enroll a Chromebook | Partial | Unsupported | Unsupported | Unsupported |
| **CAP-056** | Give a host a hardware-backed identity certificate | Not established | Unsupported | Full | Unsupported |
| **CAP-057** | Require signed requests from every host | Not established | Unsupported | Unsupported | Unsupported |
| **CAP-058** | Recognise a returning device and keep its host record | Not established | Unsupported | Unsupported | Unsupported |
| **CAP-059** | Enroll two operating systems on one machine as two hosts | Partial | Unsupported | Full | Unsupported |
| **CAP-060** | Move a host to another fleet | Full | Full | Full | Unsupported |
| **CAP-061** | Delete a host record | Full | Full | Unsupported | Unsupported |
| **CAP-062** | Retire a host so it stays retired | Partial | Partial | Unsupported | Unsupported |
| **CAP-063** | Expire host records automatically after a silence window | Full | Full | Full | Full |
| **C. Agent (fleetd) management** | | | | | |
| **CAP-064** | Build an installer for a platform | Unsupported | Unsupported | Full | Unsupported |
| **CAP-065** | Include the end-user surface in the agent | Unsupported | Partial | Full | Unsupported |
| **CAP-066** | Enable scripts on a host at packaging time | Unsupported | Unsupported | Full | Unsupported |
| **CAP-067** | Set an agent's update channel centrally | Full | Full | Full | Full |
| **CAP-068** | Set an agent's update channel on the host | Not established | Unsupported | Partial | Unsupported |
| **CAP-069** | Pin an agent component to an exact version | Full | Full | Full | Full |
| **CAP-070** | Roll an agent version backwards across the estate | Full | Full | Full | Full |
| **CAP-071** | Stop an agent updating at all | Not established | Unsupported | Full | Unsupported |
| **CAP-072** | Publish agent versions from your own update repository | Not established | Unsupported | Full | Unsupported |
| **CAP-073** | See what agent version a host is actually running | Full | Full | Full | Unsupported |
| **CAP-364** | Force an agent update check without waiting for the interval | Unsupported | Unsupported | Unsupported | Unsupported |
| **CAP-074** | Deliver an osquery extension to hosts | Full | Partial | Full | Full |
| **CAP-075** | Restrict an extension to a label | Full | Full | Full | Full |
| **CAP-076** | Set osquery runtime options for a fleet | Partial | Partial | Full | Full |
| **CAP-077** | Set Orbit's own settings for a fleet | Partial | Full | Full | Full |
| **CAP-078** | Turn on file integrity monitoring | Full | Full | Full | Full |
| **CAP-079** | Scan hosts with YARA signature sets | Full | Full | Full | Full |
| **CAP-080** | Stamp results with provenance columns | Full | Full | Full | Full |
| **CAP-081** | Turn individual osquery event subscribers on or off | Full | Full | Full | Full |
| **CAP-082** | Carve a file off a host | Unsupported | Partial | Partial | Unsupported |
| **D. Host data, vitals, and inventory** | | | | | |
| **CAP-083** | See what a device is and what is on it | Full | Partial | Full | Unsupported |
| **CAP-084** | Put a value you collect on the host record | Not established | Partial | Full | Full |
| **CAP-085** | Record a value Fleet cannot collect | Full | Full | Partial | Partial |
| **CAP-086** | Turn a SQLite file on the device into a queryable table | Full | Full | Full | Full |
| **CAP-087** | Replace or remove one of Fleet's own detail queries | Not established | Partial | Full | Full |
| **CAP-088** | Collect the local accounts on a device | Read only | Partial | Full | Full |
| **CAP-089** | See which certificates a host holds | Partial | Full | Unsupported | Unsupported |
| **CAP-090** | Attach an email address to a host | Partial | Partial | Partial | Unsupported |
| **CAP-091** | Ask a host to report again now | Full | Full | Unsupported | Unsupported |
| **CAP-092** | Refresh an iPhone or iPad's inventory on a schedule | Not established | Partial | Partial | Unsupported |
| **E. Queries and reports** | | | | | |
| **CAP-093** | Ask every online device a question now | Full | Full | Full | Unsupported |
| **CAP-094** | Save a question without running it on a schedule | Full | Full | Full | Full |
| **CAP-095** | Collect a question's answer on a schedule | Full | Full | Full | Full |
| **CAP-096** | Keep the newest result per host in Fleet | Full | Full | Full | Full |
| **CAP-097** | Send a report's results to a log destination | Full | Partial | Partial | Partial |
| **CAP-098** | Read a report's results across the estate | Full | Full | Unsupported | Unsupported |
| **CAP-099** | Read one host's result, including a successful empty one | Full | Full | Unsupported | Unsupported |
| **CAP-100** | Retrieve stored report rows for export | Full | Full | Unsupported | Unsupported |
| **CAP-101** | Keep a report away from platforms whose tables do not exist | Full | Full | Full | Full |
| **CAP-102** | Keep a report away from agents too old to run it | Full | Full | Full | Full |
| **CAP-103** | Run a report on a percentage of its targets | Partial | Partial | Unsupported | Unsupported |
| **CAP-104** | Narrow a report to hosts carrying a label | Full | Full | Full | Full |
| **CAP-105** | Let an observer run a chosen report | Full | Full | Full | Full |
| **CAP-106** | Turn live reports off for the whole server | Full | Full | Full | Full |
| **CAP-107** | Stop storing report results server-wide | Full | Full | Full | Full |
| **CAP-108** | Stop storing one report's results | Full | Full | Full | Full |
| **CAP-109** | Cap how many report rows Fleet keeps across hosts | Not established | Partial | Full | Full |
| **CAP-110** | See what a report costs the estate | Partial | Full | Unsupported | Unsupported |
| **CAP-111** | Collect per-host query statistics at all | Not established | Unsupported | Unsupported | Unsupported |
| **CAP-112** | Bound what a query may cost a host | Full | Full | Full | Full |
| **CAP-113** | Let, or refuse to let, osquery stop an expensive query | Partial | Partial | Partial | Partial |
| **CAP-351** | Retire a legacy 2017 query pack | Partial | Full | Full | Unsupported |
| **F. Policies** | | | | | |
| **CAP-114** | Ask a yes-or-no compliance question of every host | Full | Full | Full | Full |
| **CAP-115** | Assert that a Fleet-maintained app is at or above a version | Partial | Partial | Full | Full |
| **CAP-116** | Scope a policy to a platform | Full | Full | Full | Full |
| **CAP-117** | Narrow a policy by label | Full | Full | Full | Full |
| **CAP-118** | Mark a policy as one whose failure matters | Full | Full | Full | Full |
| **CAP-119** | Read how many hosts pass and fail a policy | Full | Full | Unsupported | Unsupported |
| **CAP-120** | Clear a policy's collected results | Full | Partial | Unsupported | Unsupported |
| **CAP-121** | Re-arm a policy's webhook and ticket automations | Unsupported | Partial | Unsupported | Unsupported |
| **G. Software and vulnerability knowledge** | | | | | |
| **CAP-122** | Collect what software is installed | Read only | Full | Full | Full |
| **CAP-123** | Turn software inventory on for one fleet | Read only | Partial | Full | Full |
| **CAP-124** | See which installed software has known vulnerabilities | Full | Full | Full | Unsupported |
| **CAP-125** | See which operating system builds have known vulnerabilities | Full | Full | Unsupported | Unsupported |
| **CAP-126** | Prioritise findings by severity and exploitation | Full | Partial | Full | Unsupported |
| **CAP-127** | Filter and sort by those fields | Full | Partial | Unsupported | Unsupported |
| **CAP-128** | See the version that fixes a finding | Full | Partial | Full | Unsupported |
| **CAP-129** | See whether exposure is rising or falling | Partial | Full | Unsupported | Partial |
| **CAP-130** | Stop collecting a history dataset | Full | Full | Full | Full |
| **CAP-131** | Browse what Fleet knows how to install | Full | Full | Unsupported | Unsupported |
| **CAP-132** | Supply vulnerability data yourself | Not established | Partial | Partial | Partial |
| **H. Estate-wide reading and targeting** | | | | | |
| **CAP-133** | Read the estate's headline counts | Full | Full | Unsupported | Unsupported |
| **CAP-134** | Read how many hosts are low on disk | Full | Partial | Unsupported | Unsupported |
| **CAP-135** | See how many automated enrollments are not healthy | Full | Full | Unsupported | Unsupported |
| **CAP-136** | See which hosts were online over time | Full | Full | Unsupported | Unsupported |
| **CAP-137** | Hand a population to somebody who does not use Fleet | Full | Full | Unsupported | Unsupported |
| **CAP-138** | Read the host list programmatically | Full | Partial | Partial | Unsupported |
| **CAP-139** | Be told when too much of the estate goes quiet | Full | Full | Full | Full |
| **CAP-140** | Select hosts by a query that keeps itself current | Full | Full | Full | Full |
| **CAP-141** | Select a specific list of hosts | Full | Full | Full | Full |
| **CAP-142** | Select hosts by a reported vital | Full | Partial | Full | Full |
| **CAP-143** | Confine a label to one fleet | Read only | Partial | Full | Full |
| **CAP-144** | Give a group of devices its own configuration and its own administrators | Full | Full | Partial | Partial |
| **CAP-145** | Rename a label safely | Full | Full | Partial | Partial |
| **CAP-350** | Enumerate every outbound destination Fleet reaches | Not established | Not established | Not established | Unsupported |
| **I. Configuration profiles and declarative settings** | | | | | |
| **CAP-146** | Put a setting on an Apple device and keep it there | Full | Full | Full | Full |
| **CAP-147** | Let an Apple device hold and report its own desired state | Full | Full | Full | Full |
| **CAP-148** | Put a setting on a Windows device | Full | Full | Full | Full |
| **CAP-149** | Configure an Android device | Full | Full | Full | Full |
| **CAP-150** | Give one fleet its own profiles | Full | Full | Full | Full |
| **CAP-151** | Narrow a profile to hosts carrying a label | Full | Partial | Full | Full |
| **CAP-152** | Fill in a per-host value in a profile | Full | Partial | Full | Full |
| **CAP-153** | Have a profile enrol a certificate | Full | Full | Full | Full |
| **CAP-154** | Supply a value that is never stored anywhere | Not established | Full | Full | Full |
| **CAP-372** | Provision a Mac's local account and sync its password with the identity provider | Partial | Partial | Partial | Partial |
| **CAP-155** | Keep a credential out of a profile's stored content | Full | Full | Full | Partial |
| **CAP-156** | Know whether a profile reached a device | Full | Partial | Unsupported | Unsupported |
| **CAP-157** | Send a profile to a host again | Partial | Partial | Unsupported | Unsupported |
| **CAP-158** | Take a profile off devices | Full | Partial | Full | Full |
| **J. Scripts** | | | | | |
| **CAP-159** | Run a one-off script on a device | Unsupported | Full | Full | Unsupported |
| **CAP-160** | Keep a script in a library and run it | Full | Full | Full | Partial |
| **CAP-161** | Wait for a script's result | Partial | Full | Full | Unsupported |
| **CAP-162** | Run a script across many hosts at once | Full | Full | Unsupported | Unsupported |
| **CAP-163** | Stop every script running anywhere | Full | Full | Full | Full |
| **CAP-164** | Let a script run for longer than five minutes | Full | Full | Full | Full |
| **CAP-165** | Read what a script did | Full | Full | Full | Unsupported |
| **CAP-166** | Use a credential in a script without storing it | Full | Partial | Full | Partial |
| **CAP-167** | Use a host's own vital inside an install or script | Full | Full | Full | Full |
| **K. Software delivery** | | | | | |
| **CAP-168** | Deliver software you package yourself | Partial | Full | Full | Full |
| **CAP-169** | Deliver an application from Fleet's catalogue | Full | Full | Full | Full |
| **CAP-170** | Deliver a purchased App Store application | Full | Full | Full | Full |
| **CAP-171** | Make a Play application available | Partial | Full | Full | Full |
| **CAP-172** | Deliver an app you built yourself to iPhones and iPads | Full | Full | Full | Full |
| **CAP-173** | Put a shortcut to a URL on an Android device | Partial | Full | Partial | Partial |
| **CAP-174** | Deliver a `.sh`, `.ps1` or `.py` as a package | Full | Full | Full | Full |
| **CAP-175** | Gate an install on a condition the device reports | Full | Full | Full | Full |
| **CAP-176** | Have Fleet write the install and uninstall logic for you | Full | Full | Full | Full |
| **CAP-177** | Install software on a host | Full | Partial | Unsupported | Unsupported |
| **CAP-178** | Uninstall software from a host, as an administrator | Full | Partial | Unsupported | Unsupported |
| **CAP-179** | Ship different builds of one title to different hosts | Full | Full | Full | Full |
| **CAP-180** | Hold a catalogue app at a version | Full | Full | Full | Full |
| **CAP-181** | Keep the library's catalogue apps current | Partial | Partial | Partial | Partial |
| **CAP-182** | Go back to the previous catalogue version | Full | Full | Full | Full |
| **CAP-183** | Configure a managed application on an Apple device | Partial | Partial | Full | Full |
| **CAP-184** | Configure a managed application on Android | Full | Full | Full | Full |
| **CAP-185** | Choose when apps update on a device | Full | Partial | Full | Full |
| **CAP-186** | Remove something from the library | Full | Full | Full | Full |
| **CAP-187** | Serve installers to hosts through a CDN | Not established | Unsupported | Unsupported | Unsupported |
| **CAP-188** | Accept a very large installer | Not established | Unsupported | Unsupported | Unsupported |
| **CAP-352** | Retry a failed software install or uninstall by hand | Full | Full | Unsupported | Unsupported |
| **CAP-366** | Choose whether a Play application is offered as self-service | Unsupported | Unsupported | Unsupported | Unsupported |
| **L. Setup and self-service experiences** | | | | | |
| **CAP-189** | Prepare a device before its user starts using it | Full | Full | Full | Full |
| **CAP-190** | Run a script as part of setup | Partial | Full | Full | Full |
| **CAP-191** | Deliver a package to a Mac before the agent exists | Full | Full | Full | Full |
| **CAP-192** | Create the user's local account during setup | Not established | Full | Full | Full |
| **CAP-193** | Show the user an agreement during setup | Full | Partial | Full | Full |
| **CAP-194** | Hold a Windows device at a status page until setup finishes | Partial | Partial | Partial | Partial |
| **CAP-195** | Show setup progress without holding anyone up | Read only | Unsupported | Unsupported | Unsupported |
| **CAP-196** | Install software during an automated Apple enrollment | Full | Full | Full | Full |
| **CAP-197** | Push an app to an Android device at enrollment | Full | Full | Full | Full |
| **CAP-198** | Install setup software only on devices that need it | Not established | Full | Full | Full |
| **CAP-199** | Stop setup when a piece of software fails | Full | Full | Full | Full |
| **CAP-200** | Take release of a Mac or iPhone into your own hands | Full | Full | Full | Full |
| **CAP-201** | Retry only the setup steps that failed | Not established | Unsupported | Unsupported | Unsupported |
| **CAP-202** | Offer software for people to install themselves | Full | Full | Full | Full |
| **CAP-203** | Group a large self-service catalogue | Full | Full | Full | Full |
| **CAP-204** | Let a user install everything offered to them | Unsupported | Unsupported | Unsupported | Unsupported |
| **CAP-353** | Retrieve or rotate the managed local administrator password | Full | Full | Unsupported | Unsupported |
| **CAP-361** | Let an end user see their own device's details and software | Unsupported | Unsupported | Unsupported | Unsupported |
| **CAP-362** | Let an end user see the summary the desktop menu shows | Unsupported | Unsupported | Unsupported | Unsupported |
| **CAP-365** | Let an end user uninstall their own software | Unsupported | Unsupported | Unsupported | Unsupported |
| **M. Operating system updates** | | | | | |
| **CAP-205** | Require a minimum OS version by a date on Apple devices | Full | Partial | Full | Full |
| **CAP-206** | Prompt users on older Macs to update | Read only | Partial | Full | Full |
| **CAP-207** | Set an update deadline and restart grace on Windows | Full | Full | Full | Full |
| **CAP-208** | Control Android system updates | Partial | Full | Full | Full |
| **CAP-209** | Express an update policy the built-in form cannot | Full | Full | Full | Full |
| **CAP-210** | Update a Mac or iPhone during automated enrollment | Partial | Partial | Full | Full |
| **CAP-211** | Enforce a Linux OS version | Unsupported | Unsupported | Unsupported | Unsupported |
| **CAP-212** | See whether devices actually reached the version | Partial | Partial | Partial | Unsupported |
| **N. Device actions and MDM commands** | | | | | |
| **CAP-213** | Lock a Mac | Full | Full | Full | Unsupported |
| **CAP-214** | Lock an iPhone or iPad | Full | Full | Full | Unsupported |
| **CAP-215** | Lock a Windows host | Full | Full | Full | Unsupported |
| **CAP-216** | Lock a Linux host | Full | Full | Full | Unsupported |
| **CAP-217** | Lock an Android device | Full | Full | Full | Unsupported |
| **CAP-218** | Release a locked Mac | Partial | Partial | Partial | Unsupported |
| **CAP-219** | Release a locked iPhone or iPad | Full | Full | Full | Unsupported |
| **CAP-220** | Release a locked Windows host | Full | Full | Full | Unsupported |
| **CAP-221** | Release a locked Linux host | Full | Full | Full | Unsupported |
| **CAP-222** | Release a locked Android device | Unsupported | Unsupported | Unsupported | Unsupported |
| **CAP-223** | Erase a Mac | Full | Full | Full | Unsupported |
| **CAP-224** | Erase an iPhone or iPad | Full | Full | Full | Unsupported |
| **CAP-225** | Erase a Windows host | Full | Full | Full | Unsupported |
| **CAP-226** | Erase a Linux host | Full | Full | Full | Unsupported |
| **CAP-227** | Erase a company-owned Android device | Full | Full | Full | Unsupported |
| **CAP-228** | Remove Fleet's management from a personally owned Android device | Full | Full | Unsupported | Unsupported |
| **CAP-229** | Find where a device is | Full | Partial | Unsupported | Unsupported |
| **CAP-230** | Clear a device's passcode | Full | Partial | Full | Unsupported |
| **CAP-370** | Turn Fleet's device management off for one host | Full | Full | Unsupported | Unsupported |
| **CAP-231** | Send a raw command to Apple devices | Unsupported | Full | Full | Unsupported |
| **CAP-232** | Send a raw command to Windows devices | Unsupported | Full | Full | Unsupported |
| **CAP-233** | Read what a device said about a command | Partial | Partial | Partial | Unsupported |
| **CAP-234** | Cancel a device action before it happens | Partial | Partial | Unsupported | Unsupported |
| **O. Disk encryption and recovery credentials** | | | | | |
| **CAP-235** | Turn FileVault on and hold the recovery key | Full | Full | Partial | Full |
| **CAP-236** | Turn BitLocker on and hold the protector | Full | Full | Partial | Full |
| **CAP-237** | Hold a recovery credential for an already-encrypted Linux host | Unsupported | Partial | Unsupported | Unsupported |
| **CAP-238** | Escrow silently on a TPM-backed Ubuntu host | Not established | Partial | Unsupported | Unsupported |
| **CAP-239** | Escrow by prompting the user for their LUKS passphrase | Full | Partial | Unsupported | Unsupported |
| **CAP-240** | Know whether a disk is encrypted at all | Full | Partial | Full | Unsupported |
| **CAP-241** | Read the disk-encryption status summary | Full | Full | Unsupported | Unsupported |
| **CAP-242** | Set a BitLocker startup PIN | Full | Partial | Full | Full |
| **CAP-243** | Allow a custom disk-encryption profile alongside Fleet's own | Not established | Unsupported | Unsupported | Unsupported |
| **CAP-244** | Protect a Mac's recovery environment | Full | Full | Partial | Full |
| **CAP-245** | Stop enforcing encryption without losing what is held | Full | Full | Full | Full |
| **P. Policy automations, integrations, and outbound events** | | | | | |
| **CAP-246** | Install software when a policy fails | Full | Full | Full | Full |
| **CAP-247** | Install an App Store app when a policy fails | Full | Full | Full | Full |
| **CAP-248** | Run a script when a policy fails | Full | Full | Full | Full |
| **CAP-249** | POST to a URL when hosts start failing a policy | Full | Full | Full | Full |
| **CAP-250** | Open a ticket when hosts start failing a policy | Full | Full | Partial | Partial |
| **CAP-251** | Book a maintenance window on the user's calendar | Full | Partial | Full | Full |
| **CAP-252** | Report a host as non-compliant to Microsoft Entra | Full | Full | Full | Full |
| **CAP-253** | Refuse a sign-in when a host is failing a policy | Full | Full | Full | Full |
| **CAP-254** | Grant a one-time bypass of conditional access | Partial | Partial | Partial | Partial |
| **CAP-255** | Act on every failing result rather than on the transition | Full | Full | Full | Full |
| **CAP-256** | POST when a new vulnerability is detected | Full | Partial | Partial | Partial |
| **CAP-257** | Send osquery status and result logs to a destination | Read only | Read only | Read only | Unsupported |
| **CAP-258** | Block webhook destinations on internal addresses | Not established | Unsupported | Unsupported | Unsupported |
| **Q. Automation interfaces** | | | | | |
| **CAP-259** | Apply declared configuration from a repository | Unsupported | Partial | Full | Full |
| **CAP-260** | Validate configuration before applying it | Unsupported | Partial | Partial | Partial |
| **CAP-261** | Delete fleets that are not in the repository | Not established | Partial | Full | Partial |
| **CAP-262** | Decide whether omitting a section deletes what it describes | Full | Full | Unsupported | Unsupported |
| **CAP-263** | Turn an existing deployment into YAML | Not established | Partial | Full | Unsupported |
| **CAP-264** | Make Fleet do anything an administrator can do | Partial | Full | Partial | Unsupported |
| **CAP-265** | Do supported work from a shell | Unsupported | Partial | Full | Unsupported |
| **CAP-266** | Reach a route `fleetctl` has no command for | Unsupported | Full | Full | Unsupported |
| **CAP-267** | Apply or delete a one-off spec file | Partial | Full | Full | Unsupported |
| **CAP-268** | Generate a CI pipeline for GitOps | Not established | Unsupported | Full | Unsupported |
| **R. Platform management configuration (Apple, Windows, Android)** | | | | | |
| **CAP-269** | Turn on Apple device management | Full | Full | Partial | Unsupported |
| **CAP-270** | Renew the Apple push certificate without resetting the estate | Full | Full | Partial | Unsupported |
| **CAP-271** | Have Fleet re-issue each host's identity certificate | Not established | Unsupported | Unsupported | Unsupported |
| **CAP-373** | Require hardware-attested device identity for eligible Macs | Full | Full | Full | Full |
| **CAP-272** | Connect Fleet to Apple Business | Full | Full | Partial | Partial |
| **CAP-273** | Renew the Apple Business token | Full | Full | Read only | Unsupported |
| **CAP-274** | Control what Setup Assistant shows on an ADE device | Full | Partial | Full | Full |
| **CAP-275** | Add or remove an App Store application | Full | Full | Read only | Partial |
| **CAP-276** | Renew the Volume Purchasing token | Full | Full | Unsupported | Unsupported |
| **CAP-277** | Learn from Fleet that an Apple credential is expiring | Read only | Partial | Partial | Unsupported |
| **CAP-278** | Turn on Windows device management | Partial | Partial | Partial | Partial |
| **CAP-279** | Choose whether Windows enrollment asks the end user | Full | Full | Full | Full |
| **CAP-280** | Turn Windows device management off | Partial | Partial | Partial | Partial |
| **CAP-281** | Bind Fleet to an Android Enterprise | Full | Partial | Unsupported | Unsupported |
| **CAP-282** | Deliver client certificates to Android devices | Not established | Unsupported | Full | Full |
| **CAP-283** | Tune Android API pressure and the companion app identity | Not established | Unsupported | Unsupported | Unsupported |
| **CAP-284** | Turn Android device management off | Full | Full | Unsupported | Unsupported |
| **S. Organization and server settings** | | | | | |
| **CAP-285** | Set the address everything uses to reach Fleet | Full | Full | Full | Full |
| **CAP-286** | Serve Fleet under a URL path | Not established | Unsupported | Unsupported | Unsupported |
| **CAP-287** | Let administrators sign in at a different address from devices | Full | Full | Full | Full |
| **CAP-288** | Put your organisation's name and logo in Fleet | Full | Full | Full | Full |
| **CAP-289** | Point end-user error messages at your own help desk | Full | Full | Full | Full |
| **CAP-290** | Have the identity provider decide what a Fleet account may do | Unsupported | Partial | Partial | Partial |
| **CAP-291** | Keep a way in when the identity provider is down | Full | Partial | Partial | Unsupported |
| **CAP-292** | Attach the end user's IdP identity to their devices | Partial | Partial | Partial | Partial |
| **CAP-293** | Set a host's IdP username by hand | Full | Full | Unsupported | Unsupported |
| **CAP-294** | Confirm Fleet is receiving requests from the identity provider | Full | Full | Unsupported | Unsupported |
| **CAP-295** | Send scheduled-report results somewhere | Read only | Read only | Read only | Unsupported |
| **CAP-296** | Send osquery's own status messages somewhere | Unsupported | Read only | Read only | Unsupported |
| **CAP-297** | Rotate the token of an API-only identity | Partial | Partial | Unsupported | Unsupported |
| **CAP-298** | Remove or demote a user | Full | Full | Full | Unsupported |
| **T. Running and operating the service** | | | | | |
| **CAP-299** | Ask Fleet whether it is healthy | Not established | Partial | Partial | Unsupported |
| **CAP-300** | Collect request-level metrics from Fleet | Not established | Unsupported | Unsupported | Unsupported |
| **CAP-301** | Export traces and internal metrics | Not established | Partial | Unsupported | Unsupported |
| **CAP-302** | Know whether Fleet's periodic jobs are still running | Not established | Partial | Unsupported | Unsupported |
| **CAP-303** | Ask Fleet to run one of its schedules now | Not established | Full | Full | Unsupported |
| **CAP-304** | Upgrade the Fleet server | Not established | Unsupported | Unsupported | Unsupported |
| **CAP-305** | Check whether migrations are current | Unsupported | Full | Full | Unsupported |
| **CAP-306** | Back up and restore the deployment | Not established | Not established | Unsupported | Unsupported |
| **CAP-307** | Prove a restored Fleet can still decrypt what it holds | Partial | Full | Unsupported | Unsupported |
| **CAP-308** | Keep a restored Fleet from acting on the real world | Not established | Partial | Unsupported | Unsupported |
| **CAP-309** | Read the licence's expiry date | Full | Full | Full | Unsupported |
| **CAP-310** | Rotate the server's HTTPS certificate without disconnecting agents | Not established | Read only | Unsupported | Unsupported |
| **CAP-311** | Renew the Windows enrolment certificate | Not established | Unsupported | Unsupported | Unsupported |
| **CAP-312** | Rotate an integration or service secret | Partial | Partial | Partial | Partial |
| **CAP-313** | Review who has privileged access | Partial | Partial | Partial | Unsupported |
| **CAP-314** | Size the database connection budget | Not established | Unsupported | Unsupported | Unsupported |
| **CAP-315** | Add read replicas | Not established | Unsupported | Unsupported | Unsupported |
| **CAP-316** | Configure shared object storage | Not established | Unsupported | Unsupported | Unsupported |
| **CAP-317** | Put Fleet behind an outbound proxy | Not established | Not established | Unsupported | Unsupported |
| **CAP-318** | Deploy Fleet on AWS from Fleet's reference Terraform | Not established | Not established | Unsupported | Unsupported |
| **CAP-319** | Deploy Fleet on GCP from Fleet's reference Terraform | Not established | Not established | Unsupported | Unsupported |
| **CAP-320** | Authenticate object storage without a stored key | Not established | Unsupported | Unsupported | Unsupported |
| **CAP-321** | Run Fleet with Docker Compose | Not established | Not established | Partial | Unsupported |
| **CAP-322** | Run Fleet on Kubernetes | Not established | Not established | Unsupported | Unsupported |
| **CAP-323** | Run Fleet as a binary on a virtual machine | Not established | Not established | Unsupported | Unsupported |
| **CAP-324** | Move vulnerability processing off the serving instances | Not established | Unsupported | Unsupported | Unsupported |
| **CAP-325** | Simulate load against a deployment | Not established | Not established | Unsupported | Unsupported |
| **CAP-326** | Drain an instance before stopping it | Not established | Not established | Unsupported | Unsupported |
| **CAP-327** | Retire a deployment deliberately | Partial | Partial | Unsupported | Unsupported |
| **CAP-328** | Have Fleet hosted and operated for you | Not established | Not established | Unsupported | Unsupported |
| **U. Diagnostic actions and introspection surfaces** | | | | | |
| **CAP-329** | Read the agent's own log on a host | Partial | Partial | Unsupported | Unsupported |
| **CAP-330** | Inspect the Orbit root directory on a host | Not established | Partial | Unsupported | Unsupported |
| **CAP-363** | Open an interactive query shell on the host itself | Unsupported | Unsupported | Unsupported | Unsupported |
| **CAP-331** | Raise an agent's verbosity for a bounded window | Full | Partial | Full | Full |
| **CAP-332** | Raise an agent's verbosity permanently | Partial | Partial | Full | Partial |
| **CAP-333** | Collect a diagnostic bundle from the server | Not established | Partial | Full | Unsupported |
| **CAP-334** | Read Fleet's recorded internal errors | Not established | Full | Full | Unsupported |
| **CAP-335** | Read a host's own osquery introspection tables | Full | Full | Full | Unsupported |
| **CAP-336** | Read the Apple MDM command queue | Full | Full | Partial | Unsupported |
| **CAP-337** | Read the Windows MDM command queue | Partial | Full | Partial | Unsupported |
| **CAP-338** | Read Android's command and policy state | Partial | Unsupported | Partial | Unsupported |
| **CAP-339** | Read the audit record straight from the database | Unsupported | Partial | Unsupported | Unsupported |
| **CAP-340** | Read the record of Fleet's own scheduled runs | Not established | Partial | Unsupported | Unsupported |
| **CAP-341** | Collect a Windows MDM diagnostic report from a device | Not established | Partial | Unsupported | Unsupported |
| **CAP-342** | Collect a sysdiagnose from an iPhone or iPad | Not established | Not established | Unsupported | Unsupported |
| **CAP-343** | Ask which Fleet version is answering | Full | Full | Partial | Unsupported |
| **CAP-344** | Trade host-data freshness for server load | Read only | Read only | Read only | Unsupported |
| **CAP-345** | Move host processing through Redis instead of MySQL | Not established | Unsupported | Unsupported | Unsupported |
| **CAP-346** | Stop hosts sharing an identifier from overwriting each other | Partial | Unsupported | Partial | Unsupported |
| **CAP-347** | Find the limit that is silently truncating your data | Not established | Partial | Partial | Partial |
| **CAP-348** | Rank what each scheduled query costs a host | Partial | Full | Partial | Unsupported |

<a id="the-counts-recounted-from-the-table-above"></a>

### Matrix totals

**362 rows, 1,448 cells, no blanks.**

| Value | UI | REST API | `fleetctl` | GitOps |
|---|---|---|---|---|
| **Full** | 198 | 187 | 181 | 124 |
| **Partial** | 56 | 105 | 57 | 35 |
| **Read only** | 12 | 6 | 8 | 0 |
| **Unsupported** | 27 | 52 | 115 | 203 |
| **Not established** | 69 | 12 | 1 | 0 |
| **Total** | **362** | **362** | **362** | **362** |

The totals highlight these differences in coverage:

REST has `Full` or `Partial` support for 292 actions, compared with 254 for the UI, 238 for `fleetctl`, and 159 for GitOps. It provides the broadest coverage in this matrix.

The UI has 69 unresolved cells. Thirty-three concern server operation, settings, and diagnostics; twenty-one are on rows where all three other columns are unsupported. Those neighboring answers suggest where further investigation may help, but they do not establish the UI result.

GitOps is unsupported on 105 actions available through both the UI and REST. Its declarative vocabulary and lack of read operations account for much of that limit.

Eighty-five rows are `Full` across all four columns, and 106 have the same answer in every column. Check the individual row when choosing an interface for a new workflow.

## What Fleet or an external system starts on its own

![Reference](../_assets/icons/reference-light.svg) Fleet, device users, and external systems can initiate work without an administrator calling one of the four interfaces. Include these paths when reviewing what can change your devices and stored data.

The capability register marks 141 rows as capable of automatic or external initiation, mostly periodic collection. This table selects the administrative actions from that group.

| ID | Action | Initiator | What triggers it | Material gate |
|---|---|---|---|---|
| **CAP-003** | Create a Fleet account on first identity-provider sign-in | Fleet | The user's own sign-in | Premium, and SSO enabled in the same write |
| **CAP-004** | Remove a Fleet account | The identity provider | A SCIM request | Premium **at server start**. On a server started Free the routes do not exist |
| **CAP-018** | POST an activity to a URL | Fleet | Every activity, as it happens | A destination URL. Free and Premium alike |
| **CAP-019** | Stream activities to an audit-log destination | Fleet | Every activity | Premium, plus process configuration and a restart |
| **CAP-027** | Create a pending host record | Apple | Apple's device sync | Premium, and the serial assigned to Fleet in Apple Business Manager |
| **CAP-032** | Install the agent on a Mac | Fleet | A task queued at enrollment. Command delivery does not confirm agent installation | Apple MDM enrollment |
| **CAP-035**, **CAP-039** | Enroll a Windows host in MDM, or move it off another MDM | Fleet | The agent's own configuration check-in | Windows MDM turned on, and the host already agent-enrolled |
| **CAP-040** | Start a macOS MDM migration | The end user | Pressing Start on their own machine | Premium, migration turned on, a webhook destination set |
| **CAP-050** | Register Fleet's Apple service-discovery URL | Fleet | Hourly, over every uploaded token | An uploaded Apple Business Manager token |
| **CAP-063** | Delete host records | Fleet | A scheduled sweep | Host expiry turned on with a silence window |
| **CAP-130** | Scrub stored history rows | Fleet | Turning a history dataset off. Existing stored rows are deleted | None |
| **CAP-139** | POST when too much of the estate goes quiet | Fleet | A scheduled check | A destination URL |
| **CAP-158** | Remove a profile from devices | Fleet | The device falling out of the profile's scope | None |
| **CAP-177**, **CAP-246**, **CAP-247** | Install software on a host | Fleet | A failing policy, a setup experience, or the user's own self-service page | Premium for the policy automation |
| **CAP-178** | Uninstall software from a host | Fleet | A policy automation | Premium |
| **CAP-160**, **CAP-248** | Run a script on a host | Fleet | A failing policy | Premium, and scripts enabled on the host |
| **CAP-181** | Refresh the catalogue of maintained apps | Fleet | Hourly | None |
| **CAP-189** | Hold a Mac at setup and run the setup experience | Fleet | Enrollment | Premium |
| **CAP-236**, **CAP-238** | Encrypt a disk and escrow the credential | Fleet | Enforcement reaching the host. Without user interaction on a TPM-backed Ubuntu host; on Windows any message the user sees comes from Windows | Premium |
| **CAP-371** | Rotate a Mac's FileVault recovery key | Fleet | A scheduled job marking the currently held key undecryptable. The agent then prompts the person at the keyboard for their password at their next login | Escrow Buddy capability declared by the agent; disk encryption enforced for the host's scope |
| **CAP-249** | POST when hosts start failing a policy | Fleet | Policy evaluation | A destination URL |
| **CAP-250** | Open a ticket when hosts start failing a policy | Fleet | Policy evaluation | Premium, and a configured ticketing integration |
| **CAP-251** | Book a maintenance window on a user's calendar | Fleet | A job that runs **every five minutes** | Premium, and a calendar integration |
| **CAP-252** | Report a host as non-compliant | Fleet | Evaluated inside the request that delivers the failing result | Premium, and Microsoft Entra connected |
| **CAP-253** | Refuse a sign-in | Microsoft Entra | **Every sign-in attempt**, reading state Fleet stored earlier | Premium. macOS is the platform Fleet supports it on |
| **CAP-254** | Grant a one-time bypass of conditional access | The end user | Their own device page. **No administrator can grant one** | Premium, and bypass not disabled |
| **CAP-256** | POST when a new vulnerability is detected | Fleet | Its own interval, one hour by default. **A server startup setting**, not changeable through any interface | A destination URL |
| **CAP-259** | Apply declared configuration | A CI pipeline | A repository event | Premium for anything fleet-scoped. **On Free every fleet file is skipped and the run still reports success** |
| **CAP-271** | Re-issue a host's identity certificate | Fleet | **Every 180 days**, automatically | Host identity certificates in use |
| **CAP-277** | Warn that an Apple credential is expiring | Fleet | An expiry check | Premium |
| **CAP-281** | Reconcile which Android devices still exist | Google, then Fleet | Google pushes enrollment and status events; Fleet polls hourly | Android management configured |
| **CAP-284** | Turn Android device management off | An external system | An action in Google's console. Fleet does not prompt for confirmation | None |
| **CAP-290** | Decide what a Fleet account may do | The identity provider | **Every login**, re-evaluated | Premium, and role sync configured |
| **CAP-292** | Attach the end user's identity to their devices | Fleet | The user authenticating during enrollment | Premium |

Include three of these behaviors in change-control procedures: disabling a history dataset scrubs its stored rows, a device leaving profile scope triggers removal, and an action in Google’s console can disable Android management without Fleet confirmation. See [6.1](../06-automate-fleet/6.1-automation-design-and-change-control.md) for change control and [6.5](../06-automate-fleet/6.5-integrations-webhooks-and-external-workflows.md) for outbound workflows.

<a id="not-established-deliberately"></a>

## Unresolved interface support

![Explanation](../_assets/icons/explanation-light.svg) Sixty-nine rows contain at least one `Not established` cell. No row has four: each has at least one established interface answer.

Twelve rows are unsettled in more than one column, and they fall into two groups.

CAP-350, enumerating all outbound destinations Fleet reaches, is unresolved in the UI, REST, and `fleetctl` columns. GitOps is established as unsupported.

The other eleven concern deployment or operational practices: backup and restore, outbound proxies, reference infrastructure code, Docker Compose, Kubernetes, virtual machines, load simulation, instance draining, hosted Fleet, and iPhone sysdiagnose collection. An unresolved interface cell does not establish whether the practice is possible. For example, Fleet’s separate `osquery-perf` tool supports load simulation outside all four interfaces ([7.5](../07-operate-fleet/7.5-maintain-capacity-and-availability.md)).

UI support has the largest unresolved set. The review required evidence from rendered controls, so an established answer in another column was not enough to settle a UI cell.

<a id="where-this-appendix-and-its-siblings-deliberately-differ"></a>

## Comparing related appendices

![Explanation](../_assets/icons/explanation-light.svg) The appendices organize the shared capability register for different questions. Their row counts and answers need to be read within that scope.

This index has 362 rows, [a.2](a.2-platform-capability-matrix.md) has 276, and [a.1](a.1-capability-index.md) has 364 capabilities. This matrix omits CAP-354, the MCP client covered separately, and places CAP-371, automatic repair of an undecryptable FileVault key, in the initiation table. The platform matrix excludes non-device actions and merges platform-equivalent rows. It combines CAP-048’s personal-link BYOD enrollment coverage elsewhere, while this interface index retains it as a separate action from CAP-049’s account-driven path.

Nine rows are unsupported in all four columns: CAP-204 (installing all offered software), CAP-211 (enforcing a Linux OS version), CAP-222 (releasing a locked Android device), and the following cases. CAP-361, CAP-362, and CAP-365 cover the device-owner page, Fleet Desktop summary, and self-service uninstall. CAP-363 (`orbit shell`) and CAP-364 (an immediate update check on agent restart) run locally through the agent. CAP-366 is the Android self-service toggle: all four interfaces can store it, but Fleet does not act on it for Android, so none performs the named outcome.

CAP-372, provisioning a Mac’s local account and syncing its password with an identity provider, is `Partial` everywhere. Each interface can configure Platform SSO’s OAuth token URL, client ID, and client secret; the Mac performs provisioning and synchronization. No read response exposes the secret in clear text. GitOps has no read operation, and a file generated from live configuration contains `TODO` in place of the secret.

An interface can have `Full` support while [a.4](a.4-roles-and-permissions-matrix.md) denies the action for a particular role. Check both support and authorization.

[a.7](a.7-fleetctl-command-reference.md) counts commands, while this appendix counts actions. A command can serve many rows, so the totals are not directly comparable.

## Version notes

![Explanation](../_assets/icons/explanation-light.svg) The interface review began with Fleet 4.90.0. When checking a later release, pay particular attention to these areas:

New GitOps keys can make previously unsupported actions available. Check the client’s schema for the release you use.

New UI controls can change `Read only` or `Unsupported` answers. Check the relevant page before relying on an older limitation.

Packaging and update-repository operations are native `fleetctl` responsibilities. Confirm their flags and behavior when updating a build workflow.

[a.6](a.6-glossary-and-release-compatibility.md) lists version floors and renamed terms. If your deployment differs from a matrix answer, compare its release with the edition you are reading.
