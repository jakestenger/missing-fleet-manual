# Content-type icon refresh and placement audit

Reviewed 2026-09-09 against main `4d462fd`, for the 4.91 and 4.90 editions.

The four categories now use Fleet's official six-dot logo, a checklist, a reference
book, and a magnifying glass. Each has a light and dark SVG, selected by the
Docusaurus theme control. Asset provenance and editing instructions are in
[the icon README](../../manual/_assets/icons/README.md); placement rules are in
[STYLE](../../STYLE.md#category-icons-at-useful-reading-boundaries).

All 1,217 existing chapter references were updated (614 in 4.91; 603 in 4.90),
along with the chapter template. The audit added **99 markers per edition**:
56 Explanation, 27 Reference, 8 How-to, and 8 Troubleshooting. The editions have
713 and 702 chapter markers respectively after this pass.

The largest gap was unmarked opening context: readers encountered a chapter's
first badge only after its introduction. The other additions identify choices,
lookup material, verification steps, and shifts from explanation to diagnosis.
This pass changes markers and the icon legend, not technical claims or procedures.

Part VIII keeps its existing exception: repeating a diagnostic badge throughout
an entirely diagnostic part adds little information. Short continuations, the
company/product overview subheadings, individual index letters, and individual
rows or steps also remain unmarked. This is a placement audit, not a requirement
to put an icon on every paragraph.

## New markers within chapters

These 37 placements are the most useful additions beyond chapter introductions.
Both editions receive the same placements. Where a section mixes reference and
diagnosis, the table identifies the separate paragraph.

| Chapter | Passage | Category |
|---|---|---|
| [0.3](../../manual/00-Introduction/0.3-how-to-use-this-manual.md) | The manual at a glance | Reference |
| [0.3](../../manual/00-Introduction/0.3-how-to-use-this-manual.md) | Indexes | Reference |
| [0.3](../../manual/00-Introduction/0.3-how-to-use-this-manual.md) | Conventions | Reference |
| [0.3](../../manual/00-Introduction/0.3-how-to-use-this-manual.md) | Why each chapter names a Fleet release | Explanation |
| [1.1](../../manual/01-foundations/1.1-what-fleet-is.md) | From device observations to completed work | Explanation |
| [1.1](../../manual/01-foundations/1.1-what-fleet-is.md) | Try Fleet without deploying anything | How-to |
| [1.6](../../manual/01-foundations/1.6-the-fleet-server.md) | Losing Redis and losing MySQL fail very differently | Troubleshooting |
| [3.2](../../manual/03-connect-devices/3.2-enroll-macos-devices.md) | Choose an enrollment approach | Reference |
| [3.2](../../manual/03-connect-devices/3.2-enroll-macos-devices.md) | The ADE sequence, in order | How-to |
| [3.2](../../manual/03-connect-devices/3.2-enroll-macos-devices.md) | Who owns it afterwards | Reference |
| [3.2](../../manual/03-connect-devices/3.2-enroll-macos-devices.md) | Reference and troubleshooting | Reference |
| [3.2](../../manual/03-connect-devices/3.2-enroll-macos-devices.md) | Reference and troubleshooting: paragraph beginning “When enrollment does not work, the split at the top of this chapter…” | Troubleshooting |
| [3.3](../../manual/03-connect-devices/3.3-enroll-windows-devices.md) | Choose an enrollment approach | Reference |
| [3.3](../../manual/03-connect-devices/3.3-enroll-windows-devices.md) | Who owns it afterwards | Reference |
| [3.3](../../manual/03-connect-devices/3.3-enroll-windows-devices.md) | Reference and troubleshooting | Troubleshooting |
| [3.4](../../manual/03-connect-devices/3.4-enroll-linux-devices.md) | Choose an enrollment approach | Reference |
| [3.4](../../manual/03-connect-devices/3.4-enroll-linux-devices.md) | Who owns it afterwards | How-to |
| [3.4](../../manual/03-connect-devices/3.4-enroll-linux-devices.md) | Reference and troubleshooting | Reference |
| [3.5](../../manual/03-connect-devices/3.5-enroll-ios-and-ipados-devices.md) | Choose an enrollment approach | Reference |
| [3.5](../../manual/03-connect-devices/3.5-enroll-ios-and-ipados-devices.md) | Automated Device Enrollment | Explanation |
| [3.5](../../manual/03-connect-devices/3.5-enroll-ios-and-ipados-devices.md) | Who owns it afterwards | Reference |
| [3.5](../../manual/03-connect-devices/3.5-enroll-ios-and-ipados-devices.md) | Reference and troubleshooting | Reference |
| [3.5](../../manual/03-connect-devices/3.5-enroll-ios-and-ipados-devices.md) | Reference and troubleshooting: paragraph beginning “Everything diagnostic for these devices is…” | Troubleshooting |
| [3.6](../../manual/03-connect-devices/3.6-enroll-android-devices.md) | Android: choosing a path | Reference |
| [3.6](../../manual/03-connect-devices/3.6-enroll-android-devices.md) | Who owns it afterwards | Reference |
| [3.6](../../manual/03-connect-devices/3.6-enroll-android-devices.md) | Reference and troubleshooting | Troubleshooting |
| [3.7](../../manual/03-connect-devices/3.7-enroll-chromeos-devices.md) | Who owns it afterwards | Reference |
| [5.4](../../manual/05-manage-devices/5.4-manage-software-and-applications.md) | The pre-install query is a truth test, and its failure is ambiguous | Reference |
| [5.4](../../manual/05-manage-devices/5.4-manage-software-and-applications.md) | Installation results and rollback triggers | Reference |
| [5.4](../../manual/05-manage-devices/5.4-manage-software-and-applications.md) | Verify before you roll out | How-to |
| [5.5](../../manual/05-manage-devices/5.5-design-setup-and-self-service-experiences.md) | Failure and escape, decided before rollout | How-to |
| [5.5](../../manual/05-manage-devices/5.5-design-setup-and-self-service-experiences.md) | Check configuration results after release | How-to |
| [5.5](../../manual/05-manage-devices/5.5-design-setup-and-self-service-experiences.md) | Verify before you roll out | How-to |
| [5.6](../../manual/05-manage-devices/5.6-control-operating-system-updates.md) | Verify delivery and convergence separately | How-to |
| [5.9](../../manual/05-manage-devices/5.9-automate-remediation-with-policies.md) | When a successful response leaves the policy failing | Troubleshooting |
| [6.2](../../manual/06-automate-fleet/6.2-manage-fleet-with-gitops.md) | When a run fails part way | Troubleshooting |
| [6.3](../../manual/06-automate-fleet/6.3-use-the-fleet-rest-api.md) | Filters fail quietly | Troubleshooting |

## Newly marked chapter introductions

These 62 introductions now identify the kind of guidance that opens the chapter.

| Chapter | Opening passage | Category |
|---|---|---|
| [0.1](../../manual/00-Introduction/0.1-who-fleet-is.md) | Who Fleet is | Explanation |
| [0.2](../../manual/00-Introduction/0.2-what-fleet-is.md) | What Fleet is | Explanation |
| [0.3](../../manual/00-Introduction/0.3-how-to-use-this-manual.md) | How to use this manual | Explanation |
| [1.1](../../manual/01-foundations/1.1-what-fleet-is.md) | How Fleet works | Explanation |
| [1.2](../../manual/01-foundations/1.2-how-fleet-reaches-a-device.md) | How Fleet reaches a device | Explanation |
| [1.3](../../manual/01-foundations/1.3-hosts-fleets-labels.md) | Hosts, fleets, labels, and targeting | Explanation |
| [1.4](../../manual/01-foundations/1.4-identity-and-roles.md) | Identity and roles | Explanation |
| [1.5](../../manual/01-foundations/1.5-audit-and-activity.md) | Audit and activity | Explanation |
| [1.6](../../manual/01-foundations/1.6-the-fleet-server.md) | The Fleet server | Explanation |
| [2.1](../../manual/02-administer-and-deploy-fleet/2.1-administration-model-and-deployment-choices.md) | Administration model and deployment choices | Explanation |
| [2.2](../../manual/02-administer-and-deploy-fleet/2.2-self-hosting-architecture-and-capacity.md) | Self-hosting architecture and capacity | Explanation |
| [2.3](../../manual/02-administer-and-deploy-fleet/2.3-deploy-on-aws-or-gcp.md) | Deploy on AWS or GCP | Explanation |
| [2.4](../../manual/02-administer-and-deploy-fleet/2.4-deploy-with-containers-or-virtual-machines.md) | Deploy with containers or virtual machines | Explanation |
| [2.5](../../manual/02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md) | Identity providers, SSO, SCIM, and role sync | Explanation |
| [2.6](../../manual/02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md) | User accounts, roles, and service identities | Explanation |
| [2.7](../../manual/02-administer-and-deploy-fleet/2.7-organization-and-server-settings.md) | Organization and server settings | Explanation |
| [2.8](../../manual/02-administer-and-deploy-fleet/2.8-activity-audit-logs-and-log-delivery.md) | Activity, audit logs, and log delivery | Explanation |
| [2.9](../../manual/02-administer-and-deploy-fleet/2.9-mdm-architecture-and-foundations.md) | MDM architecture and foundations | Explanation |
| [2.10](../../manual/02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md) | Apple MDM configuration | Explanation |
| [2.11](../../manual/02-administer-and-deploy-fleet/2.11-configure-windows-management.md) | Configure Windows management | Explanation |
| [2.12](../../manual/02-administer-and-deploy-fleet/2.12-bind-android-enterprise.md) | Bind Android Enterprise | Explanation |
| [2.13](../../manual/02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md) | Connect certificate authorities | Explanation |
| [3.1](../../manual/03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md) | Enrollment design and host lifecycle | Explanation |
| [3.8](../../manual/03-connect-devices/3.8-manage-fleetd-orbit-and-updates.md) | Manage fleetd, Orbit, and updates | Explanation |
| [4.1](../../manual/04-know-your-devices/4.1-understand-hosts-vitals-and-inventory.md) | Understand host data, vitals, and inventory | Explanation |
| [4.2](../../manual/04-know-your-devices/4.2-run-queries-and-reports.md) | Run queries and read reports | Explanation |
| [4.3](../../manual/04-know-your-devices/4.3-use-policies-for-compliance.md) | Use policies for compliance | Explanation |
| [4.4](../../manual/04-know-your-devices/4.4-understand-software-and-vulnerabilities.md) | Understand software and vulnerabilities | Explanation |
| [4.5](../../manual/04-know-your-devices/4.5-monitor-fleet-wide-state.md) | Monitor fleet-wide state | Explanation |
| [4.6](../../manual/04-know-your-devices/4.6-advanced-osquery-queries-and-tables.md) | Advanced osquery: query design, tables, and performance | Explanation |
| [4.7](../../manual/04-know-your-devices/4.7-extend-osquery-with-custom-tables-and-plugins.md) | Extend Fleet telemetry | Explanation |
| [5.1](../../manual/05-manage-devices/5.1-plan-target-and-govern-device-changes.md) | Plan, target, and govern device changes | Explanation |
| [5.2](../../manual/05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) | Manage configuration profiles and declarative settings | Explanation |
| [5.3](../../manual/05-manage-devices/5.3-run-and-manage-scripts.md) | Run and manage scripts | Explanation |
| [5.4](../../manual/05-manage-devices/5.4-manage-software-and-applications.md) | Manage software and applications | Explanation |
| [5.5](../../manual/05-manage-devices/5.5-design-setup-and-self-service-experiences.md) | Design setup and self-service experiences | Explanation |
| [5.6](../../manual/05-manage-devices/5.6-control-operating-system-updates.md) | Control operating system updates | Explanation |
| [5.7](../../manual/05-manage-devices/5.7-control-devices-and-send-mdm-commands.md) | Control devices and send custom MDM commands | Explanation |
| [5.8](../../manual/05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md) | Enforce disk encryption and manage recovery credentials | Explanation |
| [5.9](../../manual/05-manage-devices/5.9-automate-remediation-with-policies.md) | Automate responses to policy failures | Explanation |
| [6.1](../../manual/06-automate-fleet/6.1-automation-design-and-change-control.md) | Design safe automation and control change | Explanation |
| [6.2](../../manual/06-automate-fleet/6.2-manage-fleet-with-gitops.md) | Manage Fleet with GitOps | Explanation |
| [6.3](../../manual/06-automate-fleet/6.3-use-the-fleet-rest-api.md) | Use the Fleet REST API | Explanation |
| [6.4](../../manual/06-automate-fleet/6.4-use-fleetctl.md) | Operate Fleet with fleetctl | Explanation |
| [6.5](../../manual/06-automate-fleet/6.5-integrations-webhooks-and-external-workflows.md) | Connect integrations, webhooks, and external workflows | Explanation |
| [7.1](../../manual/07-operate-fleet/7.1-define-the-service-operating-model.md) | Define the service operating model | Explanation |
| [7.2](../../manual/07-operate-fleet/7.2-back-up-and-restore-service-state.md) | Back up and restore service state | Explanation |
| [7.3](../../manual/07-operate-fleet/7.3-upgrade-fleet-and-fleetd.md) | Upgrade Fleet server and coordinate fleetd releases | Explanation |
| [7.4](../../manual/07-operate-fleet/7.4-observe-progress-and-service-health.md) | Observe progress, performance, and service health | Explanation |
| [7.5](../../manual/07-operate-fleet/7.5-maintain-capacity-and-availability.md) | Maintain capacity and availability | Explanation |
| [7.6](../../manual/07-operate-fleet/7.6-maintain-credentials-certificates-and-access.md) | Maintain credentials, certificates, and privileged access | Explanation |
| [7.7](../../manual/07-operate-fleet/7.7-production-readiness-checklist-and-handoff.md) | Production readiness checklist and handoff | Explanation |
| [7.8](../../manual/07-operate-fleet/7.8-retire-a-fleet-deployment.md) | Retire a Fleet deployment | Explanation |
| [a.1](../../manual/09-appendices/a.1-capability-index.md) | Capability index | Reference |
| [a.2](../../manual/09-appendices/a.2-platform-capability-matrix.md) | Platform capability matrix | Reference |
| [a.3](../../manual/09-appendices/a.3-configuration-model-and-precedence.md) | Configuration sources, scopes, and precedence | Reference |
| [a.4](../../manual/09-appendices/a.4-roles-and-permissions-matrix.md) | Roles and permissions matrix | Reference |
| [a.5](../../manual/09-appendices/a.5-interface-index.md) | Action-to-interface index | Reference |
| [a.6](../../manual/09-appendices/a.6-glossary-and-release-compatibility.md) | Terminology and version boundaries | Reference |
| [a.7](../../manual/09-appendices/a.7-fleetctl-command-reference.md) | fleetctl command index and behaviour | Reference |
| [a.8](../../manual/09-appendices/a.8-api-action-and-endpoint-reference.md) | API access, versioning, and exposure | Reference |
| [a.10](../../manual/09-appendices/a.10-subject-index.md) | Subject index | Reference |

## Validation

The production build and both editions' link/image checks pass. Browser checks
covered the legend, macOS enrollment, software management, and subject index in
both editions and both themes, including theme persistence after reload. The
legend also passes at a 390 px mobile width, with one visible variant per marker
before JavaScript runs. Print styling keeps the marks legible on white paper.

All eight SVGs match across editions. Existing headings, code fences, and image
briefs are unchanged, and the screenshot checklist remains synchronized. The
chapter prose is unchanged apart from the legend and the added image prefixes.
