---
section: "A.4"
---

# a.4 Roles and permissions matrix, citation ledger

Drafted 2026-08-29, after **four research rounds**, three of which returned NOT SOUND. Held to Part
IX's cell-level evidence rule ([`../appendix-structure.md`](../appendix-structure.md)).

**The verification trail lives outside this repository**, per `README.md` in this folder. The
per-cell citations are in `../../missing-fleet-manual-private/research-sensitive/`: `a.4-scratch-matrix.md`
for the policy ledger, `a.4-scratch-rowuniverse-v2.md` for the row universe and its addendum, and
`a.4-tables.md` for the assembled tables with every rule number and line reference intact. The
extractor that guarantees rule coverage is `../../missing-fleet-manual-private/research/extract-policy-rules.py`.

## How the row universe was arrived at, since the number moved twice

| | Rows |
|---|---|
| First attempt, policy pairs treated as rows | 102 |
| First row universe | 117 |
| After merges undone and false synonyms separated | 141 |
| After the last merge was split at research round 4 | 142 |
| After draft review round 1 named six unlisted actions | 148 |
| After draft review 2 split two rows that hid two outcomes | 150 |
| After draft review 3 admitted two routes the earlier passes missed, bulk role specification and the MDM command queue | **152** |

**The 117 was 25 rows too low and both causes were one mistake made twice**: collapsing distinct
administrator intents onto a shared twelve-cell vector, once under the name "merge" and once under
the name "synonym". The synonyms were the worse half, because several were **semantic opposites**,
install against uninstall and enable against disable, which are never synonyms whatever their cells
say.

**Fourteen merges were undone.** The pattern in almost all of them was a read folded onto a write
because the twelve cells matched.

**One survived scrutiny and one did not.** Certificate-authority listing and detail inspection are one
reading family and stay merged. Reading Apple push-certificate status and listing Apple Business
Manager tokens do not, and the third fact is why: one of the operations behind that read **mutates**,
under the read action. Filed against Fleet as C32, with the impact stated as nil, because the object
grants read, write and list to the global administrator alone.

## The rule that decides what a cell says

**A cell answers what an administrator can obtain, not what the policy returns.** Four layers
contribute and all four are in the cells: the policy; service middleware that can decide before the
policy runs; response masking that strips a field after the policy allowed the object; and datastore
filtering that can empty a result after the request succeeded.

**Four decisions are made in Go rather than in the policy** and own their rows: the debug tree, a
host's device page URL, reading the global agent options, and reading a live-query result stream you
did not open (`server/service/service_campaigns.go:113`, after a permissive authorize at `:62`).
Draft review 2 added the fourth; the first three were already published. **Twenty-five more attach to
a row** as a condition or a note rather than owning one. One, the endpoint-restriction middleware for API-only
identities, sits **above** the whole matrix and qualifies every row equally, which is why it is not a
row.

## Established at the tag

| Claim | Where it is evidenced |
|---|---|
| Six roles, the same set at both scopes, and an identity holds one scope or the other | Policy ledger, and the validator that rejects both |
| 154 policy rules over 49 object types and 16 actions | `policy-rules.md`, count cross-checked against a grep |
| **The policy denies by default**, so every ungranted combination is a denial | The default rule |
| **No fleet-scoped role reaches the Unassigned fleet**, because fleet-scoped rules key on a concrete fleet and the role lookup is undefined without one | Row universe, condition C15 |
| Reading a recovery key takes exactly the permission that reading the host takes; there is no separate object | Verified independently while correcting 1.4, 1.5 and 2.6 |
| **GitOps is denied host list and host read outright** | Policy ledger rows 18 and 20 |
| Eight routes are allowed by policy for GitOps and return nothing, because the host filter names no GitOps role | Row universe §6, filed as C31. They land on seven published rows, so 14 cells |
| The label routes empty membership **only when hosts arrive by name**; raw host identifiers take a different path and are authorized host by host | `server/service/labels.go:116` and `:283` resolve names through the team filter; `:130` and `:300` then call `authorizeWriteLabelOnHosts` (`:187`), which authorizes each loaded host for `write_host_label` |
| Transfer by explicit host identifiers **executes** for global GitOps; only transfer by filter is the successful no-op | `server/service/hosts.go:1249` loads by ID with no team filter; `:1410` filters and returns early on zero hosts at `:1429` |
| Reading a live-query result stream you did not start is refused for **every** role including global admin, by an ownership comparison after a permissive authorize | Verified directly; Fleet's own comment states the intent |
| Ten policy grants have no administrator-facing call site and are not published as rows | Row universe §1, re-verified by grep at this commit |

## Scope decisions, for a reviewer to challenge

**The `object · action` pairs stay in the table.** STYLE §8 forbids naming files, paths, line numbers,
functions and internal identifiers in reader-facing prose, and every one of those was stripped from
this appendix: 50 source citations came out. The pairs are a different thing. They are Fleet's own
authorization vocabulary rather than an implementation detail, and they are the only mechanism by
which a reader can trace a cell to the rule that produced it. **If the reviewer disagrees, the column
comes out and the tracing moves here.**

**Licence is not a column and not a cell qualifier.** The part-level agreement makes licensing a
separate gate, and folding it in would have produced the project's least reliable claim class inside
its most-referenced table. A role allowed an action it has no licence for gets a licence error, not a
permission error.

## Not established

**The behaviour of two role-validation rules on every mutation path.** The bulk role-spec endpoint
performs no licence check and no API-only check, and the rule confining GitOps to API-only accounts
is unreachable on the modify path. Both are filed as C27 and S9. **What is not established is whether
any further path bypasses them**, because that would need integration tests rather than reading.

**Three refusal families have no positive `allow: false` assertion for every role in the cell**, found
while answering draft review 2's finding 11. The cells are consistent with the rule set and no rule
grants the combination, but Fleet does not assert the refusal, so the boundary evidence Part IX asks
for is absent. The appendix now names all three in reader-facing prose rather than letting them look
like the tested cells.

| Family | Test | Roles the test omits |
|---|---|---|
| Another user's session, read and write | `server/authz/policy_test.go:104` (`TestAuthorizeSession`) | Global `gitops`, and every fleet-scoped role. Covered: nil, global admin, maintainer, no-roles, observer, observer_plus, technician |
| Invites, read and write | `server/authz/policy_test.go:364` (`TestAuthorizeInvite`) | Global `gitops`, and every fleet-scoped role. Covered: nil, global admin, maintainer, no-roles, observer, observer_plus, technician |
| User accounts, all five actions | `server/authz/policy_test.go:186` (`TestAuthorizeUser`) | Global `gitops` entirely; fleet-scoped maintainer, technician, observer_plus, observer and `gitops`. Only team-admin shapes are covered, at `:323`, `:339`, `:346` and `:357` |

**The allowed half of the session rows needs no test**, because the rule granting a caller its own
session (`server/authz/policy.rego:234-239`) carries no role predicate at all: it tests only
`object.user_id == subject.id`. That is why "Inspect your own sessions" and "Revoke your own session"
became twelve `Allowed` cells rather than twelve conditionals.

## Draft review 2, the source each correction rests on

Every finding was re-verified at `fleet-v4.90.1` (`dd0200f062`) before it was applied. None was
overruled.

| # | Correction | Evidence at the tag |
|---|---|---|
| 1 | Empty-result qualifiers completed to 14 cells; the transfer row split | `server/datastore/mysql/mysql.go:870-928` names no `RoleGitOps` at either scope; `server/service/hosts.go:1249` against `:1410`; `server/service/labels.go:116`, `:283` |
| 2 | Own-session and own-account rows are unconditional for every role | `server/authz/policy.rego:234-239` (session, no role predicate) and `:165-170` (self read/write/change_password); `server/service/sessions.go:58`, `:100`; `server/service/users.go:692`; tests `server/authz/policy_test.go:112-141` |
| 3 | Creating an account is a denial, not a condition, for ten cells | `server/service/users.go:134` authorizes a zero-ID user, so the self rule's `object.id != 0` can never hold; refusals at `server/authz/policy_test.go:258`, `:271`, `:284`, `:297`, `:310` |
| 4 | Fleet admin can delete a fleet user; fleet admin and fleet GitOps can delete their own fleet | `server/service/users.go:961` authorizes `user · write` on the loaded target; `server/service/users_test.go:202` (`shouldFailTeamDelete: false`); `ee/server/service/teams.go:898`; `server/authz/policy_test.go:546`, `:574` |
| 5 | Account list and detail read split; C18 added; list memberships masked | `server/service/users.go:495-521` (list authorizes a synthetic user carrying only the requested fleet) and `:479-492` (`filterUserTeamsToRequesterScope`); `server/service/users.go:642` (detail read authorizes the loaded user) |
| 6 | Organization-settings reads carry a masking qualifier on ten cells | `server/service/appconfig.go:163-186` withholds SMTP and SSO unless global admin or admin of any team, and agent options unless global admin; the write response at `:331-339` obfuscates but applies no role mask |
| 7 | Fleet-scoped Volume Purchasing token listing is a filtered success, not C15 | `ee/server/service/vpp.go:1541-1595`; tests `ee/server/service/vpp_test.go:400-406` (team maintainer and technician scoped to their fleet plus all-fleets; team observer forbidden) |
| 8 | C16, the Windows certificate and key prerequisite | `server/service/appconfig.go:2135-2140` refuses turning Windows MDM on when the WSTEP pair is unset; turning it off has no equivalent |
| 9 | Fleet GitOps host-by-identifier is C13 **and** C15 | `server/service/hosts.go:1060` then `:1071`; `server/authz/policy_test.go:1282-1291` denies selective read of the nil-fleet host and allows it for the GitOps fleet's host |
| 10 | C08 removed from the fleet-owned label row | `server/authz/policy.rego:482-488` grants team write on a fleet's own label unconditionally; authorship (`:464-471`) applies only when the label is global |
| 11 | Negative-evidence rule reopened; three untested families named | See **Not established** above |
| 12 | Register and prose recounted; C17 added; four Go-side rows | `cmd/fleet/serve.go:982-990` and `:1366-1372` (the debug token handler is chosen before any role check); `server/service/service_campaigns.go:113` |
| 13 | STYLE 8 sweep and repair of the sentences the earlier citation strip broke | C07's duplicated clause, C11's dangling parenthesis, C12's missing call-site names and literal Go value, and the API-only paragraph's "calls ... at" all rewritten as behaviour |

**One correction outside the thirteen findings, and the new defect behind it.** While checking finding
4 the delete-user path turned out to authorize deletion with the same action as profile editing, and
the self rule grants that action unconditionally, so **any account can delete itself at any role and
either scope**. `server/service/users.go:961` calls `Authorize(user, ActionWrite)` on the loaded
target; `server/authz/policy.rego:165-170` grants `write` whenever `object.id == subject.id`; the
route is registered at `server/service/handler.go:339`; and no guard exists beyond
`DeleteUserIfNotLastAdmin` (`server/datastore/mysql/users.go:466`), which fires only when the target
holds the global admin role. The cells for "Delete a user account" said `Denied` for every non-admin
role and were wrong in the self case, so **C19 was added** and the row now carries it at both scopes.
This change was not asked for by the review; it is flagged here so round 3 can challenge it.

## Round 2's own account, because the commits do not carry it

**The a.4 round 2 changes are spread across three commits whose messages describe other work**
(`f4945fa`, `2ebc7e2`, `19faa07`). They landed that way because the appendix was being edited by a
subagent while the session committed unrelated work with `git add -A`. **Nothing is lost and the file
is correct**, but git archaeology on this appendix will mislead, so the account lives here instead.

**The process rule that follows:** commit explicit paths, never `-A`, while a subagent has a file
open. Recorded in HANDOFF as well.

### What round 2 found, and the shape it shared

**The largest class was a condition placed on an intent whose own wording had already fixed the
allowed branch.** Inspecting and revoking your own session are not conditional for any authenticated
role, because the granting rule carries no role predicate at all. Thirty-three cells were wrong that
way across sessions and own-account editing. Ten more read `Conditional` on account creation, where
the authorization object is a zero-identifier user so the self branch can never succeed; those are
denials.

**Round 1's own repairs were the largest source of new defects, for the third time in this project.**
The empty-result qualifier had been attached at the wrong grain: transfer by explicit host
identifiers executes, and only transfer by filter returns success with nothing moved; label
membership empties only when hosts arrive by name, because raw identifiers take a different path.
Five printed qualifiers became fourteen.

**The appendix was making an absence argument in its own prose.** It said denied cells need no atomic
refusal because absence is the rule in a deny-by-default policy. That is the one thing the part
agreement forbids by name. Denied cells now rest on positive refusal tests, and **the three families
whose tests omit roles are named in the appendix** rather than quietly inferred: another user's
session, invites, and user accounts.

### The security finding, verified before filing

**S13. Any Fleet account can delete itself, at any role and either scope.** Fleet decides account
deletion with the same action it uses for editing a profile, and the policy grants that action
unconditionally whenever the object is the caller. The one guard fires only when the target holds the
global administrator role, and it exists to stop a deployment losing its last administrator rather
than to stop an account removing itself.

**Why it is worth a condition rather than a note.** An administrator sizing access from the role
names reads "delete a user account" as an administrator power, because that is what every interface
makes it look like. An automation identity given observer or GitOps can remove its own account, and
that account is the subject of its own audit trail, so what goes is both the access and the record of
who held it. C19 carries it at both scopes.

## Rounds

| Round | Verdict | Outcome |
|---|---|---|
| Research 1 | NOT SOUND, six items | The matrix was a policy projection, not an administrator one |
| Research 2 | NOT SOUND, four items | Row universe built; C15 and the selective actions corrected |
| Research 3 | NOT SOUND, five items | 117 rows refused; merges and synonyms unpicked |
| Research 4 | NOT SOUND, two items | Last merge split, absent intents rerouted, 142 |
| Draft review 1 | NOT READY, five items | All applied. Six actions added: deleting a user, deleting a fleet, turning Windows management **on**, and three Volume Purchasing token actions. The empty-result qualifier was at the wrong grain and is now effect-specific. C14 added for disabled scripts, which overrides an Allowed cell for every role including a global administrator |
| Draft review 2 | NOT READY, thirteen items | **All thirteen applied, none overruled.** Two rows split (account list against detail read; host transfer by name against by filter), 150 rows. Wrong cells corrected in ten places. C16, C17, C18 and C19 added; C03 kept but no longer cited. The negative-evidence rule was reopened and three untested refusal families are now named in the appendix. STYLE 8 sweep removed every rule number, policy expression, Go name and literal value, and repaired the sentences an earlier citation strip had broken |
| Draft review 3 | NOT READY, nine items | **Eight applied in full plus the a.4 side of the ninth; none overruled.** Seven device-action rows had given GitOps a permission it does not hold, because each service path takes a broad host decision before the MDM one; those fourteen cells are now denials and the rows print the gate. The MDM-command-result row's five fleet cells were conditional on a branch that cannot occur, since Fleet narrows the answer by fleet visibility before it authorizes, and that is a sixth qualifier kind. Two rows added, bulk role specification and the MDM command queue, taking the tables to 152 rows and the qualified cells to 50 across six kinds. C19 now also governs the global-administrator deletion cell, and its last-administrator branch is about the account being deleted rather than the caller. The endpoint restriction no longer claims to sit above the debug tree, which authenticates itself. The negative-evidence disclosure grew from three families to twelve and now says the search was not exhaustive. C17 withdrawn to what Fleet's own source shows |
