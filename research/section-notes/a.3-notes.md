---
section: "A.3"
---

# a.3 Configuration sources, scopes, and precedence, citation ledger

Drafted 2026-08-29 after **three research rounds**, all of which returned NOT SOUND, plus a
normalisation pass. Held to Part IX's evidence rule ([`../appendix-structure.md`](../appendix-structure.md)).

Per-source and per-consumer citations are outside this repository, in
`../../missing-fleet-manual-private/research-sensitive/`: `a.3-scratch-core.md` for the server side,
`a.3-scratch-hostside.md` for the host side, `a.3-scratch-resolution.md` for the first resolution
model and `a.3-scratch-normalised.md` for the corrected one.

## The finding that shaped the appendix, and the two models it replaced

**Round 1** produced a layered model and was refused for treating a writer as an authority.

**Round 2** produced eight host-side authorities in a **single ranked chain**, with "later beats
earlier where they overlap". **Round 3 refused that too, and was right**: an overlap is not one
relation. It can be precedence, fallback, write-through, composition, mutual exclusion, or a channel
being removed so that nothing is compared at all. There is a confirmed instance of each, and a single
path routinely uses three or four.

**So the appendix carries a catalogue plus per-consumer resolution**, never one order. The counts,
which the appendix deliberately does not lead with: **18 sources, 18 numbered resolution points, of
which 16 arbitrate and 2 are single-authority reads.**

## Established at the tag

| Claim | Note |
|---|---|
| Within the server's process configuration: explicit flag, then non-empty environment, then file, then default. Empty environment variables ignored | The one place a simple order holds |
| Mounted secret and secret-manager values are read **once** and never re-read | Changing the file under a running server does nothing |
| **The device-management asset store outranks the process configuration after first boot** | Added at the normalisation pass; its absence was why one consumer looked one-sided |
| Fleet **warns rather than refuses** when configuration-supplied certificates are being ignored | The startup log says so; nothing enforces it |
| **The Apple Business Manager token file is parsed on every boot before the store is consulted** | A broken path stays fatal even when the parsed value is discarded |
| The macOS profile sets the Fleet URL and enrol secret unconditionally, **and the comment above it describes a guard the code does not have** | Verified independently at round 2 and again at round 3 |
| Disabling updates removes the receiver, so the last persisted override is permanent | Which narrows C29: the `stable` defect holds only while the receiver is enabled |
| osquery agent options take the fleet's document whole or the global one, never a mix. Platform overrides replace | Already carried by 1.3 |
| The Orbit half has no fallback except the script execution timeout, whose condition tests zero | |
| A locally set debug flag is a floor the server cannot lower; the profile may enable scripts and cannot disable them | Compositions, not precedence |
| GitOps: YARA rules cleared, certificate authorities cleared **through a queued second pass with deletion enabled**, conditional access left alone, expiry blocks left alone | The certificate-authority route was the last field established |
| The server replaces four blocks wholesale on any spec apply, so omitting single sign-on clears it | **The rule is the writer, not the field** |
| Nine keys survive omission | Corrected from "three", which contradicted the file's own table |
| The organisation settings document is **audited by exception**, about forty per-block activity types with no document-level fallback | SMTP, server URL and host expiry confirmed to write nothing |
| **No surface reports the running server's effective configuration.** The configuration dump starts a new process | Replaced the provenance row that had claimed otherwise |
| Fleet asks every host for its configuration hash **on each detail cycle** and discards it | Narrowed at round 3 from "every poll" |
| 320 keys registered by the configuration manager | Independently reproduced by the reviewer |

## Four reference discrepancies, published

A per-endpoint request-size override documented in full and **bound nowhere**; the Redis host-cache
lifetime documented as 60 seconds and registered as 180; the MySQL password documented as defaulting
to `fleet` and registering empty; and the private-key external identifier documented under an
environment variable the server does not read. All four are in the defect queue as D32 to D35.

## Not established, and deliberately not published

**How many of the 320 registered keys Fleet documents.** An earlier draft published 232 documented
and 93 undocumented. **The reviewer refused both**, because "documented" had not been defined
consistently: a setting may have its own reference section, be described in prose under another, or
appear only in an example, and the three counts differ. The appendix states the registered count,
which is derived, and declines the comparison until it can be produced by a reproducible parse. **No
Go toolchain is available on this machine**, which is what blocks that.

**Two GitOps fields** were open at round 3 and were settled by the reviewer directly; both are in the
table above.

## Corrections this research forced into finished chapters

| Chapter | What changed |
|---|---|
| **1.3** | The agent-options inheritance row, which was true of one case and false of the other, and had already been corrected once |
| **2.4** | A fleet cannot opt out of host expiry, only change its window. And the count of reference disagreements, twice: raised to seven, then withdrawn entirely as underived |
| **6.2** | The GitOps agent-options row, wrong in both of its last two cells |
| **5.2** | **Rotating a secret redelivers nothing.** Filed as C28 |
| **8.11** | Remote flags overwrite the local flagfile rather than losing to it |
| **1.5, 8.12** | The audit trail is by exception, not complete |

## Rounds

| Round | Verdict | Outcome |
|---|---|---|
| Research 1 | NOT SOUND, ten items | Host side entirely unchased |
| Research 2 | NOT SOUND, seven items | Eight authorities established; the ranked chain proposed |
| Research 3 | NOT SOUND, seven items | The chain refused; six mechanisms established |
| Normalisation | Applied | Units defined, counts restated, the asset store added, the provenance row replaced |
| Draft review 1 | Not yet run | |
