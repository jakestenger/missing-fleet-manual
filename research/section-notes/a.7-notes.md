---
section: "A.7"
---

# a.7 fleetctl command index and behaviour, citation ledger

Drafted 2026-08-29, from research that went through **four rounds, every one of which returned NOT
SOUND**, plus an agreed outline that came back CHANGES REQUIRED and was settled in one pass. Held to
Part IX's evidence rule ([`../appendix-structure.md`](../appendix-structure.md)) and to the
organising claim in the same file: `fleetctl` is a set of operator requests whose contract is what
each command asks Fleet to do and what its result proves, not a transcription of `--help`.

**The verification trail lives outside this repository**, per `README.md` in this folder. The
per-row citations are in `../../missing-fleet-manual-private/research-sensitive/`:

| File | What it holds |
|---|---|
| `a.7-scratch-core.md` | The inventory, the configuration and credential model, output modes, global options, the client-side defects, and a re-verification of all 50 `fleetctl` claims already live in drafted chapters |
| `a.7-scratch-contracts.md` | **The authoritative file.** Permission chains as ordered chains, the edition split, the extended exit-zero register, the deprecation recount, the destructive ranking, and the owning-chapter mapping for all 69 rows |
| `a.7-exit-zero-register.md` | The derivation of the register's class and its first thirteen rows |

The agreed outline is `../../missing-fleet-manual-private/research/a.7-outline-agreed.md` and the
research consensus is `a.7-consensus.md` beside it. **Where the scratch files and the outline
disagree, the scratch files win**, and one place they do: the outline says seventeen exit-zero cases
and the register is 33. The outline's ruling that they are all published rather than summarised to a
count is unaffected and was followed.

## Provenance, and why it is stated in the appendix itself

**The inventory is the assembled root command tree at `fleet-v4.90.1` (`dd0200f062`), not the output
of any binary.** No `fleetctl` trustworthy as 4.90.1 was available on this machine, and Part IX's
ruling is that the appendix says so rather than implying it interrogated a client. It does, in its
second section.

**Nothing here comes from `--help` output, from fleetdm.com, or from `docs/`.** Fleet's
documentation was used for leads and never as evidence, which matters more than usual for this
appendix, because the published CLI reference is generated and this project has already caught it
stale in three places in one file.

**Four mechanisms make a static file search under-report the tree**, and all four are published,
because each is also a way two machines on the same release can differ: the query-shell runner is
injected at run time (`cmd/fleetctl/main.go:21`, `goquery.go:15-21`); the update family is build
tagged (`ee/fleetctl/updates.go:1` against `ee/fleetctl/updates_windows.go:1`); a helper appends two
flags to every `get` subcommand at construction (`flags.go:107-120`, applied `get.go:485`); and three
`debug` leaves are built by a shared helper (`debug.go:664`, `:678`, `:692`, helper `:706`), so a
search for command constructors finds nine of twelve.

## Established at the tag

| Claim | Basis | Where it is evidenced |
|---|---|---|
| **27 top-level names, 50 leaves, 77 named entries, 69 behavioural rows** on macOS and Linux | Stated | `fleetctl.go:37-80` counted literally; leaves per family in `a.7-scratch-contracts.md` §1.3 |
| **72 named entries on Windows**, the update family reduced to a terminal error stub | Stated | `ee/fleetctl/updates_windows.go:12-23`, a `Before` hook that returns an error unconditionally, with no `Action` and no `Subcommands` |
| **19 of the 27 top-level commands act; 8 are pure parents** | Stated | Presence of an `Action` field on each constructed object, `a.7-scratch-contracts.md` §1.2 |
| **A two-gate authenticated prefix on 51 of the 69 rows**: a hard `version · read`, then a 403-tolerated `app_config · read` | Stated | `api.go:56-121`; version call `:90`, gate `server/service/appconfig.go:2601`; config call `:109`, gate `appconfig.go:252`; the 403 swallow at `:115-116` with Fleet's own comment naming the gitops role |
| **The 18 rows without the prefix are exactly the 18 with no Fleet authorization** | Derived, and the derivation is the useful part: the two sets were built independently, one from client construction and one from authorization decisions, and they coincide | `a.7-scratch-contracts.md` §2.0a for the 18, §7.2 for the shapes |
| **A permission contract is an ordered chain, and a role can clear the last gate and fail an earlier one** | Stated, with a worked case | `fleetctl mdm lock` reaches `server/service/hosts.go:1061`, `:1071`, then `ee/server/service/hosts.go:49` and `:60`. Gate 3 is a **broad global** `host · list` that a role holding `mdm_command · write` for the fleet still has to clear |
| **A chain is a property of a command on an edition**, in two shapes | Stated | Type 1: the community method skips authorization and returns a licence error (`server/service/scripts.go:1234-1240`, `:1263-1269`, `server/service/mdm.go:4335-4341`). Type 2: one implementation with an inline licence branch whose position differs (`scripts.go:1287`/`:1298`/`:1303-1307` against `scripts.go:125-126`) |
| **Seventeen rows split by edition**, ten of the first kind and seven of the second, with `apply -f` in both | Derived, and **published as a floor** | `a.7-scratch-contracts.md` §2.6.1. The floor is because the Type-1 stub pattern repeats at nine sites in community `teams.go` and any further path reaching one inherits the split |
| **The exit-zero register is 33 rows** | Derived under a stated class | `a.7-scratch-contracts.md` §3; class in `a.7-exit-zero-register.md` |
| **Two deliberate exit codes, 0 and 1** | Stated, with scope | Only `cmd/fleetctl/main.go:27` and `:47`. **Scoped in the appendix to what the program returns**, because signals and launcher failures produce other statuses |
| **Two error paths writing to different streams** | Stated for the paths, `Not established` for the mapping | `main.go:37` to the app's error writer, `main.go:26` to standard output. See below |
| **No app-level global flags** | Stated | `app.Flags` is never assigned, `fleetctl.go:18-82` |
| **The near-global flags are missing from eight leaves and two commands** | Stated | `package.go:36-269`, `new.go:61-80`, `mdm.go:42/170/223/274/311`, `generate.go:38-40` and `:117-120` |
| **Most client environment variables are unprefixed** | Stated, enumerated | `a.7-scratch-core.md` §5.4, verbatim from the flag definitions. `INSECURE` at `config.go:251`, `TOKEN` at `:246`, `PASSWORD` at `login.go:42` and `setup.go:45` |
| **Nineteen deprecation notices, fourteen gated and five ungated** | Stated | `a.7-scratch-contracts.md` §4.1, notice by notice with its call site. The topic constant is at `server/platform/logging/topics.go:7` and topics are enabled by default at `:11-13` |
| **One hidden command and three hidden flags** | Stated | `generate_gitops.go:283`, `gitops.go:76`, `:84`, `preview.go:160`. Established by grepping `Hidden` across `cmd/fleetctl/` and `ee/fleetctl/`: exactly four declarations |
| **Eleven terminal reads, none of them a confirmation** | Stated for the eleven, **`Not established` for exclusivity** | `login.go:85`, `setup.go:69`/`:77`, `user.go:149`/`:151`/`:165`/`:175`, `new.go:107`, `ee/fleetctl/updates.go:746`/`:758`. The appendix publishes the bound: a prompt built on a mechanism outside the enumerated set would not have been found |
| **`mdm wipe` is four different actions**, one per platform, and on Linux is not MDM at all | Stated | `ee/server/service/hosts.go:511-565`. The appendix drops "every byte", which the source does not support |
| **`fleetctl --version` never contacts the server** | Stated | `fleetctl.go:29-31`, values from `server/version/version.go:72-80` |
| **A version mismatch warns and continues** | Stated | `api.go:98-105`, with Fleet's own comment saying so |
| **All 50 `fleetctl` claims already published in drafted chapters** re-verified at the tag | Stated | `a.7-scratch-core.md` §0.1. **No command named anywhere in the book is missing from 4.90.1** |

## Deliberately not established

**Two questions end at a boundary this checkout does not carry, and both stay open in the
appendix.** A round-1 revision moved the first to established on the strength of the pinned
dependency's own upstream source; that was overturned, because the gate's rule is that this checkout
is the only source of truth and **upstream library source is not evidence**. The paragraphs that
read the library were removed rather than softened.

| Question | What Fleet's own source does establish | What was searched |
|---|---|---|
| **Whether `--config` placed after a subcommand that does not declare it parses** | The parent declares it (`mdm.go:22`, `generate.go:21`), the eight leaves do not, and the client reads a `--config` value regardless (`api.go:56`, call at `:62`). `go.mod:147` fixes the library version and nothing about its behaviour | `grep -rn -- '"--config"'` across `cmd/fleetctl/`: 40 test hits, every one in the parent's position or after a leaf that declares the flag. No `vendor/` directory. Two ways to settle it, neither available: an in-tree test at one of the eight placements, or a vendored implementation |
| **Which class of error reaches which output stream** | Two exits exist and they use different streams (`main.go:26` to standard output, `main.go:37` to the error writer) | The dispatch is the framework's. The appendix says two paths exist, tells the reader to capture both streams, and **assigns no class to either path** |

**Three further gaps, each published rather than resolved by inference:**

**Whether `fleetctl updates` is licence-enforced.** Positively established: the enterprise-licence
sentence is the parent command's description text (`ee/fleetctl/updates.go:74`, `Description`
`:78-80`, sentence `:80`), and each of the five actions works on a local repository under `--path`.
**Whether any layer enforces it is not established**, and the earlier conclusion that the constraint
was contractual rather than technical is withdrawn, because it rested on not finding a check.
Searched: both update files in full, case-insensitively, for `license`, `licence` and `premium`.

**Whether the exit-zero register is complete.** It is a floor and the appendix says so, with the
three specific places a thirty-fourth case could hide (`a.7-scratch-contracts.md` §3.5).

**Whether any permission chain is complete.** Also a floor. A chain is established by reading the
handler and the services it calls, so middleware, a wrapper this research did not assemble, or a
gate on a branch not exercised would not appear.

## The structural decisions, and the reasoning behind each

### The common prefix is stated once and every row is a suffix

**Repeating it in 51 rows states one fact 51 times**, and in this file's own history that is exactly
the mechanism that produced contradictions between rows. The appendix states the two gates in the
resolution section, names their different failure behaviour, and then says in the index legend that
every access contract is the suffix after them. A row showing an application-configuration read is
therefore showing a **second, command-specific** one, and `run-script` is called out because its
second read is the one that does **not** tolerate a 403 (`scripts.go:76-79`).

**The reader's cost is one paragraph of memory and the benefit is that the 51 rows agree with each
other.** The alternative that was rejected was a per-row footnote marker, which is the same repetition
with an indirection added.

### The edition split is carried in the row, and the seventeen are also listed together

Round 3's finding was that one chain per command is a **model error**, not a missing detail. So:

- **Each of the seventeen rows carries both answers inline**, because a reader who holds the last
  permission on Free and is refused has been told the wrong thing by a footnote.
- **The Free answer for a Type-1 row reads "no permission is evaluated at all"**, not "fewer gates".
  That is a different kind of answer and it has a consequence the appendix states: a Free refusal
  tells the operator nothing about their permissions, and Premium can then refuse them again on
  grounds they have not yet seen.
- **A locator table follows the index**, listing the seventeen with their kind, because STYLE §26
  makes a stated count a promise that the items are findable, and seventeen rows scattered through 69
  are not.
- **The five rows checked and found not to split are recorded**, so the question is not reopened.

### Eight parents are headings rather than rows

**A row for a command that does nothing is a fictitious behaviour.** `get`, `config`, `user`,
`debug`, `updates`, `hosts`, `generate` and `mdm` hold no `Action`. They appear as group headings.
`preview` is the trap and is a row: it has both an action and two subcommands.

### The sixteen unowned commands are published as a finding

**Chapters were read rather than inferred from titles**, and where no chapter teaches the workflow a
command serves, the row says `None` rather than being assigned to the nearest plausible chapter.
Six groups, listed in the appendix: legacy packs, the self-hosted update repository, the local
sandbox, carve retrieval, first-run setup with the interactive shell, and supplying vulnerability
data yourself. **The group table and the `None` rows were reconciled by count**, because a first
pass wrote five groups covering fifteen commands under a heading that said sixteen, which is the
same defect class as a stated count with unfindable items.

**Two of them are worth the owner's attention rather than a.7's.** `6.4:L59` asserts that 3.7 owns
the packaging and update-repository semantics, and **that deferral is unfulfilled**: 3.7 teaches
consuming Fleet's repository and never creating one. And `setup` and `goquery` have zero occurrences
anywhere in the manual, so no chapter covers standing a server up or creating its first
administrator.

**One row is in the list against the raw evidence.** `3.7:L51` does name `updates add`, in a
subordinate clause carrying a licence claim and a platform limit. That is a mention rather than a
chapter explaining the workflow, and assigning it would split the update family across two answers
and let the unfulfilled deferral pass unnoticed. **If the owner prefers the literal reading, that row
moves to 3.7 and the count becomes fifteen.**

### The register states its class before its rows

The earlier "seventeen cases" was refused by the research consensus because **the number had no
inclusion rule**. The published class is a materially adverse, incomplete or refused advertised
outcome that the code detected, where the invocation returns success anyway, with expected absence,
asynchronous acceptance and pending results excluded by name. **Asynchronous acceptance is not a
defect and is carried in the index's result column instead**, which is why the five `mdm`
subcommands are not register rows.

### Both large enumerations are published as floors

The chains and the register are floors, and the appendix says so in its own words rather than
implying completeness. Where a list **is** complete, such as the 27 top-level names and the four
hidden declarations, it says that too. The asymmetry is deliberate: this project's dominant defect
class is a confident claim built from a partial reading.

### What was cut, and why

**No command-to-API cross-reference**, which the stub outline promised and Part IX's enumeration line
forbids. Route-level questions are [a.8](../../manual/09-appendices/a.8-api-action-and-endpoint-reference.md)'s.

**No flag tables and no worked examples.** The appendix points at `fleetctl <command> --help` for
syntax, which is the only listing guaranteed to match the reader's binary, and at 6.4 for practice.

**No source citations in reader-facing prose.** STYLE §8. Every `path:line` in the research stayed in
the research. What survives into the appendix is Fleet's authorization vocabulary in the form
`object · action`, on the same grounds a.4 kept it: it is Fleet's own vocabulary rather than an
implementation detail, and it is the only way a reader can trace a chain into a.4's matrix.

## Defects, and what is already filed

**The a.7 research produced five defect candidates and all five are already in the queue**, under
numbers issued before this drafting pass:

| Research label | Queue | What it is |
|---|---|---|
| C46 | **C38** | `delete -f` suppresses the spec-file deprecation notices `apply -f` prints for the same file |
| C47 | **C39** | Five of nineteen deprecation notices ignore the flag meant to silence them |
| S17 | **S15** | A key rotation that reports success can leave the retired private keys on disk |
| C48 | **C47** | `fleetctl report` without a timeout can hang forever, with no exit status |
| C49 | **C48** | `run-script` re-reads the application configuration without the 403 tolerance its own preflight applies |

**The research's own numbering collides with the queue in two places** (its S17 is the queue's S15;
its C48 and C49 are the queue's C47 and C48). The queue is authoritative and the research file says
so itself; nothing was renumbered in the research, which is an agreed artefact.

**Three findings in the research are defect-shaped and are not in the queue.** They were carried into
the appendix as behaviour and are recorded here for the queue owner. None was re-verified during
drafting, so each is cited to the research rather than presented as a new source check:

- **`generate-gitops`' client-side administrator check does not hold for a fleet-scoped account**, and
  it returns success when it does refuse. `cmd/fleetctl/fleetctl/generate_gitops.go:364`, print
  `:365`, `return nil` `:366`. Compare `upgrade_packs.go:48`, which tests the nil case correctly.
  Class C.
- **`preview` replaces every context in a configuration file that exists and does not parse**, silently.
  `preview.go:354-360`, written at `:369`. The branch not taken carries the message saying the
  opposite was intended. Class C.
- **`get mdm-commands` removes commands the caller may not read and reports the pre-filter count**,
  returning success. `server/service/mdm.go:1195-1200`, filter `:1203-1218`, count not recomputed
  `:1217`, authorization error discarded `:1227`. Its sibling `get mdm-command-results` fails loudly
  on the same condition, so the two are genuinely different contracts. Class C.

## Rounds

| Round | Verdict | Outcome |
|---|---|---|
| Outline | CHANGES REQUIRED, five corrections | All five accepted verbatim. The exit-zero cases are published rather than counted; every ordinary command gets a full row; the inventory is leaves **plus** action-bearing top-level commands; pure parents are headings; a miscellaneous section was refused |
| Research 1 | NOT SOUND | The permission field was rebuilt from "server-side only" into per-command contracts. Deprecation surfaces recounted, hidden-flag heading fixed, `mdm wipe` made per-platform, destructive ranking built on a rubric |
| Research 2 | NOT SOUND | Contracts became **ordered chains** rather than the terminal authorization call. `--config` reverted to `Not established`. Four register rows corrected, five negative-from-absence claims re-argued or marked `Not established` |
| Research 3 | NOT SOUND | **Chains became edition-dependent.** The five "composite" rows rebuilt as chains, `report` and `get fleets` corrected, Z33 added, the `preview` tail settled, the owning-chapter field created |
| Research 4 | NOT SOUND | **The common authenticated prefix factored out.** The edition split corrected to seventeen, four per-fleet subchains expanded, Z11 reattributed and Z26 conditioned, ownership recounted |
| Draft review 1 | Not yet run | |

**Part IX sets three review rounds for an appendix and they do three different jobs**: coverage,
a cell-by-cell evidence audit, and a fresh whole-appendix read against the register and the chapters.
None has been run against this draft. **The rounds above are research rounds, not draft reviews**,
and the distinction is the one CONTRIBUTING makes when it says verification is necessary and not
sufficient.
