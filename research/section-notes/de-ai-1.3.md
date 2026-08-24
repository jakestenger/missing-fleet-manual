# 1.3 Hosts, fleets, and labels — style-rules and de-AI pass

Target: `manual/01-foundations/1.3-hosts-fleets-labels.md`
Pass run 2026-08-20. **Facts unchanged; presentation only.** Verified against Fleet 4.90.1
(`git tag fleet-v4.90.1`). The research trail lives in `1.3-notes.md`; this file records what
this editing pass changed and, above all, **the code pointers deleted from reader-facing
prose** (STYLE §8). The section carried 29 Go file references and 53 inline line numbers
going in. Every one of them is tabulated below against the fact it supports, so a future
editor can re-verify without the prose carrying developer detail.

## Code-citation trail removed from the section

Each row: the fact as it now reads in the section, and the source pointer deleted from the
prose. All pointers are at tag `fleet-v4.90.1`.

### Host identity

| Fact retained in prose | Source pointer removed |
|---|---|
| The six host identifiers, their columns, and which three are `UNIQUE` | `server/datastore/mysql/schema.sql:1378-1432` |
| Enrollment match is a three-way priority lookup, lowest priority wins | `matchHostDuringEnrollment`, `server/datastore/mysql/hosts.go:2294-2368` |
| Priority 2 exists so ADE serial-only rows are found by an Orbit enroll | source comment "Apple DEP pre-creates host records with hardware_serial set, so orbit-enroll can find them this way", `hosts.go:2334` |
| Windows never matches by serial | serial blanked for Windows, source comment "to retain legacy functionality", `hosts.go:2399-2402` |
| A re-enroll fills empty fields and never overwrites an existing value | UPDATE built from `COALESCE(NULLIF(col, ''), ?)` over uuid, osquery_host_id, hardware_serial, computer_name, hardware_model, `hosts.go:2433-2444` |
| `team_id` is absent from both re-enroll UPDATEs | same statements, `hosts.go:2433-2444` |
| Orbit re-enroll clears pending MDM actions, and MDM status when the platform changed away from Windows | `hosts.go:2462-2473`, source comment "so that hosts that get re-imaged with other OS don't show erroneous MDM status" |
| osquery re-enroll discards every policy result and stamps `last_enrolled_at` | `deleteAllPolicyMemberships`, `hosts.go:~2693` |
| Duplicate identifiers merge with a WARN rather than failing | source comment "can happen if two devices have duplicate hardware identifiers or if orbit's node key file was deleted from the device", `hosts.go:2416-2422` |
| Host identity certificates refuse the enroll on a host ID mismatch | `hosts.go:2424-2429` |

### Fleets

| Fact retained in prose | Source pointer removed |
|---|---|
| One fleet column, so one fleet per host; deleting a fleet moves its hosts to no fleet | `hosts.team_id` nullable `int unsigned`, `ON DELETE SET NULL` to `teams`, `schema.sql:1414,1431` |
| The no-fleet bucket is its own scope, not a fallback for hosts in a fleet | `EffectiveTeamID`, `server/fleet/apple_mdm.go:458-462`, repeated verbatim at `server/fleet/windows_mdm.go:639` and `server/fleet/datastore.go:2457,2501`. Comment: "team_id=0 is its own team (the 'no team' / global scope), NOT a fallback for teamed hosts: a host with team_id=5 matches profiles with team_id=5 only, it does not also inherit team_id=0 profiles." |
| Delivery SQL compares with the null-safe operator, so unassigned hosts match | `hosts.team_id <=> vpp_apps_teams.team_id`, `server/datastore/mysql/vpp.go:2871`, same shape at `:2856`, `:2907`, `:2928` |
| Four reserved fleet names, case-insensitive after NFC normalisation | `server/fleet/teams.go:31-45` |
| Both spellings work in GitOps | `IsNoTeam()`, `IsUnassignedTeam()`, `pkg/spec/gitops.go:667-684` |

### The rename alias layer

| Fact retained in prose | Source pointer removed |
|---|---|
| The whole alias layer comes from one struct tag, on 65 Go files at this release | `renameto:"fleet_id"` beside `json:"team_id"`, `server/fleet/labels.go:216` |
| Paths are aliased from a declarative table of 47 entries that panics at startup if a canonical handler is missing | the alias table in the route registration (see `1.3-notes.md`) |
| Go source still says `TeamID`, `TeamPayload` | unchanged across the 65 files above |

### Labels

| Fact retained in prose | Source pointer removed |
|---|---|
| Three membership types and their numeric values | `label_membership_type`, `server/fleet/labels.go:98-133` |
| Cross-field validation names the offending field in its error | `ValidateLabelMembershipFields`, `labels.go:156-201` |
| `platform` accepts exactly five values | `labels.go:145-151` |
| Host vitals criteria is a `{vital, operator, value}` tree with `and` / `or` nesting | `labels.go:23-41` |
| Thirteen built-in label names are reserved against user labels | `ReservedLabelNames()`, `labels.go:316-331` |
| Built-ins mix membership types; iOS, iPadOS and Android are manual with an empty query | seed data, `schema.sql:1653` |
| `labels.team_id` is a nullable FK; NULL means global | `schema.sql:1643,1650` |
| A fleet-scoped label is distributed only to hosts in that fleet | `LabelQueriesForHost` filter `(team_id IS NULL OR team_id = ?)` |
| Label names are globally unique regardless of fleet scope | `UNIQUE KEY idx_label_unique_name`, `schema.sql:1645` |
| Whether a host is due for label queries is gated on the interval, and a refetch request bypasses the gate | `labelQueriesForHost`, `server/service/osquery.go:867-877`, `host.RefetchRequested` |
| Per-host jitter is `max_jitter_percent * interval_minutes / 100`, keyed to the host ID | `shouldUpdate`, `osquery.go:846-866` |
| Query selection filters on platform, dynamic type, and fleet scope | `server/datastore/mysql/labels.go:932-936` |
| Label queries go out named `fleet_label_query_<label_id>` | `osquery.go:1126` |
| Three-state result handling: nil leaves membership alone, true upserts, false deletes; label IDs sorted ascending | `RecordLabelQueryExecutions`, `labels.go:957-1054`; source comments "the query errored (e.g. extension socket unavailable), rather than returning a definitive 0 rows" and "to minimize deadlocks" |
| `hosts.label_updated_at` is stamped directly or through the async write channel | `labels.go:988-994` |
| The host vitals cron runs every 5 minutes, hardcoded | schedule `host_vitals_label_membership`, `server/fleet/cron_schedules.go:45`; job `cron_host_vitals_label_membership`, `cmd/fleet/cron.go:2129-2137`, calling `UpdateLabelMembershipByHostCriteria` per label |
| The cron lists labels with a synthetic global-admin filter, or fleet-scoped host vitals labels would be skipped | source comment "falls back to the 'global-only' filter (l.team_id IS NULL), which would silently exclude every fleet-scoped host vitals label and leave them unpopulated", `cmd/fleet/cron.go:2153-2158` |
| One failing label aborts the whole cron pass | same, `cmd/fleet/cron.go:2129-2137` |
| A label query that errors leaves membership alone | the `matches == nil` branch, `labels.go:974-978`; behaviour changed in 4.90.0, `CHANGELOG.md:125` |
| `label_membership` has no status column, only `created_at` and `updated_at` | `schema.sql:1620-1627` |
| A named label that does not exist is rejected, with the names collected | `DetectMissingLabels`, `server/fleet/labels.go:335` |

### Label targeting

| Fact retained in prose | Source pointer removed |
|---|---|
| The four label scope keys and where each is available | `server/fleet/api_policies.go:15-17`, `server/fleet/vpp.go:39-47,129-133`, `server/fleet/queries.go:313-319` |
| Label targeting on policies is Premium | `premium:"true"` on the policy fields, same files |
| Queries have no exclude form | `query_labels` has `require_all` and no `exclude` column, `schema.sql:2687-2693` |
| No label keys means every host in the fleet | `docs/Configuration/yaml-files.md:453,461,604` (now cited as fleetdm.com/docs/configuration/yaml-files) |
| The validation rules: one include scope, one exclude scope, no overlap, empty slice is "no value" | `verifyPolicyLabelScopes` and its docstring, `server/fleet/policies.go:199-234`; `ErrPolicyConflictingIncludeLabels`, `ErrPolicyConflictingExcludeLabels` |
| Delivery is a three-branch UNION, one branch per scope, gated in HAVING | `server/datastore/mysql/vpp.go:2855-2935` is the clearest instance |
| The exclude branch also requires every label in the list to be trusted for the host | `count_installer_labels = count_host_updated_after_labels`, same UNION |
| The published doc comment for include-any describes include-all; the SQL is any-of | `LabelScopeIncludeAny`, `server/fleet/labels.go:404-407`. **Source-comment error, still present at 4.90.1.** Dropped from reader prose as developer-only; recorded here. |

### Edge cases

| Fact retained in prose | Source pointer removed |
|---|---|
| Exclude-any ignores items scoped to labels created after the host's `label_updated_at` | source comment "exclude any, ignore software that depends on labels created _after_ the label_updated_at timestamp of the host (because we don't have results for that label yet, the host may or may not be a member)", `server/datastore/mysql/vpp.go:2881-2884` |
| An Apple MDM reset winds `label_updated_at` back to the 2000-01-01 sentinel | `server/datastore/mysql/apple_mdm.go:7935-7941`; the 4.90.1 fix, `CHANGELOG.md:20` |
| Apple hosts get built-in label memberships at enrollment, before osquery runs | `upsertMDMAppleHostLabelMembershipDB`, `server/datastore/mysql/apple_mdm.go:2081-2141`; source comment "it may still be some time before osquery is running on these devices" |
| The four names are looked up by name, and anything other than four rows logs and does nothing | source comments "since we cannot assume IDs on labels" and log line `expected 4 builtin labels but got N`, returns nil, `apple_mdm.go:2096-2099` |
| A title holds at most 10 packages per fleet; first-added wins | `MaxPackagesPerTitle`; published rule at `CHANGELOG.md:25` |
| Four-tier resolution, add order breaks ties within a tier only | `resolveFirstAddedInstallersForHost`, `server/datastore/mysql/software.go:3833-4001` |
| Tiers 3 and 4 are display-only and can never drive an install | source comment "availability and install decisions use inScope and never the fallback", `software.go:3838-3841` |
| Labels do not apply during setup experience | `server/datastore/mysql/setup_experience.go:336-337` |
| Host transfer batches at 10,000 hosts, one transaction per batch | `AddHostsToTeam`, `server/datastore/mysql/hosts.go:3609-3671` |
| The seven ordered steps inside the transaction | steps 1 to 3 `server/datastore/mysql/policies.go:2076-2108`, step 4 `policies.go:2126`, step 5 `hosts.go:3609-3671`, step 6 `cleanupDiskEncryptionKeysOnTeamChangeDB` in `server/datastore/mysql/disk_encryption.go:358-373`, step 7 `reconcileHostDeviceNamesForTeamDB` at `hosts.go:3659` |
| The Apple FileVault profile stands in for encryption on every platform | source comment "We are using Apple's encryption profile to determine if any hosts, including Windows and Linux, are encrypted. This is a safe assumption since encryption is enabled for the whole team", `disk_encryption.go:359-360` |
| The service layer checks authorization on both ends, diffs profiles, re-points ADE hosts, rebuilds Android certificate templates and app availability | `server/service/hosts.go:1249-1325` |
| Transfer runs under a retrying transaction wrapper | `withRetryTxx` |
| No fleet is 0 in the service and authz layers | `const PolicyNoTeamID = uint(0)`, `EffectiveTeamID()` |
| Authz accepts either representation | `any([is_null(object.team_id), object.team_id == 0])`, `server/authz/policy.rego:436` |
| GitOps refuses the `labels` key in the unassigned file | `pkg/spec/gitops.go:610-616` |
| `calendar_events_enabled` is fleet-only; `run_script` and `install_software` policy automations are not | `docs/Configuration/yaml-files.md:216` |
| Renaming a label in GitOps deletes and recreates it | `docs/Configuration/yaml-files.md:16` (now cited as fleetdm.com/docs/configuration/yaml-files) |
| Omitting `labels` preserves, including it prunes; six keys are exempt from the null-clears default | `docs/Configuration/yaml-files.md:28`; `name`, `labels`, `software`, `custom_host_vitals`, `settings`, `org_settings` at `pkg/spec/gitops.go:590,602-606` |
| `hosts` omitted and `hosts: []` differ, decided by inspecting the raw JSON | `Label.UnmarshalJSON`, `gitops.go:260-280`; `ModifyLabelPayload` carries the same distinction |
| Top-level label scope keys under `policies` do not apply per policy, and fail silently | `docs/Configuration/yaml-files.md:218` |

### Version notes

CHANGELOG line numbers removed from the version-notes table, in table order:
4.90.1 built-in label memberships during ADE (L10), 4.90.1 DEP re-enrol exclude-any (L20),
4.90.1 Windows profile still listed (L14), 4.90.0 ten packages per title (L25), 4.90.0 label
query error no longer clears membership (L125), 4.90.0 policies combine include and exclude
(L169), 4.90.0 Zorin OS platform (L51), 4.90.0 Orbit config batches extension label checks
(L78). All from `CHANGELOG.md` at tag `fleet-v4.90.1`. The note about the `changes/`
directory being empty at a release tag is contributor workflow and was cut; the reader-facing
pointer is now github.com/fleetdm/fleet/releases.

## Edit log

### Batch 1 — "What it is", Vocabulary, host identity

- Opening: "They are not two levels of the same hierarchy, and the no-fleet bucket is not a
  parent of the fleets. Get that wrong and you will spend an afternoon wondering why..."
  replaced with the positive statement of the same fact (§15): every fleet is a peer, the
  no-fleet bucket is a peer, an item reaches the hosts in its scope and stops there.
- **Diagram placeholder added: "Fleets scope, labels target"** (three peer rectangles, dashed
  label loops inside one of them). This is the section's headline model.
- **Diagram placeholder added: "What survives a rebuild"** (six identifiers by three events,
  tick or cross grid), placed under the identifier table.
- Vocabulary: "Called a team everywhere in the schema and in Go source" became "everywhere in
  the database and on most of the API" (§8, no Go source in reader prose).
- **`[ADE]()` flagged** at first use, in the identifier table. Same convention as 1.2.
- "Survives" cell for hardware serial: "The hardware. Not the OS." became "The hardware,
  across an OS reinstall." (§15).
- Enrollment matching rewritten with no function name, no file, no line numbers, and the
  `Match` column restated as plain predicates on named columns rather than SQL fragments.
- The two source comments quoted verbatim in the prose ("Apple DEP pre-creates host
  records...", "to retain legacy functionality") became statements of the behaviour and its
  reason.
- "**Windows never matches by serial**" became "**Windows matches on the osquery host
  identifier alone**" (§15). Same fact, stated as what happens.

### Batch 2 — re-enrollment, Fleets

- Heading "What re-enrollment does and does not change" became "What a re-enrollment changes"
  (§15). No inbound anchors to either form; checked with a grep across `manual/`.
- The `COALESCE(NULLIF(...))` statement, the two `hosts.go` paths in the table, and the
  duplicate-identifier source comment are all gone; behaviour kept in full.
- "**`team_id` is absent from both UPDATE statements**" became "**A re-enroll leaves the host
  in the fleet it is already in**" (§8 and §15).
- "TPM-backed host identity certificates" now defined in place as "where the host proves
  itself with a TPM-backed or Secure-Enclave-backed certificate", so no `[term]()` needed.
- "and never applies to Orbit" became "and governs the osquery enroll path" (§15).
- Heading "One fleet per host, and no inheritance" became "One fleet per host, and the scopes
  are peers".
- **The verbatim `EffectiveTeamID` source blockquote is gone.** Replaced with the behaviour in
  reader terms, and the brief's required framing preserved: "The no-fleet bucket is a scope
  with its own settings, a sibling of every named fleet", plus a worked instance and "no
  inheritance in either direction". Fact unchanged.
- The `<=>` explanation kept, because a reader writing reporting SQL needs it, and it is a
  MySQL operator rather than a Fleet internal. The `vpp.go` line numbers are gone and the
  example join is now generic.
- "What scopes to a fleet" second column retitled "Where the fleet is recorded" and its Go-ish
  precision softened to table-level description where the exact column adds nothing. Columns a
  reader actually queries in 8.6 (`policies.team_id`, `queries.team_id`,
  `enroll_secrets.team_id`, `labels.team_id`) kept verbatim.
- **`[VPP]()` flagged** at first use, in that table. "FMAs" spelled out as "Fleet-maintained
  apps".
- "RBAC" row retitled "Role assignments"; `user_teams` described rather than named.
- Reserved names: "NFC normalisation" became "Unicode normalisation", and `IsNoTeam()` /
  `IsUnassignedTeam()` dropped in favour of "accepted in GitOps and mean the same scope".

### Batch 3 — the rename alias layer, label membership types, built-ins, fleet-scoped labels

- Rename table: the "Go source" row deleted. The `MySQL tables and columns` row, the REST
  path rows, and the both-keys-in-responses row are the facts the brief requires kept, and
  they are untouched.
- The `renameto:"fleet_id"` struct tag and its file dropped; the prose now says one mechanism
  produces the whole alias layer, which is the reader-relevant part. The "65 Go files" count
  went with it. The 47-route alias list stayed as a route count, with "panics at startup"
  restated as "the server refuses to start".
- §15 in the same paragraph: "never count keys in a response assertion and never read an
  absent `team_id` as 'no fleet'" became "treat a response key count as meaningless, and read
  an absent `team_id` as 'this response used the new name'".
- Label membership types: the file pointer replaced by a lead-in sentence naming
  `label_membership_type` as the field, which is what an admin sees in the API and in GitOps.
- `platform` values: "Not `linux`, not `chrome`, not `ios`" became "`linux`, `chrome`, and
  `ios` are rejected, which catches people out". Kept as an explicit contrast under the §15
  exemption, because `linux` is the guess readers actually make.
- Built-in labels: `label_type = 1` and `ReservedLabelNames()` replaced with the behaviour
  ("Fleet creates and owns it, and both the UI and the API refuse edits").
- Heading renamed downstream, so the cross-reference here now points at
  `#deleting-a-built-in-label-stops-built-in-membership-on-apple-hosts`. Both ends updated in
  the same pass.
- Fleet-scoped labels: `labels.team_id`, the FK, the `UNIQUE KEY` name, and the
  `LabelQueriesForHost` predicate all dropped; all three effects of scoping a label kept,
  including the transfer step-3 cross-reference.

### Batch 4 — the membership pipeline, the host vitals cron, label targeting

- Heading "How dynamic label membership actually gets set" lost "actually" (§12).
- Pipeline steps 2 to 6: every function name, file, and line number removed. The three-state
  result handling (yes / no / errored) is kept in full, including the point that an errored
  query is distinct from a query returning zero rows, and the label-ID ordering is kept as
  "which keeps concurrent reports from deadlocking".
- Host vitals cron: schedule name kept (an admin sees it in `cron_stats`), the two Go file
  pointers and the synthetic-admin-filter source comment removed. The behaviour that survives
  is what a reader needs: the pass covers fleet-scoped host vitals labels too, and one failing
  label aborts the pass.
- Label targeting: the three `server/fleet/*.go` source lines and `premium:"true"` replaced
  with "Label targeting on policies is a Premium feature. On profiles, software, and queries
  it is available on every plan."
- "**Queries have no exclude form**" became "**Queries take include scopes**" (§15), with the
  absent exclude form stated once as the fact the reader needs.
- The `docs/Configuration/yaml-files.md:453,461,604` quote became a plain statement plus a
  reader-usable citation, fleetdm.com/docs/configuration/yaml-files.
- Validation rules: `verifyPolicyLabelScopes` and the two `ErrPolicy...` identifiers dropped;
  the rule itself, including "an empty list counts as 'no value'", kept word for word in
  substance.
- Heading "How it is stored: two booleans, not an enum" became "How it is stored: a pair of
  booleans" (§15).
- **The SQL fence under "The evaluation SQL" is gone.** Heading is now "How delivery evaluates
  a label scope", and the three branches plus the exclude-any trust condition are stated in
  prose. This preserves the hazard fact the brief requires, without `count_host_labels` and
  friends.
- **Dropped from reader prose: the `LabelScopeIncludeAny` doc-comment error.** It is a note to
  someone reading Go, which this audience is not. Recorded in the citation table above so it
  is not lost.

### Batch 5 — "Structuring scope for a real organisation"

Almost no code citations in this part; it was a voice pass.

- `user_teams` and "RBAC" replaced with "roles are granted per fleet" in three places.
- Heading "When it does not" became "When another fleet is the right answer" (§15). All three
  bullets already argued for a fleet, so the positive heading fits the content it had.
- "There is no label form to reach for" became "a fleet is the only way to vary them".
- "Labels are not an access control mechanism" became "Access control is a fleet-level
  concept: a role is granted on a fleet".
- "A new dynamic label is not authoritative for any host until that host reports" became "A
  new dynamic label becomes authoritative for a host when that host next reports". Same fact,
  positive form, and the exclude-any consequence kept.
- "It is bad for a baseline" became "It makes a poor baseline"; "Labels also cannot be
  declared in `fleets/unassigned.yml`" became "Labels belong in `default.yml`, since
  `fleets/unassigned.yml` refuses the `labels` key".
- "The cost is history and keys, not identity" became "A transfer costs history and keys;
  identity survives intact", and the run-on semicolon list broke into four sentences (sentence
  length was getting uniform through this stretch).
- "**a transfer is not a refresh**" became "**A transfer is a destructive operation rather
  than a refresh**". The disk encryption warning is unchanged in substance.

### Batch 6 — "Edge cases and precedence", first half

- "Fleets scope, labels target, and they compose with AND": the `<=>` mention became "the
  item's fleet is the host's fleet, counting no fleet as a fleet". The three no-fallback
  clauses stayed, compressed into one sentence, because that is the fact the section exists
  to make stick.
- Heading "Label membership is not instant, ..." became "Label membership lags, ..." (§15).
  The body still says label state is not current, which the brief requires kept.
- **The verbatim exclude-any source blockquote is gone**, along with
  `count_host_updated_after_labels` and the `hosts.label_updated_at >= labels.created_at`
  comparison written as SQL. Both hazards survive intact: an early exclude scope would
  over-deliver permanently, and the trust condition trades that for under-delivery.
- MDM-reset sentinel: `apple_mdm.go` pointer and the CHANGELOG line replaced by "a fix that
  landed in 4.90.1". Structural-hazard paragraph kept, with "it does not make label state
  instant" restated as "It does not make label state current".
- Heading "A deleted built-in label fails open and silent" became "Deleting a built-in label
  stops built-in membership on Apple hosts". The one inbound cross-reference (in "Built-in
  labels") was updated in batch 3. **The fail-open-and-silent behaviour is kept in words**:
  Fleet "stops there, with no error surfaced anywhere", and the four names looked up by name.
- `upsertMDMAppleHostLabelMembershipDB` and both source comments removed. The log string
  `expected 4 builtin labels but got N` **kept**, because an admin can grep for it and 8.3.6
  indexes it.
- Heading "A label query that errors does not clear membership" became "... leaves membership
  as it was" (§15). `RecordLabelQueryExecutions`, the `matches == nil` branch and the CHANGELOG
  line all gone; the 4.90.0 behaviour change kept by release number.
- **Four-tier package resolution rewritten as a table.** `resolveFirstAddedInstallersForHost`,
  `software_installers.id`, and the `inScope` source comment are gone. The caveat added after
  review is preserved and now stated twice, once in the table's "Can drive an install" column
  and once in bold prose: **tiers 3 and 4 are display-only and can never drive an install.**
- **Diagram placeholder added: "Four tiers of package resolution"** (funnel of four bands, top
  two badged "can be installed", bottom two "shown in Fleet, never installed").
- "**Labels do not apply during setup experience** at all" became "**Setup experience ignores
  label scope.**"
- Host transfer: `AddHostsToTeam`, all four `policies.go` / `disk_encryption.go` / `hosts.go`
  pointers, the raw `DELETE FROM` / `UPDATE` statements in the step table, and the
  disk-encryption source comment are gone. **All seven steps stay in order**, and the
  transaction, the batch size, the key deletion, and the re-escrow window are unchanged.
- "**Step 3 is misread in both directions**" became "**Step 3 removes memberships in
  fleet-scoped labels, and stops there**" (§15, and §12 no throat-clearing).
- "The service layer adds four things" became "Around that transaction, four more things
  happen"; "a fleet-scoped role can only move hosts" lost the "only".
- `[ADE]()` deliberately flagged once only, at first use in the identifier table; the transfer
  paragraph's later ADE mention is unflagged.

### Batch 7 — NULL vs 0, GitOps, empty/malformed, offline, troubleshooting, version notes

- The NULL-vs-0 table lost `PolicyNoTeamID`, `EffectiveTeamID()`, and the Rego expression with
  its file and line. The fact the table exists for, that both representations appear in the
  same request path, is unchanged.
- "Two things are unavailable in the no-fleet scope specifically" became "Two things behave
  differently in the no-fleet scope" (§15), and `calendar_events_enabled` being "fleet-only,
  while ... are not" is now stated as what each one does.
- The GitOps rename quote is kept verbatim, now attributed to
  fleetdm.com/docs/configuration/yaml-files rather than to a repo path and line. **The
  re-arms-the-timing-hazard consequence is kept**, since it is one of the two hazards the brief
  protects.
- `pkg/spec/gitops.go` pointers and `Label.UnmarshalJSON` / `ModifyLabelPayload` removed. The
  omitted-versus-empty distinction survives, described as Fleet looking for the key itself
  rather than at its parsed value.
- "`labels_include_any` at the top level of `policies` does not apply to each policy" became
  "applies to nothing" (§15); `verifyPolicyLabelScopes` and `DetectMissingLabels` gone from the
  empty/malformed table. Every error string in that table is kept, because a reader greps for
  those.
- Offline: "Dynamic label membership does not change while a host is offline" became "holds
  still while a host is offline"; "permanently trusted / permanently untrusted" became "trusted
  indefinitely / untrusted indefinitely".
- Retry: `AddHostsToTeam` and `withRetryTxx` became "A transfer retries its own transaction on
  a database conflict"; "replaying a label report is a no-op" became "changes nothing".
- Troubleshooting: "its absence is not evidence of a delivery failure" became "an empty log is
  telling you about targeting rather than about delivery" (§15).
- Version notes: all eight CHANGELOG line numbers removed (tabulated above), every row
  rewritten in the positive ("Apple hosts keep their built-in label memberships" rather than
  "no longer lose"), and the `changes/`-directory paragraph replaced with
  github.com/fleetdm/fleet/releases.

### Batch 8 — recheck pass, first half

Rechecking after the rewrites turned up four things the earlier batches had displaced:

- "What it is" table still said "RBAC"; now "role assignments", matching the rest.
- The "What survives a rebuild" diagram prompt asserted the hardware serial survives a
  mainboard swap, which the section never claims. Reduced to two columns the prose does
  support, "Survives an OS reinstall" and "Survives a re-enrollment", with the UUID caveat
  moved into the diagram's footnote.
- Rename table row "GitOps YAML ... Alias registered from the same tag" referred to the struct
  tag that batch 3 removed. Now "Both keys accepted."
- Vocabulary lead-in "The rename did not reach the database, and it reached the API only as an
  alias layer" became "The database still says `team` throughout, and the API accepts both
  names through an alias layer" (§15). Same for the section opener.

### Batch 9 — recheck pass, second half

- Restored a hedge I had flattened: step 3's Kept column said "global label memberships, most
  of them, including all built-ins" in the draft, and my first rewrite dropped "most of them",
  which would have turned a hedged claim into an absolute. The hedge is back, verbatim in
  substance. **Flagging it because it was a fact change, not a style change.**
- "How delivery evaluates a label scope": the bolded trust condition was left dangling as its
  own sentence fragment starting lower-case. Folded back into the sentence it belongs to.
- "Software delivered during setup experience is not filtered by labels at all" became "A
  label list on an item has no effect on what reaches a host during setup experience" (§15,
  and it drops a doubled statement).

## Final state

- **764 lines in, 791 lines out.** The growth is the three diagram placeholders (about 50
  lines); the prose itself is shorter than it was.
- **Zero Go file references and zero inline line numbers remain.** All 29 file references and
  all 53 line numbers are tabulated above against the facts they support. Also converted: four
  `docs/Configuration/yaml-files.md:N` citations, now fleetdm.com/docs/configuration/yaml-files;
  eleven `CHANGELOG.md:N` citations, now release numbers plus
  github.com/fleetdm/fleet/releases.
- Reader-usable identifiers deliberately kept: config keys (`osquery.label_update_interval`,
  `max_jitter_percent`, `osquery.enroll_cooldown`), API and GitOps keys (`labels_include_any`
  and friends, `label_membership_type`, `hosts`, `criteria`), the query name prefixes
  (`fleet_label_query_`, `fleet_detail_query_`), the cron name
  `host_vitals_label_membership`, the log string `expected 4 builtin labels but got N`, the
  validation error strings, `fleetctl` flags, and the state-table and column names Part VIII
  tells a reader to query (`hosts.team_id`, `label_membership`, `labels.team_id`,
  `label_updated_at`, `mdm_configuration_profile_labels`, `cron_stats`).
- **Zero em-dashes. No banned words.** Remaining uses of "only" all carry meaning ("indexed
  only", "display-only", "policies only", "the only way to vary them", the API error string
  `Specify only one of ...`).
- Three diagram placeholders: **Fleets scope, labels target**; **What survives a rebuild**;
  **Four tiers of package resolution**.
- `[term]()` flags now in the section: `[ADE]()` (identifier table, first use) and `[VPP]()`
  ("What scopes to a fleet", first use), matching 1.2's convention. `[SCEP]()` is not needed;
  the section does not use it. Node key, Orbit node key, osquery host identifier, dynamic /
  manual / host vitals / built-in label, and include-any / include-all / exclude-any are all
  defined in the section's own Vocabulary table, so they stay unflagged.
- No inline HTML comments were present in the file, so none to resolve.
- Cross-references: three headings were renamed, and the one internal link affected was
  updated in the same pass. Anchors `#fleet-and-team-mean-the-same-thing` and
  `#host-transfer-between-fleets` are unchanged. No other section links to a 1.3 anchor
  (checked with `grep -rn "1.3-hosts-fleets-labels.md#" manual/`, no hits). The five outbound
  links that resolve to missing files (1.6, 2.2, 3.5, 4.3, 6.3, 7.1) are all registered in
  OUTLINE.md as claimed-but-unwritten, and were already like that.
- Frontmatter: `verified_on: 2026-08-20`. `verified_against`, `verified_source` and
  `sidebar_position` untouched.

## Facts preserved deliberately, with the wording that carries them

The four items the brief protects, and where they now live:

1. **Four-tier package resolution with the display-only caveat.** "Multiple packages per
   title". Now a table with a "Can drive an install" column (yes, yes, no, no) plus the bold
   sentence "**tiers 3 and 4 are display-only: they can never drive an install.**" Stated
   twice on purpose.
2. **Label membership is not instant, and label-scoped delivery depends on current label
   state.** Both hazards intact. The exclude-any timing hazard is under "Label membership lags,
   and exclude-any is the scope that notices", including the structural-hazard paragraph and
   the GitOps rename that re-arms it. The built-in-label-loss hazard is under "Deleting a
   built-in label stops built-in membership on Apple hosts", including the fail-open-and-silent
   behaviour and the one-log-line-per-enrollment signal.
3. **Host transfer deletes the disk encryption key, with a re-escrow window.** Step 6 of the
   transfer table, plus "**Step 6 is destructive on every platform**" and "They re-escrow once
   encryption is enforced again; until then a locked disk is unrecoverable".
4. **The rename is an alias layer.** The surface table keeps the MySQL row and the both-keys
   response row, and the prose keeps "the database still says `team` throughout", "Responses
   carry both keys", and the both-names-in-a-query-string 400.

## Judgement calls, and things kept against the brief

- **Kept `hosts.team_id`, `label_membership`, `labels.team_id` and a handful of other column
  names.** The brief targets Go files, functions, and line numbers. These columns are what
  8.6.13 tells a reader to query when answering "was this host targeted", so removing them
  would break the section's own troubleshooting pointers. The "What scopes to a fleet" table
  was softened where the exact column added nothing.
- **Kept the `<=>` operator.** It is MySQL, not Fleet internals, and a reader writing reporting
  SQL against their own Fleet database gets the wrong answer without it.
- **Kept `platform` rejecting `linux`, `chrome`, `ios`** as an explicit negative, under §15's
  exemption for misunderstandings readers demonstrably have. Same for the enrollment
  consequence that an explicit `--host_identifier` turns off serial matching.
- **Dropped from reader prose, recorded here only:** the `LabelScopeIncludeAny` doc-comment
  error ("the comment describes include-all, the SQL is any-of, trust the SQL"). It is advice
  for someone reading Go, which this audience is not.
- **Dropped:** the note that the `changes/` directory is empty at a release tag. Contributor
  workflow, not administrator behaviour.

## No facts believed wrong

Nothing in the section reads as incorrect to me, and nothing was changed on substance. One
place is worth a future editor's eye, recorded without altering it: tier 2 of package
resolution is "in label scope, on another platform", and the section treats it as a tier that
can drive an install, on the strength of "only the two in-scope tiers can be the answer to why
did this host get that package". Whether an install can genuinely land from a package built for
a different platform is a question for 4.3, not for this pass.
