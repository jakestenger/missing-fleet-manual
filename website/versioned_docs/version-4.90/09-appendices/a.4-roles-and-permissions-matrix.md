---
title: "Roles and permissions matrix"
chapter: "Appendices and indexes"
section: "A.4"
sidebar_position: 4
verified_against: Fleet 4.90.0
verified_on: 2026-08-29
verified_source: "drafted against fleet-v4.90.0 (7c428c6e46). The row universe was reconciled against the shared capability register over four research rounds and two later corrections; every published cell resolves to a policy rule, a Go-side decision, or an explicit Not established, and the row universe itself is a search result rather than a proof that nothing is missing. Citation ledger at research/section-notes/a.4-notes.md"
further_reading:
 - https://fleetdm.com/docs/rest-api/rest-api
feature_requests:
 labels: [":product"]
 match: ["role", "permission", "RBAC", "authorization"]
 exclude: []
---

# Roles and permissions matrix

![Reference](../_assets/icons/reference-light.svg) Choose the table for your account’s scope, find the action, and read across to your role. A `Conditional` cell links the answer to a numbered condition below.

Fleet authorizes an action for a particular role and scope. Licensing, platform support, and interface availability are separate checks; use the related references below when permission alone does not explain the result.

<a id="what-this-appendix-carries"></a>

## Coverage and related references

![Reference](../_assets/icons/reference-light.svg) These tables cover the administrator actions identified during the permissions review, across all six roles and both scopes. They provide the detailed breakdown introduced in [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md). The route search was not exhaustive, so an action missing here may need an additional row.

Each cell describes the result an administrator receives. That can depend on the authorization policy, middleware that runs before it, fields removed from a permitted response, or database filtering that leaves a successful response empty. The tables include these effects where the review established them.

> Response masking depends on the route. For example, reading organisation settings applies role-based field masks, while writing them returns a response with credentials obfuscated but without those masks. At this release, global GitOps can therefore receive three settings groups in a write response that are withheld on read. Rows identify known differences between reading routes.

Use [a.2](a.2-platform-capability-matrix.md) for platform support, licences, and prerequisites, and [a.5](a.5-interface-index.md) to find the available interfaces. Licence checks are not included in the permission cells: an otherwise permitted action can still return HTTP `402` for a licence restriction. A permission failure returns `403`.

## The permission matrix

![Reference](../_assets/icons/reference-light.svg) The matrix contains 152 administrator actions. Each row includes the underlying policy pair so you can trace the result.

## How to read the two tables

Table 1 covers global roles. Table 2 covers accounts with roles assigned to fleets and no global role. Fleet rejects an account that combines both scopes. Both tables use the same 152 rows in the same order for comparison.

The action column describes what you want to do. The `object · action` pair beneath it identifies the policy rule involved. Some actions use several pairs; others are decided in Go outside the policy and are labeled accordingly.

The cells use these five values:

| Value | Meaning |
|---|---|
| `Allowed` | The request succeeds and returns what it promises. |
| `Denied` | The request is refused for this role at this scope. Where Fleet has a refusal test for it, the cell rests on that test; the families found to have no such test are named below. |
| `Conditional (Cnn)` | Allowed or denied depending on the condition; both branches are in the register below. |
| `Not applicable` | The product has **no such scoped operation**: the action exists, and this scope cannot hold the object. Never a way of saying a role is refused. |
| `Not established (Enn)` | Not determined; the register below says what was searched. |

No cell currently needs `Not applicable` or `Not established`. These values distinguish an unavailable scoped operation or an unresolved answer from a permission denial.

Fifty cells include qualifiers for requests that succeed with limited results:

- **An empty part of the response:** 14 GitOps cells across seven rows and eight routes. Fleet-membership filtering does not recognize GitOps roles at either scope. Label changes can still succeed while returning no host membership, and reports can return without stored results. Moving hosts by filter succeeds without moving any. Membership filtering applies when a request names hosts; requests supplying host identifiers use per-host checks and attach the specified hosts. Ordinary `host · list` and `host · read` remain policy denials for GitOps.
- **`Allowed; field withheld`:** 11 cells for global agent options. Only a global administrator receives that field in the read response.
- **`Allowed; SMTP and SSO withheld`:** 10 cells for global organization settings. These groups are returned only to global administrators and accounts that administer at least one fleet. Other settings remain visible.
- **`Allowed; other fleets' tokens withheld`:** four fleet-scoped Volume Purchasing token cells. The list includes tokens assigned to readable fleets or all fleets, and silently excludes unassigned tokens and other fleets’ tokens.
- **`Allowed; other fleets' results withheld` / `Allowed; other fleets' commands withheld`:** ten fleet-scoped cells for MDM command responses and host command lists. Fleet filters hosts before authorization, excluding other fleets and Unassigned without triggering C15. The response count reflects only the returned items.
- **`other fleets' memberships withheld`:** one cell for listing accounts at fleet scope. Each account’s memberships are limited to fleets where the requester has a role. The separate single-account read, when authorized, returns all memberships.

An API-only account with a non-empty endpoint restriction list is denied access outside that list before the policy runs. Two routes bypass this middleware: the debug tree uses separate authentication, and the live-query results stream authenticates its bearer token when the socket opens. Endpoint restrictions do not fence either route. A restricted API-only global administrator can still reach debug endpoints; the query stream still requires a valid bearer and ownership of that run. Configuring endpoint restrictions has its own row in group 2.

Four rows are decided outside the policy: the debug tree, a host’s My Device URL, global agent-options reads, and live-query results started by another identity. The last is denied in all twelve cells because Fleet checks query ownership after the policy permits the request. Even a global administrator cannot read another identity’s live-query stream.

Some denials are established from policy rules without a corresponding role-refusal test. The evidence review found these test gaps. The search was not exhaustive, so this is a list of known gaps:

| The rows | Whose refusal Fleet's tests do not cover |
|---|---|
| Inspecting and revoking **anyone else's** session | Global GitOps, and all six fleet-scoped roles |
| Listing and reading pending invites; inviting and revoking an invite | Global GitOps, and all six fleet-scoped roles |
| Every group 2 row about a user account, except editing your own | Global GitOps; and fleet-scoped maintainer, technician, Observer+, observer and GitOps |
| Applying a role specification for many accounts at once | Every denied role, at both scopes, for the same reason as the account rows above |
| Renaming a software title | **Every denied role, at both scopes.** The refusal test for that object exercises reading only, and every denial this row prints is about writing |
| Seeing the certificate authorities; adding, editing and deleting one; reading its stored credentials | Global Observer+, and fleet-scoped technician and Observer+ |
| Reading and replacing the end-user licence agreement | Global Observer+, and fleet-scoped technician and Observer+ |
| Forcing a scheduled job to run now | Global technician, Observer+ and GitOps, and fleet-scoped technician, Observer+ and GitOps |
| Issuing a certificate from a CA; both certificate-template rows | Every denied role. The service tests for those routes exercise a global administrator and assert no refusal at all |
| The Apple platform-setup rows, and the legacy-installer and Apple-device rows that share their tests | Both technician variants throughout; and, on the narrower of the two test families, global GitOps and every fleet-scoped role except an administrator of one fleet |
| Fetching the Okta IdP signing certificate and Apple profile | Both technician variants |
| The Android Enterprise rows, the SCIM rows, and wiring up Entra conditional access | **No role-refusal test family was found for those objects at all** |

The policy grants none of these denied combinations, and the tests found do not contradict the cells. The missing evidence is a test explicitly asserting refusal for the listed role. If your deployment behaves differently, these cells merit checking first. A family absent from this list has not necessarily been shown to have complete test coverage.

---

## Table 1, global scope

| Action | Admin | Maintainer | Technician | Observer+ | Observer | GitOps |
|---|---|---|---|---|---|---|
| **Group 1, Signing in and holding a session** | | | | | | |
| Inspect your own sessions<br>`session · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| Revoke your own session<br>`session · write` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| Inspect anyone's sessions<br>`session · read` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Revoke anyone's session<br>`session · write` | Allowed | Denied | Denied | Denied | Denied | Denied |
| **Group 2, Accounts, roles and API identities** | | | | | | |
| List user accounts<br>`user · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Denied |
| Read one user account<br>`user · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Conditional (C01) |
| Create a user account<br>`user · write`; account creation has no self-service grant | Allowed | Denied | Denied | Denied | Denied | Denied |
| Edit your own account<br>`user · write` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| Edit another user's account<br>`user · write` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Delete a user account<br>`user · write` | Conditional (C19) | Conditional (C19) | Conditional (C19) | Conditional (C19) | Conditional (C19) | Conditional (C19) |
| Change a user's role or fleets<br>`user · write_role` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Apply a role specification for many accounts at once<br>`user · write`, checked before any account is named; self-service and fleet-administrator grants do not apply | Allowed | Denied | Denied | Denied | Denied | Denied |
| Change a password<br>`user · change_password` | Allowed | Conditional (C01) | Conditional (C01) | Conditional (C01) | Conditional (C01) | Conditional (C01) |
| List and read pending invites<br>`invite · read` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Invite a user; revoke an invite<br>`invite · write` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Add or remove a fleet's members<br>`team · write_members` | Allowed | Denied | Denied | Denied | Denied | Denied |
| List which API endpoints exist<br>`api_endpoint · read` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Restrict an API-only identity to named endpoints<br>`user · write_role` and `api_endpoint · read` | Allowed | Denied | Denied | Denied | Denied | Denied |
| **Group 3, Fleets** | | | | | | |
| See that a fleet exists; list fleets<br>`team · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Conditional (C04) |
| Create a fleet<br>`team · write` on the collective object | Allowed | Denied | Denied | Denied | Denied | Allowed |
| Change a fleet you administer<br>`team · write` | Allowed | Denied | Denied | Denied | Denied | Allowed |
| Delete a fleet<br>`team · write` | Allowed | Denied | Denied | Denied | Denied | Allowed |
| Read the Unassigned fleet's settings<br>`app_config · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| **Group 4, Enroll secrets** | | | | | | |
| Read an enroll secret<br>`enroll_secret · read` | Allowed | Allowed | Denied | Denied | Denied | Denied |
| Change enroll secrets<br>`enroll_secret · write` | Allowed | Allowed | Denied | Denied | Denied | Conditional (C05) |
| **Group 5, Global settings** | | | | | | |
| Read the global organization settings<br>`app_config · read` | Allowed | Allowed; SMTP and SSO withheld | Allowed; SMTP and SSO withheld | Allowed; SMTP and SSO withheld | Allowed; SMTP and SSO withheld | Allowed; SMTP and SSO withheld |
| Change the global organization settings<br>`app_config · write` | Allowed | Denied | Denied | Denied | Denied | Allowed |
| Read the global agent options<br>`app_config · read`; **decided outside the policy** | Allowed | Allowed; field withheld | Allowed; field withheld | Allowed; field withheld | Allowed; field withheld | Allowed; field withheld |
| Change the global agent options<br>`app_config · write` | Allowed | Denied | Denied | Denied | Denied | Allowed |
| Read the Fleet server version<br>`version · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| **Group 6, Hosts: reading** | | | | | | |
| Access host listings<br>`host · list` | Allowed | Allowed | Allowed | Allowed | Allowed | Denied |
| Read one host's record<br>`host · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Denied |
| Resolve a host by identifier without host read<br>`host · selective_list` and `host · selective_read` | Allowed | Allowed | Allowed | Allowed | Allowed | Conditional (C13) |
| Read a host's health scorecard<br>`host_health · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Denied |
| Read a host's disk-encryption recovery key<br>`host · list` then `host · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Denied |
| Read a Mac's Recovery Lock password<br>`host · list` then `host · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Denied |
| Read a managed local account password<br>`host · list` then `host · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Denied |
| Read one host's activity feed and its queued work<br>`host · list` then `host · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Denied |
| Read the estate-wide activity feed<br>`activity · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Denied |
| Read a host's My Device URL<br>`host · list`; **decided outside the policy** | Allowed | Denied | Denied | Denied | Denied | Denied |
| **Group 7, Hosts: writing** | | | | | | |
| Delete a host<br>`host · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Set or delete a host's IdP / device mapping<br>`host · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Lock or erase a Mac through the legacy Apple route<br>`host · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Attach or detach a label on a host<br>`host · write_host_label` | Allowed | Allowed | Allowed | Denied | Denied | Allowed |
| Move named hosts between fleets<br>`host · transfer_host` | Allowed | Allowed | Allowed | Denied | Denied | Allowed |
| Move hosts between fleets by filter<br>`host · transfer_host` | Allowed | Allowed | Allowed | Denied | Denied | Allowed; moves nothing |
| Cancel queued work on a host<br>`host · cancel_host_activity` | Allowed | Allowed | Denied | Denied | Denied | Denied |
| Ask a host to report again (refetch)<br>`host · list` then `host · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Denied |
| **Group 8, Device actions** | | | | | | |
| Lock a host<br>`host · list` then `mdm_command · write` | Allowed | Allowed | Denied | Denied | Denied | Denied |
| Unlock a host<br>`host · list` then `mdm_command · write` | Allowed | Allowed | Denied | Denied | Denied | Denied |
| Wipe a host<br>`host · list` then `mdm_command · write` | Allowed | Allowed | Denied | Denied | Denied | Denied |
| Clear a device's passcode<br>`host · read` then `mdm_command · write` | Allowed | Allowed | Denied | Denied | Denied | Denied |
| Rotate a Mac's Recovery Lock password<br>`host · list` then `mdm_command · write` | Allowed | Allowed | Denied | Denied | Denied | Denied |
| Rotate a managed local account password<br>`host · list` then `mdm_command · write` | Allowed | Allowed | Denied | Denied | Denied | Denied |
| Send a raw MDM command<br>`mdm_command · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Unenroll a host from MDM<br>`host · list` then `mdm_command · write` | Allowed | Allowed | Denied | Denied | Denied | Denied |
| Read what a device said about a command<br>`host · list` then `mdm_command · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Denied |
| List the MDM commands a host has been sent<br>`host · list` then `mdm_command · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Denied |
| **Group 9, Labels** | | | | | | |
| See labels<br>`label · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed; no host membership |
| Create a label<br>`label · create` | Allowed | Allowed | Allowed | Denied | Denied | Allowed; no members when hosts are named |
| Edit or delete a fleet's own label<br>`label · write` | Allowed | Allowed | Allowed | Denied | Denied | Allowed; membership emptied when hosts are named |
| Edit or delete a global label<br>`label · write` | Allowed | Allowed | Allowed | Denied | Denied | Allowed; membership emptied when hosts are named |
| **Group 10, Reports, live queries and carves** | | | | | | |
| See a saved report<br>`query · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed; no stored results |
| Create, edit or delete a saved report<br>`query · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Run ad-hoc SQL<br>`query · run_new` | Allowed | Allowed | Allowed | Allowed | Denied | Denied |
| Run a saved report live against hosts<br>`targeted_query · run` | Allowed | Allowed | Allowed | Allowed | Conditional (C06, C11) | Denied |
| Use the live-query target picker<br>`target · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Denied |
| Read live-query results you did not start<br>`targeted_query · run`, then an ownership check; **decided outside the policy** | Denied | Denied | Denied | Denied | Denied | Denied |
| See a legacy scheduled-query pack<br>`pack · read` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Edit or delete a legacy scheduled-query pack<br>`pack · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Download a file carve<br>`carve · read` | Allowed | Denied | Denied | Denied | Denied | Denied |
| **Group 11, Policies** | | | | | | |
| See a policy<br>`policy · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed; no automation activities |
| Create, edit or delete a policy; set its automations<br>`policy · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Clear a policy's collected results<br>`policy · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Re-arm a policy's webhook and ticket automations<br>`app_config · write` and `team · write` | Allowed | Denied | Denied | Denied | Denied | Allowed |
| **Group 12, Software and vulnerability knowledge** | | | | | | |
| Browse installed software and vulnerabilities<br>`software_inventory · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| Rename a software title<br>`software_inventory · write` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Browse Fleet's maintained-app catalogue<br>`maintained_app · read` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Read a vulnerability or uptime chart<br>`host · list` when no fleet is named, `host · read` when one is | Allowed | Allowed | Allowed | Allowed | Allowed | Denied |
| **Group 13, The software library and delivery** | | | | | | |
| See a software installer, App Store app or icon<br>`installable_entity · read` | Allowed | Allowed | Allowed | Denied | Denied | Allowed |
| Add or edit a package you upload<br>`installable_entity · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Add or remove an App Store (VPP) app<br>`installable_entity · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Add or remove a Play app or Android web app<br>`installable_entity · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Upload or delete a title icon<br>`installable_entity · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Remove a title from the software library<br>`installable_entity · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Batch-apply the whole software catalogue<br>`installable_entity · write` and `team · read` | Allowed | Allowed | Denied | Denied | Denied | Conditional (C04) |
| Choose the software installed during setup<br>`installable_entity · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Install software on a host<br>`host_software_installer_result · write` | Allowed | Allowed | Allowed | Denied | Denied | Denied |
| Uninstall software from a host<br>`host_software_installer_result · write` | Allowed | Allowed | Allowed | Denied | Denied | Denied |
| See install and uninstall results<br>`host_software_installer_result · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Denied |
| See the self-service categories<br>`software_category · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| Manage the self-service categories<br>`software_category · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| **Group 14, Configuration profiles** | | | | | | |
| See a configuration profile<br>`mdm_config_profile · read` | Allowed | Allowed | Allowed | Denied | Denied | Allowed |
| Create a profile in a fleet<br>`mdm_config_profile · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Remove a configuration profile from devices<br>`mdm_config_profile · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Batch-replace every profile for a fleet<br>`mdm_config_profile · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Preassign and match profiles during an MDM migration<br>`mdm_config_profile · write` on the Unassigned fleet's profiles, then `team · write` on the collective object, both taken before Fleet knows which fleet the host will land in | Allowed | Denied | Denied | Denied | Denied | Allowed |
| Resend a profile to a host<br>`mdm_config_profile · resend` | Allowed | Allowed | Allowed | Denied | Denied | Allowed |
| Read the disk-encryption status summary<br>`mdm_config_profile · read` | Allowed | Allowed | Allowed | Denied | Denied | Allowed |
| Read a declarative-management asset<br>`ddm_asset · read` | Allowed | Allowed | Allowed | Denied | Denied | Allowed |
| Create or delete a declarative-management asset<br>`ddm_asset · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| **Group 15, Scripts** | | | | | | |
| See a saved script<br>`script · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Denied |
| Save or delete a script<br>`script · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Designate the macOS setup script<br>`script · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Run a script on a host<br>`host_script_result · write` | Conditional (C14) | Conditional (C14) | Conditional (C14) | Denied | Denied | Denied |
| Read a script's output<br>`host_script_result · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Denied |
| **Group 16, Variables and host vitals** | | | | | | |
| List custom-variable names<br>`secret_variable · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| Set a custom variable's value<br>`secret_variable · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| See the custom host vital definitions<br>`custom_vital · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| Define a custom host vital<br>`custom_vital · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Set one host's custom vital value<br>`host_custom_vital · write` | Allowed | Allowed | Denied | Denied | Denied | Denied |
| **Group 17, Certificates** | | | | | | |
| See the certificate authorities<br>`certificate_authority · read` and `certificate_authority · list` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Add, edit or delete a certificate authority<br>`certificate_authority · write` | Allowed | Denied | Denied | Denied | Denied | Allowed |
| Read a certificate authority's stored credentials<br>`certificate_authority · read_secrets` | Allowed | Denied | Denied | Denied | Denied | Allowed |
| Issue a certificate from a CA<br>`certificate_request · write` | Allowed | Allowed | Denied | Denied | Denied | Denied |
| See a fleet's certificate templates<br>`certificate_template · read` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Manage certificate templates for a fleet<br>`certificate_template · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| **Group 18, Apple, Windows and Android platform setup** | | | | | | |
| Turn on Apple device management (APNs)<br>`mdm_apple · write` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Renew the Apple push certificate<br>`mdm_apple · write` | Allowed | Denied | Denied | Denied | Denied | Denied |
| See the APNs push-certificate status<br>`mdm_apple · read` | Allowed | Denied | Denied | Denied | Denied | Denied |
| See Apple Business Manager tokens<br>`mdm_apple · list` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Connect Fleet to Apple Business Manager<br>`mdm_apple · write` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Renew the Apple Business Manager token<br>`mdm_apple · read`; the renewal changes state under a reading permission | Allowed | Denied | Denied | Denied | Denied | Denied |
| Place an ADE device in a fleet by platform<br>`mdm_apple · write` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Add a Volume Purchasing token<br>`mdm_apple · write` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Renew the Volume Purchasing token<br>`mdm_apple · write` | Allowed | Denied | Denied | Denied | Denied | Denied |
| List Volume Purchasing tokens<br>`installable_entity · read` | Allowed | Allowed | Allowed | Denied | Denied | Allowed |
| Assign a Volume Purchasing token to fleets<br>`mdm_apple · write` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Delete a Volume Purchasing token<br>`mdm_apple · write` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Download the manual enrollment profile<br>`mdm_apple_manual_enrollment_profile · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| Upload, read or delete a legacy Apple installer<br>`mdm_apple_installer · write` | Allowed | Denied | Denied | Denied | Denied | Denied |
| List Apple MDM devices<br>`mdm_apple_device · write` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Turn disk encryption on for a fleet<br>`mdm_apple_settings · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Turn disk encryption off<br>`mdm_apple_settings · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Read the Setup Assistant profile<br>`mdm_apple_setup_assistant · read` | Allowed | Allowed | Denied | Denied | Denied | Denied |
| Customise the Setup Assistant<br>`mdm_apple_setup_assistant · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Read the bootstrap package metadata<br>`mdm_apple_bootstrap_package · read` | Allowed | Allowed | Denied | Denied | Denied | Denied |
| Upload, replace or delete the bootstrap package<br>`mdm_apple_bootstrap_package · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Read the end-user licence agreement<br>`mdm_apple_eula · read` | Allowed | Denied | Denied | Denied | Denied | Allowed |
| Replace the end-user licence agreement<br>`mdm_apple_eula · write` | Allowed | Denied | Denied | Denied | Denied | Allowed |
| Turn Windows device management off<br>`app_config · write` on the Windows device-management setting | Allowed | Denied | Denied | Denied | Denied | Allowed |
| Turn Windows device management on<br>`app_config · write` on the Windows device-management setting | Conditional (C16) | Denied | Denied | Denied | Denied | Conditional (C16) |
| See the Android Enterprise binding<br>`android_enterprise · read` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Bind Fleet to an Android Enterprise<br>`android_enterprise · write` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Issue an Android enrollment token<br>`android_enterprise · write` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Turn Android device management off<br>`android_enterprise · write` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Wire up Entra conditional access<br>`conditional_access_microsoft · write` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Fetch the Okta IdP signing certificate and Apple profile<br>`conditional_access_idp_assets · read` | Allowed | Allowed | Allowed | Denied | Denied | Allowed |
| See SCIM status and provisioned users<br>`scim_user · read` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Accept SCIM provisioning writes<br>`scim_user · write` | Allowed | Denied | Denied | Denied | Denied | Denied |
| **Group 19, Operating the service** | | | | | | |
| Force a scheduled job to run now<br>`cron_schedules · write` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Collect a server diagnostic archive; read internal errors; check migrations<br>no policy pair; **decided outside the policy** | Allowed | Conditional (C17) | Conditional (C17) | Conditional (C17) | Conditional (C17) | Conditional (C17) |

---

## Table 2, fleet scope

The subject holds this role on fleet T and holds no global role. The cell answers for an object belonging to fleet T. A denial that follows only from the object being in a *different* fleet is not a condition, that is what fleet scope means.

| Action | Admin | Maintainer | Technician | Observer+ | Observer | GitOps |
|---|---|---|---|---|---|---|
| **Group 1, Signing in and holding a session** | | | | | | |
| Inspect your own sessions<br>`session · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| Revoke your own session<br>`session · write` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| Inspect anyone's sessions<br>`session · read` | Denied | Denied | Denied | Denied | Denied | Denied |
| Revoke anyone's session<br>`session · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| **Group 2, Accounts, roles and API identities** | | | | | | |
| List user accounts<br>`user · read` | Conditional (C18); other fleets' memberships withheld | Denied | Denied | Denied | Denied | Denied |
| Read one user account<br>`user · read` | Conditional (C01, C02) | Conditional (C01) | Conditional (C01) | Conditional (C01) | Conditional (C01) | Conditional (C01) |
| Create a user account<br>`user · write`; account creation has no self-service grant | Conditional (C02) | Denied | Denied | Denied | Denied | Denied |
| Edit your own account<br>`user · write` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| Edit another user's account<br>`user · write` | Conditional (C02) | Denied | Denied | Denied | Denied | Denied |
| Delete a user account<br>`user · write` | Conditional (C02, C19) | Conditional (C19) | Conditional (C19) | Conditional (C19) | Conditional (C19) | Conditional (C19) |
| Change a user's role or fleets<br>`user · write_role` | Conditional (C02) | Denied | Denied | Denied | Denied | Denied |
| Apply a role specification for many accounts at once<br>`user · write`, checked before any account is named; self-service and fleet-administrator grants do not apply | Denied | Denied | Denied | Denied | Denied | Denied |
| Change a password<br>`user · change_password` | Conditional (C01) | Conditional (C01) | Conditional (C01) | Conditional (C01) | Conditional (C01) | Conditional (C01) |
| List and read pending invites<br>`invite · read` | Denied | Denied | Denied | Denied | Denied | Denied |
| Invite a user; revoke an invite<br>`invite · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| Add or remove a fleet's members<br>`team · write_members` | Allowed | Denied | Denied | Denied | Denied | Denied |
| List which API endpoints exist<br>`api_endpoint · read` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Restrict an API-only identity to named endpoints<br>`user · write_role` and `api_endpoint · read` | Conditional (C02) | Denied | Denied | Denied | Denied | Denied |
| **Group 3, Fleets** | | | | | | |
| See that a fleet exists; list fleets<br>`team · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Conditional (C04) |
| Create a fleet<br>`team · write` on the collective object | Denied | Denied | Denied | Denied | Denied | Denied |
| Change a fleet you administer<br>`team · write` | Allowed | Denied | Denied | Denied | Denied | Allowed |
| Delete a fleet<br>`team · write` | Allowed | Denied | Denied | Denied | Denied | Allowed |
| Read the Unassigned fleet's settings<br>`app_config · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| **Group 4, Enroll secrets** | | | | | | |
| Read an enroll secret<br>`enroll_secret · read` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Denied |
| Change enroll secrets<br>`enroll_secret · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Denied |
| **Group 5, Global settings** | | | | | | |
| Read the global organization settings<br>`app_config · read` | Allowed | Allowed; SMTP and SSO withheld | Allowed; SMTP and SSO withheld | Allowed; SMTP and SSO withheld | Allowed; SMTP and SSO withheld | Allowed; SMTP and SSO withheld |
| Change the global organization settings<br>`app_config · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| Read the global agent options<br>`app_config · read`; **decided outside the policy** | Allowed; field withheld | Allowed; field withheld | Allowed; field withheld | Allowed; field withheld | Allowed; field withheld | Allowed; field withheld |
| Change the global agent options<br>`app_config · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| Read the Fleet server version<br>`version · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| **Group 6, Hosts: reading** | | | | | | |
| Access host listings<br>`host · list` | Allowed | Allowed | Allowed | Allowed | Allowed | Denied |
| Read one host's record<br>`host · read` | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Denied |
| Resolve a host by identifier without host read<br>`host · selective_list` and `host · selective_read` | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C13, C15) |
| Read a host's health scorecard<br>`host_health · read` | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Denied |
| Read a host's disk-encryption recovery key<br>`host · list` then `host · read` | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Denied |
| Read a Mac's Recovery Lock password<br>`host · list` then `host · read` | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Denied |
| Read a managed local account password<br>`host · list` then `host · read` | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Denied |
| Read one host's activity feed and its queued work<br>`host · list` then `host · read` | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Denied |
| Read the estate-wide activity feed<br>`activity · read` | Denied | Denied | Denied | Denied | Denied | Denied |
| Read a host's My Device URL<br>`host · list`; **decided outside the policy** | Denied | Denied | Denied | Denied | Denied | Denied |
| **Group 7, Hosts: writing** | | | | | | |
| Delete a host<br>`host · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Denied |
| Set or delete a host's IdP / device mapping<br>`host · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Denied |
| Lock or erase a Mac through the legacy Apple route<br>`host · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Denied |
| Attach or detach a label on a host<br>`host · write_host_label` | Conditional (C15) | Conditional (C15) | Conditional (C15) | Denied | Denied | Conditional (C15) |
| Move named hosts between fleets<br>`host · transfer_host` | Conditional (C12) | Conditional (C12) | Conditional (C12) | Denied | Denied | Conditional (C12) |
| Move hosts between fleets by filter<br>`host · transfer_host` | Conditional (C12) | Conditional (C12) | Conditional (C12) | Denied | Denied | Conditional (C12); moves nothing |
| Cancel queued work on a host<br>`host · cancel_host_activity` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Denied |
| Ask a host to report again (refetch)<br>`host · list` then `host · read` | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Denied |
| **Group 8, Device actions** | | | | | | |
| Lock a host<br>`host · list` then `mdm_command · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Denied |
| Unlock a host<br>`host · list` then `mdm_command · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Denied |
| Wipe a host<br>`host · list` then `mdm_command · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Denied |
| Clear a device's passcode<br>`host · read` then `mdm_command · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Denied |
| Rotate a Mac's Recovery Lock password<br>`host · list` then `mdm_command · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Denied |
| Rotate a managed local account password<br>`host · list` then `mdm_command · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Denied |
| Send a raw MDM command<br>`mdm_command · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Unenroll a host from MDM<br>`host · list` then `mdm_command · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Denied |
| Read what a device said about a command<br>`host · list` then `mdm_command · read` | Allowed; other fleets' results withheld | Allowed; other fleets' results withheld | Allowed; other fleets' results withheld | Allowed; other fleets' results withheld | Allowed; other fleets' results withheld | Denied |
| List the MDM commands a host has been sent<br>`host · list` then `mdm_command · read` | Allowed; other fleets' commands withheld | Allowed; other fleets' commands withheld | Allowed; other fleets' commands withheld | Allowed; other fleets' commands withheld | Allowed; other fleets' commands withheld | Denied |
| **Group 9, Labels** | | | | | | |
| See labels<br>`label · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed; no host membership |
| Create a label<br>`label · create` | Allowed | Allowed | Allowed | Denied | Denied | Allowed; no members when hosts are named |
| Edit or delete a fleet's own label<br>`label · write` | Allowed | Allowed | Allowed | Denied | Denied | Allowed; membership emptied when hosts are named |
| Edit or delete a global label<br>`label · write` | Conditional (C08) | Conditional (C08) | Conditional (C08) | Denied | Denied | Conditional (C08); membership emptied when hosts are named |
| **Group 10, Reports, live queries and carves** | | | | | | |
| See a saved report<br>`query · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Conditional (C09); no stored results |
| Create, edit or delete a saved report<br>`query · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Run ad-hoc SQL<br>`query · run_new` | Allowed | Allowed | Allowed | Allowed | Denied | Denied |
| Run a saved report live against hosts<br>`targeted_query · run` | Conditional (C07) | Conditional (C07) | Conditional (C07) | Conditional (C07) | Conditional (C06, C07) | Denied |
| Use the live-query target picker<br>`target · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Denied |
| Read live-query results you did not start<br>`targeted_query · run`, then an ownership check; **decided outside the policy** | Denied | Denied | Denied | Denied | Denied | Denied |
| See a legacy scheduled-query pack<br>`pack · read` | Denied | Denied | Denied | Denied | Denied | Denied |
| Edit or delete a legacy scheduled-query pack<br>`pack · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| Download a file carve<br>`carve · read` | Denied | Denied | Denied | Denied | Denied | Denied |
| **Group 11, Policies** | | | | | | |
| See a policy<br>`policy · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Conditional (C10); no automation activities |
| Create, edit or delete a policy; set its automations<br>`policy · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Clear a policy's collected results<br>`policy · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Re-arm a policy's webhook and ticket automations<br>`app_config · write` and `team · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| **Group 12, Software and vulnerability knowledge** | | | | | | |
| Browse installed software and vulnerabilities<br>`software_inventory · read` | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) |
| Rename a software title<br>`software_inventory · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| Browse Fleet's maintained-app catalogue<br>`maintained_app · read` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Read a vulnerability or uptime chart<br>`host · list` when no fleet is named, `host · read` when one is | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Denied |
| **Group 13, The software library and delivery** | | | | | | |
| See a software installer, App Store app or icon<br>`installable_entity · read` | Conditional (C15) | Conditional (C15) | Conditional (C15) | Denied | Denied | Conditional (C15) |
| Add or edit a package you upload<br>`installable_entity · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Add or remove an App Store (VPP) app<br>`installable_entity · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Add or remove a Play app or Android web app<br>`installable_entity · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Upload or delete a title icon<br>`installable_entity · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Remove a title from the software library<br>`installable_entity · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Batch-apply the whole software catalogue<br>`installable_entity · write` and `team · read` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C04, C15) |
| Choose the software installed during setup<br>`installable_entity · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Install software on a host<br>`host_software_installer_result · write` | Conditional (C15) | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied |
| Uninstall software from a host<br>`host_software_installer_result · write` | Conditional (C15) | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied |
| See install and uninstall results<br>`host_software_installer_result · read` | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Denied |
| See the self-service categories<br>`software_category · read` | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) |
| Manage the self-service categories<br>`software_category · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| **Group 14, Configuration profiles** | | | | | | |
| See a configuration profile<br>`mdm_config_profile · read` | Conditional (C15) | Conditional (C15) | Conditional (C15) | Denied | Denied | Conditional (C15) |
| Create a profile in a fleet<br>`mdm_config_profile · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Remove a configuration profile from devices<br>`mdm_config_profile · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Batch-replace every profile for a fleet<br>`mdm_config_profile · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Preassign and match profiles during an MDM migration<br>`mdm_config_profile · write` on the Unassigned fleet's profiles, then `team · write` on the collective object, both taken before Fleet knows which fleet the host will land in | Denied | Denied | Denied | Denied | Denied | Denied |
| Resend a profile to a host<br>`mdm_config_profile · resend` | Conditional (C15) | Conditional (C15) | Conditional (C15) | Denied | Denied | Conditional (C15) |
| Read the disk-encryption status summary<br>`mdm_config_profile · read` | Conditional (C15) | Conditional (C15) | Conditional (C15) | Denied | Denied | Conditional (C15) |
| Read a declarative-management asset<br>`ddm_asset · read` | Conditional (C15) | Conditional (C15) | Conditional (C15) | Denied | Denied | Conditional (C15) |
| Create or delete a declarative-management asset<br>`ddm_asset · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| **Group 15, Scripts** | | | | | | |
| See a saved script<br>`script · read` | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Denied |
| Save or delete a script<br>`script · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Designate the macOS setup script<br>`script · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Run a script on a host<br>`host_script_result · write` | Conditional (C14, C15) | Conditional (C14, C15) | Conditional (C14, C15) | Denied | Denied | Denied |
| Read a script's output<br>`host_script_result · read` | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Denied |
| **Group 16, Variables and host vitals** | | | | | | |
| List custom-variable names<br>`secret_variable · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| Set a custom variable's value<br>`secret_variable · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| See the custom host vital definitions<br>`custom_vital · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| Define a custom host vital<br>`custom_vital · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| Set one host's custom vital value<br>`host_custom_vital · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Denied |
| **Group 17, Certificates** | | | | | | |
| See the certificate authorities<br>`certificate_authority · read` and `certificate_authority · list` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Add, edit or delete a certificate authority<br>`certificate_authority · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| Read a certificate authority's stored credentials<br>`certificate_authority · read_secrets` | Denied | Denied | Denied | Denied | Denied | Denied |
| Issue a certificate from a CA<br>`certificate_request · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| See a fleet's certificate templates<br>`certificate_template · read` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Manage certificate templates for a fleet<br>`certificate_template · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| **Group 18, Apple, Windows and Android platform setup** | | | | | | |
| Turn on Apple device management (APNs)<br>`mdm_apple · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| Renew the Apple push certificate<br>`mdm_apple · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| See the APNs push-certificate status<br>`mdm_apple · read` | Denied | Denied | Denied | Denied | Denied | Denied |
| See Apple Business Manager tokens<br>`mdm_apple · list` | Denied | Denied | Denied | Denied | Denied | Denied |
| Connect Fleet to Apple Business Manager<br>`mdm_apple · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| Renew the Apple Business Manager token<br>`mdm_apple · read`; the renewal changes state under a reading permission | Denied | Denied | Denied | Denied | Denied | Denied |
| Place an ADE device in a fleet by platform<br>`mdm_apple · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| Add a Volume Purchasing token<br>`mdm_apple · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| Renew the Volume Purchasing token<br>`mdm_apple · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| List Volume Purchasing tokens<br>`installable_entity · read` | Allowed; other fleets' tokens withheld | Allowed; other fleets' tokens withheld | Allowed; other fleets' tokens withheld | Denied | Denied | Allowed; other fleets' tokens withheld |
| Assign a Volume Purchasing token to fleets<br>`mdm_apple · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| Delete a Volume Purchasing token<br>`mdm_apple · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| Download the manual enrollment profile<br>`mdm_apple_manual_enrollment_profile · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| Upload, read or delete a legacy Apple installer<br>`mdm_apple_installer · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| List Apple MDM devices<br>`mdm_apple_device · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| Turn disk encryption on for a fleet<br>`mdm_apple_settings · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Turn disk encryption off<br>`mdm_apple_settings · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Read the Setup Assistant profile<br>`mdm_apple_setup_assistant · read` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Denied |
| Customise the Setup Assistant<br>`mdm_apple_setup_assistant · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Read the bootstrap package metadata<br>`mdm_apple_bootstrap_package · read` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Denied |
| Upload, replace or delete the bootstrap package<br>`mdm_apple_bootstrap_package · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Read the end-user licence agreement<br>`mdm_apple_eula · read` | Denied | Denied | Denied | Denied | Denied | Denied |
| Replace the end-user licence agreement<br>`mdm_apple_eula · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| Turn Windows device management off<br>`app_config · write` on the Windows device-management setting | Denied | Denied | Denied | Denied | Denied | Denied |
| Turn Windows device management on<br>`app_config · write` on the Windows device-management setting | Denied | Denied | Denied | Denied | Denied | Denied |
| See the Android Enterprise binding<br>`android_enterprise · read` | Denied | Denied | Denied | Denied | Denied | Denied |
| Bind Fleet to an Android Enterprise<br>`android_enterprise · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| Issue an Android enrollment token<br>`android_enterprise · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| Turn Android device management off<br>`android_enterprise · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| Wire up Entra conditional access<br>`conditional_access_microsoft · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| Fetch the Okta IdP signing certificate and Apple profile<br>`conditional_access_idp_assets · read` | Denied | Denied | Denied | Denied | Denied | Denied |
| See SCIM status and provisioned users<br>`scim_user · read` | Denied | Denied | Denied | Denied | Denied | Denied |
| Accept SCIM provisioning writes<br>`scim_user · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| **Group 19, Operating the service** | | | | | | |
| Force a scheduled job to run now<br>`cron_schedules · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| Collect a server diagnostic archive; read internal errors; check migrations<br>no policy pair; **decided outside the policy** | Conditional (C17) | Conditional (C17) | Conditional (C17) | Conditional (C17) | Conditional (C17) | Conditional (C17) |

---

## The condition register

The register contains nineteen conditions, C01–C19, each with both outcomes. Eighteen appear in matrix cells. C03 is retained for stable numbering, but no cell needs it because the relevant session rows already specify ownership.

**C01, the requester’s own account.** **Allowed** when the account exists and belongs to the caller. **Denied** for another account unless a separate grant applies. The self-service grant excludes role changes and account creation, so it cannot let a caller change their own role or create a new account.

**C02, a fleet administrator over an account, tested across every fleet that account belongs to.** **Allowed** when the target account belongs to at least one fleet **and** the caller administers **every** fleet it belongs to. **Denied** when the target belongs to no fleet at all, or belongs to any fleet the caller does not administer, including fleets the caller has no role in whatsoever. C01 applies additionally and independently wherever C02 appears.

**C03, the requester’s own session.** **Allowed** for the caller’s session at either scope and for any role. **Denied** for another identity’s session unless the caller is a global administrator. No cell cites C03 because the session rows already identify whose session is involved.

**C04, GitOps and the collective fleet object.** **Allowed** for GitOps reading the "all fleets" placeholder that a fleet listing resolves to. **Denied** for a named fleet, which no reading grant extends to GitOps at either scope. **GitOps can therefore write a fleet it cannot read.**

**C05, global GitOps and enroll secrets.** **Allowed** when the secret is the deployment's global enroll secret. **Denied** for any fleet's own enroll secret: the only grant covering a fleet's secret asks for an administrator or maintainer role **on that fleet**, which a global GitOps identity does not hold.

**C06, whether the saved report is marked runnable by observers.** **Allowed** for an observer, global or fleet-scoped, only when the saved query carries that flag. **Denied** otherwise. For a fleet-scoped administrator, maintainer, technician or Observer+ the flag does not gate access at all, and Fleet covers both settings of it, but C07 still applies to those roles.

**C07, whether every fleet the request targets is one the caller holds a role on.** **Allowed** when the request names no target fleets at all, or when every fleet it does name is one the caller holds a qualifying role on. The query itself must additionally be a global query, or one owned by a fleet the caller holds a qualifying role on. **Denied** when even one named target fleet falls outside that set: **every named fleet must qualify, not merely one of them.** A fleet-scoped observer is narrower still, and admits a fleet only when that fleet *is* the query's own fleet and the observer's role there is observer.

**C08, who wrote a global label.** **Allowed** for a global label only when the caller created it. **Denied** for a global label somebody else created. Authorship is a question about global labels alone: **a label that belongs to a fleet is writable by an administrator, maintainer, technician or GitOps identity on that fleet whoever created it**, which is why the fleet's own label row is not conditional.

**C09, a fleet-scoped GitOps identity reading saved reports.** **Allowed** for a report owned by a fleet the identity holds GitOps on. **Denied** for a global report: the one grant that covers global reports for fleet-scoped callers leaves GitOps out.

**C10, a fleet-scoped GitOps identity reading policies.** **Allowed** for a policy owned by a fleet the identity holds GitOps on. **Denied** for a global policy, which no fleet-scoped GitOps grant reaches.

**C11, a global observer and a fleet-owned live query's targets.** **Allowed** when the query is global, or when the query belongs to a fleet and either no target fleets are named or every named target fleet is the query's own. **Denied** when a global observer targets any fleet other than the query's own.

**C12, a transfer is authorised at both ends.** **Allowed** when the caller holds administrator, maintainer, technician or GitOps on the destination fleet **and** on every fleet the hosts are being moved out of. Fleet checks the destination first, then each distinct source fleet in the batch, and it treats the Unassigned fleet as a source in its own right. Moving hosts **by filter** checks the destination first and then the source fleets of whatever the filter actually selected. **Denied** otherwise, and in particular **moving a host out of the Unassigned fleet is denied to every fleet-scoped role**, because the fleet-role lookup has nothing to key on when a host belongs to no fleet.

**C13, GitOps reading an automatically enrolled Apple device.** The selective-read permission is unconditional, but the route performs an additional ordinary host read for iOS and iPadOS hosts when Apple device management is enabled and configured. GitOps lacks that permission, so the additional lookup fails the whole request.

**Allowed**, with full host detail, for every host except an iOS or iPadOS host on a deployment where Apple device management is turned on and configured. **Denied**, with the whole request failing, for an iOS or iPadOS host on such a deployment.

**C14, deployment-wide script execution.** **Allowed** as shown in the cell when script execution is enabled. **Denied for every role**, including global administrator, when it is disabled. Fleet checks this before evaluating the caller’s role.

**C15, an object assigned to a named fleet.** Most fleet-scoped rules require the caller to hold the relevant role on the object’s own fleet. This condition accounts for many of the matrix’s conditional cells.

**Allowed** when the object belongs to a fleet where the caller holds the required role. **Denied** for Unassigned objects because there is no fleet identifier for the role lookup. Global roles can reach those objects under their ordinary permissions.

Host listing uses a broader rule: a qualifying role on any fleet can satisfy it. A fleet-scoped maintainer can therefore see an Unassigned host in a list while being unable to read its record or perform the host operations listed here.

**C16, Windows device-management credentials.** **Allowed** to enable Windows device management when the server has the required enrollment certificate and key. **Denied** with a validation error when they are missing, regardless of role. Disabling Windows device management does not require these credentials.

**C17, debug-mode authentication.** A server started in debug mode generates a token and prints a debug address containing it. Debug requests presenting a token go to a handler outside Fleet’s role authentication. **Allowed** here means the caller’s Fleet role does not decide the result; the external handler’s token-acceptance behavior has not been established from Fleet’s source. Treat this path as having no Fleet-side role check. On a normally started server, Fleet’s debug authentication applies and the request is **Denied** for every role except global administrator.

**C18, fleet-scoped account listing.** **Allowed** for a fleet administrator when the request names a fleet they administer. **Denied** when no fleet is named or the caller does not administer it. Other fleet-scoped roles cannot list accounts on this route. Global roles need no fleet parameter. Reading one account is a separate operation with its own permissions.

**C19, account deletion and the last global administrator.** **Allowed** for the caller’s own account at either scope, or for another account when a separate write grant applies. A global administrator has that grant for every account. **Denied** for other accounts without a grant. Fleet then applies an additional safeguard: deleting the last remaining global administrator is **Denied for every caller** with a validation error. This protects the target account regardless of who requests deletion. Other accounts, including automation identities, can delete themselves under their self-write permission, though this is not a documented self-service route.

C14, C16, and C17 depend on deployment configuration rather than role. They can change the outcome the role alone would produce.

Two conditions in the shared row register’s addendum describe outcomes rather than permission decisions: C31 covers a transfer-by-filter request that succeeds without moving hosts (`Allowed; moves nothing`), and C32 covers Apple Business Manager token renewal using a read permission. They are noted in the corresponding rows rather than used as cell conditions.

---


## Actions that carry a secret

![Troubleshooting](../_assets/icons/troubleshooting-light.svg) Some read permissions expose credentials. Review these rows when designing access, since a role’s name may not make that access apparent:

| What is revealed | The row that governs it |
|---|---|
| A host's disk encryption recovery key | **Reading the host.** There is no separate permission |
| The macOS Recovery Lock password | The same |
| A managed local account password | The same |
| Certificate authority integration credentials | Reading certificate authorities **with secrets**. [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md) sets these integrations up |
| Enroll secrets | Reading enroll secrets |
| **A host's device page URL** | Its own row, decided outside the policy. Fleet treats this URL as a credential for acting as that device's end user, so handing one out is handing over that person's view of Fleet |

The first three credentials all use the host-read permission. Fleet has no separate recovery-key permission, so their matrix cells match. They have separate rows to make each credential easy to look up.

Five of the six roles can read these host credentials within their permitted scope. At global scope, that covers every host in the deployment. See [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md) for guidance on recovery-credential access.

## How Fleet decides

![Explanation](../_assets/icons/explanation-light.svg) These mechanics can help you investigate an action that is not listed in the matrix.

A request carries a **subject**, which is the authenticated identity and the roles it holds. It names an **object**, which is the kind of thing being acted on and, where the thing belongs to a fleet, that fleet's identifier. And it names an **action**, one of sixteen verbs.

The policy denies any combination without a grant. The matrix also uses Fleet’s role-refusal tests where available. Known gaps in that test evidence are listed before the tables; the search did not establish exhaustive coverage.

The policy has sixteen actions. Specific verbs let Fleet grant operations such as running a report, transferring a host, or reading a stored secret without granting general write or read access to the object. Use the exact action when tracing a permission.

> This manual uses *fleet*, the current product term. Authorization objects, API fields, and membership roles still use `team`. These identifiers refer to the same grouping; keep the literal form when working with the API or tracing a policy rule.

<a id="role-and-scope-combine-and-are-exclusive"></a>

### Global and fleet scopes

The same six roles exist at both scopes. An identity can have a global role or roles on fleets; Fleet rejects a combination of the two.

Choose the table matching the account’s scope, then check any fleet-membership conditions in its cells.

Most fleet-scoped rules require a concrete fleet identifier and reject Unassigned objects. A global role is needed for those operations. Host listing is broader, which explains why a fleet administrator may see an Unassigned host in a list but be unable to open it or act on it.

<a id="combinations-fleet-refuses-and-where-it-does-not"></a>

### Role-assignment restrictions

These restrictions produce different errors:

| Kind | Example | What you get |
|---|---|---|
| **Structural** | A global role and a fleet role on one identity | Rejected at write time, whatever the licence |
| **Licence-gated** | Technician, Observer+ or GitOps on Free | A licence error, not a permission error |
| **Ordinary denial** | Observer trying to write a policy | A `403` from the policy |

Licence and API-only checks are implemented in the account creation and modification paths, with the GitOps-role exception described below. The bulk role-spec route performs neither check, so a global administrator can assign Premium-only roles on Free through that route. Its separate permissions appear in the accounts group; other roles cannot reach it.

## Service identities and endpoint restrictions

![Reference](../_assets/icons/reference-light.svg) An API-only account holds one of the same six roles, and its token inherits that role and scope. Its work is attributed to the account in activities. Give each automation its own identity to keep that attribution useful ([2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md)).

GitOps is intended for API-only accounts, but the modify route cannot reach that check: the check requires an API-only field that the endpoint rejects. An ordinary interactive account can therefore be assigned GitOps. See [1.4](../01-foundations/1.4-identity-and-roles.md) for the access that follows.

A non-empty endpoint restriction list narrows an API-only account’s access before the authorization policy runs. The debug tree and live-query results stream use separate authentication and bypass this list. The debug tree can still be reached by a restricted API-only global administrator; the query stream still requires its bearer token and the identity that started the query. Keep these exceptions in mind when configuring endpoint restrictions, listed in the accounts group.

## Version notes

![Reference](../_assets/icons/reference-light.svg) Verified against Fleet 4.90.0. The policy carries 154 rules over 49 object types and 16 actions; the 152 rows here are the administrator-facing projection of them, reconciled against the manual's shared capability register.

Ten policy grants have no rows because the route search found no administrator-facing use for them; at least one remains from a removed route. That search was not exhaustive. Additional routes may require new rows or updates to the known test gaps.

Qualifiers describing empty successful responses depend on response filtering as well as policy. Their behavior can change without a permission-policy change.
