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
| After the last merge was split at research round 4 | **142** |

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

**Three decisions are made in Go rather than in the policy** and own their rows: the debug tree, a
host's device page URL, and reading the global agent options. **Twenty-six more attach to a row** as
a condition or a note rather than owning one. One, the endpoint-restriction middleware for API-only
identities, sits **above** the whole matrix and qualifies every row equally, which is why it is not a
row.

## Established at the tag

| Claim | Where it is evidenced |
|---|---|
| Six roles, the same set at both scopes, and an identity holds one scope or the other | Policy ledger, and the validator that rejects both |
| 154 policy rules over 49 object types and 16 actions | `policy-rules.md`, count cross-checked against a grep |
| **The policy denies by default**, so every ungranted combination is a denial | The default rule |
| **No fleet-scoped role reaches the Unassigned fleet**, because fleet-scoped rules key on a concrete fleet and the role lookup is undefined without one | Row universe, condition C15 |
| Reading a recovery key takes exactly the permission that reading the host takes; there is no separate object | Verified independently while correcting 1.4, 1.5 and 2.3 |
| **GitOps is denied host list and host read outright** | Policy ledger rows 18 and 20 |
| Eight routes are allowed by policy for GitOps and return nothing, because the host filter names no GitOps role | Row universe §6, filed as C31 |
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

## Rounds

| Round | Verdict | Outcome |
|---|---|---|
| Research 1 | NOT SOUND, six items | The matrix was a policy projection, not an administrator one |
| Research 2 | NOT SOUND, four items | Row universe built; C15 and the selective actions corrected |
| Research 3 | NOT SOUND, five items | 117 rows refused; merges and synonyms unpicked |
| Research 4 | NOT SOUND, two items | Last merge split, absent intents rerouted, 142 |
| Draft review 1 | Not yet run | |
