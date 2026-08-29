---
section: "A.6"
---

# a.6 Terminology and version boundaries, citation ledger

Terminology and the 4.82.0 rename written 2026-08-24. **Version boundaries written 2026-08-29**, and
the appendix re-scoped at the same time under the Part IX agreement
([`../appendix-structure.md`](../appendix-structure.md)).

## What the re-scope removed, and why

**Feature availability is gone.** Free against Premium belongs in a.2, where a claim can be qualified
by platform and scope. The reason is not tidiness: a version floor and a licence gate produce the
identical symptom, a feature that is configured and does nothing, and a reader diagnosing one needs
the other table to be a separate place they can rule out.

**Documentation maintenance is gone.** It was a third empty heading in an appendix whose own
introduction admitted to two, and its content is contributor material rather than reader material.

**Version boundaries is filled**, with cross-cutting floors only.

## The organising finding

**Fleet negotiates capabilities rather than comparing versions.** The agent and server exchange a
named capability list per request; when the server wants something the agent has not declared, it
does something else and logs at debug.

There is **exactly one server-side agent-version comparison in the 4.90.1 tree**, the Linux LUKS
passphrase escrow gate at `ee/server/service/devices.go:262`, using `IsAtLeastVersion`
(`server/fleet/utils.go:91`). `OrbitVersion` and `OsqueryVersion` appear elsewhere only in ingest and
statistics, never in a gate.

That is why the appendix's central claim is about **silence** rather than about numbers.

## Fleet contract, source checked at the tag

### The negotiation mechanism

| Claim | Source |
|---|---|
| Capabilities are exchanged in a header, populated by both sides | `server/fleet/capabilities.go:153`; server reads at `server/contexts/capabilities/capabilities.go:15`, writes at `server/service/endpoint_utils.go:317` |
| One version comparison exists in the whole server tree | `ee/server/service/devices.go:262`, definition `server/fleet/utils.go:91` |
| **No minimum agent version to enroll or talk to a 4.90.1 server.** Neither enrollment path reads a version, and the agent's enrollment record has no version field | `server/service/orbit.go:150-310`, `server/service/osquery.go:105-200`, `server/fleet/orbit.go:100-120` |
| Only one negotiated capability is persisted anywhere | `server/service/orbit.go:597-608`, into `mdm_windows_enrollments.fleetd_sync_capable` |

### Agent floors

Each row's gate cited in the research at
`../../missing-fleet-manual-private/research-sensitive/a.6-scratch-versions.md` §1. Load-bearing ones:

| Claim | Source |
|---|---|
| LUKS passphrase escrow, fleetd 1.36.0, server 4.61.0, **version-compared** | `server/fleet/service.go:1640`, `ee/server/service/devices.go:262` |
| snapd recovery-key escrow, fleetd 1.58.0, server **4.90.0**, capability-gated **both ways** | `server/fleet/capabilities.go:93,121`; agent gate `orbit/pkg/luks/luks.go:151-156` |
| `update_channels`, fleetd 1.20.0, **nothing checks**; the server sends the block unconditionally | `server/service/orbit.go:752,833`; only gate is licence, `server/fleet/agent_options.go:118` |
| FileVault rotation, fleetd 1.30.0, capability, **no fallback** | `server/service/orbit.go:937` |
| ADE setup experience, fleetd 1.35.0, capability, with a fallback for older agents | `server/service/orbit.go:542,838` |
| End-user auth, fleetd 1.50.0, and **below it Fleet allows the enrollment unauthenticated** | `server/service/orbit.go:259` |
| `EUA_TOKEN` packaging property, orbit 1.55.0, **no fallback branch** | `orbit/pkg/packaging/windows.go:107-109` |

### Operating system floors

| Claim | Source |
|---|---|
| ACME device identity needs macOS 14.0 **and** Apple Silicon **and** a DEP-assigned serial | `server/service/apple_mdm.go:2790-2806`, called at `:2769`, `:6583` |
| The macOS 14 OS-update delivery floor is a **dynamic label computed from report results**, not a version comparison | `server/fleet/labels.go:307`, migration `20240415104633_CreateMacOSSonomaBuiltinLabel.go:37`, attached `ee/server/service/mdm.go:1465` |
| **iOS 17 and iPadOS 17 are not enforced.** The built-in labels are platform-only with an empty query | `server/fleet/labels.go:308-309`, migration `20240707134036_CreateIOSAndIPADOSBuiltinLabels.go:77,82` |
| Manual migration eligibility is macOS **strictly greater than** 14.0.0 | `server/fleet/hosts.go:1829`, compared at `:1865` |
| Windows discovery requires protocol version 4.0, and the device reports a specific failure code | `server/fleet/microsoft_mdm.go:198`, `server/mdm/microsoft/syncml/syncml.go:189` |
| TPM path opens the 2.0 resource-manager device node, which Linux added in 4.12 | `ee/orbit/pkg/securehw/securehw_linux.go:15,29` |
| **No minimum Apple OS to enroll in MDM**, and no Android version gate anywhere | `server/service/apple_mdm.go:2683-2703`; nothing found in `server/mdm/android/` |

### Dependency floors

| Claim | Source |
|---|---|
| MySQL 8.0.44, moved from 8.0.36 in the 4.83 line | Already carried by 2.9 |
| **Redis 6.2**, required by the host-lookup cache on the osquery and orbit authentication paths | `CHANGELOG.md:489`, which states the requirement in the entry itself; corroborated `docs/Get started/FAQ.md:197` |

### The support policy

| Claim | Source |
|---|---|
| Bug fixes: latest version only, both tiers, **no backports**. Troubleshooting: current major for Free, all versions for Premium | `handbook/company/product-groups.md:606-616`, quoted verbatim in the research |
| It lives in the handbook, not in `docs/` | Same |
| Skipping versions within v4 is explicitly permitted, and nothing enforces an upgrade path | `docs/Get started/FAQ.md:638` |
| One minor and one patch every three weeks, scheduled patches weekly between | `docs/Contributing/workflows/releasing-fleet.md:3,72` |

## Not established

**A time-bounded support window or end-of-life date for any Fleet release.** Searched the whole
repository; the only end-of-life language concerns MySQL 5.7. The appendix says there is none rather
than inventing one, and says why that changes how to plan.

**Whether ChromeOS's documented 112 floor is enforced anywhere.** The extension manifest carries no
minimum Chrome version key. Recorded as documented-only.

**Whether the Android 14 floor in Fleet's documentation corresponds to anything.** No gate found.

## Corrections this research forced into finished chapters

| Chapter | Was | Now |
|---|---|---|
| **5.6** | Fleet sends the combined Windows deadline node, and it is unknown whether Windows 11 still honours it | Fleet sends **both split nodes**. The question does not arise |
| **2.9** | "Redis has no minimum version stated" | **6.2**, required by the host-lookup cache |
| **5.6** | The Apple version check "does not run on the team-spec and GitOps path" | Narrower: global and Unassigned **do** validate; the per-fleet spec endpoint does not, and iOS gets no validation there at all |
| **3.7** | 1.38.1 as the stepping stone | **Kept at 1.38.1**, with the discrepancy explained. See below |

**The 3.7 correction is recorded because I got it wrong first.** The research reported the boundary as
1.38.0, which is true of where the migration code lives. I swept five instances to 1.38.0 before
checking Fleet's own guidance, which names **1.38.1** as the bridge; the two releases are three days
apart and Fleet shipped a rollback with 1.38.0 in case it needed one. The chapter is back at 1.38.1
and now explains why both numbers appear. **Where the code answers a different question from the one
the chapter asks, the code is not automatically the better source.**

## Rejected, and why

**A feature-availability table.** Moved to a.2 by the part-level agreement rather than by preference.

**Every OS version Fleet supports.** This section is floors, not a support matrix. Several floors
found during research affect one chapter only and stayed there.

## Checks run

`check-links`, `check-em-dashes`, `check-crossrefs`, `unwrap` dry run.

## Rounds

| Round | Verdict | Outcome |
|---|---|---|
| 1, coverage | Not yet run | |
| 2, evidence audit | Not yet run | |
| 3, whole-appendix and cross-appendix | Not yet run | |
