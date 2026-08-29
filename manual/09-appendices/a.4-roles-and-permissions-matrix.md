---
title: "Roles and permissions matrix"
chapter: "Appendices and indexes"
section: "A.4"
sidebar_position: 4
status: drafting
verified_against: Fleet 4.90.1
verified_on: 2026-08-29
verified_source: "drafted against fleet-v4.90.1 (dd0200f062). The row universe was reconciled against the shared capability register over four research rounds; every cell resolves to a policy rule, a Go-side decision, or an explicit Not established. Citation ledger at research/section-notes/a.4-notes.md"
reviewed_by:
reviewed_on:
further_reading:
 - https://fleetdm.com/docs/rest-api/rest-api
feature_requests:
 labels: [":product"]
 match: ["role", "permission", "RBAC", "authorization"]
 exclude: []
---

# Roles and permissions matrix

**Authorisation is the intersection of an action, a role and a scope.** Licensing, platform support and interface availability are separate gates that this appendix does not answer, and a reader who conflates them will diagnose the wrong one.

## What this appendix carries

![Reference](../_assets/icons/reference.svg) Every administrator-visible action, against all six roles, at both scopes. That is the breakdown [2.3](../02-administer-and-deploy-fleet/2.3-user-accounts-roles-and-service-identities.md) promises and the reason this appendix is the most-referenced unwritten one in the book.

**A cell answers what an administrator can actually obtain**, not what Fleet's authorization policy returns. Those are different questions more often than they should be. The policy is the largest input, and a decision can also be made by service middleware before the policy runs, by a response having a field stripped from it after the policy allowed the whole object, or by a database query that filters the result to nothing after the request succeeded. **All of those change the answer, so all of them are in the cells.**

> **Masking is a property of the route, not of the object, and this appendix is organised by intent rather than by route.** Where a value is stripped from one response and not from another, the cell describes the reading route, and any row where that is known to differ says so. Reading the organisation settings is the case to know about: **the write response applies credential obfuscation and not the role masks the read response applies**, so an identity authorised to write receives fields it is masked from on read. At this release that affects exactly one identity, global GitOps, and three settings groups.

Three questions belong elsewhere. **Whether the capability exists on your platform is [a.2](a.2-platform-capability-matrix.md), not written yet**; the chapter that owns the capability is the authority meanwhile. **Whether your licence includes it is a separate gate again**, and it is not folded into any cell here: a role that is allowed an action it has no licence for gets a licence error, not a permission error, and telling them apart is most of diagnosing a `403`. **Which interface can perform it will be [a.5](a.5-interface-index.md)**, also unwritten.

## How Fleet decides

![Explanation](../_assets/icons/explanation.svg) Enough of the mechanism to predict an answer this appendix does not contain.

A request carries a **subject**, which is the authenticated identity and the roles it holds. It names an **object**, which is the kind of thing being acted on and, where the thing belongs to a fleet, that fleet's identifier. And it names an **action**, one of sixteen verbs.

**The policy is deny by default.** Every combination no rule grants is refused, which is why so many cells below say `Denied` without a rule to point at: the absence *is* the rule.

**Sixteen actions, not two.** Reading and writing are the common pair, and the rest exist because Fleet needed to give one role one verb without the general one. Running a report is not writing it. Transferring a host between fleets is not writing the host. Reading a secret is not reading the object that holds it. **A matrix built on read and write would be wrong**, and it would be wrong in the permissive direction, which is why this one is not built that way.

> **Two vocabularies for one idea.** This book says *fleet*, which is Fleet's current product term. The authorization implementation still says *team*, in identifiers such as `subject.teams`, the object's fleet, the fleet-role lookup and the `team` object type. Source references preserve those literal names, so a reader tracing a cell back into the policy lands somewhere real.

### Role and scope combine, and are exclusive

**The same six roles exist at both scopes**, and an identity holds one or the other, never both. Fleet rejects an account carrying a global role and a fleet role together.

That is why there are two tables rather than one with twelve columns. **You are always in exactly one of them.**

**A fleet-scoped role is scoped to a concrete fleet.** Most fleet-scoped rules are keyed on the object's fleet identifier and guarded against a null, and the helper that resolves a subject's role for a fleet is undefined when there is no such fleet. **So no fleet-scoped role of any kind reaches the Unassigned fleet**, whatever its role name suggests. Only a global role does. That single structural fact accounts for a large share of the conditional cells below, and it is the answer to a question that otherwise looks like a bug: a fleet administrator who can see an Unassigned host in a list and can do nothing to it.

### Combinations Fleet refuses, and where it does not

Three kinds of refusal get confused, and they fail differently:

| Kind | Example | What you get |
|---|---|---|
| **Structural** | A global role and a fleet role on one identity | Rejected at write time, whatever the licence |
| **Licence-gated** | Technician, Observer+ or GitOps on Free | A licence error, not a permission error |
| **Ordinary denial** | Observer trying to write a policy | A `403` from the policy |

**Those checks live in the create and modify paths, not in the roles themselves.** Fleet has a third route that applies roles in bulk from a spec and it performs neither: no licence check and no API-only check. So the table above describes what two paths enforce rather than an invariant about what a role can be, and a Free deployment can be given Premium-only roles through that third route.

## Service identities and endpoint restrictions

![Reference](../_assets/icons/reference.svg) **API-only is a property of an account, not a seventh role.** Such an account holds one of the same six roles, and its token inherits that role and that scope. The activity record attributes its work to it, which is the argument in [2.3](../02-administer-and-deploy-fleet/2.3-user-accounts-roles-and-service-identities.md) for giving each automation its own identity rather than sharing a person's token.

**GitOps is intended to be API-only**, and the rule that enforces it is unreachable on the modify path: it fires only when the request carries an API-only field, and that endpoint rejects any request carrying one. So the role can be given to an ordinary interactive account, and [1.4](../01-foundations/1.4-identity-and-roles.md) covers what that account can then reach.

**Endpoint restrictions narrow an API-only account further**, to a named list of endpoints, and they sit *above* every row in this appendix. Where such a list is non-empty, the middleware decides before the policy is consulted at all. That is why the restriction is not a row: it qualifies all of them equally. Configuring one is an ordinary row, in the accounts group.

## The permission matrix

![Reference](../_assets/icons/reference.svg) 148 administrator intents, grouped as a reader would look for them, with the policy pair underneath each so a cell can be traced.

## How to read the two tables

**Table 1 answers for a subject whose role is global. Table 2 answers for a subject who holds that role on a fleet and holds no global role.** The two scopes are mutually exclusive, and Fleet rejects an identity that tries to hold both, so a reader is always in one table or the other. Both tables carry the same 148 rows in the same order with the same wording, so they can be read side by side.

**The action column is the administrator's intent.** The `object · action` pair underneath it is the policy pair the intent resolves to, so a cell can be traced back to the rule that decides it. Some intents resolve to more than one pair, and a few resolve to none, because the decision is made in Go rather than in the policy; those rows say so.

**Cell vocabulary.** Five values and nothing else:

| Value | Meaning |
|---|---|
| `Allowed` | The request succeeds and returns what it promises. |
| `Denied` | The request is refused for this role at this scope. **The policy denies by default**, so every combination no rule grants is a denial. |
| `Conditional (Cnn)` | Allowed or denied depending on the condition; both branches are in the register below. |
| `Not applicable` | The product has **no such scoped operation**: the action exists, and this scope cannot hold the object. Never a way of saying a role is refused. |
| `Not established (Enn)` | Not determined; the register below says what was searched. |

Two cells carry a qualifier after `Allowed`, and both are stated in the row that carries them:

- **`Allowed`, with a stated effect**, on rows where the policy permits the request, the request succeeds, and **the part of the answer that comes through the host filter is empty**, because that filter names no GitOps role at either scope. **The qualifier says what is empty rather than declaring the whole operation empty**, because they are different: a label is still returned and still deleted, and it is the host membership that is missing; a report is still returned and its stored results are not. **Only moving hosts by filter is a wholly successful no-op.** Eight routes are affected and they print across nine cells, because one label route serves two published rows. It is **not** applied to `host · list` or `host · read`, which are policy denials for GitOps and are simply `Denied`.
- **`Allowed; field withheld`**, the request succeeds with 200 and the field is stripped from the response body before it is serialized. This is effective access, not a denial, and it applies to exactly one row: reading the global agent options.

**A prerequisite that sits above every cell in both tables.** For an API-only identity holding a non-empty `user_api_endpoints` list, every row here is additionally gated by the middleware, which calls `permissionDenied` at and `ac.SetChecked` at, so rego is never evaluated. It qualifies every row equally, which is why it is not one of them. *Configuring* the restriction is an ordinary row (group 2).

**Three rows are decided outside the policy** and say so in the row body: the debug tree, a host's My Device URL, and reading the global agent options.

---

## Table 1, global scope

| Action | Admin | Maintainer | Technician | Observer+ | Observer | GitOps |
|---|---|---|---|---|---|---|
| **Group 1, Signing in and holding a session** | | | | | | |
| Inspect your own sessions<br>`session · read` | Allowed | Conditional (C03) | Conditional (C03) | Conditional (C03) | Conditional (C03) | Conditional (C03) |
| Revoke your own session<br>`session · write` | Allowed | Conditional (C03) | Conditional (C03) | Conditional (C03) | Conditional (C03) | Conditional (C03) |
| Inspect anyone's sessions<br>`session · read` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Revoke anyone's session<br>`session · write` | Allowed | Denied | Denied | Denied | Denied | Denied |
| **Group 2, Accounts, roles and API identities** | | | | | | |
| List and read user accounts<br>`user · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Conditional (C01) |
| Create a user account<br>`user · write` (C01 requires `object.id != 0`, so the self branch cannot be met by a create) | Allowed | Conditional (C01) | Conditional (C01) | Conditional (C01) | Conditional (C01) | Conditional (C01) |
| Edit your own account<br>`user · write` | Allowed | Conditional (C01) | Conditional (C01) | Conditional (C01) | Conditional (C01) | Conditional (C01) |
| Edit another user's account<br>`user · write` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Delete a user account<br>`user · write` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Change a user's role or fleets<br>`user · write_role` | Allowed | Denied | Denied | Denied | Denied | Denied |
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
| Read the global organization settings<br>`app_config · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| Change the global organization settings<br>`app_config · write` | Allowed | Denied | Denied | Denied | Denied | Allowed |
| Read the global agent options<br>`app_config · read`; **decided outside the policy** | Allowed | Allowed; field withheld | Allowed; field withheld | Allowed; field withheld | Allowed; field withheld | Allowed; field withheld |
| Change the global agent options<br>`app_config · write` | Allowed | Denied | Denied | Denied | Denied | Allowed |
| Read the Fleet server version<br>`version · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| **Group 6, Hosts: reading** | | | | | | |
| Be allowed to look at hosts at all<br>`host · list` | Allowed | Allowed | Allowed | Allowed | Allowed | Denied |
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
| Move a host between fleets<br>`host · transfer_host` | Allowed | Allowed | Allowed | Denied | Denied | Allowed; moves nothing |
| Cancel queued work on a host<br>`host · cancel_host_activity` | Allowed | Allowed | Denied | Denied | Denied | Denied |
| Ask a host to report again (refetch)<br>`host · list` then `host · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Denied |
| **Group 8, Device actions** | | | | | | |
| Lock a host<br>`mdm_command · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Unlock a host<br>`mdm_command · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Wipe a host<br>`mdm_command · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Clear a device's passcode<br>`mdm_command · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Rotate a Mac's Recovery Lock password<br>`mdm_command · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Rotate a managed local account password<br>`mdm_command · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Send a raw MDM command<br>`mdm_command · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Unenroll a host from MDM<br>`mdm_command · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Read what a device said about a command<br>`mdm_command · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Denied |
| **Group 9, Labels** | | | | | | |
| See labels<br>`label · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed; no host membership |
| Create a label<br>`label · create` | Allowed | Allowed | Allowed | Denied | Denied | Allowed |
| Edit or delete a fleet's own label<br>`label · write` | Allowed | Allowed | Allowed | Denied | Denied | Allowed |
| Edit or delete a global label<br>`label · write` | Allowed | Allowed | Allowed | Denied | Denied | Allowed |
| **Group 10, Reports, live queries and carves** | | | | | | |
| See a saved report<br>`query · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed; no stored results |
| Create, edit or delete a saved report<br>`query · write` | Allowed | Allowed | Denied | Denied | Denied | Allowed |
| Run ad-hoc SQL<br>`query · run_new` | Allowed | Allowed | Allowed | Allowed | Denied | Denied |
| Run a saved report live against hosts<br>`targeted_query · run` | Allowed | Allowed | Allowed | Allowed | Conditional (C06, C11) | Denied |
| Use the live-query target picker<br>`target · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Denied |
| Read live-query results you did not start<br>no policy pair; **decided outside the policy** | Denied | Denied | Denied | Denied | Denied | Denied |
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
| Preassign and match profiles during an MDM migration<br>`mdm_config_profile · write` and `team · write`, both on a zero-value object | Allowed | Denied | Denied | Denied | Denied | Allowed |
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
| Renew the Apple Business Manager token<br>`mdm_apple · read`, the renewal mutates under `ActionRead` | Allowed | Denied | Denied | Denied | Denied | Denied |
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
| Turn Windows device management off<br>`app_config · write` on `windows_enabled_and_configured` | Allowed | Denied | Denied | Denied | Denied | Allowed |
| Turn Windows device management on<br>`app_config · write` on `windows_enabled_and_configured` | Allowed | Denied | Denied | Denied | Denied | Allowed |
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
| Collect a server diagnostic archive; read internal errors; check migrations<br>no policy pair; **decided outside the policy**, bypassed entirely when the server was started with `--debug` | Allowed | Denied | Denied | Denied | Denied | Denied |

---

## Table 2, fleet scope

The subject holds this role on fleet T and holds no global role. The cell answers for an object belonging to fleet T. A denial that follows only from the object being in a *different* fleet is not a condition, that is what fleet scope means.

| Action | Admin | Maintainer | Technician | Observer+ | Observer | GitOps |
|---|---|---|---|---|---|---|
| **Group 1, Signing in and holding a session** | | | | | | |
| Inspect your own sessions<br>`session · read` | Conditional (C03) | Conditional (C03) | Conditional (C03) | Conditional (C03) | Conditional (C03) | Conditional (C03) |
| Revoke your own session<br>`session · write` | Conditional (C03) | Conditional (C03) | Conditional (C03) | Conditional (C03) | Conditional (C03) | Conditional (C03) |
| Inspect anyone's sessions<br>`session · read` | Denied | Denied | Denied | Denied | Denied | Denied |
| Revoke anyone's session<br>`session · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| **Group 2, Accounts, roles and API identities** | | | | | | |
| List and read user accounts<br>`user · read` | Conditional (C02) | Conditional (C01) | Conditional (C01) | Conditional (C01) | Conditional (C01) | Conditional (C01) |
| Create a user account<br>`user · write` (C01 requires `object.id != 0`, so the self branch cannot be met by a create) | Conditional (C02) | Conditional (C01) | Conditional (C01) | Conditional (C01) | Conditional (C01) | Conditional (C01) |
| Edit your own account<br>`user · write` | Conditional (C01) | Conditional (C01) | Conditional (C01) | Conditional (C01) | Conditional (C01) | Conditional (C01) |
| Edit another user's account<br>`user · write` | Conditional (C02) | Denied | Denied | Denied | Denied | Denied |
| Delete a user account<br>`user · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| Change a user's role or fleets<br>`user · write_role` | Conditional (C02) | Denied | Denied | Denied | Denied | Denied |
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
| Delete a fleet<br>`team · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| Read the Unassigned fleet's settings<br>`app_config · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| **Group 4, Enroll secrets** | | | | | | |
| Read an enroll secret<br>`enroll_secret · read` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Denied |
| Change enroll secrets<br>`enroll_secret · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Denied |
| **Group 5, Global settings** | | | | | | |
| Read the global organization settings<br>`app_config · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| Change the global organization settings<br>`app_config · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| Read the global agent options<br>`app_config · read`; **decided outside the policy** | Allowed; field withheld | Allowed; field withheld | Allowed; field withheld | Allowed; field withheld | Allowed; field withheld | Allowed; field withheld |
| Change the global agent options<br>`app_config · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| Read the Fleet server version<br>`version · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| **Group 6, Hosts: reading** | | | | | | |
| Be allowed to look at hosts at all<br>`host · list` | Allowed | Allowed | Allowed | Allowed | Allowed | Denied |
| Read one host's record<br>`host · read` | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Denied |
| Resolve a host by identifier without host read<br>`host · selective_list` and `host · selective_read` | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C13) |
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
| Move a host between fleets<br>`host · transfer_host` | Conditional (C12) | Conditional (C12) | Conditional (C12) | Denied | Denied | Conditional (C12) |
| Cancel queued work on a host<br>`host · cancel_host_activity` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Denied |
| Ask a host to report again (refetch)<br>`host · list` then `host · read` | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Denied |
| **Group 8, Device actions** | | | | | | |
| Lock a host<br>`mdm_command · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Unlock a host<br>`mdm_command · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Wipe a host<br>`mdm_command · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Clear a device's passcode<br>`mdm_command · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Rotate a Mac's Recovery Lock password<br>`mdm_command · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Rotate a managed local account password<br>`mdm_command · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Send a raw MDM command<br>`mdm_command · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Unenroll a host from MDM<br>`mdm_command · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Read what a device said about a command<br>`mdm_command · read` | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Conditional (C15) | Denied |
| **Group 9, Labels** | | | | | | |
| See labels<br>`label · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed; no host membership |
| Create a label<br>`label · create` | Allowed | Allowed | Allowed | Denied | Denied | Allowed |
| Edit or delete a fleet's own label<br>`label · write` | Conditional (C08) | Conditional (C08) | Conditional (C08) | Denied | Denied | Conditional (C08) |
| Edit or delete a global label<br>`label · write` | Conditional (C08) | Conditional (C08) | Conditional (C08) | Denied | Denied | Conditional (C08) |
| **Group 10, Reports, live queries and carves** | | | | | | |
| See a saved report<br>`query · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Conditional (C09) |
| Create, edit or delete a saved report<br>`query · write` | Conditional (C15) | Conditional (C15) | Denied | Denied | Denied | Conditional (C15) |
| Run ad-hoc SQL<br>`query · run_new` | Allowed | Allowed | Allowed | Allowed | Denied | Denied |
| Run a saved report live against hosts<br>`targeted_query · run` | Conditional (C07) | Conditional (C07) | Conditional (C07) | Conditional (C07) | Conditional (C06, C07) | Denied |
| Use the live-query target picker<br>`target · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Denied |
| Read live-query results you did not start<br>no policy pair; **decided outside the policy** | Denied | Denied | Denied | Denied | Denied | Denied |
| See a legacy scheduled-query pack<br>`pack · read` | Denied | Denied | Denied | Denied | Denied | Denied |
| Edit or delete a legacy scheduled-query pack<br>`pack · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| Download a file carve<br>`carve · read` | Denied | Denied | Denied | Denied | Denied | Denied |
| **Group 11, Policies** | | | | | | |
| See a policy<br>`policy · read` | Allowed | Allowed | Allowed | Allowed | Allowed | Conditional (C10) |
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
| Preassign and match profiles during an MDM migration<br>`mdm_config_profile · write` and `team · write`, both on a zero-value object | Denied | Denied | Denied | Denied | Denied | Denied |
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
| Renew the Apple Business Manager token<br>`mdm_apple · read`, the renewal mutates under `ActionRead` | Denied | Denied | Denied | Denied | Denied | Denied |
| Place an ADE device in a fleet by platform<br>`mdm_apple · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| Add a Volume Purchasing token<br>`mdm_apple · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| Renew the Volume Purchasing token<br>`mdm_apple · write` | Denied | Denied | Denied | Denied | Denied | Denied |
| List Volume Purchasing tokens<br>`installable_entity · read` | Conditional (C15) | Conditional (C15) | Conditional (C15) | Denied | Denied | Conditional (C15) |
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
| Turn Windows device management off<br>`app_config · write` on `windows_enabled_and_configured` | Denied | Denied | Denied | Denied | Denied | Denied |
| Turn Windows device management on<br>`app_config · write` on `windows_enabled_and_configured` | Denied | Denied | Denied | Denied | Denied | Denied |
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
| Collect a server diagnostic archive; read internal errors; check migrations<br>no policy pair; **decided outside the policy**, bypassed entirely when the server was started with `--debug` | Denied | Denied | Denied | Denied | Denied | Denied |

---

## The condition register

Fourteen conditions numbered C01–C15. **There is no C14**, a draft C14 ("fleet-scoped roles cannot reach a host in the Unassigned fleet") turned out to be the host-shaped instance of C15 and was folded into it. The gap is deliberate.

**C01, the object user is the requester.** (RULE 012): the account is the caller's own and `object.id != 0`, for `read`, `write`, `change_password`. **Allowed** when the target user record is the caller's own. **Denied** for any other user, unless another rule grants it. Note the omission: changing a role is not in this list, so nobody can change their own role through the self branch.

**C02, team admin over a user, all-teams test.** (RULE 015), helper the subject is not an administrator of one of the fleets involved. **Allowed** when the target user belongs to at least one fleet **and** the subject is a fleet admin of **every** fleet the target belongs to. **Denied** when the target belongs to no fleet at all, or belongs to any fleet where the subject is not admin, including fleets the subject has no role in. C01 applies additionally and independently in every C02 cell.

**C03, the session belongs to the requester.** (RULE 018): the object belongs to the caller. **Allowed** for the caller's own sessions. **Denied** for anyone else's, unless global admin (RULE 019).

**C04, `gitops` and the collective team object.** (RULE 005): any authenticated subject may `read` the team object when `object.id == 0`. **Allowed** for `gitops` in that collective form only, the "all fleets" listing placeholder. **Denied** for a specific fleet: RULE 006 and RULE 007 both require `object.id != 0` and both omit `gitops`. GitOps can write a fleet it cannot read.

**C05, global `gitops` and enroll secrets.** (RULE 021): requires the secret is a global one rather than a fleet's. **Allowed** when the secret is the global enroll secret. **Denied** for any fleet's enroll secret, RULE 022 is the only fleet-scoped grant and it requires a the fleet-role lookup of admin or maintainer, which a global gitops identity does not have.

**C06, whether the saved report is marked runnable by observers.** **Allowed** for `observer`, global or fleet, only when the saved query is marked runnable by observers. **Denied** otherwise. For fleet-scoped admin, maintainer, technician and observer_plus the flag does not gate access, both branches exist (RULES 054–057 for `false`, 062–065 for `true`), but C07 still applies.

**C07, whether every fleet the request targets is one the subject holds a role on.** **Allowed** when either (a) the request names no target fleets at all the request names no target fleets at all, or (b) every fleet named in the fleets the request targets is one on which the subject holds a qualifying role, every named fleet must qualify, not merely one of them. The query itself must additionally be global a global one or owned by a fleet the subject holds a qualifying role on. **Denied** when even one named target fleet falls outside that set. A fleet-scoped `observer` is narrower still: admits a fleet only when it *is* the query's own fleet and the subject's role there is `observer`.

**C08, label authorship, fleet-scoped write.** (RULE 043): the object is global, `not is_null(object.author_id)`, the caller is the author. **Allowed** unconditionally for a label belonging to a fleet the subject holds the role on (RULE 045); and **allowed** for a global label only when the subject authored it. **Denied** for a global label authored by anyone else.

**C09, fleet-scoped `gitops` reading queries.** **Allowed** for a query owned by a fleet the subject holds `gitops` on (RULE 050). **Denied** for a global query: RULE 051 is the only grant covering the object is global for fleet-scoped subjects and its role list omits `gitops`.

**C10, fleet-scoped `gitops` reading policies.** **Allowed** for a policy owned by a fleet the subject holds `gitops` on (RULE 072). **Denied** for a global policy: RULE 073 omits `gitops`, and RULE 074 is technician/observer/observer_plus only.

**C11, global `observer` and a fleet-owned live query's targets.** (RULE 060) and (RULE 061). **Allowed** when the query is global (RULE 059, ), or when the query belongs to a fleet and either no target fleets are named or every named target fleet **is** the query's own fleet. **Denied** when a global observer targets any fleet other than the query's own.

**C12, transfer authorizes source and destination separately.** (RULE 028) / (RULE 034), plus the Go that raises them three times: destination, each distinct source fleet at, the Unassigned fleet handled by an explicit `&fleet.Host{TeamID: nil}` at (loop ). **Allowed** when the subject holds admin, maintainer, technician or gitops on **both** the destination fleet and every source fleet in the batch. **Denied** otherwise, and in particular, transferring a host **out of** the Unassigned fleet is denied to every fleet-scoped role, because authorizes a nil-team host and keys on `team_role(subject, object.team_id)`, undefined for nil. A second call site, authorizes the destination only.

**C13, GitOps reading an Apple device enrolled automatically.** The narrower read the policy grants GitOps is unconditional in itself, but the one route that uses it operatively assembles its response by calling a second lookup for iOS and iPadOS hosts, and that lookup authorises the host with a plain read, which GitOps is denied. A permission error is not a not-found, so the failure propagates and the whole request fails.

**Allowed**, with full host detail, for every host except an iOS or iPadOS host on an instance where Apple device management is enabled and configured. **Denied**, with the whole request failing, for an iOS or iPadOS host on such an instance.

**C14, scripts disabled deployment-wide.** When script execution is turned off for the deployment, Fleet skips authorisation entirely and refuses the request, so **the refusal does not depend on the role at all**. **Allowed** when scripts are enabled, according to the cell. **Denied for every role, including a global administrator**, when they are disabled. This is the one condition in the register that can override an `Allowed` cell outright, which is why it is a condition rather than a note.

**C15, the object must belong to a real fleet.** The single most consequential structural fact in the policy, and it accounts for most of the conditional cells. Fleet-scoped rules are keyed on the subject's role *for the object's own fleet*, and most carry an explicit guard against that fleet being absent.

**Allowed** when the object belongs to a fleet on which the subject holds the role. **Denied** when the object belongs to the Unassigned fleet, because the fleet-role lookup is undefined when there is no fleet, so **no fleet-scoped role of any kind reaches those objects.** A global role reaches them normally.

**Listing hosts is the exception, and it is why this looks like a bug from the interface.** The list rule asks only whether the subject holds a qualifying role on *any* fleet, and never inspects the object's fleet at all. So a fleet-scoped maintainer can see an Unassigned host in a list and cannot read it, act on it, or do anything else to it.

**Two further conditions are filed in the row universe's addendum and are not cell values here**, because they qualify an outcome rather than the decision: **C31**, transfer-by-filter reporting success having transferred nothing, which is the effect behind the `Allowed; moves nothing` cell on "Move a host between fleets"; and **C32**, renewing the Apple Business Manager token being authorised as a read, noted on "Renew the Apple Business Manager token".

---


## Actions that carry a secret

![Troubleshooting](../_assets/icons/troubleshooting.svg) Some of what Fleet can read is a credential, and the role names do not say so. These are the rows to decide separately when designing access, rather than assuming the answer falls out of a role:

| What is revealed | The row that governs it |
|---|---|
| A host's disk encryption recovery key | **Reading the host.** There is no separate permission |
| The macOS Recovery Lock password | The same |
| A managed local account password | The same |
| Certificate authority integration credentials | Reading certificate authorities **with secrets** |
| Enroll secrets | Reading enroll secrets |
| **A host's device page URL** | Its own row, decided outside the policy. Fleet's source describes this URL as a credential for acting as that device's end user, so handing one out is handing over that person's view |

**Those three are one permission decision and three separate rows, and the difference matters.** Fleet has no object type for a recovery key: revealing any of the three takes exactly the permission that reading the host takes, so the cells are identical. They stay three rows because a reader looking up who can reveal a Recovery Lock password must not have to know that Fleet decides it as a host read. **One decision is not one intent.**

So the group is five of the six roles at either scope, and at global scope that means every key in the deployment. [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md) covers what to do about that; this appendix's job is to say that it is not a separate decision, because everyone assumes it is.

## Version notes

![Reference](../_assets/icons/reference.svg) Verified against Fleet 4.90.1. The policy carries 154 rules over 49 object types and 16 actions; the 148 rows here are the administrator-facing projection of them, reconciled against the manual's shared capability register.

**Ten policy grants have no administrator-facing call site at this release** and are deliberately not rows. A grant nothing exercises would be a permission a reader could never use, and in at least one case it is the fossil of a route that no longer exists.

**Where a cell says a request succeeds and returns nothing, that is not a permission statement**, and it will change without the policy changing. It is recorded because the alternative is a reader concluding they have a broken deployment.
