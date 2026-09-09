---
title: "fleetctl command index and behaviour"
chapter: "Appendices and indexes"
section: "A.7"
sidebar_position: 7
verified_against: Fleet 4.90.0
verified_on: 2026-08-30
verified_source: "drafted against fleet-v4.90.0 (7c428c6e46). The inventory is the assembled root command tree at the tag rather than the output of any installed binary, and each permission chain was traced from the command to the authorization decisions this verification reached, then published as a floor rather than as a complete list. Citation ledger at research/section-notes/a.7-notes.md"
further_reading:
  - https://fleetdm.com/guides/fleetctl
  - https://fleetdm.com/docs/configuration/yaml-files
feature_requests:
  labels: [":product"]
  match: ["fleetctl", "CLI", "command line"]
  exclude: []
---

# fleetctl command index and behaviour

![Reference](../_assets/icons/reference-light.svg) Find a command in [the index](#the-command-index) to check its permissions, effects, and result. Each row links to the chapter that explains the workflow.

Command help lists accepted flags. This appendix adds the behavior behind them: the authorization checks a command reaches, differences between Free and Premium, and what a successful exit status confirms. Some commands operate locally; others submit work that Fleet or a device completes later.

Use the result column and exit-zero register when deciding how to verify a command in a runbook or automation.

<a id="what-this-appendix-carries"></a>

## Coverage and related references

![Reference](../_assets/icons/reference-light.svg) The index covers the public commands and leaf subcommands in the 4.90.0 macOS/Linux tree, plus the Windows-specific entry. It records access requirements, destructive effects, completion timing, and the meaning of each result.

Run `fleetctl <command> --help` for syntax matching your installed client. Use this appendix for context selection, authorization chains, output handling, and flags that expand an operation’s scope.

See [a.4](a.4-roles-and-permissions-matrix.md) for role decisions, [a.3](a.3-configuration-model-and-precedence.md) for configuration precedence, and [6.4](../06-automate-fleet/6.4-use-fleetctl.md) for installation, version pinning, CI contexts, stream capture, and examples.

## The command index

![Reference](../_assets/icons/reference-light.svg) 70 rows, grouped by top-level family: the 69 behaviours of the macOS and Linux tree, and the one row that exists only on Windows. The eight families that hold only subcommands on macOS and Linux appear as headings with no row of their own.

### How to read a row

**Access contract** lists authorization checks in order as `object · action`. Scope is `(global)` when no fleet is supplied, `(fleet)` for the object’s fleet, or `(self)` for your own record. Each required check must pass; holding the final permission is insufficient if an earlier check refuses the request.

These phrases describe commands without an ordinary policy chain:

| Phrase | Means |
|---|---|
| `local` | The invocation asks nothing of Fleet. No permission is involved |
| `unauthenticated` | The request reaches Fleet and carries no credential |
| `global administrator` | Decided by the route's own middleware rather than by the authorization policy |
| `route-dependent` | Whatever the route you named requires |
| `no contract` | The command fails before authentication is reached |

For 51 rows, the listed chain follows two common preflight reads: `version · read`, where any error ends the command, then `app_config · read`, where a permission refusal is tolerated. `preview` uses a separate chain, shown in full in its row.

Rows show separate Free and Premium paths when they differ. Seventeen known cases are collected after the index.

**Effect** describes changes and timing. `sync` returns after the operation; `accepted` returns after Fleet accepts a request; `polls` waits through repeated reads. Other values identify `streaming`, `interactive`, and `local` work.

**Result contract** is what a zero exit proves. A `Znn` reference points into the exit-zero register below.

**Chapter** links to workflow guidance. Every row currently has an owning chapter; `None` would indicate missing guidance in this manual.

### Top-level commands

| Command and purpose | Access contract | Effect | Result contract | Chapter |
|---|---|---|---|---|
| **`api <uri>`** Send a request you compose to any Fleet route. Prefixes the numbered version path unless your URI already carries a version | `route-dependent` | Uses the selected route’s scope. A delete verb against any endpoint, with no confirmation. `sync` | The status was in the 2xx range and the body was streamed out. On any other status **the body is discarded and only the number survives**, and that path exits 1. Z25 | [6.4](../06-automate-fleet/6.4-use-fleetctl.md) |
| **`apply -f <file>`** Push one spec file into Fleet, kind by kind | An ordered chain of up to thirteen steps, one per kind present in the file: `query · write` per report, `label · write` **(global, because this path sends no fleet with it)** per label, `pack · write` (global), `certificate_authority · write`, a bootstrap-package write, `script · write` (fleet), `app_config · write` (global), an Unassigned-profile batch, `enroll_secret · write` (global), `team · write` per fleet spec, then four per-fleet subchains: `mdm_config_profile · write` (the fleet, or global for Unassigned) for profiles; `script · write` (the fleet) for scripts; `team · read` **(global)** then `installable_entity · write` (the fleet) for installers, with that global read **taken again on every poll for as long as the batch runs**; and the same `team · read` (global) then `installable_entity · write` (the fleet) for App Store apps. Then `policy · write`, `user · write`. **Free:** the fleet, installer and App Store nodes evaluate no permission at those nodes and return a licence error, and a label-scoped report is refused the same way | **Destructive.** Overwrites whole objects. `--force` pushes past the server's own validation. `sync` | **On an ordinary run**, every kind present in the file was accepted. With `--dry-run` it proves that three of the eight accepted kinds were checked and says nothing about the other five. Z19 | [6.4](../06-automate-fleet/6.4-use-fleetctl.md) |
| **`delete -f <file>`** Delete the reports, packs and labels named in a spec file | Three kinds in a fixed order: `query · write` on each loaded report, `pack · write` (global) per pack, then **one** `label · write` per label, taken on one of two mutually exclusive branches: a label that does not exist is decided globally, and a label that exists is decided on that label's own scope. Identical on both editions | Deletes supported kinds only. `sync` | The three handled kinds were deleted or did not exist. It says nothing about the other five kinds the same file may carry. Z20 | [6.4](../06-automate-fleet/6.4-use-fleetctl.md) |
| **`setup`** Create the first administrator on a server that has none | `unauthenticated` | Writes the local configuration file. `sync` | The server was un-set-up, is now set up, and your context file holds the new credential | [2.2](../02-administer-and-deploy-fleet/2.2-self-hosting-architecture-and-capacity.md#complete-first-run-setup) |
| **`login`** Exchange an email and password for a token | `unauthenticated` | Overwrites the email and token in the named context. `sync` | The credentials were accepted and the context holds a session token | [6.4](../06-automate-fleet/6.4-use-fleetctl.md) |
| **`logout`** End the session the context holds | `session · write` **(self)**, on your own session. Allowed for every authenticated caller on its own session | Clears the stored token. `sync` | Fleet invalidated the session **and** the local token was cleared | [6.4](../06-automate-fleet/6.4-use-fleetctl.md) |
| **`report`** (alias `query`, deprecated) Run a live report against selected hosts and stream results back | **Two variants.** Ad hoc, with `--query`: `label · read` (global, whether or not you passed `--labels`), `app_config · read` (global) twice, `query · run_new` (global), `targeted_query · run`. Saved, with `--report-name`: `query · read` (fleet) in place of `query · run_new`, and the rest as above. Identical on both editions | No writes. Puts load on every targeted host that checks in while the campaign is live, **which is not the set the targeted count names**: that count includes offline and non-responding hosts, and a host that never checks in never fetches the query. `streaming` | Zero can occur without any host answering: it returns zero on timeout, and a per-host transport error is printed and skipped. Z9, Z10, Z26 | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) |
| **`convert -f <pack.json>`** Turn a legacy osquery pack file into report YAML | `local`. Declares `--config` and `--context` and reads neither | Writes the output file, truncating it. `local` | A file was parsed and YAML was emitted. Z28 | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) |
| **`goquery`** Open an interactive query shell against Fleet | A chain that repeats **per shell command**. Per connect: `target · read` (global). Per query: `label · read` (global), `app_config · read` (global) twice, `query · run_new` (global) **always**, `targeted_query · run`. Identical on both editions | Interactive, and can run live queries. `interactive` | **The shell opened and the session returned, and nothing beyond that.** What happens inside never reaches the exit status: a host that will not resolve, a live query that errors, results that never arrive. In practice the only non-zero exit is a configuration or credential failure before the shell opens | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) |
| **`preview`** (alias `sandbox`) Run a local sandbox Fleet under Docker | **`local` against your Fleet, and authenticated against the sandbox it creates.** It never calls your context's server. Against the sandbox, at a fixed local address, it creates the first administrator unauthenticated, logs in as that account, and then takes a chain: `app_config · read` (global), a nested GitOps reconcile carrying the common prefix and the whole of `gitops`'s chain, `app_config · write` (global) twice, `enroll_secret · read` (global), and then, **only where you did not pass `--no-hosts`**, `host · list` (global) while it waits for the machine to appear. **The account is the one it just made**, so nothing in that chain can refuse you | **Rewrites your client configuration file**, and, unless you pass `--no-hosts`, enrols the machine it runs on into the sandbox. `local` | Docker came up, a sandbox was configured, and unless `--no-hosts` this machine enrolled into it. Z30 | [0.3](../00-Introduction/0.3-how-to-use-this-manual.md#try-fleet-without-deploying-anything) |
| **`vulnerability-data-stream --dir`** Download vulnerability feeds to a directory | `local`. Declares `--config` and `--context` and reads neither | Creates the directory and fills it. `local` | Nine download-or-refresh operations returned success. **Each transfers only where the local copy is out of date**, so zero does not prove that nine feeds were downloaded | [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md) |
| **`package --type <type>`** Build a fleetd installer | `local`. Talks to the update server, never to Fleet, and declares no `--config` or `--context` at all | Writes a package. `--insecure` writes certificate-verification-off into the agent service configuration on every host installed from it. `local` | An installer file was produced | [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md) |
| **`prepare`** Present as a command, and does nothing | `no contract`. It fails before authentication is reached | None. `local` | **Never exits zero.** It returns an error telling you to use the `fleet` server binary | [7.3](../07-operate-fleet/7.3-upgrade-fleet-and-fleetd.md) |
| **`trigger --name <schedule>`** Ask Fleet to run a named scheduled job now | `cron_schedules · write` **(global)**, which [a.4](a.4-roles-and-permissions-matrix.md) records as global-administrator-only | Forces server-side background work to run now. `accepted`, and weaker than that | **The request was delivered.** Not that the schedule ran: Fleet discards the value that says whether it fired. Z7, Z8 | [8.6](../08-troubleshooting/8.6-server-state.md) |
| **`upgrade-packs -o <file>`** Write a migration file turning legacy packs into reports | The client refuses unless your account holds the global administrator role, then five decisions: `user · read` (self), `app_config · read` (global), `pack · read` (global) twice, `query · read` **(global)** | Read-only against Fleet. Writes a local file, **and only where there was something to write**. `sync` | The run reached the end of listing your packs. **It does not prove a file was written**: with no legacy packs to convert, Fleet prints an absence notice and returns before the output path is opened, so anything already sitting at that path is left as it was | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) |
| **`run-script`** (alias `run_script`) Run a script on one host | **Two chains, because the waiting form keeps asking.** Both begin with `app_config · read` (global, a second and **less tolerant** read than the prefix), `host · selective_list` (global), `host · selective_read` (fleet), `script · read` (the fleet you named, on the `--script-name` form), `host_script_result · write` (the host's fleet). **The default form then takes `host_script_result · read` (the host's fleet) once per poll**, for as long as it waits; `--async` stops at the write and takes it never. **Premium** only where `--fleet` names a fleet other than Unassigned, and there **the server checks the licence before it looks the saved script up**, so on Free neither `script · read` nor `host_script_result · write` is reached and the refusal reads `Requires Fleet Premium license`. Client preflights can still refuse you before the server is reached | **Runs arbitrary code on a device as root or SYSTEM.** No confirmation. `polls` by default: the client asks Fleet for the result every five seconds, **with no polling deadline and no overall request timeout on the client**. Where the host runs the script, the agent's own execution limit ends the wait by producing an exit code; where no result is ever recorded, nothing ends it. `--async` returns an execution identifier instead of waiting. Refused when the host is not online, or when scripts are disabled | Fleet delivered the script and a result came back. **The script's own exit code is a line of output**, which `--quiet` removes. Z18 | [5.3](../05-manage-devices/5.3-run-and-manage-scripts.md) |
| **`gitops -f <file>...`** Reconcile Fleet against declared files | A fourteen-step chain: `app_config · read` (global) twice, `label · read` (Unassigned), `team · read`, a `label · read` per non-global file, the whole of `apply`'s chain per file plus custom host vitals and organisation logos, the Apple Business token count, `app_config · write` for the token re-patch, the fleet listing and deletion under `--delete-other-fleets`, `label · write` twice per removed label, and `certificate_authority · write`. **Free:** Most fleet-scoped nodes return a licence error without evaluating permission at that node. Two nodes do the opposite and authorize first: a label-scoped policy, and a configuration profile scoped by label. Fleet files themselves never get that far on Free, because the client skips them before the run reaches the server | Replaces declared state. On Premium, and not on a dry run, `--delete-other-fleets` removes the fleets not named in the run. A global file with no Unassigned file applies an empty Unassigned configuration. `sync` | Reconciliation completed. With `--dry-run`, that validation passed. Z21 | [6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md) |
| **`generate-gitops`** (hidden) Export the running deployment as a GitOps tree, or print one configuration key | A 23-node chain behind a client-side administrator check **that does not hold for a fleet-scoped account**. Always `user · read` (self) then `app_config · read` (global); then, by scope and edition, fleet reads, enroll secrets, certificate authorities, the licence agreement, App Store tokens, per-fleet profiles, scripts, policies, reports and software, a `host · list` plus `software_inventory · read` **per software title**, and `label · read`. **Free:** the run stops at the certificate-authority or licence-agreement node | `--force` overwrites a non-empty directory. `--insecure` writes secrets in plain text. `sync` | It returns zero on a missing flag, on both flags, on a directory it will not overwrite, and on refusing you for not being authorised. Z1 to Z6, Z14, Z15, Z16 | [6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md) |
| **`new`** Render a starter GitOps repository into a directory | `local`. Declares no `--config` or `--context` | `--force` writes into an existing directory. `local` | A directory tree was written | [6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md) |

### `fleetctl get`, sixteen read subcommands

The family holds no behaviour of its own. Every subcommand is authenticated and carries the two logging flags.

| Command and purpose | Access contract | Effect | Result contract | Chapter |
|---|---|---|---|---|
| **`get reports [name]`** (aliases `report`, `r`; deprecated `queries`, `query`, `q`) List reports, or print one | List and named-lookup forms use different chains. Both take `team · read` (the fleet you named) **only where `--fleet` names a fleet**, then `query · read` on that fleet, or globally where you named none. **The list form adds two the named form never takes**: `user · read` (self), read solely to filter the list for observers, and a `query · read` **(global)** behind the inherited-reports note, which fires whenever you named a fleet and either it holds no reports of its own or you are taking the default table. A named lookup takes neither. **Free:** with `--fleet`, the fleet read returns a licence error without evaluating permission at that node, and **this is one of the few rows that then exits non-zero** | Read-only. `sync` | The list Fleet returned, filtered client-side for observers. Z11 | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) |
| **`get packs [name]`** (aliases `pack`, `p`) List legacy packs, or print one | `pack · read` (global). With `--with-reports`, a `query · read` (global) as well | Read-only. `sync` | The packs Fleet returned | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) |
| **`get labels [name]`** (aliases `label`, `l`) List labels, or print one | `label · read` (the fleet you named). **Both editions take that decision.** On Free, `--fleet` naming a fleet is authorized first and refused for the licence afterwards, so a Free refusal here does mean your permission was checked | Read-only. `sync` | The labels Fleet returned, **minus any that failed to render**. Z24 | [1.3](../01-foundations/1.3-hosts-fleets-labels.md) |
| **`get hosts [identifier]`** (aliases `host`, `H`) List hosts, or print one | Without an identifier: `host · list` (global), plus a tolerated `app_config · read` when `--mdm` or `--mdm-pending` is passed. With an identifier: `host · selective_list` (global) then `host · selective_read` (the host's fleet) | Read-only. `sync` | The hosts Fleet returned | [4.1](../04-know-your-devices/4.1-understand-hosts-vitals-and-inventory.md) |
| **`get enroll_secret`** (aliases `enroll_secrets`, `enroll-secret`, `enroll-secrets`) Print the enroll secrets | `enroll_secret · read` (global) | Read-only, and **it prints live enroll secrets to standard output**. `sync` | The secrets Fleet holds | [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md) |
| **`get config`** Print the organisation settings | `app_config · read` (global). `--include-server-config` widens the answer to the server's own configuration | Read-only. `sync` | The settings Fleet returned, with the fields your role is allowed to see ([a.4](a.4-roles-and-permissions-matrix.md)) | [2.7](../02-administer-and-deploy-fleet/2.7-organization-and-server-settings.md) |
| **`get carves`** List file carves | `carve · read` (global) | Read-only, table output only. `sync` | The carves Fleet returned | [8.7.8](../08-troubleshooting/8.7-live-query-introspection.md#878-running-and-retrieving-a-file-carve) |
| **`get carve <id>`** Print a carve, or write it out | `carve · read` (global). With `--stdout` or `--outfile` the same decision is taken again for the metadata and **once per block** until the carve ends | Writes a file **without truncating it**, so a shorter carve leaves the previous file's tail behind. `sync` | Metadata was printed, or bytes were written. Z23 | [8.7.8](../08-troubleshooting/8.7-live-query-introspection.md#878-running-and-retrieving-a-file-carve) |
| **`get user_roles`** Print account roles | `user · read` (global) | Read-only. `sync` | **The default table prints one row per account carrying the global role only**, which is blank for a fleet-scoped account and never shows that account's per-fleet roles. `--json` and `--yaml` carry the global role and every fleet role, keyed by email | [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md) |
| **`get fleets`** (aliases `fleet`, `f`; deprecated `teams`, `team`, `t`) List fleets | **Free: the listing returns a licence error and the chain has no decisions at all at that point.** Premium table output: `team · read` (global). Premium `--json` or `--yaml` adds `software_inventory · read` (fleet) per fleet, a setup-experience read per fleet where the first returned a title, then `host · list` (fleet) and `software_inventory · read` (fleet) **per title per fleet**, and a maintained-app read per distinct Fleet-maintained package. **The structured form's chain grows with the number of software titles** | Read-only. `sync` | The fleets Fleet returned | [1.3](../01-foundations/1.3-hosts-fleets-labels.md) |
| **`get software`** (alias `s`) List software titles, or versions | `software_inventory · read` (the fleet you named). With `--versions`, the same decision twice, because the endpoint lists and then counts. **Both editions take that decision.** On Free, `--fleet` naming a fleet is authorized first and refused for the licence afterwards | Read-only. `sync` | The titles or versions Fleet returned | [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md) |
| **`get mdm-apple`** (alias `mdm_apple`) Print the Apple push certificate's status | `mdm_apple · read` (global) | Read-only, key-and-value table only. `sync` | The certificate's status, or an advisory that none is configured, which also exits zero | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) |
| **`get mdm-ab`** (alias `mdm_ab`) Print the Apple Business token's status | `mdm_apple · read` (global). **Free:** a licence error without evaluating permission | Read-only, key-and-value table only. `sync` | The token's status, or an advisory that none is configured | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) |
| **`get mdm-apple-bm`** (alias `mdm_apple_bm`) **Deprecated.** The former name of `get mdm-ab`, and a separately registered command with its own deprecation notice | As `get mdm-ab`, including the Free behaviour | Read-only. `sync` | As `get mdm-ab` | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) |
| **`get mdm-command-results --id`** Print the per-host results of one MDM command | Host-filtered and unfiltered requests differ. With `--host`: a tolerated `app_config · read` (global), `host · list` (global), then `mdm_command · read` **on that host's fleet**, and **a refusal there ends the command**. Without `--host`: the same first two, then Fleet loads every result for the command, keeps only those whose host you are allowed to see, and takes `mdm_command · read` once per fleet **still standing after that filtering**, which is a decision your visibility has already satisfied. **Nothing in the second variant can refuse you on the results it removed** | Read-only, text blocks only. `sync` | **With `--host`**, the results for that host, or an advisory that none have arrived yet. **Without it, the results for the hosts you may see, and no sign that there were others.** Z34 | [8.8](../08-troubleshooting/8.8-apple-mdm-diagnostics.md) |
| **`get mdm-commands --host`** List recent MDM commands for a host | The same three decisions as the row above, but **a refusal is not fatal**: the commands you may not read are filtered out and the call still succeeds | Read-only, table output only, and a fixed page of the 20 most recent. `sync` | The commands Fleet returned **after removing any you were refused**. The printed count covers returned rows only, without indicating omissions. Z33 | [8.8](../08-troubleshooting/8.8-apple-mdm-diagnostics.md) |

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

Eleven diagnostics use the routes’ own global-administrator authentication. `debug connection` requires no credential. Eight always write a file under a generated name in the working directory; `cmdline` writes only with `--outfile`, `errors` writes unless `--stdout` is used, and `connection` creates and removes a temporary file. `migrations` writes no file. New files receive owner-only permissions. Only the archive path repairs existing permissions, and only on Unix; other existing targets keep their permissions. [8.5](../08-troubleshooting/8.5-fleetctl-debug.md) covers these diagnostics.

| Command and purpose | Access contract | Effect | Result contract |
|---|---|---|---|
| **`debug profile`** Collect a 30 second CPU profile | `global administrator` | Writes a file. `sync` | A profile file was written |
| **`debug cmdline`** Print the server's own command line | `global administrator` | Read-only against Fleet, and **`--outfile` writes it to a local file** instead of printing it. May contain sensitive command-line arguments. `sync` | The server's arguments, printed or written |
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
| **`preview stop`** Stop the sandbox | `local` | Stops the containers and the sandbox agent. `local` | The stop was issued | [0.3](../00-Introduction/0.3-how-to-use-this-manual.md#try-fleet-without-deploying-anything) |
| **`preview reset`** Delete the sandbox | `local` | Removes the sandbox's containers and Orbit's downloaded update files. **Reuses the saved private key and certificates in the config directory and leaves the named Docker volumes**, so the stored data survives and this is not a clean wipe. `local` | The sandbox was removed | [0.3](../00-Introduction/0.3-how-to-use-this-manual.md#try-fleet-without-deploying-anything) |

A preview reset retains the configuration directory, private key, certificates, and named database volumes for later reuse. To remove that saved state too, reset the sandbox, take down the Compose stacks with their volumes, and delete the preview directory before starting again.

### `fleetctl updates`, five subcommands on macOS and Linux and one behaviour on Windows

The five update-repository subcommands are available on macOS and Linux. Each works on a local signing repository under `--path` and prompts for a passphrase. Windows has a single `updates` entry that fails and directs you to Linux. The parent help describes an enterprise licence requirement; these local commands do not contact Fleet or check its licence tier.

| Command and purpose | Access contract | Effect | Result contract | Chapter |
|---|---|---|---|---|
| **`updates init`** Create a repository and its keys | `local` | Creates key material. `local` | A repository was created | [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md) |
| **`updates roots`** Print the repository's root keys | `local` | Read-only. `local` | The roots were printed | [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md) |
| **`updates add`** Publish an artifact for a platform and channel | `local` | **Publishes something your hosts will download and install.** The copy it makes is written without truncating an existing file, and it is copied before it is signed. Whether a bad copy is caught at the signing step is decided outside Fleet's own source. `local` | An artifact was added to the repository. Z31 | [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md) |
| **`updates timestamp`** Re-sign the repository's timestamp | `local` | Re-signs. `local` | The timestamp was refreshed | [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md) |
| **`updates rotate <role>`** Replace the signing key for a role | `local` | **Retires a signing key.** `local` | The repository was committed. **It does not prove the post-rotation cleanup finished**: a failure there prints one warning line that names which backup removal failed but not what it left behind. Z27 | [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md) |
| **`updates` on Windows** The whole family, reduced to one entry that refuses | `no contract`. It builds no client, declares no flags, and fails before authentication is reached | None. It reaches neither Fleet nor a local repository, and destroys nothing. `local` | **Never exits zero.** It returns the message telling you to use a Linux environment, which is also the entry's own description text | [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md#running-your-own-update-repository) |

### `fleetctl hosts`, one subcommand

| Command and purpose | Access contract | Effect | Result contract | Chapter |
|---|---|---|---|---|
| **`hosts transfer --fleet <name>`** Move hosts into a fleet | **Variant-dependent, four decisions either way.** With `--hosts`: `host · read` (global) once per host, `team · read` (global) for the destination, `host · transfer_host` on the destination fleet, then `host · transfer_host` on **each distinct source fleet**. With `--label`: `label · read` (global) in place of the per-host reads, and the same three that follow. `--status` or `--search_query` without `--label` skips the first decision entirely. Identical on both editions | Changes hosts’ configuration scope. The filter form moves whatever the filter selects, server-side, **within the hosts your own role can see**, and **the client never counts or prints how many hosts it is about to move**. `--fleet ''` means Unassigned. `sync` | Fleet accepted the transfer. **No count is available in the protocol**, so the number moved is not knowable from the command | [1.3](../01-foundations/1.3-hosts-fleets-labels.md) |

### `fleetctl generate`, three credential-request subcommands

Each credential-generation command requires a global write followed by a read. Two create key material on the Fleet server before writing a local file. On their first successful run, `generate` therefore changes server state as well as producing an artifact.

| Command and purpose | Access contract | Effect | Result contract | Chapter |
|---|---|---|---|---|
| **`generate mdm-apple`** (alias `mdm_apple`) Request the signing request for an Apple push certificate | `mdm_apple · write` (global) then `app_config · read` (global). The policy grants that write to the global administrator role and to nothing else | **Server state first, file second.** On the first run Fleet creates a certificate authority certificate and key and a push private key, and **stores all three on the server, encrypted**; later runs reuse them. It then builds a fresh signing request every time and **sends it to Fleet's own service rather than to Apple**. Writes the request file with owner-only permissions. `sync` | Fleet's service returned a signed request and the file was written. **Apple has not seen anything**: uploading the file is your next step. **A failure after this point does not undo the stored keys**, and the file is written before the settings are read, so a late failure leaves both behind | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) |
| **`generate mdm-ab`** (alias `mdm_ab`) Request the public key for an Apple Business token | `mdm_apple · write` (global) then `app_config · read` (global), the same global-administrator-only write | **Server state first, file second.** On the first run Fleet creates an Apple Business keypair and stores both halves on the server; **the private half never leaves Fleet**. Later runs hand back the stored pair, which is the renewal path. Only then is the public half written locally, with owner-only permissions. `sync` | The keypair exists on the server and the public key file was written. **The keypair persists whether or not the rest of the command succeeded** | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) |
| **`generate mdm-apple-bm`** (alias `mdm_apple_bm`) **Deprecated.** The former name of `generate mdm-ab` | Identical to `generate mdm-ab` | As above. `sync` | As above | [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) |

### `fleetctl mdm`, five device-action subcommands

Four MDM subcommands share a host-resolution preflight that contributes the first two permission checks on both Free and Premium. Later service checks differ by tier, as the rows below show.

On Premium, `lock`, `unlock`, and `wipe` additionally require a broad global `host · list`; `clear-passcode` requires global `host · read`. A role with selective host access and `mdm_command · write` can still fail that intervening check.

| Command and purpose | Access contract | Effect | Result contract | Chapter |
|---|---|---|---|---|
| **`mdm run-command --hosts --payload`** Send a raw MDM payload to one or more hosts | Five decisions: a tolerated `app_config · read` (global), `host · selective_list` (global) and `host · selective_read` (fleet) once per identifier, `host · selective_list` (global) again inside the send, then `mdm_command · write` **once per fleet the target set touches**. Identical on both editions, with Free refusing the erase, lock and clear-passcode Apple request types and the premium Windows form | **Whatever the payload does**, within the shape Fleet enforces. Fleet parses the payload on both platforms, rewrites its identifier, and refuses a malformed one, **but it does not check that the request type names a real command**. Refuses a target set mixing macOS and Windows hosts. `accepted` | Fleet stored the command for every targeted host. **A partial push failure is not reported to you and no activity is recorded for the hosts it failed for.** Z17 | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) |
| **`mdm lock --host`** Lock a device | `host · selective_list` (global), `host · selective_read` (fleet), `host · list` (global, broad), `mdm_command · write` (the host's fleet). **Free: the first two are taken exactly as on Premium**, because the client resolves the host either way; **the service node that would lock evaluates no permission at that node** and returns a licence error, so the last two are never reached and a Free refusal tells you nothing about whether you hold them | **Destructive.** Recovery needs the PIN Fleet issues, or the end user's own PIN on Android. `accepted` | Fleet accepted the lock. The device acts when it next checks in | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) |
| **`mdm unlock --host`** Unlock a device | The same four decisions. **Free: the same first two are taken, and no permission is evaluated at the unlock node; licence error** | Reverses a lock, and prints the six-digit PIN for a Mac. `accepted` | Fleet accepted the unlock | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) |
| **`mdm wipe --host`** Wipe a device | The same four decisions **on both editions**, and the licence check comes after them: on Free the command works for a company-owned Android device and returns a licence error for every other platform | **Irreversible, and platform-specific.** It asks Fleet to run the wipe action defined for that host's platform, which is an Apple erase command, a Windows remote-wipe command, an Android enterprise wipe, or, on Linux, **a script run by fleetd**, which requires the agent to have been deployed with scripts enabled. What is left on the disk is the platform's answer rather than Fleet's. One required flag, **no prompt, no dry run**. `accepted` | Fleet accepted the wipe | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) |
| **`mdm clear-passcode --host`** (alias `clear_passcode`) Clear a device or work-profile passcode | `host · selective_list` (global), `host · selective_read` (fleet), **`host · read`** (global, broad, and not `list` as the three above), `mdm_command · write` (the host's fleet). **Free: the same first two are taken, and no permission is evaluated at the clear-passcode node; licence error.** iPhone, iPad and Android only | Clears the passcode. `accepted` | Fleet accepted the request. **Fleet deliberately records no pending action on the host**, so the host record shows nothing and completion appears only as an activity | [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) |

<a id="the-seventeen-rows-whose-access-contract-differs-between-free-and-premium"></a>

### Known access differences between Free and Premium

The command’s licence tier can change both the checks performed and their order. These seventeen rows are known differences; other paths into the same community fleet-management services may share them.

The differences take two forms:

In twelve rows, the Free service returns a licence error without checking permission at that node. Earlier client or server checks can still run. For example, `mdm lock`, `unlock`, and `clear-passcode` perform two host checks first. `run-script` for a named fleet runs client preflights, then receives a licence refusal before `script · read` or `host_script_result · write`. Passing the earlier checks on Free does not establish that the later permissions will pass after an upgrade to Premium.

In seven rows, both tiers perform the same permission checks and then apply a licence restriction. `apply -f` and `gitops` contain both forms, so the two groups cover seventeen distinct rows. `mdm wipe` checks permissions before the licence; `mdm run-command` authorizes the target set before inspecting restricted request types. `user create`, `get labels --fleet`, and `get software --fleet` also authorize before returning a licence refusal.

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

No access-chain split was found for `hosts transfer`, `trigger`, `generate mdm-ab`, `delete -f`, `report`, or `goquery`. On Free, `hosts transfer` can still fail because its destination fleet does not exist.

<a id="which-commands-have-an-owning-chapter"></a>

### Workflow chapters

Every command row links to a chapter explaining when and how to use it. These two workflows include additional setup context:

| Group | Commands | Owning chapter |
|---|---|---|
| **The local evaluation sandbox** | `preview`, `preview stop`, `preview reset` | [0.3](../00-Introduction/0.3-how-to-use-this-manual.md#try-fleet-without-deploying-anything) |
| **First-run setup** | `setup` | [2.2](../02-administer-and-deploy-fleet/2.2-self-hosting-architecture-and-capacity.md#complete-first-run-setup), which teaches both the browser and command-line paths, the one-time route Fleet retires once the first administrator exists, and the refusal a second attempt produces |

[3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md#running-your-own-update-repository) covers update repositories, including the Windows refusal and the need to use a supported build environment.

Use the access, effect, and result columns for a quick lookup, then follow the chapter link for surrounding steps and verification.

[a.1](a.1-capability-index.md#where-this-index-ends) organizes outcomes rather than commands. The local evaluation sandbox has a workflow chapter here but no separate capability row there, so the two registers’ totals should not be combined.

<a id="which-server-and-which-credential-an-invocation-selects"></a>

## Selecting the server and credential

![Reference](../_assets/icons/reference-light.svg) Confirm the selected configuration file and context before running a command that changes Fleet or its hosts.

The client stores named contexts in `~/.fleet/config`, unless `--config` selects another file. `--context` selects a context, defaulting to `default`. Each context holds the server address, email, token, certificate authority, URL prefix, verification setting, and custom headers. Switching context changes all of them together.

**The file is created with owner-only permissions inside an owner-only directory**, and on macOS and Linux the client refuses to open an existing file whose group or other permissions are wider than that. On Windows there is no such check.

Configuration writes replace the whole file without locking it. Concurrent processes can overwrite each other’s changes while both exit zero. Give each automation job its own file ([6.4](../06-automate-fleet/6.4-use-fleetctl.md)).

Check these cases when setting up a context:

| Situation | What happens |
|---|---|
| No configuration file at all | One is created, and the command then fails, asking you to set an address |
| `--context` names a context that does not exist | A hard error, for every command except `config get` and `config set` |
| The same, under `config get` or `config set` | **The context is created**, with a printed note. A misspelling such as `prod-typo` becomes a separate usable context; it does not update `prod` |
| An address is set and the token is empty | An instruction to log in, on standard error, or the single sign-on instructions where the server reports it enabled |
| **Windows, with no certificate authority and no skip-verify setting** | A hard refusal. Configure a certificate authority or an explicit verification setting |

<a id="the-two-round-trips-an-authenticated-command-makes-before-its-own-work"></a>

### Common authenticated preflight requests

Most authenticated commands read Fleet’s version and application configuration before starting their own operation. Errors from the two reads are handled differently:

| | What it asks | What a refusal does |
|---|---|---|
| **First** | `version · read` (global) | **Ends the command.** Any error, a permission error included, returns before your work begins. This call doubles as the check that your token is still valid |
| **Second** | `app_config · read` (global) | **Tolerated when it is a permission refusal**, fatal otherwise. The tolerance is what lets a low-privilege automation identity, such as one holding the GitOps role, use the client at all |

The 51 affected rows list only checks after this prefix. An application-configuration read shown in a row is therefore a second, command-specific read.

Eighteen of the 69 macOS/Linux rows omit the prefix. Fourteen make no Fleet call: `convert`, `package`, `new`, `vulnerability-data-stream`, `prepare`, `preview stop`, `preview reset`, both `config` subcommands, and the five update-repository commands. Three call Fleet without credentials: `setup`, `login`, and `debug connection`. The remaining command is `preview`.

`preview` calls the sandbox it creates, never your context’s Fleet server. It creates and signs in as the first administrator, reads and writes application configuration, reads the enroll secret, lists hosts, and runs a nested GitOps reconcile with the common prefix. Those checks use the new sandbox administrator. Thus eighteen rows omit the outer prefix, but only seventeen avoid Fleet authorization entirely.

<a id="where-a-value-comes-from-when-you-did-not-pass-a-flag"></a>

### Flag defaults and environment variables

The root command declares no global flags. Individual commands declare the shared flags below. Whether the CLI framework accepts a command flag before the command name has not been established here; Fleet’s tests do not use that placement.

| Flag | Environment variable | Default |
|---|---|---|
| `--config` | `CONFIG` | `~/.fleet/config` |
| `--context` | `CONTEXT` | `default` |
| `--debug` | `DEBUG` | off |
| `--enable-log-topics`, `--disable-log-topics` | `FLEET_ENABLE_LOG_TOPICS`, `FLEET_DISABLE_LOG_TOPICS` | unset |

The standard `--debug` flag writes request bodies to standard error. On `login`, `user create`, `apply`, or `gitops`, this can include credentials in terminal history or CI logs. `config set` makes no request and has no standard debug flag.

Shared flags are not available everywhere. `package` has no `--config` or `--context`, and its own `--debug` enables agent logging in the installer. `new` declares none of the shared flags. The five `mdm` and three `generate` subcommands declare `--context` and `--debug`, while their parents declare `--config`.

Many client environment variables are unprefixed: `TOKEN`, `PASSWORD`, `INSECURE`, `FORCE`, `DRY_RUN`, `DEBUG`, `QUIET`, `TIMEOUT`, `NAME`, `DIR`, `HOSTS`, `QUERY`, `EMAIL`, `FILENAME`, and `DELETE_OTHER_FLEETS`. Check for values inherited from a shell or CI runner. `DEBUG=1` enables request-body logging on commands with the standard debug flag. `new`, `convert`, both `config` subcommands, `prepare`, and update-repository commands ignore it; `package` has a separate debug flag with no environment binding. `INSECURE=1` causes `config set` to persist disabled certificate verification. Packaging variables use the `FLEETCTL_` prefix.

**In automation, pass the flags explicitly** and give each job its own configuration file.

<a id="what-is-not-established-about-flag-placement"></a>

### Unverified flag placement

Acceptance of `--config` after a subcommand that does not declare it has not been established for this release.

The `mdm` and `generate` parents declare `--config`; their eight subcommands read its value but do not declare it. Resolving that placement belongs to the third-party CLI framework, which was outside this source review. Fleet’s tests provide no example with the flag after those subcommands.

Follow Fleet’s tested form: place `--config` on the command that declares it, or use the `CONFIG` environment variable.

## What a result and an exit status prove

![Reference](../_assets/icons/reference-light.svg) A zero exit confirms that the client returned without an error. Depending on the command, you may still need to check device completion, validation coverage, or a warning in the output.

The client returns zero or one; it does not assign separate exit codes to not-found, permission, and network failures. Signals, panics, and launcher failures can produce other process statuses.

Capture both standard output and standard error. The client has error-printing paths for both, and the CLI framework decides which handles a failure. That dispatch was not established in this source review.

The client removes the leading HTTP-status phrase from displayed request errors. A script searching the error text may therefore not find the status number.

### Four things exit zero can mean

Interpret the result column using these four cases:

**Completed request.** Fleet returned success for the operation, as most rows describe.

**Accepted work.** The five `mdm` subcommands and `run-script --async` return before device completion. Check the result in Fleet later. These normal asynchronous operations are marked `accepted` in the index and are excluded from the exit-zero exception register.

**Outcome reported in text.** A waiting `run-script` exits zero regardless of the script’s result; the script exit code appears in output unless `--quiet` removes it. `report` also exits zero on timeout.

**Refused, incomplete, or partial work.** The register below lists cases where the client detects a problem but exits zero. Many print a warning or advisory, so automation needs to inspect more than the exit status.

<a id="output-modes-and-where-structured-output-is-absent"></a>

### Terminal and file output formats

Output flags vary by command. These five renderers are available:

| Mode | Where you get it |
|---|---|
| Table | The default for `get reports`, `packs`, `labels`, `hosts`, `user_roles`, `fleets` and `software`, and the sole mode for `get carves`, `get mdm-commands`, `get mdm-apple`, `get mdm-ab` and `get mdm-apple-bm` |
| `--yaml` | Nine `get` subcommands. `get carve` prints YAML whether you ask for it or not |
| `--json` | The same nine |
| JSON lines | `fleetctl report`, by default: one object per host, carrying the host, its rows and any error |
| Live table | `fleetctl report --pretty` |

**`--remove-deprecated-keys` strips the older key spellings from JSON and YAML output.** Without it the output carries both the current and the deprecated name for the same field, which matters when the output is going back into `apply`.

Many commands print prose to the terminal: all `mdm` subcommands, `run-script`, `trigger`, `gitops`, `apply`, `delete`, `upgrade-packs`, `get mdm-command-results`, `package`, `new`, update-repository commands, and most `debug` output. Sentence wording can change between releases. `debug errors --stdout` is an exception that streams JSON.

Some of these commands write structured files. `upgrade-packs` writes report YAML to a required output path, and `new` creates a YAML repository. Four diagnostics write JSON: `errors` and the three database diagnostics, also included in `debug archive`. `get mdm-command-results` has no structured mode; it prints text blocks with XML payload and result cells.

`hosts transfer`, `goquery`, `user create`, and `user delete` declare `--yaml` but do not read its value. The flag has no destination, environment variable, or action binding; the query shell receives only a client. Framework behavior for such an unused flag is not established here.

Normal output also uses several paths: some commands use the client writer, others write directly to standard output, and API-client progress and warnings go to standard error. Preserve both streams in automation.

## The exit-zero register

![Troubleshooting](../_assets/icons/troubleshooting-light.svg) These thirty-four invocations return zero despite detecting refused, incomplete, or partial work. Check the relevant rows before running a command unattended.

The register includes cases where the code detects a material problem with the advertised outcome but returns success. It excludes these normal results:

- **Expected absence**, such as a successful lookup finding no users.
- **Asynchronous acceptance**, recorded in the index’s result column.
- **Results still pending**, before the operation can be assessed.

Every listed case exits zero. Z8 prints a success line even though the trigger signal was not published. Z20, Z23, Z24, Z28, and Z31 print no warning; inspect the expected output or stored object to detect the problem.

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
| **Z19** | `apply --dry-run` on a file holding reports, labels, packs, policies or user roles | **Five of the eight accepted kinds were not validated at all** | A `[!] ignoring` line per skipped kind | The five kinds, by applying to a non-production Fleet. A pull-request gate needs additional validation for these kinds |
| **Z20** | `delete -f` on a file holding any kind other than report, pack or label | **Nothing was deleted for those kinds** | **Nothing.** No message, no warning | Whether the objects still exist. Four other rows are silent in the same way: Z23, Z24, Z28 and Z31 |
| **Z21** | `gitops` with fleet files against a **Free** server | **Every fleet file was skipped** and the run reports success | A `[!] skipping` line per fleet file, then the success line | The fleets in Fleet against the fleets in your repository. Check for skipped scopes even when CI reports success |
| **Z22** | `debug archive` when finishing the archive fails as it closes | **The failure is discarded, so you are not told.** The path is printed before the compression and archive streams are flushed, so the success line goes out first and anything that fails after it has nowhere to land. **What the file then holds is not something the command establishes** | The archive path | That the archive opens |
| **Z23** | `get carve --outfile` | The failure to close is discarded, so you are not told whether the file finished being written. Separately, and definitely: **the file is opened without being truncated first**, so writing a shorter carve over a longer file leaves the previous file's tail attached | **Nothing** | The file's size against the carve's recorded size, and write to a fresh path each time |
| **Z24** | `get labels --json` or `--yaml` | **A label that fails to render is omitted.** For a single named label, nothing is printed at all | **Nothing** | The label count against `fleetctl get labels` in table form |
| **Z25** | `api` with a `--field` whose file **cannot be read in the `<` form, or cannot be opened in the `@` form** | **The field is sent as the literal text you typed**, sigil and all, rather than the file's contents | A warning saying so | The request Fleet received. A 2xx response to the wrong body still exits zero. **The third case behaves differently and is not this row**: an `@` file that opens and then fails part-way through copying is logged, forced to a multipart upload, and sent with whatever bytes were copied |
| **Z26** | `report` when the results connection errors mid-run and the run still reaches a normal completion | The errors never reach the exit code. In-flight results are not lost | An error line per error, on standard error | The responded count. **This row is conditioned**: it needs `--timeout`, an error that leaves the connection alive, or a status message that arrives before any totals |
| **Z27** | `updates rotate` where the cleanup after a successful rotation fails | **The rotation is correctly committed and the command exits zero, and retired key material may outlive it.** The cleanup removes the repository backup first and returns straight away if that fails, then removes the key backup. So the warning names the failed category but not the exact remainder: if repository-backup removal fails, key-backup removal is never attempted, so the key backup is untouched and the retired private keys are certainly still on disk; if key-backup removal fails, the removal may already have taken all, some or none of the backup's contents, so an indeterminate subset of the retired key files may remain | **"Warning: failure during commit: remove repository backup directory ..."** or **"... remove keys backup directory ..."** | The named backup directory under the repository, by hand. The warning identifies which removal failed but not the exact files it left, so inspect it for retired key material |
| **Z28** | `convert -o <file>` when writing the output fails | **The failure is discarded, so you are not told.** Neither the writes nor the close reports anything, so whether the file was completely written is not something the command establishes. Unlike Z23 this file is truncated when it is opened, so there is no leftover tail to confuse the question | **Nothing** | That the output parses |
| **Z29** | `config set` with no setting flag | **Nothing was written** | The subcommand's help text | The context's contents with `config get` |
| **Z30** | `preview` when `~/.fleet/config` exists and does not parse | **Every other context in the file is destroyed** and the malformed file is overwritten | Nothing about the configuration at all. No warning identifies the overwritten contexts | Your contexts, before running `preview` on a machine that has any. Back the file up first |
| **Z31** | `updates add` when the copy of the artifact fails as it closes | **The failure is discarded and the command carries on** to the signing step with the copy as it stands. The copy is also written without truncating an existing file. **What the repository ends up holding is not established here**, because that is decided by the signing library rather than by Fleet | **Nothing** | The published artifact's size against the file you gave it, before hosts install it |
| **Z32** | `config get` with any number of arguments other than one | **Nothing was retrieved** | The subcommand's help text | As Z12. This is a second, separate condition, at a separate place, from the unknown-key case |
| **Z33** | `get mdm-commands --host` where you may not read the commands of one of the fleets involved | **Fleet removes the commands you were refused, records the refusal on its own side, and returns success.** If they were all refused, you are told none have been run | A short table with no marker. **The printed count is the count of the printed rows**, so the output is internally consistent and nothing in it records the removal | The same question as a global administrator, or the command results by identifier, which returns a permission error |
| **Z34** | `get mdm-command-results --id` **without** `--host`, where the command ran on hosts outside what your role can see | **Fleet loads every result, drops the ones whose host you may not see, and returns success.** It holds both the full set and the reduced one and compares neither. Where the filter removes all of them, it returns nothing at all | The results for the hosts you may see, with nothing marking the removal. Where none survive, **"No results received. Please check again later."**, which names the wrong cause: the results exist and are not yours to see | The same command with `--host`, host by host, which returns a permission error for inaccessible hosts. Or the same question as a global administrator |

<a id="the-shape-of-the-register-which-is-the-useful-part"></a>

### Patterns to handle in automation

Nine cases involve `generate-gitops`, including permission refusal. Review its generated tree before committing it, even after a zero exit.

Three cases involve `report` and two involve `trigger`. During an incident, verify returned results or recorded job runs before treating either command as successful.

Four involve discarded file-write or close errors: `debug archive`, `get carve`, `convert`, and `updates add`. The file may be usable, but the exit status cannot establish that. Inspect the output itself.

Add explicit result checks for host-facing workflows: `mdm run-command`, `run-script`, `apply --dry-run`, `delete -f`, and GitOps against Free all have cases in this register.

> ### Set a timeout for unattended reports
>
> Without `--timeout`, `fleetctl report` installs a deadline that never fires. A persistent results-connection read error can block progress updates, prevent completion checks from passing, and leave the command printing errors indefinitely. `--exit` depends on the same blocked values and does not resolve the wait.
>
> Pass `--timeout` in unattended runs. This is a known non-terminating path; the client-library review was not exhaustive.

<a id="why-the-register-is-a-floor"></a>

### Limits of the exit-zero review

Additional cases may exist inside helpers that discard failures, in server responses the client does not fully inspect, or in client-library branches outside the reviewed command paths. Finding `trigger` and `mdm run-command` behavior required comparing the server response with client handling, beyond text searches.

Absence from the register means no case was found during this review. It does not establish complete error propagation for that command.

## Destructive commands and the flags that widen them

![Troubleshooting](../_assets/icons/troubleshooting-light.svg) Review both the intended scope and the consequences of a mistaken context, host selection, or flag. These commands can make broad or irreversible changes without a confirmation prompt.

<a id="the-six-invocations-ranked"></a>

### Six invocations requiring close review

The table considers reversibility, number of affected objects, confirmation steps, result visibility, and recovery effort.

| Invocation | Why it is here |
|---|---|
| **`api -X DELETE <route>`** | Inherits the route's reach, including Fleet's batch routes. No allow-list, no confirmation, and no validation of what you named. On a non-2xx the body is discarded, so the one place Fleet would have explained itself is gone |
| **`mdm run-command --hosts <many> --payload <raw>`** | One payload, many devices. Fleet checks the payload's shape and refuses a malformed one, and **it does not check that the request type names a real command**. Result reporting is limited: a partial push failure is neither printed nor recorded |
| **`hosts transfer --status online --fleet X`** | A broad server-side selection. `--status online` moves every online host your role can see, which for a global administrator, maintainer or technician is every online host in the deployment. **The client prints no count, asks nothing, and the protocol carries no count to print**, so nothing records the prior assignment either |
| **`user delete-users --csv`** | Irreversible, bulk, no confirmation and no dry run, and it **stops at the first failure part-way through**, so you get a partial deletion and no record of how far it reached |
| **`mdm wipe --host`** | Irreversible, one host, one required flag, no prompt. What it leaves on the disk is the platform's answer rather than Fleet's |
| **`gitops --delete-other-fleets`** | On Premium, and not on a dry run, deletes the fleets not named in the run. A dry run exists and covers it, **and the flag defaults to on in the pipeline scaffold `fleetctl new` generates** ([6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md)) |

Check the selected context and targets before using any of these commands. A narrow-looking invocation can still affect the wrong host or deployment.

<a id="flags-that-widen-what-is-destroyed"></a>

### Flags that expand destructive changes

| Flag | On | What it widens |
|---|---|---|
| `--delete-other-fleets` (alias `--delete-other-teams`) | `gitops` | Deletes **the fleets not named in this run**, one at a time. Reaching a fleet that this run's own global file names as an Apple Business or App Store target **stops the run with an error rather than skipping that fleet**, so the deletions already made stand, and which fleets those are follows the order Fleet listed them in. The guard has additional scope requirements. It is assembled only on a Premium run that carries the global file alongside at least one other file, and not for the two-file case of a global file plus Unassigned. A single global file on its own, a global file with only Unassigned beside it, and a run with no global file at all each delete with no protection. Premium only, ignored without a word on Free, and **on by default in the generated pipeline scaffold** |
| `--force` | `apply` | Tells the server to apply past its own validation errors. Its usage text scopes this to organisation-settings and fleet specs |
| `--force` | `generate-gitops` | Overwrites a directory that is not empty |
| `--force`, `-f` | `new` | Writes the scaffold into an existing directory |
| `--flush` | `debug errors` | **Clears the stored errors after reading them and before the output file is written.** If that write then fails, the errors are gone |

<a id="flags-that-reach-more-hosts-than-their-name-suggests"></a>

### Host-selection flags

| Flag | On | What it reaches |
|---|---|---|
| `--status`, `--label`, `--search_query` | `hosts transfer` | A server-side filter. `--status online` moves every online host your role can see into the named fleet, which is every online host in the deployment for a global role, and no count is printed at any point. Where the selection reaches a fleet you may read but not move hosts out of, **the whole call fails and nothing moves** |
| `--fleet ''` | `hosts transfer` | The empty string is the way to move hosts to Unassigned, so an unset variable in a script is a valid destination |
| `--hosts` with `--labels` | `report` | The **union** of the two, not the intersection |
| `--hosts` as a list | `mdm run-command` | One payload to every host in the list, all or nothing on an unknown identifier |

<a id="flags-that-turn-a-check-or-a-warning-off"></a>

### Flags that change verification or output

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

`generate-gitops` is hidden, as are two GitOps concurrency flags and one preview-path override. They remain active despite being absent from help output.

<a id="where-the-client-prompts-and-where-it-does-not"></a>

### Interactive prompts

The reviewed client reads terminal input in ten places. Nine request credentials or names: login email and password, setup password and confirmation, user-create password and confirmation, organisation name in `new`, and update-repository passphrase and repeat. `user create --api-only` uses the tenth, a keystroke before displaying the API token; it skips that pause when stdin is not a terminal.

Those reads provide no destructive-action confirmation. `mdm wipe`, `hosts transfer`, `user delete-users`, `gitops --delete-other-fleets`, and `api` with DELETE have no `--yes` flag. Of those five, only GitOps offers a dry run.

The prompt review enumerated known terminal-input mechanisms. None appeared in those five command implementations; prompting through another mechanism has not been established.

## Choosing packaging options

![How-to](../_assets/icons/howto-light.svg) `fleetctl package` builds the installer that will configure your hosts. It downloads signed artifacts from Fleet’s update server but does not contact your Fleet deployment. Use `fleetctl package --help` for your client’s flags, then make the choices below before distributing the installer. Enrollment and updater workflows are covered in [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md), [3.4](../03-connect-devices/3.4-enroll-linux-devices.md), and [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md).

Choose the server address and secret, Fleet Desktop, script support, certificate verification, and package type.

**Server address and enroll secret.** Supply both or neither; supplying only one is refused. When neither is packaged, the host needs another source, such as an MDM-delivered configuration profile on macOS.

**Fleet Desktop.** `--fleet-desktop` adds the tray application with the failing-policy count and a link to the user’s device page.

**Scripts.** Linux wipe uses a script run by fleetd. A host installed without script support cannot perform `fleetctl mdm wipe`; the error identifies the missing agent capability.

**Certificate verification.** `--insecure` disables verification in the installed agent’s service configuration. A server setting or agent upgrade will not reverse it. Rebuild and reinstall to change it across hosts, or clear the local service setting with administrator rights and restart the agent. The local location differs by platform.

**Package type.** Available `--type` choices depend on the build platform. Windows builds one type; one option is Linux-only and another is available on Windows and macOS. Check the build machine’s supported options before planning cross-platform packaging.

Installer properties for an end user’s email and a licence-agreement token depend on the versions used to build the package. Later agent upgrades cannot add a property the installer omitted. Check the floors in [a.6](a.6-glossary-and-release-compatibility.md) and rebuild with a suitable client.

On `package`, `--debug` enables logging in the installed agent. The standard client debug flag instead logs request bodies to standard error on commands that declare it.

<a id="where-the-inventory-came-from-and-why-a-file-search-under-reports-it"></a>

## Inventory source and platform differences

![Explanation](../_assets/icons/explanation-light.svg) This inventory was read from the 4.90.0 source tag. The review did not have a verified 4.90.0 client binary to inspect. If your command tree differs, check the installed version and the assembly details below.

Four assembly details affect how the command tree is read from source:

The interactive query-shell command is registered at runtime, with its implementation supplied by the program embedding the client. An embedding without that implementation still displays the command but reports that support is not built in.

The update-repository family has five subcommands on macOS and Linux. Windows registers a single entry with no action or flags; its pre-action handler returns a message directing the user to Linux. Whether that handler runs before help handling belongs to the CLI framework and was not established in this review.

Every `get` subcommand receives two logging flags after declaration: `--enable-log-topics` and `--disable-log-topics`. They also appear on three other commands.

A shared helper builds three `debug` subcommands. Searching only direct declarations finds nine of the twelve.

<a id="the-counts-which-are-platform-specific"></a>

### Counts by platform

macOS and Linux have 77 named entries; Windows has 72. All platforms register 27 top-level names. The difference comes from the five update-repository leaves absent on Windows.

| | macOS and Linux | Windows |
|---|---|---|
| Top-level names | 27 | 27 |
| Leaf subcommands | 50 | 45 |
| **Named entries** | **77** | **72** |
| Behavioural rows in the index above | 69 | 65 |

Behavioral rows describe invocations that act, including those that return an error. On macOS/Linux, nineteen top-level commands act directly and eight contain subcommands. On Windows, `updates` becomes a directly failing invocation, giving twenty acting commands and seven containers. The index represents containers as headings.

Platform differences can also exist within a single command. `package` is registered everywhere, but its supported package types and options depend on the build platform.

<a id="two-enumerations-here-are-floors-rather-than-inventories"></a>

### Review coverage

Permission chains were traced from each command to the authorization decisions reached. Middleware, wrappers, or unvisited branches may add checks not identified here. The exit-zero register likewise records known cases rather than an exhaustive client-library audit.

Complete registration counts, such as the 27 top-level names, are distinguished from these open-ended reviews.

## Aliases, deprecated surfaces, and version notes

![Reference](../_assets/icons/reference-light.svg) Verified against Fleet 4.90.0. **Every deprecated surface below still works at this release**, and each is the older half of a rename this manual's [a.6](a.6-glossary-and-release-compatibility.md) covers in full.

A client/server version mismatch prints a warning and does not block the command. Compatibility problems may appear later in the request. Pin the client to the server release in automation ([6.4](../06-automate-fleet/6.4-use-fleetctl.md)).

`fleetctl --version` prints information compiled into the client. It does not contact or identify the selected server.

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

<a id="the-deprecation-notices-and-why-silencing-them-is-unreliable"></a>

### Deprecation logging

Fourteen of the nineteen client deprecation notices use the `deprecated-field-names` log topic. Five bypass it, including four on `apply` and `gitops`, so disabling that topic cannot silence every notice.

Topic availability and timing also matter:

The topic flags are declared only by `get`, `apply`, `gitops`, and `report`. Other commands reject `--disable-log-topics`. The gated notice on `generate mdm-apple-bm` has no topic flag in its invocation.

On `apply`, the deprecated-flag notice runs before the topic setting is applied. Thus `apply --policies-team X --disable-log-topics=deprecated-field-names` still prints it. GitOps, report, and get set the topic first.

`apply -f` supplies the shared specification parser with a notice writer; `delete -f` does not. The same legacy YAML can therefore produce warnings during apply and none during delete. An absence of delete warnings does not confirm current field names.

<a id="deprecated-forms-that-are-errors-rather-than-warnings"></a>

### Compatibility errors

These four cases fail rather than emitting only a warning:

- `gitops` refuses a repository holding both `no-team.yml` and `unassigned.yml` in one run.
- Specifying both a deprecated GitOps key and its replacement is fatal, for any of the 44 renamed key pairs.
- The Apple Business default-fleet key in a GitOps file is now fatal, and a legacy Apple Business configuration with no fleets defined is refused.
- Enabling the failing-policy webhook together with the policy list it replaced is refused.

### What to re-check after an upgrade

After upgrading, compare your required commands with `fleetctl <command> --help`. Recheck flags, aliases, deprecation output, and the exit-zero cases used by unattended workflows.
