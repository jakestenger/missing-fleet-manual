# De-AI + style pass: 8.10 Android and AMAPI diagnostics

File: `manual/08-troubleshooting/8.10-android-diagnostics.md`
Started 2026-08-21. Before: 606 lines.

## Inbound links checked before any heading rename
```
grep -rn "8.10-android-diagnostics.md#" manual/   -> zero anchor links
grep -rn "8.10-android-diagnostics.md"  manual/   -> two file-level links:
  08-troubleshooting/8.1-diagnostic-method.md:322
  01-foundations/1.2-anatomy.md:699
```
No inbound `#anchor` and no inbound `§8.10.x` reference from another file, so heading
text is free to change. Section numbers left untouched anyway.

## Pre-pass mechanical check (all already clean)
- em-dashes: 0
- banned-word list: 0 hits
- inline HTML comments: 0 (nothing for Jake's review notes to resolve)
- existing `[term]()` flags in this file: 0

## Citation inventory

### Path-based Go citations (11 found; the brief listed 10)
| Line | Citation | Fact it supported | Replacement |
|---|---|---|---|
| 102 | `cmd/fleet/cron.go` | profile manager runs every 30s | interval kept, schedule name kept, path dropped |
| 103 | `server/mdm/android/service/profiles.go` | profiles merged into one policy body, name-ascending | behaviour kept; "How to observe" cell now says nothing is observable yet |
| 121 | `server/mdm/android/service/pubsub.go` | verification is gated on `included_in_policy_version` <= applied version | behaviour kept, function names and path dropped |
| 218 | `server/mdm/android/service/profiles.go` | retry ceiling of 3 | restated as "three attempts per policy write" |
| 248 | `server/mdm/android/service/handler.go` | the Pub/Sub push path | path (the URL) kept, source column removed |
| 249 | `server/fleet/mdm.go` | token stored as MDM asset `android_pubsub_token` | asset name kept, source dropped |
| 313 | `cmd/fleet/cron.go` | both cron schedules exist and their intervals | names + intervals kept, source line deleted |
| 330 | `server/config/config.go` | `mdm.android_batch_size` default 100, `0` = unlimited | config key + default kept, path dropped. **Not on the brief's list of 10; removed anyway as a code citation.** |
| 339 | `server/mdm/android/service/reconcile_devices.go` | reconciler complements Pub/Sub `DELETED` handling | behaviour kept, path dropped |
| 353 | `server/fleet/cron_schedules.go` | two one-time migration schedules, 4.76.0 / 4.77.0 | schedule names + releases kept, path dropped |
| 366 | `server/mdm/android/service/service.go` | enrollment token carries enroll secret + IdP UUID in `additionalData` | behaviour kept, path dropped |

Plus three bare package-directory citations, same class:
`server/mdm/android/` (L63, L69, L584) and `server/mdm/android/service/` (L363).
Each supported a "no such code path exists" claim; each is now stated as
"not documented; unverified" per §8 honesty rules, with no path.

### Bare filename citations removed (8 standalone)
`profiles.go` L225, L233 · `service.go` L249, L251, L252 · `handler.go` L250 ·
`pubsub.go` L253, L254.

The brief's count of 18 bare filenames is 8 standalone plus the 10 basenames carried
inside the path citations above, which reconciles to the stated 28 total
(10 paths + 18 basenames). Arithmetic confirmed; `server/config/config.go` is the
one extra the brief did not count.

### Go identifiers removed beyond the file lists
`ListHostMDMAndroidProfilesPendingOrFailedInstallWithVersion`, `verifyDevicePolicy`,
`filterProfilesWithPendingCerts`, `pubSubPushPath`, `ProcessPubSubPush`,
`authenticatePubSub`, `newAndroidMDMProfileManagerSchedule`,
`newAndroidMDMDeviceReconcilerSchedule`, `CreateEnrollmentToken`,
`DefaultAndroidPolicyID`, `hostVPPInstalls`, `MaxCertificateInstallRetries = 3`,
`maxRequestFailures` (x2, see below).

### `maxRequestFailures` (the special case)
Both occurrences of the identifier are gone. The behaviour it names is stated more
plainly than before and kept in all three places it was load-bearing:
- §8.10.5 state-combination table: "Fleet gave up after three attempts."
- §8.10.5 "Retry and idempotency": the budget is **three attempts per policy write,
  not per profile**, so one malformed profile burns the retries for every other
  profile in the same host's policy.
- §8.10.11 third cut: kept as a narrowing step (remove profiles one at a time and
  re-trigger until the PATCH returns 200).

### AMAPI / config vocabulary deliberately preserved (spot-checked after editing)
`modifyPolicyApplications`, `PREINSTALLED`, `AVAILABLE`, `PERSONAL_USAGE_ALLOWED`,
`PERSONAL_USAGE_DISALLOWED`, the `android_enterprise/pubsub` push path + its `token`
parameter + the 10 MiB limit, `mdm.android_batch_size` = 100,
`FLEET_MDM_ANDROID_BATCH_SIZE`, `included_in_policy_version`,
`applied_policy_version`, `mdm_android_profile_manager` (30s),
`mdm_android_device_reconciler` (1h), and every table and column name.

### Doc and CHANGELOG citations converted
- `docs/REST API/rest-api.md` (L94, L429) -> fleetdm.com/docs/rest-api/rest-api
- `CHANGELOG.md` (L394, L422, L426, L556, L564) -> release numbers where known,
  otherwise github.com/fleetdm/fleet/releases
- `docs/Contributing/...` inline paths (L80, L363, L411, L440, L572) and the bare
  `android-mdm.md` / `api-for-contributors.md` / `mdm-bug-checklist.md` references
  (L255, L289, L293, L362, L384, L387, L398) -> dropped from the body, URLs live in
  `further_reading`. This follows 8.9, which carries contributor-doc URLs in
  frontmatter only and cites none inline.
- `docs/solutions/android/configuration-profiles/disable-camera.json` (L538) ->
  github.com/fleetdm/fleet/tree/main/docs/solutions/android/configuration-profiles
  in `further_reading`, matching 8.9's Windows equivalent.

### The 4.89.2 stamp
L154 read "Verified against `server/datastore/mysql/schema.sql` at 4.89.2." Both the
path and the bogus CHANGELOG-derived version are gone; the sentence is now a plain
cross-reference to 8.6. Frontmatter `verified_against: Fleet 4.90.0` was already
correct and is untouched. No other 4.89.2 in the file.

## Keep-list audit
| Item | Status |
|---|---|
| Negative-capability table, early and blunt | Present, §8.10.1. Kept first, unsoftened. |
| Declarative one-policy-per-device model; "stuck in a queue" is the wrong frame | Present, intro + §8.10.3. Kept. |
| Pub/Sub as single point of failure; stale Fleet view, healthy devices | Present, §8.10.6. Kept. |
| Three enrollment types with differing signatures | Present, §8.10.8. Kept. |
| Coverage gaps, kept honest | Present. Kept, nothing added. |
| Fleet Android agent exists, scoped to certificates + managed config, is not fleetd | Present, §8.10.1 + §8.10.10. Kept. |
| Setup experience **is** implemented on Android, contradicting a Fleet architecture doc | **Partially absent.** The `PREINSTALLED` row in §8.10.9 says setup experience adds all relevant apps to the host's policy at enrollment, so the positive fact is there. The contradiction of the architecture doc is **not** in the section. Not added: writing new content is out of scope for this pass. |

## Positive voice
Zero uses of "just" in the file to begin with. Of 12 `only` uses, 3 came out
("Only covers lock, wipe, and clear passcode" -> "Covers ..."; "the only thing that
eventually notices a wiped device" -> "the one thing ..."; "the only host-side
verification Android offers" -> "the one form of host-side verification Android
offers"). The other 9 stay, because in each the restriction *is* the fact: "the only
inbound device-originated path", "the only management transport Fleet uses",
"the only place the merged policy body is preserved", "the only record that they
ran", "business only", "Wipe COBO-only", and so on.

Other negative-voice edits where the negative was rhetorical rather than
substantive:
- Intro: "Android is not a queue. Fleet does not send Android devices a list of
  commands and wait for acks." -> "Android management is declarative. ... There is
  no command queue, so 'the command is stuck in the queue' describes nothing that
  exists here." Same fact, stated forward, and it now names the wrong frame
  explicitly instead of implying it.
- "It is not fleetd and it does not run osquery" -> "It is a different program from
  fleetd, with no osquery, no scripts, and no live query." (Broader, and positively
  framed as an inventory.)
- "for the queue-based platforms this one does not resemble" -> "the two
  queue-based platforms, for contrast".
- "a totally silent staleness, not an error" -> "silent staleness rather than an
  error". Intensifier dropped.

The §8.10.1 capability table was **not** softened. Every "Does not exist" / "No
path" / "Nothing equivalent" cell stands as written.

Headings: `## 8.10.1 What does not exist on Android` -> `## 8.10.1 The instruments
Android does not have`. Kept negative because the negative is the substance, but
made it read as an inventory rather than a void. No other heading touched. Numbers
frozen; no inbound anchors exist.

## `[term]()` flags added
- `[SCEP]()` (§8.10.1, the Fleet Android agent's scope). Consistent with 8.6, 8.9,
  and 1.2, which all flag it the same way.
- `[dead lettering]()` (Relevant resources table) - Google Cloud Pub/Sub jargon an
  administrator will not know.
Glossed in place instead of flagging: `adb` -> "Android Debug Bridge (`adb`)",
`IdP` -> "identity provider". `nanoMDM` was removed rather than flagged, since the
sentence reads better as "the Apple MDM path".

## Checked and found correct (no change needed)
- `fleetctl report` in the §8.10.1 table looked like a typo for `fleetctl query`.
  It is not: 8.7 line 399 states `fleetctl query` is the deprecated alias for
  `fleetctl report`, and 8.2, 8.4 and 8.14 all use `report`. Left alone.
- `android_devices.applied_policy_id` in the §8.10.2 vocabulary table matches the
  §8.10.5 column list for the same table. Consistent.

## Facts I believe may be wrong (reported, NOT changed)
1. **Certificate retry table, "Server side" row.** It says a reported failure resets
   the certificate to `pending` for redelivery *and* logs a `failed_install` activity
   "each time", against a budget of 3. Fleet's client-side budget is also 3, so the
   worst case is 9 SCEP attempts. The section never says that, and a reader could
   read "3" as the total. Left as written; flagging for a future verification pass.
2. **"Pagination is bounded at 10,000 pages"** (§8.10.7). Pages, not devices, is a
   very large bound. Plausible as written but worth re-checking against source, since
   a devices bound is the more usual shape.

## Edit log

### Batch 1 applied (frontmatter through §8.10.5)
verified_on bumped; further_reading extended to 11 URLs (rest-api, bug checklist,
api-for-contributors, solutions/android tree, releases added). Intro reframed off the
"is not a queue / does not send / wait for acks" pile-up onto "management is
declarative", keeping the wrong-frame point explicitly. §8.10.1 renamed and its
self-referential opener replaced. Code citations removed at old L63, L69, L80, L94,
L102, L103, L121, L154 (with the 4.89.2 stamp), L218, L225, L233. `[SCEP]()` and
`[dead lettering]()` flagged. §8.10.4 heading lost "applied honestly".

### Batch 2 applied (§8.10.6 through §8.10.8)
§8.10.6's fact table lost its whole Source column (every cell was a code citation);
all eight facts survive verbatim, including the push path, its `token` parameter and
the 10 MiB limit. Citations removed at old L248-254, L288, L289, L293, L313-314, L330,
L339, L353, L362, L363, L366, L377, L384, L387, L394, L398. `adb` and `IdP` glossed
in place. `DefaultAndroidPolicyID` replaced with "the enterprise's default policy".

### Batch 3 applied (§8.10.9 to end)
Citations removed at old L411, L422 (with `nanoMDM` and `hostVPPInstalls`), L426,
L429, L440, L459 (`MaxCertificateInstallRetries`), L538, L556, L564, L572, L584.
`nanoMDM` was rewritten out rather than flagged: "because they never touch the
Apple MDM path" reads better and the term was undefined manual-wide (this file was
its only occurrence).

### Batches 4 and 5: de-AI recheck fixes
The recheck caught three things the first pass introduced or left:
- **Near-duplicate sentences.** The intro's forward pointer and §8.10.1's opener
  both said, almost word for word, "the instruments you would reach for have no
  Android counterpart". Split: the intro now calls §8.10.1 an inventory, §8.10.1
  says "reaches for these first. None of them are here."
- **Duplicated superlative.** §8.10.1 opened with "the most useful thing in the
  section" while §8.10.5 says `payload` is "the single most useful artifact".
  The §8.10.1 self-assessment is gone; §8.10.5's kept, since it is about an
  artifact rather than about the prose.
- Four reflowed lines that had run past the wrap width after editing.

## Result
596 lines (from 606). Final sweeps all clean:
- `grep -E '\.go\b|\.md`|CHANGELOG|schema\.sql|server/|cmd/fleet|4\.89\.2'` -> 0 hits
  outside Google URLs
- em-dashes: 0 · banned words: 0 · HTML comments: 0
- section numbers 8.10.1 through 8.10.11 unchanged; all 8 outbound cross-file links
  intact; no diagram placeholders added (0 occurrences of "diagram")
- AMAPI/config vocabulary spot-check passed on all 13 protected terms
