# De-AI + style pass: 8.12 Audit logs

Target: `manual/08-troubleshooting/8.12-audit-logs.md`. Before: 571 lines. After: 567 lines.
Pass finished 2026-08-21.
Pass: style rules (STYLE.md §0, §8, §14, §15) + de-AI. Presentation only; facts unchanged.

## Citation ledger: path removed -> fact it supports -> how the section now says it

| Removed reference | Fact it supported | Replacement in prose |
|---|---|---|
| `server/datastore/mysql/schema.sql:121-143` | `activity_past` column list | Table stands on its own, no source line |
| `server/datastore/mysql/migrations/tables/20260316120008_RenameActivitiesToActivityPast.go` | `activities`/`host_activities` were renamed to `activity_past`/`activity_host_past` | "a schema migration renamed them" |
| `server/activity/internal/mysql/activity.go:58` | global list query filters `WHERE host_only = false` | "The global list query filters those rows out" |
| `server/activity/internal/mysql/new_activity.go:55-59` | `host_only` set at write time from the type's `HostOnly()` method | "The flag is set at write time by the activity type itself" |
| `server/activity/api/list_activities.go:22-35` | API/stream entry struct field list | "The API response and the streamed record are the same object" (endpoint paths in 8.12.5 untouched) |
| `server/fleet/activities.go` (+ the `grep -A2 'ActivityName() string {'` recipe) | ~200 activity types, each a Go struct with `ActivityName()` | "Roughly 200 types exist"; reader-usable substitute is `SELECT DISTINCT activity_type FROM activity_past` plus fleetdm.com/docs/contributing/audit-logs |
| `cmd/fleet/cron.go:2102-2126` | `activities_streaming` cron, 5-minute interval | Cron name and interval kept, source line dropped |
| `server/activity/internal/service/service.go:24` | 500-row fetch batches, loop until short batch | Same fact, no path |
| `cmd/fleet/logging.go:80-88` | audit logger built only under Premium | "Fleet Premium. Without a Premium license Fleet builds no audit logger" |
| `server/fleet/app.go:1489-1495` | retention unlimited unless expiry enabled | Table row stands alone; Source column dropped from the retention table |
| `cmd/fleet/cron.go:1516-1528` | `cleanup_activities` runs inside `cleanups_then_aggregation` | Job and schedule names kept |
| `cmd/fleet/cron.go:1526` | 5,000-row per-run delete cap, sized for ~120,000 activities/day | Fact kept; "the source comment sizes this" removed |
| `cmd/fleet/cron.go:1530-1538` | enabling expiry also enables live-query cleanup on the same window | "One switch, two effects" kept, path dropped |
| `server/fleet/app.go:1491-1494` | `preserve_host_activities_on_reenrollment` defaults: true upgraded, false fresh | "The default differs by install history"; "per the source comment" removed |

## Doc/article/CHANGELOG references converted (precedent: 8.2, 8.3, 8.4, 8.6, 8.8, 8.14)

| Was | Now |
|---|---|
| `docs/REST API/rest-api.md:528/536/552-573/594-608/619/5850/5922/6009` | fleetdm.com/docs/rest-api/rest-api (in `further_reading`); Source column dropped from the endpoint table |
| `docs/Contributing/reference/audit-logs.md` (4 hits, incl. `:5`) | fleetdm.com/docs/contributing/audit-logs (already in `further_reading`) |
| `docs/Configuration/fleet-server-configuration.md:1418-1455, 1422, 1447, 1593-1605` | fleetdm.com/docs/configuration/fleet-server-configuration |
| `docs/Configuration/yaml-files.md:824-838` | fleetdm.com/docs/configuration/yaml-files (added to `further_reading`) |
| `articles/log-destinations.md` | fleetdm.com/guides/log-destinations (added to `further_reading`) |
| `CHANGELOG.md` | release notes at github.com/fleetdm/fleet/releases (added to `further_reading`) |

## `activities` audit: all 21 hits classified

Every hit was checked. **Nowhere does the section's own prose call the live table `activities`.**
Corrections needed: 0.

- Legitimate English word: intro ("Fleet calls the rows activities"), 8.12.6 ("shipped back into activities"), agent-version row, "120,000 activities per day".
- Endpoint paths that kept the name: `/api/v1/fleet/activities`, `/api/v1/fleet/hosts/:id/activities`, `.../activities/upcoming`, `.../automation_activities`, the `jq '.activities[]'` selector, and the `#list-activities` docs anchor.
- Other real identifiers: `upcoming_activities.execution_id` (the unified queue table, 8.6), `activities_streaming` cron, `cleanup_activities` job, index names `activities_created_at_idx` and `idx_activities_type_created`, setting `preserve_host_activities_on_reenrollment`.
- Historical, past tense and correct: "These tables were `activities` and `host_activities` until a migration renamed them."
- Quoted stale documentation: the REST API reference's own "any column in the `activities` table" wording, which the section labels stale (documentation bug 6). Kept as a quotation, since removing it would remove the bug report.

## Version claim

Line 222 read "There is no dedicated `fleetctl` subcommand for activities in 4.89.2."
4.89.2 was a bogus CHANGELOG stamp; the code read was post-4.90.0. Rewritten positively and
stamped 4.90.0, matching the frontmatter. No other version stamp in the section.

## Heading renames (no inbound anchors exist: `grep -rn "8.12-audit-logs.md#" manual/` is empty)

| Was | Now | Why |
|---|---|---|
| `8.12.6 The limit: no host-side event history` | `8.12.6 The limit: server-side action only` | §15; "limit" heading convention already exists (1.4, 8.14.4). Internal anchor in 8.12.1 updated to match. |
| `8.12.12 What this section does not cover` | `8.12.12 Questions that belong to another section` | §15; matches 8.3.10 "Questions that belong to another surface" |
| `### fleet_initiated is the row you will misread` | `### fleet_initiated separates people from automation` | §15, states the rule rather than the failure |
| `8.12.1 The one-line summary` | `8.12.1 The short answers` | It introduces a five-row table, so the old title described something the section does not do |

## Cuts and rewrites

- `TABLESPACE innodb_system` hint: cut. A schema-dump artifact with no operational use; the
  seven secondary indexes and the indexed-filter advice stay.
- The `grep` recipe over `server/fleet/activities.go`: cut per §8 (reader has no source tree).
  Replaced with a MySQL `DISTINCT activity_type` pointer, which is the same answer from a
  surface the reader has.
- `fleetctl debug errors` paragraph in 8.12.9: trimmed from "is not on this list on purpose"
  meta-commentary to the one fact that matters, with the cross-references intact.
- 8.12.6 opener: three stacked negatives ("no agent-side event feed, no local action log, no
  reconciliation pass") compressed to one sentence keeping the reconciliation point.
- "only"/"just" dropped where decorative. Kept where load-bearing: `host_only` (column name),
  "server-side action only", "Result logs only", "`per_page` max", "one node per tick".

## Keep-list verification

Present and preserved: `activity_past`, `activity_host_past`, `activity_audit_log_plugin`,
`activity_expiry_settings`, `activities_streaming`, all four endpoint families, activity type
names, column names, JSON entry shape, every destination plugin name.
Findings preserved: `host_only = 1` filtered from the global feed; enabling streaming backfills
the whole table; retention deletes in 5,000-row batches; no host-side event history (pointing at
8.4 and 8.2); audit is one of several streams with its own destination setting; `webhook` listed
in the log-destinations guide but absent from `activity_audit_log_plugin` (documentation bug 7).

## Frontmatter

`verified_on: 2026-08-20` -> `2026-08-21`. `verified_against`, `verified_source`,
`sidebar_position` untouched. `further_reading` gained the yaml-files reference, the
log-destinations guide, the REST API reference root, and the releases page.

## Open items / possible fact issues

- No inline HTML comments were present in the section; nothing to resolve.
- No new `[term]()` flags added: every term an administrator would stumble on here is glossed in
  place (GitOps mode, `fleet_initiated`, `host_only`, the streaming cursor). Terms on the
  already-flagged list (VPP, ADE, SCEP, DEP, node key, pprof, file carving) appear here only
  inside activity-type identifiers, where a flag would not read.
- Nothing believed factually wrong. One thing to watch on re-verification: the section says
  audit is "the fourth of Fleet's log streams", while 8.2 counts three plugin-configured
  streams (result, status, audit) and 8.3 counts four streams. Reworded to "one of Fleet's log
  streams" so the two counts stop colliding, with the cross-references to 8.3 and 8.2 kept.

## Additional §8 identifier cleanups found on the second pass (streaming mechanism table)

| Was | Now |
|---|---|
| "One row per `Write` call" | "One row per write to the destination" |
| "`json.Marshal` of the same `Activity` struct the API returns" | "The same JSON object the API returns, one object per row" |
| "`MarkActivitiesAsStreamed` sets `streamed = 1`" | "`streamed` flips to `1` on the rows the destination accepted" |
| "`streamed` is tagged `json:\"-\"`" | "The `streamed` bookkeeping column stays inside Fleet and never appears in the output" |

Facts unchanged in all four; only the Go-side naming went.

## Rewrites worth recording (second de-AI loop)

- 8.12.6 opener led with a bold sentence about what Fleet records, then repeated the point
  twice more. Now leads with the finding itself: "**The audit log has no host-side event
  history.**" One statement, then the mechanism.
- `host_only` paragraph: the old version ended on "So a type can exist in the table, be
  visible on the host's page, and be invisible on the global page", a reshuffle-proof
  three-clause list. Rewritten so the operational consequence carries the paragraph: an
  empty global result is not proof that nothing happened, so query the host endpoint or the
  join table.
- The `fleetctl` sentence was a bare negative with a bogus version stamp. Now positive and
  correctly stamped: "`fleetctl` reaches activities through `fleetctl get api`, as above.
  Through 4.90.0 it has no dedicated activities subcommand, so the API is the route."
- `mdm_unenrolled` note: "It does not name who did it" replaced by what the row does carry,
  the fact and the timing of Fleet observing the unenrollment.
- Global endpoint's `per_page` row reworded so the surprising default leads instead of
  trailing behind "not to a small page".
- Line wrapping normalised to the file's 88-column convention after each rewrite.

## Deliberately not done

- No `[term]()` flags added. `upcoming_activities` is the one concept a reader could stumble
  on (8.12.3 maps `uuid` to `upcoming_activities.execution_id` with no definition beyond the
  endpoint table's "still waiting to run"). A cross-reference to 8.6.4, which covers that
  table as the unified per-host queue, would close the gap, but adding it is new content
  rather than an edit pass. Left for whoever writes next.
- `released_from_ab` and the SCEP-proxy activity types appear only as identifiers inside a
  table of type names, where a `[term]()` flag would not read. Not flagged.
- No diagram placeholders added (Part VIII is the reference chapter). No table thinned.
