---
title: "Subject index"
chapter: "Appendices and indexes"
section: "A.10"
sidebar_position: 10
verified_against: Fleet 4.91.0
verified_on: 2026-09-08
verified_source: "reference aid, not a behaviour claim. Each entry was checked to resolve to a section that defines or explains the term at fleet-v4.90.0; the terms themselves are grounded in the chapters they point at. Extended 2026-09-03 (round6 M16) with host display name template, name template and device name routes to 5.2's new 'Naming hosts from a template' section. Extended 2026-09-08 (overnight campaign step 3) with twenty-five entries, one per Fleet 4.91.0 feature, each pointing at the section that now teaches it and each term checked against fleet-v4.91.0 (35fc1c0244) rather than taken from the release notes: the entries name `last_enrolled_at`, `adobe_plugins` and its `Plugin (Adobe)` label, `mdm.allow_orbit_end_user_auth_bypass`, `--bypass-end-user-auth`, `$FLEET_HOST_VITAL_<id>`, `mdm.windows_automatic_enrollment.default_fleet`, `dep_device_error`, `$FLEET_VAR_*`, `hardware_marketing_name`, `host_activities_webhook`, the twenty-nine iOS and iPadOS vitals, the `linux` label platform, `minimum_version: latest` with `deadline_days`, nested Entra groups, `patch_when_closed`, `s3_software_installers_signed_url`, `released_from_ab`, `created_setup_experience_script`, `deleted_setup_experience_script`, `enable_software_inventory`, `token_invalid`, `user_mfa_requested`, `mdm_enrolled` and the Windows `_fleetadmin` account"
---

# Subject index

![Reference](../_assets/icons/reference-light.svg) Look up a concept, component, or named artifact here to find the chapter that explains it, from APNs and Redis to node keys and work profiles.

Start with the [capability index](a.1-capability-index.md) when you have a task to complete. Use this subject index when you have a name to look up. Links to the [glossary](a.6-glossary-and-release-compatibility.md) provide short definitions and explain renamed or easily confused terms.

“See X” directs you to the entry under another name, such as an expanded acronym or the current term for a renamed feature.


<!-- IMAGE-TODO: assets/a.10-index-reading-vignette.webp
     QUESTION: Can the alphabetical index get a visual resting point without obstructing lookup?
     PROMPT: ILLUSTRATION: A small horizontal Fleet Cloud City vignette for the opening of an
     alphabetical index. One pale floating reading platform holds a few orderly blank index cards
     and an open field guide; a modest glass walkway leads toward a second quiet platform,
     suggesting finding a route through information. Use one tiny swan silhouette near still water,
     generous whitespace, navy outlines and pale-blue surfaces. No letters, alphabet, labels,
     arrows, invented UI, charts, floating paragraphs, or faux hyperlinks. Keep it low and calm so
     the first alphabetical heading remains close to the introduction.
     TERMINOLOGY: Fleet is the company, product, or server. Host groups are lowercase
     fleet/fleets, including headings and labels. Do not call these groups teams. Preserve
     exact code/API identifiers. These instructions are not text to render.
     DESIGN: Fleet is software for managing computers; draw no vehicles. Use the established Cloud
     City illustration treatment consistently: #F9FAFC background, #192147 navy, #515774 slate, and
     #D3E8F3 / #E8F1F6 pale-blue surfaces. Keep large areas quiet and the composition balanced at
     720 px reading width. Use a shallow horizontal crop. No photorealistic elements mixed with flat
     artwork, product logo, watermark, rendered text, em-dashes, or technical claims. Do not imitate
     a diagram.
     NOTE: Proposed 2026-09-08; editorial brief, not technical re-verification. Atmosphere only.
     Keep all alphabetical entries, real links, see references, and noun-versus-outcome navigation
     instructions intact; do not interrupt letter groups with decoration. Keep current prose and
     this TODO until the actual image is reviewed. Then check alt text against the artwork and
     retain an accessible summary plus all required technical qualifications.
     CANDIDATE: ../../research/visual-reviews/appendices/assets/a.10-index-reading-vignette.webp
     Rendered and inspected for the overnight batch; awaiting final joint review.
-->

<!-- IMAGE PENDING. Install reviewed artwork, then activate the image line below.
![Blank index cards and an open field guide on a quiet floating reading platform.](assets/a.10-index-reading-vignette.webp)
-->

## A

- **ABM**, see Apple Business Manager.
- **"Added to Fleet"** (the hosts-list column, sortable from Fleet 4.91, and the matching Vitals field: it holds `last_enrolled_at`, the last time the host enrolled, rather than initial discovery): [4.1](../04-know-your-devices/4.1-understand-hosts-vitals-and-inventory.md#added-to-fleet-dates-the-last-enrollment-not-the-first).
- **Adobe plugins** (Creative Cloud CEP and UXP extensions, collected on macOS and Windows from Fleet 4.91 and listed with the software type "Plugin (Adobe)"): [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md#adobe-creative-cloud-plugins); vulnerability-scan exclusions are covered in [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md#a-sixth-emptiness-software-fleet-never-scans).
- **`allow_orbit_end_user_auth_bypass`** (`mdm.allow_orbit_end_user_auth_bypass`, the server setting that from Fleet 4.91 decides whether a Linux or Windows agent which does not complete end-user authentication may enroll into a fleet that requires it; on by default): [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md#end-user-authentication).
- **account lifecycle** (of a person's Fleet account), see user account.
- **account provisioning** (creating a Mac's local account and syncing its password with the identity provider through Platform SSO, Premium and macOS-only; the `fpsso` settings-search term): [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md#provision-and-sync-the-local-account-with-platform-sso). For Fleet-console account provisioning, see [2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md).
- **activity and audit log:** the record of what changed and who caused it is defined in [1.5](../01-foundations/1.5-audit-and-activity.md); where those records are delivered is [2.8](../02-administer-and-deploy-fleet/2.8-activity-audit-logs-and-log-delivery.md); reading them during an investigation is [8.12](../08-troubleshooting/8.12-audit-logs.md).
- **ADE** (Automated Device Enrollment): [3.2](../03-connect-devices/3.2-enroll-macos-devices.md) for Macs and [3.5](../03-connect-devices/3.5-enroll-ios-and-ipados-devices.md) for iPhones and iPads. DEP is the former name; the two are separated in the [glossary](a.6-glossary-and-release-compatibility.md).
- **AI assistant** (Claude, Cursor, and other MCP clients): connecting one to Fleet through the MCP server is [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md); the exact tools it can call are [A.11](a.11-mcp-tool-reference.md).
- **AMAPI** (Android Management API): the binding is [2.12](../02-administer-and-deploy-fleet/2.12-bind-android-enterprise.md); the one-policy-per-device model and its return path are [8.10](../08-troubleshooting/8.10-android-diagnostics.md).
- **Android Enterprise:** [2.12](../02-administer-and-deploy-fleet/2.12-bind-android-enterprise.md).
- **API-only user**, see service identity.
- **API token:** a person’s token is retrieved from their account page ([1.4](../01-foundations/1.4-identity-and-roles.md)); a service identity's token is minted when the API-only user is created ([2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md)).
- **APNs** (Apple Push Notification service): the push channel is [2.9](../02-administer-and-deploy-fleet/2.9-mdm-architecture-and-foundations.md); the certificate that authorises it is [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md).
- **Apple Business Manager** (ABM): [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md); the AB, ABM, and DEP token names are explained in the [glossary](a.6-glossary-and-release-compatibility.md).
- **Apps and Books**, see VPP.
- **async host processing:** the experimental `osquery_enable_async_host_processing` mode, which moves label, policy and last-seen writes through Redis, is [8.14](../08-troubleshooting/8.14-degradation.md); its use as a capacity lever is [2.2](../02-administer-and-deploy-fleet/2.2-self-hosting-architecture-and-capacity.md).
- **asset** (Apple DDM), see declaration asset.
- **Autopilot:** Microsoft's zero-touch Windows provisioning path is set up for enrollment in [3.3](../03-connect-devices/3.3-enroll-windows-devices.md) and diagnosed, including the external Autopilot dependency, in [8.9](../08-troubleshooting/8.9-windows-mdm-diagnostics.md).

## B

- **backup and restore** (of service state: MySQL, object storage, and the server private key; Redis is deliberately not backed up): [7.2](../07-operate-fleet/7.2-back-up-and-restore-service-state.md).
- **batch script** (running one saved script across many hosts at once): [5.3](../05-manage-devices/5.3-run-and-manage-scripts.md).
- **BitLocker:** [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md); the Windows escrow key it depends on is the WSTEP certificate, [2.11](../02-administer-and-deploy-fleet/2.11-configure-windows-management.md).
- **BitLocker startup PIN:** [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md).
- **`--bypass-end-user-auth`** (the `fleetctl package` flag, new in Fleet 4.91, that builds a fleetd installer which skips the end-user authentication prompt on Linux and Windows; the server still decides whether such a host may enroll): [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md#end-user-authentication).
- **bootstrap reports** (the standard saved reports `fleet-mcp -seed` creates), see seed mode.

## C

- **carve**, see file carving.
- **certificate authority** (CA): [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md).
- **CIS benchmarks** (the Premium policy library implementing the Center for Internet Security benchmarks, distributed as importable files, and revised for macOS in Fleet 4.91): [4.3](../04-know-your-devices/4.3-use-policies-for-compliance.md#the-cis-benchmark-policy-library).
- **certificate renewal:** the recurring operational calendar, and the difference between renewing a certificate and replacing key material, is [7.6](../07-operate-fleet/7.6-maintain-credentials-certificates-and-access.md); the four Apple credential renewal workflows are [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md).
- **certificate resend** (resending one certificate a profile issued, per host, separate from resending the profile): [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md#changing-resending-and-removing).
- **Chromebook**, see ChromeOS.
- **ChromeOS extension:** [3.7](../03-connect-devices/3.7-enroll-chromeos-devices.md).
- **custom host vital** (`$FLEET_HOST_VITAL_<id>`, a custom per-host value referenced by numeric identifier): defining one and setting a host's value is [4.1](../04-know-your-devices/4.1-understand-hosts-vitals-and-inventory.md); using one in a configuration profile, a declaration or Android managed app configuration is [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md#variables-and-secrets), in a host name template [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md#naming-hosts-from-a-template), and in a script or a software title's lifecycle scripts [5.3](../05-manage-devices/5.3-run-and-manage-scripts.md#secrets-and-per-host-values). Android and host name templates both arrived in Fleet 4.91.
- **conditional access:** the feature and its proxy-trust security boundary are [5.9](../05-manage-devices/5.9-automate-remediation-with-policies.md); [2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md) points to it from the identity-provider side.
- **configuration profile:** [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md).
- **`cron_stats`:** the table that records whether a scheduled job ran is in [8.6](../08-troubleshooting/8.6-server-state.md).
- **CSP** (Configuration Service Provider, the Windows-side component a SyncML command targets): [8.9](../08-troubleshooting/8.9-windows-mdm-diagnostics.md).

## D

- **data classification**, see data inventory and trust boundaries.
- **data egress** (what data leaves Fleet, and to whom): the map is [A.8](a.8-api-action-and-endpoint-reference.md#data-inventory-and-trust-boundaries); log delivery specifically is [2.8](../02-administer-and-deploy-fleet/2.8-activity-audit-logs-and-log-delivery.md).
- **data inventory and trust boundaries** (what data Fleet holds, where it lives, and what crosses a boundary, for a privacy review): [A.8](a.8-api-action-and-endpoint-reference.md#data-inventory-and-trust-boundaries).
- **DDM** (Declarative Device Management): [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md); diagnosing declaration delivery is [8.8](../08-troubleshooting/8.8-apple-mdm-diagnostics.md).
- **dead lettering:** defined in the [glossary](a.6-glossary-and-release-compatibility.md).
- **declaration asset** (the Premium Apple DDM `com.apple.asset.*` object a declaration references for large or binary content, with its own upload, uniqueness and delete rules, and Free-tier GitOps restrictions): [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md#declaration-assets); the device requests that follow are [8.8](../08-troubleshooting/8.8-apple-mdm-diagnostics.md#888-ddm-declarations).
- **declarative settings**, see DDM.
- **default fleet (Windows)** (the fleet a user-driven Windows MDM enrollment is assigned to, before the Autopilot Enrollment Status Page runs; Premium, new in Fleet 4.91): [2.11](../02-administer-and-deploy-fleet/2.11-configure-windows-management.md#where-automatically-enrolled-windows-hosts-land). The Apple per-platform equivalent is [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md).
- **`dep_device_error`** (the human-readable reason a host's Apple Business device lookup failed, returned from Fleet 4.91 on `GET /hosts/:id/dep_assignment`): [8.8](../08-troubleshooting/8.8-apple-mdm-diagnostics.md#apple-lookup-errors-in-fleet-491).
- **decommissioning**, see retirement.
- **device channel:** the default declaration and profile delivery target, [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md); the same section explains user-channel delivery.
- **device name**, see host display name template.
- **DEP** (Device Enrollment Program), see ADE. DEP is the deprecated name, mapped to ADE in the [glossary](a.6-glossary-and-release-compatibility.md).
- **DigiCert:** one of the six certificate authority types, [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md).
- **disk encryption:** [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md).
- **drift** (a live setting no longer matching what GitOps declares, together with the out-of-band change that caused it and the partial apply that can leave it behind): resolving it is [6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md#resolve-drift-partial-applies-and-disagreement).

## E

- **egress destinations** (the outbound map for a firewall review): [2.2](../02-administer-and-deploy-fleet/2.2-self-hosting-architecture-and-capacity.md).
- **endpoint allowlist** (the Premium restriction narrowing an API-only user's routes below what its role allows): [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md); the route set per tool is [A.11](a.11-mcp-tool-reference.md).
- **endpoint catalogue** (the Premium read that returns every method-and-path pair an allowlist will accept): retrieving it is [A.8](a.8-api-action-and-endpoint-reference.md#retrieving-the-endpoint-catalog); what it constrains is the endpoint allowlist above.
- **enroll secret:** [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md).
- **enrollment profile:** [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md); the macOS route that uses it is [3.2](../03-connect-devices/3.2-enroll-macos-devices.md).
- **Entra** (Microsoft Entra ID): as an identity provider it is [2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md); its part in Windows automatic enrollment is [3.3](../03-connect-devices/3.3-enroll-windows-devices.md).
- **EPSS** (Exploit Prediction Scoring System, the exploitation-probability score Fleet Premium attaches to a vulnerability): [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md).
- **ESP** (Enrollment Status Page, Windows): holding and releasing a device at it is [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md).
- **EST** (Enrollment over Secure Transport): one of the six certificate authority types, [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md).

## F

- **file carving:** defined in the [glossary](a.6-glossary-and-release-compatibility.md); its use for introspection is covered in [8.7](../08-troubleshooting/8.7-live-query-introspection.md) and storage and limits in [8.14](../08-troubleshooting/8.14-degradation.md).
- **FileVault:** [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md).
- **first administrator**, see first-run setup.
- **first-run setup** (creating the first administrator on a new server, before anyone can sign in; the setup screen, and what "initialize the server" means): [2.2](../02-administer-and-deploy-fleet/2.2-self-hosting-architecture-and-capacity.md#complete-first-run-setup).
- **fleet** (the scoping construct, renamed from team): [1.3](../01-foundations/1.3-hosts-fleets-labels.md); the rename is recorded in the [glossary](a.6-glossary-and-release-compatibility.md).
- **Fleet Desktop:** introduced as one of the host-side components in [1.2](../01-foundations/1.2-how-fleet-reaches-a-device.md); its end-user features are covered in [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md).
- **Fleet variables** (`$FLEET_VAR_*`, the built-in per-host substitutions Fleet resolves as it delivers): in configuration profiles they are [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md#variables-and-secrets); the eight supported in scripts and in a software title's install, post-install and uninstall scripts, Premium and new in Fleet 4.91, are [5.3](../05-manage-devices/5.3-run-and-manage-scripts.md#secrets-and-per-host-values).
- **Fleet-maintained apps** (FMA): the curated catalogue is defined in [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md); installing one is [5.4](../05-manage-devices/5.4-manage-software-and-applications.md).
- **fleetd:** the host-side bundle is defined in [1.2](../01-foundations/1.2-how-fleet-reaches-a-device.md); keeping it current is [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md).

## G

- **GitOps:** [6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md).
- **GitOps mode** (locking the managed parts of the interface to read-only, `gitops_mode_enabled`, Premium): [2.7](../02-administer-and-deploy-fleet/2.7-organization-and-server-settings.md).
- **go-live decision** (approval to begin managing production hosts), see production readiness.

## H

- **handoff and handover** (handing a running deployment to the team that will operate it), see production readiness.
- **healthz** (the `/healthz` endpoint): what it checks and returns is [8.14](../08-troubleshooting/8.14-degradation.md); reading its failure in the server log is [8.3](../08-troubleshooting/8.3-server-logs.md).
- **Helm** (the Kubernetes chart): [2.4](../02-administer-and-deploy-fleet/2.4-deploy-with-containers-or-virtual-machines.md).
- **hardware marketing name** (`hardware_marketing_name`, the human-readable Apple model name Fleet 4.91 and later shows in place of the raw identifier it still stores): [4.1](../04-know-your-devices/4.1-understand-hosts-vitals-and-inventory.md#identity-operating-system-and-network).
- **host activities webhook** (the Premium per-fleet activity webhook, new in Fleet 4.91, which fires only for activities linked to that fleet's hosts): its behavior is described in [6.5](../06-automate-fleet/6.5-integrations-webhooks-and-external-workflows.md#the-activity-webhook-global-or-per-fleet); comparison with the organization-wide webhook is in [1.5](../01-foundations/1.5-audit-and-activity.md).
- **host display name template** (the per-scope, per-host template that sets the display name an Apple device reports, Premium): [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md#naming-hosts-from-a-template).
- **host identity certificate:** [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md); which platforms support it is a row in the [platform capability matrix](a.2-platform-capability-matrix.md).
- **host vitals:** [4.1](../04-know-your-devices/4.1-understand-hosts-vitals-and-inventory.md).
- **Hydrant:** one of the six certificate authority types, [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md).

## I

- **idempotency** (an action safe to repeat): defined in [a.6](a.6-glossary-and-release-compatibility.md#terms-the-manual-uses-across-chapters); designing repeatable automation is covered in [6.1](../06-automate-fleet/6.1-automation-design-and-change-control.md).
- **iOS and iPadOS device vitals** (the 29 fields a company-owned iPhone or iPad reports from Fleet 4.91, on the device-information request Fleet already makes, behind the host's **View all** button; a personally owned device is not asked for 26 of them): [4.1](../04-know-your-devices/4.1-understand-hosts-vitals-and-inventory.md#what-an-iphone-or-ipad-reports-and-what-a-personally-owned-one-does-not).
- **initialize the server**, see first-run setup.
- **IRSA** (IAM Roles for Service Accounts): defined in [a.6](a.6-glossary-and-release-compatibility.md#terms-the-manual-uses-across-chapters); using it with Fleet's S3 client on AWS is [2.3](../02-administer-and-deploy-fleet/2.3-deploy-on-aws-or-gcp.md).

## J

- **JSON-RPC** (the request and response protocol MCP speaks): defined in [a.6](a.6-glossary-and-release-compatibility.md#terms-the-manual-uses-across-chapters); smoke-testing the Fleet MCP server over it is [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md).

## L

- **label:** [1.3](../01-foundations/1.3-hosts-fleets-labels.md).
- **label platform** (the optional platform a dynamic label's query is restricted to, fixed when the label is created; `linux`, which matches any distribution, was added in Fleet 4.91): [1.3](../01-foundations/1.3-hosts-fleets-labels.md#a-dynamic-label-can-be-restricted-to-a-platform).
- **`latest`** (as a `minimum_version`, with `deadline_days`, which keeps macOS, iOS and iPadOS hosts on the newest release their own hardware can run; Premium, new in Fleet 4.91): [5.6](../05-manage-devices/5.6-control-operating-system-updates.md#enforce-the-latest-version-with-a-rolling-deadline).
- **LAPS and the managed local administrator account:** [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md); the Windows implementation, added in Fleet 4.91, is [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md#the-windows-managed-local-admin-account).
- **licence** (Fleet Premium, licence key, and licence expiry): [7.6](../07-operate-fleet/7.6-maintain-credentials-certificates-and-access.md); choosing a licence tier is [2.1](../02-administer-and-deploy-fleet/2.1-administration-model-and-deployment-choices.md).
- **license**, see licence.
- **live query**, see report.
- **local account** (a Mac's own user account that a person logs in with, provisioned and password-synced through Platform SSO; distinct from the managed local administrator account): [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md#provision-and-sync-the-local-account-with-platform-sso).
- **LocURI**: the CSP node path a SyncML command targets, [8.9](../08-troubleshooting/8.9-windows-mdm-diagnostics.md).
- **LUKS** (Linux disk encryption): escrow is [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md).

## M

- **managed local account**, see LAPS and the managed local administrator account.
- **`mdm_enrolled`** (the enrollment activity, which from Fleet 4.91 carries `host_id` and `host_serial` for Apple enrollments and appears on the host's own timeline): [8.12](../08-troubleshooting/8.12-audit-logs.md#8122-the-table).
- **MCP** (Model Context Protocol) and the **Fleet MCP server**: connecting an AI assistant to Fleet is [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md); the fixed twenty-tool list it exposes is [A.11](a.11-mcp-tool-reference.md); the term is defined in the [glossary](a.6-glossary-and-release-compatibility.md).
- **MDM enrollment:** the model is [2.9](../02-administer-and-deploy-fleet/2.9-mdm-architecture-and-foundations.md); the status values are explained in the [glossary](a.6-glossary-and-release-compatibility.md).
- **MFA** (multi-factor authentication), see two-factor authentication.
- **My Device page:** designed in [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md); the channel behind it is [1.2](../01-foundations/1.2-how-fleet-reaches-a-device.md).
- **MySQL:** its role as Fleet's authoritative store is [1.6](../01-foundations/1.6-the-fleet-server.md).

## N

- **name template** (host display name), see host display name template.
- **nested groups** (a group provisioned as a member of another group in Entra; from Fleet 4.91 Fleet resolves a user's effective membership by walking upward, so a label on a parent group matches): [2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md#connect-scim).
- **NDES:** the Microsoft SCEP proxy, [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md).
- **node key:** [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md); also defined in the [glossary](a.6-glossary-and-release-compatibility.md).
- **Nudge:** [5.6](../05-manage-devices/5.6-control-operating-system-updates.md).

## O

- **object storage** (S3 and compatible): its place in the server's stores is [1.6](../01-foundations/1.6-the-fleet-server.md); provider specifics are [2.3](../02-administer-and-deploy-fleet/2.3-deploy-on-aws-or-gcp.md).
- **Observer+** (`observer_plus`, Observer with the ability to run any report, Premium): choosing between Fleet's roles is [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md).
- **OMA-DM:** the device-management protocol Windows speaks (SyncML is its XML wire format); diagnosed in [8.9](../08-troubleshooting/8.9-windows-mdm-diagnostics.md), introduced as the fifth reach-a-device channel in [1.2](../01-foundations/1.2-how-fleet-reaches-a-device.md).
- **OOBE** (out-of-box experience): the Windows and macOS setup window a device can be held in is [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md).
- **OS updates** (operating system update enforcement and deferral): [5.6](../05-manage-devices/5.6-control-operating-system-updates.md).
- **Orbit:** introduced in [1.2](../01-foundations/1.2-how-fleet-reaches-a-device.md) as the bundle's supervisor; managed in [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md).
- **osquery:** introduced in [1.2](../01-foundations/1.2-how-fleet-reaches-a-device.md); query design and performance are [4.6](../04-know-your-devices/4.6-advanced-osquery-queries-and-tables.md).
- **osquery-perf** (the load-simulation tool): [7.5](../07-operate-fleet/7.5-maintain-capacity-and-availability.md).

## P

- **pack:** the legacy 2017 query pack is covered in [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) and defined in the [glossary](a.6-glossary-and-release-compatibility.md).
- **patch when closed** (the patch-policy install option, new in Fleet 4.91, that installs only while the app is not running on the host, and which requires continuous automations): [5.9](../05-manage-devices/5.9-automate-remediation-with-policies.md#patch-a-fleet-maintained-app-only-when-it-is-closed).
- **presigned URL** (`s3_software_installers_signed_url`, new in Fleet 4.91, which serves software installer, in-house app and bootstrap package downloads straight from Google Cloud Storage instead of through the Fleet server): [2.3](../02-administer-and-deploy-fleet/2.3-deploy-on-aws-or-gcp.md#object-storage-on-gcp-works-despite-what-the-architecture-page-says).
- **password sync** (keeping a Mac's local-account password in step with the identity provider, through Platform SSO in Password mode, Premium and macOS-only): [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md#provision-and-sync-the-local-account-with-platform-sso).
- **`PayloadScope`** (the declaration key choosing System or User channel delivery): [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md).
- **personal data**, see data inventory and trust boundaries.
- **Platform SSO:** the device registration token and its delivery are [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md); provisioning and password-syncing a Mac's local account through Platform SSO is [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md#provision-and-sync-the-local-account-with-platform-sso).
- **policy:** [4.3](../04-know-your-devices/4.3-use-policies-for-compliance.md).
- **pprof:** the profiling set is [8.5](../08-troubleshooting/8.5-fleetctl-debug.md); the term is defined in the [glossary](a.6-glossary-and-release-compatibility.md).
- **Preview** (`fleetctl preview`, alias `sandbox`): the local evaluation environment is [0.3](../00-Introduction/0.3-how-to-use-this-manual.md#try-fleet-without-deploying-anything); command behavior is covered in [a.7](a.7-fleetctl-command-reference.md).
- **privacy review**, see data inventory and trust boundaries.
- **production readiness** (the go-live checklist and handover before a deployment carries real hosts, including the go-live decision itself): [7.7](../07-operate-fleet/7.7-production-readiness-checklist-and-handoff.md#the-go-live-decision); the pilot that turns its criteria into observations is [2.1](../02-administer-and-deploy-fleet/2.1-administration-model-and-deployment-choices.md).
- **profile**, see configuration profile.
- **Prometheus:** Fleet's metrics naming, and which suffixed series to query, is [7.4](../07-operate-fleet/7.4-observe-progress-and-service-health.md).

## Q

- **query**, see report.

## R

- **readiness** (production go-live), see production readiness.
- **recovery key escrow:** [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md).
- **Recovery Lock** (the Apple silicon firmware password): [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md).
- **release from Apple Business** (the Premium, irreversible action that removes a device from your Apple Business organization; separate from unenrollment, and added in Fleet 4.91): [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md#releasing-a-device-from-apple-business); what a released device's lookup reports afterwards is [8.8](../08-troubleshooting/8.8-apple-mdm-diagnostics.md#apple-lookup-errors-in-fleet-491).
- **Redis:** storage and recovery implications, is [1.6](../01-foundations/1.6-the-fleet-server.md).
- **report and live report** (renamed from query and live query in 4.82.0): [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md); a live report used as an introspection tool is [8.7](../08-troubleshooting/8.7-live-query-introspection.md). The rename is in the [glossary](a.6-glossary-and-release-compatibility.md).
- **REST API:** using it is [6.3](../06-automate-fleet/6.3-use-the-fleet-rest-api.md); the indexed route and endpoint reference is [A.8](a.8-api-action-and-endpoint-reference.md).
- **restore**, see backup and restore.
- **retention** (how long Fleet keeps each class of data): routed by class from [A.8](a.8-api-action-and-endpoint-reference.md#data-inventory-and-trust-boundaries).
- **retirement** (decommissioning a Fleet deployment): [7.8](../07-operate-fleet/7.8-retire-a-fleet-deployment.md).

## S

- **SAML**, see SSO.
- **SCEP:** [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md); glossed in the [glossary](a.6-glossary-and-release-compatibility.md).
- **SCIM:** [2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md).
- **scheduled query:** [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md); writing efficient ones is [4.6](../04-know-your-devices/4.6-advanced-osquery-queries-and-tables.md).
- **second factor**, see two-factor authentication.
- **secret variables:** [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md); their use in version-controlled configuration is [6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md).
- **seed mode** (the `fleet-mcp -seed` flag that creates the four standard saved reports against Fleet, then exits without serving): [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md).
- **self-service:** [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md).
- **server logs:** interpreting Fleet’s process logs is [8.3](../08-troubleshooting/8.3-server-logs.md); the full set of log surfaces (agent, server, and MDM protocol) is [8.2](../08-troubleshooting/8.2-log-surfaces.md); delivering them onward is [2.8](../02-administer-and-deploy-fleet/2.8-activity-audit-logs-and-log-delivery.md).
- **server URL** (the Fleet server's own address, `server_url`): [2.7](../02-administer-and-deploy-fleet/2.7-organization-and-server-settings.md).
- **service identity** (a non-human, API-only user for automation): [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md); scoping its token to one fleet or a named list of endpoints is [1.4](../01-foundations/1.4-identity-and-roles.md).
- **setup assistant:** [3.2](../03-connect-devices/3.2-enroll-macos-devices.md); the wider setup experience is [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md).
- **setup experience script** (the Premium script that runs during setup; from Fleet 4.91 adding, replacing or removing it is audited as `created_setup_experience_script` and `deleted_setup_experience_script`): running one is [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md); the audit record is [8.12](../08-troubleshooting/8.12-audit-logs.md#8124-activity-types-the-categories).
- **setup screen** (the first-run screen that creates the first administrator), see first-run setup.
- **SIEM** (security information and event management): sending Fleet's activity and audit logs to one is [2.8](../02-administer-and-deploy-fleet/2.8-activity-audit-logs-and-log-delivery.md).
- **Smallstep:** one of the six certificate authority types, [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md).
- **software installer:** [5.4](../05-manage-devices/5.4-manage-software-and-applications.md).
- **software inventory** (what Fleet collects about installed software, and the per-fleet switch that turns it on, settable from Fleet 4.91 over `PATCH /api/v1/fleet/fleets/{id}` as well as through GitOps): [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md#turning-software-inventory-on-and-what-off-looks-like).
- **SSE** (Server-Sent Events, one of the two MCP transports): [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md).
- **SSO and SAML:** [2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md).
- **standard saved reports** (the four global reports `fleet-mcp -seed` bootstraps: macOS admin users, Windows update failures, Linux running containers, universal OS version), see seed mode.
- **stdio** (the standard-input/output MCP transport for local clients like Claude Desktop): [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md).
- **SyncML:** the Windows MDM wire format is diagnosed in [8.9](../08-troubleshooting/8.9-windows-mdm-diagnostics.md).
- **sysdiagnose** (Apple's on-demand diagnostic archive): pulling one from iOS/iPadOS is [8.2](../08-troubleshooting/8.2-log-surfaces.md); Apple MDM diagnostics generally are [8.8](../08-troubleshooting/8.8-apple-mdm-diagnostics.md).

## T

- **team**, see fleet.
- **Technician** (a Premium role that can run scripts, install and uninstall software, and read host data including recovery credentials): choosing between Fleet's roles is [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md).
- **Terraform:** the AWS reference architecture module is [2.3](../02-administer-and-deploy-fleet/2.3-deploy-on-aws-or-gcp.md).
- **TLS:** the certificate that protects communication with the service, and the server private key it depends on, is [1.6](../01-foundations/1.6-the-fleet-server.md); planning the DNS name and certificate as server settings is [2.7](../02-administer-and-deploy-fleet/2.7-organization-and-server-settings.md).
- **`token_invalid`** (the Apple Business token flag, new in Fleet 4.91, meaning Apple rejected the token or reported its signature invalid; false alone does not confirm token health): [8.8](../08-troubleshooting/8.8-apple-mdm-diagnostics.md#apple-lookup-errors-in-fleet-491).
- **trust boundary**, see data inventory and trust boundaries.
- **TUF** (The Update Framework): defined in [a.6](a.6-glossary-and-release-compatibility.md#terms-the-manual-uses-across-chapters); the update repository is [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md); confirming what a host is running is [8.4](../08-troubleshooting/8.4-host-side-investigation.md).
- **two-factor authentication** (Fleet's own email-delivered second factor, Premium): enabling it per account is [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md); its activity-record coverage is [1.5](../01-foundations/1.5-audit-and-activity.md).

## U

- **user account** (creating or inviting a person, editing their role and scope, forcing a password reset, ending their sessions, deleting them): [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md).
- **`user_mfa_requested`** (the activity, new in Fleet 4.91, written when a valid password is submitted for an account with a second factor and the verification email is sent; it confirms valid-password submission; completed sign-in needs separate evidence): [8.12](../08-troubleshooting/8.12-audit-logs.md#8124-activity-types-the-categories); the recording gap it partly closes is [1.5](../01-foundations/1.5-audit-and-activity.md).
- **user channel** (the macOS-only, sign-in-gated declaration delivery target; exists only for hosts that automatically enrolled): [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md).

## V

- **VPP** (Volume Purchasing, Apple's Apps and Books): [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md); defined in the [glossary](a.6-glossary-and-release-compatibility.md).
- **vulnerabilities** (CVEs): how software inventory is matched to known vulnerabilities is [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md).
- **`vulnerability-data-stream`** (staging offline vulnerability feeds): [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md).

## W

- **webhook:** [6.5](../06-automate-fleet/6.5-integrations-webhooks-and-external-workflows.md).
- **wipe and lock:** [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md).
- **work profile:** [3.6](../03-connect-devices/3.6-enroll-android-devices.md); the enterprise binding behind it is [2.12](../02-administer-and-deploy-fleet/2.12-bind-android-enterprise.md).
- **Windows managed local admin account** (the `_fleetadmin` administrator fleetd creates, hides and escrows on a Windows host from Fleet 4.91; Premium, revealed the same way as the macOS account and never rotated): [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md#the-windows-managed-local-admin-account).
- **WSTEP:** the Windows enrollment certificate, which also serves as Fleet's Windows disk-encryption escrow key, is [2.11](../02-administer-and-deploy-fleet/2.11-configure-windows-management.md); Windows MDM diagnostics are [8.9](../08-troubleshooting/8.9-windows-mdm-diagnostics.md).
