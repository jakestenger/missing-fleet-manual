# De-AI + style pass: 8.8 Apple MDM diagnostics

Started 2026-08-21. Section: `manual/08-troubleshooting/8.8-apple-mdm-diagnostics.md`
Before: 549 lines.

Brief: strip 18 code citations, keep reader-usable identifiers, preserve listed
findings verbatim in substance, positive voice, de-AI, `[term]()` flags, no
diagram placeholders (Part VIII is the reference chapter).

## Citation conversion table

| Path cited | Fact it supported | Disposition |
|---|---|---|
| (filling in as I go) | | |

## Change log

### Plan (batches)
1. Frontmatter + intro + 8.8.1 + 8.8.2
2. 8.8.3 to 8.8.7
3. 8.8.8 to 8.8.13 + See also
4. Recheck loop (only/just, em-dash, banned words, sentence rhythm, near-miss metaphors)

### Pre-flight checks
- Em-dashes: none. Banned vocabulary: none. HTML comments: none.
- Inbound anchor links (`8.8-apple-mdm-diagnostics.md#`): **none**. Nine files link the
  section without a fragment; 8.9 cites "§8.8.2" and "§8.8.7" by number in prose, so those
  two section numbers must keep their subject matter (fleetctl flag reference; profile status
  vocabulary). Both do.
- 30 source pointers in the body (18 Go paths plus in-repo docs, `articles/*`, `tools/*`,
  `frontend/*`), listed below.

## Citation trail removed from the section

Pointers are as the draft recorded them. `verified_source` in the frontmatter is
`fleet-public main @ 2026-08-05 (d2fe9be461)`, so every row below was read there.

| Fact retained in prose | Pointer removed |
|---|---|
| Fleet's Apple MDM architecture pages are stubs (intro says so in plain terms) | `docs/Contributing/architecture/mdm/apple-mdm-architecture.md` (8 lines, no body), `mdm-overview.md` (`[Placeholder for ... Diagram]`) |
| The eight-hop delivery path in §8.8.1, its transports, and where state lands | `tools/mdm/apple/glossary-and-protocols.md`, `server/mdm/nanomdm/` |
| Cron names `apple_mdm_apns_pusher` and `apple_mdm_dep_profile_assigner` (kept; they are what the reader types) | `server/fleet/cron_schedules.go` (constants `CronAppleMDMAPNsPusher`, `CronAppleMDMDEPProfileAssigner`), cited 3x in the draft |
| APNs carries no payload; commands wait in Fleet's queue until the device connects back | `articles/apple-push-notification-service-apns-mdm.md` -> fleetdm.com/guides/apple-push-notification-service-apns-mdm, already in `further_reading` |
| `--host` required on `get mdm-commands` since 4.89.2; the guide's unfiltered form is stale | `cmd/fleetctl/fleetctl/get.go`; the stale example is in `articles/mdm-commands.md` -> now "Fleet's MDM commands guide" |
| `--command_status` accepts `pending`, `ran`, `failed` | `cmd/fleetctl/fleetctl/flags.go` |
| A blank request type prints as `InstallProfile`; the 1,000-most-recent figure is the guide's, and the page limit is undocumented | `cmd/fleetctl/fleetctl/get.go`, `articles/mdm-commands.md` |
| The three current command endpoints, and the two deprecated aliases that still work | `server/service/handler.go` |
| The API `result` field is always base64; decode before reading | `server/fleet/mdm.go` (`Result []byte json:"result"`, plus the `encoding/json` explanation) |
| Supplying your own `CommandUUID` makes the later result lookup trivial | `articles/mdm-commands.md` |
| The Show MDM commands toggle, the info button, and the platforms the Upcoming tab covers | `frontend/pages/hosts/details/cards/Activity/Activity.tsx`, `.../MDMCommandsToggle/MDMCommandsToggle.tsx` |
| `RemoveProfile` sent this way is device-channel only; user-scoped profiles are out of reach for both surfaces | `articles/mdm-commands.md` |
| DEP page size of 200 devices per request | `DEPSyncLimit` in `server/mdm/apple/apple_mdm.go` (was the "Source" column of the §8.8.5 facts table, now dropped) |
| `mdm.apple_dep_sync_periodicity` default 1 minute, and Apple's 7 day cursor lifetime | `resetting-apple-dep-sync-cursor.md` (in `further_reading` as a GitHub URL; no fleetdm.com/docs page exists for contributor troubleshooting docs) |
| Clearing the cursor is safe at any scale, re-enrolls nothing, changes no ABM assignment, re-pushes no DEP profile | `docs/Contributing/product-groups/mdm/troubleshooting/resetting-apple-dep-sync-cursor.md` -> "documented by Fleet as such", URL in `further_reading` |
| ADE ingest is recorded in `host_dep_assignments` and deletes there are soft deletes | `docs/Contributing/architecture/mdm/automated-device-enrollment.md` -> added to `further_reading` as a GitHub URL |
| `dep_syncer` appears in Fleet's own docs; the registered cron name is `apple_mdm_dep_profile_assigner` | `server/fleet/cron_schedules.go` |
| A host restart renews enrollment on the next Setup Assistant pass | `tools/mdm/apple/troubleshooting.md` |
| The four profile status values plus NULL, and which are transitional | `server/fleet/mdm.go` (`MDMDeliveryStatus`) |
| Device-reported failures retry a fixed number of times then stick at `failed`; enqueue failures reset to NULL | `server/fleet/mdm.go` (`mdm.MaxAppleProfileRetries`, `ReconcileProfile`). The constant name is not a config key an administrator can set, so it went with the path; "a fixed number of times" preserves what the draft actually said, since the draft never gave the number |

### Batch log
- **Batch 1** (frontmatter, intro, 8.8.1, 8.8.2): `verified_on` -> 2026-08-21; two `further_reading`
  URLs added (the DDM VPN guide, the ADE architecture doc) because their in-body citations were
  converted. Intro rewritten off the "docs are stubs, here is the file that proves it" framing.
  §8.8.1's ordered-pipeline table left exactly as written, per the brief; the citation paragraph
  under it deleted whole.
- **Batch 2** (8.8.3 to 8.8.7): "do not re-derive it here" cut (instruction to the author, not the
  reader). §8.8.5 facts table lost its all-citation Source column. Heading "When a reset does not
  bring the device back" -> "When Apple stops returning the device". NanoDEP -> "Fleet's DEP
  client" (internal component name). §8.8.7 gained a pointer to 8.9's shared status vocabulary in
  place of the dropped citation, which 8.9 already claims from its side.
| The `Error.UnknownDeclarationType` status reason code is treated the same as an invalid declaration | `server/service/apple_mdm.go` (`isUnknownDeclarationType`) |
| VPN declarations need macOS 27+, and earlier versions reject them with that code | `articles/deploy-vpn-with-declarative-device-management-ddm-in-fleet.md` -> fleetdm.com/guides/deploy-vpn-with-declarative-device-management-ddm-in-fleet, added to `further_reading` |
| A deliverable declaration must be a configuration type: no OS update settings, no asset-requiring type, no status subscription type | `server/fleet/apple_mdm.go`, "as summarised in the DDM architecture doc" |
| Declarations are JSON in `mdm_apple_declarations`; the UUID prefixes `d` / `a` / `w` | `server/fleet/mdm.go` and `docs/Contributing/architecture/mdm/apple-declarative-device-management.md` (already in `further_reading`) |
| One `DeclarativeManagement` command per host rather than one per declaration | `ReconcileAppleDeclarations` (function name dropped; "Fleet's declaration reconcile" carries it) |
| VPP verification timeout of 10 minutes and 5 second request delay, with both env vars | `server/config/config.go`, `docs/Contributing/architecture/software/software-installation.md` |
| `DEP auth error: <status>: <body>` and `DEP HTTP error: <status>: <body>` formats | `server/mdm/nanodep/client/auth.go`, `server/mdm/nanodep/godep/client.go` |
| All three DEP errors can arrive as 403, so match on the body | predicate functions `IsTermsNotSigned`, `IsSignatureInvalid`, `IsTokenRejected` in `server/mdm/nanodep/godep/account.go` |
| The escalation collection list | `docs/Contributing/product-groups/mdm/mdm-bug-checklist.md` -> "what Fleet's MDM bug checklist asks for" |

Nothing path-shaped survives in the body: `grep -nE "server/|cmd/|tools/|frontend/|\.go\b|\.tsx|articles/"`
returns nothing. The three `docs/Contributing/...` strings still in the file are GitHub URLs in
`further_reading`, which is where they belong (no fleetdm.com/docs page exists for contributor
docs). No `CHANGELOG.md` citation was present, so the release-number conversion did not apply;
the one release number in the body, `--host` required "since 4.89.2", is a behaviour-change
marker an administrator can act on and stayed.

## Reader-usable identifiers deliberately kept

Every `nano_*` and `host_mdm_*` table and column named in the draft, and all four SQL blocks
unchanged; `nano_view_queue`; `nano_dep_names.syncer_cursor` / `syncer_cursor_at`;
`host_dep_assignments`; `dep_cooldowns`; `mdm_apple_declarations`,
`mdm_apple_configuration_profiles`, `mdm_apple_declarative_requests`; `upcoming_activities`;
`cron_stats`. `fleetctl get mdm-commands` and `mdm-command-results` with `--host`, `--type`,
`--command_status`, `--id`; `fleetctl mdm run-command` with `--hosts` and `--payload`;
`fleetctl trigger --name=<cron>` in all three places. All API paths including the two
deprecated aliases and both resend endpoints, plus both `curl` recipes and the
`| base64 -d` decode. `FLEET_SERVER_VPP_VERIFY_TIMEOUT` (10 minutes) and
`FLEET_SERVER_VPP_VERIFY_REQUEST_DELAY` (5 seconds) with their `server.*` keys;
`mdm.apple_dep_sync_periodicity` (1 minute). Cron names `apple_mdm_apns_pusher`,
`apple_mdm_dep_profile_assigner`, `mdm_apple_profile_manager`, and the `integrations` cron.
`T_C_NOT_SIGNED`, `signature_invalid`, `token_rejected`, both DEP error formats, and
`Error.UnknownDeclarationType`. All five profile status values; the UI path
(Host details, Activity, Show MDM commands, and the Upcoming tab platforms);
`sudo profiles renew -type enrollment`, `sudo profiles status -type enrollment`,
`sudo profiles show -type configuration`, and the `log stream` predicate.

**Kept against the brief, deliberately:** the filename
`turn_on_debug_mdm_logging.mobileconfig` in §8.8.12. It is a file the reader downloads and
installs, not a code citation, and without a name there is nothing to search for. The
directory path `tools/mdm/apple/` went; the sentence now says Fleet ships it "in its
repository".

## Findings preserved, checked one by one after the rewrite

- APNs certificate first when every Apple device stops at once; expiry produces no
  device-side error; 12 month validity; renewal needs the same Apple Account, and losing it
  forces a full re-enrollment. Kept, emphasis intact.
- TLS inspection breaks APNs, with the PAC-proxy exception and the OS versions. Kept.
- A single device failing while others work is an invalid device token, and re-enrolling that
  device is the fix. Kept, plus the topic-mismatch check.
- "Assignment time but no push time means the push never happened", still its own heading
  (§8.8.6), with `sudo profiles renew -type enrollment` and the restart alternative.
- DEP cursor: NULL means `fetch-devices` (full), set means `sync-devices` (deltas); 200 per
  page; 7 day expiry at Apple; clearing it is safe at any scale and re-enrolls, re-assigns and
  re-pushes nothing; Apple can throttle devices into a cooldown and stop returning them, which
  a reset does not fix.
- VPP verification is a second phase that fails on its own, so a reported failure may be a
  timeout with the app installed. Kept, with the command-feed signature.
- Half-enrolled state at 2 to 3 percent, `fleetdm/fleet#47793`, DDM-based agent install as the
  planned fix, detection and recovery cross-referenced to 8.4 rather than duplicated.
- Which profile statuses are transitional (NULL, `pending`, `verifying`) and which is a real
  failure (`failed`), including that `verifying` can fall back to `failed`, `pending` or NULL.
- `verifying` that never reaches `verified` points at the osquery detail-query path.

## Positive voice and heading changes (STYLE §15)

| Before | After | Why |
|---|---|---|
| Intro: "Fleet's Apple MDM architecture docs are stubs: `...apple-mdm-architecture.md` is 8 lines with no body…" | "Apple MDM puts more hops between Fleet's decision and the device's action than any other channel Fleet manages, and Fleet's own Apple MDM architecture pages are stubs." | The old opening was three sentences of citation and a promise to mark things; the new one says what the section contains. |
| "It is a wake-up signal only, and the commands sit in Fleet's queue" | "The push is a wake-up signal, and commands wait in Fleet's queue" | Dropped "only". |
| "the single most misleading Apple failure mode" | "the most misleading failure mode in the Apple stack" | Dropped the double superlative. |
| "The Upcoming tab is not supported on every platform; the tooltip in that file lists macOS, Windows, Linux, iOS, and iPadOS." | "The Upcoming tab covers macOS, Windows, Linux, iOS, and iPadOS." | Says what is supported. |
| "User-scoped profiles cannot be removed with `fleetctl mdm run-command` or the run endpoint" | "User-scoped profiles are out of reach for both `fleetctl mdm run-command` and the run endpoint" | Keeps the constraint, drops the "cannot" frame. The bold sentence before it keeps its load-bearing "only". |
| "the shorter way in when you do not need `last_seen_at`. Full column reference … do not re-derive it here." | "the shorter way in when `last_seen_at` is not part of the question. The full column reference … is in 8.6 §8.6.5." | The trailing clause was an instruction to the author. |
| "stops all pushes and produces no device-side error" | "stops every push and produces no device-side error" | "Every" over "all"; the second negative is the finding and stays. |
| "which Apple owns exclusively" | "which Apple owns outright" | "Exclusively" was doing nothing. |
| "APNs can traverse a PAC-specified web proxy, but only one that passes traffic through without decrypting" | "…a PAC-specified web proxy that passes the traffic through without decrypting it" | Dropped "but only". |
| "If commands are queueing and the cron is not advancing in `cron_stats`, the problem is Fleet-side scheduling, not Apple." | "Commands piling up while the cron stops advancing in `cron_stats` is a Fleet-side scheduling problem, not an Apple one." | Positive subject; the contrast is the finding and stays. |
| §8.8.4 sub-head body: "Not a certificate problem. The usual cause is an invalid or stale device token…" | "This pattern points at that device's push token, not at the certificate." | Opens on the cause instead of the non-cause. |
| "A mismatch … silently kills pushes" | "A mismatch … stops pushes for the affected enrollments without logging anything" | "Silently" as an intensifier, and the replacement states the observable. |
| "It does not re-enroll devices, does not change ABM assignments, and does not re-push DEP profiles. It only re-baselines Fleet's assignment list" | "It re-baselines Fleet's assignment list and stops there: no device is re-enrolled, ABM assignments are untouched, and no DEP profile is re-pushed." | Action first, then the three guarantees, which are the safety claim and had to survive. Dropped "only". |
| Heading "When a reset does not bring the device back" | "When Apple stops returning the device" | Negative heading; no inbound anchor. |
| "soft-deleted rather than removed" / "causes Fleet to immediately recreate the host" | "a delete there is a soft delete" / "causes Fleet to recreate the host immediately" | Positive form; split the run-on. |
| "Note the naming inconsistency: the ADE architecture doc calls the sync job `dep_syncer`, but…" | "Fleet's own documentation calls the sync job `dep_syncer` in places. The registered cron name is `apple_mdm_dep_profile_assigner`, and that is the one to use…" | "Note the" throat-clearing, and the reader needs the name to use, not the taxonomy of the mistake. |
| "use it to size the problem before touching individual machines rather than after" | "Size the problem there first, then work the list." | "Rather than after" answered a question nobody asked. |
| "`ReconcileAppleDeclarations` does not enqueue one command per declaration. It marks…" | "Fleet's declaration reconcile enqueues one command per host, not one per declaration. It marks…" | Positive, and the internal function name goes. |
| "Everything after that is the DDM protocol talking to itself" | "From there the device drives the exchange" | Near-miss metaphor: the device talks to Fleet, not to itself. |
| "Removal is inferred, not reported. The device does not send "remove" statuses; Fleet detects removal by the declaration's absence…" | "Removal is inferred. The device reports the declarations it holds, and Fleet reads a declaration's absence from that report as removal." | Three negatives down to zero, same mechanism. |
| "Only the one `DeclarativeManagement` command will ever appear in `nano_view_queue`." | "`nano_view_queue` shows the single `DeclarativeManagement` command and nothing more, however many declarations moved." | Dropped "only" and "will ever"; the added clause is what the reader is actually checking. |
| "declarations cannot carry OS update settings…, cannot be a type that requires assets, cannot be a status subscription type, and must be a configuration type" | "A declaration Fleet will deliver has to be a configuration type: it cannot carry OS update settings…, cannot be a type that requires assets, and cannot be a status subscription type." | Requirement first, exclusions after. Heading shortened to "DDM limits". |
| "It answers MDM commands and does not appear as an osquery host." | "It answers MDM commands and never appears as an osquery host." | Same fact, positive verb. |
| "Do not diagnose it from the server side alone: a half-enrolled host looks healthy in every Apple MDM table." | "Detection and recovery are in 8.4, and that is where the diagnosis has to happen: a half-enrolled host looks healthy in every Apple MDM table on the server." | One sentence instead of two, and the instruction points somewhere. |
| "Before treating it as an install failure, check the device. The command feed for the host will show … that pattern with no terminal success is the signature." | "Check the device before treating it as an install failure. The signature in the host's command feed is an acknowledged `InstallApplication` followed by a run of `InstalledApplicationList` commands that never reaches a terminal success." | Action first; the two-step "will show X; X is the signature" collapsed into one. |
| "differing only in that the `InstallApplication` command carries a `ManifestURL`" | "The difference is that their `InstallApplication` command carries a `ManifestURL`" | Dropped "only". |
| Heading "8.8.11 Error strings you can actually match on" | "8.8.11 Error strings worth recognising" | "Actually" is filler, and this matches 8.3.6's heading for the same material. |
| "Only strings located in source are listed." | "Every string below is emitted by the Fleet server verbatim, so grep for it." | The old sentence introduced a citation column that no longer exists. Same replacement 8.3 made. |
| "All three can arrive as 403, which is why the HTTP status alone tells you nothing." | "All three can arrive as 403, so match on the body of the message rather than on the HTTP status." | Tells the reader what to do instead of what the status fails to do. |
| "One line each. The full treatment is elsewhere." | "One line each, with the section that covers it in full." | "Elsewhere" is exactly what the third column answers. |
| "Everything left of hop 5 is healthy. Look right:" / "Look left." | "hops 1 to 5 are healthy. The failure is at 6 or later:" / "the failure is at hop 4 or earlier" | The hops are a vertical table, so left/right was a spatial metaphor with nothing behind it. Numbering the hops is also actionable. |
| Internal note in §8.8.6, second sentence ("Sizing it from the vital first is what keeps it from being diagnosed one host at a time") | cut | The body now says it in the sentence above. |

"Only" kept where it carries the fact: hop 4's "device-side only"; "`sync-devices` … Deltas
only"; "**`RemoveProfile` sent this way targets the device channel only.**"

## De-AI recheck notes

Mechanical set was already clean going in (no em-dashes, no banned vocabulary, no "serves
as"), so the pass hunted the subtler tells:

- **Near-miss metaphors:** "the DDM protocol talking to itself" and the left/right hop
  metaphor, both replaced above. "Highest-blast-radius secret" survives; it is a real term of
  art in this context and it is precise.
- **Argument teleportation:** the §8.8.5 opener used "NanoDEP" and "cursor" before either was
  a thing the reader had met, and the ADE/DEP naming split arrived three paragraphs later; the
  naming is now stated in the opener where the two names first collide.
- **Reshuffle-proof paragraphs:** the §8.8.6 internal note repeated its own body paragraph
  (cut); the §8.8.11 opener repeated "Fleet" three times in two sentences (merged).
- **Uniform sentence length:** the VPP paragraph and the "one device failing" paragraph were
  each three medium sentences; both now open short. Table cells left alone, since parallel
  phrasing inside a column is the point.
- **Manufactured specificity:** none added. Every number in the section (200, 7 days, 12
  months, 168 hours, 10 minutes, 5 seconds, 1 minute, 30 seconds, 2 to 3 percent, 1,000,
  5223, 2197, macOS 27) came from the draft.
- §8.8.1's ordered pipeline stayed a table, per the brief. No diagram placeholder anywhere in
  the section, and none was added.

## New `[term]()` flags (STYLE §14)

| Flag | Location | Why |
|---|---|---|
| `[ADE]()` | §8.8.5 opener | Matches the flag 8.6 already carries. |
| `[DEP]()` | §8.8.5 opener | Same, and this section is where the two names collide hardest (`nano_dep_names`, `dep_cooldowns`, `host_dep_assignments`, `apple_mdm_dep_profile_assigner`). |
| `[VPP]()` | §8.8.10 opener | Matches 8.6. |

Expanded in place instead of flagged: **APNs** ("APNs, the Apple Push Notification service")
at its first substantial use in §8.8.1, and **DDM** ("Declarative device management (DDM)") at
the top of §8.8.8, where **declaration** also now gets a one-line definition ("a JSON object
the device fetches, applies, and then reports back on"). That follows the OTLP precedent from
8.3: a short expansion beats a flag. **TokenUpdate** never appears in the section as a term
(only the `token_update_tally` column), so there was nothing to flag; `[SCEP]()` and
`[node key]()` do not appear either.

## HTML comments

None in the file.

## Facts I believe may be wrong (reported, NOT changed)

- **§8.8.9 said the half-enrolled issue was "open as of 4.89.2".** The brief states the fact
  as "open as of 4.90.x", and the frontmatter records `verified_against: Fleet 4.90.0`, so the
  draft's 4.89.2 is the same known-bad CHANGELOG-derived stamp STYLE §9 warns about and 8.3
  and 8.6 both hit. Changed to "open as of 4.90.x" **on the brief's instruction**, and flagged
  here because it is the one number in the section that moved.
- **§8.8.2's "`--host` **Required** … since 4.89.2"** carries the same suspect release number,
  but as a behaviour-change marker rather than a verification stamp. Left exactly as written.
- **Frontmatter `verified_source`** is still a commit on a branch ("fleet-public main @
  2026-08-05 (d2fe9be461); does NOT include 4.90.1 fixes"), which STYLE §9 rules out, and it
  disagrees with the brief's "verified at tag `fleet-v4.90.1`". Out of scope per the brief;
  flagging for the re-verification pass, along with the 4.90.0 vs 4.90.1 gap.
- Nothing else. No other fact, number, name, or hedge was altered.

## Line counts

548 lines before, 529 after.

Body source citations removed: **43 pointer instances**, of which 18 are Go file references
(matching the brief's count), 8 are in-repo `docs/` paths, 8 are `articles/` guide paths, 3
are `tools/` paths, 2 are `frontend/` paths, and one is the `server/mdm/nanomdm/` directory.
Several paths were cited more than once (`articles/mdm-commands.md` 4x,
`articles/apple-push-notification-service-apns-mdm.md` 4x, `server/fleet/cron_schedules.go`
3x, `resetting-apple-dep-sync-cursor.md` 3x, `server/fleet/mdm.go` 3x).

Also dropped: one all-citation table column (the Source column in §8.8.5) and these internal
identifiers, each replaced with behaviour: `ReconcileAppleDeclarations`,
`mdm.MaxAppleProfileRetries`, `ReconcileProfile`, `isUnknownDeclarationType`, the three `Is*`
DEP predicates, `MDMDeliveryStatus`, the `Result []byte json:"result"` field declaration, the
two `CronApple*` constant names, and NanoDEP as a component name.

Two `further_reading` URLs added to carry converted citations (the DDM VPN guide as
fleetdm.com/guides/..., the ADE architecture doc as a GitHub URL). One heading renamed
("When a reset does not bring the device back" -> "When Apple stops returning the device"),
one shortened ("DDM limits worth knowing before you debug" -> "DDM limits"), one retitled
("Error strings you can actually match on" -> "Error strings worth recognising"). No inbound
anchor links to this section exist, so nothing needed updating elsewhere; 8.9's prose
references to "§8.8.2" and "§8.8.7" still land on the same material.
