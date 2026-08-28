# Part VII structure, agreed with the independent reviewer 2026-08-28

The third of these, after `part5-structure.md` and `part6-structure.md`. Verdict: **AGREED WITH
CHANGES**, and the changes are larger than Part VI's: two chapters change contract, two swap places.

## What changed from the stubs

**7.1 was "Day-two operations" and is now "Define the service operating model."** The reviewer's
ruling was blunt: that title invites exactly the leftovers chapter it looks like. It has a real
subject only as the design chapter for operating the service, owning outcomes, recovery objectives,
ownership, maintenance authority and the runbook portfolio. If it could not be given that subject it
should have been dissolved into the others.

**7.6 has been split.** "Maintain the manual for each release" and the feature-availability ledger
move to **A.6 Glossary and release compatibility**, which already has headings for both. Maintaining
this book is not an administrator's operation. 7.6 keeps the security half and becomes **"Maintain
credentials, certificates, and privileged access."** Release-note review belongs to 7.2;
security-advisory intake and emergency rotation stay in 7.6.

**Observability now comes before scaling.** The old 7.4 and 7.5 are swapped, because you cannot make
a capacity decision before you can see the signals it depends on. The files were renamed, which is
safe here only because nothing links to Part VII yet.

## The organising claim

> **Fleet's server processes are replaceable; the service is not.** Operating Fleet means preserving
> continuity of control through version change, state loss, load, dependency failure and credential
> expiry, and proving that Fleet's asynchronous work resumed rather than stopping at "the server is
> up."

It follows the two parts before it. Part V says devices must converge on published intent. Part VI
says a successful invocation is not convergence. **Part VII says a healthy process is not a healthy
service.**

Every chapter answers the same four questions: what continuity is protected, what can interrupt it,
what proves progress before and after a change, and what recovery action and stop condition were
decided in advance.

## The evidence rule, which is this part's hardest problem

I asked whether these chapters can be verified at the tag at all, and asked to be told now rather
than discover it mid-draft. The answer is that **three of the six are mostly operational judgement**,
and the discipline is a four-class ledger per claim rather than one stamp per chapter.

| Class | Establishes | Treatment |
|---|---|---|
| **Fleet contract, source checked at the tag** | State placement, supported topology, routes, telemetry, migrations, queues, cron behaviour, licence gates, certificate and key consequences | Cite the tagged file. **Only this class may claim Fleet 4.90.1 behaviour** |
| **Fleet reference deployment, tag checked** | Sizes, cloud services and alarms in Fleet's bundled reference architecture | An example or starting point, **never a capacity guarantee** |
| **Dependency or platform behaviour** | MySQL backup and PITR, Redis persistence and failover, object-store replication, load-balancer draining, cloud monitoring | Cite the exact vendor and supported version |
| **Operational practice, or measured on this deployment** | RPO and RTO, cadence, headroom, thresholds, retention, failover choice, restore sampling, measured migration duration | Label it as such |

A fifth label, **Not established**, is required where neither the product nor a vendor contract
settles it.

`verified_against: Fleet 4.90.1` may stay in frontmatter as the product target. **It must not be read
as verifying a recovery time, an eviction threshold, a backup command, an alert rule or a local
maintenance schedule.**

Expected mix, as editorial estimate rather than target: 7.1 roughly 80% judgement; 7.2 roughly 60 to
70% tag-verifiable; 7.3 roughly 30 to 40%; 7.4 about half; 7.5 roughly 25 to 35%; 7.6 about half.

**Mostly-judgement chapters are legitimate when they supply decisions, tests and explicit dependency
contracts. They become padding when they invent universal schedules, thresholds or cloud
procedures.** That sentence is the standard for this part.

## Source-checked findings that shaped the structure

- Fleet's published upgrade sequence stops **all** instances, replaces the release, runs the database
  preparation, then starts the new release. Its "5 to 10 minutes" is typical, **not a bound**.
- **Migrations are forward-only**; new down-migrations are no-ops. Rolling back after a schema
  migration needs a compatible pre-migration restore, not just the old binary. This is why 7.2 has to
  name the data-loss point explicitly.
- Activities, Apple MDM commands, Windows MDM commands and worker jobs all have tables, and graceful
  shutdown can record work as cancelled. That supports a before-and-after work ledger, but is **not**
  a guarantee that dispatched actions are recalled or replayed.
- The health endpoint checks MySQL and Redis, **not object storage**. Metrics exist only with
  configured authentication or an explicit opt-out.
- Vulnerability processing, maintained-app refresh, maintained-app advancement and VPP refresh are
  **four separate schedules**. A green health check proves none of them ran.
- Fleet scales horizontally against shared stores with **one writable primary**, and servers must
  reach a writer in the same datacentre. Cross-region is described for failover, **not active-active**.
- **An expired Premium licence still parses as Premium at this tag.** The server warns and responses
  carry an expiry header; there is no automatic demotion path in the code. That is observed 4.90.1
  behaviour and **must not be presented as a guaranteed grace period.**
- **"Certificate rotation" is not one operation.** HTTPS trust affects agent connectivity. The Apple
  MDM CA rollover deliberately retains the CA private key so older FileVault escrow stays
  decryptable. Replacing key-bearing material is the dangerous boundary, and 5.8 already documents
  what it costs.

## Ownership, abbreviated

The full table is long; these are the decisions that were genuinely in doubt.

| Subject | Owner | Boundary |
|---|---|---|
| MySQL, Redis and object storage | Not re-explained in Part VII at all | 1.6 owns their conceptual roles, 2.9 the initial topology, 8.6 key-level inspection. Part VII asks only three operational questions of them: what must be backed up (7.3), what shows they are unhealthy (7.4), what adds headroom (7.5) |
| Certificate expiry and rotation | **7.6** | 2.7 and 2.8 own initial configuration; 5.8 owns using recovery credentials; inclusion of the private key in the recovery set is 7.3's |
| The fleetd update channel | **3.7** keeps the mechanics | 7.2 owns release coordination, rings, promotion, abort and estate-wide verification |
| "How do I know the upgrade worked" | **7.2**, as an eight-rung acceptance ladder | If a rung fails, Part VIII owns evidence capture and cause isolation |
| Monitoring implementation | **7.4**, but only Fleet's side | Enable and protect the endpoints, preserve identity, prove exports arrive, design Fleet-specific indicators, test alert paths. Prometheus, Grafana, Alertmanager, CloudWatch and paging policy are vendor or local |
| Manual maintenance and feature availability | **A.6** | Moved out of 7.6. 0.1 states the target release |

**One cleanup falls out of this:** 2.12 should become a readiness gate and shrink its backup,
upgrade, certificate and monitoring explanations to links, and 8.14 should keep profiling and active
degradation diagnosis but point its reference sizing and steady-state monitoring material back to
2.9, 7.4 and 7.5.

## Where operate stops and troubleshoot starts

Part VII owns **planned control and proof**: baseline, threshold, change, canary, drill, acceptance,
abort, recovery.

Part VIII starts when a signal breaches without an explained planned change, when a planned operation
misses its acceptance criterion, or when recovery does not return the service to its declared
objective.

Part VII may require queue age to return to baseline; Part VIII inspects which row or channel is
stuck. Part VII may identify stale vulnerability data; Part VIII examines the cron statistics, the
logs and the network failure.

## Disclosure line

**Operationally specific, recovery-verifiable, and secret-minimising.**

**In:** store and secret classes; owners and expiry dates; safe renewal order and overlap; the
consequences of losing or replacing keys; health and telemetry endpoints; the recovery set's
composition at a high level; checks proving restored state is readable and that sampled protected
values remain decryptable **without displaying them**; redacted configuration; least privilege;
access-review evidence; retention consequences; canary and failover design; isolation warnings.

**Out:** real or realistic credentials, licence keys, private keys, tokens, recovery credentials or
database dumps; commands that print any of them into a terminal, shell history or process arguments;
bulk recipes for enumerating secret-bearing rows; cryptographic plumbing beyond its operational
consequence; **restored production state connected to real hosts, push services, identity providers,
webhooks or ticket systems**; authorization-gap research; customer topology; attacker-useful rotation
races.

The distinction between renewing a certificate and replacing key-bearing material must stay explicit
wherever it appears.

## The agreed outlines

### 7.1 Define the service operating model

1. **Name the service outcomes** — availability, control-loop freshness and administrative
   capability, defined separately from process uptime.
2. **Set service levels and recovery objectives** — local SLOs, a maintenance budget, RPO and RTO,
   each with a measurement and an owner.
3. **Assign operational ownership** — Fleet, MySQL, Redis, storage, TLS, MDM providers, identity,
   observability and support, mapped to named owners.
4. **Build the operating calendar** — change windows, drills, release review, access review and
   external expiry dates in one place.
5. **Define change gates and evidence** — a baseline, a canary, acceptance criteria, an abort
   condition and recovery evidence, decided before the change.
6. **Maintain the runbook portfolio** — one owned and exercised runbook per continuity risk.

### 7.2 Upgrade Fleet server and coordinate fleetd releases

1. **Treat server, fleetctl and fleetd as separate release trains.**
2. **Assess migrations and measure the window** — rehearse the exact migration set on
   production-shaped restored data.
3. **Prepare the change and the recovery point** — including declaring the rollback data-loss point.
4. **Account for work in flight** — MySQL queues, cancelled scheduled work, Redis and in-memory work,
   and already-dispatched actions are four different things.
5. **Upgrade every instance and migrate offline.**
6. **Prove the service resumed** — the eight-rung acceptance ladder.
7. **Roll out fleetd through established channels** — rings, monitoring, stop conditions.
8. **Recover from a failed upgrade** — a binary abort and a database restore are different
   operations.

### 7.3 Back up, restore, and retire service state

1. **Define the recovery objective and failure scope.**
2. **Inventory the complete recovery set** — including private keys and external infrastructure
   references.
3. **Protect MySQL and object storage coherently** — and document the consistency gap.
4. **Plan Redis loss and restart** — persistence or deliberate empty recovery, chosen from
   consequences.
5. **Restore into an isolated environment** — no production device or integration traffic.
6. **Verify semantic recovery** — including that protected values are still decryptable, without
   displaying them.
7. **Set retention and deletion order.**
8. **Rehearse disaster recovery** — measure, do not assume.

### 7.4 Observe progress, performance, and service health

1. **Measure service progress, not only uptime.**
2. **Collect Fleet-native telemetry** — configure and secure it, preserve identity.
3. **Know the coverage and sampling gaps** — what health omits, where traces sample.
4. **Monitor operational dependencies.**
5. **Monitor queues, scheduled work and feeds** — four separate schedules, none proven by a health
   check.
6. **Monitor log and integration delivery** — silence, backlog, rejection, oversize loss.
7. **Establish baselines and leading capacity signals.**
8. **Define and test alerts** — including testing the routing.

### 7.5 Maintain capacity and availability

1. **Start from Fleet's topology constraints.**
2. **Turn telemetry into a capacity decision.**
3. **Scale Fleet instances safely.**
4. **Scale MySQL, Redis and object storage by their own limits.**
5. **Design failure domains and regional recovery** — active/passive, not active-active.
6. **Test load and failover assumptions.**
7. **Review capacity after material change.**

### 7.6 Maintain credentials, certificates, and privileged access

1. **Inventory operational trust material.**
2. **Monitor expiry, advisories and entitlement.**
3. **Renew HTTPS trust without disconnecting agents.**
4. **Renew MDM certificates and tokens in the safe order.**
5. **Protect key continuity and recovery credentials** — renewal and key replacement are different
   acts.
6. **Rotate service and integration secrets.**
7. **Review privileged access.**
8. **Prepare for compromise.**
