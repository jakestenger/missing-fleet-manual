# De-AI pass notes: 8.2 The log surfaces

Started 2026-08-21. Target: `manual/08-troubleshooting/8.2-log-surfaces.md`.
Baseline: 664 lines. Pointers read at `fleet-public main @ 2026-08-05 (d2fe9be461)`,
per the section's own frontmatter.

## Pre-flight checks (done)
- Em-dashes: 0. Banned vocabulary: 0 hits. HTML comments: 0. Existing `[term]()`: 0.
- Part VIII is the reference chapter: every table kept, **no diagram placeholders added**.

## Inbound anchors (frozen verbatim)
From `grep -rn "8.2-log-surfaces.md#" .`:
- `#822-fleetd-orbit-stdout-and-stderr` (8.4:187, 1.2:305)
- `#824-osquery-result-and-status-logs` (8.4:355)
- `#826-reading-fleetds-own-logs-without-shell-access` (8.4:442)
- `#827-the-rest-of-the-orbit-root-directory` (8.4:145, 1.2:225)
- `#8210-raising-verbosity-and-putting-it-back` (8.4:509)
- `#8211-server-side-log-destinations` (8.4:397)
- `#8212-what-survives-and-for-how-long` (8.4:615)

That locks 8.2.2, 8.2.4, 8.2.6, 8.2.7, 8.2.10, 8.2.11, 8.2.12. The five unlocked
headings (8.2.1, 8.2.3, 8.2.5, 8.2.8, 8.2.9) are all already positive, so **no
heading in the section was renamed and no inbound link needed updating.**
The section's own internal `[8.2.x](#...)` links are self-consistent and unchanged.

## Batch plan (save after each)
1. frontmatter, intro, 8.2.1, 8.2.2, 8.2.3
2. 8.2.4, 8.2.5, 8.2.6
3. 8.2.7
4. 8.2.8, 8.2.9
5. 8.2.10 (incl. the 4.89.2 fix)
6. 8.2.11, 8.2.12, See also
7. Recheck loop

## Citation conversion table

### Batch 1 (frontmatter, intro, 8.2.1, 8.2.2, 8.2.3) — done

| Fact retained in prose | Pointer removed | How the fact now reads |
|---|---|---|
| The two macOS Orbit paths are the LaunchDaemon's stdout/stderr redirects, written at package time | `articles/fleet-troubleshooting-for-it-admins.md`; `StandardOutPath` / `StandardErrorPath` in `orbit/pkg/packaging/macos_templates.go` | inline fleetdm.com/guides/fleet-troubleshooting-for-it-admins (already in `further_reading`) plus "the standard-output and standard-error redirects written into Orbit's LaunchDaemon plist at package time" |
| Windows-only rotation, driven by `--log-file`, at 25 MB / 3 backups / 28 days | MSI `--log-file` argument in `orbit/pkg/packaging/windows_templates.go`; `log-file` flag handling in `orbit/cmd/orbit/orbit.go` | "Windows is the one platform whose installer hands Orbit a `--log-file`, aimed at the path in the table above. Given a `--log-file`, Orbit rotates that file at 25 MB, keeping 3 backups for 28 days." |
| The "Collect fleetd logs" library script | `docs/scripts.yml` | Script name kept, path dropped. github.com/fleetdm/fleet/blob/main/docs/scripts.yml added to `further_reading` for readers who want the script body. |
| The `FleetDM` ETW provider and the `osquery` Event Log channel | `orbit/pkg/packaging/windows_templates.go` | Plain statement. Provider name, channel name and the five severities all kept. |

Other batch 1 changes:
- `verified_on` 2026-08-20 to 2026-08-21. `verified_against` (Fleet 4.90.0) and
  `verified_source` untouched. `sidebar_position: 2` untouched.
- `further_reading` gained fleetdm.com/guides/certificates-in-fleetd (8.2.7),
  github.com/fleetdm/fleet/tree/main/docs/solutions (8.2.10 toggle scripts), and
  github.com/fleetdm/fleet/blob/main/docs/scripts.yml (8.2.2).
- **ETW glossed in place**, not flagged: "an Event Tracing for Windows (ETW) provider".
- §15, 8.2.1: "Two traps live in that table ... people open the wrong one constantly" and
  "osquery's status log is **not** Orbit's log" to two positive statements of separateness.
  Both distinctions kept: STYLE §15 allows one explicit contrast where readers demonstrably
  get it wrong, and these are the two the section exists to settle.
- §15, 8.2.3: "depends on ... which fleetd does not set by default" to "fleetd's default list
  is `tls,filesystem`, so on a stock install the channel is registered and empty". The
  default is now stated rather than implied by an absence. "Not documented; read from the
  packaging template" to "Undocumented."
- "Rotation." to "Rotation is Windows-only." The brief lists Windows-only rotation as a
  finding to preserve; putting it in the bold label makes it scannable.
- **lumberjack removed** as a library name (internal identifier, §8). The three rotation
  values are unchanged everywhere they appear.
- "Truncate rather than delete if you need space, or Orbit keeps writing" to "... when you
  need the space back, because Orbit keeps writing". The old sentence read as a threat
  rather than a reason.

### Batch 2 (8.2.4, 8.2.5, 8.2.6) — done

| Fact retained in prose | Pointer removed | How the fact now reads |
|---|---|---|
| fleetd starts osqueryd with `--logger_plugin=tls,filesystem` and `--logger_path=<root-dir>/osquery_log`, so both destinations are live on a default install | `orbit/pkg/osquery/flags.go`; `WithLogPath` in `orbit/pkg/osquery/osquery.go`, called from `orbit/cmd/orbit/orbit.go` | "fleetd starts osqueryd with `--logger_plugin=tls,filesystem` and `--logger_path=<root-dir>/osquery_log`. Both destinations are active on a default install". Both flags kept verbatim. |
| `command_line_flags: {}` empties `osquery.flags` and restarts osquery; omitting the key leaves flags alone | `docs/Configuration/agent-configuration.md` | inline fleetdm.com/docs/configuration/agent-configuration (already in `further_reading`) |
| Fleet Desktop log directories per platform; rotation at 25 MB / 3 backups / 28 days; `fleet-desktop.err` truncated on every start | `articles/fleet-troubleshooting-for-it-admins.md`; `logDir()` and the lumberjack config in `orbit/cmd/desktop/desktop.go`; `os.O_TRUNC` in `setupStderr()` | inline fleetdm.com/guides/fleet-troubleshooting-for-it-admins for the directories; the truncation is now a plain bolded statement, closing with "Undocumented." |
| `fleetd_logs` columns, and that Orbit registers the table itself | `orbit/pkg/table/fleetd_logs/fleetd_logs.go`; `orbit/pkg/table/extension.go` | "Orbit registers the table through its own osquery extension, so it answers on hosts running fleetd and nowhere else", cross-linked to the `orbit-osquery.em` row in 8.2.7. Column list unchanged. |

Other batch 2 changes:
- **The blockquote correcting Fleet's own troubleshooting guide is preserved and
  strengthened.** It now carries the guide's URL and ends on a bolded sentence, "**The
  on-disk copy is there before you change any setting.**" That is the brief's first
  must-preserve finding, and it was the softest sentence in the section.
- The `fleetd_logs` constraint table is untouched, including the 10,000-entry capacity and
  the "**No.** The buffer is empty after a restart" row.
- §15: "is not the same as omitting it" to "behaves differently from omitting the key", split
  into two positive sentences; "It is useless for diagnosing a crash loop, because each
  restart wipes it" to "A crash loop is the one case it cannot cover, because every restart
  empties the buffer. Get the file instead."; "check every home directory, not just the one
  you are logged into" to "check every home directory on the machine".
- "**lumberjack**" removed again (§8, internal library name). Values unchanged.
- "If you are chasing a Desktop crash, copy `fleet-desktop.err`" to "When you are chasing ...
  copy `fleet-desktop.err` off the host". "Off the host" is the actual instruction: copying
  it in place does not survive the next start either.

### Batch 3 (8.2.7) — done

| Fact retained in prose | Pointer removed | How the fact now reads |
|---|---|---|
| The three Orbit roots, and the `/var/lib/orbit` symlink on Linux | `orbit/pkg/packaging/macos_templates.go`, `linux_shared.go` | plain statement; all three paths and the symlink unchanged |
| Every Orbit root filename | `orbit/pkg/constant/constant.go` and the packaging templates | Closing confirmation sentence deleted. Internal constant names `DesktopTokenFileName`, `OrbitNodeKeyFileName` and `OsqueryPidfile` dropped from three table cells (§8). Every filename in the table is unchanged. |
| `certs.pem` is the curl-derived public CA bundle, embedded in `fleetctl`, written at package time, passed as `--tls_server_certs` | `orbit/pkg/packaging/packaging.go`; `articles/certificates-in-fleetd.md` | inline fleetdm.com/guides/certificates-in-fleetd, now in `further_reading` |

Other batch 3 changes:
- **Every row of the 27-row artifact table is intact.** Spot-checked the brief's keep-list:
  `certs.pem`, `fleet.pem`, `identifier`, `osquery.db`, `secret.txt`,
  `secret-orbit-node-key.txt`, `update.pem`. Also kept `osquery.pid`, `fleet_client.crt/.key`,
  `update_client.crt/.key`, `hardware-uuid.txt`, `fleet_url.txt`, `server-overrides.json`,
  `mdm_migration.txt`, `setup_experience.json`, `host_identity.crt`,
  `host_identity_tpm.pem`, the three `bin/` paths, `osquery_log/`, `.inband_upgrade`,
  `osquery.flags`, `extensions.load`, `orbit-osquery.em` (and the Windows named pipe
  `\\.\pipe\orbit-osquery-extension`), `staging/`, `shell/`.
- `ORBIT_FLEET_CERTIFICATE` and `ORBIT_UPDATE_TLS_CERTIFICATE` **kept**: they are visible in
  the launchd plist, so they are reader-usable, not internal identifiers.
- **RocksDB glossed in place** on the `osquery.db` row, matching 8.4: "osquery's local store,
  an embedded RocksDB database".
- **TUF glossed in place** on the `update.pem` row: "a signed repository built on The Update
  Framework (TUF)". That row precedes the `staging/` row, so the later bare "TUF updater" now
  has an antecedent.
- "Why the shell cannot fight the service for the RocksDB lock" to "never contends with", to
  match the phrasing 8.4 landed on for the same fact.
- **The `cert.pem` trap was a 200-character unwrapped line** (a later insert) that said the
  same thing twice. Rewritten to three wrapped sentences ending on "**There is no
  `cert.pem`.**" The negative is the finding, so it stays; the brief and the 8.4 precedent
  both keep it.
- "These are not logs, but they answer identity and state questions faster than any log does"
  to "The files below answer identity and state questions faster than any log does" (§15).

### Batch 4 (8.2.8, 8.2.9) — done

| Fact retained in prose | Pointer removed | How the fact now reads |
|---|---|---|
| The `unified_log` / `mdmclient` live query, and the local `log show` / `log stream` equivalents | `articles/fleet-troubleshooting-for-it-admins.md` | "Fleet publishes this query at fleetdm.com/guides/fleet-troubleshooting-for-it-admins". The SQL block keeps `process`, `subsystem`, `category`, `level`, `message`, `timestamp` and the `(SELECT unix_time - 3600 FROM time)` bound; `fleetctl report --hosts ... --exit --query` block untouched. |
| The eight-step iOS/iPadOS sysdiagnose procedure and the `log show --archive` follow-up | `articles/fleet-troubleshooting-for-it-admins.md` | "Fleet documents this procedure at fleetdm.com/guides/fleet-troubleshooting-for-it-admins". All eight steps verbatim, including the button combination, the Analytics Data path, the `sysdiag` search string, `system_logs.logarchive` and Console. |

Other batch 4 changes:
- **unified log glossed in place**, not flagged: "the unified log, the system-wide log store
  behind Console and `log show`". Flagging would have been odd when the section's next code
  block is `log show`.
- **sysdiagnose glossed in place**, not flagged: "a sysdiagnose, Apple's on-demand diagnostic
  archive".
- §15: "There is no agent on iOS and iPadOS, so there is no remote log pull. The device owner
  has to generate..." to "iOS and iPadOS run no agent, so every log pull goes through the
  device owner. They generate..."; "This section only gets you the bytes" to "Getting the
  bytes is this section's job"; "Bound the window or the query is slow and enormous" to
  "Bound the time window: unbounded, the query is slow and the result is enormous" (the old
  sentence made the query enormous rather than the result).
- "You can pull it remotely, without shell access, with a live query" to "A live query against
  the `unified_log` table pulls it remotely, with no shell access on the device."
- Kept "Ask for the sysdiagnose **immediately after** reproducing the failure" and the
  aged-out-window warning. Both are actionable.
- Note `max_rows` does not appear in this section's `unified_log` query; the window is bounded
  by timestamp instead. See "Findings reported, not changed" below.

### Batch 5 (8.2.10, including the version fix) — done

| Fact retained in prose | Pointer removed | How the fact now reads |
|---|---|---|
| `--debug` lands as `ORBIT_DEBUG` in the launchd plist, `--debug` in the Windows service `ImagePath`, `ORBIT_DEBUG=true` in `/etc/default/orbit` | `orbit/pkg/packaging/macos_templates.go`, `windows_templates.go`, `linux_shared.go`; `articles/fleet-troubleshooting-for-it-admins.md` | plain statement, all three artifacts kept, plus inline fleetdm.com/guides/fleet-troubleshooting-for-it-admins |
| Both toggle scripts, and where to fetch them | in-repo `docs/solutions/...` paths | **Paths kept** (the reader has to fetch the script) and given a real URL: github.com/fleetdm/fleet/tree/main/docs/solutions, added to `further_reading`. Same call 8.4 and 8.14 made. |
| The Windows service name `Fleet osquery` | `SystemServiceName` in `orbit/pkg/constant/constant.go` | "The service name is `Fleet osquery`." |
| Linux debug via `EnvironmentFile=/etc/default/orbit` | `orbit/pkg/packaging/linux_shared.go` | "Orbit's systemd unit carries `EnvironmentFile=/etc/default/orbit`, which makes the equivalent two commands and their reverse". Closes with "Undocumented." |
| `command_line_flags` take effect on fleetd restart | `docs/Configuration/agent-configuration.md` | inline fleetdm.com/docs/configuration/agent-configuration |
| The `orbit.debug_logging` block, the per-host debug-logging endpoint, and `debug_logging_on_enroll_duration` | `docs/Configuration/agent-configuration.md` | inline fleetdm.com/docs/configuration/agent-configuration. All values kept: default 24h, max 7d, max `86400`, `--verbose`, `--tls_dump`, `POST /api/v1/fleet/hosts/:id/debug-logging`. |

**The 4.89.2 fix.** The `orbit.debug_logging` paragraph read: 'marked **"Coming soon"** in the
4.89.2 docs. Treat availability on 4.89.2 as unverified'. Per the brief, 4.89.2 there was a
CHANGELOG-derived stamp from a tree that lagged the code actually read (post-4.90.0). It now
reads 'carries a **"Coming soon"** marker in the 4.90.0 docs, so treat availability as
unverified', matching the section's own `verified_against: Fleet 4.90.0`. **4.89.2 appears
nowhere else in the section**, so nothing that names the real release was touched.

Other batch 5 changes:
- All five verbosity levers and the whole lever table are intact: `fleetctl package --debug`,
  `toggle-fleetd-debug.sh`, `toggle-fleetd-debug.ps1`, `ORBIT_DEBUG=true` in
  `/etc/default/orbit`, `command_line_flags: {verbose: true}`, each with its off switch.
  `/tmp/orbit_debug_script_logs.txt`, the `PlistBuddy` block, the `launchctl bootout` /
  `bootstrap` pair, the `Get-ItemProperty` check and the `sed -i` removal all kept.
- **lumberjack, third instance**: none left in this section.
- §15: "There is no Fleet-supplied toggle script for Linux" to "Linux has no supplied script";
  "Not documented; inferred from the packaging source" to "Undocumented"; "If the toggle
  appears not to have worked" to "When the toggle looks like it did nothing"; "so it proves
  osquery behavior but not Fleet's configuration of it" to "What it proves is osquery
  behavior. Fleet's configuration of osquery stays a separate question" (the 8.4 phrasing for
  the same fact).
- "This is deliberate:" to "and that delay is load-bearing", matching 8.4's label for the same
  15-second sleep.
- The `debug_logging` paragraph was one 8-line sentence with three parenthetical asides.
  Rebroken into four sentences, one per control. No value changed.
- Kept "run it as a script from Fleet only if you can tolerate losing the script result": the
  "only" is the condition, not a hedge.

### Batch 6 (8.2.11, 8.2.12, See also) — done

| Fact retained in prose | Pointer removed | How the fact now reads |
|---|---|---|
| The three stream settings, their env vars, their defaults, and the 5-minute audit delay | `docs/Configuration/fleet-server-configuration.md` | "All three settings are in Fleet's server configuration reference (fleetdm.com/docs/configuration/fleet-server-configuration)". Table untouched. |
| Per-destination size behavior at the boundary | `articles/log-destinations.md` and `docs/Configuration/fleet-server-configuration.md` | "Destination behavior is documented at fleetdm.com/guides/log-destinations and fleetdm.com/docs/configuration/fleet-server-configuration." Both URLs were already in `further_reading`. |
| `nats` is a valid plugin the log destinations guide skips | `log-destinations.md` filename | "Absent from Fleet's log destinations guide, listed as a valid option in the server configuration reference" |

Other batch 6 changes:
- **The three-streams finding is intact**, heading and table: results, status and audit each
  with their own plugin setting, env vars and default. So is the "and each can land somewhere
  different from the other two" statement.
- **The Redis finding is intact and promoted to bold**: "**Fleet's recorded server errors live
  in Redis rather than in a file.**" It kept the `logging_error_retention_period` TTL, the
  `fleetctl debug errors` command, and the 8.5 pointer. The 24h default also stays in both the
  `logging_*` table and the 8.2.12 survival table.
- **The webhook caveat is intact**: result logs only, own config section, outside the
  enumerated option list. All ten destination names kept.
- **journald glossed in place** in the 8.2.2 Linux row: "or journald, systemd's own log store,
  read with `journalctl -u orbit`". That gives the bare "syslog/journald" cell in 8.2.12 an
  antecedent. All three Linux paths kept.
- **HEC glossed in place** by expanding the `splunk` row to "Splunk HTTP Event Collector
  (HEC)", which is what the `your-hec-token` placeholder in the YAML below refers to.
- Kept verbatim: "Snowflake is not a plugin", the multi-node load-balancing trap, the whole
  `filesystem` settings table with its nine rows and defaults, and both production YAML blocks.
- §15: "The rotation settings only have effect when ... which it is not by default" to "take
  effect when `filesystem_enable_log_rotation` is `true`, and it is `false` by default";
  "A production deployment should set explicit paths" to "sets explicit paths"; "Distinct from
  all three streams above" to "A fourth stream, separate from the three above"; "Bounded recent
  window only" to "Bounded recent window"; "the ephemeral surfaces evaporate on restart" to
  "are gone after a restart" (evaporate was a near-miss metaphor for a file being truncated).
- `[!internal]` note rewritten positively: "Managed-cloud customers cannot change log
  destination config themselves. Only self-hosted deployments can" to "Log destination config
  is a self-hosted lever. On managed cloud the change goes through Fleet." Substance unchanged.
- **The collect-before-restart finding is intact**, naming `fleetd_logs`, `fleet-desktop.err`
  and the unified log, and so is the `osquery.db`-replays-old-timestamps consequence.

### Polish / de-AI recheck — done

- "Two pairs of rows in that table get mistaken for each other constantly" to "Two
  distinctions in that table get missed constantly". The second item is Orbit versus osquery,
  which is not a pair of rows.
- 8.2.6: my first replacement added an inference Orbit's registration does not strictly carry
  ("so it answers on hosts running fleetd and nowhere else"). Trimmed back to the grounded
  part plus the 8.2.7 cross-link.
- 8.2.5: "Undocumented." was sitting after a paragraph that is mostly documented. Now "The
  `.err` file is undocumented."
- "Bound the time window: unbounded, ..." to two sentences; the colon made the clause read as
  a definition.
- 8.2.4: "Fleet's docs name the directory, not the filenames; `ls` the directory rather than
  assuming a name" to "name the directory rather than the filenames, so `ls` it rather than
  assuming a name".
- Long-line check: the only lines over 92 columns are three real commands inside code fences
  (the Windows `Get-Content`, `Get-WinEvent`, and `Get-ItemProperty` one-liners). Left as is.
- Meaning-bearing "only"/"just" audited one by one and kept: "Present only on mTLS
  deployments", "Orbit passes the flag only when this file exists and is non-empty", "used only
  by `orbit shell`", "Only on `--use-system-configuration` packages", "Result logs only",
  "run it as a script from Fleet only if you can tolerate losing the script result". Removed
  from six places (listed above).

## Preserved deliberately (against the general de-AI instinct)

- **Every table, every row, every path.** Part VIII is the reference chapter, and this section
  is the path index other sections route to. **No diagram placeholders added.**
- All seven inbound anchor targets, verbatim. **No heading in the section was renamed**, so no
  inbound link in 8.4 or 1.2 needed updating.
- The blockquote correcting Fleet's own troubleshooting guide about `logger_path` versus
  `logger_plugin`, now ending on "**The on-disk copy is there before you change any setting.**"
- "**There is no `cert.pem`.**" (8.4 precedent, and the brief.)
- "A watchdog kill or a denied table shows up in status, never in result." The explicit
  contrast is the mistake the section exists to fix (§15's one-sentence allowance).
- "Snowflake is not a plugin." Reader-correcting negative.
- "External destinations | ... | Fleet does not retain a copy." The absence is the fact.
- "Linux has no supplied script." Reworded from "There is no Fleet-supplied toggle script for
  Linux", but the absence is kept because the reader would otherwise go looking.
- "**Truncated on every Desktop start**" and "lost on Orbit restart", in prose and in the
  8.2.12 table both.

## Findings reported, not changed

1. **`max_rows` is on the brief's keep-list but does not appear in the section.** The
   `unified_log` query bounds its window with `timestamp > (SELECT unix_time - 3600 FROM time)`
   instead, and the prose explains how to move that constant. Nothing to preserve, and nothing
   added: adding a `max_rows` constraint would be new writing needing verification. Same call
   8.4 made for `dsregcmd /status`.
2. **Frontmatter `verified_source` names a commit on `main`, not a release tag.** It reads
   `fleet-public main @ 2026-08-05 (d2fe9be461); does NOT include 4.90.1 fixes`, which is
   exactly the pattern STYLE §9 warns against ("a commit hash pins to something no reader can
   install"), and it disagrees with the brief's statement that facts were verified at tag
   `fleet-v4.90.1`. Left untouched per instruction. Worth reconciling across all of Part VIII
   rather than section by section.
3. **`setup_experience.json` in the 8.2.7 table has an empty "what its absence or contents
   tell you" cell.** Left empty rather than invented.
4. **8.2.3 and 8.2.4 now agree explicitly.** 8.2.3 used to say fleetd "does not set"
   `windows_event_log` by default; it now states the default list as `tls,filesystem`, which is
   the same string 8.2.4 gives. That was an implicit agreement before and is now checkable.

## Line count
664 before, 673 after. The section grew by 9 lines: 3 are new `further_reading` URLs, and the
rest is rewrapping where a converted citation runs longer than the file path it replaced. No
table row and no path was cut.

Citations: 24 in-repo pointers removed (16 Go files plus 8 `docs/` and `articles/` paths),
0 remaining. `grep -cE "\.go\b|orbit/pkg|orbit/cmd|cmd/fleetctl|schema/|articles/|docs/Config|CHANGELOG|it-and-security|lumberjack"` returns 0.
