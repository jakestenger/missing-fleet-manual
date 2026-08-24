# de-AI and style pass: 8.11 Reproducing and isolating

Pass date: 2026-08-21. Before: 327 lines. After: 328 lines.
Scope: presentation only. No facts re-verified, no facts changed.

## Citation inventory (all removed from reader-facing prose)

### Class A: path-based citations (18)

| Where | Citation removed | Fact it supported | How the fact now reads |
|---|---|---|---|
| Timing table, osquery check-in | `docs/Configuration/agent-configuration.md:16,274`; `docs/Contributing/guides/troubleshooting-live-queries.md` §5 | 10 to 30 second recommendation; examples of `3` global and `10` darwin override | Value kept verbatim, Source column dropped; both URLs in `further_reading` |
| Timing table, logger period | `docs/Configuration/agent-configuration.md:19,277` | examples `10` global, `300` darwin | Value kept, Source column dropped |
| Timing table, Orbit config receiver | `docs/Contributing/architecture/mdm/setup-experience-overview.md:9,29,113` | 30 second poll, all platforms | Value kept; URL added to `further_reading` |
| Timing table, install script | `docs/Contributing/architecture/software/software-installation.md:106` | 1 hour timeout | Value kept; URL already in `further_reading` |
| Timing table, post-install script | `Same, :112` | 1 hour timeout | Value kept |
| Timing table, uninstall script | `Same, :115` | 1 hour timeout | Value kept |
| Timing table, script result upload | `Same, :109` | 5 retries with backoff | Value kept |
| Timing table, VPP verify timeout | `server/config/config.go:1463`; `software-installation.md:58` | 10 minutes, `server.vpp_verify_timeout`, `FLEET_SERVER_VPP_VERIFY_TIMEOUT` | Value and both config surfaces kept |
| Timing table, VPP poll gap | `server/config/config.go:1464` | 5 seconds, `server.vpp_verify_request_delay` | Value kept |
| Timing table, Windows relaxed poll | `server/service/microsoft_mdm.go:2113-2116` | 480 minutes | Value kept; mechanism now cross-refs 8.9 instead of naming the CSP wire detail |
| Timing table, Windows fast poll | `server/service/microsoft_mdm.go:2110-2112` | 1 minute | Value kept |
| Timing table, DEP sync | `server/config/config.go:1854` | 1 minute, `mdm.apple_dep_sync_periodicity` | Value kept |
| Timing table, first cron run | `server/service/schedule/schedule.go`, `Start()` | 10 seconds, or the interval if shorter | Value kept, stated as behaviour |
| Timing table, cron config reload | `server/service/schedule/schedule.go`, `New()` | 1 hour reload | Value kept, stated as behaviour |
| Windows paragraph | `docs/Contributing/architecture/mdm/windows-mdm-architecture.md`, "Command delivery and poll schedule" | design intent: non-poll commands ride an on-demand session via fleetd check-in | Stated as Fleet's design intent; URL added to `further_reading` |
| Effective interval | `docs/REST API/rest-api.md` | the three interval columns are on the host object from `GET /api/v1/fleet/hosts/:id` | Inline `fleetdm.com/docs/rest-api/rest-api`; URL added to `further_reading` |
| Effective interval | `docs/queries.yml:790` | the `osquery_flags` query is Fleet's own | "This is Fleet's own query for it"; queries.yml URL added to `further_reading` |
| Throwaway instance | `articles/deploy-fleet-on-docker-compose.md` | the Compose route and its 15 minute / port cost | Now "Fleet's own guide", with the existing `fleetdm.com/guides/deploy-fleet-on-docker-compose` slug inline |

### Class B: bare filenames, Go identifiers, non-path refs (11)

| Where | Citation removed | Fact it supported | How the fact now reads |
|---|---|---|---|
| Trigger trap, intro | `Schedule.Trigger()` | a trigger can return without triggering | "A trigger returns without triggering in three cases" |
| Trigger trap, intro | `server/service/schedule/schedule.go`, `Trigger()` | same | citation dropped |
| Trigger trap, row 3 | `nil` stats, `didTrigger: false`, no error | the silent no-op has no error signal | "No stats, no error, and no run" |
| Trigger trap, prose | `CronSchedules.TriggerCronSchedule` | the API layer never checks whether the run started | "Nothing on the path from the API to the CLI checks whether the run started" |
| Trigger trap, prose | `didTrigger` (discarded return value) | same | folded into the sentence above |
| Trigger trap, prose | `server/fleet/cron_schedules.go:114-129` | same | citation dropped |
| Multi-node bullet | `RemoteTriggerSchedule` (identifier) | a queued row is inserted for the node that owns the schedule | "Fleet records a remote trigger, a `queued` row…" |
| Multi-node bullet | `schedule.go` (bare filename) | same | citation dropped |
| Double-run bullet | `schedule.go`, `RemoteTriggerSchedule.Trigger` | read-then-insert is not atomic, double-run accepted | "Fleet accepts that, because the worst case is the schedule running twice" |
| Differential table | `CHANGELOG.md` | compare versions for a regression | "Read the release notes between the two (github.com/fleetdm/fleet/releases)" |
| Not-documented table | `Trigger()`, `server/service/schedule/schedule.go`, `server/fleet/cron_schedules.go`, `server/config/config.go` | verification provenance for three rows | Replaced with "verified behaviour" / "verified in the server" wording |

Total removed: 18 path-based + 11 bare = 29 distinct citations (brief estimated 28; the extra
is the second bare `schedule.go` in the double-run bullet).

Kept deliberately, not citations:
- `trigger channel not available` — a server log string the reader greps for.
- `raw.githubusercontent.com/.../docs/solutions/docker-compose/...` URLs — commands the reader runs.
- Config keys and env vars (`logging_error_retention_period`, `server.vpp_verify_timeout`,
  `FLEET_SERVER_VPP_VERIFY_TIMEOUT`, `mdm.apple_dep_sync_periodicity`, `command_line_flags`).
- Schema/column names (`cron_stats`, `stats_type`, `created_at`), API paths, `osquery_flags`.

## The 4.89.2 reference

Line 102 read: "Schedule names, from `server/fleet/cron_schedules.go` at 4.89.2."
Path removed; version stamp corrected to 4.90.0 per the brief (4.89.2 came from a CHANGELOG
that lagged the working tree; the code read was post-4.90.0). Now: "Schedule names as of
4.90.0." The full name list is unchanged.

## Headings

| Before | After | Reason |
|---|---|---|
| `### Read the effective interval, not the configured one` | `### Read the interval the host is using` | §15, drops the "not the X" construction |
| `### A trigger that looks like it worked may have done nothing` | `### A trigger can report success for a run that never happened` | §15, states what happens |
| `## 8.11.8 When you cannot reproduce it` | `## 8.11.8 Preparing for the next occurrence` | §15 |
| `### Aggregate metrics cannot answer the two-clocks question` | `### The two-clocks question needs per-record timestamps` | §15 |
| `## 8.11.10 What is not documented` | unchanged | Chapter convention, matches 8.14.8. Kept per brief. |

Inbound links checked: `grep -rn "8.11-reproducing-and-isolating.md#"` returns nothing, and no
other section references an `8.11.x` subsection number. All 13 inbound links are plain
file links and are unaffected.

## Findings preserved verbatim in substance

- Trigger reporting success for a run that never happened, all three cases, with the third
  as a silent no-op logged at debug only. The pairing with `cron_stats` is stated as
  mandatory ("pair every trigger with").
- No invented osquery defaults. Example values, the 10 to 30 second recommendation, and
  "read the effective value from the host" all kept.
- The support case where aggregate-only latency monitoring made the two-clocks check
  impossible, kept in the `[!internal]` block.
- Redis retention aging out recorded errors across a long reproduction window.

## Keep-list audit

Everything on the brief's keep-list was present and is still present. One wording note: the
brief lists "the 5 retries with backoff" and "the 10 minute VPP verification default and its
environment variable" — both present. The `SELECT 1 WHERE 1 = 0;` control test and the
"(100% responded)" expectation are **not** in this section: §8.11.2 delegates the live-query
control to 8.14 §8.14.2, where that query and that expectation live. Nothing added here.

## Terms (§14)

No new `[term]()` flags. Two terms glossed in place instead:
- `ADE/DEP` in §8.11.6 became "automated device enrollment (ADE, formerly DEP)".
- `ABM token` in §8.11.9 became "an Apple Business Manager (ABM) token".
`APNs`, `VPP`, `GitOps`, `Android Enterprise`, and the watchdog denylist were left alone:
each is either ubiquitous in Fleet's own UI and docs or cross-referenced to the section
that owns it.

## Facts I believe may be wrong (reported, not changed)

None found. One presentational inconsistency noted below.

## Prose changes beyond citation removal

- Opening paragraph: the two "because" clauses were restructured so the two instructions
  do not share one sentence shape.
- Timing table, "Where it is set" column: "Not configurable" became "Fixed", matching the
  wording already used in §8.11.10.
- Windows paragraph: dropped the trailing "not whether the queue is moving", per §15.
- "Then scope the profile, script, or installer to `repro-host` only." lost its "only".
  The five remaining instances of "only" all carry meaning: "read-only command",
  "debug level only", "the only proof", "one platform only", "exposed only an aggregated
  latency figure". All kept.
- Two-clocks paragraph: "the comparison is not available at any sample rate" became "no
  sample rate recovers the comparison".
- "What it does not get you." kept as a bold label in §8.11.9. It enumerates real limits
  of a throwaway instance rather than pre-empting a misunderstanding, and it is the middle
  term of a costs / limits / proof triple.
- One over-long wrapped line in §8.11.9 rewrapped to the 88-column body width.

## Other notes

- The timing table's `Source` column was dropped whole rather than cell by cell, since every
  cell in it was a citation. Precedent: 8.9's tables carry no source column.
- No diagram placeholders added (Part VIII is the reference chapter).
- No inline HTML comments were present in the section.
- Zero em-dashes before and after.
