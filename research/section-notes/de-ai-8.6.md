# De-AI pass: 8.6-server-state.md

Started 2026-08-20. Section: `manual/08-troubleshooting/8.6-server-state.md`.
Before: 1111 lines, 172 table rows, 21 Go file references, 1 line number.

## Anchors linked from elsewhere (must not break)
- `#862-cron_stats-did-the-job-run` — linked from 1.3 (x2), i.e. heading "8.6.2 `cron_stats`: did the job run?"
- `#8613-scoping-which-fleet-which-labels-was-this-host-targeted` — linked from 1.3 (x2) and 8.1.

## Citation removals
(table filled in as work proceeds)

## Notes / open items

## Citation removals (path -> fact it supported)

| Was cited | Fact it supports, as now stated in the section |
|---|---|
| `server/datastore/mysql/schema.sql` (L32) | Column names and types in every table below. Sentence deleted; frontmatter carries the verification stamp |
| `cmd/fleet/serve.go` (L140) | `instance` is a random per-process identifier, logged at startup as `instance info` with an `instanceID` field |
| `cmd/fleet/cron.go` + `cleanupCronStatsOnShutdown` (L177) | On graceful shutdown Fleet flips that instance's `pending` rows to `canceled` |
| `server/datastore/mysql/cron_stats.go` + `CleanupCronStats` (L178) | `expired` is reaped after 2 h pending/queued with no live lock, or 12 h regardless |
| `server/service/schedule/schedule.go` + `Trigger()` (L182) | The three cases where a trigger returns without triggering, and which of them logs |
| `cmd/fleet/cron_registration.go` + `registerCleanupAndMaintenanceCrons` (L210) | `cron_stats` cleanup runs hourly, outside the schedule system |
| `server/fleet/datastore.go` + `GetLatestCronStats` (L215) | Fleet reads at most two rows per schedule and ignores `expired` / `canceled` |
| `server/fleet/cron_schedules.go`, `cmd/fleet/cron.go`, `server/cron/` (L227-228) | Schedule names and default intervals in the §8.6.3 table |
| `cmd/fleet/cron.go` + `CronScheduleName` (L261) | `mdm_service_discovery` is registered outside Fleet's canonical schedule-name list, and is undocumented |
| `server/datastore/mysql/activities.go` + `activateNextUpcomingActivity` (L318) | Activation order, one activity at a time per host, VPP batch of 5 |
| `server/mdm/nanomdm/mdm/type.go` (L410) | The five `nano_enrollments.type` values |
| `server/mdm/nanomdm/storage/mysql/queue.go` (L417) | `NotNow` keeps the queue row active, bumps `not_now_tally`, and `not_now_at` records the first only |
| `server/fleet/mdm.go` (L599) | Profile `status` vocabulary: pending, verifying, verified, failed, NULL |
| `server/datastore/mysql/apple_mdm.go` + `insertMDMConfigAssets` (L802) | `mdm_config_assets.value` is encrypted with `server_private_key` |
| `server/fleet/mdm.go` (L806) | The list of known `mdm_config_assets` names |
| `server/mdm/apple/apple_mdm.go` + `DEPSyncLimit` (L842, L844) | 200 devices per DEP request, looping until Apple reports no more pages |
| `server/live_query/redis_live_query.go` (L902) | Live query campaign keys in Redis |
| `server/pubsub/redis_query_results.go` (L906) | `results_<campaignID>` is a pub/sub channel |
| `server/errorstore/errors.go` (L907) | Recorded server errors live under `error:{<hash>}:json` |
| `server/service/redis_policy_set/` (L909) | Failing-policy sets in Redis |
| `server/service/trigger.go` + `ActionWrite` on `fleet.CronSchedules` (L1020) | The trigger endpoint requires write permission on Fleet's schedules |
| `server/service/osquery.go:869` (L1095) | `refetch_requested` bypasses the interval gate and lands on the next distributed read |

The whole "Set by" column of the Redis key table (L900-909) was Go paths and was dropped; key
pattern and contents survive.

## Facts I believe are wrong or inconsistent (reported, NOT changed)
- Body said column names were read "at Fleet 4.89.2" (L33) and "Thirty-seven schedules are
  registered at 4.89.2" (L222), while frontmatter says `verified_against: Fleet 4.90.0` and the
  task brief says facts were verified at tag `fleet-v4.90.1`. STYLE §9 documents 4.89.2 as the
  known-bad CHANGELOG-derived stamp on Part VIII. I removed the two in-text version stamps
  (frontmatter is the single place for them) and left every number and name untouched.
- L1030 said "Columns read at `fleet-v4.90.1`", which contradicts the frontmatter's 4.90.0 /
  main @ d2fe9be461. Sentence removed as redundant with frontmatter; no fact altered.
- L167 pointed at §8.6.2.5 (Retention) for the `trigger-api` sentinel. That material is at the
  end of §8.6.3 (the `vulnerabilities` proxy). Reference corrected to §8.6.3.

## Cut for cause
- "It appears zero times in Fleet's documentation and zero times across 5,112 entries of
  Fleet's own support history" — the 5,112 figure is internal research, not reader-usable, and
  §15 forbids the zero-times framing. Replaced with "There is no read API and no entry in
  Fleet's documentation."
- "Worth filing." (§8.6.12) — instruction to nobody; the frontmatter `feature_requests` block
  already carries it.

## Progress log
- Batch 1 (intro, 8.6.1, 8.6.2, 8.6.3): citations stripped, canceled-vs-expired paragraph added,
  trigger-case list restructured, `[DEP]()` and `[ADE]()` flagged, "from the team" -> "from the
  fleet" for terminology consistency with 8.6.13.
- Batch 2 (8.6.4 to 8.6.9): citations stripped, `[VPP]()` and `[SCEP]()` flagged, the
  `windows_mdm_responses` paragraph rewrapped (the run-on line) with the envelope/results
  distinction and its "only" intact.
- Batch 3 (8.6.10 to 8.6.13): Redis key table lost its "Set by" column (all Go paths);
  §8.6.12 heading renamed off "A known gap" (nothing links to that anchor); refetch and
  scoping citations replaced with behaviour.
- All 24 path-shaped citations and the single line number are gone; grep for
  `server/`, `cmd/`, `*.go`, `*.sql` in the section returns nothing.

## Round-5 voice phase (V2c §28 sweep) — 2026-09-03
- STYLE §28 sweep of Part VIII (already fully de-AI'd 2026-08-21; this pass only re-checks
  the two §28 shapes). One genuine hit in 8.6.1: the "read-only" safety paragraph was the
  announce-then-correct rhythm stacked on a qualification stack (bold "Every query is
  read-only" -> "Nothing here mutates... except" -> "Read-only is not the same as free,
  though: ...several clauses..."). Rewrote to lead with the load-bearing caution
  ("Read-only is not the same as free."), state the SELECT/one-mutation fact plainly, then
  rank the scale-cost detail and the actions. No fact/identifier/anchor change; links=0.
- Rest of Part VIII confirmed §28-clean: bold lead-ins are §26 list/branch labels (grep for
  the bold-then-walk-back signature returned 0), and the long sentences (8.6:638 two-tier
  cert renewal, the colon-introduced lists in 8.5/8.12) are ranked enumerations with worked
  examples, not qualifier-on-qualifier stacks. No manufactured edits.
