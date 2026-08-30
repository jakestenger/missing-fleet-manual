---
title: "API access, versioning, and exposure"
chapter: "Appendices and indexes"
section: "A.8"
sidebar_position: 8
status: drafting
verified_against: Fleet 4.90.1
verified_on: 2026-08-29
verified_source: "drafted against fleet-v4.90.1 (dd0200f062), with every path in the exposure matrix read from the server's own route registrations rather than from the published reference. Citation ledger at research/section-notes/a.8-notes.md, which records the evidence class of every path and distinguishes the routes Fleet registers from the ones it emits"
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

Fleet's request surface is easier to reason about once you stop reading it as a list of endpoints and start reading it as **callers**. Five of them share a credential Fleet's own authenticator understands. Everything else bypasses that authenticator, and **whether such a route requires anything at all has to be established route by route**: some carry a token or a certificate, and some are genuinely unauthenticated.

**What a caller must present is the useful grouping. What has to be reachable is a different question**, answered by capability further down, and the two do not line up neatly enough to organise one table by the other.

## What this appendix carries

![Reference](../_assets/icons/reference.svg) The caller model, the authentication rules, the versioning scheme, and the matrix of what has to be reachable from where. Those are the parts that make the request surface usable and that are not collected in one place anywhere else.

Per-endpoint parameters, request bodies and response shapes live in Fleet's own REST API reference. **That reference is hand-maintained**, so treat it as the best available account rather than a guarantee that it matches the release you are running. This appendix points there rather than copying it.

Three questions belong elsewhere and are deliberately unanswered here. **Which role may perform an action is [a.4](a.4-roles-and-permissions-matrix.md)**, which carries it action by action against all six roles at both scopes; [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md) explains the model behind it. **Which interface can perform it at all is [a.5](a.5-interface-index.md)**, which carries every action against all four. How to use the API in practice is [6.3](../06-automate-fleet/6.3-use-the-fleet-rest-api.md), which is written.

## Who calls Fleet, and what they present

![Reference](../_assets/icons/reference.svg) **Five shared-credential classes, and everything else.** This groups callers by what they must present. It is not a claim about how Fleet registers routes: Fleet does not pass every handler through one of six constructors, and several of the most important paths are registered directly on the root router.

| Class | Who calls it | What it presents |
|---|---|---|
| **User** | A person through the UI, `fleetctl` or a script; or an API-only account, which cannot use the UI, through `fleetctl`, GitOps or a script | A Fleet API token, as `Authorization: Bearer <token>` |
| **Host** | osquery on an enrolled device | The osquery node key issued at enrollment |
| **Orbit** | Orbit on an enrolled device | The Orbit node key, a separate credential from osquery's |
| **Device** | Fleet Desktop, and the **My device** page an end user opens | A per-device token, not a user account |
| **fleetd certificate** | fleetd, fetching a certificate template Fleet has asked it to install and reporting the result | The **Orbit** node key, in an `Authentication` header |
| **Route-local or protocol** | Everything that does not go through Fleet's shared authenticator. Some of these check a credential themselves; **some require none at all** | An enrollment secret, a download token, a SAML response, a query-string token, a device identity certificate, a credential inside a protocol message, or nothing |

> **The last row is not a class in the sense the other five are.** It is everything left over once the shared authenticator is out of the picture, so **membership tells you nothing**: what a route requires has to be read off that route.
>
> Google's callback for Android events presents a route-specific token. An over-the-air enrollment presents an enroll secret. Apple's protocol paths authenticate the device by its identity certificate. Of the five Windows protocol paths, **policy and enrollment take a token in the request, and management authenticates the device inside the handler**, by a client certificate whose common name carries the device identifier or, failing that, a credential in the message itself. **Discovery and the terms-of-use page genuinely require nothing**, which is ordinary for pre-enrollment surfaces.
>
> What the row's members have in common is only that Fleet's usual authentication middleware did not run. **Fleet's registration comments describe that layer, not the route**, and one of them calls the management path unauthenticated while the handler beneath it rejects an untrusted device. Read the handler.

The first class is the one people mean by "the Fleet API". The Host and Orbit classes are why [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md) treats a host's credentials as more than one thing: they authenticate separately with separate keys, so a host can be half-working in a way a single credential could not produce.

**The Device class is the one most often missed when planning exposure, and it is far larger than the page it is named after.** It authenticates the device rather than the person, and at this release it carries policies, software inventory, self-service install and uninstall, certificates, the setup-experience status, Linux escrow triggering, conditional-access bypass and MDM migration, alongside the ping and desktop calls that Fleet Desktop needs for its failing-policy count. Exposing only those two leaves most of what an end user can do unreachable, and the symptom is a device page that loads and does nothing.

**The fleetd certificate class is easy to mistake for an Android class.** It is not Google calling Fleet. It is fleetd on a device, holding an Orbit node key, asking for a certificate template and reporting what it did with it. Google's own callback belongs to the route-local class.

## How a user request authenticates

![Reference](../_assets/icons/reference.svg) A Fleet API token belongs to a user account, which is what makes [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md)'s advice about giving automation its own account matter: the token inherits that account's role and scope, and the activity record attributes the work to it.

Send it as a bearer token:

```http
Authorization: Bearer <your token>
```

Two ways to obtain one. Through the UI, under **My account** and **Get API token**. Or by calling the login endpoint with an email and password, which returns a token.

**For SSO and MFA users the second route is closed.** Email and password login is disabled for those accounts, so the token has to come from the profile page in the UI. An automation account created for API use is the usual answer, and [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md) covers creating one with an explicit role.

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

## Paths outside `/api`, a prefix, and which base URL Fleet advertises

![Reference](../_assets/icons/reference.svg) Some routes are deliberately not under `/api`, because they are not REST endpoints and are not meant for API clients or browsers. The Apple MDM protocol paths are the clearest case, along with the SCEP service, the SCEP proxy used for delivering your own certificates, and the Platform SSO well-known document.

A proxy configuration written on the assumption that everything Fleet serves lives under `/api` will miss them, and the symptom is device management failing while the API and UI look healthy. [2.9](../02-administer-and-deploy-fleet/2.9-mdm-architecture-and-foundations.md) covers why the set of these grows as features are enabled.

**A configured URL prefix is prepended to everything Fleet serves**, including the paths on the root router, because Fleet wraps the finished router and strips the prefix before dispatch. Every path in this appendix is origin-relative and assumes no prefix.

**Apple device management can be given its own server URL, and that is a narrower thing than it sounds.** It does not create a second listener and it does not make any path unreachable at the main origin, which Fleet expects to resolve to the same server. What it changes is **which base URL Fleet advertises** when it builds a URL for a device or a profile:

| Advertised at the Apple URL | Still advertised at the main URL |
|---|---|
| `/enroll`, the over-the-air profile and `ota_enrollment` endpoints, and `/api/mdm/apple/enroll` | `/api/mdm/apple/installer` |
| `/mdm/apple/scep`, `/mdm/apple/mdm`, and the ACME family, inside enrollment profiles | Platform SSO's issuer, key set and app-site-association document |
| MDM setup SSO and account-driven enrollment | The in-house app **manifest** |
| Generated SCEP-proxy URLs, **including the ones written into Windows profiles** | The server URL fleetd is given |

**Two downloads may not be on a Fleet hostname at all.** Where a content delivery network is configured, the bootstrap package and an in-house app's **package** are handed out as signed CDN URLs. **Configured is not the same as used**: if signing fails, or the stored object cannot be confirmed, Fleet falls back and hands out a Fleet URL instead, logging the failure. The two fall back to different places, the bootstrap package to the Apple base URL and the in-house package to the main server URL.

So those two rows are conditional in a way the rest are not: **the path is registered and reachable either way, and which origin a device is sent to depends on configuration you hold and on whether signing worked at that moment.** Expose the Fleet paths regardless. The in-house app's manifest always stays on the main Fleet URL, so a manifest and its package can end up on different hosts.

The ingress question is therefore not "which paths moved" but **"which hostname will a device have been told to use"**, and every hostname you advertise needs to reach the same Fleet.

## What has to be reachable, by capability

![Reference](../_assets/icons/reference.svg) This is the matrix network reviews ask for, and the one genuinely uncollected elsewhere. **Expose only what a capability needs.**

> ### What this matrix includes, and what it does not
>
> **Included:** every path a caller outside the Fleet server must reach for a named capability to work. Devices, end users, administrators, and third parties calling in.
>
> **Excluded deliberately, each for a reason.** Fleet's health, version and metrics endpoints and its debug tree are operator surfaces rather than capability surfaces, and [7.4](../07-operate-fleet/7.4-observe-progress-and-service-health.md) governs who should reach them. The metrics endpoint in particular is not mounted at all unless you either configure credentials for it or explicitly disable its basic authentication. The UI's own frontend and asset routes are excluded except where a capability's flow passes through one, which is called out where it happens.
>
> **A capability absent from this matrix has not been assessed**, rather than been found to need nothing. The ledger records which were assessed.
>
> **Registered is not the same as required, and that difference is most of this matrix's value.** A route registration tells you a path exists and how it matches. It does not tell you a capability needs that path open. Fleet routinely registers a route under all three version prefixes and then emits exactly one of them in the URL it hands to a device, a browser or a third party, and **the emitted one is what has to be reachable**. Several rows below name a deprecated path for that reason: the replacement is registered, and the older path is the one Fleet still sends.
>
> Where a row names a narrower set than the prefix rules above would suggest, that is deliberate. Opening what Fleet emits is the smaller configuration; opening every registered alias is not wrong, only wider.

**Four capabilities have prerequisites beyond exposure.** SCIM and the SCEP proxy are Premium. Okta conditional access is Premium **and** needs the server private key configured. Apple's root protocol services need that key too, and are not mounted at all without it.

**Baseline, for agents on devices that leave the network:**

| Path | For |
|---|---|
| `/api/osquery/*`, `/api/v1/osquery/*` | osquery check-in and log submission |
| `/api/fleet/orbit/*` | Orbit, including scripts and software |
| `/api/{v1,2022-04,latest}/fleet/device/*` | **The whole Device class.** Fleet Desktop's ping and counts, and everything an end user does on their own device page |

**For `fleetctl` and API clients from outside the network**, add `/api/{v1,2022-04,latest}/fleet/*`, plus `/api/setup` and `/api/v1/setup` for the initial setup flow. **Setup is not a versioned family**: there is no `/api/2022-04/setup` and no `/api/latest/setup`.

**For identity**, Fleet's own SSO is `/api/v1/fleet/sso` and `/api/v1/fleet/sso/callback`, both literal `v1` paths reachable under **no other API-version prefix**, though a configured URL prefix still precedes them.

**SCIM provisioning** is prefix-mounted at `/api/v1/fleet/scim/` and `/api/latest/fleet/scim/`, and those two are what your identity provider needs ([2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md)). One SCIM path is outside that mount: the details endpoint is an ordinary core route and therefore also exists at `2022-04`. SCIM is Premium.

**For Apple device management**, add `/mdm/apple/scep` and `/mdm/apple/mdm`, both outside `/api`, plus `/api/mdm/apple/enroll` for automatic enrollment. Where hardware attestation is enabled, Fleet puts its own ACME directory URL into the enrollment profile, so add `/api/mdm/acme/*`. Where an installer is served to devices, that is `/api/mdm/apple/installer`.

**Setup-experience features each add their own:**

| Feature | What Fleet actually emits |
|---|---|
| Identity-provider authentication during setup | Three separate things, all needed: the browser starts at `/api/latest/fleet/mdm/sso`, the identity provider is given `/api/v1/fleet/mdm/sso/callback`, and the flow returns the user to the frontend route `/mdm/sso/callback`, which `/assets/*` serves |
| End user licence agreement | **`/api/latest/fleet/mdm/setup/eula/{token}`**, the deprecated form. The replacement `/api/*/fleet/setup_experience/eula/{token}` is registered and is not what this flow loads at the tag |
| Bootstrap package | **`/api/latest/fleet/mdm/bootstrap`**, also the deprecated form, hard-coded into the URL Fleet builds, **and used only when a CDN URL is not** (see above). Expose it either way |
| Fleet's Platform SSO extension | `/api/mdm/apple/psso/*` and `/.well-known/apple-app-site-association` |

**For any Apple device enrolled by link**, which is macOS as well as iOS and iPadOS, the chain is `/enroll`, then `/api/v1/fleet/enrollment_profiles/ota`, then **`/api/v1/fleet/ota_enrollment`**, which is where the profile the second one hands out sends the device next. The last two exist under the other prefixes and **Fleet emits `v1` at both transitions**. Omitting the third leaves an enrollment that starts and never completes. None of them is platform-specific: a reverse proxy that exposes them only for mobile will block a Mac enrolling from the **Add hosts** link ([3.2](../03-connect-devices/3.2-enroll-macos-devices.md), [3.5](../03-connect-devices/3.5-enroll-ios-and-ipados-devices.md)).

**For iOS and iPadOS specifically**, in-house app delivery adds **two** paths, and Fleet emits `latest` for both: `/api/latest/fleet/software/titles/*/in_house_app/{token}` and `/api/latest/fleet/software/titles/*/in_house_app/manifest/{token}`. A rule matching only the first serves the app and not the manifest that tells the device to install it. **The package path is the one a CDN URL can replace**; the manifest path never moves.

**Account-driven user enrollment** needs each of these, and they are separate registrations rather than one family:

| Path | For |
|---|---|
| `/mdm/apple/service_discovery/{token}` | The discovery document the device fetches first. A tokenless form is registered and deprecated |
| `/api/mdm/apple/account_driven_enroll/{token}` | The enrollment itself. A tokenless form is registered and deprecated |
| `/mdm/apple/account_driven_enroll/sso/{token}` | Its identity-provider hop. A tokenless form is registered and deprecated |
| The MDM SSO callback flow above | Shared with the setup-experience path, and needed here too |

**For Windows device management**, add the four Microsoft protocol paths under `/api/mdm/microsoft/`, which are `management`, `discovery`, `policy` and `enroll`, plus `/api/mdm/microsoft/tos` for automatic enrollment. [2.11](../02-administer-and-deploy-fleet/2.11-configure-windows-management.md) covers why exposing some but not all of these fails partway rather than cleanly.

**For Android**, add `/enroll`, `/api/v1/fleet/android_enterprise/enrollment_token`, and the enablement callback `/api/v1/fleet/android_enterprise/connect/{token}`. **Android's module declares `v1` alone**, so its routes exist at `v1` and `latest` and nowhere else, which is why the prefix set here is shorter than everywhere above, and **Fleet emits `v1` in both the enrollment page and the signup callback it generates**. The event callback `/api/v1/fleet/android_enterprise/pubsub` is a literal `v1` path, is how Google delivers device events, and is why [2.12](../02-administer-and-deploy-fleet/2.12-bind-android-enterprise.md) requires a publicly reachable server URL.

**For delivering your own certificates to devices**, rather than Fleet's, add `/mdm/scep/proxy/*`, which sits outside `/api`. Where fleetd fetches and reports on those certificates, add `/api/fleetd/certificates/*`.

**For the Google Calendar integration**, add `/api/v1/fleet/calendar/webhook/{event_uuid}`. The route is registered under all three prefixes and **the address Fleet supplies to Google is the `v1` one**, so that is the one Google will call.

**For Okta conditional access**, add `/api/fleet/conditional_access/scep`, `/api/fleet/conditional_access/idp/metadata` and `/api/fleet/conditional_access/idp/sso`. None of the three is versioned. **They do not all belong to the same origin**: Fleet builds the SSO URL against the conditional-access hostname, which is expected to be reached over mutual TLS, while metadata and SCEP sit on Fleet's ordinary origin. It is Premium, and requires the server private key.

## API conventions

![Reference](../_assets/icons/reference.svg) List endpoints share a convention: `page` for the zero-based page number, `per_page` for its size, `order_key` for the column to sort by, and `order_direction` for the direction.

```
GET /api/v1/fleet/activities?page=0&per_page=10&order_key=created_at&order_direction=desc
```

An endpoint's valid `order_key` values are its own, and Fleet's reference documents them per endpoint. [6.3](../06-automate-fleet/6.3-use-the-fleet-rest-api.md) covers paginating a large result set in practice.

## Where the rest lives

![Reference](../_assets/icons/reference.svg) Request bodies, response shapes, per-endpoint parameters and error codes are in Fleet's REST API reference at `fleetdm.com/docs/rest-api/rest-api`, and endpoints intended for contributors rather than administrators are documented separately in the Fleet repository.

Which actions each role may perform is [a.4](a.4-roles-and-permissions-matrix.md). Which surface can perform one at all is [a.5](a.5-interface-index.md), which carries every action against all four interfaces.

## Version notes

![Reference](../_assets/icons/reference.svg) Verified against Fleet 4.90.1. `v1` and `2022-04` are what the **core** module declares at this release; other modules declare their own, and `latest` is added to whatever set each declares.

**This appendix is not a complete inventory of everything Fleet serves.** Fleet embeds a catalogue of method-and-path entries which is sometimes mistaken for one, and it is not: **it is the allowlist consulted for API-only accounts that carry a non-empty endpoint restriction list**, and it constrains nobody else. **It also does not constrain every route those accounts can reach**: the check is wired into the API endpoint chains, and Fleet's debug tree is registered on the root with its own authentication, so a restricted account reaches those endpoints whether or not the list names them ([a.4](a.4-roles-and-permissions-matrix.md)). Its own validation runs in one direction, checking that every catalogue entry has a registered route, which establishes nothing about the reverse, and Fleet separately registers backward-compatible aliases the catalogue does not carry. An earlier draft of this appendix published its size as though it were a route count; the number is withheld here until it can be derived through Fleet's own loader rather than counted.

**The exposure matrix is the part most likely to change between releases**, because it grows as features are enabled and as features are added. Re-check it against Fleet's own guidance when adding a capability rather than assuming this list still covers it, and re-check it after an upgrade.
