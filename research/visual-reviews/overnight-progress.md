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
| Part 0–1 | 9 | Completed baseline; direction approved | Baseline commit immediately after this file |
| Part II | 14 | In progress | — |
| Part III | 10 | Pending | — |
| Part IV | 7 | Pending | — |
| Part V | 18 | Pending | — |
| Part VI | 11 | Pending | — |
| Part VII | 15 | Pending | — |
| Part VIII | 15 | Pending | — |
| Appendices | 10 | Pending | — |

## Blockers

None established yet. A My Device screenshot and some older capture briefs require authentic demo UI. Inspect available capture sources when reaching those chapters, document missing access precisely, and continue the diagrams.

## Validation

Baseline: production website build, all 83 chapter link checks, em-dash check, and diff whitespace check passed. Native SVG XML and terminology checks passed. Nine redo markers across the collection remain intentionally pending.
