# De-AI + style pass: 8.5 `fleetctl debug`

File: `manual/08-troubleshooting/8.5-fleetctl-debug.md`
Started: 2026-08-21. Before: 607 lines.

## Inbound links (checked before any heading rename)
`grep -rn "8.5-fleetctl-debug.md#"` -> zero anchor links.
But numbered cross-refs exist and MUST keep their numbers:
- 8.13 -> §8.5.5, §8.5.6, §8.5.13
- 8.14, 8.13, 8.2, 8.1, 8.3, 8.6, 8.8, 8.9, 8.12, 1.2, 1.4 -> file-level links only.
=> Section numbering is frozen. Heading *text* may change; numbers may not.

## Citation removals (path-based / bare filename)
(appended as work proceeds)

### Path-based citations removed (12)
| Line (orig) | Citation | Fact it supported | Replacement |
|---|---|---|---|
| 28 | `cmd/fleetctl/fleetctl/debug.go`, `debugCommand()` | Twelve subcommands exist | plain count, no source |
| 46 | `server/service/client_debug.go` | subcommand -> endpoint mapping | mapping stays in the table, attribution dropped |
| 47 | `server/service/debug_handler.go` | same | same |
| 64 | `server/service/debug_handler.go` + `debugAuthenticationMiddleware.Middleware` + Go snippet | every `/debug/` route needs global admin; team admin and global maintainer get 403 | prose statement of the behaviour, Go block deleted |
| 85 | `server/datastore/mysql/mysql.go`, `InnoDBStatus()` | the PROCESS-privilege error text | error text kept verbatim as output, attribution dropped |
| 103 | `cmd/fleetctl/fleetctl/flags.go` | flag/env-var definitions | flag table stands alone |
| 194 | `cmd/fleet/serve.go`, `liveQueryRestPeriod` | server allows >=100s write time, so a 30s profile timing out is a proxy timeout | behaviour stated without the identifier |
| 234 | `server/errorstore/errors.go` | errors live in Redis under `error:{hash}:json` / `:count` | Redis keys kept (reader-inspectable), attribution dropped |
| 436 | `server/service/debug_handler.go:93` | `net/http/pprof` mounted unmodified, so `?debug=2` works | behaviour kept, `net/http/pprof` KEPT per brief |
| 493 | `server/datastore/mysql/mysql.go` + source comment | the three db-* commands use the writer connection | behaviour + reason stated in prose |
| 555 | `server/errorstore/errors.go` | socket addresses normalized to `<addr>` for request-timeout errors | behaviour kept, attribution dropped |
| 563 | `cmd/fleetctl/fleetctl/fleetctl.go`, `defaultFileMode` | output files written 0600 | mode kept, attribution dropped |

### Bare filenames removed (17 of the 18 counted)
`debug.go` x3 (L28 path, L121, L189) · `debug_handler.go` x3 (L47, L64, L436) ·
`mysql.go` x2 (L85, L493) · `errors.go` x2 (L234, L555) · `config.go` (L103) ·
`flags.go` (L103) · `serve.go` (L194) · `client_debug.go` (L46) · `fleetctl.go` (L563) ·
`ctxerr.go` (L261) · `transport_error.go` (L262).

**`pkg.go` is a false positive.** The 18th counted match is the frontmatter
`further_reading` URL `https://pkg.go.dev/net/http/pprof`. That is a documentation URL a
reader can open, not a code citation, so it stays.

### Go identifiers removed beyond the file lists
`debugCommand()`, `debugAuthenticationMiddleware.Middleware`, `fleet.RoleAdmin`,
`outfileName()` + its Go body, `debugArchiveCommand()`, `runtime.SetBlockProfileRate`,
`runtime.SetMutexProfileFraction`, `tarName := outfile + "/" + outname`,
`collectBatchErrors`, `debugConnectionCommand()`, `packaging.OsqueryCerts`,
`debugMigrations()`, `defaultFileMode`, `InnoDBStatus()`.
Three ```go blocks deleted (auth middleware check, `outfileName`, the archive
skip-and-continue `Fprintf`). Their behaviour is now prose; the stderr strings readers
actually see are kept as plain output.

### Doc/CHANGELOG citations converted
- `docs/` tree (L49) -> fleetdm.com/docs
- `docs/Deploy/Reference-Architectures.md` (L220) -> fleetdm.com/docs/deploy/reference-architectures
- `docs/REST API/rest-api.md` (L270, L529) -> fleetdm.com/docs/rest-api/rest-api
- `CHANGELOG.md` (L394, L530, L599) -> release number + github.com/fleetdm/fleet/releases
- New `further_reading` entry: https://github.com/fleetdm/fleet/releases

### JSON example
The "Get errors" response sample carried real stack frames naming `ctxerr.go:262` and
`transport_error.go:80`. Both are on the removal list, so the two frames are now shown as
the shape a reader should expect rather than as literal Fleet source frames. Field names,
nesting, and the `count`-as-string detail are unchanged.

### Version claims
L166 read "verified by grep across all `*.go` in `fleet-public` at 4.89.2". 4.89.2 was the
bogus CHANGELOG stamp; the sentence also cited code. Rewritten to state the behaviour
(Fleet never turns block or mutex profiling on) with no version and no grep. No other
4.89.2 remained. 4.86.0 and 4.87.0 are real release numbers and stay.

### Positive voice / heading renames
- `### What it does not cover` -> `### What a pass proves`
- `### The one thing fleetctl will not give you` -> `### Full goroutine stacks as text`
- `## 8.5.12 Trace sampling has no fleetctl subcommand` -> `## 8.5.12 Trace sampling, endpoints only`
Numbers untouched, so §8.5.5/§8.5.6/§8.5.13 references from 8.13 still land. No anchor
links exist to any heading in this file.

### One finding added, not merely preserved (flagged)
Brief item 4 lists "errors are server faults only; client 4xx is never recorded". That
sentence was **absent** from 8.5 as written (grep: no `4xx`, no `server fault` in the
original). It is present and verified in 8.3 (§"Fleet's error handler stores an error in
Redis when the error is a server fault", L175-177). I added one sentence to 8.5.6 carrying
that fact and pointing at 8.3, because the brief asks for it as a preserved finding and a
reader hunting a 401 in `debug errors` is the exact failure mode it prevents. Flagging it as
an addition rather than an edit.

Minor tension noted, not changed: the "Get errors" response sample (taken from Fleet's REST
API docs) shows a chain whose first message is `Authorization header required`, which reads
like a client error. The sample is upstream Fleet documentation, so it stays as published.

### De-AI loop findings acted on
- Two meta-sentences about the section's own purpose ("most of why this section exists" /
  "the reason this section is long") were doing the same job. First one cut to a plain fact,
  second kept as the corpus-gap point that item 4 of the brief calls load-bearing.
- Intro sentence "Nothing in it needs shell access" and its restatement in 8.5.2 were the
  same negative claim twice. Intro now states the requirement positively (a reachable API
  and a global admin token); the 8.5.2 restatement is gone.
- `Read is destructive? | No, unless --flush` -> two positive rows: reading is
  non-destructive, `--flush` deletes after a successful read.
- `A single heap profile ... It does not tell you what is growing` -> the same point stated
  once, positively.
- Timestamp paragraph reworked: the `Z`-is-a-literal fact now carries the consequence
  (filename order equals capture order on one machine, not across two) instead of trailing
  "Confirmed in source".
- Glossed in place rather than flagged: pprof ("Go's standard profiling format"), goroutine
  ("Go's unit of concurrent work"), RSS ("resident memory"), protobuf ("the compressed
  binary form that pprof reads"). `[pprof]()` is already flagged in 8.14, so no second flag.
- **No new `[term]()` flags.** Every candidate took a short in-place gloss.
- No diagram placeholders added. Tables untouched except the two row rewrites above.

### Possible cross-section conflict (reported, not changed)
8.5 says released binaries ship without debug symbols as of 4.86.0, "so passing the `fleet`
binary alongside a profile adds nothing". 8.14 L174 says "Supplying the Fleet binary as well
gets you symbol names". One of the two is wrong for 4.90.0. Flagged for whoever re-verifies
against the tag.

### Counts
Before 607 lines, after 593. Zero em-dashes, zero banned words, zero `CHANGELOG.md`,
zero `Source:`/`Confirmed in` attributions, zero Go paths or bare Go filenames
(the one remaining `.go` match is the pkg.go.dev URL). Kept: `go tool pprof` x9,
`/debug/pprof/*` x8 (one added by the new `Failed profile` sample output),
`net/http/pprof` x2.
