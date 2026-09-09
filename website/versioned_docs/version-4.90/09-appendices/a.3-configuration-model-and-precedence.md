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

![Reference](../_assets/icons/reference-light.svg) The same-looking Fleet setting can come from the server, organization settings, a fleet, or the host. When two sources disagree, the winner depends on the setting. Use this appendix to find the owner and the precedence rule.

<a id="what-this-appendix-carries"></a>

## How to use this reference

![Reference](../_assets/icons/reference-light.svg) Use the tables below to trace a setting from its source to the value a host or server uses. They cover ownership, precedence, and the known exceptions. Where a comparison is incomplete, the text identifies that limit.

The catalog at the end lists each registered server key, its default, and its usage string, the description used by `fleet serve --help`. These entries were generated from the server registrations. Some differ from Fleet’s published configuration reference; the differences are listed before the catalog.

For help choosing a setting or deciding when to change it, see [2.7](../02-administer-and-deploy-fleet/2.7-organization-and-server-settings.md). Return here when you need to establish which source controls the value or how competing sources resolve.

<a id="the-authorities"></a>

## Configuration sources

![Reference](../_assets/icons/reference-light.svg) When a value seems to be ignored, ask three questions: where was it declared, where is the active value stored, and which interface wrote it? The tables distinguish the stores Fleet reads from the tools that write to them.

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
| **Settings for a fleet** | A fleet's settings block | The database, cached about a minute | Per request |
| **Agent options** | An `agent_options` block | Inside organisation or fleet settings | Per host check-in |
| **Per-host stored control** | Nothing an administrator writes | A column on the host | Per agent poll |
| **The device-management asset store** | Nothing, once populated | The database, encrypted, with a deletion history | Per use |

The host has seven additional sources. Fleet reports only a small part of their resulting configuration: each detail cycle collects four osquery flags covering the distributed interval, the configuration refresh pair, and the logger period. Those values can help confirm the result, but they do not identify its source or describe the other host settings.

| Source | Declared as | Stored | Read |
|---|---|---|---|
| **Compiled-in agent defaults** | Nothing. They are the fallback | The binary | On a miss |
| **The service definition** | A flag on the agent's command line, or its upper-cased environment form | The launch daemon's property list, the service defaults file, or the Windows service entry | Once, at start |
| **The agent's own root files** | The enroll secret file, the server URL file, the osquery flags file, the extensions list, the persisted server overrides | Files under the agent's root directory | At start, and each time a receiver runs |
| **The operating-system keystore** | Nothing an administrator writes directly | Keychain, or Credential Manager | At start, **and only as a fallback** |
| **The macOS configuration profile** | A profile delivered by whichever MDM manages the Mac | The device's profile state | In a loop at start, and every five minutes for one setting |
| **Direct agent environment reads** | A variable the agent reads itself. No flag form, no entry in its help output | The process environment | Varies |
| **Trailing osquery arguments** | Whatever follows the separator on the agent's own command line | The argument list handed to osquery | Every osquery start |

The packager, installer properties, local edits, and Fleet’s delivery mechanisms write into these host stores. Values written to disk can remain in use after the server becomes unreachable; a later section distinguishes those from settings held only in memory.

> ### Host inputs to inspect locally
>
> The agent assembles osquery’s command line in this order: generated flags, the local osquery flags file, then the settings it protects from that file: the host identifier, database directory, and extensions autoload list where configured. Arguments after the separator on the agent’s command line are appended last. Fleet’s source describes them as overrides for the preceding flags and flagfile entries.
>
> Duplicate-option handling belongs to osquery and has not been verified here. Treat trailing arguments as possible overrides, including for the three protected settings, and confirm their effect on the host. Fleet’s macOS, Linux, and Windows packages supply no trailing arguments; they require a local change to the service definition and are not visible in Fleet.
>
> Direct environment reads also need local inspection. They have no flag, help entry, or server setting. Two are useful during support work: one suppresses a retry-notice line while leaving each enrollment failure logged at ordinary verbosity ([1.2](../01-foundations/1.2-how-fleet-reaches-a-device.md)); another preserves each script run’s temporary directory. Disable the latter after the investigation to avoid accumulating script bodies and output.
>
> Fleet Desktop gets its configuration through environment variables set by the agent when it launches Desktop. Its only command-line options are `--version` and `--help`; those environment variables are an internal communication path rather than operator settings.

### What the server can and cannot change on an installed host

![Reference](../_assets/icons/reference-light.svg) Each check-in gives the agent a fresh configuration document. The settings in it have different lifetimes, so a useful first step is to check which survive an agent restart.

| What the server sends | What it changes, and what survives a restart |
|---|---|
| **The three update channels**, for the agent, osquery, and Fleet Desktop | Written to a persisted overrides file. A change forces an agent restart, and the values survive later restarts |
| **The debug log level and script execution timeout** | Agent settings held in memory. They are lost on restart and re-applied at the next check-in. An agent started in debug has a local floor: the server can raise its log level but cannot lower it |
| **osquery startup flags, osquery extensions, and Nudge configuration** | Written to files in the agent’s root directory, where they survive restarts. These configure the components the agent supervises |
| **Twelve notifications** | Instructions to act, such as rotating an encryption key, running a pending script, or starting the setup experience |

Of the agent’s own settings in this table, only the update channels are persisted. You can audit them from host files. The debug level and script execution timeout are server-controlled too, but their current values leave no record on disk.

The following counts and input forms describe different parts of this configuration:

| Configuration surface | Scope |
|---|---|
| **Agent command-line settings** | Twenty-nine settings, of which twenty-eight also accept an environment variable. `--version` is the exception. This describes local inputs, not which settings the server controls |
| **Persisted override file** | The three update channels last sent by the server, plus two locally derived paths to helper binaries |
| **`command_line_flags` in agent options** | Settings for the child osquery process, in the third group above |
| **Packaging environment inputs** | Twelve inputs on the build host: five for packaging and signing, and seven that also have runtime environment forms. None of the twelve is exclusive to packaging |

For host settings outside these groups, use configuration management or a reinstall to change the source the host reads. Before rolling out update-channel changes, also check the persisted-override behavior below.

> ### Stored device-management assets take precedence
>
> The device-management asset store holds three kinds of material:
>
> | Material | How it gets there |
> |---|---|
> | **Apple push certificate and key, Apple SCEP certificate and key, and Apple Business Manager certificate, key, and token** | Imported from process configuration at first boot. The database controls subsequent use |
> | **Apple SCEP enrollment challenge** | Imported when supplied, or generated randomly when absent |
> | **Android enterprise material and Platform SSO signing material** | Generated during the Google enterprise signup handshake or the first Platform SSO configuration. Neither has a process-configuration form |
>
> Once imported, rotate Apple assets through the interface or API. Changing a deployment manifest and restarting does not replace the stored material. Startup logs warn that configured push, SCEP certificate, and Business Manager values are being ignored. A stored SCEP enrollment challenge takes precedence without an ordinary-boot warning.
>
> Apple Business Manager still parses its configured certificate, key, and token *before* consulting the database. A broken path or conflicting path and inline value can therefore stop every startup, even when the database has valid material. Remove those process settings entirely to boot from the stored token.
>
> Push and SCEP certificate files are read only when the database lacks the required assets. Moving a Business Manager token file can stop startup; moving an already-imported push certificate file does not.

## Inputs that change the result without owning a value

![Explanation](../_assets/icons/explanation-light.svg) Some inputs determine who receives a setting, how it is delivered, or whether it takes effect. Use this table to separate those effects from the source of the value.

| | What it does |
|---|---|
| **Labels, fleet placement, platform** | *Select* which hosts a value reaches. They do not compete for the value |
| **Licence** | Controls capability access, precedence, and some stored values; see below |
| **Fleet secret variables, host attributes, identity-provider attributes** | *Substitute* into a value at delivery, changing what the device receives without authoring it |
| **The device platform, and any external management provider** | *Enforce*, or fail to. They hold actual state, not Fleet's desired state |
| **GitOps** | Writes stored settings through the API. Your repository can remain your organisation’s source of truth |

> ### How the licence affects configuration
>
> The licence determines which capabilities are available. A capability outside your tier returns a licence error; role restrictions return a permission error ([a.4](a.4-roles-and-permissions-matrix.md)).
>
> The licence also changes precedence for the transparency URL: Free uses process configuration, while Premium uses the stored setting. Check the tier when that URL appears to be ignored.
>
> On Free, saving organisation settings clears three stored values: the transparency URL, the alternative browser host, and a populated device-management host name template. This happens even when the save does not mention those fields, without an error, warning, or activity. Before downgrading from Premium, record all three. Upgrading later will not restore values cleared by a settings save.

## How collisions resolve

![Reference](../_assets/icons/reference-light.svg) Precedence depends on the setting. These six mechanisms describe the resolution paths observed at this release; a single path can combine several of them.

| Mechanism | What happens |
|---|---|
| **Precedence** | The stronger source's value replaces the weaker one's |
| **Fallback** | The second source is consulted only when the first produced nothing |
| **Write-through** | The weaker source rewrites the stronger one's store, then deletes itself |
| **Composition** | Both values combine, by OR, by a floor, or by merge-if-absent |
| **Mutual exclusion** | Setting both is a fatal error. There is no winner |
| **Channel disabled** | One setting removes the channel by which the other would arrive, so no comparison ever happens |

When a channel is disabled, its receiver is never registered. The server’s value cannot reach the host through that channel.

For the server’s process configuration, Fleet’s configuration-dump help gives a fixed order: command-line flags, environment variables, the configuration file, then built-in defaults.

> To remove an environment override, remove the variable rather than leaving it empty. Empty-value handling belongs to the configuration library, which this release does not vendor, and has not been established here from Fleet’s source or tests.

### Pairs that must not both be set

Fleet resolves the configuration before checking these mutually exclusive pairs. The checks apply to the resolved values, so a flag can conflict with an environment variable just as two entries in a file can. Any listed conflict prevents startup.

Per-key type and range checks run earlier, during loading. A value of the wrong type or an out-of-range TLS compatibility setting can fail before the pair checks run.

| Pair | What happens |
|---|---|
| **A device-management certificate, key or token given both as a path and as inline content** | Startup fails, with a message naming the certificate, the key or the token. It covers the Apple push certificate and key, the Apple SCEP certificate and key, the Apple Business Manager certificate, key and server token, and the Windows device-management identity certificate and key |
| **`mysql.password` with `mysql.password_path`** | Startup fails. The same check covers the read replica, so `mysql_read_replica.password` with `mysql_read_replica.password_path` fails the same way, its message prefixed to say which of the two connections was at fault |
| **`server.private_key` with `server.private_key_arn`** | Startup fails before Fleet calls the secret manager. A key that resolves shorter than 32 bytes is a separate startup failure, checked after the fetch |
| **On the host, `--insecure` with `--fleet-certificate`** | The agent refuses to start, saying the two may not be specified together |
| **On the host, `--insecure` with `--update-tls-certificate`** | The agent refuses to start because the update server’s certificate conflicts with insecure mode |

> During a certificate migration, adding `--insecure` alongside either certificate flag prevents the agent from starting. If you intend to use insecure mode, remove the conflicting certificate flag.

> The path/inline checks cover device-management material. The server’s own TLS certificate and key have no inline form, and the rule does not apply to object-store or licence settings.
>
> Push and SCEP certificate parsing is skipped once the database holds every required asset. A conflicting pair can therefore stop startup before import but go unreported afterwards. If only some assets are stored, parsing and conflict checks still run.
>
> Apple Business Manager parses before consulting the database, and the Windows identity certificate is never stored as an asset. Their path/inline conflicts remain fatal on every boot.

### Where several mechanisms meet

Agent credentials combine several resolution mechanisms. Their order depends on whether the agent was installed to read the macOS configuration profile; this is the agent path where a remote source can override locally supplied credentials.

Without the macOS profile, the enroll secret and server URL resolve separately:

| Credential | How it resolves |
|---|---|
| **The enroll secret** | Supplying both `--enroll-secret` and `--enroll-secret-path` is a fatal error at start, with no winner. A non-empty secret file has its contents written into the keystore and **the file is then deleted**, so the credential moves and the file you created disappears. The keystore is consulted only when nothing has been set by flag or environment. Otherwise: flag, then environment variable, then compiled default |
| **The server URL** | The flag takes precedence over `ORBIT_FLEET_URL`. There is no compiled default or keystore fallback. With neither input set, the value is empty. Its local file is read only in the profile-enabled path below |

With the profile enabled on macOS, both values follow this sequence. The separate keystore fallback described above is skipped:

| Step | What happens |
|---|---|
| The macOS configuration profile | **Sets both values unconditionally**, beating the flag and the environment, and writes both back to the agent's local files |
| Both values now present | The agent stops looking |
| Otherwise the local server URL file, then the local secret file, then the keystore | Consulted in that order. **Keystore errors here are logged rather than returned** |
| Still nothing | **The agent waits thirty seconds and repeats, indefinitely.** It does not exit |

> The source comment says the profile applies only when neither credential is set, but the implementation applies it regardless. On a Mac installed this way, the managing MDM’s profile overrides the enroll secret and server URL supplied in the package.
>
> If the required values remain missing, the agent keeps retrying. A process or service-status check can pass even though the host has not appeared in Fleet.

<a id="the-update-channel-exception-and-why-that-file-is-not-what-it-looks-like"></a>

### How persisted update channels affect a rollout

Update-channel changes depend on the existing override file as well as on whether the agent accepts updates.

At startup, the persisted overrides file takes precedence over flags and environment variables for the three channels. At check-in, the agent compares the server’s request with that file. Missing values on either side count as `stable`.

The comparison includes all three channels together, except that Fleet Desktop is excluded when Desktop is disabled. It does not include the channels built into the package.

For example, an agent packaged for `edge` may have no override file. The comparison reads that absent file as all-`stable`, so a request for `stable` on every enabled channel appears unchanged. Nothing is written or restarted, and the host continues using its packaged `edge` channel even though Fleet shows the requested value.

A request containing at least one non-`stable` value on an enabled channel triggers a write of all three values. Any `stable` values in that same request take effect too.

Before an all-`stable` rollout, check for hosts without an override file. Naming several channels in the request does not resolve this case; the comparison still sees no change.

### Auditing the channels actually in force on a host

**The file is `server-overrides.json`, in the agent's root directory.** By default that directory is `/opt/orbit` on macOS and on Linux, and `C:\Program Files\Orbit` on Windows, following the system's own program-files location where that has been moved. **The root directory is itself overridable at install time**, by `--root-dir` or `ORBIT_ROOT_DIR`, so confirm it from the service definition before concluding that a file is missing.

Read the file’s contents as well as checking for its presence. Each write includes all three channels and two fallback binary paths. The agent does not delete or empty the file.

| What you find | What it establishes |
|---|---|
| **No file** | No write has ever happened: either the server sent no channels at all, or everything it sent normalised to all-`stable`. **Either way the host runs whatever its package was built with**, which is the case the exception above hides |
| **A file** | A write happened at some point. **On its own that says nothing about the channels now in force** |
| **The three values inside it** | **The channels in force.** A file holding three `stable` values is the ordinary result of moving a host back to `stable`, and not evidence of anything wrong |
| **An empty value for a channel** | That channel is **not** overridden. It falls back to the flag or environment variable the host was installed with, each of which defaults to `stable` |

To audit a host, confirm its root directory from the service definition, then read the three channel values.

> If the server sends no update channels, as older Fleet versions do, the agent ignores the request before comparing values. Removing the key will not restore packaged channels.

> Disabling updates prevents the receiver from writing new overrides, but the agent still reads the existing file at startup. Its last override remains in force while updates are disabled.

<a id="where-the-planes-cross"></a>

## Where process and stored settings interact

![Reference](../_assets/icons/reference-light.svg) Process configuration and stored configuration usually control different settings. The verified cases below cover two overlapping values and two prerequisites that determine whether a stored setting can be written.

> These are known overlaps, not an exhaustive list. A complete comparison of all 320 registered process keys with the nineteen top-level organisation-settings blocks and their nested fields has not been performed.

<a id="the-two-known-to-exist-in-both-planes"></a>

### Values controlled by both sources

| Setting | How it resolves |
|---|---|
| **The vulnerability database directory** | `vulnerabilities.databases_path` in the process configuration **beats** `vulnerability_settings.databases_path` in organisation settings, and the server logs an informational line saying that it did. **The process key ships with a non-empty default**, so on an otherwise untouched server the process value always wins and the stored setting never takes effect at all. Setting it in the interface and seeing nothing change is the expected outcome rather than a fault |
| **The transparency URL** | Three-way and licence-conditional: Fleet's built-in default, then the `partnerships.enable_secureframe` process setting, then the stored `fleet_desktop.transparency_url`, **which is read only on Premium**. So on Free the process configuration wins and the stored value is never consulted, and on Premium the stored value wins. **The same two values resolve in opposite directions on the two tiers** |

The interface displays the stored value, without identifying which source takes precedence. A saved value may therefore differ from the one Fleet uses. On Free, the stored transparency URL can read back successfully even though Fleet does not consult it.

<a id="two-preconditions-where-the-process-plane-gates-a-stored-write"></a>

### Process prerequisites for stored settings

In these cases, a missing process setting causes Fleet to reject the write.

**Disk encryption requires the server private key.** Turning on `mdm.enable_disk_encryption`, from the interface, the API or GitOps, is rejected unless the server was started with `server.private_key` configured. **The requirement is not platform-specific**: this is the single organisation-wide toggle covering FileVault, BitLocker and Linux, so all three fail together. The same key gates uploading an Apple push certificate, saving secret variables and Apple account provisioning, so a deployment missing it fails a scattered set of operations that do not obviously belong together.

**Disk-encryption payloads inside custom profiles are refused unless a process setting allows them.** By default Fleet rejects a macOS profile carrying FileVault settings and a Windows profile targeting the BitLocker area, telling you to use the disk-encryption setting instead. Three process settings lift that restriction, two of them older names for the third, and **any one of them lifts it for both platforms at once.** There is no way to allow it for Apple and not for Windows.

> These settings allow disk-encryption content within custom profiles. They do not control permission to upload other custom-profile content.

<a id="agent-options-resolve-per-consumer-not-once"></a>

## How each component reads agent options

![Troubleshooting](../_assets/icons/troubleshooting-light.svg) osquery and Orbit read agent options through different paths. Check which component uses the setting before relying on a fallback.

osquery uses the fleet’s whole document when one exists; otherwise it uses the global document. Missing keys in an existing fleet document do not fall back to global values ([1.3](../01-foundations/1.3-hosts-fleets-labels.md)).

A platform override replaces the base configuration entirely. Include the complete configuration needed by hosts on that platform.

Orbit reads update channels, command-line flags, and extensions from the fleet’s document without falling back to global values, even when the fleet has no document. The script execution timeout is the exception: it falls back when its value is zero, so an explicit zero and an unset value have the same effect.

Two settings combine local and remote values. The macOS profile can enable scripts but cannot disable a locally enabled value. A local debug flag sets a floor that the server cannot lower by sending false.

<a id="the-per-host-debug-window-is-a-merge-and-it-loses-to-an-explicit-value"></a>

### Enrollment debug windows and explicit verbosity

At this release, `orbit.debug_logging_on_enroll_duration` is the only way to open a per-host debug window. It applies to hosts enrolling under that scope. Configure it before enrollment; there is no host action or endpoint to open a window for an existing host.

During the window, Fleet adds `verbose: true` to the fleet’s `command_line_flags` only if `verbose` is absent. All existing keys are preserved.

An explicit `verbose: false` therefore keeps osquery at normal verbosity. The agent still receives a separate signal to raise its own log level, so agent debug logs can be available while osquery detail is missing.

The single-host API returns the window’s expiry in `orbit_debug_until`. The host list, CSV export, and interface do not expose it, and no field reports whether an explicit `verbose` value prevented the osquery change.

When setting the enrollment duration, check the fleet’s agent options too. Remove an explicit `verbose` value if you want the window to raise osquery verbosity along with the agent’s.

### Absent and empty mean different things for osquery startup flags

The presence and value of `command_line_flags` determine what happens to the host’s local osquery flags file:

| `command_line_flags` in agent options | What the agent does |
|---|---|
| **Absent** | **Leaves the host's osquery flags file untouched**, preserving whatever was packaged with the agent or written locally |
| **Explicitly empty**, as `{}` or `null` | **Clears the file** and restarts osquery without those flags |
| **Set to a value that differs from the file** | **Replaces the file wholesale** and restarts osquery |
| **Set to a value matching the file** | Nothing. Re-applying unchanged configuration causes no restart |

A replacement overwrites the entire local file, including comments. Removing `command_line_flags` later leaves Fleet’s last file in place; it does not restore the earlier contents. Keep a copy of locally maintained flags in your packaging inputs ([8.11](../08-troubleshooting/8.11-reproducing-and-isolating.md)).

<a id="what-the-two-document-writers-do-with-what-you-leave-out"></a>

## How settings writers handle omitted fields

![Reference](../_assets/icons/reference-light.svg) Organisation settings and fleet specs handle omitted fields differently. GitOps adds another step by supplying values before sending the request. Check the writer’s behavior before applying a partial document.

<a id="the-organisation-settings-writer-patches"></a>

### Organisation settings: patch behavior

The organisation settings writer reads the stored document, applies your request body, and saves the result. Omitted fields generally retain their stored values, so you can change one setting without sending the whole document.

These six cases modify or reset values during that patch:

| What you omit or send | What the writer does |
|---|---|
| `mdm.ios_updates.update_new_hosts` and the iPadOS equivalent | Wiped back to unset on every save, whatever you send. **Only the macOS form of that setting is honoured** |
| The Windows Entra allowlists, **omitted or sent empty**, in a request that also turns Windows device management off | Both lists are emptied, with an activity for each identifier removed. **Send either list non-empty in that same request and the request is rejected instead**, saying the identifiers cannot be set while Windows device management is off. Nothing saves, and Windows device management does not turn off either |
| `mdm.windows_migration_enabled`, in that same request | Forced off unless you re-assert it explicitly |
| The Windows Entra client identifiers, when you do send them | Stored lower-cased and de-duplicated, so a read-back is not byte-identical to what you sent |
| `org_info.contact_url`, when the merged result is empty | Replaced with Fleet's own default |
| `server_settings.enable_analytics`, on a tier not permitted to disable it | Forced on |

Four server-owned status settings ignore supplied values: Apple device-management enablement and configuration, Apple Business Manager configuration, Android configuration, and expired Apple Business Manager terms. Fleet restores their stored values before saving, allowing a configuration read to be sent back without failing. A GitOps declaration for these fields can therefore apply successfully without changing them.

> Windows device-management enablement is writable. Changing it records an activity.

The Free-tier reset described above also runs on every organisation-settings save.

<a id="four-blocks-are-replaced-wholesale-but-only-on-request"></a>

### Organisation settings: four blocks with overwrite behavior

The organisation settings route accepts an overwrite option. When enabled, omitted single sign-on, features, MDM end-user authentication, and Apple account provisioning blocks are cleared. Within Fleet’s clients, GitOps sets this option; `fleetctl apply` and the interface do not.

> Any caller with permission to write organisation settings can set the overwrite option. A script that sends the same request as GitOps will get the same clearing behavior, without a separate indication in the response.
>
> Historical-data sub-keys are an exception: when omitted under overwrite, they default to on. This prevents an older client from unintentionally stopping collection and triggering a data scrub.

<a id="the-fleet-spec-writer-patches-and-then-stops"></a>

### Fleet specs: patch behavior and exceptions

**A direct write to the fleet spec route preserves most of what you omit**, sub-key by sub-key: the update settings for each platform, disk encryption, the BitLocker requirement, the recovery-lock password, `mdm.name_template`, the custom-settings lists on Windows and Android, scripts, software, secrets, host expiry, the webhooks and the integrations. `agent_options` has a three-state contract of its own: absent keeps it, an explicit null clears it, and a value replaces it whole.

These five fields reset on omission:

| Field | On omission |
|---|---|
| **The whole `features` block** | **Replaced against Fleet's built-in defaults rather than merged.** Naming the block and omitting a sub-key reverts that sub-key too, so a partial `features` block silently resets what it does not mention |
| `setup_experience.enable_end_user_authentication` | Off |
| `setup_experience.lock_end_user_info` | Forced to follow the setting above, so with both omitted, off |
| `setup_experience.require_all_software_macos` | Off |
| `setup_experience.require_all_software_windows` | Off |

End-user authentication and the two software requirements are plain booleans in the request format, so they cannot distinguish an omitted value from false. For example, applying a fleet spec that omits end-user authentication turns off a value previously enabled through the interface, without an error or warning.

`lock_end_user_info` is optional and preserves an explicit true or false. When omitted, it follows end-user authentication to preserve the behavior from before this setting was configurable.

Three other setup-experience settings receive a default only when their stored value has never been explicitly set: manual device release, local administrator account creation, and that account’s type. These are one-time migration defaults.

<a id="then-the-gitops-client-changes-the-question"></a>

### Values supplied by the GitOps client

GitOps supplies a value for every block it manages. A key omitted from YAML may therefore arrive at the server as an explicit empty or default value, which the API then applies.

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

<a id="reading-the-effective-value-and-what-fleet-does-not-keep"></a>

## Checking the effective value and change history

![Troubleshooting](../_assets/icons/troubleshooting-light.svg) When a setting behaves differently from the value you saved, use these surfaces to compare stored intent with the running configuration.

| Plane | The stored intent | What is actually in force | Who changed it |
|---|---|---|---|
| **Server process** | A configuration dump, **which starts a new process** | **Partly.** The configuration API returns a live subset from the running server, named below. The rest goes unreported | Not retained |
| **Organisation settings** | The API or the interface | **Close, but not the same.** Reads are served from a cache held about a second | **By exception only.** See below |
| **Settings for a fleet** | The API or the interface | **Not the same.** A fleet's agent options, its features and its device-management configuration are cached about a minute each | An activity, for the changes Fleet names. The recorded file name is the only writer marker **stored on the settings row itself** |
| **Agent options** | The API | Inspect the host’s active configuration | Recorded as an edit |
| **Host-local** | The host's own files | The host | Not retained |
| **Enforced on the device** | Fleet's desired state | The device's report | Per platform ([a.6](a.6-glossary-and-release-compatibility.md)) |

> A configuration dump starts a new process and reports what that invocation loads. It does not inspect the running server, so it may differ after a configuration file or deployment definition changes. It also omits direct environment reads outside the configuration manager.
>
> The configuration API exposes a live subset from the running service:
>
> | Section | Coverage |
> |---|---|
> | Update intervals | The osquery detail and policy update intervals; no cron, webhook, or schedule intervals |
> | Vulnerabilities | The full block, around ten keys including the database path and feed URLs |
> | Logging | Debug and JSON flags, plus resolved status, result, and audit log destinations |
> | Email | Present only for Amazon SES. With the default SMTP backend, the SMTP settings returned elsewhere come from the database |
> | Sandbox, partnerships, licence | The sandbox flag, one partnership key when enabled, and decoded licence claims |
>
> The exposed partnership key is not the one controlling the transparency URL. The API therefore cannot explain that URL’s precedence. Any authenticated role, including a fleet-scoped observer, can read this live subset. The endpoint’s admin restriction covers only the database-stored SMTP, single sign-on, and agent-options fields.
>
> Around twenty of the 320 registered process keys are visible through this API. For the remaining registered keys, a configuration dump shows a fresh load of the inputs rather than the values held by the running server.

> Each Fleet instance caches organisation settings for about a second and fleet settings for about a minute. Immediately after a change, hosts checking in through different instances can receive different values. The write response reads stored data directly and bypasses these caches, so a successful read-back does not confirm that every instance has refreshed. Allow the longer cache period before investigating a change that seems unapplied ([1.6](../01-foundations/1.6-the-fleet-server.md)).
>
> Device-management assets use a checksum in their cache key, read fresh on each lookup. A rotated certificate is therefore picked up on its next use; an old cached copy can remain in memory until it expires without being used.

For agent options, inspect each consumer on the host. Fleet does not publish a reconciliation between the stored document and the values in use. A live query can inspect osquery; update channels, extensions, debug state, and script behavior need the relevant host files, process state, or logs.

The osquery detail query selects a configuration hash but Fleet retains only the version from that introspection row. It therefore does not provide a stored hash to compare against desired configuration. This collection runs on the detail interval or a forced refetch, not every poll. Hosts without osquery, including iOS, iPadOS, and Android devices, do not contribute this data.

<a id="the-audit-trail-is-by-exception"></a>

### Which settings changes produce activities

Organisation-settings changes can produce forty-two distinct activity types. One save may produce several records: agent options are a single type covering the whole block regardless of how many options change, while the Entra identifier types fire once per identifier added or removed. Among the forty-two are disk encryption on and off, Windows device management, the minimum operating system versions, the Google Workspace integration, conditional access, the historical datasets and GitOps mode.

Enrollment secrets use a separate route and activity. That activity is written only when the set of secret values changes; submitting the same secrets in a different order writes nothing.

Twenty of these types also come from other writers. The fleet writer emits the same types for the minimum operating system versions on all three Apple platforms, the macOS and Windows update settings, disk encryption on and off, recovery-lock passwords, conditional access, agent options and the historical datasets. The setup-experience authentication pair and the managed-local-account pair come from the Apple setup writer. The deleted organisation logo has its own endpoint. Check the event’s context before attributing one of these types to an organisation-settings change. The remaining twenty-two, among them the Windows device-management types, the Entra identifier types and the GitOps-mode types, are written on this path alone.

> Disk-encryption activities need particular care. The fleet writer and Apple disk-encryption path emit both enabled and disabled events. Uploading an Apple push certificate emits enabled events for the unassigned fleet and every fleet already enforcing encryption. A single upload can therefore produce events for scopes whose encryption settings were unchanged. The activity type alone does not identify the affected scope or the writer.

Three of the forty-two activity types are best effort: deleted organisation logo and the two historical-dataset types. Their requests can succeed even if activity creation fails; the failure is logged. The other thirty-nine fail the request if they cannot record the activity.

There is no catch-all activity for the organisation settings document. Changes to fields without a dedicated activity type, such as SMTP settings, the server URL, or the host expiry window, leave no entry. Use the feed to review the changes Fleet records, and keep another change record when you need complete settings history ([1.5](../01-foundations/1.5-audit-and-activity.md)).

<a id="what-the-device-says-back-and-what-fleet-keeps-of-it"></a>

## Device reports and the state Fleet retains

![Explanation](../_assets/icons/explanation-light.svg) Fleet records reports from devices to track whether desired configuration has taken effect. The evidence behind those reports varies by platform and profile type.

Per-profile status uses the same four names across the three platforms: `pending`, `verifying`, `verified`, and `failed`. The profile’s class determines which states it can reach and what each state confirms.

| Platform and class | How it reaches `verified`, and what happens after |
|---|---|
| **macOS, ordinary profile** | An acknowledgement moves it to `verifying`. **A routine inventory check, hourly by default, moves it to `verified` once it sees the profile installed.** Should the profile later leave the device, the same check notices, Fleet re-pushes up to three times, and only then marks it `failed`, with a detail recording that it had previously been confirmed |
| **iOS and iPadOS, ordinary profile** | **An install acknowledgement goes straight to `verified`**, skipping `verifying`, because there is no agent on the device to look. A device answering that it is busy stays `pending` |
| **Any Apple platform, declarative profile** | The device's own status report drives it, and **an active and valid report records `verified` directly**, so the normal path skips `verifying` here too |
| **Windows, ordinary profile** | **A successful response maps directly to `verified`**, and nothing re-checks it afterwards. An empty response is `pending`; anything else becomes `failed` after one retry |
| **Windows, profile whose certificate Fleet brokered** | **Deliberately held at `verifying` despite a successful response**, and moved to `verified` only once the issued certificate appears in the host's certificate inventory. **So Windows does reach all four states**, in this class |
| **Android, any profile** | `pending` before delivery, then `verified` or `failed` once Google reports back. **Nothing sets `verifying` on this platform** |
| **A third-party management provider** | Only what the device itself reports, through ordinary inventory. Fleet holds no channel to the other provider, so this is observation rather than knowledge |

> ### What `verified` confirms on each platform
>
> For ordinary macOS profiles, Fleet continues checking inventory after verification. If the profile disappears, the next check, hourly by default, triggers retries and can eventually mark it failed.
>
> For iOS, iPadOS, and ordinary Windows profiles, `verified` records a successful device acknowledgement. That path does not revisit the installation, so a later removal may leave the status unchanged.
>
> Compare verified counts with these differences in mind. Where you need confirmation of current state, check the device ([8.9](../08-troubleshooting/8.9-windows-mdm-diagnostics.md)).

> ### Windows profiles with brokered certificates
>
> The additional inventory check applies when Fleet brokers the certificate request for that host and profile through a custom SCEP proxy, NDES, or Smallstep. DigiCert is excluded. A profile that installs a certificate through another route follows ordinary Windows profile behavior and moves directly to `verified` after a successful response.
>
> If a brokered certificate appears in inventory after the profile was marked `failed`, the profile can recover to `verified` automatically.

Removal has two useful exceptions. Windows treats several not-found responses as successful removal because the profile is already absent. A successful Apple removal deletes the record, so the profile disappears from the host’s list instead of receiving a final state.

On Apple and Windows, Fleet is the management authority and there is no separate external provider acceptance stage. Device acknowledgement and confirmation of enforcement can still be separate, as the macOS inventory check shows.

<a id="android-retains-four-things-and-publishes-one-of-them"></a>

### Android policy records and API visibility

The configuration-profile API exposes Android’s derived per-profile progress in the same format as other platforms. You can distinguish delivery progress from a profile that has not started. Some supporting records remain internal:

| Retained | Exposed through an API |
|---|---|
| The profile you authored | **Yes** |
| The policy payload Fleet actually sent to Google, after merging | **No** |
| Google's response to that submission, and the policy version it assigned | **No** |
| The version the device reports as applied, and when it last synchronised | **No** |

On Android, Fleet separately stores Google’s acceptance and the device’s report. Those records can establish whether Google accepted a policy that the device has not yet applied, but neither is published through the interface or API. Inspecting them requires database access ([8.10](../08-troubleshooting/8.10-android-diagnostics.md)).

### Two collision rules at the device boundary

Android merges a host’s eligible profiles into one policy. A network profile waiting for a referenced certificate is excluded from the merge and held at `pending` until that certificate is verified or finally fails. Its detail names the certificate it is waiting for. Either terminal certificate outcome releases the profile for another delivery attempt.

Eligible profiles are merged alphabetically by name. If two set the same top-level field, the later name wins and the other profile is marked `failed`, with the conflicting fields named in its message. Check for these overlaps before renaming or adding a profile, since either change can affect a previously working profile.

Windows rejects a custom profile targeting operating-system updates when the organisation or fleet already manages them through settings. Profile-based update management requires Premium, cleared update settings, and no other profile targeting that area. Turn off the conflicting settings before uploading the profile.

> ### Apple commands and push failures
>
> Fleet queues the command before sending its push notification. The queued command remains pending even if the push fails, and the push response itself is not stored. The caller determines how the failure is reported:
>
> | Caller | Result of a failed push |
> |---|---|
> | **A host control:** lock, unlock, wipe, clear passcode, or manual refetch | Returns a gateway error and writes no success activity. The command remains queued for the next check-in, so the device may later execute it while Fleet still shows the earlier state |
> | **A background job:** profile delivery, scheduled refetch, declarative sync, device rename, or retry cron | Treats the queued command as success. A profile remains `pending` |
> | **Automatic recovery-lock or managed-local-account password rotation** | Writes the activity despite the failed push |
> | **A command targeting many hosts** | Returns an error if every push fails; otherwise succeeds and names the hosts it could not reach |
>
> Mac lock requests have a race-condition exception. If another request enqueues the lock first, Fleet pushes for the winning command. A failed push on this path is logged, but Fleet returns the PIN, reports success, and writes the success activity. The response does not identify this path.
>
> An inactive Apple device token changes stored state only during the scheduled iPhone and iPad refresh: Fleet disables device management for the host and fails pending app installs. Other callers, including lock, wipe, profile delivery, and manual refetch, do not make that state change. The scheduled job does not cover Macs.
>
> A pending command confirms that the command exists without a recorded device answer. It cannot distinguish a failed push from a successful push followed by no check-in. In either case, wait for or prompt a check-in ([8.8](../08-troubleshooting/8.8-apple-mdm-diagnostics.md)).

## Where Fleet's reference and the running server disagree

![Reference](../_assets/icons/reference-light.svg) The following differences were verified at this release. Check them when choosing a value or investigating a setting that appears to be ignored.

| Setting | The reference says | The server does |
|---|---|---|
| A per-endpoint request-size override | Documents it in full, with a default and a worked example | **The key does not exist.** Setting it does nothing and reports nothing |
| The Redis host-cache lifetime | 60 seconds | 180 seconds |
| The MySQL password default | `fleet` | Empty |
| The private-key external identifier | Names an environment variable without the middle component | That variable is not read. The documented form is silently ignored |
| The "secret key" for invite and reset tokens (`app.token_key`, default `CHANGEME`) | A secret that those tokens are generated from | **Never reads the key.** Invite and reset tokens are random text sized by `token_key_size`, so setting `token_key` changes nothing and its `CHANGEME` default is inert |
| The invite-token validity period | Its usage text ends "i.e. 1h" | Registers a five-day (`120h`) default. The "1h" is stale and contradicts the default the same key registers, which the catalog below shows correctly as `120h` |
| The session validity period (`session.duration`) | Its usage text ends "i.e. 4h" | Registers the same five-day (`120h`) default. The "4h" is stale in exactly the same way, so a login lasts five days rather than four hours unless you shorten it, which matters because it sets how long a stolen session stays valid |

Before relying on a published default, confirm it through the available configuration surface:

| Plane | How to establish the value in force |
|---|---|
| **Stored settings**, organisation and fleet | **Read it back**, allowing for the cache periods above. The API returns what the server stored, so a difference from what you sent is real and worth investigating |
| **Server process configuration** | **Partly.** For the live subset the configuration API reports, named above, read the running value back and trust it. **For everything else there is no read-back**: the configuration dump starts a fresh process and reports what *that* invocation would load, which need not match what the running server holds, and it omits every setting read directly from the environment. **Control the input instead**: pin the deployment definition, keep one source of truth for it, and treat a restart as the only thing that changes it |

For process keys outside the API’s live subset, keep the deployment inputs versioned and auditable. The running server provides no read-back for those keys, so a wrong default in the reference can be difficult to detect after startup.

## Version notes

![Reference](../_assets/icons/reference-light.svg) Verified against Fleet 4.90.0. The server's configuration manager registers **320 distinct keys** at this release.

The registered-key count covers the configuration manager’s bindings. It is not a count of documented settings: Fleet’s reference describes some keys in dedicated sections, others in prose or examples, and no reproducible comparison has been completed here.

## The complete configuration-key catalog

![Reference](../_assets/icons/reference-light.svg) This catalog was generated from the server’s configuration-registration calls at the pinned release. It lists the keys the binary binds and the defaults it registers. For those bindings and defaults, use this catalog when it differs from the published configuration reference.

For example, `redis.host_cache_ttl` registers 180 seconds and `mysql.password` registers an empty default. The documented per-endpoint request-size override has no registered key and does not appear. See [Where Fleet’s reference and the running server disagree](#where-fleets-reference-and-the-running-server-disagree) for other differences.

Read the columns as the key, the environment variable that sets it, the type, the default the server registers, and what it's for. A key marked *(hidden)* is bound and functional but kept out of `fleet serve --help`. A default marked *(computed)* is derived when the server starts rather than being a fixed literal, so the cell shows the value it resolves to, which for a few paths is relative to a directory the operating system chooses at runtime.

The “what it’s for” column uses each key’s registered usage string. The generator cannot read the `fmt.Sprintf` expression used for `server.tls_compatibility`, so that cell is blank even though the server has a description. All 320 registered keys are included. HTML comments on each row retain source locations for editors.

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
