---
section: "A.2"
---

# a.2 Platform capability matrix, citation ledger

Drafted 2026-08-29 after a research pass and a corrective second pass, the first of which the
research gate returned NOT SOUND. Held to Part IX's cell-level evidence rule
([`../appendix-structure.md`](../appendix-structure.md)).

Per-cell evidence lives outside this repository, in
`../../missing-fleet-manual-private/research-sensitive/`: `a.2-scratch-core.md` carries every cell
with its `path:line`, `a.2-scratch-corrections.md` supersedes it wherever the two disagree, and
`a.2-tables.md` is the assembled matrix. Rows come from the shared register at
`../../missing-fleet-manual-private/research/capability-register.md`.

## The discipline this appendix exists to enforce, and how the first pass failed it

**A negative claim needs positive evidence of the boundary.** Absence of a code path is not evidence.
The first pass wrote `Unsupported` in a number of places where it meant "no mechanism found", which is
the one argument the part-level agreement forbids by name.

**The second pass reclassified in three directions**, and the shape is worth carrying to a.5:

| Was | Became | Because |
|---|---|---|
| `Unsupported` by omission of a delivery path | `Not established` | No boundary was found in either direction |
| `Unsupported` on a sibling platform row | `Not applicable` | Locking a Mac is not a thing ChromeOS refuses. It is a thing ChromeOS has no version of |
| `Unsupported` inherited from a neighbouring capability | Re-derived per platform | **No platform answer may be inherited from another capability**, which is the rule the "Linux has no lock and no wipe" defect produced |

**One reclassification went the other way and is the useful case.** A conditional-access capability
was marked `Unsupported` on Windows by absence; the second pass found a **real** refusal for any
platform that is not macOS or Windows, so Linux and ChromeOS became `Unsupported` with evidence and
Windows became `Not established`, which is a different question.

## The structural decision

**Licence and prerequisite are columns, not cell values.** A Premium capability is `Supported` with
`Premium` recorded beside it.

The first pass had at least fourteen cells reading `Conditional` for no reason other than a licence
gate, and several more treating an inherent delivery prerequisite as a condition. The normalisation
order, applied in the second pass and worth reusing for a.5:

1. Plan gate becomes `Supported` plus a licence.
2. Inherent delivery prerequisite becomes `Supported` plus a prerequisite, because "supported" already
   means supported once prerequisites hold.
3. Platform subtype, ownership, enrollment mode, setting-dependent behaviour or partial coverage
   becomes `Conditional`.
4. Mixed administrator intents get split into separate rows.

## The scope decision, taken and justified

**88 of the register's rows are not device-facing.** Carrying them as six-column rows would have
generated over five hundred machine-made `Not applicable` cells and presented them as coverage.
Omitting them entirely would break the four-projection invariant the part agreement sets, and would
leave a reader unable to tell "not covered here" from "no platform answer exists".

**They are carried as a one-line disposition list with no platform columns.** The matrix proper is
266 rows, after review round 1 added four capabilities the register had missed, split one, and
merged two.

**Merged, and the register still needs updating to match.** CAP-048, enrolling a personally owned
iPhone or iPad from a link, was a strict subset of CAP-029: identical on every platform except macOS,
where CAP-029 says Supported and CAP-048 said Not applicable. One administrator intent, so one row,
now named for the intent rather than for a device. **The shared register still carries both**, and
was deliberately not edited while three researchers were reading it as their row universe for a.5.
Apply the merge there before a.1, a.4 or a.5 project from it again.

**Added**, each verified at the tag rather than taken from the review: seeing your own device's
details and software as an end user, which is Free; seeing the desktop summary, which is Premium and
refused with a licence error on Free; opening the interactive query shell on the host, which starts a
separate instance and therefore does not show the running agent's state; and forcing an update check
by restarting the agent, which runs before any subsystem starts and is gated only on updates not
having been disabled at packaging time.

**Split.** Uninstalling software as an administrator and an end user uninstalling their own are
different contracts on different routes, and the second is authenticated by the device's own address
rather than by a Fleet account.

**Fixed three names that answered for platforms they did not mention**, which is the failure the
reviewer described as leaving a reader unable to infer what intent a row represents: preparing a
device rather than a Mac, installing during an automated Apple enrollment rather than an iPhone's,
and removing Fleet's management from a personally owned Android device rather than "dealing with"
one.

## Established, and the three findings the appendix leads with

| Claim | Note |
|---|---|
| **Requiring signed host requests is deployment-wide, has no platform predicate, and can only be satisfied by a Linux package** | Verified independently before it was written. Fleet's packaging refuses the option for any non-Linux package type in as many words. **Filed as C36**, the highest-consequence finding in the queue |
| **Reading a disk encryption key is Free; only escrowing was ever Premium** | So a Premium deployment that drops to Free keeps surrendering every key it holds. The first pass had this as "Premium in practice" and contradicted itself elsewhere in the same file |
| **Wipe is Free on the Android company-owned path and Premium on the other five platforms** | One licence split inside one administrator intent |
| Software inventory collection reaches only the platforms that run an agent | Corrected into 4.4, and **filed as D38** because Fleet documents the setting as collecting "from hosts" without qualification |
| Android operating-system vulnerabilities are matched; iOS and iPadOS applications are excluded outright, with Fleet's own comment saying so | Corrected into 4.4 |
| **Disabling the vulnerability source cleans up Ubuntu and RHEL findings in both directions and leaves Android findings in place** | **Filed as C33**, after I filed a weaker and partly wrong version of it first |

## Not established, deliberately

**Fourteen cells**, each with a record of what was searched. Two of them are on-device capabilities
that **Fleet's source cannot settle in either direction**, because the question is what the platform
does rather than what Fleet does; settling those needs a vendor contract this research did not have.
One row was removed outright for the same reason rather than being answered from Fleet's silence.

## Rounds

| Round | Verdict | Outcome |
|---|---|---|
| Research 1 | NOT SOUND, seven items | Negatives argued from absence; licence answers contradicting themselves; a single-pass section |
| Research 2 | Corrections applied | Section G redone; reclassifications in three directions; the scope decision taken |
| Draft review 1 | Not yet run | |
