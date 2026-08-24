# Refocus pass notes — 1.2 and 1.3

Scope clarification applied: Part VIII owns all troubleshooting content (procedures **and**
reference tables). Feature sections cover design and use. Target shape is
`manual/01-foundations/1.4-server-state.md`.

Started 2026-08-20.

## Order of work

1. 1.2 completely, saved.
2. Then 1.3.

## Pre-flight survey (both sections)

Checked what Part VIII already owns before deleting anything from 1.2:

| 1.2 content | Already in Part VIII? | Action |
|---|---|---|
| Orbit root file inventory (30 rows) | Yes, 8.2.7 (nearly complete) and 8.4.3 (diagnostic subset) | Cut from 1.2, link. 5 missing rows appended to 8.2.7. |
| Per-platform service management commands | Yes, 8.4.2 (incl. `CPUQuota=20%`, launchd throttle, `sc.exe`/`PathName`) | Compress in 1.2 to a design table. |
| Five channels table | Yes, 8.1.4 | Keep in 1.2: it is the design spine of the section, and 1.2 is where the cadences and the flag detail belong. |
| Channel isolation sweep, half-enrolled detection | Yes, 8.1.4 and 8.4.5 | Cut from 1.2, pointer only. |
| `orbit shell` as an isolation tool | Yes, 8.4.7 | Cut from 1.2, pointer only. |
| osquery introspection (`orbit_info`, `osquery_flags`) | Yes, 8.4.6 | Cut from 1.2, pointer only. |
| **TUF / agent-update narrowing** (channel dir vs `orbit_info`, `tuf: file not found`, 24h cooldown, downgrade loop, update-debug repro) | **No. Gap.** | **Moved into a new 8.4.12.** |
| `bin/<target>/<platform>/<channel>` target table | No | **Moved into 8.4.12.** |

---

## 1.2 Anatomy — DONE (saved)

**842 lines to 682. Table lines 176 to 136 (104 data rows across 16 tables).**
Frontmatter already carried `status: drafting` and `verified_on: 2026-08-20`; unchanged.

### Moved into Part VIII (nothing discarded)

| Content | New home | Why |
|---|---|---|
| The `bin/<target>/<platform>/<channel>` target table (platform strings, archive names, extracted executables) | **new 8.4.12** | Not present anywhere in Part VIII. It is what you read to answer "which channel actually landed". |
| The three on-disk channel states (`tuf: file not found`, `max retries exceeded` cooldown, restart-not-fired, downgrade-loop flapping) | **new 8.4.12** | This was 1.2's "third cut" narrowing block. Part VIII had no agent-update diagnosis at all. |
| Update retry policy: 3 attempts then 24h cooldown keyed by content hash; startup fetch retries forever at 5 min | **new 8.4.12** | Was an edge case in 1.2; kept there in one compressed paragraph that points at 8.4.12 for the mechanics. |
| Corrupt-target health check and self-heal | **new 8.4.12** | Same. |
| Expired TUF role behaviour, Orbit 1.38.1 TUF-server-move floor | **new 8.4.12** | Same. |
| Update-check reproduction (`--update-interval` short, `--debug`, `hash(<target>)=` lines, startup random offset) | **new 8.4.12** | Reproduction is Part VIII's job. |
| `osquery.flags`, `extensions.load`, `orbit-osquery.em` socket, `staging/`, `shell/` | **5 new rows in 8.2.7** | The only Orbit-root entries 1.2 listed that 8.2.7 lacked. |

8.4 also gained an index row in 8.4.1 pointing at 8.4.12. 8.4: 646 to 726 lines.
8.2: 658 to 663 lines. No renumbering anywhere; 8.4.12 is append-only after 8.4.11.

### Cut without moving (already covered in Part VIII, now a link)

- Orbit root file inventory, 30 rows: 8.2.7 has all of it. 1.2 keeps four design paragraphs
  (two CA files and why, enroll secret leaving disk, RocksDB durability, channels as
  directories).
- Per-platform service commands, launchd/systemd/SCM detail, the full systemd unit: 8.4.2.
  Replaced by a four-column design table (supervisor, unit, **where configuration is read
  from**, restart policy, resource cap) plus the three notes that are decisions rather than
  commands.
- The 85-line "Troubleshooting this component" block: now 16 lines, an 8-row pointer table
  naming 8.1, 8.2, 8.4, 8.4.5, 8.4.12, 8.5, 8.7, 8.8/8.9/8.10.
- `orbit shell` / `orbit_info` / `osquery_flags` procedure: 8.4.6 and 8.4.7.

### Compressed rather than cut

- The 17-line osqueryd flag dump became a 5-row endpoint table, keeping the two flags with
  consequences beyond their endpoint (`logger_plugin=tls,filesystem`, `tls_accept_gzip`).
- The 16-row Orbit endpoint list became a 7-row table grouped by job.
- The 13-row receiver table became 8 rows grouped by throttle.

### Added

**"What the split and the channels let you do"** (79 lines, 5 subsections):
agent delivery and MDM enrolment as two separate projects (with a what-you-get matrix);
the channel deciding what you check first; channels as the agent release-management tool
(canary on `edge`, pin to a literal version, roll back without repackaging, plus the two
traps); what only Fleet Desktop can do and what it costs; and how the plan changes where
there is no agent.

### Judgement calls

- **Kept the full edge-case register (93 lines).** `STYLE.md` §4 assigns conflicts,
  ordering, offline, retry, interruption, and limits to the feature chapter, and these are
  design behaviour rather than "what do I run". Five TUF-failure entries were compressed to
  one paragraph because 8.4.12 now owns their mechanics.
- **Kept "Setting it up" (about 70 lines).** Packaging is neither troubleshooting nor
  duplicated in Part VIII, and 2.1 and 2.6 do not exist yet, so there is nowhere else for
  it. This is the main reason 1.2 lands at 682 rather than inside 650.
- Kept the "where there is no agent at all" comparison table, as instructed.

---

## 1.3 Hosts, fleets, and labels — DONE (saved)

**1130 lines to 763. Table lines 165 to 144.**
Frontmatter already carried `status: drafting` and `verified_on: 2026-08-20`; unchanged.

### Moved into Part VIII (nothing discarded)

Part VIII had **no coverage of scoping state at all**. 8.6 mentioned `label_membership`
zero times and `hosts.team_id` zero times, while 1.3's troubleshooting section was pointing
readers at 8.6 for exactly those. That was the largest gap this pass found.

| Content | New home | Why |
|---|---|---|
| Which table answers which scoping question (`hosts.team_id`, `label_updated_at`, `label_membership`, `labels`, the six label join tables and their `exclude`/`require_all` pair, `cron_stats`) | **new 8.6.13** | The reference half of "was this host targeted", absent from Part VIII |
| The joined host-plus-labels query, and the `<=>` warning for hand-written scoping queries | **new 8.6.13** | |
| The three-cut narrowing: fleet or label, member versus believed-not-member, then split a population by membership type | **new 8.6.13** | This was 1.3's 83-line troubleshooting subsection |
| `refetch_requested` as the way to force a label refresh, and the one-host manual-label minimal case | **new 8.6.13** | Reproduction is Part VIII's job |
| Five server log strings: duplicate-identifier WARN, the TPM host-identity refusal, `enrolling too often`, `expected 4 builtin labels but got N`, and the `deprecated_path` / `deprecation_warning` pair | **5 new rows in 8.3.6** | 8.3.6 is the error-string register and had none of them |

8.1.5's class 1 row ("Not targeted") now points at 8.6.13 instead of at §8.1.6, so the new
subsection is reachable from the diagnostic method. 8.6: 1031 to 1111 lines.
8.3: 429 to 435 lines. No renumbering; 8.6.13 is append-only after 8.6.12.

### Compressed rather than cut

- The `renameto` alias-layer mechanism: 96 lines to 35. The surface table (which word each
  API, CLI, and YAML surface wants) is the artifact a reader needs; the walkthrough of
  `DuplicateJSONKeys`, the 47-entry path alias table, and the GitOps validator is now four
  sentences that keep every fact.
- Multiple packages per title: 60 lines to 14, keeping only the label-scope tiering and the
  display-only fallback, with the package limits and hash rules pointed at 4.3.
- Host transfer: 84 to 49, keeping the seven-step table intact because that table **is** the
  answer to "what did I lose", and compressing the service-layer narrative.
- The dynamic-label pipeline, the host vitals cron, built-in labels, and the storage and
  evaluation subsections were each tightened without dropping a claim.

### Added

**"Structuring scope for a real organisation"** (84 lines, 6 subsections): the one question
that decides fleet versus label; four axes (platform, department, rollout stage,
environment) and what each wants; when a label beats another fleet; when it does not (the
four fleet-only capabilities, RBAC, and the label-latency argument); what the no-fleet
bucket is good for and why it is a bad baseline; and what host transfer is for against what
it costs. All of it grounded in mechanics already verified in the section.

### Judgement calls

- **1.3 lands at 763, above the 700 line.** The remaining bulk is not troubleshooting and
  not duplicated in Part VIII. It is three topics in one section: host identity (80 lines),
  fleets (55), labels (120), plus targeting semantics (60) and a 210-line edge-case register
  that `STYLE.md` §4 assigns to the feature chapter. The three blocks that could legitimately
  leave are **host identity and enrollment matching** (2.1's topic), **multi-package
  resolution** (4.3's), and **the GitOps label rules** (7.1's). None of those files exist
  yet, and the brief scopes relocation to Part VIII, so the material stayed. Revisit when
  2.1, 4.3, and 7.1 are written.
- Kept the include/exclude semantics, the two-boolean storage table, and the exclude-any
  trust guard in full, as instructed.
- Kept the `matchHostDuringEnrollment` priority table: it is the only place the book explains
  why an ADE Mac with a custom `--host_identifier` enrolls as a second host record.

### Noticed, not chased

`manual/01-foundations/1.4-server-state.md` has a broken in-file anchor:
`#object-storage-is-not-optional-in-production` does not match any heading in that file
(the heading is "Object storage is for bytes, not rows"). Pre-existing, not touched by this
pass.
