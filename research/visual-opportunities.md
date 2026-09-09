# Additional visual opportunities

Editorial briefs proposed 2026-09-08 on `feature/visual-brief-refinement`.
There is one additional opportunity in every numbered chapter and appendix: 83 in all.
Four priority briefs cover the earlier audit's Windows enrollment comparison, policy
trigger traces, Apple MDM wake/fetch sequence, and a real My Device screenshot. The last
expands an existing screenshot comment; it is not a duplicate capture request.

The 87 briefs comprise 84 technical diagrams, two atmospheric illustrations, and one
real screenshot. They are proposals, not accepted images or fresh technical verification.
Existing artwork and chapter prose remain in place. New references are commented out
until reviewed assets exist. The nine existing `IMAGE-REDO` briefs remain separate work.

The complete prompts live beside the relevant prose in each chapter's HTML comments.
Their QUESTION names the reader need; their NOTE identifies text to shorten after image
acceptance and details that must stay selectable. This index tracks coverage, not a second
copy of the production prompts. Follow STYLE.md §13 and HANDOFF.md for production and review.
Use real demo UI for the screenshot. Keep atmospheric vignettes compact and outside lookup
groups. Resolve a contradiction against the chapter's evidence before accepting artwork.

## Four priority gaps

| Chapter | Brief | Reader question |
|---|---|---|
| 3.3 | [3.3-windows-enrollment-sequences.webp](../manual/03-connect-devices/3.3-enroll-windows-devices.md) | How do the agent-first and Entra MDM-first Windows enrollment paths converge? |
| 5.9 | [5.9-policy-trigger-result-traces.webp](../manual/05-manage-devices/5.9-automate-remediation-with-policies.md) | How do repeated failures, continuous mode, and no-answer affect policy automation firing? |
| 8.8 | [8.8-apple-mdm-wake-and-fetch.webp](../manual/08-troubleshooting/8.8-apple-mdm-diagnostics.md) | Does APNs carry a command, or wake a device to fetch it from Fleet? |
| 5.5 | [5.5-my-device-self-service.webp](../manual/05-manage-devices/5.5-design-setup-and-self-service-experiences.md) | What does the end user actually see on My Device? |

## One additional opportunity per chapter and appendix

| Chapter | Brief | Reader question |
|---|---|---|
| 0.3 | [0.1-new-reader-route.webp](../manual/00-Introduction/0.3-how-to-use-this-manual.md) | Which chapters get a first deployment to a handoff? |
| 0.4 | [0.2-release-maintenance-vignette.webp](../manual/00-Introduction/0.4-changelog.md) | Can the release ledger have a quiet visual opening without inventing a feature story? |
| 1.1 | [1.1-fleet-environment-boundaries.webp](../manual/01-foundations/1.1-what-fleet-is.md) | Where does Fleet fit among the systems an organization already runs? |
| 1.2 | [1.2-online-evidence-boundary.webp](../manual/01-foundations/1.2-how-fleet-reaches-a-device.md) | What evidence does the Online badge actually provide? |
| 1.3 | [1.3-host-transfer-state.webp](../manual/01-foundations/1.3-hosts-fleets-labels.md) | What survives a fleet transfer, and what must be checked beforehand? |
| 1.4 | [1.4-account-review-lifecycles.webp](../manual/01-foundations/1.4-identity-and-roles.md) | Which accounts need an explicit owner-led retirement process? |
| 1.5 | [1.5-activity-actor-retention.webp](../manual/01-foundations/1.5-audit-and-activity.md) | Why can a valid activity have no current actor link? |
| 1.6 | [1.6-datastore-outage-paths.webp](../manual/01-foundations/1.6-the-fleet-server.md) | Why does losing Redis look different from losing MySQL? |
| 2.1 | [2.1-ownership-escalation-map.webp](../manual/02-administer-and-deploy-fleet/2.1-administration-model-and-deployment-choices.md) | How does an ownership record help when a dependency fails? |
| 2.2 | [2.2-async-observation-buffer.webp](../manual/02-administer-and-deploy-fleet/2.2-self-hosting-architecture-and-capacity.md) | What changes when host observations are written asynchronously? |
| 2.3 | [2.3-report-volume-cost-drivers.webp](../manual/02-administer-and-deploy-fleet/2.3-deploy-on-aws-or-gcp.md) | How do report choices change exported volume on AWS? |
| 2.4 | [2.4-external-vulnerability-job.webp](../manual/02-administer-and-deploy-fleet/2.4-deploy-with-containers-or-virtual-machines.md) | What must change together when vulnerability processing moves outside serving instances? |
| 2.5 | [2.5-console-versus-device-account.webp](../manual/02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md) | Which account does JIT create, and which one does Platform SSO provision? |
| 2.6 | [2.6-endpoint-permission-intersection.webp](../manual/02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md) | Can an endpoint allowlist grant permission that the role lacks? |
| 2.7 | [2.7-configuration-storage-planes.webp](../manual/02-administer-and-deploy-fleet/2.7-organization-and-server-settings.md) | Which settings are stored in Fleet, and which start the server process? |
| 2.8 | [2.8-independent-log-routing.webp](../manual/02-administer-and-deploy-fleet/2.8-activity-audit-logs-and-log-delivery.md) | Why does configuring one log destination leave another stream empty? |
| 2.9 | [2.9-mdm-ingress-boundary.webp](../manual/02-administer-and-deploy-fleet/2.9-mdm-architecture-and-foundations.md) | Why does an ingress rule covering only the REST API break MDM enrollment? |
| 2.10 | [2.10-stored-enrollment-default.webp](../manual/02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) | Why can two servers on the same release send different default enrollment profiles? |
| 2.11 | [2.11-windows-escrow-identity.webp](../manual/02-administer-and-deploy-fleet/2.11-configure-windows-management.md) | Why can a renewed Windows enrollment certificate break retrieval of an existing BitLocker key? |
| 2.12 | [2.12-android-companion-boundary.webp](../manual/02-administer-and-deploy-fleet/2.12-bind-android-enterprise.md) | What does the small Android agent do alongside Google's management path? |
| 2.13 | [2.13-certificate-renewal-marker.webp](../manual/02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md) | How does Fleet recognize an issued certificate for automatic renewal? |
| 3.1 | [3.1-enroll-secret-rotation.webp](../manual/03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md) | Why does revoking an enroll secret leave existing hosts running but break later re-enrollment? |
| 3.2 | [3.2-macos-migration-branches.webp](../manual/03-connect-devices/3.2-enroll-macos-devices.md) | Who releases the old MDM enrollment, and which re-enrollment screen follows? |
| 3.3 | [3.3-msi-build-install-values.webp](../manual/03-connect-devices/3.3-enroll-windows-devices.md) | How does a credential-free MSI receive real enrollment settings later? |
| 3.4 | [3.4-linux-escrow-choice.webp](../manual/03-connect-devices/3.4-enroll-linux-devices.md) | How does Orbit choose silent recovery-key escrow or an interactive passphrase? |
| 3.5 | [3.5-ios-lock-enrollment-choice.webp](../manual/03-connect-devices/3.5-enroll-ios-and-ipados-devices.md) | Which enrollment choice preserves the ability to remotely lock an iPhone or iPad? |
| 3.6 | [3.6-android-ownership-containers.webp](../manual/03-connect-devices/3.6-enroll-android-devices.md) | What is removed when a personally owned Android device is unenrolled? |
| 3.7 | [3.7-chromeos-extension-delivery.webp](../manual/03-connect-devices/3.7-enroll-chromeos-devices.md) | How do the extension and its managed settings reach a Chromebook? |
| 3.8 | [3.8-orbit-update-bridge.webp](../manual/03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md) | Why do older Orbit agents need an intermediate rollout? |
| 4.1 | [4.1-host-identity-sources.webp](../manual/04-know-your-devices/4.1-understand-hosts-vitals-and-inventory.md) | Why do local accounts and device-owner emails disagree? |
| 4.2 | [4.2-report-two-row-gates.webp](../manual/04-know-your-devices/4.2-run-queries-and-reports.md) | Where are report rows rejected, and where are they trimmed later? |
| 4.3 | [4.3-policy-population-denominator.webp](../manual/04-know-your-devices/4.3-use-policies-for-compliance.md) | Which hosts belong in a compliance denominator? |
| 4.4 | [4.4-vulnerability-empty-pipeline.webp](../manual/04-know-your-devices/4.4-understand-software-and-vulnerabilities.md) | Where should you look when the vulnerability list is empty? |
| 4.5 | [4.5-history-gap-and-deletion.webp](../manual/04-know-your-devices/4.5-monitor-fleet-wide-state.md) | What does a gap in Fleet's uptime history prove? |
| 4.6 | [4.6-query-denylist-population.webp](../manual/04-know-your-devices/4.6-advanced-osquery-queries-and-tables.md) | How can an expensive query bias the hosts represented in its results? |
| 4.7 | [4.7-additional-query-refresh.webp](../manual/04-know-your-devices/4.7-extend-osquery-with-custom-tables-and-plugins.md) | When does a custom host field refresh, and when is it skipped? |
| 5.1 | [5.1-cancel-activation-boundary.webp](../manual/05-manage-devices/5.1-plan-target-and-govern-device-changes.md) | Where does cancelling queued work stop being a reliable recall? |
| 5.2 | [5.2-profile-value-resolution.webp](../manual/05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) | How can one profile carry per-host values while keeping a secret out of its stored content? |
| 5.3 | [5.3-repeatable-script-flow.webp](../manual/05-manage-devices/5.3-run-and-manage-scripts.md) | What makes a remediation script safe to run again? |
| 5.4 | [5.4-package-variant-selection.webp](../manual/05-manage-devices/5.4-manage-software-and-applications.md) | Why can installation and uninstallation choose different package variants? |
| 5.5 | [5.5-windows-setup-gate.webp](../manual/05-manage-devices/5.5-design-setup-and-self-service-experiences.md) | Which Windows enrollments actually block the user during setup? |
| 5.6 | [5.6-windows-deadline-overlap.webp](../manual/05-manage-devices/5.6-control-operating-system-updates.md) | How do the Windows update deadline and restart grace period overlap? |
| 5.7 | [5.7-offline-mdm-action.webp](../manual/05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) | Why can an offline Apple device execute a command long after it was sent? |
| 5.8 | [5.8-recovery-key-fallback.webp](../manual/05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md) | Which stored recovery credential does Fleet return when the current key cannot decrypt? |
| 5.9 | [5.9-remediation-refetch-clocks.webp](../manual/05-manage-devices/5.9-automate-remediation-with-policies.md) | Why can a successful script sit beside a policy that still says failing? |
| 6.1 | [6.1-ambiguous-write-reconcile.webp](../manual/06-automate-fleet/6.1-automation-design-and-change-control.md) | What should an automation do after a write times out? |
| 6.2 | [6.2-gitops-assignment-loss-window.webp](../manual/06-automate-fleet/6.2-manage-fleet-with-gitops.md) | How can a partial GitOps apply leave Apple token assignments cleared? |
| 6.3 | [6.3-host-list-cursor.webp](../manual/06-automate-fleet/6.3-use-the-fleet-rest-api.md) | How does a client traverse a large host list without relying on unstable offset ordering? |
| 6.4 | [6.4-fleetctl-config-write-race.webp](../manual/06-automate-fleet/6.4-use-fleetctl.md) | Why should simultaneous automation jobs use separate fleetctl configuration files? |
| 6.5 | [6.5-webhook-receive-and-act.webp](../manual/06-automate-fleet/6.5-integrations-webhooks-and-external-workflows.md) | How should a receiver separate durable receipt from a repeatable side effect? |
| 6.6 | [6.6-mcp-transport-boundaries.webp](../manual/06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md) | What changes operationally between a local stdio connection and a remote SSE connection? |
| 7.1 | [7.1-recovery-objective-windows.webp](../manual/07-operate-fleet/7.1-define-the-service-operating-model.md) | How are acceptable data loss and acceptable recovery time measured separately? |
| 7.2 | [7.2-backup-cross-store-gap.webp](../manual/07-operate-fleet/7.2-back-up-and-restore-service-state.md) | What happens when a database backup and object-store snapshot disagree? |
| 7.3 | [7.3-restart-activated-queue.webp](../manual/07-operate-fleet/7.3-upgrade-fleet-and-fleetd.md) | Why can a restart leave one host's queue blocked indefinitely? |
| 7.4 | [7.4-latency-metric-unit-check.webp](../manual/07-operate-fleet/7.4-observe-progress-and-service-health.md) | How can a misleading metric name prevent a latency alert from firing? |
| 7.5 | [7.5-capacity-decision-path.webp](../manual/07-operate-fleet/7.5-maintain-capacity-and-availability.md) | What evidence justifies scaling instead of repairing stalled work? |
| 7.6 | [7.6-private-ca-cutover.webp](../manual/07-operate-fleet/7.6-maintain-credentials-certificates-and-access.md) | In what order should a private trust root and served TLS chain change? |
| 7.7 | [7.7-handoff-evidence-gate.webp](../manual/07-operate-fleet/7.7-production-readiness-checklist-and-handoff.md) | What turns a readiness claim into an accepted operational handoff? |
| 7.8 | [7.8-deployment-retirement-order.webp](../manual/07-operate-fleet/7.8-retire-a-fleet-deployment.md) | Which dependencies must be released before Fleet is shut down? |
| 8.1 | [8.1-two-clocks-diagnostic.webp](../manual/08-troubleshooting/8.1-diagnostic-method.md) | How do record time and arrival time distinguish delayed delivery from stale consumption? |
| 8.2 | [8.2-debug-window-lifecycle.webp](../manual/08-troubleshooting/8.2-log-surfaces.md) | How do you end a diagnostic logging session without leaving elevated verbosity behind? |
| 8.3 | [8.3-request-to-node-log.webp](../manual/08-troubleshooting/8.3-server-logs.md) | Why can the log on a healthy Fleet node miss a reproduced failure? |
| 8.4 | [8.4-half-enrolled-diagnosis.webp](../manual/08-troubleshooting/8.4-host-side-investigation.md) | Does a missing agent explain MDM commands that also stop completing? |
| 8.5 | [8.5-debug-node-selection.webp](../manual/08-troubleshooting/8.5-fleetctl-debug.md) | How do you make a profile or archive describe the node you are investigating? |
| 8.6 | [8.6-cron-run-observation.webp](../manual/08-troubleshooting/8.6-server-state.md) | Which cron status proves a run started, and which still needs its error field checked? |
| 8.7 | [8.7-file-carve-auth-sequence.webp](../manual/08-troubleshooting/8.7-live-query-introspection.md) | What authenticates the beginning of a file carve versus each uploaded block? |
| 8.8 | [8.8-app-install-verification-loop.webp](../manual/08-troubleshooting/8.8-apple-mdm-diagnostics.md) | Why can an acknowledged App Store install still be reported as failed? |
| 8.9 | [8.9-windows-poll-and-wake.webp](../manual/08-troubleshooting/8.9-windows-mdm-diagnostics.md) | How can a Windows device use an eight-hour poll yet receive commands sooner? |
| 8.10 | [8.10-android-return-path-ownership.webp](../manual/08-troubleshooting/8.10-android-diagnostics.md) | Which Android return-path evidence can the operator inspect on proxy versus direct deployments? |
| 8.11 | [8.11-one-axis-reproduction.webp](../manual/08-troubleshooting/8.11-reproducing-and-isolating.md) | What does a controlled comparison establish during reproduction? |
| 8.12 | [8.12-incident-activity-window.webp](../manual/08-troubleshooting/8.12-audit-logs.md) | How do you turn an onset time into a focused activity investigation? |
| 8.13 | [8.13-escalation-evidence-chain.webp](../manual/08-troubleshooting/8.13-escalation.md) | What makes an escalation's diagnosis checkable by the next person? |
| 8.14 | [8.14-degradation-isolation-forks.webp](../manual/08-troubleshooting/8.14-degradation.md) | What experiment separates a hard limit from expensive work or resource contention? |
| a.1 | [a.1-reference-index-navigation.webp](../manual/09-appendices/a.1-capability-index.md) | How does one capability identifier lead to platform and interface answers? |
| a.2 | [a.2-capability-condition-layers.webp](../manual/09-appendices/a.2-platform-capability-matrix.md) | Why does platform alone fail to determine whether a capability is available? |
| a.3 | [a.3-startup-flags-file-lifecycle.webp](../manual/09-appendices/a.3-configuration-model-and-precedence.md) | Why does omitting command_line_flags fail to restore a locally maintained file? |
| a.4 | [a.4-role-scope-table-choice.webp](../manual/09-appendices/a.4-roles-and-permissions-matrix.md) | Which permission table applies, and why is Unassigned unreachable to fleet-scoped roles? |
| a.5 | [a.5-gitops-interface-direction.webp](../manual/09-appendices/a.5-interface-index.md) | What does a GitOps apply write, and where must an operator go to read state? |
| a.6 | [a.6-agent-feature-compatibility.webp](../manual/09-appendices/a.6-glossary-and-release-compatibility.md) | Why can an agent enroll successfully and still lack one feature? |
| a.7 | [a.7-fleetctl-option-resolution.webp](../manual/09-appendices/a.7-fleetctl-command-reference.md) | Why can an unrelated shell variable change a fleetctl command's behavior? |
| a.8 | [a.8-api-token-entry-points.webp](../manual/09-appendices/a.8-api-action-and-endpoint-reference.md) | How does a user obtain a token, and which account's permissions does it carry? |
| a.10 | [a.10-index-reading-vignette.webp](../manual/09-appendices/a.10-subject-index.md) | Can the alphabetical index get a visual resting point without obstructing lookup? |
| a.11 | [a.11-mcp-tool-route-allowlist.webp](../manual/09-appendices/a.11-mcp-tool-reference.md) | How do tool choices become an API endpoint allowlist? |
