# Part VII visual candidates

Fifteen candidates for the final joint review: fourteen editable SVG diagrams and one built-in image-generation replacement. `index.html` presents the collection at 720 px, with expansion and grayscale controls. The chapter comments link to candidates; published artwork and visible prose remain unchanged.

`render-diagrams.py` uses the approved shared Fleet primitives to write SVG, PNG and lossless WebP. `briefs.json` retains the current chapter comments. `raster-prompt-history.json` records the upgrade diagram's initial edit and two connector corrections; `raster-selections.json` identifies the selected master. The previous raster is included for comparison.

The six older diagram briefs were adapted to the actual reading-size layouts. The outcome comparison uses rows with cost chips; the observation diagram separates its five failure lanes from telemetry sources; connection budgets remain separate by endpoint; the escrow and renewal comparisons preserve all three dependency chains; the handover diagram emphasizes ongoing responsibilities. These are editorial adaptations against the current chapters, not new release verification.

Every native diagram was inspected at 720 px. Grayscale spotchecks covered measurement costs, connection budgets and credential renewal. Review corrections cleared labels from connectors, kept Windows escrow separate from the Fleet server private key, and returned incomplete handoff evidence to the review gate. The raster's dashed restore arrow now originates exclusively at database restore and bypasses all shared acceptance paths. Raster labels and topology were inspected at its native resolution; final page typography and tall-diagram placement remain for joint review.

Validation: production website build, all 83 chapter link checks, em-dash check and diff whitespace check passed. Candidate/source pairs, SVG XML and minimum 28 px native labels, terminology, current packaged comments, local gallery references and unchanged visible chapter prose were checked. No artwork is installed or marked IMAGE-OK, and nothing is pushed.
