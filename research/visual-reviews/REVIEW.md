# Fleet manual artwork review

Current installation status (2026-09-09): seven figures are installed in chapters 0.1, 0.2 and 1.1–1.4 in both editions. Another 101 candidates await installation. See [installation progress](installation-progress.md). The production record below describes the earlier gallery-only handoff.

108 candidates are ready: 97 editable SVG diagrams and 11 raster images. Open `index.html` to browse by part at 720 px, compare replaced images, inspect full-size sources, or switch to grayscale.

All independent production is complete. The only missing image is the genuine **5.5 My Device / self-service screenshot**. It requires a consented demo host with Fleet 4.90.0, Fleet Desktop and self-service configured. Its exact capture plan and observed access blockers are in `part-5/capture-blockers.json`. No product screen was fabricated.

## Local commits

Production branch: `feature/part-0-1-visuals`, descended from `feature/visual-brief-refinement`. The production batches were subsequently merged into `main`; the table records their original commits.

| Batch | Candidates | Commit |
|---|---:|---|
| Part 0–1 | 9 | `2a1c793` |
| Part II | 14 | `d857e42` |
| Part III | 10 | `b3cdd13` |
| Part IV | 7 | `e1f047e` |
| Part V | 17 + one capture outstanding | `6b173c1` |
| Part VI | 11 | `2d35887` |
| Part VII | 15 | `0e1274d` |
| Part VIII | 15 | `bbcc437` |
| Appendices | 10 | `5e0f9bc` |

A final collection audit commit follows these batches to reconcile metadata and save this handoff.

## Review scope

The galleries contain candidates, not installed replacements. Existing published artwork, visible chapter words, and pending approval markers are preserved. The one code-layout repair moves chapter 8.2's image prompt outside a shell fence; command words remain unchanged.

Review the explanatory value and reading flow first, then final page typography, especially raster replacements and tall diagrams. Each brief identifies the prose that can be reduced after acceptance. Exact commands, reference tables, conditions and accessible summaries should stay as text. Fleet names the product/company/server; fleet and fleets name host groups.

Every candidate received visual inspection. Native diagrams were checked at 720 px with representative grayscale checks per batch. The final collection audit verifies 108 unique source/candidate sets, gallery links, current chapter prompts, all 97 SVGs and minimum fonts, terminology, prompt placement, and preserved published content. Production website build, 83 chapter link checks, em-dash and whitespace checks pass. The nine existing IMAGE-REDO markers are intentionally pending and nonblocking.

This was visual production from the manual's current content and evidence, not a complete new-release technical verification. Per-part READMEs record meaningful corrections and remaining layout considerations.
