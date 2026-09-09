# Part II visual candidates

Current status (2026-09-09): six figures are installed in chapters 2.1 and 2.10–2.13 in both editions; eight remain pending. See [installation progress](../installation-progress.md). The notes below record the original production handoff.

Thirteen new diagrams and one Apple credential renewal replacement. All fourteen were rendered and inspected against their chapter briefs; the new diagrams were checked at 720 px. Candidate status remains pending the final joint review.

The native diagrams reuse the Part 0–1 drawing primitives; run `python3 research/visual-reviews/part-2/render-diagrams.py` from the repository. It requires the sibling Part 0–1 source, Inter, Roboto Mono, rsvg-convert, and cwebp. The Apple credential replacement used the built-in image-generation tool; its complete production/edit prompts are recorded in raster-prompt-history.json.

The ingress brief was corrected against appendix a.8: Windows protocol paths are under `/api/mdm/microsoft/`, so an `/api`-only rule must not be shown rejecting that lane. The uncovered Apple protocol lane is stopped. No new assertion about route authentication was introduced.

Review refinements included label/arrow separation, visible account-creation connectors across boundaries, separate token and certificate time scales, and preserved qualifiers on async processing, certificate identity, template licensing, and renewal scope. Rendered diagram text uses Fleet for product/server/company and lowercase fleet/fleets for host groups. The raster renewal image uses a different typographic treatment; review it at intended print size with the rest of the collection.

Published images, active Markdown references, and visible prose remain unchanged. Full briefs and editorial consolidation notes are in briefs.json and in chapter comments. Perform installation and prose consolidation only after final review.

Validation passed: production website build; all 83 chapter links; em-dash and diff whitespace checks; 14 candidate/source pairs; native SVG XML, minimum font size, and terminology assertions; unchanged visible chapter text.
