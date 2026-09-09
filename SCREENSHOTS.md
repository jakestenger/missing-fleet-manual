# Screenshot capture checklist: Parts 0–V

64 capture briefs, plus 12 reuse placements in the living edition. Each brief describes a useful view; some call for two separate frames. The same captures can serve the frozen edition when its visible behavior and controls match.

The chapter comments are the source of truth. This checklist covers the company and product introductions and every remaining chapter in Parts 0–V. The approved introduction prose is retained. Chapters without a new screenshot use text or existing diagrams where those explain the subject more clearly.

## Capture conventions

- Use a demo instance whenever practical. Dogfood is suitable for existing, non-sensitive views; stage enrollment, failures, configuration changes, and state-changing actions on disposable test devices.
- Record the Fleet server version, fleetd version where relevant, device OS, date, and source instance with each capture. If Dogfood is newer than the book, compare the visible controls with the pinned edition before reusing the image. Capture 4.90 separately where it differs. The three briefs marked **4.91 only** do not belong in the frozen 4.90 edition.
- Use the same Fleet theme, browser zoom, and approximate viewport for desktop captures. A 1440-pixel-wide viewport at 100% zoom with a 2× capture is a useful starting point. Keep native product fonts, colors, labels, and proportions. Device setup screens should retain their actual OS appearance.
- Save clean PNGs. Crop around the useful content while retaining enough page, fleet, or host context to orient the reader. Check that essential labels remain readable at about 720 pixels wide; use a detail crop or second frame when needed.
- Keep credentials, enrollment links, QR codes, My Device URLs, personal information, and private company data out of the frame. Use demo identities and non-sensitive output. Opaque redaction is acceptable when necessary; label a redaction rather than replacing a value with invented UI. Never photograph a revealed recovery key.
- Capture each real state separately. Do not combine controls or statuses that never coexist, redraw product UI, or add fictional success messages. Keep explanations in the caption. Use at most a few numbered callouts if the accepted image needs them.
- Use the proposed filename for one frame. For multiple frames add descriptive suffixes such as `-settings`, `-result`, or `-detail`; add `-4.90` for a distinct frozen-edition capture. Keep the SS ID in every filename so the artwork can be matched to its chapter comment.
- Check off a brief when its requested primary frames are captured. Note omitted optional frames and record the saved paths/version in your working copy. Artwork still needs review, alt text, and insertion into the chapter; these comments do not create visible placeholders.

## Chapter coverage

| Chapter | Topic | New briefs | Reuse |
|---|---|---|---|
| 0.1 | Who Fleet is | — | — |
| 0.2 | What Fleet is | [SS-0.2-01](#ss-02-01) | — |
| 0.3 | How to use this manual | [SS-0.3-01](#ss-03-01) | — |
| 0.4 | What changed, by release | — | — |
| 1.1 | How Fleet works | — | — |
| 1.2 | How Fleet reaches a device | [SS-1.2-01](#ss-12-01), [SS-1.2-02](#ss-12-02) | — |
| 1.3 | Hosts, fleets, labels, and targeting | [SS-1.3-01](#ss-13-01), [SS-1.3-02](#ss-13-02) | — |
| 1.4 | Identity and roles | [SS-1.4-01](#ss-14-01) | [SS-1.5-01](#ss-15-01) |
| 1.5 | Audit and activity | [SS-1.5-01](#ss-15-01) | — |
| 1.6 | The Fleet server | — | — |
| 2.1 | Administration model and deployment choices | — | — |
| 2.2 | Self-hosting architecture and capacity | [SS-2.2-01](#ss-22-01) | — |
| 2.3 | Deploy on AWS or GCP | — | [SS-2.2-01](#ss-22-01) |
| 2.4 | Deploy with containers or virtual machines | — | [SS-2.2-01](#ss-22-01) |
| 2.5 | Identity providers, SSO, SCIM, and role sync | [SS-2.5-01](#ss-25-01), [SS-2.5-02](#ss-25-02), [SS-2.5-03](#ss-25-03) | — |
| 2.6 | User accounts, roles, and service identities | [SS-2.6-01](#ss-26-01) | [SS-1.4-01](#ss-14-01) |
| 2.7 | Organization and server settings | [SS-2.7-01](#ss-27-01), [SS-2.7-02](#ss-27-02) | — |
| 2.8 | Activity, audit logs, and log delivery | — | [SS-1.5-01](#ss-15-01) |
| 2.9 | MDM architecture and foundations | — | [SS-2.10-01](#ss-210-01) |
| 2.10 | Apple MDM configuration | [SS-2.10-01](#ss-210-01), [SS-2.10-02](#ss-210-02) | — |
| 2.11 | Configure Windows management | [SS-2.11-01](#ss-211-01) | — |
| 2.12 | Bind Android Enterprise | [SS-2.12-01](#ss-212-01) | — |
| 2.13 | Connect certificate authorities | [SS-2.13-01](#ss-213-01) | — |
| 3.1 | Enrollment design and host lifecycle | — | [SS-1.2-02](#ss-12-02), [SS-1.3-01](#ss-13-01) |
| 3.2 | Enroll macOS devices | [SS-3.2-01](#ss-32-01), [SS-3.2-02](#ss-32-02), [SS-3.2-03](#ss-32-03) | — |
| 3.3 | Enroll Windows devices | [SS-3.3-01](#ss-33-01) | [SS-2.11-01](#ss-211-01) |
| 3.4 | Enroll Linux devices | [SS-3.4-01](#ss-34-01) | — |
| 3.5 | Enroll iOS and iPadOS devices | [SS-3.5-01](#ss-35-01) | [SS-2.10-02](#ss-210-02) |
| 3.6 | Enroll Android devices | [SS-3.6-01](#ss-36-01), [SS-3.6-02](#ss-36-02) | — |
| 3.7 | Enroll ChromeOS devices | [SS-3.7-01](#ss-37-01), [SS-3.7-02](#ss-37-02) | — |
| 3.8 | Manage fleetd, Orbit, and updates | — | [SS-1.2-01](#ss-12-01) |
| 4.1 | Understand host data, vitals, and inventory | [SS-4.1-01](#ss-41-01), [SS-4.1-02](#ss-41-02) | — |
| 4.2 | Run queries and read reports | [SS-4.2-01](#ss-42-01), [SS-4.2-02](#ss-42-02) | — |
| 4.3 | Use policies for compliance | [SS-4.3-01](#ss-43-01) | — |
| 4.4 | Understand software and vulnerabilities | [SS-4.4-01](#ss-44-01), [SS-4.4-02](#ss-44-02) | — |
| 4.5 | Monitor fleet-wide state | [SS-4.5-01](#ss-45-01), [SS-4.5-02](#ss-45-02) | — |
| 4.6 | Advanced osquery: query design, tables, and performance | [SS-4.6-01](#ss-46-01) | — |
| 4.7 | Extend Fleet telemetry | [SS-4.7-01](#ss-47-01) | — |
| 5.1 | Plan, target, and govern device changes | [SS-5.1-01](#ss-51-01) | — |
| 5.2 | Manage configuration profiles and declarative settings | [SS-5.2-01](#ss-52-01), [SS-5.2-02](#ss-52-02) | — |
| 5.3 | Run and manage scripts | [SS-5.3-01](#ss-53-01), [SS-5.3-02](#ss-53-02) | — |
| 5.4 | Manage software and applications | [SS-5.4-01](#ss-54-01), [SS-5.4-02](#ss-54-02), [SS-5.4-03](#ss-54-03) | — |
| 5.5 | Design setup and self-service experiences | [SS-5.5-01](#ss-55-01), [SS-5.5-02](#ss-55-02), [SS-5.5-03](#ss-55-03), [SS-5.5-04](#ss-55-04) | — |
| 5.6 | Control operating system updates | [SS-5.6-01](#ss-56-01), [SS-5.6-02](#ss-56-02), [SS-5.6-03](#ss-56-03) | — |
| 5.7 | Control devices and send custom MDM commands | [SS-5.7-01](#ss-57-01), [SS-5.7-02](#ss-57-02) | — |
| 5.8 | Enforce disk encryption and manage recovery credentials | [SS-5.8-01](#ss-58-01), [SS-5.8-02](#ss-58-02), [SS-5.8-03](#ss-58-03) | [SS-3.4-01](#ss-34-01) |
| 5.9 | Automate responses to policy failures | [SS-5.9-01](#ss-59-01), [SS-5.9-02](#ss-59-02), [SS-5.9-03](#ss-59-03) | — |

## Part 0 — Introduction

### SS-0.2-01

- [ ] **SS-0.2-01: Fleet’s Hosts page**

**Place:** Chapter 0.2, “What Fleet is” ([4.91](manual/00-Introduction/0.2-what-fleet-is.md#what-fleet-is), [4.90](website/versioned_docs/version-4.90/00-Introduction/0.2-what-fleet-is.md#what-fleet-is)).

**Purpose:** Give the product overview a concrete view of the devices an administrator manages.

**Prepare:** Use a populated demo deployment with macOS, Windows, Linux and mobile hosts; choose realistic fictional hostnames and a mix of online/offline devices.

**Capture:** Capture the Hosts list with platform icons, hostnames, online indicators, and the fleet column visible. Keep the active fleet scope and filter/search controls in view.

**Frame:** One wide screenshot of the table and filter bar; include enough rows to show variety without a full-page scroll.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-0.2-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-0.3-01

- [ ] **SS-0.3-01: Finding a chapter and choosing an edition**

**Place:** Chapter 0.3, “Where to start” ([4.91](manual/00-Introduction/0.3-how-to-use-this-manual.md#where-to-start), [4.90](website/versioned_docs/version-4.90/00-Introduction/0.3-how-to-use-this-manual.md#where-to-start)).

**Purpose:** Show how the reading paths map to the published manual.

**Prepare:** Open this manual on a desktop browser, on How to use this manual in the 4.91 edition. Expand the relevant sidebar category.

**Capture:** Open the version dropdown so the 4.91 and 4.90 editions are visible. Include the active chapter title and the left chapter navigation.

**Frame:** Capture the manual page header and upper sidebar with a small amount of chapter text; leave browser tabs and address bar out.

**Edition:** Current published manual; this screenshot documents the manual rather than the Fleet application.

**Privacy:** No application or company data needed; capture the public manual.

**Filename:** `ss-0.3-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.


## Part I — Foundations

### SS-1.2-01

- [ ] **SS-1.2-01: Agent versions on a host**

**Place:** Chapter 1.2, “The host-side bundle” ([4.91](manual/01-foundations/1.2-how-fleet-reaches-a-device.md#the-host-side-bundle), [4.90](website/versioned_docs/version-4.90/01-foundations/1.2-how-fleet-reaches-a-device.md#the-host-side-bundle)).

**Purpose:** Connect fleetd’s component names to a real device record.

**Prepare:** Use a demo Mac or Windows host with fleetd enrolled and component versions populated.

**Capture:** Open host details and capture the Agent section showing the reported Orbit/fleetd and osquery versions, along with any Fleet Desktop version the release exposes. Preserve the UI’s actual labels.

**Frame:** Crop to Agent and a small amount of host header; use a readable scale and no unrelated tabs.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-1.2-01.png`

**Also place:** Chapter 3.8, “Verification and ownership” ([4.91](manual/03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md#verification-and-ownership), [4.90](website/versioned_docs/version-4.90/03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md#verification-and-ownership)). SS-1.2-01. Reuse the host agent-version capture to show verification after a channel change. Keep update_channels YAML and repository commands as selectable text.

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-1.2-02

- [ ] **SS-1.2-02: Online status and last-seen time**

**Place:** Chapter 1.2, “What “online” tells you” ([4.91](manual/01-foundations/1.2-how-fleet-reaches-a-device.md#what-online-tells-you), [4.90](website/versioned_docs/version-4.90/01-foundations/1.2-how-fleet-reaches-a-device.md#what-online-tells-you)).

**Purpose:** Show which visible fields describe contact freshness.

**Prepare:** Use an established demo host that has checked in successfully. Have an offline host available for an optional comparison frame.

**Capture:** Capture the online indicator and the last-seen timestamp together in host details. If a tooltip supplies the exact time, capture it open. A second frame may show the same area for the offline host.

**Frame:** Keep both fields in one frame wherever possible; do not imply that the indicator proves an MDM command succeeded.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-1.2-02.png`

**Also place:** Chapter 3.1, “Verification and ownership” ([4.91](manual/03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md#verification-and-ownership), [4.90](website/versioned_docs/version-4.90/03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md#verification-and-ownership)). SS-1.3-01 and SS-1.2-02. Reuse the host identity/fleet and status captures as the visual verification reference. Keep enroll secrets masked; no credential screenshot is needed.

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-1.3-01

- [ ] **SS-1.3-01: The host record and its fleet**

**Place:** Chapter 1.3, “What a host record holds” ([4.91](manual/01-foundations/1.3-hosts-fleets-labels.md#what-a-host-record-holds), [4.90](website/versioned_docs/version-4.90/01-foundations/1.3-hosts-fleets-labels.md#what-a-host-record-holds)).

**Purpose:** Show how identity, scope and observed device facts meet in host details.

**Prepare:** Use a fictional host assigned to Workstations, with software inventory and policy results populated.

**Capture:** Capture the host header, fleet assignment, basic hardware/OS details, and navigation to software, policies and activity.

**Frame:** One upper-page view with readable labels; leave long serial numbers and identifying user data out of frame.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-1.3-01.png`

**Also place:** Chapter 3.1, “Verification and ownership” ([4.91](manual/03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md#verification-and-ownership), [4.90](website/versioned_docs/version-4.90/03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md#verification-and-ownership)). SS-1.3-01 and SS-1.2-02. Reuse the host identity/fleet and status captures as the visual verification reference. Keep enroll secrets masked; no credential screenshot is needed.

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-1.3-02

- [ ] **SS-1.3-02: Comparing profile and software targeting**

**Place:** Chapter 1.3, “Targeting: how fleets and labels combine” ([4.91](manual/01-foundations/1.3-hosts-fleets-labels.md#targeting-how-fleets-and-labels-combine), [4.90](website/versioned_docs/version-4.90/01-foundations/1.3-hosts-fleets-labels.md#targeting-how-fleets-and-labels-combine)).

**Purpose:** Show that label-targeting combinations depend on the kind of item.

**Prepare:** In a Premium demo fleet, prepare harmless profile and software entries plus two labels, Canary ring and macOS. Open their targeting editors without applying new changes.

**Capture:** Capture the profile targeting controls and, separately, the software targeting controls. Show the actual include/exclude and any/all options offered by each editor, with fleet scope visible.

**Frame:** Deliver two matched crops at the same scale; leave controls unselected where selecting them would hide the alternatives. Capture the actual UI, not a composed mockup.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-1.3-02.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-1.4-01

- [ ] **SS-1.4-01: Assigning a role within a fleet**

**Place:** Chapter 1.4, “Role and scope are independent of each other” ([4.91](manual/01-foundations/1.4-identity-and-roles.md#role-and-scope-are-independent-of-each-other), [4.90](website/versioned_docs/version-4.90/01-foundations/1.4-identity-and-roles.md#role-and-scope-are-independent-of-each-other)).

**Purpose:** Make the relationship between an account, its role, and its fleet scope visible.

**Prepare:** Use a fictional demo user. Prepare two named fleets, such as Computer lab and Corporate workstations. Open the user edit dialog without saving a change.

**Capture:** Capture the role assignment controls with fleet-scoped access selected and one fleet row visible. If the UI cannot show global and fleet-scoped choices together, capture a second frame of the global-role choice from the same dialog.

**Frame:** Crop to the dialog; keep the scope selector, fleet name and role labels readable. Deliver separate frames rather than compositing them.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-1.4-01.png`

**Also place:** Chapter 2.6, “Create and manage a person's account” ([4.91](manual/02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md#create-and-manage-a-persons-account), [4.90](website/versioned_docs/version-4.90/02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md#create-and-manage-a-persons-account)). SS-1.4-01. Reuse the role-assignment dialog to illustrate account role and fleet scope; SS-2.6-01 separately covers the API-only choice.

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-1.5-01

- [ ] **SS-1.5-01: Reading actors and timestamps in the activity feed**

**Place:** Chapter 1.5, “Reading the record: in Fleet, by webhook, or streamed” ([4.91](manual/01-foundations/1.5-audit-and-activity.md#reading-the-record-in-fleet-by-webhook-or-streamed), [4.90](website/versioned_docs/version-4.90/01-foundations/1.5-audit-and-activity.md#reading-the-record-in-fleet-by-webhook-or-streamed)).

**Purpose:** Help readers recognize the records they will use during a change review.

**Prepare:** Prepare a demo feed with real recorded actions by a named administrator and a purpose-named API-only account. Include a Fleet-initiated event if one is naturally available.

**Capture:** Capture several complete activity rows with action text, actor labels and timestamps. Choose benign actions such as a policy/configuration change; do not reveal a secret to create an example.

**Frame:** Use the feed’s native layout, with its heading and scope visible. Avoid cropping away the actor or time at the row edge.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-1.5-01.png`

**Also place:** Chapter 1.4, “Why shared credentials cost you” ([4.91](manual/01-foundations/1.4-identity-and-roles.md#why-shared-credentials-cost-you), [4.90](website/versioned_docs/version-4.90/01-foundations/1.4-identity-and-roles.md#why-shared-credentials-cost-you)). SS-1.5-01. Reuse the activity-feed capture from 1.5 here to illustrate named human and service-account actors; no additional capture is needed.

**Also place:** Chapter 2.8, “Verification and ownership” ([4.91](manual/02-administer-and-deploy-fleet/2.8-activity-audit-logs-and-log-delivery.md#verification-and-ownership), [4.90](website/versioned_docs/version-4.90/02-administer-and-deploy-fleet/2.8-activity-audit-logs-and-log-delivery.md#verification-and-ownership)). SS-1.5-01. Reuse the named-actor activity feed as the Fleet-side reference when checking delivery. Keep exported event payloads as selectable JSON; an external SIEM screenshot would depend on the reader’s chosen product.

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.


## Part II — Administer and deploy Fleet

### SS-2.2-01

- [ ] **SS-2.2-01: Creating the first administrator**

**Place:** Chapter 2.2, “Complete first-run setup” ([4.91](manual/02-administer-and-deploy-fleet/2.2-self-hosting-architecture-and-capacity.md#complete-first-run-setup), [4.90](website/versioned_docs/version-4.90/02-administer-and-deploy-fleet/2.2-self-hosting-architecture-and-capacity.md#complete-first-run-setup)).

**Purpose:** Help a first-time deployer recognize the one-time setup screen and the information it asks for.

**Prepare:** Use a fresh disposable Fleet deployment with no administrator. Prepare a fictional organization and administrator; do not submit setup until the capture is complete.

**Capture:** Open the Fleet server URL and show the setup form with its name, email, password, and organization fields. Use example values in non-secret fields; leave the password empty or masked.

**Frame:** One browser-content frame, cropped around the complete form and its heading; include the submit button.

**Edition:** Capture each edition if the setup form differs.

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-2.2-01.png`

**Also place:** Chapter 2.3, “Understand and consume Fleet's AWS module” ([4.91](manual/02-administer-and-deploy-fleet/2.3-deploy-on-aws-or-gcp.md#understand-and-consume-fleets-aws-module), [4.90](website/versioned_docs/version-4.90/02-administer-and-deploy-fleet/2.3-deploy-on-aws-or-gcp.md#understand-and-consume-fleets-aws-module)). SS-2.2-01. Reuse the first-run setup form here after the AWS deployment procedure; the same capture also applies to GCP. No cloud-console screenshot is needed for this shared Fleet step.

**Also place:** Chapter 2.4, “Verification and ownership” ([4.91](manual/02-administer-and-deploy-fleet/2.4-deploy-with-containers-or-virtual-machines.md#verification-and-ownership), [4.90](website/versioned_docs/version-4.90/02-administer-and-deploy-fleet/2.4-deploy-with-containers-or-virtual-machines.md#verification-and-ownership)). SS-2.2-01. Reuse the first-run setup form when explaining the first browser visit. Keep container listings and systemd output as selectable text rather than screenshots.

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-2.5-01

- [ ] **SS-2.5-01: Administrator SSO settings**

**Place:** Chapter 2.5, “Configure SSO” ([4.91](manual/02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md#configure-sso), [4.90](website/versioned_docs/version-4.90/02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md#configure-sso)).

**Purpose:** Distinguish Fleet administrator sign-in from end-user setup authentication and locate JIT provisioning.

**Prepare:** Use a demo SAML integration with non-sensitive example metadata. Prepare the Fleet users tab; show the JIT checkbox in the state used by the example.

**Capture:** Settings > Integrations > Single sign-on (SSO), Fleet users tab. Include Identity provider name, Entity ID, metadata input choice, and Create user and sync permissions on login.

**Frame:** One readable frame of the settings panel; keep both Fleet users and End users tab labels visible. Hide tenant-specific URLs or replace them with demo values.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-2.5-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-2.5-02

- [ ] **SS-2.5-02: Confirming SCIM requests reach Fleet**

**Place:** Chapter 2.5, “Connect SCIM” ([4.91](manual/02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md#connect-scim), [4.90](website/versioned_docs/version-4.90/02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md#connect-scim)).

**Purpose:** Show the Fleet-side indication that the identity provider has contacted the SCIM integration.

**Prepare:** Connect a demo identity provider and send at least one successful test provisioning request.

**Capture:** Settings > Integrations > Identity provider (IdP), showing the actual received-request or connected status exposed by this release. Include the setting label that identifies the integration.

**Frame:** One focused settings-panel frame. Do not show a bearer token or raw request payload.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-2.5-02.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-2.5-03

- [ ] **SS-2.5-03: Device-owner context on a host**

**Place:** Chapter 2.5, “Map device owners when you need user context on hosts” ([4.91](manual/02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md#map-device-owners-when-you-need-user-context-on-hosts), [4.90](website/versioned_docs/version-4.90/02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md#map-device-owners-when-you-need-user-context-on-hosts)).

**Purpose:** Show how IdP information becomes useful to an administrator looking at a device.

**Prepare:** Use a demo host associated with a fictional employee, department, and two readable IdP groups. For 4.91, optionally use an inherited group from a nested membership.

**Capture:** Open Host details and show the IdP username, groups, and department vitals available for that host. Keep the host name and fleet context visible.

**Frame:** One host-details crop containing the relevant vitals; use a fictional email and neutral group names. If fields are separated, use two tightly matched frames.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-2.5-03.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-2.6-01

- [ ] **SS-2.6-01: Creating a dedicated automation identity**

**Place:** Chapter 2.6, “Give automation its own identities” ([4.91](manual/02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md#give-automation-its-own-identities), [4.90](website/versioned_docs/version-4.90/02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md#give-automation-its-own-identities)).

**Purpose:** Make the API-only account choice easy to recognize without exposing a generated token.

**Prepare:** Use an administrator in a demo instance. Prepare a fictional automation identity such as Inventory reporting; decide its role and scope before capture.

**Capture:** Settings > Users > Create user with API-only selected and the role/scope controls visible. Capture before submission or token generation.

**Frame:** One complete dialog with readable labels and the intended role. Do not capture the token result.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-2.6-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-2.7-01

- [ ] **SS-2.7-01: Organization branding and support details**

**Place:** Chapter 2.7, “Organization name, logo, and contact URL” ([4.91](manual/02-administer-and-deploy-fleet/2.7-organization-and-server-settings.md#organization-name-logo-and-contact-url), [4.90](website/versioned_docs/version-4.90/02-administer-and-deploy-fleet/2.7-organization-and-server-settings.md#organization-name-logo-and-contact-url)).

**Purpose:** Show where administrators make Fleet recognizable and direct employees to internal support.

**Prepare:** Prepare a fictional organization name, demo logo, and example help-desk URL.

**Capture:** Settings > Organization settings > Organization info, showing the name, logo controls, and contact URL.

**Frame:** One panel crop with all relevant labels; use a neutral demo logo and a non-sensitive support address.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-2.7-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-2.7-02

- [ ] **SS-2.7-02: Recognizing GitOps-managed settings**

**Place:** Chapter 2.7, “GitOps mode: making the interface read-only” ([4.91](manual/02-administer-and-deploy-fleet/2.7-organization-and-server-settings.md#gitops-mode-making-the-interface-read-only), [4.90](website/versioned_docs/version-4.90/02-administer-and-deploy-fleet/2.7-organization-and-server-settings.md#gitops-mode-making-the-interface-read-only)).

**Purpose:** Explain why a managed setting cannot be edited in the interface and where to make the change.

**Prepare:** Use a Premium demo instance with GitOps mode enabled and a public example repository URL configured.

**Capture:** Open one managed settings section with disabled controls and show the tooltip or message linking to the owning repository.

**Frame:** One crop showing the setting, its read-only state, and the repository message together. Capture the actual tooltip if needed; do not add explanatory UI overlays.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-2.7-02.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-2.10-01

- [ ] **SS-2.10-01: Apple management connections and renewal dates**

**Place:** Chapter 2.10, “Turning Apple MDM on” ([4.91](manual/02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md#turning-apple-mdm-on), [4.90](website/versioned_docs/version-4.90/02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md#turning-apple-mdm-on)).

**Purpose:** Show the independent Apple credentials and the dates an administrator must track.

**Prepare:** Use a demo instance with Apple MDM enabled and test AB/ABM and VPP connections. Use fictional connection names; no actual token contents.

**Capture:** Settings > Integrations > MDM with Apple MDM on and the Apple Business/Apple Business Manager and Volume Purchasing connection rows visible. Include Renew date and the relevant Actions menus.

**Frame:** One readable panel crop, or two matched crops if the credential rows cannot fit legibly. Do not force an expired state on Dogfood.

**Edition:** Capture 4.91 and 4.90 separately if Apple Business naming or controls differ; use the actual release labels.

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-2.10-01.png`

**Also place:** Chapter 2.9, “The credentials you are taking on” ([4.91](manual/02-administer-and-deploy-fleet/2.9-mdm-architecture-and-foundations.md#the-credentials-you-are-taking-on), [4.90](website/versioned_docs/version-4.90/02-administer-and-deploy-fleet/2.9-mdm-architecture-and-foundations.md#the-credentials-you-are-taking-on)). SS-2.10-01. Reuse the Apple MDM credential/status capture to make ownership and renewal dates concrete; retain the platform diagram for the overall trust model.

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-2.10-02

- [ ] **SS-2.10-02: Assigning Apple enrollment destinations**

**Place:** Chapter 2.10, “Where automatically enrolled hosts land” ([4.91](manual/02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md#where-automatically-enrolled-hosts-land), [4.90](website/versioned_docs/version-4.90/02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md#where-automatically-enrolled-hosts-land)).

**Purpose:** Show that default fleet placement is chosen separately for macOS, iOS, and iPadOS within an Apple token.

**Prepare:** Create demo fleets with clearly different names, then open one test AB/ABM token’s Actions > Edit fleets dialog.

**Capture:** Capture the per-platform default fleet selectors, with at least two different destinations and one Unassigned example if allowed. Include the BYOD destination selector if this release provides it, using a second crop if needed; chapter 3.5 reuses that account-driven enrollment detail.

**Frame:** One complete dialog showing the token context, platform labels, and selected fleets; no token value.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-2.10-02.png`

**Also place:** Chapter 3.5, “Automated Device Enrollment” ([4.91](manual/03-connect-devices/3.5-enroll-ios-and-ipados-devices.md#automated-device-enrollment), [4.90](website/versioned_docs/version-4.90/03-connect-devices/3.5-enroll-ios-and-ipados-devices.md#automated-device-enrollment)). SS-2.10-02. Reuse the Apple-token default-fleet selectors; extend that capture to include the BYOD selector if present in the release, because it governs account-driven enrollment.

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-2.11-01

- [ ] **SS-2.11-01: Windows MDM and enrollment settings**

**Place:** Chapter 2.11, “Turning Windows MDM on” ([4.91](manual/02-administer-and-deploy-fleet/2.11-configure-windows-management.md#turning-windows-mdm-on), [4.90](website/versioned_docs/version-4.90/02-administer-and-deploy-fleet/2.11-configure-windows-management.md#turning-windows-mdm-on)).

**Purpose:** Show where administrators choose the Windows enrollment experience and connect Entra.

**Prepare:** Use a demo instance with Windows certificate configuration complete and Windows MDM enabled. Use a test Entra application with non-sensitive identifiers.

**Capture:** Settings > Integrations > MDM > Windows management. Show Automatic/Manual enrollment controls and the Entra connection section. In 4.91, include User driven enrollment and Default fleet in a second frame if needed.

**Frame:** One or two focused panel captures with complete labels. Keep tenant/client IDs masked or replace them with demo values; no private key or certificate contents.

**Edition:** Capture 4.90 separately: the user-driven Default fleet control is a 4.91 addition.

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-2.11-01.png`

**Also place:** Chapter 3.3, “Choose an enrollment approach” ([4.91](manual/03-connect-devices/3.3-enroll-windows-devices.md#choose-an-enrollment-approach), [4.90](website/versioned_docs/version-4.90/03-connect-devices/3.3-enroll-windows-devices.md#choose-an-enrollment-approach)). SS-2.11-01. Reuse the Windows management controls when comparing automatic and manual enrollment. The Windows-side confirmation is SS-3.3-01.

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-2.12-01

- [ ] **SS-2.12-01: A completed Android Enterprise connection**

**Place:** Chapter 2.12, “Verification and ownership” ([4.91](manual/02-administer-and-deploy-fleet/2.12-bind-android-enterprise.md#verification-and-ownership), [4.90](website/versioned_docs/version-4.90/02-administer-and-deploy-fleet/2.12-bind-android-enterprise.md#verification-and-ownership)).

**Purpose:** Give the reader a clear Fleet-side success state after Google’s signup flow.

**Prepare:** Complete a test Android Enterprise binding at a stable demo Fleet URL. Do not disconnect or recreate the company’s Dogfood enterprise for this capture.

**Capture:** Settings > Integrations > MDM showing Android connected/on and the enterprise identity or status the release exposes.

**Frame:** One focused Android panel with its heading and successful connection state. Hide real account identifiers; leave destructive controls untouched.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-2.12-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-2.13-01

- [ ] **SS-2.13-01: Connected certificate authorities**

**Place:** Chapter 2.13, “The six certificate authority types” ([4.91](manual/02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md#the-six-certificate-authority-types), [4.90](website/versioned_docs/version-4.90/02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md#the-six-certificate-authority-types)).

**Purpose:** Show how named authorities in Fleet correspond to the names used in profile variables.

**Prepare:** In a Premium demo instance, connect a working test custom SCEP authority with a simple name such as Corporate_SCEP. Add a second type only if a test service is already available.

**Capture:** Settings > Integrations > Certificate authorities, showing the connected authority names and types. If the add dialog explains type selection more clearly, include it as a second frame before entering credentials.

**Frame:** One readable list crop; optionally one type-selector dialog. Never include passwords, tokens, challenges, or private keys.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-2.13-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.


## Part III — Connect devices

### SS-3.2-01

- [ ] **SS-3.2-01: Choosing a macOS enrollment link**

**Place:** Chapter 3.2, “Enrolling by link, which is the ordinary manual path” ([4.91](manual/03-connect-devices/3.2-enroll-macos-devices.md#enrolling-by-link-which-is-the-ordinary-manual-path), [4.90](website/versioned_docs/version-4.90/03-connect-devices/3.2-enroll-macos-devices.md#enrolling-by-link-which-is-the-ordinary-manual-path)).

**Purpose:** Show the company-owned and personal choices and where the enrollment link is obtained.

**Prepare:** Use a demo instance with Apple MDM configured and a clearly named pilot fleet selected. Open Add hosts for macOS.

**Capture:** Capture the Add hosts dialog with macOS selected, the company-owned/personal choice, and the copy-link control.

**Frame:** One complete dialog. Mask the entire secret-bearing link while retaining the control label; do not show a usable enroll secret or QR code.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-3.2-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-3.2-02

- [ ] **SS-3.2-02: The employee’s macOS migration prompt**

**Place:** Chapter 3.2, “The device flow, and the two branches after unenrolment” ([4.91](manual/03-connect-devices/3.2-enroll-macos-devices.md#the-device-flow-and-the-two-branches-after-unenrolment), [4.90](website/versioned_docs/version-4.90/03-connect-devices/3.2-enroll-macos-devices.md#the-device-flow-and-the-two-branches-after-unenrolment)).

**Purpose:** Show the interaction an employee must take even when migration is configured as forced.

**Prepare:** Use a test Mac already managed by a disposable previous MDM and eligible for Fleet migration, with Fleet Desktop installed. Coordinate the test webhook; capture before starting migration.

**Capture:** Open the actual Fleet Desktop migration dialog with the Start and Later buttons visible.

**Frame:** One dialog with enough macOS menu-bar context to identify Fleet Desktop. Use a fictional organization; do not click Start merely for the screenshot.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-3.2-02.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-3.2-03

- [ ] **SS-3.2-03: Apple enrollment assignment and retrieval timestamps**

**Place:** Chapter 3.2, “The ADE sequence, in order” ([4.91](manual/03-connect-devices/3.2-enroll-macos-devices.md#the-ade-sequence-in-order), [4.90](website/versioned_docs/version-4.90/03-connect-devices/3.2-enroll-macos-devices.md#the-ade-sequence-in-order)).

**Purpose:** Make the two ADE timestamps easy to distinguish before a reader investigates a pending device.

**Prepare:** Use an AB/ABM-assigned test Mac whose enrollment profile has been assigned. Prefer a device that has also retrieved it so both timestamps are populated.

**Capture:** Open the host’s MDM/enrollment details where Fleet displays profile assignment and pushed timestamps. Include the pushed-time tooltip explaining retrieval by the device.

**Frame:** One close crop containing the two labeled timestamps and tooltip, with the test host identity for context. Mask serial numbers if using Dogfood.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-3.2-03.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-3.3-01

- [ ] **SS-3.3-01: Confirming Windows work or school enrollment**

**Place:** Chapter 3.3, “Verifying an enrollment” ([4.91](manual/03-connect-devices/3.3-enroll-windows-devices.md#verifying-an-enrollment), [4.90](website/versioned_docs/version-4.90/03-connect-devices/3.3-enroll-windows-devices.md#verifying-an-enrollment)).

**Purpose:** Show the Windows-side view that an administrator or employee can use to confirm the management connection.

**Prepare:** Enroll a disposable Windows test device through the path described in the chapter. Use a fictional user and organization.

**Capture:** Windows Settings > Accounts > Access work or school, with the relevant connected organization/management entry expanded. Include the Info control or management-details view if it identifies Fleet.

**Frame:** One Windows settings crop, plus a second detail frame only if needed to identify the MDM connection. Mask tenant-specific addresses and personal details.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-3.3-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-3.4-01

- [ ] **SS-3.4-01: Starting Linux recovery-key escrow**

**Place:** Chapter 3.4, “Configure the Linux escrow prerequisites” ([4.91](manual/03-connect-devices/3.4-enroll-linux-devices.md#configure-the-linux-escrow-prerequisites), [4.90](website/versioned_docs/version-4.90/03-connect-devices/3.4-enroll-linux-devices.md#configure-the-linux-escrow-prerequisites)).

**Purpose:** Show the employee action that requests escrow after the administrator has configured it.

**Prepare:** Use a supported disposable Linux device with an encrypted root disk, eligible fleetd, Premium configuration, and no key already escrowed or pending. For the passphrase path, install zenity or kdialog.

**Capture:** Open My Device and show the disk-encryption recovery-key action/instructions before submitting credentials. A second frame may show the local passphrase prompt with the input empty.

**Frame:** One clear My Device action crop and, if useful, one complete local dialog. Never show a passphrase or recovery key; use demo data.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-3.4-01.png`

**Also place:** Chapter 5.8, “Escrow recovery material from an already-encrypted LUKS host” ([4.91](manual/05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md#escrow-recovery-material-from-an-already-encrypted-luks-host), [4.90](website/versioned_docs/version-4.90/05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md#escrow-recovery-material-from-an-already-encrypted-luks-host)). SS-3.4-01. Reuse the Linux My Device escrow entry and empty passphrase dialog here to guide the required user step.

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-3.5-01

- [ ] **SS-3.5-01: Installing the enrollment profile on an iPhone or iPad**

**Place:** Chapter 3.5, “Guide the user through enrollment” ([4.91](manual/03-connect-devices/3.5-enroll-ios-and-ipados-devices.md#guide-the-user-through-enrollment), [4.90](website/versioned_docs/version-4.90/03-connect-devices/3.5-enroll-ios-and-ipados-devices.md#guide-the-user-through-enrollment)).

**Purpose:** Show the transition from downloading a profile to installing and trusting it, where employees often pause.

**Prepare:** Use a disposable iPhone or iPad and a demo company-owned manual enrollment link. Prepare the profile download in Safari. Do not include the credential-bearing browser URL.

**Capture:** Capture two or three device screens in order: the Fleet enrollment instructions after download; Settings > Profile Downloaded with the Install control; and the Remote Management trust prompt. Retain the actual Not Verified warning if it appears.

**Frame:** Use matched device-screen crops with native text readable and the same device orientation. No personal notifications, passcodes, or usable enrollment URLs. Label the frames in the caption rather than editing the UI.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-3.5-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-3.6-01

- [ ] **SS-3.6-01: Choosing personal or company-owned Android enrollment**

**Place:** Chapter 3.6, “Doing it” ([4.91](manual/03-connect-devices/3.6-enroll-android-devices.md#doing-it), [4.90](website/versioned_docs/version-4.90/03-connect-devices/3.6-enroll-android-devices.md#doing-it)).

**Purpose:** Show the ownership decision before a device receives its enrollment token.

**Prepare:** Open Add hosts in a demo instance with Android Enterprise connected and a named pilot fleet selected.

**Capture:** Choose Android and capture the Personal (BYOD) and Company-owned (fully-managed) controls with the selected path’s instructions. If the instructions change substantially, provide one frame per selection.

**Frame:** One or two matched dialog crops. Fully mask enrollment links and QR codes; retain their surrounding labels and instructions.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-3.6-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-3.6-02

- [ ] **SS-3.6-02: Recognizing the Android work profile**

**Place:** Chapter 3.6, “Verifying an enrollment” ([4.91](manual/03-connect-devices/3.6-enroll-android-devices.md#verifying-an-enrollment), [4.90](website/versioned_docs/version-4.90/03-connect-devices/3.6-enroll-android-devices.md#verifying-an-enrollment)).

**Purpose:** Show employees and support staff the result of personal enrollment: a separate managed work area.

**Prepare:** Enroll a disposable Android device through the personal path and add one or two benign work apps. Use a blank personal profile.

**Capture:** Capture the app drawer’s Work tab or work section with briefcase-marked apps and Android Device Policy visible.

**Frame:** One native device-screen crop showing the Work label and app badges. Exclude notifications and personal apps or account details.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-3.6-02.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-3.7-01

- [ ] **SS-3.7-01: Deploying Fleetd for Chrome through managed extension policy**

**Place:** Chapter 3.7, “Doing it” ([4.91](manual/03-connect-devices/3.7-enroll-chromeos-devices.md#doing-it), [4.90](website/versioned_docs/version-4.90/03-connect-devices/3.7-enroll-chromeos-devices.md#doing-it)).

**Purpose:** Connect the values Fleet provides to the force-install policy in Google Admin.

**Prepare:** Use a test Chrome organizational unit and the Fleetd for Chrome extension configuration. Prepare the extension ID and update URL from Fleet’s Add hosts > ChromeOS dialog.

**Capture:** Capture Google Admin’s extension configuration showing Fleetd for Chrome, the target organizational unit, and Force install. Include the managed policy editor only if fleet_url and enroll_secret field names remain readable with values masked.

**Frame:** One settings-panel crop. Keep the public extension ID/update URL if useful; fully mask enroll-secret values and any real organization identifiers.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-3.7-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-3.7-02

- [ ] **SS-3.7-02: A Chromebook answering a live report**

**Place:** Chapter 3.7, “Verifying an enrollment” ([4.91](manual/03-connect-devices/3.7-enroll-chromeos-devices.md#verifying-an-enrollment), [4.90](website/versioned_docs/version-4.90/03-connect-devices/3.7-enroll-chromeos-devices.md#verifying-an-enrollment)).

**Purpose:** Show the useful reporting result of a successful ChromeOS enrollment.

**Prepare:** Enroll a demo Chromebook and run SELECT * FROM os_version against that single host.

**Capture:** Capture the Fleet live-report view with the SQL, successful host response, and a compact row of ChromeOS version results.

**Frame:** One readable report crop with host context; use a fictional host name and no user data.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-3.7-02.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.


## Part IV — Know your devices

### SS-4.1-01

- [ ] **SS-4.1-01: Reading a host’s certificate inventory**

**Place:** Chapter 4.1, “Certificates” ([4.91](manual/04-know-your-devices/4.1-understand-hosts-vitals-and-inventory.md#certificates), [4.90](website/versioned_docs/version-4.90/04-know-your-devices/4.1-understand-hosts-vitals-and-inventory.md#certificates)).

**Purpose:** Show the certificate list used to confirm issuance and review expiry.

**Prepare:** Use a demo Mac or Windows host with two or three test certificates, including one issued through Fleet if available.

**Capture:** Host details > Certificates, showing certificate names, issuers, expiry dates, and any scope information visible in the release.

**Frame:** One table crop with the host context and column headings. Use test certificate subjects; do not expose private keys or employee identity information.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-4.1-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-4.1-02

- [ ] **SS-4.1-02: Expanded iPhone or iPad vitals**

**Place:** Chapter 4.1, “What an iPhone or iPad reports, and what a personally owned one does not” ([4.91](manual/04-know-your-devices/4.1-understand-hosts-vitals-and-inventory.md#what-an-iphone-or-ipad-reports-and-what-a-personally-owned-one-does-not)).

**Purpose:** Introduce the View all panel added for the fuller mobile inventory in 4.91.

**Prepare:** Use a company-owned test iPhone or iPad on Fleet 4.91 with a completed device-information refetch. Populate ordinary non-sensitive vitals.

**Capture:** Open the host’s Vitals card and View all. Capture the expanded panel with readable device properties, showing the breadth of information without scrolling through every field.

**Frame:** One focused expanded-panel frame with its title and a representative set of values. Mask serial, IMEI, phone number, account, and network identifiers.

**Edition:** 4.91 only; this expanded set must not be illustrated as a 4.90 feature.

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-4.1-02.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-4.2-01

- [ ] **SS-4.2-01: Reading live-report responses and errors**

**Place:** Chapter 4.2, “Getting results out of Fleet” ([4.91](manual/04-know-your-devices/4.2-run-queries-and-reports.md#getting-results-out-of-fleet), [4.90](website/versioned_docs/version-4.90/04-know-your-devices/4.2-run-queries-and-reports.md#getting-results-out-of-fleet)).

**Purpose:** Show why result rows, empty responses, and execution errors need separate interpretation.

**Prepare:** Use a small disposable set of hosts. Run a harmless report that returns rows on one host, no rows on another, and a deliberate unsupported-table error on a separate test platform; keep any intentional mismatch confined to the demo.

**Capture:** Capture the live report while response counters and a few result rows are visible. Then capture the Errors tab with one readable error. Keep targeted/responding and no-results/error counts visible where the UI exposes them.

**Frame:** Two matched report-panel frames, one results and one errors, with SQL and example host names. Use real states produced by the test; do not edit counters or fabricate rows.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-4.2-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-4.2-02

- [ ] **SS-4.2-02: Configuring a scheduled report’s output**

**Place:** Chapter 4.2, “From question to scheduled report” ([4.91](manual/04-know-your-devices/4.2-run-queries-and-reports.md#from-question-to-scheduled-report), [4.90](website/versioned_docs/version-4.90/04-know-your-devices/4.2-run-queries-and-reports.md#from-question-to-scheduled-report)).

**Purpose:** Connect the interval and output choices to the report’s behavior.

**Prepare:** Save a harmless demo report scoped to a pilot population. Prepare a nonzero interval, stored results enabled, and automations set to the intended forwarding state.

**Capture:** Open the report edit/settings surface showing its schedule and storage/automations controls. Include the exact labels this release uses.

**Frame:** One settings frame, or two matched crops if schedule and output controls are separate. Use a compact report name and no sensitive SQL literals.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-4.2-02.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-4.3-01

- [ ] **SS-4.3-01: Policy results and assessment coverage**

**Place:** Chapter 4.3, “Reading a policy result honestly” ([4.91](manual/04-know-your-devices/4.3-use-policies-for-compliance.md#reading-a-policy-result-honestly), [4.90](website/versioned_docs/version-4.90/04-know-your-devices/4.3-use-policies-for-compliance.md#reading-a-policy-result-honestly)).

**Purpose:** Show passing and failing counts with the refresh context, without implying they cover every host.

**Prepare:** Create a harmless demo policy with at least one passing, one failing, and one not-yet-evaluated host in a known pilot population. Allow aggregate counts to refresh.

**Capture:** Capture the Policies list with the named policy’s passing and failing counts and the page’s Last updated indicator. If opening a count reveals its host list, include one second frame.

**Frame:** One readable list crop with fleet context. The caption should state the known pilot population and explain the uncounted host; do not invent a no-answer counter or per-policy timestamp absent from the UI.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-4.3-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-4.4-01

- [ ] **SS-4.4-01: Turning a vulnerability into an affected-device list**

**Place:** Chapter 4.4, “Prioritising a list you can act on” ([4.91](manual/04-know-your-devices/4.4-understand-software-and-vulnerabilities.md#prioritising-a-list-you-can-act-on), [4.90](website/versioned_docs/version-4.90/04-know-your-devices/4.4-understand-software-and-vulnerabilities.md#prioritising-a-list-you-can-act-on)).

**Purpose:** Show the practical path from prioritizing a finding to identifying the software and hosts to update.

**Prepare:** Use a Premium demo instance with populated vulnerability data and a known test finding. Prefer a finding with CVSS, EPSS, a known-exploited value, and a resolved version where available; do not install vulnerable software on Dogfood for a capture.

**Capture:** Capture the Software vulnerabilities list with prioritization columns and affected-host counts, then the selected vulnerability’s detail view showing affected titles/versions and the route to hosts.

**Frame:** Two matched Fleet-content crops. Use actual feed values and a demo host population; do not manufacture scores or imply every finding has a resolved version.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-4.4-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-4.4-02

- [ ] **SS-4.4-02: Recognizing disabled software inventory**

**Place:** Chapter 4.4, “Handing a finding to remediation” ([4.91](manual/04-know-your-devices/4.4-understand-software-and-vulnerabilities.md#handing-a-finding-to-remediation), [4.90](website/versioned_docs/version-4.90/04-know-your-devices/4.4-understand-software-and-vulnerabilities.md#handing-a-finding-to-remediation)).

**Purpose:** Distinguish intentionally disabled collection from an empty or healthy software list.

**Prepare:** Use a disposable demo instance or isolated test scope where inventory can be disabled without affecting company operations. Record the previous setting for restoration.

**Capture:** Open the software surface that shows the explicit inventory-disabled message. Include the heading and message that explains collection is off.

**Frame:** One focused empty-state panel; no artificial empty table or edited message. This is a supporting capture after the primary populated-inventory example.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-4.4-02.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-4.5-01

- [ ] **SS-4.5-01: Reviewing the device population from the dashboard**

**Place:** Chapter 4.5, “When a number does not make sense” ([4.91](manual/04-know-your-devices/4.5-monitor-fleet-wide-state.md#when-a-number-does-not-make-sense), [4.90](website/versioned_docs/version-4.90/04-know-your-devices/4.5-monitor-fleet-wide-state.md#when-a-number-does-not-make-sense)).

**Purpose:** Show an administrator’s starting point for a regular review and make platform segmentation visible.

**Prepare:** Use a demo instance with a modest, varied host population: at least two desktop platforms and one mobile platform, with some online and offline computers. Select a clearly named fleet or global scope.

**Capture:** Capture the dashboard host-summary tiles and platform breakdown. Include the scope selector. If selecting a platform changes the summary, provide a second frame for one desktop platform.

**Frame:** One balanced dashboard crop, optionally one matched filtered frame. Keep actual counts, clear labels, and readable chart legends; do not adjust data to make overlapping counts sum to the total.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-4.5-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-4.5-02

- [ ] **SS-4.5-02: Filtering an actionable host list**

**Place:** Chapter 4.5, “Cutting the estate into populations” ([4.91](manual/04-know-your-devices/4.5-monitor-fleet-wide-state.md#cutting-the-estate-into-populations), [4.90](website/versioned_docs/version-4.90/04-know-your-devices/4.5-monitor-fleet-wide-state.md#cutting-the-estate-into-populations)).

**Purpose:** Demonstrate how an overview becomes a specific population to review or export.

**Prepare:** Use a demo population with a few Windows or macOS hosts that share one policy failure or software version.

**Capture:** Open Hosts, apply a platform and a policy-result or software filter, and show the filtered rows, active filter controls, fleet scope, and export action.

**Frame:** One host-table crop with enough rows to show a useful population and the full active filter context. Use fictional host names and masked identifiers.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-4.5-02.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-4.6-01

- [ ] **SS-4.6-01: Comparing report performance impact**

**Place:** Chapter 4.6, “When a query stops behaving” ([4.91](manual/04-know-your-devices/4.6-advanced-osquery-queries-and-tables.md#when-a-query-stops-behaving), [4.90](website/versioned_docs/version-4.90/04-know-your-devices/4.6-advanced-osquery-queries-and-tables.md#when-a-query-stops-behaving)).

**Purpose:** Show where administrators review cost before broadening a report rollout.

**Prepare:** Use a demo instance with several scheduled reports that have collected performance statistics. Prefer real examples with different impact values; do not run a deliberately expensive query on Dogfood.

**Capture:** Capture the Reports list with the Performance impact column and several readable report names. Include Minimal and a higher value if the existing test data provides them.

**Frame:** One table crop centered on the impact column and enough neighboring context to identify reports. The caption should note that the indicator reflects median cost and detailed tail statistics require the API.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-4.6-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-4.7-01

- [ ] **SS-4.7-01: Checking the available table schema before extending collection**

**Place:** Chapter 4.7, “Choosing, in practice” ([4.91](manual/04-know-your-devices/4.7-extend-osquery-with-custom-tables-and-plugins.md#choosing-in-practice), [4.90](website/versioned_docs/version-4.90/04-know-your-devices/4.7-extend-osquery-with-custom-tables-and-plugins.md#choosing-in-practice)).

**Purpose:** Show where an administrator can inspect existing tables and columns before choosing a custom mechanism.

**Prepare:** Open a new report in a demo Fleet instance. Prepare a harmless question using a built-in table such as system_info.

**Capture:** Open Schema in the report editor and expand the relevant table so its columns and description are visible beside a short SELECT statement.

**Frame:** One balanced editor-and-schema frame with readable table/column names. No host results or personal data needed. This is schema reference, not proof that every target host has the table.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-4.7-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.


## Part V — Manage devices

### SS-5.1-01

- [ ] **SS-5.1-01: Following a host’s upcoming activity queue**

**Place:** Chapter 5.1, “Ownership” ([4.91](manual/05-manage-devices/5.1-plan-target-and-govern-device-changes.md#ownership), [4.90](website/versioned_docs/version-4.90/05-manage-devices/5.1-plan-target-and-govern-device-changes.md#ownership)).

**Purpose:** Show the order of pending work and why a later installation may be waiting.

**Prepare:** Use a disposable pilot host. Queue two harmless scripts and one benign software install so one item is in progress and others are waiting; do not use lock or wipe.

**Capture:** Open Host details > Activity > Upcoming activities, with one active row and several queued rows. Include the action menu showing where queued work can be cancelled, without submitting cancellation.

**Frame:** One readable queue crop with the host name, status labels, and requested order. Use neutral script/software names and actual queue states.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-5.1-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-5.2-01

- [ ] **SS-5.2-01: Interpreting profile delivery status**

**Place:** Chapter 5.2, “When a profile is not on a device” ([4.91](manual/05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md#when-a-profile-is-not-on-a-device), [4.90](website/versioned_docs/version-4.90/05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md#when-a-profile-is-not-on-a-device)).

**Purpose:** Show status and operation together so Pending removal is not mistaken for a failed installation.

**Prepare:** Use a disposable managed host with several benign test profiles. Prepare a mix of real states such as Verified, Pending, and Failed; use an intentionally invalid test value only on that device if a failure is needed.

**Capture:** Open the host’s configuration-profile/OS-settings list. Include names, statuses, and install/remove context wherever the release displays it. Open one Failed detail to show the returned reason in a second frame.

**Frame:** One readable list crop plus an optional failure-detail crop. Do not fabricate a five-state sample if those states cannot coexist; show the useful states the device actually reports.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-5.2-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-5.2-02

- [ ] **SS-5.2-02: Setting a device-name template**

**Place:** Chapter 5.2, “Naming hosts from a template” ([4.91](manual/05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md#naming-hosts-from-a-template), [4.90](website/versioned_docs/version-4.90/05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md#naming-hosts-from-a-template)).

**Purpose:** Show how one template can produce consistent names for a fleet.

**Prepare:** Use a demo fleet with company-owned Apple test devices. Prepare a simple supported template using the hardware serial variable; use a custom vital only for a separately labeled 4.91 capture.

**Capture:** Open the fleet’s OS settings host-name template control, showing the template and any built-in help or preview. Optionally pair it with the synthetic Host name status row on one test host.

**Frame:** One settings crop and, if useful, one matching host-result crop. Mask serial numbers and avoid secrets in the naming template.

**Edition:** Both editions for supported host variables; custom-host-vital naming is 4.91 only.

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-5.2-02.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-5.3-01

- [ ] **SS-5.3-01: Reading a completed script result**

**Place:** Chapter 5.3, “Test before expanding script scope” ([4.91](manual/05-manage-devices/5.3-run-and-manage-scripts.md#test-before-expanding-script-scope), [4.90](website/versioned_docs/version-4.90/05-manage-devices/5.3-run-and-manage-scripts.md#test-before-expanding-script-scope)).

**Purpose:** Show the exit code, useful output, and runtime together as the evidence for a run.

**Prepare:** Run a harmless diagnostic script on a demo host that prints one concise status line and exits zero. Optionally prepare a separate controlled prerequisite failure for comparison.

**Capture:** Open the completed script activity on Host details. Include the script name, exit code, output, and runtime or timestamps exposed by the release.

**Frame:** One complete result dialog/panel with short readable output. No tokens, user paths, environment dumps, or secret-bearing command lines.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-5.3-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-5.3-02

- [ ] **SS-5.3-02: Selecting a script for a batch run**

**Place:** Chapter 5.3, “Running it on many at once” ([4.91](manual/05-manage-devices/5.3-run-and-manage-scripts.md#running-it-on-many-at-once), [4.90](website/versioned_docs/version-4.90/05-manage-devices/5.3-run-and-manage-scripts.md#running-it-on-many-at-once)).

**Purpose:** Show the reviewable population and saved-script choice before dispatch.

**Prepare:** As an admin or maintainer, select two or three demo hosts from the same fleet and prepare one harmless saved script in that fleet.

**Capture:** Open the multi-host Run script flow, showing the selected host count, saved-script selector, and the final run control before submission.

**Frame:** One complete dialog with its target context; do not launch work merely to capture the screen. Use a neutral name such as Check demo folder.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-5.3-02.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-5.4-01

- [ ] **SS-5.4-01: Choosing a Fleet-maintained application**

**Place:** Chapter 5.4, “Choose a software source and confirm prerequisites” ([4.91](manual/05-manage-devices/5.4-manage-software-and-applications.md#choose-a-software-source-and-confirm-prerequisites), [4.90](website/versioned_docs/version-4.90/05-manage-devices/5.4-manage-software-and-applications.md#choose-a-software-source-and-confirm-prerequisites)).

**Purpose:** Show the maintained catalog as a practical starting point that reduces installer preparation.

**Prepare:** Use a Premium demo instance and a pilot fleet. Open the maintained-app catalog with familiar supported applications populated.

**Capture:** Software > Add software > Fleet-maintained apps, showing a searchable selection of app names, platforms, and the available add action. Select one familiar app for a detail frame if it explains the maintained package clearly.

**Frame:** One clean catalog crop, optionally one app detail. Use the real catalog for the pinned release; do not add a fabricated app-count claim.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-5.4-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-5.4-02

- [ ] **SS-5.4-02: Reviewing a custom package’s lifecycle scripts**

**Place:** Chapter 5.4, “Prepare the package lifecycle contract” ([4.91](manual/05-manage-devices/5.4-manage-software-and-applications.md#prepare-the-package-lifecycle-contract), [4.90](website/versioned_docs/version-4.90/05-manage-devices/5.4-manage-software-and-applications.md#prepare-the-package-lifecycle-contract)).

**Purpose:** Show where the administrator reviews installation and removal logic before rollout.

**Prepare:** Upload a benign test package to a demo fleet and prepare concise install, post-install, and uninstall scripts with no secrets.

**Capture:** Open the package edit/details surface with lifecycle-script controls visible. Capture one short script expanded, keeping the names of the other stages in view if possible.

**Frame:** One focused package panel with application/version context; keep code legible. The chapter’s selectable examples remain the source for copying syntax.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-5.4-02.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-5.4-03

- [ ] **SS-5.4-03: Following an installation and its retry control**

**Place:** Chapter 5.4, “Manual retries” ([4.91](manual/05-manage-devices/5.4-manage-software-and-applications.md#manual-retries), [4.90](website/versioned_docs/version-4.90/05-manage-devices/5.4-manage-software-and-applications.md#manual-retries)).

**Purpose:** Show the host-level result an operator uses after requesting software.

**Prepare:** Use a disposable host with a benign test installation. Prepare either a completed result or a controlled failure with a useful message; do not disrupt a production application.

**Capture:** Open the host’s Software library and the selected title’s installation result. For the failed case, include Retry and the associated output/reason.

**Frame:** One host software row plus its result dialog, or two matched frames. Keep the host, title, version, and outcome readable; exclude secret-bearing output.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-5.4-03.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-5.5-01

- [ ] **SS-5.5-01: My Device and the transparency link**

**Place:** Chapter 5.5, “The Fleet Desktop and My Device surface” ([4.91](manual/05-manage-devices/5.5-design-setup-and-self-service-experiences.md#the-fleet-desktop-and-my-device-surface), [4.90](website/versioned_docs/version-4.90/05-manage-devices/5.5-design-setup-and-self-service-experiences.md#the-fleet-desktop-and-my-device-surface)).

**Purpose:** Show the employee view and the route to information about device management.

**Prepare:** Use a demo desktop host with Fleet Desktop installed. Open My Device from its menu-bar or tray item.

**Capture:** Capture the device summary with the page navigation visible. As a small second frame, capture the Fleet Desktop menu with About Fleet visible. Include a recovery-key availability banner only if naturally present; it must contain no key.

**Frame:** Two separate crops: the readable My Device content and the actual menu. Exclude browser chrome and the complete device-token URL.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-5.5-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-5.5-02

- [ ] **SS-5.5-02: macOS setup progress**

**Place:** Chapter 5.5, “Build the macOS setup experience” ([4.91](manual/05-manage-devices/5.5-design-setup-and-self-service-experiences.md#build-the-macos-setup-experience), [4.90](website/versioned_docs/version-4.90/05-manage-devices/5.5-design-setup-and-self-service-experiences.md#build-the-macos-setup-experience)).

**Purpose:** Help support staff recognize the screen an employee sees while a new Mac is prepared.

**Prepare:** Enroll a disposable ADE Mac into a test fleet with two small, tested setup apps and, if used, a harmless final script.

**Capture:** Capture the actual Fleet setup progress screen while one item is complete and another is underway, if that state occurs. Preserve the real item names and statuses.

**Frame:** Crop to the full setup panel, including its title, progress, and any available action. Record macOS and fleetd versions with the capture.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-5.5-02.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-5.5-03

- [ ] **SS-5.5-03: Windows Enrollment Status Page**

**Place:** Chapter 5.5, “Hold and release Windows at the Enrollment Status Page” ([4.91](manual/05-manage-devices/5.5-design-setup-and-self-service-experiences.md#hold-and-release-windows-at-the-enrollment-status-page), [4.90](website/versioned_docs/version-4.90/05-manage-devices/5.5-design-setup-and-self-service-experiences.md#hold-and-release-windows-at-the-enrollment-status-page)).

**Purpose:** Identify the blocking OOBE experience before troubleshooting its hold or failure.

**Prepare:** Use a disposable Windows device or VM undergoing automatic enrollment during OOBE with a tested setup application.

**Capture:** Capture the genuine Windows Enrollment Status Page while setup is running. An optional second capture may show a controlled failure and its actual Reset or Continue anyway choices; record the stop-on-failure setting used.

**Frame:** Show the Windows panel at readable size. Keep separate states as separate images; do not reset or enroll a Dogfood device just for the screenshot.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-5.5-03.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-5.5-04

- [ ] **SS-5.5-04: The employee self-service catalog**

**Place:** Chapter 5.5, “Where people find it” ([4.91](manual/05-manage-devices/5.5-design-setup-and-self-service-experiences.md#where-people-find-it), [4.90](website/versioned_docs/version-4.90/05-manage-devices/5.5-design-setup-and-self-service-experiences.md#where-people-find-it)).

**Purpose:** Show how employees browse and request approved software.

**Prepare:** Publish several harmless test applications to a demo fleet, assign categories and self-service entitlement, and open the entitled host's My Device page.

**Capture:** Open Self-service. Show category navigation, several app entries, and their real Install or installed-state controls. Include Uninstall only for an installer-backed title where Fleet actually offers it.

**Frame:** Crop the catalog and navigation together. Exclude the device-token URL; avoid an oversized full-screen image with tiny app labels.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-5.5-04.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-5.6-01

- [ ] **SS-5.6-01: A fixed Apple version requirement and current versions**

**Place:** Chapter 5.6, “Enforce Apple operating-system versions and deadlines” ([4.91](manual/05-manage-devices/5.6-control-operating-system-updates.md#enforce-apple-operating-system-versions-and-deadlines), [4.90](website/versioned_docs/version-4.90/05-manage-devices/5.6-control-operating-system-updates.md#enforce-apple-operating-system-versions-and-deadlines)).

**Purpose:** Orient readers to the requirement and the inventory used to follow adoption.

**Prepare:** Use a test fleet with Apple MDM configured and devices reporting at least two OS versions. Open Controls > OS updates and select macOS.

**Capture:** Capture the fixed-version and deadline fields with the selected fleet and platform visible. Take a second crop of Current versions with its timestamp and host-count links.

**Frame:** Keep the settings and inventory in separate crops if one frame would make text small. Use an existing test requirement; do not enforce a new deadline on Dogfood devices for the capture.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-5.6-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-5.6-02

- [ ] **SS-5.6-02: Latest-version enforcement and the resolved host target**

**Place:** Chapter 5.6, “Enforce the latest version with a rolling deadline” ([4.91](manual/05-manage-devices/5.6-control-operating-system-updates.md#enforce-the-latest-version-with-a-rolling-deadline)).

**Purpose:** Show the difference between a rolling requirement and the version resolved for one host.

**Prepare:** Use Fleet 4.91 with a test Apple fleet already tracking latest. Allow the hourly target-resolution job to run for a supported host.

**Capture:** Capture Controls > OS updates > macOS with latest selected and the deadline in days. Take a second crop of an Apple host's vitals showing its resolved version and deadline; an unevaluated host may be captured separately as Pending if useful.

**Frame:** Two separate views with the fleet/platform and host identity clear. Never invent a resolved target or edit UI labels.

**Edition:** 4.91 only; latest-version enforcement is absent from 4.90

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-5.6-02.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-5.6-03

- [ ] **SS-5.6-03: Windows update deadline and restart grace**

**Place:** Chapter 5.6, “Configure Windows update deadlines and grace periods” ([4.91](manual/05-manage-devices/5.6-control-operating-system-updates.md#configure-windows-update-deadlines-and-grace-periods), [4.90](website/versioned_docs/version-4.90/05-manage-devices/5.6-control-operating-system-updates.md#configure-windows-update-deadlines-and-grace-periods)).

**Purpose:** Locate the two controls readers must configure together.

**Prepare:** Open the Windows tab under Controls > OS updates for a test fleet with Windows MDM enabled.

**Capture:** Show the deadline and restart grace-period fields, their units, and the selected fleet/platform. Use a preconfigured test policy or leave a demonstration unsaved.

**Frame:** Crop the complete settings card. The caption can explain the two clocks; do not add an invented timeline inside the UI.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-5.6-03.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-5.7-01

- [ ] **SS-5.7-01: Host identity and available device actions**

**Place:** Chapter 5.7, “Make the action safe before you send it” ([4.91](manual/05-manage-devices/5.7-control-devices-and-send-mdm-commands.md#make-the-action-safe-before-you-send-it), [4.90](website/versioned_docs/version-4.90/05-manage-devices/5.7-control-devices-and-send-mdm-commands.md#make-the-action-safe-before-you-send-it)).

**Purpose:** Help operators confirm the host and recognize platform-specific action availability.

**Prepare:** Open a demo macOS or Windows host whose enrollment and action prerequisites are already satisfied.

**Capture:** Expand the host Actions menu. Keep the demo hostname, platform, and enough host identity visible to show that actions belong to one device. Optionally take an Android comparison frame to show its different available actions.

**Frame:** Crop the identity summary and menu together. Do not select Lock, Wipe, Unenroll, or any other state-changing action for this capture.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-5.7-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-5.7-02

- [ ] **SS-5.7-02: Apple MDM command result**

**Place:** Chapter 5.7, “Apple command states” ([4.91](manual/05-manage-devices/5.7-control-devices-and-send-mdm-commands.md#apple-command-states), [4.90](website/versioned_docs/version-4.90/05-manage-devices/5.7-control-devices-and-send-mdm-commands.md#apple-command-states)).

**Purpose:** Show where to read the device response when an action needs investigation.

**Prepare:** Use a demo Apple host with an existing harmless command in its command history. A normal inventory request is suitable; do not send a destructive command.

**Capture:** In host details, open Activity and enable Show MDM commands. Open an existing command's details. Show the command name, status, timestamps, and readable response details available in this version. Use an existing NotNow or Error result as a second frame only if naturally available.

**Frame:** Crop the history row and result details at readable size. Exclude sensitive payload contents and private identifiers. Record the exact navigation used in the capture notes.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-5.7-02.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-5.8-01

- [ ] **SS-5.8-01: Disk encryption and the BitLocker PIN requirement**

**Place:** Chapter 5.8, “Require a BitLocker startup PIN” ([4.91](manual/05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md#require-a-bitlocker-startup-pin), [4.90](website/versioned_docs/version-4.90/05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md#require-a-bitlocker-startup-pin)).

**Purpose:** Locate the shared encryption control and the additional Windows requirement.

**Prepare:** Open Controls > OS settings for a test fleet with disk encryption configured. Expand the Disk encryption card's Advanced options.

**Capture:** Show the encryption control and Require the end user to set a BitLocker PIN checkbox, with the selected fleet visible. Use an existing configuration or leave changes unsaved.

**Frame:** Crop the complete card with its helper text; no recovery credentials belong in this image.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-5.8-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-5.8-02

- [ ] **SS-5.8-02: Reported encryption status and the recovery-key action**

**Place:** Chapter 5.8, “Reveal, validate, and repair disk-recovery credentials safely” ([4.91](manual/05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md#reveal-validate-and-repair-disk-recovery-credentials-safely), [4.90](website/versioned_docs/version-4.90/05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md#reveal-validate-and-repair-disk-recovery-credentials-safely)).

**Purpose:** Show the operator entry point without exposing a recovery credential.

**Prepare:** Use a demo host with an escrowed credential and settled encryption status. Open host details.

**Capture:** Expand Actions with Show disk encryption key visible. Include the host's encryption status in a separate crop if it cannot be legibly shown with the menu. Stop before selecting the key-reveal action.

**Frame:** Capture only the menu and non-secret status. Do not open or photograph a revealed-key modal, including on Dogfood. The caption explains that authorized retrieval opens a credential dialog.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-5.8-02.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-5.8-03

- [ ] **SS-5.8-03: My Device instructions for creating a BitLocker PIN**

**Place:** Chapter 5.8, “Require a BitLocker startup PIN” ([4.91](manual/05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md#require-a-bitlocker-startup-pin), [4.90](website/versioned_docs/version-4.90/05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md#require-a-bitlocker-startup-pin)).

**Purpose:** Help support staff guide the user through the Windows-owned PIN creation step.

**Prepare:** Use a Windows demo host that requires a BitLocker PIN and has not yet set one. Open its My Device page and the Create PIN instructions.

**Capture:** Show the instruction dialog directing the user to Windows Manage BitLocker and the final refetch step. This is an instruction dialog, not a place to type a PIN.

**Frame:** Crop the dialog at readable size and exclude the full device-token URL. Do not include an entered PIN or recovery password.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-5.8-03.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-5.9-01

- [ ] **SS-5.9-01: A policy and its configured response**

**Place:** Chapter 5.9, “Design a transition-based or continuous closed loop” ([4.91](manual/05-manage-devices/5.9-automate-remediation-with-policies.md#design-a-transition-based-or-continuous-closed-loop), [4.90](website/versioned_docs/version-4.90/05-manage-devices/5.9-automate-remediation-with-policies.md#design-a-transition-based-or-continuous-closed-loop)).

**Purpose:** Connect a failing condition with the action Fleet is configured to take.

**Prepare:** Use a named test fleet with a harmless policy and a matching saved script or test software title. Keep the policy and response label scopes aligned.

**Capture:** Open the policy's automation configuration. Show the selected response and the continuous-automation setting where available, with the policy name and fleet context visible. A second small crop can show its matching policy scope.

**Frame:** Capture the genuine configuration controls; leave any demonstration change unsaved. Exclude webhook secrets and private integration destinations.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-5.9-01.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-5.9-02

- [ ] **SS-5.9-02: Automation runs and the result of one attempt**

**Place:** Chapter 5.9, “Where to look” ([4.91](manual/05-manage-devices/5.9-automate-remediation-with-policies.md#where-to-look), [4.90](website/versioned_docs/version-4.90/05-manage-devices/5.9-automate-remediation-with-policies.md#where-to-look)).

**Purpose:** Show how to connect a completed response to its policy, host, and diagnostic output.

**Prepare:** Use a test policy with completed harmless script or install responses on demo hosts. Use a pre-existing failure or a controlled test failure if comparison is needed.

**Capture:** Open the policy automation-runs view. Capture rows with host, time, and outcome, then open one attempt's details to show its real output. Keep repeated attempts separate rather than implying they are one run.

**Frame:** Use a table crop plus a readable detail crop. Redact sensitive script output before capture, or choose a script that prints only non-sensitive diagnostics.

**Edition:** 4.91; reuse for 4.90 only when the visible controls and wording match

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-5.9-02.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

### SS-5.9-03

- [ ] **SS-5.9-03: Patch when closed and an app-open skip**

**Place:** Chapter 5.9, “Patch a Fleet-maintained app only when it is closed” ([4.91](manual/05-manage-devices/5.9-automate-remediation-with-policies.md#patch-a-fleet-maintained-app-only-when-it-is-closed)).

**Purpose:** Explain the user-friendly patch option and the result administrators should expect while an app remains open.

**Prepare:** Use Fleet 4.91 and a maintained app in a named test fleet with its patch policy configured to patch when closed. A demo host should have an older version and the app open during an actual evaluation.

**Capture:** Capture the Add software or Deploy dialog showing the real patch timing choices and Patch when closed selected. As a separate frame, capture the policy automation history or host activity explaining an install skipped because the app was open.

**Frame:** Show each UI state separately. Use a disposable test host and a harmless app; if no real skip is available, capture the setting first and leave the outcome frame unchecked.

**Edition:** 4.91 only; patch when closed is absent from 4.90

**Privacy:** Use demo names and non-sensitive data; exclude tokens, passwords, keys, and personal identifiers.

**Filename:** `ss-5.9-03.png`

**Capture record:** Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.

## Maintaining this list

Edit the structured `SCREENSHOT:` or `SCREENSHOT-REUSE:` comments in the relevant chapters, keeping the edition-specific content accurate. Then run `python3 build/screenshot-checklist.py` from the repository. It preserves checked SS IDs and the single-paragraph Capture record notes in this file. Use `--check` to verify that the list matches the comments without changing it.
