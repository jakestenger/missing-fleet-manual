---
title: "API access, versioning, and exposure"
chapter: "Appendices and indexes"
section: "A.8"
sidebar_position: 8
status: drafting
verified_against: Fleet 4.90.1
verified_on: 2026-08-29
verified_source: "drafted against fleet-v4.90.1 (dd0200f062), with every path in the exposure matrix read from the server's own route registrations rather than from the published reference. Citation ledger at research/section-notes/a.8-notes.md, which records the evidence class of every path and the derivation of every count"
reviewed_by:
reviewed_on:
further_reading:
  - https://fleetdm.com/docs/rest-api/rest-api
  - https://fleetdm.com/guides/what-api-endpoints-to-expose-to-the-public-internet
feature_requests:
  labels: [":product"]
  match: ["API", "endpoint", "REST", "token"]
  exclude: []
---

# API access, versioning, and exposure

Fleet's request surface is easier to reason about once you stop reading it as a list of endpoints and start reading it as **six classes of caller**. The class decides what a request must present, what a `401` means, and whether a path can be exposed to the internet. Most confusion about Fleet's API is a request arriving in the wrong class.

## What this appendix carries

![Reference](../_assets/icons/reference.svg) The caller model, the authentication rules, the versioning scheme, and the matrix of what has to be reachable from where. Those are the parts that make the request surface usable and that are not collected in one place anywhere else.

Per-endpoint parameters, request bodies and response shapes live in Fleet's own REST API reference. **That reference is hand-maintained**, so treat it as the best available account rather than a guarantee that it matches the release you are running. This appendix points there rather than copying it.

Three questions belong elsewhere and are deliberately unanswered here. **Which role may perform an action is [a.4](a.4-roles-and-permissions-matrix.md).** Which interface can perform it at all is [a.5](a.5-interface-index.md). How to use the API in practice is [6.3](../06-automate-fleet/6.3-use-the-fleet-rest-api.md).

## Six classes of caller

![Reference](../_assets/icons/reference.svg) **This is an ingress model rather than a claim about how Fleet registers routes.** It groups callers by what they must present, which is the question a network design turns on. Fleet does not pass every handler through one of six constructors, and a few of the most important paths are registered directly on the server's root router.

| Class | Who calls it | What it presents |
|---|---|---|
| **User** | A person or an API-only account, through the UI, `fleetctl`, GitOps or a script | A Fleet API token, as `Authorization: Bearer <token>` |
| **Host** | osquery on an enrolled device | The osquery node key issued at enrollment |
| **Orbit** | Orbit on an enrolled device | The Orbit node key, a separate credential from osquery's |
| **Device** | Fleet Desktop, and the **My device** page an end user opens | A per-device token, not a user account |
| **fleetd certificate** | fleetd, fetching a certificate template Fleet has asked it to install and reporting the result | The **Orbit** node key, in an `Authentication` header |
| **Route-local or protocol** | Everything whose credential belongs to the route rather than to Fleet's shared authenticator | An enrollment secret, a download token, a SAML response, a query-string token, a device identity certificate, or a protocol signature |

> **Do not read the last class as "unauthenticated".** It is the class where Fleet's shared authenticator is skipped and the route does its own checking, and most of its members require something. Google's callback for Android events presents a route-specific token. An over-the-air enrollment presents an enroll secret. Apple's protocol paths authenticate the device by its identity certificate. **A path here is not safe to expose merely because no bearer token appears in the request.**

The first class is the one people mean by "the Fleet API". The Host and Orbit classes are why [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md) treats a host's credentials as more than one thing: they authenticate separately with separate keys, so a host can be half-working in a way a single credential could not produce.

**The Device class is the one most often missed when planning exposure, and it is far larger than the page it is named after.** It authenticates the device rather than the person, and at this release it carries policies, software inventory, self-service install and uninstall, certificates, the setup-experience status, Linux escrow triggering, conditional-access bypass and MDM migration, alongside the ping and desktop calls that Fleet Desktop needs for its failing-policy count. Exposing only those two leaves most of what an end user can do unreachable, and the symptom is a device page that loads and does nothing.

**The fleetd certificate class is easy to mistake for an Android class.** It is not Google calling Fleet. It is fleetd on a device, holding an Orbit node key, asking for a certificate template and reporting what it did with it. Google's own callback belongs to the route-local class.

## How a user request authenticates

![Reference](../_assets/icons/reference.svg) A Fleet API token belongs to a user account, which is what makes [2.3](../02-administer-and-deploy-fleet/2.3-user-accounts-roles-and-service-identities.md)'s advice about giving automation its own account matter: the token inherits that account's role and scope, and the activity record attributes the work to it.

Send it as a bearer token:

```http
Authorization: Bearer <your token>
```

Two ways to obtain one. Through the UI, under **My account** and **Get API token**. Or by calling the login endpoint with an email and password, which returns a token.

**For SSO and MFA users the second route is closed.** Email and password login is disabled for those accounts, so the token has to come from the profile page in the UI. An automation account created for API use is the usual answer, and [2.3](../02-administer-and-deploy-fleet/2.3-user-accounts-roles-and-service-identities.md) covers creating one with an explicit role.

## Version prefixes expand for some routes and not others

![Reference](../_assets/icons/reference.svg) **A route declared with Fleet's version placeholder** is registered under each version its own registering module declares, plus a `latest` alias. So a core route such as the host list exists at three paths at once:

```
/api/v1/fleet/hosts
/api/2022-04/fleet/hosts
/api/latest/fleet/hosts
```

`latest` is inserted into the route expression and handled directly, so nothing resolves or forwards at request time.

> ### Three things narrow or bypass that expansion
>
> **Each module declares its own ordered set.** The core module declares `v1` and `2022-04`. The Android module declares `v1` alone, so its versioned routes exist at `v1` and `latest` and never at `2022-04`.
>
> **An individual route can narrow its module's set further**, with its own start and end boundaries. A route that ends before its module's last version does not get a `latest` alias at all.
>
> **Some paths are literal and never expand.** Fleet's own SSO initiation and callback are written as `/api/v1/fleet/sso`, fixed. So is Android's event callback. And the Apple MDM protocol paths, the SCEP service, Apple service discovery and the Platform SSO well-known document are registered directly on the root router, outside the versioned mechanism entirely.

That has one practical consequence worth planning around. **A proxy rule, allowlist or firewall pattern written against `/api/v1/` does not cover the rest.** Fleet's own documentation uses `/api/v1/` and `/api/latest/` in different places and both work, so matching one literal version lets some traffic through and not other traffic doing exactly the same thing.

**Match the three prefixes explicitly rather than with a wildcard.** `v1`, `2022-04` and `latest` are the complete set at this release. A wildcard segment written as `/api/*/fleet/` means different things in different proxies and will accept segments you did not intend. Then handle the unversioned families separately: `/api/fleet/orbit/*`, `/api/osquery/*`, `/api/fleetd/*`, `/api/mdm/*`, `/api/setup`, and the paths outside `/api` below.

## Two origins, and a prefix

![Reference](../_assets/icons/reference.svg) Some routes are deliberately not under `/api`, because they are not REST endpoints and are not meant for API clients or browsers. The Apple MDM protocol paths are the clearest case, along with the SCEP service, the SCEP proxy used for delivering your own certificates, and the Platform SSO well-known document.

A proxy configuration written on the assumption that everything Fleet serves lives under `/api` will miss them, and the symptom is device management failing while the API and UI look healthy. [2.6](../02-administer-and-deploy-fleet/2.6-mdm-architecture-and-foundations.md) covers why the set of these grows as features are enabled.

**Two further things move every path in this appendix**, and a matrix that ignores them is wrong for your deployment:

- **A configured URL prefix** is prepended to everything Fleet serves. Every path below is origin-relative and assumes no prefix.
- **Apple device management can be given its own server URL**, separate from the one everything else uses. Where that is set, the Apple protocol paths are reachable at that origin rather than at Fleet's main one, and the two need separate ingress treatment.

## What has to be reachable, by capability

![Reference](../_assets/icons/reference.svg) This is the matrix network reviews ask for, and the one genuinely uncollected elsewhere. **Expose only what a capability needs.**

> ### What this matrix includes, and what it does not
>
> **Included:** every path a caller outside the Fleet server must reach for a named capability to work. Devices, end users, administrators, and third parties calling in.
>
> **Excluded deliberately, each for a reason.** Fleet's health, version and metrics endpoints and its debug tree are operator surfaces rather than capability surfaces, and [7.4](../07-operate-fleet/7.4-observe-progress-and-service-health.md) governs who should reach them. The metrics endpoint in particular is not mounted at all unless you configure credentials for it. The UI's own frontend and asset routes are excluded except where a capability's flow passes through one, which is called out where it happens.
>
> **A capability absent from this matrix has not been assessed**, rather than been found to need nothing. The ledger records which were assessed.

**Baseline, for agents on devices that leave the network:**

| Path | For |
|---|---|
| `/api/osquery/*`, `/api/v1/osquery/*` | osquery check-in and log submission |
| `/api/fleet/orbit/*` | Orbit, including scripts and software |
| `/api/{v1,2022-04,latest}/fleet/device/*` | **The whole Device class.** Fleet Desktop's ping and counts, and everything an end user does on their own device page |

**For `fleetctl` and API clients from outside the network**, add `/api/{v1,2022-04,latest}/fleet/*`, plus `/api/setup` and `/api/v1/setup` for the initial setup flow. **Setup is not a versioned family**: there is no `/api/2022-04/setup` and no `/api/latest/setup`.

**For identity**, Fleet's own SSO is `/api/v1/fleet/sso` and `/api/v1/fleet/sso/callback`, both fixed at `v1` and reachable under no other prefix. **SCIM provisioning** is `/api/v1/fleet/scim/*` and `/api/latest/fleet/scim/*`, those two prefixes only, which is what [2.2](../02-administer-and-deploy-fleet/2.2-identity-providers-sso-scim-and-role-sync.md) needs reachable by your identity provider.

**For Apple device management**, add `/mdm/apple/scep` and `/mdm/apple/mdm`, both outside `/api`, plus `/api/mdm/apple/enroll` for automatic enrollment. Where hardware attestation is enabled, Fleet puts its own ACME directory URL into the enrollment profile, so add `/api/mdm/acme/*`. Where an installer is served to devices, that is `/api/mdm/apple/installer`.

**Setup-experience features each add their own:**

| Feature | Paths |
|---|---|
| Identity-provider authentication during setup | `/mdm/sso` and `/assets/*`, plus the callback the provider returns to at `/api/{v1,2022-04,latest}/fleet/mdm/sso/callback` |
| End user licence agreement | `/api/{v1,2022-04,latest}/fleet/setup_experience/eula/{token}`. The older `/fleet/mdm/setup/eula/*` form is deprecated |
| Bootstrap package | `/api/{v1,2022-04,latest}/fleet/bootstrap`. The older `/fleet/mdm/bootstrap` form is deprecated |
| Fleet's Platform SSO extension | `/api/mdm/apple/psso/*` and `/.well-known/apple-app-site-association` |

**For any Apple device enrolled by link**, which is macOS as well as iOS and iPadOS, add `/enroll` and `/api/{v1,2022-04,latest}/fleet/enrollment_profiles/ota`, **and `/api/{v1,2022-04,latest}/fleet/ota_enrollment`**, which is where the profile those two hand out sends the device next. Omitting the third leaves an enrollment that starts and never completes. None of the three is platform-specific: a reverse proxy that exposes them only for mobile will block a Mac enrolling from the **Add hosts** link ([3.2](../03-connect-devices/3.2-enroll-macos-devices.md), [3.5](../03-connect-devices/3.5-enroll-ios-and-ipados-devices.md)).

**For iOS and iPadOS specifically**, in-house app delivery adds **two** paths, `/api/{v1,2022-04,latest}/fleet/software/titles/*/in_house_app/{token}` and the same with `/manifest/{token}` before the token. A rule matching only the first serves the app and not the manifest that tells the device to install it. Account-driven user enrollment adds the account-driven enrollment paths, both service-discovery paths including `/mdm/apple/service_discovery`, and the frontend SSO routes its flow passes through.

**For Windows device management**, add the four Microsoft protocol paths under `/api/mdm/microsoft/`, which are `management`, `discovery`, `policy` and `enroll`, plus `/api/mdm/microsoft/tos` for automatic enrollment. [2.8](../02-administer-and-deploy-fleet/2.8-windows-and-android-management-configuration.md) covers why exposing some but not all of these fails partway rather than cleanly.

**For Android**, add `/enroll`, `/api/{v1,latest}/fleet/android_enterprise/enrollment_token`, and the enablement callback `/api/{v1,latest}/fleet/android_enterprise/connect/{token}`. **Android's module declares `v1` alone**, so those two exist at `v1` and `latest` and nowhere else, which is why the prefix list here is shorter than everywhere above. The event callback `/api/v1/fleet/android_enterprise/pubsub` is a literal path fixed at `v1`, is how Google delivers device events, and is why [2.8](../02-administer-and-deploy-fleet/2.8-windows-and-android-management-configuration.md) requires a publicly reachable server URL.

**For delivering your own certificates to devices**, rather than Fleet's, add `/mdm/scep/proxy/*`, which sits outside `/api`. Where fleetd fetches and reports on those certificates, add `/api/fleetd/certificates/*`.

**For the Google Calendar integration**, add `/api/{v1,2022-04,latest}/fleet/calendar/webhook/{event_uuid}`, which is the address Fleet gives Google and which Google calls back on.

**For Okta conditional access**, add `/api/fleet/conditional_access/scep`, `/api/fleet/conditional_access/idp/metadata` and `/api/fleet/conditional_access/idp/sso`. None of the three is versioned.

## API conventions

![Reference](../_assets/icons/reference.svg) List endpoints share a convention: `page` for the zero-based page number, `per_page` for its size, `order_key` for the column to sort by, and `order_direction` for the direction.

```
GET /api/v1/fleet/activities?page=0&per_page=10&order_key=created_at&order_direction=desc
```

An endpoint's valid `order_key` values are its own, and Fleet's reference documents them per endpoint. [6.3](../06-automate-fleet/6.3-use-the-fleet-rest-api.md) covers paginating a large result set in practice.

## Where the rest lives

![Reference](../_assets/icons/reference.svg) Request bodies, response shapes, per-endpoint parameters and error codes are in Fleet's REST API reference at `fleetdm.com/docs/rest-api/rest-api`, and endpoints intended for contributors rather than administrators are documented separately in the Fleet repository.

Which actions each role may perform is [a.4](a.4-roles-and-permissions-matrix.md). Which surface can perform a given action at all is [a.5](a.5-interface-index.md).

## Version notes

![Reference](../_assets/icons/reference.svg) Verified against Fleet 4.90.1. `v1` and `2022-04` are what the **core** module declares at this release; other modules declare their own, and `latest` is added to whatever set each declares.

**This appendix is not a complete inventory of everything Fleet serves, and one number is easy to mistake for one.** Fleet embeds a catalogue of 234 method-and-path entries, 12 of them marked deprecated. **That catalogue is the allowlist for API-only accounts rather than a list of routes.** Its own validation runs in one direction, checking that every catalogue entry has a registered route, which does not establish the reverse. Fleet separately registers backward-compatible path aliases that the catalogue does not carry. Treat the number as the size of the allowlist and nothing more.

**The exposure matrix is the part most likely to change between releases**, because it grows as features are enabled and as features are added. Re-check it against Fleet's own guidance when adding a capability rather than assuming this list still covers it, and re-check it after an upgrade.
