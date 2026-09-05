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

![Reference](../_assets/icons/reference.svg) The exact tools the Fleet MCP server exposes to an AI assistant, and the arguments each one takes. [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md) is the chapter: it explains what the server is, how to build and connect it, and the security model this reference assumes. The REST routes underneath these tools are [a.8](a.8-api-action-and-endpoint-reference.md). This appendix is the argument-level contract, grouped by the four domains the server registers: hosts, queries, policies and vulnerabilities, and inventory. Look up the tool you're calling; the tables below aren't meant to be read start to finish. The binary also carries one non-tool flag, `-seed`, a one-shot bootstrap that creates a set of standard saved reports and then exits without serving; it is not one of the tools below, and [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md) covers it.

Twenty tools. Sixteen read Fleet's own data; three read from outside Fleet and never reach it; and one, `run_live_query`, executes on and consumes resources on devices. The three that never touch Fleet are `get_vetted_queries`, which serves a bundled query library, and `get_osquery_schema` and `refresh_osquery_schema`, which serve the osquery schema. `refresh_osquery_schema` fetches from `raw.githubusercontent.com` and replaces the MCP server's shared in-memory schema on success, so every subsequent `get_osquery_schema` call in that process sees the new data ([6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md)). The read/destructive marks below are the advisory annotations the server sends to a cooperating client, not a control Fleet enforces: the enforced boundary is the Fleet role of the token the server holds ([6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md)).

Every tool table below has a **Fleet routes** column, for building or auditing an endpoint allowlist on the server's API-only token ([6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md)). Routes omit the common `/api/v1/fleet` prefix, but an allowlist entry cannot: Fleet's match is against the **literal submitted path**, and only the literal `v1` form is accepted. Submitting `latest` or a dated version (e.g. `2022-04`) is rejected outright: Fleet's version-agnostic normalization exists only internally, to build its own route catalog from route templates, and it never runs against a user-submitted allowlist entry ([a.8](a.8-api-action-and-endpoint-reference.md)). An allowlist entry is a full `{"method", "path"}` pair, not the short form used in the tables below. For example, to allow `get_endpoints`'s `GET /hosts` row, submit `{"method": "GET", "path": "/api/v1/fleet/hosts"}`. The server also calls `GET /me` once per process, at startup, to identify the token and fail closed if it's invalid; that check runs once, not on every connection.

**The enumerating tools fan out across fleets or software versions, and a failed component request is dropped rather than surfaced.** `get_queries` and `get_policies` list the global items first, then fetch each fleet's items in parallel; the two CVE tools fetch hosts one software version at a time; `get_vulnerability_impact` also fetches the estate total separately for its denominator. When one of the fan-out requests fails, the server logs a warning to its own process log and returns the rest as an ordinary success, with no field marking the result partial. A count from these tools can therefore run silently low: a fleet's queries or policies missing, or a CVE's host list short by whichever versions failed. Retry and read the server's process log for those warnings before treating any of them as a census, a compliance total, or a security decision.

**One failure on `get_vulnerability_impact` logs nothing at all: the total-systems denominator.** That figure comes from a single separate estate-count call, and when it fails the tool falls back to `total_systems` of zero and writes no warning, so here a clean process log is not proof the run was complete. A `total_systems` of zero does not mean the fleet is empty, and it is what makes the impact read as impossibly severe: a nonzero affected count against a zero estate is every host affected out of none. Treat a zero denominator, or any impact ratio that looks that extreme, as a failed estate count rather than a real result, and confirm the total against `get_total_system_count` (the same `GET /hosts/count` route) before trusting it.

## Outcome to tool

![Reference](../_assets/icons/reference.svg) The fixed twenty-tool subset is not the REST API column: [a.1](a.1-capability-index.md)'s outcome rows are. This matrix keys the tools below to the [a.1](a.1-capability-index.md) capability ID whose outcome they answer, so an outcome you already have a CAP-ID for (from a.1, a.2 or a.5) resolves straight to a tool name instead of a scan of the twenty rows below. Several tools share a CAP-ID because a.1's outcome grain is coarser than the tool-argument grain this appendix carries; five resolution-only or narrower-scoped tools (`get_fleets`, `get_labels`, `get_osquery_schema`, `refresh_osquery_schema`, `get_queries`) look up ids or schema for another tool's call, or answer a narrower outcome than any CAP-ID names, so they carry no CAP-ID here. `get_queries` is one of these: it lists saved report *definitions* (its own row below), not a report's stored *results*. CAP-098 names the latter, and no tool in this reference answers it.

| CAP-ID | Outcome ([a.1](a.1-capability-index.md)) | Tool(s) |
|---|---|---|
| CAP-138 | List hosts through the API | `get_endpoints` |
| CAP-083 | See what a device is and what is on it | `get_host`, `get_host_users` |
| CAP-114 | Ask a pass-or-fail question | `get_host_policies`, `get_policies`, `get_vetted_queries` |
| CAP-133 | Count the estate | `get_total_system_count`, `get_aggregate_platforms` |
| CAP-093 | Run a query right now | `prepare_live_query`, `run_live_query` |
| CAP-119 | Count how many hosts are failing | `get_policy_compliance`, `get_policy_hosts` |
| CAP-124 | Find vulnerable software | `get_vulnerability_impact`, `get_vulnerability_hosts` |
| CAP-122 | List what is installed | `get_software` |

## Arguments common to several tools

![Reference](../_assets/icons/reference.svg) The host-facing tools share one filter vocabulary, resolved server-side. Learn it once and it reads across the tables below.

| Argument | Meaning | Notes |
|---|---|---|
| `query` | Substring match | Covers hostname, serial, primary IP, hardware model, and host-user fields (username, email, IdP group). Does not match display name. |
| `fleet` | Restrict to one fleet by name | Resolved to a fleet id server-side. |
| `label` | Restrict to one label by name | Resolved to a label id. Single label only; Fleet does not intersect multiple labels. On the plain host filters `label` and `platform` do not compose: when both are set the label wins and `platform` is silently ignored, so pair them only on a CVE-filtered live query, where the two do apply together (see below). |
| `platform` | `macos`, `windows`, `linux`, or `chromeos` | A standard Fleet host filter, resolved to a built-in platform label; any other value is rejected. When `label` is also set the label wins and this is silently ignored on the plain host filters (see the `label` row); the two apply together only on a CVE-filtered live query. The software tool takes its own, wider `platform` set (see `get_software`). |
| `status` | Host status (online, offline, and the rest) | A standard Fleet host filter. |
| `policy_id` + `policy_response` | Hosts on one side of a policy | `policy_response` is `passing` or `failing` and requires `policy_id`; the orphan is rejected at the server. |
| `per_page` | Page size for host listings | Clamped to a maximum of 200. |
| `host_id` vs `identifier` | Which host | A numeric `host_id` is exact. An `identifier` (hostname, UUID, serial, computer name, or a fuzzy substring) may match several hosts, in which case the tool returns a candidate list to disambiguate; re-call with the chosen `host_id`. |
| `cve_id` | A CVE | Must match `CVE-YYYY-NNNN` (`^CVE-\d{4}-\d{4,}$`); a malformed value is rejected before Fleet is called. |

## Hosts

![Reference](../_assets/icons/reference.svg) Reading enrolled hosts, their policy results, and fleet-wide counts. All read-only.

| Tool | What it does | Arguments | Fleet routes |
|---|---|---|---|
| `get_endpoints` | List and filter enrolled hosts; the returned `total` reflects the filtered scope | `fleet`, `platform`, `status`, `query`, `label`, `policy_id`, `policy_response`, `per_page` (compose, except that `label` overrides `platform` rather than intersecting it) | `GET /hosts`, `GET /hosts/count`; `GET /labels` and `GET /fleets` to resolve a `label`/`platform`/`fleet` name to an id; `GET /labels/{id}/hosts` when a `label` or `platform` filter is set (that endpoint silently ignores label population, so with no `policy_id` set the tool backfills it with one `GET /hosts/{id}` per returned host) |
| `get_host` | A selected projection of one host, not Fleet's full host detail: identity (hostname, display and computer name), status and last-seen, platform, osquery version, serial, primary IP, fleet, and labels | `host_id` (preferred) or `identifier` | `GET /hosts/{id}`, or `GET /hosts/identifier/{identifier}` (falls back to `GET /hosts` first when the identifier is a fuzzy match) |
| `get_host_policies` | Every policy applied to one host with its pass/fail/not-run response, plus a summary block | `host_id` or `identifier`; optional `response` to narrow to passing or failing | `GET /hosts/{id}` for a numeric `host_id`; for `identifier`, a query-first `GET /hosts` search, then either `GET /hosts/{id}` (unique match) or `GET /hosts/identifier/{identifier}` (fallback) |
| `get_total_system_count` | Count of retained enrolled host records visible to the API token, across all statuses | none | `GET /hosts/count` |
| `get_aggregate_platforms` | System counts broken down by OS platform | none | `GET /host_summary` |
| `get_fleets` | List all fleets with ids and names | none | `GET /fleets` |
| `get_labels` | List all labels | none | `GET /labels` |

**`get_aggregate_platforms` buckets only a fixed subset of Linux distributions as Linux.** It reads Fleet's server-side host summary, which counts each distribution under its own platform string, then re-buckets those counts: only `linux`, `ubuntu`, `centos`, `rhel`, `debian`, `fedora`, and `amzn` are summed into the Linux total. Hosts Fleet reports under any other Linux platform string it recognizes (Zorin, SLES, Kali, Arch, and roughly twenty more) fall into the breakdown's Other line, so the Linux count reads low and Other reads high. The same fixed subset governs the `platform` filter on the CVE host tools, so `platform=linux` on `get_vulnerability_hosts` drops those same hosts. The plain host-listing tools (`get_endpoints`, `get_policy_hosts`) are unaffected: they resolve `platform=linux` to Fleet's built-in All Linux label, which is complete. For an accurate Linux census, filter or count against that built-in All Linux label rather than the aggregate's Linux line.

## Queries

![Reference](../_assets/icons/reference.svg) The saved-report list (`get_queries`), the osquery schema, and running live osquery. `run_live_query` is the one destructive tool; the rest are read-only.

| Tool | What it does | Arguments | Fleet routes |
|---|---|---|---|
| `get_queries` | List saved reports, global and per-fleet | none | `GET /reports`, `GET /fleets` (to enumerate fleets), then `GET /reports` scoped per fleet |
| `get_osquery_schema` | Osquery table schema for column types, refreshed from Fleet's `main` branch rather than pinned to your release ([6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md)) | `platform` (returns a curated short list) or `tables` (comma-separated, for full coverage of any of the 360+ tables) | none (reads a schema file fetched from GitHub, not from Fleet; [a.6](a.6-glossary-and-release-compatibility.md)) |
| `refresh_osquery_schema` | Force an immediate refresh of the in-memory schema from Fleet's published schema file | none | none (same GitHub-sourced schema as above) |
| `get_vetted_queries` | A bundled library of CIS-8.1-derived policy queries for macOS, Windows and Linux, labelled in the source as transcribed from those benchmarks; nothing in the tagged source verifies that labelling, executes them, or validates them, so treat the library as a starting point to test rather than a pre-validated one | optional `platform` (`darwin`/`macos`, `windows`, `linux`, or `all`; defaults to `all`) | none (bundled into the server binary) |
| `prepare_live_query` | Step 1 of 2: validate targets and return the schema for the platforms in scope, so the assistant can author valid SQL | the target filters (`hostnames`, `host_ids`, and the composing host filters above, subject to the `label`/`platform` exception noted there) | same target-resolution routes as `get_endpoints` above for the intersecting filters; when `cve_id` is set, the CVE composition routes from `get_vulnerability_hosts` below instead; plus `GET /hosts/{id}` per explicit `host_ids` entry, and, per explicit `hostnames` entry, a query-first `GET /hosts` search falling back to `GET /hosts/identifier/{identifier}` |
| `run_live_query` | Step 2 of 2: run an osquery SQL statement against live devices. **Destructive.** Re-resolves its own targets when it runs. The SQL gets a best-effort pre-flight against the current schema: a known table used on a platform the schema says it does not support is rejected, and a known text column compared against a bare integer is rejected (except a literal `0` or `1`, let through as a boolean-style flag). Tables and columns the schema does not recognize pass through unchecked, since Fleet itself is the authority on those, so the check catches the common mistakes rather than proving the query valid | `sql`; direct selectors `hostnames` / `host_ids`; composing `fleet`, `platform`, `label` (`label` overrides `platform` except when `cve_id` is set, see below), `status`, `query`, `policy_id`, `policy_response`, `cve_id` | target-resolution routes as above, plus one of: `POST /hosts/{id}/query` for a single target, or `POST /reports/run` followed by `GET /results/websocket` to stream results for multiple targets |

Both `prepare_live_query` and `run_live_query` also accept three undocumented legacy aliases, kept for backward compatibility: `labels`, `platforms`, and `fleets`, each a comma-separated string where only the first item is used. Prefer the singular `label` / `platform` / `fleet` arguments above; the plural forms silently drop everything past the first value rather than intersecting on all of them.

**On a plain live query, do not combine `label` and `platform`.** They do not intersect: the label wins and `platform` is silently dropped. SQL that was validated against the declared `platform` can then execute against labeled hosts running a different operating system, which is not what the caller asked for. Scope such a query by `label` or by `platform`, not both. The one exception is a CVE-filtered live query (`cve_id` set): there `label` and `platform` do apply together, narrowing the affected-host set by both.

`GET /results/websocket` is not in Fleet's own endpoint catalog: it authenticates the bearer token when the connection opens rather than through the same per-route check the rest of this table goes through, so an endpoint allowlist cannot name it and does not gate it: a token that can start a multi-host run can always read that run's results back over the stream ([6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md)).

## Policies and vulnerabilities

![Reference](../_assets/icons/reference.svg) Policy pass/fail counts and the hosts on either side, and the hosts a CVE affects. All read-only. The host-listing tools here return a capped page with no running total; read a count question from the counting tools rather than the length of a list (see [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md) on completeness limits).

| Tool | What it does | Arguments | Fleet routes |
|---|---|---|---|
| `get_policies` | List all policies, global and per-fleet, with pass/fail host counts | none | `GET /global/policies`, `GET /fleets` (to enumerate fleets), `GET /fleets/{id}/policies` per fleet |
| `get_policy_compliance` | Pass/fail counts for one policy; global aggregate by default | `policy_id`; optional `fleet` to scope to one fleet | `GET /global/policies/{id}`, or `GET /fleets` + `GET /fleets/{id}/policies/{id}` when `fleet` is set |
| `get_policy_hosts` | The hosts that pass or fail a given policy | `policy_id` (required); optional `response`, `fleet`, `platform`, `label`, `status`, `query`, `per_page` (compose, except that `label` overrides `platform`) | same host-listing routes as `get_endpoints` above |
| `get_vulnerability_impact` | Aggregate count of systems affected by a CVE; over-counts hosts on unaffected versions of an affected title (see below), and can also report a lower bound at the internal host ceiling | `cve_id` | `GET /software/titles` (paginated, to find titles the CVE affects), `GET /software/titles/{id}` per matching title (to get its version ids), `GET /hosts` per version id (to get the affected hosts), and `GET /hosts/count` (for the total-systems denominator) |
| `get_vulnerability_hosts` | The hosts affected by a CVE, composed across several Fleet calls because Fleet's single-filter path is unreliable; the composition over-includes hosts on unaffected versions of an affected title (see below) | `cve_id`; optional `fleet`, `platform`, `label`, `status`, `query`, `per_page` | `GET /fleets` when `fleet` is set (to resolve the fleet name); then the same three-step composition as `get_vulnerability_impact`: `GET /software/titles`, `GET /software/titles/{id}` per title, `GET /hosts` per version id |

**Both CVE tools over-include hosts on unaffected versions.** The composition finds the software titles a CVE affects, then fetches hosts for every version of each title, dropping which versions actually carry the CVE. A title with a mix of affected and unaffected versions therefore contributes hosts from all of them, so `get_vulnerability_hosts` lists hosts that run a safe version and `get_vulnerability_impact` counts them. Do not use either for authoritative remediation targeting or exposure counts; confirm a listed host against its own software inventory ([6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md)).

## Inventory

![Reference](../_assets/icons/reference.svg) Stored software and local user accounts, read from Fleet's cached inventory so they answer for offline hosts. Both read-only. The freshness of these answers is the last successful inventory collection, not the last check-in ([4.1](../04-know-your-devices/4.1-understand-hosts-vitals-and-inventory.md), [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md)).

**At 4.90.0, `get_software`'s own tool description tells the assistant its data is "refreshed on each host check-in," which is not what the source does**: detail-query issuance, software included, is throttled to the configured inventory interval rather than tied to every check-in. The assistant reads that description as fact along with everything else the tool returns, so if it states a freshness guarantee for software data, don't take the assistant's word for it; check the host's own last-collection time instead. That freshness line is not the only tool description that reads simpler than the tool behaves: `get_endpoints` advertises that all its filters compose, yet `label` and `platform` do not, and setting both drops `platform` silently (the argument notes above). Read a tool's self-description as a claim to check against this reference, not a contract the server keeps.

| Tool | What it does | Arguments | Fleet routes |
|---|---|---|---|
| `get_software` | Stored software. Two auto-selected modes: **per-host** with a host argument returns up to `per_page` packages (default 50, max 200) on that host with versions, source and matching CVEs; **cross-host** with no host argument returns software titles seen across hosts | per-host: `host_id` or `host_identifier`; cross-host: optional `fleet`, `vulnerable`, and `platform` (which requires `fleet`); `source` (e.g. `apps`, `deb_packages`, `chrome_extensions`) filters client-side; `query` filters server-side; `per_page` (default 50, max 200), applied after any source filter, in both modes | per-host: first resolves the host (`GET /hosts/{id}` for a numeric `host_id`, or for `host_identifier` a query-first `GET /hosts` search falling back to `GET /hosts/identifier/{identifier}`), then `GET /hosts/{id}/software`; cross-host: `GET /software/titles`, plus `GET /fleets` when `fleet` is set (to resolve the fleet name) |
| `get_host_users` | OS-local user accounts on one host as inventoried by osquery: uid, username, type, groupname, shell | `host_id` (preferred) or `host_identifier`; optional `query` to filter the returned users | `GET /hosts/{id}` for a numeric `host_id`; for `host_identifier`, a query-first `GET /hosts` search, then either `GET /hosts/{id}` (unique match) or, on fallback, `GET /hosts/identifier/{identifier}` followed by `GET /hosts/{id}` (the identifier route doesn't return user data, so the resolved id is re-fetched) |

**In cross-host mode, `platform` filters the installable catalogue, not host inventory by operating system.** It narrows the returned titles to those that carry an installable artifact (a software installer, a VPP app, or an in-house app) targeting that platform for the fleet, which is why it requires `fleet` and answers only for a fleet's own installers. It does not restrict the list to software actually observed on hosts running that operating system. To inventory installed software by host OS, resolve the hosts first (by platform or label) and read each host's own inventory with the per-host mode above.

## Starting allowlist profiles

![Reference](../_assets/icons/reference.svg) Two ready-made endpoint allowlists, assembled from the **Fleet routes** columns above, de-duplicated, plus the startup `GET /me`. Copy the one that matches the token's job; [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md#two-starting-allowlist-profiles) is where you attach it to the API-only user and confirm the boundary. Restore the `/api/v1/fleet` prefix on every route and submit each as a full `{"method", "path"}` pair, as the note on the routes column near the top of this appendix describes: the shorthand here cannot go into `api_endpoints` unchanged. Re-derive both lists whenever the tools change or one is added, and test the result against your own deployment rather than treating it as a quick lock-down.

- **Read-only** (every tool except `run_live_query`): `GET /me`, `GET /hosts`, `GET /hosts/count`, `GET /hosts/{id}`, `GET /hosts/identifier/{identifier}`, `GET /hosts/{id}/software`, `GET /host_summary`, `GET /labels`, `GET /labels/{id}/hosts`, `GET /fleets`, `GET /fleets/{id}/policies`, `GET /fleets/{id}/policies/{policy_id}`, `GET /global/policies`, `GET /global/policies/{id}`, `GET /software/titles`, `GET /software/titles/{id}`, `GET /reports`.
- **Read plus live query**: the read-only list above, plus `POST /hosts/{id}/query` and `POST /reports/run` for running queries. It cannot add the results stream: `GET /results/websocket` sits outside the allowlist mechanism entirely (above), so anyone who can reach `POST /reports/run` can already read what it returns.

![Reference](../_assets/icons/reference.svg) The server tells a cooperating client to fetch the schema before writing SQL and to confirm before running a live query, and it advertises the read/destructive annotations above. These are instructions to the assistant, not gates the server keeps: a client can ignore them, and `run_live_query` resolves its targets and validates its SQL itself at call time regardless. The controls that hold are the token's Fleet role and, on the agent, osquery's own table controls, both covered in [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md).
