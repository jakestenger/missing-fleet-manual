# Part IV visual candidates

Seven new editable SVG diagrams, pending the final manual-wide review. Published chapter prose and images are unchanged.

Run `python3 research/visual-reviews/part-4/render-diagrams.py` to render the diagrams with the Part 0–1 primitives. Requires Inter, Roboto Mono, rsvg-convert and cwebp. Chapter prompts, editorial payoffs and candidate references are in briefs.json.

Source checks against the surrounding chapters preserve the distinction between local accounts and device mappings; rejection of a whole oversized host result versus later estate-wide trimming; the policy population denominator; vulnerability provisioning, loading and matching; missing uptime buckets; per-host query denylisting; and the critical-only refetch path. These are illustrations of the current manuscript, not a fresh release audit.

The 4.6 prompt now explicitly requires denylisting to be enabled. Its coverage-gap callout is an editorial explanation outside the report collector, not an invented Fleet UI status or a message sent by the host. Figure 4.2 does not imply that the 500 retained rows must all come from the example host. Figure 4.5 uses illustrative hourly slots and retains the default three-hour display aggregation note; missing observations are never charted as zero uptime. Figure 4.7 uses asset_tag as an example query name, with platform compatibility left to the author.

All seven rendered candidates were inspected at 720 px. Layout corrections separated labels from connectors and moved row marks inside their source cards. Grayscale checks covered policy populations and uptime history. The figures retain distinct boundaries, labels and line styles without relying on color.

Validation: production website build, all 83 chapter link checks, em-dash and diff whitespace checks, seven candidate/source pairs, native SVG XML and minimum 28 px typography, terminology, and unchanged visible chapter prose.
