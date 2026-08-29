---
title: "API action and endpoint reference"
chapter: "Appendices and indexes"
section: "A.8"
sidebar_position: 8
status: drafting
verified_against: Fleet 4.90.1
verified_on: 2026-08-25
verified_source: "partial: route classes, versioning and exposure verified at git tag fleet-v4.90.1; independent review not yet run"
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

# API action and endpoint reference

Fleet's API is easier to reason about once you stop reading it as a list of endpoints and start reading it as **six classes of caller**. Every route belongs to exactly one, the class decides how a request proves who it is, and most confusion about Fleet's API is a request arriving in the wrong class.

## What this appendix carries

![Reference](../_assets/icons/reference.svg) The organizing model, the authentication rules, the versioning scheme, and the matrix of what has to be reachable from where. Those are the parts that make the API usable and that are not collected in one place anywhere else.

Per-endpoint parameters, request bodies and response shapes live in Fleet's own REST API reference. **That reference is hand-maintained**, so treat it as the best available account rather than a guarantee that it matches the release you are running. This appendix points there rather than copying it.

## Six classes of route

![Reference](../_assets/icons/reference.svg) Fleet registers every endpoint through one of six authenticators. Knowing which class a route belongs to answers what credential it wants, what a `401` means, and whether it can be exposed to the internet.

| Class | Who calls it | Credential |
|---|---|---|
| **User** | A person or an API-only account, through the UI, `fleetctl`, GitOps or a script | A Fleet API token, sent as `Authorization: Bearer <token>` |
| **Host** | osquery on an enrolled device | The osquery node key issued at enrollment |
| **Orbit** | Orbit on an enrolled device | The orbit node key, which is separate from osquery's |
| **Device** | Fleet Desktop, and the **My device** page an end user opens | A per-device token, not a user account |
| **Android** | Google's Android Management API, calling back into Fleet | Its own token, described in [2.8](../02-administer-and-deploy-fleet/2.8-windows-and-android-management-configuration.md) |
| **No auth** | Endpoints that must work before any credential exists, such as SSO initiation and callback | None |

The first is the one people mean by "the Fleet API". The middle three are why [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md) treats a host's credentials as more than one thing: Orbit and osquery authenticate separately, with separate keys, so a host can be half-working in a way a single credential could not produce.

The device class is the one most often missed when planning network exposure. It is how an end user reaches their own device page, and it authenticates the device rather than the person.

## How a user request authenticates

![Reference](../_assets/icons/reference.svg) A Fleet API token belongs to a user account, which is what makes [2.3](../02-administer-and-deploy-fleet/2.3-user-accounts-roles-and-service-identities.md)'s advice about giving automation its own account matter: the token inherits that account's role and scope, and the activity record attributes the work to it.

Send it as a bearer token:

```http
Authorization: Bearer <your token>
```

Two ways to obtain one. Through the UI, under **My account** and **Get API token**. Or by calling the login endpoint with an email and password, which returns a token.

**For SSO and MFA users the second route is closed.** Email and password login is disabled for those accounts, so the token has to come from the profile page in the UI. An automation account created for API use is the usual answer, and [2.3](../02-administer-and-deploy-fleet/2.3-user-accounts-roles-and-service-identities.md) covers creating one with an explicit role.

## The same endpoint reaches several paths, and the set is not global

![Reference](../_assets/icons/reference.svg) A route is registered under each version its **own registering module** declares, plus a `latest` alias. So a core route such as the host list exists at three paths at once:

```
/api/v1/fleet/hosts
/api/2022-04/fleet/hosts
/api/latest/fleet/hosts
```

`latest` is a registered path rather than a redirect, so nothing resolves or forwards at request time.

> **Versions resolve in two stages, and not once for the API.** Each module declares an ordered base set, and **an individual route can narrow that set further** with its own start and end boundaries, so a `latest` registration is not added to every route. The core module declares `v1` and `2022-04`; other modules declare their own, and at least one route family is fixed to `v1` alone. **There is therefore no single dated prefix on which the whole API exists.** Default to the documented method and path for each resource, prefix included ([6.3](../06-automate-fleet/6.3-use-the-fleet-rest-api.md)).

That has one practical consequence worth planning around. **A proxy rule, allowlist or firewall pattern written against `/api/v1/` does not cover the other two.** Fleet's own documentation uses `/api/v1/` and `/api/latest/` in different places, and both work, so matching on a single literal version will let some traffic through and not other traffic that does exactly the same thing. Match `/api/*/fleet/` where you can.

## Paths that sit outside `/api`

![Reference](../_assets/icons/reference.svg) Some routes are deliberately not under `/api`, because they are not REST endpoints and are not meant for API clients or browsers. The Apple MDM protocol paths are the clearest case.

A proxy configuration written on the assumption that everything Fleet serves lives under `/api` will miss them, and the symptom is device management failing while the API and UI look healthy. [2.6](../02-administer-and-deploy-fleet/2.6-mdm-architecture-and-foundations.md) covers why the set of these grows as features are enabled.

## What has to be reachable from the internet

![Reference](../_assets/icons/reference.svg) This is the matrix that network reviews ask for, and the one that is genuinely uncollected elsewhere. Expose only what a capability needs.

**Baseline, for agents on devices that leave the network:**

| Path | For |
|---|---|
| `/api/osquery`, `/api/v1/osquery` | osquery check-in |
| `/api/fleet/orbit/*` | Orbit, including scripts and software |
| `/api/fleet/device/ping` | Fleet Desktop reachability |
| `/api/*/fleet/device/*/desktop` | The minimum for Fleet Desktop's failing-policy count |

**For `fleetctl` from outside the network**, add `/api/setup`, `/api/*/setup` and `/api/*/fleet/*`.

**For Apple device management**, add `/mdm/apple/scep` and `/mdm/apple/mdm`, both outside `/api`, plus `/api/mdm/apple/enroll` for automatic enrollment and `/api/*/fleet/device/*` for the end user's device page. Setup-experience features each add their own: identity-provider authentication during setup adds the `/mdm/sso` family and `/assets/*`, an end user licence agreement adds `/api/*/fleet/mdm/setup/eula/*`, a bootstrap package adds `/api/*/fleet/mdm/bootstrap`, and Fleet's own Platform SSO extension adds `/api/mdm/apple/psso/*` and `/.well-known/apple-app-site-association`.

**For Windows device management**, add the four Microsoft protocol paths under `/api/mdm/microsoft/`, which are `management`, `discovery`, `policy` and `enroll`, plus `/api/mdm/microsoft/tos` for automatic enrollment. [2.8](../02-administer-and-deploy-fleet/2.8-windows-and-android-management-configuration.md) covers why exposing some but not all of these fails partway rather than cleanly.

**For any Apple device enrolled by link**, which is macOS as well as iOS and iPadOS, add `/enroll` and `/api/*/fleet/enrollment_profiles/ota`. Those two are the over-the-air enrollment path and are not platform-specific; a reverse proxy that exposes them only for mobile will block a Mac enrolling from the **Add hosts** link ([3.2](../03-connect-devices/3.2-enroll-macos-devices.md), [3.5](../03-connect-devices/3.5-enroll-ios-and-ipados-devices.md)).

**For iOS and iPadOS specifically**, in-house app delivery adds `/api/*/fleet/software/titles/*/in_house_app`, and account-driven user enrollment adds the `/api/mdm/apple/account_driven_enroll` family, its SSO paths, and `/mdm/apple/service_discovery`.

**For Android**, add `/enroll`, `/api/*/fleet/android_enterprise/enrollment_token`, and `/api/v1/fleet/android_enterprise/pubsub`. That last one is how Google delivers device events, is why [2.8](../02-administer-and-deploy-fleet/2.8-windows-and-android-management-configuration.md) requires a publicly reachable server URL, and is **fixed at `v1`** rather than being served under every prefix, so a wildcard rule written for the others will not match it.

## Pagination and ordering

![Reference](../_assets/icons/reference.svg) List endpoints share a convention: `page` for the zero-based page number, `per_page` for its size, `order_key` for the column to sort by, and `order_direction` for the direction.

```
GET /api/v1/fleet/activities?page=0&per_page=10&order_key=created_at&order_direction=desc
```

An endpoint's valid `order_key` values are its own, and Fleet's reference documents them per endpoint.

## Where the rest lives

![Reference](../_assets/icons/reference.svg) Request bodies, response shapes, per-endpoint parameters and error codes are in Fleet's REST API reference at `fleetdm.com/docs/rest-api/rest-api`, and endpoints intended for contributors rather than administrators are documented separately in the Fleet repository.

Which actions each role may perform is [a.4](a.4-roles-and-permissions-matrix.md). Which surface can perform a given action at all is [a.5](a.5-interface-index.md).

## Version notes

![Reference](../_assets/icons/reference.svg) Verified against Fleet 4.90.1. `v1` and `2022-04` are what the **core** module declares at this release, and the `latest` alias is added to whatever set each module declares.

**This appendix is not a complete inventory.** Fleet's own machine-readable route catalogue carries 234 entries with 12 marked deprecated, and it does not enumerate the backward-compatible name aliases that also exist. Treat what follows as a map of the classes and the rules, not as a list of everything Fleet serves.

The public-exposure matrix grows as features are enabled and is the part of this appendix most likely to change between releases. Re-check it against Fleet's own guidance when adding a capability rather than assuming this list still covers it.
