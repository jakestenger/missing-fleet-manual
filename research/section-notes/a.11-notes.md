---
section: "A.11"
---

# A.11 Fleet MCP tool reference, citation ledger

Drafted 2026-09-01 from `cmd/fleet-mcp` at tag `fleet-v4.90.1` (commit `dd0200f062`), the same source 6.6 was verified against. Reference appendix; every row is the tool's own contract, read from the registrations.

## Stated: verified at the tag

| Claim | Basis |
|---|---|
| **Twenty tools** across four domains: 7 hosts, 6 queries, 5 policies/vulnerabilities, 2 inventory | The `register*` calls in `mcp_tools_hosts.go`, `mcp_tools_queries.go`, `mcp_tools_policies.go`, `mcp_tools_inventory.go` |
| Shared host-filter vocabulary (`query`, `fleet`, `label`, `platform`, `status`, `policy_id`+`policy_response`, `per_page`) resolved server-side; `query` covers hostname/serial/IP/model/host-users but not display name | README operational learnings + the filter plumbing in `fleet_integration.go`; the host resolver in `mcp_tools_hosts.go` |
| Validation: `per_page` clamped to 200 (`defaultPerPageMax`); `cve_id` matches `^CVE-\d{4}-\d{4,}$`; `policy_response` requires `policy_id`; malformed inputs rejected before Fleet is called | `mcp_helpers.go` validators |
| `run_live_query` is the **only** tool annotated destructive; it re-resolves targets and validates SQL (text-vs-bare-integer rejected) at call time | `mcp_tools_queries.go` (`WithDestructiveHintAnnotation(true)` only here); `schema.go` `ValidateSQLForPlatforms` |
| `get_vetted_queries` reads data **bundled into the server**, not Fleet REST state | `vetted_queries.go` / `mcp_tools_queries.go` |
| `get_software` has two auto-selected modes (per-host vs cross-host titles); cross-host `platform` requires `fleet` | README inventory section; `mcp_tools_inventory.go` |
| `get_vulnerability_impact` can report a lower bound at the internal host ceiling; `get_vulnerability_hosts` composes several calls | `fleet_integration.go` `GetHostsForCVE` + the 10,000-host cap |
| The schema-first workflow and the read/destructive annotations are **advisory** to a cooperating client, not server-enforced | `mcp_server.go` `fleetMCPInstructions` comment |

## Wiring done alongside this file

- OUTLINE A.11 registry row added.
- 6.6's "exact arguments" pointer changed from the tagged `cmd/fleet-mcp` directory to A.11.
- Per §8, no Go file paths or function names appear in the appendix prose; tool names and argument names are the reader-facing MCP contract (like endpoints in a.8) and are the content itself.

## 2026-09-02 addition: Fleet routes column (queue R1-M8)

| Claim | Basis |
|---|---|
| Per-tool Fleet route list, added as a column on all four tool tables | Grepped every hardcoded `/api/v1/fleet/...` literal in `fleet_integration.go` and `live_query_campaign.go`, then traced each tool's `register*` handler in the four `mcp_tools_*.go` files to the `FleetClient` method(s) it calls (`GetEndpoints*`, `GetHostBy*`, `GetPolicies`, `GetHostsForCVE`, `ResolveLiveQueryTargets`, `runMultiHostCampaign`, `runAdHocSingleHost`, etc.) |
| Filter-driven fan-out (`GET /labels`, `GET /fleets`, `GET /labels/{id}/hosts`) on any tool accepting `label`/`platform`/`fleet` | `resolveLabelName`, `resolveTeamNames`, `resolvePlatformOrLabelToLabelID` in `fleet_integration.go`, called from `GetEndpointsWithFilters` |
| `get_osquery_schema`/`refresh_osquery_schema`/`get_vetted_queries` call **no** Fleet route at all | `schema.go` fetches `raw.githubusercontent.com/fleetdm/fleet/main/schema/osquery_fleet_schema.json`, not a Fleet server endpoint; `vetted_queries.go` is bundled data — neither calls `makeFleetRequest` |
| `run_live_query` uses `POST /hosts/{id}/query` for a single target or `POST /reports/run` + `GET /results/websocket` for multiple | `runAdHocSingleHost` vs `runMultiHostCampaign` branch in `mcp_tools_queries.go`, confirmed at `fleet_integration.go:2018` and `live_query_campaign.go:79,314` |
| Route matching is version-agnostic (`v1`/`latest`/dated all fingerprint the same) — an allowlist entry must not pin one version literal | `NewAPIEndpointFromTpl` in `server/fleet/api_endpoints.go` strips the `{fleetversion:...}` mux segment to `/v1/` before fingerprinting |
| `GET /results/websocket` is **not** in Fleet's endpoint-restriction catalog and is not gated by the same per-route check as the rest of this table | Grepped `server/api_endpoints/api_endpoints.yml` for `websocket` — zero matches. Its mux registration (`server/service/handler.go` `ne.UsePathPrefix().PathHandler("GET", "/api/_version_/fleet/results/", ...)`) is on the unauthenticated-endpointer group; `makeStreamDistributedQueryCampaignResultsHandler` (`server/service/endpoint_campaigns.go`) authenticates the bearer token itself when the socket opens (`auth.AuthViewer`) rather than through `APIOnlyEndpointCheck` (`server/service/middleware/auth/api_only.go`), which is the function that actually consults the restriction list |

This surfaced a real gap in the existing 6.6 "endpoint allowlist" paragraph — it didn't previously say the live-query results stream sits outside the allowlist mechanism — so 6.6 was updated in the same batch with a matching note and two reference allowlist profiles (read-only; read + live query).

## 2026-09-02 fix: fan-out routes missing from the R1-M8 column (round3 B3, REGRESSION)

The R1-M8 pass above built the Fleet-routes column but several rows only captured the tool's primary call, not its full transitive route set. Re-traced each flagged tool's handler against `fleet_integration.go` / `live_query_campaign.go` at `fleet-v4.90.1`:

| Tool | Was missing | Traced to |
|---|---|---|
| `get_queries` | `GET /fleets` + per-team `GET /reports` | `GetQueries` calls `GetTeams` (`GET /fleets`) then fans out `GET /reports?team_id=N` per team, concurrently |
| `get_host_policies` | query-first `GET /hosts` search when called by `identifier` | `registerGetHostPolicies` → `resolveHostDetail` generic helper (`mcp_helpers.go`) always tries `GetEndpointsWithFilters` (→ `GET /hosts`) first when no `host_id`, only falling back to the identifier route on zero/ambiguous matches |
| `get_host_users` | same query-first `GET /hosts`, plus a second call on the identifier-fallback path | `resolveHostWithUsers` (`mcp_tools_inventory.go`) wraps the same `resolveHostDetail` helper; its `byIdentifier` closure calls `GetHostByIdentifier` (`GET /hosts/identifier/{id}`) *then* `GetHostByIDWithUsers` (`GET /hosts/{id}`) as a second call, because the identifier route doesn't return the `users` array — unlike `get_host_policies`, whose identifier route does return policies directly via `?populate_policies=true`, one call |
| `get_vulnerability_impact` | `GET /software/titles/{id}` per title, `GET /hosts` per version id, `GET /hosts/count` | `GetVulnerabilityImpact` calls `GetHostsForCVE` (the full 3-step composition) for the impacted set, then `GetHostCount` for the denominator |
| `get_vulnerability_hosts` | `GET /fleets` when `fleet` is set | `GetHostsForCVE` calls `resolveTeamNames` (→ `GET /fleets`) before the 3-step composition when `teamName` is non-empty |
| `get_software` (cross-host) | `GET /fleets` when `fleet` is set | `ListSoftwareTitles` calls `resolveTeamNames` (→ `GET /fleets`) before `GET /software/titles` when `teamName` is non-empty |
| `prepare_live_query` / `run_live_query` | the CVE-composition branch and the explicit `host_ids`/`hostnames` resolution routes | `ResolveLiveQueryTargets`: `cve_id` set routes through `GetHostsForCVE` instead of `GetEndpointsWithFilters`; each `host_ids` entry is a direct `GetHostByID` call; each `hostnames` entry is a query-first `GetEndpointsWithFilters` call, then `GetHostByID` to confirm, then `GetHostByIdentifier` as a last resort |

All confirmed via direct read of the named functions at `fleet-v4.90.1` (`dd0200f062`), not inferred from names. `check-links.py`, `check-table-names.py`, `check-column-names.py` clean after the edit.

## 2026-09-02 fix: get_software's own tool description overclaims freshness (round3 M5)

The Inventory intro correctly distinguishes "last inventory collection" from "last check-in," but
never warned that `get_software`'s own MCP tool description — the text baked into the tool
registration and handed to the assistant, not anything in this book — literally says the data is
"refreshed on each host check-in." Verified against `fleet-v4.90.1`:
`cmd/fleet-mcp/mcp_tools_inventory.go:34`'s `mcp.WithDescription(...)` string contains that exact
phrase, while `server/service/osquery.go:762-773`'s `detailQueriesForHost` gates detail-query
issuance (software included) on `svc.shouldUpdate(host.DetailUpdatedAt,
svc.config.Osquery.DetailUpdateInterval, host.ID)` — throttled to the configured interval, not
tied to every check-in. Since the assistant receives the tool's self-description as part of its
context, a false freshness guarantee baked into the tool itself is a defect the book's accurate
prose doesn't cover on its own. Added a warning that operators shouldn't trust the assistant's own
freshness claims for this tool and should check the host's last-collection time instead.

## 2026-09-02 fix: "vetted, production-safe" CIS library overclaim (round3 M6)

The `get_vetted_queries` row called the bundled CIS-8.1 library "vetted, production-safe" with no
qualification. Verified against `fleet-v4.90.1`: `cmd/fleet-mcp/vetted_queries.go` is static data
transcribed from the CIS benchmarks (the file's own comment says "DO NOT add any query that has
not been read verbatim from a CIS benchmark"), but no test anywhere under `cmd/fleet-mcp/*_test.go`
executes or validates any of these queries — `fleet_integration_test.go` is the only test file and
doesn't reference them. "Vetted" against the benchmark text and "production-safe" against this
codebase's own execution evidence are two different claims, and only the first is backed here.
Reworded to say the queries are transcribed verbatim (real) without asserting execution safety
that isn't tested, and to tell the reader to treat the library as a tested starting point rather
than pre-validated.

## Fix-loop round (2026-09-02, round4 RM6 + RM7)

- **RM6 — outcome-to-tool matrix mapped CAP-098 ("read a report's results") to `get_queries`,
  which only lists report definitions.** Verified `GetQueries` (`fleet_integration.go`) calls
  `GET /reports` and returns Fleet's `Query` struct, which has no stored-result fields — no MCP
  tool answers CAP-098. Removed the row; added `get_queries` to the "carries no CAP-ID" list
  with a one-line explanation of the definitions-vs-results distinction, rather than inventing a
  new CAP-ID (would reopen the register-drift class RB1 already fixed this cycle).
- **RM7 — "version-agnostic" allowlist claim was backwards.** Verified
  `server/fleet/api_endpoints.go`'s `versionSegmentRe` only rewrites the internal
  `{fleetversion:...}` route-template placeholder to `/v1/`; a user-submitted literal path like
  `/api/latest/fleet/hosts` never matches that pattern and is rejected by
  `validateAPIEndpointRefs` (`server/service/users.go`) as unknown. Confirmed the real payload
  shape (`{"method","path"}` with the full literal path) against
  `integration_enterprise_test.go`. Corrected the claim to "only literal v1 is accepted" and
  added a copyable full-path JSON example.

## Fix-loop round (2026-09-02, round4 RM1)

- **RM1 — fan-out routes still incomplete after round-3's B3 "complete transitive call graph"
  fix.** Verified against source: `get_endpoints` (via `GetEndpointsWithFilters`,
  `fleet_integration.go`) taking Path 2 (label/platform filter, no `policy_id`) calls
  `enrichHostLabels`, which issues one `GET /hosts/{id}` per host still missing labels, because
  `/labels/{id}/hosts` silently ignores `populate_labels=true`. That fan-out wasn't in the row.
  Separately, `get_software`'s per-host mode calls `resolveHost` (`mcp_tools_inventory.go`) —
  `GET /hosts/{id}` for a numeric `host_id`, or a query-first `GET /hosts` search falling back to
  `GET /hosts/identifier/{identifier}` for `host_identifier` — before its own
  `GET /hosts/{id}/software` call, and none of that resolution sequence was listed. Added both.

## Fix-loop round (2026-09-02, round4 m1, m2)

- **"Every connection also calls `GET /me`" was wrong** — the identity check runs once per MCP
  server process at startup, not per connection (matches 6.6:86's correct "checked by the server
  at startup, once"). Corrected the wording.
- **"Every other tool only reads" hid `refresh_osquery_schema`'s side effects.** It performs an
  outbound fetch to `raw.githubusercontent.com` and replaces the MCP server's shared in-memory
  schema on success (`RefreshSchemaNow`/`storeSchema` in `cmd/fleet-mcp/schema.go:163-186`), so
  subsequent `get_osquery_schema` calls in that process see the new data. Added a disclosure
  sentence naming it as a partial exception.

## Fix-loop round (2026-09-02, round4 m7, m8)

- **`get_software` row's Arguments cell omitted `per_page`**, though the description prose
  already mentioned it. Confirmed `per_page` is a real registered arg applying to both per-host
  and cross-host modes (`cmd/fleet-mcp/mcp_tools_inventory.go:33-49`, `parsePerPageArg`). Added
  it to the Arguments cell.
- **`run_live_query` row stated the bare-integer TEXT-column rejection without the `0`/`1`
  boolean-flag exception** that 6.6's prose already carries correctly (6.6:72, fixed there by
  round-3 m7 but never propagated here). Confirmed exception at `cmd/fleet-mcp/schema.go:361-458`
  ("Don't flag literal 0 / 1 against TEXT"). Added the parenthetical to the row.

## Fix-loop round (2026-09-03, round5 MJ4)

- **The opening summary conflated "reads Fleet" with "reads at all" and mislabeled
  `run_live_query`.** It said "one changes devices; every other tool only reads Fleet's own data,"
  which is wrong on both counts: three tools never touch Fleet, and `run_live_query` does not
  change devices. Counted the registrations in `cmd/fleet-mcp` (fleet-v4.90.1): 20 `mcp.NewTool`
  calls total. Three operate outside Fleet — `get_vetted_queries` (bundled library via
  `GetVettedQueries`, no fleetClient), `get_osquery_schema` and `refresh_osquery_schema` (osquery
  schema from the embedded snapshot / `raw.githubusercontent.com`, `openWorld=true`). One,
  `run_live_query`, is annotated `ReadOnly=false`/`Destructive=true` with the source comment that
  it "consumes device CPU and surfaces in EDR telemetry" — i.e. executes on and consumes resources
  on devices, not persistent mutation. The remaining 16 read Fleet. Rewrote line 25 to that single
  model, consistent with 6.6's own carve-out (MJ4). Verified fleet-v4.90.1.

## Round 6 fix cycle (2026-09-03) — re-validated vs fleet-v4.90.0

`cmd/fleet-mcp/` is byte-identical between fleet-v4.90.0 and fleet-v4.90.1, so the round6 MCP
findings (verified against 4.90.1) hold unchanged at the book's 4.90.0 base; not point-release fixes.

- **C1 (both CVE tools over-include hosts on unaffected versions).** `fleet_integration.go` CVE
  composition (Step 2 ~1651-1689) decodes only `SoftwareTitle.Versions[].ID` and appends every
  version id, discarding the per-version vulnerability array; Step 3 (~1695+) fetches hosts for
  every version id. Adjusted the `get_vulnerability_impact` row (added over-count of unaffected
  versions alongside the existing lower-bound-at-ceiling note), the `get_vulnerability_hosts` row
  ("the hosts affected", not "the specific hosts", + over-include note), and added a shared
  **"Both CVE tools over-include hosts on unaffected versions"** caveat paragraph after the
  policies/vulnerabilities table routing readers to per-host software inventory. links=0.
- **C2 (`label` overrides `platform`, does not intersect).** Verified at fleet-v4.90.0:
  `resolvePlatformOrLabelToLabelID` (~1207-1226) returns immediately when `labelName != ""`
  ("labelName takes precedence over platform when both are set"), so `platform` is never resolved
  when both are supplied. `GetEndpointsWithFilters` shows the *other* filters do compose: the
  label-routing path calls `/labels/:id/hosts` (respects `team_id`/`status`/`query`) and intersects
  a `policy_id` side via `/hosts`, so only the `label`/`platform` pair fails to intersect. Softened
  the overclaims: common-args `label`+`platform` rows note the override; `get_endpoints` and
  `get_policy_hosts` "(compose, except that `label` overrides `platform`)"; `prepare_live_query`/
  `run_live_query` "composing" not "intersecting"; added a **"Never combine `label` and `platform`
  on a live query"** warning (SQL validated for the declared `platform` can hit labeled hosts on a
  different OS). links=0.
- **M1 (`get_software` cross-host `platform` filters installable artifacts, not host OS).** Verified
  at fleet-v4.90.0: `fleet_integration.go:632-657` (`ListSoftwareTitles`) passes `platform` to
  `GET /software/titles` with `team_id`; datastore comment `software_titles.go:250-256` states "the
  platform filters for **installable** software on the given platform ... supported on a per team
  basis, so we require both", and the SQL postfix (`:774`, `:777`) applies the platform set to the
  software-installer / VPP-app / in-house-app platform columns, not to host-observed inventory.
  Added a bold note after the Inventory table: cross-host `platform` narrows to titles carrying an
  installable artifact targeting that platform for the fleet (hence it requires `fleet`), not
  software observed on hosts of that OS; to inventory by host OS, resolve hosts first then read
  per-host inventory. links=0.
- **M2 (MCP recognizes only a subset of Fleet's Linux platform class).** Verified at
  fleet-v4.90.0: `fleet_integration.go` buckets only seven Linux strings (`normalizePlatform`
  ~302-316; `matchesPlatform` ~318-324; host-summary re-bucket ~903-922, `default` case dumps the
  rest into Other) = linux/ubuntu/centos/rhel/debian/fedora/amzn. Fleet's own `HostLinuxOSs`
  (`server/fleet/hosts.go:1231-1257`) lists 26 (linux, ubuntu, zorin, debian, rhel, centos, sles,
  kali, gentoo, amzn, pop, arch, linuxmint, void, nixos, endeavouros, manjaro, manjaro-arm,
  opensuse-leap/-tumbleweed, tuxedo, neon, archarm, flatcar, coreos, cachyos); `fedora` is in the
  MCP set but not in Fleet's list. Finding said "27"; actual is 26 at both 4.90.0 and 4.90.1 (file
  unchanged between tags) — behaviour unaffected. Scope: bites `get_aggregate_platforms` (Linux
  census undercounts, Other overcounts) and the CVE post-filter `matchesPlatform` at ~1763-1788
  (`platform=linux` on `get_vulnerability_hosts`). Host-listing (`get_endpoints`/`get_policy_hosts`)
  is NOT affected: `platform=linux` resolves via `platformToBuiltinLabel` (~1216) to the complete
  "All Linux" built-in label. Added a bold note after the Hosts table naming the seven-string
  subset, the Other-bucket effect, the CVE `platform=linux` drop, and the recommendation to use the
  built-in All Linux label for census. Kept out of 6.6 (density, M21). links=0.
