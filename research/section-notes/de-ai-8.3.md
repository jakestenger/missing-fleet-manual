# 8.3 Fleet server logs: style-rules and de-AI pass

Target: `manual/08-troubleshooting/8.3-server-logs.md`
Pass run 2026-08-20. **Facts unchanged; presentation only.** Frontmatter `verified_against`
(Fleet 4.90.0) and `verified_source` left as written; `verified_on` set to 2026-08-20.

Going in, the section carried the heaviest citation load in the book: 51 source pointers
(49 Go files plus 2 in-repo docs), 48 of them with line numbers, in 435 lines. Every one is
tabulated below against the fact it supports, so a future editor can re-verify without the
published prose carrying developer detail (STYLE §8).

## Code-citation trail removed from the section

Pointers are as the draft recorded them. The draft's `verified_source` is
`fleet-public main @ 2026-08-05 (d2fe9be461)`, except the four rows the draft marked "Read at
`fleet-v4.90.1`", which are noted as such below.

| Fact retained in prose | Pointer removed |
|---|---|
| The server's own log goes to stderr, plus the OTLP collector when OTLP export is on. No plugin setting, no `logging_plugin` | `server/platform/logging/logging.go:46-48` |
| The nine `logging_*` keys, their env vars, flags, defaults and effects | `docs/Configuration/fleet-server-configuration.md` → now cited as fleetdm.com/docs/configuration/fleet-server-configuration |
| Same table, plus: `logging_tracing_type` is accepted as a configuration key with no entry in the reference | `server/config/config.go:384-398, 1566-1583` |
| Exactly two levels: info normally, debug when `logging_debug` is on. No warn-only or error-only threshold | `server/platform/logging/logging.go:51-54` |
| `logging_otel_logs_enabled` without `logging_tracing_enabled` is fatal at startup, with the quoted message | `server/config/config.go:402-405` (message also cited at `:404` in the error-string table) |
| `logging_disable_banner` is read from configuration and has no consumer elsewhere in the server as of 4.89.2; effect unverified | `server/config/` (no line numbers in the draft) |
| The level is fixed at process start: no SIGHUP handler, no level-setting endpoint | absence in `cmd/fleet/` and `server/platform/logging/`; draft's mechanism detail was `slog.HandlerOptions.Level` set to a plain `slog.Level` rather than a `slog.LevelVar` |
| Field rewriting shared by text and JSON output: `ts` in UTC RFC3339 renamed from `time`, lowercased `level`, `msg` omitted when empty, `trace_id`/`span_id` when tracing is on | `server/platform/logging/logging.go:87-113` |
| Per-request line attributes: `user`, `method`, `uri`, `took`, `err`, `internal`, `uuid`, per-endpoint extras | `server/contexts/logging/logging.go:142-225` |
| Per-request records log at `error` on a server fault and at `debug` for everything else, including every 4xx | `server/contexts/logging/logging.go:146-153, 227-244` |
| `authentication error: invalid node key` is a client error, so no line at default verbosity | `server/service/transport_error.go:92-104` |
| The `uuid` in a JSON error response body matches the `uuid` attribute on that request's log line | `server/platform/endpointer/transport_error.go:25-30, 87-92` |
| The uuid is read from the unwrapped cause without walking the chain, so an error whose top-of-chain type carries no uuid produces no uuid in either place | `server/platform/endpointer/transport_error.go:86-92` (draft named the direct type assertion, `errors.As`, and `ErrorWithUUID`) |
| Recorded-error mechanism: Redis keys `error:{<hash>}:json` / `:count`, TTL from `logging_error_retention_period`, SHA-256 dedup key, async write with a 2s give-up, `GET /debug/errors`, cluster-wide scope | `server/errorstore/errors.go:100-290`, `cmd/fleet/serve.go:456`, `server/service/client_debug.go:50-56` |
| Errors are recorded when they are server faults; client errors increment a metric, return to the caller, and never reach the store. Not documented | `server/contexts/ctxerr/ctxerr.go:314-386` (draft named `ctxerr.Handle`) |
| Entry shape `{"count": N, "chain": [...]}`, each element with `message`, optional `data`, optional `stack` | `server/contexts/ctxerr/ctxerr.go:259-264` |
| The chain is reversed before storage into chronological order: element zero is the root cause | `server/contexts/ctxerr/ctxerr.go:232-257` |
| Dedup key covers the root cause's type, its message, and the stack captured where the error originated; the root error carries a full stack, wrappers one frame each | same, plus `FleetError` as the draft's type name |
| `data` always carries `timestamp` in RFC3339 plus registered diagnostic context | `server/contexts/ctxerr/metadata.go`, `ctxerr.go:113-128` |
| HTTP 408 errors have socket addresses normalised to `<addr>` before hashing, so request-timeout entries aggregate | `server/errorstore/errors.go:31-36, 165-176` |
| `--flush` issues a Redis `DEL` on the keys it read. No undo, no copy elsewhere | `server/errorstore/errors.go:151-155` |
| Without `--stdout`, output goes to `fleet-errors-<ts>.json` in the working directory with a sensitive-data warning | `cmd/fleetctl/fleetctl/debug.go:589-660` |
| `DEP auth error: 403 Forbidden: T_C_NOT_SIGNED` | format at `server/mdm/nanodep/client/auth.go:31`, matched at `server/mdm/nanodep/godep/account.go:54-55` |
| `DEP auth error: 403 Forbidden: signature_invalid`, also matched on 401 | same format, matched at `server/mdm/nanodep/godep/account.go:81-83` |
| `authentication error: missing node key` | `server/service/osquery.go:53` |
| `authentication error: invalid node key` | `server/service/osquery.go:61` |
| `authentication error: missing orbit node key` | `server/service/orbit.go:73` |
| `authentication error: invalid orbit node key` | `server/service/orbit.go:81` |
| `authentication error: invalid authorization header` | `server/service/osquery_header_auth.go:82, 91, 155, 163` |
| `authentication error: missing HTTP signature` | `server/service/orbit.go:208` |
| `authentication error: certificate serial number mismatch` | `server/service/orbit.go:211` |
| `authentication error: certificate matching HTTP message signature not found` | `server/service/orbit.go:214` |
| `health check failed` at warn, with `component=healthz`, `health-checker=<name>`, `err=<cause>` | `server/health/health.go:56` |
| `total runtime (<d>) exceeded schedule interval (<d>)` at info | `server/service/schedule/schedule.go:392` |
| `pending job might still be running, wait <d>` at info | `server/service/schedule/schedule.go:337` |
| `lock failed` at error | `server/service/schedule/schedule.go:660` |
| `Request exceeds the max size limit of <size>`, tied to `server_default_max_request_body_size` | `server/platform/http/errors.go` (`PayloadTooLargeError`; internal type name dropped) |
| `logging.otel_logs_enabled requires logging.tracing_enabled to be true` | `server/config/config.go:404` |
| `orbit host with duplicate identifier has enrolled…` at warn, with `identifier=` and `host_id=`; osquery-channel twin names `osquery.db` | `server/datastore/mysql/hosts.go:2416-2422`, twin at `:2679-2685`. Read at `fleet-v4.90.1` |
| `orbit host identity cert host id does not match enrolled host id…`, where Fleet refuses the enroll | `server/datastore/mysql/hosts.go:2424-2429`. Read at `fleet-v4.90.1` |
| `host identified by <osquery host id> enrolling too often`, gated by `osquery.enroll_cooldown` | `server/datastore/mysql/hosts.go:2668-2670`. Read at `fleet-v4.90.1` |
| `expected 4 builtin labels but got N` | `server/datastore/mysql/apple_mdm.go:2096-2099`. Read at `fleet-v4.90.1` |
| `deprecated_path=` / `deprecation_warning=` at warn, on the `deprecated-field-names` topic | `server/platform/endpointer/endpoint_utils.go:858-872` |
| `Your Fleet database is not initialized. Fleet cannot start up.` | `cmd/fleet/serve.go:1167-1175` |
| `Your Fleet database is missing required migrations.` | `cmd/fleet/serve.go:1177-1190` |
| `Your Fleet database has unrecognized migrations.` | `cmd/fleet/prepare.go:127-136` |
| The three banners are written straight to stdout with `fmt.Printf`, bypassing the logger | same three, plus the `fmt.Printf` call named in prose |
| systemd unit and `journalctl -u fleet.service -f`, with `--logging_json` in the sample unit | `docs/Deploy/Reference-Architectures.md:60-90` → now cited as fleetdm.com/docs/deploy/reference-architectures |
| `instance info` line logged once at startup with `instanceID=<base64>` | `cmd/fleet/serve.go:627-631` |
| The instance identifier is 64 random bytes, base64-encoded, generated in memory at every process start | `server/utils.go:55-62` |
| Cron schedule log lines carry the same `instanceID`, alongside `schedule=<name>` | `server/service/schedule/schedule.go:105, 203` |
| With `logging_otel_logs_enabled`, every record is emitted twice | `server/platform/logging/logging.go:74-78` |

Reader-usable identifiers deliberately **kept**: all nine `logging_*` keys with their
`FLEET_LOGGING_*` env vars and `--logging_*` flags; `logging_error_retention_period` with its
`24h` default, `0` meaning no expiry and a negative value disabling recording;
`server_default_max_request_body_size`; `osquery.enroll_cooldown`;
`FLEET_UPGRADES_ALLOW_MISSING_MIGRATIONS` and `updates.allow_missing_migrations`; the log
field names `ts`, `level`, `msg`, `trace_id`, `span_id`, `user`, `method`, `uri`, `took`,
`err`, `internal`, `uuid`, `instanceID`, `component`, `health-checker`, `schedule`,
`identifier`, `host_id`, `deprecated_path`, `deprecation_warning`; every error string in
8.3.6 including both DEP strings; `/healthz`, `GET /debug/errors`; the Redis key shapes
`error:{<hash>}:json` and `:count`; `fleet prepare db`; `fleetctl debug errors` with
`--flush` and `--stdout` and the generated filename shape; the `cron_stats` table and its
`instance` column; `journalctl`, `docker logs`, `kubectl logs` invocations.

## Internal identifiers dropped from prose (STYLE §8), and what replaced them

| Dropped | Now reads |
|---|---|
| `os.Stderr` | "stderr" |
| `slog.NewJSONHandler` / `slog.NewTextHandler` | "JSON records instead of `key=value` text" |
| slog level `Debug` / `Info` | "debug level instead of info" |
| `slog.HandlerOptions.Level`, `slog.LevelVar` | "Fleet reads the level once, when the process starts" (SIGHUP kept: an operator would try it) |
| go-kit (library name) | "Fleet's older log format" |
| `SkipUser` | "endpoints that skip caller logging" |
| `ctxerr.Handle` | "Fleet's error handler" |
| `FleetError`, "Go type" | "the root error", "the root cause's type" |
| `ErrorWithUUID`, `errors.As`, "direct type assertion on the unwrapped cause" | "Fleet reads the uuid from the unwrapped cause without walking the chain, so an error whose top-of-chain type carries no uuid produces no uuid in either place" |
| `fmt.Printf` | "written straight to stdout, bypassing the logger" |
| `PayloadTooLargeError` | (dropped; the config key carries the meaning) |
| "confirmed in source" / "confirmed by absence in `cmd/fleet/`…" | "This behaviour is not documented." / "not documented; established by its absence" |

## In-repo doc citations converted to public URLs (precedent from 1.3 and 1.4)

| Was | Now reads |
|---|---|
| `docs/Configuration/fleet-server-configuration.md` | fleetdm.com/docs/configuration/fleet-server-configuration (already in `further_reading`) |
| `docs/Deploy/Reference-Architectures.md:60-90` | "Fleet's reference architectures (fleetdm.com/docs/deploy/reference-architectures)" (already in `further_reading`) |

No `CHANGELOG.md` citations were present. The four rows the draft stamped "Read at
`fleet-v4.90.1`" now read "Confirmed at 4.90.1": reader-facing prose should name a release,
not a git tag (same change 1.4 made).

## Findings preserved verbatim in substance

Checked one by one after the rewrite:

- `fleetctl debug errors` records server faults only; client 4xx never reaches the store, so
  an empty output says nothing about hosts being rejected. Kept as its own heading, "Server
  faults only", and the "empty output is meaningful in a specific way" paragraph is untouched.
- Per-request lines log at debug unless the error is a server fault, so an invalid node key
  produces no line at default verbosity. Kept, with the emphasis intact.
- API error responses and the log line share a `uuid`; behind a load balancer that is the
  reliable way to tie a customer-visible error to the node that produced it. Kept, with the
  top-of-chain caveat and its "not documented" hedge.
- `internal` carries the cause deliberately withheld from the client. Kept.
- The startup instance identifier is the same value recorded against each scheduled job run,
  and is regenerated on every process start. Kept ("Those are the same value. That is the
  join.").
- The three migration banners bypass the logger, so a structured-stderr collector misses
  them. Kept.
- Recorded errors live in Redis and are ephemeral; capture before flushing. Kept, including
  the `DEL`, "no undo", and the generated filename.

## Positive-voice and heading changes (STYLE §15)

| Before | After | Why |
|---|---|---|
| "…what a line contains, and the large set of things it does not contain" | "…and which questions belong to another surface" | Intro framed on absence. |
| Heading "8.3.1 Four streams, and only one of them is this section" | "8.3.1 Four streams, and which one this is" | Dropped "only". |
| "**only the first stream has no plugin setting**" | "**the first stream has no plugin setting**" | Dropped "only". |
| "writes to `os.Stderr` and nothing else, unless you also turn on OTLP export" | "writes to stderr, and additionally to an OpenTelemetry collector over OTLP when you turn that export on" | Positive form, and it expands OTLP in place (8.2 spells out OpenTelemetry; 8.3 never did), so no `[OTLP]()` flag was needed. |
| "Three things the table does not say." | "Three behaviours the table leaves out." | Off the negative. |
| "no way to raise the floor above `Info`" | "no setting raises the floor above info" | Positive construction. |
| "Added only when `logging_tracing_enabled` and a span is active" | "Present when `logging_tracing_enabled` is on and a span is active" | Dropped "only"; says what happens. |
| Heading "8.3.4 The per-request line, and why you usually cannot see it" | "8.3.4 The per-request line, and the level it needs" | Off the negative, and names the thing the reader must change. In-file anchor updated in 8.3.9. No other file links this anchor (checked: only `#836-error-strings-worth-recognising` has inbound links, from 1.3, and that heading is unchanged). |
| "logged at `error` only when the request produced an error that is not a client error" | "logged at `error` when the request produced a server fault" | Double negative into the positive form; the debug case follows unchanged. |
| "Consequences worth internalising:" | "Consequences:" | Throat-clearing (STYLE §12). |
| "Silence is not evidence of a problem, and it is not evidence of health either." | "Read silence as no information, in either direction." | Two negatives, and the parallel construction read as a manufactured epigram. |
| "This is the only reliable way to find the one node…" | "Behind a load balancer that is the reliable way to tie a customer-visible error to the node that produced it." | Dropped "only"; names what the correlation buys. |
| "and it is only present at the verbosity where that line survives" | "at the verbosity where that line survives" | Dropped "only". |
| Heading "Only server errors get recorded" | "Server faults only" | Keeps the load-bearing "only" and matches the term used in 8.3.4. |
| "stores an error in Redis only when the error is **not** a client error" | "stores an error in Redis when the error is a **server fault**" | Positive. |
| "Client errors still increment a metric and still return to the caller, but they never reach the store." | "Client errors increment a metric and return to the caller without reaching the store." | Dropped two "still"s and the "but" pivot. |
| "Only the root `FleetError` carries a full stack. Wrappers carry one frame each." | "The root error carries a full stack trace, and each wrapper carries one frame." | Dropped "only" and the internal type name. |
| "Only strings located in source are listed. Each row gives the file that produces it." | "Every string below is emitted by the Fleet server verbatim. Grep for it." | The old sentence existed to introduce the citation column, which is gone. |
| Heading "8.3.7 Startup messages that never reach your log pipeline" | "8.3.7 Startup messages that bypass the logger" | Off the negative and states the mechanism. |
| "a collector that only ingests structured stderr can miss them entirely" | "a collector configured for structured stderr misses them" | Dropped "only" and "entirely". |
| "Every Fleet process logs only its own work" / "can be entirely confined" | "Each Fleet process logs its own work" / "can be confined" | Dropped "only" and "entirely". |
| "It does not survive a restart and is not derived from a hostname or pod name." | "A restart produces a new one, and the value is unrelated to the hostname or the pod name." | Positive form of both halves. |
| Heading "8.3.10 What is not in the server logs" | "8.3.10 Questions that belong to another surface" | Off the negative; matches the new intro line. Middle column renamed from "It is not here" to "Where it lives", and two cells reworded to name the surface rather than the absence ("Host-side agent logs…", "Fleet's state tables…"). |
| "It does not tell you what a host did, and it is not a record of user intent. …It does not prove the host changed." | "Host behaviour and user intent live on other surfaces. …proves that a request arrived, not that the host changed." | Three negatives into one contrast. |
| "What you gain is mostly that first item, and it is also the entire cost." | "The per-request line is most of the gain and all of the volume." | The original was a near-miss aphorism: "gain" was doing two jobs and "the entire cost" did not match the sentence it landed in. |
| "Retention is not Fleet's." / "applies to recorded errors in Redis only, not to stderr" | "Retention belongs to your platform." / "applies to recorded errors in Redis, not to stderr" | Positive opening; dropped "only" where the following clause already carries the contrast. |

"Only" and "just" kept where load-bearing: "Server faults only"; "debug level only, and not
in `fleetctl debug errors`"; "osquery channel only, never Orbit"; "no warn-only or error-only
threshold"; "leaves a trace on one node only"; "enable debug there only".

## De-AI recheck notes

Second pass over the rewritten prose, hunting relocated tells rather than the mechanical set
(no em-dashes, no banned vocabulary, no "serves as" in the file before or after):

- **Near-miss metaphor:** "and it is also the entire cost" (fixed above). Also checked "the
  level rule is the trap" and "the load balancer trap", which are literal enough to stand.
- **Argument teleportation:** the `internal` paragraph jumped from "Fleet splits the text" to
  "it is only present at the verbosity where that line survives" with the level rule
  unstated; the sentence now reads as a condition on the same clause rather than a new claim.
- **Manufactured specificity:** none added. Existing numbers (64 random bytes, 2 second
  give-up, `24h`, HTTP 408, four built-in labels) are all from the verification trail.
- **Uniform sentence length:** the 8.3.4 consequences list and the 8.3.9 opener were three
  medium sentences each; both now open short. Left the table-heavy stretches alone, since
  parallel phrasing inside a column is the point of a table.
- **Reshuffle-proof paragraph:** "Read silence as no information, in either direction" now
  depends on the sentence before it, which the old two-negative version did not.

## New `[term]()` flags (STYLE §14)

| Flag | Location | Why |
|---|---|---|
| `[node key]()` | 8.3.4, first consequence bullet | The section greps for `invalid node key` in three places and never defines the term. Defined in 1.3's vocabulary table, so this wants a glossary entry rather than a repeat definition. |
| `[DEP]()` | 8.3.6, first row | Matches the flag 1.4 already carries. The literal string is `DEP auth error`, so an administrator who has only met the name ADE has nothing to search for. |

Considered and rejected: `[OTLP]()` (expanded in place in 8.3.1 instead), `[JSON logging]()`
(the `logging_json` row states its effect), `[load balancer affinity]()` (8.3.9 explains the
behaviour in place, and the term itself is not used).

## HTML comments

None present in the file.

## Facts I believe may be wrong (reported, not changed)

- **`logging_disable_banner` "in 4.89.2".** The sentence reads "has no consumer elsewhere in
  the server as of 4.89.2" while the frontmatter records `verified_against: Fleet 4.90.0`.
  4.89.2 is exactly the wrong stamp STYLE §9 warns about (derived from `CHANGELOG.md` on
  `main`). Left as written, including the "treat its effect as unverified" hedge. Worth
  re-checking at a release tag and restamping.
- **Frontmatter `verified_source`** still reads `fleet-public main @ 2026-08-05
  (d2fe9be461); does NOT include 4.90.1 fixes`, which STYLE §9 rules out (a commit on a
  branch, not a release tag), and four table rows are stamped 4.90.1 against a
  `verified_against` of 4.90.0. Out of scope for this pass per the brief; flagging for the
  re-verification pass.
- Nothing else. No fact was altered, no hedge removed.

## Line counts

435 lines before, 418 after. Citations removed: 51 source pointers (49 Go, 2 in-repo docs),
48 of them carrying line numbers. Two table columns dropped (the Source column in 8.3.6 and
8.3.7, the Reference column in 8.3.9), 6 standalone source sentences deleted, and 13
internal identifiers replaced with behaviour.
