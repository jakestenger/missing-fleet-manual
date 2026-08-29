---
title: "Configuration sources, scopes, and precedence"
chapter: "Appendices and indexes"
section: "A.3"
sidebar_position: 3
status: drafting
verified_against: Fleet 4.90.1
verified_on: 2026-08-29
verified_source: "drafted against fleet-v4.90.1 (dd0200f062) over three research rounds. Every source, resolution and exception was read from the code that performs it; where a claim rests on release history rather than the tag, the ledger says so. Citation ledger at research/section-notes/a.3-notes.md"
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

**On the host**, a further set: compiled-in agent defaults, what the installer baked in, what the service definition passes, local fallback files, the operating system keystore, the macOS configuration profile, and what the server delivers.

> ### The asset store outranks the server's own configuration, and only warns you
>
> The last row above is the one that surprises people, because it inverts the usual direction. Apple push certificates, the Apple Business Manager token, Android and Platform SSO material are first imported from the process configuration at first boot, **and after that the database is the authority.** The process configuration is checked only on a miss, so a certificate supplied by environment variable is read once and never again.
>
> **Fleet tells you and does not stop you.** The startup log says it will ignore certificates provided by environment variable when this happens. So an operator who rotates a certificate by changing a deployment manifest, restarts, and sees no error has changed nothing, and the only evidence is a log line they had no reason to read.
>
> **The Apple Business Manager path breaks the same pattern in the other direction.** Its token file is parsed on every boot, *before* the database is consulted, so a broken or missing path is fatal at start for good, even though the parsed value is then discarded in favour of the stored one. A path that no longer needs to work still has to.

## Inputs that change the result without owning a value

![Explanation](../_assets/icons/explanation.svg) Several things shape what a device ends up with and are **not** authorities, and treating them as peers of the list above is the commonest way to reason wrongly about this.

| | What it does |
|---|---|
| **Labels, fleet placement, platform, licence** | *Select* which hosts a value reaches. They do not compete for the value |
| **Fleet secret variables, host attributes, identity-provider attributes** | *Substitute* into a value at delivery, changing what the device receives without authoring it |
| **The device platform, and any external management provider** | *Enforce*, or fail to. They hold actual state, not Fleet's desired state |
| **GitOps** | **A writer, not a source.** Your repository may be your organisation's declared authority; Fleet sees an ordinary client writing ordinary stored state |

## How collisions resolve

![Reference](../_assets/icons/reference.svg) **There is no single precedence order, and expecting one is the mistake this section exists to prevent.** Two sources meeting produce one of six outcomes, and a single resolution path routinely uses three or four of them at once.

| Mechanism | What happens |
|---|---|
| **Precedence** | The stronger source's value replaces the weaker one's |
| **Fallback** | The second source is consulted only when the first produced nothing |
| **Write-through** | The weaker source rewrites the stronger one's store, then deletes itself |
| **Composition** | Both values combine, by OR, by a floor, or by merge-if-absent |
| **Mutual exclusion** | Setting both is a fatal error. There is no winner |
| **Channel disabled** | One setting removes the channel by which the other would arrive, so no comparison ever happens |

**The last one is categorically different and worth its own sentence.** Nothing is compared and no value loses: the receiver is never registered, so the server's value never reaches the host at all.

**Within the server's process configuration the order is stable**, and it is the one place a simple rule holds: an explicitly set flag beats a non-empty environment variable, which beats the configuration file, which beats the built-in default. An empty environment variable is ignored rather than treated as a value.

### Where several mechanisms meet

**Agent credentials on the host use four at once.** Supplying both the secret and its file path is a fatal error at start. A non-empty secret file rewrites the keystore and then deletes itself. The keystore is consulted only when nothing is set. And the macOS configuration profile beats both the flag and the environment, unconditionally.

> **That last one has a comment above it describing a check the code does not make.** The comment says the profile applies only when neither value is already set. It applies regardless. The behaviour is the profile winning, and a reader who trusts the comment will predict the opposite.

**Update channels combine write-through with a disabled channel.** The persisted overrides file overwrites both the flag and the environment when it is read at start. Disabling updates removes the receiver that would ever write that file, so **with updates disabled the last override written stays in force permanently and the server has no say at any point.**

## Agent options resolve per consumer, not once

![Troubleshooting](../_assets/icons/troubleshooting.svg) **This is the single most consequential precedence question in Fleet, and it has more than one answer**, because more than one consumer reads the document.

**The osquery half** takes the fleet's document whole when the fleet has one, and the global document when it has none. **Never a mix.** So "a fleet with no options of its own falls back to global" is true when the fleet has no agent options at all, and false when the fleet has a document that omits a setting: the setting does not come from anywhere ([1.3](../01-foundations/1.3-hosts-fleets-labels.md)).

**Platform overrides replace rather than merge.** A platform override for a host's platform replaces the base configuration entirely, so it has to be complete.

**The Orbit half is a separate path with a different rule.** Update channels, command-line flags and extensions are read from the fleet's own document with **no fallback at all**, not even when the fleet has no document. Only the script execution timeout falls back, which Fleet's source states in words, and its condition tests for zero, so an explicit zero is indistinguishable from unset.

**Two settings compose rather than resolve.** The macOS profile may *enable* scripts and cannot disable a locally enabled value. And a locally set debug flag cannot be lowered by the server sending false: the local value is a floor.

## What GitOps does with what you leave out

![Reference](../_assets/icons/reference.svg) **The answer depends on the writer, not on the field**, which is why a single rule has never worked here.

**The ordinary API preserves what you omit.** It patches the stored document.

**The server replaces four blocks wholesale** whenever a spec is applied, whatever applied it. So **omitting the single sign-on block clears it**, and the same is true of the features block, the MDM end-user authentication block, and Apple account provisioning.

**The GitOps client mostly resets.** Omitted YARA rules are converted to an empty list and therefore cleared. Omitted certificate authorities are cleared too, and by a less obvious route: the run queues a second pass that re-applies the empty grouping with deletion enabled, so the emptiness is acted on after the main apply rather than during it. Omitted conditional access is left alone. Activity expiry and host expiry are left alone.

**Nine keys survive omission**, among them organisation information, Fleet Desktop and the vulnerability settings. [6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md) is the field-level account; this is the rule behind it.

## Reading the effective value, and what Fleet does not keep

![Troubleshooting](../_assets/icons/troubleshooting.svg) A precedence table nobody can apply to a live system is a description rather than a tool. This is where a reader with a value in front of them that is not what they set goes next.

| Plane | The stored intent | What is actually in force | Who changed it |
|---|---|---|---|
| **Server process** | A configuration dump, **which starts a new process** | **No surface reports it** | Not retained |
| **Organisation settings** | The API or the interface | The same | **By exception only.** See below |
| **Fleet settings** | The API or the interface | The same | The file name a GitOps run recorded, and nothing else |
| **Agent options** | The API | **Only the host knows.** Ask it | Recorded as an edit |
| **Host-local** | The host's own files | The host | Not retained |
| **Enforced on the device** | Fleet's desired state | The device's report | Per platform ([a.6](a.6-glossary-and-release-compatibility.md)) |

> **The server-process row is the one to read twice.** The configuration dump does not introspect the running server: it starts a fresh process and dumps what *that* process loads. So it can differ silently from what is in force after a configuration file or deployment definition has changed, and it omits every setting read directly from the environment rather than through the configuration manager. **Fleet has no surface that reports the running server's effective configuration.**

**Agent options are the plane where stored and in-force genuinely diverge**, and Fleet publishes no reconciliation. Reading the host is the only method, and it has to be a live query, because the routine detail collection gathers four flags and nothing else. **Fleet asks every host for its configuration hash on every detail cycle and discards it**, which is the one piece of evidence that would answer the question directly.

### The audit trail is by exception

**The organisation settings document is audited by exception rather than as a document.** Around forty specific changes each write their own activity: agent options, enroll secrets, disk encryption, Windows device management, minimum operating system versions, the integrations, GitOps mode.

**There is no activity for the document itself and no fallback.** Every one of those writes is guarded by a condition on its own block, so a change to a part with no dedicated type writes nothing at all. Changing SMTP settings, the server URL, or the host expiry window leaves no entry. **The feed is silent rather than incomplete**, which is worse, because nothing indicates a settings change happened ([1.5](../01-foundations/1.5-audit-and-activity.md)).

## Where Fleet's reference and the running server disagree

![Reference](../_assets/icons/reference.svg) Verified at this release, and listed because each one changes a decision or a diagnosis rather than to keep score.

| Setting | The reference says | The server does |
|---|---|---|
| A per-endpoint request-size override | Documents it in full, with a default and a worked example | **The key does not exist.** Setting it does nothing and reports nothing |
| The Redis host-cache lifetime | 60 seconds | 180 seconds |
| The MySQL password default | `fleet` | Empty |
| The private-key external identifier | Names an environment variable without the middle component | That variable is not read. The documented form is silently ignored |

**Read per-key defaults out of Fleet's reference with that in mind**, and confirm anything you are about to depend on by reading the value back rather than by trusting the published default.

## Version notes

![Reference](../_assets/icons/reference.svg) Verified against Fleet 4.90.1. The server's configuration manager registers **320 distinct keys** at this release.

**This appendix deliberately publishes no count of how many of those Fleet documents.** An earlier draft did, and the comparison was withdrawn because "documented" had not been defined consistently enough for the number to mean anything: a setting can have its own reference section, be described in prose under another, or appear only in an example. **The count of registered keys is derived and stated; the comparison is not, until it can be produced reproducibly.**
