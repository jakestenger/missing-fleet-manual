# Part 0–1 visual review

Prepared 2026-09-08 on `feature/part-0-1-visuals`, branched from `feature/visual-brief-refinement` at `702a5a5`.

Open `index.html` for all nine candidates at 720 px reading width. It includes a grayscale toggle, expanded view, and the previous labels diagram for comparison. As of 2026-09-09, seven figures are installed in chapters 0.1, 0.2 and 1.1–1.4 in both editions. The two candidates for 1.5 and 1.6 remain pending. See [installation progress](../installation-progress.md).

Seven new technical diagrams were authored as editable SVG from the chapter briefs. `render-diagrams.py` regenerates their PNG and lossless WebP exports using Inter, Roboto Mono, `rsvg-convert`, and `cwebp`. The maintenance illustration and existing labels-diagram replacement used the built-in image-generation tool; their PNG masters and lossless WebP exports are included. The illustration uses the existing introduction hero as a visual reference. `briefs.json` records the self-contained chapter briefs and editorial payoffs; `raster-prompt-history.json` records available image-tool prompts for the selected raster work.

Fleet means the company, software product, or server. Host groups are lowercase fleet/fleets, including titles and labels. Literal API identifiers keep their actual spelling.

Rendered candidates were inspected at 720 px, checking labels, containment, arrow direction, and conditions against the current chapters and their existing evidence. This is not a fresh release audit. Check intended print size when the book's print layout is fixed. The generated labels replacement still has a softer panel finish and different typography than the SVG family; that consistency is an open review point.

For the remaining candidates after review: refine any rejected candidates; copy accepted WebP assets to the chapters' stable filenames; activate new Markdown references; update alt text to match the selected art; perform each brief's proposed prose consolidation without losing exceptions or accessible explanations; only then mark IMAGE-OK.

Original production validation (2026-09-08): the website production build passed, all 83 chapter link checks passed, the em-dash check passed, and `git diff --check` passed. All nine candidate files exist, SVG XML parses, and visible chapter content matches the branch base after removing HTML comments. The nine collection-wide IMAGE-REDO markers remain intentionally pending. Gallery browser inspection was unavailable: localhost timed out and the browser policy blocks local file URLs. The artwork itself was inspected from its rendered files; the saved HTML gallery can be opened locally by the reader.
