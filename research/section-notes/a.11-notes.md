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
