# 1.4 The server: MySQL, Redis, and state — style-rules and de-AI pass

Target: `manual/01-foundations/1.4-server-state.md`
Pass run 2026-08-20. **Facts unchanged; presentation only.** Verified against Fleet 4.90.1
(`git tag fleet-v4.90.1`). The research trail lives in `1.4-notes.md`; this file records what
this editing pass changed and, above all, **the code pointers deleted from reader-facing
prose** (STYLE §8). The section carried 14 Go file references going in. Every one is tabulated
below against the fact it supports, so a future editor can re-verify without the prose
carrying developer detail.

## Code-citation trail removed from the section

Each row: the fact as it now reads in the section, and the pointer deleted from the prose.
All pointers are at tag `fleet-v4.90.1`.

| Fact retained in prose | Source pointer removed |
|---|---|
| Live query results travel back through Redis pub/sub because the websocket is held by one instance | `docs/Contributing/guides/troubleshooting-live-queries.md` (now cited as fleetdm.com/docs/contributing/guides/troubleshooting-live-queries) |
| Recorded errors are ephemeral by intent: deduplicate, hold, flush on read | package doc comment, `server/errorstore/errors.go` ("ephemeral data, deduplication, flush on read"). Direct quote dropped as a source quote; behaviour kept. |
| Apple profile pre-assign keys live under `mdm:preassign:` for an hour | `server/mdm/apple/profile_matcher.go`. Redis key prefix kept: it is inspectable by the reader. |
| Reconciler cursors for Apple, Apple declaration, Windows, Android live in Redis | `server/datastore/mysqlredis/` |
| With no carve bucket, carve blocks are written to the database as rows | `cmd/fleet/datastore.go` (carve store starts as the MySQL datastore, replaced when a bucket is configured) |
| With no installer bucket, Fleet writes to the instance's own filesystem, system temp dir unless `FLEET_SOFTWARE_INSTALLER_STORE_DIR` overrides, and logs "using local filesystem software installer store, this is not suitable for production use" | `cmd/fleet/serve.go`. Env var and log string kept: both are the reader's interface. |
| In-memory config cache in front of MySQL, 1s app config / 1m the rest, per process | `server/datastore/cached_mysql/cached_mysql.go` |
| A path that reads a value in order to modify it bypasses the cache | `ctxdb.BypassCachedMysql` (internal identifier, dropped) |
| Codebase over 600,000 lines being reorganised from layers into bounded contexts, boundaries enforced at build time | `docs/Contributing/architecture/modular-monolith/README.md` (now cited as fleetdm.com/docs/contributing/architecture/modular-monolith); Go `internal/` dirs and `arch_test.go` import tests dropped as developer-only, replaced by "enforced at build time"; "2,300+ Go files" dropped as developer detail |
| MySQL floor 8.0.44, tested 8.0.44 / 8.4.8 / 9.5.0, 9.6.0 incompatible, Aurora 3.10.3+, variants unsupported | `docs/Get started/FAQ.md` (now cited as fleetdm.com/docs/get-started/faq) |
| Reads default to the replica; writes always the primary; a small set of paths reads the primary | `server/datastore/mysql/mysql.go`, `ctxdb.RequirePrimary`. **"About 34 non-test call sites" dropped** as manufactured specificity plus developer detail; the named areas (server config, Apple/Windows MDM, Android, jobs, VPP, Fleet-maintained apps, user management) carry the same information for an operator. |
| Cluster mode is detected at startup, falling back to a standalone pool on "ERR This instance has cluster support disabled" or an unknown/not-permitted command | `server/datastore/redis/redis.go`. Was flagged "inferred from source, not documented"; now reads "This detection is not documented." The Redis error string is kept as a searchable log string. |
| Cron schedules take a lock in the `locks` table, keyed by schedule name, owner is the instance, expiry equals the interval, renewed while running | `server/datastore/mysql/locks.go`, `server/service/schedule/schedule.go`. `locks` table name kept: the reader queries it. |
| A separate Redis-backed lock, 60s default expiry, for shorter-lived coordination | `server/service/redis_lock` |
| `instanceID` is 64 bytes of random text generated at process start, logged once as `instance info`, recorded in `cron_stats.instance` | `cmd/fleet/serve.go`. Table, column, log line and field name kept: all reader-facing. |
| 575 schema migrations and 9 data migrations at this release; `fleet prepare db` applies them | `server/datastore/mysql/migrations/`. "Go files in two families" dropped. |
| Four startup states: all applied, none applied (exit), some missing (exit unless `allow_missing_migrations`), unknown applied (keeps serving in production, dev build exits) | `cmd/fleet/datastore.go`, `server/fleet/datastore.go`. "inferred from source, not documented" kept as "This behaviour is not documented." |
| Upgrade procedure: stop instances, back up, migrate, start new version; 5 to 10 minutes typical | `docs/Deploy/Upgrading-Fleet.md` (now cited as fleetdm.com/docs/deploy/upgrading-fleet) |
| Three 4.90.1 fixes quoted in prose (host-certificate migration, maintained-apps lock contention, DEP assignment 500) | `CHANGELOG.md` at this tag (now cited as release notes for 4.90.1, github.com/fleetdm/fleet/releases) |
| Host auth cache miss falls through to MySQL, so check-ins keep working | `server/datastore/mysqlredis/host_cache.go` |
| `/healthz` returns 500 when either store fails; `?check=mysql` and `?check=redis` check one each | `server/health/health.go`. Endpoints kept: they are the reader's interface. |
| Three infrastructure dependencies (MySQL, Redis, TLS cert); single-writer only; writes local; AWS sizings | `docs/Deploy/Reference-Architectures.md` (now cited as fleetdm.com/docs/deploy/reference-architectures) |

Reader-usable identifiers deliberately **kept**: every `mysql_*`, `redis_*`, `s3_*`,
`osquery_*` and `logging_*` config key; `FLEET_MYSQL_REGION`,
`FLEET_MYSQL_READ_REPLICA_REGION`, `FLEET_SOFTWARE_INSTALLER_STORE_DIR`,
`FLEET_UPGRADES_ALLOW_MISSING_MIGRATIONS`; `client-output-buffer-limit` and the three
ElastiCache parameter names; `/healthz` and its `check` values; `fleet prepare db`; the
`locks`, `cron_stats`, `software` and `software_titles` tables and the `instance` column;
`mdm:preassign:`; the `instance info` log line; the installer-store log string; the AWS
instance classes `db.t4g.medium` and `db.r6g.8xlarge`.

## Diagram placeholders added (STYLE §13)

| Placeholder | Placed | Idea |
|---|---|---|
| **Three stores, and what survives a restart** | end of "What it is", after the store table | Column per store, contents as pills, a green/amber "survives a restart" band per column. Caption: "Three stores. One of them is meant to be disposable." |
| **Shared stores, separate caches** | top of "Horizontal scale, and what is actually coordinated" | Load balancer over three Fleet instances over MySQL primary plus Redis, with a per-instance in-memory cache box. Caption: "The stores are shared. The cache is not." |

Nothing was drawn. Prose stands on its own without either image.

## Positive-voice and heading changes (STYLE §15)

| Before | After | Why |
|---|---|---|
| Heading "Object storage is for bytes, not rows" | "Object storage holds the bytes" | Heading off a negative. The inbound link from "What it is" said "Object storage is not optional in production" while pointing at that anchor; link text and anchor now agree. |
| Heading "The fourth store nobody configures" | "The fourth store, and why two instances disagree" | Off a negative, and names the consequence the reader came for. |
| "**Nothing is inherited.**" | "**Configure the replica from scratch.**" | Same fact, positive imperative. |
| "**API and check-in traffic is not coordinated at all.**" | "**Any instance answers any request.**" | Positive form; the uncoordinated-by-design point follows in the body. |
| "None of it is a fact you cannot recompute." | "Every one of those is recomputable." | Double negative. |
| "Nothing errors." | "The drop is silent." | Says what happens. |
| "Only two of the three stores need backing up, and they cannot be captured at a consistent point in time relative to each other." | "Two of the three stores need backing up, and no snapshot captures both at the same instant." | Dropped "only"; positive form of the consistency point. |
| "Looking for the Redis name in an ElastiCache parameter group and not finding it is a normal way to conclude, wrongly, that the setting does not apply." | "Search an ElastiCache parameter group for those three names rather than the Redis one." | Named a misunderstanding in order to deny it. |
| "worth knowing so you do not read that message as fatal" | "The message reports the state and Fleet carries on." | Same. The "rolling back the binary is survivable" point already follows in the next paragraph, so the duplicate was cut rather than reworded. |
| "Reading the code, you will find most of Fleet still in the older layered shape, and that is expected rather than a sign you are looking in the wrong place." | "Most of Fleet is still in the older layered shape, so the term describes a direction of travel more than it describes today's binary." | Addressed a code reader, and pre-empted a misunderstanding. |
| "So a replica does not need per-query annotation to be useful. Add one and read traffic moves." | "Add a replica and read traffic moves, with no per-query work on your side." | Answered a question nobody asked; "annotation" was developer framing. |
| "It does not handle it everywhere." | "Coverage is not complete." | **Hedge preserved deliberately.** Fleet does not handle replica lag on every path; that is the point of the following 4.90.1 example. Not flattened into an absolute. |
| "kill any one of them without consequence" | "replace any one of them" | The original overstated: the section later says in-flight live queries die with their instance. Presentation change, no fact touched. |
| "which is the whole reason it exists" | (cut) | Flourish. |
| "purely to keep those lookups off MySQL" / "entirely" / "It is per process." | trimmed | Intensifiers and defensive qualifiers. |

"Only" and "just" kept where load-bearing: "only one instance runs it at a time" (cron), "a `PUBLISH` on one node reports only its own subscribers", "only one winning the lock", "reproducible only by luck", and inside the two direct quotations.

## Other presentation changes

- Renamed the fourth store from "in-process cache" to "in-memory cache" throughout, including the store table, so the term matches the diagram label and the prose.
- "at this tag" to "at this release" everywhere (5 places). Reader-facing prose should not talk about git tags.
- "config documentation" / "config reference" / "the doc" to "configuration reference" / "Fleet's own documentation" / "the same page".
- Added a **File carve** row to the Vocabulary table. "File carve blocks" appeared in the opening store table with no definition anywhere in the section; defining it in place beat flagging it.
- Added an in-place gloss for Redis pub/sub ("a channel that delivers each message to whoever is listening at that moment and keeps nothing afterwards"), which also carries the non-durability point the following sentences rely on. No `[pubsub]()` flag needed as a result.
- Vocabulary already defines read replica, instance, campaign, cron schedule and reconciler in place, and cluster mode and object storage are explained where they appear, so none of those were flagged.
- Rewrapped touched paragraphs at 88 columns to match the rest of the file.

## New `[term]()` flags (STYLE §14)

| Flag | Location | Why |
|---|---|---|
| `[VPP]()` | "When a read replica helps", in the list of areas that read from the primary | Matches the flags already in 1.2 and 1.3. |
| `[DEP]()` | replica-lag paragraph, "a host had no [DEP]() assignment yet" | The quoted 4.90.1 fix uses DEP; an administrator who has only met the name ADE will stumble. 1.3 flagged `[ADE]()`, and the glossary entry should cover both names. |

## HTML comments

None present in the file.

## Facts I believe may be wrong (reported, not changed)

- **None.** Every fact was left as written. Two presentation notes that touch on accuracy, both listed above rather than acted on as fact changes: the original "kill any one of them without consequence" sat in tension with the later statement that in-flight live queries die with their instance (reworded to "replace any one of them", which is presentation only); and "About 34 non-test call sites require the primary at this tag" was dropped as developer detail, so the count now survives only in this notes file and in `1.4-notes.md`.

## Line counts

530 lines before, 559 after. The growth is the two diagram placeholders (32 lines) plus one Vocabulary row; prose is slightly shorter than it was.
