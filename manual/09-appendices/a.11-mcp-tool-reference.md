---
title: "Fleet MCP tool reference"
chapter: "Appendices and indexes"
section: "A.11"
sidebar_position: 11
status: drafting
verified_against: Fleet 4.90.1
verified_source: "drafted against fleet-v4.90.1 (dd0200f062), reading cmd/fleet-mcp at that tag: the tool registrations in mcp_tools_hosts.go, mcp_tools_queries.go, mcp_tools_policies.go and mcp_tools_inventory.go, the argument parsing in mcp_helpers.go, and the server instructions in mcp_server.go. Citation ledger at research/section-notes/a.11-notes.md."
reviewed_by:
reviewed_on:
further_reading:
  - https://github.com/fleetdm/fleet/tree/fleet-v4.90.1/cmd/fleet-mcp
  - https://modelcontextprotocol.io/
feature_requests:
  labels: []
  match: []
  exclude: []
---

# Fleet MCP tool reference

![Reference](../_assets/icons/reference.svg) The exact tools the Fleet MCP server exposes to an AI assistant, and the arguments each one takes. [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md) is the chapter: it explains what the server is, how to build and connect it, and the security model this reference assumes. The REST routes underneath these tools are [a.8](a.8-api-action-and-endpoint-reference.md). This appendix is the argument-level contract, grouped by the four domains the server registers: hosts, queries, policies and vulnerabilities, and inventory.

Twenty tools. One of them, `run_live_query`, changes devices; every other tool only reads. The read/destructive marks below are the advisory annotations the server sends to a cooperating client, not a control Fleet enforces — the enforced boundary is the Fleet role of the token the server holds ([6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md)).

## Arguments common to several tools

![Reference](../_assets/icons/reference.svg) The host-facing tools share one filter vocabulary, resolved server-side. Learn it once and it reads across the tables below.

| Argument | Meaning | Notes |
|---|---|---|
| `query` | Substring match | Covers hostname, serial, primary IP, hardware model, and host-user fields (username, email, IdP group). Does not match display name. |
| `fleet` | Restrict to one fleet by name | Resolved to a fleet id server-side. |
| `label` | Restrict to one label by name | Resolved to a label id. Single label only; Fleet does not intersect multiple labels. |
| `platform` | `macos` / `windows` / `linux` / etc. | A standard Fleet host filter. |
| `status` | Host status (online, offline, and the rest) | A standard Fleet host filter. |
| `policy_id` + `policy_response` | Hosts on one side of a policy | `policy_response` is `passing` or `failing` and requires `policy_id`; the orphan is rejected at the server. |
| `per_page` | Page size for host listings | Clamped to a maximum of 200. |
| `host_id` vs `identifier` | Which host | A numeric `host_id` is exact. An `identifier` (hostname, UUID, serial, computer name, or a fuzzy substring) may match several hosts, in which case the tool returns a candidate list to disambiguate; re-call with the chosen `host_id`. |
| `cve_id` | A CVE | Must match `CVE-YYYY-NNNN` (`^CVE-\d{4}-\d{4,}$`); a malformed value is rejected before Fleet is called. |

## Hosts

![Reference](../_assets/icons/reference.svg) Reading enrolled hosts, their policy results, and fleet-wide counts. All read-only.

| Tool | What it does | Arguments |
|---|---|---|
| `get_endpoints` | List and filter enrolled hosts; the returned `total` reflects the filtered scope | `fleet`, `platform`, `status`, `query`, `label`, `policy_id`, `policy_response`, `per_page` (all compose) |
| `get_host` | Full detail for one host, including labels, fleet, serial, primary IP, platform | `host_id` (preferred) or `identifier` |
| `get_host_policies` | Every policy applied to one host with its pass/fail/not-run response, plus a summary block | `host_id` or `identifier`; optional `response` to narrow to passing or failing |
| `get_total_system_count` | Count of active enrolled systems | none |
| `get_aggregate_platforms` | System counts broken down by OS platform | none |
| `get_fleets` | List all fleets with ids and names | none |
| `get_labels` | List all labels | none |

## Queries

![Reference](../_assets/icons/reference.svg) The saved-query list, the osquery schema, and running live osquery. `run_live_query` is the one destructive tool; the rest are read-only.

| Tool | What it does | Arguments |
|---|---|---|
| `get_queries` | List saved queries, global and per-fleet | none |
| `get_osquery_schema` | Canonical osquery table schema, source of truth for column types | `platform` (returns a curated short list) or `tables` (comma-separated, for full coverage of any of the 360+ tables) |
| `refresh_osquery_schema` | Force an immediate refresh of the in-memory schema from Fleet's published schema file | none |
| `get_vetted_queries` | A library of vetted, production-safe CIS-8.1 policy queries for macOS, Windows and Linux, read from data bundled into the server | none |
| `prepare_live_query` | Step 1 of 2: validate targets and return the schema for the platforms in scope, so the assistant can author valid SQL | the target filters (`hostnames`, `host_ids`, and the intersecting host filters above) |
| `run_live_query` | Step 2 of 2: run an osquery SQL statement against live devices. **Destructive.** Re-resolves its own targets when it runs; SQL is checked against canonical column types first, and a text-column-versus-bare-integer comparison is rejected | `sql`; direct selectors `hostnames` / `host_ids`; intersecting `fleet`, `platform`, `label`, `status`, `query`, `policy_id`, `policy_response`, `cve_id` |

## Policies and vulnerabilities

![Reference](../_assets/icons/reference.svg) Policy pass/fail counts and the hosts on either side, and the hosts a CVE affects. All read-only. The host-listing tools here return a capped page with no running total; read a count question from the counting tools rather than the length of a list (see [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md) on completeness limits).

| Tool | What it does | Arguments |
|---|---|---|
| `get_policies` | List all policies, global and per-fleet, with pass/fail host counts | none |
| `get_policy_compliance` | Pass/fail counts for one policy; global aggregate by default | `policy_id`; optional `fleet` to scope to one fleet |
| `get_policy_hosts` | The hosts that pass or fail a given policy | `policy_id`, `policy_response`; optional `fleet`, `platform`, `label`, `status`, `query` (compose) |
| `get_vulnerability_impact` | Aggregate count of systems affected by a CVE; can report a lower bound at the internal host ceiling | `cve_id` |
| `get_vulnerability_hosts` | The specific hosts affected by a CVE, composed across several Fleet calls because Fleet's single-filter path is unreliable | `cve_id`; optional `fleet`, `platform`, `label`, `status`, `query` |

## Inventory

![Reference](../_assets/icons/reference.svg) Stored software and local user accounts, read from Fleet's cached inventory so they answer for offline hosts. Both read-only. The freshness of these answers is the last successful inventory collection, not the last check-in ([4.1](../04-know-your-devices/4.1-understand-hosts-vitals-and-inventory.md), [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md)).

| Tool | What it does | Arguments |
|---|---|---|
| `get_software` | Stored software. Two auto-selected modes: **per-host** with a host argument returns every package on that host with versions, source and matching CVEs; **cross-host** with no host argument returns software titles seen across hosts | per-host: `host_id` or `host_identifier`; cross-host: optional `fleet`, `vulnerable`, and `platform` (which requires `fleet`); `source` (e.g. `apps`, `deb_packages`, `chrome_extensions`) and `query` filter client-side |
| `get_host_users` | OS-local user accounts on one host as inventoried by osquery: uid, username, type, groupname, shell | `host_id` (preferred) or `host_identifier`; optional `query` to filter the returned users |

## The schema-first workflow is advised, not enforced

![Reference](../_assets/icons/reference.svg) The server tells a cooperating client to fetch the schema before writing SQL and to confirm before running a live query, and it advertises the read/destructive annotations above. These are instructions to the assistant, not gates the server keeps: a client can ignore them, and `run_live_query` resolves its targets and validates its SQL itself at call time regardless. The controls that hold are the token's Fleet role and, on the agent, osquery's own table controls — both covered in [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md).
