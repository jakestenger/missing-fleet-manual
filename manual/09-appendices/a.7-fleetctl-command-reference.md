---
title: "fleetctl command index and behaviour"
chapter: "Appendices and indexes"
section: "A.7"
sidebar_position: 7
status: drafting
verified_against: Fleet 4.90.1
verified_on: 2026-08-29
verified_source: "drafted against fleet-v4.90.1 (dd0200f062). The inventory is the assembled root command tree at the tag rather than the output of any installed binary, and each permission chain was traced from the command to the authorization decisions this verification reached, then published as a floor rather than as a complete list. Citation ledger at research/section-notes/a.7-notes.md"
reviewed_by:
reviewed_on:
further_reading:
  - https://fleetdm.com/guides/fleetctl
  - https://fleetdm.com/docs/configuration/yaml-files
feature_requests:
  labels: [":product"]
  match: ["fleetctl", "CLI", "command line"]
  exclude: []
---

# fleetctl command index and behaviour

**Find the command in [the index](#the-command-index) below; its row says what it asks Fleet to do, what must allow it, and what its exit status proves.**

**A `fleetctl` command is a request to Fleet, and its contract is what it asks Fleet to do and what its result proves.** That is a different document from the one `--help` prints. Help tells you the flags a command accepts. It does not tell you that an invocation reaches four separate authorization decisions and that clearing the last one is not enough, that the answer changes between Fleet Free and Fleet Premium, or that a command exits zero after Fleet refused it.

Those three gaps are what this appendix carries, and each one is a place where an operator acts on a result that means less than it appears to.

## What this appendix carries

![Reference](../_assets/icons/reference.svg) Every public command and leaf subcommand in the 4.90.1 tree on macOS and Linux, and the one entry that differs on Windows, with what it asks Fleet to do, what it must be allowed to do, whether it destroys anything, whether it returns before or after Fleet acted, what its exit status proves, and the chapter that explains the workflow.

**Exact syntax is the installed client's job.** Run `fleetctl <command> --help` for the flag list of the client you actually have, which is the only listing guaranteed to match your binary. What is here instead is the part help does not carry: the resolution model, the per-command contract, the register of results that mislead, and the option families that widen an operation past what its name suggests.

**Three questions belong elsewhere.** Which role may perform an action, across all six roles at both scopes, is [a.4](a.4-roles-and-permissions-matrix.md). Which configuration authority wins when two disagree is [a.3](a.3-configuration-model-and-precedence.md). How to use the client in practice, meaning installation, version pinning, safe context use in CI, stream capture and worked examples, is [6.4](../06-automate-fleet/6.4-use-fleetctl.md). This appendix carries lookup contracts and links out; it reteaches none of the three.

## The command index

![Reference](../_assets/icons/reference.svg) 70 rows, grouped by top-level family: the 69 behaviours of the macOS and Linux tree, and the one row that exists only on Windows. The eight families that hold only subcommands on macOS and Linux appear as headings with no row of their own.

### How to read a row

**Access contract** is the ordered chain of authorization decisions the invocation reaches, written as `object · action` with the scope Fleet uses for that decision: `(global)` where the decision carries no fleet, `(fleet)` where it carries the object's fleet, and `(self)` where the object is your own record. **The order matters and the chain is not a union.** A role can hold the last decision in the chain and be refused by an earlier one, which is the single most useful thing this column carries, and it is why the column does not simply name the permission the command is "about".

Five phrases replace a chain where there is nothing to chain:

| Phrase | Means |
|---|---|
| `local` | The invocation asks nothing of Fleet. No permission is involved |
| `unauthenticated` | The request reaches Fleet and carries no credential |
| `global administrator` | Decided by the route's own middleware rather than by the authorization policy |
| `route-dependent` | Whatever the route you named requires |
| `no contract` | The command fails before authentication is reached |

**A chain is the suffix after the common prefix** stated below, for the 51 rows that carry it: a `version · read` that ends the command on any error, then an `app_config · read` that tolerates a permission refusal. **`preview` is the one row whose authorization sits outside that prefix**, and its own row carries the chain in full.

**Where a row's chain differs between Fleet Free and Fleet Premium, the row carries both**, because a reader who holds the last permission on Free and is refused has been told the wrong thing. The seventeen such rows are listed after the index.

**Effect** carries the destructive character, then one timing word: `sync` for a command that returns after Fleet did the thing, `accepted` for one that returns after Fleet accepted a request, `polls` where the client waits by asking repeatedly, `streaming`, `interactive`, or `local`.

**Result contract** is what a zero exit proves. A `Znn` reference points into the exit-zero register below.

**Chapter** is the section that explains the workflow. **`None` means this manual does not explain that command**, which is a finding about the manual rather than about Fleet, and the fifteen are listed together after the index.

### Top-level commands

| Command and purpose | Access contract | Effect | Result contract | Chapter |
|---|---|---|---|---|
| **`api <uri>`** Send a request you compose to any Fleet route. Prefixes the numbered version path unless your URI already carries a version | `route-dependent` | **As destructive as the route you name.** A delete verb against any endpoint, with no confirmation. `sync` | The status was in the 2xx range and the body was streamed out. On any other status **the body is discarded and only the number survives**, and that path exits 1. Z25 | [6.4](../06-automate-fleet/6.4-use-fleetctl.md) |
| **`apply -f <file>`** Push one spec file into Fleet, kind by kind | An ordered chain of up to thirteen steps, one per kind present in the file: `query · write` per report, `label · write` **(global, because this path sends no fleet with it)** per label, `pack · write` (global), `certificate_authority · write`, a bootstrap-package write, `script · write` (fleet), `app_config · write` (global), an Unassigned-profile batch, `enroll_secret · write` (global), `team · write` per fleet spec, then **the four per-fleet subchains, named rather than summarised**: `mdm_config_profile · write` (the fleet, or global for Unassigned) for profiles; `script · write` (the fleet) for scripts; `team · read` **(global)** then `installable_entity · write` (the fleet) for installers, with that global read **taken again on every poll for as long as the batch runs**; and the same `team · read` (global) then `installable_entity · write` (the fleet) for App Store apps. Then `policy · write`, `user · write`. **Free:** the fleet, installer and App Store nodes evaluate no permission at those nodes and return a licence error, and a label-scoped report is refused the same way | **Destructive.** Overwrites whole objects. `--force` pushes past the server's own validation. `sync` | **On an ordinary run**, every kind present in the file was accepted. With `--dry-run` it proves that three of the eight accepted kinds were checked and says nothing about the other five. Z19 | [6.4](../06-automate-fleet/6.4-use-fleetctl.md) |
| **`delete -f <file>`** Delete the reports, packs and labels named in a spec file | Three kinds in a fixed order: `query · write` on each loaded report, `pack · write` (global) per pack, then **one** `label · write` per label, taken on one of two mutually exclusive branches: a label that does not exist is decided globally, and a label that exists is decided on that label's own scope. Identical on both editions | **Destructive and quietly partial.** `sync` | The three handled kinds were deleted or did not exist. It says nothing about the other five kinds the same file may carry. Z20 | [6.4](../06-automate-fleet/6.4-use-fleetctl.md) |
| **`setup`** Create the first administrator on a server that has none | `unauthenticated` | Writes the local configuration file. `sync` | The server was un-set-up, is now set up, and your context file holds the new credential | None |
| **`login`** Exchange an email and password for a token | `unauthenticated` | Overwrites the email and token in the named context. `sync` | The credentials were accepted and the context holds a session token | [6.4](../06-automate-fleet/6.4-use-fleetctl.md) |
| **`logout`** End the session the context holds | `session · write` **(self)**, on your own session. A decision no authenticated caller can fail, and a real decision nonetheless | Clears the stored token. `sync` | Fleet invalidated the session **and** the local token was cleared | [6.4](../06-automate-fleet/6.4-use-fleetctl.md) |
| **`report`** (alias `query`, deprecated) Run a live report against selected hosts and stream results back | **Two variants.** Ad hoc, with `--query`: `label · read` (global, whether or not you passed `--labels`), `app_config · read` (global) twice, `query · run_new` (global), `targeted_query · run`. Saved, with `--report-name`: `query · read` (fleet) in place of `query · run_new`, and the rest as above. Identical on both editions | No writes. Puts load on every targeted host that checks in while the campaign is live, **which is not the set the targeted count names**: that count includes offline and non-responding hosts, and a host that never checks in never fetches the query. `streaming` | **Very little.** Zero is compatible with no host answering: it returns zero on timeout, and a per-host transport error is printed and skipped. Z9, Z10, Z26 | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) |
| **`convert -f <pack.json>`** Turn a legacy osquery pack file into report YAML | `local`. Declares `--config` and `--context` and reads neither | Writes the output file, truncating it. `local` | A file was parsed and YAML was emitted. Z28 | None |
| **`goquery`** Open an interactive query shell against Fleet | A chain that repeats **per shell command**. Per connect: `target · read` (global). Per query: `label · read` (global), `app_config · read` (global) twice, `query · run_new` (global) **always**, `targeted_query · run`. Identical on both editions | Interactive, and can run live queries. `interactive` | **The shell opened and the session returned, and nothing beyond that.** What happens inside never reaches the exit status: a host that will not resolve, a live query that errors, results that never arrive. In practice the only non-zero exit is a configuration or credential failure before the shell opens | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) |
| **`preview`** (alias `sandbox`) Run a local sandbox Fleet under Docker | **`local` against your Fleet, and authenticated against the sandbox it creates.** It never calls your context's server. Against the sandbox, at a fixed local address, it creates the first administrator unauthenticated, logs in as that account, and then takes a chain: `app_config · read` (global), a nested GitOps reconcile carrying the common prefix and the whole of `gitops`'s chain, `app_config · write` (global) twice, `enroll_secret · read` (global), and then, **only where you did not pass `--no-hosts`**, `host · list` (global) while it waits for the machine to appear. **The account is the one it just made**, so nothing in that chain can refuse you | **Rewrites your client configuration file**, and, unless you pass `--no-hosts`, enrols the machine it runs on into the sandbox. `local` | Docker came up, a sandbox was configured, and unless `--no-hosts` this machine enrolled into it. Z30 | None |
| **`vulnerability-data-stream --dir`** Download vulnerability feeds to a directory | `local`. Declares `--config` and `--context` and reads neither | Creates the directory and fills it. `local` | Nine download-or-refresh operations returned success. **Each transfers only where the local copy is out of date**, so zero does not prove that nine feeds were downloaded | None |
| **`package --type <type>`** Build a fleetd installer | `local`. Talks to the update server, never to Fleet, and declares no `--config` or `--context` at all | Writes a package. `--insecure` writes certificate-verification-off into the agent service configuration on every host installed from it. `local` | An installer file was produced | [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md) |
| **`prepare`** Present as a command, and does nothing | `no contract`. It fails before authentication is reached | None. `local` | **Never exits zero.** It returns an error telling you to use the `fleet` server binary | [7.3](../07-operate-fleet/7.3-upgrade-fleet-and-fleetd.md) |
| **`trigger --name <schedule>`** Ask Fleet to run a named scheduled job now | `cron_schedules · write` **(global)**, which [a.4](a.4-roles-and-permissions-matrix.md) records as global-administrator-only | Forces server-side background work to run now. `accepted`, and weaker than that | **The request was delivered.** Not that the schedule ran: Fleet discards the value that says whether it fired. Z7, Z8 | [8.6](../08-troubleshooting/8.6-server-state.md) |
| **`upgrade-packs -o <file>`** Write a migration file turning legacy packs into reports | The client refuses unless your account holds the global administrator role, then five decisions: `user · read` (self), `app_config · read` (global), `pack · read` (global) twice, `query · read` **(global)** | Read-only against Fleet. Writes a local file, **and only where there was something to write**. `sync` | The run reached the end of listing your packs. **It does not prove a file was written**: with no legacy packs to convert, Fleet prints an absence notice and returns before the output path is opened, so anything already sitting at that path is left as it was | None |
| **`run-script`** (alias `run_script`) Run a script on one host | **Two chains, because the waiting form keeps asking.** Both begin with `app_config · read` (global, a second and **less tolerant** read than the prefix), `host · selective_list` (global), `host · selective_read` (fleet), `script · read` (the fleet you named, on the `--script-name` form), `host_script_result · write` (the host's fleet). **The default form then takes `host_script_result · read` (the host's fleet) once per poll**, for as long as it waits; `--async` stops at the write and takes it never. **Premium** only where `--fleet` names a fleet other than Unassigned, and there **the server checks the licence before it looks the saved script up**, so on Free neither `script · read` nor `host_script_result · write` is reached and the refusal reads `Requires Fleet Premium license`. Client preflights can still refuse you before the server is reached | **Runs arbitrary code on a device as root or SYSTEM.** No confirmation. `polls` by default: the client asks Fleet for the result every five seconds, **with no polling deadline and no overall request timeout on the client**. Where the host runs the script, the agent's own execution limit ends the wait by producing an exit code; where no result is ever recorded, nothing ends it. `--async` returns an execution identifier instead of waiting. Refused when the host is not online, or when scripts are disabled | Fleet delivered the script and a result came back. **The script's own exit code is a line of output**, which `--quiet` removes. Z18 | [5.3](../05-manage-devices/5.3-run-and-manage-scripts.md) |
| **`gitops -f <file>...`** Reconcile Fleet against declared files | A fourteen-step chain: `app_config · read` (global) twice, `label · read` (Unassigned), `team · read`, a `label · read` per non-global file, the whole of `apply`'s chain per file plus custom host vitals and organisation logos, the Apple Business token count, `app_config · write` for the token re-patch, the fleet listing and deletion under `--delete-other-fleets`, `label · write` twice per removed label, and `certificate_authority · write`. **Free: mixed, and the distinction matters.** Most fleet-scoped nodes return a licence error without evaluating permission at that node. Two nodes do the opposite and authorize first: a label-scoped policy, and a configuration profile scoped by label. Fleet files themselves never get that far on Free, because the client skips them before the run reaches the server | **Destructive by design.** On Premium, and not on a dry run, `--delete-other-fleets` removes the fleets not named in the run. A global file with no Unassigned file applies an empty Unassigned configuration. `sync` | Reconciliation completed. With `--dry-run`, that validation passed. Z21 | [6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md) |
| **`generate-gitops`** (hidden) Export the running deployment as a GitOps tree, or print one configuration key | A 23-node chain behind a client-side administrator check **that does not hold for a fleet-scoped account**. Always `user · read` (self) then `app_config · read` (global); then, by scope and edition, fleet reads, enroll secrets, certificate authorities, the licence agreement, App Store tokens, per-fleet profiles, scripts, policies, reports and software, a `host · list` plus `software_inventory · read` **per software title**, and `label · read`. **Free:** the run stops at the certificate-authority or licence-agreement node | `--force` overwrites a non-empty directory. `--insecure` writes secrets in plain text. `sync` | **Very little.** It returns zero on a missing flag, on both flags, on a directory it will not overwrite, and on refusing you for not being authorised. Z1 to Z6, Z14, Z15, Z16 | [6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md) |
| **`new`** Render a starter GitOps repository into a directory | `local`. Declares no `--config` or `--context` | `--force` writes into an existing directory. `local` | A directory tree was written | [6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md) |

### `fleetctl get`, sixteen read subcommands

The family holds no behaviour of its own. Every subcommand is authenticated and carries the two logging flags.

| Command and purpose | Access contract | Effect | Result contract | Chapter |
|---|---|---|---|---|
| **`get reports [name]`** (aliases `report`, `r`; deprecated `queries`, `query`, `q`) List reports, or print one | **Two forms, and they do not share a chain.** Both take `team · read` (the fleet you named) **only where `--fleet` names a fleet**, then `query · read` on that fleet, or globally where you named none. **The list form adds two the named form never takes**: `user · read` (self), read solely to filter the list for observers, and a `query · read` **(global)** behind the inherited-reports note, which fires whenever you named a fleet and either it holds no reports of its own or you are taking the default table. A named lookup takes neither. **Free:** with `--fleet`, the fleet read returns a licence error without evaluating permission at that node, and **this is one of the few rows that then exits non-zero** | Read-only. `sync` | The list Fleet returned, filtered client-side for observers. Z11 | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) |
| **`get packs [name]`** (aliases `pack`, `p`) List legacy packs, or print one | `pack · read` (global). With `--with-reports`, a `query · read` (global) as well | Read-only. `sync` | The packs Fleet returned | None |
| **`get labels [name]`** (aliases `label`, `l`) List labels, or print one | `label · read` (the fleet you named). **Both editions take that decision.** On Free, `--fleet` naming a fleet is authorized first and refused for the licence afterwards, so a Free refusal here does mean your permission was checked | Read-only. `sync` | The labels Fleet returned, **minus any that failed to render**. Z24 | [1.3](../01-foundations/1.3-hosts-fleets-labels.md) |
| **`get hosts [identifier]`** (aliases `host`, `H`) List hosts, or print one | Without an identifier: `host · list` (global), plus a tolerated `app_config · read` when `--mdm` or `--mdm-pending` is passed. With an identifier: `host · selective_list` (global) then `host · selective_read` (the host's fleet) | Read-only. `sync` | The hosts Fleet returned | [4.1](../04-know-your-devices/4.1-understand-hosts-vitals-and-inventory.md) |
| **`get enroll_secret`** (aliases `enroll_secrets`, `enroll-secret`, `enroll-secrets`) Print the enroll secrets | `enroll_secret · read` (global) | Read-only, and **it prints live enroll secrets to standard output**. `sync` | The secrets Fleet holds | [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md) |
| **`get config`** Print the organisation settings | `app_config · read` (global). `--include-server-config` widens the answer to the server's own configuration | Read-only. `sync` | The settings Fleet returned, with the fields your role is allowed to see ([a.4](a.4-roles-and-permissions-matrix.md)) | [2.7](../02-administer-and-deploy-fleet/2.7-organization-and-server-settings.md) |
| **`get carves`** List file carves | `carve · read` (global) | Read-only, table output only. `sync` | The carves Fleet returned | None |
| **`get carve <id>`** Print a carve, or write it out | `carve · read` (global). With `--stdout` or `--outfile` the same decision is taken again for the metadata and **once per block** until the carve ends | Writes a file **without truncating it**, so a shorter carve leaves the previous file's tail behind. `sync` | Metadata was printed, or bytes were written. Z23 | None |
| **`get user_roles`** Print account roles | `user · read` (global) | Read-only. `sync` | **The default table prints one row per account carrying the global role only**, which is blank for a fleet-scoped account and never shows that account's per-fleet roles. `--json` and `--yaml` carry the global role and every fleet role, keyed by email | [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md) |
| **`get fleets`** (aliases `fleet`, `f`; deprecated `teams`, `team`, `t`) List fleets | **Free: the listing returns a licence error and the chain has no decisions at all at that point.** Premium table output: `team · read` (global). Premium `--json` or `--yaml` adds `software_inventory · read` (fleet) per fleet, a setup-experience read per fleet where the first returned a title, then `host · list` (fleet) and `software_inventory · read` (fleet) **per title per fleet**, and a maintained-app read per distinct Fleet-maintained package. **The structured form's chain grows with the number of software titles** | Read-only. `sync` | The fleets Fleet returned | [1.3](../01-foundations/1.3-hosts-fleets-labels.md) |
| **`get software`** (alias `s`) List software titles, or versions | `software_inventory · read` (the fleet you named). With `--versions`, the same decision twice, because the endpoint lists and then counts. **Both editions take that decision.** On Free, `--fleet` naming a fleet is authorized first and refused for the licence afterwards | Read-only. `sync` | The titles or versions Fleet returned | [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md) |
| **`get mdm-apple`** (alias `mdm_apple`) Print the Apple push certificate's status | `mdm_apple · read` (global) | Read-only, key-and-value table only. `sync` | The certificate's status, or an advisory that none is configured, which also exits zero | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) |
| **`get mdm-ab`** (alias `mdm_ab`) Print the Apple Business token's status | `mdm_apple · read` (global). **Free:** a licence error without evaluating permission | Read-only, key-and-value table only. `sync` | The token's status, or an advisory that none is configured | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) |
| **`get mdm-apple-bm`** (alias `mdm_apple_bm`) **Deprecated.** The former name of `get mdm-ab`, and a separately registered command with its own deprecation notice | As `get mdm-ab`, including the Free behaviour | Read-only. `sync` | As `get mdm-ab` | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) |
| **`get mdm-command-results --id`** Print the per-host results of one MDM command | **Two variants, and only one of them can refuse you.** With `--host`: a tolerated `app_config · read` (global), `host · list` (global), then `mdm_command · read` **on that host's fleet**, and **a refusal there ends the command**. Without `--host`: the same first two, then Fleet loads every result for the command, keeps only those whose host you are allowed to see, and takes `mdm_command · read` once per fleet **still standing after that filtering**, which is a decision your visibility has already satisfied. **Nothing in the second variant can refuse you on the results it removed** | Read-only, text blocks only. `sync` | **With `--host`**, the results for that host, or an advisory that none have arrived yet. **Without it, the results for the hosts you may see, and no sign that there were others.** Z34 | [8.8](../08-troubleshooting/8.8-apple-mdm-diagnostics.md) |
| **`get mdm-commands --host`** List recent MDM commands for a host | The same three decisions as the row above, but **a refusal is not fatal**: the commands you may not read are filtered out and the call still succeeds | Read-only, table output only, and a fixed page of the 20 most recent. `sync` | The commands Fleet returned **after removing any you were refused**. The count printed is the number of rows printed, so nothing in the output disagrees with anything. **Fleet knows the result is partial and says nothing about it.** Z33 | [8.8](../08-troubleshooting/8.8-apple-mdm-diagnostics.md) |

### `fleetctl config`, two local subcommands

Neither reaches Fleet. Both read and write the local configuration file only.

| Command and purpose | Access contract | Effect | Result contract | Chapter |
|---|---|---|---|---|
| **`config set`** Write settings into a context | `local` | Rewrites the whole file, unlocked. **Creates a missing context** rather than refusing. `local` | A local file was written, or, when you passed no setting flag, nothing was written and help was printed. Z29 | [6.4](../06-automate-fleet/6.4-use-fleetctl.md) |
| **`config get <key>`** Print one setting from a context | `local` | Read-only. `local` | The value, or, for an unknown key or the wrong number of arguments, help text and **exit zero**. Z12, Z32 | [6.4](../06-automate-fleet/6.4-use-fleetctl.md) |

### `fleetctl user`, four account subcommands

| Command and purpose | Access contract | Effect | Result contract | Chapter |
|---|---|---|---|---|
| **`user create`** Create an account | `user · write`, scoped by the fleets named in the request. **Permission is charged before the licence check**, so a Premium role on Free is refused for the licence after passing the permission decision | Writes an account. `--api-only` prints a permanent API token to standard output. The default role is global observer. `sync` | The account exists | [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md) |
| **`user delete --email`** Delete one account | Two decisions: `user · read` (global) to translate the address into an identifier, then `user · write` on the loaded account, **carrying that account's fleets** | **Irreversible. No confirmation.** `sync` | The account is gone | [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md) |
| **`user create-users --csv`** Create accounts in bulk | The `user create` chain, once per row of the file | Writes accounts, and **prints each generated password to standard output**. An account created for single sign-on is given no password and prints a single sign-on marker in its place. `sync` | Every row was created | [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md) |
| **`user delete-users --csv`** Delete accounts in bulk | The `user delete` two-decision chain, once per row | **Irreversible, bulk, no confirmation and no dry run.** It stops at the first failure part-way through, leaving a partial deletion. `sync` | The rows processed before any failure are gone | [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md) |

### `fleetctl debug`, twelve server diagnostics

**Eleven need a global administrator token**, and that is decided by the diagnostic routes' own middleware rather than by the authorization policy, so [a.4](a.4-roles-and-permissions-matrix.md)'s matrix does not reach them. `debug connection` is the exception and needs no credential at all. **Eight of the twelve write a file whether you ask for one or not**, into the working directory, under a generated name. `cmdline` writes one only with `--outfile`, `errors` writes one unless you pass `--stdout`, `connection` writes only a temporary file it then removes, and `migrations` is the one that writes nothing at all. Every file they write has owner-only permissions. Every one is owned by [8.5](../08-troubleshooting/8.5-fleetctl-debug.md).

| Command and purpose | Access contract | Effect | Result contract |
|---|---|---|---|
| **`debug profile`** Collect a 30 second CPU profile | `global administrator` | Writes a file. `sync` | A profile file was written |
| **`debug cmdline`** Print the server's own command line | `global administrator` | Read-only against Fleet, and **`--outfile` writes it to a local file** instead of printing it. **The highest-risk single item in the archive below**. `sync` | The server's arguments, printed or written |
| **`debug heap`** Collect a heap profile | `global administrator` | Writes a file. `sync` | A profile file was written |
| **`debug goroutine`** Collect a goroutine profile | `global administrator` | Writes a file, in binary form rather than the readable one. `sync` | A profile file was written |
| **`debug trace`** Collect a one second execution trace | `global administrator` | Writes a file. `sync` | A trace file was written |
| **`debug errors`** Print or save the errors Fleet recorded about itself | `global administrator` | **`--flush` deletes the stored errors after reading them**, before the output file is written. `--stdout` skips the sensitive-data banner. `sync` | The error store's contents were rendered |
| **`debug archive`** Collect thirteen diagnostics into one archive | `global administrator` | Writes an archive **without truncating an existing file**. `migrations` is not among the thirteen. `sync` | An archive was written. **It does not prove the archive is complete or readable**: a failed member is reported and skipped, and a failure closing the file is discarded. Z13, Z22 |
| **`debug connection [address]`** Check that a Fleet address is reachable and its certificate chain valid | `unauthenticated`. It builds no API client, and **rejects `--config` and `--context` outright when you give it an address** | Read-only. `local` | The address answered and the chain validated. With no certificate flag and no context authority it falls back to the client's embedded bundle and says so |
| **`debug migrations`** Report which schema migrations are outstanding | `global administrator` | Read-only. `sync` | The migration status Fleet returned |
| **`debug db-locks`** Print database lock contention | `global administrator`, and the database account needs the process privilege | Writes a file. `sync` | The lock report was written |
| **`debug db-innodb-status`** Print the storage engine's status | `global administrator` | Writes a file. `sync` | The status was written |
| **`debug db-process-list`** Print the database process list | `global administrator` | Writes a file **containing in-flight SQL text**. `sync` | The process list was written |

### `fleetctl preview`, two sandbox subcommands

| Command and purpose | Access contract | Effect | Result contract | Chapter |
|---|---|---|---|---|
| **`preview stop`** Stop the sandbox | `local` | Stops the containers and the sandbox agent. `local` | The stop was issued | None |
| **`preview reset`** Delete the sandbox | `local` | **Destroys the sandbox's data**, its containers and its agent directory. `local` | The sandbox was removed | None |

### `fleetctl updates`, five subcommands on macOS and Linux and one behaviour on Windows

**Present on macOS and Linux. On Windows the family is a single entry that fails on any invocation.** None of the five talks to Fleet; each operates on a local signing repository under `--path`, and each prompts for a passphrase. The parent command's description says the functionality is licensed under Fleet's enterprise licence. **Nothing in these commands could enforce it**: not one of the five contacts a Fleet server, holds a session, or reads an application configuration, so there is no channel by which a licence tier could even be learned. The sentence is a licensing statement rather than a gate.

| Command and purpose | Access contract | Effect | Result contract | Chapter |
|---|---|---|---|---|
| **`updates init`** Create a repository and its keys | `local` | Creates key material. `local` | A repository was created | None |
| **`updates roots`** Print the repository's root keys | `local` | Read-only. `local` | The roots were printed | None |
| **`updates add`** Publish an artifact for a platform and channel | `local` | **Publishes something your hosts will download and install.** The copy it makes is written without truncating an existing file, and it is copied before it is signed. Whether a bad copy is caught at the signing step is decided outside Fleet's own source. `local` | An artifact was added to the repository. Z31 | None |
| **`updates timestamp`** Re-sign the repository's timestamp | `local` | Re-signs. `local` | The timestamp was refreshed | None |
| **`updates rotate <role>`** Replace the signing key for a role | `local` | **Retires a signing key.** `local` | The repository was committed. **It does not prove the post-rotation cleanup finished**: a failure there prints one warning line that does not say which removal failed or what it left behind. Z27 | None |
| **`updates` on Windows** The whole family, reduced to one entry that refuses | `no contract`. It builds no client, declares no flags, and fails before authentication is reached | None. It reaches neither Fleet nor a local repository, and destroys nothing. `local` | **Never exits zero.** It returns the message telling you to use a Linux environment, which is also the entry's own description text | None |

### `fleetctl hosts`, one subcommand

| Command and purpose | Access contract | Effect | Result contract | Chapter |
|---|---|---|---|---|
| **`hosts transfer --fleet <name>`** Move hosts into a fleet | **Variant-dependent, four decisions either way.** With `--hosts`: `host · read` (global) once per host, `team · read` (global) for the destination, `host · transfer_host` on the destination fleet, then `host · transfer_host` on **each distinct source fleet**. With `--label`: `label · read` (global) in place of the per-host reads, and the same three that follow. `--status` or `--search_query` without `--label` skips the first decision entirely. Identical on both editions | **Destructive in the sense that matters: it moves configuration scope.** The filter form moves whatever the filter selects, server-side, **within the hosts your own role can see**, and **the client never counts or prints how many hosts it is about to move**. `--fleet ''` means Unassigned. `sync` | Fleet accepted the transfer. **No count is available in the protocol**, so the number moved is not knowable from the command | [1.3](../01-foundations/1.3-hosts-fleets-labels.md) |

### `fleetctl generate`, three credential-request subcommands

**Each is a global write followed by a read**, which is the clearest case in the client for reading a chain in order rather than naming its last decision: a contract naming only the last would report these as a settings read when they require a global Apple MDM write. **And the write is not only a permission label.** Two of the three create key material on the Fleet server and store it there before anything reaches your disk, so a command named `generate` changes server state on its first successful run.

| Command and purpose | Access contract | Effect | Result contract | Chapter |
|---|---|---|---|---|
| **`generate mdm-apple`** (alias `mdm_apple`) Request the signing request for an Apple push certificate | `mdm_apple · write` (global) then `app_config · read` (global). The policy grants that write to the global administrator role and to nothing else | **Server state first, file second.** On the first run Fleet creates a certificate authority certificate and key and a push private key, and **stores all three on the server, encrypted**; later runs reuse them. It then builds a fresh signing request every time and **sends it to Fleet's own service rather than to Apple**. Writes the request file with owner-only permissions. `sync` | Fleet's service returned a signed request and the file was written. **Apple has not seen anything**: uploading the file is your next step. **A failure after this point does not undo the stored keys**, and the file is written before the settings are read, so a late failure leaves both behind | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) |
| **`generate mdm-ab`** (alias `mdm_ab`) Request the public key for an Apple Business token | `mdm_apple · write` (global) then `app_config · read` (global), the same global-administrator-only write | **Server state first, file second.** On the first run Fleet creates an Apple Business keypair and stores both halves on the server; **the private half never leaves Fleet**. Later runs hand back the stored pair, which is the renewal path. Only then is the public half written locally, with owner-only permissions. `sync` | The keypair exists on the server and the public key file was written. **The keypair persists whether or not the rest of the command succeeded** | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) |
| **`generate mdm-apple-bm`** (alias `mdm_apple_bm`) **Deprecated.** The former name of `generate mdm-ab` | Identical to `generate mdm-ab` | As above. `sync` | As above | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) |

### `fleetctl mdm`, five device-action subcommands

**This is the most destructive family in the client, and the family where the edition split bites hardest.** Four of the five share a client preflight that resolves the host and turns a permission refusal into a readable message; that preflight contributes the first two decisions of each chain, **and it contributes them on both editions**, which is why the Free answer below is about a service node rather than about the command.

**The third decision is the one that catches people.** On Premium, `lock`, `unlock` and `wipe` require a **broad, global** `host · list` in addition to the selective host decisions before them, and `clear-passcode` requires a broad, global `host · read`. A role granted the selective host actions instead of the broad ones clears the first two decisions, holds `mdm_command · write` for the host's fleet, and is still refused.

| Command and purpose | Access contract | Effect | Result contract | Chapter |
|---|---|---|---|---|
| **`mdm run-command --hosts --payload`** Send a raw MDM payload to one or more hosts | Five decisions: a tolerated `app_config · read` (global), `host · selective_list` (global) and `host · selective_read` (fleet) once per identifier, `host · selective_list` (global) again inside the send, then `mdm_command · write` **once per fleet the target set touches**. Identical on both editions, with Free refusing the erase, lock and clear-passcode Apple request types and the premium Windows form | **Whatever the payload does**, within the shape Fleet enforces. Fleet parses the payload on both platforms, rewrites its identifier, and refuses a malformed one, **but it does not check that the request type names a real command**. Refuses a target set mixing macOS and Windows hosts. `accepted` | Fleet stored the command for every targeted host. **A partial push failure is not reported to you and no activity is recorded for the hosts it failed for.** Z17 | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) |
| **`mdm lock --host`** Lock a device | `host · selective_list` (global), `host · selective_read` (fleet), `host · list` (global, broad), `mdm_command · write` (the host's fleet). **Free: the first two are taken exactly as on Premium**, because the client resolves the host either way; **the service node that would lock evaluates no permission at that node** and returns a licence error, so the last two are never reached and a Free refusal tells you nothing about whether you hold them | **Destructive.** Recovery needs the PIN Fleet issues, or the end user's own PIN on Android. `accepted` | Fleet accepted the lock. The device acts when it next checks in | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) |
| **`mdm unlock --host`** Unlock a device | The same four decisions. **Free: the same first two are taken, and no permission is evaluated at the unlock node; licence error** | Reverses a lock, and prints the six-digit PIN for a Mac. `accepted` | Fleet accepted the unlock | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) |
| **`mdm wipe --host`** Wipe a device | The same four decisions **on both editions**, and the licence check comes after them: on Free the command works for a company-owned Android device and returns a licence error for every other platform | **Irreversible, and platform-specific.** It asks Fleet to run the wipe action defined for that host's platform, which is an Apple erase command, a Windows remote-wipe command, an Android enterprise wipe, or, on Linux, **a script run by fleetd**, which requires the agent to have been deployed with scripts enabled. What is left on the disk is the platform's answer rather than Fleet's. One required flag, **no prompt, no dry run**. `accepted` | Fleet accepted the wipe | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) |
| **`mdm clear-passcode --host`** (alias `clear_passcode`) Clear a device or work-profile passcode | `host · selective_list` (global), `host · selective_read` (fleet), **`host · read`** (global, broad, and not `list` as the three above), `mdm_command · write` (the host's fleet). **Free: the same first two are taken, and no permission is evaluated at the clear-passcode node; licence error.** iPhone, iPad and Android only | Clears the passcode. `accepted` | Fleet accepted the request. **Fleet deliberately records no pending action on the host**, so the host record shows nothing and completion appears only as an activity | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) |

### The seventeen rows whose access contract differs between Free and Premium

**A permission chain is a property of a command on an edition**, and treating it as a property of the command alone produces a confidently wrong answer for a quarter of the index. The seventeen below are a floor rather than a closed set: the pattern behind the first kind is uniform across Fleet's community fleet-management code, so any further path reaching one of those inherits the split.

**Two kinds, and they behave differently:**

**The community build evaluates no permission at that service node and returns a licence error.** Twelve rows. **The Free chain takes no decision at that node, rather than taking a smaller one**, which is a different kind of answer. **It is a claim about the node and not about the whole command**: `mdm lock`, `unlock` and `clear-passcode` resolve the host first and take two host decisions on both editions, and only the final node skips. `run-script` against a named fleet is the same shape from the other direction: the client's preflights run on both editions, and the server skips authorization and refuses for the licence **before** it reaches either of the two decisions that row lists. What a refusal at that node tells the operator about the permissions behind it is nothing, and moving to Premium can then refuse them again on grounds they have not yet seen.

**The decisions are the same on both editions and a licence check is added.** Seven rows. **Two rows appear in both kinds**, `apply -f` and `gitops`, because each carries nodes of both shapes, which is how twelve and seven cover seventeen rows rather than nineteen. **Where that check sits is the useful part**, and it differs: `mdm wipe` takes every permission decision and then checks the licence, while `mdm run-command` authorizes the whole target set up front and refuses only where the payload names a request type Free does not carry. `user create` charges the permission before the licence refusal, so a Premium-only role requested on Free is refused for the licence rather than for permission. `get labels --fleet` and `get software --fleet` are the same shape as `user create`: authorized first, refused for the licence afterwards.

| Row | Kind | What differs |
|---|---|---|
| `mdm lock` | No decision at that node on Free | The two host decisions are taken on both editions. Premium goes on to a broad global `host · list` and `mdm_command · write` |
| `mdm unlock` | No decision at that node on Free | As above |
| `mdm clear-passcode` | No decision at that node on Free | The two host decisions are taken on both editions. Premium goes on to a broad global `host · read` and `mdm_command · write` |
| `get fleets` | No decision at that node on Free | The whole structured continuation is unreachable on Free |
| `get mdm-ab` | No decision at that node on Free | The Apple Business token read is the whole chain, so Free reaches none of it |
| `get mdm-apple-bm` | No decision at that node on Free | A separately registered command, so a separate row |
| `get reports --fleet <id>` | No decision at that node on Free | The fleet read is the split; the report reads that follow are not |
| `gitops` | **Both kinds** | No decision at the node for fleet listing, fleet specs, fleet deletion, Apple Business tokens, installers and setup experience. **A label-scoped policy and a label-scoped configuration profile take the other shape**, reached through the same chain `apply -f` uses: both authorize before they refuse for the licence |
| `generate-gitops` | No decision at those nodes on Free | Fleet reads, certificate authorities, the licence agreement, App Store tokens, maintained apps, setup experience, icons |
| `apply -f` and `gitops` fleet software and App Store apps | No decision at those nodes on Free | Premium takes a fleet read then an `installable_entity · write` for each |
| `run-script` | No decision at that node on Free | Only where `--fleet` names a fleet other than Unassigned. The server skips authorization and returns the licence error before it looks the saved script up, so neither `script · read` nor `host_script_result · write` is evaluated. The client's own preflights run on both editions |
| `apply -f` | **Both kinds** | The fleet kind and a label-scoped report take the first shape. **A label-scoped policy and a label-scoped configuration profile take the second**: both authorize before they refuse for the licence |
| `mdm wipe` | Licence check added | Same decisions on both. **Free works for a company-owned Android device only** |
| `mdm run-command` | Licence check added | Same decisions. Free refuses the erase, lock and clear-passcode Apple request types, and the premium Windows form |
| `get labels --fleet <id>` | Licence check added | The label read is authorized on both editions, and Free refuses for the licence after it |
| `get software --fleet <id>` | Licence check added | The software read is authorized on both editions, and Free refuses for the licence after it |
| `user create`, and `user create-users` per row | Licence check added | For a Premium role, or an API-only account carrying fleets or endpoint restrictions |

**Six rows were checked for a split and do not have one**, recorded so the question is not reopened: `hosts transfer`, `trigger`, `generate mdm-ab`, `delete -f`, `report` and `goquery`. On Free, `hosts transfer` can still fail, and it fails because the destination fleet does not exist rather than because a permission decision refused it.

### Fifteen commands this manual does not explain

**Fifteen of the 69 macOS and Linux rows have no owning chapter, and this appendix names them rather than inventing a link.** A chapter owns a row when it explains the workflow the command serves, not when it mentions the command in passing, and equally not when it explains the workflow without naming the command. Six groups, and each is a gap in the book rather than in Fleet:

| Group | Commands | Why nothing owns it |
|---|---|---|
| **Legacy osquery packs** | `convert`, `upgrade-packs`, `get packs` | Packs appear in the manual as an object type in passing and are defined only in the glossary. The reports chapter does not cover them |
| **Running your own update repository** | `updates init`, `updates roots`, `updates add`, `updates timestamp`, `updates rotate` | [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md) teaches consuming Fleet's update repository. Creating, signing, key-rotating and re-timestamping your own is not covered anywhere, and [6.4](../06-automate-fleet/6.4-use-fleetctl.md) says so plainly |
| **The local evaluation sandbox** | `preview`, `preview stop`, `preview reset` | The sandbox is named twice in the manual, once as a hazard to pin and once in a list of surfaces. Nothing teaches starting, stopping or resetting it |
| **Retrieving file carves** | `get carve`, `get carves` | Carving is sized, bucketed and limit-tabled across several chapters, and no chapter initiates a carve or reads one back |
| **First-run setup** | `setup` | `setup` appears nowhere in the manual, and no chapter covers standing a server up or creating its first administrator |
| **Supplying vulnerability data yourself** | `vulnerability-data-stream` | The command downloads nine datasets. [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md) carries one line saying that something else places the data where Fleet reads it, which is a mention rather than a workflow, and no chapter teaches running Fleet without that egress |

**Read those rows as complete contracts and incomplete guidance.** The access, effect and result columns are verified for all fifteen exactly as they are for the other 54; what is missing is a chapter explaining when you would want the command and what to do around it. **The Windows-only `updates` row has no owning chapter either**, for the same reason as the family it replaces, and it is outside the fifteen because the fifteen are counted over the macOS and Linux index.

**The outcome-level sibling of this register is [a.1](a.1-capability-index.md#where-this-index-ends)'s closing section, "Where this index ends".** Five of the six groups above appear there as outcomes: the update repository, file carving and vulnerability data as capability rows, packs and the sandbox in its no-row list. First-run `setup` is this register's alone. The two registers describe overlapping gaps at different grain, so quote either count on its own and never their sum.

## Which server and which credential an invocation selects

![Reference](../_assets/icons/reference.svg) One question decides where a destructive command lands, and it is answered before any flag you typed is considered.

**The client reads a configuration file holding named contexts.** Each context carries a server address, an account email, a token, and the transport settings for reaching that server: a certificate authority, a URL prefix, whether to skip verification, and any custom headers. Switching context switches all of it at once. The file is `~/.fleet/config` unless `--config` names another, and the context is `default` unless `--context` names another.

**The file is created with owner-only permissions inside an owner-only directory**, and on macOS and Linux the client refuses to open an existing file whose group or other permissions are wider than that. On Windows there is no such check.

**Writes to it are whole-file and unlocked**, so two `fleetctl` processes changing configuration at the same time lose one of the two changes and both exit zero. [6.4](../06-automate-fleet/6.4-use-fleetctl.md) covers giving each automation job its own file, which removes the class of problem rather than narrowing it.

Five situations produce answers worth knowing in advance:

| Situation | What happens |
|---|---|
| No configuration file at all | One is created, and the command then fails, asking you to set an address |
| `--context` names a context that does not exist | A hard error, for every command except `config get` and `config set` |
| The same, under `config get` or `config set` | **The context is created**, with a printed note. Fleet does not know `prod-typo` is a typo: it creates a perfectly usable context with exactly that name, and a later command passing the same typo selects exactly it. The `prod` context you meant is untouched, still holding whatever it held before, or does not exist and fails outright |
| An address is set and the token is empty | An instruction to log in, on standard error, or the single sign-on instructions where the server reports it enabled |
| **Windows, with no certificate authority and no skip-verify setting** | A hard refusal. A genuine platform difference in the client, not a convention |

### The two round-trips an authenticated command makes before its own work

**Nearly every authenticated command asks Fleet two questions before it asks the one you typed.** It reads Fleet's version, and it reads the application configuration. Both are authenticated requests, both can be refused, and the two refusals differ:

| | What it asks | What a refusal does |
|---|---|---|
| **First** | `version · read` (global) | **Ends the command.** Any error, a permission error included, returns before your work begins. This call doubles as the check that your token is still valid |
| **Second** | `app_config · read` (global) | **Tolerated when it is a permission refusal**, fatal otherwise. The tolerance is what lets a low-privilege automation identity, such as one holding the GitOps role, use the client at all |

**The 51 rows that carry the prefix state only the suffix after those two.** It is stated once here rather than in 51 rows, and a row that shows an application-configuration read is showing a second, command-specific one. The other eighteen rows are the subject of the paragraph below, and one of them has authorization of its own that this prefix does not describe.

**Eighteen of the 69 rows do not carry the prefix, and seventeen of those eighteen reach no Fleet authorization at all.** The two counts differ by one row and the row is `preview`. Fourteen make no call to any Fleet: `convert`, `package`, `new`, `vulnerability-data-stream`, `prepare`, `preview stop`, `preview reset`, both `config` subcommands and the five update-repository subcommands. Three reach Fleet without a credential: `setup`, `login` and `debug connection`.

**`preview` is the one that differs, and it differs in both directions.** It never calls your Fleet, and it is not free of Fleet authorization: inside the sandbox it starts, it creates the first administrator, logs in as that account, then reads and writes the application configuration, reads the enroll secret, lists hosts, and runs a nested GitOps reconcile that carries this same prefix. Those are the sandbox's authorization decisions rather than your Fleet's, and the account taking them is the one `preview` just created, so none of them can refuse you. **The count is therefore eighteen rows without the prefix and seventeen with no Fleet authorization anywhere**, and the two are not the same set.

### Where a value comes from when you did not pass a flag

**There are no global options.** The root declares no flags of its own, so there is nothing to set before a command name and nothing that overrides what a command declares for itself. **Whether a command's own flag is accepted in that position is the command-line framework's decision rather than Fleet's, and is not established at this release**, which is the same boundary as the placement question after a subcommand further down. No test in Fleet's tree puts a flag before a command name. Four flags are declared command by command and behave as though they were global:

| Flag | Environment variable | Default |
|---|---|---|
| `--config` | `CONFIG` | `~/.fleet/config` |
| `--context` | `CONTEXT` | `default` |
| `--debug` | `DEBUG` | off |
| `--enable-log-topics`, `--disable-log-topics` | `FLEET_ENABLE_LOG_TOPICS`, `FLEET_DISABLE_LOG_TOPICS` | unset |

**`--debug` dumps the client's own request bodies to standard error**, which on a `login`, a `user create`, an `apply` or a `gitops` run puts a credential into the terminal scrollback and into any captured CI log. `config set` is not in that list, because it declares no `--debug` and makes no request.

**Not every command declares all four.** `package` declares none of `--config`, `--context` or `--debug`, and carries an unrelated `--debug` of its own that turns on agent debug logging in the package it builds. `new` declares none of them. The five `mdm` subcommands and the three `generate` subcommands declare `--context` and `--debug` but not `--config`. So a claim that a flag is available on every subcommand is true of the `debug` family and untrue of the client.

**Most of the client's environment variables are unprefixed, which is the sharpest option-resolution hazard here.** Fleet's server variables all begin `FLEET_`. The client's flag variables mostly do not, and the set includes `TOKEN`, `PASSWORD`, `INSECURE`, `FORCE`, `DRY_RUN`, `DEBUG`, `QUIET`, `TIMEOUT`, `NAME`, `DIR`, `HOSTS`, `QUERY`, `EMAIL`, `FILENAME` and `DELETE_OTHER_FLEETS`. Several of those are names a CI runner or a shell profile sets for unrelated reasons. An exported `DEBUG=1` makes every `fleetctl` call **that declares the standard debug flag** dump request bodies, which is most of them and not all: `new`, `convert`, the two `config` subcommands, `prepare` and the update-repository commands do not declare it and ignore the variable, and `package`'s `--debug` is a different flag that reads no environment variable at all. An exported `INSECURE=1` makes `fleetctl config set` disable certificate verification for the context it writes. `fleetctl package` prefixes its own variables `FLEETCTL_`, which is a good indication that the unprefixed set is inherited rather than intended.

**In automation, pass the flags explicitly** and give each job its own configuration file.

### What is not established about flag placement

**Whether `--config` is accepted after a subcommand that does not declare it is not established at this release**, and the index above is laid out so as to imply neither answer.

What Fleet's source settles is the shape of the question. For the five `mdm` subcommands and the three `generate` subcommands, the parent command declares `--config`, the subcommand does not, and the code that builds the API client reads a `--config` value regardless. Whether the value is readable at that position is decided by the third-party command-line framework Fleet is built on, which is not part of Fleet's own source and could not be read at the tag. No test in Fleet's tree places the flag after any of those eight subcommands, so nothing in the release settles it either.

**The form Fleet's own tests use is the safe one**: put `--config` where the command that declares it sits, or use the `CONFIG` environment variable, which is read the same way whatever the placement.

## What a result and an exit status prove

![Reference](../_assets/icons/reference.svg) This is the legend the index is read through. **A zero exit proves that the client reached the end of its work without returning an error.** It does not prove that Fleet did the thing, that the thing reached a device, that your file was fully validated, that you were authorised, or that the flags you passed were understood.

**The client's own exits are zero and one.** No command distinguishes "not found" from "forbidden" from "the network is down" in its status, so a pipeline branching on the exit code is branching on one bit. Signals, panics and a launcher's own failure produce other process statuses, so this is a statement about what the program returns rather than about everything a shell can observe.

**Two error sinks exist and they write to different streams.** One prints to standard error and the other to standard output. **Which class of failure reaches which sink is not established, and this appendix assigns neither**: that dispatch belongs to the command-line framework rather than to Fleet, which also decides whether a given failure reaches one sink, the other, or both. The consequence for a pipeline holds either way. **Capture both streams**, because the text you need is not reliably on one of them.

**The displayed error text has the HTTP status stripped out of it.** Where a request failed with a status code, the client removes the leading "received status N" portion before printing, so the number is not in the string a script would search for.

### Four things exit zero can mean

Read a row's result contract as one of these four. The fourth is why this appendix has a register.

**The request completed and Fleet returned success.** The ordinary case, and what most rows carry.

**Fleet accepted a request and a device has not acted on it.** The five `mdm` subcommands and `run-script --async`. All five `mdm` subcommands say so in their output, in the form "when it comes online", and the index marks them `accepted`. A command that is accepted rather than done is not a defect and is not in the register: it is a property of the operation, and you confirm it by reading the result from Fleet afterwards.

**The client's work completed and the outcome is in the text rather than in the status.** `run-script` waiting for its result exits zero whatever the script returned, and the script's own exit code is a line of output that `--quiet` removes. `report` exits zero when it stops on a timeout.

**The advertised outcome was refused, incomplete or partial, and the status does not say so.** That is the register below. **Most of those cases print something**, a warning line or an advisory, so the shared property is not silence: it is that the exit status is zero either way, and nothing a script can branch on records the refusal.

### Output modes, and where structured output is absent

There is no single output-format flag. Five renderers exist and they are attached command by command:

| Mode | Where you get it |
|---|---|
| Table | The default for `get reports`, `packs`, `labels`, `hosts`, `user_roles`, `fleets` and `software`, and the sole mode for `get carves`, `get mdm-commands`, `get mdm-apple`, `get mdm-ab` and `get mdm-apple-bm` |
| `--yaml` | Nine `get` subcommands. `get carve` prints YAML whether you ask for it or not |
| `--json` | The same nine |
| JSON lines | `fleetctl report`, by default: one object per host, carrying the host, its rows and any error |
| Live table | `fleetctl report --pretty` |

**`--remove-deprecated-keys` strips the older key spellings from JSON and YAML output.** Without it the output carries both the current and the deprecated name for the same field, which matters when the output is going back into `apply`.

**A large part of the client has no structured output on the terminal.** Every `mdm` subcommand, `run-script`, `trigger`, `gitops`, `apply`, `delete`, `upgrade-packs`, `get mdm-command-results`, `package`, `new`, the update-repository subcommands, and every `debug` subcommand **but one**, print prose to your screen. **The exception is `debug errors --stdout`**, which streams Fleet's error store to the terminal as JSON. Anything parsing that is parsing sentences, and sentences change between releases without a deprecation.

**Several of them do write structured output, to a file rather than to your terminal**, and that is the distinction the sentence above hides. `upgrade-packs` requires an output path and writes report YAML into it. `new` writes a whole YAML repository. Four `debug` subcommands write JSON: `errors`, which `--stdout` sends to the terminal instead, as above, and the three database diagnostics, which `debug archive` then bundles alongside the profiling files. `get mdm-command-results` is the opposite case: it has no structured mode at all, and the payload and result cells inside its text blocks are XML.

**Four commands declare a `--yaml` flag that nothing in them reads**: `hosts transfer`, `goquery`, `user create` and `user delete`. The declaration carries no destination, no environment variable and no action of its own, so the only route to the value is the invocation's own context, and none of the four takes it: the query shell is handed a client and never sees the context at all. What the framework does with a declared flag nobody reads is a question about the framework.

**Stream discipline is inconsistent.** Some commands print through the client's own writer and others print straight to standard output, while progress and warning lines from the API client go to standard error. That is the second reason to capture both streams.

## The exit-zero register

![Troubleshooting](../_assets/icons/troubleshooting.svg) **Thirty-four invocations where Fleet or the client detected an adverse, incomplete or refused outcome and the command still exited zero.** This is the section to read before you run `fleetctl` unattended, because every row is a case where a pipeline that branches on the exit code branches the wrong way.

**The class is stated before the rows, because a register with no inclusion rule grows without bound.** A row qualifies when the advertised outcome was materially refused, incomplete or partial, **the code detected or knew it**, and the invocation returned success anyway. Three things are deliberately outside the class:

- **Expected absence.** "No users found" is a correct answer to a question about what exists, and exit zero is right.
- **Asynchronous acceptance.** A command that returns when Fleet accepted a request rather than when a device acted. That is a real property, it belongs in the index's result column, and it is there.
- **Results that have not arrived yet.** The same shape at a different layer.

**Every row below exits zero**, so there is no status column. **Z8 is the one row where a command prints its success line for work that did not happen**, and it is the one to read first. **Five rows print nothing at all**: Z20, Z23, Z24, Z28 and Z31, where the only evidence that anything went wrong is the object the command was supposed to produce.

| ID | Invocation | What was detected | What you see | What to check instead |
|---|---|---|---|---|
| **Z1** | `generate-gitops` with neither `--dir` nor `--key` | Refused. Nothing was generated | A line saying one of the two is required | Whether the output directory exists at all |
| **Z2** | `generate-gitops` with both | Refused. Nothing was generated | A line saying only one may be given | As above |
| **Z3** | `generate-gitops` run by a global role that is not administrator | **Authorization refused** | "You are not authorized to run this command" | The directory is empty. Re-run as a global administrator. **A fleet-scoped account is not caught by this check at all** |
| **Z4** | `generate-gitops` into a directory that is not empty, without `--force` | Refused. Nothing was written | A line naming the directory | Whether the directory's contents are the ones you expected to be replaced |
| **Z5** | `generate-gitops --fleet` naming a fleet that does not exist | The lookup failed. Nothing was generated | "Fleet not found" | The fleet name, against `fleetctl get fleets` |
| **Z6** | `generate-gitops --key` naming a key that does not exist | The lookup failed | "Key not found" | The key path, against `fleetctl get config` |
| **Z7** | `trigger` for a schedule that is unknown, or already running | **The run did not happen** | A `[!]` line and the reason | The schedule's recorded run history in Fleet ([8.6](../08-troubleshooting/8.6-server-state.md)) |
| **Z8** | `trigger` when the server could not publish the signal | **The run did not happen and the success line prints anyway** | "Sent request to trigger" | The schedule's recorded run history. **Fleet makes no distinction between publishing the signal and finding the channel unavailable**, and the value that would say which is discarded before the response is built |
| **Z9** | `report` that reaches its timeout | Incomplete results | "Stopped by timeout", and **with `--quiet`, nothing at all** | The responded-against-online counts, which `--quiet` also removes. Re-run with a longer `--timeout` |
| **Z10** | `report` that cannot render a result it received | **That host's result is lost** and the run continues | An error line per failed result, on standard error | Whether the host count you received matches the host count you targeted |
| **Z11** | `get reports --fleet <identifier that does not exist>` | Nothing was listed and no report was matched | "Team not found." on standard output, still using the older word for a fleet | The fleet identifier. The command takes a numeric identifier, not a name |
| **Z12** | `config get <unknown key>` | Nothing was retrieved | The subcommand's help text | The key spelling. **A script capturing this gets an empty value and a zero status** |
| **Z13** | `debug archive` when some or all members fail | **An archive missing the members that failed**, possibly all of them | A failure line per member, then the archive path | The archive's contents against the thirteen expected members, before attaching it to a support case |
| **Z14** | `generate-gitops` with a profile whose platform it does not recognise | **The profile is dropped from the export** | A warning naming the profile | The exported tree against the profiles Fleet holds |
| **Z15** | `generate-gitops` with a software title that has neither a package nor an App Store app | **The title is dropped from the export** | An error line naming the title | As above, for software |
| **Z16** | `generate-gitops` when the settings advertise a Fleet-hosted organisation logo and no logo is stored | The logo is not exported and the file keeps a URL that will not resolve for anyone else | A warning about the logo | The exported settings file's logo URL |
| **Z17** | `mdm run-command --hosts a,b,c` when the wake-up push fails for some of the targets | **The push failed for those hosts.** The command itself was stored for every targeted host before the push, so they will collect it on their next check-in | "Hosts will run the command the next time they check into Fleet", which is accurate | The activity feed, which **records nothing for the hosts the push failed for**, so it understates what is queued. Confirm through the command's results rather than the activity |
| **Z18** | `run-script` where the script fails, times out, or is refused on the host | **The script did not succeed** | The exit code as a line of output, and **with `--quiet` only the raw output, with no exit code at all** | The exit-code line, or the script's recorded result in Fleet. Do not run `--quiet` in automation that needs to know |
| **Z19** | `apply --dry-run` on a file holding reports, labels, packs, policies or user roles | **Five of the eight accepted kinds were not validated at all** | A `[!] ignoring` line per skipped kind | The five kinds, by applying to a non-production Fleet. A pull-request gate built on this validates syntax and rather less content than it appears to |
| **Z20** | `delete -f` on a file holding any kind other than report, pack or label | **Nothing was deleted for those kinds** | **Nothing.** No message, no warning | Whether the objects still exist. Four other rows are silent in the same way: Z23, Z24, Z28 and Z31 |
| **Z21** | `gitops` with fleet files against a **Free** server | **Every fleet file was skipped** and the run reports success | A `[!] skipping` line per fleet file, then the success line | The fleets in Fleet against the fleets in your repository. In CI this looks like a green reconcile that changed nothing |
| **Z22** | `debug archive` when finishing the archive fails as it closes | **The failure is discarded, so you are not told.** The path is printed before the compression and archive streams are flushed, so the success line goes out first and anything that fails after it has nowhere to land. **What the file then holds is not something the command establishes** | The archive path | That the archive opens |
| **Z23** | `get carve --outfile` | **Two separate things, and only one of them is an outcome.** The failure to close is discarded, so you are not told whether the file finished being written. Separately, and definitely: **the file is opened without being truncated first**, so writing a shorter carve over a longer file leaves the previous file's tail attached | **Nothing** | The file's size against the carve's recorded size, and write to a fresh path each time |
| **Z24** | `get labels --json` or `--yaml` | **A label that fails to render is omitted.** For a single named label, nothing is printed at all | **Nothing** | The label count against `fleetctl get labels` in table form |
| **Z25** | `api` with a `--field` whose file **cannot be read in the `<` form, or cannot be opened in the `@` form** | **The field is sent as the literal text you typed**, sigil and all, rather than the file's contents | A warning saying so | The request Fleet received. A 2xx response to the wrong body still exits zero. **The third case behaves differently and is not this row**: an `@` file that opens and then fails part-way through copying is logged, forced to a multipart upload, and sent with whatever bytes were copied |
| **Z26** | `report` when the results connection errors mid-run and the run still reaches a normal completion | The errors never reach the exit code. In-flight results are not lost | An error line per error, on standard error | The responded count. **This row is conditioned**: it needs `--timeout`, an error that leaves the connection alive, or a status message that arrives before any totals |
| **Z27** | `updates rotate` where the cleanup after a successful rotation fails | **The cleanup did not finish, and the warning does not tell you how far it got.** The rotation itself is correctly committed. The cleanup removes the repository backup first and returns straight away if that fails, then removes the key backup, so one warning covers three different situations: the key backup was never reached, or it was removed and only its directory remained, or retired key material is still sitting in it. **What the warning does not establish is that any private-key file remains** | "Warning: failure during commit" | Both backup directories under the repository, by hand, because the warning says neither which removal failed nor what it left. The point of a rotation is that the retired key is gone, and this is the signal to go and look rather than the news that it is not |
| **Z28** | `convert -o <file>` when writing the output fails | **The failure is discarded, so you are not told.** Neither the writes nor the close reports anything, so whether the file was completely written is not something the command establishes. Unlike Z23 this file is truncated when it is opened, so there is no leftover tail to confuse the question | **Nothing** | That the output parses |
| **Z29** | `config set` with no setting flag | **Nothing was written** | The subcommand's help text | The context's contents with `config get` |
| **Z30** | `preview` when `~/.fleet/config` exists and does not parse | **Every other context in the file is destroyed** and the malformed file is overwritten | Nothing about the configuration at all. The line that would have reassured you is on the branch that was not taken | Your contexts, before running `preview` on a machine that has any. Back the file up first |
| **Z31** | `updates add` when the copy of the artifact fails as it closes | **The failure is discarded and the command carries on** to the signing step with the copy as it stands. The copy is also written without truncating an existing file. **What the repository ends up holding is not established here**, because that is decided by the signing library rather than by Fleet | **Nothing** | The published artifact's size against the file you gave it, before hosts install it |
| **Z32** | `config get` with any number of arguments other than one | **Nothing was retrieved** | The subcommand's help text | As Z12. This is a second, separate condition, at a separate place, from the unknown-key case |
| **Z33** | `get mdm-commands --host` where you may not read the commands of one of the fleets involved | **Fleet removes the commands you were refused, records the refusal on its own side, and returns success.** If they were all refused, you are told none have been run | A short table with no marker. **The printed count is the count of the printed rows**, so the output is internally consistent and nothing in it records the removal | The same question as a global administrator, or the command results by identifier, which refuses out loud instead |
| **Z34** | `get mdm-command-results --id` **without** `--host`, where the command ran on hosts outside what your role can see | **Fleet loads every result, drops the ones whose host you may not see, and returns success.** It holds both the full set and the reduced one and compares neither. Where the filter removes all of them, it returns nothing at all | The results for the hosts you may see, with nothing marking the removal. Where none survive, **"No results received. Please check again later."**, which names the wrong cause: the results exist and are not yours to see | The same command with `--host`, host by host, which refuses out loud on the ones you may not read. Or the same question as a global administrator |

### The shape of the register, which is the useful part

**Nine of the thirty-four are one command.** `generate-gitops` refuses in nine distinct ways and exits zero every time, including on an authorization refusal. It is hidden, which softens the consequence, and it is the command whose entire output is a repository you are about to commit.

**Three are `report` and two are `trigger`.** Both are commands an operator reaches for during an incident, and in both the zero says considerably less than it will be read to mean.

**Four are a file whose final write or close failure is discarded**, in `debug archive`, `get carve`, `convert` and `updates add`. **None of the four establishes that the file is bad**, only that the command cannot tell you if it is, which is why the check in each case is the file itself.

**Five are in commands run against production hosts**: `mdm run-command`, `run-script`, `apply --dry-run`, `delete -f`, and `gitops` against a Free server. Those are the five worth encoding into whatever runs `fleetctl` for you.

> ### A path with no exit status at all
>
> **`fleetctl report` without `--timeout` can fail to return.** When no timeout is given, the client installs a deadline that by construction never fires. If the results connection then takes a persistent read error, the part of the client that stores progress blocks, the two completion tests can never become true, and the command prints errors indefinitely. `--exit` does not rescue it, because that test needs both values the blocked path stops storing.
>
> **Always pass `--timeout` when the command runs unattended.** It is an invocation where the answer to "what does the exit status prove" is that there is no exit status. **Whether it is the only one is not established**, because the client-library audit behind this appendix is a floor rather than a sweep.

### Why the register is a floor

**Three places a thirty-fifth case could hide**, each stated so a later pass knows where to look. A failure detected inside a helper that returns success to a caller which then prints nothing leaves no trace at either end. The two most consequential rows here, `trigger` and `mdm run-command`, were found by reading Fleet's responses against what the client does with them, which is work no search performs. And the client library paths were audited where the commands reach them rather than in full.

**The class is bounded and the enumeration is a floor.** Treat an absence from this register as "not found" rather than as "does not happen".

## Destructive commands and the flags that widen them

![Troubleshooting](../_assets/icons/troubleshooting.svg) Two different things get called dangerous, and separating them is what makes this section usable. **Some invocations are dangerous in proportion to your intent**: they inherit whatever you point them at, and they announce themselves. **Others are dangerous in proportion to your mistake**: a wrong host, a stale context, or a flag whose reach is wider than its name suggests.

### The six invocations ranked

Ranked on five axes: whether it can be undone, how much one invocation reaches, how much friction stands before the act, whether the output tells you what was done, and what recovery costs.

| Invocation | Why it is here |
|---|---|
| **`api -X DELETE <route>`** | Inherits the route's reach, including Fleet's batch routes. No allow-list, no confirmation, and no validation of what you named. On a non-2xx the body is discarded, so the one place Fleet would have explained itself is gone |
| **`mdm run-command --hosts <many> --payload <raw>`** | One payload, many devices. Fleet checks the payload's shape and refuses a malformed one, and **it does not check that the request type names a real command**. The evidential gap is the worst in the client: a partial push failure is neither printed nor recorded |
| **`hosts transfer --status online --fleet X`** | The largest selection in the client that nothing bounds. `--status online` moves every online host your role can see, which for a global administrator, maintainer or technician is every online host in the deployment. **The client prints no count, asks nothing, and the protocol carries no count to print**, so nothing records the prior assignment either |
| **`user delete-users --csv`** | Irreversible, bulk, no confirmation and no dry run, and it **stops at the first failure part-way through**, so you get a partial deletion and no record of how far it reached |
| **`mdm wipe --host`** | Irreversible, one host, one required flag, no prompt. What it leaves on the disk is the platform's answer rather than Fleet's |
| **`gitops --delete-other-fleets`** | On Premium, and not on a dry run, deletes the fleets not named in the run. A dry run exists and covers it, **and the flag defaults to on in the pipeline scaffold `fleetctl new` generates** ([6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md)) |

**The last two come last on the ranking and are still the two most often named as footguns.** That is the correct result rather than an argument against it: the first four inherit their reach from what you asked for, and the last two are the ones a wrong flag or a stale context turns into an incident.

### Flags that widen what is destroyed

| Flag | On | What it widens |
|---|---|---|
| `--delete-other-fleets` (alias `--delete-other-teams`) | `gitops` | Deletes **the fleets not named in this run**, one at a time. Reaching a fleet that this run's own global file names as an Apple Business or App Store target **stops the run with an error rather than skipping that fleet**, so the deletions already made stand, and which fleets those are follows the order Fleet listed them in. **The guard covers fewer runs than you would expect.** It is assembled only on a Premium run that carries the global file alongside at least one other file, and not for the two-file case of a global file plus Unassigned. A single global file on its own, a global file with only Unassigned beside it, and a run with no global file at all each delete with no protection. Premium only, ignored without a word on Free, and **on by default in the generated pipeline scaffold** |
| `--force` | `apply` | Tells the server to apply past its own validation errors. Its usage text scopes this to organisation-settings and fleet specs |
| `--force` | `generate-gitops` | Overwrites a directory that is not empty |
| `--force`, `-f` | `new` | Writes the scaffold into an existing directory |
| `--flush` | `debug errors` | **Clears the stored errors after reading them and before the output file is written.** If that write then fails, the errors are gone |

### Flags that reach more hosts than their name suggests

| Flag | On | What it reaches |
|---|---|---|
| `--status`, `--label`, `--search_query` | `hosts transfer` | A server-side filter. `--status online` moves every online host your role can see into the named fleet, which is every online host in the deployment for a global role, and no count is printed at any point. Where the selection reaches a fleet you may read but not move hosts out of, **the whole call fails and nothing moves** |
| `--fleet ''` | `hosts transfer` | The empty string is the way to move hosts to Unassigned, so an unset variable in a script is a valid destination |
| `--hosts` with `--labels` | `report` | The **union** of the two, not the intersection |
| `--hosts` as a list | `mdm run-command` | One payload to every host in the list, all or nothing on an unknown identifier |

### Flags that turn a check or a warning off

| Flag | What stops happening |
|---|---|
| `--tls-skip-verify`, or `INSECURE` in the environment, on `config set` | Certificate verification is off **for every later command that builds a client from that context**, because the setting is persisted and no flag turns it back off. `config get` and `config set` read the same context and perform no TLS at all, and `debug connection` overrides the setting and verifies anyway on most of its paths |
| `--insecure` on `package` | Verification is off on **every host installed from that package**. It is a setting in the installed agent service rather than a property of the binary, so it can also be cleared on one host with local administrator rights and a restart of the agent. Rebuilding and reinstalling is the fleet-wide remedy rather than the only one |
| `--insecure` on `generate-gitops` | Secrets are written to the exported tree in plain text |
| `--allow-unknown-keys` on `gitops` | An unknown key becomes a warning instead of an error, which is exactly the check that catches a typo doing nothing |
| `--quiet` on `run-script` | The script's exit-code line is removed from the output, which is where the script's result lives |
| `--quiet` on `report` | The responded-against-online line is removed, and so is the timeout notice |
| `--stdout` on `debug errors` | The "may contain sensitive data" banner is skipped |
| `--debug` on any authenticated command | Request bodies, including tokens and secrets, are written to standard error |

**There is one hidden command and there are three hidden flags.** The command is `generate-gitops`. The flags are two concurrency controls on `gitops` and one path override on `preview`. Hidden means absent from help output, not disabled.

### Where the client prompts, and where it does not

**The client reads from the terminal in ten places, and nine of the ten are a credential or a name**: the email and the password on `login`, the password and its confirmation on `setup`, the password and its confirmation in `user create`, the organisation name in `new`, and the passphrase and its repeat in the update-repository commands. **The tenth is not a credential and not a name.** `user create --api-only` reads a single keystroke, any keystroke, to gate printing the API token, and it skips that read when standard input is not a terminal.

**None of the ten is a confirmation before a destructive act.** `mdm wipe`, `hosts transfer`, `user delete-users`, `gitops --delete-other-fleets` and `api` with a delete verb declare no `--yes`, and four of the five have no dry run either. `gitops` is the one that has one.

**The bound on that claim, stated rather than hidden.** The ten were enumerated from the mechanisms the client can prompt with, and none of the files holding those five invocations uses one of them. A prompt built on something outside that set would not have been found, so **whether any of the five confirms by some other means is not established, and this appendix does not claim that none does**. What is established is where the client is known to read from the terminal, and none of those places is one of the five.

## Choosing packaging options

![How-to](../_assets/icons/howto.svg) `fleetctl package` never contacts your Fleet, and it is the command whose mistakes are hardest to undo, because the result is installed on hosts. **It is not the only row that never calls your Fleet**, as the fourteen listed earlier show, and it is not fully offline either: it downloads signed agent artifacts from Fleet's update server while it builds. [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md), [3.4](../03-connect-devices/3.4-enroll-linux-devices.md) and [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md) defer the option choice here rather than each carrying a flag list; run `fleetctl package --help` for the list itself, which is current for your client.

**Before packaging, settle five choices: server address and secret, Fleet Desktop, scripts, certificate verification, and package type. The last two are the expensive ones.**

**Whether the package carries the server address and the enroll secret.** You may pass both, or neither. **What the command refuses is one without the other.** Omitting both is a deliberate configuration: the host then has to be told where Fleet is by some other means, which on macOS is a configuration profile delivered by MDM.

**Whether the end user gets Fleet Desktop.** `--fleet-desktop` adds the tray application, which is what gives the user a failing-policy count and a way to reach their own device page.

**Whether scripts are enabled on the host.** This one has a consequence outside packaging: **on Linux, wiping a host is a script rather than an MDM command**, so a Linux host packaged without scripts enabled cannot be wiped through `fleetctl mdm wipe` at all, and the error names the missing agent capability rather than the packaging choice.

**Whether certificate verification is on.** `--insecure` writes verification-off into the agent service configuration the package installs, so **every host installed from it skips verification until something changes that setting**. There is no server-side setting that turns it back on and no agent upgrade that fixes it, which leaves two remedies rather than one: rebuild and reinstall, which is the fleet-wide answer, or clear the setting on a host directly with local administrator rights and restart the agent. The second is a per-platform job, because the setting lives in a different place on each of the three.

**Which package type you can build here.** `--type` is platform-gated: **on Windows the client builds one type**, one option is available only when building on Linux, and one only on Windows and macOS. Building for a platform you are not on is a question about your build machine, not about Fleet.

**Two more options bind at build time and cannot be repaired later.** The properties that carry an end user's email and a licence-agreement token into the installer are written by the client that builds the package, so an old client produces a package that cannot carry them and no later agent upgrade changes that. [a.6](a.6-glossary-and-release-compatibility.md) carries the agent floors for both. **Rebuild the package rather than upgrading the agent.**

**The package's `--debug` is not the client's `--debug`.** On `package` it turns on debug logging in the agent you are shipping. Everywhere else it dumps the client's own request bodies to standard error.

## Where the inventory came from, and why a file search under-reports it

![Explanation](../_assets/icons/explanation.svg) The inventory above is the command tree Fleet assembles at 4.90.1, read from source at the release tag, because no `fleetctl` binary trustworthy as 4.90.1 was available to interrogate. That matters when your client disagrees with this table: the likely explanation is that you are running a different version, and the version notes at the end say why that is easy to do without noticing.

**Four things make the tree non-uniform**, and each defeats a naive search of the source files. They are worth knowing because they are also the four places the tree differs between two machines running the same release.

**One command is wired in at run time.** The interactive query shell is always present in the tree, and its implementation is supplied by the program that builds the client. A binary that embeds Fleet's client library without supplying it still shows the command, which then reports that the support is not built in.

**One family exists on two platforms of three.** The self-hosted update repository commands are built for macOS and Linux. On Windows the family is present as a single entry carrying no subcommands, no action and no flags, whose pre-action step returns a message telling you to use a Linux environment. **Whether that pre-action step runs ahead of the client's own help handling is not established here**, because it is decided by the command-line framework rather than by Fleet, and this manual verifies against Fleet's source alone.

**Every `get` subcommand is modified after it is declared**, gaining two logging flags that are not written where the subcommand is. That is why `--enable-log-topics` and `--disable-log-topics` appear across the `get` family and on three other commands and nowhere else.

**Three `debug` subcommands are built by a shared helper** rather than declared one by one, so a search for command declarations finds nine of the twelve.

### The counts, which are platform-specific

**77 named entries on macOS and Linux. 72 on Windows.** The root registers 27 top-level names on every platform. What differs is the update family, which contributes five leaves on macOS and Linux and none on Windows.

| | macOS and Linux | Windows |
|---|---|---|
| Top-level names | 27 | 27 |
| Leaf subcommands | 50 | 45 |
| **Named entries** | **77** | **72** |
| Behavioural rows in the index above | 69 | 65 |

**A behavioural row is an invocation that does something.** On macOS and Linux, nineteen of the 27 top-level commands act in their own right and the other eight are containers whose job is to hold subcommands. On Windows it is twenty and seven, because `updates` holds no subcommands there and fails on invocation instead, which is a behaviour rather than a container. Containers appear in the index as group headings rather than as rows, because a row for a command that does nothing describes a behaviour that does not exist.

**Do not carry 77 across platforms.** It is the count for the macOS and Linux assembly. `fleetctl package` is one command everywhere and still differs by platform in its options: on Windows it builds one package type, one option is available on Linux alone, and another on Windows and macOS alone.

### Two enumerations here are floors rather than inventories

**The permission chains are established by reading each command through to the authorization decisions it reaches**, so a decision taken in middleware, in a wrapper this verification did not assemble, or on a branch it did not reach would not appear. **The exit-zero register is bounded by a stated class and enumerated by search**, and its two most consequential rows were found by reading rather than by searching, which is a fair warning about what a search alone returns.

A floor is useful and it is a different claim from a complete list. Where this appendix has a complete list, such as the 27 top-level names, it says so.

## Aliases, deprecated surfaces, and version notes

![Reference](../_assets/icons/reference.svg) Verified against Fleet 4.90.1. **Every deprecated surface below still works at this release**, and each is the older half of a rename this manual's [a.6](a.6-glossary-and-release-compatibility.md) covers in full.

**A version mismatch between client and server produces a warning and nothing else.** There is no gate and no refusal, on any command, so a client built for another release will talk to your server and fail later in some unrelated-looking way. Pin the client to the server's release in automation ([6.4](../06-automate-fleet/6.4-use-fleetctl.md)).

**`fleetctl --version` never asks the server.** It prints values compiled into the binary, so it answers what you installed and says nothing about what you are connected to.

### The deprecated spellings still accepted

| Deprecated | Current |
|---|---|
| `fleetctl query` | `fleetctl report` |
| `get queries`, `get query`, `get q` | `get reports` |
| `get teams`, `get team`, `get t` | `get fleets` |
| `get mdm-apple-bm` | `get mdm-ab` |
| `generate mdm-apple-bm` | `generate mdm-ab` |
| `--policies-team` on `apply` | `--policies-fleet` |
| `--with-queries` on `get packs` | `--with-reports` |
| `--query-name` on `report`, and `QUERYNAME` | `--report-name`, and `REPORT_NAME` |
| `--delete-other-teams` on `gitops`, and `DELETE_OTHER_TEAMS` | `--delete-other-fleets`, and `DELETE_OTHER_FLEETS` |
| `no-team.yml` in a GitOps repository | `unassigned.yml` |
| `kind: query`, `kind: team` in a spec file | `kind: report`, `kind: fleet` |

**Two aliases are not deprecations and carry no notice**: `run_script` for `run-script`, and `sandbox` for `preview`.

### The deprecation notices, and why silencing them is unreliable

**Nineteen client-side deprecation notices exist. Fourteen are gated on the `deprecated-field-names` logging topic and five are not**, so `--disable-log-topics=deprecated-field-names` and its environment variable cannot silence those five. **Four of the five are on `apply` and `gitops`**, which are the two commands most likely to be running unattended with their output parsed.

Two further asymmetries are worth knowing before you build anything on that flag:

**The topic flags exist on four surfaces only**: the `get` family, `apply`, `gitops` and `report`. Everywhere else `--disable-log-topics` is an unknown flag. One gated notice, on `generate mdm-apple-bm`, therefore sits behind a gate nothing in its own invocation can reach.

**On `apply`, one notice fires before the flag is applied.** The deprecated-flag notice runs in the command's setup and the topic setting is applied at the start of its work, so `apply --policies-team X --disable-log-topics=deprecated-field-names` prints the notice anyway. `gitops`, `report` and the `get` family apply the setting first.

**And `delete -f` prints none of the spec-file notices that `apply -f` prints for the same file.** Both hand the file to the same parser and the notices are the parser's, not the command's; `apply` gives it somewhere to write them and `delete` gives it nowhere, which leaves it no way to say anything at all. The same YAML fed to the two commands that both accept it warns in one and is silent in the other, so a `delete -f` run against a legacy file looks clean whatever it contains.

### Deprecated forms that are errors rather than warnings

Four compatibility conditions fail outright rather than warning, which is the good case and worth knowing so the failure is recognised:

- `gitops` refuses a repository holding both `no-team.yml` and `unassigned.yml` in one run.
- Specifying both a deprecated GitOps key and its replacement is fatal, for any of the 44 renamed key pairs.
- The Apple Business default-fleet key in a GitOps file is now fatal, and a legacy Apple Business configuration with no fleets defined is refused.
- Enabling the failing-policy webhook together with the policy list it replaced is refused.

### What to re-check after an upgrade

**The command tree, the option families and the deprecation surfaces are the volatile parts of this appendix.** The resolution model, the exit-status contract and the shape of the permission chains change far more slowly. When you upgrade, compare `fleetctl <command> --help` against the rows you depend on, and re-read the exit-zero register for the commands your automation runs unattended.
