---
title: "Platform capability matrix"
chapter: "Appendices and indexes"
section: "A.2"
sidebar_position: 2
verified_against: Fleet 4.91.0
verified_on: 2026-09-08
verified_source: "drafted against fleet-v4.90.0 (7c428c6e46) over two research passes. Every cell rests on source read at the tag; Fleet's documentation was used for leads only, never as evidence. Extended 2026-09-08 for Fleet 4.91.0 (overnight campaign step 3), verified at tag fleet-v4.91.0 (35fc1c0244): fifteen platform-matrix rows and six not-platform-scoped bullets added for a.1's new CAP-374 to CAP-385 and CAP-387 to CAP-393, taking the matrix from 276 rows to 291 and the bullet list from 92 to 98. Cells were read at the tag rather than inferred: the Adobe detail query's `Platforms: []string{'darwin', 'windows'}` allow-list and its `discoveryTable('adobe_plugins')` gate (`server/service/osquery_utils/queries.go`), `ValidLabelPlatformVariants` and the manual/host-vitals platform rejections (`server/fleet/labels.go`), the `platform == 'linux' || platform == 'windows'` gate on Orbit end-user authentication (`server/service/orbit.go`), the Windows-only `BypassEndUserAuth` packaging templates (`orbit/pkg/packaging/linux_shared.go`, `windows_templates.go`, with no macOS counterpart), `windows_settings.enable_managed_local_account` (`ee/server/service/teams.go`), and `AppleOSUpdateLatestVersion` with its mutually exclusive deadline fields (`server/fleet/app.go`). Two `Unsupported` cells rest on an allow-list a platform is absent from rather than on an error arm, which this appendix's own definition admits: the Adobe row and the label-platform row. The Version notes stamp below is left at 4.90.0 deliberately, because this pass added rows and did not re-read the 276 cells that were already there. Citation ledger at research/section-notes/a.2-notes.md. Amended 2026-09-08 (overnight campaign step 7, round-2 review finding 6), verified at fleet-v4.91.0 (35fc1c0244): CAP-395, sorting the host list by when a host last enrolled, added as `Supported` on all six platforms, Free, with no prerequisite. The sort reads `last_enrolled_at` from the hosts table through the sortable-column map at `server/datastore/mysql/hosts.go:74` and has no platform branch anywhere in the query builder, so there is no cell here that any platform answers differently. The matrix goes from 291 rows to 292. CAP-385's label was brought back into line with a.1 and a.5; its cells were already scored for profiles and managed app configuration only and did not change. Amended again 2026-09-08 (overnight campaign step 7, round-3 review finding 3): the headline row count above the matrix still read 291. Recounted from the matrix (292, lettered split rows included) and corrected; `build/check-cap-ids.py` now recomputes that sentence rather than only the frontmatter"
further_reading:
  - https://fleetdm.com/docs/get-started/faq
feature_requests:
  labels: [":product"]
  match: ["platform", "iOS", "Android", "ChromeOS", "Linux"]
  exclude: []
---

# Platform capability matrix

![Reference](../_assets/icons/reference-light.svg) Use this matrix to check a specific capability on each platform. Read its license and prerequisites alongside the platform result: support can depend on the management channel, ownership type, and configuration already in place.

## What this appendix carries

![Reference](../_assets/icons/reference-light.svg) Every device-facing capability the manual teaches, across six platform columns, with the licence and the prerequisites that change the answer.

License and prerequisites have their own columns so you can check them separately from platform support.

Use [a.6](a.6-glossary-and-release-compatibility.md) for OS-version requirements, [a.4](a.4-roles-and-permissions-matrix.md) for roles, and [a.5](a.5-interface-index.md) for interfaces. [a.1](a.1-capability-index.md) links each task to the chapter with its procedure.

## What decides most cells

![Explanation](../_assets/icons/explanation-light.svg) Four structural differences help explain the platform results below.

macOS, Windows, and Linux run fleetd. iOS, iPadOS, and Android do not provide its osquery and script paths. ChromeOS uses an extension with a smaller set of capabilities. Each row distinguishes an explicit Fleet restriction from a feature that has no applicable platform equivalent.

Apple MDM, Windows MDM, and Google's AMAPI offer different operations and delivery mechanisms. The same administrator task may follow a different path on each platform ([1.2](../01-foundations/1.2-how-fleet-reaches-a-device.md)).

Some capabilities depend on a vendor operation that has no equivalent on another platform. Those rows use `Not applicable` where the subject itself does not exist.

Ownership can also change the result, especially for personally owned versus company-owned Android devices. The condition register explains these differences.


<!-- IMAGE-TODO: assets/a.2-capability-condition-layers.webp
     QUESTION: Why does platform alone fail to determine whether a capability is available?
     PROMPT: DIAGRAM: A capability question passes through layered checks: Provider operation
     exists, Fleet implements a delivery path, Platform/enrollment supports it, Ownership and other
     row conditions satisfied. Display Agent and Native management/API as alternative mechanisms
     feeding the delivery-path layer, including ChromeOS extension as its own path rather than
     fleetd. Finish at Read the specific cell and condition register, not an automatically
     calculated Yes. Use diagrammatic layers rather than copying any matrix row. Do not equate
     Unsupported with Not applicable or treat mobile's small certificate app as full fleetd.
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
     NOTE: Proposed 2026-09-08; editorial brief, not technical re-verification. Reduce the
     structural overview above the matrix. Keep all cells, condition IDs, definitions, and version
     qualifications as searchable Markdown. Keep current prose and this TODO until the actual image
     is reviewed. Then check alt text against the artwork and retain an accessible summary plus all
     required technical qualifications.
     CANDIDATE: ../../research/visual-reviews/appendices/assets/a.2-capability-condition-layers.webp
     Rendered and inspected for the overnight batch; awaiting final joint review.
-->

<!-- IMAGE PENDING. Install reviewed artwork, then activate the image line below.
![Provider support, delivery mechanism, platform, enrollment, and ownership conditions jointly shape each capability cell.](assets/a.2-capability-condition-layers.webp)
-->

<a id="three-rows-worth-reading-before-you-plan"></a>

## Three platform differences to check when planning

![Troubleshooting](../_assets/icons/troubleshooting-light.svg) The following examples show why the platform, license, and prerequisite columns need to be read together.

> ### Signed host requests require Linux agents
>
> The setting that requires signed host requests applies deployment-wide to the covered agent, osquery, and certificate-request paths. The capability handshake is exempt.
>
> At this release, only Linux packages and agents support the signing option. Enabling the server requirement on a mixed deployment therefore rejects unsigned macOS and Windows requests without a platform exception or warning at configuration time.
>
> My Device uses a separate path and can remain reachable while the affected agents stop reporting or receiving work.

> ### Disk-encryption behavior after a downgrade to Free
>
> Free rejects a settings write that turns disk encryption on, but an existing enabled setting remains in place after a downgrade. Windows key collection can continue under that stored setting, and roles permitted to read the host can still retrieve held keys ([a.4](a.4-roles-and-permissions-matrix.md)).
>
> Linux rejects a new escrow attempt on Free. An attempt already pending at the downgrade can finish because its upload does not recheck the license.
>
> An enabled encryption setting can also prevent other device-management settings from being saved after a downgrade: the write is rejected while the new encryption value remains on. Disable enforcement before saving those changes.

> ### Wipe support depends on platform and license
>
> Free supports wiping a company-owned Android device. Other platforms encounter the Premium requirement first. Premium supports wipe on macOS, iOS/iPadOS, Windows, Linux, and Android, subject to the row's prerequisites. ChromeOS is unsupported on both editions.

## How to read it

![Reference](../_assets/icons/reference-light.svg) Platform cells use these five values:

| Value | What it means |
|---|---|
| **Supported** | Fleet does this on this platform once the row's prerequisite holds. |
| **Conditional (Cnn)** | Fleet does this only when a stated condition holds. Both branches are in the condition register. |
| **Unsupported** | Fleet refuses. A positive boundary was found: an explicit rejection, an error arm, an allow-list the platform is absent from, or a branch that names the platform and throws the request's substance away. |
| **Not applicable** | The row's subject does not exist on this platform. This is a statement about the platform, not about Fleet. |
| **Not established (Enn)** | No boundary was found in either direction. The record says what was searched. |

Apply the following reading rules throughout the matrix.

`Unsupported` requires evidence of an explicit platform restriction. If the source review found neither a working path nor a restriction, the cell uses `Not established`.

An explicit restriction can discard a value without returning an error. For example, the macOS managed-app paths accept configuration input and then clear it. Android Play-app creation forces self-service on, while edits retain the stored value regardless of the supplied setting. These cases are marked `Unsupported` for the requested capability.

A missing consumer alone is classified differently. ChromeOS agent options use `Not established` because the shared server accepts them, while the extension has no observed request path for them.

Read `Supported` with the separate license and prerequisite columns. A Premium requirement or prior MDM setup is recorded there. `Conditional` refers to the additional behavior explained by its condition ID.

This appendix uses release, erase, and turn off device management for the actions called unlock, wipe, and unenroll in [a.4](a.4-roles-and-permissions-matrix.md) and [a.7](a.7-fleetctl-command-reference.md). [a.1](a.1-capability-index.md) includes both sets of terms.

Some tasks have separate platform-specific rows. For example, the Mac-lock row uses `Not applicable` for Windows because Windows lock has its own row.

Each cell has one value. Follow its condition ID when the behavior needs further explanation.

## The matrix

![Reference](../_assets/icons/reference-light.svg) The matrix contains 292 capability rows. Bold section rows group related tasks and have no platform values.

| ID | Capability | macOS | iOS/iPadOS | Windows | Linux | Android | ChromeOS | Licence | Prerequisite |
|---|---|---|---|---|---|---|---|---|---|
| **A. Identity, access, and governance** | | | | | | | | | |
| **CAP-022** | Keep a host's activity history across an Apple ADE re-enrollment | Conditional (C001) | Conditional (C002) | Not applicable | Not applicable | Not applicable | Not applicable | Free | Apple MDM configured, automated enrollment, first check-in of the new enrollment |
| **CAP-023** | Read a disk-encryption recovery key | Supported | Not applicable | Supported | Conditional (C003) | Not applicable | Not applicable | Free to read, Premium prerequisite to escrow | MDM configured for the platform, and a stored key |
| **CAP-024** | Have the read of a secret recorded as an event | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | Disk encryption already escrowed |
| **B. Enrollment and host lifecycle** | | | | | | | | | |
| **CAP-025** | Create and hold enroll secrets for a scope | Supported | Supported | Supported | Supported | Supported | Supported | Free globally, Premium per fleet | None |
| **CAP-026** | Rotate an enroll secret without a flag day | Supported | Supported | Supported | Supported | Supported | Supported | Free globally, Premium per fleet | None |
| **CAP-027** | Enroll a Mac in MDM automatically during Setup Assistant | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple Business Manager token, and the serial assigned to Fleet there |
| **CAP-028** | Enroll a Mac in MDM from a link, company-owned | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Free | Apple MDM configured, and a valid enroll secret |
| **CAP-029** | Enroll a personally owned device from a link | Supported | Supported | Unsupported | Not applicable | Supported | Not applicable | Free | A valid enroll secret, and the platform's own management already in place: Apple MDM configured for a Mac, iPhone or iPad, and Android management configured with an enterprise record for an Android device |
| **CAP-030** | Download an unsigned manual macOS enrollment profile | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple MDM configured |
| **CAP-031** | Download the default Setup Assistant profile | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple MDM configured |
| **CAP-032** | Have Fleet install the agent on a Mac it enrolls | Supported | Unsupported | Not applicable | Not applicable | Not applicable | Not applicable | Free | Apple MDM enrollment on the device channel |
| **CAP-033** | Suppress Fleet's ADE agent install so a bootstrap package delivers it | Conditional (C004) | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable | Premium | A bootstrap package already configured |
| **CAP-034** | Attach the end user's identity at enrollment | Conditional (C005) | Conditional (C006) | Conditional (C007) | Conditional (C008) | Conditional (C009) | Not established (E01) | Premium | An identity provider configured for MDM features |
| **CAP-389** | Decide on the server whether an agent that does not authenticate may enroll | Not applicable | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | A fleet that requires end-user authentication, and the setting made in server configuration rather than through any interface. The gate exists only for Linux and Windows agent enrollments, which is why macOS reads Not applicable: a Mac settles end-user authentication during MDM enrollment instead |
| **CAP-035** | Enroll a Windows host by installing the agent | Not applicable | Not applicable | Conditional (C010) | Not applicable | Not applicable | Not applicable | Free | Windows MDM configured, and the host already agent-enrolled |
| **CAP-036** | Enroll a Windows host at first boot through Autopilot | Not applicable | Not applicable | Conditional (C011) | Not applicable | Not applicable | Not applicable | Premium | Windows MDM configured, and the Entra tenant and client lists populated |
| **CAP-037** | Let a person enroll a Windows host from Settings | Not applicable | Not applicable | Conditional (C012) | Not applicable | Not applicable | Not applicable | Premium | Windows MDM configured, and the Entra lists populated |
| **CAP-038** | Stop Fleet enrolling Windows hosts unasked | Not applicable | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Premium | Windows MDM turned on |
| **CAP-039** | Move Windows hosts off another MDM with no user interaction | Not applicable | Not applicable | Conditional (C013) | Not applicable | Not applicable | Not applicable | Premium | Windows MDM turned on, and the host already agent-enrolled |
| **CAP-040** | Prompt a Mac's user to migrate from another MDM | Conditional (C014) | Unsupported | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Migration turned on, a webhook destination set, and the host eligible |
| **CAP-041** | Have Fleet push the agent to an Entra-enrolled Windows host | Not applicable | Not applicable | Conditional (C015) | Not applicable | Not applicable | Not applicable | No direct gate, Premium-only prerequisite | An Entra-enrolled host and a global enroll secret |
| **CAP-042** | Enroll a Linux host | Not applicable | Not applicable | Not applicable | Supported | Not applicable | Not applicable | Free | A valid enroll secret, supplied with the server address |
| **CAP-043** | Re-point or reconfigure a deployed Linux agent without rebuilding | Not applicable | Not applicable | Not applicable | Supported | Not applicable | Not applicable | Free | Root on the host, and a service restart |
| **CAP-044** | Build a macOS package that carries no URL or secret | Supported | Not applicable | Unsupported | Unsupported | Not applicable | Not applicable | Free | A device-level agent configuration profile delivered by MDM |
| **CAP-045** | Supply a Windows host's URL, secret and flags at install time | Not applicable | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Free | Installer properties supplied on the command line |
| **CAP-046** | Enroll an iPhone or iPad automatically | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple Business Manager token, with the devices assigned to Fleet |
| **CAP-047** | Enroll an iPhone or iPad from a link, company-owned | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Free to enroll, Premium to attach the owner | Apple MDM configured, and a valid enroll secret |
| **CAP-049** | Have a person enroll their own device with a Managed Apple Account | Unsupported | Conditional (C016) | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple Business Manager token, MDM single sign-on, and a Managed Apple Account |
| **CAP-051** | Place an ADE device in a fleet by platform | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple Business Manager token uploaded |
| **CAP-383** | Release a device from Apple Business | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple Business connected, the device assigned to this Fleet server there, Apple Business itself set to allow this service to release devices, and a global administrator or an administrator of the host's fleet |
| **CAP-052** | Enroll an Android device as a personal work profile | Not applicable | Not applicable | Not applicable | Not applicable | Supported | Not applicable | Free | Android Enterprise bound, and a valid enroll secret |
| **CAP-053** | Enroll a company-owned Android device by QR at first boot | Not applicable | Not applicable | Not applicable | Not applicable | Conditional (C017) | Not applicable | Free | Android Enterprise bound, and the device at its out-of-box screen |
| **CAP-054** | Issue a single-use Android enrollment token | Not applicable | Not applicable | Not applicable | Not applicable | Supported | Not applicable | Free | Android Enterprise bound, and a valid enroll secret |
| **CAP-055** | Enroll a Chromebook | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable | Supported | Free | A valid enroll secret in Chrome policy, and the extension force-installed |
| **CAP-056** | Give a host a hardware-backed identity certificate | Unsupported | Not applicable | Unsupported | Conditional (C018) | Not applicable | Not applicable | Premium | A TPM 2.0 device, and the server private key set |
| **CAP-057** | Require signed requests from every host | Conditional (C019) | Not applicable | Conditional (C020) | Conditional (C021) | Not applicable | Not applicable | Premium | A server configuration key, set before start |
| **CAP-058** | Recognise a returning device and keep its host record | Supported | Supported | Supported | Supported | Supported | Supported | Free | None |
| **CAP-059** | Enroll two operating systems on one machine as two hosts | Conditional (C022) | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | Chosen at packaging time |
| **CAP-060** | Move a host to another fleet | Supported | Supported | Supported | Supported | Supported | Supported | No direct gate, Premium-only prerequisite | A named fleet to move the host to |
| **CAP-061** | Delete a host record | Supported | Supported | Supported | Supported | Supported | Supported | Free | None |
| **CAP-062** | Retire a host so it stays retired | Conditional (C023) | Conditional (C024) | Supported | Supported | Supported | Supported | Free to delete, Premium to restore | The Apple Business Manager assignment must change for a delete to stick |
| **CAP-063** | Expire host records automatically after a silence window | Conditional (C025) | Conditional (C026) | Supported | Supported | Supported | Supported | Free globally, Premium per fleet | None |
| **C. Agent (fleetd) management** | | | | | | | | | |
| **CAP-064** | Build an installer for a platform | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | Build host must match the package type |
| **CAP-388** | Build an installer that does not ask for end-user authentication | Not applicable | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | fleetd v1.60.0 or later, and an installer you build yourself. On Windows an installer carrying an end-user-authentication token takes precedence and the bypass does not apply |
| **CAP-065** | Include the end-user surface in the agent | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | Chosen at packaging time on macOS and Linux, at install time on Windows |
| **CAP-361** | Let an end user see their own device's details and software | Supported | Supported | Supported | Supported | Supported | Supported | Free | An address for the device. The end-user surface issues one where it runs, an administrator can mint one on every platform except iPhone and iPad, and those two authenticate by certificate or by their own issued address instead |
| **CAP-362** | Let an end user see the summary the desktop menu shows | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Premium | The end-user surface installed. On Free the request is refused with a licence error |
| **CAP-363** | Open an interactive query shell on the host itself | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | The agent installed, and local access to the host. Starts a separate instance, so it does not show the running agent's state |
| **CAP-364** | Force an agent update check without waiting for the interval | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | Updates not disabled at packaging time. The check runs at start, before any subsystem |
| **CAP-066** | Enable scripts on a host at packaging time | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | Chosen at packaging time, or by profile on macOS |
| **CAP-067** | Set an agent's update channel centrally | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Premium | Agent built with updates enabled |
| **CAP-068** | Set an agent's update channel on the host | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | An agent restart |
| **CAP-069** | Pin an agent component to an exact version | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Premium centrally, Free per host | The pinned version must exist in the update repository |
| **CAP-070** | Roll an agent version backwards across the estate | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Premium | Updates not disabled, and the older version still published. Rolling one host back by re-packaging or by changing its own update channel is Free |
| **CAP-071** | Stop an agent updating at all | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | Set at packaging time or by editing the host's service configuration |
| **CAP-072** | Publish agent versions from your own update repository | Supported | Not applicable | Unsupported | Supported | Not applicable | Not applicable | Free, and not enforced | Signing keys present, and an initialised repository |
| **CAP-073** | See what agent version a host is actually running | Supported | Not applicable | Supported | Supported | Not applicable | Supported | Free | The host must be running the Fleet agent, not plain osquery |
| **CAP-074** | Deliver an osquery extension to hosts | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free, Premium once a label is named | Agent updates enabled, and the extension published to the update repository |
| **CAP-075** | Restrict an extension to a label | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Premium | The label must already exist and be in scope |
| **CAP-076** | Set osquery runtime options for a fleet | Supported | Not applicable | Supported | Supported | Not applicable | Not established (E15) | Free globally, Premium per fleet | Agent installed |
| **CAP-077** | Set Orbit's own settings for a fleet | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free globally, Premium per fleet | Agent installed |
| **CAP-078** | Turn on file integrity monitoring | Supported | Not applicable | Supported | Supported | Not applicable | Not established (E16) | Free globally, Premium per fleet | A log destination configured |
| **CAP-079** | Scan hosts with YARA signature sets | Supported | Not applicable | Supported | Supported | Not applicable | Not established (E17) | Free globally, Premium per fleet | Agent installed |
| **CAP-080** | Stamp results with provenance columns | Supported | Not applicable | Supported | Supported | Not applicable | Not established (E18) | Free globally, Premium per fleet | Applies to logged results, not host vitals |
| **CAP-081** | Turn individual osquery event subscribers on or off | Supported | Not applicable | Supported | Supported | Not applicable | Not established (E19) | Free globally, Premium per fleet | Agent installed |
| **CAP-082** | Carve a file off a host | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | A carve store configured |
| **D. Host data, vitals, and inventory** | | | | | | | | | |
| **CAP-083** | See what a device is and what is on it | Supported | Supported | Supported | Supported | Supported | Supported | Free | Enrolled by the platform's own channel |
| **CAP-395** | Sort the host list by when a host last enrolled | Supported | Supported | Supported | Supported | Supported | Supported | Free | None. The sort reads the `last_enrolled_at` column every enrolled host carries, so it has no platform branch |
| **CAP-382** | Read a hardware model as a marketing name rather than an identifier | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Free | The model identifier must be in the mapping the Fleet release ships. Anything else resolves to an empty name and the raw identifier is shown instead, so new hardware needs an upgrade rather than a refetch |
| **CAP-084** | Put a value you collect on the host record | Supported | Not applicable | Supported | Supported | Not applicable | Supported | Free globally, Premium per fleet | None |
| **CAP-085** | Record a value Fleet cannot collect | Supported | Supported | Supported | Supported | Supported | Supported | Free | The vital must be defined first |
| **CAP-086** | Turn a SQLite file on the device into a queryable table | Supported | Not applicable | Supported | Supported | Not applicable | Not established (E20) | Free globally, Premium per fleet | The database file must exist at the given path |
| **CAP-087** | Replace or remove one of Fleet's own detail queries | Supported | Not applicable | Supported | Supported | Not applicable | Supported | Free globally, Premium per fleet | The override must name an existing query |
| **CAP-088** | Collect the local accounts on a device | Supported | Not applicable | Supported | Supported | Not applicable | Supported | Free | None |
| **CAP-089** | See which certificates a host holds | Supported | Supported | Supported | Unsupported | Unsupported | Unsupported | Free | A recent enough osquery on Windows |
| **CAP-090** | Attach an email address to a host | Supported | Supported | Supported | Supported | Supported | Supported | Free set by hand, Premium from the identity provider | None |
| **CAP-091** | Ask a host to report again now | Supported | Supported | Supported | Supported | Not established (E21) | Supported | Free | On iPhone and iPad, Apple MDM configured and connected. On the other platforms none: Fleet records the request for any host, and the agent collects it on its next check-in |
| **CAP-092** | Refresh an iPhone or iPad's inventory on a schedule | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple MDM configured, and push notifications working |
| **CAP-381** | Read the full device-information set an iPhone or iPad reports | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Free | Apple MDM configured, and a company-owned enrollment. A personal enrollment is sent a shorter request and receives three of the twenty-nine fields |
| **E. Queries and reports** | | | | | | | | | |
| **CAP-093** | Ask every online device a question now | Supported | Not applicable | Supported | Supported | Not applicable | Supported | Free | An enrolled agent, and live queries not disabled |
| **CAP-095** | Collect a question's answer on a schedule | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Free | An interval above zero, and results not discarded |
| **CAP-096** | Keep the newest result per host in Fleet | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Free | Results not discarded, and snapshot logging |
| **CAP-097** | Send a report's results to a log destination | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Free | A destination chosen at server start |
| **CAP-098** | Read a report's results across the estate | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Free | Results not discarded |
| **CAP-099** | Read one host's result, including a successful empty one | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Free | None |
| **CAP-100** | Retrieve stored report rows for export | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Free | Results not discarded |
| **CAP-101** | Keep a report away from platforms whose tables do not exist | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Free | None |
| **CAP-102** | Keep a report away from agents too old to run it | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | None |
| **CAP-103** | Run a report on a percentage of its targets | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | A pack, with the query scheduled into it |
| **CAP-104** | Narrow a report to hosts carrying a label | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Premium | The labels must exist and be in scope |
| **CAP-105** | Let an observer run a chosen report | Supported | Not applicable | Supported | Supported | Not applicable | Supported | Free | The query must be saved |
| **CAP-110** | See what a report costs the estate | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Free | Scheduled query statistics turned on |
| **CAP-111** | Collect per-host query statistics at all | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | A server configuration key, set before start |
| **CAP-112** | Bound what a query may cost a host | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | Values must match the agent's known flag set |
| **CAP-113** | Let, or refuse to let, osquery stop an expensive query | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | Settable only through a pack |
| **F. Policies** | | | | | | | | | |
| **CAP-114** | Ask a yes-or-no compliance question of every host | Supported | Not applicable | Supported | Supported | Not applicable | Supported | Free | Agent installed |
| **CAP-115** | Assert that a Fleet-maintained app is at or above a version | Supported | Unsupported | Supported | Unsupported | Unsupported | Unsupported | No direct gate, Premium-only prerequisite | A Fleet-maintained app installer must exist, and the policy must be fleet-scoped |
| **CAP-393** | Assess a host against Fleet's published CIS benchmark policies | Supported | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Premium | The benchmark set for the host's operating-system version converted and applied yourself, normally through GitOps. Import the policies separately; an upgrade does not install them or update existing copies |
| **CAP-116** | Scope a policy to a platform | Supported | Not applicable | Supported | Supported | Not applicable | Supported | Free | None |
| **CAP-117** | Narrow a policy by label | Supported | Not applicable | Supported | Supported | Not applicable | Supported | Premium | Labels must exist and not appear on both sides |
| **CAP-118** | Mark a policy as one whose failure matters | Supported | Not applicable | Supported | Supported | Not applicable | Supported | Premium | None |
| **CAP-119** | Read how many hosts pass and fail a policy | Supported | Not applicable | Supported | Supported | Not applicable | Supported | Free | None |
| **CAP-120** | Clear a policy's collected results | Supported | Not applicable | Supported | Supported | Not applicable | Supported | Free | None |
| **G. Software and vulnerability knowledge** | | | | | | | | | |
| **CAP-122** | Collect what software is installed | Supported | Conditional (C028) | Supported | Supported | Supported | Conditional (C029) | Free | Software inventory turned on, and enrollment by the platform's own channel |
| **CAP-380** | Read the Adobe Creative Cloud plugins installed on a host | Supported | Unsupported | Supported | Unsupported | Unsupported | Unsupported | Free | Software inventory turned on, and a fleetd build that provides the `adobe_plugins` table. The detail query names macOS and Windows and no other platform, so the rest are never asked |
| **CAP-123** | Turn software inventory on for one fleet | Supported | Not applicable | Supported | Supported | Not applicable | Supported | Free globally, Premium per fleet | The host must be assigned to the fleet |
| **CAP-124** | See which installed software has known vulnerabilities | Supported | Unsupported | Supported | Supported | Not established (E02) | Not established (E03) | Free | Software inventory on, and a vulnerability database path configured |
| **CAP-125** | See which operating system builds have known vulnerabilities | Supported | Unsupported | Conditional (C030) | Supported | Conditional (C031) | Unsupported | Free | A vulnerability database path configured |
| **CAP-126** | Prioritise findings by severity and exploitation | Supported | Unsupported | Supported | Supported | Conditional (C032) | Not established (E04) | Premium | Vulnerability metadata populated |
| **CAP-127** | Filter and sort by those fields | Supported | Unsupported | Supported | Supported | Conditional (C033) | Not established (E05) | Premium | Vulnerability metadata populated |
| **CAP-128** | See the version that fixes a finding | Supported | Unsupported | Supported | Supported | Conditional (C034) | Not established (E06) | Premium | Vulnerability metadata populated |
| **CAP-131** | Browse what Fleet knows how to install | Supported | Not established (E32) | Supported | Not established (E33) | Not established (E34) | Not established (E35) | Premium | Outbound network reach to the app catalogue |
| **H. Estate-wide reading and targeting** | | | | | | | | | |
| **CAP-133** | Read the estate's headline counts | Supported | Conditional (C035) | Supported | Supported | Conditional (C036) | Supported | Free | None |
| **CAP-134** | Read how many hosts are low on disk | Supported | Supported | Supported | Supported | Supported | Unsupported | Premium | A threshold between 1 and 100 GiB |
| **CAP-135** | See how many automated enrollments are not healthy | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Free to read the count, Premium to make it non-zero | An Apple Business Manager token, and MDM configured |
| **CAP-136** | See which hosts were online over time | Supported | Supported | Supported | Supported | Supported | Supported | Free | Historical uptime collection left on |
| **CAP-137** | Export a host list for use outside Fleet | Supported | Supported | Supported | Supported | Supported | Supported | Free | None |
| **CAP-138** | Read the host list programmatically | Supported | Supported | Supported | Supported | Supported | Supported | Free, with Premium-only filters silently dropped | None |
| **CAP-139** | Be told when too much of the estate goes quiet | Supported | Conditional (C037) | Supported | Supported | Conditional (C038) | Supported | Free globally, Premium per fleet | A destination URL, a day count and a percentage |
| **CAP-140** | Select hosts by a query that keeps itself current | Supported | Not applicable | Supported | Supported | Unsupported | Supported | Free globally, Premium per fleet | Agent installed |
| **CAP-387** | Restrict a label's query to one platform | Supported | Unsupported | Supported | Supported | Unsupported | Unsupported | Free | A dynamic label. Fleet rejects a platform on a manual or host-vitals label, and the accepted values are the empty string, `darwin`, `windows`, `linux`, `ubuntu` and `centos`, so no other platform can be named. The choice is fixed when the label is created |
| **CAP-141** | Select a specific list of hosts | Supported | Supported | Supported | Supported | Supported | Supported | Free globally, Premium per fleet | A manual label, and write access to every target host |
| **CAP-142** | Select hosts by a reported vital | Supported | Supported | Supported | Supported | Supported | Supported | Free for a hand-set vital, Premium for identity-provider vitals | Exactly one criterion, and the vital must exist |
| **I. Configuration profiles and declarative settings** | | | | | | | | | |
| **CAP-146** | Put a setting on an Apple device and keep it there | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Free globally without labels, Premium per fleet or with labels | Apple MDM configured, and an unsigned profile |
| **CAP-147** | Let an Apple device hold and report its own desired state | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Free globally without labels, Premium with variables or for updates | Apple MDM configured |
| **CAP-148** | Put a setting on a Windows device | Not applicable | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Free globally without labels, Premium per fleet or with labels | Windows MDM configured |
| **CAP-149** | Configure an Android device | Not applicable | Not applicable | Not applicable | Not applicable | Supported | Not applicable | Free globally without labels, Premium per fleet or with labels | Android MDM configured, and Android Enterprise bound |
| **CAP-150** | Give one fleet its own profiles | Supported | Supported | Supported | Not applicable | Supported | Not applicable | Premium | The platform's MDM configured |
| **CAP-151** | Narrow a profile to hosts carrying a label | Supported | Supported | Supported | Unsupported | Supported | Unsupported | Premium | The labels must exist and be visible to the fleet |
| **CAP-152** | Fill in a per-host value in a profile | Supported | Supported | Supported | Not applicable | Supported | Not applicable | Premium on Apple and Windows, Free on Android | On Android the variable must sit inside a string value |
| **CAP-385** | Fill in a custom host vital in a profile or a managed app configuration | Supported | Supported | Supported | Not applicable | Supported | Not applicable | Free | The vital must be defined and the host must have a value. An empty value fails that host's profile rather than substituting nothing, and setting a value re-delivers what depends on it for that host alone |
| **CAP-153** | Have a profile enrol a certificate | Supported | Supported | Supported | Unsupported | Supported | Unsupported | Premium | A configured certificate authority of the matching type and name |
| **CAP-154** | Supply a value that is never stored anywhere | Supported | Not established (E07) | Unsupported | Not applicable | Unsupported | Not applicable | Premium | Platform single sign-on configured |
| **CAP-155** | Keep a credential out of a profile's stored content | Supported | Supported | Supported | Not applicable | Unsupported | Not applicable | Free | The server private key set when the secret is written |
| **CAP-156** | Know whether a profile reached a device | Supported | Supported | Supported | Not applicable | Supported | Not applicable | Free | Host MDM-enrolled on the matching platform |
| **CAP-157** | Send a profile to a host again | Supported | Supported | Supported | Unsupported | Unsupported | Unsupported | Free | The platform's MDM configured |
| **CAP-158** | Take a profile off devices | Supported | Supported | Supported | Not applicable | Supported | Not applicable | Free globally, Premium per fleet | None |
| **J. Scripts** | | | | | | | | | |
| **CAP-159** | Run a one-off script on a device | Supported | Unsupported | Supported | Supported | Unsupported | Unsupported | Free globally, Premium per fleet | Agent installed with scripts enabled |
| **CAP-160** | Keep a script in a library and run it | Supported | Unsupported | Supported | Supported | Unsupported | Unsupported | Free globally, Premium per fleet | A recognised file extension, and matching interpreter line |
| **CAP-161** | Wait for a script's result | Supported | Unsupported | Supported | Supported | Unsupported | Unsupported | Free globally, Premium per fleet | Host online, with nothing already pending |
| **CAP-162** | Run a script across many hosts at once | Supported | Unsupported | Supported | Supported | Unsupported | Unsupported | No licence check on the run; Premium only to create the fleets a fleet batch targets | All targets in the same fleet as the script |
| **CAP-163** | Stop every script running anywhere | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | None |
| **CAP-164** | Let a script run for longer than five minutes | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | A value of 18,000 seconds or less |
| **CAP-165** | Read what a script did | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | A script must have run |
| **CAP-166** | Use a credential in a script without storing it | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | The server private key configured |
| **CAP-167** | Use a host's own vital inside an install or script | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | The referenced vital must be defined |
| **CAP-379** | Fill in one of Fleet's built-in variables inside a script | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Premium | One of eight supported names, and a value Fleet can resolve for the host. Any other `$FLEET_VAR_` name is refused when the script is saved, and an unresolvable one ends the run at exit code -5 before the script executes |
| **K. Software delivery** | | | | | | | | | |
| **CAP-168** | Deliver software you package yourself | Supported | Unsupported | Supported | Supported | Unsupported | Unsupported | Premium | Agent installed with scripts enabled |
| **CAP-169** | Deliver an application from Fleet's catalogue | Supported | Unsupported | Supported | Not established (E41) | Unsupported | Unsupported | Premium | Outbound reach to the app catalogue |
| **CAP-170** | Deliver a purchased App Store application | Supported | Supported | Unsupported | Unsupported | Unsupported | Unsupported | Premium | Apple MDM on, host connected, and a token assigned to the host's fleet |
| **CAP-171** | Make a Play application available | Unsupported | Unsupported | Unsupported | Unsupported | Supported | Unsupported | Premium | Android Enterprise bound, and the app in the managed catalogue |
| **CAP-172** | Deliver an app you built yourself to iPhones and iPads | Unsupported | Supported | Unsupported | Unsupported | Unsupported | Unsupported | Premium | A genuine iOS application archive with a bundle identifier |
| **CAP-173** | Put a shortcut to a URL on an Android device | Unsupported | Unsupported | Unsupported | Unsupported | Supported | Unsupported | Premium | Android Enterprise bound, and a unique name within the fleet |
| **CAP-174** | Deliver a `.sh`, `.ps1` or `.py` as a package | Supported | Unsupported | Supported | Supported | Unsupported | Unsupported | Premium | A recognised extension, with a matching interpreter line |
| **CAP-175** | Gate an install on a condition the device reports | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Premium | Agent installed |
| **CAP-176** | Have Fleet write the install and uninstall logic for you | Supported | Not applicable | Conditional (C040) | Supported | Not applicable | Not applicable | Premium | Package identifiers must be extractable |
| **CAP-177** | Install software on a host | Supported | Supported | Supported | Supported | Unsupported | Unsupported | Premium | Agent installed, or MDM connected for the Apple path |
| **CAP-178** | Uninstall software from a host, as an administrator | Conditional (C041) | Unsupported | Supported | Supported | Unsupported | Unsupported | Premium | Agent installed with scripts enabled, and an uninstall script on file |
| **CAP-365** | Let an end user uninstall their own software | Conditional (C041) | Unsupported | Supported | Supported | Unsupported | Unsupported | Premium | The title offered as self-service, and the end-user surface installed. Authenticated by the device's own address, not by a Fleet account |
| **CAP-352** | Retry a failed software install or uninstall by hand | Supported | Supported | Supported | Supported | Unsupported | Unsupported | Premium | A failed install or uninstall to retry. Re-issuing the action, which is what the retry does, carries the same requirements as the original |
| **CAP-179** | Ship different builds of one title to different hosts | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Premium | At most ten packages per title |
| **CAP-180** | Hold a catalogue app at a version | Supported | Supported | Supported | Supported | Supported | Supported | Premium | A cached version must exist |
| **CAP-181** | Keep the library's catalogue apps current | Supported | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Premium | An installer store, and no literal version pin |
| **CAP-182** | Go back to the previous catalogue version | Supported | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Premium | The target version must still be cached |
| **CAP-183** | Configure a managed application on an Apple device | Unsupported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Premium | The configuration must be supplied as a string containing the markup |
| **CAP-184** | Configure a managed application on Android | Not applicable | Not applicable | Not applicable | Not applicable | Supported | Not applicable | Premium | Android Enterprise bound, and not a web app |
| **CAP-185** | Choose when apps update on a device | Unsupported | Supported | Unsupported | Unsupported | Unsupported | Unsupported | Premium | The host must report a time zone, and a token must exist for its fleet |
| **CAP-186** | Remove something from the library | Supported | Supported | Supported | Supported | Supported | Not applicable | Premium | None |
| **CAP-187** | Serve installers to hosts through a CDN | Supported | Supported | Supported | Supported | Not applicable | Not applicable | No direct gate, Premium-only prerequisite | A content delivery URL with a signing key pair |
| **CAP-188** | Accept a very large installer | Supported | Supported | Supported | Supported | Not applicable | Not applicable | Premium | None |
| **L. Setup and self-service experiences** | | | | | | | | | |
| **CAP-189** | Prepare a device before its user starts using it | Supported | Conditional (C043) | Conditional (C044) | Conditional (C045) | Not established (E40) | Unsupported | Premium | The platform's own management channel configured and the device enrolled through it: automated enrollment on macOS, iPhone and iPad, first boot on Windows, the agent on Linux, and Android Enterprise on Android |
| **CAP-190** | Run a script as part of setup | Supported | Unsupported | Unsupported | Unsupported | Not applicable | Not applicable | Premium | Automated enrollment, with manual agent install off |
| **CAP-191** | Deliver a package to a Mac before the agent exists | Supported | Unsupported | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Automated enrollment, and Apple MDM configured |
| **CAP-192** | Create the user's local account during setup | Supported | Unsupported | Not applicable | Not applicable | Not applicable | Not applicable | Premium at delivery, not refused at the settings interface | Automated enrollment, and Apple MDM configured |
| **CAP-372** | Provision a Mac's local account and sync its password with the identity provider | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple MDM configured, an OAuth identity provider set for account provisioning, and the server private key set |
| **CAP-374** | Create and hold a managed local administrator account on Windows | Not applicable | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Premium | Windows MDM turned on, fleetd 1.60.0 or later on the host, and the server private key set to encrypt the escrowed password |
| **CAP-193** | Show the user an agreement during setup | Conditional (C046) | Supported | Unsupported | Not applicable | Not applicable | Not applicable | Premium | An identity provider configured for MDM features |
| **CAP-194** | Hold a Windows device at a status page until setup finishes | Not applicable | Not applicable | Conditional (C047) | Not applicable | Not applicable | Not applicable | No direct gate, Premium-only prerequisite | Windows MDM configured, and automatic enrollment at first boot |
| **CAP-195** | Show setup progress without holding anyone up | Unsupported | Not applicable | Conditional (C049) | Supported | Not applicable | Not applicable | Premium | Agent installed with the end-user surface enabled |
| **CAP-196** | Install software during an automated Apple enrollment | Supported | Supported | Not applicable | Not applicable | Not applicable | Unsupported | Premium | A purchase token with licences available |
| **CAP-197** | Push an app to an Android device at enrollment | Not applicable | Not applicable | Not applicable | Not applicable | Supported | Not applicable | Premium | Android Enterprise bound |
| **CAP-198** | Install setup software only on devices that need it | Unsupported | Unsupported | Supported | Supported | Not applicable | Not applicable | Premium | A fleet policy whose automation points at the same installer |
| **CAP-199** | Stop setup when a piece of software fails | Supported | Unsupported | Conditional (C050) | Unsupported | Not applicable | Not applicable | Premium | Windows MDM turned on |
| **CAP-200** | Control when a Mac or iPhone is released | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple MDM configured |
| **CAP-201** | Retry only the setup steps that failed | Conditional (C051) | Not applicable | Unsupported | Unsupported | Not applicable | Not applicable | Premium | Require-all-software on, a failed install, and an agent restart |
| **CAP-202** | Offer software for people to install themselves | Supported | Conditional (C052) | Supported | Supported | Conditional (C053) | Unsupported | Premium | The end-user surface on desktop platforms, a web clip on Apple mobile |
| **CAP-203** | Group a large self-service catalogue | Supported | Conditional (C054) | Supported | Supported | Unsupported | Not applicable | Premium | As the row above |
| **CAP-204** | Let a user install everything offered to them | Supported | Conditional (C055) | Supported | Supported | Unsupported | Unsupported | Premium | As the row above |
| **CAP-366** | Choose whether a Play application is offered as self-service | Not applicable | Not applicable | Not applicable | Not applicable | Unsupported | Not applicable | Premium | Android Enterprise bound, and the application already in the library |
| **M. Operating system updates** | | | | | | | | | |
| **CAP-205** | Require a minimum OS version by a date on Apple devices | Supported | Supported | Not applicable | Unsupported | Unsupported | Unsupported | Premium | Apple MDM on, with a minimum version and a deadline set together |
| **CAP-376** | Track the latest OS version Apple publishes for each host | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple MDM on, `minimum_version` set to `latest` with `deadline_days` and no fixed deadline, and hosts on macOS 14, iOS 17 or iPadOS 17 and later |
| **CAP-206** | Prompt users on older Macs to update | Conditional (C056) | Unsupported | Unsupported | Unsupported | Not applicable | Not applicable | Premium | Agent enrolled, host connected to MDM, and macOS updates configured |
| **CAP-207** | Set an update deadline and restart grace on Windows | Not applicable | Not applicable | Supported | Unsupported | Unsupported | Unsupported | Premium | Windows MDM on, with both fields set together |
| **CAP-208** | Control Android system updates | Not applicable | Not applicable | Not applicable | Unsupported | Supported | Unsupported | Premium | Android MDM configured, and Android Enterprise bound |
| **CAP-209** | Express an update policy the built-in form cannot | Conditional (C057) | Conditional (C058) | Conditional (C059) | Not applicable | Not applicable | Not applicable | Premium | The built-in update settings must be unset for that scope |
| **CAP-210** | Update a Mac or iPhone during automated enrollment | Conditional (C060) | Conditional (C061) | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Host in automated enrollment, and able to request a software update |
| **CAP-211** | Enforce a Linux OS version | Not applicable | Not applicable | Not applicable | Unsupported | Not applicable | Not applicable | Not applicable | Not applicable |
| **CAP-212** | See whether devices actually reached the version | Supported | Supported | Unsupported | Unsupported | Unsupported | Unsupported | Free | A minimum version set for the host's scope |
| **N. Device actions and MDM commands** | | | | | | | | | |
| **CAP-213** | Lock a Mac | Conditional (C062) | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple MDM configured, host enrolled, and not a personal enrollment |
| **CAP-214** | Lock an iPhone or iPad | Not applicable | Conditional (C063) | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple MDM configured, and an automatic enrollment |
| **CAP-215** | Lock a Windows host | Not applicable | Not applicable | Conditional (C064) | Not applicable | Not applicable | Not applicable | Premium | Windows MDM configured, and the agent installed with scripts enabled |
| **CAP-216** | Lock a Linux host | Not applicable | Not applicable | Not applicable | Conditional (C065) | Not applicable | Not applicable | Premium | Agent installed with scripts enabled, running as root |
| **CAP-217** | Lock an Android device | Not applicable | Not applicable | Not applicable | Not applicable | Conditional (C066) | Not applicable | Premium | Android Enterprise bound, and the device enrolled |
| **CAP-367** | Lock a Chromebook | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable | Unsupported | Not applicable | Not applicable |
| **CAP-218** | Release a locked Mac | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable | Premium | The host must currently be locked, and a person at the keyboard |
| **CAP-219** | Release a locked iPhone or iPad | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Premium | The device must check in over push for the command to land |
| **CAP-220** | Release a locked Windows host | Not applicable | Not applicable | Conditional (C067) | Not applicable | Not applicable | Not applicable | Premium | Machine powered on with the agent running, and scripts enabled |
| **CAP-221** | Release a locked Linux host | Not applicable | Not applicable | Not applicable | Conditional (C068) | Not applicable | Not applicable | Premium | Agent installed with scripts enabled, running as root |
| **CAP-222** | Release a locked Android device | Not applicable | Not applicable | Not applicable | Not applicable | Unsupported | Not applicable | Not applicable | Not applicable |
| **CAP-368** | Release a locked Chromebook | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable | Unsupported | Not applicable | Not applicable |
| **CAP-223** | Erase a Mac | Conditional (C069) | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple MDM configured, host connected, and not a personal enrollment |
| **CAP-224** | Erase an iPhone or iPad | Not applicable | Conditional (C070) | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple MDM configured, host connected, and not a personal enrollment |
| **CAP-225** | Erase a Windows host | Not applicable | Not applicable | Conditional (C071) | Not applicable | Not applicable | Not applicable | Premium | Windows MDM configured, and the host enrolled in it |
| **CAP-226** | Erase a Linux host | Not applicable | Not applicable | Not applicable | Conditional (C072) | Not applicable | Not applicable | Premium | Agent installed with scripts enabled, running as root |
| **CAP-227** | Erase a company-owned Android device | Not applicable | Not applicable | Not applicable | Not applicable | Supported | Not applicable | Free | Android Enterprise bound, device enrolled, and company-owned |
| **CAP-369** | Erase a Chromebook | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable | Unsupported | Not applicable | Not applicable |
| **CAP-370** | Turn Fleet's device management off for one host | Supported | Supported | Unsupported | Unsupported | Supported | Unsupported | Free | The host must currently be enrolled in Fleet's management for its platform |
| **CAP-228** | Remove Fleet's management from a personally owned Android device | Not applicable | Not applicable | Not applicable | Not applicable | Supported | Not applicable | Free | Android Enterprise bound, and the device enrolled with a work profile |
| **CAP-229** | Find where a device is | Unsupported | Conditional (C073) | Unsupported | Unsupported | Unsupported | Unsupported | Premium | Automated enrollment assigned to Fleet, and the device in lost mode |
| **CAP-230** | Clear a device's passcode | Unsupported | Conditional (C074) | Unsupported | Unsupported | Supported | Unsupported | Premium | Apple MDM configured, non-personal enrollment, and an unlock token on file |
| **CAP-231** | Send a raw command to Apple devices | Conditional (C075) | Conditional (C076) | Not applicable | Unsupported | Unsupported | Unsupported | Free, Premium for three Apple request types | Apple MDM configured, and every target connected and on one platform |
| **CAP-232** | Send a raw command to Windows devices | Not applicable | Not applicable | Conditional (C077) | Unsupported | Unsupported | Unsupported | Free, Premium for the remote-wipe subtree | Windows MDM configured, and every target enrolled |
| **CAP-233** | Read what a device said about a command | Supported | Supported | Supported | Not applicable | Unsupported | Not applicable | Free | At least one MDM configured |
| **CAP-234** | Cancel a device action before it happens | Conditional (C078) | Conditional (C079) | Conditional (C080) | Conditional (C081) | Conditional (C082) | Not applicable | Free | The activity must still be queued for that host |
| **O. Disk encryption and recovery credentials** | | | | | | | | | |
| **CAP-235** | Turn FileVault on and hold the recovery key | Conditional (C083) | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple MDM configured, the server private key set, and a user login |
| **CAP-371** | Rotate the FileVault recovery key Fleet holds for a Mac | Conditional (C106) | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable | No direct gate, Premium-only prerequisite | Apple MDM configured, the host connected to it and agent-enrolled, and disk encryption enforced for its scope |
| **CAP-236** | Turn BitLocker on and hold the protector | Not applicable | Not applicable | Conditional (C084) | Not applicable | Not applicable | Not applicable | Premium | Windows MDM configured, agent enrolled, and a TPM on a non-server edition |
| **CAP-237** | Hold a recovery credential for an already-encrypted Linux host | Not applicable | Not applicable | Not applicable | Conditional (C085) | Not applicable | Not applicable | Premium | A supported distribution, already encrypted, with encryption enforced for the scope |
| **CAP-238** | Escrow silently on a TPM-backed Ubuntu host | Not applicable | Not applicable | Not applicable | Conditional (C086) | Not applicable | Not applicable | Premium | Snap-managed encryption, a reachable service socket, and the disk tool installed |
| **CAP-239** | Escrow by prompting the user for their LUKS passphrase | Not applicable | Not applicable | Not applicable | Conditional (C087) | Not applicable | Not applicable | Premium | A dialog tool, a desktop session, and a person who knows the passphrase |
| **CAP-240** | Know whether a disk is encrypted at all | Supported | Not applicable | Supported | Supported | Not applicable | Not established (E08) | Free | Agent installed and enrolled |
| **CAP-241** | Read the disk-encryption status summary | Supported | Not applicable | Supported | Conditional (C088) | Not applicable | Not applicable | Premium | Disk encryption enforced for the scope |
| **CAP-242** | Set a BitLocker startup PIN | Not applicable | Not applicable | Conditional (C089) | Not applicable | Not applicable | Not applicable | Premium | Windows MDM configured, encryption on for the scope, and a TPM |
| **CAP-243** | Allow a custom disk-encryption profile alongside Fleet's own | Conditional (C090) | Not applicable | Conditional (C091) | Not applicable | Not applicable | Not applicable | Premium | Server-level configuration and a restart |
| **CAP-244a** | Turn Recovery Lock on for a scope | Conditional (C092) | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable | Free globally, Premium per fleet | Apple silicon, enrolled and not personally enrolled, with the setting on for the scope |
| **CAP-244b** | Reveal a Mac's Recovery Lock password | Supported | Unsupported | Unsupported | Unsupported | Unsupported | Unsupported | Free | Apple silicon, and Apple MDM configured |
| **CAP-353** | Retrieve or rotate the managed local administrator password | Supported | Unsupported | Unsupported | Unsupported | Unsupported | Unsupported | Premium | The managed local account turned on for the scope. Fleet refuses any host that is not a Mac, by name |
| **CAP-244c** | Rotate a Recovery Lock password | Conditional (C093) | Unsupported | Unsupported | Unsupported | Unsupported | Unsupported | Premium | Apple silicon, MDM connected, and an existing password |
| **CAP-245** | Stop enforcing encryption without losing what is held | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Premium | The decryption material for the platform must still be held |
| **P. Policy automations, integrations, and outbound events** | | | | | | | | | |
| **CAP-246** | Install software when a policy fails | Supported | Unsupported | Supported | Supported | Unsupported | Unsupported | Premium | Agent installed, and an installer for the host's platform |
| **CAP-378** | Hold a patch policy's install until the app is closed | Supported | Unsupported | Supported | Unsupported | Unsupported | Unsupported | Premium | A patch policy on a Fleet-maintained app, with continuous automations on. Fleet refuses the option on a title you packaged yourself, because the closed-app check reads the maintained-app manifest |
| **CAP-247** | Install an App Store app when a policy fails | Supported | Unsupported | Unsupported | Unsupported | Unsupported | Unsupported | Premium | Agent installed |
| **CAP-248** | Run a script when a policy fails | Supported | Unsupported | Supported | Supported | Unsupported | Unsupported | Premium | Agent installed |
| **CAP-252** | Report a host as non-compliant to Microsoft Entra | Supported | Unsupported | Supported | Unsupported | Unsupported | Unsupported | Premium | Agent installed |
| **CAP-253** | Refuse a sign-in when a host is failing a policy | Supported | Not applicable | Not established (E09) | Unsupported | Not applicable | Unsupported | Premium | A proxy in front of Fleet that forwards the client certificate serial |
| **CAP-254** | Grant a one-time bypass of conditional access | Supported | Not applicable | Not established (E10) | Unsupported | Not applicable | Unsupported | Premium | Conditional access already refusing the sign-in |
| **CAP-255** | Act on every failing result rather than on the transition | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Premium | Agent installed |
| **CAP-257** | Send osquery status and result logs to a destination | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Free | Agent installed |
| **R. Platform management configuration (Apple, Windows, Android)** | | | | | | | | | |
| **CAP-269** | Turn on Apple device management | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Free | The server private key must be set |
| **CAP-270** | Renew the Apple push certificate without resetting the estate | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Free | Apple MDM already on |
| **CAP-271** | Have Fleet re-issue each host's identity certificate | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Free | Apple MDM already on |
| **CAP-272** | Connect Fleet to Apple Business | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple MDM already on |
| **CAP-273** | Renew the Apple Business token | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple MDM already on |
| **CAP-274** | Control what Setup Assistant shows on an ADE device | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Premium | An Apple Business Manager token |
| **CAP-275** | Add or remove an App Store application | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple MDM already on, and the licence already purchased in Apple Business. Fleet cannot buy one: it looks for an asset you already hold and tells you to purchase it there when it finds none |
| **CAP-276** | Renew the Volume Purchasing token | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Premium | A purchase token uploaded |
| **CAP-277** | Learn from Fleet that an Apple credential is expiring | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Free for the push certificate, Premium for the rest | The relevant Apple credential must be on file |
| **CAP-373** | Require hardware-attested device identity for eligible Macs | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple MDM configured, automated enrollment, and an Apple Silicon Mac on macOS 14 or later. The requirement is skipped for a Mac that does not qualify |
| **CAP-278** | Turn on Windows device management | Not applicable | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Free | A certificate and key pair configured in server settings |
| **CAP-279** | Choose whether Windows enrollment asks the end user | Not applicable | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Premium | Windows MDM already on |
| **CAP-375** | Choose the fleet user-driven Windows enrollments land in | Not applicable | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Premium to name a fleet, Free to clear it | Windows MDM turned on and Fleet connected to Entra. A host is only moved when the enrollment carries a signed-in user, the host has no fleet yet, and its record is new to Fleet |
| **CAP-280** | Turn Windows device management off | Not applicable | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Free | Windows MDM already on |
| **CAP-281** | Bind Fleet to an Android Enterprise | Not applicable | Not applicable | Not applicable | Not applicable | Supported | Not applicable | Not established (E42) | The server private key set, a server address that is not localhost, and Android **not** already configured |
| **CAP-282** | Deliver client certificates to Android devices | Not applicable | Not applicable | Not applicable | Not applicable | Supported | Not applicable | Premium | A custom SCEP proxy authority, which is the only type accepted, plus the Android binding and a non-empty companion application package |
| **CAP-283** | Tune Android API pressure and the companion app identity | Not applicable | Not applicable | Not applicable | Not applicable | Supported | Not applicable | Free | None, though the settings are absent from the generated reference |
| **CAP-284** | Turn Android device management off | Not applicable | Not applicable | Not applicable | Not applicable | Supported | Not applicable | Free | Android Enterprise bound |
| **S. Organization and server settings** | | | | | | | | | |
| **CAP-285** | Set the address everything uses to reach Fleet | Conditional (C094) | Conditional (C095) | Not established (E11) | Not established (E12) | Conditional (C096) | Not applicable | Free to change, Premium for the automatic re-sync | None |
| **CAP-289** | Point end-user error messages at your own help desk | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable | Free for settings and the device page, Premium for the desktop surface | None |
| **CAP-292** | Attach the end user's IdP identity to their devices | Supported | Supported | Supported | Supported | Supported | Unsupported | Premium | End-user authentication enabled for the scope |
| **CAP-293** | Set a host's IdP username by hand | Supported | Supported | Supported | Supported | Supported | Supported | Premium | None |
| **CAP-295** | Send scheduled-report results somewhere | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Free | A destination chosen at server start |
| **CAP-296** | Send osquery's own status messages somewhere | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Free | A destination chosen at server start |
| **T. Running and operating the service** | | | | | | | | | |
| **CAP-307** | Prove a restored Fleet can still decrypt what it holds | Supported | Not applicable | Supported | Conditional (C097) | Not applicable | Not applicable | Free to read, Premium prerequisite to escrow | The decryption material for the platform must still be held |
| **CAP-310** | Rotate the server's HTTPS certificate without disconnecting agents | Conditional (C098) | Not applicable | Conditional (C099) | Conditional (C100) | Not applicable | Not established (E13) | Free | Depends on how the agent was packaged |
| **CAP-311** | Renew the Windows enrolment certificate | Not applicable | Not applicable | Conditional (C101) | Not applicable | Not applicable | Not applicable | Free | Windows MDM already on |
| **CAP-325** | Simulate load against a deployment | Supported | Supported | Supported | Supported | Supported | Unsupported | Free | None |
| **U. Diagnostic actions and introspection surfaces** | | | | | | | | | |
| **CAP-329** | Read the agent's own log on a host | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | Agent installed, and administrator rights on the host |
| **CAP-330** | Inspect the Orbit root directory on a host | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | Agent installed, and administrator rights on the host |
| **CAP-331** | Raise an agent's verbosity for a bounded window | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free globally, Premium per fleet | Agent installed, and a re-enrollment for the setting to take effect |
| **CAP-332** | Raise an agent's verbosity permanently | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | Re-packaging, host shell access, or an agent-options push, by lever |
| **CAP-335** | Read a host's own osquery introspection tables | Supported | Not applicable | Supported | Supported | Not applicable | Conditional (C102) | Free | Agent installed and checking in |
| **CAP-336** | Read the Apple MDM command queue | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Free | Apple MDM configured and the host enrolled |
| **CAP-390** | Read why Apple Business is not returning a device | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Free | Apple Business connected. A false `token_invalid` means Apple is not known to have rejected the token, not that the token has been checked and is healthy |
| **CAP-337** | Read the Windows MDM command queue | Not applicable | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Free | Windows MDM configured and the host enrolled |
| **CAP-338** | Read Android's command and policy state | Not applicable | Not applicable | Not applicable | Not applicable | Supported | Not applicable | Free | Android Enterprise bound |
| **CAP-341a** | Trigger a Windows MDM diagnostic collection | Not applicable | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Free | Windows MDM configured, host connected, and a destination for the archive |
| **CAP-341b** | Retrieve the produced diagnostic archive through Fleet | Not applicable | Not applicable | Not established (E14) | Not applicable | Not applicable | Not applicable | Free | Windows MDM configured, and the collection already triggered |
| **CAP-344** | Trade host-data freshness for server load | Supported | Not applicable | Supported | Supported | Not applicable | Supported | Free | A server restart |
| **CAP-345** | Move host processing through Redis instead of MySQL | Supported | Not applicable | Supported | Supported | Not applicable | Conditional (C103) | Free | A server restart |
| **CAP-346** | Stop hosts sharing an identifier from overwriting each other | Supported | Not applicable | Supported | Supported | Not applicable | Supported | Free | A server restart, and no hosts already enrolled |
| **CAP-347** | Find the limit that is silently truncating your data | Supported | Not applicable | Supported | Supported | Not applicable | Conditional (C104) | Free | A server restart, or an agent-options push |
| **CAP-348** | Rank what each scheduled query costs a host | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Free | Agent installed, with scheduled query statistics left on |

## The condition register

Each `Conditional` cell links to a record explaining when the operation works and when it does not. The 101 records cover 102 cells because administrator and self-service uninstall share one condition. Gaps in condition numbering preserve IDs from retired records so existing citations remain stable.

**C001** CAP-022, macOS. Supported when the preserve setting is on for the host's scope and the Mac reaches Setup Assistant on the first check-in of the new enrollment: past activity survives. Not supported when the setting is off, in which case past activity and the pending command queue are both cleared. On macOS only, a migration already in progress skips the reset entirely, so history survives whatever the setting says.

**C002** CAP-022, iOS/iPadOS. Supported on the same three conditions as macOS, with the setting deciding the outcome. Not supported when the setting is off. The migration exemption does not exist here, so on iPhone and iPad the setting always applies on a first check-in after re-enrollment.

**C003** CAP-023, Linux. Supported when the host runs a distribution Fleet escrows for, meaning Ubuntu, Zorin, Fedora, Arch, Manjaro or CachyOS, and the server private key is set. Not supported on any other distribution, Debian and non-Fedora Red Hat derivatives included, which fall through to the Apple branch and fail, and not supported when the private key is unset, which returns an unavailable-key error before any lookup.

**C004** CAP-033, macOS. Supported when manual agent install is on for the host's scope, so Fleet skips its own agent install and only the bootstrap package is sent. Not supported when it is off, which is the default, because Fleet sends the agent installer as usual. The setting resolves from the fleet configuration when the host has one, otherwise from the deployment configuration.

**C005** CAP-034, macOS. Supported when end-user authentication is on for the enroll secret's scope: the over-the-air endpoints refuse to issue a profile without an identity, and the automated enrollment path routes through MDM single sign-on. Not supported when it is off, because enrollment proceeds anonymously.

**C006** CAP-034, iOS/iPadOS. Supported on the same setting and the same over-the-air path as macOS, and always supported for account-driven user enrollment, which consumes the identity provider account from the enrollment challenge. Not supported when the setting is off and the enrollment is not account-driven.

**C007** CAP-034, Windows. Supported when the setting is on: an agent enrollment carrying no identity is refused so the agent can prompt for one, and an installer that carried an authenticated token has that token validated and enrollment continues. Not supported when the setting is off, and not applied when the host was previously agent-enrolled, which is let through without a prompt.

**C008** CAP-034, Linux. Supported when the setting is on, by the same refuse-and-prompt branch as Windows, minus the pre-authenticated installer token, which is Windows only. Not supported when the setting is off. Fleet states the boundary directly: agent enrollment is gated on end-user authentication for Linux and Windows only, because on macOS the MDM enrollment handles it.

**C009** CAP-034, Android. Supported when the enroll secret's scope requires end-user authentication, in which case the enrollment must carry an identity provider reference and that reference must resolve. Not supported when the setting is off, because the enrollment token is issued without one.

**C010** CAP-035, Windows. Supported when Windows MDM is configured and manual turn-on is off: every agent check-in from an eligible host carries the enrollment instruction and a discovery endpoint, and the agent enrolls itself. Not supported when either condition fails, because the instruction is never set. Eligibility also requires the host to be agent-enrolled, not a Windows Server edition, and not already enrolled in any MDM.

**C011** CAP-036, Windows. Supported when the Entra tenant and client lists are populated: the enrollment handler accepts the device's Azure token, extracts the user name and records the enrollment as automatic. Not supported when the tenant list is empty, in which case the request is refused outright. Ownership is recorded as company-owned only when the device is also at first boot.

**C012** CAP-037, Windows. Settings-app enrollment is recorded as manual when the device reports that it is outside first boot, and refetch preserves that classification. First-boot enrollment follows the automatic path described by CAP-036.

**C013** CAP-039, Windows. Supported when Windows migration is turned on and the host is currently enrolled in a non-Fleet MDM: the agent is told to unenroll itself and Fleet shortens the refetch window so the change is ingested quickly. Not supported when the host is not in a third-party MDM, in which case nothing happens.

**C014** CAP-040, macOS. Supported when macOS migration is turned on, a webhook destination is set, and the host is eligible: the device page posts the migration webhook and shortens the refetch window, and the end-user surface shows the prompt. Not supported when any of those is missing, which returns an error naming the specific reason.

**C015** CAP-041, Windows. Supported when the enrolled device carries a valid user principal name and no recent agent check-in is on record: the session-start alert enqueues an installer download and a silent install, with scripts enabled and an optional authentication token. Not supported when the enrollment carries no user name, which is what a programmatic agent-driven enrollment looks like, because Fleet then treats the agent as already present and skips the install.

**C016** CAP-049, iOS/iPadOS. Supported when the licence is Premium and the enrollment token in the address resolves to an Apple Business Manager token: the first request challenges the device for a web sign-in against Fleet's MDM single sign-on address, and the second returns a signed account-driven profile carrying the assigned Managed Apple ID. Not supported without that token, or without MDM single sign-on and an identity provider configured. The result is always recorded as a personal enrollment.

**C017** CAP-053, Android. Supported when the enrollment token is requested as fully managed, which disallows personal usage and renders a QR code alongside factory-reset instructions. Not supported when that flag is absent, in which case the token produces a work-profile enrollment instead, which is a different row.

**C018** CAP-056, Linux. Supported when the agent was packaged with the managed host identity certificate option and the host has a usable TPM 2.0: the agent generates a hardware-backed key, obtains a certificate over the enrollment protocol using a valid enroll secret, and signs later requests through a local signing proxy. Not supported when no TPM is present, in which case setup fails and the end-user surface reports the device as unavailable. The option is refused outright on any operating system other than Linux.

**C019** CAP-057, macOS. With signature enforcement off, unsigned requests pass without signature verification. With it on, Fleet rejects unsigned requests on covered paths. The requirement applies to Macs, but macOS packages and agents cannot satisfy it at this release. Enabling it therefore disconnects those agent paths.

**C020** CAP-057, Windows. Unsigned requests pass when enforcement is off. Enabling it rejects unsigned Windows requests on covered paths, while Windows packages and agents cannot provide the required host-identity signing. The enabled requirement is enforced but cannot be satisfied at this release.

**C021** CAP-057, Linux. Supported when the setting is on and the host holds a certificate: requests are signed and the server verifies them. Not supported when the setting is on and the host has no certificate, in which case every agent and osquery request is refused with an authentication error.

**C022** CAP-059, macOS. Supported when the agent is packaged to identify hosts by instance rather than by hardware identifier, which suppresses the serial-matching branch on agent enrollment. Not supported on the Apple MDM side, where the enrollment path matches on serial regardless and no suppression applies, so the two operating systems merge back into a single host record.

**C023** CAP-062, macOS. Supported, meaning the deletion sticks, when the Mac has no live automated enrollment assignment, or when the licence is Free, where the restore path never runs. Not supported when the Mac has a live assignment on Premium, because the delete restores a pending host inside the same request. The restore reuses the host identifier and unique identifier but deliberately not the agent identifier.

**C024** CAP-062, iOS/iPadOS. A deletion can remain effective when the device has no live ADE assignment, is no longer enrolled, or the Premium restore path does not run on Free. On Premium, a live ADE assignment recreates a pending record within the deletion request. Separately, any still-enrolled iPhone or iPad can reappear at its next MDM check-in, including devices without an ADE assignment.

**C025** CAP-063, macOS. Supported when the Mac has no live automated enrollment assignment and its last contact is older than the configured window. Not supported when it has a live assignment, which makes the record permanently immune to expiry.

**C026** CAP-063, iOS/iPadOS. Supported on the same rule, with last contact read from the MDM channel because these platforms never write an agent last-seen record. Not supported when the device has a live automated enrollment assignment.

**C028** CAP-122, iOS/iPadOS. Supported for the full installed-application list when the device was enrolled through automated device enrollment. Not supported beyond Fleet-managed apps when the device was enrolled manually or personally, because Fleet then asks the device for managed applications only, on both the hourly refresh and an operator-triggered refetch.

**C029** CAP-122, ChromeOS. Supported for browser extensions, which is the only software source declared for ChromeOS. Not supported for desktop applications, because the three desktop software queries carry platform lists that ChromeOS is absent from.

**C030** CAP-125, Windows. Supported when the setting that disables Windows operating-system vulnerability processing is left off, which is the default: Fleet analyses Windows builds against the vendor's security data. Not supported when it is turned on, in which case the definition sync still runs but no Windows operating-system finding is ever produced.

**C031** CAP-125, Android. With the open-source vulnerability feed enabled, Fleet refreshes feed data and analyzes Android OS builds. Disabling it stops new Android OS analysis but leaves existing findings until no host reports the build, so retained findings can become stale. The setting also affects Ubuntu and Red Hat analysis.

**C032** CAP-126, Android. Supported when the open-source vulnerability feed setting is on, so Android operating-system findings exist for the scoring, filtering and fixed-version machinery to shape. That machinery is per-vulnerability, joined from the shared vulnerability metadata, with no Android-specific branch. Not supported when the setting is off, because no Android finding is produced for these fields to describe. Whether Android application findings additionally exist is unsettled and recorded separately; if they do, the same shaping applies with no extra gate.

**C033** CAP-127, Android. Supported when the open-source vulnerability feed setting is on, so Android operating-system findings exist to filter and sort. The fields are per-vulnerability and carry no Android-specific branch. Not supported when the setting is off, because no Android finding is produced. Whether Android application findings additionally exist is unsettled and recorded separately.

**C034** CAP-128, Android. Supported when the open-source vulnerability feed setting is on, so Android operating-system findings exist and each carries its own fixed-version field on the finding row. Not supported when the setting is off, because no Android finding is produced. Whether Android application findings additionally exist is unsettled and recorded separately.

**C035** CAP-133, iOS/iPadOS. Supported for the total, the new count, the per-platform breakdown and the missing count, which falls back to the MDM channel's last-seen time and then to the detail-update time. Not supported for the online and offline split, which reads an agent last-seen record these devices never write, so they read as permanently offline. Devices still pending automated enrollment are excluded from the counts outright.

**C036** CAP-133, Android. Supported for the totals and for the missing count, which falls back to the detail-update time Fleet writes on every management check-in, so an actively managed Android host is not permanently missing. Not supported for the online and offline split, for the same reason as Apple mobile: no agent last-seen record is ever written.

**C037** CAP-139, iOS/iPadOS. These hosts enter the quiet-estate check's total count, but the check cannot provide a useful management-availability signal for them. They never write the agent last-seen field, so they enter the unseen count once the configured days have elapsed. This path has no MDM last-seen fallback.

**C038** CAP-139, Android. Android hosts enter the total count, then the unseen count after the configured days, because they never write an agent last-seen value. The check therefore does not reflect whether Android management is active.

**C040** CAP-176, Windows. Supported for a Windows installer package, for which Fleet generates both the install and the uninstall script, including the variant that uninstalls by upgrade code. Not supported for an executable or an archive, where both generators return nothing, so the upload is refused unless the administrator supplies both scripts by hand.

**C041** CAP-178 and CAP-365, macOS. The same constraint governs both, because an end user's self-service uninstall runs the same machinery as an administrator's. Supported for a package Fleet stores as macOS, meaning an installer package or a Fleet-maintained app: the uninstall script is queued and run like any other script. Not supported for a shell or Python package, which Fleet stores as Linux and refuses to uninstall on a Mac, even though the same host was allowed to install it.

**C043** CAP-189, iOS/iPadOS. Automated enrollment can hold the device in Setup Assistant until purchased applications finish. Fleet provides no agent, script, installer, or setup dialog on these platforms, and unsupported item types fail with an explanatory message. Outside automated enrollment, items can be queued once without holding the device.

**C044** CAP-189, Windows. Supported by a different mechanism: at first boot with automatic enrollment the device is held at the Windows enrollment status page. Not supported as Fleet's macOS pre-desktop experience, which Windows never gets. Outside first boot the device gets the non-blocking browser page instead.

**C045** CAP-189, Linux. Supported only in its non-blocking form, which reports software status. Not supported as a pre-desktop hold: there are no profiles, no bootstrap package, no account configuration and no release step on Linux.

**C046** CAP-193, macOS. Supported when the Mac enrolls through automated device enrollment, end-user authentication is on, and an agreement has been uploaded. Not supported when any of those is missing, in which case Setup Assistant never opens the web view, or the agreement reference is empty and the callback falls through to the enrollment profile.

**C047** CAP-194, Windows. Supported when the device enrolls automatically and is at first boot: Fleet marks it as awaiting configuration and sends the settings that hold it on the status page and block progress. Not supported when either condition fails, in which case the device is never marked, the status-page commands are never sent, and it takes the ordinary non-blocking path.

**C049** CAP-195, Windows. Supported when the agent starts and the server says the setup experience is enabled: the agent opens the device page in a browser window and registers a poller that writes a completion marker when all software reaches a terminal state. Not supported as a hold, because that poller blocks nothing.

**C050** CAP-199, Windows. Supported when require-all-software is on for Windows and the host is inside a Fleet-tracked enrollment status page, either pending or active: a failure cancels the remaining work and drives the hard-block choice. Not supported outside that window, which Fleet enumerates: a work or school account added after first boot, a programmatic agent enrollment after first boot, an agent with no Windows MDM, and any host that has already finished or timed out the status page.

**C051** CAP-201, macOS. Supported when the host has a failed software install, require-all-software is on, and the request asks to reset the failed steps: only the failed items are rebuilt and successful installs and purchases are excluded from re-insertion. Not supported otherwise, and the agent asks for it only on its first poll after a restart, so an ordinary poll never triggers it.

**C052** CAP-202, iOS/iPadOS. Supported for the mechanism: Fleet provides the device authentication these platforms need, by client certificate or by an address carrying the host identifier, and refuses ordinary device-token authentication for them explicitly. Not supported for the surface: Fleet builds no web clip, so the administrator must supply the shortcut that puts the catalogue on the device.

**C053** CAP-202, Android. Apps marked available can be installed from Managed Google Play. That user action creates no Fleet install-request record; forced setup installs have a separate record. CAP-366 covers the self-service setting, whose supplied value is not honored on Android.

**C054** CAP-203, iOS/iPadOS. Supported only through a shortcut the administrator authored, on the same terms as the row above. Not supported as a Fleet-built surface, because Fleet builds no web clip to group anything in.

**C055** CAP-204, iOS/iPadOS. Supported for purchased applications, reachable over client-certificate or address-based device authentication. Not supported for anything else, because no other software type is installable on these platforms by this path.

**C056** CAP-206, macOS. Supported when all of the following hold: Apple MDM enabled and configured, an MDM configuration present, the host agent-enrolled and connected to Fleet's MDM, macOS updates configured for its scope, and the host's operating system old enough to need the prompt. Not supported when any one fails, in which case no prompt configuration is sent at all.

**C057** CAP-209, macOS. Supported when no built-in Apple operating-system update setting is configured for that scope. Not supported when one is, in which case the custom declaration is refused with a message telling the administrator to remove the built-in settings first. The exclusion runs both ways and is family-wide: a custom declaration for any Apple platform blocks configuring built-in updates for all three.

**C058** CAP-209, iOS/iPadOS. Supported when no built-in Apple operating-system update setting is configured for that scope. Not supported when one is, which refuses the custom declaration. The check treats macOS, iPhone and iPad as one family in both directions, so a declaration for any of the three blocks configuring built-in updates for all three.

**C059** CAP-209, Windows. Supported when no built-in Windows operating-system update setting is configured for that scope. Not supported when one is, in which case the custom profile is refused. The exclusion covers the whole update policy subtree, not only the handful of nodes Fleet itself writes, and it runs in both directions.

**C060** CAP-210, macOS. Supported when the update-new-hosts switch is on for the host's scope: with no minimum version set the Mac is always taken to the latest release, and with one set the ordinary below-minimum comparison decides. Not supported when the switch is off, which is also what an unset switch reads as, in which case the enrollment never requires an update.

**C061** CAP-210, iOS/iPadOS. Supported when a minimum version is set for the platform: an automatically enrolled iPhone or iPad below that version is required to update, and the update requested is Apple's latest release rather than the configured target. Not supported when no minimum version is set, because the check returns early for any non-Mac. The update-new-hosts switch itself is macOS only and is blanked for these platforms.

**C062** CAP-213, macOS. Supported when the enrollment is not personal, Apple MDM is configured, and the host is currently connected to Fleet's MDM: a lock command with a Fleet-generated six-digit PIN is sent. Not supported for a personal enrollment, which is refused by name, nor when MDM is off or the host is disconnected, and not while another lock, unlock or wipe is pending or the host is already locked or wiped.

**C063** CAP-214, iOS/iPadOS. Supported when the enrollment is automatic, meaning automated device enrollment, and Apple MDM is configured and connected: Fleet enables lost mode with a message naming the organisation. Not supported for a personal enrollment, and not for a manual one, which is refused by name for iPhone and iPad specifically. No PIN is generated on this path.

**C064** CAP-215, Windows. Supported when Windows MDM is configured and the host is not known to have scripts disabled: a lock script is queued. Not supported when Windows MDM is off, and not when the host reports scripts disabled, which is refused with a message telling the administrator to redeploy the agent with scripts enabled and refetch.

**C065** CAP-216, Linux. Supported when the host is not known to have scripts disabled: a lock script is queued. Not supported when scripts are disabled, with the same redeploy-and-refetch refusal as Windows. No MDM of any kind is required, because the Windows MDM check is skipped for Linux.

**C066** CAP-217, Android. Lock is supported for personal and company-owned devices when Android MDM is configured and the host is connected. Fleet sends a long-duration AMAPI command. The request is refused if Android management is not configured or the device is unenrolled.

**C067** CAP-220, Windows. Supported when Windows MDM is configured and the host is not known to have scripts disabled: an unlock script is queued. Not supported when scripts are disabled, which is refused with the redeploy-and-refetch message.

**C068** CAP-221, Linux. Supported when the host is not known to have scripts disabled: an unlock script is queued. Not supported when scripts are disabled. No MDM check applies to Linux.

**C069** CAP-223, macOS. Supported when the enrollment is not personal, Apple MDM is configured, and the host is connected to Fleet's MDM: an erase command with a generated PIN is sent. Not supported for a personal enrollment, which is refused by name, and not while a lock, unlock or wipe is pending, or the host is currently locked or already wiped.

**C070** CAP-224, iOS/iPadOS. Supported when the enrollment is not personal, Apple MDM is configured, and the host is connected. Not supported for a personal enrollment, which includes account-driven user enrollment, since that is recorded as personal. A manual non-personal enrollment is allowed here, unlike lock, which refuses it.

**C071** CAP-225, Windows. Wipe requires configured Windows MDM and a connected host. Fleet sends a protected remote-wipe command by default and accepts an explicitly requested unprotected variant. Other wipe types are rejected. This MDM operation does not require scripts; requests fail when MDM is off or the host is disconnected.

**C072** CAP-226, Linux. Supported when the host is not known to have scripts disabled: a wipe script is queued and runs as root. Not supported when scripts are disabled, which is refused with the redeploy-and-refetch message. No MDM of any kind is required or checked on this path.

**C073** CAP-229, iOS/iPadOS. Supported when the platform is iPhone or iPad, Apple MDM is enabled and configured, the licence is Premium, and the device is assigned to Fleet through automated device enrollment: Fleet asks the device for its location and stores it. Not supported when any of those fails, in which case the host falls back to a network-address estimate. The request is sent in exactly two situations, immediately after lost mode is enabled and on refetch while the device is locked.

**C074** CAP-230, iOS/iPadOS. Supported when Apple MDM is enabled and configured, the enrollment is not personal, and Fleet holds an unlock token for the device. Not supported for a personal enrollment or when no unlock token is held, both of which are refused with the same message. Delivery can still fail later if the token has gone missing when the command is expanded.

**C075** CAP-231, macOS. Supported when Apple MDM is configured, every targeted host is MDM-connected, and all targets are on one platform Fleet supports for MDM: the supplied payload is decoded and enqueued as sent. Not supported when the targets span platforms, which is refused by name, or when any target is disconnected, or when the payload does not decode.

**C076** CAP-231, iOS/iPadOS. Supported on the same path as macOS, because Fleet maps iPhone and iPad onto the Apple branch for command dispatch. Not supported on the same three grounds: mixed target platforms, a disconnected target, or a payload that does not decode.

**C077** CAP-232, Windows. Supported when Windows MDM is configured, every target is connected and on one platform, and the payload is a single top-level execute element containing exactly one item. Not supported when any of those shape rules fails, each of which is refused with its own message, and not when a target is disconnected.

**C078** CAP-234, macOS. Supported for queue-backed work, meaning script runs and software installs, which can be cancelled until they activate. Not supported for lock and wipe on a Mac, which are MDM commands rather than queue entries and are outside this operation entirely.

**C079** CAP-234, iOS/iPadOS. Supported for queue-backed work, which on these platforms means purchased and in-house application installs. Not supported for anything else, because there are no script activities without an agent, and MDM commands are not queue entries.

**C080** CAP-234, Windows. Supported for queue-backed work, which on Windows includes lock and unlock, because both are scripts. Not supported once such an entry has activated, which is refused with a message explaining that letting a lock or wipe be cancelled at that point risks losing access to the host. Windows wipe is an MDM command rather than a queue entry and is outside this operation entirely.

**C081** CAP-234, Linux. Supported for queue-backed work, which on Linux includes lock, unlock and wipe, because all three are scripts, so all three can be cancelled before they activate. Not supported once they have activated, which is refused on the same grounds as Windows.

**C082** CAP-234, Android. Supported for queue-backed work only. Not supported for lock, wipe or passcode clearing, which are management-API commands tracked separately rather than queue entries.

**C083** CAP-235, macOS. Supported when Apple MDM is enabled and configured and the server private key is set: Fleet delivers its own encryption profile, which enables the disk encryption, escrows the key to Fleet and blocks the user from turning it off. Not supported when Apple MDM is off, in which case the setting is still saved but no profile is ever delivered, and not without the server private key, which is refused by name. The key itself arrives by agent query after a user login.

**C084** CAP-236, Windows. Supported when some MDM is configured, the host is MDM-connected and agent-enrolled, disk encryption is on for its scope, the edition is not a server edition, and either the disk is unencrypted or it is encrypted but Fleet holds no usable key. Not supported when any of those fails, in which case the enforcement instruction is simply never set in the agent's configuration.

**C085** CAP-237, Linux. Supported when the distribution is one Fleet escrows for, disk encryption is enforced for the host's scope, the disk is already encrypted, and a person triggers the escrow from the device page. Not supported on any other distribution, which is refused with a message saying so, and not without that trigger, because nothing else ever sets the flag that produces the agent instruction.

**C086** CAP-238, Linux. Supported when the host's encryption is managed by the system snap service, which Fleet detects first and prefers: Fleet creates its own named recovery key slot so the user's original key is untouched, and posts a recovery key with no salt and no slot number. Not supported when that service is absent, in which case Fleet falls back to prompting the user, and not when the server rejects the shape of the submission, which refuses a stray salt or slot on this path.

**C087** CAP-239, Linux. Supported when a graphical dialog tool is installed, the disk tool is present, a desktop session exists, the person knows the current passphrase, and a key slot is free: Fleet adds an escrow passphrase and posts it with its salt and slot number. Not supported when no dialog tool is found, which fails immediately, and a cancelled or timed-out prompt is a clean no-op. If the submission fails the added slot is removed again.

**C088** CAP-241, Linux. A supported Linux distribution contributes to verified, action-required, and failed counts when encryption is enforced for its scope. With enforcement off, it contributes no encryption-status result. Linux does not enter verifying, enforcing, or removing-enforcement counts.

**C089** CAP-242, Windows. Supported when disk encryption is on for the same scope, in which case the PIN requirement is accepted and the PIN-related queries are added to the host. Not supported on its own: turning the PIN on without encryption is refused, and turning encryption off while the PIN is required is refused too, each with its own message.

**C090** CAP-243, macOS. Supported when the deployment-level custom disk encryption setting is on, which lets a custom profile carrying Apple's encryption or key-escrow payloads through alongside Fleet's own. Not supported when it is off, which is the default: such a profile is rejected, and so is a managed-preferences payload containing encryption options.

**C091** CAP-243, Windows. Supported when the same deployment-level setting is on, which stops Fleet rejecting a profile that targets the reserved encryption node. Not supported when it is off, which rejects it with the same message as the Apple side. It is one flag governing both platforms.

**C092** CAP-244a, macOS. Supported when the Mac is Apple silicon, has an enabled MDM enrollment on the device or user-enrollment-device channel, is currently enrolled, and is not a personal enrollment: a reconciler picks it up within about half a minute and sets the password. Not supported when any of those fails, because the host is never selected and no password is ever set. Turning the setting off removes the credential rather than leaving it in place.

**C093** CAP-244c, macOS. Supported when the Mac is MDM-connected, the feature is enabled for its scope, a password already exists, no rotation is in flight, no clear is in progress, and the current state is verified or failed. Not supported when any of those fails, each refused with its own typed error. Revealing a password also schedules a rotation an hour later, overwriting whatever was pending.

**C094** CAP-285, macOS. Supported for future enrollments and only on Premium: when the address changes, Fleet re-syncs the Apple automated enrollment profiles so devices enrolling afterwards get the new address. Not supported for devices already enrolled, whose check-in address was baked into the profile they installed and is not re-pointed by anything on this path. A separate setting exists so the device-facing address can be decoupled from the administrator-facing one.

**C095** CAP-285, iOS/iPadOS. Supported for future enrollments and only on Premium, because the automated enrollment re-sync is platform-blind: devices enrolling after the change get the new address. Not supported for devices already enrolled, whose check-in address was baked into the profile they installed.

**C096** CAP-285, Android. Fleet accepts a server-address change, but the existing Android binding remains tied to the old address. The proxy no longer finds that binding under the new address, and a new signup creates another enterprise record. Google's status push destination also remains the address set at enterprise creation.

**C097** CAP-307, Linux. Supported when the host runs a distribution Fleet escrows for and the server private key is still configured, which is what the stored key was encrypted with. Not supported when the private key is missing or has changed, in which case the stored key cannot be decrypted and nothing can be proved.

**C098** CAP-310, macOS. Supported when the agent was packaged without a pinned certificate, in which case the operating system trust store applies and a publicly-trusted rotation is transparent. Not supported when the agent was packaged with one, because that pins a replacement trust store rather than an addition, so the new server certificate must chain to a root already inside the pinned file or verification fails.

**C099** CAP-310, Windows. Supported when the agent was packaged without a pinned certificate, in which case the operating system trust store applies and a publicly-trusted rotation is transparent. Not supported when it was packaged with one, because the pinned file replaces the trust store rather than adding to it, so the new server certificate must chain to a root already inside it. The Windows installer threads the same option through.

**C100** CAP-310, Linux. Supported when the agent was packaged without a pinned certificate, in which case the operating system trust store applies and a publicly-trusted rotation is transparent. Not supported when it was packaged with one, for the same replacement-trust-store reason as macOS and Windows.

**C101** CAP-311, Windows. Supported when the currently configured Windows enrollment certificate is the very certificate the keys were escrowed under, with its private key, because retrieval matches the stored ciphertext to the current certificate by issuer and serial. Not supported after the certificate is replaced or renewed, even by a renewal that keeps the same key pair, because keys escrowed under the previous certificate can no longer be decrypted.

**C102** CAP-335, ChromeOS. Supported for three of the six introspection tables, which the extension declares and answers from its own implementation: the agent information table, the operating-system version table and the system information table. Not supported for the other three, along with carving and agent logs, because those tables do not exist in the extension's closed set, so the query simply returns nothing.

**C103** CAP-345, ChromeOS. Supported for three of the four processing tasks, label membership, policy membership and last-seen, because ChromeOS hosts do submit results and are not excluded from the osquery path. Not supported for scheduled-query statistics, because the query that produces them is explicitly not sent to ChromeOS.

**C104** CAP-347, ChromeOS. Supported for the two request-size limits that apply to the write endpoint, which the extension does call. Not supported for the log-write limit, because the extension never calls the log endpoint, and not for the event and carving limits, which are agent flags for a process ChromeOS does not run.

**C106** CAP-371, macOS. When Fleet finds an undecryptable stored FileVault key and the agent advertises rotation support, Fleet sends a rotation instruction. At the next login, the agent asks for the user's password, creates a replacement key, and escrows it. Without the advertised capability, Fleet logs at DEBUG and sends no instruction or user-visible notification.

This automatic repair applies only to an undecryptable stored key; it provides no on-demand rotation of a healthy key. [a.6](a.6-glossary-and-release-compatibility.md) lists the version requirements.

## Rows that are not platform-scoped

96 rows have no device-platform result. They cover server settings, stored data, identity, automation interfaces, service operations, and hosting arrangements.

They are listed separately below so you can find the task without interpreting six identical `Not applicable` cells.

Use [a.4](a.4-roles-and-permissions-matrix.md) for their permissions and [a.5](a.5-interface-index.md) for their interfaces.


**A. Identity, access, and governance**

- **CAP-001** Sign in to Fleet with a Fleet password. An identity operation against Fleet's own user records, with no device involved.
- **CAP-002** Sign in through the organisation's identity provider. An identity operation: a browser sign-in between Fleet and the identity provider.
- **CAP-003** Have Fleet create the account on first IdP sign-in. An identity operation: account creation inside the sign-in callback.
- **CAP-004** Remove Fleet accounts when people leave, from the IdP. An identity operation: a provisioning protocol the identity provider speaks to Fleet. **Premium**: on Free the provisioning surface returns a licence error without checking anything else.
- **CAP-005** Have SCIM skip accounts it must not delete. An identity operation: a guard inside that provisioning handler. **Premium**, for the same reason as the row above.
- **CAP-006** Challenge a sign-in with an emailed second factor. An identity operation: an email round-trip on the sign-in path.
- **CAP-007** Create or modify a user and give it a global role. An identity operation: a write to Fleet's user records.
- **CAP-008** Give a user the Technician, Observer+ or GitOps role. An identity operation: a write to Fleet's user records.
- **CAP-009** Give a user a role scoped to one or more fleets. An identity operation: a write to the user-to-fleet mapping.
- **CAP-010** Create an API-only identity for automation. An identity operation: a user record marked as automation-only.
- **CAP-011** Give an API-only identity a fleet role. An identity operation: a write to the user-to-fleet mapping.
- **CAP-012** Restrict an API-only identity to named API endpoints. An identity operation: an endpoint allow-list evaluated on the server.
- **CAP-013** Add or remove a member of a fleet. An identity operation: a write to the user-to-fleet mapping.
- **CAP-014** Make managed settings read-only in the interface. Server configuration: a deployment setting the web interface reads.
- **CAP-015** Read the organisation-wide activity feed. A server-side store: the deployment-wide activity record.
- **CAP-016** Read one host's activity feed. A server-side store: one host's activity record, read on the server.
- **CAP-017** Read the work still queued for a host. A server-side store: the queue of work Fleet holds for a host.
- **CAP-018** POST every activity to a URL as it happens. A server-side outbound call made as activities are written.
- **CAP-019** Stream activities to an audit-log destination. A server-side job draining unstreamed activity to a log destination.
- **CAP-020** Know which activities never reach a streamed destination. A server-side store: a marker on the activity record itself.
- **CAP-021** Set how long Fleet keeps activity records. Server configuration: a retention setting driving a cleanup job.
- **CAP-391** Detect a valid password used against an account with a second factor. An identity operation: an activity written on the sign-in path when the verification email goes out.
- **CAP-392** Find out who changed the setup experience script. A server-side store: two activity types written when the stored script is added, replaced or removed.

**B. Enrollment and host lifecycle**

- **CAP-050** Register Fleet's Apple service-discovery URL. Server configuration: registering Fleet's Apple service-discovery address.

**E. Queries and reports**

- **CAP-094** Save a question without running it on a schedule. A server-side store: a saved question that never reaches a device.
- **CAP-106** Turn live reports off for the whole server. Server configuration: one setting that turns live reporting off deployment-wide.
- **CAP-107** Stop storing report results server-wide. Server configuration: one setting that stops results being stored.
- **CAP-108** Stop storing one report's results. A server-side field on one report, with no device component.
- **CAP-109** Cap how many report rows Fleet keeps across hosts. Server configuration: a storage policy over retained report rows.
- **CAP-351** Retire a legacy 2017 query pack. A server-side operation on saved queries: converting or disabling an imported osquery pack, with nothing asked of any device.

**F. Policies**

- **CAP-121** Re-arm a policy's webhook and ticket automations. A server-side operation: re-arming automations already recorded as fired.

**G. Software and vulnerability knowledge**

- **CAP-129** See whether exposure is rising or falling. A server-side time series over host counts, not a device capability.
- **CAP-130** Stop collecting a history dataset. Server configuration: whether a server-side time series is collected.
- **CAP-132** Supply vulnerability data yourself. Server configuration: supplying vulnerability data to the deployment.

**H. Estate-wide reading and targeting**

- **CAP-143** Confine a label to one fleet. A server-side scoping attribute on a label.
- **CAP-144** Give a group of devices its own configuration and its own administrators. A server-side grouping with its own configuration and administrators.
- **CAP-145** Rename a label safely. A server-side operation on the label record.

**P. Policy automations, integrations, and outbound events**

- **CAP-249** POST to a URL when hosts start failing a policy. A server-side automation that posts when policy failures appear.
- **CAP-250** Open a ticket when hosts start failing a policy. A server-side automation that opens a ticket through an integration.
- **CAP-251** Book a maintenance window on the user's calendar. A server-side job over policies and the calendars of the people who own hosts.
- **CAP-256** POST when a new vulnerability is detected. A server-side automation over the vulnerability tables.
- **CAP-377** POST one fleet's host activities to a URL. A server-side outbound call made as host-linked activities are written, one request per fleet.
- **CAP-258** Block webhook destinations on internal addresses. A deployment property of Fleet's outbound network behaviour.
- **CAP-349** Connect a certificate authority. A server-side integration: Fleet stores an external issuing authority's connection details and credentials. Delivering a certificate to a device is the separate CAP-153.

**Q. Automation interfaces**

- **CAP-259** Apply declared configuration from a repository. An automation interface: a client applying declared configuration to the server.
- **CAP-260** Validate configuration before applying it. An automation interface: a client flag that validates without applying.
- **CAP-261** Delete fleets that are not in the repository. An automation interface: a client flag that deletes fleets absent from the repository.
- **CAP-262** Decide whether omitting a section deletes what it describes. Server configuration: three settings deciding what omission means.
- **CAP-263** Turn an existing deployment into YAML. An automation interface: a client command that writes the deployment out as configuration.
- **CAP-264** Make Fleet do anything an administrator can do. An automation interface: Fleet's own route table.
- **CAP-265** Do supported work from a shell. An automation interface: the command-line tool's command set.
- **CAP-266** Reach a route `fleetctl` has no command for. An automation interface: a raw pass-through to any route.
- **CAP-267** Apply or delete a one-off spec file. An automation interface: applying or deleting a single specification file.
- **CAP-268** Generate a CI pipeline for GitOps. An automation interface: pipeline templates the tool writes out.
- **CAP-354** Connect an AI assistant to Fleet. An automation interface: the Fleet MCP server brokers an assistant's read and live-query requests to Fleet's own routes ([a.11](a.11-mcp-tool-reference.md) is the tool reference).

**S. Organization and server settings**

- **CAP-286** Serve Fleet under a URL path. A deployment property: the path Fleet is served under.
- **CAP-287** Let administrators sign in at a different address from devices. Server configuration: a separate sign-in address for administrators.
- **CAP-288** Put your organisation's name and logo in Fleet. Server configuration: organisation name and logo.
- **CAP-290** Have the identity provider decide what a Fleet account may do. An identity operation: role decisions carried in the sign-in assertion.
- **CAP-291** Keep a way in when the identity provider is down. An identity operation: authentication settings on the user record.
- **CAP-294** Confirm Fleet is receiving requests from the identity provider. A server-side status read on the channel to the identity provider.
- **CAP-297** Rotate the token of an API-only identity. An identity operation: rotating an automation identity's token.
- **CAP-298** Remove or demote a user. An identity operation: removing or demoting a user record.

**T. Running and operating the service**

- **CAP-299** Ask Fleet whether it is healthy. A deployment property: an unauthenticated health route on the server.
- **CAP-300** Collect request-level metrics from Fleet. A deployment property: a metrics route mounted on the server.
- **CAP-301** Export traces and internal metrics. A deployment property: trace and metric exporters built at server start.
- **CAP-302** Know whether Fleet's periodic jobs are still running. A server-side store: the record of Fleet's own periodic jobs.
- **CAP-303** Ask Fleet to run one of its schedules now. A server-side operation: asking one of Fleet's schedules to run now.
- **CAP-304** Upgrade the Fleet server. A deployment property: upgrading the server binary and its schema.
- **CAP-305** Check whether migrations are current. A server-side read: whether the schema is current.
- **CAP-306** Back up and restore the deployment. A deployment property: backing up and restoring the server's stores.
- **CAP-308** Keep a restored Fleet from acting on the real world. A deployment property: how a restored server behaves before it is let loose.
- **CAP-309** Read the licence's expiry date. A server-side read: a field on the licence the server holds.
- **CAP-312** Rotate an integration or service secret. A server-side store: integration and service secrets held by the server.
- **CAP-313** Review who has privileged access. An identity operation: reviewing sessions and privileged users.
- **CAP-314** Size the database connection budget. A deployment property: the server's database connection budget.
- **CAP-315** Add read replicas. A deployment property: read replicas behind the server.
- **CAP-316** Configure shared object storage. A deployment property: shared object storage for server-side stores.
- **CAP-317** Put Fleet behind an outbound proxy. A deployment property: outbound proxy configuration for the server process.
- **CAP-350** Enumerate every outbound destination Fleet reaches. A deployment property: the set of addresses the server calls, read for a firewall review rather than asked of any device.
- **CAP-318** Deploy Fleet on AWS from Fleet's reference Terraform. A deployment property: reference infrastructure code for one cloud.
- **CAP-319** Deploy Fleet on GCP from Fleet's reference Terraform. A deployment property: reference infrastructure code for one cloud.
- **CAP-320** Authenticate object storage without a stored key. A deployment property: object-store credentials without a stored key.
- **CAP-384** Serve installer downloads straight from Google Cloud Storage. A deployment property: whether the server proxies the bytes or hands the client a presigned URL. It is mutually exclusive with the row above, because presigning needs the stored key that workload identity exists to remove.
- **CAP-321** Run Fleet with Docker Compose. A deployment property: running the server under container orchestration.
- **CAP-322** Run Fleet on Kubernetes. A deployment property: running the server under container orchestration.
- **CAP-323** Run Fleet as a binary on a virtual machine. A deployment property: running the server as a supervised process.
- **CAP-324** Move vulnerability processing off the serving instances. A deployment property: where vulnerability processing runs.
- **CAP-326** Drain an instance before stopping it. A deployment property: draining a server instance before stopping it.
- **CAP-327** Retire a deployment deliberately. A server-side procedure carried out through Fleet's own interfaces.
- **CAP-328** Have Fleet hosted and operated for you. A commercial arrangement, with no corresponding mode in the software.

**U. Diagnostic actions and introspection surfaces**

- **CAP-333** Collect a diagnostic bundle from the server. A server-side read: a diagnostic bundle of the server's own process.
- **CAP-334** Read Fleet's recorded internal errors. A server-side store: the errors Fleet records about itself.
- **CAP-339** Read the audit record straight from the database. A server-side store: the audit record, read directly from the database.
- **CAP-340** Read the record of Fleet's own scheduled runs. A server-side store: the record of Fleet's own scheduled runs.
- **CAP-343** Ask which Fleet version is answering. A server-side read: which server version is answering.

## Not established

The 28 records below document unresolved cells: 27 platform results and one license result decided by an external service. Each preserves the evidence and search scope from the source review for a later update.

**E01** CAP-034, ChromeOS. End-user identity at enrollment is unverified. The extension uses the normal agent endpoint, whose handler has no ChromeOS identity-authentication branch. The review searched enrollment handling and the extension for identity, end-user authentication, its flags, and related errors without finding an explicit support or rejection path.

**E02** CAP-124, Android. Application vulnerability matching is unverified. Android application rows enter matching, but the reviewed vulnerability tree and translation logic supplied neither a Play Store package-name match generator nor an explicit rejection. Android OS vulnerability analysis is established separately.

**E03** CAP-124, ChromeOS. Extension vulnerability matching is unverified. Extension rows enter the shared matcher, but searches across the vulnerability tree and translation logic found no extension-specific source or explicit rejection.

**E04** CAP-126, ChromeOS. Severity and exploitation fields apply to any generated finding through shared metadata. Whether ChromeOS extension findings exist remains unresolved in E03; this result depends on that same evidence.

**E05** CAP-127, ChromeOS. Filtering and sorting use shared vulnerability fields. Their usefulness for ChromeOS depends on the unresolved extension findings in E03.

**E06** CAP-128, ChromeOS. The fixed-version field belongs to the finding. This result depends on whether extension findings exist, as documented in E03.

**E07** CAP-154, iOS/iPadOS. Use of the Platform SSO registration variable is unverified. It appears in the shared Apple profile allowlist without an iOS/iPadOS exclusion. The review searched Platform SSO packages, stored assets, shared-device-key settings, extension identifiers, and platform checks. Documentation describes a Mac extension, but no enforced mobile-platform boundary was found.

**E08** CAP-240, ChromeOS. Disk-encryption reporting is unverified. ChromeOS is absent from the three agent-query platform lists, and the reviewed extension and query definitions offered no alternate table. The review did not establish a complete support or refusal boundary.

**E09** CAP-253, Windows. Conditional-access policies permit Windows, and the evaluator has no platform check. The source review found only an Apple certificate-delivery path, leaving Windows consumption unverified. Searches covered conditional-access routes, Windows profile handlers, and platform checks.

**E10** CAP-254, Windows. A bypass grant can be stored without a platform check, but consuming it depends on the unresolved Windows certificate path in E09. The review covered the grant, enabled check, consume logic, and platform references in conditional access. No additional delivery path or explicit refusal was found.

**E11** CAP-285, Windows. Repointing an enrolled Windows host after a server-address change is unverified. The settings-change signal feeds Apple re-sync; searches of that handler and Windows MDM found neither a Windows repoint path nor an explicit refusal.

**E12** CAP-285, Linux. Automatic repointing after a server-address change is unverified. The packaged agent supplies its address. Searches of the enrollment handler and agent tree found no repoint path or explicit refusal.

**E13** CAP-310, ChromeOS. The extension's behavior after server-certificate rotation is unverified. Searches for certificates, authority, pinning, and transport security found no pinning option. Ordinary browser requests suggest browser trust handling, but the review did not establish that behavior directly.

**E14** CAP-341b, Windows. Fleet can trigger the diagnostic collection as a raw command and store its raw result. The unresolved question is whether Microsoft's collection protocol returns the archive in that result or uploads it to a supplied destination.

The review covered Fleet's server, UI, and CLI for diagnostic-log providers, result storage, and collection-specific handling. No such parser or retrieval interface was found. A versioned Microsoft protocol reference is needed to settle the archive-delivery behavior.

**E15** CAP-076, ChromeOS. Agent-option delivery remains unverified. The shared server validator and configuration endpoint accept ChromeOS options, while the reviewed extension uses enrollment and live-query endpoints without fetching configuration. Its collection interval is fixed locally.

The UI says Chromebooks ignore agent options, but the review found no server rejection implementing that label. Searches covered validation, schema, platform overrides, configuration lookup, the extension and managed-policy schema, UI, and configuration reference.

**E16** CAP-078, ChromeOS. File integrity monitoring depends on the unresolved agent-options path in E15. The shared schema accepts it without a platform check, but the extension does not request those options. Feature-specific ChromeOS searches across the server, extension, and UI found no additional support or rejection.

**E17** CAP-079, ChromeOS. YARA scanning depends on E15's unresolved agent-options delivery. The shared schema has no platform restriction, and the extension does not fetch it. YARA/ChromeOS searches across the server, extension, and UI found no additional path or rejection.

**E18** CAP-080, ChromeOS. Result provenance columns depend on E15's unresolved agent-options delivery. The shared schema accepts the configuration; searches for this feature with ChromeOS across the server, extension, and UI found no consumer or explicit restriction.

**E19** CAP-081, ChromeOS. Event-subscriber settings depend on the agent-options behavior in E15. They are accepted by the shared schema, but the extension does not fetch them. Feature-specific searches across the server, extension, and UI found no other support or refusal path.

**E20** CAP-086, ChromeOS. SQLite table construction follows E15's unresolved agent-options path. The shared schema accepts it, and the extension does not request it. Searches across the server, extension, and UI found no additional ChromeOS-specific behavior.

**E21** CAP-091, Android. Fleet accepts refetch and sets the generic request flag, but the reviewed Android service has no consumer for it. The additional MDM refetch branch names iOS/iPadOS and contains an open question about Android. Searches covered the full refetch handler, flag consumers, and Android service. With no explicit Android refusal found, the cell remains unverified.

**E32** CAP-131, iOS/iPadOS. The maintained-app catalog comes from an external list, with a fallback to the project's development branch. Its platform field is unrestricted; ingestion copies it, and listing filters only when macOS or Windows is requested.

The review covered fetch addresses, entry types, ingestion, listing options, and platform references. It found no iOS/iPadOS rejection or entry to test, leaving catalog availability unverified.

**E33** CAP-131, Linux. Catalog availability is unverified for the reasons in E32. Linux-specific searches across the catalog code found no additional entry or enforced restriction.

**E34** CAP-131, Android. Catalog availability is unverified on the evidence in E32 and an additional search for Android-specific catalog handling.

**E35** CAP-131, ChromeOS. Catalog availability is unverified on the evidence in E32 and an additional search for ChromeOS-specific catalog handling.

**E41** CAP-169, Linux. Fleet's ingestion and install paths would accept a Linux catalog entry with a matching installer and host platform. Whether the external catalog supplies that entry is unverified. The review covered ingestion, adding an app, install-platform checks, and platform references in maintained-app code.

**E42** CAP-281, license. Android Enterprise binding on Free is unverified. Fleet's signup handler has no local license check, but sends the key to the external proxy that completes binding. The review covered signup, the proxy client, and Android license checks; the proxy's decision remains outside the reviewed source.

**E40** CAP-189, Android. Fleet accepts Android setup-software selection, queues work, and records results. The source review did not establish a device hold, visible progress, or ordered setup steps for Android. Those steps use agent endpoints that Android devices do not call.

Searches covered accepted platforms, software selection, the setup engine and callers, Android management, and hold/progress/ordering behavior. No explicit refusal was found. App delivery through the enrollment policy is established separately in CAP-197.

<a id="one-row-that-is-not-a-fleet-capability"></a>

## Device diagnostics collected outside Fleet

**CAP-342, collect a sysdiagnose from an iPhone or iPad.** The person holding the device collects this through iOS/iPadOS. Fleet neither triggers nor retrieves it: its eighteen-type Apple command list has no collection operation, and these devices have no fleetd script path. Fleet's four documented diagnostic-log recipes are for Windows. This task therefore sits outside the Fleet capability matrix.

<a id="one-row-merged-into-another"></a>

## Combined enrollment row

**CAP-048, enroll a personally owned iPhone or iPad,** is included in the cross-platform CAP-029 row here. [a.5](a.5-interface-index.md) retains it separately because its interface result differs.


## Version notes

![Reference](../_assets/icons/reference-light.svg) The baseline matrix was reviewed against Fleet 4.90.0 source. Documentation helped locate relevant code; cells follow the implementation evidence, including differences from published guidance noted in [a.6](a.6-glossary-and-release-compatibility.md).

Recheck `Unsupported` and `Not established` when upgrading. An explicit platform restriction supports the former; an unresolved delivery path without such a restriction supports the latter. `Not applicable` describes a subject without a platform equivalent.

Match each restriction to the exact operation in its row. A platform filter for listing reports, for example, does not establish whether Fleet accepts that platform when creating or delivering a report.

The condition and evidence records preserve those operation-specific distinctions for later reviews.

Catalog availability remains `Not established` where the source accepts an external platform value but the reviewed catalog provides no entry to test. A description naming two platforms does not impose a code-level restriction.

Version pinning of an existing catalog app is different: once a cached version meets the row's prerequisite, the operation changes the active installer without a platform check. That row therefore remains `Supported` across all six columns.
