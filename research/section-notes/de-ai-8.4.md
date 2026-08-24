# De-AI pass notes: 8.4 Host-side investigation

Started 2026-08-21. Target file: `manual/08-troubleshooting/8.4-host-side-investigation.md`.
Baseline: 726 lines, 17 Go/code citations.

## Status log
- [ ] Read STYLE.md §0, §8, §14, §15
- [ ] Read 8.14 for target voice
- [ ] Inbound anchor inventory
- [ ] Citation table
- [ ] Edit pass
- [ ] Recheck

## Inbound anchors (from grep, do not break)
- `#846-osquery-introspection-tables` (8.2:260, 1.2:514)
- `#847-orbit-shell-the-local-osquery-shell` (8.2:264)
- `#8412-agent-updates-which-channel-landed-and-why-it-did-not` (1.2:250, 1.2:627, 1.2:695)
- `#842-is-the-agent-running` (1.2:303)
- `#845-the-half-enrolled-state-mdm-without-an-agent` (1.2:669, 1.2:696)

Note: 8.4.7 and 8.4.12 and 8.4.5 headings are anchor-locked by inbound links.

## Pre-flight checks (done)
- Em-dashes: 0. Banned vocabulary: none found. HTML comments: none. Existing `[term]()`: none.
- 8.4.11 heading "What the host cannot tell you" matches 8.7.3 "What live query cannot tell
  you" as a chapter convention. Per the 8.14 precedent, **kept** rather than renamed alone.
- 8.4.2, 8.4.5, 8.4.6, 8.4.7, 8.4.12 headings are anchor-locked by inbound links from 1.2
  and 8.2. Frozen verbatim.
- The brief's "in-band upgrade marker / postinstall delays the daemon bounce" finding is
  **not present in the draft**. Nothing to preserve; nothing added (no re-verification).

## Batch plan (save after each)
1. frontmatter, intro, 8.4.1, 8.4.2
2. 8.4.3, 8.4.4
3. 8.4.5, 8.4.6
4. 8.4.7, 8.4.8, 8.4.9
5. 8.4.10, 8.4.11, 8.4.12, See also
6. Recheck loop

## Citation conversion table
Pointers were read at `fleet-public main @ 2026-08-05 (d2fe9be461)`, per frontmatter.

### Batch 1 (frontmatter, intro, 8.4.1, 8.4.2) — done

| Fact retained in prose | Pointer removed | How the fact now reads |
|---|---|---|
| `com.fleetdm.orbit` LaunchDaemon label, `Fleet osquery` service name, `orbit.service` unit | `orbit/pkg/packaging/macos_templates.go` (`DAEMON_LABEL`, launchd `Label`); `constant.SystemServiceName` in `orbit/pkg/constant/constant.go`; `writeSystemdUnit()` in `orbit/pkg/packaging/linux_shared.go` | "Those three names are the ones the packaging process writes, so they are stable across versions and across every package `fleetctl` builds." All three names kept in the table. |
| macOS plist `ThrottleInterval` of 10 seconds | `orbit/pkg/packaging/macos_templates.go` | "The plist throttles respawns to one every ten seconds, so a crash-looping Orbit comes back on that cadence rather than instantly." |
| The five paths Fleet's uninstall script removes | `it-and-security/lib/macos/scripts/uninstall-fleetd-macos.sh` | "Fleet's published uninstall script removes ..." with every path kept |
| Windows `ImagePath` carries the packaged flags, including `--debug` and `--fleet-url` | `orbit/pkg/packaging/windows_templates.go`, MSI `ServiceInstall` arguments | "The MSI writes those arguments at install time." |
| `Restart=always`, `RestartSec=1`, `CPUQuota=20%` | `orbit/pkg/packaging/linux_shared.go` | plain statement, values kept |

Other batch 1 changes:
- `verified_on` 2026-08-20 to 2026-08-21. `verified_against` / `verified_source` untouched.
- `further_reading` gained https://fleetdm.com/guides/certificates-in-fleetd (batch 2 uses it)
  and https://github.com/fleetdm/fleet/tree/main/docs/solutions (batch 4, the toggle scripts).
- Intro: "this section is how you find out which one is lying" was a near-miss metaphor (a
  stale read is not a lie). Now "When the two disagree the host settles it, and this section
  is how you get its answer."
- 8.4.1: cut "Where the two differ, the difference is called out." Meta-promise, no fact.
- **LaunchDaemon glossed in place**, not flagged: "Orbit runs as a LaunchDaemon, meaning a
  system-wide background service that launchd starts at boot, with no user logged in."
- §15: "its absence says nothing about the other two" to "the other two run with or without
  it"; "If the plist is missing entirely, the agent was uninstalled, not broken" to "A missing
  plist means the agent was uninstalled"; "Anything that removed some but not all of those was
  not that script" to "A host with some of those paths still standing was cleaned up by
  something other than that script"; "are standard Windows and are not documented by Fleet" to
  "The cmdlets are stock Windows."

### Batch 2 (8.4.3, 8.4.4) — done

| Fact retained in prose | Pointer removed | How the fact now reads |
|---|---|---|
| Orbit root per platform; Windows resolves it from `ProgramFiles` at startup | `orbit/pkg/update/options_darwin.go`, `options_linux_amd64.go`, `options_windows_amd64.go` (`RootDirectory`) | "Windows reads that path from the `ProgramFiles` environment variable at startup, so on a non-standard install drive the Orbit root moves with it." Table of the three roots untouched. |
| Orbit root filenames and the `bin/` layout | `orbit/pkg/constant/constant.go`; `osquery.db` and `osquery.flags` in `orbit/cmd/orbit/orbit.go` | Confirmation sentences deleted. Every filename in the table is unchanged. |
| `certs.pem` is curl's `cacert.pem`, embedded in `fleetctl`, written by `fleetctl package` | `articles/certificates-in-fleetd.md` | inline fleetdm.com/guides/certificates-in-fleetd, added to `further_reading` |
| `orbit version` exists | `versionCommand` in `orbit/cmd/orbit/orbit.go` | "`orbit version` is a real subcommand." |
| Uninstall script greps `MDM enrollment: Yes` / `No` | `it-and-security/lib/macos/scripts/uninstall-fleetd-macos.sh` | "Fleet's own uninstall script branches on this output, grepping for ..." |
| fleetd reads the assigned enrollment profile with `profiles show -type enrollment`, run as the console user | `orbit/pkg/profiles/profiles_darwin.go`, `CheckAssignedEnrollmentProfile` | Plain statement, and the `launchctl asuser ...` invocation was promoted out of inline backticks into its own copyable code block. |
| `profiles show -type configuration` and `profiles renew -type enrollment` are Fleet-sanctioned | `tools/mdm/apple/troubleshooting.md` | "Fleet's internal MDM troubleshooting notes use ..." (in-repo tooling doc with no public URL, so no conversion; same call 8.14 made for docs with no fleetdm.com equivalent, minus the GitHub link because this one is a tools directory rather than a contributor guide) |
| The `mdm` table column list | `schema/osquery_fleet_schema.json` | "macOS only." The column list stays in the SQL block. |

Other batch 2 changes:
- **RocksDB glossed in place**: "osquery's local store, an embedded RocksDB database".
- `[node key]()` flagged on the `secret-orbit-node-key.txt` row (first use in the section).
- `[ADE]()` and `[DEP]()` flagged together on the `Enrolled via DEP:` row, matching 8.8's
  pairing: "Automated Device Enrollment ([ADE]()), which Apple's older API and this command
  still call [DEP]()."
- §15 / de-AI: "Note that fleetd runs it ... because" to a direct statement; "`profiles
  status` does not need that treatment" to "reads the same either way"; "the single best
  host-side MDM check available on macOS" to "the best host-side MDM check macOS offers";
  "treat the exact flag as unverified against Fleet's docs, though the command itself is
  standard" to "stock macOS, with no Fleet documentation behind the flag".
- "**UI equivalent, volatile:**" was a near-miss label (the UI is not volatile, its location
  is). Now "**UI equivalent, and it moves between macOS versions:**".
- "cannot ask them to open Terminal" to "who should not be asked to open Terminal" (§15).
- Kept "There is no `cert.pem`" and the `certs.pem` / `fleet.pem` contrast verbatim. It is a
  naming trap the brief lists as reader-usable, and the negative is the point.

### Batch 3 (8.4.5, 8.4.6) — done

| Fact retained in prose | Pointer removed | How the fact now reads |
|---|---|---|
| `fleetctl package` flag set for the rebuild | `cmd/fleetctl/fleetctl/package.go` | Confirmation sentence deleted. The command block with `--type`, `--fleet-url`, `--enroll-secret`, `--fleet-desktop`, `--enable-scripts` is untouched. |
| Every table in 8.4.6 is a real, cross-platform table | `schema/osquery_fleet_schema.json` | "Every table below is in Fleet's published table schema (fleetdm.com/tables)". Added fleetdm.com/tables to `further_reading`. |
| `command_line_flags` take effect on fleetd restart, via `<orbit root>/osquery.flags`; a revoked enroll secret stops flag updates | `docs/Configuration/agent-configuration.md` + `orbit/cmd/orbit/orbit.go` | inline fleetdm.com/docs/configuration/agent-configuration (already in `further_reading`) |
| `disable_events: false` turns eventing on; the three per-platform extra flags | `articles/osquery-evented-tables-overview.md` (x2) | inline fleetdm.com/guides/osquery-evented-tables-overview (already in `further_reading`); "All three are in that guide." |

**The 4.89.2 claim.** 8.4.5 read "open as of 4.89.2" on issue 47793. Per the brief this was a
CHANGELOG-derived stamp from a tree that lagged the code actually read (post-4.90.0). Now
"still open as of 4.90.x", which keeps the point (the issue has no fix in any shipped release)
without asserting a release that was never checked. No other 4.89.2 appears in the section, so
nothing else moved.

Other batch 3 changes:
- **Counting bug fixed.** "**Confirm it in two commands.** Both must be true:" preceded a
  block of **three** commands. Now "**Confirm it on the host.** The first command says
  enrolled, the other two say the agent is not there:". Reported as a draft defect, not a fact
  change.
- **Evented tables glossed in place** rather than flagged: "An evented table is filled by a
  background publisher as things happen, rather than by inspecting the system at the moment a
  query runs."
- §15 / filler: dropped "simply" from "is simply absent"; "Not documented; this is an observed
  rate ..., not a published figure" to "... rather than a published figure"; "`command_line_flags`
  only apply after fleetd restarts" to "apply after fleetd restarts"; "If the flag is not in
  this table, either the restart has not happened or ..." to "A flag missing from this table
  means the restart has not happened, or ..."; "while leaving everything else working" to
  "while everything else keeps working".
- `[!internal]` note: "never used as an inference" was strained. Now "never picked up". The
  note is otherwise preserved, including the 24-pending-commands detail and the queue-depth
  tell.
- Kept "never in the result log" in the osquery-uptime paragraph. §15 allows one explicit
  contrast where readers demonstrably get it wrong, and the result log is where they look.

### Batch 4 (8.4.7, 8.4.8, 8.4.9) — done

| Fact retained in prose | Pointer removed | How the fact now reads |
|---|---|---|
| `orbit shell` is aliased as `orbit osqueryi` | `orbit/cmd/orbit/shell.go` | plain statement, both invocations kept |
| The shell runs standalone with a default config and its own `<orbit root>/shell` data path, so it never takes the daemon's RocksDB lock | `docs/Configuration/agent-configuration.md` + `shell.go` | inline fleetdm.com/docs/configuration/agent-configuration, "draws the same line" |
| `--disable-events false` is the documented local test for evented tables | `articles/osquery-evented-tables-overview.md` | inline fleetdm.com/guides/osquery-evented-tables-overview |
| A trailing bare argument means single-query mode, where Fleet's own tables are absent | `shell.go` argument inspection; "Read from source; not documented" | "a trailing argument that does not start with `--` puts osquery in single-query mode ... **Fleet's own tables are available only in the interactive shell**. Undocumented." |
| Both debug-toggle scripts, and where to get them | `docs/solutions/...` in-repo paths | Paths kept (the reader needs them to fetch the script) and given a real URL: github.com/fleetdm/fleet/tree/main/docs/solutions, now in `further_reading`. Same call 8.14 made for contributor guides. |
| Linux debug via `EnvironmentFile=/etc/default/orbit` and `ORBIT_DEBUG=true` | `writeSystemdUnit()` and `envTemplate` in `orbit/pkg/packaging/linux_shared.go` | "Its systemd unit carries `EnvironmentFile=/etc/default/orbit`, and a package built with `--debug` writes `ORBIT_DEBUG=true` into that file, which is the mechanism the table above works by hand." |

Other batch 4 changes:
- The 15-second sleep finding is preserved. Cut its negative twin, "Without it, Fleet would see
  a script that never returned", which restated the preceding sentence backwards (§15).
- "**It is not the running agent.**" to "**The shell is a separate osquery, not the running
  agent.**" Positive lead, warning intact. "So it proves osquery behavior. It does not prove
  Fleet's configuration of osquery." to "What it proves is osquery behaviour. Fleet's
  configuration of osquery stays a separate question."
- "to avoid fighting the daemon over the RocksDB lock" to "so it never contends with the daemon
  for the RocksDB lock".
- "Go left to the network path or right to the server" was a near-miss metaphor: the manual
  establishes no left/right pipeline axis (checked 8.1, no such language). Now "The next
  candidates are the network path between host and server, and the server itself."
- Kept both meaning-bearing "only"s: "events gathered while it is open" and "available only in
  the interactive shell".

### Batch 5 (8.4.10, 8.4.11, 8.4.12, See also) — done

| Fact retained in prose | Pointer removed | How the fact now reads |
|---|---|---|
| Binaries land at `<orbit root>/bin/<target>/<platform>/<channel>/<file>`, so a channel change shows up as a new directory | `LocalTargetPaths` in `orbit/pkg/update/update.go` | plain statement; the full target/platform/file table is untouched |
| 3 download attempts, then a 24 hour cooldown per target, keyed on the target's content hash | `retry.NewLimitedWithCooldown(3, 24*time.Hour)`, `orbit/pkg/update/update.go` | "A failed target download gets 3 attempts, then a **24 hour cooldown for that target**. The retry key is the target's content hash" |

Other batch 5 changes:
- **TUF glossed in place** rather than flagged: "a signed update repository of its own, built
  on The Update Framework (TUF)". Later bare uses of TUF (`tuf: file not found`, "Expired TUF
  signatures", "TUF metadata") now have an antecedent.
- 8.4.11 kept its heading and every row, including the audit-log finding: no host-side event
  history, so a locally removed agent leaves no trace in Fleet's audit log.
- "an event that does not exist" to "an event that was never written"; the three platform audit
  facilities are now a list rather than a parenthetical with a trailing "not from Fleet" (§15).
- "Three states, and they mean different things:" to "Three states, each pointing somewhere
  different:" (the old clause carried no fact).
- "**Expired TUF signatures block startup selectively.**" to "**... block startup by role.**"
  The role-by-role behaviour is what the paragraph then describes.
- See also: "whether the host is even the right end of the pipeline" to "whether the host is
  the right end of the pipeline".

### Polish / de-AI recheck — done

- Batch 1's replacement sentence had drifted into an unverified claim ("stable across
  versions"). Rewritten to what was actually read: "Those names come from fleetd's own
  packaging templates, so every package `fleetctl` builds uses them."
- "**An Orbit root that does not exist at all**" to "**No Orbit root at all**", parallel with
  the sentence before it.
- "as things happen" to "as events occur" in the evented-table gloss.
- "which is the mechanism the table above works by hand" was ungrammatical. Now "which is what
  the table above does by hand."
- `profiles status` paragraph reordered so the undocumented-but-best point lands last as one
  sentence instead of two glued clauses.
- Reflowed the lines my edits pushed past the file's ~80 column wrap. 8.4.12 wraps at ~88 in
  the original and was left at ~88.
- Meaning-bearing "only"/"actually" audited one by one and kept: "present only on packages
  built with `--fleet-certificate`", "the binary actually installed, versus what agent options
  claim", "holds only `certs.pem` and `bin/`", "reflects the MDM channel only", "Queue depth
  that only grows", "Did the flag actually take", "what profiles actually applied", "events
  gathered while it is open", "available only in the interactive shell", "The device only sees
  commands it has been handed", "records server-side actions only".

## Preserved deliberately (against the general de-AI instinct)

- Every table. Part VIII is the reference chapter; **no diagram placeholders added**.
- "There is no `cert.pem`." The negative is the finding.
- "never in the result log" (osquery status log vs result log).
- "Restarting Orbit does not." (reset the cooldown) The negative is the actionable fact.
- "What the host cannot tell you" as the 8.4.11 heading: chapter convention shared with 8.7.3
  "What live query cannot tell you". Renaming one alone breaks the pattern (8.14 precedent).
- 8.4.2, 8.4.5, 8.4.6, 8.4.7, 8.4.12 headings, all anchor-locked. No heading in the section
  was renamed, so no inbound link needed updating.
- Both landing points other sections route to: 8.4.5 (half-enrolled) and 8.4.6 (host-side
  checks) keep their headings, their anchors, and their content.
- The `[!internal]` customer-thread note in 8.4.5.
- Every identifier on the brief's keep-list. Spot-checked after the edit: `com.fleetdm.orbit`,
  `Fleet osquery`, `orbit.service`, `EnvironmentFile=/etc/default/orbit`, `certs.pem`,
  `fleet.pem`, `identifier`, `osquery.db`, `secret.txt`, `secret-orbit-node-key.txt`, `bin/`,
  `profiles status/list/show/renew/remove`, `launchctl` (print, bootout, bootstrap, kickstart,
  asuser), `dsregcmd /status` (absent from the draft, see below), systemd commands,
  `orbit shell` with `--` passthrough and `--disable-events false`, `osquery_info`,
  `osquery_flags`, `osquery_schedule`, `osquery_events`, `fleetd_logs`, `time`, `ORBIT_DEBUG`,
  both toggle scripts, `fleetctl package` flags, log paths.

## Findings reported, not changed

1. **`dsregcmd /status` is on the brief's keep-list but is not in the draft.** Nothing to
   preserve. Not added, since adding it would be new writing and would need verification.
2. **The brief's "in-band upgrade marker / postinstall delays the daemon bounce" finding is
   also absent from the draft.** Same call. Both may belong to a different section, or to a
   research note that never landed here.
3. **Draft defect, corrected:** "**Confirm it in two commands.** Both must be true:" introduced
   a block of three commands. Now "**Confirm it on the host.** The first command says enrolled,
   the other two say the agent is not there:". Presentation, not fact.
4. **8.4.10 is titled "The three log files you open first" and lists four paths** (orbit
   stderr, journalctl, the osquery INFO log, and the Windows `orbit-osquery.log`). Read
   generously it is three per platform. Left alone; worth a glance.

## Line count
726 before, 722 after. 17+ code pointers removed, 0 remaining
(`grep` for `orbit/pkg`, `orbit/cmd`, `cmd/fleetctl`, `server/`, `schema/`, `articles/`,
`docs/Config`, `CHANGELOG`, `it-and-security`, `tools/mdm`, `.go` returns nothing).
