---
title: "Fleet MCP tool reference"
chapter: "Appendices and indexes"
section: "A.11"
sidebar_position: 11
verified_against: Fleet 4.90.0
verified_on: 2026-09-01
verified_source: "drafted against fleet-v4.90.0 (7c428c6e46), reading cmd/fleet-mcp at that tag: the tool registrations in mcp_tools_hosts.go, mcp_tools_queries.go, mcp_tools_policies.go and mcp_tools_inventory.go, the argument parsing in mcp_helpers.go, and the server instructions in mcp_server.go. Citation ledger at research/section-notes/a.11-notes.md."
further_reading:
  - https://github.com/fleetdm/fleet/tree/fleet-v4.90.0/cmd/fleet-mcp
  - https://modelcontextprotocol.io/
feature_requests:
  labels: []
  match: []
  exclude: []
---

# Fleet MCP tool reference

![Reference](../_assets/icons/reference-light.svg) Look up a Fleet MCP tool here to find its arguments, underlying routes, and known limits. Tools are grouped into hosts, queries, policies and vulnerabilities, and inventory. [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md) covers building, connecting, and securing the MCP server, including the separate `-seed` flag that creates standard reports and exits. [a.8](a.8-api-action-and-endpoint-reference.md) covers REST routes.

Of the twenty tools, sixteen read Fleet data, three work without calling Fleet, and `run_live_query` executes SQL on devices. The three independent tools are `get_vetted_queries`, which reads a bundled library, and the two schema tools. `refresh_osquery_schema` fetches from `raw.githubusercontent.com` and, on success, replaces the process’s shared in-memory schema for subsequent calls. Read/destructive annotations advise cooperating clients; Fleet enforces the token’s role and scope ([6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md)).

Use the **Fleet routes** column to build endpoint restrictions for the API-only token. The tables omit `/api/v1/fleet` for readability, but submitted entries require the full literal path and method. For example, `GET /hosts` becomes `{"method": "GET", "path": "/api/v1/fleet/hosts"}`. `latest` and dated prefixes are rejected in submitted allowlists; Fleet’s internal template normalization does not apply to those entries ([a.8](a.8-api-action-and-endpoint-reference.md)). Include `GET /me` for the startup check that identifies the token and stops the process if it is invalid. That check runs once per process.

Some tools combine several requests. `get_queries` and `get_policies` read global items, then fetch each fleet’s items in parallel. The CVE tools fetch hosts per software version; `get_vulnerability_impact` also fetches a deployment-wide total. Most failed component requests produce a process-log warning but no partial-result field, so the tool returns ordinary success with missing data. Retry and inspect those warnings before using the results as complete counts or decision inputs.

The total-count request in `get_vulnerability_impact` is an exception: failure sets `total_systems` to zero without logging a warning. A zero denominator can therefore reflect a failed count rather than an empty deployment. If it is zero or inconsistent with the affected count, confirm it with `get_total_system_count`, which uses the same `GET /hosts/count` route.

## Outcome to tool

![Reference](../_assets/icons/reference-light.svg) This table maps tool names to outcomes in [a.1](a.1-capability-index.md). Several tools share a capability ID because the index groups outcomes more broadly. Five have no matching ID: `get_fleets`, `get_labels`, `get_osquery_schema`, `refresh_osquery_schema`, and `get_queries`. They provide supporting lookups or narrower results. In particular, `get_queries` lists saved report definitions; it does not retrieve the stored results described by CAP-098, which no listed tool provides.

| CAP-ID | Outcome ([a.1](a.1-capability-index.md)) | Tool(s) |
|---|---|---|
| CAP-138 | List hosts through the API | `get_endpoints` |
| CAP-083 | See what a device is and what is on it | `get_host`, `get_host_users` |
| CAP-114 | Ask a pass-or-fail question | `get_host_policies`, `get_policies`; `get_vetted_queries` supplies starting-point check definitions to build from, not a pass/fail result |
| CAP-133 | Count the estate | `get_total_system_count`, `get_aggregate_platforms` |
| CAP-093 | Run a query right now | `prepare_live_query`, `run_live_query` |
| CAP-119 | Count how many hosts are failing | `get_policy_compliance` for the count; `get_policy_hosts` returns only a capped page of which hosts, not a total |
| CAP-124 | Find vulnerable software | `get_vulnerability_impact`, `get_vulnerability_hosts` |
| CAP-122 | List what is installed | `get_software` |

## Arguments common to several tools

![Reference](../_assets/icons/reference-light.svg) Host-facing tools use these shared filters. Check the exceptions before combining them.

| Argument | Meaning | Notes |
|---|---|---|
| `query` | Substring match | Covers hostname, serial, primary IP, hardware model, and host-user fields (username, email, IdP group). Does not match display name. |
| `fleet` | Restrict to one fleet by name | Resolved to a fleet id server-side. |
| `label` | Restrict to one label by name | Resolved to a label id. Single label only; Fleet does not intersect multiple labels. On the plain host filters `label` and `platform` do not compose: when both are set the label wins and `platform` is silently ignored, so pair them only on a CVE-filtered live query, where the two do apply together (see below). |
| `platform` | `macos`, `windows`, `linux`, or `chromeos` | A standard Fleet host filter, resolved to a built-in platform label; any other value is rejected. When `label` is also set the label wins and this is silently ignored on the plain host filters (see the `label` row); the two apply together only on a CVE-filtered live query. The software tool takes its own, wider `platform` set (see `get_software`). |
| `status` | Host status (online, offline, and the rest) | A standard Fleet host filter. |
| `policy_id` + `policy_response` | Hosts on one side of a policy | `policy_response` is `passing` or `failing` and requires `policy_id`; a response without a policy ID is rejected. |
| `per_page` | Page size for host listings | Clamped to a maximum of 200. |
| `host_id` vs `identifier` | Which host | A numeric `host_id` is exact. An `identifier` (hostname, UUID, serial, computer name, or a fuzzy substring) may match several hosts, in which case a successful preliminary search returns a candidate list to disambiguate; re-call with the chosen `host_id`. That candidate return depends on the search succeeding: if it errors, the tool falls back to a single-record identifier lookup that returns one host with no defined ordering and can pick one of several duplicates silently, so prefer `host_id` when an exact target matters. |
| `cve_id` | A CVE | Must match `CVE-YYYY-NNNN` (`^CVE-\d{4}-\d{4,}$`); a malformed value is rejected before Fleet is called. |

## Hosts

![Reference](../_assets/icons/reference-light.svg) These read-only tools return enrolled hosts, policy results, and counts across the token’s accessible scope.

| Tool | What it does | Arguments | Fleet routes |
|---|---|---|---|
| `get_endpoints` | List and filter enrolled hosts; the returned `total` reflects the filtered scope | `fleet`, `platform`, `status`, `query`, `label`, `policy_id`, `policy_response`, `per_page` (compose, except that `label` overrides `platform` rather than intersecting it) | `GET /hosts`, `GET /hosts/count`; `GET /labels` and `GET /fleets` to resolve a `label`/`platform`/`fleet` name to an id; `GET /labels/{id}/hosts` when a `label` or `platform` filter is set (that endpoint silently ignores label population, so with no `policy_id` set the tool backfills it with one `GET /hosts/{id}` per returned host) |
| `get_host` | Selected fields for one host: identity (hostname, display and computer name), status and last-seen, platform, osquery version, serial, primary IP, fleet, and labels | `host_id` (preferred) or `identifier` | `GET /hosts/{id}` for a numeric `host_id`; for `identifier`, a query-first `GET /hosts` search, then either `GET /hosts/{id}` (unique match) or `GET /hosts/identifier/{identifier}` (fallback) |
| `get_host_policies` | Every policy applied to one host with its pass/fail/not-run response, plus a summary block | `host_id` or `identifier`; optional `response` to narrow to passing or failing | `GET /hosts/{id}` for a numeric `host_id`; for `identifier`, a query-first `GET /hosts` search, then either `GET /hosts/{id}` (unique match) or `GET /hosts/identifier/{identifier}` (fallback) |
| `get_total_system_count` | Count of retained enrolled host records visible to the API token, across all statuses | none | `GET /hosts/count` |
| `get_aggregate_platforms` | System counts broken down by OS platform | none | `GET /host_summary` |
| `get_fleets` | List all fleets with ids and names | none | `GET /fleets` |
| `get_labels` | List all labels | none | `GET /labels` |

`get_aggregate_platforms` sums only `linux`, `ubuntu`, `centos`, `rhel`, `debian`, `fedora`, and `amzn` into its Linux total. Other recognized distributions, including Zorin, SLES, Kali, and Arch, appear under Other. The CVE host tools use the same limited set for `platform=linux`. For a complete Linux selection, use the built-in All Linux label through a host-listing tool such as `get_endpoints` or `get_policy_hosts`.

## Queries

![Reference](../_assets/icons/reference-light.svg) These tools provide report definitions, schema, and live queries. `run_live_query` carries the destructive annotation; the others carry read-only annotations.

| Tool | What it does | Arguments | Fleet routes |
|---|---|---|---|
| `get_queries` | List saved reports, global and per-fleet | none | `GET /reports`, `GET /fleets` (to enumerate fleets), then `GET /reports` scoped per fleet |
| `get_osquery_schema` | Osquery table schema for column types, refreshed from Fleet's `main` branch rather than pinned to your release ([6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md)) | `platform` (returns a curated short list) or `tables` (comma-separated, for full coverage of any of the 360+ tables) | none (reads a schema file fetched from GitHub, not from Fleet; [a.6](a.6-glossary-and-release-compatibility.md)) |
| `refresh_osquery_schema` | Force an immediate refresh of the in-memory schema from Fleet's published schema file | none | none (same GitHub-sourced schema as above) |
| `get_vetted_queries` | A bundled library of CIS-8.1-derived policy queries for macOS, Windows and Linux, labelled in the source as transcribed from those benchmarks; the tagged source provides no verification or execution tests for that label, so test the queries before using them | optional `platform` (`darwin`/`macos`, `windows`, `linux`, or `all`; defaults to `all`) | none (bundled into the server binary) |
| `prepare_live_query` | Step 1 of 2: validate targets and return the schema for the platforms in scope, so the assistant can author valid SQL | the target filters (`hostnames`, `host_ids`, and the composing host filters above, subject to the `label`/`platform` exception noted there) | same target-resolution routes as `get_endpoints` above for the intersecting filters; when `cve_id` is set, the CVE composition routes from `get_vulnerability_hosts` below instead; plus `GET /hosts/{id}` per explicit `host_ids` entry, and, per explicit `hostnames` entry, a query-first `GET /hosts` search falling back to `GET /hosts/identifier/{identifier}` |
| `run_live_query` | Step 2 of 2: run an osquery SQL statement against live devices. **Destructive.** Re-resolves its own targets when it runs. The SQL gets a best-effort pre-flight against the current schema: a known table used on a platform the schema says it does not support is rejected, and a known text column compared against a bare integer is rejected (except a literal `0` or `1`, let through as a boolean-style flag). Tables and columns the schema does not recognize pass through unchecked, so this preflight provides limited validation | `sql`; direct selectors `hostnames` / `host_ids`; composing `fleet`, `platform`, `label` (`label` overrides `platform` except when `cve_id` is set, see below), `status`, `query`, `policy_id`, `policy_response`, `cve_id` | target-resolution routes as above, plus one of: `POST /hosts/{id}/query` for a single target, or `POST /reports/run` followed by `GET /results/websocket` to stream results for multiple targets |

`prepare_live_query` and `run_live_query` also accept legacy `labels`, `platforms`, and `fleets` arguments. Each is a comma-separated string, but only its first value is used. Prefer the singular `label`, `platform`, and `fleet` arguments to make the selected scope explicit.

For a plain live query, choose either `label` or `platform`. When both are supplied, the label overrides the platform silently, so SQL checked for one platform could reach labeled hosts on another. With `cve_id` set, both filters do apply together to narrow the affected-host set.

`GET /results/websocket` authenticates its bearer token inside the connection handler and is absent from the endpoint restriction catalog. The allowlist therefore cannot gate that stream. A token permitted to start a multi-host run can read its own results through it ([6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md)).

## Policies and vulnerabilities

![Reference](../_assets/icons/reference-light.svg) These read-only tools return policy counts, policy host lists, and CVE-related host data. Host lists are capped pages without a running total. Use the counting tools for totals, and check their completeness limits below and in [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md).

| Tool | What it does | Arguments | Fleet routes |
|---|---|---|---|
| `get_policies` | List all policies, global and per-fleet, with pass/fail host counts | none | `GET /global/policies`, `GET /fleets` (to enumerate fleets), `GET /fleets/{id}/policies` per fleet |
| `get_policy_compliance` | Pass/fail counts for one policy; global aggregate by default | `policy_id`; optional `fleet` to scope to one fleet | `GET /global/policies/{id}`, or `GET /fleets` + `GET /fleets/{id}/policies/{id}` when `fleet` is set |
| `get_policy_hosts` | The hosts that pass or fail a given policy | `policy_id` (required); optional `response`, `fleet`, `platform`, `label`, `status`, `query`, `per_page` (compose, except that `label` overrides `platform`) | same host-listing routes as `get_endpoints` above |
| `get_vulnerability_impact` | Aggregate count of systems affected by a CVE; over-counts hosts on unaffected versions of an affected title (see below), and can also report a lower bound at the internal host ceiling | `cve_id` | `GET /software/titles` (paginated, to find titles the CVE affects), `GET /software/titles/{id}` per matching title (to get its version ids), `GET /hosts` per version id (to get the affected hosts), and `GET /hosts/count` (for the total-systems denominator) |
| `get_vulnerability_hosts` | The hosts affected by a CVE, composed across several Fleet calls because Fleet's single-filter path is unreliable; the composition over-includes hosts on unaffected versions of an affected title (see below) | `cve_id`; optional `fleet`, `platform`, `label`, `status`, `query`, `per_page` | `GET /fleets` when `fleet` is set (to resolve the fleet name); then the same three-step composition as `get_vulnerability_impact`: `GET /software/titles`, `GET /software/titles/{id}` per title, `GET /hosts` per version id |

Both CVE tools can include hosts running unaffected versions. They identify affected software titles, then fetch hosts for every version of those titles without retaining the version-level CVE distinction. Confirm each host’s software inventory before using the list for remediation or its count as an exposure total ([6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md)).

## Inventory

![Reference](../_assets/icons/reference-light.svg) These tools read stored software and local-account inventory, including for offline hosts. Freshness depends on the last successful inventory collection ([4.1](../04-know-your-devices/4.1-understand-hosts-vitals-and-inventory.md), [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md)).

At 4.90.0, `get_software` describes inventory as refreshed at each check-in, but the implementation issues detail queries on the configured inventory interval. Check the host’s collection time before relying on a freshness claim. Likewise, `get_endpoints` describes composing filters without accounting for the `label`/`platform` exception above. These tool descriptions omit limits that affect how an assistant may interpret the result.

| Tool | What it does | Arguments | Fleet routes |
|---|---|---|---|
| `get_software` | Stored software. Two auto-selected modes: **per-host** with a host argument returns up to `per_page` packages (default 50, max 200) on that host with versions, source and matching CVEs; **cross-host** with no host argument returns software titles seen across hosts | per-host: `host_id` or `host_identifier`; cross-host: optional `fleet`, `vulnerable`, and `platform` (which requires `fleet`); `source` (e.g. `apps`, `deb_packages`, `chrome_extensions`) filters client-side; `query` filters server-side; `per_page` (default 50, max 200), applied after any source filter, in both modes | per-host: first resolves the host (`GET /hosts/{id}` for a numeric `host_id`, or for `host_identifier` a query-first `GET /hosts` search falling back to `GET /hosts/identifier/{identifier}`), then `GET /hosts/{id}/software`; cross-host: `GET /software/titles`, plus `GET /fleets` when `fleet` is set (to resolve the fleet name) |
| `get_host_users` | OS-local user accounts on one host as inventoried by osquery: uid, username, type, groupname, shell | `host_id` (preferred) or `host_identifier`; optional `query` to filter the returned users | `GET /hosts/{id}` for a numeric `host_id`; for `host_identifier`, a query-first `GET /hosts` search, then either `GET /hosts/{id}` (unique match) or, on fallback, `GET /hosts/identifier/{identifier}` followed by `GET /hosts/{id}` (the identifier route doesn't return user data, so the resolved id is re-fetched) |

In cross-host mode, `get_software` uses `platform` to select installable artifacts for the specified fleet: installers, VPP apps, or in-house apps targeting that platform. It does not filter observed host inventory by OS. To inventory software on hosts of a particular OS, select those hosts first and call the per-host mode for each.

## Starting allowlist profiles

![Reference](../_assets/icons/reference-light.svg) These starting lists combine the routes above with startup’s `GET /me`. Restore `/api/v1/fleet` on every path and submit full method/path pairs. [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md#two-starting-allowlist-profiles) explains how to attach and test the list. Recheck it when tools change or are added.

- **Read-only** (every tool except `run_live_query`): `GET /me`, `GET /hosts`, `GET /hosts/count`, `GET /hosts/{id}`, `GET /hosts/identifier/{identifier}`, `GET /hosts/{id}/software`, `GET /host_summary`, `GET /labels`, `GET /labels/{id}/hosts`, `GET /fleets`, `GET /fleets/{id}/policies`, `GET /fleets/{id}/policies/{policy_id}`, `GET /global/policies`, `GET /global/policies/{id}`, `GET /software/titles`, `GET /software/titles/{id}`, `GET /reports`.
- **Read plus live query**: the read-only list above, plus `POST /hosts/{id}/query` and `POST /reports/run` for running queries. It cannot add the results stream: `GET /results/websocket` sits outside the allowlist mechanism entirely (above), so anyone who can reach `POST /reports/run` can already read what it returns.

![Reference](../_assets/icons/reference-light.svg) The MCP server asks clients to fetch schema before writing SQL and seek confirmation before running a live query. Those instructions and annotations depend on client cooperation. `run_live_query` independently resolves targets and checks SQL at call time. Enforced controls include the token’s Fleet role and the agent’s osquery table controls ([6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md)).
