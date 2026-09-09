# Artwork installation and editorial review

Updated 2026-09-09. Seven of the 108 produced figures are installed in the live 4.91 and frozen 4.90 editions; 101 candidates remain. The separately planned 5.5 screenshot still needs an authentic capture. “Installed” means the chapter has a visible image reference, meaningful alt text, an IMAGE-OK brief, and the reviewed WebP asset. Production galleries alone do not count as installation.

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
