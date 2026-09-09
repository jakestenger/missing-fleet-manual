# Overnight visual production

Authorized by Jake on 2026-09-08: finish remaining parts and appendices; commit each completed part; review together when the entire manual is complete. He liked Part 0–1. Continue on `feature/part-0-1-visuals`; do not push.

Heartbeat: `complete-fleet-manual-visuals-overnight`, every 30 minutes in this task. Pause it after completion or after all independent work is exhausted and only documented external blockers remain. Do not send routine per-part notifications.

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
| Part V | 18 | 17 candidates ready; 1 authentic capture outstanding | Part V batch commit (see git log) |
| Part VI | 11 | Next batch | — |
| Part VII | 15 | Pending | — |
| Part VIII | 15 | Pending | — |
| Appendices | 10 | Pending | — |

## Blockers

Part V’s 5.5 My Device screenshot requires an accessible, consented demo host on Fleet 4.90.0 with Fleet Desktop and self-service configured. No suitable capture was found in the repos or available app/browser surfaces, and the local Docker daemon is unavailable. `part-5/capture-blockers.json` records the checks and capture plan. Continue Parts VI–VIII and appendices; do not repeatedly retry this capture without a new source. Other legacy capture briefs still need inspection when reached.

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
