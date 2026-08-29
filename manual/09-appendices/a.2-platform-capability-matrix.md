---
title: "Platform capability matrix"
chapter: "Appendices and indexes"
section: "A.2"
sidebar_position: 2
status: drafting
verified_against: Fleet 4.90.1
verified_on: 2026-08-29
verified_source: "drafted against fleet-v4.90.1 (dd0200f062) over two research passes. Every cell rests on source read at the tag; Fleet's documentation was used for leads only, never as evidence. Citation ledger at research/section-notes/a.2-notes.md"
reviewed_by:
reviewed_on:
further_reading:
  - https://fleetdm.com/docs/get-started/faq
feature_requests:
  labels: [":product"]
  match: ["platform", "iOS", "Android", "ChromeOS", "Linux"]
  exclude: []
---

# Platform capability matrix

**Platform support is a per-capability contract, not a property of an operating system.** Fleet does not support macOS and not support Android. It supports a particular thing on a particular platform, by a particular mechanism, sometimes on one licence and not another, and the answer changes capability by capability rather than platform by platform.

## What this appendix carries

![Reference](../_assets/icons/reference.svg) Every device-facing capability the manual teaches, across six platform columns, with the licence and the prerequisites that change the answer.

**Licence and prerequisite are columns, never cell values**, which is the appendix's main structural decision. Folding a licence into a cell would put this project's least reliable claim class inside its most consulted table, and it would answer two questions with one word. The rule itself is restated where you will need it, above the matrix.

**What is not here.** Operating system versions and floors are [a.6](a.6-glossary-and-release-compatibility.md). Which role may do it is [a.4](a.4-roles-and-permissions-matrix.md). Which interface can do it is [a.5](a.5-interface-index.md). And how the thing actually works is the chapter that owns it: this appendix answers whether, not how, and does not repeat a chapter's explanation. Use [a.1](a.1-capability-index.md) to get from a capability to its chapter.

## What decides most cells

![Explanation](../_assets/icons/explanation.svg) Most cells are decided by a small number of structural facts, and knowing them lets you predict a row this table does not contain.

**Whether the platform runs an agent.** macOS, Windows and Linux run fleetd. iOS, iPadOS and Android do not, so nothing that depends on running a query or a script reaches them. Which of `Unsupported` and `Not applicable` a given cell gets is decided per row rather than by the platform: where Fleet holds a target list that mobile platforms are absent from, the cell is `Unsupported` on that evidence, and where the subject simply has no mobile version, it is `Not applicable`. ChromeOS runs an extension that answers some of the same questions with none of the same machinery.

**Whether Fleet holds a management channel, and whose it is.** Apple's protocol, Microsoft's, and Google's management API differ in what they will carry, so the same administrator intent arrives by three mechanisms with three sets of failure modes ([1.2](../01-foundations/1.2-how-fleet-reaches-a-device.md)).

**Whether the operation exists at the provider at all.** Several rows are not applicable on a platform because the vendor offers nothing Fleet could call, which is a different thing from Fleet not having implemented it.

**Whether ownership changes the answer.** Personally owned and company-owned devices differ, most sharply on Android, and that difference is a condition rather than a platform column.

## Three rows worth reading before you plan

![Troubleshooting](../_assets/icons/troubleshooting.svg) Each of these is a place where the obvious expectation is wrong, and each is in the matrix below with its evidence.

> ### Requiring signed host requests locks out every Mac and Windows host
>
> Fleet can require that agent requests carry a signature. **The setting is deployment-wide and has no platform exception.** It covers the agent's own request paths, everything under the osquery path, and the certificate-request route, refusing an unsigned request on any of them with an authentication error. The capability handshake is the one exemption.
>
> **Only Linux can satisfy it, and Fleet says so twice.** Packaging refuses the option for anything other than a Linux package type, and the agent refuses it again at startup on any operating system that is not Linux.
>
> So on a mixed estate, turning this on stops every macOS and Windows host checking in, reporting or receiving work, and no packaging option produces a Mac or Windows agent that can sign. **Nothing warns you at the point of change**, and Fleet knows which platforms are enrolled.
>
> The end-user surface is outside the covered set, so **a locked-out host can still look reachable**: My Device answers while the host itself has stopped participating.

> ### Downgrading to Free does not stop disk encryption escrow
>
> What Free refuses is narrow: a write that **switches disk encryption on**. Everything downstream of that switch is gated on the stored setting rather than on the licence.
>
> So a deployment that ran Premium with encryption enforced, and then drops to Free, does not stop. The stored setting is still on, because nothing clears it, and Fleet **goes on collecting and storing new recovery keys** from Windows and Linux hosts. Reading a key was never licence-gated at all, so it also goes on surrendering every key it holds, to every role that can read the host ([a.4](a.4-roles-and-permissions-matrix.md)).
>
> There is a second effect that is easier to hit and harder to diagnose. Because the refusal fires on any write whose new value is on, **a downgraded deployment cannot save any device-management setting** until it first turns disk encryption off, and the error names the encryption field rather than the change you were making.

> ### Wipe has three different answers, not two
>
> One administrator intent, three outcomes. On Free, only a company-owned Android device can be wiped; every other platform gets a licence error before Fleet looks at the platform at all. On Premium, macOS, iPhone and iPad, Windows, Linux and Android all work. **ChromeOS works on neither**, because the Premium path rejects it by name as an unsupported platform.
>
> A reader who learns the licence answer on one platform will get it wrong on the others, which is the whole argument for this appendix being organised the way it is.

## How to read it

![Reference](../_assets/icons/reference.svg) Five values, and the distinction between three of them is the whole discipline of the appendix.

| Value | What it means |
|---|---|
| **Supported** | Fleet does this on this platform once the row's prerequisite holds. |
| **Conditional (Cnn)** | Fleet does this only when a stated condition holds. Both branches are in the condition register. |
| **Unsupported** | Fleet refuses. A positive boundary was found: an explicit rejection, an error arm, or an allow-list the platform is absent from. |
| **Not applicable** | The row's subject does not exist on this platform. This is a statement about the platform, not about Fleet. |
| **Not established (Enn)** | No boundary was found in either direction. The record says what was searched. |

Three habits of this table are worth knowing before you use it.

**Absence is never evidence of a refusal.** `Unsupported` always rests on something Fleet actually does to say no. Where the only finding was that no code path exists, the answer is `Not established`, which is an honest answer rather than a failure.

**Licence and prerequisite are columns, not cell values.** A Premium capability is `Supported` with `Premium` in the licence column. A capability that needs MDM configured first is `Supported` with that named as its prerequisite. Neither ever appears as `Conditional`, because neither is a condition on whether Fleet does the thing, only on whether you may ask or on what you must have in place first.

**Some rows are deliberately per-platform.** Locking a Mac and locking a Windows host are separate rows, so each reads `Not applicable` on the platforms the other covers. That is the grain at which the six platforms can actually disagree.

No cell holds two values. Where a cell needs explaining, that is what a condition identifier is for.

## The matrix

![Reference](../_assets/icons/reference.svg) Grouped as a reader would look for a capability, 262 rows. Section rows in bold carry no cells; they mark where a family starts.

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
| **CAP-029** | Enroll a Mac in MDM from a link, personally owned | Supported | Supported | Unsupported | Not applicable | Supported | Not applicable | Free | Apple MDM configured, and a valid enroll secret |
| **CAP-030** | Download an unsigned manual macOS enrollment profile | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple MDM configured |
| **CAP-031** | Download the default Setup Assistant profile | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple MDM configured |
| **CAP-032** | Have Fleet install the agent on a Mac it enrolls | Supported | Unsupported | Not applicable | Not applicable | Not applicable | Not applicable | Free | Apple MDM enrollment on the device channel |
| **CAP-033** | Suppress Fleet's ADE agent install so a bootstrap package delivers it | Conditional (C004) | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable | Premium | A bootstrap package already configured |
| **CAP-034** | Attach the end user's identity at enrollment | Conditional (C005) | Conditional (C006) | Conditional (C007) | Conditional (C008) | Conditional (C009) | Not established (E01) | Premium | An identity provider configured for MDM features |
| **CAP-035** | Enroll a Windows host by installing the agent | Not applicable | Not applicable | Conditional (C010) | Not applicable | Not applicable | Not applicable | Free | Windows MDM configured, and the host already agent-enrolled |
| **CAP-036** | Enroll a Windows host at first boot through Autopilot | Not applicable | Not applicable | Conditional (C011) | Not applicable | Not applicable | Not applicable | Premium | Windows MDM configured, and the Entra tenant and client lists populated |
| **CAP-037** | Let a person enroll a Windows host from Settings | Not applicable | Not applicable | Conditional (C012) | Not applicable | Not applicable | Not applicable | Premium | Windows MDM configured, and the Entra lists populated |
| **CAP-038** | Stop Fleet enrolling Windows hosts unasked | Not applicable | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Premium | Windows MDM turned on |
| **CAP-039** | Move Windows hosts off another MDM with no user interaction | Not applicable | Not applicable | Conditional (C013) | Not applicable | Not applicable | Not applicable | Premium | Windows MDM turned on, and the host already agent-enrolled |
| **CAP-040** | Prompt a Mac's user to migrate from another MDM | Conditional (C014) | Unsupported | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Migration turned on, a webhook destination set, and the host eligible |
| **CAP-041** | Have Fleet push the agent to an Entra-enrolled Windows host | Not applicable | Not applicable | Conditional (C015) | Not applicable | Not applicable | Not applicable | No direct gate, Premium-only prerequisite | An Entra-enrolled host and a global enroll secret |
| **CAP-042** | Enroll a Linux host | Not applicable | Not applicable | Not applicable | Supported | Not applicable | Not applicable | Free | A valid enroll secret, supplied with the server address |
| **CAP-043** | Re-point or reconfigure a deployed Linux agent without rebuilding | Unsupported | Not applicable | Unsupported | Supported | Not applicable | Not applicable | Free | Root on the host, and a service restart |
| **CAP-044** | Build a macOS package that carries no URL or secret | Supported | Not applicable | Unsupported | Unsupported | Not applicable | Not applicable | Free | A device-level agent configuration profile delivered by MDM |
| **CAP-045** | Supply a Windows host's URL, secret and flags at install time | Not applicable | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Free | Installer properties supplied on the command line |
| **CAP-046** | Enroll an iPhone or iPad automatically | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple Business Manager token, with the devices assigned to Fleet |
| **CAP-047** | Enroll an iPhone or iPad from a link, company-owned | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Free to enroll, Premium to attach the owner | Apple MDM configured, and a valid enroll secret |
| **CAP-048** | Enroll an iPhone or iPad from a link, personally owned | Not applicable | Supported | Unsupported | Not applicable | Supported | Not applicable | Free | Apple MDM configured, and a valid enroll secret |
| **CAP-049** | Have a person enroll their own device with a Managed Apple Account | Unsupported | Conditional (C016) | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple Business Manager token, MDM single sign-on, and a Managed Apple Account |
| **CAP-051** | Place an ADE device in a fleet by platform | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple Business Manager token uploaded |
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
| **CAP-065** | Include the end-user surface in the agent | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free surface, Premium features inside it | Chosen at packaging time on macOS and Linux, at install time on Windows |
| **CAP-066** | Enable scripts on a host at packaging time | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | Chosen at packaging time, or by profile on macOS |
| **CAP-067** | Set an agent's update channel centrally | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Premium | Agent built with updates enabled |
| **CAP-068** | Set an agent's update channel on the host | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | An agent restart |
| **CAP-069** | Pin an agent component to an exact version | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Premium centrally, Free per host | The pinned version must exist in the update repository |
| **CAP-070** | Roll an agent version backwards across the estate | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | Updates not disabled, and the older version still published |
| **CAP-071** | Stop an agent updating at all | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | Set at packaging time or by editing the host's service configuration |
| **CAP-072** | Publish agent versions from your own update repository | Supported | Not applicable | Unsupported | Supported | Not applicable | Not applicable | Free, and not enforced | Signing keys present, and an initialised repository |
| **CAP-073** | See what agent version a host is actually running | Supported | Not applicable | Supported | Supported | Not applicable | Supported | Free | The host must be running the Fleet agent, not plain osquery |
| **CAP-074** | Deliver an osquery extension to hosts | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free, Premium once a label is named | Agent updates enabled, and the extension published to the update repository |
| **CAP-075** | Restrict an extension to a label | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Premium | The label must already exist and be in scope |
| **CAP-076** | Set osquery runtime options for a fleet | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Free globally, Premium per fleet | Agent installed |
| **CAP-077** | Set Orbit's own settings for a fleet | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free globally, Premium per fleet | Agent installed |
| **CAP-078** | Turn on file integrity monitoring | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Free globally, Premium per fleet | A log destination configured |
| **CAP-079** | Scan hosts with YARA signature sets | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Free globally, Premium per fleet | Agent installed |
| **CAP-080** | Stamp results with provenance columns | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Free globally, Premium per fleet | Applies to logged results, not host vitals |
| **CAP-081** | Turn individual osquery event subscribers on or off | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Free globally, Premium per fleet | Agent installed |
| **CAP-082** | Carve a file off a host | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | A carve store configured |
| **D. Host data, vitals, and inventory** | | | | | | | | | |
| **CAP-083** | See what a device is and what is on it | Supported | Supported | Supported | Supported | Supported | Supported | Free | Enrolled by the platform's own channel |
| **CAP-084** | Put a value you collect on the host record | Supported | Not applicable | Supported | Supported | Not applicable | Supported | Free globally, Premium per fleet | None |
| **CAP-085** | Record a value Fleet cannot collect | Supported | Supported | Supported | Supported | Supported | Supported | Free | The vital must be defined first |
| **CAP-086** | Turn a SQLite file on the device into a queryable table | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Free globally, Premium per fleet | The database file must exist at the given path |
| **CAP-087** | Replace or remove one of Fleet's own detail queries | Supported | Not applicable | Supported | Supported | Not applicable | Supported | Free globally, Premium per fleet | The override must name an existing query |
| **CAP-088** | Collect the local accounts on a device | Supported | Not applicable | Supported | Supported | Not applicable | Supported | Free | None |
| **CAP-089** | See which certificates a host holds | Supported | Supported | Supported | Unsupported | Unsupported | Unsupported | Free | A recent enough osquery on Windows |
| **CAP-090** | Attach an email address to a host | Supported | Supported | Supported | Supported | Supported | Supported | Free set by hand, Premium from the identity provider | None |
| **CAP-091** | Ask a host to report again now | Supported | Supported | Supported | Supported | Unsupported | Supported | Free | Apple MDM configured and connected |
| **CAP-092** | Refresh an iPhone or iPad's inventory on a schedule | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple MDM configured, and push notifications working |
| **E. Queries and reports** | | | | | | | | | |
| **CAP-093** | Ask every online device a question now | Supported | Not applicable | Supported | Supported | Not applicable | Supported | Free | An enrolled agent, and live queries not disabled |
| **CAP-095** | Collect a question's answer on a schedule | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Free | An interval above zero, and results not discarded |
| **CAP-096** | Keep the newest result per host in Fleet | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Free | Results not discarded, and snapshot logging |
| **CAP-097** | Send a report's results to a log destination | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Free | A destination chosen at server start |
| **CAP-098** | Read a report's results across the estate | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Free | Results not discarded |
| **CAP-099** | Read one host's result, including a successful empty one | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Free | None |
| **CAP-100** | Retrieve stored report rows for export | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Free | Results not discarded |
| **CAP-101** | Keep a report away from platforms whose tables do not exist | Supported | Not applicable | Supported | Supported | Not applicable | Conditional (C027) | Free | None |
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
| **CAP-116** | Scope a policy to a platform | Supported | Not applicable | Supported | Supported | Not applicable | Supported | Free | None |
| **CAP-117** | Narrow a policy by label | Supported | Not applicable | Supported | Supported | Not applicable | Supported | Premium | Labels must exist and not appear on both sides |
| **CAP-118** | Mark a policy as one whose failure matters | Supported | Not applicable | Supported | Supported | Not applicable | Supported | Premium | None |
| **CAP-119** | Read how many hosts pass and fail a policy | Supported | Not applicable | Supported | Supported | Not applicable | Supported | Free | None |
| **CAP-120** | Clear a policy's collected results | Supported | Not applicable | Supported | Supported | Not applicable | Supported | Free | None |
| **G. Software and vulnerability knowledge** | | | | | | | | | |
| **CAP-122** | Collect what software is installed | Supported | Conditional (C028) | Supported | Supported | Supported | Conditional (C029) | Free | Software inventory turned on, and enrollment by the platform's own channel |
| **CAP-123** | Turn software inventory on for one fleet | Supported | Not applicable | Supported | Supported | Not applicable | Supported | Free globally, Premium per fleet | The host must be assigned to the fleet |
| **CAP-124** | See which installed software has known vulnerabilities | Supported | Unsupported | Supported | Supported | Not established (E02) | Not established (E03) | Free | Software inventory on, and a vulnerability database path configured |
| **CAP-125** | See which operating system builds have known vulnerabilities | Supported | Unsupported | Conditional (C030) | Supported | Conditional (C031) | Unsupported | Free | A vulnerability database path configured |
| **CAP-126** | Prioritise findings by severity and exploitation | Supported | Unsupported | Supported | Supported | Conditional (C032) | Not established (E04) | Premium | Vulnerability metadata populated |
| **CAP-127** | Filter and sort by those fields | Supported | Unsupported | Supported | Supported | Conditional (C033) | Not established (E05) | Premium | Vulnerability metadata populated |
| **CAP-128** | See the version that fixes a finding | Supported | Unsupported | Supported | Supported | Conditional (C034) | Not established (E06) | Premium | Vulnerability metadata populated |
| **CAP-131** | Browse what Fleet knows how to install | Supported | Unsupported | Supported | Unsupported | Unsupported | Unsupported | Premium | Outbound network reach to the app catalogue |
| **H. Estate-wide reading and targeting** | | | | | | | | | |
| **CAP-133** | Read the estate's headline counts | Supported | Conditional (C035) | Supported | Supported | Conditional (C036) | Supported | Free | None |
| **CAP-134** | Read how many hosts are low on disk | Supported | Supported | Supported | Supported | Supported | Unsupported | Premium | A threshold between 1 and 100 GiB |
| **CAP-135** | See how many automated enrollments are not healthy | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Free to read the count, Premium to make it non-zero | An Apple Business Manager token, and MDM configured |
| **CAP-136** | See which hosts were online over time | Supported | Supported | Supported | Supported | Supported | Supported | Free | Historical uptime collection left on |
| **CAP-137** | Hand a population to somebody who does not use Fleet | Supported | Supported | Supported | Supported | Supported | Supported | Free | None |
| **CAP-138** | Read the host list programmatically | Supported | Supported | Supported | Supported | Supported | Supported | Free, with Premium-only filters silently dropped | None |
| **CAP-139** | Be told when too much of the estate goes quiet | Supported | Conditional (C037) | Supported | Supported | Conditional (C038) | Supported | Free globally, Premium per fleet | A destination URL, a day count and a percentage |
| **CAP-140** | Select hosts by a query that keeps itself current | Supported | Not applicable | Supported | Supported | Unsupported | Supported | Free globally, Premium per fleet | Agent installed |
| **CAP-141** | Select a specific list of hosts | Supported | Supported | Supported | Supported | Supported | Supported | Free globally, Premium per fleet | A manual label, and write access to every target host |
| **CAP-142** | Select hosts by a reported vital | Supported | Supported | Supported | Supported | Supported | Supported | Free for a hand-set vital, Premium for identity-provider vitals | Exactly one criterion, and the vital must exist |
| **I. Configuration profiles and declarative settings** | | | | | | | | | |
| **CAP-146** | Put a setting on an Apple device and keep it there | Supported | Supported | Not applicable | Unsupported | Not applicable | Unsupported | Free globally without labels, Premium per fleet or with labels | Apple MDM configured, and an unsigned profile |
| **CAP-147** | Let an Apple device hold and report its own desired state | Supported | Supported | Not applicable | Unsupported | Not applicable | Unsupported | Free globally without labels, Premium with variables or for updates | Apple MDM configured |
| **CAP-148** | Put a setting on a Windows device | Not applicable | Not applicable | Supported | Unsupported | Not applicable | Unsupported | Free globally without labels, Premium per fleet or with labels | Windows MDM configured |
| **CAP-149** | Configure an Android device | Not applicable | Not applicable | Not applicable | Unsupported | Supported | Unsupported | Free globally without labels, Premium per fleet or with labels | Android MDM configured, and Android Enterprise bound |
| **CAP-150** | Give one fleet its own profiles | Supported | Supported | Supported | Not applicable | Supported | Not applicable | Premium | The platform's MDM configured |
| **CAP-151** | Narrow a profile to hosts carrying a label | Supported | Supported | Supported | Unsupported | Supported | Unsupported | Premium | The labels must exist and be visible to the fleet |
| **CAP-152** | Fill in a per-host value in a profile | Supported | Supported | Supported | Not applicable | Supported | Not applicable | Premium on Apple and Windows, Free on Android | On Android the variable must sit inside a string value |
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
| **CAP-162** | Run a script across many hosts at once | Supported | Unsupported | Supported | Supported | Unsupported | Unsupported | Free globally, Premium per fleet | All targets in the same fleet as the script |
| **CAP-163** | Stop every script running anywhere | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | None |
| **CAP-164** | Let a script run for longer than five minutes | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | A value of 18,000 seconds or less |
| **CAP-165** | Read what a script did | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | A script must have run |
| **CAP-166** | Use a credential in a script without storing it | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | The server private key configured |
| **CAP-167** | Use a host's own vital inside an install or script | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | The referenced vital must be defined |
| **K. Software delivery** | | | | | | | | | |
| **CAP-168** | Deliver software you package yourself | Supported | Unsupported | Supported | Supported | Unsupported | Unsupported | Free | Agent installed with scripts enabled |
| **CAP-169** | Deliver an application from Fleet's catalogue | Supported | Unsupported | Supported | Unsupported | Unsupported | Unsupported | Premium | Outbound reach to the app catalogue |
| **CAP-170** | Deliver a purchased App Store application | Supported | Supported | Unsupported | Unsupported | Conditional (C039) | Unsupported | Premium | Apple MDM on, host connected, and a token assigned to the host's fleet |
| **CAP-171** | Make a Play application available | Unsupported | Unsupported | Unsupported | Unsupported | Supported | Unsupported | Free | Android Enterprise bound, and the app in the managed catalogue |
| **CAP-172** | Deliver an app you built yourself to iPhones and iPads | Unsupported | Supported | Unsupported | Unsupported | Unsupported | Unsupported | Free | A genuine iOS application archive with a bundle identifier |
| **CAP-173** | Put a shortcut to a URL on an Android device | Unsupported | Unsupported | Unsupported | Unsupported | Supported | Unsupported | Free | Android Enterprise bound, and a unique name within the fleet |
| **CAP-174** | Deliver a `.sh`, `.ps1` or `.py` as a package | Supported | Unsupported | Supported | Supported | Unsupported | Unsupported | Free | A recognised extension, with a matching interpreter line |
| **CAP-175** | Gate an install on a condition the device reports | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | Agent installed |
| **CAP-176** | Have Fleet write the install and uninstall logic for you | Supported | Not applicable | Conditional (C040) | Supported | Not applicable | Not applicable | Free | Package identifiers must be extractable |
| **CAP-177** | Install software on a host | Supported | Supported | Supported | Supported | Unsupported | Unsupported | Free | Agent installed, or MDM connected for the Apple path |
| **CAP-178** | Uninstall software from a host | Conditional (C041) | Unsupported | Supported | Supported | Unsupported | Unsupported | Free | Agent installed with scripts enabled, and an uninstall script on file |
| **CAP-179** | Ship different builds of one title to different hosts | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | At most ten packages per title |
| **CAP-180** | Hold a catalogue app at a version | Supported | Unsupported | Supported | Unsupported | Unsupported | Unsupported | Free | A cached version must exist |
| **CAP-181** | Keep the library's catalogue apps current | Supported | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Free | An installer store, and no literal version pin |
| **CAP-182** | Go back to the previous catalogue version | Supported | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Free | The target version must still be cached |
| **CAP-183** | Configure a managed application on an Apple device | Conditional (C042) | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Free | The configuration must be supplied as a string containing the markup |
| **CAP-184** | Configure a managed application on Android | Not applicable | Not applicable | Not applicable | Not applicable | Supported | Not applicable | Free | Android Enterprise bound, and not a web app |
| **CAP-185** | Choose when apps update on a device | Unsupported | Supported | Unsupported | Unsupported | Unsupported | Unsupported | Premium | The host must report a time zone, and a token must exist for its fleet |
| **CAP-186** | Remove something from the library | Supported | Supported | Supported | Supported | Supported | Not applicable | Free | None |
| **CAP-187** | Serve installers to hosts through a CDN | Supported | Supported | Supported | Supported | Not applicable | Not applicable | Free | A content delivery URL with a signing key pair |
| **CAP-188** | Accept a very large installer | Supported | Supported | Supported | Supported | Not applicable | Not applicable | Premium | None |
| **L. Setup and self-service experiences** | | | | | | | | | |
| **CAP-189** | Prepare a Mac before its user reaches the desktop | Supported | Conditional (C043) | Conditional (C044) | Conditional (C045) | Not applicable | Unsupported | Premium | Apple MDM configured, automated enrollment, and the agent delivered |
| **CAP-190** | Run a script as part of setup | Supported | Unsupported | Unsupported | Unsupported | Not applicable | Not applicable | Premium | Automated enrollment, with manual agent install off |
| **CAP-191** | Deliver a package to a Mac before the agent exists | Supported | Unsupported | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Automated enrollment, and Apple MDM configured |
| **CAP-192** | Create the user's local account during setup | Supported | Unsupported | Not applicable | Not applicable | Not applicable | Not applicable | Premium at delivery, not refused at the settings interface | Automated enrollment, and Apple MDM configured |
| **CAP-193** | Show the user an agreement during setup | Conditional (C046) | Supported | Unsupported | Not applicable | Not applicable | Not applicable | Premium | An identity provider configured for MDM features |
| **CAP-194** | Hold a Windows device at a status page until setup finishes | Not applicable | Not applicable | Conditional (C047) | Not applicable | Not applicable | Not applicable | Not established | Windows MDM configured, and automatic enrollment at first boot |
| **CAP-195** | Show setup progress without holding anyone up | Conditional (C048) | Not applicable | Conditional (C049) | Supported | Not applicable | Not applicable | Premium | Agent installed with the end-user surface enabled |
| **CAP-196** | Install software as part of an ADE iPhone's setup | Supported | Supported | Not applicable | Not applicable | Not applicable | Unsupported | Premium | A purchase token with licences available |
| **CAP-197** | Push an app to an Android device at enrollment | Not applicable | Not applicable | Not applicable | Not applicable | Supported | Not applicable | Premium | Android Enterprise bound |
| **CAP-198** | Install setup software only on devices that need it | Unsupported | Unsupported | Supported | Supported | Not applicable | Not applicable | Premium | A fleet policy whose automation points at the same installer |
| **CAP-199** | Stop setup when a piece of software fails | Supported | Unsupported | Conditional (C050) | Unsupported | Not applicable | Not applicable | Premium | Windows MDM turned on |
| **CAP-200** | Take release of a Mac or iPhone into your own hands | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple MDM configured |
| **CAP-201** | Retry only the setup steps that failed | Conditional (C051) | Not applicable | Unsupported | Unsupported | Not applicable | Not applicable | Premium | Require-all-software on, a failed install, and an agent restart |
| **CAP-202** | Offer software for people to install themselves | Supported | Conditional (C052) | Supported | Supported | Conditional (C053) | Unsupported | Premium | The end-user surface on desktop platforms, a web clip on Apple mobile |
| **CAP-203** | Group a large self-service catalogue | Supported | Conditional (C054) | Supported | Supported | Unsupported | Not applicable | Premium | As the row above |
| **CAP-204** | Let a user install everything offered to them | Supported | Conditional (C055) | Supported | Supported | Unsupported | Unsupported | Premium | As the row above |
| **M. Operating system updates** | | | | | | | | | |
| **CAP-205** | Require a minimum OS version by a date on Apple devices | Supported | Supported | Not applicable | Unsupported | Unsupported | Unsupported | Premium | Apple MDM on, with a minimum version and a deadline set together |
| **CAP-206** | Prompt users on older Macs to update | Conditional (C056) | Unsupported | Unsupported | Unsupported | Not applicable | Not applicable | Premium | Agent enrolled, host connected to MDM, and macOS updates configured |
| **CAP-207** | Set an update deadline and restart grace on Windows | Not applicable | Not applicable | Supported | Unsupported | Unsupported | Unsupported | Premium | Windows MDM on, with both fields set together |
| **CAP-208** | Control Android system updates | Not applicable | Not applicable | Not applicable | Unsupported | Supported | Unsupported | Premium | Android MDM configured, and Android Enterprise bound |
| **CAP-209** | Express an update policy the built-in form cannot | Conditional (C057) | Conditional (C058) | Conditional (C059) | Not applicable | Not applicable | Not applicable | Premium | The built-in update settings must be unset for that scope |
| **CAP-210** | Update a Mac or iPhone during automated enrollment | Conditional (C060) | Conditional (C061) | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Host in automated enrollment, and able to request a software update |
| **CAP-211** | Enforce a Linux OS version | Not applicable | Not applicable | Not applicable | Unsupported | Unsupported | Unsupported | Not applicable | Not applicable |
| **CAP-212** | See whether devices actually reached the version | Supported | Supported | Unsupported | Unsupported | Unsupported | Unsupported | Premium | A minimum version set for the host's scope |
| **N. Device actions and MDM commands** | | | | | | | | | |
| **CAP-213** | Lock a Mac | Conditional (C062) | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple MDM configured, host enrolled, and not a personal enrollment |
| **CAP-214** | Lock an iPhone or iPad | Not applicable | Conditional (C063) | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple MDM configured, and an automatic enrollment |
| **CAP-215** | Lock a Windows host | Not applicable | Not applicable | Conditional (C064) | Not applicable | Not applicable | Not applicable | Premium | Windows MDM configured, and the agent installed with scripts enabled |
| **CAP-216** | Lock a Linux host | Not applicable | Not applicable | Not applicable | Conditional (C065) | Not applicable | Not applicable | Premium | Agent installed with scripts enabled, running as root |
| **CAP-217** | Lock an Android device | Not applicable | Not applicable | Not applicable | Not applicable | Conditional (C066) | Not applicable | Premium | Android Enterprise bound, and the device enrolled |
| **CAP-218** | Release a locked Mac | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable | Premium | The host must currently be locked, and a person at the keyboard |
| **CAP-219** | Release a locked iPhone or iPad | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Premium | The device must check in over push for the command to land |
| **CAP-220** | Release a locked Windows host | Not applicable | Not applicable | Conditional (C067) | Not applicable | Not applicable | Not applicable | Premium | Machine powered on with the agent running, and scripts enabled |
| **CAP-221** | Release a locked Linux host | Not applicable | Not applicable | Not applicable | Conditional (C068) | Not applicable | Not applicable | Premium | Agent installed with scripts enabled, running as root |
| **CAP-222** | Release a locked Android device | Not applicable | Not applicable | Not applicable | Not applicable | Unsupported | Not applicable | Not applicable | Not applicable |
| **CAP-223** | Erase a Mac | Conditional (C069) | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple MDM configured, host connected, and not a personal enrollment |
| **CAP-224** | Erase an iPhone or iPad | Not applicable | Conditional (C070) | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple MDM configured, host connected, and not a personal enrollment |
| **CAP-225** | Erase a Windows host | Not applicable | Not applicable | Conditional (C071) | Not applicable | Not applicable | Not applicable | Premium | Windows MDM configured, and the host enrolled in it |
| **CAP-226** | Erase a Linux host | Not applicable | Not applicable | Not applicable | Conditional (C072) | Not applicable | Not applicable | Premium | Agent installed with scripts enabled, running as root |
| **CAP-227** | Erase a company-owned Android device | Not applicable | Not applicable | Not applicable | Not applicable | Supported | Not applicable | Free on Android, Premium on every other platform | Android Enterprise bound, device enrolled, and company-owned |
| **CAP-228** | Deal with a personally owned Android device | Not applicable | Not applicable | Not applicable | Not applicable | Supported | Not applicable | Free | Android Enterprise bound, and the device enrolled with a work profile |
| **CAP-229** | Find where a device is | Unsupported | Conditional (C073) | Unsupported | Unsupported | Unsupported | Unsupported | Premium | Automated enrollment assigned to Fleet, and the device in lost mode |
| **CAP-230** | Clear a device's passcode | Unsupported | Conditional (C074) | Unsupported | Unsupported | Supported | Unsupported | Premium | Apple MDM configured, non-personal enrollment, and an unlock token on file |
| **CAP-231** | Send a raw command to Apple devices | Conditional (C075) | Conditional (C076) | Not applicable | Unsupported | Unsupported | Unsupported | Free, Premium for three Apple request types | Apple MDM configured, and every target connected and on one platform |
| **CAP-232** | Send a raw command to Windows devices | Not applicable | Not applicable | Conditional (C077) | Unsupported | Unsupported | Unsupported | Free, Premium for the remote-wipe subtree | Windows MDM configured, and every target enrolled |
| **CAP-233** | Read what a device said about a command | Supported | Supported | Supported | Not applicable | Unsupported | Not applicable | Free | At least one MDM configured |
| **CAP-234** | Cancel a device action before it happens | Conditional (C078) | Conditional (C079) | Conditional (C080) | Conditional (C081) | Conditional (C082) | Not applicable | Free | The activity must still be queued for that host |
| **O. Disk encryption and recovery credentials** | | | | | | | | | |
| **CAP-235** | Turn FileVault on and hold the recovery key | Conditional (C083) | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable | Premium | Apple MDM configured, the server private key set, and a user login |
| **CAP-236** | Turn BitLocker on and hold the protector | Not applicable | Not applicable | Conditional (C084) | Not applicable | Not applicable | Not applicable | Premium | Windows MDM configured, agent enrolled, and a TPM on a non-server edition |
| **CAP-237** | Hold a recovery credential for an already-encrypted Linux host | Not applicable | Not applicable | Not applicable | Conditional (C085) | Not applicable | Not applicable | Premium | A supported distribution, already encrypted, with encryption enforced for the scope |
| **CAP-238** | Escrow silently on a TPM-backed Ubuntu host | Not applicable | Not applicable | Not applicable | Conditional (C086) | Not applicable | Not applicable | Premium | Snap-managed encryption, a reachable service socket, and the disk tool installed |
| **CAP-239** | Escrow by prompting the user for their LUKS passphrase | Not applicable | Not applicable | Not applicable | Conditional (C087) | Not applicable | Not applicable | Premium | A dialog tool, a desktop session, and a person who knows the passphrase |
| **CAP-240** | Know whether a disk is encrypted at all | Supported | Not applicable | Supported | Supported | Not applicable | Not established (E08) | Free | Agent installed and enrolled |
| **CAP-241** | Read the disk-encryption status summary | Supported | Not applicable | Supported | Conditional (C088) | Not applicable | Not applicable | Premium | Disk encryption enforced for the scope |
| **CAP-242** | Set a BitLocker startup PIN | Not applicable | Not applicable | Conditional (C089) | Not applicable | Not applicable | Not applicable | Premium | Windows MDM configured, encryption on for the scope, and a TPM |
| **CAP-243** | Allow a custom FileVault profile alongside Fleet's own | Conditional (C090) | Not applicable | Conditional (C091) | Not applicable | Not applicable | Not applicable | Premium | Server-level configuration and a restart |
| **CAP-244a** | Turn Recovery Lock on for a scope | Conditional (C092) | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable | Free globally, Premium per fleet | Apple silicon, enrolled and not personally enrolled, with the setting on for the scope |
| **CAP-244b** | Reveal a Mac's Recovery Lock password | Supported | Unsupported | Unsupported | Unsupported | Unsupported | Unsupported | Free | Apple silicon, and Apple MDM configured |
| **CAP-244c** | Rotate a Recovery Lock password | Conditional (C093) | Unsupported | Unsupported | Unsupported | Unsupported | Unsupported | Premium | Apple silicon, MDM connected, and an existing password |
| **CAP-245** | Stop enforcing encryption without losing what is held | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Premium | The decryption material for the platform must still be held |
| **P. Policy automations, integrations, and outbound events** | | | | | | | | | |
| **CAP-246** | Install software when a policy fails | Supported | Unsupported | Supported | Supported | Unsupported | Unsupported | Premium | Agent installed, and an installer for the host's platform |
| **CAP-247** | Install an App Store app when a policy fails | Supported | Unsupported | Unsupported | Unsupported | Unsupported | Unsupported | Premium | Agent installed |
| **CAP-248** | Run a script when a policy fails | Supported | Unsupported | Supported | Supported | Unsupported | Unsupported | Premium | Agent installed |
| **CAP-252** | Report a host as non-compliant to Microsoft Entra | Supported | Unsupported | Supported | Unsupported | Unsupported | Unsupported | Premium | Agent installed |
| **CAP-253** | Refuse a sign-in when a host is failing a policy | Supported | Not applicable | Not established (E09) | Unsupported | Not applicable | Unsupported | Premium | A proxy in front of Fleet that forwards the client certificate serial |
| **CAP-254** | Grant a one-time bypass of conditional access | Supported | Not applicable | Not established (E10) | Unsupported | Not applicable | Unsupported | Premium | Conditional access already refusing the sign-in |
| **CAP-255** | Act on every failing result rather than on the transition | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Premium | Agent installed |
| **CAP-257** | Send osquery status and result logs to a destination | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Premium | Agent installed |
| **R. Platform management configuration (Apple, Windows, Android)** | | | | | | | | | |
| **CAP-269** | Turn on Apple device management | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Free | The server private key must be set |
| **CAP-270** | Renew the Apple push certificate without resetting the estate | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Free | Apple MDM already on |
| **CAP-271** | Have Fleet re-issue each host's identity certificate | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Free | Apple MDM already on |
| **CAP-272** | Connect Fleet to Apple Business | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Free | Apple MDM already on |
| **CAP-273** | Renew the Apple Business token | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Free | Apple MDM already on |
| **CAP-274** | Control what Setup Assistant shows on an ADE device | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Premium | An Apple Business Manager token |
| **CAP-275** | Buy and distribute App Store apps | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Free | Apple MDM already on |
| **CAP-276** | Renew the Volume Purchasing token | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Free | A purchase token uploaded |
| **CAP-277** | Learn from Fleet that an Apple credential is expiring | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Free for the push certificate, Premium for the rest | The relevant Apple credential must be on file |
| **CAP-278** | Turn on Windows device management | Not applicable | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Free | A certificate and key pair configured in server settings |
| **CAP-279** | Choose whether Windows enrollment asks the end user | Not applicable | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Free | Windows MDM already on |
| **CAP-280** | Turn Windows device management off | Not applicable | Not applicable | Supported | Not applicable | Not applicable | Not applicable | Free | Windows MDM already on |
| **CAP-281** | Bind Fleet to an Android Enterprise | Not applicable | Not applicable | Not applicable | Not applicable | Supported | Not applicable | Free | Android Enterprise bound |
| **CAP-282** | Deliver client certificates to Android devices | Not applicable | Not applicable | Not applicable | Not applicable | Supported | Not applicable | Premium | A configured certificate authority |
| **CAP-283** | Tune Android API pressure and the companion app identity | Not applicable | Not applicable | Not applicable | Not applicable | Supported | Not applicable | Free | None, though the settings are absent from the generated reference |
| **CAP-284** | Turn Android device management off | Not applicable | Not applicable | Not applicable | Not applicable | Supported | Not applicable | Free | Android Enterprise bound |
| **S. Organization and server settings** | | | | | | | | | |
| **CAP-285** | Set the address everything uses to reach Fleet | Conditional (C094) | Conditional (C095) | Not established (E11) | Not established (E12) | Conditional (C096) | Not applicable | Free to change, Premium for the automatic re-sync | None |
| **CAP-289** | Point end-user error messages at your own help desk | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable | Free for settings and the device page, Premium for the desktop surface | None |
| **CAP-292** | Attach the end user's IdP identity to their devices | Supported | Supported | Supported | Supported | Supported | Unsupported | Premium | End-user authentication enabled for the scope |
| **CAP-293** | Set a host's IdP username by hand | Supported | Supported | Supported | Supported | Supported | Supported | Free | None |
| **CAP-295** | Send scheduled-report results somewhere | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Free | A destination chosen at server start |
| **CAP-296** | Send osquery's own status messages somewhere | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Free | A destination chosen at server start |
| **T. Running and operating the service** | | | | | | | | | |
| **CAP-307** | Prove a restored Fleet can still decrypt what it holds | Supported | Not applicable | Supported | Conditional (C097) | Not applicable | Not applicable | Free to read, Premium prerequisite to escrow | The decryption material for the platform must still be held |
| **CAP-310** | Rotate the server's HTTPS certificate without disconnecting agents | Conditional (C098) | Not applicable | Conditional (C099) | Conditional (C100) | Not applicable | Not established (E13) | Free | Depends on how the agent was packaged |
| **CAP-311** | Renew the Windows enrolment certificate | Not applicable | Not applicable | Conditional (C101) | Not applicable | Not applicable | Not applicable | Free | Windows MDM already on |
| **CAP-325** | Simulate load against a deployment | Supported | Supported | Supported | Supported | Supported | Unsupported | Free | None |
| **U. Diagnostic actions and introspection surfaces** | | | | | | | | | |
| **CAP-329** | Read the agent's own log on a host | Supported | Not applicable | Supported | Supported | Not applicable | Unsupported | Free | Agent installed, and administrator rights on the host |
| **CAP-330** | Inspect the Orbit root directory on a host | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | Agent installed, and administrator rights on the host |
| **CAP-331** | Raise an agent's verbosity for a bounded window | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free globally, Premium per fleet | Agent installed, and a re-enrollment for the setting to take effect |
| **CAP-332** | Raise an agent's verbosity permanently | Supported | Not applicable | Supported | Supported | Not applicable | Not applicable | Free | Re-packaging, host shell access, or an agent-options push, by lever |
| **CAP-335** | Read a host's own osquery introspection tables | Supported | Not applicable | Supported | Supported | Not applicable | Conditional (C102) | Free | Agent installed and checking in |
| **CAP-336** | Read the Apple MDM command queue | Supported | Supported | Not applicable | Not applicable | Not applicable | Not applicable | Free | Apple MDM configured and the host enrolled |
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

Every `Conditional` cell in the matrix, with both of its branches: what makes Fleet do the thing on that platform, and what makes it not. 104 conditions.

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

**C012** CAP-037, Windows. Supported when the device reports that it is not at first boot, which makes Fleet record the enrollment as manual and keep it that way on every refetch. Not this row when the device is at first boot, because that is the automatic enrollment answer and a different row.

**C013** CAP-039, Windows. Supported when Windows migration is turned on and the host is currently enrolled in a non-Fleet MDM: the agent is told to unenroll itself and Fleet shortens the refetch window so the change is ingested quickly. Not supported when the host is not in a third-party MDM, in which case nothing happens.

**C014** CAP-040, macOS. Supported when macOS migration is turned on, a webhook destination is set, and the host is eligible: the device page posts the migration webhook and shortens the refetch window, and the end-user surface shows the prompt. Not supported when any of those is missing, which returns an error naming the specific reason.

**C015** CAP-041, Windows. Supported when the enrolled device carries a valid user principal name and no recent agent check-in is on record: the session-start alert enqueues an installer download and a silent install, with scripts enabled and an optional authentication token. Not supported when the enrollment carries no user name, which is what a programmatic agent-driven enrollment looks like, because Fleet then treats the agent as already present and skips the install.

**C016** CAP-049, iOS/iPadOS. Supported when the licence is Premium and the enrollment token in the address resolves to an Apple Business Manager token: the first request challenges the device for a web sign-in against Fleet's MDM single sign-on address, and the second returns a signed account-driven profile carrying the assigned Managed Apple ID. Not supported without that token, or without MDM single sign-on and an identity provider configured. The result is always recorded as a personal enrollment.

**C017** CAP-053, Android. Supported when the enrollment token is requested as fully managed, which disallows personal usage and renders a QR code alongside factory-reset instructions. Not supported when that flag is absent, in which case the token produces a work-profile enrollment instead, which is a different row.

**C018** CAP-056, Linux. Supported when the agent was packaged with the managed host identity certificate option and the host has a usable TPM 2.0: the agent generates a hardware-backed key, obtains a certificate over the enrollment protocol using a valid enroll secret, and signs later requests through a local signing proxy. Not supported when no TPM is present, in which case setup fails and the end-user surface reports the device as unavailable. The option is refused outright on any operating system other than Linux.

**C019** CAP-057, macOS. Not supported when the setting is off, which is the default: an unsigned request from a Mac is passed through unverified, so nothing changes. Supported when the setting is on, in the sense that it is then enforced: an unsigned request from a Mac on a covered path is refused with an authentication error. Enforced but not satisfiable, because no macOS package can carry a host identity certificate and the agent refuses the option on macOS anyway, so turning the setting on locks every Mac out. The setting is deployment-wide and has no platform exception.

**C020** CAP-057, Windows. Not supported when the setting is off, which is the default: an unsigned request from a Windows host is passed through unverified. Supported when the setting is on, in the sense that it is then enforced: an unsigned request from a Windows host on a covered path is refused with an authentication error. Enforced but not satisfiable, because no Windows package can carry a host identity certificate and the agent refuses the option on Windows anyway, so turning the setting on locks every Windows host out.

**C021** CAP-057, Linux. Supported when the setting is on and the host holds a certificate: requests are signed and the server verifies them. Not supported when the setting is on and the host has no certificate, in which case every agent and osquery request is refused with an authentication error.

**C022** CAP-059, macOS. Supported when the agent is packaged to identify hosts by instance rather than by hardware identifier, which suppresses the serial-matching branch on agent enrollment. Not supported on the Apple MDM side, where the enrollment path matches on serial regardless and no suppression applies, so the two operating systems merge back into a single host record.

**C023** CAP-062, macOS. Supported, meaning the deletion sticks, when the Mac has no live automated enrollment assignment, or when the licence is Free, where the restore path never runs. Not supported when the Mac has a live assignment on Premium, because the delete restores a pending host inside the same request. The restore reuses the host identifier and unique identifier but deliberately not the agent identifier.

**C024** CAP-062, iOS/iPadOS. Supported, meaning the deletion sticks, when the device has no live automated enrollment assignment, is no longer enrolled, or the licence is Free. Not supported when it has a live assignment on Premium, which restores a pending record inside the same request, and separately Not supported for any still-enrolled iPhone or iPad, which reappears on its next MDM check-in whether or not it is assigned in Apple Business Manager. That second resurrection path involves no automated enrollment at all.

**C025** CAP-063, macOS. Supported when the Mac has no live automated enrollment assignment and its last contact is older than the configured window. Not supported when it has a live assignment, which makes the record permanently immune to expiry.

**C026** CAP-063, iOS/iPadOS. Supported on the same rule, with last contact read from the MDM channel because these platforms never write an agent last-seen record. Not supported when the device has a live automated enrollment assignment.

**C027** CAP-101, ChromeOS. Supported to the extent that a ChromeOS scope is accepted, stored and shown, so the report appears targeted at ChromeOS. Not supported in effect, because ChromeOS is not a scheduled-query target: the extension never fetches a schedule, so the report returns nothing, for ever.

**C028** CAP-122, iOS/iPadOS. Supported for the full installed-application list when the device was enrolled through automated device enrollment. Not supported beyond Fleet-managed apps when the device was enrolled manually or personally, because Fleet then asks the device for managed applications only, on both the hourly refresh and an operator-triggered refetch.

**C029** CAP-122, ChromeOS. Supported for browser extensions, which is the only software source declared for ChromeOS. Not supported for desktop applications, because the three desktop software queries carry platform lists that ChromeOS is absent from.

**C030** CAP-125, Windows. Supported when the setting that disables Windows operating-system vulnerability processing is left off, which is the default: Fleet analyses Windows builds against the vendor's security data. Not supported when it is turned on, in which case the definition sync still runs but no Windows operating-system finding is ever produced.

**C031** CAP-125, Android. Supported when the open-source vulnerability feed setting is on, which is the default: Fleet lists the Android builds in the estate, refreshes the feed artefacts and analyses each build. Not supported when it is off, because the Android analysis is never called and no Android operating-system finding is produced. Turning it off does not remove findings already stored, which persist and go stale until no host reports that build any more. The same setting also diverts Ubuntu and Red Hat analysis, so it is not an Android-only switch.

**C032** CAP-126, Android. Supported when the open-source vulnerability feed setting is on, so Android operating-system findings exist for the scoring, filtering and fixed-version machinery to shape. That machinery is per-vulnerability, joined from the shared vulnerability metadata, with no Android-specific branch. Not supported when the setting is off, because no Android finding is produced for these fields to describe. Whether Android application findings additionally exist is unsettled and recorded separately; if they do, the same shaping applies with no extra gate.

**C033** CAP-127, Android. Supported when the open-source vulnerability feed setting is on, so Android operating-system findings exist to filter and sort. The fields are per-vulnerability and carry no Android-specific branch. Not supported when the setting is off, because no Android finding is produced. Whether Android application findings additionally exist is unsettled and recorded separately.

**C034** CAP-128, Android. Supported when the open-source vulnerability feed setting is on, so Android operating-system findings exist and each carries its own fixed-version field on the finding row. Not supported when the setting is off, because no Android finding is produced. Whether Android application findings additionally exist is unsettled and recorded separately.

**C035** CAP-133, iOS/iPadOS. Supported for the total, the new count, the per-platform breakdown and the missing count, which falls back to the MDM channel's last-seen time and then to the detail-update time. Not supported for the online and offline split, which reads an agent last-seen record these devices never write, so they read as permanently offline. Devices still pending automated enrollment are excluded from the counts outright.

**C036** CAP-133, Android. Supported for the totals and for the missing count, which falls back to the detail-update time Fleet writes on every management check-in, so an actively managed Android host is not permanently missing. Not supported for the online and offline split, for the same reason as Apple mobile: no agent last-seen record is ever written.

**C037** CAP-139, iOS/iPadOS. Supported in the sense that these hosts are counted in the denominator of the quiet-estate check. Not supported as a signal, because they never write an agent last-seen record, so they fall into the unseen numerator once the day count elapses after creation and stay there permanently. This path has no MDM-channel fallback, unlike the headline counts.

**C038** CAP-139, Android. Supported in the sense that Android hosts are counted in the denominator of the quiet-estate check. Not supported as a signal, on identical grounds to Apple mobile: no agent last-seen record is ever written for an Android host, so it falls into the unseen numerator once the day count elapses after creation and stays there permanently.

**C039** CAP-170, Android. Supported for a managed Google Play purchase, which shares the same entry point and appears in the same platform list, though it consumes no Apple purchase licence. Not supported for this row's subject, an Apple App Store purchase, which is refused on the Apple branch when an Android application identifier is supplied.

**C040** CAP-176, Windows. Supported for a Windows installer package, for which Fleet generates both the install and the uninstall script, including the variant that uninstalls by upgrade code. Not supported for an executable or an archive, where both generators return nothing, so the upload is refused unless the administrator supplies both scripts by hand.

**C041** CAP-178, macOS. Supported for a package Fleet stores as macOS, meaning an installer package or a Fleet-maintained app: the uninstall script is queued and run like any other script. Not supported for a shell or Python package, which Fleet stores as Linux and refuses to uninstall on a Mac, even though the same host was allowed to install it.

**C042** CAP-183, macOS. Supported only in appearance: the request is accepted and returns success whenever a configuration is supplied. Not supported in substance, in every macOS case Fleet handles. A Mac App Store purchase has its configuration cleared on add, on edit and through declared configuration, and a custom macOS package has it cleared too. No path returns an error, so the configuration silently never reaches the Mac. This is the drop-rather-than-refuse failure mode, and it is worth knowing about precisely because nothing tells you.

**C043** CAP-189, iOS/iPadOS. Supported to the extent that an automatically enrolled iPhone or iPad is held at Setup Assistant and released by Fleet when its items finish. Not supported for the substance of the row: there is no dialog, no agent, no installer and no script, only purchased applications, and any other item is force-failed with a message saying so. When the device is not automatically enrolled, items are still enqueued once but nothing blocks.

**C044** CAP-189, Windows. Supported by a different mechanism: at first boot with automatic enrollment the device is held at the Windows enrollment status page. Not supported as Fleet's macOS pre-desktop experience, which Windows never gets. Outside first boot the device gets the non-blocking browser page instead.

**C045** CAP-189, Linux. Supported only in its non-blocking form, which reports software status. Not supported as a pre-desktop hold: there are no profiles, no bootstrap package, no account configuration and no release step on Linux.

**C046** CAP-193, macOS. Supported when the Mac enrolls through automated device enrollment, end-user authentication is on, and an agreement has been uploaded. Not supported when any of those is missing, in which case Setup Assistant never opens the web view, or the agreement reference is empty and the callback falls through to the enrollment profile.

**C047** CAP-194, Windows. Supported when the device enrolls automatically and is at first boot: Fleet marks it as awaiting configuration and sends the settings that hold it on the status page and block progress. Not supported when either condition fails, in which case the device is never marked, the status-page commands are never sent, and it takes the ordinary non-blocking path.

**C048** CAP-195, macOS. Supported as a surface, but a different one: macOS does not open the browser page. It shows the same device page inside the agent's own dialog window. Not supported as described, because that macOS surface is blocking, not non-blocking, since the device is not released until it finishes.

**C049** CAP-195, Windows. Supported when the agent starts and the server says the setup experience is enabled: the agent opens the device page in a browser window and registers a poller that writes a completion marker when all software reaches a terminal state. Not supported as a hold, because that poller blocks nothing.

**C050** CAP-199, Windows. Supported when require-all-software is on for Windows and the host is inside a Fleet-tracked enrollment status page, either pending or active: a failure cancels the remaining work and drives the hard-block choice. Not supported outside that window, which Fleet enumerates: a work or school account added after first boot, a programmatic agent enrollment after first boot, an agent with no Windows MDM, and any host that has already finished or timed out the status page.

**C051** CAP-201, macOS. Supported when the host has a failed software install, require-all-software is on, and the request asks to reset the failed steps: only the failed items are rebuilt and successful installs and purchases are excluded from re-insertion. Not supported otherwise, and the agent asks for it only on its first poll after a restart, so an ordinary poll never triggers it.

**C052** CAP-202, iOS/iPadOS. Supported for the mechanism: Fleet provides the device authentication these platforms need, by client certificate or by an address carrying the host identifier, and refuses ordinary device-token authentication for them explicitly. Not supported for the surface: Fleet builds no web clip, so the administrator must supply the shortcut that puts the catalogue on the device.

**C053** CAP-202, Android. Supported in the sense that Fleet marks applications as available rather than forced in managed Google Play, which is offered-not-required. Not supported as Fleet's self-service feature: the self-service flag itself is refused for Android software, and no install request is recorded when a person installs from the store, so only the forced setup path leaves a trace.

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

**C066** CAP-217, Android. Supported when Android MDM is configured and the host is MDM-connected: a lock command with a very long duration is sent. Not supported when Android MDM is not configured or the host is unenrolled. Both ownership models are allowed, and Fleet says so in the source: lock works for personal and company-owned devices alike.

**C067** CAP-220, Windows. Supported when Windows MDM is configured and the host is not known to have scripts disabled: an unlock script is queued. Not supported when scripts are disabled, which is refused with the redeploy-and-refetch message.

**C068** CAP-221, Linux. Supported when the host is not known to have scripts disabled: an unlock script is queued. Not supported when scripts are disabled. No MDM check applies to Linux.

**C069** CAP-223, macOS. Supported when the enrollment is not personal, Apple MDM is configured, and the host is connected to Fleet's MDM: an erase command with a generated PIN is sent. Not supported for a personal enrollment, which is refused by name, and not while a lock, unlock or wipe is pending, or the host is currently locked or already wiped.

**C070** CAP-224, iOS/iPadOS. Supported when the enrollment is not personal, Apple MDM is configured, and the host is connected. Not supported for a personal enrollment, which includes account-driven user enrollment, since that is recorded as personal. A manual non-personal enrollment is allowed here, unlike lock, which refuses it.

**C071** CAP-225, Windows. Supported when Windows MDM is configured and the host is MDM-connected: a remote-wipe command is sent, protected by default, with the unprotected variant available by request. Not supported when Windows MDM is off or the host is disconnected, and a wipe type other than the two Fleet accepts is rejected when the request is read. Unlike Windows lock, wipe needs no scripts, because it is not a script.

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

**C088** CAP-241, Linux. Supported when disk encryption is enforced for the scope and the host runs a distribution Fleet escrows for: it contributes to the verified, action-required and failed counts. Not supported when encryption is not enforced, because Fleet says outright that with nothing enforced there is nothing to report, and Linux never appears in the verifying, enforcing or removing-enforcement counts at all.

**C089** CAP-242, Windows. Supported when disk encryption is on for the same scope, in which case the PIN requirement is accepted and the PIN-related queries are added to the host. Not supported on its own: turning the PIN on without encryption is refused, and turning encryption off while the PIN is required is refused too, each with its own message.

**C090** CAP-243, macOS. Supported when the deployment-level custom disk encryption setting is on, which lets a custom profile carrying Apple's encryption or key-escrow payloads through alongside Fleet's own. Not supported when it is off, which is the default: such a profile is rejected, and so is a managed-preferences payload containing encryption options.

**C091** CAP-243, Windows. Supported when the same deployment-level setting is on, which stops Fleet rejecting a profile that targets the reserved encryption node. Not supported when it is off, which rejects it with the same message as the Apple side. It is one flag governing both platforms.

**C092** CAP-244a, macOS. Supported when the Mac is Apple silicon, has an enabled MDM enrollment on the device or user-enrollment-device channel, is currently enrolled, and is not a personal enrollment: a reconciler picks it up within about half a minute and sets the password. Not supported when any of those fails, because the host is never selected and no password is ever set. Turning the setting off removes the credential rather than leaving it in place.

**C093** CAP-244c, macOS. Supported when the Mac is MDM-connected, the feature is enabled for its scope, a password already exists, no rotation is in flight, no clear is in progress, and the current state is verified or failed. Not supported when any of those fails, each refused with its own typed error. Revealing a password also schedules a rotation an hour later, overwriting whatever was pending.

**C094** CAP-285, macOS. Supported for future enrollments and only on Premium: when the address changes, Fleet re-syncs the Apple automated enrollment profiles so devices enrolling afterwards get the new address. Not supported for devices already enrolled, whose check-in address was baked into the profile they installed and is not re-pointed by anything on this path. A separate setting exists so the device-facing address can be decoupled from the administrator-facing one.

**C095** CAP-285, iOS/iPadOS. Supported for future enrollments and only on Premium, because the automated enrollment re-sync is platform-blind: devices enrolling after the change get the new address. Not supported for devices already enrolled, whose check-in address was baked into the profile they installed.

**C096** CAP-285, Android. Supported to change the setting, which is never refused. Not supported in effect, and in two concrete ways. The binding between Fleet and Google's management service is keyed by the server address, so after a change Fleet no longer finds the existing enterprise and re-signing up creates a different record. And the push address Google delivers status reports to is fixed when the enterprise is created and never updated, so reports keep going to the old address.

**C097** CAP-307, Linux. Supported when the host runs a distribution Fleet escrows for and the server private key is still configured, which is what the stored key was encrypted with. Not supported when the private key is missing or has changed, in which case the stored key cannot be decrypted and nothing can be proved.

**C098** CAP-310, macOS. Supported when the agent was packaged without a pinned certificate, in which case the operating system trust store applies and a publicly-trusted rotation is transparent. Not supported when the agent was packaged with one, because that pins a replacement trust store rather than an addition, so the new server certificate must chain to a root already inside the pinned file or verification fails.

**C099** CAP-310, Windows. Supported when the agent was packaged without a pinned certificate, in which case the operating system trust store applies and a publicly-trusted rotation is transparent. Not supported when it was packaged with one, because the pinned file replaces the trust store rather than adding to it, so the new server certificate must chain to a root already inside it. The Windows installer threads the same option through.

**C100** CAP-310, Linux. Supported when the agent was packaged without a pinned certificate, in which case the operating system trust store applies and a publicly-trusted rotation is transparent. Not supported when it was packaged with one, for the same replacement-trust-store reason as macOS and Windows.

**C101** CAP-311, Windows. Supported when the currently configured Windows enrollment certificate and key are the same pair the keys were escrowed under, because that is what decrypts them. Not supported after the pair is replaced, because keys escrowed under the previous leaf certificate can no longer be decrypted.

**C102** CAP-335, ChromeOS. Supported for three of the six introspection tables, which the extension declares and answers from its own implementation: the agent information table, the operating-system version table and the system information table. Not supported for the other three, along with carving and agent logs, because those tables do not exist in the extension's closed set, so the query simply returns nothing.

**C103** CAP-345, ChromeOS. Supported for three of the four processing tasks, label membership, policy membership and last-seen, because ChromeOS hosts do submit results and are not excluded from the osquery path. Not supported for scheduled-query statistics, because the query that produces them is explicitly not sent to ChromeOS.

**C104** CAP-347, ChromeOS. Supported for the two request-size limits that apply to the write endpoint, which the extension does call. Not supported for the log-write limit, because the extension never calls the log endpoint, and not for the event and carving limits, which are agent flags for a process ChromeOS does not run.

## Rows that are not platform-scoped

88 rows have no platform answer. Most are about the Fleet server rather than a device: server configuration, a server-side store, an identity operation, or a property of how the deployment is run. **A few are not server-side and still have no platform answer**, which is why the section is named for what is true of all of them rather than for the common case. An automation interface is one, and a commercial arrangement with no corresponding mode in the software is another.

Carrying all 88 as six `Not applicable` cells each would add 528 cells that say nothing and would distort every per-platform count. Omitting them would be worse, because a reader who looked one up and found nothing could not tell whether a.2 does not cover it or whether it simply has no platform answer.

So they are carried here, one line each, grouped by the same sections as the matrix. The role answer for these rows is in a.4 and the interface answer is in a.5, which is where they genuinely resolve.


**A. Identity, access, and governance**

- **CAP-001** Sign in to Fleet with a Fleet password. An identity operation against Fleet's own user records, with no device involved.
- **CAP-002** Sign in through the organisation's identity provider. An identity operation: a browser sign-in between Fleet and the identity provider.
- **CAP-003** Have Fleet create the account on first IdP sign-in. An identity operation: account creation inside the sign-in callback.
- **CAP-004** Remove Fleet accounts when people leave, from the IdP. An identity operation: a provisioning protocol the identity provider speaks to Fleet.
- **CAP-005** Have SCIM skip accounts it must not delete. An identity operation: a guard inside that provisioning handler.
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

**B. Enrollment and host lifecycle**

- **CAP-050** Register Fleet's Apple service-discovery URL. Server configuration: registering Fleet's Apple service-discovery address.

**E. Queries and reports**

- **CAP-094** Save a question without running it on a schedule. A server-side store: a saved question that never reaches a device.
- **CAP-106** Turn live reports off for the whole server. Server configuration: one setting that turns live reporting off deployment-wide.
- **CAP-107** Stop storing report results server-wide. Server configuration: one setting that stops results being stored.
- **CAP-108** Stop storing one report's results. A server-side field on one report, with no device component.
- **CAP-109** Cap how many report rows Fleet keeps across hosts. Server configuration: a storage policy over retained report rows.

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
- **CAP-258** Block webhook destinations on internal addresses. A deployment property of Fleet's outbound network behaviour.

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
- **CAP-318** Deploy Fleet on AWS from Fleet's reference Terraform. A deployment property: reference infrastructure code for one cloud.
- **CAP-319** Deploy Fleet on GCP from Fleet's reference Terraform. A deployment property: reference infrastructure code for one cloud.
- **CAP-320** Authenticate object storage without a stored key. A deployment property: object-store credentials without a stored key.
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

14 cells where no boundary was found in either direction. Each record says what was searched, which is the part a later pass needs.

**E01** CAP-034, ChromeOS. Whether an end user's identity can be attached to a Chromebook at enrollment. The extension enrolls through the ordinary agent enrollment endpoint, and that handler has no end-user-authentication branch, but absence from one path is not a boundary. Searched: the end-user-authentication flag, the over-the-air authentication requirement, the identity-required error, and the word identity, across the enrollment handler; and ChromeOS crossed with identity, end user and authentication across the server and the extension. No hits in either direction. Every other platform on this row is established.

**E02** CAP-124, Android. Whether Android applications, as opposed to Android operating-system builds, are matched against known vulnerabilities. Android application rows are not on the exclusion list that keeps Apple mobile applications out of matching, so they do enter it. No generator was found that produces a match for a Play Store package name, and no positive rejection was found either. Searched: Android across the whole vulnerability tree, the Android application source name, and a full read of the matching translation. Android operating-system findings are a separate and definite yes.

**E03** CAP-124, ChromeOS. Whether browser extensions are matched against known vulnerabilities. Extension rows are likewise absent from the exclusion list, so they enter matching, but no extension-specific source was found and no explicit rejection either. Searched: ChromeOS across the whole vulnerability tree, the translation path, and a full read of the matching translation.

**E04** CAP-126, ChromeOS. Follows the extension question above. If extension findings exist, the severity and exploitation fields apply to them with no ChromeOS-specific branch, because those fields are per-vulnerability. If they do not, there is nothing to score. Nothing was found that settles which. Searched as for the row above.

**E05** CAP-127, ChromeOS. Follows the extension question above, on the same evidence: the filter and sort fields are per-vulnerability and carry no ChromeOS branch, so the answer depends entirely on whether extension findings exist at all. Searched as for the row above.

**E06** CAP-128, ChromeOS. Follows the extension question above, on the same evidence: the fixed-version field is carried on the finding, so the answer depends entirely on whether extension findings exist at all. Searched as for the row above.

**E07** CAP-154, iOS/iPadOS. Whether the platform single sign-on registration variable can be used in a profile for an iPhone or iPad. Fleet applies no platform check to it: it sits in the shared Apple profile allow-list, which serves macOS, iOS and iPadOS alike. Searched: every spelling of platform single sign-on, the shared-device-key option and the related stored assets, across the server, the enterprise code and the four platform single sign-on packages; then those files searched again for each Apple platform name. The only evidence of macOS scope is documentary, describing a Mac extension, and a naming rule on the extension identifier. There is no allow-list that iPhone and iPad are absent from, so this is not a refusal.

**E08** CAP-240, ChromeOS. Whether Fleet can tell that a Chromebook's disk is encrypted. The three disk-encryption queries carry platform allow-lists that ChromeOS is absent from, but no extension table was found that answers the question either, so calling it a refusal would rest on absence alone. Searched: disk encryption across the query definitions, and ChromeOS across the whole query-definition package.

**E09** CAP-253, Windows. Whether a Windows host can be refused a sign-in for failing a policy. The policy side explicitly permits it: a policy carrying the conditional-access flag must name macOS or Windows, and Windows is one of the two. The evaluator itself contains no platform check. What is missing is a Windows certificate-delivery route, and the only such route in the tree is the Apple profile one. Searched: every conditional-access route, the Windows-specific profile handler names, and every mention of platform inside the conditional-access package. That is absence, not a refusal.

**E10** CAP-254, Windows. Whether a bypass granted to a Windows host can actually be consumed. Granting one is platform-blind, with no platform check on the grant path or in the store, and a Windows host may carry a conditional-access policy. Consuming it means reaching the identity provider flow, which needs the same Windows certificate delivery the row above leaves unsettled. Unsettled, not conditional: there is no branch to state.

**E11** CAP-285, Windows. Whether changing the address everything uses to reach Fleet re-points an already-enrolled Windows host, or is refused. Neither was found. Searched: the address-changed signal in the settings handler, which has one use and feeds only the Apple re-sync; and the server address across the whole Windows MDM package. Absence of a path is not evidence of a boundary.

**E12** CAP-285, Linux. The same question for Linux, where the agent's server address comes from packaging. No re-point path and no refusal were found. Searched: the server address across the agent enrollment handler and the whole agent tree.

**E13** CAP-310, ChromeOS. Whether the extension pins a certificate, and so whether rotating Fleet's own certificate disconnects Chromebooks. No pinning option was found. Searched: certificate, authority, pin and transport security across the extension source. The extension makes ordinary web requests, so the browser's trust store presumably applies, but there is no positive evidence for that, which makes it unsettled rather than supported.

**E14** CAP-341b, Windows. Whether the diagnostic archive a Windows device produces can be retrieved through Fleet. Fleet stores and returns the raw result the device sends, not merely a status code, so the storage side is not the obstacle. What is unsettled is whether the collection command returns the archive inline in that result or uploads it to an address the operator supplies. That is a Microsoft protocol question, and no vendor source carrying a version was available to settle it. Fleet implements no parsing, result handler, interface or command specific to that collection. A later pass should read Microsoft's reference for the diagnostic-log configuration provider, over the Windows builds Fleet supports, and answer one question: whether the archive definition returns data inline.

## One row that is not a Fleet capability

**CAP-342, collect a sysdiagnose from an iPhone or iPad.** This row is not in the matrix, and it is not server-side either. Fleet neither triggers nor retrieves a sysdiagnose on any platform. The Apple command set Fleet implements is a closed list of eighteen request types, none of which collects a log or an archive; the four diagnostic-log recipes Fleet documents are all Windows; and there is no agent and no script execution on iPhone or iPad. On those devices the artefact does exist, and the person holding the phone produces it through iOS itself. That is a fact about Apple's platform rather than about Fleet, so it cannot honestly be written as a Fleet capability cell in either direction.


## Version notes

![Reference](../_assets/icons/reference.svg) Verified against Fleet 4.90.1. Every cell was read from source at that tag. **Fleet's own documentation was used to find things and never as evidence for a cell**, because this project has confirmed it wrong at this release in four separate ways, including an operating-system floor Fleet documents that nothing implements ([a.6](a.6-glossary-and-release-compatibility.md)).

**The count of `Unsupported` cells fell substantially between the two research passes**, and that is worth knowing when reading them. The first pass wrote `Unsupported` in places where it meant that it had not found a mechanism; the second reclassified those to `Not established` unless a positive boundary existed, and reclassified another group to `Not applicable` where the row's subject does not exist on the platform at all. **The remaining `Unsupported` cells each have a refusal behind them.**
