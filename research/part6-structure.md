# Part VI structure, agreed with the independent reviewer 2026-08-28

The same job that `part5-structure.md` records for Part V, done once for Part VI before any of its
five chapters was outlined individually. Verdict: **AGREED WITH CHANGES.** Five chapters kept; their
contracts sharpened.

## The organising claim

> **Fleet exposes one control plane through several paths.** Reliable automation gives every field
> and action one owner, uses the appropriate declarative, request-driven, or event-driven path, and
> verifies the resulting state rather than trusting a successful invocation.

The last clause is the part's through-line and the thing most of its warnings come back to. A
successful invocation is not convergence, and Part V spent six chapters establishing why.

## Why five chapters and not three

The obvious objection is that GitOps, the REST API and `fleetctl` overlap: `fleetctl` is a client of
the API, and GitOps is a mode of `fleetctl`. The reviewer's ruling is that they are not three
equivalent control planes and should not be presented as one chapter:

- **GitOps** owns declarative reconciliation.
- **The REST API** owns custom programmatic reads and actions.
- **`fleetctl`** owns the supported shell client: contexts, output, exit status, CI mechanics.
- **Webhooks** own event-driven handoff.
- **6.1** owns what all four share.

`fleetctl gitops` parses Fleet's YAML model, reads current state, and performs a *sequence* of API
operations. It is not a server-side API and not a repository watcher, and a real run can stop partway
with some operations already applied. Its `--dry-run` means "validate", not "produce an atomic
execution plan". That single fact is why 6.2 cannot be folded into 6.4.

**The division only works if authentication, secrets, testing and verification stop recurring in
every interface chapter.** Hence the ownership table below.

## Once-only ownership

| Subject | Canonical owner | Boundary |
|---|---|---|
| Identity, roles, token lifetime, ownership, rotation | **2.3**; 6.1 adds a short automation bridge | 6.2 to 6.5 cross-link only. Never repeat token creation |
| API token versus "bearer token" | **6.1** | Bearer is the HTTP scheme, not a second kind of token |
| How `fleetctl` holds credentials | **6.1** for the security consequence, **6.4** for the context commands | 6.4 does not re-explain identity |
| GitOps' relationship to the API | **6.2** | 6.3 must not reverse-engineer GitOps |
| Fields in GitOps but not REST, and the reverse | **6.2**, as a capability table | GitOps YAML is not a serialised REST resource. An exhaustive index can live in a.5 |
| Pagination, filtering, HTTP errors, rate limits, versioning, deprecation | **6.3** | 6.4 covers only how `fleetctl` surfaces an error or a version mismatch |
| General secret governance | **6.1**, on 2.3 and 7.6 | Ownership, storage class, rotation, redaction, incident response |
| GitOps secret injection and generated files | **6.2** | CI secret stores, substitution, placeholders, `generate-gitops` |
| Secrets inside scripts or profiles | **5.3** and **5.2** | Part VI explains only how CI supplies them |
| Webhook receiver credentials and destinations | **6.5** | Receiver authentication, URL handling, rotation, logging |

### The authentication correction the part must make

Fleet treats the value returned by login as a **session key**, and extracts that same value from
`Authorization: Bearer …`. Regular-user sessions follow the configured inactivity duration; API-only
sessions are unlimited. `fleetctl` stores the token in a named context in its configuration file,
created mode `0600`.

**So there is no distinct "automation bearer token."** Automation uses an API-only user's API token,
transmitted with the Bearer scheme. The part should say this plainly, because the opposite
assumption is common.

## What the stubs did not mention and the part needs

- **Brownfield migration to GitOps** (6.2). `fleetctl generate-gitops` exports current configuration,
  deliberately omits sensitive values, and has release-specific export gaps needing manual review.
- **Omission and deletion semantics, rename handling, GitOps exceptions, reconciliation cadence,
  concurrent-run prevention, partial application** (6.2). And re-applying a prior commit as recovery,
  which must **not** be called "rollback" as though it were atomic or could reverse device-side
  effects.
- **What happens when GitOps and the UI disagree** (6.2). The next apply governs resources GitOps
  owns. GitOps mode makes supported UI controls read-only but is **not** a general API authorization
  boundary: API writers can still create drift between runs.
- **A common test ladder** (6.1), with each interface chapter supplying only its own mechanism.
- **Endpoint-specific idempotency** (6.3). Fleet 4.90.1 documents no general `Idempotency-Key`
  contract, so the chapter must not tell readers to retry every failed write.
- **Pagination and rate limiting are not global rules** (6.3). Page/per-page plus optional cursor
  `after`, with per-endpoint defaults and limits; `429` and `Retry-After` documented for login, with
  limiters attached to selected routes.
- **Versioning and deprecation** (6.3), including not treating `/latest` as a stable external
  contract merely because `fleetctl` uses it internally.
- **Per-webhook contracts** (6.5). Activity, failing-policy, vulnerability and host-status webhooks
  differ in trigger, batching, retry and duplicate behaviour. They are not one mechanism.
- **Receiver security as a section, not a footnote** (6.5).

### Terraform: no chapter

The tagged public tree ships no first-party Terraform provider for *configuring* Fleet. Its Terraform
material is about deploying Fleet infrastructure, which is Part II's. A short note in 6.1 should
distinguish deploying the service (Part II), managing its contents (GitOps or REST, Part VI), and
unverified third-party providers (outside this manual). Do not broaden that into a claim that no
community provider exists anywhere.

## Cross-part seams

| Owner | Part VI may | Part VI must not |
|---|---|---|
| **2.3** identities | Apply the identity model to clients, CI, receivers | Re-teach roles, restrictions, token creation, rotation |
| **2.4** server settings | Show how GitOps or REST represents a known setting | Explain what settings mean |
| **2.5** audit logs | Use activity as change evidence | Reconfigure log destinations |
| **5.1** targeting | Encode an already-chosen target, add pipeline gates | Re-teach targeting, rings, queues, cancellation |
| **5.2 to 5.8** | Show generic patterns, link to examples | Re-explain profiles, scripts, software, updates, commands, encryption |
| **5.9** policy automation | Configure webhook, ticket and calendar destinations; operate receivers | Re-explain triggers, remediation loops, queue bounding |
| **Part VII** | Pin client and API contracts, prepare compatibility tests | Own upgrades, backups, availability, monitoring, release execution |

## Disclosure line for the part

The 5.8 formulation, adjusted: **operationally specific, exploit-path restrained.**

**In:** how API-only and regular-user tokens differ operationally; that Bearer is a transport scheme;
where `fleetctl` stores a token and how to keep it out of shell history and CI logs; least-privilege
roles and endpoint restrictions; **that built-in webhook requests are not signed at 4.90.1**; payload
sensitivity, HTTPS, receiver authentication, validation, deduplication, replay; rotation and
revocation outcomes; benign examples with placeholder tokens.

**Out:** real or realistic credential values; commands that put a token in shell history or process
arguments; bulk extraction workflows; sensitive recovery-credential endpoints; internal token storage
or retrieval plumbing; authorization-gap research or route chains that turn a leaked credential into
a recipe; internal-network pivot recipes through webhook destinations; receiver examples that execute
an incoming field without an allowlist.

The line deliberately **permits** stating that Fleet does not sign its outbound webhook POSTs.
Concealing that would cause insecure receiver designs, which is the opposite of the point.

## The agreed outlines

### 6.1 Design safe automation and control change

1. **Choose the automation path and declare ownership** — declarative state, direct requests,
   supported CLI work, event-driven workflows; one writer per field or action.
2. **Authenticate automation clients** — 2.3's identity model applied once: API tokens, Bearer
   transport, regular sessions, API-only tokens, scopes, how `fleetctl` contexts consume the same
   credential.
3. **Manage automation secrets** — ownership, storage, injection, rotation, redaction, revocation;
   GitOps substitution deferred to 6.2, script and profile payloads to Part V.
4. **Design for repetition and ambiguous outcomes** — idempotency, read-before-write, stable
   identifiers, change detection, concurrency control, partial failure.
5. **Test before production** — validation, contract tests, a non-production instance or test fleet,
   bounded production scope, explicit promotion gates.
6. **Review, verify and recover** — approval evidence, attributable execution, live-state and
   device-state verification, stop conditions, a recovery path.

One diagram belongs here, showing the paths without pretending they are interchangeable.

### 6.2 Manage Fleet with GitOps

1. **Understand Fleet's GitOps execution model** — repository YAML parsed by `fleetctl`, compared
   with live state, translated into a sequence of REST operations.
2. **Design the repository and configuration boundaries** — global, Unassigned and per-fleet files,
   referenced assets, naming, environment separation, ownership.
3. **Know what GitOps owns and can represent** — the canonical GitOps-versus-REST capability table,
   client-side fields, API-only fields, exceptions, release-specific gaps.
4. **Migrate from click-ops** — `generate-gitops`, omitted or placeholder content, a baseline,
   deliberate exceptions, one ownership boundary at a time.
5. **Supply secrets without committing them** — CI secret stores, environment substitution,
   `FLEET_SECRET_` handling, generated-file review, safe logs.
6. **Validate, review and apply** — strict parsing, matching client and server versions, pull-request
   dry runs, protected branches, serialised production applies, deletion flags.
7. **Resolve drift, partial applies and UI/API disagreement** — reconciliation cadence, GitOps mode's
   UI boundary, out-of-band API changes, omitted-resource deletion, reruns, recovery by applying a
   known repository state.

### 6.3 Use the Fleet REST API

1. **Start from the documented resource and scope** — endpoint, role, global or fleet scope, request
   shape, result contract, without duplicating the owning feature chapter.
2. **Build and authenticate a request** — URL construction, headers, content types, benign examples;
   token selection and lifecycle referred back to 6.1 and 2.3.
3. **Page, filter and order complete result sets** — endpoint-specific page sizes, stable ordering,
   cursor or page iteration, response metadata, large payloads.
4. **Handle errors, limits and ambiguous writes** — authentication, authorization, validation,
   conflict, selected `429` behaviour, server failure, timeout; retry only where semantics permit.
5. **Design idempotent and observable clients** — stable business keys, state checks, structured
   logs, correlation data, verification reads.
6. **Version and test the integration contract** — documented routes, deprecated routes and fields,
   fixtures pinned to the release, compatibility tests before Part VII upgrades production.

### 6.4 Operate Fleet with fleetctl

1. **Install and match fleetctl to the server** — installation, version checks, mismatch warnings,
   the boundary with Part VII's upgrade procedure.
2. **Configure connections and contexts safely** — addresses, custom CAs, URL prefixes, named
   contexts, token storage, without re-teaching identity.
3. **Choose the appropriate command surface** — native commands, one-off `apply`, raw `fleetctl api`,
   `fleetctl gitops`; semantics deferred to 6.2 and 6.3.
4. **Use commands without duplicating feature chapters** — discovery and composition, linking to
   owning chapters.
5. **Consume output and failures in automation** — structured output where available, standard output
   and error, exit status, deprecation warnings, partial results.
6. **Run fleetctl in CI and troubleshoot the client boundary** — isolated configuration, secret
   injection, deterministic versions, diagnostics; server health handed to Parts VII and VIII.

### 6.5 Connect integrations, webhooks, and external workflows

1. **Choose event delivery, polling or a native integration** — Fleet webhook, REST polling, Jira or
   Zendesk, Google Calendar, or another part's identity and log integrations.
2. **Configure destinations and ownership** — webhook URLs and native destinations owned here; policy
   trigger semantics left to 5.9, IdP and SCIM setup to 2.2.
3. **Understand each webhook contract** — activity, failing-policy, vulnerability and host-status
   payloads compared: trigger cadence, batching, success criteria, retries, duplicates.
4. **Secure the receiver** — no Fleet-supplied request signature at 4.90.1; HTTPS, an authenticating
   boundary, schema validation, input limits, least-privilege downstream credentials, careful logging.
5. **Build idempotent external workflows** — stable deduplication keys, receipt separated from side
   effects, replay and out-of-order tolerance, bounded calls back into Fleet.
6. **Observe, test and recover delivery** — recorded test payloads, receiver metrics, Fleet activities
   and logs, dead-letter handling, manual replay, credential and destination rotation.
