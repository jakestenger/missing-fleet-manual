---
title: "Capability index"
chapter: "Appendices and indexes"
section: "A.1"
sidebar_position: 1
verified_against: Fleet 4.90.0
verified_on: 2026-09-03
verified_source: "drafted against fleet-v4.90.0 (7c428c6e46) from a pass over all 364 rows of the shared capability register (360 in the original pass, plus four amendments below). Every word in the index was read somewhere it can be met: Fleet's source at the tag, Fleet's own published documentation at the same tag, or this manual. None was invented. Amended 2026-09-02 (round4 RB3): CAP-003's `fpsso` search term was misrouted to 2.5's Fleet-console JIT provisioning; `fpsso` is Fleet's own settings-search term for the unrelated Platform SSO account-provisioning and password-sync feature, which had no capability row at all. Removed from CAP-003, added as the new CAP-372, routed to 5.5. Amended again 2026-09-02 (round4 RM9): added CAP-373, requiring ACME/Managed Device Attestation for eligible Macs' identity certificates, routed to 2.10; verified against `appconfig.go`, `apple_mdm.go` (`isMDMAppleACMERequired`, `RenewSCEPCertificates`, `maybeQueueCertificateListForACMEProfile`) and the frontend's `HostLifecycleSection.tsx` at the tag. Amended again 2026-09-03 (round4 RM17): CAP-370 (turning MDM off for one host) and CAP-371 (Fleet's own FileVault-key repair) already existed in this register with no owning chapter; gave both formal rows now that 5.7 and 5.8 teach them, verified against `server/service/mdm.go` (`UnenrollMDM`), `server/mdm/android/service/service.go` (`UnenrollAndroidHost`), `cmd/fleet/cron.go` (`verifyDiskEncryptionKeys`) and `server/service/orbit.go` (`setDiskEncryptionNotifications`) at the tag. Amended again 2026-09-03 (round6 M16): the host display name template, now taught in 5.2, joined the no-capability-row register (five outcomes to six); it keeps no formal CAP row, so the 364-row count above is unchanged. Amended again 2026-09-03 (round6 M17): the Apple DDM declaration asset, now taught in 5.2, joined the no-capability-row register (six outcomes to seven); it keeps no formal CAP row, so the 364-row count above is unchanged. Amended again 2026-09-04 (round8 MJ-H): first-run setup, taught in 2.2 and gated by SetupRequired in the Fleet server at the tag, joined the no-capability-row register (seven outcomes to eight) and gained subject-index routing in a.10; it keeps no formal CAP row, so the 364-row count above is unchanged. Citation ledger at research/section-notes/a.1-notes.md"
further_reading:
  - https://fleetdm.com/docs/get-started/faq
feature_requests:
  labels: [":product"]
  match: ["rename", "terminology", "naming", "deprecated", "search"]
  exclude: []
---

# Capability index

**Search the last column for the word you have. Open the owning chapter. `(no)` means Fleet does not provide the capability.** The rows themselves are in [The index](#the-index); the sections after it explain where its words come from.

**Every outcome this manual teaches has one chapter that owns it, and this index gets you there from the word you would actually type.** A table of contents can only expose the book's own vocabulary. Administrators arrive holding Apple's word, Microsoft's word, the name of the product they are migrating off, or the name Fleet itself used two releases ago, and none of those is what a chapter is called.

That distance is the appendix. A row earns its place when the words in its last column are words the contents page would not have given you.

## What this appendix carries

![Reference](../_assets/icons/reference.svg) 364 outcomes in eight groups, each with one canonical chapter, and the attested words that lead to it: Fleet's older names that still work, the vendors' names, the strings Fleet prints on screen, and the terms this manual coined. Group 8 also carries the sentences people arrive with when something has already gone wrong. The last section says where the index stops.

**What is not here.** Whether your platform can do it is [a.2](a.2-platform-capability-matrix.md). Which role may do it is [a.4](a.4-roles-and-permissions-matrix.md). Which interface can do it is [a.5](a.5-interface-index.md). Which configuration authority owns a key you find here, and what wins when two disagree, is [a.3](a.3-configuration-model-and-precedence.md). What a route requires is [a.8](a.8-api-action-and-endpoint-reference.md), and what a `fleetctl` command asks Fleet to do is [a.7](a.7-fleetctl-command-reference.md). What a word means is [a.6](a.6-glossary-and-release-compatibility.md), which owns meaning while this index owns routing. How to do the thing is the chapter each row names. This appendix answers where, and makes no claim about capability, licence or procedure.

## How to read a row

![Reference](../_assets/icons/reference.svg) Five columns, and the last one is the reason the appendix exists.

| Column | What it holds |
|---|---|
| **ID** | The shared capability identifier. Use it to find the same capability in [a.2](a.2-platform-capability-matrix.md) and [a.5](a.5-interface-index.md). [a.5](a.5-interface-index.md) carries one row per ID. [a.2](a.2-platform-capability-matrix.md) carries nearly the same set, with two differences: it splits a few outcomes into lettered sub-rows (CAP-244a and its siblings, CAP-341a and its sibling) where the parts of one outcome answer differently by platform, so an ID can land you on more than one row there, and it carries three Chromebook IDs (CAP-367, CAP-368 and CAP-369) that this index holds only in its no-row list below rather than as index rows. [a.4](a.4-roles-and-permissions-matrix.md) is coarser again: its 152 administrator intents are a coarser grouping than this index's 364 outcomes, so no row-for-row ID exists there |
| **What you are trying to do** | The outcome in the words somebody would use for it, rather than the words the chapter uses |
| **Chapter** | The one section that teaches this outcome. `None` means no chapter does, and those rows are collected at the end |
| **Also** | Sections carrying part of the answer, as plain numbers, because the linked chapter is the one to open first |
| **Words that lead here** | Words and phrases attested somewhere a person would meet them, separated by a middle dot |

Six markers, and each changes what you do with the word next to it.

| Marker | Means |
|---|---|
| **(still accepted)** | Fleet's own older name, live at 4.90.0. Type it, send it, leave it in your scripts |
| **(vendor)** | Apple's, Microsoft's or Google's word. Fleet does not use it, so searching Fleet for it returns nothing |
| **(ours)** | This manual's word. It will not appear in Fleet's interface, API or documentation |
| **(clash)** | Two live Fleet names for one thing, disagreeing with each other. Both appear, neither is marked wrong |
| **(no)** | The chapter named is the one that records that Fleet does not do this. Read it and stop looking |
| **[a.6]** | [a.6](a.6-glossary-and-release-compatibility.md) settles what the word means. This row carries only the route |

**Where the last column is empty, the row's own words are the search words.** The row is present so the enumeration is complete, and it is not what the appendix is for.

## The index

![Reference](../_assets/icons/reference.svg) 364 outcomes. Find the row by the words you would type, then open the linked chapter.

### 1. Access and accountability

**Who can use Fleet, how they prove it, and what is recorded.** 32 outcomes, cutting across Parts I, II and VII.

| ID | What you are trying to do | Chapter | Also | Words that lead here |
|---|---|---|---|---|
| **CAP-001** | Sign in, or reset a password | [1.4](../01-foundations/1.4-identity-and-roles.md) | 2.6 | `user_logged_in` · `user_failed_login` · Access denied · my account · change password · API token · disable password-based authentication |
| **CAP-002** | Sign in through the identity provider | [1.4](../01-foundations/1.4-identity-and-roles.md) | 2.5 | SSO · SAML · single sign-on · log in with Okta · log in with Entra · IdP · authentik · Google Workspace · `user_added_by_sso` |
| **CAP-003** | Create accounts the first time someone signs in | [2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md) | 1.4 | JIT · just-in-time provisioning · auto-create users · account provisioning |
| **CAP-004** | Remove accounts when people leave | [2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md) | 1.4 | SCIM · deprovision · offboarding · account provisioning |
| **CAP-005** | Work out why an account was not deprovisioned | [2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md) | 2.6 | required SCIM attributes · `email` · `userName` · `givenName` · `familyName` · deprovisioning matches by email · API-only and non-SSO accounts skipped · last global admin never deleted |
| **CAP-006** | Require a second factor | [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md) | 1.5, 2.5 | 2FA · MFA · email two-factor · one-time code |
| **CAP-007** | Add a person and give them a role | [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md) | 1.4 | invite · new user · create user · human user · make someone an admin · `created_user` · `changed_user_global_role` · Add User button disabled |
| **CAP-008** | Choose between Fleet's roles | [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md) | 1.4 | `observer_plus` · Observer+ · observer plus · `gitops` · `technician` · role-based access |
| **CAP-009** | Give someone access to one fleet only | [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md) | 1.4, 1.3 | team role (still accepted) · team admin (still accepted) · `--team` (still accepted) · fleet-level permissions · `changed_user_team_role` |
| **CAP-010** | Create a non-human identity for automation | [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md) | 6.1, 1.4 | API token · API-only user · service account · bot user · gitops user · `api only user` · retrieve your API token |
| **CAP-011** | Scope a non-human identity to one fleet | [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md) | 1.4 | `--team <id>:<role>` (still accepted) · `--fleet <id>:<role>` |
| **CAP-012** | Restrict a token to particular endpoints | [1.4](../01-foundations/1.4-identity-and-roles.md) | 2.6, 6.1 | endpoint restrictions (ours) · `user_api_endpoints` · allowlist endpoints |
| **CAP-013** | Add or remove a fleet's members | [1.4](../01-foundations/1.4-identity-and-roles.md) | 2.6 | team member (still accepted) · `/fleet/teams/{id}/users` (still accepted) · add users to fleet |
| **CAP-014** | Make the interface read-only | [2.7](../02-administer-and-deploy-fleet/2.7-organization-and-server-settings.md) | 6.2 | GitOps mode · change management · lock the interface · workflow · `enabled_gitops_mode` |
| **CAP-015** | Find out who changed something | [1.5](../01-foundations/1.5-audit-and-activity.md) | 2.8, 8.12 | audit log · activity feed · who did that · `activities` (clash) · `activity_past` · [a.6] |
| **CAP-016** | Read one host's history | [1.5](../01-foundations/1.5-audit-and-activity.md) | 8.12 | host timeline · past activity |
| **CAP-017** | See what is queued for a host | [1.5](../01-foundations/1.5-audit-and-activity.md) | 5.1, 8.6 | upcoming activity · pending work · queued · [a.6] |
| **CAP-018** | Push every activity to a webhook | [1.5](../01-foundations/1.5-audit-and-activity.md) | 6.5, 2.8 | activity automations · `enabled_activity_automations` · Manage automations |
| **CAP-019** | Stream the audit record to a SIEM | [2.8](../02-administer-and-deploy-fleet/2.8-activity-audit-logs-and-log-delivery.md) | 1.5 | audit log destination · external activity audit logging · Splunk · Firehose · Kinesis · Lambda · Pub/Sub · Kafka · log destinations |
| **CAP-020** | Work out why an activity never reached the SIEM | [1.5](../01-foundations/1.5-audit-and-activity.md) | 8.12 | `host_only` |
| **CAP-021** | Set how long Fleet keeps activity | [2.7](../02-administer-and-deploy-fleet/2.7-organization-and-server-settings.md) | 1.5 | `activity_expiry_settings` · activity retention |
| **CAP-022** | Keep a host's history across re-enrollment | [1.5](../01-foundations/1.5-audit-and-activity.md) | 2.7 | `preserve_host_activities_on_reenrollment` |
| **CAP-023** | Read a disk encryption recovery key | [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md) | 1.4, 2.6 | recovery key · FileVault key · `filevault2` · bitlocker key (vendor) · unlock this laptop · Show disk encryption key · `read_host_disk_encryption_key` |
| **CAP-024** | Prove nobody read a secret without permission | [1.5](../01-foundations/1.5-audit-and-activity.md) | 5.8 | `read_host_disk_encryption_key` · `viewed_host_recovery_lock_password` · `read_managed_local_account` |
| **CAP-290** | Set roles from the identity provider | [2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md) | 2.6 | role sync · SAML role attribute · `FLEET_JIT_USER_ROLE_TEAM_<id>` (still accepted) · `FLEET_JIT_USER_ROLE_FLEET_<id>` · customization of user roles |
| **CAP-291** | Keep a way in when the identity provider is down | [2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md) | 2.6 | break-glass account (ours) |
| **CAP-292** | Put the end user's name on the host record | [2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md) | 4.1 | human-device mapping · foreign host vitals · User mapping · `identity-provider` (clash) · Okta · Entra · Azure AD (vendor) · LDAP (vendor) |
| **CAP-293** | Set a host's user by hand | [2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md) | 4.1 | `edited_host_idp_data` |
| **CAP-294** | Check the identity provider connection | [2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md) | 8.13 | No IdP connected · identity provider details |
| **CAP-297** | Rotate an API token | [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md) | 7.6 | revoke the authorization tokens for a user · **(no)** |
| **CAP-298** | Remove a person, or demote an administrator | [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md) | 1.4 | `deleted_user` · `deleted_user_global_role` · last admin |
| **CAP-313** | Run an access review | [7.6](../07-operate-fleet/7.6-maintain-credentials-certificates-and-access.md) | 2.6 | who has admin · least privilege · last token use · **(no)** |

### 2. Connecting devices

**Getting a device enrolled, and the platform connections that must exist first.** 68 outcomes. The credentials that make these connections work are in group 7, because you meet them again at renewal.

| ID | What you are trying to do | Chapter | Also | Words that lead here |
|---|---|---|---|---|
| **CAP-025** | Understand how a device authenticates to Fleet | [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md) | 1.3 | enroll secret · enrollment token · `enroll_secrets` · `fleetctl get enroll-secret` · `edited_enroll_secrets` · system keystore |
| **CAP-026** | Rotate an enroll secret | [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md) | 3.2, 3.3, 3.4 | the secret leaked · target hosts by enroll secret |
| **CAP-027** | Enroll a Mac with no hands on it | [3.2](../03-connect-devices/3.2-enroll-macos-devices.md) | 2.10 | DEP (vendor) · Device Enrollment Program (vendor) · ADE · ABM · zero-touch · company-owned Mac · automated enrollment · [a.6] |
| **CAP-028** | Enroll a Mac from a link | [3.2](../03-connect-devices/3.2-enroll-macos-devices.md) | 3.1 | Add hosts · enrollment link · manual enrollment · onboard · provision · fleetd |
| **CAP-029** | Enroll a personally owned Mac | [3.2](../03-connect-devices/3.2-enroll-macos-devices.md) | 5.7 | BYOD · personal Mac · personally owned · `On (manual - personal)` · [a.6] |
| **CAP-030** | Download the manual enrollment profile | [3.2](../03-connect-devices/3.2-enroll-macos-devices.md) | 6.3 | unsigned mobileconfig · `/fleet/mdm/manual_enrollment_profile` (still accepted) |
| **CAP-031** | Get the default automatic enrollment profile | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) | 3.2 | Setup Assistant profile · `/fleet/mdm/apple/enrollment_profile` (still accepted) |
| **CAP-032** | Work out why the agent never arrived after MDM enrollment | [3.2](../03-connect-devices/3.2-enroll-macos-devices.md) | 8.4 | `InstallEnterpriseApplication` · half-enrolled (ours) |
| **CAP-033** | Let a bootstrap package deliver the agent instead | [3.2](../03-connect-devices/3.2-enroll-macos-devices.md) | 5.5 | `manual_agent_install` (still accepted) · `macos_manual_agent_install` |
| **CAP-034** | Make the user sign in during enrollment | [3.2](../03-connect-devices/3.2-enroll-macos-devices.md) | 2.5, 5.5 | end user authentication · require IdP authentication · `enabled_macos_setup_end_user_auth` |
| **CAP-035** | Enroll Windows by installing the agent | [3.3](../03-connect-devices/3.3-enroll-windows-devices.md) | 2.11 | MSI · `win10` · `win11` · pc · install fleetd |
| **CAP-036** | Enroll Windows at first boot | [3.3](../03-connect-devices/3.3-enroll-windows-devices.md) | 2.11 | Autopilot (vendor) · OOBE (vendor) · Entra · Azure AD (vendor) · Active Directory (vendor) · repurposing a Windows device |
| **CAP-037** | Let a person enroll Windows from Settings | [3.3](../03-connect-devices/3.3-enroll-windows-devices.md) | 2.11 | Access work or school (vendor) · Automatic enrollment (clash) |
| **CAP-038** | Stop Fleet turning Windows MDM on by itself | [3.3](../03-connect-devices/3.3-enroll-windows-devices.md) | 2.11 | `enable_turn_on_windows_mdm_manually` |
| **CAP-039** | Move Windows hosts off another MDM with no prompt | [2.11](../02-administer-and-deploy-fleet/2.11-configure-windows-management.md) | 3.3 | Intune (vendor) · automatic Windows MDM migration · `enabled_windows_mdm_migration` |
| **CAP-040** | Prompt a Mac's user to migrate from another MDM | [3.2](../03-connect-devices/3.2-enroll-macos-devices.md) | 6.5, 1.2 | Jamf (vendor) · Workspace ONE (vendor) · Kandji (vendor) · Munki (vendor) · macOS MDM migration · seamless migration |
| **CAP-041** | Have Fleet push the agent to Entra-enrolled Windows hosts | [3.3](../03-connect-devices/3.3-enroll-windows-devices.md) | 2.11 | global enroll secret |
| **CAP-042** | Enroll a Linux host | [3.4](../03-connect-devices/3.4-enroll-linux-devices.md) | 3.1 | deb · rpm · `tar.gz` · tarballs · Arch · Linux support |
| **CAP-043** | Re-point a deployed Linux agent | [3.4](../03-connect-devices/3.4-enroll-linux-devices.md) | 3.8 | `/etc/default/orbit` · `ORBIT_*` · config-less deployment · change the Fleet URL |
| **CAP-044** | Build a Mac package with no secret inside it | [3.2](../03-connect-devices/3.2-enroll-macos-devices.md) | 3.1 | `--use-system-configuration` · system keystore |
| **CAP-045** | Supply a Windows host's settings at install time | [3.3](../03-connect-devices/3.3-enroll-windows-devices.md) | 3.1 | MSI properties · `FLEET_URL` · `FLEET_SECRET` · `ENABLE_SCRIPTS` · `END_USER_EMAIL` · `EUA_TOKEN` · heat failed |
| **CAP-046** | Enroll an iPhone or iPad with no hands on it | [3.5](../03-connect-devices/3.5-enroll-ios-and-ipados-devices.md) | 2.10 | zero-touch iPhone · ADE iPad · which Apple devices work with ADE |
| **CAP-047** | Enroll a company-owned iPhone from a link | [3.5](../03-connect-devices/3.5-enroll-ios-and-ipados-devices.md) | 2.10 | enrollment URL for an iPhone |
| **CAP-048** | Enroll a personally owned iPhone or iPad | [3.5](../03-connect-devices/3.5-enroll-ios-and-ipados-devices.md) | 5.7 | BYOD iPad · personal iPhone · profile-based enrollment |
| **CAP-049** | Let a person enroll with a Managed Apple Account | [3.5](../03-connect-devices/3.5-enroll-ios-and-ipados-devices.md) | 2.5, 2.10 | Managed Apple ID (vendor) · account-driven enrollment |
| **CAP-050** | Work out why account-driven enrollment cannot find the server | [3.5](../03-connect-devices/3.5-enroll-ios-and-ipados-devices.md) | 8.8 | `mdm_service_discovery` · service discovery |
| **CAP-051** | Decide which fleet automatically enrolled devices land in | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) | 3.5, 3.2 | default team (still accepted) · `macos_team` (still accepted) · `ios_team` (still accepted) · `ipados_team` (still accepted) · `byod_team` (still accepted) · `macos_fleet` |
| **CAP-052** | Enroll a personally owned Android device | [3.6](../03-connect-devices/3.6-enroll-android-devices.md) | 2.12 | work profile (vendor) · profile owner (vendor) · Android BYOD migration · remove the old work profile |
| **CAP-053** | Enroll a company-owned Android device at first boot | [3.6](../03-connect-devices/3.6-enroll-android-devices.md) | 2.12 | QR code · fully managed (vendor) · device owner (vendor) · `fully_managed` |
| **CAP-054** | Issue an Android enrollment token | [3.6](../03-connect-devices/3.6-enroll-android-devices.md) | 8.10 | token expired · one hour · one device |
| **CAP-055** | Enroll a Chromebook | [3.7](../03-connect-devices/3.7-enroll-chromeos-devices.md) | 4.2 | ChromeOS · Fleetd for Chrome · force-installed extension · managing Chrome with Fleet |
| **CAP-056** | Give a host a hardware-backed identity | [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md) | 3.4 | TPM · device attestation · host identity certificates · certificates in fleetd |
| **CAP-057** | Require signed requests from hosts | [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md) | 2.2 | `auth.require_http_message_signature` · fleetd authentication |
| **CAP-058** | Recognise a returning device instead of creating a new one | [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md) | 4.1, 8.4 | duplicate enrollment · re-enrollment · the host came back as a new record · IP duplication · node key · [a.6] |
| **CAP-059** | Enroll two operating systems on one machine | [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md) | 8.14 | `--host-identifier=instance` · dual boot · cloned VM |
| **CAP-060** | Move a host to another fleet | [1.3](../01-foundations/1.3-hosts-fleets-labels.md) | 5.8 | Transfer · move a host to another team (still accepted) · fleet move (ours) · `transferred_hosts` · update hosts' fleet |
| **CAP-061** | Delete a host record | [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md) | 4.5 | remove a device from Fleet · `deleted_host` |
| **CAP-062** | Stop a deleted host coming back | [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md) | 2.10, 8.4 | the host keeps reappearing |
| **CAP-063** | Expire stale host records | [2.7](../02-administer-and-deploy-fleet/2.7-organization-and-server-settings.md) | 4.5 | `host_expiry_settings` · clean up old records |
| **CAP-064** | Build an installer | [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md) | 3.2, 3.3, 3.4 | `fleetctl package` · pkg · msi · deb · rpm · exe · ps1 · signing fleetd · a.7 owns the command contract |
| **CAP-065** | Configure the end user's own surface | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) | 3.2, 3.3, 3.4 | Fleet Desktop · My device · tray icon · transparency · browser host · custom proxy |
| **CAP-066** | Allow scripts on a host | [5.3](../05-manage-devices/5.3-run-and-manage-scripts.md) | 3.2, 3.3, 3.4 | `--enable-scripts` · `ENABLE_SCRIPTS` · `ORBIT_ENABLE_SCRIPTS` · Running scripts is disabled in organization settings |
| **CAP-067** | Set which agent versions a host takes | [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md) | 1.2 | `update_channels` · update channel · pin the agent · fleetd updates |
| **CAP-068** | Set the channel on one host | [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md) | 3.4 | `--orbit-channel` · `ORBIT_ORBIT_CHANNEL` · `ORBIT_OSQUERYD_CHANNEL` · `ORBIT_DESKTOP_CHANNEL` |
| **CAP-069** | Pin the agent to an exact version | [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md) | 1.2 | version pinning |
| **CAP-070** | Roll the agent back | [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md) | 7.3 | downgrade the agent (clash: downgrading Fleet is a different operation) |
| **CAP-071** | Stop an agent updating at all | [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md) | 8.4 | `--disable-updates` · `ORBIT_DISABLE_UPDATES` |
| **CAP-072** | Publish agent versions from your own repository | [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md) | 6.4 | TUF · `fleetctl updates init` · `updates add` · `updates roots` · `updates timestamp` · `updates rotate` · air-gapped agents · where does fleetd get update information |
| **CAP-073** | See what agent version a host is running | [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md) | 4.5, 8.4 | Agent card · component versions |
| **CAP-364** | Force an agent update check without waiting for the interval | [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md) |  | restart the agent to check for updates now · Orbit restart triggers an immediate update check · skip the update interval |
| **CAP-074** | Ship an osquery extension to hosts | [4.7](../04-know-your-devices/4.7-extend-osquery-with-custom-tables-and-plugins.md) | 3.8 | custom table · `extensions` · bundle osquery extensions into fleetd |
| **CAP-075** | Send an extension only to some hosts | [4.7](../04-know-your-devices/4.7-extend-osquery-with-custom-tables-and-plugins.md) | 1.3 | targeting extensions with labels |
| **CAP-076** | Set osquery runtime options | [1.2](../01-foundations/1.2-how-fleet-reaches-a-device.md) | 4.6, 6.2 | agent options · `distributed_interval` · `config_refresh` · `config_tls_refresh` (clash) · `command_line_flags` · global config · `edited_agent_options` |
| **CAP-077** | Set the supervisor's own settings | [1.3](../01-foundations/1.3-hosts-fleets-labels.md) | 3.8 | `orbit` · `script_execution_timeout` · `update_channels` |
| **CAP-078** | Watch files for change | [4.7](../04-know-your-devices/4.7-extend-osquery-with-custom-tables-and-plugins.md) | 4.6 | FIM · file integrity monitoring · `file_paths` · `file_accesses` |
| **CAP-079** | Scan hosts with signature sets | [4.7](../04-know-your-devices/4.7-extend-osquery-with-custom-tables-and-plugins.md) | 5.7 | YARA · `yara` · remote deployment of YARA rules |
| **CAP-080** | Add columns to every result | [4.7](../04-know-your-devices/4.7-extend-osquery-with-custom-tables-and-plugins.md) | 4.6 | `decorators` |
| **CAP-081** | Turn event collection on or off | [4.7](../04-know-your-devices/4.7-extend-osquery-with-custom-tables-and-plugins.md) | 8.14 | evented tables · event subscribers · `disable_events` |
| **CAP-082** | Get a file off a device | [8.7](../08-troubleshooting/8.7-live-query-introspection.md) | 1.6 | file carving · carve · `fleetctl get carve` · `get carves` · collect a log file · [a.6] |
| **CAP-269** | Turn Apple MDM on | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) | 2.9 | APNs · push certificate · `apns` · activate · iphone · ipad · macbook |
| **CAP-272** | Connect Apple Business Manager | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) | 3.2, 3.5 | ABM token · AB token · DEP token · `abm_token` (still accepted) · `ab_token` · `fleetctl get mdm-ab` · `mdm_apple_bm` (still accepted) · [a.6] |
| **CAP-275** | Connect Apple's app purchasing | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) | 5.4 | VPP (vendor) · Volume Purchasing Program (vendor) · Apps and Books · App and Book token · [a.6] |
| **CAP-278** | Turn Windows MDM on | [2.11](../02-administer-and-deploy-fleet/2.11-configure-windows-management.md) | 3.3 | WSTEP · `mdm.windows_wstep_identity_cert_bytes` |
| **CAP-279** | Choose the Windows enrollment experience | [2.11](../02-administer-and-deploy-fleet/2.11-configure-windows-management.md) | 3.3 | Automatic enrollment (clash) · Manual enrollment |
| **CAP-281** | Bind Fleet to Android Enterprise | [2.12](../02-administer-and-deploy-fleet/2.12-bind-android-enterprise.md) | 3.6 | AMAPI (vendor) · Managed Google Play (vendor) · google · enterprise · phone · tablet |
| **CAP-282** | Deliver certificates to Android | [2.12](../02-administer-and-deploy-fleet/2.12-bind-android-enterprise.md) | 5.2 | `COMPANION_APP` · `CERT_INSTALL` · `android_settings.certificates` · the Fleet Android app |
| **CAP-283** | Tune the Android integration | [2.12](../02-administer-and-deploy-fleet/2.12-bind-android-enterprise.md) | 8.10 | `mdm.android_agent.package` · `mdm.android_batch_size` |
| **CAP-349** | Connect a certificate authority | [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md) | 5.2, 2.5 | connect a certificate authority · connect an issuing authority · the certificate prerequisite · six certificate authority types · `certificate_authorities` · `ndes_scep_proxy` · `custom_scep_proxy` · what creation validates · where Fleet keeps the credentials · distinct from delivering a certificate (CAP-153) |

### 3. Scope and targeting

**Deciding who a change reaches and whose data you are reading.** 8 outcomes, and they precede both the reading group and the writing group, which is why they are not filed inside either.

| ID | What you are trying to do | Chapter | Also | Words that lead here |
|---|---|---|---|---|
| **CAP-140** | Group hosts by a question | [1.3](../01-foundations/1.3-hosts-fleets-labels.md) | 4.2 | dynamic label · smart group · query-based group · tag · category · filter · `created_label` |
| **CAP-141** | Group hosts by hand | [1.3](../01-foundations/1.3-hosts-fleets-labels.md) | 4.5 | manual label · static group · add labels to host |
| **CAP-142** | Group hosts on a vital | [1.3](../01-foundations/1.3-hosts-fleets-labels.md) | 4.1 | host vitals label |
| **CAP-143** | Keep a label inside one fleet | [1.3](../01-foundations/1.3-hosts-fleets-labels.md) | 6.2 | team-scoped label (still accepted) · label scope, global against fleet |
| **CAP-144** | Separate configuration by department | [1.3](../01-foundations/1.3-hosts-fleets-labels.md) | 1.4, 2.6 | teams (still accepted) · `add team` (still accepted) · `fleetctl get teams` (still accepted) · groups · No fleets yet · [a.6] |
| **CAP-145** | Rename a label | [1.3](../01-foundations/1.3-hosts-fleets-labels.md) | 6.2 | `edited_label` |
| **CAP-150** | Give one fleet its own profiles | [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) | 1.3 | exact scope · a global profile and a named fleet |
| **CAP-151** | Send something to only some hosts | [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) | 1.3 | label scoping · `labels_include_all` · `labels_include_any` · `labels_exclude_any` · `labels` (still accepted) · combining include and exclude |

### 4. Knowing what a device is

**Reading state: vitals, reports, policies, software, vulnerabilities and estate counts.** 58 outcomes.

| ID | What you are trying to do | Chapter | Also | Words that lead here |
|---|---|---|---|---|
| **CAP-083** | See what a device is and what is on it | [4.1](../04-know-your-devices/4.1-understand-hosts-vitals-and-inventory.md) | 4.5 | host details · vitals · inventory · devices · endpoints · machines · computers · serial number · hostname |
| **CAP-084** | Add a field to every host record | [4.7](../04-know-your-devices/4.7-extend-osquery-with-custom-tables-and-plugins.md) | 4.1 | `additional_queries` (clash: Fleet's own FAQ still asks about them by the pre-rename name) |
| **CAP-085** | Record a value Fleet cannot collect | [4.1](../04-know-your-devices/4.1-understand-hosts-vitals-and-inventory.md) | 4.7 | custom host vital · asset tag · Variables · `created_custom_host_vital` |
| **CAP-086** | Query an application's own database | [4.7](../04-know-your-devices/4.7-extend-osquery-with-custom-tables-and-plugins.md) | 4.6 | `auto_table_construction` · ATC · SQLite |
| **CAP-087** | Replace one of Fleet's built-in queries | [4.7](../04-know-your-devices/4.7-extend-osquery-with-custom-tables-and-plugins.md) | 4.1 | `detail_query_overrides` |
| **CAP-088** | Collect the accounts on a machine | [4.1](../04-know-your-devices/4.1-understand-hosts-vitals-and-inventory.md) | 8.4 | `enable_host_users` · who is logged in · local accounts |
| **CAP-089** | See which certificates a host holds | [4.1](../04-know-your-devices/4.1-understand-hosts-vitals-and-inventory.md) | 5.2 | view certificates in host vitals · get host's certificates |
| **CAP-090** | Attach an email address to a host | [4.1](../04-know-your-devices/4.1-understand-hosts-vitals-and-inventory.md) | 2.5 | device mapping · human-device mapping · `END_USER_EMAIL` · whose laptop is this |
| **CAP-091** | Ask a host to report again now | [4.3](../04-know-your-devices/4.3-use-policies-for-compliance.md) | 5.9, 4.1 | Refetch · refresh this host · how often is software inventory updated |
| **CAP-092** | Refresh an iPhone's inventory on a schedule | [3.5](../03-connect-devices/3.5-enroll-ios-and-ipados-devices.md) | 4.1 | `apple_mdm_iphone_ipad_refetcher` · my iPhone data is stale |
| **CAP-093** | Run a query right now | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) | 8.7 | live query (still accepted) · live report · ad hoc · `fleetctl query` (still accepted) · run report · execute report · Live report whose value is `query` (clash) · [a.6] |
| **CAP-094** | Save a query without scheduling it | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) | 6.2 | saved query (still accepted) · Save report · `created_saved_query` · [a.6] |
| **CAP-095** | Run a query on a schedule | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) | 2.8 | scheduled query (still accepted) · `scheduled_query_id` (still accepted) · `scheduled_report_id` · interval · Where did the Schedule page go |
| **CAP-096** | Find where the results went | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) | 8.7 | Nothing to report yet · Collecting results · stored report · get report data |
| **CAP-097** | Send results to a log destination | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) | 2.8 | query automations · report automations · Splunk · why aren't my live queries being logged |
| **CAP-098** | Read one report across the estate | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) | 4.5 | estate-wide results |
| **CAP-099** | Read one host's result, empty included | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) | 8.7 | get host's report data |
| **CAP-100** | Get the rows out of Fleet | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) | 6.3 | export query results · import and export queries · fetch results from a scheduled query |
| **CAP-101** | Run something on one platform only | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) | 4.6 | `darwin` · `windows` · `linux` · `chrome` · `macos` (clash: an extension's platform token) · platform selector |
| **CAP-102** | Require a minimum osquery version | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) | 4.6 | minimum osquery version on a report |
| **CAP-103** | Run something on a fraction of hosts | [4.6](../04-know-your-devices/4.6-advanced-osquery-queries-and-tables.md) | 4.2 | shard · canary · ten percent · staged rollout |
| **CAP-104** | Target a report by label | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) | 1.3 | label targeting on a report |
| **CAP-105** | Let observers run a report | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) | 2.6 | `observer_can_run` |
| **CAP-106** | Turn live reporting off | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) | 8.14 | `live_query_disabled` (still accepted) · `live_reporting_disabled` · advanced options |
| **CAP-107** | Stop storing report results | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) | 2.8 | `query_reports_disabled` (still accepted) · `discard_reports_data` |
| **CAP-108** | Stop storing one report's results | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) | 6.2 | `discard_data` |
| **CAP-109** | Find out how many rows Fleet keeps | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) | 4.6, 8.14 | `query_report_cap` (still accepted) · `report_cap` · results truncated |
| **CAP-351** | Retire a legacy 2017 query pack | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) | 6.4 | pack · 2017 pack · retire a pack · migrate packs to reports · `fleetctl upgrade-packs` · `fleetctl convert` · import an osquery pack · disable the old pack |
| **CAP-110** | Find out what a query costs | [4.6](../04-know-your-devices/4.6-advanced-osquery-queries-and-tables.md) | 4.2, 8.14 | performance impact · Undetermined · Minimal · Considerable · Excessive · Denylisted |
| **CAP-111** | Work out why query statistics are empty | [4.6](../04-know-your-devices/4.6-advanced-osquery-queries-and-tables.md) | 8.14 | `enable_scheduled_query_stats` · `app_enable_report_stats` (clash) |
| **CAP-112** | Cap what osquery may consume | [4.6](../04-know-your-devices/4.6-advanced-osquery-queries-and-tables.md) | 8.14 | watchdog · `watchdog_memory_limit` · `watchdog_utilization_limit` · `disable_watchdog` · osquery using too much CPU |
| **CAP-113** | Work out why a query stopped running on some hosts | [4.6](../04-know-your-devices/4.6-advanced-osquery-queries-and-tables.md) | 8.14 | `denylist` · blacklist · `distributed_denylist_duration` |
| **CAP-114** | Ask a pass-or-fail question | [4.3](../04-know-your-devices/4.3-use-policies-for-compliance.md) | 4.2 | policy · compliance check · device health · failing · `created_policy` |
| **CAP-115** | Check whether an application is up to date | [4.3](../04-know-your-devices/4.3-use-policies-for-compliance.md) | 5.4 | patch policy · patch management |
| **CAP-116** | Run a policy on one platform | [4.3](../04-know-your-devices/4.3-use-policies-for-compliance.md) | 4.1 | targeting hosts using platforms |
| **CAP-117** | Run a policy on some hosts only | [4.3](../04-know-your-devices/4.3-use-policies-for-compliance.md) | 1.3 | targeting hosts using labels · exclude hosts from a policy |
| **CAP-118** | Mark a policy important | [4.3](../04-know-your-devices/4.3-use-policies-for-compliance.md) | 5.9 | `critical` |
| **CAP-119** | Count how many hosts are failing | [4.3](../04-know-your-devices/4.3-use-policies-for-compliance.md) | 4.5 | compliance percentage · out-of-policy devices · No hosts are online |
| **CAP-120** | Clear a policy's stored results | [5.9](../05-manage-devices/5.9-automate-remediation-with-policies.md) | 4.3 | `reset_policy` · my policy is stuck · host not updating a policy's response |
| **CAP-121** | Re-arm a policy's automations | [5.9](../05-manage-devices/5.9-automate-remediation-with-policies.md) | 4.3 | reset automations |
| **CAP-122** | List what is installed | [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md) | 4.1 | software inventory · titles · library · managed · Software inventory disabled |
| **CAP-123** | Turn software inventory on for one fleet | [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md) | 6.2 | `features` · `host_settings` (still accepted) |
| **CAP-124** | Find vulnerable software | [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md) | 5.4 | CVE · cves · vulns · CVSS · exploit · security findings · Vulnerabilities are not supported for this type of host |
| **CAP-125** | Find out whether an operating system build is vulnerable | [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md) | 5.6 | OS vulnerabilities · operating systems |
| **CAP-126** | Prioritise by exploitability | [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md) | 5.4 | EPSS · KEV · CISA · known exploited · `cisa_known_exploits_url` |
| **CAP-127** | Sort and filter findings | [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md) | 6.3 | sort by severity · filter by exploited |
| **CAP-128** | Find the version that fixes it | [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md) | 5.4 | resolved version |
| **CAP-129** | See exposure over time | [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md) | 4.5 | vulnerability trend · dashboard vulnerability exposure · charts |
| **CAP-130** | Turn the history chart off | [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md) | 4.5 | `disabled_historical_dataset` |
| **CAP-131** | Find out what Fleet can install for you | [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md) | 5.4 | FMA · Fleet-maintained apps · fleet maintained · app store · google play |
| **CAP-132** | Supply vulnerability data yourself | [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md) |  | air-gapped · offline CVE data · `cpe_database_url` · `cve_feed_prefix_url` · NVD · `fleetctl vulnerability-data-stream` |
| **CAP-133** | Count the estate | [4.5](../04-know-your-devices/4.5-monitor-fleet-wide-state.md) | 1.2 | online · offline · missing · MIA (still accepted) · No hosts match your filters · how does Fleet determine online and offline status · [a.6] |
| **CAP-134** | Count hosts low on disk | [4.5](../04-know-your-devices/4.5-monitor-fleet-wide-state.md) | 6.3 | low disk space |
| **CAP-135** | Find automated enrollments that failed | [4.5](../04-know-your-devices/4.5-monitor-fleet-wide-state.md) | 2.10, 8.8 | failed enrollments · ADE devices failing |
| **CAP-136** | See whether hosts were online last week | [4.5](../04-know-your-devices/4.5-monitor-fleet-wide-state.md) | 4.4 | uptime history |
| **CAP-137** | Hand a host list to somebody | [4.5](../04-know-your-devices/4.5-monitor-fleet-wide-state.md) | 6.3 | export to CSV |
| **CAP-138** | List hosts through the API | [4.5](../04-know-your-devices/4.5-monitor-fleet-wide-state.md) | 6.3 | pagination · `after` key · No more hosts to display |
| **CAP-139** | Be told when hosts go offline | [4.5](../04-know-your-devices/4.5-monitor-fleet-wide-state.md) | 6.5 | host status alerts · missing hosts · notification · host status automations |

### 5. Changing a device

**Writing state, split by the mechanism that carries it.** 107 outcomes, in the three lanes [5.1](../05-manage-devices/5.1-plan-target-and-govern-device-changes.md) teaches: settings that persist, work that runs once, and experiences. If you know which lane you are in, you know which sub-table to scan.

#### Settings that persist

32 outcomes. Profiles, operating system updates and disk encryption: things Fleet keeps true rather than things Fleet does once.

| ID | What you are trying to do | Chapter | Also | Words that lead here |
|---|---|---|---|---|
| **CAP-146** | Push a setting to a Mac | [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) | 3.2 | configuration profile · mobileconfig · custom profiles · `custom_settings` (still accepted) · `configuration_profiles` · OS settings · custom OS settings |
| **CAP-147** | Use Apple's declarative mechanism | [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) | 5.6 | DDM (vendor) · declaration · declarative device management · `profile_uuid` (clash: a declaration carries a profile identifier) · `PayloadScope` · user channel · device channel |
| **CAP-148** | Push a setting to Windows | [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) | 8.9 | OMA-URI (vendor) · LocURI (vendor) · CSP (vendor) · SyncML (vendor) · ADMX (vendor) · Windows configuration profile · CSP converter · migrating Intune policies |
| **CAP-149** | Push a setting to Android | [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) | 2.12 | `android_settings` · Android profile · Android policy · `created_android_profile` |
| **CAP-152** | Put a host's own values into a profile | [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) | 6.2 | Fleet variable · `$FLEET_VAR_` · Variables · built-in variables · put the serial in a profile |
| **CAP-153** | Issue a certificate to a device | [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) | 2.13, 2.12, 8.9 | SCEP · EST · PKI · NDES (vendor) · DigiCert (vendor) · Smallstep (vendor) · Hydrant (vendor) · certificate authority · CA · Certificate enrollment · `certificate-authorities` (clash) · `added_hydrant` · `added_custom_est_proxy` · [a.6] |
| **CAP-154** | Deliver a Platform SSO registration token | [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) | 5.5 | Platform SSO · PSSO · Okta Verify · Entra Platform SSO |
| **CAP-372** | Provision a Mac's local account and sync its password with the identity provider | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) | 5.2 | Platform SSO · PSSO · account provisioning · password sync · OAuth IdP · ROPG · Resource Owner Password Grant · `apple_account_provisioning` · `oauth_idp_token_url` · `fpsso` |
| **CAP-155** | Keep a password out of a spec file | [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) | 6.1 | `$FLEET_SECRET_` · custom variable · secret · `created_custom_variable` |
| **CAP-156** | Read a profile's delivery state | [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) | 8.8, 8.9 | pending · verifying · verified · failed · the profile says failed · configuration profile status |
| **CAP-157** | Push a profile again | [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) | 8.8 | resend · batch-resend · `resent_configuration_profile` |
| **CAP-158** | Remove a profile from a device | [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) | 1.3 | removal behavior · `install` and `remove` · it disappeared from the device |
| **CAP-205** | Require a minimum macOS version by a date | [5.6](../05-manage-devices/5.6-control-operating-system-updates.md) | 5.2 | OS updates · minimum version · deadline · `macos_updates.minimum_version` · `edited_macos_min_version` · `edited_ios_min_version` · `edited_ipados_min_version` · enforce OS updates |
| **CAP-206** | Nag older Macs to update | [5.6](../05-manage-devices/5.6-control-operating-system-updates.md) | 8.2 | Nudge (vendor) |
| **CAP-207** | Set a Windows update deadline | [5.6](../05-manage-devices/5.6-control-operating-system-updates.md) | 5.2 | `windows_updates` · grace period · force a restart · `edited_windows_updates` · Windows Update CSP |
| **CAP-208** | Control Android system updates | [5.6](../05-manage-devices/5.6-control-operating-system-updates.md) | 5.2 | `systemUpdate` (vendor) · freeze period · postpone |
| **CAP-209** | Express what the update form cannot | [5.6](../05-manage-devices/5.6-control-operating-system-updates.md) | 5.2 | custom OS update profile · Fleet-managed updates against custom profiles |
| **CAP-210** | Update newly enrolled Macs during setup | [5.6](../05-manage-devices/5.6-control-operating-system-updates.md) | 3.2 | `enabled_macos_update_new_hosts` · update new hosts to latest |
| **CAP-211** | Force a Linux operating system update | [5.6](../05-manage-devices/5.6-control-operating-system-updates.md) | 4.3 | **(no)** |
| **CAP-212** | Confirm the devices actually updated | [5.6](../05-manage-devices/5.6-control-operating-system-updates.md) | 4.1 | Current versions |
| **CAP-235** | Enforce disk encryption on Macs | [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md) | 3.2 | FileVault · `filevault2` · Disk encryption · Escrow Buddy · `enabled_macos_disk_encryption` · `mdm.macos_settings.enable_disk_encryption` (still accepted) · `mdm.enable_disk_encryption` |
| **CAP-236** | Enforce disk encryption on Windows | [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md) | 3.3 | BitLocker (vendor) · numerical password protector · `mdm.enable_custom_os_updates_and_filevault` (still accepted, clash) |
| **CAP-237** | Escrow a Linux disk encryption key | [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md) | 3.4 | LUKS (vendor) · encrypt your Fleet-managed Linux device · escrow your key with Fleet · `escrowed_disk_encryption_key` |
| **CAP-238** | Escrow on Ubuntu with no prompt | [3.4](../03-connect-devices/3.4-enroll-linux-devices.md) | 5.8 | snapd · headless host |
| **CAP-239** | Have the user type their passphrase | [3.4](../03-connect-devices/3.4-enroll-linux-devices.md) | 5.8 | `cryptsetup` · `zenity` · `kdialog` |
| **CAP-240** | Find out whether a disk is encrypted at all | [3.4](../03-connect-devices/3.4-enroll-linux-devices.md) | 5.8, 4.1 | `disk_encryption_enabled` |
| **CAP-241** | Read disk encryption enforcement state | [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md) | 4.5 | `action_required` · `enforcing` · `removing_enforcement` · disk encryption status |
| **CAP-242** | Require a BitLocker startup PIN | [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md) |  | `windows_require_bitlocker_pin` · BitLocker PIN enforcement |
| **CAP-243** | Use your own encryption profile instead | [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md) | 5.2 | `mdm.enable_custom_filevault` · `mdm.enable_custom_disk_encryption` · escape hatch |
| **CAP-244** | Set and read a firmware password on Apple silicon | [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md) | 1.4 | Recovery Lock · `laps` · rotation · Show Recovery Lock password · `viewed_host_recovery_lock_password` · `rotated_host_recovery_lock_password` |
| **CAP-371** | Have Fleet rotate an undecryptable FileVault recovery key on its own | [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md) | 4.5 | Escrow Buddy · `RotateDiskEncryptionKey` · `setDiskEncryptionNotifications` · key repair · undecryptable key |
| **CAP-245** | Stop enforcing encryption without losing the keys | [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md) | 7.2 | disable enforcement |

#### Work that runs once

54 outcomes. Scripts, software installs and device actions: a single unit of work, queued, delivered and finished.

| ID | What you are trying to do | Chapter | Also | Words that lead here |
|---|---|---|---|---|
| **CAP-159** | Run a script on a host | [5.3](../05-manage-devices/5.3-run-and-manage-scripts.md) | 5.1 | remote shell · powershell · bash · remediate · Run script · `ran_script` |
| **CAP-160** | Keep a library of scripts | [5.3](../05-manage-devices/5.3-run-and-manage-scripts.md) | 6.2 | script library · saved · uploaded · `added_script` |
| **CAP-161** | Wait for a script to finish | [5.3](../05-manage-devices/5.3-run-and-manage-scripts.md) | 6.4 | `fleetctl run-script` · synchronous · `--async` |
| **CAP-162** | Run a script across many hosts | [5.3](../05-manage-devices/5.3-run-and-manage-scripts.md) | 6.1, 1.5 | batch script · Run script on many hosts · script batch progress · `ran_script_batch` · `scheduled_script_batch` · `canceled_script_batch` |
| **CAP-163** | Turn scripts off everywhere | [5.3](../05-manage-devices/5.3-run-and-manage-scripts.md) | 2.7 | `scripts_disabled` · Running scripts is disabled in organization settings |
| **CAP-164** | Change the script timeout | [5.3](../05-manage-devices/5.3-run-and-manage-scripts.md) | 1.3 | `script_execution_timeout` · my script times out at five minutes |
| **CAP-165** | Read what a script printed | [5.3](../05-manage-devices/5.3-run-and-manage-scripts.md) | 8.4 | exit code · output truncated |
| **CAP-166** | Keep a password out of a script | [5.3](../05-manage-devices/5.3-run-and-manage-scripts.md) | 6.1 | secret in a script |
| **CAP-167** | Use a host's own values inside an install script | [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) | 5.3 | `$FLEET_HOST_VITAL_` |
| **CAP-168** | Deploy an installer you supply | [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) | 6.2 | upload a package · Add software · custom package · pkg · msi · exe · deb · rpm · `added_software` · EXE install scripts |
| **CAP-169** | Install an application Fleet maintains | [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) | 4.4 | FMA · Fleet-maintained app · fleet maintained · install Chrome for me |
| **CAP-170** | Install an App Store application | [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) | 2.10 | VPP app (vendor) · volume purchase · app store · `added_app_store_app` · `installed_app_store_app` |
| **CAP-171** | Install a Play application | [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) | 2.12 | google play · play store · Android app · private app · APK · Android MDM isn't enabled |
| **CAP-172** | Deploy an application Apple did not distribute | [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) | 3.5 | in-house app (vendor) · sideload · enterprise app · `ipa` |
| **CAP-173** | Put a shortcut on an Android home screen | [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) | 5.5 | Android web app |
| **CAP-174** | Ship a shell script as software | [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) | 5.3 | script-only package |
| **CAP-175** | Install only when a condition holds | [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) | 4.2 | pre-install query · conditional install |
| **CAP-176** | Use the install and uninstall scripts Fleet writes | [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) | 5.3 | install script · post-install script · uninstall script · generated script |
| **CAP-177** | Install software on one host | [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) | 5.1, 8.11 | `installed_software` · Library tab · it says installed and it is not there |
| **CAP-178** | Remove software from a host | [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) | 8.11 | uninstall · `uninstalled_software` · uninstall by source |
| **CAP-352** | Retry a failed software install or uninstall by hand | [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) | 8.11 | Retry · Retry uninstall · retry a failed install · re-send an install · manual retry · resets the automatic retry budget · forcing action |
| **CAP-179** | Ship different builds per architecture | [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) | 1.3 | arm64 · x86 · Apple silicon and Intel |
| **CAP-180** | Hold an application at a version | [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) | 4.3 | pin a version |
| **CAP-181** | Keep applications current | [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) | 4.3 | automatic updates |
| **CAP-182** | Go back to an earlier version | [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) | 8.11 | roll back to a previous version |
| **CAP-183** | Configure an application on an iPhone | [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) | 5.2 | managed app config · app configuration |
| **CAP-184** | Configure an application on Android | [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) | 2.12 | Android Managed App Configurations · Work Profile Widgets |
| **CAP-185** | Choose when applications update | [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) | 5.6 | app update window · configure automatic updates for an app |
| **CAP-186** | Delete software from the library | [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) | 6.2 | `deleted_software` · `deleted_app_store_app` |
| **CAP-187** | Speed up installer downloads | [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) | 2.3 | CDN · CloudFront signed URLs |
| **CAP-188** | Find the installer size limit | [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) | 8.14 | too big · 10 GiB |
| **CAP-213** | Lock a Mac | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) | 3.2 | Lock · remote lock · `locked_host` · lock and wipe hosts |
| **CAP-214** | Lock an iPhone or iPad | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) | 3.5 | Lost Mode (vendor) · find my iPad |
| **CAP-215** | Lock a Windows host | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) | 5.3 | lock a PC |
| **CAP-216** | Lock a Linux host | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) | 3.4 | lock a Linux desktop |
| **CAP-217** | Lock an Android device | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) | 3.6 | lock a phone |
| **CAP-218** | Unlock a Mac | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) | 5.8 | Unlock · unlock PIN · `unlocked_host` |
| **CAP-219** | Unlock an iPhone or iPad | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) | 3.5 | release Lost Mode (vendor) · unlock offline iOS hosts |
| **CAP-220** | Unlock a Windows host | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) | 5.3 | unlock a PC |
| **CAP-221** | Unlock a Linux host | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) | 3.4 | unlock a Linux desktop |
| **CAP-222** | Unlock an Android device | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) | 3.6 | **(no)** |
| **CAP-223** | Wipe a Mac | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) | 3.2 | Wipe · erase · remote wipe · `wiped_host` · `failed_wipe` |
| **CAP-224** | Wipe an iPhone or iPad | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) | 3.5 | erase an iPad |
| **CAP-225** | Wipe a Windows host | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) | 8.9 | OMA-DM (vendor) · remote wipe a PC |
| **CAP-226** | Wipe a Linux host | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) | 3.4 | secure erase |
| **CAP-227** | Wipe an Android device | [3.6](../03-connect-devices/3.6-enroll-android-devices.md) | 5.7 | erase a phone |
| **CAP-228** | Wipe a personally owned Android device | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) | 3.6 | unenroll · remove the work profile |
| **CAP-229** | Locate a device | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) | 3.5 | find my device · Apple device location |
| **CAP-230** | Clear a passcode | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) | 3.5, 3.6 | Clear passcode · forgotten PIN · `cleared_passcode` · `fleetctl mdm clear-passcode` · `clear_passcode` |
| **CAP-370** | Turn MDM off for one host, independent of the platform-wide switch | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) | 2.12 | Turn off MDM · Unenroll · `UnenrollMDM` · `mdmUnenrollEndpoint` |
| **CAP-231** | Send a payload Fleet has no button for | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) | 6.4 | custom MDM command · raw Apple command · `fleetctl mdm run-command` · `run_command` · `/fleet/mdm/apple/enqueue` (still accepted) · `/mdm/commands/run` |
| **CAP-232** | Send a raw Windows command | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) | 8.9 | SyncML Exec (vendor) · raw Windows MDM command |
| **CAP-233** | Read what the device said back | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) | 8.8, 8.9 | command results · `fleetctl get mdm-command-results` · `mdm_command_results` · `/fleet/mdm/apple/commandresults` (still accepted) |
| **CAP-234** | Stop something before it runs | [5.1](../05-manage-devices/5.1-plan-target-and-govern-device-changes.md) | 5.7, 6.1 | cancel · upcoming activity · `canceled_run_script` · `canceled_install_software` |

#### Experiences

21 outcomes. What the person holding the device sees, at first boot and afterwards.

| ID | What you are trying to do | Chapter | Also | Words that lead here |
|---|---|---|---|---|
| **CAP-189** | Design what happens at first boot | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) | 3.2, 2.10 | setup experience · onboarding · first run · customize · `macos_setup` (still accepted) · `setup_experience` |
| **CAP-190** | Run a script during setup | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) | 5.3 | Run script · post-enrollment · shell |
| **CAP-191** | Install something before the agent exists | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) | 1.6 | bootstrap package · `bootstrap_package` (still accepted) · `macos_bootstrap_package` · `added_bootstrap_package` |
| **CAP-192** | Create the end user's account | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) | 5.8 | LAPS (vendor) · managed local account · standard against admin account · `enable_managed_local_account` (still accepted) · `enable_create_local_admin_account` · secure local admin passwords |
| **CAP-353** | Retrieve or rotate the managed local administrator password | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) | 5.8, 1.5 | reveal the managed local admin password · rotate the `_fleetadmin` password · LAPS password (vendor) · `read_managed_local_account` · view-triggered rotation · distinct from creating the account (CAP-192) |
| **CAP-193** | Show an agreement at enrollment | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) | 2.5 | EULA · end user license agreement · `/fleet/mdm/setup/eula` (still accepted) |
| **CAP-194** | Hold a Windows host at first boot | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) | 8.9 | ESP (vendor) · Enrollment Status Page (vendor) · OOBE (vendor) · Windows updates during Autopilot |
| **CAP-195** | Show the setup page outside first boot, and on Linux | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) | 8.2 | Windows and Linux setup experience |
| **CAP-196** | Install applications during an iPhone's setup | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) | 3.5 | App Store apps in setup experience |
| **CAP-197** | Push an application to Android at enrollment | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) | 5.4 | Android setup software |
| **CAP-198** | Install setup software only where it is needed | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) | 4.3 | policy gate · conditional setup software |
| **CAP-199** | Stop setup when software fails | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) | 8.9 | cancel setup if software fails |
| **CAP-200** | Release the device yourself | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) | 3.2 | `enable_release_device_manually` (still accepted) · `apple_enable_release_device_manually` · stop the automatic release · release-ready (ours) |
| **CAP-201** | Retry a setup step that failed | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) | 8.11 | `canceled_setup_experience` · retry |
| **CAP-202** | Let people install applications themselves | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) | 5.4 | self-service · self service · app catalog · software library · web clip |
| **CAP-203** | Group the self-service catalogue | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) | 6.2 | self-service categories · End user experience · `added_self_service_category` |
| **CAP-204** | Offer everything in a category at once | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) | 8.11 | Install all · `installed_all_self_service_software` |
| **CAP-361** | Let an end user see their own device's details and software | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) | 4.1 | My Device page · device summary as the end user sees it |
| **CAP-362** | Let an end user see the summary the desktop menu shows | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) |  | Fleet Desktop menu-bar item · tray icon summary |
| **CAP-365** | Let an end user uninstall their own software | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) | 5.4 | self-service uninstall · Uninstall button on My Device |
| **CAP-366** | Choose whether a Play application is offered as self-service | [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) |  | Android self-service toggle · Play app self-service setting |

### 6. Automating Fleet

**Making Fleet, or another system, act without a person.** 24 outcomes.

| ID | What you are trying to do | Chapter | Also | Words that lead here |
|---|---|---|---|---|
| **CAP-246** | Install software when a policy fails | [5.9](../05-manage-devices/5.9-automate-remediation-with-policies.md) | 4.3, 5.4 | self-healing · software automations · automatic software install · templates for policy queries |
| **CAP-247** | Install an App Store application on failure | [5.9](../05-manage-devices/5.9-automate-remediation-with-policies.md) | 5.4 | VPP automation (vendor) |
| **CAP-248** | Run a script when a policy fails | [5.9](../05-manage-devices/5.9-automate-remediation-with-policies.md) | 5.3 | policy automation run script · remediate |
| **CAP-249** | Call a webhook when hosts fail a policy | [5.9](../05-manage-devices/5.9-automate-remediation-with-policies.md) | 6.5 | `failing_policies_webhook` · webhooks and tickets · `ran_automation_webhook` |
| **CAP-250** | Open a ticket when hosts fail a policy | [5.9](../05-manage-devices/5.9-automate-remediation-with-policies.md) | 6.5 | Jira (vendor) · Zendesk (vendor) · Ticketing · `ticket-destinations` (clash) · `jira` · `zendesk` · `ran_automation_ticket` |
| **CAP-251** | Put remediation in the user's calendar | [5.9](../05-manage-devices/5.9-automate-remediation-with-policies.md) | 6.5 | maintenance window · Calendar events · `google_calendar` · `ran_automation_calendar_event` |
| **CAP-252** | Block sign-in for a non-compliant device | [5.9](../05-manage-devices/5.9-automate-remediation-with-policies.md) | 2.5 | conditional access · zero trust · Entra compliance · Company Portal (vendor) · `added_conditional_access_integration_microsoft` |
| **CAP-253** | Block sign-in through Okta | [5.9](../05-manage-devices/5.9-automate-remediation-with-policies.md) | 2.5 | Okta conditional access · mTLS proxy · `added_conditional_access_okta` |
| **CAP-254** | Let one person through once | [5.9](../05-manage-devices/5.9-automate-remediation-with-policies.md) | 2.6 | bypass · per-policy bypass · `update_conditional_access_bypass` · `host_bypassed_conditional_access` |
| **CAP-255** | Keep an automation firing rather than firing once | [5.9](../05-manage-devices/5.9-automate-remediation-with-policies.md) | 4.3 | `continuous_automations_enabled` · continuous · transition-based (ours) · re-fire (ours) |
| **CAP-256** | Call a webhook on a new vulnerability | [6.5](../06-automate-fleet/6.5-integrations-webhooks-and-external-workflows.md) | 4.4 | `vulnerabilities_webhook` · vulnerability automations |
| **CAP-257** | Send osquery logs somewhere | [2.8](../02-administer-and-deploy-fleet/2.8-activity-audit-logs-and-log-delivery.md) | 6.5 | log plugin · `osquery.status_log_file` (still accepted) · `osquery.result_log_file` (still accepted) · `filesystem.*` · `logger_path` (clash) · `logger_plugin` |
| **CAP-258** | Stop webhooks reaching internal addresses | [6.5](../06-automate-fleet/6.5-integrations-webhooks-and-external-workflows.md) | 2.2 | SSRF · outbound webhook restrictions |
| **CAP-259** | Manage Fleet from a repository | [6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md) | 6.1 | GitOps · declarative config · `team_settings` (still accepted) · `queries` (still accepted) · `kind: team` (still accepted) · `kind: query` (still accepted) · `kind: fleet` · `kind: report` · preventing mistakes with GitOps |
| **CAP-260** | Validate before applying | [6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md) | 6.4 | dry run · `--dry-run` |
| **CAP-261** | Delete fleets that are not in the repository | [6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md) | 6.4 | `--delete-other-teams` (still accepted) · `--delete-other-fleets` · `DELETE_OTHER_TEAMS` (still accepted) · `DELETE_OTHER_FLEETS` |
| **CAP-262** | Find out whether omitting a section deletes it | [6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md) | 2.7 | change management exceptions · `enabled_gitops_exception` · deprecation warnings in GitOps |
| **CAP-263** | Export a running deployment to YAML | [6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md) | 6.4 | `fleetctl generate-gitops` · `--team no-team` (still accepted) · `--fleet unassigned` · migrating to GitOps |
| **CAP-264** | Call the API | [6.3](../06-automate-fleet/6.3-use-the-fleet-rest-api.md) | 6.1, 2.6 | REST API · `/api/v1/osquery/*` (still accepted) · `/api/osquery/*` · retrieve your API token · fleetctl against the REST API against the UI |
| **CAP-265** | Use the command line | [6.4](../06-automate-fleet/6.4-use-fleetctl.md) | 6.3 | `fleetctl` · a.7 owns the command contract |
| **CAP-266** | Call an endpoint the command line has no verb for | [6.4](../06-automate-fleet/6.4-use-fleetctl.md) | 6.3 | `fleetctl api` |
| **CAP-267** | Push or delete spec files | [6.4](../06-automate-fleet/6.4-use-fleetctl.md) | 6.2 | `fleetctl apply` · `fleetctl delete` · `--policies-team` (still accepted) · `--policies-fleet` |
| **CAP-268** | Generate a pipeline for Fleet | [6.4](../06-automate-fleet/6.4-use-fleetctl.md) | 6.2 | `fleetctl new` · GitHub Action · CI scaffold |
| **CAP-354** | Connect an AI assistant to Fleet | [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md) | 6.3, 2.6 | MCP · Model Context Protocol · Fleet MCP server · AI assistant · Claude (vendor) · Cursor (vendor) · `fleet-mcp` · natural-language queries · live query from an assistant |

### 7. Running the service

**Deploying, upgrading, backing up, sizing, monitoring, and keeping credentials alive.** 46 outcomes. The credentials are here rather than in group 2 because a token is a connection task once and a renewal task every year after that, and it is the renewal you arrive searching for.

| ID | What you are trying to do | Chapter | Also | Words that lead here |
|---|---|---|---|---|
| **CAP-270** | Renew the Apple push certificate | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) | 7.6 | APNs · push certificate expired · renew APNs · APNs expiration |
| **CAP-271** | Understand how host certificates renew themselves | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) | 8.8 | `mdm.apple_scep_signer_validity_days` · SCEP renewal |
| **CAP-373** | Require hardware-attested device identity for eligible Macs | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) | 3.2 | ACME · Managed Device Attestation · hardware attestation · Secure Enclave · `apple_require_hardware_attestation` · attested identity |
| **CAP-273** | Renew the Apple Business token | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) | 7.6 | ABM token expired · AB token · renew AB · `/fleet/abm_tokens/{id}/renew` (still accepted) |
| **CAP-274** | Customise what Setup Assistant shows | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) | 5.5 | `macos_setup_assistant` (still accepted) · `apple_setup_assistant` · `changed_macos_setup_assistant` |
| **CAP-276** | Renew the Apps and Books token | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) | 7.6 | VPP token (vendor) · renew VPP · `enabled_vpp` |
| **CAP-277** | Be warned before a credential expires | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) | 7.6 | expiry banner · certificate expiration monitoring |
| **CAP-280** | Turn Windows MDM off | [2.11](../02-administer-and-deploy-fleet/2.11-configure-windows-management.md) | 3.3 | `disabled_windows_mdm` |
| **CAP-284** | Turn Android management off | [2.12](../02-administer-and-deploy-fleet/2.12-bind-android-enterprise.md) | 3.6 | Turn off Android MDM · delete Android Enterprise · `disabled_android_mdm` |
| **CAP-285** | Change the Fleet server address | [2.7](../02-administer-and-deploy-fleet/2.7-organization-and-server-settings.md) | 2.12, 2.1 | Fleet web address · `server_url` · `kolide_server_url` (still accepted) · apple mdm server url · migrate hosts from one Fleet server to another |
| **CAP-286** | Run Fleet under a path | [2.7](../02-administer-and-deploy-fleet/2.7-organization-and-server-settings.md) | 2.2 | `url_prefix` · `server_url_prefix` (clash) |
| **CAP-287** | Let administrators sign in at a different address | [2.7](../02-administer-and-deploy-fleet/2.7-organization-and-server-settings.md) | 2.5 | `sso_server_url` · sso user url |
| **CAP-288** | Brand the interface | [2.7](../02-administer-and-deploy-fleet/2.7-organization-and-server-settings.md) | 6.2 | `org_info` · Organization info · `org_logo_url` (still accepted) · `org_logo_url_dark_mode` · `org_logo_url_light_background` (still accepted) · `org_logo_url_light_mode` · `changed_org_logo` |
| **CAP-289** | Point error messages at your help desk | [2.7](../02-administer-and-deploy-fleet/2.7-organization-and-server-settings.md) | 5.5 | `contact_url` |
| **CAP-295** | Choose where scheduled results go | [2.8](../02-administer-and-deploy-fleet/2.8-activity-audit-logs-and-log-delivery.md) | 4.2 | `osquery_result_log_plugin` · `osquery.result_log_file` (still accepted) · Firehose · Kinesis · Lambda · Pub/Sub · Kafka · log destinations |
| **CAP-296** | Choose where agent status logs go | [2.8](../02-administer-and-deploy-fleet/2.8-activity-audit-logs-and-log-delivery.md) | 8.2 | `osquery_status_log_plugin` · what happens when the logging destination is offline |
| **CAP-299** | Check whether Fleet is up | [7.4](../07-operate-fleet/7.4-observe-progress-and-service-health.md) | 2.2 | `healthz` · health check · how do I monitor a Fleet server |
| **CAP-300** | Scrape Fleet's metrics | [7.4](../07-operate-fleet/7.4-observe-progress-and-service-health.md) | 2.2 | Prometheus · metrics endpoint |
| **CAP-301** | Export traces | [7.4](../07-operate-fleet/7.4-observe-progress-and-service-health.md) | 8.14 | OpenTelemetry · traces |
| **CAP-302** | Monitor the freshness of schedule-produced state | [7.4](../07-operate-fleet/7.4-observe-progress-and-service-health.md) | 8.6, 8.11 | scheduled jobs · schedule freshness · is the data a schedule maintains current · service health · observe progress |
| **CAP-303** | Force a schedule to run now | [7.4](../07-operate-fleet/7.4-observe-progress-and-service-health.md) | 8.11 | `fleetctl trigger` · trigger a cron |
| **CAP-304** | Upgrade Fleet | [7.3](../07-operate-fleet/7.3-upgrade-fleet-and-fleetd.md) | 2.4 | run migrations · `fleet prepare db` · `upgrades.allow_missing_migrations` · `updates.allow_missing_migrations` (clash) · `--upgrades_allow_missing_migrations` · skip versions · unknown column error |
| **CAP-305** | Check whether migrations are current | [7.3](../07-operate-fleet/7.3-upgrade-fleet-and-fleetd.md) | 8.5 | `fleetctl debug migrations` |
| **CAP-306** | Back Fleet up and restore it | [7.2](../07-operate-fleet/7.2-back-up-and-restore-service-state.md) | 7.7 | disaster recovery · point-in-time recovery · migrate Fleet server · **(no)** |
| **CAP-307** | Prove a restored Fleet can still decrypt the keys | [7.2](../07-operate-fleet/7.2-back-up-and-restore-service-state.md) | 5.8 | server private key · escrow chain |
| **CAP-308** | Stop a restored copy acting on the real world | [7.2](../07-operate-fleet/7.2-back-up-and-restore-service-state.md) | 7.1 | read-only mode · dry-run server · **(no)** |
| **CAP-309** | Find out when the licence expires | [7.6](../07-operate-fleet/7.6-maintain-credentials-certificates-and-access.md) | 2.1 | licence key · `basic` (still accepted) · `premium` · migrate from Fleet Free to Fleet Premium · downgrade from Premium |
| **CAP-310** | Rotate the server's TLS certificate | [7.6](../07-operate-fleet/7.6-maintain-credentials-certificates-and-access.md) | 7.7 | certificate verify failed · private root · change the Fleet server TLS certificate |
| **CAP-311** | Rotate the Windows enrollment certificate | [7.6](../07-operate-fleet/7.6-maintain-credentials-certificates-and-access.md) | 2.11 | WSTEP · `mdm.windows_wstep_identity_cert_bytes` (clash: Fleet's documentation attributes the effect to macOS) |
| **CAP-312** | Rotate an integration secret | [7.6](../07-operate-fleet/7.6-maintain-credentials-certificates-and-access.md) | 6.5 | |
| **CAP-314** | Size the database connection pool | [2.2](../02-administer-and-deploy-fleet/2.2-self-hosting-architecture-and-capacity.md) | 7.5 | `mysql.max_open_conns` · too many connections · database connection error when preparing the database · MySQL user requirements |
| **CAP-315** | Add read replicas | [7.5](../07-operate-fleet/7.5-maintain-capacity-and-availability.md) | 2.2 | MySQL replication · scale MySQL |
| **CAP-316** | Decide where installers and carves live | [2.2](../02-administer-and-deploy-fleet/2.2-self-hosting-architecture-and-capacity.md) | 1.6, 2.3 | S3 · GCS · object storage · `s3.bucket` (still accepted) · `s3.prefix` (still accepted) · `s3.region` (still accepted) · `s3.carves_*` |
| **CAP-317** | Send Fleet's outbound traffic through a proxy | [2.2](../02-administer-and-deploy-fleet/2.2-self-hosting-architecture-and-capacity.md) | 8.13 | `HTTP_PROXY` · `NO_PROXY` · using a proxy · public IPs of devices |
| **CAP-350** | Enumerate every outbound destination Fleet reaches | [2.2](../02-administer-and-deploy-fleet/2.2-self-hosting-architecture-and-capacity.md) | 8.13, 6.5 | egress map · egress destinations · firewall review · what leaves Fleet · which addresses Fleet calls · outbound allow-list · built-in and configured destinations |
| **CAP-318** | Deploy on AWS | [2.3](../02-administer-and-deploy-fleet/2.3-deploy-on-aws-or-gcp.md) | 2.2 | ECS · Terraform · reference architecture |
| **CAP-319** | Deploy on GCP, or ask about Azure | [2.3](../02-administer-and-deploy-fleet/2.3-deploy-on-aws-or-gcp.md) | 2.2 | Cloud Run · Cloud SQL · Azure |
| **CAP-320** | Avoid storing a key for the bucket | [2.3](../02-administer-and-deploy-fleet/2.3-deploy-on-aws-or-gcp.md) | 2.2 | workload identity |
| **CAP-321** | Run Fleet with Docker Compose | [2.4](../02-administer-and-deploy-fleet/2.4-deploy-with-containers-or-virtual-machines.md) | 7.3 | easiest way to deploy Fleet · Docker container |
| **CAP-322** | Run Fleet on Kubernetes | [2.4](../02-administer-and-deploy-fleet/2.4-deploy-with-containers-or-virtual-machines.md) | 7.3 | Helm chart · pre-upgrade hook |
| **CAP-323** | Run Fleet on a virtual machine | [2.4](../02-administer-and-deploy-fleet/2.4-deploy-with-containers-or-virtual-machines.md) | 7.3 | systemd · run with systemd |
| **CAP-324** | Move vulnerability processing off the serving instances | [2.4](../02-administer-and-deploy-fleet/2.4-deploy-with-containers-or-virtual-machines.md) | 4.4 | dedicated cron instance · `vulnerabilities.disable_schedule` |
| **CAP-325** | Find out how many hosts Fleet takes | [7.5](../07-operate-fleet/7.5-maintain-capacity-and-availability.md) | 2.2 | load test · `osquery-perf` · stress test · Fleet server performance |
| **CAP-326** | Drain an instance before stopping it | [7.5](../07-operate-fleet/7.5-maintain-capacity-and-availability.md) | 7.3 | graceful shutdown |
| **CAP-327** | Shut Fleet down for good | [7.8](../07-operate-fleet/7.8-retire-a-fleet-deployment.md) | 7.7 | decommission · release devices · release external assignments |
| **CAP-328** | Ask whether Fleet can host it for you | [2.1](../02-administer-and-deploy-fleet/2.1-administration-model-and-deployment-choices.md) | 2.8 | managed cloud · SaaS · can you host Fleet for me |

### 8. When it did not work

**Symptoms, and the surfaces that answer them.** 21 outcomes, plus the sentences people actually arrive with. This is the group that cannot be reconstructed from the table of contents, because nobody types a capability name when something is broken.

#### Sentences people type

![Troubleshooting](../_assets/icons/troubleshooting.svg) **Every sentence below is a string Fleet prints, a question Fleet's own documentation asks, or a phrasing this manual records.** The middle column is the ambiguity to resolve, not the fix.

| The sentence you arrive with | What it turns on | Start at |
|---|---|---|
| "my hosts went offline", "everything shows offline", "my computer is showing up as an offline host" | The online window is calculated from the agent's own reporting interval, and a mobile device managed without an agent is permanently offline | [4.5](../04-know-your-devices/4.5-monitor-fleet-wide-state.md), then [8.1](../08-troubleshooting/8.1-diagnostic-method.md) |
| "no hosts match your filters", "I expected to see more hosts than this" | Pagination, scope, or a parameter your licence causes Fleet to drop rather than refuse | [4.5](../04-know-your-devices/4.5-monitor-fleet-wide-state.md) |
| "the profile says failed", "stuck on pending", "stuck verifying" | Which of the five delivery states you are in, and that Verifying means accepted rather than confirmed | [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md), then [8.8](../08-troubleshooting/8.8-apple-mdm-diagnostics.md) or [8.9](../08-troubleshooting/8.9-windows-mdm-diagnostics.md) |
| "the app will not install", "it says installed and it is not there" | Installed means four different things depending on where the software came from | [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) |
| "why aren't my DDM declarations applying to devices?" | Declarations are delivered on a different mechanism from profiles and report their state differently | [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md), then [8.8](../08-troubleshooting/8.8-apple-mdm-diagnostics.md) |
| "nothing to report yet", "collecting results", "no results returned" | The report never joined a schedule, or result storage is off | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) |
| "where are my query results?", "why aren't my live queries being logged?" | Stored reports and forwarded results are two different destinations with two different switches | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md), then [2.8](../02-administer-and-deploy-fleet/2.8-activity-audit-logs-and-log-delivery.md) |
| "why does my query work locally with osquery but not in Fleet?" | Which osquery is running it, with which flags and which tables | [8.7](../08-troubleshooting/8.7-live-query-introspection.md), then [4.6](../04-know-your-devices/4.6-advanced-osquery-queries-and-tables.md) |
| "I'm only getting partial results from live queries" | The targeted count includes hosts that never fetch the query | [8.14](../08-troubleshooting/8.14-degradation.md), then [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) |
| "running scripts is disabled in organization settings" | `scripts_disabled` at the organization, or a host packaged without scripts | [5.3](../05-manage-devices/5.3-run-and-manage-scripts.md) |
| "software inventory disabled" | The organization's feature block, or the fleet's | [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md) |
| "vulnerabilities are not supported for this type of host" | Application findings are not produced for every platform | [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md) |
| "unable to detect MDM enrollment", "no MDM solutions detected" | A dashboard card describing the estate, not the host you are looking at | [4.5](../04-know-your-devices/4.5-monitor-fleet-wide-state.md) |
| "access denied", "api only user" | A role, a scope, GitOps mode, or a password reset Fleet is waiting on | [1.4](../01-foundations/1.4-identity-and-roles.md), then [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md) |
| "this fleet isn't added to Volume Purchasing Program (VPP)" | The token exists and is not assigned to this scope | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) |
| "no hosts are online", on a policy's results | Live evaluation needs hosts that are online now, not hosts that have ever answered | [4.3](../04-know-your-devices/4.3-use-policies-for-compliance.md) |
| "MDM is on but the agent never arrived", "half-enrolled" | One channel enrolled and the other did not | [8.4](../08-troubleshooting/8.4-host-side-investigation.md) |
| "why aren't my osquery agents connecting to Fleet?" | Which hop failed: address, certificate, secret, or the agent's own service | [8.4](../08-troubleshooting/8.4-host-side-investigation.md), then [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md) |
| "certificate verify failed", from the agent | The chain the agent trusts, and the order a rotation has to happen in | [7.6](../07-operate-fleet/7.6-maintain-credentials-certificates-and-access.md), then [8.4](../08-troubleshooting/8.4-host-side-investigation.md) |
| "my EDR is flagging the fleetd agent" | Agent packaging and signing | [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md), then [8.4](../08-troubleshooting/8.4-host-side-investigation.md) |
| "what is duplicate enrollment, and how do I fix it?" | The host identifier, and the cooldown | [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md), then [8.14](../08-troubleshooting/8.14-degradation.md) |
| "I renamed a label and the targeting broke" | A rename through a repository deletes and recreates | [1.3](../01-foundations/1.3-hosts-fleets-labels.md) |
| "the recovery key will not reveal", "encryption keys unreadable" | A Windows enrollment certificate change, a fleet transfer, or Apple MDM being turned off | [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md), then [7.6](../07-operate-fleet/7.6-maintain-credentials-certificates-and-access.md) |
| "the automation saved and never fired" | Ticketing reads its policy list from the webhook settings, and calendar automation needs a named fleet | [5.9](../05-manage-devices/5.9-automate-remediation-with-policies.md) |
| "it says success and nothing happened" | Several operations report before the destructive phase, or ignore part of what you sent | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md), then [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) |
| "the estate stopped updating and nothing said so" | An agent below the floor ignores the central channel setting | [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md) |
| "I set it in the API and it did nothing" | Two per-fleet agent settings are accepted by the API and applied only from a repository | [4.7](../04-know-your-devices/4.7-extend-osquery-with-custom-tables-and-plugins.md) |
| "why is my host not updating a policy's response?" | When a policy is evaluated, and what resets a stored answer | [4.3](../04-know-your-devices/4.3-use-policies-for-compliance.md), then [5.9](../05-manage-devices/5.9-automate-remediation-with-policies.md) |
| "why am I getting errors generating a .msi package", "package root files: heat failed" | The build host has to match the package type | [3.3](../03-connect-devices/3.3-enroll-windows-devices.md) |
| "how do I resolve an unknown column error when upgrading Fleet?" | Migrations ran partially, or not at all | [7.3](../07-operate-fleet/7.3-upgrade-fleet-and-fleetd.md) |
| "what do I do about too many open files errors?" | A limit on the server rather than a Fleet setting | [8.14](../08-troubleshooting/8.14-degradation.md) |
| "what happens if a device fails to enroll during first boot?" | Which of the setup steps failed, and whether the device was released | [3.2](../03-connect-devices/3.2-enroll-macos-devices.md), then [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) |
| "it isn't working", "one host, never reproduced", "Fleet's UI disagrees with the host", "cron output missing", "profile stays at Pending indefinitely and no error surfaces anywhere" | What to collect before you ask anybody else | [8.13](../08-troubleshooting/8.13-escalation.md) |

#### The diagnostic capabilities

| ID | What you are trying to do | Chapter | Also | Words that lead here |
|---|---|---|---|---|
| **CAP-329** | Find the agent's logs on the host | [8.2](../08-troubleshooting/8.2-log-surfaces.md) | 8.4 | orbit log · osqueryd log · finding fleetd logs · `logger_path` (clash) |
| **CAP-330** | Find out what the agent puts on disk | [8.2](../08-troubleshooting/8.2-log-surfaces.md) | 8.4 | `/opt/orbit` · `secret.txt` · `fleet.pem` |
| **CAP-363** | Open an interactive query shell on the host itself | [8.4](../08-troubleshooting/8.4-host-side-investigation.md) |  | `orbit shell` · `orbit osqueryi` · interactive osquery shell · local osquery shell |
| **CAP-331** | Turn debug logging on for a while | [8.2](../08-troubleshooting/8.2-log-surfaces.md) | 8.4 | `debug_logging_on_enroll_duration` · `debug_logging` |
| **CAP-332** | Turn verbose logging on permanently | [8.2](../08-troubleshooting/8.2-log-surfaces.md) | 8.4 | `--debug` · `--verbose` · enabling debug mode for fleetd |
| **CAP-333** | Collect diagnostics for support | [8.5](../08-troubleshooting/8.5-fleetctl-debug.md) | 8.13 | `fleetctl debug archive` · `db-process-list` · pprof · [a.6] |
| **CAP-334** | Read the server's recorded errors | [8.5](../08-troubleshooting/8.5-fleetctl-debug.md) | 1.6 | `fleetctl debug errors` · get errors |
| **CAP-335** | Ask a host what osquery is doing | [8.7](../08-troubleshooting/8.7-live-query-introspection.md) | 4.6 | `osquery_info` · `osquery_flags` · `osquery_schedule` · `osquery_events` · `fleetd_logs` |
| **CAP-336** | Inspect the Apple command queue | [8.8](../08-troubleshooting/8.8-apple-mdm-diagnostics.md) | 8.6 | nano tables · checking MDM commands · `fleetctl get mdm-commands` · `mdm_commands` |
| **CAP-337** | Inspect the Windows command queue | [8.9](../08-troubleshooting/8.9-windows-mdm-diagnostics.md) | 8.6 | Windows command feed |
| **CAP-338** | Inspect Android command and policy state | [8.10](../08-troubleshooting/8.10-android-diagnostics.md) | 8.6 | Android policy state |
| **CAP-339** | Read the audit record out of the database | [8.12](../08-troubleshooting/8.12-audit-logs.md) | 1.5 | `activity_past` · `activities` (clash) · `host_only` |
| **CAP-340** | Inspect `cron_stats` for whether a named schedule ran | [8.6](../08-troubleshooting/8.6-server-state.md) | 7.4, 8.11 | `cron_stats` · did the schedule run · which schedule last ran · `dep_syncer` (clash) · `apple_mdm_dep_profile_assigner` |
| **CAP-341** | Read Windows' own view of its management state | [8.9](../08-troubleshooting/8.9-windows-mdm-diagnostics.md) | 5.6 | `mdmdiagnosticstool` (vendor) · PolicyManager registry (vendor) · MDM diagnostic report |
| **CAP-342** | Get logs off an iPhone | [8.2](../08-troubleshooting/8.2-log-surfaces.md) | 8.13, 3.5 | sysdiagnose (vendor) · MDMClient logs |
| **CAP-343** | Find out what version of Fleet you are talking to | [8.13](../08-troubleshooting/8.13-escalation.md) | 7.3 | per instance · behind the load balancer |
| **CAP-344** | Reduce the load Fleet is under | [8.14](../08-troubleshooting/8.14-degradation.md) | 2.2, 7.5 | tune the intervals · Fleet is slow · slow or unresponsive after enabling a feature |
| **CAP-345** | Process host results asynchronously | [8.14](../08-troubleshooting/8.14-degradation.md) | 1.6 | `osquery_enable_async_host_processing` |
| **CAP-346** | Stop hosts overwriting each other | [8.14](../08-troubleshooting/8.14-degradation.md) | 3.1 | duplicate hosts · enroll cooldown · `--host-identifier` |
| **CAP-347** | Work out what truncated or refused a request | [8.14](../08-troubleshooting/8.14-degradation.md) | 6.3 | 429 · too many open files · body too large · partial results |
| **CAP-348** | Find which query costs the most on the host | [8.14](../08-troubleshooting/8.14-degradation.md) | 4.6, 8.7 | per-query cost on the device |

## Why the eight groups are not the table of contents

![Explanation](../_assets/icons/explanation.svg) **Groups shaped like the manual's parts produce a re-worded contents page**, so these are shaped like the question you are holding instead. Three of them cut across parts as a result: scope and targeting spans Parts I and V, access and accountability spans Parts I, II and VII, and the diagnosis group spans Parts VII and VIII.

| | Group | The question it answers | Outcomes |
|---|---|---|---|
| 1 | Access and accountability | Who can use Fleet, how they prove it, and what is recorded | 32 |
| 2 | Connecting devices | Getting a device enrolled, and the platform connections that must exist first | 68 |
| 3 | Scope and targeting | Deciding who a change reaches and whose data you are reading | 8 |
| 4 | Knowing what a device is | Reading state: vitals, reports, policies, software, vulnerabilities, estate counts | 58 |
| 5 | Changing a device | Writing state, split by the mechanism that carries it | 107 |
| 6 | Automating Fleet | Making Fleet or another system act without a person | 24 |
| 7 | Running the service | Deploying, upgrading, backing up, sizing, monitoring, and keeping credentials alive | 46 |
| 8 | When it did not work | Symptoms, and the surfaces that answer them | 21 |

**Group 5 gets one level of sub-grouping and no more**, along the line [5.1](../05-manage-devices/5.1-plan-target-and-govern-device-changes.md) already teaches: settings that persist, work that runs once, and experiences. Every reader of Part V has met that distinction, so it costs nothing to reuse and it splits the largest group along a boundary people already hold.

**One outcome, one group.** A row appears once and is reached from elsewhere through its `Also` column. Duplicating a row is how two projections of the same set of capabilities drift apart, and this book has already paid for that once.

**Outcomes Fleet refuses keep their rows.** Enforcing a Linux operating system version, releasing a locked Android device, rotating an API token, backing Fleet up with Fleet's own tooling, and keeping a restored copy from acting on the real world are all things people search for and Fleet does not do. Each keeps a row, marked **(no)**, pointing at the chapter that records the refusal. An index that leaves them out sends you off to look for them.

## Where the words in the last column come from

![Explanation](../_assets/icons/explanation.svg) **Every word was read somewhere. None was invented**, because a synonym built from a plausible guess routes a reader to the wrong chapter with more confidence than no index at all.

Six places supply them.

1. **Fleet's interface**, in the labels and empty states it prints, and in the keyword lists behind its search box.
2. **Fleet's older names**, still accepted at this release in request bodies, GitOps keys, environment variables, command aliases and route paths.
3. **Fleet's activity types**, which are what the audit record literally says and therefore what somebody searches it for.
4. **Fleet's own published documentation** at this release. It is evidence of what Fleet calls a thing, because it is what a searcher has already read, and never evidence of how Fleet behaves.
5. **The vendors**, for the words an administrator arrives holding from Apple, Microsoft or Google.
6. **This manual**, for the concepts it names that Fleet does not name at all.

### Fleet ships its own synonym index and does not publish it

**The command palette in Fleet's web interface matches on 98 hand-written keyword lists**, one per capability, and they are the closest thing Fleet has to an answer to the question this appendix asks. They carry `filevault2`, `laps`, `ade`, `dep`, `win10`, `win11`, `fma`, `pki`, `est`, `zero trust`, `azure ad`, `ldap`, `tag`, `endpoints`, `machines`, `computers`, `ad hoc`, `tarballs` and `service account`. Fleet's own engineers wrote them, for exactly the reason this index exists: after a rename, people go on typing the old word for a long time.

**They also index things this manual routes differently**, which makes them a source of rows rather than only of words. Fleet keeps `filevault`, `filevault2`, `bitlocker` and `recovery key` in one list under disk encryption. This manual splits that outcome across five rows and argues at [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md) that "the BitLocker key" is the wrong name for what Windows actually escrows. So `bitlocker key` is a phrase this index has to carry **because** the manual refuses it, not in spite of that.

The lists are reachable only by typing into the search box of a running Fleet. They are not in Fleet's documentation, and they are not in its API.

## Fleet's older names, and which ones still work

![Reference](../_assets/icons/reference.svg) **Everything in this section is accepted at 4.90.0.** [a.6](a.6-glossary-and-release-compatibility.md) owns the rename itself and the surfaces it covered. What follows is the part you type: the spec kinds, keys, variables, flags and paths that carry the older word and still resolve.

**Fleet serves 47 route aliases covering 58 deprecated paths**, and accepts **44 deprecated GitOps keys**. Renamed request fields keep taking the old name in a body and answer with the new one. So a script written before March 2026 keeps working, a runbook keeps being correct, and a search of your own repository for the current word comes back empty while the deployment is running fine.

### The fleet and report family

| You would type | Current name | Where you would type it | Route |
|---|---|---|---|
| `team`, `teams`, `team_id` | fleet, `fleet_id` | API bodies and query strings, GitOps, the interface | [1.3](../01-foundations/1.3-hosts-fleets-labels.md) |
| `kind: team` | `kind: fleet` | A spec file | [6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md) |
| `/api/v1/fleet/teams`, `/fleet/spec/teams`, `/fleet/team/{id}/policies`, `/fleet/teams/{id}/users` | the `fleets` forms | A URL, a client, a saved request | [6.3](../06-automate-fleet/6.3-use-the-fleet-rest-api.md) |
| `team_settings` | `settings` | GitOps | [6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md) |
| `no-team.yml`, `No team`, team 0 | `unassigned.yml`, Unassigned | GitOps, the interface | [1.3](../01-foundations/1.3-hosts-fleets-labels.md), and [a.6] for how it is stored |
| `--team`, `--policies-team`, `--delete-other-teams`, `DELETE_OTHER_TEAMS` | `--fleet`, `--policies-fleet`, `--delete-other-fleets`, `DELETE_OTHER_FLEETS` | `fleetctl`, and CI environment | [6.4](../06-automate-fleet/6.4-use-fleetctl.md) |
| `FLEET_JIT_USER_ROLE_TEAM_<id>` | `FLEET_JIT_USER_ROLE_FLEET_<id>` | A SAML attribute in your identity provider | [2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md) |
| `apple_bm_default_team`, `macos_team`, `ios_team`, `ipados_team`, `byod_team` | `mdm.apple_business`, `macos_fleet`, and the matching `_fleet` forms | GitOps, the API | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) |
| `query`, `queries`, `saved query`, `live query`, `scheduled query` | report, live report, scheduled report | Everywhere | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) |
| `kind: query` | `kind: report` | A spec file | [6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md) |
| `/api/v1/fleet/queries`, the live-query run paths, host query paths | the `reports` forms | A URL, a client, a saved request | [6.3](../06-automate-fleet/6.3-use-the-fleet-rest-api.md) |
| `queries` (GitOps top level), `scheduled_query_id` | `reports`, `scheduled_report_id` | GitOps, the API | [6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md) |
| `fleetctl query`, `--query-name`, `QUERYNAME` | `fleetctl report`, `--report-name`, `REPORT_NAME` | `fleetctl`, and CI environment | [6.4](../06-automate-fleet/6.4-use-fleetctl.md) |
| `live_query_disabled`, `query_reports_disabled`, `query_report_cap` | `live_reporting_disabled`, `discard_reports_data`, `report_cap` | Organization settings, GitOps | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) |
| `/api/v1/osquery/*` | `/api/osquery/*` | The agent's own paths | [6.3](../06-automate-fleet/6.3-use-the-fleet-rest-api.md) |
| `/fleet/global/policies`, `/fleet/global/schedule` | `/fleet/policies`, `/fleet/schedule` | A URL, a client | [6.3](../06-automate-fleet/6.3-use-the-fleet-rest-api.md) |

### Other names Fleet has not retired

| You would type | Current name | Route |
|---|---|---|
| `host_settings` | `features` | [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md) |
| `enable_jit_role_sync` | Nothing. It is accepted and does nothing | [2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md) |
| `macos_settings` | `apple_settings` | [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) |
| `custom_settings` | `configuration_profiles` | [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) |
| `macos_setup` | `setup_experience` | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) |
| `bootstrap_package` | `macos_bootstrap_package` | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) |
| `macos_setup_assistant` | `apple_setup_assistant` | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) |
| `manual_agent_install` | `macos_manual_agent_install` | [3.2](../03-connect-devices/3.2-enroll-macos-devices.md) |
| `enable_release_device_manually` | `apple_enable_release_device_manually` | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) |
| `enable_managed_local_account` | `enable_create_local_admin_account` | `None`, and see the last section |
| `mdm.macos_settings.enable_disk_encryption` | `mdm.enable_disk_encryption` | [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md) |
| `mdm.enable_custom_os_updates_and_filevault` | `mdm.enable_custom_filevault`, `mdm.enable_custom_disk_encryption`. Any of the three enables it | [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md) |
| `org_logo_url`, `org_logo_url_light_background` | `org_logo_url_dark_mode`, `org_logo_url_light_mode` | [2.7](../02-administer-and-deploy-fleet/2.7-organization-and-server-settings.md) |
| `s3.bucket`, `s3.prefix`, `s3.region` and eight siblings | the `s3.carves_*` forms, hidden from the help output | [2.2](../02-administer-and-deploy-fleet/2.2-self-hosting-architecture-and-capacity.md) |
| `osquery.status_log_file`, `osquery.result_log_file`, `osquery.enable_log_rotation` | the `filesystem.*` forms | [2.8](../02-administer-and-deploy-fleet/2.8-activity-audit-logs-and-log-delivery.md) |
| `packaging.*` | Nothing. The feature they configured was removed and the keys stayed | [6.4](../06-automate-fleet/6.4-use-fleetctl.md) |
| `SCEP_RENEWAL_ID` | `CERTIFICATE_RENEWAL_ID` | [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) |
| `HOST_END_USER_EMAIL_IDP` | `HOST_END_USER_IDP_USERNAME` | [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) |
| `abm_token` | `ab_token` | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) |
| `fleetctl generate mdm-apple-bm`, `get mdm-apple-bm` | `generate mdm-ab`, `get mdm-ab` | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) |
| `browser` | `extension_for` | [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md) |
| `software_id` as a host filter | `software_version_id` | [4.5](../04-know-your-devices/4.5-monitor-fleet-wide-state.md) |
| `profile_id` | `profile_uuid` | [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) |
| `orbot_node_key` | `orbit_node_key`. A shipped typo kept for agents at 1.38.0 and below | [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md), and [a.6] for node keys |
| `kolide_server_url` | `server_url` | [2.7](../02-administer-and-deploy-fleet/2.7-organization-and-server-settings.md) |
| `mia` | `missing` | [4.5](../04-know-your-devices/4.5-monitor-fleet-wide-state.md), and [a.6] |
| tier `basic` | `premium` | [7.6](../07-operate-fleet/7.6-maintain-credentials-certificates-and-access.md) |
| `vendor_old` | `vendor` | [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md) |

## The vendors' words for things Fleet renames

![Reference](../_assets/icons/reference.svg) **These are the words an administrator arrives holding**, and the third column is the one that matters: how many of this book's chapters use the word at all. Where that count is low, the index is the only route from the word to the chapter.

| You arrive with | Fleet or this manual calls it | Chapters using the word | Route |
|---|---|---|---|
| DEP, Device Enrollment Program | Automated Device Enrollment, ADE, company-owned | DEP in six, ADE in thirteen, and [a.6] owns the pair | [3.2](../03-connect-devices/3.2-enroll-macos-devices.md) |
| VPP, Volume Purchase Program | Apps and Books, App and Book token | VPP in eight, Apps and Books in one | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) |
| Autopilot, OOBE | Windows automatic enrollment through Entra | Autopilot in five, OOBE in two | [3.3](../03-connect-devices/3.3-enroll-windows-devices.md) |
| Azure AD, AAD, Active Directory, LDAP | Microsoft Entra | None | [2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md) |
| Intune | Named as the thing you are leaving, or the thing that wins a conflict | Two | [2.11](../02-administer-and-deploy-fleet/2.11-configure-windows-management.md) |
| Jamf, Workspace ONE, Kandji, Munki | "another MDM" | Jamf in two, Workspace ONE and Kandji in one each, Munki in none | [3.2](../03-connect-devices/3.2-enroll-macos-devices.md) |
| OMA-URI, LocURI, CSP, ADMX | Windows configuration profile | CSP in two and LocURI in one, both Windows diagnostics. OMA-URI in none | [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) |
| SyncML | The Windows management channel | Three, all in Part VIII | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) |
| DDM | declaration, declarative device management | The acronym in one, the spelled-out form in three | [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) |
| zero-touch | ADE on Apple, Autopilot on Windows, the QR path on Android | Two | [3.2](../03-connect-devices/3.2-enroll-macos-devices.md) |
| LAPS | managed local administrator account | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) creates, enables and rotates it | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) |
| EST, PKI, NDES, DigiCert, Smallstep, Hydrant | certificate authority | All six now appear in [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md). Four also appear in [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) or Part VIII | [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md) for the prerequisite, [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) to deliver |
| Lost Mode | Fleet's button says Lock | One | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) |
| Managed Apple ID | Managed Apple Account, Apple's current term | None. [3.5](../03-connect-devices/3.5-enroll-ios-and-ipados-devices.md) uses Apple's current term on purpose | [3.5](../03-connect-devices/3.5-enroll-ios-and-ipados-devices.md) |
| work profile, device owner, profile owner | personally enrolled and company-owned Android | Six | [3.6](../03-connect-devices/3.6-enroll-android-devices.md) |
| Nudge | The update path for macOS 13 and earlier | One | [5.6](../05-manage-devices/5.6-control-operating-system-updates.md) |
| Managed Google Play, AMAPI | Android Enterprise, bound to Fleet | Three and seven | [2.12](../02-administer-and-deploy-fleet/2.12-bind-android-enterprise.md) |
| LUKS | Linux disk encryption | Eight | [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md) |
| Okta, Jira, Zendesk | conditional access, ticketing | Three, four and four | [5.9](../05-manage-devices/5.9-automate-remediation-with-policies.md) |

**Five of those words appear in no chapter of this book**: Azure AD, LDAP, Munki, OMA-URI and Managed Apple ID. Their rows are the ones that earn the appendix, because there is no other route from the word to the page.

**Fleet documents all of them.** At this release Jamf heads twenty-six sections of Fleet's own documentation, Kandji and Munki eight each, and Workspace ONE three. [3.2](../03-connect-devices/3.2-enroll-macos-devices.md)'s migration section now names Jamf, Workspace ONE and Kandji, so Munki is the only one of the four still absent from this book: standard in the industry and present in the vendor's material, but not used here, which is a gap in the book rather than in the reader.

**OMA-URI is the one word neither Fleet nor this book gives a heading to**, and it is the only word an Intune administrator has for the thing [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) calls a Windows configuration profile. Managed Google Play and AMAPI have no heading in Fleet's documentation either, though both are used in this book's chapters.

## Words this manual uses that Fleet does not

![Reference](../_assets/icons/reference.svg) **The reverse direction, and this index is the only place it can be fixed.** A reader who has read the chapter will search for the manual's word; a reader who has not will never guess it. Both need the row.

| This manual's word | What Fleet calls it, if anything | Where it is defined |
|---|---|---|
| desired state, discrete activity, device action | Nothing. The three mechanisms have no collective Fleet name | [5.1](../05-manage-devices/5.1-plan-target-and-govern-device-changes.md) |
| rollout rings | Nothing | [5.1](../05-manage-devices/5.1-plan-target-and-govern-device-changes.md) |
| families, for the ways Fleet reaches a device | Nothing. **[1.2](../01-foundations/1.2-how-fleet-reaches-a-device.md)'s heading says channels and the paragraph beneath it says families**, so search for both | [1.2](../01-foundations/1.2-how-fleet-reaches-a-device.md) |
| the unnamed state | Nothing | [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) |
| the three representations of a piece of software | Nothing, and [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) says you never see those names in the interface | [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) |
| variants, not versions | Nothing | [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) |
| configuration lane, setup-item lane | Nothing | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) |
| release-ready | Nothing | [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) |
| the evidence ladder | Nothing | [5.6](../05-manage-devices/5.6-control-operating-system-updates.md) |
| supported action, against custom command | Nothing | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) |
| archived credential | Nothing | [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md) |
| fleet move | Fleet says transfer, and the activity is `transferred_hosts` | [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md) |
| transition-based, against continuous | `continuous_automations_enabled` is the setting | [5.9](../05-manage-devices/5.9-automate-remediation-with-policies.md) |
| re-fire, duplicate suppression, cooldown | Nothing | [5.9](../05-manage-devices/5.9-automate-remediation-with-policies.md) |
| the label-scope trap | Nothing | [5.9](../05-manage-devices/5.9-automate-remediation-with-policies.md) |
| sentinel | Nothing | [3.3](../03-connect-devices/3.3-enroll-windows-devices.md) |
| endpoint restrictions | `user_api_endpoints` | [1.4](../01-foundations/1.4-identity-and-roles.md) |
| break-glass account | Nothing, and Fleet's documentation has no heading for it | [2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md) |
| estate | Fleet says fleet, for the same thing and also for a different one | [4.5](../04-know-your-devices/4.5-monitor-fleet-wide-state.md) |

## Where two live Fleet names disagree

![Troubleshooting](../_assets/icons/troubleshooting.svg) **Fourteen places where Fleet, or this book, uses two names for one thing and neither is marked wrong.** Each is a row in the index. Seven are defects rather than dialects: a name that Fleet prints, documents or emits where a different name is the one that actually works, so following the visible name gets you nothing and says nothing.

**The seven that will waste your time.**

**`dep_syncer` is a job name and never a schedule name.** Fleet's own documentation calls it "the `dep_syncer` cron job". The schedule that contains it is `apple_mdm_dep_profile_assigner`, and that is the name recorded when it runs. Searching the schedule history for `dep_syncer` finds nothing ([8.6](../08-troubleshooting/8.6-server-state.md)).

**`app_enable_report_stats` is documented and not registered.** The server registers `app.enable_scheduled_query_stats`. Setting the documented name silently does nothing ([4.6](../04-know-your-devices/4.6-advanced-osquery-queries-and-tables.md)).

**Fleet's own startup message names the wrong configuration key, one line above the right one.** It tells you to set `updates.allow_missing_migrations`; the registered key is `upgrades.allow_missing_migrations`, and the next line gives the correct `--upgrades_allow_missing_migrations` flag ([7.3](../07-operate-fleet/7.3-upgrade-fleet-and-fleetd.md)).

**The API reference names a table called `activities`. No such table exists.** The audit rows are in `activity_past`, which is what a query against your own database has to say ([8.12](../08-troubleshooting/8.12-audit-logs.md)).

**`logger_path` is documented as an agent option where osquery's flag is `logger_plugin`**, and Fleet's own guidance uses the working name elsewhere in the same documentation set ([8.2](../08-troubleshooting/8.2-log-surfaces.md)).

**Fleet's documentation attributes the Windows enrollment key pair's effect to macOS hosts.** Changing that pair makes escrowed disk encryption credentials unreadable, and this manual adjudicates the effect to Windows ([2.11](../02-administer-and-deploy-fleet/2.11-configure-windows-management.md), [7.6](../07-operate-fleet/7.6-maintain-credentials-certificates-and-access.md)).

**`fleetctl get user_roles` prints the deprecated vocabulary.** Its output carries `team:` for a concept the release notes say the command line renamed, so a GitOps-managed user-role file grepped for `fleet:` comes back empty ([a.7](a.7-fleetctl-command-reference.md)).

**The other seven are live ambiguities to search around.**

**Three names for one Apple credential, all live at once.** The interface says AB token, the API says `abm_token`, and the tables say DEP. [a.6] owns which is which ([2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md)).

**The host action reads "Live report" and the value behind it is `query`** ([4.2](../04-know-your-devices/4.2-run-queries-and-reports.md)).

**`enable_jit_role_sync` is accepted and does nothing.** The capability it names is now implicit ([2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md)).

**`packaging.*` configures a feature Fleet removed.** The keys remain and set nothing ([6.4](../06-automate-fleet/6.4-use-fleetctl.md)).

**`mdm.enable_custom_os_updates_and_filevault` and its two successors are all live, and any one of the three enables the behaviour** ([5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md)).

**`channels` and `families` both name the ways Fleet reaches a device**, in adjacent lines of [1.2](../01-foundations/1.2-how-fleet-reaches-a-device.md), and both spellings of Apple Business appear across Part I and Part II. Search for both.

**`fleet` means two opposite things inside this book.** [5.4](../05-manage-devices/5.4-manage-software-and-applications.md) uses it for the whole estate in one heading and for a single scope in the same chapter, and [4.5](../04-know-your-devices/4.5-monitor-fleet-wide-state.md) says fleet-wide meaning estate-wide. It is the most-typed word in the manual and it is ambiguous; when a sentence could mean either, the scope reading is the one Fleet's API uses.

## Where this index ends

![Troubleshooting](../_assets/icons/troubleshooting.svg) **Eight things a reader will search for that this index has no formal row for.** They are published rather than omitted, because an index that goes quiet sends you looking for a chapter that is not there, and a stated absence takes ten seconds to act on. Only one of the eight is a genuine coverage gap with no chapter behind it; the other seven are already taught or recorded and lack only a row, so read the split below rather than the headline count. Thirteen earlier entries left the count once a chapter covered them; they close this section, with links to the coverage, rather than disappearing.

**No link is invented for any of them.** A chapter owns an outcome when it explains the workflow, not when it mentions the thing in passing, and not when it explains the surrounding workflow without covering this step.

**[a.7](a.7-fleetctl-command-reference.md#which-commands-have-an-owning-chapter) keeps the sibling register at command granularity.** Every `fleetctl` command group there now has an owning chapter, including first-run `setup` ([2.2](../02-administer-and-deploy-fleet/2.2-self-hosting-architecture-and-capacity.md#complete-first-run-setup)). The local evaluation sandbox has an owning chapter there too ([1.1](../01-foundations/1.1-what-fleet-is.md#try-fleet-without-deploying-anything)) even though it remains one of this index's no-row absences below, since a.7 tracks commands and this index tracks outcomes. The two registers describe overlapping gaps at different grain, so never add one count to the other.

### Eight things with no capability row

These are attested in Fleet but have no capability row, so they do not appear in the index above. They are not equally uncovered, and the distinction is the whole point of listing them apart: **only the first, Android enrollment through a Google account, also has no owning chapter,** which makes it the one genuine coverage gap. The other seven are already taught or recorded and wait only on a formal row: the host display name template and the Apple DDM declaration asset are both taught in [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md), the local evaluation sandbox is taught in [1.1](../01-foundations/1.1-what-fleet-is.md#try-fleet-without-deploying-anything), first-run setup is taught in [2.2](../02-administer-and-deploy-fleet/2.2-self-hosting-architecture-and-capacity.md#complete-first-run-setup), and the Chromebook trio's blanket refusal is recorded in [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md). Those three Chromebook IDs are attested only in [a.2](a.2-platform-capability-matrix.md)'s platform research, which found them while answering a different question and gave each a shared-register ID with nowhere in the index yet to send a reader for per-command detail.

**Android enrollment through a Google account.** A named absence: [3.6](../03-connect-devices/3.6-enroll-android-devices.md) says a third path exists and this manual cannot describe it, and [8.13](../08-troubleshooting/8.13-escalation.md) adds that no expected status has been established for it.

**The local evaluation sandbox.** [1.1](../01-foundations/1.1-what-fleet-is.md#try-fleet-without-deploying-anything) teaches running `fleetctl preview`, but it still has no capability row of its own in the matrix above. Its command contracts are in [a.7](a.7-fleetctl-command-reference.md#which-commands-have-an-owning-chapter).

**The host display name template.** [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md#naming-hosts-from-a-template) teaches the Premium per-scope template that sets the display name Apple hosts report, including its variables, the device-name byte limit and the enforcement lifecycle, but it has no capability row of its own. Its endpoints are in [a.8](a.8-api-action-and-endpoint-reference.md) and the GitOps key is `controls.name_template`.

**The Apple DDM declaration asset.** [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md#declaration-assets) teaches the Premium `com.apple.asset.*` object a declaration references for large or binary content, including the validation rules, the per-fleet name and identifier uniqueness, the delete-while-referenced refusal, and the licence trap where a GitOps run on Fleet Free uploads none of them without erroring, but it has no capability row of its own. Its endpoints are in [a.8](a.8-api-action-and-endpoint-reference.md) and the GitOps key is `controls.macos_settings.assets`.

**First-run setup.** [2.2](../02-administer-and-deploy-fleet/2.2-self-hosting-architecture-and-capacity.md#complete-first-run-setup) teaches creating the first administrator on a new server, the one-time step whose route stops existing once an administrator has been created, but it has no capability row of its own. This is the server's own initialization, distinct from CAP-189's device setup experience at first boot; its command form is recorded in [a.7](a.7-fleetctl-command-reference.md#which-commands-have-an-owning-chapter).

**Locking, releasing and erasing a Chromebook.** CAP-367, CAP-368 and CAP-369. Fleet refuses all three outright: the lock, unlock and wipe handlers each fall through to a `default:` case that returns "Unsupported host platform" for ChromeOS (`ee/server/service/hosts.go:139,230,330` at fleet-v4.90.0). [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) records the blanket refusal in prose directly beneath its lock-unlock-wipe matrix ("ChromeOS supports none of it"), but the matrix itself carries no ChromeOS column, so no chapter gives the refusal per-command detail the way it does for CAP-222's Android unlock.

### Thirteen entries re-audited out of the count

**An entry leaves this register by being taught, and these thirteen left it that way: three when a re-audit found the teaching already in the book, and ten when new content took the outcome on.** They stay listed so the register never shrinks silently, and so the next audit does not re-open them.

**The device-authenticated API.** Counted here in an earlier revision on the grounds that it was covered only through the things that run on it. The coverage stands in its own right: [1.2](../01-foundations/1.2-how-fleet-reaches-a-device.md#the-five-channels) explains the channel, its per-host token and who consumes it, and [a.8](a.8-api-action-and-endpoint-reference.md#who-calls-fleet-and-what-they-present) carries the Device caller class and enumerates the surface that token authenticates.

**Turning stored reporting off across the whole server, and what that does to forwarding.** An earlier revision said two chapters touch the switch and neither owns the consequence. Both halves are owned: [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md#what-stops-a-result-being-stored) owns the switch, including that `discard_reports_data` deletes the rows already stored, [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md#getting-results-out-of-fleet) owns the forwarding consequence, namely that a server-wide disable forwards incoming results without the per-report automations filter, and [1.1](../01-foundations/1.1-what-fleet-is.md#what-does-fleet-do) carries the storage-against-forwarding model the two hang from.

**An infrastructure intake checklist.** [8.13](../08-troubleshooting/8.13-escalation.md#8134-infrastructure-intake-list-self-hosted) carries a usable one. It is assembled by this manual and marked as not official because Fleet publishes none, which is the absence [8.14](../08-troubleshooting/8.14-degradation.md) records; unofficial is a provenance note rather than a missing chapter, so this register no longer counts it.

**Carving a file off a host, and reading the server's record of it.** Counted here while eight chapters sized, budgeted and bucketed a carve and none started one or read one back. [8.7](../08-troubleshooting/8.7-live-query-introspection.md#878-running-and-retrieving-a-file-carve) now owns both halves: initiating a carve, and retrieving the completed one through `fleetctl get carves`, `get carve` and the REST equivalents. It is not licence-gated, so this was never a Premium omission.

**ChromeOS diagnosis.** Counted here while [3.7](../03-connect-devices/3.7-enroll-chromeos-devices.md) said there was no ChromeOS troubleshooting chapter. [3.7](../03-connect-devices/3.7-enroll-chromeos-devices.md) now carries the diagnosis itself, so the absence it recorded is closed.

**Retrying a failed software install or uninstall.** Counted here while the retry controls had no capability row and no chapter that owned the workflow. [5.4](../05-manage-devices/5.4-manage-software-and-applications.md#retries-you-ask-for) now owns it: **Retry** on a failed install and **Retry uninstall** on a failed uninstall, appearing in two places on two different routes. From the host's software library an operator's retry re-sends the operator host action, `POST /api/v1/fleet/hosts/:id/software/:software_title_id/install` or the matching `.../uninstall`; from the self-service page the user's retry re-sends the device-authenticated self-service action, `POST /api/v1/fleet/device/{token}/software/install/:software_title_id` or `.../uninstall/:software_title_id`. Both are Premium, and there is no retry-specific endpoint, no `fleetctl` command and no GitOps path. [8.11](../08-troubleshooting/8.11-reproducing-and-isolating.md) still lists the retry as a forcing action with its production-safety verdict.

**The managed local administrator account.** Counted here while no chapter created or rotated the account Fleet holds on a Mac. [5.5](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md) now owns it: enabling `_fleetadmin`, the standard-account interlock, and [retrieving and rotating its password](../05-manage-devices/5.5-design-setup-and-self-service-experiences.md#retrieve-and-rotate-the-managed-local-administrator-password), including the view-triggered rotation. It is macOS-only and Premium. `LAPS` is the word people arrive with, and it now leads to a chapter.

**Prompting a Mac's user to migrate from another MDM.** Counted here while [3.2](../03-connect-devices/3.2-enroll-macos-devices.md) had no migration section and [6.5](../06-automate-fleet/6.5-integrations-webhooks-and-external-workflows.md) taught only the webhook contract. [3.2](../03-connect-devices/3.2-enroll-macos-devices.md#migrating-a-mac-from-another-mdm) now owns it: enabling the `macos_migration` block, voluntary against forced mode, the eligibility floor, and the device flow through the webhook your own automation receives. CAP-040 routes there, and the webhook contract stays with [6.5](../06-automate-fleet/6.5-integrations-webhooks-and-external-workflows.md#understand-each-webhook-contract).

**Running a script across many hosts at once.** Counted here while no chapter owned the batch, and separately while the batch's per-host records were said to reach no external log destination that any chapter owned. [5.3](../05-manage-devices/5.3-run-and-manage-scripts.md#running-it-on-many-at-once) now owns both: targeting, the 5,000-host ceiling and the incompatible-host reasons, and that the per-host `ran_script` records a batch produces stay host-only, off the global feed and the external log stream. CAP-162 routes there.

**Creating a custom host vital definition.** Counted here while [4.1](../04-know-your-devices/4.1-understand-hosts-vitals-and-inventory.md) named the feature and taught only reading a value. [4.1](../04-know-your-devices/4.1-understand-hosts-vitals-and-inventory.md) now teaches the definition lifecycle: creating, listing, renaming and deleting a definition, setting or clearing a host's value, and declaring the whole set in a GitOps spec, each written to the activity log. It is on Fleet Free.

**The mutual-TLS proxy in front of Okta conditional access.** Counted here while the proxy was a one-sentence prerequisite no chapter owned. [2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md#device-conditional-access-trusts-the-proxy-set-certificate-serial) now owns it: the client-certificate-serial header the proxy sets, that Fleet trusts it with no cryptographic binding to the request, and the requirement that the terminator derive the serial from the verified peer certificate and discard every inbound copy, with the origin restriction and the serial-format setting. It is Premium.

**Turning Fleet's device management off for one host, independent of the platform-wide switch.** Counted here while no chapter taught an administrator when or how to invoke it standalone, only Android's estate-wide toggle in [2.12](../02-administer-and-deploy-fleet/2.12-bind-android-enterprise.md#turning-android-mdm-off-deletes-your-enterprise). [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md#turn-mdm-off-for-one-host) now owns it: which platforms offer it and which refuse, what re-enrollment looks like per enrollment type, and the record-flips-before-the-device inversion between Apple and Android BYOD. CAP-370 routes there. It is Free.

**Rotating the FileVault recovery key Fleet holds for a Mac.** Counted here while [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md) said only that reading a key never rotates it, with no mention of the one case where Fleet rotates a key on its own. [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md#the-one-credential-fleet-repairs-on-its-own) now owns it: the scheduled verification job that marks a stored key undecryptable, the Escrow Buddy capability that turns that into an automatic re-key at the person's next login, and that Windows and Linux have no equivalent. CAP-371 routes there.
