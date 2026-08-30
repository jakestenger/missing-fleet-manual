---
title: "Hands-on labs"
chapter: "Appendices and indexes"
section: "A.9"
sidebar_position: 9
status: drafting
verified_against: Fleet 4.90.1
verified_on: 2026-08-30
verified_source: "git tag fleet-v4.90.1. Every command, flag, endpoint, configuration key and metric a lab relies on was confirmed present at that tag before the lab was written; no lab depends on a capability that is not there."
reviewed_by:
reviewed_on:
further_reading:
  - https://fleetdm.com/docs/get-started/try-fleet
feature_requests:
  labels: [":product"]
  match: ["preview", "sandbox", "osquery-perf"]
  exclude: []
---

# Hands-on labs

![How-to](../_assets/icons/howto.svg) The rest of this book explains how Fleet works and what to do with it. This appendix is where you do it. Each lab takes one thing the book teaches and turns it into a short, self-contained exercise: a goal, the prerequisites, numbered steps that use only what a chapter already covers, a check that tells you it worked, a teardown, and an honest note on what the exercise proves and what it does not.

Wherever a lab can run without touching a real device or a production server, it runs inside `fleetctl preview`. Preview stands up a complete throwaway Fleet on your own machine, with simulated hosts already reporting, and tears down again in one command. It is the closest thing Fleet has to a practice range, and most of the conceptual labs below live in it. The labs that need a real device, a real MDM tenant, or a real deployment say so in their prerequisites, because preview cannot stand in for those.

Read a lab before you run it. Several touch destructive or irreversible actions, and each of those states its blast radius, the set of things a wrong step would damage, immediately before the step that carries the risk.

## The ten labs

![Reference](../_assets/icons/reference.svg) Each lab names the chapter that owns every concept it uses, so a step that assumes something sends you to where that something is taught.

| Lab | What you practise | Chapters it exercises | Edition |
|---|---|---|---|
| 1 | Preview as a sandbox | 3.1, 4.2, 6.4 | Free |
| 2 | Production bootstrap, at reading level | 2.2, 2.3, 2.4 | Free |
| 3 | Enroll one host of each channel | 3.1 to 3.8 | Free, some steps Premium |
| 4 | Policy to automated response loop | 4.3, 5.9 | Free, continuous mode Premium |
| 5 | Lost-device recovery | 5.7, 5.8 | Premium |
| 6 | Adopt GitOps | 6.2, 6.4 | Free |
| 7 | Certificate lifecycle | 2.13, 5.2 | Premium |
| 8 | Offline vulnerability pipeline | 4.4 | Free |
| 9 | Capacity validation | 7.4, 7.5 | Free |
| 10 | Failure-injection lab | 8.1 and the rest of Part VIII | Free |

## Lab 1: Preview as a sandbox

![How-to](../_assets/icons/howto.svg) Stand up a throwaway Fleet with simulated hosts, run a report against them, and take the whole thing down again. This is the environment the other conceptual labs assume, so it comes first.

### Goal

Prove you can start Fleet locally, see hosts reporting, run both a saved report and a live report, and explain what was local, what changed in your `fleetctl` configuration, and what a reset destroys.

### Prerequisites

- Docker running locally, and the `fleetctl` client installed. Preview brings up the Fleet server, MySQL and Redis as containers; [1.6](../01-foundations/1.6-the-fleet-server.md) explains what those three stores hold.
- No existing Fleet is required. Preview is self-contained and does not touch any server you already run.

### Steps

> **Blast radius: your `fleetctl` context file, `~/.fleet/config`.** Preview rewrites that file to point your client at the sandbox. If the file already exists and does not parse, preview overwrites the whole thing and every other context in it is lost. Back it up before you run preview on a machine that already has contexts.

1. Start the sandbox with pinned versions. `fleetctl preview --tag v4.90.1` pins the Fleet server image, but only the image. Preview also downloads its compose file and its simulated-host assets from the preview repository, at the ref given by `--preview-config`, which defaults to the mutable `main` branch. So `--tag` on its own does not freeze the environment: the server is pinned while the configuration and assets can still move under you. For a reproducible run, pin both, giving `--preview-config` an immutable ref such as this release's tag rather than a branch: `fleetctl preview --tag v4.90.1 --preview-config fleet-v4.90.1`. Without `--no-hosts`, preview also starts a set of simulated hosts that enroll themselves, which is what you want here. [6.4](../06-automate-fleet/6.4-use-fleetctl.md) covers `fleetctl` and its context file.
2. Note that preview has repointed your client at the local sandbox. Confirm where you are pointed by reading `~/.fleet/config`, or by printing one key with `fleetctl config get address`. This is the side effect to be aware of before you run `fleetctl` against anything else.
3. Open the local console at the address preview prints, and confirm the simulated hosts appear on the Hosts page. Enrollment as a lifecycle is [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md).
4. Run a live report: on the Queries page choose a built-in query such as one listing installed software, target the simulated hosts, and run it. A live report is the ad-hoc form; [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) explains the difference between a live report and a saved one whose results Fleet stores.
5. Save a report, let it run on its schedule, and compare the stored results with what a live run returns now. Stored results are a snapshot from the last scheduled collection; a live run reflects the hosts as they are at the moment you ask.

### Expected result

The Hosts page shows simulated hosts within a minute of startup, the live report returns rows from them, and `~/.fleet/config` shows your client pointed at the local preview context rather than at a real server.

### Cleanup

> **Blast radius: the sandbox only.** Reset erases every host, report and setting inside preview. It cannot reach a real Fleet, but it does throw away anything you built in the sandbox.

- `fleetctl preview stop` halts the containers and keeps their data, so you can resume.
- `fleetctl preview reset` deletes the sandbox entirely. Run it when you want a clean slate.
- If you pointed `fleetctl` elsewhere afterwards, set your context back with `fleetctl config set`.

### What this proves, and what it does not

It proves you can drive Fleet's query pipeline end to end and that you understand what preview changed on your machine. It does not prove anything about production: the hosts are simulated, the data is synthetic, and preview is a sandbox rather than a deployment. Labs 2 and 9 are where deployment and scale come in.

## Lab 2: Production bootstrap, at reading level

![How-to](../_assets/icons/howto.svg) Walk the first-run sequence for a self-hosted server, from an empty database to a first administrator, as a reading and dry-run exercise rather than a real deployment.

### Goal

Build a one-page first-run runbook: each stage that takes a self-hosted Fleet from nothing to an authenticated control plane, the command or endpoint that performs it, and the failure that stage prevents.

### Prerequisites

- The self-hosting chapters as your reference: [2.2](../02-administer-and-deploy-fleet/2.2-self-hosting-architecture-and-capacity.md) for sizing and the stores, [2.3](../02-administer-and-deploy-fleet/2.3-deploy-on-aws-or-gcp.md) for the AWS or GCP reference architectures, and [2.4](../02-administer-and-deploy-fleet/2.4-deploy-with-containers-or-virtual-machines.md) for containers or plain virtual machines.
- A disposable MySQL and Redis if you want to run the safe steps for real. None of this belongs on a server you rely on.

> **Blast radius: a throwaway database only.** The one step here that writes state is the schema migration in step 2. Point it at a scratch database, never at one that holds anything.

### Steps

1. Generate and set aside the server private key. Fleet reads it from the `server.private_key` setting, and it is what encrypts secrets at rest, so it has to exist before Fleet stores anything and has to survive restarts. [2.2](../02-administer-and-deploy-fleet/2.2-self-hosting-architecture-and-capacity.md) covers what the server keeps.
2. Prepare the schema. `fleet prepare db` runs the migrations against an empty database. Read what it reports; a server that starts against an unmigrated database is the missing-migration failure this step exists to prevent.
3. Configure TLS and start the server with `fleet serve`. Reading level here means understanding which settings terminate TLS and where the private key is read from, not exposing a real listener.
4. Confirm readiness. Fleet answers `/healthz` when it is up, which is the signal an orchestrator or load balancer waits on.
5. Create the first administrator. A brand-new server has no accounts, so the first one is created through the setup endpoint `/api/v1/setup`, which takes the administrator and organisation details and returns the first session. The `fleetctl setup` command is the client-side equivalent.
6. Log in, then restart the server and confirm the administrator, the organisation settings and the key-encrypted secrets are all still there.

### Expected result

Your runbook reads key, then migrate, then serve, then health check, then setup, with the failure each stage prevents noted beside it, and it says what breaks if any stage is skipped or reordered. If you ran the safe steps, `fleet prepare db` completed against the scratch database and nothing touched a real server.

### Cleanup

- Drop the scratch database and discard the containers.
- Destroy the throwaway private key. A real one is a long-lived secret; a practice one should not linger.

### What this proves, and what it does not

It proves you understand the first-run path and can spot where it is commonly cut short, at first-administrator creation. It does not prove a production deployment: there is no real TLS termination, no persistent storage, no availability, and no load. Take those to Part II proper and to Lab 9.

## Lab 3: Enroll one host of each channel

![How-to](../_assets/icons/howto.svg) Enroll a disposable device on each platform, record which enrollment channels it uses, then deliberately half-enroll one desktop and recover it.

### Goal

See for yourself that a host reaches Fleet over more than one independent channel, and that a host present on one channel but absent on another is a real and detectable state rather than an error.

### Prerequisites

- Disposable devices, one per platform you care about. [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md) is the design behind all of them.
- A running Fleet you can enroll against. Preview will not do for this lab: real enrollment and real MDM need a real server and, for the MDM steps, the appropriate Apple, Windows or Android tenant configured per Part II. Those tenant steps are Premium.

### Steps

1. Enroll a Mac with fleetd, following [3.2](../03-connect-devices/3.2-enroll-macos-devices.md), and note that the agent channel and the MDM channel are separate enrollments that happen to arrive together.
2. Enroll a Windows device per [3.3](../03-connect-devices/3.3-enroll-windows-devices.md) and a Linux device per [3.4](../03-connect-devices/3.4-enroll-linux-devices.md). Linux has an agent channel and no MDM channel, which is the first channel asymmetry to record.
3. Enroll an iPhone or iPad per [3.5](../03-connect-devices/3.5-enroll-ios-and-ipados-devices.md). These devices have an MDM channel and no osquery agent, the mirror image of Linux.
4. Enroll an Android device per [3.6](../03-connect-devices/3.6-enroll-android-devices.md) and a ChromeOS device per [3.7](../03-connect-devices/3.7-enroll-chromeos-devices.md). ChromeOS reports through a browser extension rather than osquery, a fourth kind of channel.
5. For any host with both an agent and MDM, open the My Device page it exposes to the end user. That device-authenticated surface is a channel in its own right, presenting a per-device token rather than a user account, as [a.8](a.8-api-action-and-endpoint-reference.md) sets out in its caller model.
6. Now half-enroll on purpose. On the Mac, turn MDM off but leave fleetd running, or enroll fleetd without ever turning MDM on. You now have a host that is present on the agent channel and absent on the MDM channel.
7. Recover it. Complete the missing enrollment and confirm the host reads as fully enrolled again. [3.8](../03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md) covers the fleetd side of this.

### Expected result

A table you filled in yourself: for each platform, which of agent, MDM, device-authenticated and extension channels exist. The half-enrolled Mac shows a recent agent check-in with its MDM status off, and after recovery both read healthy. The per-platform channel support is catalogued in [a.2](a.2-platform-capability-matrix.md) if you want to check your table against the reference.

### Cleanup

> **Blast radius: the disposable devices and their host records.** The steps below turn a management channel off and delete host records; they touch only the hosts you enrolled for the lab. Keep the hardware disposable so a mistake costs nothing.

Unenrolling a device is not the same as removing its record, and this is the lab's own teardown honesty check. Turning MDM off disables that one channel; stopping the agent makes the record go stale and read offline. Neither deletes the host record, and Fleet does not age hosts out on its own unless you have turned host expiry on. So clean up in two deliberate moves:

- Turn off what you can, then stop the agent. Turn MDM off where the platform allows it, noting that Windows MDM unenrollment is refused, so on Windows you stop the reporting component rather than unenrolling. Then stop fleetd. Confirm each host reads offline, rather than expecting it to disappear.
- Delete each test host record explicitly if you want it gone, using the delete-a-host action from [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md). Deleting the record uninstalls nothing, so if anything is still enrolling the device, an agent still running or a live automatic-enrollment assignment, the record comes straight back; stop the source first.
- Reset or reimage the disposable hardware if you will reuse it.

### What this proves, and what it does not

It proves the channels are independent and that a half-enrolled host is a detectable state, not a mystery. Detecting half-enrollment across a whole estate rather than one host is a server-side question that [8.4](../08-troubleshooting/8.4-host-side-investigation.md) hands off to [8.6](../08-troubleshooting/8.6-server-state.md). It does not prove MDM behaviour at scale, and preview cannot substitute for the external MDM tenants the real channels depend on.

## Lab 4: Policy to automated response loop

![How-to](../_assets/icons/howto.svg) Author a policy that fails, wire an automated response to the failure, watch every attempt, then remediate the host and confirm the response stops.

### Goal

Build the full compliance loop, policy then automation then remediation, and be able to tell a retry apart from a cooldown by reading Fleet's own record of the attempts.

### Prerequisites

- A running Fleet with at least one host you can make fail a policy. Authoring and observing the loop works against any failing host, but a script response only runs on a host with fleetd installed: preview's simulated hosts are vanilla osquery, so they fail policies fine but silently skip an attached script rather than running it. Target the script response at preview's own local fleetd host, the one `fleetctl preview` enrolls on your machine, or at a real disposable fleetd host.
- Policies are [4.3](../04-know-your-devices/4.3-use-policies-for-compliance.md); automated responses to policy failures are [5.9](../05-manage-devices/5.9-automate-remediation-with-policies.md).

### Steps

1. Write a policy that a host in scope will fail. A policy is a yes-or-no question asked of every host in its scope, with the verdict stored per host, so choose a question you can flip later. [4.3](../04-know-your-devices/4.3-use-policies-for-compliance.md) is the model.
2. Attach a harmless response to the failing verdict: a script that writes a marker file, or a package that is safe to install. [5.9](../05-manage-devices/5.9-automate-remediation-with-policies.md) covers wiring a script or software response to a policy.

> **Blast radius: every host failing this policy in its scope.** An automated response runs on all of them, not just your test host. Scope the policy narrowly to a single fleetd host, preview's local one or a disposable one, before you attach anything.

3. Let the host fail and watch the response fire. Read the attempts through the policy automation activity endpoint, `/api/v1/fleet/policies/{policy_id}/automation_activities`, which returns one activity row per attempt. This is the observability surface [5.9](../05-manage-devices/5.9-automate-remediation-with-policies.md) points to.
4. Observe the retry limit. Fleet retries a failed automated response a bounded number of times rather than forever, and the activity rows show each distinct attempt.
5. Remediate the host so it passes, force a re-evaluation, and confirm no further response fires.
6. Repeat with continuous mode and describe the difference between a cooldown and a retry. Continuous automations, which keep acting while a host stays failing rather than acting once per transition, are a Premium capability. On Fleet Free the continuous-mode toggle is not available, so this step is read-only unless you are on Premium.

### Expected result

The activity endpoint shows a bounded series of attempts while the host fails, then nothing after you remediate. You can state, in one sentence each, what a retry is and what a cooldown is, and which of the two continuous mode changes.

### Cleanup

- Delete the test policy and its attached automation.
- Remove the marker file or uninstall the test package from any real host you used.

### What this proves, and what it does not

It proves you can author, automate, observe and stop a compliance loop, and read the per-attempt record. It does not prove continuous-mode behaviour unless you are on Premium, and a marker-file response is a stand-in, not a real remediation you would trust in production.

## Lab 5: Lost-device recovery

![How-to](../_assets/icons/howto.svg) Work a lost-or-stolen-laptop scenario end to end on a spare Mac: choose lock or wipe, reveal the escrowed recovery key through an authorised account, and confirm the disclosure was recorded.

### Goal

Turn the lost-device decision model into muscle memory and prove the recovery credential is actually retrievable, and audited, when you need it.

### Prerequisites

- A spare, disposable, encrypted Mac you are willing to lock, wipe and recover. The lab runs one macOS device end to end so the mechanism stays concrete; step 1 says why the transports differ on other platforms. This lab is Premium: disk-encryption enforcement and key escrow are Premium capabilities.
- The decision model for locking, wiping and preserving evidence lives in [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md); which recovery credentials exist and who may reveal them is [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md).

### Steps

1. From a written scenario, decide lock versus wipe using the model in [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md). On the Mac in front of you, lock and wipe are both Apple MDM commands, and the choice turns on whether you expect to get the device back. How Fleet carries the same two actions out is not uniform across platforms, though, so do not carry a Mac's behaviour across without checking: Windows lock and every Linux action are scripts, Windows wipe is an OMA-DM command, iOS and iPadOS use Apple MDM, and Android goes through its own management API. [5.7](../05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) is the per-platform matrix.

> **Blast radius: the spare device.** Wipe is irreversible: it erases the device. Lock renders it unusable until unlocked. Run this only against hardware you have chosen to sacrifice to the exercise.

2. Retrieve the escrowed recovery key through an account authorised to reveal it. In the console this is the host's disk-encryption key; through the API it is the host encryption-key endpoint, `/api/v1/fleet/hosts/{id}/encryption_key`, which returns the decrypted value to an authorised caller. Who is authorised is in [a.4](a.4-roles-and-permissions-matrix.md).
3. Confirm the disclosure was recorded. Revealing a key writes a read-disk-encryption-key activity, so the fact that someone read it is itself auditable. [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md) explains the lifecycle.
4. Perform an actual recovery on the spare, using the revealed key, to prove the credential is the right one.
5. See what Fleet does, and does not do, with the key afterwards. Revealing a disk-recovery key does not rotate it: Fleet decrypts the stored value, records the read, and hands it back unchanged, and there is no Fleet action that rotates a disk-recovery key on demand. That is the opposite of Recovery Lock and the managed local administrator password, where a reveal schedules a rotation. If a disclosed key must stop being the standing one, that is a platform-specific re-escrow on the device rather than a Fleet rotate command; on an already-encrypted Mac, for instance, Fleet arranges a new key it can hold and the old one stops mattering. [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md) is the lifecycle.

### Expected result

You unlocked or recovered the spare with the revealed key, and the activity feed shows both the command you sent and the key disclosure, attributed to the account that performed it. You can state that the reveal left the escrowed key unchanged, and say what a genuine re-escrow would take on this platform.

### Cleanup

- Wipe and reset the spare device for reuse.
- Handle the revealed key as the credential it is: move it through your secrets channel, not a ticket or chat, and treat a disclosure that went somewhere it should not have as an incident for your own process, since Fleet has no rotate action to undo it.

### What this proves, and what it does not

It proves the decision model, the retrieval path and the audit trail are real and connected. It does not prove recovery of a device you do not physically control, and it does not rehearse the parts of a genuine incident that live outside Fleet, such as chain-of-custody and legal hold.

## Lab 6: Adopt GitOps

![How-to](../_assets/icons/howto.svg) Take state you built by clicking, generate GitOps files from it, dry-run them, reconcile, introduce deliberate drift, and reapply.

### Goal

Move a Fleet from click-built to version-controlled and understand that the completion criterion is a predicted diff and a verified resulting state, not a zero exit code.

### Prerequisites

- A Fleet with some click-built state to export. Preview is fine for the whole lab.
- GitOps is [6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md); the `fleetctl` commands that drive it are catalogued in [a.7](a.7-fleetctl-command-reference.md).

### Steps

1. Build a little state in the UI: a policy, a query, a configuration setting.
2. Generate GitOps files from the live server with `fleetctl generate-gitops`. Its flags select the output directory and the target; [6.2](../06-automate-fleet/6.2-manage-fleet-with-gitops.md) covers ownership and how secrets are kept out of the files.
3. Separate secrets from the generated configuration, so the repository holds references rather than values.
4. Dry-run the configuration with `fleetctl gitops --dry-run` and read the predicted changes. Predicting the diff before you apply is the skill this lab builds.

> **Blast radius: the whole configuration scope the repository targets.** A reconcile makes the live server match the files, which means it removes managed objects that are not in the repository. Dry-run first, every time, and run this against preview or a test instance rather than a Fleet you rely on.

5. Reconcile with `fleetctl gitops` and confirm the resulting state matches your prediction, not merely that the command exited zero.
6. Introduce drift by changing something in the UI, dry-run again to see the drift as a diff, then reapply to restore the repository's version.

### Expected result

The dry-run output matched what actually changed on reconcile, and reapplying after UI drift returned the server to the repository's state. You treated the predicted diff, not the exit code, as the proof.

### Cleanup

- Reset the preview sandbox, or on a test instance remove the objects the lab created.
- Keep the generated repository if it is useful; it is the artefact this lab was for.

### What this proves, and what it does not

It proves you can generate, dry-run, reconcile and recover configuration, and that you read the diff rather than the exit status. It does not prove your production reconcile is safe until you have dry-run it against production state, because the deletion hazard is real and specific to what each server already holds.

## Lab 7: Certificate lifecycle

![How-to](../_assets/icons/howto.svg) Connect a certificate authority to Fleet, validate it, deliver a certificate to a device through a configuration profile, and see both the success and the failure path.

### Goal

Complete the prerequisite that certificate delivery depends on: a working, validated certificate-authority integration, and then use it.

### Prerequisites

- A test certificate authority you can connect to Fleet. This lab is Premium: the certificate-authority integrations are a Premium capability.
- Connecting a certificate authority is [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md); delivering a certificate through a profile is [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md).

### Steps

1. Choose your CA type deliberately, because it decides both what creation checks and how a certificate is later delivered. To exercise the whole path here, connect a type that both proves its credentials at creation and delivers through a profile: DigiCert, NDES, or Smallstep. Connect it per [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md). Creation makes a live outbound call, so for these three a good URL and set of credentials is accepted and a bad one is refused at creation rather than failing silently later.
2. Make the failure visible on purpose, and notice that creation validates different things for different types. A wrong URL, or an endpoint that is unreachable or speaking the wrong protocol, is refused at creation for any type, because creation always checks reachability and protocol. A wrong credential is refused at creation only for DigiCert, NDES, and Smallstep, the three whose live check also authenticates. For Hydrant, custom EST, and custom SCEP, creation does not test the credential: a wrong secret survives the connection and surfaces later, custom SCEP the first time a host requests a certificate, Hydrant and custom EST only when a caller invokes the test-issue endpoint. So connect a second integration of your chosen type with a wrong credential and watch it rejected at creation; to see the delayed failure instead, connect a Hydrant or custom EST authority with a wrong secret, watch it pass creation, then fail when you test-issue. [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md) sets out which types validate what.
3. Reference the working authority from a configuration profile so an enrolled device requests a certificate. This delivery path exists only for the four delivery-capable types, NDES, custom SCEP, Smallstep, and DigiCert; Hydrant and custom EST have no profile variable and do not deliver to a host at this release, so for those the only issuance path is the synchronous test-issue endpoint, which hands a certificate back to the caller rather than installing one. [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) covers profiles and their certificate variables.
4. For a delivery-capable type, deliver the profile to a test host and confirm the certificate is issued and installed. For Hydrant or custom EST, issue one certificate through the test-issue endpoint instead and confirm it returns a certificate to you.
5. Rotate the integration credentials and delete a test integration safely, watching what happens to profiles that depend on it.

### Expected result

For a delivery-capable type, the valid authority is accepted and issues a certificate that lands on the host through the profile; for Hydrant or custom EST it returns a certificate from the test-issue endpoint. The deliberately broken authority is refused at creation when the fault is a bad URL for any type, or a bad credential on DigiCert, NDES, or Smallstep; for Hydrant, custom EST, or custom SCEP a bad credential passes creation and fails only later. Deleting an integration that a profile depends on shows you the dependency rather than hiding it.

### Cleanup

> **Blast radius: profiles and hosts that depend on the integration.** Deleting a certificate authority affects every profile referencing it. Remove the profiles first, then the integration, on test objects only.

- Remove the test profile from the host.
- Delete the test integrations, valid and broken.

### What this proves, and what it does not

It proves the full path from connecting an authority to a certificate, reaching a device through a profile for a delivery-capable type or a caller through the test-issue endpoint for Hydrant and custom EST, including the type-specific failure path and the deletion dependency. It does not prove your production authority's own issuance policy, renewal cadence or scale behaviour, which live in the certificate authority rather than in Fleet.

## Lab 8: Offline vulnerability pipeline

![How-to](../_assets/icons/howto.svg) Run Fleet's vulnerability processing without direct feed egress: stage the data on a connected machine, move it to an isolated one, and process it there.

### Goal

Operate the vulnerability pipeline in a controlled-egress or air-gapped shape, where the server that processes vulnerabilities is not the one allowed to reach the internet.

### Prerequisites

- Two environments, one that may reach Fleet's data sources and one that may not. Both need somewhere to keep the downloaded databases.
- Software and vulnerabilities are [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md). The configuration keys this lab sets are catalogued in [a.3](a.3-configuration-model-and-precedence.md).

### Steps

1. On the connected machine, let Fleet download the vulnerability data sources to a directory of your choice. The `vulnerabilities.databases_path` setting is where Fleet reads and writes that data, so point it somewhere you can copy from.
2. Copy the populated `databases_path` directory to the isolated environment. This is the transfer step the whole architecture exists for.

> **Blast radius: the vulnerability freshness of the server you change.** Turning off data sync on a server that was updating itself freezes its vulnerability data at whatever you last placed there. Do this on a test server, and treat stale data as a first-class failure to watch for.

3. On the isolated server, set two things, so it neither fetches data nor competes for the job. Set `vulnerabilities.disable_data_sync` so Fleet expects the data to be present in `databases_path` rather than fetching it, and point `databases_path` at the copied directory. Then set `vulnerabilities.disable_schedule` so the server stops running vulnerability processing on its own internal cron and hands ownership of the job to the external command you run next. The two share one database lock, so if the internal schedule is left on, whichever grabs the lock first wins and the other is refused; disabling the schedule is what makes the external command the owner. [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md) explains how a finding is a match between installed software and downloaded data.
4. Run vulnerability processing with `fleet vuln_processing`, the external command that now owns the job, which does the matching pass against the data you placed. Because you disabled the internal schedule, it takes the shared lock cleanly; a `vulnerabilities processing locked` failure here is the sign the schedule is still on.
5. Simulate a stale or missing dataset: withhold the next copy, run processing again, and confirm you can tell fresh data from old by when you last transferred it.

### Expected result

The isolated server produces vulnerability findings from data it never downloaded itself, and you can point to the directory the data came from and the day you last refreshed it. The stale-data simulation shows why a freshness check belongs in your routine.

### Cleanup

- Re-enable data sync and the internal schedule on any server that should update and process on its own again, or decommission the test servers.
- Remove the staged database copies you no longer need.

### What this proves, and what it does not

It proves you can place vulnerability data by hand and process it offline, and that you know how to check its freshness. It does not prove the findings are complete or correct: a match depends on both the installed-software inventory and the downloaded data, and old or partial data produces confidently wrong conclusions.

## Lab 9: Capacity validation

![How-to](../_assets/icons/howto.svg) Put simulated load on a test Fleet, scrape its metrics, find the first component to saturate, then change one variable and explain why the bottleneck moved.

### Goal

Measure where a Fleet server saturates under representative load, using Fleet's own load simulator and its metrics endpoint, before you grow a real one into the same wall.

### Prerequisites

- A test Fleet server you can push to the edge and its supporting MySQL and Redis. Never point this at production.
- `osquery-perf`, Fleet's workload simulator, built from the Fleet source tree. It is a development and testing tool rather than something shipped in a release, so it is built, not installed. Capacity and availability are [7.5](../07-operate-fleet/7.5-maintain-capacity-and-availability.md); observing performance and health is [7.4](../07-operate-fleet/7.4-observe-progress-and-service-health.md).
- Prometheus or any scraper that reads Fleet's `/metrics` endpoint, which [7.4](../07-operate-fleet/7.4-observe-progress-and-service-health.md) covers as a monitoring surface.

### Steps

1. Point `osquery-perf` at the test server and ramp a representative host count, using its platform templates so the simulated hosts resemble your real mix and its startup spread so they do not all arrive at once.

> **Blast radius: the test server and its stores.** Simulated load is designed to saturate something. Aimed at a production server it degrades a real service, so keep it on disposable infrastructure.

2. Scrape `/metrics` while the load runs. Watch request latency through `http_request_duration_seconds` and request volume through `http_requests_total`, alongside the database and Redis you provisioned.
3. Record the first component to saturate: the API tier, MySQL, or Redis. That first wall is the number this lab is for.
4. Change exactly one variable, the host ramp, the query interval, the scheduled result rate, or the MDM probability, and run again.
5. Explain why the bottleneck moved, or did not. Connecting a metric to a cause is the skill; [7.5](../07-operate-fleet/7.5-maintain-capacity-and-availability.md) is the model for it.

### Expected result

A short table: variable changed, first component to saturate, and the metric that showed it. You can say why the wall moved when you changed the one variable.

### Cleanup

- Stop `osquery-perf`. Its simulated hosts stop checking in and read offline; they do not age out on their own. Fleet removes an offline host automatically only if you have turned host expiry on and its window has passed, so to clear them without waiting, either enable host expiry or delete the host records explicitly.
- Tear down the test server and its stores, which discards the records along with everything else.

### What this proves, and what it does not

It proves how much load your server tier and stores absorb before something saturates, and which metric reveals it. It does not prove endpoint performance: the hosts are simulated agents generating server-side traffic, so this measures the server's capacity and says nothing about how osquery behaves on real hardware. Treat the result as a server-sizing input, not an agent-performance claim.

## Lab 10: Failure-injection lab

![How-to](../_assets/icons/howto.svg) Break things on purpose, one at a time, and diagnose each one with the method Part VIII teaches before you read a single log.

### Goal

Practise the diagnostic method on faults whose cause you already know, so that when a real one arrives you reason from symptom to failing stage instead of guessing.

### Prerequisites

- A disposable Fleet and at least one enrolled test host. Preview covers several of these injections; the MDM ones need a real enrolled device.
- The diagnostic method is [8.1](../08-troubleshooting/8.1-diagnostic-method.md), and the rest of Part VIII is the reference it draws on.

> **Blast radius: the test Fleet and its test host.** This lab deliberately damages a running system. Every injection below is safe only because the system is disposable. Do none of it on a Fleet anyone depends on.

### Steps

For each fault, force yourself to name the channel, the evidence surface, the next discriminating test, and the safe recovery, before you open the logs. Then check your reasoning against what the logs say.

1. Present a bad TLS arrangement to an agent and watch it fail to check in. Diagnose from the host side per [8.4](../08-troubleshooting/8.4-host-side-investigation.md).
2. Invalidate a host's node key using a method the book already gives you, and reversible by design: delete that host's record in Fleet while its agent keeps running. The agent's next check-in no longer matches any host row, so it fails with `invalid node key` ([8.3](../08-troubleshooting/8.3-server-logs.md)), then re-enrolls with its enroll secret and a fresh record appears ([3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md)). Observe that recovery rather than engineering a broken key by hand.
3. Let a host go stale by stopping its agent, and tell staleness apart from a genuine outage.
4. Split the agent and MDM state, as in Lab 3, and locate the half-enrollment from the server side per [8.6](../08-troubleshooting/8.6-server-state.md).
5. Make a software install fail and read the failure, then the retry.
6. Block a log destination and watch results back up, using the server logs per [8.3](../08-troubleshooting/8.3-server-logs.md).
7. Put the datastore under pressure, from Lab 9 if you like, and recognise degradation as distinct from a hard failure, per [8.14](../08-troubleshooting/8.14-degradation.md).

### Expected result

For each injection, a written prediction that you made before reading logs, and a note on whether the evidence confirmed it. The value is in the predictions you got wrong.

### Cleanup

- Reverse each injection, or reset the preview sandbox for a clean start.
- Re-enroll or reset the test host if an injection left it in a broken state.

### What this proves, and what it does not

It proves you can apply the narrowing method to a known fault and read the evidence surface for each stage. It does not prove you will recognise a novel production fault, because a fault you injected is one you already understood. What transfers is the habit of predicting before reading, not the specific faults.
