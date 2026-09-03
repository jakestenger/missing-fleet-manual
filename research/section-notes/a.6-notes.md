---
section: "A.6"
---

# a.6 Terminology and version boundaries, citation ledger

Terminology and the 4.82.0 rename written 2026-08-24. **Version boundaries written 2026-08-29**, and
the appendix re-scoped at the same time under the Part IX agreement
([`../appendix-structure.md`](../appendix-structure.md)).

## What the re-scope removed, and why

**Feature availability is gone.** Free against Premium belongs in a.2, where a claim can be qualified
by platform and scope. The reason is not tidiness: a version boundary and a licence gate **can converge on** the same
symptom, a feature that is configured and does nothing, and a reader ruling one out needs the other
to be a separate place. Narrowed at round 1: many licence gates refuse explicitly, so the convergence
is common rather than universal.

**Documentation maintenance is gone.** It was a third empty heading in an appendix whose own
introduction admitted to two, and its content is contributor material rather than reader material.

**Version boundaries is filled**, with cross-cutting boundaries only, typed by kind rather than all
called floors.

## The organising finding, as narrowed at round 1

**Fleet 4.90.1 declares and enforces no global minimum agent version.** Its Orbit and device protocols
negotiate named capabilities for several boundaries; others are ungated, chosen locally by the agent,
or implemented as fallbacks. **The server compares a reported agent version in exactly one gate**, the
Linux LUKS passphrase escrow gate at `ee/server/service/devices.go:262`, using `IsAtLeastVersion`
(`server/fleet/utils.go:91`). `OrbitVersion` and `OsqueryVersion` appear elsewhere only in ingest and
statistics, never in a gate.

So most incompatibilities degrade one feature rather than refusing anything, and many are invisible
from the console. **My first draft of this said "everything else is negotiated" and the appendix's own
table disproved it**; see round 1 below.

## Fleet contract, source checked at the tag

### The negotiation mechanism

| Claim | Source |
|---|---|
| Capabilities are exchanged in a header, populated by both sides, **on the Orbit and device protocols only** | `server/fleet/capabilities.go:153`; server reads at `server/contexts/capabilities/capabilities.go:15`, writes at `server/service/endpoint_utils.go:317`; clients at `client/orbit_client.go:157-168` and `client/device_client.go:91-110`. **Narrowed at round 1 from "every request"** |
| One version comparison exists in the whole server tree | `ee/server/service/devices.go:262`, definition `server/fleet/utils.go:91` |
| **No minimum agent version to enroll or talk to a 4.90.1 server.** Neither enrollment path reads a version, and the agent's enrollment record has no version field | `server/service/orbit.go:150-310`, `server/service/osquery.go:105-200`, `server/fleet/orbit.go:100-120` |
| Only one negotiated capability is persisted anywhere | `server/service/orbit.go:597-608`, into `mdm_windows_enrollments.fleetd_sync_capable` |

### Agent boundaries

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

### Operating system boundaries

| Claim | Source |
|---|---|
| ACME device identity needs macOS 14.0 **and** Apple Silicon **and** a DEP-assigned serial | `server/service/apple_mdm.go:2790-2806`, called at `:2769`, `:6583` |
| The macOS 14 OS-update delivery floor is a **dynamic label computed from report results**, not a version comparison | `server/fleet/labels.go:307`, migration `20240415104633_CreateMacOSSonomaBuiltinLabel.go:37`, attached `ee/server/service/mdm.go:1465` |
| **iOS 17 and iPadOS 17 are not enforced.** The built-in labels are platform-only with an empty query | `server/fleet/labels.go:308-309`, migration `20240707134036_CreateIOSAndIPADOSBuiltinLabels.go:77,82` |
| Manual migration eligibility is macOS **strictly greater than** 14.0.0 | `server/fleet/hosts.go:1829`, compared at `:1865` |
| Windows discovery requires protocol version 4.0, and the device reports a specific failure code | `server/fleet/microsoft_mdm.go:198`, `server/mdm/microsoft/syncml/syncml.go:189` |
| TPM path opens the 2.0 resource-manager device node | `ee/orbit/pkg/securehw/securehw_linux.go:15,29`. **The kernel version that added it is Linux's fact, not Fleet's, and no upstream citation was taken**, so neither the appendix nor this ledger states a number. Round 2 removed the inference and round 3 found this row still asserting it |
| **No minimum Apple OS to enroll in MDM**, and no Android version gate anywhere | `server/service/apple_mdm.go:2683-2703`; nothing found in `server/mdm/android/` |

### Dependency constraints

| Claim | Source |
|---|---|
| MySQL 8.0.44, moved from 8.0.36 in the 4.83 line | Already carried by 2.2 |
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
| **2.2** | "Redis has no minimum version stated" | **6.2**, required by the host-lookup cache |
| **5.6** | The Apple version check "does not run on the team-spec and GitOps path" | Narrower: global and Unassigned **do** validate; the per-fleet spec endpoint does not, and iOS gets no validation there at all |
| **3.8** | 1.38.1 as the stepping stone | **Kept at 1.38.1**, with the discrepancy explained. See below |

**The 3.8 correction is recorded because I got it wrong first.** The research reported the boundary as
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



## Round 1, coverage

NOT READY with seven items. **Three load-bearing conclusions were broader than the tag supported**,
which is the failure mode this project keeps producing: a true narrow finding promoted into a
universal.

| Was | Now | Why |
|---|---|---|
| "The agent and server exchange capabilities on every request" | **The Orbit and device protocols** negotiate. osquery's does not | `client/orbit_client.go:157-168`, `client/device_client.go:91-110`. An osquery-side boundary is chosen locally or ungated, never negotiated |
| "Everything else is negotiated" | **Four mechanisms**: negotiated, ungated, chosen locally, compared | The appendix's own rows disproved it. `update_channels` is ungated (`server/service/orbit.go:730-754`), MSI properties are selected while packaging (`orbit/pkg/packaging/windows.go:99-110`), Python inventory uses complementary discovery queries (`server/service/osquery_utils/queries.go:1374-1420`), gzip is chosen inside Orbit |
| "Missing capability means it does something else and logs at debug" | Per row. **End-user auth fails open with a warning**; ADE setup falls back; Windows sync is persisted; Escrow Buddy is skipped | `server/service/orbit.go:251-286`, `:533-547`, `:591-620`, `:929-942` |
| "A current server will enroll an arbitrarily old agent" | "**Fleet declares and enforces no global minimum**" | Absence of a gate does not prove every historical wire format works. Fleet's own process treats new-server-with-old-agent as nice to have, with a minimum named in release notes when it breaks (`docs/Contributing/workflows/fleetd-development-and-release-strategy.md:10-30`) |

### The macOS trap was half right, and the wrong half was the absolute

**Correct:** the macOS 14 label is dynamic and osquery-computed, the declaration attaches to it, and
the older path needs the agent too. So **a Mac that never produced a result cannot enter the label**
and gets neither mechanism.

**Wrong:** the conclusion that any MDM-enrolled Mac without fleetd gets no enforcement. Dynamic
membership is deleted only when a later result is **definitively false**; an error leaves it alone
(`server/datastore/mysql/labels.go:957-1019`). A Mac that joined and later lost its agent keeps
membership and keeps receiving enforcement. **Stale membership, not absence of enforcement**, and the
appendix now separates the two cases.

The iOS and iPadOS finding is confirmed exactly: platform-only manual labels, empty queries, no
version predicate (`20240707134036_CreateIOSAndIPADOSBuiltinLabels.go:55-84`,
`ee/server/service/mdm.go:1461-1473`).

### The support conclusion was unfair and is rewritten

I had written that no version is ever declared unsupported and that "supported" is not the category
to plan in. **That contradicts the table directly above it.** A non-latest release is outside the
scope for fixes, and on Free a previous major is outside the scope for troubleshooting. What Fleet
lacks is a **dated** end of life, not the concept of support. The appendix now gives two planning
questions, remediation against the latest release and support access against the troubleshooting
scope, and says a date is the thing that does not exist.

### Taxonomy, and what came in and out

The single word "floor" was doing five jobs. Rows are now typed as hard floor, silent floor, fallback
or routing boundary, published baseline, or dependency constraint.

**Added:** the published host baselines for all six platforms, which an administrator looks here for
first (`docs/Get started/FAQ.md:72-87`); Aurora MySQL 3.10.3; `fleetctl` against the server, which
**warns and continues** rather than refusing (`cmd/fleetctl/fleetctl/api.go:87-105`); the asymmetric
compatibility contract; the cross-platform web setup capability, where **the agent refuses to start
the flow** against a server that lacks it (`server/fleet/capabilities.go:99-104`,
`orbit/cmd/orbit/orbit.go:1642-1666`); and the three semantic-versioning exceptions, experimental
features, security fixes and default-value changes (`docs/Deploy/Upgrading-Fleet.md:79-87`).

**Removed** as not estate-planning material: gzip compression and per-certificate display scope.

**Split:** the update-server migration now carries both numbers with what each answers, 1.38.0 as the
code boundary and 1.38.1 as Fleet's documented bridge. Calling 1.38.1 the floor said 1.38.0 cannot do
the rewrite, which the code contradicts.

### Terminology

Round 1 caught the section's own opening being false: **there are no `[term]()` markers anywhere in
the manual**, and the entries are reached by ordinary links. Fixed, and the selection rule is stated
in its place.

Seven entries added, all meeting the rule that competing names would make an administrator act or
search incorrectly: **fleetd and its components**, without which the version tables cannot be read;
**AB, ABM and DEP token**; **Unassigned, No team and a null fleet**; **MDM enrollment status on screen
against in a filter** (`frontend/interfaces/mdm.ts:85-115`), which is the strongest fit for the rule
because the wrong value returns an empty result rather than an error; **MIA and missing**
(`server/fleet/hosts.go:20-40`); **pack and scheduled report**; and **the two meanings of activity**
(`20260316120008_RenameActivitiesToActivityPast.go:13`, `20250127162751_AddUnifiedQueueTable.go:72-108`).

### Feature availability

Removal upheld. The rationale is softened from "produce the identical symptom" to "can converge on
the same symptom", because many licence gates refuse explicitly.



## Round 2, the evidence audit

NOT READY, six items, all applied. The numbers came through better than the classifications did: every
version in the appendix checked out except one, and the **kind** assigned to each row, which is the
column that tells a reader what they would see, was wrong or inconsistent across half the table.

### The one wrong number

**The web setup experience row was wrong and was two rows.** I had it as server 4.90.0 for Windows and
Linux together. Linux arrived at Orbit 1.48.0 with server 4.74.0, Windows at Orbit 1.49.0 with server
4.75.0, a release apart. Split, and the agent component named as Orbit rather than fleetd.

Everything else verified: the capability pairs, osquery 5.16.0, the two packaging floors, 1.38.0 and
1.38.1, the Apple and Windows boundaries, the copied host baselines, MySQL, Redis and Aurora, and the
4.82.0 rename.

**One inference removed.** Linux kernel 4.12 is not established by the Fleet tag, which establishes
only that Fleet opens the TPM 2.0 resource-manager device node. That node's kernel version is Linux's
fact and I had no upstream citation, so the appendix now states the requirement and declines the
number.

### "Silent" was doing two jobs

The word meant "nothing anywhere" in some rows and "nothing in the console" in others, and rows were
assigned on whichever reading suited. **It now has one definition, stated in the table: nothing an
administrator sees in Fleet.** A debug line in a server log, or a line in the agent's own log on the
host, is still silent by that definition, because neither reaches the console.

Re-kinded accordingly:

| Row | Was | Is |
|---|---|---|
| snapd recovery-key escrow | One silent row | **Two rows.** New agent against an old server logs a warning and shows the user a notification; the reverse direction is silent |
| ADE setup experience | Silent floor | **Fallback**, to the older worker-based release path |
| End-user authentication | Silent | **Fails open with a warning.** Not silent, and still easy to miss |
| ACME device identity | Not kinded | **Fallback** to SCEP, with an info log |
| macOS 14 update mechanism | Not kinded | **Routing.** Both paths exist |
| Windows discovery version | Not kinded | **Hard floor**, the only one on the OS table: the device reports a specific code |

The operating-system table also declared four columns and supplied five cells, and never assigned the
five kinds it advertised. Rebuilt.

### Two negative claims narrowed

**"Nothing in the code enforces any published baseline"** was contradicted by the macOS 14 gates in the
table immediately above it. Now: **no global admission gate enforces the matrix**, and individual
features have their own.

**"No Fleet release has a published end-of-life date"** exceeded what a repository search can support.
Now: **no dated policy was found anywhere in the 4.90.1 repository**, which is the claim the evidence
actually is.

### Five terminology entries corrected

| Entry | Was | Is |
|---|---|---|
| fleetd | "not a version you can compare" | **No version line of its own**, and what Fleet shows as the agent version is Orbit's. The old wording contradicted the appendix's own numbered rows |
| MDM status filter | The wrong value "returns an empty result" | An unrecognised value is a `400`. The bad case is a **recognised** value meaning something else. Also adds `personal` and `pending` |
| activity | A queued script "will never be in" the audit stream | Too exclusive. Scheduling is itself an action and Fleet records batch scheduling as an activity |
| MIA and missing | Only one "will keep working" | Deprecation is not a removal date, and Fleet has published none |
| pack | Meeting one means the configuration predates the migration | **The pack specification endpoint still accepts new ones**, so it proves only which of two vocabularies was used |

AB/ABM/DEP token and Unassigned/No team/null fleet verified unchanged.

### What the ledger owed, and now carries

**The frontmatter's claim that every floor was "read from the gate" was false**, and it is corrected in
the file: boundaries Fleet enforces were read from the gate, and **the version at which a capability
was introduced is derived from release history**, since the tag only shows the constant existing now.
Those rows are derived and are marked so.

The published-baseline table is now labelled as a **4.90.1 snapshot** rather than presented as an
evergreen list, with the instruction to check Fleet's current table before planning. Reproducing a
list that moves is exactly what this appendix warns about, so it carries the warning about itself.



## Round 3, the whole read

NOT READY, six items. Round 3 confirmed the appendix reads as one thing rather than two, that the
4.82 rename is a genuine hinge between translating names and translating versions, and that all
seventeen Part VIII handoffs resolve to entries that give those chapters what they need. Then it found
the same defect a.8 had just been caught with, twice.

### Three round-2 corrections were in this ledger and not in the appendix

The baseline snapshot label, "no global admission gate", and the narrowed end-of-life claim. **The
ledger described all three as applied and none of them was.**

**The mechanism is worth writing down, because it is mechanical and will recur.** Those three edits
were written against hard-wrapped source text. `unwrap.py` had already joined those paragraphs into
single lines, so the strings I was replacing no longer existed, and a plain `str.replace` that matches
nothing **fails silently**. My assert-guarded edits in the same batch all landed; the three without an
assertion all vanished.

**Every replacement gets an assertion.** Not as a style preference: a silent no-op in a batch of
fourteen edits is invisible, and the ledger then records the intent as the outcome.

### "Silent" had two meanings again

Round 2 gave it a definition and round 3 found two rows contradicting it. The definition said a log
line still counts as silent; the end-user-auth row called a server-log warning "not silent", and the
snapd row called a host notification "not silent".

**One boundary now, stated in the table: nothing reaches an administrator through Fleet.** A process
log, an agent log on the host, and a notification shown to the device's user are all silent by it,
because none reaches the console or raises an alert. Both rows re-kinded, and each says where its
signal does go, since "silent to you, not to the user" is the useful distinction for the snapd row.

The operating-system table was also still headed "boundaries that Fleet does check" while containing
rows that say "Nowhere" and "Nothing checks".

### Unassigned was a data-model claim and I had made it a vocabulary claim

"In the database and in the authorization policy it is a null fleet identifier" is too universal.
Hosts use a null. Some scoped resources pair a nullable identifier with a zero. And where a resource
can also mean *all fleets*, a null can mean all fleets while an explicit zero means Unassigned.

Now: two vocabularies, several storage representations, read the table you are querying. **The role
consequence survives and is the part that matters**, because the policy rejects both null and zero for
fleet-scoped access, so fleet-scoped roles do not reach Unassigned at all.

### Three neighbouring passages tightened

The MDM status table gives three of five and I had called it "the enrolled states" while it includes
Off and omits the enrolled personal state and Pending. The node-key entry opened with "every request"
immediately before explaining that fleetd holds two keys, and it is neither: Fleet Desktop and the
device page use a separate per-device token. And the 4.82 rename said old field names continue to
work, where Fleet deprecated **certain** renamed fields rather than making a blanket promise.

### The a.2 deferral was dishonest, in three places

a.6 sent capability availability to a.2, which is an empty outline, without saying so. **0.1 and 2.9
made the same promise.** All three now follow 1.1's pattern: a.2 will collect it, and the chapter that
owns the capability is authoritative until it does. 1.3 had the reverse problem, still calling a.6 an
outline after it was written.



## Round 4, verification

NOT READY, five items, all applied. **Four of round 3's six landed fully and two landed partially**,
which is a better ratio than the two rounds before it, and the two partials were both of the same
kind: a summary sentence updated while the table it summarised was not.

### The two partials

**The server-floor table's introduction said it included the web setup rows and the rows were not
there.** Added, at 4.74.0 for Linux and 4.75.0 for Windows.

**The 4.82 rename paragraph was narrowed to "certain fields" and the table beneath it still carried
the blanket promise.** Narrowed to match.

### The kind definition, applied a third time, moved two more rows

Round 3 settled what silent means. Round 4 applied it to rows I had not revisited and found two
Windows rows misclassified as hard floors:

- **Discovery request version.** Fleet writes a debug line and returns a fault to the device. The
  device reports the failure; **Fleet's console says nothing**, so it is silent by the definition and
  the evidence is on the machine.
- **Windows 11 25H2 without server 4.89.1.** The enrollment fails outright, the device reports error
  `80180006`, and in Fleet it is a host that never appeared.

Both re-kinded, and the claim that discovery was "the only hard floor on this table" is gone, since it
was immediately followed by another row claiming to be one.

Two rows are **no boundary at all** and now say so rather than being forced into one of the five
kinds. They are listed because their absence is the useful fact.

### Two findings in old content, which is the value of a whole read

Neither is a correction of a correction. Both are in terminology written six days ago and reviewed
until now only for its selection rule.

**File carving was described as the only path by which a file's contents leave a host through
osquery.** It is the purpose-built path and not the only one: osquery reads files line by line, and
**Fleet's own disk-encryption query uses that to ingest a key file** (`server/service/osquery_utils/queries.go:929`,
ingested at `:2951`). An absolute in a glossary entry, which is exactly where nobody looks for one.

**`mia` has a stated removal boundary and the entry said Fleet had published none.** The source says
it was deprecated in 4.15 and **will be removed in Fleet 5.0** (`server/fleet/hosts.go:1178`). In an
appendix about version boundaries, omitting a named removal version is material, and I had written
the opposite.

### Backlog, agreed with the reviewer rather than assumed

- 1.3's pointer, softened here: a.6 gives a surface-level mapping and does not enumerate every renamed
  field.
- The round-3 terminology corrections need direct source rows in this ledger rather than evidence
  living only in review history. Deferred to the whole-book citation pass.

## Rounds

| Round | Verdict | Outcome |
|---|---|---|
| 1, coverage | NOT READY, seven items | Three universals narrowed, the macOS trap corrected, the support conclusion rewritten |
| 2, evidence audit | NOT READY, six items | One wrong version split in two, "silent" defined, six rows re-kinded, five terminology entries corrected |
| 3, whole read | NOT READY, six items | Three round-2 corrections found never applied, from unasserted replacements against reflowed text. Unassigned corrected from vocabulary to data model; the a.2 deferral made honest in four chapters |
| 4, verification | NOT READY, five items | Two summaries that had outrun their tables. Two more Windows rows re-kinded. **Two new findings in old glossary content**: file carving was not the only path, and `mia` has a stated removal in 5.0 |

## Fix-loop round (2026-09-02, round4 RM2)

- **"Pin or disable" row implied `FLEET_MCP_SCHEMA_REFRESH_DISABLE` covers the manual
  `refresh_osquery_schema` tool too.** Same source verification as 6.6's RM2 fix
  (`schema.go`, `mcp_tools_queries.go`): the variable only stops the background fetch. Split
  the row in two — one for the automatic-refresh pin, one stating the manual tool still
  reaches `raw.githubusercontent.com` regardless.
