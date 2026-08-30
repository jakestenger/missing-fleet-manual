---
title: "Configuration sources, scopes, and precedence"
chapter: "Appendices and indexes"
section: "A.3"
sidebar_position: 3
status: drafting
verified_against: Fleet 4.90.1
verified_on: 2026-08-29
verified_source: "drafted against fleet-v4.90.1 (dd0200f062) over three research rounds, then rebuilt against the same tag after independent review round 1 returned NOT READY. Every source, resolution and exception was read from the code that performs it, and every finding applied in that round was re-verified rather than taken on the reviewer's authority; where a claim rests on release history rather than the tag, the ledger says so. Citation ledger at research/section-notes/a.3-notes.md"
reviewed_by:
reviewed_on:
further_reading:
  - https://fleetdm.com/docs/configuration/fleet-server-configuration
feature_requests:
  labels: [":product"]
  match: ["configuration", "precedence", "agent options", "GitOps"]
  exclude: []
---

# Configuration sources, scopes, and precedence

**Fleet's configuration comes from several independently scoped authorities.** Correctness depends on knowing which one owns a value and what happens when two of them have an opinion, and neither question has a single answer.

## What this appendix carries

![Reference](../_assets/icons/reference.svg) The authorities, what each one owns, and how collisions resolve. That is the part nothing else collects.

**It does not enumerate settings or their defaults.** Fleet's own configuration reference does that, and copying it would be a liability rather than a service: this project has confirmed the reference and the server disagreeing in two different ways at this release, about what a default is and about whether a documented key is bound at all. The last section records the ones that change a decision.

**The boundary with [2.4](../02-administer-and-deploy-fleet/2.4-organization-and-server-settings.md)** is worth stating because the two are adjacent. If the question is *why, when, or how to choose* a particular setting, that is 2.4's. If it is *which source controls a class of values, or how competing sources resolve*, it is this appendix's.

## The authorities

![Reference](../_assets/icons/reference.svg) Three things get conflated and are worth separating before any table makes sense: **where a value is declared**, **where it is stored at runtime**, and **which interface can write it**. A source owns a runtime store. Something that only writes into another source's store is a writer, not an authority.

**On the server:**

| Source | Declared as | Stored | Read |
|---|---|---|---|
| **Command-line flags** | A flag on the process | Process memory | Once, at start |
| **Environment variables** | The upper-cased key | Process memory | Once, at start |
| **A configuration file** | YAML | Process memory | Once, at start |
| **Built-in defaults** | Nothing. They are the fallback | Process memory | On a miss |
| **Mounted secrets and secret-manager values** | The `_path` and `_bytes` forms, and the private-key reference | Process memory | Once. **Never re-read**, so changing the file under a running server does nothing |
| **Direct environment reads** | A variable the configuration manager never sees | Varies | Varies: at start, per request, per scheduled run, or inside a migration |
| **Organisation settings** | The organisation settings document, the interface, or the API | The database, cached about a second | Per request |
| **Fleet settings** | A fleet's settings block | The database, cached about a minute | Per request |
| **Agent options** | An `agent_options` block | **Inside the two rows above**, which is why they are constantly confused with them | Per host check-in |
| **Per-host stored control** | Nothing an administrator writes | A column on the host | Per agent poll |
| **The device-management asset store** | Nothing, once populated | The database, encrypted, with a deletion history | Per use |

**On the host**, a further seven. This is where the surprising resolutions live, because **Fleet reports almost nothing about them.** The one window it has is narrow: on each detail cycle it collects four resultant osquery flags, the distributed interval, the configuration refresh pair and the logger period. **Those tell you the value a host ended up with, never which of the seven produced it**, and nothing at all about the other settings.

| Source | Declared as | Stored | Read |
|---|---|---|---|
| **Compiled-in agent defaults** | Nothing. They are the fallback | The binary | On a miss |
| **The service definition** | A flag on the agent's command line, or its upper-cased environment form | The launch daemon's property list, the service defaults file, or the Windows service entry | Once, at start |
| **The agent's own root files** | The enroll secret file, the server URL file, the osquery flags file, the extensions list, the persisted server overrides | Files under the agent's root directory | At start, and each time a receiver runs |
| **The operating-system keystore** | Nothing an administrator writes directly | Keychain, or Credential Manager | At start, **and only as a fallback** |
| **The macOS configuration profile** | A profile delivered by whichever MDM manages the Mac | The device's profile state | In a loop at start, and every five minutes for one setting |
| **Direct agent environment reads** | A variable the agent reads itself. No flag form, no entry in its help output | The process environment | Varies |
| **Trailing osquery arguments** | Whatever follows the separator on the agent's own command line | The argument list handed to osquery | Every osquery start |

**The packager, the installer's properties, a host edit and Fleet's own delivery are writers into those rows rather than rows of their own.** That is worth stating for the server in particular: what Fleet delivers has no runtime storage on the host until a receiver writes it into one of the files above, which is why a host keeps obeying the last delivery after the server becomes unreachable.

> ### The last two rows are the ones nothing in Fleet will show you
>
> **Trailing arguments are placed after everything else, on every osquery start.** The agent assembles osquery's command line in a fixed order: its own generated flags, then the local osquery flags file, then the three settings it deliberately protects from that file, the host identifier, the database directory, and the extensions autoload list where one is configured. Anything after the separator is appended last, **and Fleet's own source states that it intends those to override every flag and flagfile entry before them.**
>
> **Whether they do is osquery's behaviour, and this appendix does not assert it.** How osquery resolves the same option supplied twice is settled inside osquery, not inside Fleet, and nothing in Fleet establishes it either way. **So treat a trailing argument as capable of displacing anything Fleet placed earlier, including the three settings Fleet fences off**, and confirm the result on the host rather than predicting it.
>
> **No package Fleet builds passes any.** The macOS launch daemon, the Linux service unit and the Windows service entry all invoke the agent with none, so this is reachable only by a host edit to the service definition. It is invisible from Fleet and it silently outranks everything configured on the server.
>
> **Direct environment reads have no flag, no help entry, and no server setting.** Two of them matter for support work. One suppresses enrollment failure messages from the agent's log entirely, so a host that cannot enroll looks quiet rather than broken. The other stops the agent deleting the temporary directory it creates for each script run, which is worth one investigation and then accumulates directories holding script bodies and their output for as long as it stays set. Fleet Desktop is configured this way in its entirety: it accepts `--version` and `--help` and nothing else, so **its configuration has no command-line surface**. The agent sets those variables itself when it launches the process, so they are an internal channel rather than something to tune.

### What the server can and cannot change on an installed host

![Reference](../_assets/icons/reference.svg) **The server hands the agent a fresh configuration document on every check-in, and the useful question is not how many settings it can change but which of them survive a restart.** Four groups, and they behave differently:

| What the server sends | What it changes, and what survives a restart |
|---|---|
| **The three update channels**, for the agent, for osquery and for Fleet Desktop | The agent's own settings, **and the only ones written down.** They go into a persisted overrides file and force an agent restart when they change. **This group is what outlives the server** |
| **The debug log level, and the script execution timeout** | The agent's own settings too, **held in memory and never written.** Both are lost on restart and re-applied at the next check-in, so they last as long as the server keeps asking for them. The debug level has a local floor: an agent started in debug can be raised by the server and cannot be lowered |
| **osquery startup flags, osquery extensions, the Nudge configuration** | Written into files in the agent's root directory, and these do survive a restart. **They configure the components the agent supervises rather than the agent itself** |
| **Twelve notifications** | Instructions to act now: rotate a disk encryption key, run a pending script, start the setup experience. **Not configuration at all** |

**So the three update channels are what the server *persists*, which is a narrower claim than what it changes.** The debug level and the script execution timeout are genuinely agent settings and genuinely server-controlled; they simply leave nothing on disk. Read a host's files to audit the first group, and expect the second to be invisible there.

Four further claims get run together, and separating them is what makes the boundary usable:

| | What is actually true |
|---|---|
| **The agent's command-line settings** | Twenty-nine of them. Twenty-eight also accept an environment variable, `--version` being the one that does not. **That is a statement about how you set them on the host**, not about the server reaching them |
| **The persisted override file** | Holds the three update channels the server last sent, plus two locally derived paths to the agent's helper binaries. **Those three are the whole of what the server writes down**, not the whole of what it controls |
| **`command_line_flags` in agent options** | Configures the child osquery process. **It belongs in the third group above**, because it never touches a setting of the agent's own |
| **Packaging environment inputs** | Twelve are accepted on the build host. Five are packaging and signing inputs rather than agent settings at all, and the other seven each have a runtime environment form as well, **so none of the twelve is available only at packaging time** |

**What to do with that.** Treat anything outside those four groups as host state: to change it across a fleet of machines you change it where the host reads it, through configuration management or a reinstall, and Fleet will not do it for you. The update channel is the exception that is persisted, and it has an exception of its own further down.

> ### The asset store outranks the server's own configuration, and only warns you
>
> The device-management asset store, the last row of the server table above, inverts the usual direction. **The material in it is not one class, and treating it as one is the mistake to avoid**: three kinds sit there and they arrive by three different routes.
>
> | Material | How it gets there |
> |---|---|
> | **The Apple push certificate and key, the Apple SCEP certificate and key, and the Apple Business Manager certificate, key and token** | Imported from the process configuration at first boot, **and after that the database is the authority** |
> | **The Apple SCEP enrollment challenge** | Imported the same way when you supply one, **and minted at random when you do not** |
> | **Android enterprise material, and Platform SSO signing material** | **Generated, never imported.** Android's comes into existence during the Google enterprise signup handshake, and Platform SSO's is minted the first time that feature is configured. Neither has a process-configuration form at all |
>
> **The conclusion is the same for all three and the reason is not.** For the first two the database wins because it is consulted first. For the third there is nothing for it to win against.
>
> **Fleet usually tells you and never stops you.** For the push certificate, the SCEP certificate and the Business Manager material, the startup log says it will ignore what the environment supplied. So an operator who rotates a certificate by editing a deployment manifest, restarts and sees no error has changed nothing, and the only evidence is a log line they had no reason to read. **Rotate through the interface or the API instead.**
>
> **The SCEP enrollment challenge is the one that says nothing at all.** Once a challenge is stored, the configured value is never read again and **no warning is logged on any ordinary boot**. An administrator who rotates that environment variable gets no feedback whatever that Fleet kept the old value.
>
> **Apple Business Manager breaks the pattern in the other direction, and the asymmetry is the useful part.** Its certificate, key and token are parsed *before* the database is consulted, so a broken path or a conflicting pair is **fatal at start for good**, even though the parsed value is then discarded in favour of the stored one. The push and SCEP certificates are the opposite: their files are read only when the database has nothing to offer. **So a moved Business Manager token file stops the server starting and a moved push certificate file does not.** Removing the Business Manager settings from the process configuration entirely is what lets the server boot from the stored token.

## Inputs that change the result without owning a value

![Explanation](../_assets/icons/explanation.svg) Several things shape what a device ends up with and are **not** authorities, and treating them as peers of the list above is the commonest way to reason wrongly about this.

| | What it does |
|---|---|
| **Labels, fleet placement, platform** | *Select* which hosts a value reaches. They do not compete for the value |
| **Licence** | **Three separate things, and only the first is selection.** See below |
| **Fleet secret variables, host attributes, identity-provider attributes** | *Substitute* into a value at delivery, changing what the device receives without authoring it |
| **The device platform, and any external management provider** | *Enforce*, or fail to. They hold actual state, not Fleet's desired state |
| **GitOps** | **A writer, not a source.** Your repository may be your organisation's declared authority; Fleet sees an ordinary client writing ordinary stored state |

> ### Licence is not only a selector, and the other two things it does are easy to miss
>
> **It selects**, in the ordinary way: a capability your tier does not include is refused, and the refusal is a licence error rather than a permission error ([a.4](a.4-roles-and-permissions-matrix.md)).
>
> **It can change which authority wins.** The transparency URL is read from the process configuration on Free and from the stored setting on Premium. **The same two values resolve in opposite directions on the two tiers**, so a value that appears to be ignored may be losing to an authority that only outranks it at your licence level.
>
> **It can reset stored configuration, and this one loses data.** On a Free server, saving organisation settings blanks the stored transparency URL and the alternative browser host, and blanks the device-management host name template if it holds anything. **The save does not have to touch those fields.** There is no error, no warning and no activity. So a deployment that drops from Premium to Free loses all three at the next unrelated settings edit, and upgrading again does not bring them back. If you are downgrading deliberately, record those three values first.

## How collisions resolve

![Reference](../_assets/icons/reference.svg) **There is no single precedence order, and expecting one is the mistake this section exists to prevent.** Six mechanisms were observed at this release. They are **not six classes a collision falls into**: they co-occur, and a single resolution path routinely uses three or four of them at once. Read the table as a vocabulary rather than a taxonomy.

| Mechanism | What happens |
|---|---|
| **Precedence** | The stronger source's value replaces the weaker one's |
| **Fallback** | The second source is consulted only when the first produced nothing |
| **Write-through** | The weaker source rewrites the stronger one's store, then deletes itself |
| **Composition** | Both values combine, by OR, by a floor, or by merge-if-absent |
| **Mutual exclusion** | Setting both is a fatal error. There is no winner |
| **Channel disabled** | One setting removes the channel by which the other would arrive, so no comparison ever happens |

**The last one is categorically different and worth its own sentence.** Nothing is compared and no value loses: the receiver is never registered, so the server's value never reaches the host at all.

**Within the server's process configuration the order is stable**, and it is the one place a simple rule holds. **Fleet states it itself**, in the help text of its own configuration dump: command-line flags, then environment variables, then the configuration file, then the built-in defaults.

> **What that statement does not settle is how an *empty* environment variable is treated, and this appendix declines to guess.** An earlier draft said an empty value is ignored, so that an orchestrator would have to remove a variable rather than blank it. That behaviour belongs to the configuration library, **which this release does not vendor**, and Fleet neither states it nor tests it. **Remove the variable rather than blanking it**, which is the safe action whichever way it resolves.

### Pairs that must not both be set

**Fleet loads and resolves the whole configuration first, then validates the result.** So these are checks on the resolved value rather than on where you set it, and supplying one half by flag and the other by environment variable collides exactly as if both sat in the file. **There is no winner and nothing is compared: the process refuses to start.**

**Per-key type and range checks are the exception, and they happen during the load**, so a value of the wrong type or an out-of-range TLS compatibility setting fails earlier than anything below.

| Pair | What happens |
|---|---|
| **A device-management certificate, key or token given both as a path and as inline content** | Startup fails, with a message naming the certificate, the key or the token. It covers the Apple push certificate and key, the Apple SCEP certificate and key, the Apple Business Manager certificate, key and server token, and the Windows device-management identity certificate and key |
| **`mysql.password` with `mysql.password_path`** | Startup fails. **The identical check runs on the read replica**, so `mysql_read_replica.password` with `mysql_read_replica.password_path` fails the same way, its message prefixed to say which of the two connections was at fault |
| **`server.private_key` with `server.private_key_arn`** | Startup fails **before Fleet makes any call to the secret manager**, which is deliberate: a misconfiguration should not cost a lookup. A key that resolves shorter than 32 bytes is a separate startup failure, checked after the fetch |
| **On the host, `--insecure` with `--fleet-certificate`** | The agent refuses to start, saying the two may not be specified together |
| **On the host, `--insecure` with `--update-tls-certificate`** | The same again, for the update server's certificate |

> **The two host-side rows bite hardest during a migration**, because `--insecure` is exactly what an operator reaches for when a certificate is the thing that is broken. Removing the certificate flag is the fix. Adding `--insecure` beside it stops the agent from starting at all.

> **Two things about the first row are worth knowing before you debug it.** The path and inline forms exist only for device-management material. The server's own TLS certificate and key have no inline form, so the rule never applies to them, and neither does it apply to the object-store or licence settings.
>
> **When the check runs depends on the family, and this is where a plausible simplification goes wrong.** For the push certificate and the SCEP certificate authority, the parse is skipped once the database holds **every** one of those assets, so a conflicting pair stops being reported after first boot. **Store only some of them and the parse still happens and the conflict is still fatal.**
>
> **Apple Business Manager and the Windows identity certificate never stop being checked.** Business Manager parses before it consults the database, and the Windows certificate is never stored as an asset at all, so **a conflicting pair in either of those is fatal on every boot, forever.** The asset store above is why the first two differ.

### Where several mechanisms meet

**Agent credentials use four mechanisms at once**, and they are worth setting out in full, because this is the only place in the agent where a remote authority overrides a locally supplied credential. There are two orders, selected by whether the agent was installed to read the macOS configuration profile.

**Without the profile the two credentials do not behave alike**, and assuming they do is the easy mistake:

| Credential | How it resolves |
|---|---|
| **The enroll secret** | **All four mechanisms.** Supplying both `--enroll-secret` and `--enroll-secret-path` is a fatal error at start, with no winner. A non-empty secret file has its contents written into the keystore and **the file is then deleted**, so the credential moves and the file you created disappears. The keystore is consulted only when nothing has been set by flag or environment. Otherwise: flag, then environment variable, then compiled default |
| **The server URL** | **One mechanism, and no more.** The flag, then `ORBIT_FLEET_URL`. **There is no compiled default**, so with neither set the value is simply empty, and there is no file, no keystore and no write-through. **Its local file is read only inside the profile branch below** |

**With the profile**, on macOS only, the two move together, and the keystore fallback above is skipped entirely:

| Step | What happens |
|---|---|
| The macOS configuration profile | **Sets both values unconditionally**, beating the flag and the environment, and writes both back to the agent's local files |
| Both values now present | The agent stops looking |
| Otherwise the local server URL file, then the local secret file, then the keystore | Consulted in that order. **Keystore errors here are logged rather than returned** |
| Still nothing | **The agent waits thirty seconds and repeats, indefinitely.** It does not exit |

> **The profile branch carries a comment describing a check the code does not make.** The comment says the profile applies only when neither value is already set. It applies regardless. **The behaviour is the profile winning**, and a reader who trusts the comment will predict the opposite. In practice, on a Mac installed this way, the enroll secret and server URL baked into the package are decorative, and whichever MDM manages the device decides both.
>
> **The last row is why a misconfigured Mac looks healthy.** The agent is running and retrying rather than failed, so a process check and a service status both pass while the host never appears in Fleet.

### The update channel exception, and why that file is not what it looks like

**Update channels combine write-through with a disabled channel, and then add an exception worth planning a rollout around.**

**At start**, the persisted overrides file overwrites both the flag and the environment for the three channels it holds. **At check-in**, the agent decides whether to rewrite that file by comparing what the server sent against *the file*, never against what the package was built with, and **an absent value on either side is read as `stable`.**

**So a move to `stable` can be dropped silently, and whether it is depends on the whole request rather than on the channel you were changing.** All three channels are compared together, absent values on either side count as `stable`, and Fleet Desktop drops out of the comparison entirely where Desktop is disabled. **The package's own channels never enter the comparison at all.**

**On a host with no override file, every channel reads as `stable` whatever the package was built with.** So a request that asks for `stable` on all enabled channels matches, nothing is written, nothing restarts, and the host carries on running `edge` from its package while Fleet shows the channel you asked for. **Asking for `stable` on several channels at once does not escape this**, because the tuple still matches.

**What does land is a request where at least one enabled channel asks for something other than `stable`.** The two sides then differ, the file is written with all three values, and **any `stable` in that same request takes effect alongside the value that triggered the write.**

**The rollout rule that follows**: an all-`stable` request against a host that has no override file is the case that quietly does nothing, however many channels it names. Mix in one non-`stable` channel and the whole request applies.

### Auditing the channels actually in force on a host

**The file is `server-overrides.json`, in the agent's root directory.** By default that directory is `/opt/orbit` on macOS and on Linux, and `C:\Program Files\Orbit` on Windows, following the system's own program-files location where that has been moved. **The root directory is itself overridable at install time**, by `--root-dir` or `ORBIT_ROOT_DIR`, so confirm it from the service definition before concluding that a file is missing.

**Then read the contents rather than the presence.** When the agent writes, it writes all three channels explicitly, whatever their values, alongside two fallback binary paths. **It never deletes or empties the file.**

| What you find | What it establishes |
|---|---|
| **No file** | No write has ever happened: either the server sent no channels at all, or everything it sent normalised to all-`stable`. **Either way the host runs whatever its package was built with**, which is the case the exception above hides |
| **A file** | A write happened at some point. **On its own that says nothing about the channels now in force** |
| **The three values inside it** | **The channels in force.** A file holding three `stable` values is the ordinary result of moving a host back to `stable`, and not evidence of anything wrong |
| **An empty value for a channel** | That channel is **not** overridden. It falls back to the flag or environment variable the host was installed with, each of which defaults to `stable` |

**So the audit is two steps: confirm the root directory, then read the three values.** Reasoning from whether the file exists will mislead you in both directions.

> **A second and simpler no-op sits in front of that one.** A server that sends no update channels at all, which is what an older Fleet does, is ignored before any comparison happens. Removing the key is therefore not a way to reset a host to its packaged channels.

> **Disabling updates removes the channel altogether.** The receiver that would ever write that file is never registered, while the file is still read at start. So **with updates disabled the last override written stays in force permanently and the server has no say at any point**, which is a larger effect than the exception above and a different one.

## Where the planes cross

![Reference](../_assets/icons/reference.svg) **Process configuration and stored configuration are mostly about different things, and the places they meet are the ones that waste an afternoon.** This section carries the meeting points this project has verified: **two values that resolve against each other**, and **two preconditions** where a process setting decides whether a stored value may be written at all.

> **Those are the known instances rather than a complete count, and the distinction is deliberate.** Establishing that *only* two values exist in both planes would mean comparing all 320 registered process keys against every field of the stored organisation settings, which is nineteen top-level blocks with substantial structure beneath them. **That comparison has not been done.** Treat the pair below as the ones to check first, not as a closed set.

### The two known to exist in both planes

| Setting | How it resolves |
|---|---|
| **The vulnerability database directory** | `vulnerabilities.databases_path` in the process configuration **beats** `vulnerability_settings.databases_path` in organisation settings, and the server logs an informational line saying that it did. **The process key ships with a non-empty default**, so on an otherwise untouched server the process value always wins and the stored setting never takes effect at all. Setting it in the interface and seeing nothing change is the expected outcome rather than a fault |
| **The transparency URL** | Three-way and licence-conditional: Fleet's built-in default, then the `partnerships.enable_secureframe` process setting, then the stored `fleet_desktop.transparency_url`, **which is read only on Premium**. So on Free the process configuration wins and the stored value is never consulted, and on Premium the stored value wins. **The same two values resolve in opposite directions on the two tiers** |

**The interface shows neither resolution.** It displays the stored value it accepted, and for the transparency URL that field reads back cleanly while never being consulted on Free. **Nothing in either surface names the authority that won**, so a value that looks saved and correct can be inert.

### Two preconditions, where the process plane gates a stored write

**These are not collisions.** A process setting decides whether a stored value can be written at all, so the failure arrives as a rejected write rather than as a losing value.

**Disk encryption requires the server private key.** Turning on `mdm.enable_disk_encryption`, from the interface, the API or GitOps, is rejected unless the server was started with `server.private_key` configured. **The requirement is not platform-specific**: this is the single organisation-wide toggle covering FileVault, BitLocker and Linux, so all three fail together. The same key gates uploading an Apple push certificate, saving secret variables and Apple account provisioning, so a deployment missing it fails a scattered set of operations that do not obviously belong together.

**Disk-encryption payloads inside custom profiles are refused unless a process setting allows them.** By default Fleet rejects a macOS profile carrying FileVault settings and a Windows profile targeting the BitLocker area, telling you to use the disk-encryption setting instead. Three process settings lift that restriction, two of them older names for the third, and **any one of them lifts it for both platforms at once.** There is no way to allow it for Apple and not for Windows.

> **This gates disk-encryption content within profiles, not custom profiles as a class.** Everything else you can put in a profile is unaffected by those three settings.

## Agent options resolve per consumer, not once

![Troubleshooting](../_assets/icons/troubleshooting.svg) **This is the single most consequential precedence question in Fleet, and it has more than one answer**, because more than one consumer reads the document.

**The osquery half** takes the fleet's document whole when the fleet has one, and the global document when it has none. **Never a mix.** So "a fleet with no options of its own falls back to global" is true when the fleet has no agent options at all, and false when the fleet has a document that omits a setting: the setting does not come from anywhere ([1.3](../01-foundations/1.3-hosts-fleets-labels.md)).

**Platform overrides replace rather than merge.** A platform override for a host's platform replaces the base configuration entirely, so it has to be complete.

**The Orbit half is a separate path with a different rule.** Update channels, command-line flags and extensions are read from the fleet's own document with **no fallback at all**, not even when the fleet has no document. Only the script execution timeout falls back, which Fleet's source states in words, and its condition tests for zero, so an explicit zero is indistinguishable from unset.

**Two settings compose rather than resolve.** The macOS profile may *enable* scripts and cannot disable a locally enabled value. And a locally set debug flag cannot be lowered by the server sending false: the local value is a floor.

### The per-host debug window is a merge, and it loses to an explicit value

**The window opens at enrollment and nowhere else.** At this release the only thing that stamps one is the agent option `orbit.debug_logging_on_enroll_duration`, applied to every host enrolling under that scope. **There is no host action and no endpoint that opens a window on demand**, so this is something you configure in advance for hosts that have yet to enroll, rather than something you switch on for a host you are already investigating.

**While a window is open, Fleet merges rather than replaces.** It takes the fleet's `command_line_flags`, adds `verbose` set to true **only when that key is absent**, and delivers the result. Everything else you set is preserved, which is the intent.

**So a fleet whose agent options explicitly set `verbose: false` gets half of what the window promises.** The explicit value survives the merge, so **osquery keeps running at its normal verbosity**. The agent's own log level is raised anyway, because the window carries a second and separate signal that is sent whenever the window is open, whatever the merge decided. **You get the agent's debug logging and not osquery's.**

**The window itself is visible, barely**: the host's record carries its expiry as `orbit_debug_until`, and **that field is returned by the single-host API and nowhere else**, so it is absent from the host list, from a CSV export and from the interface. **What nothing reports is that the osquery half of the merge lost**, so an escalation that collects agent logs and no osquery detail reads as a broken window rather than a working one with an explicit setting standing in front of it.

**Check the fleet's agent options in the same change that sets the enrollment duration**, and remove an explicit `verbose` rather than setting it to false where you want osquery's verbosity raised as well as the agent's.

### Absent and empty mean different things for osquery startup flags

**This is the distinction that decides whether a host keeps its locally maintained flag file**, and Fleet's own source states it in words rather than leaving it to be inferred:

| `command_line_flags` in agent options | What the agent does |
|---|---|
| **Absent** | **Leaves the host's osquery flags file untouched**, preserving whatever was packaged with the agent or written locally |
| **Explicitly empty**, as `{}` or `null` | **Clears the file** and restarts osquery without those flags |
| **Set to a value that differs from the file** | **Replaces the file wholesale** and restarts osquery |
| **Set to a value matching the file** | Nothing. Re-applying unchanged configuration causes no restart |

**Replacement is wholesale, so a hand-maintained flag file does not survive the first non-empty value**, comments included. It does not lose a merge, because there is no merge. **And clearing the key afterwards does not restore it**, because absent means "leave alone" rather than "undo": the file keeps whatever Fleet last wrote. If you maintain osquery flags locally, keep them in your packaging inputs, not only on the host ([8.11](../08-troubleshooting/8.11-reproducing-and-isolating.md)).

## What the two document writers do with what you leave out

![Reference](../_assets/icons/reference.svg) **Omission is not one behaviour, and the answer depends on the writer rather than on the field.** Fleet has two document writers with different contracts, and the GitOps client changes the question before either of them sees it. Read this before assuming a value you did not mention is safe.

### The organisation settings writer patches

**It reads the stored document, applies your body on top and writes the result.** Anything you omit keeps its stored value, so you never have to send the whole document to change one setting.

**Six things do not survive that patch anyway**, and they are worth knowing precisely because they defeat the rule above:

| What you omit or send | What the writer does |
|---|---|
| `mdm.ios_updates.update_new_hosts` and the iPadOS equivalent | Wiped back to unset on every save, whatever you send. **Only the macOS form of that setting is honoured** |
| The Windows Entra allowlists, **omitted or sent empty**, in a request that also turns Windows device management off | Both lists are emptied, with an activity for each identifier removed. **Send either list non-empty in that same request and the request is rejected instead**, saying the identifiers cannot be set while Windows device management is off. Nothing saves, and Windows device management does not turn off either |
| `mdm.windows_migration_enabled`, in that same request | Forced off unless you re-assert it explicitly |
| The Windows Entra client identifiers, when you do send them | Stored lower-cased and de-duplicated, so a read-back is not byte-identical to what you sent |
| `org_info.contact_url`, when the merged result is empty | Replaced with Fleet's own default |
| `server_settings.enable_analytics`, on a tier not permitted to disable it | Forced on |

**Four more settings are server-owned and silently ignored**: whether Apple device management is enabled and configured, whether Apple Business Manager is, whether Android is, and whether the Apple Business Manager terms have expired. Sending them is neither honoured nor rejected, because the stored value is put back over yours. **Fleet does that deliberately**, so that the output of reading the configuration can be fed straight back in as input without the round trip failing. **The cost is that a GitOps file declaring any of the four applies cleanly and changes nothing**, which is indistinguishable from success.

> **Windows device management enablement is not one of the four**, although it sits beside them and reads as though it should be. It is writable, and turning it on or off writes an activity.

**The licence reset above is a seventh**, and it fires on every Free-tier save.

### Four blocks are replaced wholesale, but only on request

**The organisation settings route takes an overwrite option**, and when it is set, **omitting the single sign-on block clears it**, along with the features block, the MDM end-user authentication block and Apple account provisioning. **Exactly those four.** The GitOps client is the only thing in Fleet that sets the option. `fleetctl apply` does not, and neither does the interface.

> **It is an ordinary request option, not a GitOps privilege.** Any caller who can write organisation settings can set it, so a script that reproduces what GitOps sends will also clear those four blocks by omitting them, and nothing in the response distinguishes the two behaviours.
>
> **One carve-out sits inside the replacement.** With the option set, an absent historical-data sub-key is defaulted back to *on* rather than to off, so a client that does not know those keys cannot silently stop collection and trigger a data scrub.

### The fleet spec writer patches, and then stops

**A direct write to the fleet spec route preserves most of what you omit**, sub-key by sub-key: the update settings for each platform, disk encryption, the BitLocker requirement, the recovery-lock password, `mdm.name_template`, the custom-settings lists on Windows and Android, scripts, software, secrets, host expiry, the webhooks and the integrations. `agent_options` has a three-state contract of its own: absent keeps it, an explicit null clears it, and a value replaces it whole.

**Five things break that pattern, and the first is large:**

| Field | On omission |
|---|---|
| **The whole `features` block** | **Replaced against Fleet's built-in defaults rather than merged.** Naming the block and omitting a sub-key reverts that sub-key too, so a partial `features` block silently resets what it does not mention |
| `setup_experience.enable_end_user_authentication` | Off |
| `setup_experience.lock_end_user_info` | Forced to follow the setting above, so with both omitted, off |
| `setup_experience.require_all_software_macos` | Off |
| `setup_experience.require_all_software_windows` | Off |

**Three of those four are plain booleans on the wire, which is exactly why they cannot tell absent from false**: end-user authentication and the two software requirements. Turn end-user authentication on in the interface, then apply a fleet spec that does not mention it, and it is off again, with no error and no warning.

**`lock_end_user_info` reaches the same result by a different route**, and the difference matters when you are trying to set it. It is an optional boolean that **can** tell absent from an explicit false. Set it explicitly and your value is kept. Omit it and Fleet deliberately makes it follow end-user authentication, preserving how it behaved before it was configurable at all. **So an explicit `false` is honoured here, where on the other three it is indistinguishable from silence.**

Three further setup-experience settings, whether to release the device manually, whether to create a local administrator account, and what type that account is, are defaulted only when the stored value was never explicitly set. **That is a migration default rather than a clobber**, and it fires once.

### Then the GitOps client changes the question

**The client supplies a value for every block it manages**, so a key absent from your YAML is rarely absent from the request the server receives. That is how "the API preserves omissions" and "GitOps clears things" are both true at once.

| Omitted from a GitOps file | Result |
|---|---|
| `yara_rules` | **Cleared.** The client sends an explicit empty list |
| `certificate_authorities` | **Cleared, by a route worth knowing.** The run queues a second pass that re-applies the empty grouping with deletion enabled, so the emptiness is acted on after the main apply rather than during it. Global files only, never a dry run, and a silent no-op on Free |
| `custom_host_vitals` | **Cleared** |
| `features`, `webhook_settings`, `integrations`, and most of the `mdm` and `controls` blocks | **Reset or cleared**, field by field |
| `agent_options` | **A hard error.** It is required in a global or named-fleet file |
| `conditional_access` | **Left alone** |

**Nine top-level organisation keys survive omission untouched**: organisation information, server settings, SMTP, host expiry, activity expiry, Fleet Desktop, the vulnerability settings, the GitOps block, and conditional access. [6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md) is the field-level account; this is the rule behind it.

## Reading the effective value, and what Fleet does not keep

![Troubleshooting](../_assets/icons/troubleshooting.svg) A precedence table nobody can apply to a live system is a description rather than a tool. This is where a reader with a value in front of them that is not what they set goes next.

| Plane | The stored intent | What is actually in force | Who changed it |
|---|---|---|---|
| **Server process** | A configuration dump, **which starts a new process** | **Partly.** The configuration API returns a live subset from the running server, named below. The rest goes unreported | Not retained |
| **Organisation settings** | The API or the interface | **Close, but not the same.** Reads are served from a cache held about a second | **By exception only.** See below |
| **Fleet settings** | The API or the interface | **Not the same.** A fleet's agent options, its features and its device-management configuration are cached about a minute each | An activity, for the changes Fleet names. The recorded file name is the only writer marker **stored on the settings row itself** |
| **Agent options** | The API | **Only the host knows.** Ask it | Recorded as an edit |
| **Host-local** | The host's own files | The host | Not retained |
| **Enforced on the device** | Fleet's desired state | The device's report | Per platform ([a.6](a.6-glossary-and-release-compatibility.md)) |

> **The server-process row is the one to read twice.** The configuration dump does not introspect the running server: it starts a fresh process and dumps what *that* process loads. So it can differ silently from what is in force after a configuration file or deployment definition has changed, and it omits every setting read directly from the environment rather than through the configuration manager.
>
> **What the running server does report is a real subset, and knowing its edges is the difference between a two-minute check and an afternoon.** The configuration API returns these **taken live from the running service rather than from the database**:
>
> | Section | What it actually covers |
> |---|---|
> | Update intervals | **Two keys only**, the osquery detail and policy update intervals. No cron, webhook or schedule interval appears |
> | Vulnerabilities | The full block, around ten keys including the database path and the feed URLs |
> | Logging | The debug and JSON flags, plus the resolved status, result and audit log destinations |
> | Email | **Only when the backend is Amazon SES.** Under the default SMTP backend the section is absent, and the SMTP settings you do see come from the database |
> | Sandbox, partnerships, licence | The sandbox flag; **one partnership key, and only when it is on**; and the licence as decoded claims rather than the configured key |
>
> **Two edges of that subset matter more than its contents.** The partnership setting that changes the transparency URL **is not the one exposed**, so the API cannot tell you why a transparency URL is not what you set. And **any authenticated user of any role can read all of it**, including a fleet-scoped observer, because the admin gate on that endpoint covers only the database-stored SMTP, single sign-on and agent-options fields.
>
> **So the accurate claim is that Fleet has no *complete* effective-configuration surface**, not that it has none. Around twenty of the 320 registered keys are visible this way. **For the rest, the only complete view belongs to whoever can run the configuration dump on the host itself**, and that view is a fresh load rather than the running server's.

> **Stored and in force differ by a cache on both settings planes, and the caches are per instance.** Each Fleet instance holds its own copy, so straight after a change two hosts checking in against two instances can legitimately be given different answers, for about a second on organisation settings and about a minute on a fleet's. **Your own read-back is not a fair test of this**, because the write path reads the stored document directly and bypasses the cache. Wait out the longer period before concluding a change did not apply ([1.6](../01-foundations/1.6-the-fleet-server.md)).
>
> **The device-management asset store behaves better and it is worth knowing why**, because it is the one place the obvious worry does not apply. Its cache key includes the asset's current checksum, and that checksum is read fresh on every lookup, so a rotated certificate is picked up on the next use rather than after an expiry. The stale copy merely lingers in memory until it ages out.

**Agent options are the plane where stored and in-force genuinely diverge**, and Fleet publishes no reconciliation. **Host-side, per-consumer observation is the only complete method**, and there is no single question that answers it: a live query reaches the osquery half, while update channels, extensions, debug state and script behaviour each need their own host file, process state or log.

**Fleet asks for a configuration hash it then throws away, and it asks only the hosts that run osquery.** The detail query selects the whole introspection row and keeps only the version, discarding the hash that would answer the question directly. **This is a mechanism of the osquery path rather than a universal one**, so hosts Fleet manages without osquery, iOS and iPadOS devices and Android devices among them, never contribute it at all and never could. Note too that it happens on a **detail cycle rather than on every poll**: Fleet skips detail queries until the detail interval comes round or a refetch forces them, so even where the evidence is collected and discarded, it is periodic rather than continuous.

### The audit trail is by exception

**Forty-two distinct activity types are reachable from a change to the organisation settings document.** That is a count of types rather than of changes, and the difference matters in both directions: agent options are a single type covering the whole block however much of it you edit, while the Entra identifier types fire once per identifier added or removed. Among the forty-two are disk encryption on and off, Windows device management, the minimum operating system versions, the Google Workspace integration, conditional access, the historical datasets and GitOps mode.

**Enrolment secrets are not one of them.** They are edited through their own route and write their own activity, and that activity appears only when the *set* of secret values actually changed, so re-submitting the same secrets in a different order writes nothing.

**Neither are the forty-two a partition of the feed, and the overlap is large: twenty of them are also emitted elsewhere.** The fleet writer emits the same types for the minimum operating system versions on all three Apple platforms, the macOS and Windows update settings, disk encryption on and off, recovery-lock passwords, conditional access, agent options and the historical datasets. The setup-experience authentication pair and the managed-local-account pair come from the Apple setup writer. The deleted organisation logo has its own endpoint. **So seeing one of those twenty establishes only that something changed somewhere, not that the organisation settings document is what changed.** The remaining twenty-two, among them the Windows device-management types, the Entra identifier types and the GitOps-mode types, are written on this path alone.

> **Disk encryption is the worst case and worth naming**, because it has several other emitters and they do not behave alike. The fleet writer and the Apple disk-encryption path each produce both halves, enabled and disabled. **Uploading an Apple push certificate produces only the enabled half**, and it produces one for the unassigned fleet and one for every fleet already enforcing encryption. **So a single certificate upload can fill the feed with enabled events for scopes nobody touched.** An activity saying disk encryption was enabled identifies neither the scope nor the writer.

**Three of the forty-two are best effort.** The deleted organisation logo, and both historical-dataset types, are written on a path that logs a failure and carries on, so the request can succeed with no activity behind it. **Absence of one of those three is not evidence that the change did not happen.** The other thirty-nine fail the request rather than lose the record.

**There is no activity for the document itself and no fallback.** Every write is guarded by a condition on its own block and there is no catch-all branch anywhere on the path, so a change to a part with no dedicated type writes nothing at all. Changing SMTP settings, the server URL or the host expiry window leaves no entry. **The feed is silent rather than incomplete**, which is worse, because nothing indicates a settings change happened. Read it as a list of the changes Fleet names, not as an audit log of the document ([1.5](../01-foundations/1.5-audit-and-activity.md)).

## What the device says back, and what Fleet keeps of it

![Explanation](../_assets/icons/explanation.svg) The last row of the table above is the one Fleet controls least, because the value in force is the device's and Fleet only holds a report of it. **The reports are not equivalent across platforms**, and treating them as one thing is how a dashboard comes to be trusted for something it cannot know.

**Fleet uses one vocabulary of per-profile states across all three platforms**, which is exactly what makes them look interchangeable: `pending`, `verifying`, `verified` and `failed`. **Which of them a profile can reach depends on its class as much as on its platform**, so read the row for the thing you are actually shipping rather than the row for the operating system.

| Platform and class | How it reaches `verified`, and what happens after |
|---|---|
| **macOS, ordinary profile** | An acknowledgement moves it to `verifying`. **A routine inventory check, hourly by default, moves it to `verified` once it sees the profile installed.** Should the profile later leave the device, the same check notices, Fleet re-pushes up to three times, and only then marks it `failed`, with a detail recording that it had previously been confirmed |
| **iOS and iPadOS, ordinary profile** | **An install acknowledgement goes straight to `verified`**, skipping `verifying`, because there is no agent on the device to look. A device answering that it is busy stays `pending` |
| **Any Apple platform, declarative profile** | The device's own status report drives it, and **an active and valid report records `verified` directly**, so the normal path skips `verifying` here too |
| **Windows, ordinary profile** | **A successful response maps directly to `verified`**, and nothing re-checks it afterwards. An empty response is `pending`; anything else becomes `failed` after one retry |
| **Windows, profile whose certificate Fleet brokered** | **Deliberately held at `verifying` despite a successful response**, and moved to `verified` only once the issued certificate appears in the host's certificate inventory. **So Windows does reach all four states**, in this class |
| **Android, any profile** | `pending` before delivery, then `verified` or `failed` once Google reports back. **Nothing sets `verifying` on this platform** |
| **A third-party management provider** | Only what the device itself reports, through ordinary inventory. Fleet holds no channel to the other provider, so this is observation rather than knowledge |

> ### `verified` carries different weight in each row, and only one row is ever revisited
>
> **On macOS it means Fleet looked, and it keeps looking.** A profile removed on the device is caught within about an hour and eventually fails. **macOS is the one case where `verified` is not a final answer**, which also makes it the only one that will report drift back to you.
>
> **On iOS, iPadOS and ordinary Windows profiles it means the device said yes once.** Nothing revisits it, so a profile removed afterwards keeps reading `verified` indefinitely.
>
> **A `verified` count is therefore not comparable across platforms**, and the macOS figure is the conservative one by construction. Where the difference matters, confirm on the device ([8.9](../08-troubleshooting/8.9-windows-mdm-diagnostics.md)).

> ### Which Windows profiles are the exception, stated narrowly
>
> **It is not "profiles that contain a certificate".** The exception applies where **Fleet itself brokered the certificate request** for that host and that profile, through a custom SCEP proxy, NDES or Smallstep. **DigiCert is excluded by design.** A profile you wrote that installs a certificate some other way is an ordinary profile and jumps straight to `verified`.
>
> **In this class `failed` is not final either.** Where the certificate turns up later, the profile heals back to `verified` on its own.

**Two removal behaviours are worth carrying**, because they explain result lists that otherwise look wrong. **Windows counts several not-found responses as a successful removal**, on the reasoning that a profile which is not there has been removed. **And a successful Apple removal deletes the record rather than setting a state**, so the profile leaves the host's list instead of coming to rest at `verified`.

**What Apple and Windows genuinely have in common is narrower than it looks: neither has a separate acceptance tier for an external policy provider.** Fleet is the management authority for both, so no third party sits between Fleet's intent and the device's report whose acceptance could be recorded. **That is the correct observation, and it is not the same as saying acceptance and enforcement are one report**, which holds for Windows and fails for macOS.

### Android retains four things and publishes one of them

**Fleet exposes derived per-profile progress for Android through the ordinary configuration-profile API**, in the same shape as the other platforms, so a device part-way through *is* distinguishable from one that has not started. What is retained internally and never published is a different and more interesting list:

| Retained | Exposed through an API |
|---|---|
| The profile you authored | **Yes** |
| The policy payload Fleet actually sent to Google, after merging | **No** |
| Google's response to that submission, and the policy version it assigned | **No** |
| The version the device reports as applied, and when it last synchronised | **No** |

**Android is the only platform where Fleet holds a provider's acceptance separately from the device's report**, because Google is a genuine third party in the path. Both are stored and neither is published, so **the question "did Google accept this, and is the device simply behind?" has an answer Fleet keeps and no interface will show you.** Reading it means going to the database ([8.10](../08-troubleshooting/8.10-android-diagnostics.md)).

### Two collision rules at the device boundary

**Android merges a host's *eligible* profiles into a single policy, and a collision costs you a profile.** Eligible is doing real work in that sentence: **a profile whose network configuration references a certificate that has not yet reached a terminal state**, verified or finally failed, **is withheld from the merge entirely**, held at `pending`, and re-sent once the certificate resolves either way, since a finally failed certificate releases it too. **The reason is written into the profile's detail**, which says it is waiting for the named certificate to be installed, and that detail is the only thing distinguishing it from an ordinary pending profile. Withheld profiles never reach the collision rule.

The rest are sorted **by name, alphabetically**, and merged in that order, so **where two of them set the same top-level field, the alphabetically later name wins.** The loser is not silently overridden: **it is marked `failed`**, with a message naming the fields it lost. Two consequences follow that are easy to miss. Renaming a profile can change which one wins. And adding a profile can fail an existing one that was working yesterday.

**Windows refuses a custom profile that collides with Fleet's own operating-system update settings.** Where a fleet or the organisation has Windows updates configured through settings, uploading a profile that targets the same area is rejected with a message saying operating-system updates are already configured. **The gate has three parts**: managing updates by profile is Premium-only, the settings must be clear, and a second profile targeting that area is rejected even when they are. Turn the settings off first if you intend to manage updates by profile.

> ### What Fleet keeps about an Apple push, and who gets told when one fails
>
> **The command is written to its queue before the push goes out.** So an enqueued command is a durable record that exists whether or not the push succeeded, and it is visible as pending. **The push response itself is not stored.**
>
> **Whether a failed push reaches you depends entirely on what asked for it.** Every sending path reports the failure upwards; the caller decides what to do with it, and the split is clean enough to predict:
>
> | Who asked | What a failed push does |
> |---|---|
> | **You, through a control on a host**: lock, unlock, wipe, clear passcode, the refetch button | **You are told**, as a gateway error, and no success activity is written. **The command is queued regardless and the device will obey it at its next check-in**, so the host reads as not locked in Fleet while being locked in reality |
> | **A background job**: profile delivery, scheduled refetch, declarative sync, device rename, the retry cron | **Nothing is reported.** The failure counts as success, on the deliberate reasoning that the command is already queued. A profile in this state stays `pending` rather than turning `failed` |
> | **The two automatic rotation jobs**: recovery lock, managed local account password | **Nothing is reported, and the activity is written anyway**, recording the rotation as though it had reached the device |
> | **Running a command against many hosts at once** | **Partly.** You get an error only where the push failed for every target. Otherwise the response succeeds and names the hosts it could not reach |
>
> **Locking a Mac carries an exception inside that first row.** Where a second request wins the race to enqueue the lock command, Fleet sends the push for the command that won, and **if that push fails it logs the failure, returns the PIN and reports success.** The success activity is written on top. So the ordinary lock path tells you about a failed push, the raced path does not, and **the two are indistinguishable from outside.**
>
> **One class of push response does change stored state, and it is caller-scoped too.** When Apple reports a device token as inactive, Fleet turns device management off for that host and fails its pending app installs. **That happens only during the scheduled iPhone and iPad refresh.** The same dead token during a lock, a wipe, profile delivery or the manual refetch button produces nothing at all, and **Macs are never covered**, because that job enumerates only iPhones and iPads.
>
> **So what a pending command tells you is narrower than it looks.** It establishes that the command exists and the device has not answered. **It does not separate a push that failed from a push that succeeded and a device that has not checked in**, and in both cases the remedy is the same: wait for the check-in, or prompt one ([8.8](../08-troubleshooting/8.8-apple-mdm-diagnostics.md)).

## Where Fleet's reference and the running server disagree

![Reference](../_assets/icons/reference.svg) Verified at this release, and listed because each one changes a decision or a diagnosis rather than to keep score.

| Setting | The reference says | The server does |
|---|---|---|
| A per-endpoint request-size override | Documents it in full, with a default and a worked example | **The key does not exist.** Setting it does nothing and reports nothing |
| The Redis host-cache lifetime | 60 seconds | 180 seconds |
| The MySQL password default | `fleet` | Empty |
| The private-key external identifier | Names an environment variable without the middle component | That variable is not read. The documented form is silently ignored |

**Read per-key defaults out of Fleet's reference with that in mind**, and confirm anything you are about to depend on rather than trusting the published default. **How you confirm it depends on the plane, and one of the two is only partly confirmable:**

| Plane | How to establish the value in force |
|---|---|
| **Stored settings**, organisation and fleet | **Read it back**, allowing for the cache periods above. The API returns what the server stored, so a difference from what you sent is real and worth investigating |
| **Server process configuration** | **Partly.** For the live subset the configuration API reports, named above, read the running value back and trust it. **For everything else there is no read-back**: the configuration dump starts a fresh process and reports what *that* invocation would load, which need not match what the running server holds, and it omits every setting read directly from the environment. **Control the input instead**: pin the deployment definition, keep one source of truth for it, and treat a restart as the only thing that changes it |

**Outside that subset the discipline is to make the input auditable, because Fleet gives you no way to observe the output.** That is the most consequential limitation in this appendix, and it is why the reference disagreements above matter more than their number suggests: for a key the configuration API does not return, a wrong published default is not something you can catch by looking at the running server.

## Version notes

![Reference](../_assets/icons/reference.svg) Verified against Fleet 4.90.1. The server's configuration manager registers **320 distinct keys** at this release.

**This appendix deliberately publishes no count of how many of those Fleet documents.** An earlier draft did, and the comparison was withdrawn because "documented" had not been defined consistently enough for the number to mean anything: a setting can have its own reference section, be described in prose under another, or appear only in an example. **The count of registered keys is derived and stated; the comparison is not, until it can be produced reproducibly.**
