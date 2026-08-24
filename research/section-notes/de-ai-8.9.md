# de-AI + style pass: 8.9 Windows MDM diagnostics

Started 2026-08-21. Before: 699 lines (698 content + trailing).

## Plan
1. Strip code citations (path-based + bare filenames/Go identifiers).
2. Triage the two 4.89.2 refs.
3. Positive voice, heading check, de-AI, `[term]()` flags.

## Citation removal table
(filled in as I go)

## Inbound anchor check
`grep -rn "8.9-windows-mdm-diagnostics.md#" manual/` → zero results. No inbound
anchors, so headings can be renamed freely. Nine plain-file links exist
(8.1, 8.6, 8.8, 8.10, 1.2) and none target a heading.

## Citations removed, and the fact each one supported

### Path-based (13 by grep, plus doc/CHANGELOG paths)
| Removed citation | Fact it supported | Now presented as |
|---|---|---|
| `server/mdm/microsoft/microsoft_mdm.go` | The five HTTP endpoint paths | Plain list of paths and roles; "Constant" column dropped (`MDE2DiscoveryPath`, `MDE2PolicyPath`, `MDE2EnrollPath`, `MDE2ManagementPath`, `MDE2TOSPath`) |
| `server/mdm/microsoft/syncml/syncml.go` (×3: token type URIs, status codes, reserved LocURIs) | Both `BinarySecurityToken` value types; the SyncML status and alert code sets; the three reserved LocURI prefixes | Stated directly. Constant columns dropped from all three tables |
| `server/service/microsoft_mdm.go` (×2, incl. `reconcileWindowsMDMPollSchedule`) | 1 minute / 480 minute poll values; poll-schedule reconcile behaviour | Behaviour statement; both intervals kept |
| `server/fleet/capabilities.go` / `CapabilityWindowsMDMSync` | fleetd advertises `windows_mdm_sync` in `X-Fleet-Capabilities` | Capability name and header kept, source dropped |
| `server/service/orbit.go` | `fleetd_sync_capable` written on Orbit config check-in | Behaviour statement |
| `server/fleet/orbit.go` | `windows_mdm_sync_request: true` in the config response | Field name kept, source dropped |
| `server/datastore/mysql/schema.sql` (×3) | Column lists for the Windows MDM tables; `wstep_cert_auth_associations`; `host_mdm_windows_profiles` | Tables and columns kept verbatim, "verified in schema.sql" dropped |
| `server/mdm/microsoft/admx/admx.go` (`IsADMX`, `Equal`) | Fleet parses ADMX fragments and compares semantically | Behaviour statement |
| `server/mdm/microsoft/wstep.go` | Fleet fetches Entra's JWKS to verify the token | Behaviour statement, JWKS URL kept |
| `server/fleet/cron_schedules.go` / `CronMDMWindowsProfileManager` / `cmd/fleet/cron_registration.go` | The `mdm_windows_profile_manager` cron exists and reconciles profiles | Cron name kept, registration paths dropped |
| `docs/Contributing/architecture/mdm/windows-mdm-architecture.md` (×2, plus bare `windows-mdm-architecture.md`) | Sync request is repeated until acked; WNS is a possible future addition | Behaviour statement; URL already in `further_reading` |
| `docs/Contributing/product-groups/mdm/windows-mdm-glossary-and-protocol.md` (×2, plus bare `windows-mdm-glossary-and-protocol.md` ×4) | Enrollment SOAP sequence; WSTEP role; registry value meanings | Behaviour statements; "Verified in" column dropped from the host-side table; URL in `further_reading` |
| `docs/Contributing/product-groups/mdm/windows-autopilot.md` (plus bare `windows-autopilot.md` ×7) | Autopilot licensing, `dsregcmd` fields, OOBE diagnostics, error strings | Attributed as "Fleet's Autopilot documentation" where the claim is Fleet's own hedged understanding; otherwise stated plainly. URL in `further_reading` |
| `docs/solutions/windows/configuration-profiles/...xml` (×2) | Worked profile examples, incl. the ADMX Chrome example | Described as Fleet's published worked examples; directory URL moved into `further_reading` |
| `CHANGELOG.md` (×9) | Queue cleanup job; upload validation; top-level-verb rejection; `host_uuid` link at first session; token audience v1/v2; challenge validation; client errors logged at info; profiles queued at enroll; 4.89.1 and 4.89.2 entries | Release numbers where known, plus one pointer to github.com/fleetdm/fleet/releases in Version notes |

### Bare filenames and Go identifiers (the class a path grep misses)
`admx.go` · `capabilities.go` · `orbit.go` · `syncml.go` (×3) · `wstep.go` ·
`schema.sql` (×2) · `microsoft_mdm.go` · `cron_schedules.go` ·
`windows-autopilot.md` (×7) · `windows-mdm-glossary-and-protocol.md` (×4) ·
`windows-mdm-architecture.md` · `CHANGELOG.md` (×9) · `MDE2DiscoveryPath` ·
`MDE2PolicyPath` · `MDE2EnrollPath` · `MDE2ManagementPath` · `MDE2TOSPath` ·
`CapabilityWindowsMDMSync` · `reconcileWindowsMDMPollSchedule` ·
`CronMDMWindowsProfileManager` · `IsADMX` · `Equal` · all 19 `CmdStatus*` ·
all 7 `CmdAlert*` · `FleetBitLockerTargetLocURI` · `FleetOSUpdateTargetLocURI` ·
`FleetRemoteWipeTargetLocURI` · `PolicyMinKeyLength` ·
`PolicyCertValidityPeriodInSecs` · `PolicyCertRenewalPeriodInSecs` ·
`WstepCertRenewalPeriodInDays` · `WstepRenewRetryInterval` · `WstepROBOSupport` ·
`DocProvisioningAppProviderID` (×2) · `EnrollmentVersionV4` ·
`RegisterDeviceWithManagement`

Kept deliberately: `mdmregistration.dll` (a real Windows component, on the
keep-list), `DeviceEnrollmentUserToken` and `urn:ietf:params:oauth:token-type:jwt`
(MS-MDE2 / OASIS protocol token-type URIs a reader sees in a SOAP envelope, not
Go identifiers), and every table and column name.

## The two 4.89.2 references
- **Line 171-172, the bogus stamp:** "Columns below are verified against
  `server/datastore/mysql/schema.sql` at 4.89.2." Version dropped entirely; the
  sentence reads fine as a pointer to 8.6 for the full reference.
- **Line 689, the real release:** the version-notes row for 4.89.2 (Autopilot
  enrollments hanging on the Enrollment Status Page at "Account setup") left
  untouched.

## Presentation changes, batch by batch

### Batch 1 (frontmatter, intro, 8.9.1 to 8.9.4)
- `verified_on` → 2026-08-21. Added two `further_reading` URLs: the worked
  Windows profile directory and github.com/fleetdm/fleet/releases.
- Intro reordered to lead with the mechanism (wake via fleetd) rather than with a
  comparison to Apple MDM and a run of three negatives. "Fleet does not use WNS"
  kept, since it is a keep-list fact.
- 8.9.1: "Constant" column dropped. OMA-DM, SyncML, WSTEP and MS-MDE2 glossed in
  place inside the table rather than flagged, since one clause does the job.
- 8.9.1: "Only `/management` uses mTLS" → "The management endpoint is the one that
  uses mTLS" (§15). The later instance at 8.9.8 keeps "only", where it carries the
  contrast that makes the bisection work.
- 8.9.2 step 2: "The header only exists on the Orbit request" → "The header rides
  on the Orbit request", and dropped the "which has no such header" aside.
- 8.9.2 boot/resume: "Do not escalate a delay measured in single-digit minutes"
  → "resolves itself" (§15, and it stops instructing the reader not to do
  something).
- Heading "Why there is no push" → "Wake without a push service". No inbound
  anchors, and it matches the positive-heading convention in the rest of the file.
- 8.9.3: cut "Fleet has no way to reach into the device", which repeats the WNS
  fact stated two screens earlier.
- 8.9.4 queue cleanup: "Do not treat a missing old queue row as proof" → stated as
  what the evidence is worth instead.

### Batch 2 (8.9.5, 8.9.6)
- Both code tables lost their Constant column. The five status codes that had an
  empty Meaning cell (401, 403, 407, 418, 425) now carry the plain reading of the
  same fact. Alert codes likewise.
- "Seeing `1201` when you expected a server-initiated session is correct
  behavior" was answering a question nobody asked (§15); replaced with a positive
  statement of what you will see.
- ADMX paragraph rewritten so the diagnostic conclusion is stated positively
  ("points at delivery") instead of as a double negative.

### Batch 3 (8.9.7, 8.9.8)
- `RegisterDeviceWithManagement` dropped; `mdmregistration.dll` kept, as
  "calls into Windows' `mdmregistration.dll` to register the device for
  management".
- Autopilot glossed in place ("Microsoft's zero-touch provisioning flow for new
  Windows devices"), OOBE glossed in place ("the out-of-box experience (OOBE), the
  first-boot setup flow"), MS-MDE2 glossed in the endpoint table.
- WSTEP fact table lost its Source column. Two rows renamed so the pair of
  renewal periods is legible without the constant names: "Renewal period offered
  in the certificate policy" (180 days) and "Renewal period written into the
  provisioning document" (365 days).
- "Renewal retry interval | `4`" carried no unit in the source constant, so the
  row now says so rather than implying minutes or days.
- Client-error logging paragraph rewritten positively: Fleet logs at info, so an
  error-level filter misses the token error, and `fleetctl debug errors` stores
  server faults.

### Batch 4 (8.9.9, 8.9.10, 8.9.11, Version notes)
- Cron registration paths dropped; `mdm_windows_profile_manager` kept everywhere.
- Host-side surfaces table lost its "Verified in" column, which held nothing but
  doc filenames.
- Event-log-channel paragraph reworded off "the Fleet repository" onto "Fleet's
  documentation", keeping the "Not documented; unverified" marker intact.
- "Source: `CHANGELOG.md`" under Version notes replaced by the release-notes
  pointer, matching 8.14.

### Batches 5 to 7 (de-AI passes)
- Opening paragraph rewritten twice. It now leads with the mechanism ("Every
  Windows MDM session is opened by the device") instead of a comparison to Apple
  MDM followed by three negatives in a row.
- The three fleetd checks in 8.9.2 were three questions of near-identical length,
  two of which restated each other. Now one question and two conditionals.
- "simply" removed from "The device simply has not been told to connect".
- "Treat them as opposite ends of the pipeline" kept, but the sentence before it
  now states both codes positively rather than as "not that delivery is broken".
- "To force the slow path deliberately, note that..." was a near-miss opener: the
  sentence that followed described a comparison, not forcing anything. Opener cut.
- "Go look at Orbit, not at MDM. §8.9.2. Confirm fleetd is checking in at all
  before touching anything MDM." collapsed to two clauses; the third restated the
  first.
- Grammar: "Two enrollment subkeys ... means" → "mean".

## Heading renamed
- "### Why there is no push" → "### Wake without a push service". Zero inbound
  anchors anywhere in `manual/`, so no links to update. The eleven numbered
  subsection headings are untouched, so every `§8.9.x` cross-reference in this
  file and in 8.1, 8.6, 8.8, 8.10 and 1.2 still resolves.

## Term flags added
- `[SCEP]()` in 8.9.8, where WSTEP is described as its counterpart. SCEP is
  already flagged in 8.6, and the convention in this manual is one flag per
  section per term (ADE, VPP, DEP are each flagged in several sections).
- `[node key]()` in the 8.9.7 enrollment table. Already flagged in 8.3 and 8.4.
- Everything else was glossed in place instead: OMA-DM, SyncML, MS-MDE2, WSTEP,
  OOBE, Autopilot, ADMX. CSP was already defined in 8.9.6, so the earlier uses
  now carry a `§8.9.6` pointer.
- ESP: the acronym does not appear in this section. The version-notes row spells
  out "Enrollment Status Page", so there was nothing to flag and nothing added.

## Keep-list items absent from the section
- **An event log channel name.** §8.9.10 states that none is documented and
  asserts none. Nothing added.
- Everything else on the keep-list is present: both `Poll` intervals, the
  `windows_mdm_sync` capability and the config check-in behaviour, all four error
  codes and both code tables, `dsregcmd /status`, the registry paths, the Entra
  JWKS URL, `mdm_windows_profile_manager`, `LocURI` / `<Format>` / reserved
  LocURIs / ADMX ingestion, `mdmregistration.dll`, and every table and column.

## Facts I did not change but want to flag
1. **Two different renewal periods.** The certificate policy offers a 180 day
   renewal period while the provisioning document written to the device says 365
   days. Both were in the draft and both are preserved. They may both be correct
   (different fields, different consumers), but a reader comparing them will
   notice. Worth one line of explanation from someone who can check.
2. **`Renewal retry interval: 4`** has no unit anywhere in the verified material.
   Preserved, now labelled as unit-unknown rather than presented as a bare number.
3. **fleetd 1.57.0** as the version that introduced on-demand Windows MDM sync
   came from a CHANGELOG entry, which is the same source class that produced the
   bogus 4.89.2 stamp. The release number itself is plausible and was left alone,
   but it is the one remaining version claim in the section that has not been
   confirmed against a release tag.

## Counts
Before: 698 lines. After: 671 lines.

Citations removed, counted by occurrence:
- **Path-based: 21.** The brief's `server/mdm/microsoft/...` grep matches 13 of
  them; the other 8 are `server/service/*`, `server/fleet/*`,
  `server/datastore/mysql/schema.sql`, `cmd/fleet/cron_registration.go`, and the
  `docs/*` paths.
- **Bare filenames with no directory: 25** occurrences over 6 distinct names
  (`CHANGELOG.md` ×9, `windows-autopilot.md` ×7,
  `windows-mdm-glossary-and-protocol.md` ×4, `windows-mdm-architecture.md` ×2,
  `schema.sql` ×2, `syncml.go` ×1).
- **Bare Go identifiers: 49** occurrences over 48 distinct names (19 `CmdStatus*`,
  7 `CmdAlert*`, 5 `MDE2*Path`, 3 `Fleet*TargetLocURI`, 3 `Policy*`, 3 `Wstep*`,
  `DocProvisioningAppProviderID` ×2, plus `CapabilityWindowsMDMSync`,
  `reconcileWindowsMDMPollSchedule`, `CronMDMWindowsProfileManager`, `IsADMX`,
  `Equal`, `EnrollmentVersionV4`, `RegisterDeviceWithManagement`).

Total: 95 occurrences removed. Zero em-dashes, zero banned words. The remaining
four instances of "only" each carry the contrast the sentence depends on.
