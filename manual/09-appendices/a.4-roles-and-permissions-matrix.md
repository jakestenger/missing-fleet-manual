---
title: "Roles and permissions matrix"
chapter: "Appendices and indexes"
section: "A.4"
sidebar_position: 4
status: drafting
verified_against: Fleet 4.90.1
verified_on: 2026-08-29
verified_source: "drafted against fleet-v4.90.1 (dd0200f062). The row universe was reconciled against the shared capability register over four research rounds and two later corrections; every published cell resolves to a policy rule, a Go-side decision, or an explicit Not established, and the row universe itself is a search result rather than a proof that nothing is missing. Citation ledger at research/section-notes/a.4-notes.md"
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

**Choose the table for your scope, find the action, then read across to your role. `Conditional` points to the condition register.**

**Authorisation is the intersection of an action, a role and a scope.** Licensing, platform support and interface availability are separate gates that this appendix does not answer, and a reader who conflates them will diagnose the wrong one.

## What this appendix carries

![Reference](../_assets/icons/reference.svg) The administrator-visible actions this appendix's research found, against all six roles, at both scopes. That is the breakdown [2.3](../02-administer-and-deploy-fleet/2.3-user-accounts-roles-and-service-identities.md) promises and the reason this appendix is the most-referenced one in the book. **The row universe is a search result and not a proof**: two rows were added after a review round found routes the earlier passes had missed, so a reader who finds another has found a gap rather than a contradiction.

**A cell answers what an administrator can actually obtain**, not what Fleet's authorization policy returns. Those are different questions more often than they should be. The policy is the largest input, and a decision can also be made by service middleware before the policy runs, by a response having a field stripped from it after the policy allowed the whole object, or by a database query that filters the result to nothing after the request succeeded. **All four change the answer, so all four are in the cells wherever this appendix found them.**

> **Masking is a property of the route, not of the object, and this appendix is organised by intent rather than by route.** Where a value is stripped from one response and not from another, the cell describes the reading route, and any row where that is known to differ says so. Reading the organisation settings is the case to know about: **the write response applies credential obfuscation and not the role masks the read response applies**, so an identity authorised to write receives fields it is masked from on read. At this release that affects exactly one identity, global GitOps, and three settings groups.

Three questions belong elsewhere. **Whether the capability exists on your platform is [a.2](a.2-platform-capability-matrix.md)**, which answers it per platform with the licence and prerequisites beside it. **Whether your licence includes it is a separate gate again**, and it is not folded into any cell here: a role that is allowed an action it has no licence for gets a licence error, not a permission error, and telling them apart is most of diagnosing a `403`. **Which interface can perform it is [a.5](a.5-interface-index.md)**, which answers it interface by interface.

## How Fleet decides

![Explanation](../_assets/icons/explanation.svg) Enough of the mechanism to predict an answer this appendix does not contain.

A request carries a **subject**, which is the authenticated identity and the roles it holds. It names an **object**, which is the kind of thing being acted on and, where the thing belongs to a fleet, that fleet's identifier. And it names an **action**, one of sixteen verbs.

**The policy is deny by default.** Every combination no rule grants is refused. That is a stated rule rather than an argument from silence, but it says nothing about any particular role, so a `Denied` cell below is not written off the default. **A `Denied` cell is checked against Fleet's own refusal tests wherever Fleet has such a test**, and those tests assert, role by role and action by action, that a request is turned away. **Where they do not cover a role, this appendix says so** instead of inferring the refusal, and the families found that way are named just before the tables. **That naming is what the search found rather than a closed list.**

**Sixteen actions, not two.** Reading and writing are the common pair, and the rest exist because Fleet needed to give one role one verb without the general one. Running a report is not writing it. Transferring a host between fleets is not writing the host. Reading a secret is not reading the object that holds it. **A matrix built on read and write would be wrong**, and it would be wrong in the permissive direction, which is why this one is not built that way.

> **Two vocabularies for one idea.** This book says *fleet*, which is Fleet's current product term. **Fleet's authorization vocabulary still says *team***, and so do the API fields, the object type printed under each action below, and the role a fleet membership records. The two words mean the same thing, and a reader who traces a cell into the API or into a GitOps file will meet the older one.

### Role and scope combine, and are exclusive

**The same six roles exist at both scopes**, and an identity holds one or the other, never both. Fleet rejects an account carrying a global role and a fleet role together.

That is why there are two tables rather than one with twelve columns. **You are always in exactly one of them.**

**A fleet-scoped role is scoped to a concrete fleet.** Most fleet-scoped rules are keyed on the object's fleet identifier and guarded against a null, and the helper that resolves a subject's role for a fleet is undefined when there is no such fleet. **So no fleet-scoped role of any kind reaches the Unassigned fleet**, whatever its role name suggests. Only a global role does. That single structural fact accounts for a large share of the conditional cells below, and it is the answer to a question that otherwise looks like a bug: a fleet administrator who can see an Unassigned host in a list and can do none of this appendix's host operations to it.

### Combinations Fleet refuses, and where it does not

Three kinds of refusal get confused, and they fail differently:

| Kind | Example | What you get |
|---|---|---|
| **Structural** | A global role and a fleet role on one identity | Rejected at write time, whatever the licence |
| **Licence-gated** | Technician, Observer+ or GitOps on Free | A licence error, not a permission error |
| **Ordinary denial** | Observer trying to write a policy | A `403` from the policy |

**Those checks live in the create and modify paths, not in the roles themselves.** Fleet has a third route that applies roles in bulk from a spec and it performs neither: no licence check and no API-only check. So the table above describes what two paths enforce rather than an invariant about what a role can be, and a Free deployment can be given Premium-only roles through that third route. **That route has its own row**, in the accounts group, and only a global administrator reaches it.

## Service identities and endpoint restrictions

![Reference](../_assets/icons/reference.svg) **API-only is a property of an account, not a seventh role.** Such an account holds one of the same six roles, and its token inherits that role and that scope. The activity record attributes its work to it, which is the argument in [2.3](../02-administer-and-deploy-fleet/2.3-user-accounts-roles-and-service-identities.md) for giving each automation its own identity rather than sharing a person's token.

**GitOps is intended to be API-only**, and the rule that enforces it is unreachable on the modify path: it fires only when the request carries an API-only field, and that endpoint rejects any request carrying one. So the role can be given to an ordinary interactive account, and [1.4](../01-foundations/1.4-identity-and-roles.md) covers what that account can then reach.

**Endpoint restrictions narrow an API-only account further**, to a named list of endpoints, and they sit *above* every row this appendix reaches through the authenticated API. Where such a list is non-empty, the middleware decides before the policy is consulted at all. **The debug tree is outside that chain.** It authenticates its own callers and never consults the endpoint list, so **a restricted API-only global administrator reaches those endpoints whether or not its list names them**. That is why the restriction is not a row: everywhere else it qualifies the rows equally. Configuring one is an ordinary row, in the accounts group.

## The permission matrix

![Reference](../_assets/icons/reference.svg) 152 administrator intents, grouped as a reader would look for them, with the policy pair underneath each so a cell can be traced.

## How to read the two tables

**Table 1 answers for a subject whose role is global. Table 2 answers for a subject who holds that role on a fleet and holds no global role.** The two scopes are mutually exclusive, and Fleet rejects an identity that tries to hold both, so a reader is always in one table or the other. Both tables carry the same 152 rows in the same order with the same wording, so they can be read side by side.

**The action column is the administrator's intent.** The `object · action` pair underneath it is the policy pair the intent resolves to, so a cell can be traced back to the rule that decides it. Some intents resolve to more than one pair, and a few resolve to none, because the decision is made in Go rather than in the policy; those rows say so.

**Cell vocabulary.** Five values and nothing else:

| Value | Meaning |
|---|---|
| `Allowed` | The request succeeds and returns what it promises. |
| `Denied` | The request is refused for this role at this scope. Where Fleet has a refusal test for it, the cell rests on that test; the families found to have no such test are named below. |
| `Conditional (Cnn)` | Allowed or denied depending on the condition; both branches are in the register below. |
| `Not applicable` | The product has **no such scoped operation**: the action exists, and this scope cannot hold the object. Never a way of saying a role is refused. |
| `Not established (Enn)` | Not determined; the register below says what was searched. |

**`Not applicable` and `Not established` are part of the vocabulary and no cell needs either at this release.** They are defined so that a future row that does need one is not written as a denial instead.

**50 cells carry a qualifier after their value**, because the request succeeds and the administrator still does not get everything the row's name promises. That is effective access, not a refusal, and there are six kinds:

- **An empty part, named.** 14 cells, every one of them GitOps. The policy permits the request, the request succeeds, and **the part of the answer that is filtered by fleet membership comes back empty**, because that filter recognises no GitOps role at either scope. **The qualifier names what is empty rather than declaring the operation empty**, because they are different: a label is still created, still edited and still deleted, and it is the host membership that is missing; a report is still returned and its stored results are not. **Only moving hosts by filter is a wholly successful no-op.** Eight routes are affected; they land on seven rows, and since every row is printed in both tables that is 14 cells. **Membership is emptied only when the request names its hosts.** A request that gives host identifiers instead takes a different path, is checked host by host, and attaches exactly the hosts it named. The qualifier is **not** applied to `host · list` or `host · read`, which are policy denials for GitOps and are simply `Denied`.
- **`Allowed; field withheld`**, on reading the global agent options. 11 cells. The request succeeds and the field is removed from the response body before it is sent. Only a global administrator receives the agent options this way.
- **`Allowed; SMTP and SSO withheld`**, on reading the global organization settings. 10 cells. Everything else in the settings comes back. The mail and single-sign-on groups are removed for every global role except administrator, and for every fleet-scoped identity that is not an administrator of at least one fleet.
- **`Allowed; other fleets' tokens withheld`**, on listing Volume Purchasing tokens at fleet scope. 4 cells. The request succeeds and the list is narrowed to tokens assigned to a fleet the requester can read, plus tokens assigned to all fleets. Unassigned tokens and other fleets' tokens are not in it, and their absence is not announced.
- **`Allowed; other fleets' results withheld`** and **`Allowed; other fleets' commands withheld`**, on reading what a device said about an MDM command and on listing the commands a host has been sent, both at fleet scope. 10 cells. **Fleet narrows the answer to the hosts the caller can see before it authorizes anything**, so the fleet-scope refusal the rest of this appendix records as C15 never arises on these two rows: the request succeeds, and the results belonging to other fleets and to the Unassigned fleet are simply not in it. **Their absence is not announced**, and the count Fleet prints is the count of what it returned, so nothing in the answer disagrees with anything else in it.
- **`other fleets' memberships withheld`**, on listing accounts at fleet scope. 1 cell. Each account comes back with its fleet memberships trimmed to the fleets the requester has a role in, so **a fleet administrator cannot learn through the listing** where else an account has access. **Reading one account is a different route and trims nothing**: where that read is authorised, the account comes back whole, memberships included.

**A prerequisite that sits above every cell the authenticated API decides.** When an API-only identity has been restricted to a named list of endpoints, any request to something outside that list is refused **before the authorization policy is consulted at all**, so no `Allowed` cell below can widen it. **One row is not under it.** The debug tree has its own authentication, outside the chain the restriction is wired into, and never consults the endpoint list, so a restricted API-only global administrator reaches those endpoints regardless. Everywhere else the restriction qualifies the rows equally, which is why it is not a row of its own. *Configuring* the restriction is an ordinary row, in group 2.

**Four rows are decided outside the policy** and say so in the row body: the debug tree, a host's My Device URL, reading the global agent options, and reading live-query results somebody else started. The last of those is the one row that is `Denied` in all twelve cells: the policy lets the request through, and Fleet then compares the requester against the identity that started the query, so **not even a global administrator can read a live-query stream they did not open**.

**Some denials rest on the rule set rather than on a refusal test.** Fleet's authorization tests assert refusals role by role, and this appendix's evidence pass found several places where they stop short of the full role set. **These are the gaps that search found, and the search was not exhaustive**, so read the list as a floor and not as a total. Those cells are named here rather than left looking like the rest:

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

**Nothing in those tests contradicts the cells**, and no rule in the policy grants the combinations. What is missing is Fleet's own assertion that they are refused, which is the evidence this appendix asks for everywhere else. They are the cells to challenge first if a deployment behaves otherwise. **A family absent from this table has not been shown to be covered**, only not to have been found missing.

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
| Create a user account<br>`user · write`; the account does not exist yet, so the self branch cannot apply | Allowed | Denied | Denied | Denied | Denied | Denied |
| Edit your own account<br>`user · write` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| Edit another user's account<br>`user · write` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Delete a user account<br>`user · write` | Conditional (C19) | Conditional (C19) | Conditional (C19) | Conditional (C19) | Conditional (C19) | Conditional (C19) |
| Change a user's role or fleets<br>`user · write_role` | Allowed | Denied | Denied | Denied | Denied | Denied |
| Apply a role specification for many accounts at once<br>`user · write`, taken once before any account is named, so neither the self grant nor a fleet administrator's grant can reach it | Allowed | Denied | Denied | Denied | Denied | Denied |
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
| Create a user account<br>`user · write`; the account does not exist yet, so the self branch cannot apply | Conditional (C02) | Denied | Denied | Denied | Denied | Denied |
| Edit your own account<br>`user · write` | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed |
| Edit another user's account<br>`user · write` | Conditional (C02) | Denied | Denied | Denied | Denied | Denied |
| Delete a user account<br>`user · write` | Conditional (C02, C19) | Conditional (C19) | Conditional (C19) | Conditional (C19) | Conditional (C19) | Conditional (C19) |
| Change a user's role or fleets<br>`user · write_role` | Conditional (C02) | Denied | Denied | Denied | Denied | Denied |
| Apply a role specification for many accounts at once<br>`user · write`, taken once before any account is named, so neither the self grant nor a fleet administrator's grant can reach it | Denied | Denied | Denied | Denied | Denied | Denied |
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
| Be allowed to look at hosts at all<br>`host · list` | Allowed | Allowed | Allowed | Allowed | Allowed | Denied |
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

**Nineteen conditions, C01 to C19, with no gaps in the numbering.** Every one of them states both branches. Eighteen are cited from at least one cell. **C03 is not cited at this release**, because the two rows that carried it turned out to be unconditional for every role; it keeps its number so that the research ledger behind this appendix still lines up.

**C01, the account is the requester's own.** **Allowed** when the account being read or written is the caller's own and that account already exists. **Denied** for any other account, unless a separate grant covers it. Note the two omissions. Changing a role is not on the self list, so nobody can change their own role this way. And a brand-new account has no identity yet, so **creating an account is never a self-service act**, which is why the creation row is a denial for every role that has no general grant rather than a condition.

**C02, a fleet administrator over an account, tested across every fleet that account belongs to.** **Allowed** when the target account belongs to at least one fleet **and** the caller administers **every** fleet it belongs to. **Denied** when the target belongs to no fleet at all, or belongs to any fleet the caller does not administer, including fleets the caller has no role in whatsoever. C01 applies additionally and independently wherever C02 appears.

**C03, the session belongs to the requester.** **Allowed** for the caller's own session, whatever role the caller holds and whatever scope it is held at. **Denied** for anyone else's, unless the caller is a global administrator. No cell cites this condition, because a row that says *your own* has already settled which branch applies.

**C04, GitOps and the collective fleet object.** **Allowed** for GitOps reading the "all fleets" placeholder that a fleet listing resolves to. **Denied** for a named fleet, which no reading grant extends to GitOps at either scope. **GitOps can therefore write a fleet it cannot read.**

**C05, global GitOps and enroll secrets.** **Allowed** when the secret is the deployment's global enroll secret. **Denied** for any fleet's own enroll secret: the only grant covering a fleet's secret asks for an administrator or maintainer role **on that fleet**, which a global GitOps identity does not hold.

**C06, whether the saved report is marked runnable by observers.** **Allowed** for an observer, global or fleet-scoped, only when the saved query carries that flag. **Denied** otherwise. For a fleet-scoped administrator, maintainer, technician or Observer+ the flag does not gate access at all, and Fleet covers both settings of it, but C07 still applies to those roles.

**C07, whether every fleet the request targets is one the caller holds a role on.** **Allowed** when the request names no target fleets at all, or when every fleet it does name is one the caller holds a qualifying role on. The query itself must additionally be a global query, or one owned by a fleet the caller holds a qualifying role on. **Denied** when even one named target fleet falls outside that set: **every named fleet must qualify, not merely one of them.** A fleet-scoped observer is narrower still, and admits a fleet only when that fleet *is* the query's own fleet and the observer's role there is observer.

**C08, who wrote a global label.** **Allowed** for a global label only when the caller created it. **Denied** for a global label somebody else created. Authorship is a question about global labels alone: **a label that belongs to a fleet is writable by an administrator, maintainer, technician or GitOps identity on that fleet whoever created it**, which is why the fleet's own label row is not conditional.

**C09, a fleet-scoped GitOps identity reading saved reports.** **Allowed** for a report owned by a fleet the identity holds GitOps on. **Denied** for a global report: the one grant that covers global reports for fleet-scoped callers leaves GitOps out.

**C10, a fleet-scoped GitOps identity reading policies.** **Allowed** for a policy owned by a fleet the identity holds GitOps on. **Denied** for a global policy, which no fleet-scoped GitOps grant reaches.

**C11, a global observer and a fleet-owned live query's targets.** **Allowed** when the query is global, or when the query belongs to a fleet and either no target fleets are named or every named target fleet is the query's own. **Denied** when a global observer targets any fleet other than the query's own.

**C12, a transfer is authorised at both ends.** **Allowed** when the caller holds administrator, maintainer, technician or GitOps on the destination fleet **and** on every fleet the hosts are being moved out of. Fleet checks the destination first, then each distinct source fleet in the batch, and it treats the Unassigned fleet as a source in its own right. Moving hosts **by filter** checks the destination first and then the source fleets of whatever the filter actually selected. **Denied** otherwise, and in particular **moving a host out of the Unassigned fleet is denied to every fleet-scoped role**, because the fleet-role lookup has nothing to key on when a host belongs to no fleet.

**C13, GitOps reading an Apple device that enrolled automatically.** The narrower read GitOps is granted is unconditional in itself, but the one route that uses it assembles its answer with a second lookup for iOS and iPadOS hosts, and that lookup asks for the ordinary host read GitOps does not have. A permission error is not a not-found, so the failure propagates and the whole request fails.

**Allowed**, with full host detail, for every host except an iOS or iPadOS host on a deployment where Apple device management is turned on and configured. **Denied**, with the whole request failing, for an iOS or iPadOS host on such a deployment.

**C14, script execution turned off for the deployment.** When script execution is turned off, Fleet refuses the request without evaluating the caller's role at all, so **the refusal does not depend on the role**. **Allowed** when script execution is on, as the cell says. **Denied for every role, including a global administrator**, when it is off.

**C15, the object must belong to a real fleet.** The single most consequential structural fact in the policy, and it accounts for most of the conditional cells. Fleet-scoped rules are keyed on the caller's role *for the object's own fleet*, and most carry an explicit guard against that fleet being absent.

**Allowed** when the object belongs to a fleet on which the caller holds the role. **Denied** when the object belongs to the Unassigned fleet, because the fleet-role lookup has nothing to resolve when there is no fleet, so **no fleet-scoped role of any kind reaches those objects.** A global role reaches them normally.

**Listing hosts is the exception, and it is why this looks like a bug from the interface.** The listing rule asks only whether the caller holds a qualifying role on *any* fleet, and never inspects the object's fleet at all. So a fleet-scoped maintainer can see an Unassigned host in a list and cannot read it or act on it through any of the host operations this appendix carries.

**C16, Windows device management needs its certificate and key first.** **Allowed** to turn Windows device management on when the server has been configured with the certificate and key pair that Windows enrollment needs. **Denied** when it has not, with a validation error rather than a permission error, and **that refusal does not depend on the caller's role either**. Turning Windows device management **off** carries no such prerequisite, which is why the two rows do not share one vector.

**C17, debug mode routes the request past Fleet's own role check.** A server started in debug mode generates a token and prints a debug address carrying it. Fleet then routes any debug request that presents a token to a handler outside its own authentication, so **Fleet's global-administrator check is not applied to that request at all**. **Allowed**, in the sense that the caller's Fleet role does not decide the answer, for a request presenting a token to a server started in debug mode. **What that handler accepts instead is settled outside Fleet's own source and this appendix does not claim it**, so a deployment that runs in debug mode should be treated as having no Fleet-side role check on the debug tree rather than as having a known one. **Denied** for every role except a global administrator on a server started normally, where Fleet's own debug authentication decides.

**C18, listing accounts is scoped by the fleet the request names.** **Allowed** for a fleet administrator when the request names a fleet they administer. **Denied** when the request names no fleet, or names one they do not administer. A global role needs no fleet in the request and is not subject to this. **A fleet-scoped role other than administrator cannot list accounts on this route**, which is a statement about the listing and not about every way an account can be read: reading one account is a separate row with its own cells.

**C19, deleting an account, including your own, and the last global administrator.** Fleet decides account deletion with the same permission it uses for editing an account, and **every authenticated identity may write its own account**, so the permission itself never stands between you and deleting yourself, whatever role you hold. **Allowed** when the account being deleted is the caller's own, at either scope; and for anybody else's account where a separate grant covers it, which for a global administrator is every account. **Denied** for anybody else's account where no such grant covers it, and **denied for every caller, a global administrator included, when the account being deleted is the last remaining global administrator**, which Fleet checks after the permission and refuses with a validation error rather than a permission error. **The last-administrator branch is about the account being deleted and not about who asked**, so it refuses a global administrator deleting the last remaining one as readily as it refuses that administrator deleting itself. This is not a documented self-service route and it is worth knowing before an automation account is given a role on the assumption it cannot remove itself.

**C14, C16 and C17 are the three conditions that do not turn on the caller's role at all.** Two of them refuse a request the role alone would allow, and the third admits one the role alone would refuse. They are conditions rather than notes for exactly that reason: a note beside a cell would not tell you the cell's answer can be wrong.

**Two further conditions are filed in the row universe's addendum and are not cell values here**, because they qualify an outcome rather than the decision: **C31**, transfer-by-filter reporting success having transferred nothing, which is the effect behind the `Allowed; moves nothing` cell on "Move hosts between fleets by filter"; and **C32**, renewing the Apple Business Manager token being authorised as a read, noted on "Renew the Apple Business Manager token".

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
| **A host's device page URL** | Its own row, decided outside the policy. Fleet treats this URL as a credential for acting as that device's end user, so handing one out is handing over that person's view of Fleet |

**Those three are one permission decision and three separate rows, and the difference matters.** Fleet has no object type for a recovery key: revealing any of the three takes exactly the permission that reading the host takes, so the cells are identical. They stay three rows because a reader looking up who can reveal a Recovery Lock password must not have to know that Fleet decides it as a host read. **One decision is not one intent.**

So the group is five of the six roles at either scope, and at global scope that means every key in the deployment. [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md) covers what to do about that; this appendix's job is to say that it is not a separate decision, because everyone assumes it is.

## Version notes

![Reference](../_assets/icons/reference.svg) Verified against Fleet 4.90.1. The policy carries 154 rules over 49 object types and 16 actions; the 152 rows here are the administrator-facing projection of them, reconciled against the manual's shared capability register.

**Ten policy grants are not published as rows**, because the research pass found no administrator-facing route that exercises them, and in at least one case the grant is the fossil of a route that no longer exists. **That is a search result and not a proof.** So are the row universe itself and the list of untested refusal families above: those are the three claims in this appendix that rest on having failed to find something, and all three are written that way so a reader who does find the missing thing knows which claim gave first.

**Where a cell says a request succeeds and returns nothing, that is not a permission statement**, and it will change without the policy changing. It is recorded because the alternative is a reader concluding they have a broken deployment.
