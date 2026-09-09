# Part III visual candidates

Ten candidates: nine new editable SVG diagrams and one built-in image-generation replacement for the fleetd update-check diagram. All remain pending the final manual-wide review. Published chapter prose and images are unchanged.

Run `python3 research/visual-reviews/part-3/render-diagrams.py` to render the nine diagrams. It imports the reviewed Part 0–1 primitives and requires Inter, Roboto Mono, rsvg-convert and cwebp. The raster replacement's complete generation/edit prompts are in raster-prompt-history.json. Chapter-local prompts, editorial payoffs, and candidate references are recorded in briefs.json.

The diagrams preserve separate agent and MDM evidence, the macOS migration's three re-enrollment experiences, the external receiver's responsibility for old-MDM release, Orbit's fatal metadata-check branch, Android ownership boundaries, and ChromeOS's node-key reporting path. The iOS/iPadOS brief was clarified to state that lock and wipe require Premium wherever supported, including company-owned URL wipe. This follows the existing chapter's explicit qualification.

Rendered review corrected labels crossing connectors, a dangling MSI connector, an update-bridge route that could bypass its first verification checkpoint, and an ambiguous update-check annotation. Native diagrams were inspected at 720 px, including grayscale spot checks for the migration, MSI, iOS/iPadOS, and ChromeOS figures. The raster update-check replacement was inspected for its distinct scales and non-causal annotation leader. Inspect raster typography at the final print size with the collection.

The two Windows lanes are conditional examples, not a guarantee of enrollment timing; the signed-in-user completion and 90-second agent-check grace remain in prose. The Orbit bridge retains the chapter's distinction between migration code in 1.38.0 and the documented 1.38.1 bridge. No fresh release audit is claimed.

Validation passed: production website build; all 83 chapter link checks; em-dash and whitespace checks; ten candidate/source pairs; native SVG XML, minimum font size and terminology; unchanged visible chapter text.
