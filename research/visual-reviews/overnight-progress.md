# Overnight visual production

Authorized by Jake on 2026-09-08: finish remaining parts and appendices; commit each completed part; review together when the entire manual is complete. He liked Part 0–1. Continue on `feature/part-0-1-visuals`; do not push.

Heartbeat: `complete-fleet-manual-visuals-overnight`. All independent artwork is complete; pause the heartbeat for the external capture requirement and final joint review.

## Scope and workflow

- Part 0–1: nine candidates finished; Jake approved their direction. Existing published images/prose remain unchanged until final installation. Source and gallery: `part-0-1/`.
- `remaining-briefs.json` inventories 100 TODO/REDO comments across Parts II–VIII and appendices, including older pending comments. Inspect old comments to distinguish real screenshot requirements from diagrams. Do not manufacture screenshots.
- Per-part directories: `part-2/` through `part-8/`, then `appendices/`. Save SVG source when authored, rendered PNG masters, lossless WebP, chapter briefs, and a review gallery. Use the Part 0–1 SVG renderer/design as the starting point, adapting layout to the relationship rather than forcing a template.
- Add terminology and candidate location to chapter comments without changing visible prose. Keep TODO/REDO pending until final joint review. Preserve all already-OK images.
- Fleet = company/product/server. Host groups = lowercase fleet/fleets, even in headings. Preserve literal API identifiers.
- Read each surrounding chapter and relevant evidence, inspect each rendered candidate at 720 px, and correct wrong topology, cropped text, ambiguous containment, and small labels. Keep exact conditions.
- Built-in imagegen is required for raster edits/illustrations. Do not use an API fallback without Jake asking. Technical diagrams can be authored directly as SVG.
- Commit each completed part after checks, including this progress update. Do not include unrelated private-repo edits.
- Deliverables copy: `/Users/jake/Documents/Codex/2026-09-08/ca/outputs/`. Maintain a whole-manual gallery as parts finish. Browser UI preview previously could not access localhost and blocks file URLs; inspect rendered files directly. This does not prevent producing review files.

## Progress

| Batch | Pending comments | Status | Commit |
|---|---:|---|---|
| Part 0–1 | 9 | Completed baseline; direction approved | `2a1c793` |
| Part II | 14 | Completed candidates; final review pending | `d857e42` |
| Part III | 10 | Completed candidates; final review pending | `b3cdd13` |
| Part IV | 7 | Completed candidates; final review pending | `e1f047e` |
| Part V | 18 | 17 candidates ready; 1 authentic capture outstanding | `6b173c1` |
| Part VI | 11 | Completed candidates; final review pending | `2d35887` |
| Part VII | 15 | Completed candidates; final review pending | `0e1274d` |
| Part VIII | 15 | Completed candidates; final review pending | `bbcc437` |
| Appendices | 10 | Completed candidates; final review pending | `5e0f9bc` |

## Blockers

Part V’s 5.5 My Device screenshot requires an accessible, consented demo host on Fleet 4.90.0 with Fleet Desktop and self-service configured. No suitable capture was found in the repos or available app/browser surfaces, and the local Docker daemon is unavailable. `part-5/capture-blockers.json` records the checks and capture plan. All remaining parts and appendices are now complete. Do not retry this capture without a new source. All other pending briefs have candidates.

## Validation

Baseline: production website build, all 83 chapter link checks, em-dash check, and diff whitespace check passed. Native SVG XML and terminology checks passed. Nine redo markers across the collection remain intentionally pending.

## Part II handoff

Completed 14 candidates: 13 native SVG diagrams and one built-in imagegen Apple credential renewal replacement. Sources and gallery are in `part-2/`. `package-review.py part-2 02 "Part II"` packages chapter comments, briefs, the collection gallery and output copy; this utility never installs or approves art. Use it only after actual inspection.

The ingress brief was corrected against appendix a.8 so Windows protocol paths under /api are admitted by an /api-only rule; uncovered Apple paths are stopped. All 14 assets/sources exist; native SVG XML, minimum 28 px labels and terminology checks pass; visible chapter prose equals the prior commit after stripping HTML comments. Website build, 83 chapter link checks, em-dash check and diff whitespace check passed.

Next: Part III's 10 TODO/REDO comments. Read the chapter-local prompts and evidence. Inspect the legacy comments as well as the new one-per-chapter briefs. Continue without waiting for another review. A whole-manual gallery now exists at `research/visual-reviews/index.html`, copied to `/Users/jake/Documents/Codex/2026-09-08/ca/outputs/manual-visuals/index.html`. It currently contains 23 candidates.

## Part III handoff

Completed 10 candidates: nine new native diagrams and one built-in imagegen update-check replacement. `part-3/` contains the gallery, editable SVG sources, raster master, prompts and before-image comparison. The collection now contains 33 candidates. The iOS/iPadOS brief now explicitly applies Premium to lock and wipe wherever supported, including company-owned URL wipe, matching the current chapter.

Review fixed crossing labels, ChromeOS credential/reporting path separation, MSI sentinel failure presentation, the migration observation annotation, and the required verification checkpoint between Orbit rollouts. Native diagrams were inspected at 720 px; grayscale spot checks covered migration, MSI, iOS/iPadOS and ChromeOS. The raster update-check replacement uses a non-causal annotation leader to distinguish an immediate check from entering the scheduled wait.

Validation: website production build passed; all 83 chapter links passed; em-dash and diff whitespace checks passed; ten candidate/source pairs exist; native SVG XML, minimum 28 px fonts, and Fleet/fleets terminology checks passed; visible chapter content is unchanged after stripping HTML comments.

Next: Part IV's seven pending briefs. Continue from the chapter comments and current evidence. No new blockers were found in Part III. Keep working through the remaining parts and appendices, committing each completed batch and saving the output copy. No routine per-part notification to Jake.

## Part IV handoff

Completed seven new native SVG diagrams. The collection now contains 40 candidates. Sources, PNG masters, WebP assets, briefs and gallery are in `part-4/`. The query-denylisting brief now requires `denylist: true` and treats the coverage gap as an explanatory annotation outside the collector, not an invented Fleet UI status or a marker received from the host.

All seven candidates were inspected at 720 px; policy populations and uptime history were checked in grayscale. Layout fixes separated labels from connectors, kept row marks inside source cards, and connected the sync-failure annotation to its source. Validation passed: website production build, 83 chapter links, em-dash and whitespace checks, seven source/asset pairs, SVG XML/fonts/terminology, and unchanged visible chapter prose.

Next: Part V's 18 pending briefs, including a genuine My Device screenshot requirement. Read the chapter-local prompts and evidence before production. Continue independent diagrams if a capture source is unavailable. Keep all candidates pending joint review and commit each completed part. No routine per-part notification.

## Part V handoff

Prepared 17 candidates: thirteen native SVG diagrams and four built-in raster replacements. The collection now contains 57 candidates. One authentic My Device screenshot remains outstanding, with no fabricated placeholder asset. Part V's gallery and the collection index explicitly flag the capture requirement. All independent Part V artwork is complete; **continue Part VI next**, leaving the capture for an available demo source or the final input-needed handoff.

The profile-status prompt and candidate now qualify Verified by platform instead of claiming universal independent confirmation. The OS-update flow folds its numbered process into two rows with evidence-stage references to preserve reading-size labels, and the two-audience diagram uses a taller canvas. Both briefs record those layouts. Generated replacements required corrections to independent setup paths, policy-response destinations, the Android unlock annotation, a Windows success mark and a corrupted subtitle. Final selected raster paths and every correction prompt are saved in Part V.

Native candidates were inspected at 720 px, with grayscale spot checks for Windows deadlines, disk-encryption signals and policy trigger traces. Raster candidates were inspected for labels, scope and topology; final print-size typography remains part of joint review. Validation passed: production website build, 83 chapter links, em-dash and whitespace checks, 17 candidate/source pairs, current packaged briefs, native SVG XML/fonts/terminology, unchanged visible prose, and gallery links including the explicit capture blocker.

`package-review.py` now accepts a part-local `capture-blockers.json` solely for genuine screenshot briefs with documented missing access. It packages available candidates, preserves the outstanding brief, and flags the capture in both galleries. It also keeps the current chapter prompt in inventory/brief records, including production corrections. Do not use blockers to skip ordinary diagram work.

Next: Part VI’s eleven briefs, then VII (15), VIII (15), and appendices (10). Keep the heartbeat active while this independent work remains. Commit each batch and maintain the output copy. No routine per-part notification; final joint review follows the whole collection.

## Part VI handoff

Completed eleven candidates: ten new native SVG diagrams and one built-in raster replacement for the seven-sender comparison. The collection now contains 68 candidates. All Part VI work is packaged and checked; continue Part VII next, then VIII and appendices. The only established capture blocker remains Part V’s My Device screenshot. Keep independent work moving.

The GitOps legacy brief now describes ordered phases with independent API requests rather than suggesting per-file atomicity. The prefix brief focuses on core and activities examples, checked directly in the fleet-v4.90.0 source registration code. The fleetctl outcome brief explicitly detaches ignored delete kinds as a client-only exception, outside its illustrative server-backed lifecycle. Assignment-loss wording clarifies that assignment lists are temporarily cleared under the new-fleet condition. Receiver logic now explicitly decides whether a side effect is needed, while MCP client-access and Fleet API credentials remain separate.

All ten native candidates were inspected at 720 px. Grayscale spot checks covered assignment loss, prefix modules and MCP. Native layout corrections removed crossing labels and cursor/error-route overlaps; the raster was refined to keep ownership bands around the receiver, remove duplicate labels, and preserve exact request/response directions with optional polling separate. Tall native layouts and raster print typography remain part of joint review.

Validation passed: website production build, all 83 chapter links, em-dash and whitespace checks, eleven candidate/source pairs, current packaged briefs, native SVG XML/minimum-font/terminology checks, unchanged visible chapter prose, and gallery links. No assets are installed or marked OK. The repository is ready to continue on the same branch.

Next: Part VII (15 briefs), Part VIII (15), appendices (10), then resolve or hand off authentic captures and perform the final collection audit. Commit each batch and copy the review tree to outputs. The heartbeat remains ACTIVE; do not create another automation or ask for another interim review.

## Part VII handoff

Completed fifteen candidates: fourteen new native SVG diagrams and one built-in raster upgrade-recovery replacement. The collection now contains 83 candidates. Continue Part VIII's fifteen briefs, then the ten appendices briefs. The only documented external blocker remains the authentic Part V My Device capture.

Six legacy prompts were rewritten around the inspected layouts while retaining their technical scope: outcome measurement costs, escrow backup dependencies, independent health signals, per-endpoint connection budgets, certificate renewal consequences, and handover responsibilities. Dense comparisons use taller canvases with readable type. Native inspection corrected arrows crossing labels, kept the three escrow chains separate, and sent unresolved handoff evidence back to the review gate instead of a particular rehearsal.

All fourteen native diagrams were inspected at 720 px; grayscale spotchecks covered outcome costs, connection budgets and renewal. The raster required two corrections to separate its dashed database-restore return from the common acceptance-check connector. Every label and recovery branch was checked at native resolution. Its final page typography, and placement of tall native figures, remain for joint review.

Validation passed: website production build, all 83 chapter links, em-dash and diff whitespace checks, fifteen candidate/source pairs, fourteen valid SVGs with minimum 28 px labels, terminology, current chapter comments in packaged briefs, gallery links, and unchanged visible chapter text. All published assets and IMAGE-OK states remain untouched. Part VII is committed separately and the review tree is copied to outputs.

Next: Part VIII (15), appendices (10), final collection audit, then obtain or hand off the genuine capture requirement. During the final audit, reconcile older inventory `brief` text with current chapter comments where needed; Parts II–IV were packaged before the utility began updating this field. Do not regenerate from stale inventory wording. Keep the existing heartbeat active while independent work remains, with no routine per-part notifications.

## Part VIII handoff

Completed fifteen native SVG candidates. The collection now contains 98 candidates. Every figure was inspected at 720 px, with grayscale spotchecks for Windows polling/wake, incident attribution and file-carve authentication. Native refinements kept APNs outside the command path, separated branch labels and restart annotations, and distinguished possible load-balancer destinations from the selected node.

Brief corrections qualify the UUID-present error example, scope half-enrollment to macOS with confirmed absent fleetd, move file-carve authentication cards below the sequence, specify later Idle eligibility after NotNow, and keep fleet scope lowercase. Chapter 8.2's image comments were accidentally inside a shell fence; they now sit before the relevant debug subsection. Shell commands and visible words are unchanged; only whitespace differs after stripping comments.

Validation passed: production website build, all 83 chapter links, em-dash and diff whitespace checks, fifteen complete native source/asset sets, SVG XML/minimum fonts/terminology, and current briefs. The image-redo checker reports nine intentional nonblocking pending markers. Tall figure placement remains for joint review. Part VIII is packaged separately, with the review tree copied to outputs.

Next: ten appendix briefs, then final collection audit and genuine capture handoff. Reconcile older inventory brief text and check all image comments for accidental placement inside code fences. The only external blocker remains the My Device capture. Keep the existing heartbeat active while independent work remains.

## Appendices handoff

Completed ten candidates: nine native SVG diagrams and one built-in Cloud City subject-index illustration. The collection now contains 108 candidates. All independent artwork is complete; the sole missing asset is the authentic My Device screenshot in Part V.

All native figures were inspected at 720 px. Grayscale spotchecks covered file-state replacement, role scope and endpoint allowlists. Corrections removed overlapping labels and clarified that API responses return from Fleet while the client generates GitOps apply output. Briefs preserve lowercase fleet scope and restore full method/path prefixes for the MCP allowlist. The illustration uses the approved Part 0 reference with no text or technical claims.

Validation passed: production website build, 83 chapter links, em-dash and whitespace checks, ten source/asset sets, SVG XML/fonts/terminology, current packaged briefs and unchanged visible chapter content. Existing nonblocking redo markers remain pending. The appendix batch is committed separately and copied to outputs.

Next: final collection audit, synchronize older brief metadata, check prompt placement, then pause the existing heartbeat when only the authentic capture and joint review remain. Prepare a concise final handoff with the collection link and exact capture requirement.

## Final collection audit

108 unique candidates are ready: 97 editable SVG diagrams and 11 raster images across nine batches. Exactly one of the 109 pending image briefs has no candidate: Part V's authentic My Device screenshot. Every source and candidate exists, every gallery link resolves, and all packaged chapter comments match the manuscript. Parts II–IV had 31 stale `brief` fields in both package records and the remaining inventory; these now match the current chapter comments without changing or regenerating artwork.

All 97 SVGs parse and use labels at least 28 px at 1400 px source width. Automated terminology checks found no old team names or capitalized fleet-group labels in native artwork. Every chapter has image comments, none lies inside a code fence, visible manuscript words match the branch base after excluding comments, and all existing published artwork is unchanged. Chapter 8.2 retains only the documented whitespace difference from relocating comments outside a shell fence. All TODO/REDO acceptance states remain pending.

The final appendix production build and repository checks passed. Final metadata-only changes pass whitespace and gallery/source checks. Each part has its own commit, with a final collection-audit commit afterward. The public branch remains feature/part-0-1-visuals; no push or private-repo modification was performed by overnight production.

The final review package is in outputs/manual-visuals/index.html, with REVIEW.md describing counts, commits, review scope and the capture requirement. Pause the heartbeat now: independent production is exhausted. Resume only for new capture access, joint review or requested revisions.
