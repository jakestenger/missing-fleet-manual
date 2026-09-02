---
title: "Fleet MCP tool reference"
chapter: "Appendices and indexes"
section: "A.11"
sidebar_position: 11
status: drafting
verified_against: Fleet 4.90.1
verified_on: 2026-09-01
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

Every tool table below has a **Fleet routes** column, for building or auditing an endpoint allowlist on the server's API-only token ([6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md)). Routes omit the common `/api/v1/fleet` prefix; Fleet's allowlist match is version-agnostic (`v1`, `latest`, and dated versions all fingerprint the same route), so don't pin an allowlist entry to one literal version ([a.8](a.8-api-action-and-endpoint-reference.md)). Every connection also calls `GET /me` once at startup, to identify the token and fail closed if it's invalid.

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

| Tool | What it does | Arguments | Fleet routes |
|---|---|---|---|
| `get_endpoints` | List and filter enrolled hosts; the returned `total` reflects the filtered scope | `fleet`, `platform`, `status`, `query`, `label`, `policy_id`, `policy_response`, `per_page` (all compose) | `GET /hosts`, `GET /hosts/count`; `GET /labels` and `GET /fleets` to resolve a `label`/`platform`/`fleet` name to an id; `GET /labels/{id}/hosts` when a `label` or `platform` filter is set |
| `get_host` | Full detail for one host, including labels, fleet, serial, primary IP, platform | `host_id` (preferred) or `identifier` | `GET /hosts/{id}`, or `GET /hosts/identifier/{identifier}` (falls back to `GET /hosts` first when the identifier is a fuzzy match) |
| `get_host_policies` | Every policy applied to one host with its pass/fail/not-run response, plus a summary block | `host_id` or `identifier`; optional `response` to narrow to passing or failing | `GET /hosts/{id}` for a numeric `host_id`; for `identifier`, a query-first `GET /hosts` search, then either `GET /hosts/{id}` (unique match) or `GET /hosts/identifier/{identifier}` (fallback) |
| `get_total_system_count` | Count of retained enrolled host records visible to the API token, across all statuses | none | `GET /hosts/count` |
| `get_aggregate_platforms` | System counts broken down by OS platform | none | `GET /host_summary` |
| `get_fleets` | List all fleets with ids and names | none | `GET /fleets` |
| `get_labels` | List all labels | none | `GET /labels` |

## Queries

![Reference](../_assets/icons/reference.svg) The saved-report list (`get_queries`), the osquery schema, and running live osquery. `run_live_query` is the one destructive tool; the rest are read-only.

| Tool | What it does | Arguments | Fleet routes |
|---|---|---|---|
| `get_queries` | List saved reports, global and per-fleet | none | `GET /reports`, `GET /fleets` (to enumerate fleets), then `GET /reports` scoped per fleet |
| `get_osquery_schema` | Osquery table schema for column types, refreshed from Fleet's `main` branch rather than pinned to your release ([6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md)) | `platform` (returns a curated short list) or `tables` (comma-separated, for full coverage of any of the 360+ tables) | none (reads a schema file fetched from GitHub, not from Fleet; [a.6](a.6-glossary-and-release-compatibility.md)) |
| `refresh_osquery_schema` | Force an immediate refresh of the in-memory schema from Fleet's published schema file | none | none (same GitHub-sourced schema as above) |
| `get_vetted_queries` | A bundled library of CIS-8.1-derived policy queries for macOS, Windows and Linux, transcribed verbatim from the benchmarks; nothing in the tagged source executes or validates them, so treat the library as a starting point to test rather than a pre-validated one | optional `platform` (`darwin`/`macos`, `windows`, `linux`, or `all`; defaults to `all`) | none (bundled into the server binary) |
| `prepare_live_query` | Step 1 of 2: validate targets and return the schema for the platforms in scope, so the assistant can author valid SQL | the target filters (`hostnames`, `host_ids`, and the intersecting host filters above) | same target-resolution routes as `get_endpoints` above for the intersecting filters; when `cve_id` is set, the CVE composition routes from `get_vulnerability_hosts` below instead; plus `GET /hosts/{id}` per explicit `host_ids` entry, and, per explicit `hostnames` entry, a query-first `GET /hosts` search falling back to `GET /hosts/identifier/{identifier}` |
| `run_live_query` | Step 2 of 2: run an osquery SQL statement against live devices. **Destructive.** Re-resolves its own targets when it runs; SQL is checked against the current schema's column types first, and a text-column-versus-bare-integer comparison is rejected | `sql`; direct selectors `hostnames` / `host_ids`; intersecting `fleet`, `platform`, `label`, `status`, `query`, `policy_id`, `policy_response`, `cve_id` | target-resolution routes as above, plus one of: `POST /hosts/{id}/query` for a single target, or `POST /reports/run` followed by `GET /results/websocket` to stream results for multiple targets |

Both `prepare_live_query` and `run_live_query` also accept three undocumented legacy aliases, kept for backward compatibility: `labels`, `platforms`, and `fleets`, each a comma-separated string where only the first item is used. Prefer the singular `label` / `platform` / `fleet` arguments above; the plural forms silently drop everything past the first value rather than intersecting on all of them.

`GET /results/websocket` is not in Fleet's own endpoint catalog: it authenticates the bearer token when the connection opens rather than through the same per-route check the rest of this table goes through, so an endpoint allowlist cannot name it and does not gate it: a token that can start a multi-host run can always read that run's results back over the stream ([6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md)).

## Policies and vulnerabilities

![Reference](../_assets/icons/reference.svg) Policy pass/fail counts and the hosts on either side, and the hosts a CVE affects. All read-only. The host-listing tools here return a capped page with no running total; read a count question from the counting tools rather than the length of a list (see [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md) on completeness limits).

| Tool | What it does | Arguments | Fleet routes |
|---|---|---|---|
| `get_policies` | List all policies, global and per-fleet, with pass/fail host counts | none | `GET /global/policies`, `GET /fleets` (to enumerate fleets), `GET /fleets/{id}/policies` per fleet |
| `get_policy_compliance` | Pass/fail counts for one policy; global aggregate by default | `policy_id`; optional `fleet` to scope to one fleet | `GET /global/policies/{id}`, or `GET /fleets` + `GET /fleets/{id}/policies/{id}` when `fleet` is set |
| `get_policy_hosts` | The hosts that pass or fail a given policy | `policy_id` (required); optional `response`, `fleet`, `platform`, `label`, `status`, `query`, `per_page` (compose) | same host-listing routes as `get_endpoints` above |
| `get_vulnerability_impact` | Aggregate count of systems affected by a CVE; can report a lower bound at the internal host ceiling | `cve_id` | `GET /software/titles` (paginated, to find titles the CVE affects), `GET /software/titles/{id}` per matching title (to get its version ids), `GET /hosts` per version id (to get the affected hosts), and `GET /hosts/count` (for the total-systems denominator) |
| `get_vulnerability_hosts` | The specific hosts affected by a CVE, composed across several Fleet calls because Fleet's single-filter path is unreliable | `cve_id`; optional `fleet`, `platform`, `label`, `status`, `query`, `per_page` | `GET /fleets` when `fleet` is set (to resolve the team name); then the same three-step composition as `get_vulnerability_impact`: `GET /software/titles`, `GET /software/titles/{id}` per title, `GET /hosts` per version id |

## Inventory

![Reference](../_assets/icons/reference.svg) Stored software and local user accounts, read from Fleet's cached inventory so they answer for offline hosts. Both read-only. The freshness of these answers is the last successful inventory collection, not the last check-in ([4.1](../04-know-your-devices/4.1-understand-hosts-vitals-and-inventory.md), [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md)).

**At 4.90.1, `get_software`'s own tool description tells the assistant its data is "refreshed on each host check-in," which is not what the source does** — detail-query issuance, software included, is throttled to the configured inventory interval rather than tied to every check-in. The assistant reads that description as fact along with everything else the tool returns, so if it states a freshness guarantee for software data, don't take the assistant's word for it; check the host's own last-collection time instead.

| Tool | What it does | Arguments | Fleet routes |
|---|---|---|---|
| `get_software` | Stored software. Two auto-selected modes: **per-host** with a host argument returns up to `per_page` packages (default 50, max 200) on that host with versions, source and matching CVEs; **cross-host** with no host argument returns software titles seen across hosts | per-host: `host_id` or `host_identifier`; cross-host: optional `fleet`, `vulnerable`, and `platform` (which requires `fleet`); `source` (e.g. `apps`, `deb_packages`, `chrome_extensions`) filters client-side; `query` filters server-side | per-host: `GET /hosts/{id}/software`; cross-host: `GET /software/titles`, plus `GET /fleets` when `fleet` is set (to resolve the team name) |
| `get_host_users` | OS-local user accounts on one host as inventoried by osquery: uid, username, type, groupname, shell | `host_id` (preferred) or `host_identifier`; optional `query` to filter the returned users | `GET /hosts/{id}` for a numeric `host_id`; for `host_identifier`, a query-first `GET /hosts` search, then either `GET /hosts/{id}` (unique match) or, on fallback, `GET /hosts/identifier/{identifier}` followed by `GET /hosts/{id}` (the identifier route doesn't return user data, so the resolved id is re-fetched) |

## The schema-first workflow is advised, not enforced

![Reference](../_assets/icons/reference.svg) The server tells a cooperating client to fetch the schema before writing SQL and to confirm before running a live query, and it advertises the read/destructive annotations above. These are instructions to the assistant, not gates the server keeps: a client can ignore them, and `run_live_query` resolves its targets and validates its SQL itself at call time regardless. The controls that hold are the token's Fleet role and, on the agent, osquery's own table controls — both covered in [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md).
