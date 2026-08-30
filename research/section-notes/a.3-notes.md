---
section: "A.3"
---

# a.3 Configuration sources, scopes, and precedence, citation ledger

Drafted 2026-08-29 after **three research rounds**, all of which returned NOT SOUND, plus a
normalisation pass. Held to Part IX's evidence rule ([`../appendix-structure.md`](../appendix-structure.md)).

Per-source and per-consumer citations are outside this repository, in
`../../missing-fleet-manual-private/research-sensitive/`: `a.3-scratch-core.md` for the server side,
`a.3-scratch-hostside.md` for the host side, `a.3-scratch-resolution.md` for the first resolution
model and `a.3-scratch-normalised.md` for the corrected one.

## The finding that shaped the appendix, and the two models it replaced

**Round 1** produced a layered model and was refused for treating a writer as an authority.

**Round 2** produced eight host-side authorities in a **single ranked chain**, with "later beats
earlier where they overlap". **Round 3 refused that too, and was right**: an overlap is not one
relation. It can be precedence, fallback, write-through, composition, mutual exclusion, or a channel
being removed so that nothing is compared at all. There is a confirmed instance of each, and a single
path routinely uses three or four.

**So the appendix carries a catalogue plus per-consumer resolution**, never one order. The counts,
which the appendix deliberately does not lead with: **18 sources, 18 numbered resolution points, of
which 16 arbitrate and 2 are single-authority reads.**

## Established at the tag

| Claim | Note |
|---|---|
| Within the server's process configuration: flags, then environment, then file, then defaults, **as Fleet itself states in its configuration-dump help text** | The one place a simple order holds. **The "empty environment variables ignored" half was withdrawn at draft review 2**: it came from the configuration library, which this release does not vendor, and no test in the checkout pins it |
| Mounted secret and secret-manager values are read **once** and never re-read | Changing the file under a running server does nothing |
| **The device-management asset store outranks the process configuration after first boot** | Added at the normalisation pass; its absence was why one consumer looked one-sided |
| Fleet **warns rather than refuses** when configuration-supplied certificates are being ignored | The startup log says so; nothing enforces it. **Narrowed at draft review 2**: true of the push certificate, the SCEP certificate and the ABM material. **The SCEP enrollment challenge warns on no ordinary boot at all** |
| **The Apple Business Manager token file is parsed on every boot before the store is consulted** | A broken path stays fatal even when the parsed value is discarded |
| The macOS profile sets the Fleet URL and enrol secret unconditionally, **and the comment above it describes a guard the code does not have** | Verified independently at round 2 and again at round 3 |
| Disabling updates removes the receiver, so the last persisted override is permanent | Which narrows C29: the `stable` defect holds only while the receiver is enabled |
| osquery agent options take the fleet's document whole or the global one, never a mix. Platform overrides replace | Already carried by 1.3 |
| The Orbit half has no fallback except the script execution timeout, whose condition tests zero | |
| A locally set debug flag is a floor the server cannot lower; the profile may enable scripts and cannot disable them | Compositions, not precedence |
| GitOps: YARA rules cleared, certificate authorities cleared **through a queued second pass with deletion enabled**, conditional access left alone, expiry blocks left alone | The certificate-authority route was the last field established |
| The server replaces four blocks wholesale on any spec apply, so omitting single sign-on clears it | **The rule is the writer, not the field** |
| Nine keys survive omission | Corrected from "three", which contradicted the file's own table |
| The organisation settings document is **audited by exception**, with no document-level fallback. **42 distinct activity types are reachable from a modification**, corrected at draft review 1 from "42 changes each writing one" | SMTP, server URL and host expiry confirmed to write nothing. Enrolment secrets are outside the set. Three of the 42 are best effort |
| **No *complete* surface reports the running server's effective configuration.** The configuration dump starts a new process | Replaced the provenance row that had claimed otherwise. **Corrected at draft review 2**: the unqualified "no surface" was an over-correction. The configuration API exposes a live subset, roughly 20 of the 320 keys, readable by any authenticated role |
| Fleet asks for a configuration hash **on each detail cycle** and discards it | Narrowed at round 3 from "every poll", and **narrowed again at draft review 1 from "every host"**: it is an osquery detail-query mechanism, so iOS, iPadOS and Android hosts never contribute it |
| 320 keys registered by the configuration manager | Independently reproduced by the reviewer |

## Four reference discrepancies, published

A per-endpoint request-size override documented in full and **bound nowhere**; the Redis host-cache
lifetime documented as 60 seconds and registered as 180; the MySQL password documented as defaulting
to `fleet` and registering empty; and the private-key external identifier documented under an
environment variable the server does not read. All four are in the defect queue as D32 to D35.

## Not established, and deliberately not published

**How many of the 320 registered keys Fleet documents.** An earlier draft published 232 documented
and 93 undocumented. **The reviewer refused both**, because "documented" had not been defined
consistently: a setting may have its own reference section, be described in prose under another, or
appear only in an example, and the three counts differ. The appendix states the registered count,
which is derived, and declines the comparison until it can be produced by a reproducible parse. **No
Go toolchain is available on this machine**, which is what blocks that.

**Two GitOps fields** were open at round 3 and were settled by the reviewer directly; both are in the
table above.

## Corrections this research forced into finished chapters

| Chapter | What changed |
|---|---|
| **1.3** | The agent-options inheritance row, which was true of one case and false of the other, and had already been corrected once |
| **2.4** | A fleet cannot opt out of host expiry, only change its window. And the count of reference disagreements, twice: raised to seven, then withdrawn entirely as underived |
| **6.2** | The GitOps agent-options row, wrong in both of its last two cells |
| **5.2** | **Rotating a secret redelivers nothing.** Filed as C28 |
| **8.11** | Remote flags overwrite the local flagfile rather than losing to it |
| **1.5, 8.12** | The audit trail is by exception, not complete |

## Rounds

| Round | Verdict | Outcome |
|---|---|---|
| Research 1 | NOT SOUND, ten items | Host side entirely unchased |
| Research 2 | NOT SOUND, seven items | Eight authorities established; the ranked chain proposed |
| Research 3 | NOT SOUND, seven items | The chain refused; six mechanisms established |
| Normalisation | Applied | Units defined, counts restated, the asset store added, the provenance row replaced |
| Draft correction | Applied | Six claims in the draft that the normalisation made wrong, corrected in the appendix and listed below |
| Draft review 1 | **NOT READY**, five findings | Applied in full, 2026-08-29. Coverage gap closed, 2,921 to 7,939 words. Three of my own unverified claims withdrawn, the activity restatement repaired, five scope overreaches corrected. §"Draft review 1" below |
| Draft review 2 | **NOT READY**, twelve findings | Applied in full, 2026-08-29, to 9,868 words. **Three of the twelve were the round 1 corrections committing the same defect again**, recorded separately below. Two were the provenance rule, one was an over-correction to undo, six were ordinary. §"Draft review 2" below |

## The recursion, which is the most useful thing this appendix has taught the project

**Round 1 named this appendix's characteristic failure as the class-versus-member claim, and replaced five of them. Round 2 found that three of the replacements were themselves class-versus-member claims.** Not the same sentences returning: new sentences, written specifically to fix that defect, exhibiting it again.

| The round 1 correction | What round 2 found |
|---|---|
| "Windows maps every success straight to `verified`, and nothing re-checks it" | True of ordinary profiles. A profile whose certificate Fleet brokered is deliberately held at `verifying` and advanced only when the issued certificate is observed. **Windows reaches all four states** |
| "Apple profiles rest at `verifying` after acknowledgement" | True of the command-status mapper. The datastore then promotes an iPhone or iPad install straight to `verified`, and declarative profiles record `verified` directly. **The mapper is not the whole path** |
| "A failed push is deliberately treated as success, and an inactive token turns device management off" | True of specific callers. Profile delivery swallows the error; device lock returns it. Inactive-token handling fires only in the scheduled mobile refetch. **Both are caller-scoped, not class-wide** |

**Why the fix failed the first time.** Each round 1 correction was verified, and verified correctly, against *one* implementation: the mapper, the ordinary-profile path, the profile processor. Confirming a source says X is not the same as establishing that X has no siblings, and the verification step as practised answers only the first. The correction then reads as authoritative precisely because it was checked.

**The rule this produces, and it is now a drafting rule rather than a review finding.** Before writing a sentence about how Fleet handles something, **find the second caller.** Where a behaviour is reached through a mapper, a helper or a shared processor, ask which other callers reach it and whether they agree. Where they disagree, **the sentence carries the distinction rather than picking the majority**, and it names the caller or the class each branch belongs to. A sentence that cannot name what it is true of is not finished.

**The tell to look for in a draft**, since this defect survives source-checking: a confident universal about a platform, a plane or an operation, with no clause naming what it excludes. Round 2's three findings all had that shape, and so did round 1's five.

## The six claims the normalisation made wrong, and what replaced them

Recorded because five of the six were claims about **scope**, not about behaviour: each said of a
whole class what was true of one member. That is this appendix's characteristic failure, and the
next reviewer should look for it first.

| The draft said | It is actually |
|---|---|
| The server replaces four blocks wholesale whenever a spec is applied, whatever applied it | A request option on the organisation settings route. **The GitOps client is the only thing in Fleet that sets it**, and `fleetctl apply` does not. Any caller who can write organisation settings can set it |
| The ordinary API preserves what you omit | True of the organisation settings patch, **false of the fleet spec path**, which resets or clears several fields |
| Reading the host is the only method, and it has to be a live query | A live query reaches **the osquery half only**. Update channels, extensions, debug state and script behaviour each need their own host-side observation, so host-side per-consumer observation is the complete method |
| Fleet settings retain the file name a GitOps run recorded, and nothing else | Activity rows retain actors for the changes Fleet names. The file name is the only writer marker **stored on the settings row itself** |
| Two sources meeting produce one of six outcomes | Six **observed mechanisms** which co-occur. Credential resolution alone uses three |
| Around forty specific changes write their own activity | **Corrected again at draft review 1, because the restatement was itself wrong.** It is 42 distinct activity **types reachable from** organisation-settings modification, not 42 changes each writing one. Enrolment secrets sit outside the set, on their own route. Three of the 42 are best effort. Nine are also emitted elsewhere |

**One claim held on re-examination and is worth saying so:** the server-process provenance row. The
configuration dump starts a new process and dumps what that process loads, so it is neither
introspection of the running server nor necessarily equal to what is in force, and it omits every
setting read directly from the environment. The draft already said this.

## What the draft gained rather than corrected

> **ALL THREE ENTRIES BELOW WERE WRONG AND ARE SUPERSEDED BY DRAFT REVIEW 1.** They are kept in place
> rather than deleted, because they are the record of how the defect entered: all three were added to
> the draft on a researcher's summary without being read at the tag, which is the exact failure this
> project exists to catch. The corrected versions are in §"Draft review 1" below.

**The enforcement plane**, which had been one table row. ~~The device reports are not equivalent across
platforms: **Android holds four states and publishes only the first and the last**, so a device
part-way through enforcement is indistinguishable through any API from one that has not started.
Apple and Windows have no separate acceptance state for a policy provider~~. **Wrong twice.** Android
exposes derived per-profile progress through the ordinary API, and Apple and Windows do not have the
same acceptance report. The half that survives is that neither Apple nor Windows has a separate
external policy-provider tier. A third-party management provider contributes device-reported
observation only, which stands.

~~**Apple push responses are inspected and never persisted.** Which is why a command that never
arrived looks afterwards exactly like one that was never sent.~~ **The first clause is right about the
raw response and wrong about everything around it.** The command is persisted before the push, a
failed push leaves that enqueued record, and an inactive-token response turns MDM off for the host
and writes activities.

~~**Two host-side counts** that bound how much of a host's configuration is reachable at all: twelve
settings supplied by environment variable at packaging time and at no other moment, and twenty-eight
of the agent's twenty-nine command-line settings overridable by the server.~~ **Both counts are real
numbers attached to the wrong claims.** 28 of 29 is environment-variable availability on the host,
not server override; the server's reach is three update channels. The twelve are `fleetctl package`
inputs, five of them packaging or signing rather than agent settings, and the other seven all have
runtime forms too, so "at no other moment" is false for every one of them.

## Draft review 1

Independent review, 2026-08-28, verdict **NOT READY**, five findings. Transcript at
`../../missing-fleet-manual-private/reviews/2026-08-28/appendices/a.3-sol-r1.out`. Every finding was
re-verified against `dd0200f062` before applying; nothing was taken on the reviewer's authority.

**Finding 1, coverage.** The appendix was 2,921 words against a contract of "every configuration
authority, scope, ownership boundary, precedence rule, and every verified exception". Ten omissions,
all added:

| Added | Key citations |
|---|---|
| Host-side authority table, replacing a prose list that miscounted and included the server as a host authority | `orbit/cmd/orbit/orbit.go:1407`, `:1413`–`:1424`; writers vs rows per normalised §1 |
| Trailing osquery arguments, appended last, beating the flagfile and the two protected options | `orbit/cmd/orbit/orbit.go:1422`–`:1424` |
| Direct agent environment reads, outside the CLI binding path | `orbit/pkg/logging/logging.go:22`, `orbit/pkg/scripts/scripts.go:97` |
| Process-config mutual exclusions: `_path`/`_bytes` (MDM material only), `mysql.password`, `server.private_key` vs `_arn` | `server/config/config.go:1018`–`:1030`, `:185`–`:192` |
| Cross-plane precedence: vulnerability database path (process wins, **and its default is non-empty**, so the stored key is inert on an untouched server), transparency URL (licence-conditional) | `cmd/fleet/vuln_process.go:136`–`:150`, `server/config/config.go:1713`; `server/service/devices.go:648`–`:657` |
| Cross-plane preconditions: disk encryption needs `server.private_key`; custom disk-encryption payloads need an OR of three process keys | `server/service/appconfig.go:765`–`:769`; `server/config/config.go:958`–`:960`, `server/service/apple_mdm.go:484`, `server/service/windows_mdm_profiles.go:103` |
| Full semantics of both document writers, including six org-settings fields that defeat the patch and four server-owned fields silently ignored | `server/service/appconfig.go:528`, `:537`–`:547`, `:667`; `ee/server/service/teams.go:1748`–`:1990` |
| Per-host debug-window merge: `verbose` added **only when absent**, so an explicit `false` defeats the window silently | `server/service/orbit.go:457`–`:478` |
| Update-channel `stable` exception, and the file's real meaning | `orbit/cmd/orbit/orbit.go:2398`–`:2428` |
| Credential-source ordering, both paths, incl. the profile's unconditional set and the 30 s retry loop | `orbit/cmd/orbit/orbit.go:463`–`:564` |
| Absent vs empty `command_line_flags`, and wholesale file replacement | `orbit/pkg/update/flag_runner.go:45`–`:93`. **The source comment states the distinction in words** |
| Device-side collision rules: Android alphabetical-by-name merge, later wins, loser marked `failed`; Windows OS-update profile conflict | `server/mdm/android/service/profiles.go:222`–`:224`, `:369`–`:396`; `server/service/windows_mdm_profiles.go:251`–`:277` |

**Finding 2(f), the damaged activity correction.** Restated: 42 distinct activity **types reachable
from** organisation-settings modification. Counted as 32 inline (`server/service/appconfig.go:1126`–
`:1685`) + 5 Apple OS-update (`:1745`–`:1769`) + 3 Google Workspace (`:1815`–`:1820`) + 2 historical
(`server/fleet/historical_data.go:73`, `:79`). Enrolment secrets are outside the set (`:2520`).
Three are best effort (`:1179` and both historical types). Nine are also emitted elsewhere.

**Finding 3, my own three unverified claims.** All three withdrawn and replaced, as recorded above.
The Android replacement establishes what *is* true: three reachable states (`pending` before
delivery `server/mdm/android/service/profiles.go:378`, `verified`/`failed` after the device reports
`server/mdm/android/service/pubsub.go:1128`, `:1214`–`:1219`), **`verifying` is never set on
Android**, and four artefacts are retained of which one is published. Apple maps acknowledgement to
`verifying` (`server/service/apple_mdm.go:6347`), macOS advances later on inventory
(`server/datastore/mysql/apple_mdm.go:3025`); Windows maps 2xx straight to `verified`
(`server/fleet/microsoft_mdm.go:1824`). Push: command enqueued first
(`server/mdm/apple/commander.go:671`), failed push treated as success on purpose
(`server/mdm/apple/profile_processor.go:108`–`:114`), inactive token turns MDM off and writes
activities (`server/mdm/apple/apple_mdm.go:1740`–`:1768`).

**Finding 4, five more scope overreaches.** Asset store narrowed to three arrival routes, only Apple
material being imported (`cmd/fleet/mdm_apple.go:109`, `:184`; Android at
`server/mdm/android/service/service.go:260`; PSSO at `server/service/apple_psso.go:300`). Licence
given its own row: selector, authority-changer, and **resetter** (`server/service/appconfig.go:1136`
blanks three Fleet Desktop and MDM fields on every Free-tier save). Cache periods stated: 1 s for
organisation settings, 1 min for the fleet-derived caches
(`server/datastore/cached_mysql/cached_mysql.go:38`–`:56`). Closing advice split by plane, since
process configuration has no read-back (`cmd/fleet/config_dump.go:28`–`:29`). Configuration hash
narrowed to the osquery detail-query path (`server/service/osquery_utils/queries.go:367`–`:379`).

**Finding 5, house style.** Passed at review and re-checked after this pass: no Go filenames, paths,
line numbers, functions or internal identifiers in reader-facing prose or table cells, and no em
dashes. Administrator-facing configuration keys are used freely and are not violations.

**One reviewer-adjacent claim declined.** A 15-minute expiry exists on the MDM asset cache
(`server/datastore/cached_mysql/cached_mysql.go:67`), and the obvious reading, that a rotated
certificate stays stale for 15 minutes, is **wrong**. The cache key embeds the asset's checksum,
which is read fresh on every lookup (`:456`, `:480`–`:481`), so a rotated asset is picked up on next
use and only the dead entry lingers. The appendix says so positively rather than repeating the
plausible-but-false version.

**Correction pushed into a finished chapter.** 1.5's audit blockquote said "around forty specific
changes ... agent options, enroll secrets", which the restatement contradicts twice. Corrected in
place to "around forty distinct activity types reachable from a change to it", with enroll secrets
named as a separate route.

## Draft review 2

Independent review, 2026-08-28, verdict **NOT READY**, twelve findings. Transcript at
`../../missing-fleet-manual-private/reviews/2026-08-28/appendices/a.3-sol-r2.out`. Finding 13
re-checked the round 1 numbers (twelve packaging inputs, 29 flags with 28 environment forms, three
Android states, the two cache periods, 320 registered keys, 42 activity types with three best
effort, the trailing-argument boundary) and all agreed with the tag. House style clean.

**Findings 1, 2, 9: the recursion.** Rewritten to carry distinctions. See the section above.

| Finding | What changed | Key citations |
|---|---|---|
| 1, Windows states | Device-state table re-keyed on **platform and profile class**. Windows reaches all four; the exception is narrowly a profile whose SCEP request Fleet brokered through a custom SCEP proxy, NDES or Smallstep, **DigiCert excluded by design**. `failed` self-heals in that class | `server/datastore/mysql/microsoft_mdm.go:1296`, `:1322`; `server/datastore/mysql/host_certificates.go:570`; `server/fleet/certificate_authorities.go:27` |
| 2, Apple states | iOS and iPadOS **installs** are promoted straight to `verified`; predicate is a literal two-platform match, not "non-macOS". Declarative profiles record `verified` from an active valid report. macOS is the only case where `verified` is not final | `server/service/apple_mdm.go:6345`, `:7279`; `server/datastore/mysql/apple_mdm.go:3060`; `server/mdm/apple/profile_verifier.go:44` |
| 9, push | Split by caller: administrator-initiated operations report the failure, background jobs swallow it, the two rotation jobs swallow it **and write the activity anyway**, multi-host run reports only a total failure. Inactive-token unenrolment fires **only in the scheduled mobile refetch** | `server/mdm/apple/profile_processor.go:108`; `server/mdm/apple/commander.go:180`; `ee/server/service/hosts.go:383`, `:887`; `server/service/mdm.go:699`; `server/mdm/apple/apple_mdm.go:1675`, `:1698`, `:1721` |
| 3, agent boundary | Replaced "exactly three settings" with four groups by durability: three persisted channels; debug level and script timeout live in memory; osquery flags, extensions and Nudge as component files; twelve notifications | `server/fleet/orbit.go:65`; `orbit/pkg/update/debug_log_runner.go:38`; `orbit/pkg/update/notifications.go:425`; `orbit/cmd/orbit/orbit.go:2463` |
| 4, reuse count | Nine to **twenty**, with the reused families named and disk encryption flagged as having three other emitters | `ee/server/service/teams.go:501`, `:523`, `:625`, `:747`; `ee/server/service/mdm.go:319`, `:332`; `server/service/org_logo.go:289` |
| 5, asset store | Self-contradiction resolved: push and SCEP stop being checked only when **every** such asset is stored; ABM and the Windows identity certificate stay fatal forever. **The SCEP challenge warns on no ordinary boot** | `cmd/fleet/mdm_apple.go:141`, `:204`, `:212`; `server/config/config.go:1176`; `cmd/fleet/serve.go:863`, `:876` |
| 6, server-owned fields | Windows replaced by **Apple Business Manager enablement**; Windows enablement is writable and audited. Entra row narrowed: cleared when omitted or empty, **rejected when sent non-empty** | `server/service/appconfig.go:1013`, `:1584`, `:726`, `:2162` |
| 7, exclusions | Read replica added, two host-side `--insecure` pairs added, and the ordering claim **reversed**: load and resolve first, validate after. Per-key type and range checks are the exception and happen during load | `server/datastore/mysql/mysql.go:239`, `:246`, `:440`; `orbit/cmd/orbit/orbit.go:451`; `cmd/fleet/serve.go:169`, `:226`, `:265` |
| 8, `stable` | Qualified to the whole normalised tuple. **An all-`stable` request is a no-op however many channels it names**; one non-`stable` channel carries the rest through. Added the no-update-channels early return | `orbit/cmd/orbit/orbit.go:2398`, `:2406`, `:2420`, `:2380` |
| 10, observability | Over-correction undone. Subset named with its real edges: two osquery intervals only, email only under SES, one partnership key, licence as decoded claims. **The transparency-URL partnership key is not exposed**, and **any authenticated role can read the lot** | `server/service/appconfig.go:41`, `:107`, `:244`; `server/service/service_appconfig.go:103`; `server/authz/policy.rego:71` |
| 11, cross-plane | Count replaced by instances, with the size of the unperformed comparison stated: 320 registered keys against 19 top-level stored groups **expanding to several hundred leaves** | `server/config/config.go:1299`; `server/fleet/app.go:760` |
| 12, empty environment | **Withdrawn.** Fleet's own precedence statement is silent on empty values, the configuration library is not vendored, and no test pins it. Replaced with the four-step order Fleet states plus actionable advice to remove rather than blank a variable | `cmd/fleet/config_dump.go:23`; `go.mod:141`; `server/config/config.go:2287` |

**Two provenance rulings applied, both the same rule.** Finding 12 is the second instance in this
project of a claim resting on a library outside the checkout, after the `fleetctl` appendix and its
flag parser. Finding 11 is the same rule in exclusivity form: two instances are established, "there
are two" is not. **Publish the instances, state the comparison that was not done.**

**One reviewer decomposition declined as arithmetic, while its conclusion was accepted.** The
reviewer's breakdown of the twenty reused activity types sums to twenty-one. The total of twenty is
right; the itemisation double-counts. Counted independently and listed in full above.
