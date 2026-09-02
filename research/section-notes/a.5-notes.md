---
section: "A.5"
---

# a.5 Action-to-interface index, citation ledger

Drafted 2026-08-29 from **four independently built research columns**, one per interface, each
covering all 348 rows of the shared capability register. Held to Part IX's cell-level evidence rule
([`../appendix-structure.md`](../appendix-structure.md)) and to the organising claim in the same
file: Fleet's interfaces overlap but are not interchangeable, and each administrative action has a
specific set of supported control surfaces.

**The verification trail lives outside this repository**, per `README.md` in this folder. The
per-cell citations with `path:line` are in `../../missing-fleet-manual-private/research-sensitive/`:

- `a.5-ui-column.md`, 348 entries, one per row, prose form with a leading value.
- `a.5-restapi-column.md`, 348 entries with an explicit `Cell:` field, plus its own section tally.
- `a.5-gitops-column.md`, 348 table rows carrying cell, key, omission behaviour and evidence.
- `a.5-fleetctl-column.md`, 348 table rows carrying cell, command and evidence, plus the
  cross-column comparison that raised the reconciliation problem.

Row universe: `../../missing-fleet-manual-private/research/capability-register.md`, CAP-001 to
CAP-348. Source of truth for every re-check: `/Users/jake/Source/Fleet/fleet-public` at tag
`fleet-v4.90.1`, commit `dd0200f062c5982c46dd3bf8de81a6b5c0c5ce6d`, confirmed with
`git rev-parse HEAD` and `git describe --tags` before work started. `main` was never read.
`fleet-confidential` was never opened. Upstream library source was not treated as evidence.

## Extraction, and why it was mechanical

The four columns were parsed into one table by script rather than read into prose, because the
failure this appendix most needed to avoid is a transcription error inside 1,392 cells.

`extract.py` (session scratchpad) parses each column in its own format, refuses to run if any of the
348 rows is missing from any column, and normalises the five values. **Its output was validated
against each column's own published tally before anything was reconciled**, and all four matched
exactly:

| Column | Full | Partial | Read only | Unsupported | Not established | Matched its own tally |
|---|---|---|---|---|---|---|
| UI | 196 | 50 | 12 | 16 | 74 | yes |
| REST API | 175 | 99 | 12 | 51 | 11 | yes |
| `fleetctl` | 179 | 51 | 8 | 108 | 2 | yes |
| GitOps | 123 | 31 | 0 | 192 | 2 | yes |

One extraction bug was caught by that check and fixed: the `fleetctl` parser was matching CAP-263 in
an earlier summary table rather than in the register-rows section, so both table parsers were scoped
to the register-rows span between named headings, with an assertion that the span is non-empty.

## The reconciliation, which was the first job and is the reviewer's first target

The `fleetctl` researcher flagged one conflict before handing over: five rows where that column says
`Read only` because the client reads a value and the REST column says `Unsupported` because no route
writes it, **while both are reading the same response**. Published as-is that produces five false
claims of `fleetctl` exclusivity.

Sweeping for the whole class found **17 rows in conflict, 29 cells changed, in six classes**. Every
change is asserted in `reconcile.py`: the script refuses to run if a cell's value before the change
is not what the decision expected, so a column edited later cannot be silently overwritten.

### Class 1: the read-intent convention, 8 cells

**The largest class, and it is a convention divergence rather than a factual one.** The UI and
`fleetctl` columns both declared, in writing, that where the register's action is itself a read, an
interface that returns the thing completely is `Full`, and that `Read only` is reserved for a row
whose action includes changing something. **The REST column used `Read only` to mean "a GET exists
and no mutating sibling does"**, regardless of the action.

Published unreconciled, four of those cells would have claimed the UI is the only interface that can
read the organisation-wide activity feed, one host's activity feed, the disk-encryption status
summary and the identity-provider connection status. All four are false: the REST column's own
entries cite the routes.

**Ruling: adopt the convention two of the four columns already declared and apply it to all four.**
Eight REST cells changed.

| Row | From | To | Note |
|---|---|---|---|
| CAP-015, CAP-016 | Read only | Full | The activity module registers exactly two routes, both GET, and the action is a read |
| CAP-241 | Read only | Full | Six buckets across three platforms, Premium |
| CAP-294 | Read only | Full | The SCIM details route is the administrator-facing connection status |
| CAP-305 | Read only | Full | Same `/debug/migrations` path `fleetctl debug migrations` is a thin client over. **Two columns, one route, two values** |
| CAP-309 | Read only | Full | Matches UI and `fleetctl`, which were already `Full` |
| CAP-212 | Read only | Partial | The delivery-evidence gap is real: OS inventory reports what is running, never whether the enforcement was delivered. Matches UI and `fleetctl` |
| CAP-233 | Read only | Partial | See class 3 |

**Four REST `Read only` cells were kept**, because their action genuinely includes changing
something the interface cannot change: CAP-019, CAP-257, CAP-310 and CAP-344.

### Class 2: read without write, where a column missed its own sibling evidence, 2 cells

The exact class the `fleetctl` researcher predicted, and it turned out to be **inside the REST
column rather than between two columns**. Three register rows describe the same two process-
configuration keys. CAP-257 covers both and the REST column marked it `Read only`, citing the
`logging` block returned by `GET /api/_version_/fleet/config` with `result.plugin` and
`status.plugin`. CAP-295 and CAP-296 are those same two keys split apart, and the REST column marked
both **`Unsupported`, "Route: none found"**.

Re-verified at the tag rather than taken from either column: `server/service/service_appconfig.go`
`LoggingConfig` at `:125-140` builds `logging.status` from `conf.Osquery.StatusLogPlugin` and
`logging.result` from `conf.Osquery.ResultLogPlugin`; `server/fleet/app.go:1981-1986` declares the
struct; `server/service/appconfig.go:229` attaches it to the config response through
`enrichedAppConfigFields` (`server/fleet/app.go:1056-1062`).

**Ruling: CAP-295 and CAP-296 become `Read only` in the REST column**, matching `fleetctl` and the
REST column's own CAP-257.

**Of the researcher's original five, three had already converged** on `Read only` in both columns
(CAP-019, CAP-257, CAP-344) and only two were live. The prediction was right about the class and
generous about the count.

### The vocabulary rule this class forced, now stated in the appendix

The brief asked for a rule covering "an interface can read a value that nothing can write", because
the five values do not distinguish it. The rule adopted, and published under **How to read it**:

> `Read only` means the interface can show you the value and cannot change it. **It is a claim about
> the interface, not about Fleet.** It does not imply that another interface can write.

And because that leaves a real fact homeless, the appendix publishes the complement mechanically:
**41 rows have no `Full` and no `Partial` in any column, and 7 of those are readable somewhere**
(CAP-019, CAP-195, CAP-257, CAP-295, CAP-296, CAP-310, CAP-344). That is the honest home for
"readable, unwritable anywhere", and it needed no sixth value.

### Class 3: a server-side incompleteness is shared by every reader, 1 cell

CAP-233, reading what a device said about a command. The REST column established positively that
Android is accepted and returns an empty list, with Fleet's own comment saying responses are not
stored. Re-verified at `server/service/mdm.go:938-941`. **That branch is in the shared service
layer**, so it governs the UI, the API and `fleetctl` identically.

The UI column had `Partial`; `fleetctl` had `Full` on the strength of a different boundary (text
output only). **Ruling: `fleetctl` becomes `Partial`.** A caller cannot tell Android's empty list
from "no results yet", whichever interface it used.

### Class 4: a `Not established` a source check settles, 4 cells

**A wrong `Not established` is a failure in the same way a wrong `Unsupported` is**, so four UI cells
were re-checked at the tag rather than accepted.

| Row | From | To | What settled it |
|---|---|---|---|
| CAP-344 | Not established | Read only | **A wrong `Not established`.** The researcher searched the server-config key names (`osquery_policy_update_interval`) and not the response field. `config.update_interval.osquery_policy` is read at `frontend/pages/policies/ManagePoliciesPage/components/PoliciesTable/PoliciesTable.tsx:229`, declared at `frontend/interfaces/config.ts:217` |
| CAP-019 | Not established | Unsupported | `grep -rn "\.logging" frontend/pages frontend/components` returns only `logging.result` reads, at `ManageQueriesPage.tsx:402-405`, `QueryDetailsPage.tsx:352-356`, `EditQueryForm.tsx:717-722` and `SaveNewQueryModal.tsx:307-311`. `logging.audit` is read nowhere. **Sibling wired, sibling not**, which is the boundary shape the UI column itself accepted for CAP-121 and CAP-231 |
| CAP-296 | Not established | Unsupported | Same grep, same result, for `logging.status` |
| CAP-305 | Not established | Unsupported | `frontend/utilities/endpoints.ts` contains no `/debug` path at all, and the UI column's own preamble makes that file the closed set of what the UI can call |

**The other 66 UI `Not established` cells were left alone**, and that is a deliberate stopping point
rather than an oversight. Twenty-one of them sit on rows where all three other columns found
`Unsupported`; converting those on the neighbours' evidence is exactly the inheritance the part
agreement forbids. The appendix publishes the 21 as a named soft spot instead.

### Class 5: arming against performing, 13 cells across 4 rows

Four rows name an act performed by Fleet or by the person holding the device, where what an
administrator controls is the switch. **The four columns graded three different targets**: the
GitOps column graded the configuration and said so (three cells written `Full (configuration)`), the
UI graded whichever surface it found, and REST and `fleetctl` graded the act.

**Ruling: arming a capability is `Partial`; performing it is `Full`.** This uses the existing
vocabulary, carries the distinction rather than picking a winner, and makes all four columns answer
the same question.

| Row | Result | Reasoning |
|---|---|---|
| CAP-002, sign in through the IdP | UI `Full`; the other three `Partial` | The UI is where the act happens. The other three can write `sso_settings` and cannot sign anyone in. `fleetctl`'s positive refusal (`fleetctl login` prints that email and password login is not supported on SSO-enabled accounts) survives inside `Partial` |
| CAP-003, just-in-time account creation | All four `Partial` | No interface performs it; the account is created inside the SSO callback. All four can write `enable_jit_provisioning` |
| CAP-292, attach the end user's IdP identity | All four `Partial` | Collection is automatic at enrollment. All four can write the arming configuration; the API can additionally undo what was collected |
| CAP-254, grant a one-time bypass | All four `Partial` | The grant is an end-user act on the device page. All four can write `conditional_access.bypass_disabled`, verified in the UI at `frontend/pages/admin/IntegrationsPage/cards/ConditionalAccess/ConditionalAccess.tsx:340` |

**The refinement that keeps this from swallowing everything**: a mere prerequisite an interface
happens to control (an enroll secret, say) does not upgrade a row. `Partial` is for the switch that
decides whether the capability functions at all.

### Class 6: an end-user surface is not administrator support, 1 cell

CAP-204, letting a user install everything offered to them. The REST column marked it `Unsupported`
because the only route is on the device endpointer. The UI column marked it **`Full`, on the
end-user surface**, and its own evidence names the device-token route.

**The UI column was internally inconsistent on this**: it applied the administrator rule to CAP-237,
writing `Unsupported` for an administrator and describing the end-user page in prose, and did not
apply it to CAP-204 or CAP-254.

**Ruling: `Unsupported` for CAP-204 in the UI column**, with the end-user surface in prose. Published
unreconciled it would have claimed the UI is the only interface for an action no administrative
interface performs.

### What the reconciliation changed about the published conclusions

| Claim | Before reconciling | After |
|---|---|---|
| Rows where only the UI can act | 9 by the raw columns, 12 by the UI column's own three-column computation | **4**, and all four are Android or ChromeOS enrollment |
| Rows where only `fleetctl` can act | 11 | **10**. CAP-305 left the list because the API reads migrations through the same path |
| Rows where only the REST API can act | 16 | 16, unchanged |
| Rows where only GitOps can act | 0 | 0 |

**The brief's "twelve rows are UI-only, nine of them one family" is the UI column's figure, computed
before the `fleetctl` column existed and against a looser test.** The appendix publishes 4, recounted
from the table it prints, because five of the twelve are reachable by `fleetctl` packaging or
`fleetctl login`, two are `Read only` rather than support, and one is CAP-204 above. **The story
survives and sharpens**: the surviving four are still enrollment, and they are the two platforms with
no other way in.

## Established, and what the appendix leads with

| Claim | Note |
|---|---|
| **`fleetctl api` is not `fleetctl` support; `gitops`, `apply` and `delete` are** | Decides 145 rows: 45 `[api-reachable]` become `Unsupported`, 100 `[spec-file]` rows count. The asymmetry is the appendix's most interesting idea and is stated where the reader meets it |
| **`apply` reaches two spec kinds GitOps cannot express** | `pack` has no GitOps key at all, and `user_roles` is never populated by the GitOps path. This is why Rule 2 is not a transcription of the GitOps column |
| **The REST column's boundary is exhaustive, not sampled** | Fleet's shared user authenticator has exactly five registration sites, plus the `/debug/` tree behind its own global-admin middleware. It changed 33 answers a naive reading would have called `Full` |
| **GitOps has no read direction at all** | 20 rows the other columns call `Read only` are `Unsupported` here, and that is stated as a non-disagreement |
| **GitOps omission semantics are the sharpest material in any column** | Omitting some keys clears what they describe, omitting others turns features on, and a third group is genuinely left alone. **Which rule applies is only discoverable by reading the client** |
| **`fleetctl` is Fleet's build tool** | 10 exclusive rows, 9 of them packaging, the self-hosted update repository and repository scaffolding |
| **The UI cannot run an ad-hoc script** | Fleet's own source says the field is supported for the command line only |
| **The UI cannot write software inventory at either scope** | It reads the setting in six places and writes it nowhere |
| **The UI is one control for two platforms on disk encryption** | One value covers FileVault and BitLocker; there is no per-platform switch |
| **41 rows have no supported interface** | Mostly process configuration and deployment infrastructure. 7 of the 41 are readable somewhere |

## Deliberately not established

**72 rows carry at least one `Not established` cell. No row carries four**, so every action has at
least one interface answer resting on evidence.

**Thirteen rows are unsettled in more than one column.** Two are open in three columns and are the
same two questions each time: package variants (CAP-179) and the Windows automatic-against-manual
enrollment control (CAP-279). **Both were reached independently by two researchers**, which argues
the questions are real. What would settle CAP-179 is the server-side batch software-installer
handler, read for how it groups entries by title. What would settle CAP-279 is the Windows MDM
settings card in the frontend, read for which stored field its controls write.

**Eleven are deployment and operations rows** where the question is what an operating practice looks
like rather than what Fleet does. Fleet's source cannot settle them in either direction and this
manual verifies against Fleet's source.

**The 70 UI cells are the appendix's largest soft spot and are published as such.** 33 of the 70 are
in sections S, T and U, and 21 sit on rows where the other three columns all found `Unsupported`.
Resolving those on neighbour evidence is forbidden by the part agreement; the appendix names the
number instead.

**Two questions inherited from a.7 and not reopened**, because settling either needs source outside
this checkout: whether `--config` is accepted after a subcommand that does not declare it, and which
error path a flag or usage failure takes. Both are decided by the command-line framework. Neither
changes a cell.

## Structural decisions, and the reasoning behind each

### The matrix carries values only, and the boundaries are modelled above it

The enumeration line for a.5 is "enumerate every action against four interfaces; **model and point
at** why partial interfaces differ; do not attempt every button, endpoint, flag or YAML field".

247 cells are `Partial`. A per-cell boundary column would have been 247 short claims inside the
appendix's most consulted table, which is the shape a.2's ledger warns about, and it would have
drifted from the four research columns at the first correction. **The boundaries are instead modelled
as recurring shapes**, one section per column, each naming the shape rather than the row. A reader
who learns four shapes can predict a row the table does not contain, which is the test the part
agreement sets.

Five boundaries that no model predicts are published as blockquote callouts, matching a.2's
"rows worth reading before you plan".

### The second table is kept, and curated rather than transcribed

The part agreement records the reviewer changing position on this: dropping automation as a column
would have made a.5 wrong by omission, because policy automations, webhooks, schedules and
integrations cause actions no operator invoked.

**The register marks 141 rows as self-initiated and the table publishes 34.** The other 107 are
ordinary periodic collection, where "self-initiated" means a detail query ran on schedule. Those are
not administrative actions and listing them would have turned the table into the vendor catalogue the
agreement refuses. The 34 published are the ones that change state without an operator.

### 348 rows here against 273 in a.2, and it is not a contradiction

a.2 merged CAP-048 into CAP-029 and set aside 88 non-device-facing rows. **The shared register was
deliberately not edited while three researchers were reading it as their row universe for a.5**, per
a.2's own ledger. So a.5 uses the register as it stands and the appendix carries a short section
saying where the two deliberately differ. **The merge should be applied to the register before a.1
projects from it.**

### Interface support and permission are separate gates, said twice

Once in "What this appendix carries" and once in the value table, because the failure it prevents is
a reader treating a `Full` cell as an authorisation answer. a.4 is the authorisation projection and
this appendix links to it rather than qualifying cells.

## Defects

**No new Fleet defect was found while drafting.** Three were found while the `fleetctl` column was
built and are already filed as **C54, C55 and C56**; four more came out of the GitOps column and are
in that file as D1 to D4. The queue stands at **C56, D48, S18** and this appendix does not move it.

The one thing drafting did surface is **a research defect rather than a Fleet defect**, recorded here
because the review structure exists to catch exactly it: the REST column contradicted itself across
CAP-257 against CAP-295 and CAP-296, and the UI column contradicted itself across CAP-237 against
CAP-204 and CAP-254. **Both were internal to a single column** and neither would have been visible
without building the cross-column table. The `fleetctl` researcher's flag found the class from
outside; the sweep found the instances inside.

## Rounds

| Round | Verdict | Outcome |
|---|---|---|
| Column extraction | Clean | All 348 rows present in all four columns. Output matched every column's own published tally exactly. One parser bug found and fixed by that check |
| Reconciliation sweep | **17 rows in conflict** | 29 cells changed across six classes, every change asserted. Five false exclusivity claims removed, one `Not established` corrected, one class traced to a column contradicting itself |
| Draft | Written | Matrix generated from the reconciled table by script; prose written to the four boundary models |
| Recount | **Clean** | All published figures re-derived by parsing the printed table, not the research. Published counts asserted equal to the recount |
| Checkers | **Clean** | `check-links`, `check-em-dashes`, `check-crossrefs`, `check-headings` and `unwrap.py dryrun` all exit 0. Two advisory heading notes are keyword false positives on "conditional" and "self-hosted" |
| Draft review 1 | Not yet run | Coverage |
| Draft review 2 | Not yet run | Cell-by-cell evidence audit |
| Draft review 3 | Not yet run | Fresh whole-appendix read plus cross-appendix consistency |

## The recurring defect this appendix was most at risk of

**Publishing an exclusivity claim that is an artefact of two columns using different conventions.**

Every one of the five false exclusives found here had the same shape: two columns read the same
mechanism, one graded the action and one graded the mechanism, and the difference read as a fact
about Fleet. **None of them was a wrong reading of source.** Both columns were right about what they
each measured.

The defence that worked is the one to reuse: **compute the exclusivity list mechanically and treat
every entry as a hypothesis until the other columns' evidence for that row has been read.** An
exclusive cell is the highest-consequence cell in an interface matrix and it is the one a naive
assembly gets wrong most often, because it is produced by three negatives rather than by one
positive.

---

## 2026-09-01 reconciliation to the current register

Owner-requested focused pass. A.5 was a stale projection: A.1 holds 354 unique CAP IDs; A.5 projected 347. Programmatic set-diff (grep CAP IDs, `comm`) showed A.5 is a strict subset of A.1 missing exactly 7 IDs: CAP-048, CAP-349, CAP-350, CAP-351, CAP-352, CAP-353, CAP-354.

**Resolutions:**
- **CAP-048** ("Enroll a personally owned iPhone or iPad"): a.2 and A.5 had both dropped it, citing a.2's strict-subset merge. But 3.5 documents the personal-link BYOD path (serial+UDID, Free) as **distinct** from account-driven Managed Apple Account enrollment (CAP-049; enrollment identifier, Premium) — line 119 says so explicitly. So CAP-048 is a genuine distinct interface action. **Restored to A.5** (Full/Partial/Unsupported/Unsupported, mirroring CAP-047). a.2's merge stands as its own platform-scope decision; the a.2 relationship note now frames this as a scope decision, not a contradiction. A.1 unchanged.
- **CAP-349** (connect a CA): Full/Full/Full/Full. GitOps confirmed by 2.13's "GitOps representation" / certificate-authorities spec. Section A.
- **CAP-350** (enumerate egress destinations): Not established/Not established/Not established/Unsupported (GitOps has no read direction; no single Fleet interface enumerates egress — the manual assembles it in 2.2). Section H.
- **CAP-351** (retire 2017 pack): Partial/Full/Full/Unsupported, from 4.2 (native `upgrade-packs`/`convert`/`get packs`; pack apply API; UI disables at the packs page; not modern GitOps). Section E.
- **CAP-352** (retry install by hand): Full/Full/Unsupported/Unsupported (A.1: no fleetctl verb, no GitOps path). Section K.
- **CAP-353** (managed local admin pw): Full/Full/Unsupported/Unsupported. Section L.
- **CAP-354** (MCP): deliberate exclusion — a client of the REST API, not an interface of its own (the "MCP server is not a column here" note). A.5 now covers all of A.1 except this one.

**Counts recomputed from the matrix (awk), all updated to stay consistent:** 353 rows / 1,412 cells; value table (UI 196/54/12/21/70, REST 185/104/6/46/12, fleetctl 178/56/8/108/3, GitOps 121/34/0/196/2, Total 353 each); Full+Partial reach 289/250/234/155; api-only 47; gitops-served 101 (×2 sites); GitOps-Unsupported 196; GitOps-Unsupported-but-UI+REST-perform 104; all-four-Full 82 / all-agree 95; UI Not-established 70; rows with ≥1 Not-established 72. (Left "247 boundaries" in the Partial discussion as-is — its derivation was already non-obvious and not cleanly recomputable; flagged, not guessed.)

## 2026-09-02 fix: six label mismatches against a.2 (round3 B1)

The new `build/check-cap-ids.py` (written for round3's a.2 collision fix, [[a.2-notes]]) checks
that a.2 and a.5 agree verbatim wherever they carry the same CAP-ID. Six didn't: CAP-178, 189, 196,
228, 243, 275. Checked each against its own cell values rather than just picking a side — a.2's
wording won every time, because a.5's was narrower than the row's actual platform reach (e.g.
"Prepare a Mac before its user reaches the desktop" for CAP-189, a row whose cells are Full across
macOS, iOS/iPadOS and Windows; "Allow a custom FileVault profile" for CAP-243, which is also
Windows-conditional per C091). Relabeled to match a.2 in all six.
