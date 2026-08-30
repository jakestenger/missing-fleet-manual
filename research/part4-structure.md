---
part: "IV. Know your devices"
agreed_on: 2026-08-27
agreed_with: codex gpt-5.6-sol
verified_against: fleet-v4.90.1 (dd0200f062)
---

# Part IV structure, agreed 2026-08-27

> **Historical numbering.** This document predates the chapter renumbering of 2026-08-30 (P6 structural moves); section numbers in it are the old ones. The renumber map in `section-notes/README.md` translates them to the current numbering.

Settled before drafting, with the independent reviewer, rather than discovered chapter by chapter. Full exchange at `reviews/2026-08-27/part4-structure/structure.out`.

## What I proposed and what came back

The reviewer agreed with four of my five re-scopings and disagreed with one, for a reason I had missed.

**Agreed.** Re-scoping 4.5 away from single-host status, which 1.2, 4.1 and 8.1 already cover, and toward fleet-wide monitoring. Leading 4.1 with the *mechanism*, the fixed set of detail queries, rather than a list of fields. Leading 4.4 with the deployment-history trap on `enable_software_inventory`. Leading 4.2 with the storage model, which I got wrong twice while writing 1.1.

**Disagreed, and it was right.** I wanted to keep 4.7 as a custom-tables-and-plugins chapter. Building osquery plugins is too specialised to take a seventh of Fleet's reading half, and the outline omitted the mechanism most administrators would actually reach for: **`features.additional_queries`**, which appends administrator-defined detail queries and ingests their results into the host's `additional` data. The chapter becomes **Extend Fleet telemetry**, built around a hierarchy of extension points from lightest to heaviest, with plugins at the far end.

`features.detail_query_overrides` sits alongside it and is **not** a peer: Fleet's own contributor documentation calls it a debugging tool and warns it can break host-data ingestion. It belongs in the chapter as an escape hatch with that warning attached, not as an option.

## Seven subjects the outline did not name

1. **Reading at scale.** Host-summary counts, filters, labels as population lenses, pagination, API retrieval, CSV, `fleetctl`. Population material into 4.5, stored-report retrieval into 4.2.
2. **Field provenance and four independent freshness clocks.** `seen_time`, `detail_updated_at`, `label_updated_at` and `policy_updated_at` are stored separately and mean different things, and a report row carries its own fetch time. The model goes in 4.1 and is applied again in 4.2 and 4.3.
3. **Users against people.** Local host users come from platform-specific queries with system accounts filtered out; device mappings are separately sourced email-to-host relationships. Both in 4.1, explicitly answering different questions.
4. **Mobile and ChromeOS provenance.** iOS and iPadOS detail arrives through enrollment and MDM `DeviceInformation`; Android status reports populate hardware, OS, storage and timing; ChromeOS uses the extension's virtual tables. Field sources in 4.1, query limits in 4.2, software sources in 4.4.
5. **Historical data, and a trap inside it.** This tag registers two datasets, uptime and CVE. **Uptime history records which hosts were online in time buckets; it is not a history of the boot-duration `uptime` field**, which is the obvious wrong reading. Uptime history into 4.5, vulnerability exposure history into 4.4.
6. **Query errors against empty answers.** "No rows" and "could not execute" are different states, and the difference matters most for policies, labels and ChromeOS. Reading semantics in 4.2 and 4.3; diagnosis stays in Part VIII.
7. **The extension hierarchy** as an ordered choice: ordinary report, then policy or label, then `additional_queries`, then a custom table or plugin.

## Boundaries agreed with neighbours

Enrollment stays in Part III. Log destinations stay in 2.5. Anything that **changes** a device is Part V. Single-host channel diagnosis, watchdog incidents and forensic confirmation stay in Part VIII. The complete per-feature platform matrix is A.2; Part IV keeps only the differences that change how a reading is interpreted.

## Writing order

Publication order, 4.1 through 4.7, because each chapter supplies vocabulary the next relies on. The reviewer considered moving 4.6 ahead of 4.3 and rejected it: a policy author needs result semantics and basic query discipline, not advanced joins and watchdog analysis.

## The agreed headings

| | Chapter | Sections |
|---|---|---|
| 4.1 | Understand host data, vitals, and inventory | How Fleet builds and refreshes a host record; identity, hardware, OS and network; users, device mappings and certificates; desktop against mobile, Android and ChromeOS coverage; judging freshness, absence and unknown values |
| 4.2 | Run queries and read reports | Execution, storage and forwarding; live, saved and scheduled; designing and scoping a report; results, timestamps, errors and clipping; sharing, retrieving and exporting; verifying query impact |
| 4.3 | Use policies for compliance | Pass, fail and unknown; policy type, query and platform; scoping with fleets and labels; host status, counts and freshness; descriptions and resolutions; outcomes and automations |
| 4.4 | Understand software and vulnerabilities | Verify inventory before interpreting absence; inventory and Fleet-maintained app metadata; platform sources, coverage and freshness; vulnerability matching and metadata; filtering, prioritising and exposure history; handing findings to remediation |
| 4.5 | Monitor fleet-wide state | Dashboard counts and host-summary signals; segmenting with fleets, filters and labels; fleet-wide agent, enrollment and MDM posture; uptime and vulnerability trends; reading at scale through API, CSV and `fleetctl`; the host-status webhook; a recurring operational review |
| 4.6 | Advanced osquery: query design, tables, and performance | Cost before syntax; choosing, constraining and joining tables; time, platform and osquery-version differences; testing on representative hosts; query statistics, watchdog and denylisting; a reusable report library |
| 4.7 | Extend Fleet telemetry | Choosing the lightest extension point; custom host data with additional queries; detail-query overrides as a debugging escape hatch; when a custom table or plugin is necessary; designing a stable schema; building, distributing, securing and testing; versioning and operating custom telemetry |

## How these get written

One chapter at a time. Each is drafted, sent for **one** review, corrected, and only then is the next started. The review asks the standard questions and one more: whether the chapter gives an administrator a complete enough picture to learn and master this part of Fleet, or leaves a subject out.
