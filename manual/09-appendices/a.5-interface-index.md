---
title: "Action-to-interface index"
chapter: "Appendices and indexes"
section: "A.5"
sidebar_position: 5
verified_against: Fleet 4.90.0
verified_on: 2026-09-02
verified_source: "drafted against fleet-v4.90.0 (7c428c6e46) from four independently built research columns, one per interface, each covering the register rows as they stood at first drafting. Every column was read at the tag; Fleet's documentation was used for leads only, never as evidence. The columns disagreed on 17 rows and those were reconciled against source before drafting. Reconciled 2026-09-01 to the then-current 354-capability register: six rows the index had not yet projected were added: CAP-048 restored as a distinct interface action, and the newer CAP-349 to CAP-353, with cells verified at the tag, CAP-354 (MCP) left as a documented exclusion, and the counts recounted from the table. Reconciled again 2026-09-02 to a.1's 360-capability register: CAP-361, CAP-362, CAP-363, CAP-364, CAP-365 and CAP-366, labelled from a.2's existing platform research, were added as Unsupported in every column, each for the reason its own row states; CAP-354 remains the sole documented exclusion, and the counts were recounted from the table again. Reconciled a third time 2026-09-02 (round4 RB3) to a.1's 361-capability register: CAP-372, provisioning a Mac's local account and syncing its password with the identity provider, was added scored Full and later corrected to Partial in every column, because setting the OAuth IdP through the UI's Account provisioning page, the REST API, `fleetctl` and GitOps only arms an outcome the Mac itself performs; the counts were recounted from the table again. Reconciled a fourth time 2026-09-02 (round4 RM9) to a.1's 362-capability register: CAP-373, requiring ACME/Managed Device Attestation for eligible Macs, was added scored Full in every column, because the checkbox, `mdm.apple_require_hardware_attestation` on the REST API's config endpoint, the same field via classic `fleetctl get/apply config`, and `controls.apple_require_hardware_attestation` in GitOps all read and write the one boolean identically, confirmed against fleetctl's own testdata fixtures; the counts and the derived narrative figures (Full/Partial totals, all-four-agree rows) were recounted from the table again. Reconciled a fifth time 2026-09-04 (round8) after two cells were rescored against the tag: CAP-279 (Windows enrollment prompt) `fleetctl` and GitOps moved from Not established to Full, because GitOps writes `controls.enable_turn_on_windows_mdm_manually` (pkg/spec/gitops.go) and classic `fleetctl apply` writes the same `mdm` key (server/service/client.go), and CAP-181 (keep the library's catalogue apps current) UI moved from Not established to Partial, because the UI arms the no-pin auto-update through the software title's Versions control the same way the other three interfaces do; the rows-with-any-Not-established total fell 72 to 70, the UI Not-established total 70 to 69, the Partial total rose 252 to 253, the more-than-one-column group 14 to 13, and section N was corrected 22 to 23 rows. Citation ledger at research/section-notes/a.5-notes.md"
further_reading:
  - https://fleetdm.com/docs/configuration/yaml-files
  - https://fleetdm.com/docs/rest-api/rest-api
feature_requests:
  labels: [":product"]
  match: ["GitOps", "fleetctl", "API", "UI"]
  exclude: []
---

# Action-to-interface index

**Fleet's interfaces overlap, but they are not interchangeable.** Each administrative action has a specific set of supported control surfaces, and the overlap is wide enough to make the gaps invisible until you hit one. A runbook that says "do it with `fleetctl`" is fine for most of what you will ask for and wrong for reading the activity feed. A repository that declares everything you care about still cannot run a script. A plan that standardises on the UI cannot build an installer.

This appendix is the lookup that tells you which of those you are about to hit.

## What this appendix carries

![Reference](../_assets/icons/reference.svg) Every administrator action in the manual's capability register, 362 of them, against all four operator interfaces: the Fleet UI, the REST API, `fleetctl` and GitOps. Plus a second, shorter table for a different question, which is what Fleet or an external system starts without anyone asking.

**What is not here is the detail of any one interface.** Which command to run and what its exit status proves is [a.7](a.7-fleetctl-command-reference.md). What a caller must present and what has to be reachable is [a.8](a.8-api-action-and-endpoint-reference.md). Which configuration authority wins when two of these disagree is [a.3](a.3-configuration-model-and-precedence.md). Which role may perform the action, once you know an interface supports it, is [a.4](a.4-roles-and-permissions-matrix.md). Which platforms it reaches is [a.2](a.2-platform-capability-matrix.md).

**Interface support and permission are separate gates and this appendix only opens the first one.** A `Full` cell means the interface can perform the action. It does not mean your account may.

Buttons, endpoints, flags and YAML keys are deliberately absent. They change every release, Fleet already enumerates them, and copying them here would produce a table that is wrong at the next tag. What is here instead is the shape of each interface's reach, which is stable, and the boundaries that shape produces.

## How to read it

![Reference](../_assets/icons/reference.svg) Five values, and the difference between three of them is most of the work.

| Value | What it means |
|---|---|
| **Full** | The interface performs the action. |
| **Partial** | The interface performs part of the action and a stated boundary stops it. The boundary is either predictable from the interface model below or named in this appendix. |
| **Read only** | The interface can show you the current value and cannot change it. **This is a claim about the interface, not about Fleet.** Some of these values can be changed elsewhere and some cannot be changed anywhere. |
| **Unsupported** | The interface refuses or has no surface, and a positive boundary was found: a rendered refusal, a closed command tree, a closed request surface, a closed key vocabulary, or a route behind a credential an administrator does not hold. |
| **Not established** | The sources do not settle it. The record of what was searched is in the appendix's notes. |

Four conventions decide a large number of cells, and knowing them saves reading the boundary twice.

**A read served completely is `Full`, not `Read only`.** Where the action itself is a read, an interface that returns the thing has performed the action. `Read only` is reserved for a row whose action includes changing something and where the interface can only report the current state. **All four columns are held to this.**

**`Read only` does not imply that some other interface can write.** Forty-eight rows have no `Full` and no `Partial` in any column, and seven of those are readable somewhere. Reading the audit-log destination, the osquery log destinations and two of the host-freshness intervals is possible; changing any of them means restarting the server with different process configuration, which is [a.3](a.3-configuration-model-and-precedence.md)'s subject and no interface's.

**Arming a capability is `Partial`. Performing it is `Full`.** Several actions are performed by Fleet itself or by the person holding the device, and what an administrator controls is the switch that decides whether they happen at all. Just-in-time account creation, attaching the end user's identity to their devices, and granting a one-time conditional-access bypass all read this way. An interface that can write the switch and cannot perform the act is `Partial` in every column.

**An end-user surface is not administrator support.** Where the only way to do something is the device owner's own page, authenticated by that device's token rather than by a Fleet account, every column reads `Unsupported` and the end-user surface is described in prose. Installing everything offered to you and triggering Linux escrow both read that way, and both are visibly present in the web interface.

## What each interface is, and the boundary that decides its column

![Explanation](../_assets/icons/explanation.svg) Each column has one boundary rule that decides most of it. Learn the four and you can predict a row this table does not contain.

### `fleetctl api` is not `fleetctl` support. `gitops`, `apply` and `delete` are

**This decision alone decides 148 rows**, which is why it is stated before the matrix rather than inside it.

`fleetctl api` builds an arbitrary HTTP request from a URI you type. It carries no Fleet vocabulary: it does not know what a fleet is, what a policy is, or what any response means. **Counting it as `fleetctl` support would make the `fleetctl` column a transcription of the REST API column**, since anything the API can do it can technically reach. So it does not count. Forty-seven rows have no native command and are reachable only that way, and each is `Unsupported` here.

`fleetctl gitops`, `fleetctl apply` and `fleetctl delete` do count, for three reasons that all point the same way. They are registered commands in the client's own tree. The client does the work, because **there is no server-side GitOps engine**: the client parses the YAML, decides what changed, and drives ordinary endpoints. And `apply` reaches two specification kinds the GitOps vocabulary cannot express at all, so scoring it as GitOps would lose real reach. One hundred and one rows depend on one of those three commands.

**The asymmetry is deliberate and it is the whole point.** `gitops` and `apply` are Fleet semantics executed by the client. `api` is an HTTP request executed by you. The difference is not how much typing each saves. It is whether the client understands what it is sending.

Because `gitops` counts, the `fleetctl` column is `Full` on many rows whose only path is a specification file, and **the operator experience on those rows is writing YAML, not typing a command**. [6.4](../06-automate-fleet/6.4-use-fleetctl.md) covers the client in practice and [6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md) covers the repository workflow.

### The REST API column counts a route only if it sits behind Fleet's shared user authenticator

A Fleet API token belongs to a user account. **A route is in this column only if its registration puts it behind the middleware that checks that token**, which is a stronger test than "a route exists at this path".

The test is exhaustive rather than sampled, because that middleware has exactly five registration sites across the whole server, and one route family outside the versioned tree that additionally demands a global administrator. Everything else authenticates a device, an agent, an identity provider or a vendor's callback, or requires nothing at all. [a.8](a.8-api-action-and-endpoint-reference.md) sets out the six caller classes and which paths belong to each.

**The rule changed 33 answers a naive reading would have called `Full`.** Eighteen became `Partial` because part of the action sits on a device, agent or protocol caller, and fifteen became `Unsupported` because that caller is the only one. Linux escrow, self-service installation, the conditional-access bypass and both enrollment protocols are the clearest cases. **A row that reads `Unsupported` in this column is not a claim that no HTTP request performs the action.** It is a claim that no request you can make with your own token does.

### The UI column is what is rendered, not what the browser received

The web interface issues requests from a closed set of endpoints and renders from a closed set of components. Both are enumerable at a release, which is what makes a negative answer here a boundary rather than a gap in the search.

**A value can arrive in the browser and never appear on a page**, and that is `Unsupported` rather than `Read only`. The configuration response carries three log destinations. One of them is displayed in four places. The other two are displayed nowhere, so the UI cannot tell you what the audit and osquery status destinations are set to while the REST API and `fleetctl` both can.

### GitOps has no read direction at all

`fleetctl gitops` writes an apply log and two status lines. **There is no read command, no export and no report**, so a cell meaning "you can look but not change" cannot arise on this interface: **GitOps has zero `Read only` cells**, because it has no read direction to put one in.

That is not the same claim as "every row the other three columns call `Read only` is `Unsupported` here." Eighteen rows carry `Read only` in the UI, REST API, or `fleetctl` column. Twelve of them are `Unsupported` for GitOps too, because nothing about the underlying data has a declarative form.

The other six are independently writable through GitOps despite no interface exposing a matching read: collecting local accounts (CAP-088), collecting software inventory and turning it on per fleet (CAP-122, CAP-123), confining a label to one fleet (CAP-143), and prompting users on older Macs to update (CAP-206) are all `Full` for GitOps against a `Read only` UI cell; buying and distributing App Store apps (CAP-275) is `Partial` for GitOps against a `Read only` `fleetctl` cell. A `Read only` cell elsewhere is a hint GitOps might be `Unsupported`, not a guarantee.

The vocabulary is closed in the other direction too. Exactly ten top-level keys are valid and anything else is a hard error. Below the top level every key is checked against the schema at every depth, with a spelling suggestion offered when it fails. `--allow-unknown-keys` downgrades those errors to warnings and **does not make the keys mean anything**: they are dropped. That closure is what makes `Unsupported` in this column a boundary rather than an absence, and it is why 203 rows carry it.

**Reads and imperative acts are the two families it excludes.** Locking a device, running a script, erasing a phone and signing in are acts rather than states, and a declarative repository has nothing to say about them. That accounts for the whole of section N, where GitOps supports none of the 23 rows.

### The MCP server is not a column here

The Fleet MCP server ([6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md)) lets an AI assistant operate Fleet, but it is a client of the REST API rather than an interface of its own, so it earns no column in the matrix. What an assistant can reach through it is **not** the REST API column: it is the fixed twenty-tool subset in [A.11](a.11-mcp-tool-reference.md), spanning four groups (hosts, queries, policies and vulnerabilities, inventory), further narrowed by whatever its token's role forbids.

There is no delete-host tool, no generic REST passthrough and no config-writing tool, even though REST itself can do all three. Read A.11 for the exact tool list, and 6.6 for how the proxy and its one destructive tool change the security model around it.

## Five boundaries worth knowing before you plan

![Troubleshooting](../_assets/icons/troubleshooting.svg) Each of these is a place where the interface does less than its name suggests, and each one is in the matrix below with its answer.

> ### Omitting a GitOps key does not mean "leave this alone"
>
> **It means one of three different things, and which one applies is only discoverable by reading the client.** This is the single most consequential behaviour in any of the four interfaces, because it is destructive, silent and invited by ordinary practice: you delete a block you no longer need.
>
> **Omitting some keys clears what they describe.** Leave out `policies:` and every policy in scope is deleted. Leave out `reports:` and every report is deleted. Leave out `org_settings.yara_rules` and every YARA rule goes. Leave out `controls:` from a named fleet file and every control resets, including removing all configuration profiles and switching disk encryption off. **Across the global and unassigned files, exactly one must define `controls` instead**: setting it in both is an error, setting it in neither is an error, and when only the unassigned file defines it those controls are applied to the global scope. So the same absence means "reset everything" in a named fleet file and, on the global pair, "exactly one of you must own this".
>
> **Omitting other keys turns features on.** Leave out `features.enable_software_inventory`, `enable_host_users` or the historical-data keys and Fleet writes `true` for all of them on every apply. For vulnerability history that is the reverse of a destructive toggle: turning it off scrubs the stored rows, and omitting it turns collection back on without restoring anything. `controls.macos_updates.update_new_hosts` is derived rather than defaulted, so omitting it turns the behaviour on whenever a minimum version and a deadline are both set.
>
> **And omitting a third group genuinely leaves things alone**, because a missing key inside `org_settings` is merged over the stored configuration. **There is no way to tell which of the three rules applies to a given key except by reading the client**, and the exceptions are exactly the blocks the client fabricates when they are absent.
>
> Four more that do not fit the pattern. **`labels[].hosts` is the only key in the whole vocabulary where absent and explicit null differ**: absent preserves membership, null clears it. **A `$FLEET_SECRET_` value is never deleted**, because the save is upsert-only, so a secret that stops being referenced stays in Fleet's store with no declarative way to remove it, and its value is transmitted even on a dry run. And **supplying a global file without an unassigned-scope file resets the unassigned scope**, by synthesising an empty configuration and applying it. Finally, **omitting `agent_options` is a hard error, not a clearing**, in a global or named-fleet file, because the client requires the key there; in an unassigned-scope file the key is unsupported, so a supplied value is ignored with a warning and an omission changes nothing.
>
> A dry run does not protect you from most of this. Reports, labels, packs, policies and user roles are not validated at all, **which means a dry run cannot catch the most destructive thing a GitOps run does**.

> ### `fleetctl` is Fleet's build tool, and that is why it is sometimes the only answer
>
> Ten rows have exactly one supported interface and it is `fleetctl`. **Nine of them are one story**: the decisions that are baked into an agent at build time, the agent update repository you host yourself, and the scaffolding for a GitOps repository have no other surface anywhere in Fleet.
>
> Building an installer for a platform, enabling scripts at packaging time, giving a host a hardware-backed identity certificate, supplying a Windows host's URL and secret at install time, setting an agent's update channel on the host, stopping an agent updating at all, building a macOS package that carries no URL or secret, publishing agent versions from your own repository, and generating a CI pipeline for GitOps. **That is the list, and no button, endpoint or YAML key reaches any of it.**
>
> **Two of those decisions cannot be undone from Fleet afterwards.** An agent built with updates disabled and an agent built to skip certificate verification both stay that way until you replace the package on the host.
>
> The tenth row is running Fleet itself under Docker Compose, and it is a weaker claim than the other nine: the command starts an evaluation sandbox at a fixed local address rather than the deployment the row means.

> ### Three things the UI cannot do
>
> **The UI cannot run an ad-hoc script.** It runs a script from the library and it can run one across many hosts, but pasting script contents into a one-off run is refused, and the field carries a note in Fleet naming the command line as its only supported caller. **This is the reverse of the usual direction**, in which the command line is the narrower interface.
>
> **The UI cannot turn software inventory on or off, at either scope.** It reads the setting in six places to decide what to show you and writes it nowhere. **There is no control for it on the software page or anywhere else in the interface**, and the switch is in the API, `fleetctl` and GitOps.
>
> **The UI presents disk encryption as one control for two platforms.** There is a single switch and it sends one value covering FileVault and BitLocker together. **You cannot enable encryption on Macs without also enabling it on Windows hosts from this interface**, which matters on an estate that is rolling out to one platform at a time.

> ### The UI is the only interface that can enroll an Android device or a Chromebook
>
> Four rows have exactly one supported interface and it is the UI, and all four are enrollment: enrolling an Android device as a personal work profile, enrolling a company-owned Android device by QR code at first boot, issuing the single-use Android enrollment token behind both, and enrolling a Chromebook.
>
> **A fully automated enrollment pipeline is therefore impossible for those two platforms at this release.** Everything downstream of enrollment is available through other interfaces; getting the device into Fleet in the first place is not. Plan the Android and ChromeOS rollout as an interactive step, and see [3.6](../03-connect-devices/3.6-enroll-android-devices.md) and [3.7](../03-connect-devices/3.7-enroll-chromeos-devices.md) for what that step involves.

> ### Every Apple credential renewal is half automatable
>
> `fleetctl` can request the push-certificate signing request and the Apple Business public key. **It has no upload counterpart for either, and none for a Volume Purchasing token.** So the half that can be scripted is the half that produces a file, and the half that is left is the half that must be done in a browser, on Apple's site, before an expiry date.
>
> GitOps inverts the same boundary rather than closing it: it assigns an already-uploaded token's default fleets and cannot upload, renew or delete the token. **In GitOps you can only do the part after the token.**
>
> The renewal itself is `Full` in the UI and the API and `Read only` in `fleetctl`, which is the shape to design the calendar reminder around. [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) covers the workflow.

## What decides a `Partial` cell

![Explanation](../_assets/icons/explanation.svg) `Partial` is the most common non-`Full` answer in one of the four columns (REST API); `Unsupported` and `Not established` are larger in the other three. It is still worth knowing the shapes `Partial` takes, since it appears 253 times across the four columns, rather than reading each of those boundaries one at a time.

**In the REST API column** it is nearly always that part of the action belongs to another caller. The administrator half is there and the device, agent or protocol half is not, and the missing half is usually the one that touches the machine.

**In the `fleetctl` column** it takes four shapes. A build-time-only answer, where the client sets something into a package and cannot change it afterwards. A request with no counterpart, which is the Apple credential story above. A fixed page size, which is why reading the MDM command queue returns twenty entries and says so in a line that is accurate about the twenty and silent about the rest. And a default output that omits what you asked for, which is why an access review run with the obvious command shows a blank role for exactly the fleet-scoped accounts you were reviewing.

**In the GitOps column** it is almost always library against execution, or definition against value. The repository owns the script library completely and cannot run a line of it. It declares a custom host vital's name and can never set a per-host value. It creates a fleet and its entire configuration and cannot give that fleet a single administrator. It defines ticketing integrations globally and is rejected by the server if you try to enable them per fleet.

**In the UI column** it is usually a platform subset or a licence gate that hides a control, and occasionally a split between the administrator's page and the device owner's page.

## Where exactly one interface can do it

![Reference](../_assets/icons/reference.svg) Counted from the matrix below, treating `Full` and `Partial` as "can" and `Read only`, `Unsupported` and `Not established` as "cannot".

| Interface | Rows where it is the only one | What they are |
|---|---|---|
| **REST API** | 16 | The largest exclusive set, and it has no single theme. Identity-provider driven removal, several diagnostic and introspection reads, re-arming a policy's automations, and the Linux escrow surfaces |
| **`fleetctl`** | 10 | Packaging, the self-hosted update repository, and repository scaffolding. Nine of the ten are the build-tool story above |
| **UI** | 4 | Android and ChromeOS enrollment |
| **GitOps** | 0 | GitOps expresses no action that another interface cannot also perform, which follows from it being a client over ordinary endpoints |

**Forty-eight rows have no supported interface at all.** Most are `fleet serve` process configuration and deployment infrastructure, where the answer is a restart with different settings rather than a request of any kind, and six are the end-user-surface and local-host rows added below. Seven of the 48 are readable somewhere without being writable anywhere.

## The matrix

![Reference](../_assets/icons/reference.svg) All 362 register rows, grouped as a reader would look for an action. Section rows in bold carry no cells; they mark where a family starts. Counts by value are published after the table and were recounted from it.

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
| **CAP-179** | Ship different builds of one title to different hosts | Full | Full | Not established | Not established |
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

### The counts, recounted from the table above

**362 rows, 1,448 cells, no blanks.**

| Value | UI | REST API | `fleetctl` | GitOps |
|---|---|---|---|---|
| **Full** | 198 | 187 | 180 | 123 |
| **Partial** | 56 | 105 | 57 | 35 |
| **Read only** | 12 | 6 | 8 | 0 |
| **Unsupported** | 27 | 52 | 115 | 203 |
| **Not established** | 69 | 12 | 2 | 1 |
| **Total** | **362** | **362** | **362** | **362** |

Four things in that shape are worth reading before you use any single row.

**The REST API reaches more actions than any other interface**, 292 at `Full` or `Partial` against 254 for the UI, 237 for `fleetctl` and 158 for GitOps. The other three are clients of it, so its reach is the ceiling theirs are measured against.

**The UI's 69 `Not established` cells are the appendix's largest soft spot**, and they are not evenly spread. Thirty-three of them are in the three sections about running the server, its settings and its diagnostics, where the answer is nearly always that the value is process configuration no interface writes. Twenty-one of the 69 sit on rows where all three other columns independently found `Unsupported`. **Those are very probably `Unsupported` too, and they are not published that way**, because the boundary that would justify it was not found. A wrong `Not established` is a failure in the same way a wrong `Unsupported` is, so the appendix records the uncertainty rather than resolving it in the direction the neighbours point.

**GitOps is `Unsupported` on 105 rows the UI and the REST API can both perform.** That is not a defect in GitOps. It is the closed vocabulary and the missing read direction working as designed, and it is the number that bounds how much of Fleet a repository can manage.

**Eighty-four rows are `Full` in all four columns and 105 rows have all four columns agreeing.** The overlap is real. It is just not where the planning risk is.

## What Fleet or an external system starts on its own

![Reference](../_assets/icons/reference.svg) A different question from the matrix, and the reason the matrix has four columns rather than five. **These actions happen without an operator invoking anything**, so no interface column can describe them, so an inventory of four control surfaces is an incomplete account of what changes an estate.

This is the set worth knowing about, not a catalogue. The register marks 141 rows as capable of self-initiation, most of which are ordinary periodic collection. What is below is the subset that performs an administrative action.

| ID | Action | Initiator | What triggers it | Material gate |
|---|---|---|---|---|
| **CAP-003** | Create a Fleet account on first identity-provider sign-in | Fleet | The user's own sign-in | Premium, and SSO enabled in the same write |
| **CAP-004** | Remove a Fleet account | The identity provider | A SCIM request | Premium **at server start**. On a server started Free the routes do not exist |
| **CAP-018** | POST an activity to a URL | Fleet | Every activity, as it happens | A destination URL. Free and Premium alike |
| **CAP-019** | Stream activities to an audit-log destination | Fleet | Every activity | Premium, plus process configuration and a restart |
| **CAP-027** | Create a pending host record | Apple | Apple's device sync | Premium, and the serial assigned to Fleet in Apple Business Manager |
| **CAP-032** | Install the agent on a Mac | Fleet | A task queued at enrollment. **Fleet guarantees the command is sent, not that the agent arrives** | Apple MDM enrollment |
| **CAP-035**, **CAP-039** | Enroll a Windows host in MDM, or move it off another MDM | Fleet | The agent's own configuration check-in | Windows MDM turned on, and the host already agent-enrolled |
| **CAP-040** | Start a macOS MDM migration | The end user | Pressing Start on their own machine | Premium, migration turned on, a webhook destination set |
| **CAP-050** | Register Fleet's Apple service-discovery URL | Fleet | Hourly, over every uploaded token | An uploaded Apple Business Manager token |
| **CAP-063** | Delete host records | Fleet | A scheduled sweep | Host expiry turned on with a silence window |
| **CAP-130** | Scrub stored history rows | Fleet | Turning a history dataset off. **Treat the toggle as destructive, because it is** | None |
| **CAP-139** | POST when too much of the estate goes quiet | Fleet | A scheduled check | A destination URL |
| **CAP-158** | Remove a profile from devices | Fleet | The device falling out of the profile's scope. **Nobody asks for this one** | None |
| **CAP-177**, **CAP-246**, **CAP-247** | Install software on a host | Fleet | A failing policy, a setup experience, or the user's own self-service page | Premium for the policy automation |
| **CAP-178** | Uninstall software from a host | Fleet | A policy automation | Premium |
| **CAP-160**, **CAP-248** | Run a script on a host | Fleet | A failing policy | Premium, and scripts enabled on the host |
| **CAP-181** | Refresh the catalogue of maintained apps | Fleet | Hourly | None |
| **CAP-189** | Hold a Mac at setup and run the setup experience | Fleet | Enrollment | Premium |
| **CAP-236**, **CAP-238** | Encrypt a disk and escrow the credential | Fleet | Enforcement reaching the host. **No dialog and no person** on a TPM-backed Ubuntu host; on Windows any message the user sees comes from Windows | Premium |
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
| **CAP-284** | Turn Android device management off | An external system | An action in Google's console. **There is no confirmation step in Fleet to catch it** | None |
| **CAP-290** | Decide what a Fleet account may do | The identity provider | **Every login**, re-evaluated | Premium, and role sync configured |
| **CAP-292** | Attach the end user's identity to their devices | Fleet | The user authenticating during enrollment | Premium |

**Three of these deserve a place in a change-control document rather than a lookup table.** Turning a history dataset off scrubs what is already stored. A device falling out of a profile's scope removes the profile with nobody asking. And Android management can be dismantled from outside Fleet entirely, with Fleet offering no confirmation and no warning. [6.1](../06-automate-fleet/6.1-automation-design-and-change-control.md) is where those belong; [6.5](../06-automate-fleet/6.5-integrations-webhooks-and-external-workflows.md) covers the outbound half.

## Not established, deliberately

![Explanation](../_assets/icons/explanation.svg) **Seventy rows carry at least one `Not established` cell, and no row carries four.** Every action in the register has at least one interface answer that rests on evidence.

Thirteen rows are unsettled in more than one column, and they fall into three groups.

**One row is open in three columns: CAP-350, enumerating every outbound destination Fleet reaches**, where the UI, the REST API and `fleetctl` are all unsettled and only GitOps has a confident answer (`Unsupported`).

**One more is open in two columns: whether Fleet's package variants map onto several software entries for one title (CAP-179)**, unsettled in `fleetctl` and GitOps alike. Two researchers reached it independently, which is a point in favour of the question being real rather than of one search being bad.

**Eleven are deployment and operations rows** where the question is what an operating practice looks like rather than what Fleet does. Backing up and restoring a deployment, running behind an outbound proxy, deploying from reference infrastructure code, running under Docker Compose, on Kubernetes or on a virtual machine, simulating load, draining an instance, hosted Fleet, and collecting a sysdiagnose from an iPhone. **This manual verifies against Fleet's own source**, and a `Not established` cell in these rows means the interface answer is unsettled, not the practice: load simulation, for one, is settled by `osquery-perf`, a purpose-built tool Fleet ships in its own tree ([7.5](../07-operate-fleet/7.5-maintain-capacity-and-availability.md)), which is reachable from none of the four interfaces scored here.

The single largest concentration is the UI column's 69 cells, described in the counts above. The UI column is the most conservative of the four, not the least capable interface: its `Not established` cells and the REST API column's `Unsupported` cells were often reached on the same underlying fact, from different standards of proof.

## Where this appendix and its siblings deliberately differ

![Explanation](../_assets/icons/explanation.svg) Read this before you compare a cell here against the same action in another appendix, because two of the differences are intentional.

**This appendix carries 362 rows and [a.2](a.2-platform-capability-matrix.md) carries 276.** They are projections of one register: [a.1](a.1-capability-index.md) holds 364 capabilities, and this index covers all of them except **CAP-354, connecting an AI assistant**, which is a client of the REST API rather than an interface of its own, as the note above the matrix records, and except **CAP-371, Fleet's own repair of an undecryptable FileVault key**, which no operator interface invokes at all; it is listed in the self-initiation table above instead. a.2 is a narrower projection again: it sets aside the rows that are not device-facing, because a platform matrix has nothing to say about a server setting, and it merges rows that are platform-identical, retiring an enrollment identifier this index keeps. **CAP-048 is a strict platform subset of another row for a.2's purposes, but a distinct interface action here**: the personal-link BYOD enrollment, which is not the account-driven path CAP-049 describes. Both differences are scope decisions rather than contradictions: a row present in one projection and absent from another follows from what that projection is for.

**Nine rows read `Unsupported` in every column. Three of them follow directly from the general boundary text above: CAP-204 (letting a user install everything offered), CAP-211 (enforcing a Linux OS version) and CAP-222 (releasing a locked Android device). The other six each read `Unsupported` for a reason the row's own action explains rather than that general boundary: CAP-361 and CAP-362 (the My Device page and the Fleet Desktop menu-bar summary), CAP-363 (`orbit shell`), CAP-364 (an agent restart forcing an immediate update check), CAP-365 (self-service uninstall) and CAP-366 (the Android self-service toggle a.2's CAP-366 note records Fleet as accepting and then discarding).** CAP-361, CAP-362 and CAP-365 are end-user-surface actions in the sense already defined: the only route is the device owner's own page, authenticated by that device's token, so no administrator interface performs them, the same shape as CAP-204. CAP-363 and CAP-364 are narrower still: `orbit shell` and the update check both run locally, on the host, through the agent's own binary rather than through any interface Fleet exposes to an administrator, so none of the four columns ever had a claim to make. CAP-366 is the odd one: an administrator can set the toggle through every interface, and Fleet stores what was sent, but a.2 records that Fleet then discards it on Android rather than acting on it, so no interface performs the outcome the row names even though all four accept the input. **CAP-354 is the only capability this appendix leaves out entirely**, because it is a client of an interface already in the matrix rather than a boundary case of one; these six earned matrix rows because each is answerable, and the answer for all six happens to be the same. CAP-371, Fleet's own repair of an undecryptable FileVault key, is the other row set aside from the matrix, but set aside rather than dropped: no operator interface invokes it, so it sits in the self-initiation table above.

**A further row, CAP-372, provisioning a Mac's local account and syncing its password with the identity provider, reads `Partial` in every column.** What each interface controls is the OAuth identity provider behind Platform SSO: the token URL, client ID and client secret can all be set through the UI's Account provisioning page, the REST API's config endpoint, `fleetctl` and GitOps. Setting those arms the capability; the account is then provisioned and the password synced on the Mac itself, not by any interface, which is the arming-versus-performing boundary that scores `Partial`. Even the arming half is not "identical" across the four: none of them ever returns the secret in the clear on a read, GitOps carries no read direction at all, and a GitOps file generated from a live config gets a `TODO` placeholder in the secret's place rather than the value itself.

**A `Full` cell here and a refusal in [a.4](a.4-roles-and-permissions-matrix.md) are both true.** Interface support and authorisation are separate gates, checked in that order. The interface has to be able to make the request before your role can be refused it.

**[a.7](a.7-fleetctl-command-reference.md) counts commands and this appendix counts actions**, so the two never line up. One command serves many rows here, and 101 rows are served by three commands between them.

## Version notes

![Explanation](../_assets/icons/explanation.svg) Every cell is Fleet 4.90.0. Three things move faster than the rest and are worth re-checking rather than trusting at a later release.

**The GitOps vocabulary grows.** New keys arrive at almost every release, so a `Unsupported` in that column ages faster than any other cell in this table. The closure argument behind it stays valid; the set it closes over does not.

**The UI gains controls for things that were command-line only.** The `Read only` and `Unsupported` cells in that column are the ones most likely to have changed under you.

**`fleetctl`'s exclusive rows are the most stable**, because packaging and the update repository are the client's own job rather than a thin layer over an endpoint. Those ten are the safest cells in the table to build a process on.

Version floors and the names that changed are [a.6](a.6-glossary-and-release-compatibility.md). Where a cell here disagrees with your deployment, check the release you are running before you conclude the table is wrong.
