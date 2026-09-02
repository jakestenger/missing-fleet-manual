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
