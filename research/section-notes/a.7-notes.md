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
and the register is 34, having been 33 until draft review 3 found a qualifying row. The outline's ruling that they are all published rather than summarised to a
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
| **72 named entries and 65 behavioural rows on Windows**, the update family reduced to a terminal error stub, **now carried as a row of its own** | Stated. The row was added in draft review 1, finding 1 | `ee/fleetctl/updates_windows.go:12-23`, a `Before` hook that returns an error unconditionally, with no `Action`, no `Subcommands` and no `Flags`. Registered unconditionally for every platform at `fleetctl.go:59`; the split is the build tags at `ee/fleetctl/updates.go:1` against `ee/fleetctl/updates_windows.go:1`. It never exits zero (`cmd/fleetctl/main.go:25-28`, `:32-47`) |
| **19 of the 27 top-level commands act; 8 are pure parents** | Stated | Presence of an `Action` field on each constructed object, `a.7-scratch-contracts.md` §1.2 |
| **A two-gate authenticated prefix on 51 of the 69 rows**: a hard `version · read`, then a 403-tolerated `app_config · read` | Stated | `api.go:56-121`; version call `:90`, gate `server/service/appconfig.go:2601`; config call `:109`, gate `appconfig.go:252`; the 403 swallow at `:115-116` with Fleet's own comment naming the gitops role |
| **18 rows without the prefix, and 17 with no Fleet authorization.** The two sets differ by one row and the row is `preview` | **Corrected in draft review 1, findings 2 and 4.** The earlier entry claimed the two sets coincide; they do not, and the draft's narrower phrase "your Fleet" avoided the literal contradiction while leaving the structural proposition wrong | `a.7-scratch-contracts.md` §2.0a for the 18. `preview` builds an unauthenticated client (`preview.go:374`), sets the sandbox up (`:335`), logs in (`:379`, token stored `:384`, set `:387`), installs the starter library (`:396` into `server/service/endpoint_setup.go:122-124` app-config read and `:165-181` a nested `fleetctl gitops` that itself goes through `clientFromCLI` at `gitops.go:131`), PATCHes the application configuration twice (`:411-416`, `:428-432`), reads the enroll secret (`:418`) and lists hosts (`:451` via `:695`). Server gates: `appconfig.go:252` read, `:529` write, `:2570` enroll secret, `hosts.go:450` host list |
| **A permission contract is an ordered chain, and a role can clear the last gate and fail an earlier one** | Stated, with a worked case | `fleetctl mdm lock` reaches `server/service/hosts.go:1061`, `:1071`, then `ee/server/service/hosts.go:49` and `:60`. Gate 3 is a **broad global** `host · list` that a role holding `mdm_command · write` for the fleet still has to clear |
| **A chain is a property of a command on an edition**, in two shapes, **and shape one is a property of a service node rather than of the command** | Stated. The node-versus-command distinction was **corrected in draft review 1, finding 3** | Type 1: the community method skips authorization and returns a licence error (`server/service/scripts.go:1234-1240`, `:1263-1269`, `server/service/mdm.go:4335-4341`). **But the command reaches authorization before it**: the client resolves the host at `cmd/fleetctl/fleetctl/mdm.go:343`/`:353`, reaching `host · selective_list` at `server/service/hosts.go:1061` and `host · selective_read` at `:1071` on both editions. Type 2: one implementation with an inline licence branch whose position differs. **`run-script`'s licence gate is `scripts.go:122-128`, before the host-result authorization at `:179`**, not late; it is conditional on a fleet identifier being supplied. `mdm wipe` is the late one (`scripts.go:1287`/`:1298`/`:1303-1307`) |
| **Seventeen rows split by edition**, **twelve** of the first kind and **seven** of the second, with **`apply -f` and `gitops`** in both | Derived, **published as a floor**. The second count was corrected from seven in draft review 1; the first from ten in draft review 2, finding 10 | `a.7-scratch-contracts.md` §2.6.1. The floor is because the Type-1 stub pattern repeats at nine sites in community `teams.go`. **Arithmetic:** ten rows are first-kind only, two are both, five are second-kind only, so 10 + 2 + 5 = 17 distinct rows and the subtotals are 12 and 7, summing to 19. **Two reviewers have now proposed wrong subtotals for this table.** Draft review 2 proposed 10 and 9, which needs seven second-kind-only rows against the table's six. Draft review 3 was right that `run-script` is first-kind, not second (`server/service/scripts.go:125-126` skips authorization and refuses for the licence before the `script · read` at `:83` and the `host_script_result · write` at `:179`), but stated the post-move result as 9 + 2 + 6, subtotals 11 and 8, which is the **pre-move** membership: moving one row out of second-kind-only must add one to the first bucket and take one from the third. **Both rows are in both kinds, but not for the reason draft review 1 gave.** `ApplyLabelSpecs` does authorize at `server/service/labels.go:692` before the licence check at `:699`, but that check is conditional on a non-nil, non-zero fleet: `apply` always passes nil (`server/service/client.go:605`), and a Free `gitops` never sends a fleet-scoped label write because the client skips non-global files first (`cmd/fleetctl/fleetctl/gitops.go:290-293`). What actually puts both rows in the second kind is **label-scoped policies** (`server/service/global_policies.go:457-459`, comment "Check authorization first", licence refusal `:493-494`) and **label-scoped configuration profiles** (`server/service/mdm.go:2428` authorizing via `:2852`, licence refusal `:2470-2471`). Conversely a **label-scoped report is first-kind**, not second: `server/service/queries.go` refuses the licence in its validation pass before the authorization pass. `get labels --fleet` and `get software --fleet` remain second-kind (`labels.go:986` then `:990-992`; `software_titles.go:75-79` then `:86-88`) |
| **The exit-zero register is 34 rows** | Derived under a stated class, **corrected from 33 in draft review 3, finding 1** | `a.7-scratch-contracts.md` §3; class in `a.7-exit-zero-register.md`. Z34 is `get mdm-command-results` without `--host`: `server/service/mdm.go:826` loads every result, `:845-847` lists only the hosts the caller's team filter admits, `:888-901` drops each result whose host is missing, `:851-855` returns nil when none survive, and `cmd/fleetctl/fleetctl/get.go:1800-1803` prints "No results received. Please check again later." and returns nil. **The `mdm_command · read` at `:871-881` looks fatal and cannot fire on the withheld results**, because its team set is built from the already-filtered hosts. The `--host` form at `:1025` does authorize fatally, which is why the row now carries two variants |
| **Two deliberate exit codes, 0 and 1** | Stated, with scope | Only `cmd/fleetctl/main.go:27` and `:47`. **Scoped in the appendix to what the program returns**, because signals and launcher failures produce other statuses |
| **Two error paths writing to different streams** | Stated for the paths, `Not established` for the mapping | `main.go:37` to the app's error writer, `main.go:26` to standard output. See below |
| **No app-level global flags** | Stated | `app.Flags` is never assigned, `fleetctl.go:18-82` |
| **The near-global flags are missing from eight leaves and two commands** | Stated | `package.go:36-269`, `new.go:61-80`, `mdm.go:42/170/223/274/311`, `generate.go:38-40` and `:117-120` |
| **Most client environment variables are unprefixed** | Stated, enumerated | `a.7-scratch-core.md` §5.4, verbatim from the flag definitions. `INSECURE` at `config.go:251`, `TOKEN` at `:246`, `PASSWORD` at `login.go:42` and `setup.go:45` |
| **Nineteen deprecation notices, fourteen gated and five ungated** | Stated | `a.7-scratch-contracts.md` §4.1, notice by notice with its call site. The topic constant is at `server/platform/logging/topics.go:7` and topics are enabled by default at `:11-13` |
| **One hidden command and three hidden flags** | Stated | `generate_gitops.go:283`, `gitops.go:76`, `:84`, `preview.go:160`. Established by grepping `Hidden` across `cmd/fleetctl/` and `ee/fleetctl/`: exactly four declarations |
| **Ten terminal reads, nine of them a credential or a name, none of them a confirmation** | Stated for the ten, **`Not established` for exclusivity**. **Corrected from eleven in draft review 1, finding 8** | `login.go:76` (email) and `:85` (password), `setup.go:69`/`:77`, `user.go:151` (a single arbitrary keystroke gating the API-token reveal, guarded by the terminal test at `:149`), `user.go:165`/`:175`, `new.go:107` (promptui, invisible to a stdin grep), `ee/fleetctl/updates.go:746`/`:758` (skipped when the role passphrase variable is set, `:727-734`). **The published eleven counted the guard at `user.go:149` as a read and missed the login email**, and the tenth read is neither a credential nor a name. The appendix publishes the bound: a prompt built on a mechanism outside the enumerated set would not have been found |
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

### The fifteen unowned commands are published as a finding

**Chapters were read rather than inferred from titles**, and where no chapter teaches the workflow a
command serves, the row says `None` rather than being assigned to the nearest plausible chapter.
Six groups, listed in the appendix: legacy packs, the self-hosted update repository, the local
sandbox, carve retrieval, first-run setup, and supplying vulnerability data yourself. **The group
table and the `None` rows were reconciled by count**, because a first pass wrote five groups
covering fifteen commands under a heading that said sixteen, which is the same defect class as a
stated count with unfindable items.

**`goquery` was moved from unowned to 4.2 in draft review 1, finding 7, and that reverses an
earlier decision recorded here.** The earlier reasoning is at `a.7-scratch-contracts.md:1287` and
`:1295`: `goquery` has zero occurrences anywhere in the manual, 4.2's CLI passage enumerates only
`fleetctl report` and `fleetctl get reports`, and on that ground the row stayed `None`.
**The workflow rule wins over the command list**, because the rule this appendix publishes is that a
chapter owns a row when it explains the workflow the command serves, and the converse of "a mention
is not ownership" is that a chapter can own a workflow without naming the command that performs it.
`goquery` resolves a host (`goquerycmd/goquery.go:46-73`) and runs a live query against it
(`:75-107`, live query issued at `:84`); 4.2 opens by claiming "asking your own questions"
(`4.2-run-queries-and-reports.md:22`) and defines the live-report workflow over the osquery
distributed channel (`:81`, `:85-98`). Reading ownership off the chapter's command list rather than
off its workflow is the same error as reading it off a title. **The Unix counts become 54 owned and
15 unowned**, and the absence of the command's name from 4.2 stays a gap in 4.2 rather than a reason
to leave the row unowned.

**Two things are worth the owner's attention rather than a.7's.** `6.4:L59` asserts that 3.8 owns
the packaging and update-repository semantics, and **that deferral is unfulfilled**: 3.8 teaches
consuming Fleet's repository and never creating one. And `setup` has zero occurrences anywhere in
the manual, so no chapter covers standing a server up or creating its first administrator.
`goquery` has zero occurrences too, and **4.2 should name it**, now that 4.2 owns it.

**One row is in the list against the raw evidence.** `3.8:L51` does name `updates add`, in a
subordinate clause carrying a licence claim and a platform limit. That is a mention rather than a
chapter explaining the workflow, and assigning it would split the update family across two answers
and let the unfulfilled deferral pass unnoticed. **If the owner prefers the literal reading, that row
moves to 3.8 and the count becomes fifteen.**

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

### The `object · action` pairs stay, and the question is closed

**Draft review 1's finding 9 was overruled by the owner on 2026-08-29, and the contradiction is
recorded here so the next round does not reopen it.**

The a.7 reviewer ruled that the access column's `object · action` pairs are internal authorization
identifiers banned by STYLE §8, citing `a.7-sol-r1.out` finding 9. **The same reviewer ruled the
opposite way on the identical question in a.4**, in `2026-08-28/appendices/a.4-sol-r1.out:1`, in as
many words: "Keep the `object · action` pairs—they are essential authorization vocabulary and make
the action dimension traceable without violating the prohibition on source locations."

**The a.4 ruling stands and a.7 follows it.** a.4 publishes 325 of these pairs and justifies them in
its own prose; a.7 publishes 111 of the same vocabulary. Changing one appendix and not the other
would break the cross-appendix consistency the part structure exists to protect, and would sever the
only route a reader has from a command's chain in a.7 into a.4's matrix. STYLE §8's prohibition is on
Go file names, paths, line numbers, function names and implementation symbols; none of those appears
in this appendix, and the reviewer's own sweep confirmed it. **No change was made for finding 9.**

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
| S17 | **S15** | A key rotation that reports success can leave its own cleanup unfinished, with a warning that does not say how far it got. **Restated in draft review 2, finding 6, and the queue entry needs the same correction.** The earlier form said the failure leaves the retired private keys on disk; the source does not establish that. `ee/fleetctl/updates.go:505-514` removes the repository backup first and returns immediately if that fails (`:507-509`), so the keys backup removal at `:510` may never run; and `os.RemoveAll` can fail on the directory after removing its contents. The warning is printed at `:432-434` after the command has already returned nil at `:490`, so the exit status is zero either way. What is established is an unfinished cleanup of unstated extent |
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
- **`get mdm-commands` removes commands the caller may not read and reports success without saying
  the result is partial.** `server/service/mdm.go:1203-1218` filters after taking the total at
  `:1161`, never recomputes it, logs "unauthorized to view some team commands" server-side at
  `:1203-1204`, and discards the authorization error at `:1227`. Its sibling `get mdm-command-results`
  fails loudly on the same condition, so the two are genuinely different contracts. Class C.
  **Restated in draft review 1, finding 5.** The earlier form said the client reports the pre-filter
  count; it does not. The server's `count` never reaches the client (`server/service/client_mdm.go:318`
  returns only `Results`) and `fleetctl` prints `len(results)` (`cmd/fleetctl/fleetctl/get.go:1889`),
  so the printed count matches the printed rows. The defect is the silence, not a mismatch.

**One further defect candidate, found during draft review 1 and not in the queue.** It is a new
source check rather than a carry-over from the research:

- **`fleetctl run-script` waiting for its result can poll forever.** `server/service/client_scripts.go:100-135`
  is a bare loop with no deadline, no attempt limit and no context, sleeping
  `pollWaitTime` (`:19`, five seconds) and breaking only on a non-nil `ExitCode`. The ordinary API
  client sets no overall HTTP timeout (`client/base_client.go:203` passes no `WithTimeout`, so
  `pkg/fleethttp/fleethttp.go:194-203` builds `http.Client{Timeout: 0}`; only a 30 s dial timeout is
  set at `:263-266`). Where the host runs the script this is bounded, because the agent's own
  execution limit (`pkg/scripts/scripts.go:10`) produces exit code `-1`
  (`server/fleet/scripts.go:361-363`). Where no result is ever recorded, the server **does** detect
  it, computing a host timeout at `server/service/scripts.go:319-320` and setting
  `RunScriptHostTimeoutErrMsg` (`server/fleet/errors.go:530`), **but `exit_code` stays null and the
  poll loop tests only `exit_code`**, so the timeout signal arrives every five seconds and is
  discarded. Same shape as the queue's C47 for `report`. Class C.

**Two further candidates found during draft review 3**, neither in the queue. The silent
result-filtering itself is already filed as C57 on the a.4 side; these are separate:

- **`get mdm-command-results --host` returns a server error where it means a refusal.** When the
  named host exists but falls outside the caller's team filter, `server/service/mdm.go:1016-1018`
  returns `ctxerr.Errorf(... "unexpected result for host identifier %s")`, which surfaces as HTTP
  500 rather than the 403 the situation calls for. The exit status is non-zero either way, so this
  is not a register row; it is a misleading failure mode, and it defeats the client's own 403
  handler at `cmd/fleetctl/fleetctl/get.go:1746-1751`. Class C.
- **Both `generate` subcommands write their local file before the step that can still fail.**
  `cmd/fleetctl/fleetctl/generate.go:64` writes the CSR and `:146` writes the ABM public key, in
  both cases before `GetAppConfig` at `:69` and `:151`. A failure there exits non-zero with the file
  already on disk, and, from the first successful run onward, with the server-side key material
  already persisted. Cosmetic beside C57, but it is why the appendix's result cells now say what a
  failure does not undo. Class D.

## Rounds

| Round | Verdict | Outcome |
|---|---|---|
| Outline | CHANGES REQUIRED, five corrections | All five accepted verbatim. The exit-zero cases are published rather than counted; every ordinary command gets a full row; the inventory is leaves **plus** action-bearing top-level commands; pure parents are headings; a miscellaneous section was refused |
| Research 1 | NOT SOUND | The permission field was rebuilt from "server-side only" into per-command contracts. Deprecation surfaces recounted, hidden-flag heading fixed, `mdm wipe` made per-platform, destructive ranking built on a rubric |
| Research 2 | NOT SOUND | Contracts became **ordered chains** rather than the terminal authorization call. `--config` reverted to `Not established`. Four register rows corrected, five negative-from-absence claims re-argued or marked `Not established` |
| Research 3 | NOT SOUND | **Chains became edition-dependent.** The five "composite" rows rebuilt as chains, `report` and `get fleets` corrected, Z33 added, the `preview` tail settled, the owning-chapter field created |
| Research 4 | NOT SOUND | **The common authenticated prefix factored out.** The edition split corrected to seventeen, four per-fleet subchains expanded, Z11 reattributed and Z26 conditioned, ownership recounted |
| Draft review 3 | **NOT READY**, six blocking plus one improvement | **All seven applied; one applied against the reviewer's arithmetic.** 1: `get mdm-command-results` split into two variants, because without `--host` Fleet filters the results silently and the authorization that looks fatal cannot fire on what it removed; the register goes to **34 rows** and the a.4 contradiction closes. 2: `run-script` moved to the first kind, and the subtotals corrected to **12 and 7**, not the reviewer's 11 and 8. 3, 4 and 7: **three under-claims published**. The two `generate` rows create and store server-side key material before writing anything locally and one of them talks to Fleet rather than Apple, and `debug cmdline` writes a file; plus two over-claims withdrawn, `upgrade-packs` zero not proving a file and `goquery` zero proving only that the session returned. 5: `get reports` split into list and named forms, so a named lookup no longer appears to need `user · read`. 6: Z25 narrowed to the two field forms it covers, with the mid-copy case named as the one that behaves differently. 7: the structured-output claim fixed rather than its counterexample. Cross-appendix pairing with a.4 now agrees on the seven device actions |
| Draft review 2 | **NOT READY**, ten findings | **All ten addressed; two applied against the reviewer's stated reason.** 1: `run-script` split into two chains, the polling form taking `host_script_result · read` per poll, and the Free chain corrected again because the licence check precedes the saved-script lookup. 2: the deletion guard narrowed to the run shapes that actually build it. 3: the four per-fleet subchains named gate by gate, and the top-level `label · write` corrected from fleet to global. 4: `delete -f` authorizes once per label on one of two exclusive branches, not twice. 5: `preview`'s host listing and enrolment made conditional on `--no-hosts`. 6: five register rows rewritten from file outcomes to discarded errors, `updates rotate` most of all. 7: the pre-command flag position and the error-sink mapping withdrawn to what Fleet's own source shows. 8: four exclusivity claims rebuilt; **two of them were not absence claims** and were restated as the positive boundaries they are. 9: both factual errors fixed. 10: subtotals reconciled to **11 and 8, not the reviewer's 10 and 9**, and both "Both kinds" justifications replaced, because the ones draft review 1 published are unreachable |
| Draft review 1 | **NOT READY**, nine findings | **Eight applied, one overruled.** 1: the Windows terminal `updates` behaviour got a full row, and the Windows behavioural count became 65. 2 and 4: `preview`'s row rebuilt to carry its sandbox chain, and the structural claim corrected to 18 without the prefix and 17 without any Fleet authorization. 3: "no permission at that service node" replaces "no permission in the command"; `run-script`'s licence gate moved to before the host-result authorization with the Free chain given inline; `gitops` made mixed; the two `--fleet` rows given both answers inline. 5: the `get mdm-commands` count corrected to agree with its rows, with the real finding restated as a partial result the server knows about and does not report; the "only silent row" claim replaced by five named rows. 6: the Windows row and `run-script`'s unbounded poll restored. 7: `goquery` moved to 4.2, giving 54 owned and 15 unowned. 8: every "narrower class" absolute rewritten to the established boundary. **9 overruled by the owner**, see the section above |

## The recurring defect: publishing an outcome the source does not establish

**Three rounds in a row, the correction has been to withdraw an outcome the source did not
establish.** Research round 2 marked five negative-from-absence claims unestablished. Draft review 1
withdrew the equivalence between the eighteen prefix-free rows and the rows reaching no
authorization, the claim that a displayed count disagreed with its displayed rows, and roughly
nineteen universals whose boundary had never been checked. Draft review 2 withdrew five register
rows that turned a discarded error into a definite bad file, two framework-dependent assignments,
and four exclusivity claims.

**The move is the same every time: the code shows a mechanism, and the draft publishes the
consequence that mechanism usually has.** An error is thrown away, so the file "is truncated". Two
sinks exist, so one of them "is where usage errors go". A search found nothing, so "nothing does
it". Each is one inferential step past the evidence, and each reads as more useful than the fact
underneath, which is exactly why it survives drafting and why a reader would act on it.

**The test that catches it, for whoever writes the next appendix.** Write the mechanism down first,
then ask what a reader would have to go and look at to confirm the consequence. If the answer is
"the artifact itself", the consequence is not established and the mechanism is the whole claim.
**"You will not be told" and "the file is bad" are different facts**, and only the first is in the
source. Add the consequence only where a second, separate piece of evidence carries it.

**A corollary that cost time this round.** Withdrawing is not always right either. Two of draft
review 2's absence claims turned out to be genuine positive boundaries once the call graph was
read: the update commands cannot enforce a licence because none of them reaches a Fleet server at
all, and `delete -f` cannot print the parser's deprecation notices because it hands the parser
nowhere to write them. **Check whether the boundary exists before softening the claim**, or the
appendix loses a fact it had earned.

**Draft review 3 gave the corollary its second half: neither is hedging always right.** That round
found three settled facts the appendix was *under*-claiming, all of them consequential and all of
them sitting in the checkout the whole time. `generate mdm-apple` and `generate mdm-ab` were
described as writing local files when each creates and stores key material on the Fleet server
first, and the first of the two sends its request to Fleet's own service rather than to Apple, which
the row named wrongly. `debug cmdline` was called read-only when its output option writes a local
file, and the wider truth was that eight of the twelve `debug` subcommands write a file whether you
ask or not. **So the discipline is symmetric.** The question is never "is this claim strong or
weak", it is "what exactly does the source settle", and the answer is as often more than the draft
says as less. An under-claim is the same defect wearing the opposite sign, and it is harder to catch
because it never reads as overreach.

**Part IX sets three review rounds for an appendix and they do three different jobs**: coverage,
a cell-by-cell evidence audit, and a fresh whole-appendix read against the register and the chapters.
None has been run against this draft. **The rounds above are research rounds, not draft reviews**,
and the distinction is the one CONTRIBUTING makes when it says verification is necessary and not
sufficient.

## 2026-09-02 fix: stale "setup has no owning chapter" claim (round3 B4)

The "Which commands have an owning chapter" table said `setup` had no owner, with prose explaining
it was briefly owned by a since-removed labs appendix. Verified against the book at HEAD: commit
`f091d69` (today) added a full `## Complete first-run setup` section to 2.2 — the `fleetctl setup`
command, `config set --address` pairing, password-prompt behavior, the `fleetctl get config`
verification step, and the "Fleet has already been setup" second-run failure. That commit fixed
2.3/2.4's cross-references to point at 2.2 but never updated this row. Fixed: assigned the row to
2.2, removed the labs-appendix prose, and updated the closing "outcome-level sibling" paragraph
since `setup` is no longer a named absence in a.7.

## 2026-09-02 fix: the round3 B4 fix above never reached the main table (round4 RB1)

The previous entry's fix apparently didn't survive, or was scoped to the audit table alone: the main
per-command index's Chapter cell for `setup` still read the literal string "No owning chapter" going
into this pass, and so did `preview`, `preview stop` and `preview reset` — while the "Which commands
have an owning chapter" audit table (added specifically to close this gap) correctly named `setup`
→ 2.2 and all three `preview` variants → 1.1, and the prose between the two tables flatly asserted
"Every row has an owning chapter." The file had been contradicting itself since at least round 3.

Fixed all four main-table cells to match the audit table exactly, rather than re-deriving the
chapters independently: `setup` → `[2.2](.../2.2-self-hosting-architecture-and-capacity.md#complete-first-run-setup)`,
`preview`/`preview stop`/`preview reset` → `[1.1](.../1.1-what-fleet-is.md#try-fleet-without-deploying-anything)`.
Confirmed zero remaining occurrences of "No owning chapter" anywhere in the file afterward.

Also checked the "70 vs 69" shared-prefix-contract arithmetic RB1 flagged as a MINOR sub-item.
Recounted directly: 69 behavioural rows in the macOS/Linux tree (regex-counted off the actual
tables, not read off the prose), of which the file says 51 carry the shared authorization prefix and
eighteen do not (the fourteen that call no Fleet at all, plus `setup`/`login`/`debug connection`,
plus `preview` itself) — 51 + 18 = 69, and 69 (the tree) + 1 (the Windows-only `updates` entry) = 70
matches the file's own "70 rows... 69 behaviours... one row that exists only on Windows" total. The
arithmetic is already internally consistent and matches the actual row count as of this pass; the
finding's literal "the file states 70" for the prefix-carrying total does not describe the file as it
stands now, so no change was made there beyond confirming it. `build/check-cap-ids.py` now recomputes
this from the tables on every run rather than trusting the prose, so if it drifts again the check
catches it instead of a fifth review round.

New machine check: `build/check-cap-ids.py` (extended today, [[a.1-notes]], [[a.5-notes]]) now also
asserts the main index and the audit table agree on every command's chapter, that no row's Chapter
cell is the literal "No owning chapter" string, and that the 51/18/69/70 shared-prefix arithmetic
above holds against the actual row count rather than just against itself on paper.
