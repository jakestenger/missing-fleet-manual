# De-AI + style pass: 8.14 Diagnosing degradation

Started 2026-08-21. Section: `manual/08-troubleshooting/8.14-degradation.md`
Before: 675 lines.

Brief: strip 18 Go code citations plus the in-repo docs/CHANGELOG pointers, remove two
bogus "at 4.89.2" verification stamps, keep every reader-usable identifier, preserve the
listed findings, positive voice (§15), de-AI loop, `[term]()` flags (§14), no diagram
placeholders (Part VIII is the reference chapter).

## Pre-flight checks

- Em-dashes in the draft: none. Banned vocabulary: none. HTML comments: none.
- Inbound anchor links: one, `8.7-live-query-introspection.md:319` points at
  `8.14-degradation.md#8142-establish-a-control-first`. **That `##` heading is frozen.**
  Prose in other sections cites §8.14.1, §8.14.2 and §8.14.5 by number, so those numbered
  subsections keep their subject matter. `###` headings carry no inbound anchors, so they
  are free to rename.
- 25 files link to this section without a fragment. 8.7 names it as the owner of the
  `SELECT 1 WHERE 1 = 0;` control test and the layer-bypass table; 8.11 §8.14.2 for the
  same, §8.14.1 for content-vs-cardinality, §8.14.5 for watchdog denylist state. All
  landing points preserved.

## Plan (batches, saved after each)

1. Frontmatter, intro, §8.14.1, §8.14.2
2. §8.14.3 (the profiling section, where most Go citations live)
3. §8.14.4, §8.14.5
4. §8.14.6, §8.14.7
5. §8.14.8, §8.14.9, Version notes, See also
6. Recheck loop: only/just, em-dash, banned words, sentence rhythm, near-miss metaphor,
   reshuffle-proof paragraphs, self-referential filler

## Citation conversion table

Every pointer below was read at `fleet-public main @ 2026-08-05 (d2fe9be461)`, per the
frontmatter's `verified_source`. Filled in as each batch lands.

| Fact retained in prose | Pointer removed | How the fact now reads |
|---|---|---|
| (batch 1 onward, below) | | |

### Batch 1 (frontmatter, intro, §8.14.1, §8.14.2) — done

| Fact retained in prose | Pointer removed | How the fact now reads |
|---|---|---|
| The control test and the `(100% responded)` expectation | `docs/Contributing/guides/troubleshooting-live-queries.md` | "Fleet's own live-query troubleshooting guide opens with the same test." Guide stays in `further_reading` as a GitHub URL; contributor guides have no fleetdm.com/docs equivalent (same call 8.8 made) |
| `POST /api/v1/fleet/reports/:id/run` replaced `GET /queries/run` in 4.43.0, old endpoint still answers | `docs/REST API/rest-api.md` | inline `fleetdm.com/docs/rest-api/rest-api`, also added to `further_reading` |
| `/healthz` semantics and the `check` parameter | `docs/Deploy/Reference-Architectures.md` | inline `fleetdm.com/docs/deploy/reference-architectures` |
| `FLEET_LIVE_QUERY_REST_PERIOD` 25s result deadline | `server/service/live_queries.go:206` | "Source" column dropped from the two-row table; the defaults stay |
| The same variable as a floor for the HTTP write timeout, plus 10s, default 90s | `cmd/fleet/serve.go` | same table, no pointer |
| The docs/code mismatch on "~100 seconds" is known to Fleet and left alone to protect long-running uploads | source comment in `cmd/fleet/serve.go` | "Fleet treats the mismatch as known and has left it alone, so that a short deadline cannot shorten the write timeout and break long-running uploads." |
| `distributed_interval` recommended 10 to 30 seconds | `troubleshooting-live-queries.md` §5 | plain statement, no pointer |

Other batch 1 changes:
- `verified_on` 2026-08-20 to 2026-08-21. `verified_against` / `verified_source` untouched.
- **Cross-reference bug fixed:** the control-result table sent a query-side finding to
  "§8.14.6" (Interference). Query cost is §8.14.5. Changed to §8.14.5. Reported.
- Intro now names `fleetctl debug archive` as the right first move, per the brief.
- `[pprof]()` flagged at first use in the intro (recurring term, needs a glossary entry).
- §15: "It does not appear in the server configuration reference" to "absent from the server
  configuration reference"; "That is a configuration interaction, not a fault" to "Fix that by
  raising the period or lowering the interval"; `/healthz` "returns HTTP 200 only if" to
  "returns HTTP 200 when ... and", which keeps the necessary-condition sense without "only".

### Batch 2 (§8.14.3, server profiling) — done

| Fact retained in prose | Pointer removed | How the fact now reads |
|---|---|---|
| The eleven `fleetctl debug` subcommands, what each produces, `archive` as the right first move | **"Verified against `cmd/fleetctl/fleetctl/debug.go` at 4.89.2"** | Line deleted entirely. The 4.89.2 stamp is the known-bad CHANGELOG-derived stamp STYLE §9 warns about; the code read was post-4.90.0, and the frontmatter already carries 4.90.0. No surviving sentence needed a version. |
| Thirteen files in `archive`, in order | `debug.go`, `debugArchiveCommand` | "Thirteen files, in this order:" |
| Through `fleetctl`, `profile` is 30s and `trace` is 1s | (same file) | "Through `fleetctl` the durations are fixed", pointing at the raw-endpoint subsection |
| `db-innodb-status` and `db-locks` need global `PROCESS` and `SELECT`; the grant statement | `server/datastore/mysql/mysql.go:1259`, `server/datastore/mysql/locks.go` | grant SQL kept verbatim, "The error message names the grant:" |
| All three database profiles read the writer, never a replica | (same files) | "query the **writer** by design. Lock and process state on a read replica describes the replica, not the deployment." |
| `/debug/` requires a global admin; team admins get 403; undocumented | `server/service/debug_handler.go`, `debugAuthenticationMiddleware` | plain statement, "This requirement is undocumented." |
| Pinning a `--context` to one node makes profiles repeatable | `docs/Deploy/Reference-Architectures.md` | pointer dropped (the same URL is cited inline in §8.14.2 and §8.14.7) |
| `fleetctl` sends no query parameters, so `?seconds=` needs a direct call | `server/service/client_debug.go:35` | "`fleetctl` calls `/debug/pprof/<name>` with no query parameters, which is why the sample duration is fixed there." |
| `?seconds=` works because the standard Go handlers are mounted unmodified | `server/service/debug_handler.go` (`pprof.Profile`, `pprof.Trace`) | "inferred from Fleet mounting the standard profile and trace handlers unmodified" |
| Trace sampler override, one-minute propagation, high span volume at 100% | `docs/Deploy/Reference-Architectures.md` | pointer dropped, same reason as above |

Other batch 2 changes:
- `goroutine` glossed in place in the command table ("the server's individual in-flight
  tasks"), so no `[goroutine]()` flag.
- The "Failed profile" finding now leads with "normal rather than an error" and covers the
  run-from-outside-the-server case the brief calls out, then attributes the common
  `db-innodb-status` / `db-locks` pair to missing privileges.
- Headings renamed off negatives (no inbound anchors on any `###`):
  "Profiling one node, not the load balancer" to "Pin profiling to a named node";
  "Raw pprof, when 30 seconds is not enough" to "Raw pprof, for a longer sample";
  "Traces, when profiles are not enough" to "Traces, for request-level detail".
- §15: "not available as their own subcommand and are only ever produced by" to "come only
  from `archive`, with no subcommand of their own"; "Durations are not exposed as flags" to
  "the durations are fixed"; "not fatal" to "normal rather than an error"; "the Fleet binary
  is optional but gives you symbol names" to "Supplying the Fleet binary as well gets you
  symbol names".

### Batch 3 (§8.14.4 limits, §8.14.5 query cost) — done

| Fact retained in prose | Pointer removed | How the fact now reads |
|---|---|---|
| Login 10/min burst 9, forgot-password 10/hour burst 9, org-logo 60/min burst 20, all returning 429 | `server/service/handler.go:1201`, `:1236`, `:1189` | "Set where" is now "built in"; "Confirm with" is now the access log, which is the surface the reader actually has |
| Fleet Desktop: 1,000 consecutive failing requests per minute bans the source IP for a minute | `server/service/handler.go:280` | same treatment, "Access log, 429s clustered by source IP" |
| **Rate limiting covers those endpoints and no others** | `server/service/handler.go` **at 4.89.2** | Second bogus 4.89.2 stamp. Removed with its path; no version claim replaces it, since the statement is about the current release the frontmatter already names. Now: "Fleet rate-limits the endpoints above and no others. So a 429 on a plain read endpoint comes from something between you and Fleet: a load balancer, a WAF, or an API gateway." |
| 10,000 S3 carve parts, `carver_block_size` >= 5MiB, 8GB per carve | `articles/file-carving.md` | fleetdm.com/guides/file-carving, also in `further_reading` |
| The `osquery_schedule` column list | `schema/osquery_fleet_schema.json` | "Columns:" |
| The per-execution CPU form is what Fleet uses for host vitals | `docs/Contributing/product-groups/orchestration/understanding-host-vitals.md` | plain statement, no pointer |
| A denylisted query stays out of the schedule until osquery restarts | `schema/tables/osquery_schedule.yml` | plain statement |
| 4.74.0 downgraded `distributed query is denylisted` from error to warning | `CHANGELOG.md` | release number kept, pointer converted to github.com/fleetdm/fleet/releases |
| Watchdog default budget 200 MB and 10% CPU | `articles/how-fleet-helps-federal-agencies-meet-cisa-bod-23-01.md` | plain statement. No fleetdm.com slug guessed for that article. |
| Kill sequence, respawn limit, osquery shutting down entirely | `articles/osquery-watchdog.md` | fleetdm.com/guides/osquery-watchdog, also in `further_reading` |
| Watchdog flags are command-line flags and need a restart; the five settings that work either way | `osqueryCommandLineFlags` in `server/fleet/agent_options_generated.go:125-305` | "Every watchdog flag is a command-line flag, so it goes under `command_line_flags` ... and takes effect on the next fleetd restart." The struct name carried nothing for an administrator. |
| `subscriptions = 0` means events with no reader | `schema/tables/osquery_events.yml` | plain statement |
| Evented-table cost controls and the two drop paths | `articles/osquery-evented-tables-overview.md` | fleetdm.com/guides/osquery-evented-tables-overview (already in `further_reading`) |
| `buffered_log_max` and the buffer-through-downtime availability model | `docs/Deploy/Reference-Architectures.md` | plain statement |

Other batch 3 changes:
- Cut the self-referential "This is the highest-yield table in the section." Replaced with a
  concrete claim that ties back to §8.14.1: every row is a single lookup, so clear them
  before opening a scale investigation.
- pubsub expanded on first use: "Redis publish/subscribe (pubsub) output buffer". The
  `client-output-buffer-limit pubsub 32mb 8mb 60` default and the three ElastiCache
  parameter names are untouched. "Elasticache" corrected to "ElastiCache".
- `[file carving]()` flagged on the `carver_block_size` row. The section uses "carve",
  "carver_block_size" and "carve parts" with no definition anywhere in it.
- "Two limits, checked by osquery's watcher process" preceded a seven-row table, so it now
  reads "osquery's watcher process enforces a memory limit and a CPU limit against the
  worker process, and against each managed extension".
- §15: "is not run again until" to "stays out of the schedule until"; "take effect only on
  fleetd restart" to "takes effect on the next fleetd restart"; "when it cannot reach Fleet"
  to "while Fleet is unreachable"; "osquery logs when it drops them but cannot see drops by
  the utility" to "osquery logs its own drops; drops inside the utility are invisible to it".

### Batch 4 (§8.14.6 interference, §8.14.7 scale) — done

| Fact retained in prose | Pointer removed | How the fact now reads |
|---|---|---|
| Item 7 of Fleet's MDM bug checklist is the allow-list intake question; Santa and Jamf Pro are its examples | `docs/Contributing/product-groups/mdm/mdm-bug-checklist.md` | quoted question kept, "Fleet's own checklist names Santa and Jamf Pro there as examples" |
| The EDR-vs-osquery cluster; the fix version is unverified | `CHANGELOG.md` (internal note) | "not identifiable in Fleet's public release notes" |
| The eight sizing breakpoints, 5,000 to 300,000 hosts | `docs/Deploy/Reference-Architectures.md` | "Reproduced from fleetdm.com/docs/deploy/reference-architectures, for AWS with Fargate, Aurora MySQL 8 and ElastiCache Redis 7.x" |
| Prometheus metrics, and Fleet's suggested alerts | `docs/Deploy/Reference-Architectures.md` | plain statement |
| `redis_host_cache_ttl` docs/code disagreement, 60s vs 180s, raised in 4.89.0 | `server/config/config.go:1428` and `CHANGELOG.md` for 4.89.0 | "The configuration reference says `60s`. The server's own default is `180s`, and Fleet's 4.89.0 release notes record the raise from 60s to 180s. Treat 180s as the live value." |
| `distributed_query_campaign_targets` index plus 24-hour cleanup; campaign activity cleaned on a cron | `CHANGELOG.md` | plain statement |
| The performance-fix and performance-regression history, and the 4.73.x MySQL read regression | `CHANGELOG.md` (x2) | "Fleet's release notes"; the closing instruction now points at github.com/fleetdm/fleet/releases |

Other batch 4 changes:
- EDR expanded on first use: "Endpoint detection and response (EDR) tooling is the usual
  counterparty." No `[EDR]()` flag needed after the expansion. The internal note's later
  "an EDR product" now has an antecedent.
- "head-sampled" was jargon with a negative construction attached ("use metrics, not traces").
  Now: "Traces are sampled at the moment a request arrives, at the rates in §8.14.3, so read
  total request counts and error rates from metrics." Glosses the term and points at the
  sampling-tier table that was already in the section.
- Heading renamed: "Table growth that is not load" to "Row counts, before hardware". No
  inbound anchor.
- "DDM reconciler" expanded to "declarative device management reconciler", matching the
  in-place-expansion precedent from 8.8.
- "the answer sometimes makes the whole investigation unnecessary" to "sometimes settles the
  investigation on its own" (§15).
- "Elasticache" corrected to "ElastiCache" in the scale prose too.

### Batch 5 (§8.14.8, §8.14.9, version notes, see also) — done

| Fact retained in prose | Pointer removed | How the fact now reads |
|---|---|---|
| The four profile subcommands exist and are undocumented | `cmd/fleetctl/fleetctl/debug.go` | "All four work. No usage documentation anywhere in Fleet's docs: `archive` is documented, the individual profiles are not." |
| The global-admin requirement on `/debug/` is real and undocumented | `server/service/debug_handler.go` | "Confirmed behaviour, undocumented." |
| `FLEET_LIVE_QUERY_REST_PERIOD` defaults were read from the server, not from docs | (source-verified) | "come from the server rather than from documentation" |
| The four version-note entries (4.89.0, 4.84.3, 4.74.0, 4.43.0) | `CHANGELOG.md` | "Release notes for each of these are at github.com/fleetdm/fleet/releases." |

`net/http/pprof` is deliberately kept in §8.14.3 and §8.14.8. It names a Go standard-library
package, not Fleet source, and it is the reason `?seconds=` works on an endpoint `fleetctl`
does not expose. STYLE §8 bans showing the reader Fleet's own code; this is the reader's own
verification route.

### Polish / de-AI recheck pass — done

- "Two of these lie about each other" was a near-miss metaphor (a limit does not lie).
  Now: "Two of these imitate each other. A limit trips at volume, so it presents as a scale
  ceiling. A scale ceiling has a cliff, so it presents as a limit." Also removes an "only".
- Added subsection pointers to the four-causes table (`(§8.14.6)`, `(§8.14.7)`, `(§8.14.4)`,
  `(§8.14.5)`), so the entry table routes mid-incident. This is the table 8.11 and 8.1 send
  readers to.
- Filler intensifiers cut: "prove the path works at all", "how long the API actually waits",
  "a completely healthy server", "span volume is very high", "in the first place".
- "**What each outcome rules out:**" to "**What each outcome tells you:**" (§15).
- "Synchronous live report, which uses no websockets:" to "over plain HTTP:" (§15).
- "Sampling is route-aware and fixed in code, not controlled by `OTEL_TRACES_SAMPLER`" to
  "route-aware and built in, so `OTEL_TRACES_SAMPLER` has no effect on it". Drops the code
  reference and the negative in one move.
- "idle connections must be recycled to notice" was ambiguous about who notices. Now
  "Fleet notices the new address when idle connections are recycled."
- The `osquery_schedule` column list was reflowed after its citation was removed.

## Preserved deliberately

- Every table in the section. Part VIII is the reference chapter; no diagram placeholders
  added.
- `SELECT 1 WHERE 1 = 0;`, `(100% responded)`, the layer-bypass table, and the
  `## 8.14.2 Establish a control first` heading, which is the target of the only inbound
  anchor in the manual.
- `client-output-buffer-limit pubsub 32mb 8mb 60`, the three ElastiCache parameter names,
  `max_allowed_packet`, `carver_block_size`, every connection-pool setting and default,
  every rate-limit and quota value, every endpoint path, `distributed_interval` and
  `logger_tls_period` with the 10 to 30 second range, `osquery_schedule` and
  `osquery_events`, and all eleven `fleetctl debug` subcommands with their consumption
  commands.
- "What is not documented" as the §8.14.8 heading. It is a chapter-wide convention (8.11 uses
  the same heading) and renaming this one alone would break the pattern. Noted rather than
  changed.
- "Upgrading is a legitimate remediation" as a heading: already positive.
- Both `[!internal]` blocks, including the EDR cluster note, which the brief lists as a
  finding to preserve.

## `[term]()` flags added

- `[pprof]()`, intro, first use. Recurring term (pprof format, `go tool pprof`, the
  `/debug/pprof/` endpoints, the §8.14.8 row) and it needs a real glossary entry rather than
  a parenthetical.
- `[file carving]()`, §8.14.4, on the `carver_block_size` row. The section says "carve",
  "carve parts" and "carver_block_size" with no definition anywhere in it.

Glossed in place instead of flagged, following the OTLP / APNs / DDM precedent:
- **goroutine**: "Stack traces of every goroutine, meaning each concurrent task the server
  has in flight".
- **pubsub**: "Redis publish/subscribe (pubsub) output buffer".
- **EDR**: "Endpoint detection and response (EDR) tooling is the usual counterparty."
- **head sampling**: "Traces are sampled at the moment a request arrives, at the rates in
  §8.14.3."
- **DDM**: "the Apple profile and declarative device management reconciler".

## Possible errors found, reported not changed

1. **The control-result table pointed the wrong way.** "100% responded / partial or hangs"
   concluded "The **query**. Go to §8.14.6." §8.14.6 is Interference; query cost is §8.14.5.
   This is an internal cross-reference rather than a verified fact, so I corrected it to
   §8.14.5 and am reporting it.
2. **`--events_expiry` default is given as `86000` seconds.** osquery's documented default
   is 86,400 (one day). 86000 may be a transcription slip in the draft. Not changed, since
   the brief forbids re-verification. Worth one lookup.
3. **`mysql_max_open_conns` default is given as `50`** in §8.14.4, while the reference
   architecture table in §8.14.7 recommends 10 to 20 per task. Both can be true (default vs
   recommendation) and the draft treats them as such, but a reader may read it as a
   contradiction. Left as written.

## Line count

675 before, 670 after.
