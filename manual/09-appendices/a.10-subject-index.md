---
title: "Subject index"
chapter: "Appendices and indexes"
section: "A.10"
sidebar_position: 10
status: drafting
verified_against: Fleet 4.90.1
verified_on: 2026-08-30
verified_source: "reference aid, not a behaviour claim. Each entry was checked to resolve to a section that defines or explains the term at fleet-v4.90.1; the terms themselves are grounded in the chapters they point at"
reviewed_by:
reviewed_on:
---

# Subject index

An A-Z of the concepts, components, and named artifacts a reader looks up by name: APNs, Redis, the node key, a work profile. Each entry points at the chapter that defines or explains the thing, not at every chapter that mentions it.

This is the noun counterpart to the [capability index](a.1-capability-index.md), which starts from an outcome you want, a verb. Start here when you have met a word and want to know what it is; start there when you know the job and want the chapter that does it. Where a term also carries a short definition in the [glossary](a.6-glossary-and-release-compatibility.md), that is noted, because the glossary is where a renamed or easily-confused term is pinned down.

A cross-reference of the form "see X" means the book files the concept under X, because Fleet renamed it or because one name is the expansion of another.

## A

- **ABM**, see Apple Business Manager.
- **activity and audit log:** the record of what changed and who caused it is defined in [1.5](../01-foundations/1.5-audit-and-activity.md); where those records are delivered is [2.8](../02-administer-and-deploy-fleet/2.8-activity-audit-logs-and-log-delivery.md); reading them during an investigation is [8.12](../08-troubleshooting/8.12-audit-logs.md).
- **ADE** (Automated Device Enrollment): [3.2](../03-connect-devices/3.2-enroll-macos-devices.md) for Macs and [3.5](../03-connect-devices/3.5-enroll-ios-and-ipados-devices.md) for iPhones and iPads. DEP is the former name; the two are separated in the [glossary](a.6-glossary-and-release-compatibility.md).
- **AMAPI** (Android Management API): the binding is [2.12](../02-administer-and-deploy-fleet/2.12-bind-android-enterprise.md); the one-policy-per-device model and its return path are [8.10](../08-troubleshooting/8.10-android-diagnostics.md).
- **Android Enterprise:** [2.12](../02-administer-and-deploy-fleet/2.12-bind-android-enterprise.md).
- **APNs** (Apple Push Notification service): the push channel is [2.9](../02-administer-and-deploy-fleet/2.9-mdm-architecture-and-foundations.md); the certificate that authorises it is [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md).
- **Apple Business Manager** (ABM): [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md); the AB, ABM, and DEP token names are pinned down in the [glossary](a.6-glossary-and-release-compatibility.md).
- **Apps and Books**, see VPP.
- **async host processing:** the experimental `osquery_enable_async_host_processing` mode, which moves label, policy and last-seen writes through Redis, is [8.14](../08-troubleshooting/8.14-degradation.md); its use as a capacity lever is [2.2](../02-administer-and-deploy-fleet/2.2-self-hosting-architecture-and-capacity.md).
- **Autopilot:** Microsoft's zero-touch Windows provisioning path is set up for enrollment in [3.3](../03-connect-devices/3.3-enroll-windows-devices.md) and diagnosed, including why Fleet never talks to it, in [8.9](../08-troubleshooting/8.9-windows-mdm-diagnostics.md).

## B

- **batch script** (running one saved script across many hosts at once): [5.3](../05-manage-devices/5.3-run-and-manage-scripts.md).
- **BitLocker:** [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md); the Windows escrow key it depends on is the WSTEP certificate, [2.11](../02-administer-and-deploy-fleet/2.11-configure-windows-management.md).
- **BitLocker startup PIN:** [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md).

## C

- **carve**, see file carving.
- **certificate authority** (CA): [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md).
- **Chromebook**, see ChromeOS.
- **ChromeOS extension:** [3.7](../03-connect-devices/3.7-enroll-chromeos-devices.md).
- **conditional access:** the policy-driven side is [5.9](../05-manage-devices/5.9-automate-remediation-with-policies.md); the identity-provider side is [2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md).
- **configuration profile:** [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md).
- **`cron_stats`:** the table that records whether a scheduled job ran is in [8.6](../08-troubleshooting/8.6-server-state.md).

## D

- **DDM** (Declarative Device Management): [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md); diagnosing declaration delivery is [8.8](../08-troubleshooting/8.8-apple-mdm-diagnostics.md).
- **dead lettering:** defined in the [glossary](a.6-glossary-and-release-compatibility.md).
- **declarative settings**, see DDM.
- **DEP** (Device Enrollment Program), see ADE. DEP is the deprecated name, kept apart from ADE in the [glossary](a.6-glossary-and-release-compatibility.md).
- **DigiCert:** one of the six certificate authority types, [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md).
- **disk encryption:** [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md).

## E

- **egress destinations** (the outbound map for a firewall review): [2.2](../02-administer-and-deploy-fleet/2.2-self-hosting-architecture-and-capacity.md).
- **enroll secret:** [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md).
- **enrollment profile:** [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md); the macOS route that uses it is [3.2](../03-connect-devices/3.2-enroll-macos-devices.md).
- **Entra** (Microsoft Entra ID): as an identity provider it is [2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md); its part in Windows automatic enrollment is [3.3](../03-connect-devices/3.3-enroll-windows-devices.md).
- **EST** (Enrollment over Secure Transport): one of the six certificate authority types, [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md).

## F

- **file carving:** defined in the [glossary](a.6-glossary-and-release-compatibility.md); it surfaces as an introspection tool in [8.7](../08-troubleshooting/8.7-live-query-introspection.md) and as a storage and limits question in [8.14](../08-troubleshooting/8.14-degradation.md).
- **FileVault:** [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md).
- **fleet** (the scoping construct, renamed from team): [1.3](../01-foundations/1.3-hosts-fleets-labels.md); the rename is recorded in the [glossary](a.6-glossary-and-release-compatibility.md).
- **Fleet Desktop:** introduced as one of the host-side components in [1.2](../01-foundations/1.2-how-fleet-reaches-a-device.md); its end-user surface is designed in [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md).
- **Fleet-maintained apps** (FMA): the curated catalogue is defined in [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md); installing one is [5.4](../05-manage-devices/5.4-manage-software-and-applications.md).
- **fleetd:** the host-side bundle is defined in [1.2](../01-foundations/1.2-how-fleet-reaches-a-device.md); keeping it current is [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md).

## G

- **GitOps:** [6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md).

## H

- **Helm** (the Kubernetes chart): [2.4](../02-administer-and-deploy-fleet/2.4-deploy-with-containers-or-virtual-machines.md).
- **host identity certificate:** [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md); which platforms support it is a row in the [platform capability matrix](a.2-platform-capability-matrix.md).
- **host vitals:** [4.1](../04-know-your-devices/4.1-understand-hosts-vitals-and-inventory.md).
- **Hydrant:** one of the six certificate authority types, [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md).

## L

- **label:** [1.3](../01-foundations/1.3-hosts-fleets-labels.md).
- **LAPS and the managed local administrator account:** [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md).
- **live query**, see report.
- **LUKS** (Linux disk encryption): escrow is [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md).

## M

- **MDM enrollment:** the model is [2.9](../02-administer-and-deploy-fleet/2.9-mdm-architecture-and-foundations.md); the status values are pinned down in the [glossary](a.6-glossary-and-release-compatibility.md).
- **My Device page:** designed in [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md); the channel behind it is [1.2](../01-foundations/1.2-how-fleet-reaches-a-device.md).
- **MySQL:** its role as Fleet's authoritative store is [1.6](../01-foundations/1.6-the-fleet-server.md).

## N

- **NDES:** the Microsoft SCEP proxy, [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md).
- **node key:** [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md); also glossed in the [glossary](a.6-glossary-and-release-compatibility.md).
- **Nudge:** [5.6](../05-manage-devices/5.6-control-operating-system-updates.md).

## O

- **object storage** (S3 and compatible): its place in the server's stores is [1.6](../01-foundations/1.6-the-fleet-server.md); provider specifics are [2.3](../02-administer-and-deploy-fleet/2.3-deploy-on-aws-or-gcp.md).
- **Orbit:** introduced in [1.2](../01-foundations/1.2-how-fleet-reaches-a-device.md) as the bundle's supervisor; managed in [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md).
- **osquery:** introduced in [1.2](../01-foundations/1.2-how-fleet-reaches-a-device.md); query design and performance are [4.6](../04-know-your-devices/4.6-advanced-osquery-queries-and-tables.md).
- **osquery-perf** (the load-simulation tool): [7.5](../07-operate-fleet/7.5-maintain-capacity-and-availability.md).

## P

- **pack:** the legacy 2017 query pack is covered in [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) and glossed in the [glossary](a.6-glossary-and-release-compatibility.md).
- **Platform SSO:** the device registration token and its delivery are [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md).
- **policy:** [4.3](../04-know-your-devices/4.3-use-policies-for-compliance.md).
- **pprof:** the profiling set is [8.5](../08-troubleshooting/8.5-fleetctl-debug.md); the term is glossed in the [glossary](a.6-glossary-and-release-compatibility.md).
- **Preview** (`fleetctl preview`, alias `sandbox`): the throwaway local Fleet; its command contracts are in [a.7](a.7-fleetctl-command-reference.md).
- **profile**, see configuration profile.

## Q

- **query**, see report.

## R

- **recovery key escrow:** [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md).
- **Recovery Lock** (the Apple silicon firmware password): [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md).
- **Redis:** what it holds, and what its loss does and does not cost, is [1.6](../01-foundations/1.6-the-fleet-server.md).
- **report and live report** (renamed from query and live query in 4.82.0): [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md); a live report used as an introspection tool is [8.7](../08-troubleshooting/8.7-live-query-introspection.md). The rename is in the [glossary](a.6-glossary-and-release-compatibility.md).

## S

- **SAML**, see SSO.
- **SCEP:** [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md); glossed in the [glossary](a.6-glossary-and-release-compatibility.md).
- **SCIM:** [2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md).
- **scheduled query:** [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md); writing efficient ones is [4.6](../04-know-your-devices/4.6-advanced-osquery-queries-and-tables.md).
- **secret variables:** [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md); their use in version-controlled configuration is [6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md).
- **self-service:** [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md).
- **setup assistant:** [3.2](../03-connect-devices/3.2-enroll-macos-devices.md); the wider setup experience is [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md).
- **Smallstep:** one of the six certificate authority types, [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md).
- **software installer:** [5.4](../05-manage-devices/5.4-manage-software-and-applications.md).
- **SSO and SAML:** [2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md).
- **SyncML:** the Windows MDM wire format is diagnosed in [8.9](../08-troubleshooting/8.9-windows-mdm-diagnostics.md).

## T

- **team**, see fleet.
- **Terraform:** the AWS reference architecture module is [2.3](../02-administer-and-deploy-fleet/2.3-deploy-on-aws-or-gcp.md).
- **TUF** (The Update Framework): the update repository is [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md); confirming what a host is running is [8.4](../08-troubleshooting/8.4-host-side-investigation.md).

## V

- **VPP** (Volume Purchasing, Apple's Apps and Books): [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md); glossed in the [glossary](a.6-glossary-and-release-compatibility.md).
- **vulnerabilities** (CVEs): how software inventory is matched to known vulnerabilities is [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md).
- **`vulnerability-data-stream`** (staging offline vulnerability feeds): [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md).

## W

- **webhook:** [6.5](../06-automate-fleet/6.5-integrations-webhooks-and-external-workflows.md).
- **wipe and lock:** [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md).
- **work profile:** [3.6](../03-connect-devices/3.6-enroll-android-devices.md); the enterprise binding behind it is [2.12](../02-administer-and-deploy-fleet/2.12-bind-android-enterprise.md).
- **WSTEP:** the Windows enrollment certificate, which also serves as Fleet's Windows disk-encryption escrow key, is [2.11](../02-administer-and-deploy-fleet/2.11-configure-windows-management.md); Windows MDM diagnostics are [8.9](../08-troubleshooting/8.9-windows-mdm-diagnostics.md).
