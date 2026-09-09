# Fuller company and product introductions, 2026-09-09

Jake requested more expansive marketing prose in 0.1 and 0.2 after reviewing the live
opening sequence. The company story now emphasizes transparency across software,
public work tracking, documentation, and the employee handbook. The product story
explains the problems solved by mixed-platform management, vulnerability ingestion,
maintained applications, integration, and shared IT/security evidence.

Both 4.91 and 4.90 receive the same narrative with their edition metadata retained.
The 0.3 contents descriptions and STYLE.md opening-chapter guidance are also updated.
Images, retained prompts, chapter order, slugs, and procedures are unchanged.

## Company context: public sources read 2026-09-09

| Source | Claims drawn from it |
|---|---|
| https://fleetdm.com/handbook/company | Purpose, five values, company history and remote contributors |
| https://fleetdm.com/lp/open-source | Public source, issues and roadmap; practical inspectability |
| https://fleetdm.com/handbook/engineering | Issue tracking, bug-fix links, review and implementation workflow |
| https://fleetdm.com/handbook/product-design | Feedback, design and release planning |
| https://fleetdm.com/handbook/company/why-this-way | Handbook-first practice, open-core model, participation |
| https://fleetdm.com/docs/get-started/why-fleet | Scope transparency toward device users |

The prose uses concise paraphrases from each source, then illustrates their practical
value in original administrator scenarios. It describes public-by-default work rather
than asserting that private customer information or undisclosed security reports are
public. The engineering handbook explicitly describes confidential handling for those.
Public visibility is not presented as a promise that every requested feature will ship
or that a release plan guarantees a particular delivery date.

Company context is current to the reading date, not frozen to either software release.

## Product claims: evidence and scope

Release tags inspected in the local Fleet source checkout:

- `fleet-v4.90.0`: `7c428c6e467d4dd642b0375350eecca7138746d1`
- `fleet-v4.91.0`: `35fc1c0244907c157a64d05d4ec291c0a3a20e32`

| Claim | Evidence | Editorial boundary |
|---|---|---|
| Multi-platform MDM and device management in one product | Existing 1.1 platform table and Part III chapters in both editions; public Why Fleet and open-source product descriptions | Native Apple/Windows/Android MDM is distinguished from Linux agent management and ChromeOS inventory visibility |
| Automatic ingestion and matching of vulnerability data | `docs/Contributing/architecture/security-compliance/vulnerability-processing.md:28-35` at both tags describes prepared feed downloads and matching against host software; existing 4.4 describes software/OS paths, sources and scheduled processing | Supported inventory, scheduled processing, no promise of instant detection or complete coverage |
| Extensive maintained-app catalog for macOS and Windows | `ee/maintained-apps/outputs/apps.json` at both tags; `ee/maintained-apps/README.md`; https://fleetdm.com/guides/fleet-maintained-apps | Catalog preparation and patch-policy deployment are described separately; configured policies request installation |
| Examples Chrome, Firefox, Slack and Zoom | Their manifest directories exist at both tags under `ee/maintained-apps/outputs/` | Examples, not an exhaustive title or version list |
| API-first extensibility | Public https://fleetdm.com/lp/open-source positioning; tagged `docs/REST API/rest-api.md`; existing 6.3, 6.4, 6.5 and 2.8 | Integration examples are proposed uses of supported interfaces, not promises of turnkey integrations or universal endpoint parity |
| IT administration and security evidence share a system | Existing 4.1, 4.3, 4.4, Part V, 1.5 and 2.8 | Support for controls and audit preparation; no automatic certification or guaranteed audit outcome |

For reproducibility, the catalog JSON contains 1,350 platform entries at 4.90.0 and
1,396 at 4.91.0. Counting distinct app directories with a darwin.json or windows.json
manifest yields 1,103 and 1,145 respectively. These measurements support the catalog's
breadth; the reader-facing chapter avoids a brittle live catalog total and does not
confuse platform entries with distinct app titles. The named examples occur in both.

The public maintained-app guide supports the description of installation metadata,
script preparation and testing. Existing 5.4 and 5.9 establish the distinction between
catalog/library updates and installing on hosts. No current website claim about later
release functionality is imported into either edition.

The rollout, audit, and integration examples illustrate combinations of existing
capabilities. They are editorial scenarios, not measured customer outcomes or a new
full verification of every owning chapter.

## Validation

- Full Docusaurus production build passed for both editions.
- All 13 PR-workflow Python checks returned zero; source-name/schema checks used the
  local 4.91 release extract. Existing cross-reference/frequency advisories remain
  outside this prose change; no new opening-chapter findings require correction.
- Links, anchors, and images resolve in all 85 chapters of each edition.
- Image and screenshot prompt comments were compared against the parent commit and
  remain byte-for-byte unchanged in both edited chapters and both editions.
- The updated standalone reading preview has working chapter and heading links.
- `git diff --check` passed.
