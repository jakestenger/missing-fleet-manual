---
title: "Subject index"
chapter: "Appendices and indexes"
section: "A.10"
sidebar_position: 10
verified_against: Fleet 4.90.0
verified_on: 2026-09-03
verified_source: "reference aid, not a behaviour claim. Each entry was checked to resolve to a section that defines or explains the term at fleet-v4.90.0; the terms themselves are grounded in the chapters they point at. Extended 2026-09-03 (round6 M16) with host display name template, name template and device name routes to 5.2's new 'Naming hosts from a template' section"
---

# Subject index

An A-Z of the concepts, components, and named artifacts a reader looks up by name: APNs, Redis, the node key, a work profile. Each entry points at the chapter that defines or explains the thing, not at every chapter that mentions it.

This is the noun counterpart to the [capability index](a.1-capability-index.md), which starts from an outcome you want, a verb. Start here when you have met a word and want to know what it is; start there when you know the job and want the chapter that does it. Where a term also carries a short definition in the [glossary](a.6-glossary-and-release-compatibility.md), that is noted, because the glossary is where a renamed or easily-confused term is pinned down.

A cross-reference of the form "see X" means the book files the concept under X, because Fleet renamed it or because one name is the expansion of another.

## A

- **ABM**, see Apple Business Manager.
- **account lifecycle** (of a person's Fleet account), see user account.
- **account provisioning** (creating a Mac's local account and syncing its password with the identity provider through Platform SSO, Premium and macOS-only; the `fpsso` settings-search term): [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md#provision-and-sync-the-local-account-with-platform-sso). This is not the Fleet-console account [2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md) provisions.
- **activity and audit log:** the record of what changed and who caused it is defined in [1.5](../01-foundations/1.5-audit-and-activity.md); where those records are delivered is [2.8](../02-administer-and-deploy-fleet/2.8-activity-audit-logs-and-log-delivery.md); reading them during an investigation is [8.12](../08-troubleshooting/8.12-audit-logs.md).
- **ADE** (Automated Device Enrollment): [3.2](../03-connect-devices/3.2-enroll-macos-devices.md) for Macs and [3.5](../03-connect-devices/3.5-enroll-ios-and-ipados-devices.md) for iPhones and iPads. DEP is the former name; the two are separated in the [glossary](a.6-glossary-and-release-compatibility.md).
- **AI assistant** (Claude, Cursor, and other MCP clients): connecting one to Fleet through the MCP server is [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md); the exact tools it can call are [A.11](a.11-mcp-tool-reference.md).
- **AMAPI** (Android Management API): the binding is [2.12](../02-administer-and-deploy-fleet/2.12-bind-android-enterprise.md); the one-policy-per-device model and its return path are [8.10](../08-troubleshooting/8.10-android-diagnostics.md).
- **Android Enterprise:** [2.12](../02-administer-and-deploy-fleet/2.12-bind-android-enterprise.md).
- **API-only user**, see service identity.
- **API token:** creating one belongs to the identity that holds it: a person's own token is retrieved from their account page ([1.4](../01-foundations/1.4-identity-and-roles.md)); a service identity's token is minted when the API-only user is created ([2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md)).
- **APNs** (Apple Push Notification service): the push channel is [2.9](../02-administer-and-deploy-fleet/2.9-mdm-architecture-and-foundations.md); the certificate that authorises it is [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md).
- **Apple Business Manager** (ABM): [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md); the AB, ABM, and DEP token names are pinned down in the [glossary](a.6-glossary-and-release-compatibility.md).
- **Apps and Books**, see VPP.
- **async host processing:** the experimental `osquery_enable_async_host_processing` mode, which moves label, policy and last-seen writes through Redis, is [8.14](../08-troubleshooting/8.14-degradation.md); its use as a capacity lever is [2.2](../02-administer-and-deploy-fleet/2.2-self-hosting-architecture-and-capacity.md).
- **asset** (Apple DDM), see declaration asset.
- **Autopilot:** Microsoft's zero-touch Windows provisioning path is set up for enrollment in [3.3](../03-connect-devices/3.3-enroll-windows-devices.md) and diagnosed, including why Fleet never talks to it, in [8.9](../08-troubleshooting/8.9-windows-mdm-diagnostics.md).

## B

- **backup and restore** (of service state: MySQL, Redis, object storage, and the server private key): [7.2](../07-operate-fleet/7.2-back-up-and-restore-service-state.md).
- **batch script** (running one saved script across many hosts at once): [5.3](../05-manage-devices/5.3-run-and-manage-scripts.md).
- **BitLocker:** [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md); the Windows escrow key it depends on is the WSTEP certificate, [2.11](../02-administer-and-deploy-fleet/2.11-configure-windows-management.md).
- **BitLocker startup PIN:** [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md).
- **bootstrap reports** (the standard saved reports `fleet-mcp -seed` creates), see seed mode.

## C

- **carve**, see file carving.
- **certificate authority** (CA): [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md).
- **certificate renewal:** the recurring operational calendar, and the difference between renewing a certificate and replacing key material, is [7.6](../07-operate-fleet/7.6-maintain-credentials-certificates-and-access.md); the four Apple credentials with their own renewal stories are [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md).
- **Chromebook**, see ChromeOS.
- **ChromeOS extension:** [3.7](../03-connect-devices/3.7-enroll-chromeos-devices.md).
- **conditional access:** the policy-driven side is [5.9](../05-manage-devices/5.9-automate-remediation-with-policies.md); the identity-provider side is [2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md).
- **configuration profile:** [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md).
- **`cron_stats`:** the table that records whether a scheduled job ran is in [8.6](../08-troubleshooting/8.6-server-state.md).
- **CSP** (Configuration Service Provider, the Windows-side component a SyncML command targets): [8.9](../08-troubleshooting/8.9-windows-mdm-diagnostics.md).

## D

- **data classification**, see data inventory and trust boundaries.
- **data egress** (what data leaves Fleet, and to whom): the map is [A.8](a.8-api-action-and-endpoint-reference.md#data-inventory-and-trust-boundaries); log delivery specifically is [2.8](../02-administer-and-deploy-fleet/2.8-activity-audit-logs-and-log-delivery.md).
- **data inventory and trust boundaries** (what data Fleet holds, where it lives, and what crosses a boundary, for a privacy review): [A.8](a.8-api-action-and-endpoint-reference.md#data-inventory-and-trust-boundaries).
- **DDM** (Declarative Device Management): [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md); diagnosing declaration delivery is [8.8](../08-troubleshooting/8.8-apple-mdm-diagnostics.md).
- **dead lettering:** defined in the [glossary](a.6-glossary-and-release-compatibility.md).
- **declaration asset** (the Premium Apple DDM `com.apple.asset.*` object a declaration references for large or binary content, with its own upload, uniqueness and delete rules, and a Fleet-Free GitOps licence trap): [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md#declaration-assets); the device requests that follow are [8.8](../08-troubleshooting/8.8-apple-mdm-diagnostics.md#888-ddm-declarations).
- **declarative settings**, see DDM.
- **decommissioning**, see retirement.
- **device channel:** the default declaration and profile delivery target, [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md); contrasted with the user channel there.
- **device name**, see host display name template.
- **DEP** (Device Enrollment Program), see ADE. DEP is the deprecated name, kept apart from ADE in the [glossary](a.6-glossary-and-release-compatibility.md).
- **DigiCert:** one of the six certificate authority types, [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md).
- **disk encryption:** [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md).

## E

- **egress destinations** (the outbound map for a firewall review): [2.2](../02-administer-and-deploy-fleet/2.2-self-hosting-architecture-and-capacity.md).
- **endpoint allowlist** (the Premium restriction narrowing an API-only user's routes below what its role allows): [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md); the route set per tool is [A.11](a.11-mcp-tool-reference.md).
- **enroll secret:** [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md).
- **enrollment profile:** [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md); the macOS route that uses it is [3.2](../03-connect-devices/3.2-enroll-macos-devices.md).
- **Entra** (Microsoft Entra ID): as an identity provider it is [2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md); its part in Windows automatic enrollment is [3.3](../03-connect-devices/3.3-enroll-windows-devices.md).
- **EPSS** (Exploit Prediction Scoring System, the exploitation-probability score Fleet Premium attaches to a vulnerability): [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md).
- **ESP** (Enrollment Status Page, Windows): holding and releasing a device at it is [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md).
- **EST** (Enrollment over Secure Transport): one of the six certificate authority types, [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md).

## F

- **file carving:** defined in the [glossary](a.6-glossary-and-release-compatibility.md); it surfaces as an introspection tool in [8.7](../08-troubleshooting/8.7-live-query-introspection.md) and as a storage and limits question in [8.14](../08-troubleshooting/8.14-degradation.md).
- **FileVault:** [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md).
- **first administrator**, see first-run setup.
- **first-run setup** (creating the first administrator on a new server, before anyone can sign in; the setup screen, and what "initialize the server" means): [2.2](../02-administer-and-deploy-fleet/2.2-self-hosting-architecture-and-capacity.md#complete-first-run-setup).
- **fleet** (the scoping construct, renamed from team): [1.3](../01-foundations/1.3-hosts-fleets-labels.md); the rename is recorded in the [glossary](a.6-glossary-and-release-compatibility.md).
- **Fleet Desktop:** introduced as one of the host-side components in [1.2](../01-foundations/1.2-how-fleet-reaches-a-device.md); its end-user surface is designed in [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md).
- **Fleet-maintained apps** (FMA): the curated catalogue is defined in [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md); installing one is [5.4](../05-manage-devices/5.4-manage-software-and-applications.md).
- **fleetd:** the host-side bundle is defined in [1.2](../01-foundations/1.2-how-fleet-reaches-a-device.md); keeping it current is [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md).

## G

- **GitOps:** [6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md).
- **GitOps mode** (locking the managed parts of the interface to read-only, `gitops_mode_enabled`, Premium): [2.7](../02-administer-and-deploy-fleet/2.7-organization-and-server-settings.md).
- **go-live decision** (the readiness gate a deployment clears before it carries real hosts), see production readiness.

## H

- **handoff and handover** (handing a running deployment to the team that will operate it), see production readiness.
- **healthz** (the `/healthz` endpoint): what it checks and returns is [8.14](../08-troubleshooting/8.14-degradation.md); reading its failure in the server log is [8.3](../08-troubleshooting/8.3-server-logs.md).
- **Helm** (the Kubernetes chart): [2.4](../02-administer-and-deploy-fleet/2.4-deploy-with-containers-or-virtual-machines.md).
- **host display name template** (the per-scope, per-host template that sets the display name an Apple device reports, Premium): [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md#naming-hosts-from-a-template).
- **host identity certificate:** [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md); which platforms support it is a row in the [platform capability matrix](a.2-platform-capability-matrix.md).
- **host vitals:** [4.1](../04-know-your-devices/4.1-understand-hosts-vitals-and-inventory.md).
- **Hydrant:** one of the six certificate authority types, [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md).

## I

- **initialize the server**, see first-run setup.

## L

- **label:** [1.3](../01-foundations/1.3-hosts-fleets-labels.md).
- **LAPS and the managed local administrator account:** [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md).
- **licence** (Fleet Premium, licence key, and licence expiry): [7.6](../07-operate-fleet/7.6-maintain-credentials-certificates-and-access.md); choosing a licence tier is [2.1](../02-administer-and-deploy-fleet/2.1-administration-model-and-deployment-choices.md).
- **live query**, see report.
- **local account** (a Mac's own user account that a person logs in with, provisioned and password-synced through Platform SSO; distinct from the managed local administrator account): [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md#provision-and-sync-the-local-account-with-platform-sso).
- **LocURI**: the CSP node path a SyncML command targets, [8.9](../08-troubleshooting/8.9-windows-mdm-diagnostics.md).
- **LUKS** (Linux disk encryption): escrow is [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md).

## M

- **managed local account**, see LAPS and the managed local administrator account.
- **MCP** (Model Context Protocol) and the **Fleet MCP server**: connecting an AI assistant to Fleet is [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md); the fixed twenty-tool list it exposes is [A.11](a.11-mcp-tool-reference.md); the term is glossed in the [glossary](a.6-glossary-and-release-compatibility.md).
- **MDM enrollment:** the model is [2.9](../02-administer-and-deploy-fleet/2.9-mdm-architecture-and-foundations.md); the status values are pinned down in the [glossary](a.6-glossary-and-release-compatibility.md).
- **MFA** (multi-factor authentication), see two-factor authentication.
- **My Device page:** designed in [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md); the channel behind it is [1.2](../01-foundations/1.2-how-fleet-reaches-a-device.md).
- **MySQL:** its role as Fleet's authoritative store is [1.6](../01-foundations/1.6-the-fleet-server.md).

## N

- **name template** (host display name), see host display name template.
- **NDES:** the Microsoft SCEP proxy, [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md).
- **node key:** [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md); also glossed in the [glossary](a.6-glossary-and-release-compatibility.md).
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

- **pack:** the legacy 2017 query pack is covered in [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) and glossed in the [glossary](a.6-glossary-and-release-compatibility.md).
- **password sync** (keeping a Mac's local-account password in step with the identity provider, through Platform SSO in Password mode, Premium and macOS-only): [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md#provision-and-sync-the-local-account-with-platform-sso).
- **`PayloadScope`** (the declaration key choosing System or User channel delivery): [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md).
- **personal data**, see data inventory and trust boundaries.
- **Platform SSO:** the device registration token and its delivery are [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md); provisioning and password-syncing a Mac's local account through Platform SSO is [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md#provision-and-sync-the-local-account-with-platform-sso).
- **policy:** [4.3](../04-know-your-devices/4.3-use-policies-for-compliance.md).
- **pprof:** the profiling set is [8.5](../08-troubleshooting/8.5-fleetctl-debug.md); the term is glossed in the [glossary](a.6-glossary-and-release-compatibility.md).
- **Preview** (`fleetctl preview`, alias `sandbox`): the throwaway local Fleet; its command contracts are in [a.7](a.7-fleetctl-command-reference.md).
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
- **Redis:** what it holds, and what its loss does and does not cost, is [1.6](../01-foundations/1.6-the-fleet-server.md).
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
- **server logs:** what Fleet's own process logs actually tell you is [8.3](../08-troubleshooting/8.3-server-logs.md); the full set of log surfaces (agent, server, and MDM protocol) is [8.2](../08-troubleshooting/8.2-log-surfaces.md); delivering them onward is [2.8](../02-administer-and-deploy-fleet/2.8-activity-audit-logs-and-log-delivery.md).
- **server URL** (the Fleet server's own address, `server_url`): [2.7](../02-administer-and-deploy-fleet/2.7-organization-and-server-settings.md).
- **service identity** (a non-human, API-only user for automation): [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md); scoping its token to one fleet or a named list of endpoints is [1.4](../01-foundations/1.4-identity-and-roles.md).
- **setup assistant:** [3.2](../03-connect-devices/3.2-enroll-macos-devices.md); the wider setup experience is [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md).
- **setup screen** (the first-run screen that creates the first administrator), see first-run setup.
- **SIEM** (security information and event management): sending Fleet's activity and audit logs to one is [2.8](../02-administer-and-deploy-fleet/2.8-activity-audit-logs-and-log-delivery.md).
- **Smallstep:** one of the six certificate authority types, [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md).
- **software installer:** [5.4](../05-manage-devices/5.4-manage-software-and-applications.md).
- **SSE** (Server-Sent Events, one of the two MCP transports): [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md).
- **SSO and SAML:** [2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md).
- **standard saved reports** (the four global reports `fleet-mcp -seed` bootstraps: macOS admin users, Windows update failures, Linux running containers, universal OS version), see seed mode.
- **stdio** (the standard-input/output MCP transport for local clients like Claude Desktop): [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md).
- **SyncML:** the Windows MDM wire format is diagnosed in [8.9](../08-troubleshooting/8.9-windows-mdm-diagnostics.md).
- **sysdiagnose** (Apple's on-demand diagnostic archive): pulling one from iOS/iPadOS is [8.2](../08-troubleshooting/8.2-log-surfaces.md); Apple MDM diagnostics generally are [8.8](../08-troubleshooting/8.8-apple-mdm-diagnostics.md).

## T

- **team**, see fleet.
- **Technician** (a role defined by what it can change: run scripts, install or uninstall software, with read access much wider than that summary suggests, including recovery secrets; Premium): choosing between Fleet's roles is [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md).
- **Terraform:** the AWS reference architecture module is [2.3](../02-administer-and-deploy-fleet/2.3-deploy-on-aws-or-gcp.md).
- **TLS:** the certificate that protects communication with the service, and the server private key it depends on, is [1.6](../01-foundations/1.6-the-fleet-server.md); planning the DNS name and certificate as server settings is [2.7](../02-administer-and-deploy-fleet/2.7-organization-and-server-settings.md).
- **trust boundary**, see data inventory and trust boundaries.
- **TUF** (The Update Framework): the update repository is [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md); confirming what a host is running is [8.4](../08-troubleshooting/8.4-host-side-investigation.md).
- **two-factor authentication** (Fleet's own email-delivered second factor, Premium): enabling it per account is [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md); why it leaves almost no trace in the activity record is [1.5](../01-foundations/1.5-audit-and-activity.md).

## U

- **user account** (creating or inviting a person, editing their role and scope, forcing a password reset, ending their sessions, deleting them): [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md).
- **user channel** (the macOS-only, sign-in-gated declaration delivery target; exists only for hosts that automatically enrolled): [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md).

## V

- **VPP** (Volume Purchasing, Apple's Apps and Books): [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md); glossed in the [glossary](a.6-glossary-and-release-compatibility.md).
- **vulnerabilities** (CVEs): how software inventory is matched to known vulnerabilities is [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md).
- **`vulnerability-data-stream`** (staging offline vulnerability feeds): [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md).

## W

- **webhook:** [6.5](../06-automate-fleet/6.5-integrations-webhooks-and-external-workflows.md).
- **wipe and lock:** [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md).
- **work profile:** [3.6](../03-connect-devices/3.6-enroll-android-devices.md); the enterprise binding behind it is [2.12](../02-administer-and-deploy-fleet/2.12-bind-android-enterprise.md).
- **WSTEP:** the Windows enrollment certificate, which also serves as Fleet's Windows disk-encryption escrow key, is [2.11](../02-administer-and-deploy-fleet/2.11-configure-windows-management.md); Windows MDM diagnostics are [8.9](../08-troubleshooting/8.9-windows-mdm-diagnostics.md).
