---
title: "Configuration sources, scopes, and precedence"
chapter: "Appendices and indexes"
section: "A.3"
sidebar_position: 3
verified_against: Fleet 4.90.0
verified_on: 2026-08-29
verified_source: "drafted against fleet-v4.90.0 (7c428c6e46) over three research rounds, then rebuilt against the same tag after independent review round 1 returned NOT READY. Every source, resolution and exception was read from the code that performs it, and every finding applied in that round was re-verified rather than taken on the reviewer's authority; where a claim rests on release history rather than the tag, the ledger says so. Citation ledger at research/section-notes/a.3-notes.md"
further_reading:
  - https://fleetdm.com/docs/configuration/fleet-server-configuration
feature_requests:
  labels: [":product"]
  match: ["configuration", "precedence", "agent options", "GitOps"]
  exclude: []
---

# Configuration sources, scopes, and precedence

The same-looking Fleet setting can come from the server, organization settings, a fleet, or the host. When two sources disagree, the winner depends on the setting. Use this appendix to find the owner and the precedence rule.

## What this appendix carries

![Reference](../_assets/icons/reference.svg) The authorities, what each one owns, and the known rules for how collisions resolve. That is the part nothing else collects. Where a comparison has not been carried out in full, this appendix says so rather than implying a settled order.

**It explains what nearly every setting is for, in the binary's own words rather than copied prose.** The full catalog carries each key's registered usage string (the same one-line description `fleet serve --help` prints), read mechanically from the server binary rather than transcribed from Fleet's hand-maintained reference: this project has confirmed the reference and the server disagreeing in two different ways at this release, about what a default is and about whether a documented key is bound at all. A usage string names what a setting does, not when or why you'd change it; for that, see [2.7](../02-administer-and-deploy-fleet/2.7-organization-and-server-settings.md). The disagreements that change a decision are called out first; the full catalog, keys and their usage strings both generated rather than copied, closes the appendix.

**The boundary with [2.7](../02-administer-and-deploy-fleet/2.7-organization-and-server-settings.md)** is worth stating because the two are adjacent. If the question is *why, when, or how to choose* a particular setting, that is 2.7's. If it is *which source controls a class of values, or how competing sources resolve*, it is this appendix's.

## The authorities

![Reference](../_assets/icons/reference.svg) Do not memorize the authority tables. When a value seems ignored, ask three questions in order: where was it declared, where is the live value stored, and which interface wrote that store? A source owns a runtime store. Something that only writes into another source's store is a writer, not an authority.

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

> **What that statement does not settle is how an *empty* environment variable is treated, and this appendix declines to guess.** Whether an empty value is treated as ignored, so that an orchestrator would have to remove a variable rather than blank it, is a property of the configuration library, **which this release does not vendor**, and Fleet neither states it nor tests it. **Remove the variable rather than blanking it**, which is the safe action whichever way it resolves.

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
| `features`, `webhook_settings`, `integrations`, and most of the `mdm` block | **Reset or cleared**, field by field |
| `controls` | **Named-fleet omission resets it.** Across the global and unassigned files exactly one must define it: setting both is an error, setting neither is an error, and the unassigned file's controls are applied to the global scope when the global file omits them |
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

Agent options are the plane where stored and in-force genuinely diverge, and Fleet publishes no reconciliation. Reading what is in force means observing each consumer on the host, and no single question answers it: a live query reaches the osquery half, while update channels, extensions, debug state and script behaviour each need their own host file, process state or log.

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
| The "secret key" for invite and reset tokens (`app.token_key`, default `CHANGEME`) | A secret that those tokens are generated from | **Never reads the key.** Invite and reset tokens are random text sized by `token_key_size`, so setting `token_key` changes nothing and its `CHANGEME` default is inert |
| The invite-token validity period | Its usage text ends "i.e. 1h" | Registers a five-day (`120h`) default. The "1h" is stale and contradicts the default the same key registers, which the catalog below shows correctly as `120h` |
| The session validity period (`session.duration`) | Its usage text ends "i.e. 4h" | Registers the same five-day (`120h`) default. The "4h" is stale in exactly the same way, so a login lasts five days rather than four hours unless you shorten it, which matters because it sets how long a stolen session stays valid |

**Read per-key defaults out of Fleet's reference with that in mind**, and confirm anything you are about to depend on rather than trusting the published default. **How you confirm it depends on the plane, and one of the two is only partly confirmable:**

| Plane | How to establish the value in force |
|---|---|
| **Stored settings**, organisation and fleet | **Read it back**, allowing for the cache periods above. The API returns what the server stored, so a difference from what you sent is real and worth investigating |
| **Server process configuration** | **Partly.** For the live subset the configuration API reports, named above, read the running value back and trust it. **For everything else there is no read-back**: the configuration dump starts a fresh process and reports what *that* invocation would load, which need not match what the running server holds, and it omits every setting read directly from the environment. **Control the input instead**: pin the deployment definition, keep one source of truth for it, and treat a restart as the only thing that changes it |

**Outside that subset the discipline is to make the input auditable, because Fleet gives you no way to observe the output.** That is the most consequential limitation in this appendix, and it is why the reference disagreements above matter more than their number suggests: for a key the configuration API does not return, a wrong published default is not something you can catch by looking at the running server.

## Version notes

![Reference](../_assets/icons/reference.svg) Verified against Fleet 4.90.0. The server's configuration manager registers **320 distinct keys** at this release.

**This appendix deliberately publishes no count of how many of those Fleet documents.** "Documented" is not defined consistently enough for that comparison to mean anything: a setting can have its own reference section, be described in prose under another, or appear only in an example. **The count of registered keys is derived and stated; the comparison is not, until it can be produced reproducibly.**

## The complete configuration-key catalog

![Reference](../_assets/icons/reference.svg) This table is generated rather than written. It is read directly from the registration calls the server binary makes as it starts, at the release this book is pinned to, so it records the keys the server actually binds and the defaults it registers rather than what any document says it binds. That is what makes it authoritative: where this catalog and Fleet's published configuration reference disagree, the catalog is right, because it is the code path the running server takes.

The disagreements named under [Where Fleet's reference and the running server disagree](#where-fleets-reference-and-the-running-server-disagree) are all visible in it, which is the proof that generating it matters. The reference gives the Redis host-cache lifetime as 60 seconds; `redis.host_cache_ttl` below registers 180. The reference gives `mysql.password` a default of `fleet`; below it is empty. And the per-endpoint request-size override the reference documents in full is absent from this table altogether, which is how a generated catalog says the server binds no such key: a key that is not a row here is one the binary never registers, whatever the documentation shows.

Read the columns as the key, the environment variable that sets it, the type, the default the server registers, and what it's for. A key marked *(hidden)* is bound and functional but kept out of `fleet serve --help`. A default marked *(computed)* is derived when the server starts rather than being a fixed literal, so the cell shows the value it resolves to, which for a few paths is relative to a directory the operating system chooses at runtime.

The "what it's for" cell is that key's own registered usage string; it is blank for the one key (`server.tls_compatibility`) whose usage argument is built with `fmt.Sprintf` rather than a plain string the generator can read, and that gap is the generator's, not a claim the server carries no description. Every one of the 320 registered keys is listed here; none is omitted. The source location of each registration sits in an HTML comment on its row, for an editor checking the work, and not in the reader's way.

<!-- To regenerate: python3 build/gen-config-catalog.py --out FILE  (FLEET_SRC overrides the source checkout). Pinned to fleet-v4.90.0 (7c428c6e46). -->
<!-- GENERATED by build/gen-config-catalog.py; do not edit by hand.
     source: server/config/config.go @ 7c428c6e467d4dd642b0375350eecca7138746d1
     registration calls found: 302; keys parsed: 320 (of which 5 computed defaults); unparsed: 0; duplicate keys: 0 -->

| Key | Environment variable | Type | Registered default | What it's for |
|---|---|---|---|---|
| `mysql.protocol` | `FLEET_MYSQL_PROTOCOL` | string | `"tcp"` | MySQL server communication protocol (tcp,unix,...). <!-- server/config/config.go:1301; via addMysqlConfig("mysql", "localhost:3306", ".") -->|
| `mysql.address` | `FLEET_MYSQL_ADDRESS` | string | `"localhost:3306"` | MySQL server address (host:port). <!-- server/config/config.go:1303; via addMysqlConfig("mysql", "localhost:3306", ".") -->|
| `mysql.username` | `FLEET_MYSQL_USERNAME` | string | `"fleet"` | MySQL server username. <!-- server/config/config.go:1305; via addMysqlConfig("mysql", "localhost:3306", ".") -->|
| `mysql.password` | `FLEET_MYSQL_PASSWORD` | string | `""` | MySQL server password (prefer env variable for security). <!-- server/config/config.go:1307; via addMysqlConfig("mysql", "localhost:3306", ".") -->|
| `mysql.password_path` | `FLEET_MYSQL_PASSWORD_PATH` | string | `""` | Path to file containg MySQL server password. <!-- server/config/config.go:1309; via addMysqlConfig("mysql", "localhost:3306", ".") -->|
| `mysql.database` | `FLEET_MYSQL_DATABASE` | string | `"fleet"` | MySQL database name. <!-- server/config/config.go:1311; via addMysqlConfig("mysql", "localhost:3306", ".") -->|
| `mysql.tls_cert` | `FLEET_MYSQL_TLS_CERT` | string | `""` | MySQL TLS client certificate path. <!-- server/config/config.go:1313; via addMysqlConfig("mysql", "localhost:3306", ".") -->|
| `mysql.tls_key` | `FLEET_MYSQL_TLS_KEY` | string | `""` | MySQL TLS client key path. <!-- server/config/config.go:1315; via addMysqlConfig("mysql", "localhost:3306", ".") -->|
| `mysql.tls_ca` | `FLEET_MYSQL_TLS_CA` | string | `""` | MySQL TLS server CA. <!-- server/config/config.go:1317; via addMysqlConfig("mysql", "localhost:3306", ".") -->|
| `mysql.tls_server_name` | `FLEET_MYSQL_TLS_SERVER_NAME` | string | `""` | MySQL TLS server name. <!-- server/config/config.go:1319; via addMysqlConfig("mysql", "localhost:3306", ".") -->|
| `mysql.tls_config` | `FLEET_MYSQL_TLS_CONFIG` | string | `""` | MySQL TLS config value. Use skip-verify, true, false or custom key. <!-- server/config/config.go:1321; via addMysqlConfig("mysql", "localhost:3306", ".") -->|
| `mysql.max_open_conns` | `FLEET_MYSQL_MAX_OPEN_CONNS` | int | `50` | MySQL maximum open connection handles. <!-- server/config/config.go:1323; via addMysqlConfig("mysql", "localhost:3306", ".") -->|
| `mysql.max_idle_conns` | `FLEET_MYSQL_MAX_IDLE_CONNS` | int | `50` | MySQL maximum idle connection handles. <!-- server/config/config.go:1324; via addMysqlConfig("mysql", "localhost:3306", ".") -->|
| `mysql.conn_max_lifetime` | `FLEET_MYSQL_CONN_MAX_LIFETIME` | int | `0` | MySQL maximum amount of time a connection may be reused. <!-- server/config/config.go:1325; via addMysqlConfig("mysql", "localhost:3306", ".") -->|
| `mysql.sql_mode` | `FLEET_MYSQL_SQL_MODE` | string | `""` | MySQL sql_mode. <!-- server/config/config.go:1326; via addMysqlConfig("mysql", "localhost:3306", ".") -->|
| `mysql.region` | `FLEET_MYSQL_REGION` | string | `""` | RDS region for AWS authentication. <!-- server/config/config.go:1327; via addMysqlConfig("mysql", "localhost:3306", ".") -->|
| `mysql.sts_assume_role_arn` | `FLEET_MYSQL_STS_ASSUME_ROLE_ARN` | string | `""` | ARN of role to assume for AWS authentication. <!-- server/config/config.go:1328; via addMysqlConfig("mysql", "localhost:3306", ".") -->|
| `mysql.sts_external_id` | `FLEET_MYSQL_STS_EXTERNAL_ID` | string | `""` | Optional unique identifier that can be used by the principal assuming the role to assert its identity. <!-- server/config/config.go:1329; via addMysqlConfig("mysql", "localhost:3306", ".") -->|
| `mysql_read_replica.protocol` | `FLEET_MYSQL_READ_REPLICA_PROTOCOL` | string | `"tcp"` | MySQL server communication protocol (tcp,unix,...) for the read replica. <!-- server/config/config.go:1301; via addMysqlConfig("mysql_read_replica", "", " for the read replica.") -->|
| `mysql_read_replica.address` | `FLEET_MYSQL_READ_REPLICA_ADDRESS` | string | `""` | MySQL server address (host:port) for the read replica. <!-- server/config/config.go:1303; via addMysqlConfig("mysql_read_replica", "", " for the read replica.") -->|
| `mysql_read_replica.username` | `FLEET_MYSQL_READ_REPLICA_USERNAME` | string | `"fleet"` | MySQL server username for the read replica. <!-- server/config/config.go:1305; via addMysqlConfig("mysql_read_replica", "", " for the read replica.") -->|
| `mysql_read_replica.password` | `FLEET_MYSQL_READ_REPLICA_PASSWORD` | string | `""` | MySQL server password (prefer env variable for security) for the read replica. <!-- server/config/config.go:1307; via addMysqlConfig("mysql_read_replica", "", " for the read replica.") -->|
| `mysql_read_replica.password_path` | `FLEET_MYSQL_READ_REPLICA_PASSWORD_PATH` | string | `""` | Path to file containg MySQL server password for the read replica. <!-- server/config/config.go:1309; via addMysqlConfig("mysql_read_replica", "", " for the read replica.") -->|
| `mysql_read_replica.database` | `FLEET_MYSQL_READ_REPLICA_DATABASE` | string | `"fleet"` | MySQL database name for the read replica. <!-- server/config/config.go:1311; via addMysqlConfig("mysql_read_replica", "", " for the read replica.") -->|
| `mysql_read_replica.tls_cert` | `FLEET_MYSQL_READ_REPLICA_TLS_CERT` | string | `""` | MySQL TLS client certificate path for the read replica. <!-- server/config/config.go:1313; via addMysqlConfig("mysql_read_replica", "", " for the read replica.") -->|
| `mysql_read_replica.tls_key` | `FLEET_MYSQL_READ_REPLICA_TLS_KEY` | string | `""` | MySQL TLS client key path for the read replica. <!-- server/config/config.go:1315; via addMysqlConfig("mysql_read_replica", "", " for the read replica.") -->|
| `mysql_read_replica.tls_ca` | `FLEET_MYSQL_READ_REPLICA_TLS_CA` | string | `""` | MySQL TLS server CA for the read replica. <!-- server/config/config.go:1317; via addMysqlConfig("mysql_read_replica", "", " for the read replica.") -->|
| `mysql_read_replica.tls_server_name` | `FLEET_MYSQL_READ_REPLICA_TLS_SERVER_NAME` | string | `""` | MySQL TLS server name for the read replica. <!-- server/config/config.go:1319; via addMysqlConfig("mysql_read_replica", "", " for the read replica.") -->|
| `mysql_read_replica.tls_config` | `FLEET_MYSQL_READ_REPLICA_TLS_CONFIG` | string | `""` | MySQL TLS config value for the read replica. Use skip-verify, true, false or custom key. <!-- server/config/config.go:1321; via addMysqlConfig("mysql_read_replica", "", " for the read replica.") -->|
| `mysql_read_replica.max_open_conns` | `FLEET_MYSQL_READ_REPLICA_MAX_OPEN_CONNS` | int | `50` | MySQL maximum open connection handles for the read replica. <!-- server/config/config.go:1323; via addMysqlConfig("mysql_read_replica", "", " for the read replica.") -->|
| `mysql_read_replica.max_idle_conns` | `FLEET_MYSQL_READ_REPLICA_MAX_IDLE_CONNS` | int | `50` | MySQL maximum idle connection handles for the read replica. <!-- server/config/config.go:1324; via addMysqlConfig("mysql_read_replica", "", " for the read replica.") -->|
| `mysql_read_replica.conn_max_lifetime` | `FLEET_MYSQL_READ_REPLICA_CONN_MAX_LIFETIME` | int | `0` | MySQL maximum amount of time a connection may be reused for the read replica. <!-- server/config/config.go:1325; via addMysqlConfig("mysql_read_replica", "", " for the read replica.") -->|
| `mysql_read_replica.sql_mode` | `FLEET_MYSQL_READ_REPLICA_SQL_MODE` | string | `""` | MySQL sql_mode for the read replica. <!-- server/config/config.go:1326; via addMysqlConfig("mysql_read_replica", "", " for the read replica.") -->|
| `mysql_read_replica.region` | `FLEET_MYSQL_READ_REPLICA_REGION` | string | `""` | RDS region for AWS authentication for the read replica. <!-- server/config/config.go:1327; via addMysqlConfig("mysql_read_replica", "", " for the read replica.") -->|
| `mysql_read_replica.sts_assume_role_arn` | `FLEET_MYSQL_READ_REPLICA_STS_ASSUME_ROLE_ARN` | string | `""` | ARN of role to assume for AWS authentication for the read replica. <!-- server/config/config.go:1328; via addMysqlConfig("mysql_read_replica", "", " for the read replica.") -->|
| `mysql_read_replica.sts_external_id` | `FLEET_MYSQL_READ_REPLICA_STS_EXTERNAL_ID` | string | `""` | Optional unique identifier that can be used by the principal assuming the role to assert its identity for the read replica. <!-- server/config/config.go:1329; via addMysqlConfig("mysql_read_replica", "", " for the read replica.") -->|
| `redis.address` | `FLEET_REDIS_ADDRESS` | string | `"localhost:6379"` | Redis server address (host:port) <!-- server/config/config.go:1336 -->|
| `redis.username` | `FLEET_REDIS_USERNAME` | string | `""` | Redis server username <!-- server/config/config.go:1338 -->|
| `redis.password` | `FLEET_REDIS_PASSWORD` | string | `""` | Redis server password (prefer env variable for security) <!-- server/config/config.go:1340 -->|
| `redis.cache_name` | `FLEET_REDIS_CACHE_NAME` | string | `""` | Redis server Elasticache cache name <!-- server/config/config.go:1342 -->|
| `redis.region` | `FLEET_REDIS_REGION` | string | `""` | Redis server Elasticache region <!-- server/config/config.go:1344 -->|
| `redis.database` | `FLEET_REDIS_DATABASE` | int | `0` | Redis server database number <!-- server/config/config.go:1346 -->|
| `redis.use_tls` | `FLEET_REDIS_USE_TLS` | bool | `false` | Redis server enable TLS <!-- server/config/config.go:1348 -->|
| `redis.duplicate_results` | `FLEET_REDIS_DUPLICATE_RESULTS` | bool | `false` | Duplicate Live Query results to another Redis channel <!-- server/config/config.go:1349 -->|
| `redis.connect_timeout` | `FLEET_REDIS_CONNECT_TIMEOUT` | duration | `5s` | Timeout at connection time <!-- server/config/config.go:1350 -->|
| `redis.keep_alive` | `FLEET_REDIS_KEEP_ALIVE` | duration | `10s` | Interval between keep alive probes <!-- server/config/config.go:1351 -->|
| `redis.connect_retry_attempts` | `FLEET_REDIS_CONNECT_RETRY_ATTEMPTS` | int | `0` | Number of attempts to retry a failed connection <!-- server/config/config.go:1352 -->|
| `redis.cluster_follow_redirections` | `FLEET_REDIS_CLUSTER_FOLLOW_REDIRECTIONS` | bool | `true` | Automatically follow Redis Cluster redirections <!-- server/config/config.go:1353 -->|
| `redis.cluster_read_from_replica` | `FLEET_REDIS_CLUSTER_READ_FROM_REPLICA` | bool | `false` | Prefer reading from a replica when possible (for Redis Cluster) <!-- server/config/config.go:1354 -->|
| `redis.tls_cert` | `FLEET_REDIS_TLS_CERT` | string | `""` | Redis TLS client certificate path <!-- server/config/config.go:1355 -->|
| `redis.tls_key` | `FLEET_REDIS_TLS_KEY` | string | `""` | Redis TLS client key path <!-- server/config/config.go:1356 -->|
| `redis.tls_ca` | `FLEET_REDIS_TLS_CA` | string | `""` | Redis TLS server CA <!-- server/config/config.go:1357 -->|
| `redis.tls_server_name` | `FLEET_REDIS_TLS_SERVER_NAME` | string | `""` | Redis TLS server name <!-- server/config/config.go:1358 -->|
| `redis.tls_handshake_timeout` | `FLEET_REDIS_TLS_HANDSHAKE_TIMEOUT` | duration | `10s` | Redis TLS handshake timeout <!-- server/config/config.go:1359 -->|
| `redis.max_idle_conns` | `FLEET_REDIS_MAX_IDLE_CONNS` | int | `3` | Redis maximum idle connections <!-- server/config/config.go:1360 -->|
| `redis.max_open_conns` | `FLEET_REDIS_MAX_OPEN_CONNS` | int | `0` | Redis maximum open connections, 0 means no limit <!-- server/config/config.go:1361 -->|
| `redis.conn_max_lifetime` | `FLEET_REDIS_CONN_MAX_LIFETIME` | duration | `0s` | Redis maximum amount of time a connection may be reused, 0 means no limit <!-- server/config/config.go:1362 -->|
| `redis.idle_timeout` | `FLEET_REDIS_IDLE_TIMEOUT` | duration | `240s` | Redis maximum amount of time a connection may stay idle, 0 means no limit <!-- server/config/config.go:1363 -->|
| `redis.conn_wait_timeout` | `FLEET_REDIS_CONN_WAIT_TIMEOUT` | duration | `0s` | Redis maximum amount of time to wait for a connection if the maximum is reached (0 for no wait) <!-- server/config/config.go:1364 -->|
| `redis.write_timeout` | `FLEET_REDIS_WRITE_TIMEOUT` | duration | `10s` | Redis maximum amount of time to wait for a write (send) on a connection <!-- server/config/config.go:1365 -->|
| `redis.read_timeout` | `FLEET_REDIS_READ_TIMEOUT` | duration | `10s` | Redis maximum amount of time to wait for a read (receive) on a connection <!-- server/config/config.go:1366 -->|
| `redis.sts_assume_role_arn` | `FLEET_REDIS_STS_ASSUME_ROLE_ARN` | string | `""` | ARN of role to assume for AWS authentication <!-- server/config/config.go:1367 -->|
| `redis.sts_external_id` | `FLEET_REDIS_STS_EXTERNAL_ID` | string | `""` | Optional unique identifier that can be used by the principal assuming the role to assert its identity <!-- server/config/config.go:1368 -->|
| `redis.host_cache_enabled` | `FLEET_REDIS_HOST_CACHE_ENABLED` | bool | `true` | Enable Redis-backed cache for host lookups on the osquery and orbit auth paths. Disable to bypass the cache and serve every check-in from MySQL. <!-- server/config/config.go:1369 -->|
| `redis.host_cache_ttl` | `FLEET_REDIS_HOST_CACHE_TTL` | duration | `180s` | Base TTL for Redis-backed host lookup cache entries. Actual per-entry TTL is jittered by ±10% to avoid synchronized expiry waves. Must be > 0 when redis.host_cache_enabled is true; set redis.host_cache_enabled=false to disable the cache. <!-- server/config/config.go:1372 -->|
| `redis.live_query_small_target_threshold` | `FLEET_REDIS_LIVE_QUERY_SMALL_TARGET_THRESHOLD` | int | `1000` | Maximum number of targeted hosts for a live query to use the per-host reverse index instead of a fleet-wide bitfield, avoiding one GETBIT per query on every host check-in. Set to 0 to disable the reverse index and use the bitfield for all live queries. <!-- server/config/config.go:1376 -->|
| `server.address` | `FLEET_SERVER_ADDRESS` | string | `"0.0.0.0:8080"` | Fleet server address (host:port) <!-- server/config/config.go:1382 -->|
| `server.cert` | `FLEET_SERVER_CERT` | string | `"./tools/osquery/fleet.crt"` | Fleet TLS certificate path <!-- server/config/config.go:1384 -->|
| `server.key` | `FLEET_SERVER_KEY` | string | `"./tools/osquery/fleet.key"` | Fleet TLS key path <!-- server/config/config.go:1386 -->|
| `server.tls` | `FLEET_SERVER_TLS` | bool | `true` | Enable TLS (required for osqueryd communication) <!-- server/config/config.go:1388 -->|
| `server.tls_compatibility` | `FLEET_SERVER_TLS_COMPATIBILITY` | string | `"intermediate"` |  <!-- server/config/config.go:1390 -->|
| `server.url_prefix` | `FLEET_SERVER_URL_PREFIX` | string | `""` | URL prefix used on server and frontend endpoints <!-- server/config/config.go:1393 -->|
| `server.keepalive` | `FLEET_SERVER_KEEPALIVE` | bool | `true` | Controls whether HTTP keep-alives are enabled. <!-- server/config/config.go:1395 -->|
| `server.sandbox_enabled` *(hidden)* | `FLEET_SERVER_SANDBOX_ENABLED` | bool | `false` | When enabled, Fleet limits some features for the Sandbox <!-- server/config/config.go:1397 -->|
| `server.websockets_allow_unsafe_origin` | `FLEET_SERVER_WEBSOCKETS_ALLOW_UNSAFE_ORIGIN` | bool | `false` | Disable checking the origin header on websocket connections, this is sometimes necessary when proxies rewrite origin headers between the client and the Fleet webserver <!-- server/config/config.go:1399 -->|
| `server.frequent_cleanups_enabled` | `FLEET_SERVER_FREQUENT_CLEANUPS_ENABLED` | bool | `false` | Enable frequent cleanups of expired data (15 minute interval) <!-- server/config/config.go:1400 -->|
| `server.force_h2c` | `FLEET_SERVER_FORCE_H2C` | bool | `false` | Force the fleet server to use HTTP2 cleartext aka h2c (ignored if using TLS) <!-- server/config/config.go:1401 -->|
| `server.private_key` | `FLEET_SERVER_PRIVATE_KEY` | string | `""` | Used for encrypting sensitive data, such as MDM certificates. <!-- server/config/config.go:1402 -->|
| `server.private_key_region` | `FLEET_SERVER_PRIVATE_KEY_REGION` | string | `""` | AWS region of the Secrets Manager secret containing server private key <!-- server/config/config.go:1403 -->|
| `server.private_key_arn` | `FLEET_SERVER_PRIVATE_KEY_ARN` | string | `""` | ARN of AWS Secrets Manager secret containing server private key <!-- server/config/config.go:1404 -->|
| `server.private_key_sts_assume_role_arn` | `FLEET_SERVER_PRIVATE_KEY_STS_ASSUME_ROLE_ARN` | string | `""` | ARN of role to assume for accessing private key secret <!-- server/config/config.go:1405 -->|
| `server.private_key_sts_external_id` | `FLEET_SERVER_PRIVATE_KEY_STS_EXTERNAL_ID` | string | `""` | External ID for STS role assumption when accessing private key secret <!-- server/config/config.go:1406 -->|
| `server.vpp_verify_timeout` | `FLEET_SERVER_VPP_VERIFY_TIMEOUT` | duration | `10m` | Maximum amount of time to wait for VPP app install verification <!-- server/config/config.go:1407 -->|
| `server.vpp_verify_request_delay` | `FLEET_SERVER_VPP_VERIFY_REQUEST_DELAY` | duration | `5s` | Delay in between requests to verify VPP app installs <!-- server/config/config.go:1408 -->|
| `server.cleanup_dist_targets_age` | `FLEET_SERVER_CLEANUP_DIST_TARGETS_AGE` | duration | `24h` | Specifies the cleanup age for completed live query distributed targets. <!-- server/config/config.go:1409 -->|
| `server.max_installer_size` | `FLEET_SERVER_MAX_INSTALLER_SIZE` | bytes | `10 GiB` *(computed)* | Maximum size in bytes for software installer uploads (e.g. 10GiB, 500MB, 1G) <!-- server/config/config.go:1410; expr installersize.Human(installersize.MaxSoftwareInstallerSize) -->|
| `server.trusted_proxies` | `FLEET_SERVER_TRUSTED_PROXIES` | string | `""` | Trusted proxy configuration for client IP extraction: 'none' (RemoteAddr only), a header name (e.g., 'True-Client-IP'), a hop count (e.g., '2'), or comma-separated IP/CIDR ranges <!-- server/config/config.go:1411 -->|
| `server.gzip_responses` | `FLEET_SERVER_GZIP_RESPONSES` | bool | `false` | Enable gzip-compressed responses for supported clients <!-- server/config/config.go:1413 -->|
| `server.allow_private_network_integrations` | `FLEET_SERVER_ALLOW_PRIVATE_NETWORK_INTEGRATIONS` | bool | `false` | Allow integration HTTP requests to private network addresses (RFC 1918). Loopback and cloud metadata addresses are always blocked regardless of this setting. <!-- server/config/config.go:1414 -->|
| `server.bypass_network_blocking` | `FLEET_SERVER_BYPASS_NETWORK_BLOCKING` | bool | `false` | Disable all outbound network blocking protections for integration HTTP requests (loopback, cloud metadata, and private network addresses). Only intended for environments where egress is already constrained by external infrastructure (e.g. an egress proxy or firewall) that Fleet's own checks would otherwise conflict with. This is an infrastructure-level setting and cannot be changed at runtime. <!-- server/config/config.go:1415 -->|
| `server.default_max_request_body_size` | `FLEET_SERVER_DEFAULT_MAX_REQUEST_BODY_SIZE` | bytes | `1 MiB` *(computed)* | Default maximum size in bytes for request bodies, certain endpoints will have higher limits (e.g. 10MiB, 500KB, 1G) <!-- server/config/config.go:1416; expr installersize.Human(platform_http.MaxRequestBodySize) -->|
| `auth.bcrypt_cost` | `FLEET_AUTH_BCRYPT_COST` | int | `12` | Bcrypt iterations <!-- server/config/config.go:1422 -->|
| `auth.salt_key_size` | `FLEET_AUTH_SALT_KEY_SIZE` | int | `24` | Size of salt for passwords <!-- server/config/config.go:1424 -->|
| `auth.sso_session_validity_period` | `FLEET_AUTH_SSO_SESSION_VALIDITY_PERIOD` | duration | `15m` | Timeout from SSO start to SSO callback <!-- server/config/config.go:1426 -->|
| `auth.require_http_message_signature` | `FLEET_AUTH_REQUIRE_HTTP_MESSAGE_SIGNATURE` | bool | `false` | Require HTTP message signatures for fleetd requests (Premium feature) <!-- server/config/config.go:1428 -->|
| `auth.sso_rate_limit_per_minute` | `FLEET_AUTH_SSO_RATE_LIMIT_PER_MINUTE` | int | `0` | Number of allowed requests per minute to the SSO callback endpoint (default uses the login rate limit value in a dedicated bucket) <!-- server/config/config.go:1430 -->|
| `app.token_key` | `FLEET_APP_TOKEN_KEY` | string | `"CHANGEME"` | Secret key for generating invite and reset tokens <!-- server/config/config.go:1434 -->|
| `app.invite_token_validity_period` | `FLEET_APP_INVITE_TOKEN_VALIDITY_PERIOD` | duration | `120h` | Duration invite tokens remain valid (i.e. 1h) <!-- server/config/config.go:1436 -->|
| `app.token_key_size` | `FLEET_APP_TOKEN_KEY_SIZE` | int | `24` | Size of generated tokens <!-- server/config/config.go:1438 -->|
| `app.enable_scheduled_query_stats` | `FLEET_APP_ENABLE_SCHEDULED_QUERY_STATS` | bool | `true` | If true (default) it gets scheduled query stats from hosts <!-- server/config/config.go:1440 -->|
| `session.key_size` | `FLEET_SESSION_KEY_SIZE` | int | `64` | Size of generated session keys <!-- server/config/config.go:1444 -->|
| `session.duration` | `FLEET_SESSION_DURATION` | duration | `120h` | Duration session keys remain valid (i.e. 4h) <!-- server/config/config.go:1446 -->|
| `osquery.node_key_size` | `FLEET_OSQUERY_NODE_KEY_SIZE` | int | `24` | Size of generated osqueryd node keys <!-- server/config/config.go:1450 -->|
| `osquery.host_identifier` | `FLEET_OSQUERY_HOST_IDENTIFIER` | string | `"provided"` | Identifier used to uniquely determine osquery clients <!-- server/config/config.go:1452 -->|
| `osquery.enroll_cooldown` | `FLEET_OSQUERY_ENROLL_COOLDOWN` | duration | `0s` | Cooldown period for duplicate host enrollment (default off) <!-- server/config/config.go:1454 -->|
| `osquery.status_log_plugin` | `FLEET_OSQUERY_STATUS_LOG_PLUGIN` | string | `"filesystem"` | Log plugin to use for status logs <!-- server/config/config.go:1456 -->|
| `osquery.result_log_plugin` | `FLEET_OSQUERY_RESULT_LOG_PLUGIN` | string | `"filesystem"` | Log plugin to use for result logs <!-- server/config/config.go:1458 -->|
| `osquery.label_update_interval` | `FLEET_OSQUERY_LABEL_UPDATE_INTERVAL` | duration | `1h` | Interval to update host label membership (i.e. 1h) <!-- server/config/config.go:1460 -->|
| `osquery.policy_update_interval` | `FLEET_OSQUERY_POLICY_UPDATE_INTERVAL` | duration | `1h` | Interval to update host policy membership (i.e. 1h) <!-- server/config/config.go:1462 -->|
| `osquery.detail_update_interval` | `FLEET_OSQUERY_DETAIL_UPDATE_INTERVAL` | duration | `1h` | Interval to update host details (i.e. 1h) <!-- server/config/config.go:1464 -->|
| `osquery.status_log_file` | `FLEET_OSQUERY_STATUS_LOG_FILE` | string | `""` | (DEPRECATED: Use filesystem.status_log_file) Path for osqueryd status logs <!-- server/config/config.go:1466 -->|
| `osquery.result_log_file` | `FLEET_OSQUERY_RESULT_LOG_FILE` | string | `""` | (DEPRECATED: Use filesystem.result_log_file) Path for osqueryd result logs <!-- server/config/config.go:1468 -->|
| `osquery.enable_log_rotation` | `FLEET_OSQUERY_ENABLE_LOG_ROTATION` | bool | `false` | (DEPRECATED: Use filesystem.enable_log_rotation) Enable automatic rotation for osquery log files <!-- server/config/config.go:1470 -->|
| `osquery.max_jitter_percent` | `FLEET_OSQUERY_MAX_JITTER_PERCENT` | int | `10` | Maximum percentage of the interval to add as jitter <!-- server/config/config.go:1472 -->|
| `osquery.enable_async_host_processing` | `FLEET_OSQUERY_ENABLE_ASYNC_HOST_PROCESSING` | string | `"false"` | Enable asynchronous processing of host-reported query results (either 'true'/'false' or set per task, e.g., 'label_membership=true&policy_membership=true') <!-- server/config/config.go:1474 -->|
| `osquery.async_host_collect_interval` | `FLEET_OSQUERY_ASYNC_HOST_COLLECT_INTERVAL` | string | `"30s"` | Interval to collect asynchronous host-reported query results (e.g. '30s' or set per task 'label_membership=10s&policy_membership=1m') <!-- server/config/config.go:1476 -->|
| `osquery.async_host_collect_max_jitter_percent` | `FLEET_OSQUERY_ASYNC_HOST_COLLECT_MAX_JITTER_PERCENT` | int | `10` | Maximum percentage of the interval to collect asynchronous host results <!-- server/config/config.go:1478 -->|
| `osquery.async_host_collect_lock_timeout` | `FLEET_OSQUERY_ASYNC_HOST_COLLECT_LOCK_TIMEOUT` | string | `"1m0s"` | Timeout of the exclusive lock held during async host collection (e.g., '30s' or set per task 'label_membership=10s&policy_membership=1m' <!-- server/config/config.go:1480 -->|
| `osquery.async_host_collect_log_stats_interval` | `FLEET_OSQUERY_ASYNC_HOST_COLLECT_LOG_STATS_INTERVAL` | duration | `1m` | Interval at which async host collection statistics are logged (0 disables logging of stats) <!-- server/config/config.go:1482 -->|
| `osquery.async_host_insert_batch` | `FLEET_OSQUERY_ASYNC_HOST_INSERT_BATCH` | int | `2000` | Batch size for async collection inserts in mysql <!-- server/config/config.go:1484 -->|
| `osquery.async_host_delete_batch` | `FLEET_OSQUERY_ASYNC_HOST_DELETE_BATCH` | int | `2000` | Batch size for async collection deletes in mysql <!-- server/config/config.go:1486 -->|
| `osquery.async_host_update_batch` | `FLEET_OSQUERY_ASYNC_HOST_UPDATE_BATCH` | int | `1000` | Batch size for async collection updates in mysql <!-- server/config/config.go:1488 -->|
| `osquery.async_host_redis_pop_count` | `FLEET_OSQUERY_ASYNC_HOST_REDIS_POP_COUNT` | int | `1000` | Batch size to pop items from redis in async collection <!-- server/config/config.go:1490 -->|
| `osquery.async_host_redis_scan_keys_count` | `FLEET_OSQUERY_ASYNC_HOST_REDIS_SCAN_KEYS_COUNT` | int | `1000` | Batch size to scan redis keys in async collection <!-- server/config/config.go:1492 -->|
| `osquery.min_software_last_opened_at_diff` | `FLEET_OSQUERY_MIN_SOFTWARE_LAST_OPENED_AT_DIFF` | duration | `2m` | Minimum time difference of the software's last opened timestamp (compared to the last one saved) to trigger an update to the database <!-- server/config/config.go:1494 -->|
| `osquery.max_log_write_body_size` | `FLEET_OSQUERY_MAX_LOG_WRITE_BODY_SIZE` | bytes | `"0"` | Maximum body size for the osquery/log endpoint (e.g. 10MiB, 500KB). 0 means use the built-in default (10MiB). Only applied when osquery.allow_body_auth_fallback is true. In header-auth mode (false) the route is not subject to any body size limit; this value is ignored. <!-- server/config/config.go:1496 -->|
| `osquery.max_distributed_write_body_size` | `FLEET_OSQUERY_MAX_DISTRIBUTED_WRITE_BODY_SIZE` | bytes | `"0"` | Maximum body size for the osquery/distributed/write endpoint (e.g. 10MiB, 500KB). 0 means use the built-in default (5MiB). Only applied when osquery.allow_body_auth_fallback is true. In header-auth mode (false) the route is not subject to any body size limit; this value is ignored. <!-- server/config/config.go:1498 -->|
| `osquery.allow_body_auth_fallback` | `FLEET_OSQUERY_ALLOW_BODY_AUTH_FALLBACK` | bool | `true` | Selects how host-authenticated osquery requests are authenticated. When true (default), only body-based node_key is used for authentication. When false, the nodey_key header is required for authentication and the body's node_key is ignored; pre-auth rejects absent/invalid headers before the body is read. <!-- server/config/config.go:1500 -->|
| `activity.enable_audit_log` | `FLEET_ACTIVITY_ENABLE_AUDIT_LOG` | bool | `false` | Enable audit logs <!-- server/config/config.go:1504 -->|
| `activity.audit_log_plugin` | `FLEET_ACTIVITY_AUDIT_LOG_PLUGIN` | string | `"filesystem"` | Log plugin to use for audit logs <!-- server/config/config.go:1506 -->|
| `logging.debug` | `FLEET_LOGGING_DEBUG` | bool | `false` | Enable debug logging <!-- server/config/config.go:1510 -->|
| `logging.json` | `FLEET_LOGGING_JSON` | bool | `false` | Log in JSON format <!-- server/config/config.go:1512 -->|
| `logging.disable_banner` | `FLEET_LOGGING_DISABLE_BANNER` | bool | `false` | Disable startup banner <!-- server/config/config.go:1514 -->|
| `logging.error_retention_period` | `FLEET_LOGGING_ERROR_RETENTION_PERIOD` | duration | `24h` | Amount of time to keep errors, 0 means no expiration, < 0 means disable storage of errors <!-- server/config/config.go:1516 -->|
| `logging.tracing_enabled` | `FLEET_LOGGING_TRACING_ENABLED` | bool | `false` | Enable Tracing, further configured via standard env variables <!-- server/config/config.go:1518 -->|
| `logging.tracing_type` | `FLEET_LOGGING_TRACING_TYPE` | string | `""` | Select the kind of tracing, defaults to OpenTelemetry, can also be elasticapm <!-- server/config/config.go:1520 -->|
| `logging.otel_logs_enabled` | `FLEET_LOGGING_OTEL_LOGS_ENABLED` | bool | `false` | Enable exporting logs to an OpenTelemetry collector (requires tracing_enabled) <!-- server/config/config.go:1522 -->|
| `logging.enable_topics` | `FLEET_LOGGING_ENABLE_TOPICS` | string | `""` | Comma-separated log topics to enable (overrides code defaults) <!-- server/config/config.go:1524 -->|
| `logging.disable_topics` | `FLEET_LOGGING_DISABLE_TOPICS` | string | `""` | Comma-separated log topics to disable (overrides code defaults) <!-- server/config/config.go:1526 -->|
| `email.backend` | `FLEET_EMAIL_BACKEND` | string | `""` | Provide the email backend type, acceptable values are currently \"ses\" and \"default\" or empty string which will default to SMTP <!-- server/config/config.go:1530 -->|
| `ses.region` | `FLEET_SES_REGION` | string | `""` | AWS Region to use <!-- server/config/config.go:1533 -->|
| `ses.endpoint_url` | `FLEET_SES_ENDPOINT_URL` | string | `""` | AWS Service Endpoint to use (leave empty for default service endpoints) <!-- server/config/config.go:1534 -->|
| `ses.access_key_id` | `FLEET_SES_ACCESS_KEY_ID` | string | `""` | Access Key ID for AWS authentication <!-- server/config/config.go:1535 -->|
| `ses.secret_access_key` | `FLEET_SES_SECRET_ACCESS_KEY` | string | `""` | Secret Access Key for AWS authentication <!-- server/config/config.go:1536 -->|
| `ses.sts_assume_role_arn` | `FLEET_SES_STS_ASSUME_ROLE_ARN` | string | `""` | ARN of role to assume for AWS <!-- server/config/config.go:1537 -->|
| `ses.sts_external_id` | `FLEET_SES_STS_EXTERNAL_ID` | string | `""` | Optional unique identifier that can be used by the principal assuming the role to assert its identity. <!-- server/config/config.go:1538 -->|
| `ses.source_arn` | `FLEET_SES_SOURCE_ARN` | string | `""` | ARN of the identity that is associated with the sending authorization policy that permits you to send for the email address specified in the Source parameter <!-- server/config/config.go:1539 -->|
| `ses.sender_domain` | `FLEET_SES_SENDER_DOMAIN` | string | `""` | Optional domain to use in the From address for SES emails. If empty, Fleet uses the hostname from the Fleet Web Address (server_settings.server_url) <!-- server/config/config.go:1540 -->|
| `firehose.region` | `FLEET_FIREHOSE_REGION` | string | `""` | AWS Region to use <!-- server/config/config.go:1543 -->|
| `firehose.endpoint_url` | `FLEET_FIREHOSE_ENDPOINT_URL` | string | `""` | AWS Service Endpoint to use (leave empty for default service endpoints) <!-- server/config/config.go:1544 -->|
| `firehose.access_key_id` | `FLEET_FIREHOSE_ACCESS_KEY_ID` | string | `""` | Access Key ID for AWS authentication <!-- server/config/config.go:1546 -->|
| `firehose.secret_access_key` | `FLEET_FIREHOSE_SECRET_ACCESS_KEY` | string | `""` | Secret Access Key for AWS authentication <!-- server/config/config.go:1547 -->|
| `firehose.sts_assume_role_arn` | `FLEET_FIREHOSE_STS_ASSUME_ROLE_ARN` | string | `""` | ARN of role to assume for AWS <!-- server/config/config.go:1548 -->|
| `firehose.sts_external_id` | `FLEET_FIREHOSE_STS_EXTERNAL_ID` | string | `""` | Optional unique identifier that can be used by the principal assuming the role to assert its identity. <!-- server/config/config.go:1550 -->|
| `firehose.status_stream` | `FLEET_FIREHOSE_STATUS_STREAM` | string | `""` | Firehose stream name for status logs <!-- server/config/config.go:1552 -->|
| `firehose.result_stream` | `FLEET_FIREHOSE_RESULT_STREAM` | string | `""` | Firehose stream name for result logs <!-- server/config/config.go:1554 -->|
| `firehose.audit_stream` | `FLEET_FIREHOSE_AUDIT_STREAM` | string | `""` | Firehose stream name for audit logs <!-- server/config/config.go:1556 -->|
| `kinesis.region` | `FLEET_KINESIS_REGION` | string | `""` | AWS Region to use <!-- server/config/config.go:1560 -->|
| `kinesis.endpoint_url` | `FLEET_KINESIS_ENDPOINT_URL` | string | `""` | AWS Service Endpoint to use (leave empty for default service endpoints) <!-- server/config/config.go:1561 -->|
| `kinesis.access_key_id` | `FLEET_KINESIS_ACCESS_KEY_ID` | string | `""` | Access Key ID for AWS authentication <!-- server/config/config.go:1563 -->|
| `kinesis.secret_access_key` | `FLEET_KINESIS_SECRET_ACCESS_KEY` | string | `""` | Secret Access Key for AWS authentication <!-- server/config/config.go:1564 -->|
| `kinesis.sts_assume_role_arn` | `FLEET_KINESIS_STS_ASSUME_ROLE_ARN` | string | `""` | ARN of role to assume for AWS <!-- server/config/config.go:1565 -->|
| `kinesis.sts_external_id` | `FLEET_KINESIS_STS_EXTERNAL_ID` | string | `""` | Optional unique identifier that can be used by the principal assuming the role to assert its identity. <!-- server/config/config.go:1567 -->|
| `kinesis.status_stream` | `FLEET_KINESIS_STATUS_STREAM` | string | `""` | Kinesis stream name for status logs <!-- server/config/config.go:1569 -->|
| `kinesis.result_stream` | `FLEET_KINESIS_RESULT_STREAM` | string | `""` | Kinesis stream name for result logs <!-- server/config/config.go:1571 -->|
| `kinesis.audit_stream` | `FLEET_KINESIS_AUDIT_STREAM` | string | `""` | Kinesis stream name for audit logs <!-- server/config/config.go:1573 -->|
| `lambda.region` | `FLEET_LAMBDA_REGION` | string | `""` | AWS Region to use <!-- server/config/config.go:1577 -->|
| `lambda.access_key_id` | `FLEET_LAMBDA_ACCESS_KEY_ID` | string | `""` | Access Key ID for AWS authentication <!-- server/config/config.go:1578 -->|
| `lambda.secret_access_key` | `FLEET_LAMBDA_SECRET_ACCESS_KEY` | string | `""` | Secret Access Key for AWS authentication <!-- server/config/config.go:1579 -->|
| `lambda.sts_assume_role_arn` | `FLEET_LAMBDA_STS_ASSUME_ROLE_ARN` | string | `""` | ARN of role to assume for AWS <!-- server/config/config.go:1580 -->|
| `lambda.sts_external_id` | `FLEET_LAMBDA_STS_EXTERNAL_ID` | string | `""` | Optional unique identifier that can be used by the principal assuming the role to assert its identity. <!-- server/config/config.go:1582 -->|
| `lambda.status_function` | `FLEET_LAMBDA_STATUS_FUNCTION` | string | `""` | Lambda function name for status logs <!-- server/config/config.go:1584 -->|
| `lambda.result_function` | `FLEET_LAMBDA_RESULT_FUNCTION` | string | `""` | Lambda function name for result logs <!-- server/config/config.go:1586 -->|
| `lambda.audit_function` | `FLEET_LAMBDA_AUDIT_FUNCTION` | string | `""` | Lambda function name for audit logs <!-- server/config/config.go:1588 -->|
| `s3.bucket` *(hidden)* | `FLEET_S3_BUCKET` | string | `""` | Deprecated: Bucket where to store file carves <!-- server/config/config.go:1592 -->|
| `s3.prefix` *(hidden)* | `FLEET_S3_PREFIX` | string | `""` | Deprecated: Prefix under which carves are stored <!-- server/config/config.go:1593 -->|
| `s3.region` *(hidden)* | `FLEET_S3_REGION` | string | `""` | Deprecated: AWS Region (if blank region is derived) <!-- server/config/config.go:1594 -->|
| `s3.endpoint_url` *(hidden)* | `FLEET_S3_ENDPOINT_URL` | string | `""` | Deprecated: AWS Service Endpoint to use (leave blank for default service endpoints) <!-- server/config/config.go:1595 -->|
| `s3.access_key_id` *(hidden)* | `FLEET_S3_ACCESS_KEY_ID` | string | `""` | Deprecated: Access Key ID for AWS authentication <!-- server/config/config.go:1596 -->|
| `s3.secret_access_key` *(hidden)* | `FLEET_S3_SECRET_ACCESS_KEY` | string | `""` | Deprecated: Secret Access Key for AWS authentication <!-- server/config/config.go:1597 -->|
| `s3.sts_assume_role_arn` *(hidden)* | `FLEET_S3_STS_ASSUME_ROLE_ARN` | string | `""` | Deprecated: ARN of role to assume for AWS <!-- server/config/config.go:1598 -->|
| `s3.sts_external_id` *(hidden)* | `FLEET_S3_STS_EXTERNAL_ID` | string | `""` | Deprecated: Optional unique identifier that can be used by the principal assuming the role to assert its identity. <!-- server/config/config.go:1599 -->|
| `s3.disable_ssl` *(hidden)* | `FLEET_S3_DISABLE_SSL` | bool | `false` | Deprecated: Disable SSL (typically for local testing) <!-- server/config/config.go:1600 -->|
| `s3.force_s3_path_style` *(hidden)* | `FLEET_S3_FORCE_S3_PATH_STYLE` | bool | `false` | Deprecated: Set this to true to force path-style addressing, i.e., 'http://s3.amazonaws.com/BUCKET/KEY' <!-- server/config/config.go:1601 -->|
| `s3.carves_bucket` | `FLEET_S3_CARVES_BUCKET` | string | `""` | Bucket where to store file carves <!-- server/config/config.go:1620 -->|
| `s3.carves_prefix` | `FLEET_S3_CARVES_PREFIX` | string | `""` | Prefix under which carves are stored <!-- server/config/config.go:1621 -->|
| `s3.carves_region` | `FLEET_S3_CARVES_REGION` | string | `""` | AWS Region (if blank region is derived) <!-- server/config/config.go:1622 -->|
| `s3.carves_endpoint_url` | `FLEET_S3_CARVES_ENDPOINT_URL` | string | `""` | AWS Service Endpoint to use (leave blank for default service endpoints) <!-- server/config/config.go:1623 -->|
| `s3.carves_access_key_id` | `FLEET_S3_CARVES_ACCESS_KEY_ID` | string | `""` | Access Key ID for AWS authentication <!-- server/config/config.go:1624 -->|
| `s3.carves_secret_access_key` | `FLEET_S3_CARVES_SECRET_ACCESS_KEY` | string | `""` | Secret Access Key for AWS authentication <!-- server/config/config.go:1625 -->|
| `s3.carves_sts_assume_role_arn` | `FLEET_S3_CARVES_STS_ASSUME_ROLE_ARN` | string | `""` | ARN of role to assume for AWS <!-- server/config/config.go:1626 -->|
| `s3.carves_sts_external_id` | `FLEET_S3_CARVES_STS_EXTERNAL_ID` | string | `""` | Optional unique identifier that can be used by the principal assuming the role to assert its identity. <!-- server/config/config.go:1627 -->|
| `s3.carves_disable_ssl` | `FLEET_S3_CARVES_DISABLE_SSL` | bool | `false` | Disable SSL (typically for local testing) <!-- server/config/config.go:1628 -->|
| `s3.carves_force_s3_path_style` | `FLEET_S3_CARVES_FORCE_S3_PATH_STYLE` | bool | `false` | Set this to true to force path-style addressing, i.e., 'http://s3.amazonaws.com/BUCKET/KEY' <!-- server/config/config.go:1629 -->|
| `s3.carves_gcs_iam_auth` | `FLEET_S3_CARVES_GCS_IAM_AUTH` | bool | `false` | Use Google ADC bearer tokens for GCS endpoint authentication instead of S3 HMAC keys <!-- server/config/config.go:1630 -->|
| `s3.carves_cleanup_disabled` | `FLEET_S3_CARVES_CLEANUP_DISABLED` | bool | `false` | Disable the periodic cleanup that marks carves whose S3 object no longer exists as expired <!-- server/config/config.go:1631 -->|
| `s3.carves_cleanup_max_per_run` | `FLEET_S3_CARVES_CLEANUP_MAX_PER_RUN` | int | `1000` | Maximum number of carves the S3 cleanup reconciles (and S3 HeadObject requests it makes) per run <!-- server/config/config.go:1632 -->|
| `s3.carves_cleanup_concurrency` | `FLEET_S3_CARVES_CLEANUP_CONCURRENCY` | int | `32` | Number of concurrent S3 HeadObject probes the carve cleanup performs <!-- server/config/config.go:1633 -->|
| `s3.software_installers_bucket` | `FLEET_S3_SOFTWARE_INSTALLERS_BUCKET` | string | `""` | Bucket where to store uploaded software installers <!-- server/config/config.go:1636 -->|
| `s3.software_installers_prefix` | `FLEET_S3_SOFTWARE_INSTALLERS_PREFIX` | string | `""` | Prefix under which software installers are stored <!-- server/config/config.go:1637 -->|
| `s3.software_installers_region` | `FLEET_S3_SOFTWARE_INSTALLERS_REGION` | string | `""` | AWS Region (if blank region is derived) <!-- server/config/config.go:1638 -->|
| `s3.software_installers_endpoint_url` | `FLEET_S3_SOFTWARE_INSTALLERS_ENDPOINT_URL` | string | `""` | AWS Service Endpoint to use (leave blank for default service endpoints) <!-- server/config/config.go:1639 -->|
| `s3.software_installers_access_key_id` | `FLEET_S3_SOFTWARE_INSTALLERS_ACCESS_KEY_ID` | string | `""` | Access Key ID for AWS authentication <!-- server/config/config.go:1640 -->|
| `s3.software_installers_secret_access_key` | `FLEET_S3_SOFTWARE_INSTALLERS_SECRET_ACCESS_KEY` | string | `""` | Secret Access Key for AWS authentication <!-- server/config/config.go:1641 -->|
| `s3.software_installers_sts_assume_role_arn` | `FLEET_S3_SOFTWARE_INSTALLERS_STS_ASSUME_ROLE_ARN` | string | `""` | ARN of role to assume for AWS <!-- server/config/config.go:1642 -->|
| `s3.software_installers_sts_external_id` | `FLEET_S3_SOFTWARE_INSTALLERS_STS_EXTERNAL_ID` | string | `""` | Optional unique identifier that can be used by the principal assuming the role to assert its identity. <!-- server/config/config.go:1643 -->|
| `s3.software_installers_disable_ssl` | `FLEET_S3_SOFTWARE_INSTALLERS_DISABLE_SSL` | bool | `false` | Disable SSL (typically for local testing) <!-- server/config/config.go:1644 -->|
| `s3.software_installers_force_s3_path_style` | `FLEET_S3_SOFTWARE_INSTALLERS_FORCE_S3_PATH_STYLE` | bool | `false` | Set this to true to force path-style addressing, i.e., 'http://s3.amazonaws.com/BUCKET/KEY' <!-- server/config/config.go:1645 -->|
| `s3.software_installers_gcs_iam_auth` | `FLEET_S3_SOFTWARE_INSTALLERS_GCS_IAM_AUTH` | bool | `false` | Use Google ADC bearer tokens for GCS endpoint authentication instead of S3 HMAC keys <!-- server/config/config.go:1646 -->|
| `s3.software_installers_cloudfront_url` | `FLEET_S3_SOFTWARE_INSTALLERS_CLOUDFRONT_URL` | string | `""` | CloudFront URL for software installers <!-- server/config/config.go:1647 -->|
| `s3.software_installers_cloudfront_url_signing_public_key_id` | `FLEET_S3_SOFTWARE_INSTALLERS_CLOUDFRONT_URL_SIGNING_PUBLIC_KEY_ID` | string | `""` | CloudFront public key ID for URL signing <!-- server/config/config.go:1648 -->|
| `s3.software_installers_cloudfront_url_signing_private_key` | `FLEET_S3_SOFTWARE_INSTALLERS_CLOUDFRONT_URL_SIGNING_PRIVATE_KEY` | string | `""` | CloudFront private key for URL signing <!-- server/config/config.go:1649 -->|
| `pubsub.project` | `FLEET_PUBSUB_PROJECT` | string | `""` | Google Cloud Project to use <!-- server/config/config.go:1652 -->|
| `pubsub.status_topic` | `FLEET_PUBSUB_STATUS_TOPIC` | string | `""` | PubSub topic for status logs <!-- server/config/config.go:1653 -->|
| `pubsub.result_topic` | `FLEET_PUBSUB_RESULT_TOPIC` | string | `""` | PubSub topic for result logs <!-- server/config/config.go:1654 -->|
| `pubsub.audit_topic` | `FLEET_PUBSUB_AUDIT_TOPIC` | string | `""` | PubSub topic for audit logs <!-- server/config/config.go:1655 -->|
| `pubsub.add_attributes` | `FLEET_PUBSUB_ADD_ATTRIBUTES` | bool | `false` | Add PubSub attributes in addition to the message body <!-- server/config/config.go:1656 -->|
| `filesystem.status_log_file` | `FLEET_FILESYSTEM_STATUS_LOG_FILE` | string | `<system temp dir>/osquery_status` *(computed)* | Log file path to use for status logs <!-- server/config/config.go:1659; expr filepath.Join(os.TempDir(), "osquery_status") -->|
| `filesystem.result_log_file` | `FLEET_FILESYSTEM_RESULT_LOG_FILE` | string | `<system temp dir>/osquery_result` *(computed)* | Log file path to use for result logs <!-- server/config/config.go:1661; expr filepath.Join(os.TempDir(), "osquery_result") -->|
| `filesystem.audit_log_file` | `FLEET_FILESYSTEM_AUDIT_LOG_FILE` | string | `<system temp dir>/audit` *(computed)* | Log file path to use for audit logs <!-- server/config/config.go:1663; expr filepath.Join(os.TempDir(), "audit") -->|
| `filesystem.enable_log_rotation` | `FLEET_FILESYSTEM_ENABLE_LOG_ROTATION` | bool | `false` | Enable automatic rotation for osquery log files <!-- server/config/config.go:1665 -->|
| `filesystem.enable_log_compression` | `FLEET_FILESYSTEM_ENABLE_LOG_COMPRESSION` | bool | `false` | Enable compression for the rotated osquery log files <!-- server/config/config.go:1667 -->|
| `filesystem.max_size` | `FLEET_FILESYSTEM_MAX_SIZE` | int | `500` | Maximum size in megabytes log files will grow until rotated (only valid if enable_log_rotation is true) default is 500MB <!-- server/config/config.go:1669 -->|
| `filesystem.max_age` | `FLEET_FILESYSTEM_MAX_AGE` | int | `28` | Maximum number of days to retain old log files based on the timestamp encoded in their filename. Setting to zero wil retain old log files indefinitely (only valid if enable_log_rotation is true) default is 28 days <!-- server/config/config.go:1670 -->|
| `filesystem.max_backups` | `FLEET_FILESYSTEM_MAX_BACKUPS` | int | `3` | Maximum number of old log files to retain. Setting to zero will retain all old log files (only valid if enable_log_rotation is true) default is 3 <!-- server/config/config.go:1671 -->|
| `webhook.status_url` | `FLEET_WEBHOOK_STATUS_URL` | string | `""` | Webhook URL for osquery status logs <!-- server/config/config.go:1674 -->|
| `webhook.result_url` | `FLEET_WEBHOOK_RESULT_URL` | string | `""` | Webhook URL for osquery result logs <!-- server/config/config.go:1675 -->|
| `kafkarest.status_topic` | `FLEET_KAFKAREST_STATUS_TOPIC` | string | `""` | Kafka REST topic for status logs <!-- server/config/config.go:1678 -->|
| `kafkarest.result_topic` | `FLEET_KAFKAREST_RESULT_TOPIC` | string | `""` | Kafka REST topic for result logs <!-- server/config/config.go:1679 -->|
| `kafkarest.audit_topic` | `FLEET_KAFKAREST_AUDIT_TOPIC` | string | `""` | Kafka REST topic for audit logs <!-- server/config/config.go:1680 -->|
| `kafkarest.proxyhost` | `FLEET_KAFKAREST_PROXYHOST` | string | `""` | Kafka REST proxy host url <!-- server/config/config.go:1681 -->|
| `kafkarest.content_type_value` | `FLEET_KAFKAREST_CONTENT_TYPE_VALUE` | string | `"application/vnd.kafka.json.v1+json"` | Kafka REST proxy content type header (defaults to \"application/vnd.kafka.json.v1+json\" <!-- server/config/config.go:1682 -->|
| `kafkarest.timeout` | `FLEET_KAFKAREST_TIMEOUT` | int | `5` | Kafka REST proxy json post timeout <!-- server/config/config.go:1684 -->|
| `nats.status_subject` | `FLEET_NATS_STATUS_SUBJECT` | string | `""` | NATS subject for status logs <!-- server/config/config.go:1687 -->|
| `nats.result_subject` | `FLEET_NATS_RESULT_SUBJECT` | string | `""` | NATS subject for result logs <!-- server/config/config.go:1688 -->|
| `nats.audit_subject` | `FLEET_NATS_AUDIT_SUBJECT` | string | `""` | NATS subject for audit logs <!-- server/config/config.go:1689 -->|
| `nats.server` | `FLEET_NATS_SERVER` | string | `""` | NATS server URL <!-- server/config/config.go:1690 -->|
| `nats.cred_file` | `FLEET_NATS_CRED_FILE` | string | `""` | NATS credentials file <!-- server/config/config.go:1691 -->|
| `nats.nkey_file` | `FLEET_NATS_NKEY_FILE` | string | `""` | NATS NKey file <!-- server/config/config.go:1692 -->|
| `nats.tls_client_crt_file` | `FLEET_NATS_TLS_CLIENT_CRT_FILE` | string | `""` | NATS TLS client certificate file <!-- server/config/config.go:1693 -->|
| `nats.tls_client_key_file` | `FLEET_NATS_TLS_CLIENT_KEY_FILE` | string | `""` | NATS TLS client key file <!-- server/config/config.go:1694 -->|
| `nats.ca_crt_file` | `FLEET_NATS_CA_CRT_FILE` | string | `""` | NATS CA certificate file <!-- server/config/config.go:1695 -->|
| `nats.compression` | `FLEET_NATS_COMPRESSION` | string | `""` | NATS compression algorithm (gzip, snappy, zstd) <!-- server/config/config.go:1696 -->|
| `nats.jetstream` | `FLEET_NATS_JETSTREAM` | bool | `false` | NATS JetStream publish <!-- server/config/config.go:1697 -->|
| `nats.timeout` | `FLEET_NATS_TIMEOUT` | duration | `30s` | NATS timeout <!-- server/config/config.go:1698 -->|
| `splunk.url` | `FLEET_SPLUNK_URL` | string | `""` | Splunk HEC URL (e.g. https://splunk.example.com:8088) <!-- server/config/config.go:1701 -->|
| `splunk.token` | `FLEET_SPLUNK_TOKEN` | string | `""` | Splunk HEC authentication token <!-- server/config/config.go:1702 -->|
| `splunk.index` | `FLEET_SPLUNK_INDEX` | string | `""` | Splunk index to send events to <!-- server/config/config.go:1703 -->|
| `splunk.source` | `FLEET_SPLUNK_SOURCE` | string | `""` | Splunk source value for events <!-- server/config/config.go:1704 -->|
| `splunk.source_type` | `FLEET_SPLUNK_SOURCE_TYPE` | string | `""` | Splunk sourcetype value for events <!-- server/config/config.go:1705 -->|
| `splunk.insecure_skip_verify` | `FLEET_SPLUNK_INSECURE_SKIP_VERIFY` | bool | `false` | Skip TLS certificate verification for Splunk HEC (for self-signed certs) <!-- server/config/config.go:1706 -->|
| `license.key` | `FLEET_LICENSE_KEY` | string | `""` | Fleet license key (to enable Fleet Premium features) <!-- server/config/config.go:1709 -->|
| `license.enforce_host_limit` | `FLEET_LICENSE_ENFORCE_HOST_LIMIT` | bool | `false` | Enforce license limit of enrolled hosts <!-- server/config/config.go:1710 -->|
| `vulnerabilities.databases_path` | `FLEET_VULNERABILITIES_DATABASES_PATH` | string | `"/tmp/vulndbs"` | Path where Fleet will download the data feeds to check CVEs <!-- server/config/config.go:1713 -->|
| `vulnerabilities.periodicity` | `FLEET_VULNERABILITIES_PERIODICITY` | duration | `1h` | How much time to wait between processing software for vulnerabilities. <!-- server/config/config.go:1715 -->|
| `vulnerabilities.cpe_database_url` | `FLEET_VULNERABILITIES_CPE_DATABASE_URL` | string | `""` | URL from which to get the latest CPE database. If empty, it will be downloaded from the latest release available at https://github.com/fleetdm/nvd/releases. <!-- server/config/config.go:1717 -->|
| `vulnerabilities.cpe_translations_url` | `FLEET_VULNERABILITIES_CPE_TRANSLATIONS_URL` | string | `""` | URL from which to get the latest CPE translations. If empty, it will be downloaded from the latest release available at https://github.com/fleetdm/nvd/releases. <!-- server/config/config.go:1719 -->|
| `vulnerabilities.cve_feed_prefix_url` | `FLEET_VULNERABILITIES_CVE_FEED_PREFIX_URL` | string | `""` | Prefix URL for the CVE data feed. If empty, default to https://nvd.nist.gov/ <!-- server/config/config.go:1721 -->|
| `vulnerabilities.cisa_known_exploits_url` | `FLEET_VULNERABILITIES_CISA_KNOWN_EXPLOITS_URL` | string | `""` | URL from which to get the latest CISA (Known exploited vulnerabilities) database. If empty, it will be downloaded from https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json <!-- server/config/config.go:1723 -->|
| `vulnerabilities.current_instance_checks` | `FLEET_VULNERABILITIES_CURRENT_INSTANCE_CHECKS` | string | `"auto"` | Allows to manually select an instance to do the vulnerability processing. <!-- server/config/config.go:1725 -->|
| `vulnerabilities.disable_schedule` | `FLEET_VULNERABILITIES_DISABLE_SCHEDULE` | bool | `false` | Set this to true when the vulnerability processing job is scheduled by an external mechanism <!-- server/config/config.go:1727 -->|
| `vulnerabilities.disable_data_sync` | `FLEET_VULNERABILITIES_DISABLE_DATA_SYNC` | bool | `false` | Skips synchronizing data streams and expects them to be available in the databases_path. <!-- server/config/config.go:1729 -->|
| `vulnerabilities.recent_vulnerability_max_age` | `FLEET_VULNERABILITIES_RECENT_VULNERABILITY_MAX_AGE` | duration | `720h` | Maximum age of the published date of a vulnerability (CVE) to be considered 'recent'. <!-- server/config/config.go:1731 -->|
| `vulnerabilities.disable_win_os_vulnerabilities` | `FLEET_VULNERABILITIES_DISABLE_WIN_OS_VULNERABILITIES` | bool | `false` | Don't sync installed Windows updates nor perform Windows OS vulnerability processing. <!-- server/config/config.go:1733 -->|
| `vulnerabilities.osv_for_vulnerabilities` | `FLEET_VULNERABILITIES_OSV_FOR_VULNERABILITIES` | bool | `true` | Use OSV (osv.dev) format for vulnerability detection instead of OVAL where supported. <!-- server/config/config.go:1738 -->|
| `vulnerabilities.max_concurrency` | `FLEET_VULNERABILITIES_MAX_CONCURRENCY` | int | `1` | Maximum number of concurrent database queries to use for processing vulnerabilities. <!-- server/config/config.go:1743 -->|
| `upgrades.allow_missing_migrations` | `FLEET_UPGRADES_ALLOW_MISSING_MIGRATIONS` | bool | `false` | Allow serve to run even if migrations are missing. <!-- server/config/config.go:1750 -->|
| `sentry.dsn` | `FLEET_SENTRY_DSN` | string | `""` | DSN for Sentry <!-- server/config/config.go:1754 -->|
| `geoip.database_path` | `FLEET_GEOIP_DATABASE_PATH` | string | `""` | path to mmdb file <!-- server/config/config.go:1757 -->|
| `prometheus.basic_auth.username` | `FLEET_PROMETHEUS_BASIC_AUTH_USERNAME` | string | `""` | Prometheus username for HTTP Basic Auth <!-- server/config/config.go:1760 -->|
| `prometheus.basic_auth.password` | `FLEET_PROMETHEUS_BASIC_AUTH_PASSWORD` | string | `""` | Prometheus password for HTTP Basic Auth <!-- server/config/config.go:1761 -->|
| `prometheus.basic_auth.disable` | `FLEET_PROMETHEUS_BASIC_AUTH_DISABLE` | bool | `false` | Disable HTTP Basic Auth for Prometheus <!-- server/config/config.go:1762 -->|
| `packaging.global_enroll_secret` | `FLEET_PACKAGING_GLOBAL_ENROLL_SECRET` | string | `""` | Enroll secret to be used for the global domain (instead of randomly generating one) <!-- server/config/config.go:1767 -->|
| `packaging.s3.bucket` | `FLEET_PACKAGING_S3_BUCKET` | string | `""` | Bucket where to retrieve installers <!-- server/config/config.go:1768 -->|
| `packaging.s3.prefix` | `FLEET_PACKAGING_S3_PREFIX` | string | `""` | Prefix under which installers are stored <!-- server/config/config.go:1769 -->|
| `packaging.s3.region` | `FLEET_PACKAGING_S3_REGION` | string | `""` | AWS Region (if blank region is derived) <!-- server/config/config.go:1770 -->|
| `packaging.s3.endpoint_url` | `FLEET_PACKAGING_S3_ENDPOINT_URL` | string | `""` | AWS Service Endpoint to use (leave blank for default service endpoints) <!-- server/config/config.go:1771 -->|
| `packaging.s3.access_key_id` | `FLEET_PACKAGING_S3_ACCESS_KEY_ID` | string | `""` | Access Key ID for AWS authentication <!-- server/config/config.go:1772 -->|
| `packaging.s3.secret_access_key` | `FLEET_PACKAGING_S3_SECRET_ACCESS_KEY` | string | `""` | Secret Access Key for AWS authentication <!-- server/config/config.go:1773 -->|
| `packaging.s3.sts_assume_role_arn` | `FLEET_PACKAGING_S3_STS_ASSUME_ROLE_ARN` | string | `""` | ARN of role to assume for AWS <!-- server/config/config.go:1774 -->|
| `packaging.s3.sts_external_id` | `FLEET_PACKAGING_S3_STS_EXTERNAL_ID` | string | `""` | Optional unique identifier that can be used by the principal assuming the role to assert its identity. <!-- server/config/config.go:1775 -->|
| `packaging.s3.disable_ssl` | `FLEET_PACKAGING_S3_DISABLE_SSL` | bool | `false` | Disable SSL (typically for local testing) <!-- server/config/config.go:1776 -->|
| `packaging.s3.force_s3_path_style` | `FLEET_PACKAGING_S3_FORCE_S3_PATH_STYLE` | bool | `false` | Set this to true to force path-style addressing, i.e., 'http://s3.amazonaws.com/BUCKET/KEY' <!-- server/config/config.go:1777 -->|
| `mdm.apple_apns_cert` | `FLEET_MDM_APPLE_APNS_CERT` | string | `""` | Apple APNs PEM-encoded certificate path <!-- server/config/config.go:1780 -->|
| `mdm.apple_apns_cert_bytes` | `FLEET_MDM_APPLE_APNS_CERT_BYTES` | string | `""` | Apple APNs PEM-encoded certificate bytes <!-- server/config/config.go:1781 -->|
| `mdm.apple_apns_key` | `FLEET_MDM_APPLE_APNS_KEY` | string | `""` | Apple APNs PEM-encoded private key path <!-- server/config/config.go:1782 -->|
| `mdm.apple_apns_key_bytes` | `FLEET_MDM_APPLE_APNS_KEY_BYTES` | string | `""` | Apple APNs PEM-encoded private key bytes <!-- server/config/config.go:1783 -->|
| `mdm.apple_scep_cert` | `FLEET_MDM_APPLE_SCEP_CERT` | string | `""` | Apple SCEP PEM-encoded certificate path <!-- server/config/config.go:1784 -->|
| `mdm.apple_scep_cert_bytes` | `FLEET_MDM_APPLE_SCEP_CERT_BYTES` | string | `""` | Apple SCEP PEM-encoded certificate bytes <!-- server/config/config.go:1785 -->|
| `mdm.apple_scep_key` | `FLEET_MDM_APPLE_SCEP_KEY` | string | `""` | Apple SCEP PEM-encoded private key path <!-- server/config/config.go:1786 -->|
| `mdm.apple_scep_key_bytes` | `FLEET_MDM_APPLE_SCEP_KEY_BYTES` | string | `""` | Apple SCEP PEM-encoded private key bytes <!-- server/config/config.go:1787 -->|
| `mdm.apple_bm_server_token` | `FLEET_MDM_APPLE_BM_SERVER_TOKEN` | string | `""` | Apple Business encrypted server token path (.p7m file) <!-- server/config/config.go:1788 -->|
| `mdm.apple_bm_server_token_bytes` | `FLEET_MDM_APPLE_BM_SERVER_TOKEN_BYTES` | string | `""` | Apple Business encrypted server token bytes <!-- server/config/config.go:1789 -->|
| `mdm.apple_bm_cert` | `FLEET_MDM_APPLE_BM_CERT` | string | `""` | Apple Business PEM-encoded certificate path <!-- server/config/config.go:1790 -->|
| `mdm.apple_bm_cert_bytes` | `FLEET_MDM_APPLE_BM_CERT_BYTES` | string | `""` | Apple Business PEM-encoded certificate bytes <!-- server/config/config.go:1791 -->|
| `mdm.apple_bm_key` | `FLEET_MDM_APPLE_BM_KEY` | string | `""` | Apple Business PEM-encoded private key path <!-- server/config/config.go:1792 -->|
| `mdm.apple_bm_key_bytes` | `FLEET_MDM_APPLE_BM_KEY_BYTES` | string | `""` | Apple Business PEM-encoded private key bytes <!-- server/config/config.go:1793 -->|
| `mdm.apple_enable` | `FLEET_MDM_APPLE_ENABLE` | bool | `false` | Enable MDM Apple functionality <!-- server/config/config.go:1794 -->|
| `mdm.apple_scep_signer_validity_days` | `FLEET_MDM_APPLE_SCEP_SIGNER_VALIDITY_DAYS` | int | `365` | Days signed client certificates will be valid <!-- server/config/config.go:1795 -->|
| `mdm.apple_vpp_app_metadata_api_bearer_token` | `FLEET_MDM_APPLE_VPP_APP_METADATA_API_BEARER_TOKEN` | string | `""` | Apple Connect JWT, used for accessing VPP app metadata directly from Apple <!-- server/config/config.go:1796 -->|
| `mdm.apple_scep_challenge` | `FLEET_MDM_APPLE_SCEP_CHALLENGE` | string | `""` | SCEP static challenge for enrollment <!-- server/config/config.go:1797 -->|
| `mdm.apple_dep_sync_periodicity` | `FLEET_MDM_APPLE_DEP_SYNC_PERIODICITY` | duration | `1m` | How much time to wait for DEP profile assignment <!-- server/config/config.go:1798 -->|
| `mdm.windows_wstep_identity_cert` | `FLEET_MDM_WINDOWS_WSTEP_IDENTITY_CERT` | string | `""` | Microsoft WSTEP PEM-encoded certificate path <!-- server/config/config.go:1799 -->|
| `mdm.windows_wstep_identity_key` | `FLEET_MDM_WINDOWS_WSTEP_IDENTITY_KEY` | string | `""` | Microsoft WSTEP PEM-encoded private key path <!-- server/config/config.go:1800 -->|
| `mdm.windows_wstep_identity_cert_bytes` | `FLEET_MDM_WINDOWS_WSTEP_IDENTITY_CERT_BYTES` | string | `""` | Microsoft WSTEP PEM-encoded certificate bytes <!-- server/config/config.go:1801 -->|
| `mdm.windows_wstep_identity_key_bytes` | `FLEET_MDM_WINDOWS_WSTEP_IDENTITY_KEY_BYTES` | string | `""` | Microsoft WSTEP PEM-encoded private key bytes <!-- server/config/config.go:1802 -->|
| `mdm.sso_rate_limit_per_minute` | `FLEET_MDM_SSO_RATE_LIMIT_PER_MINUTE` | int | `0` | Number of allowed requests per minute to MDM SSO endpoints (default is sharing login rate limit bucket) <!-- server/config/config.go:1803 -->|
| `mdm.certificate_profiles_limit` | `FLEET_MDM_CERTIFICATE_PROFILES_LIMIT` | int | `100` | Maximum number of CA certificate profile installations per batch (0 = unlimited) <!-- server/config/config.go:1804 -->|
| `mdm.enable_custom_os_updates_and_filevault` | `FLEET_MDM_ENABLE_CUSTOM_OS_UPDATES_AND_FILEVAULT` | bool | `false` | Allows usage of custom Apple MDM profiles for FileVault (Fleet Premium required) <!-- server/config/config.go:1805 -->|
| `mdm.enable_custom_filevault` | `FLEET_MDM_ENABLE_CUSTOM_FILEVAULT` | bool | `false` | Allows usage of custom Apple MDM profiles for FileVault (Fleet Premium required) <!-- server/config/config.go:1806 -->|
| `mdm.enable_custom_disk_encryption` | `FLEET_MDM_ENABLE_CUSTOM_DISK_ENCRYPTION` | bool | `false` | Allows usage of custom Apple MDM profiles for FileVault and custom Windows profiles for BitLocker (Fleet Premium required) <!-- server/config/config.go:1807 -->|
| `mdm.allow_all_declarations` | `FLEET_MDM_ALLOW_ALL_DECLARATIONS` | bool | `false` | Allows all MDM declaration types to be sent, bypassing safety checks <!-- server/config/config.go:1808 -->|
| `mdm.android_agent.package` *(hidden)* | `FLEET_MDM_ANDROID_AGENT_PACKAGE` | string | `"com.fleetdm.agent"` | Package name for the Fleet Android agent <!-- server/config/config.go:1809 -->|
| `mdm.android_agent.signing_sha256` *(hidden)* | `FLEET_MDM_ANDROID_AGENT_SIGNING_SHA256` | string | `"x+IyvrwVbQEBYV/ojWmLavJE0VIZE1RAT2JmxeI5sFw="` | Signing certificate SHA256 fingerprint for the Fleet Android agent <!-- server/config/config.go:1810 -->|
| `mdm.android_batch_size` *(hidden)* | `FLEET_MDM_ANDROID_BATCH_SIZE` | int | `100` | Maximum number of hosts per batch for Android MDM API operations (100 default; 0 = no limit) <!-- server/config/config.go:1813 -->|
| `calendar.periodicity` | `FLEET_CALENDAR_PERIODICITY` | duration | `0s` | How much time to wait between processing calendar integration. <!-- server/config/config.go:1817 -->|
| `partnerships.enable_secureframe` | `FLEET_PARTNERSHIPS_ENABLE_SECUREFRAME` | bool | `false` | Point transparency URL at Secureframe landing page <!-- server/config/config.go:1823 -->|
| `microsoft_compliance_partner.proxy_uri` | `FLEET_MICROSOFT_COMPLIANCE_PARTNER_PROXY_URI` | string | `"https://fleetdm.com"` | URI of the Microsoft Compliance Partner proxy (for development/testing) <!-- server/config/config.go:1826 -->|
| `partnerships.enable_primo` | `FLEET_PARTNERSHIPS_ENABLE_PRIMO` | bool | `false` | Disables the ability to manage multiple fleets in an instance, even in premium tier <!-- server/config/config.go:1828 -->|
| `conditional_access.cert_serial_format` | `FLEET_CONDITIONAL_ACCESS_CERT_SERIAL_FORMAT` | string | `"hex"` | Format for parsing certificate serial numbers from X-Client-Cert-Serial header: 'hex' (default, used by AWS ALB) or 'decimal' (used by Caddy) <!-- server/config/config.go:1831 -->|
