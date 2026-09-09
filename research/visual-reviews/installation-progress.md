# Artwork installation and editorial review

Updated 2026-09-09. Fifteen of the 108 produced figures are installed in the live 4.91 and frozen 4.90 editions; 93 candidates remain. The separately planned 5.5 screenshot still needs an authentic capture. “Installed” means the chapter has a visible image reference, meaningful alt text, an IMAGE-OK brief, and the reviewed WebP asset. Production galleries alone do not count as installation.

## First editorial batch

Started from `origin/main` at `c0e597d`, then fast-forwarded through Claude’s five ready chapter commits at `93beaba`. Chapter 1.1 came directly from main at the user’s request. Later commits on `style/de-ai-full-manual` were excluded from this batch. The review branch is `review/de-ai-first-five`; the name predates adding 1.1.

| Chapter | Input | Final editorial commit | Installed figures |
|---|---|---|---:|
| 0.1 | `02f1891` | `fcbf9b6` | 1 |
| 0.2 | `e3aeef6` | `890ca88` | 1 |
| 1.1 | `main at c0e597d` | `0d5f743` | 1 |
| 1.2 | `b176883` | `eabd3eb` | 1 |
| 1.3 | `1da6e90` | `0e5a25f` | 2 |
| 1.4 | `93beaba` | `68bb0e7` | 1 |

Each final chapter commit updates both editions. The pass removes repeated rhetorical contrasts, long qualification stacks, redundant summaries, and excessive sentence-length bolding. Commands, reference tables, technical conditions, and accessible explanations remain. The 1.3 repeated inheritance table was consolidated into the earlier table. Renamed headings in 1.2 and 1.4 retain their old anchors.

The installed artwork is in `part-0-1/briefs.json`, with `status: installed after editorial review`. All seven master files match the live and frozen copies byte for byte. The transfer diagram’s Old scope label was moved clear of its connector. Chapters 1.5 and 1.6 are still pending in that gallery.

## Focused factual checks

This was an editorial and illustration review, not a complete release verification. Existing release provenance was retained. Source was read at `fleet-v4.91.0` (`35fc1c0244907c157a64d05d4ec291c0a3a20e32`) and compared with `fleet-v4.90.0` where relevant.

- 0.1: corrected the live coverage statement to Fleet 4.91.0; frozen coverage remains 4.90.0. Reading routes were checked against chapter destinations.
- 1.1: live preview now pins server image `v4.91.0` and compose source `fleet-v4.91.0`; frozen preview keeps 4.90.0. Flag names/defaults were checked in `cmd/fleetctl/fleetctl/preview.go`. Preview was not executed because it starts services and can enroll the workstation. Retained the existing custom-vital timestamp exception.
- 1.2: Online uses the minimum refresh interval plus the buffer, with seen-time/created-time behavior checked in `server/fleet/hosts.go` and `server/datastore/mysql/hosts.go`. The figure distinguishes that signal from MDM command evidence.
- 1.3: transfer cleanup was checked in `server/datastore/mysql/hosts.go`. Key cleanup and archive lookup were checked in `server/datastore/mysql/disk_encryption.go`, unchanged between the two tags. `server/service/hosts.go` tries the newest archived record, rather than searching all older records for a decryptable one; the text now says so. The relevant fallback code is unchanged between tags.
- 1.4: SCIM eligibility, last-global-admin protection, and Premium startup registration were checked in `ee/server/scim/users.go` and `cmd/fleet/serve.go`. Password and API-only accounts retain their separate owner-led retirement requirement.

## Validation

- Docusaurus production build passed for both editions.
- Link/anchor/image checks passed for all 83 chapters in each edition.
- All 14 figure placements and the preserved legacy anchors occur in generated HTML.
- All chapter code fences match the input, except the intentional live 1.1 release pin.
- Every Python check listed in `.github/workflows/pr-check.yml`, plus `check-image-redo.py`, exited successfully. Source-dependent checks used files extracted from the 4.91.0 tag, avoiding a change to the developer’s source checkout. Frequency and cross-reference reports remain advisory. Pending image markers elsewhere remain outside this batch.
- `git diff --check` passed.

For the next batch, start from current main and apply only the chapter commits ready for review. Preserve these final edits when resolving overlaps. Install and verify the corresponding artwork in both editions, commit each chapter separately, and update this ledger before pushing to main.


## Second editorial batch (2026-09-09)

Reviewed the seven chapter commits available when this batch began, through `e389c6b`. Merged that exact tip into `review/de-ai-second-batch`, based on reviewed main at `08cd870`. Later arrivals on Claude’s branch are outside this batch. Eight more figures are installed in both editions: the two remaining Part I diagrams, the ownership map, two Apple diagrams, and the Windows, Android, and CA diagrams. The Part 0–1 gallery is now fully installed; Part II has six installed figures and eight pending candidates.

| Chapter | Claude input | Final editorial commit | Installed figures |
|---|---|---|---:|
| 1.5 | `4d5c54b` | `d2dc557` | 1 |
| 1.6 | `350cbb9` | `95e8634` | 1 |
| 2.1 | `a99530b` | `761dab1` | 1 |
| 2.10 | `b673832` | `6b4e57b` | 2 |
| 2.11 | `8441b82` | `992a025` | 1 |
| 2.12 | `8a7bc74` | `3b1f2bf` | 1 |
| 2.13 | `e389c6b` | `57c8e2d` | 1 |

The prose pass removes repeated announce-then-correct paragraphs, shortens qualification stacks, and makes procedures easier to scan. CA profile variables are now a table, with renewal identifiers and platform placement kept in selectable text. Every code fence is unchanged. The renamed Android companion-app heading retains its former anchor. The live edition keeps the 4.91 MFA event, Apple release action, and Windows default-fleet behavior; the frozen edition retains its 4.90 content.

Two unsupported diagnostic conclusions were softened: a Pending Apple estate with continuing macOS inventory is a reason to check the push certificate, not proof of expiry; Windows enrollment timing remains attributed guidance to test locally, including in the closing edge-case summary. The Windows certificate instructions now explicitly say to track the chosen expiry despite the absence of vendor renewal.

### Focused artwork/source review

All eight rendered candidates were visually inspected for labels, connections, scope, and legibility. No new generation was needed. The Apple replacement separates certificate age from time remaining until token expiry; the old shared timeline is replaced and its alt text updated. The checks below are focused evidence checks, not a complete release re-verification. Historical chapter provenance remains intact.

- **1.5 activity actors:** at `fleet-v4.91.0`, `server/service/apple_mdm.go` records CheckOut with a nil user; `server/activity/internal/mysql/new_activity.go` stores user name/email; `server/datastore/mysql/schema.sql` sets the user foreign key to NULL on deletion. `server/activity/internal/service/service.go` enriches actor type only from users that still resolve. This supports the diagram’s two independent examples.
- **1.6 outage paths:** `server/datastore/mysqlredis/host_cache.go` treats Redis/JSON errors as cache misses and falls through to the database. Other failure paths retain the chapter’s existing evidence and the explicit asynchronous-processing condition. The diagram does not equate an outage with deletion of Redis data.
- **2.1 ownership:** the diagram is an illustrative responsibility record, with no invented provider contract or product behavior. The fillable worksheet and review cadences remain.
- **2.10 stored defaults:** `server/mdm/apple/apple_mdm.go`, `EnsureDefaultSetupAssistant`, creates the stored default only when absent or lacking its token; `RegisterProfileWithAppleDEPServer` reads it back. A/B are illustrative defaults. Renewal timings retain the existing release evidence; `server/service/apple_mdm.go` still defines `scepCertRenewalThresholdDays = 180`.
- **2.11 escrow identity:** `server/service/hosts.go` routes Windows recovery to the configured WSTEP certificate/key; `server/mdm/mdm.go` passes both to PKCS7. The helper and Windows encryption implementation are unchanged between the 4.90.0 and 4.91.0 tags. The dependency pinned in `go.mod`, `github.com/smallstep/pkcs7` at `5e2c6a136dfa`, selects recipients by issuer and serial in `decrypt.go:226-232`. That selection was also inspected directly at the pinned upstream commit.
- **2.12 Android companion:** `server/mdm/android/service/service.go`, `buildFleetAgentAppPolicy`, retains FORCE_INSTALLED, CERT_INSTALL, COMPANION_APP, granted permissions, signing-key pinning, and high-priority updates. The diagram’s Premium condition applies to template creation, not installation of the companion app.
- **2.13 renewal marker:** `server/fleet/certificate_authorities.go` restricts renewal-ID support to NDES, custom SCEP, and Smallstep; DigiCert renewal uses a separate mechanism. `server/service/windows_mdm_profiles.go` checks the preferred or legacy marker in OU. `server/service/mdm_profiles.go` validates companion URL/challenge variables. The diagram is explicitly limited to supported proxied SCEP profile paths.

### Validation

The production build passed with a local `npm ci` dependency installation. An initial attempt using a symlink to another checkout’s dependencies failed during static rendering; no repository code change was needed to resolve that environment issue. All CI Python checks plus `check-image-redo.py` exited successfully, with source-dependent checks pointed at extracted 4.91.0 sources. Link/anchor/image checks passed for all 83 chapters in each edition. All 16 new figure placements and the legacy Android anchor are present in generated HTML. Both edition copies of each image match the reviewed master. Existing IMAGE-OK markers and all 14 chapter code-fence sets are preserved. `git diff --check` passed.
