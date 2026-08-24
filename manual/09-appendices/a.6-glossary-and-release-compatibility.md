---
title: "Glossary and release compatibility"
chapter: "Appendices and indexes"
section: "A.6"
sidebar_position: 6
status: outline
verified_against: Fleet 4.90.1
verified_on: 2026-08-24
verified_source: "partial: the 4.82.0 rename is verified at git tag fleet-v4.90.1; the rest of this appendix is an outline"
---

# Glossary and release compatibility

<!--
Structured placeholder. Replace this outline with release-verified guidance for Fleet 4.90.1.
-->

## Terminology

Entries are added as chapters need them. Terms currently flagged for definition, from the `[term]()` markers in the manual: ADE, DEP, SCEP, VPP, node key, pprof, file carving, dead lettering.

### report, and query

**A report is Fleet's saved, runnable object.** You create it, target it, run it live, or put it on a schedule. Running one ad hoc is a **live report**.

**A query is osquery's mechanism**, and also plain SQL. osquery runs queries: on a schedule, or on demand through its distributed channel.

The two words describe different layers of the same action. Running a live report in Fleet causes osquery to execute a query on each targeted host. Both terms are correct, and which one is right depends on the layer you are talking about.

| You mean | Say | Because |
|---|---|---|
| The Fleet object you saved | report | Renamed in Fleet 4.82.0 |
| Running one ad hoc from Fleet | live report | Renamed in Fleet 4.82.0 |
| osquery's distributed channel | distributed query | osquery's own term, unchanged |
| An entry in `osquery_schedule` | scheduled query | osquery's own term, unchanged |
| The MySQL table | `queries` | The schema was not renamed |
| The Redis key | `live_query` | Internal naming was not renamed |
| SQL text | query | Generic |

Part VIII works at all of these layers at once, which is why both words appear there. Its opening section carries a note explaining the split in context.

## Feature availability

## Version boundaries

## Deprecated names and APIs

### Fleet 4.82.0 renamed teams to fleets, and queries to reports

Released 11 March 2026. From the release notes:

> Renamed teams and queries to fleets and reports in the UI, API, CLI, and GitOps.
>
> Deprecated certain API field names to reflect the renaming of "teams" to "fleets" and "queries" to "reports".

The old field names are **deprecated rather than removed**, so integrations written against the earlier names continue to work. New work should use the current names.

**The rename covered the surfaces administrators touch, and stopped there.** Storage and internal naming kept the original words:

| Surface | Current | Notes |
|---|---|---|
| UI, API paths, CLI, GitOps | fleets, reports | `/api/v1/fleet/reports`, `fleetctl report` |
| API field names | fleets, reports | Old names deprecated, still accepted |
| MySQL tables | `teams`, `queries` | Schema unchanged |
| Redis keys | `live_query` | Unchanged |
| osquery | query | osquery is a separate project and renamed nothing |

This is why documentation, forum posts, and scripts written before March 2026 use the older words for the same things, and why Fleet's own documentation still contains both.

A related change in the same release: `no-team.yml` in GitOps was deprecated in favour of `unassigned.yml`.

## Documentation maintenance
