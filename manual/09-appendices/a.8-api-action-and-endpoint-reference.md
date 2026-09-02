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
  - https://github.com/fleetdm/fleet/blob/fleet-v4.90.1/docs/REST%20API/rest-api.md
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

**For delivering your own certificates to devices**, rather than Fleet's, add `/mdm/scep/proxy/*`, which sits outside `/api`. Where fleetd fetches and reports on those certificates, add `/api/fleetd/certificates/*`. The integrations these deliver from are created and managed through the `/api/*/fleet/certificate_authorities` endpoints, which are the API behind [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md); the per-authority `request_certificate` route issues from an existing authority and is accepted only for Hydrant and custom EST authorities.

**For the Google Calendar integration**, add `/api/v1/fleet/calendar/webhook/{event_uuid}`. The route is registered under all three prefixes and **the address Fleet supplies to Google is the `v1` one**, so that is the one Google will call.

**For Okta conditional access**, add `/api/fleet/conditional_access/scep`, `/api/fleet/conditional_access/idp/metadata` and `/api/fleet/conditional_access/idp/sso`. None of the three is versioned. **They do not all belong to the same origin**: Fleet builds the SSO URL against the conditional-access hostname, which is expected to be reached over mutual TLS, while metadata and SCEP sit on Fleet's ordinary origin. It is Premium, and requires the server private key.

## API conventions

![Reference](../_assets/icons/reference.svg) List endpoints share a convention: `page` for the zero-based page number, `per_page` for its size, `order_key` for the column to sort by, and `order_direction` for the direction.

```
GET /api/v1/fleet/activities?page=0&per_page=10&order_key=created_at&order_direction=desc
```

An endpoint's valid `order_key` values are its own, and Fleet's reference documents them per endpoint. [6.3](../06-automate-fleet/6.3-use-the-fleet-rest-api.md) covers paginating a large result set in practice.

## Where the rest lives

![Reference](../_assets/icons/reference.svg) This appendix gives the method, path and authentication class for each action; it does not reproduce request bodies, response shapes, per-endpoint parameters or error codes. Fleet's own REST API reference at `fleetdm.com/docs/rest-api/rest-api` is the best available account of those, but it is hand-maintained and describes the current release rather than 4.90.1 specifically, so a mismatch against what you observe is a version question, not necessarily an error in either source; the version-pinned copy of that same reference, checked out at the tag this book verifies against, is linked under further reading. Endpoints intended for contributors rather than administrators are documented separately in the Fleet repository.

Which actions each role may perform is [a.4](a.4-roles-and-permissions-matrix.md). Which surface can perform one at all is [a.5](a.5-interface-index.md), which carries every action against all four interfaces.

## Version notes

![Reference](../_assets/icons/reference.svg) Verified against Fleet 4.90.1. `v1` and `2022-04` are what the **core** module declares at this release; other modules declare their own, and `latest` is added to whatever set each declares.

**The exposure matrix above is deliberately selective, not a complete inventory of everything Fleet serves.** The complete list of routes the server registers is the catalog at the end of this appendix. Fleet also embeds a catalogue of method-and-path entries which is sometimes mistaken for a route inventory, and it is not: **it is the allowlist consulted for API-only accounts that carry a non-empty endpoint restriction list**, and it constrains nobody else. **It also does not constrain every route those accounts can reach**: the check is wired into the API endpoint chains, and Fleet's debug tree is registered on the root with its own authentication, so a restricted account reaches those endpoints whether or not the list names them ([a.4](a.4-roles-and-permissions-matrix.md)). Its own validation runs in one direction, checking that every catalogue entry has a registered route, which establishes nothing about the reverse, and Fleet separately registers backward-compatible aliases the catalogue does not carry. The catalogue's size is withheld here rather than reported as though it were a route count, because deriving it honestly requires running it through Fleet's own loader rather than counting entries.

**The exposure matrix is the part most likely to change between releases**, because it grows as features are enabled and as features are added. Re-check it against Fleet's own guidance when adding a capability rather than assuming this list still covers it, and re-check it after an upgrade.

## The complete route catalog

![Reference](../_assets/icons/reference.svg) Like the configuration catalog in [a.3](a.3-configuration-model-and-precedence.md#the-complete-configuration-key-catalog), this table is generated rather than written. It is read directly from the route registrations the server makes as it builds its router, at the release this book is pinned to, so it lists what the server actually serves rather than what the REST reference documents. Where the two disagree, the catalog is the authority, for the same reason: it is the registration the running server performs.

It answers a different question from the exposure matrix above. The matrix says which paths a capability requires you to reach; this says which paths exist at all, and what each one asks a caller to present. The Auth column uses the same vocabulary as the caller model at the top of this appendix: a user token, a host, orbit or device key, or nothing where the route is reached before any credential exists. The device-management protocol paths are registered directly on the router and carry their own protocol authentication; they are grouped last.

Every route the server registers is listed, in three groups: the endpointer routes, the deprecated aliases still served, and the raw protocol routes. None is omitted. `_version_` stands for the API-version prefixes a route expands to, which [Version prefixes expand for some routes and not others](#version-prefixes-expand-for-some-routes-and-not-others) explains. Each route's handler and source location are kept in its HTML comment, not on the page.

<!-- To regenerate: python3 build/gen-api-catalog.py --out FILE  (FLEET_SRC overrides the source checkout). Pinned to fleet-v4.90.1 (dd0200f062). -->
<!-- GENERATED by build/gen-api-catalog.py; do not edit by hand.
     source: server/service/handler.go, server/mdm/android/service/handler.go, server/activity/internal/service/handler.go, server/mdm/acme/internal/service/handler.go, server/chart/internal/service/handler.go + handler_deprecated_paths.go @ dd0200f062c5982c46dd3bf8de81a6b5c0c5ce6d
     registrations found: 560; routes parsed: 560 (494 endpointer incl. alt paths, 58 deprecated aliases, 8 raw mux); unparsed: 0 -->

### API endpoints

| Method | Path | Auth |
|---|---|---|
| POST | `/api/_version_/fleet/trigger` | user (session or API token) <!-- server/service/handler.go:303; handler triggerEndpoint -->|
| GET | `/api/_version_/fleet/me` | user (session or API token) <!-- server/service/handler.go:305; handler meEndpoint -->|
| GET | `/api/_version_/fleet/sessions/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:306; handler getInfoAboutSessionEndpoint -->|
| DELETE | `/api/_version_/fleet/sessions/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:307; handler deleteSessionEndpoint -->|
| GET | `/api/_version_/fleet/config/certificate` | user (session or API token) <!-- server/service/handler.go:309; handler getCertificateEndpoint -->|
| GET | `/api/_version_/fleet/config` | user (session or API token) <!-- server/service/handler.go:310; handler getAppConfigEndpoint -->|
| PATCH | `/api/_version_/fleet/config` | user (session or API token) <!-- server/service/handler.go:311; handler modifyAppConfigEndpoint -->|
| PUT | `/api/_version_/fleet/logo` | user (session or API token) <!-- server/service/handler.go:312; handler putOrgLogoEndpoint -->|
| DELETE | `/api/_version_/fleet/logo` | user (session or API token) <!-- server/service/handler.go:313; handler deleteOrgLogoEndpoint -->|
| POST | `/api/_version_/fleet/spec/enroll_secret` | user (session or API token) <!-- server/service/handler.go:314; handler applyEnrollSecretSpecEndpoint -->|
| GET | `/api/_version_/fleet/spec/enroll_secret` | user (session or API token) <!-- server/service/handler.go:315; handler getEnrollSecretSpecEndpoint -->|
| GET | `/api/_version_/fleet/version` | user (session or API token) <!-- server/service/handler.go:316; handler versionEndpoint -->|
| POST | `/api/_version_/fleet/users/roles/spec` | user (session or API token) <!-- server/service/handler.go:318; handler applyUserRoleSpecsEndpoint -->|
| POST | `/api/_version_/fleet/translate` | user (session or API token) <!-- server/service/handler.go:319; handler translatorEndpoint -->|
| POST | `/api/_version_/fleet/spec/fleets` | user (session or API token) <!-- server/service/handler.go:320; handler applyTeamSpecsEndpoint -->|
| PATCH | `/api/_version_/fleet/fleets/{fleet_id:[0-9]+}/secrets` | user (session or API token) <!-- server/service/handler.go:321; handler modifyTeamEnrollSecretsEndpoint -->|
| POST | `/api/_version_/fleet/fleets` | user (session or API token) <!-- server/service/handler.go:322; handler createTeamEndpoint -->|
| GET | `/api/_version_/fleet/fleets` | user (session or API token) <!-- server/service/handler.go:323; handler listTeamsEndpoint -->|
| GET | `/api/_version_/fleet/fleets/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:324; handler getTeamEndpoint -->|
| PATCH | `/api/_version_/fleet/fleets/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:325; handler modifyTeamEndpoint -->|
| DELETE | `/api/_version_/fleet/fleets/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:326; handler deleteTeamEndpoint -->|
| POST | `/api/_version_/fleet/fleets/{id:[0-9]+}/agent_options` | user (session or API token) <!-- server/service/handler.go:327; handler modifyTeamAgentOptionsEndpoint -->|
| GET | `/api/_version_/fleet/fleets/{id:[0-9]+}/users` | user (session or API token) <!-- server/service/handler.go:328; handler listTeamUsersEndpoint -->|
| PATCH | `/api/_version_/fleet/fleets/{id:[0-9]+}/users` | user (session or API token) <!-- server/service/handler.go:329; handler addTeamUsersEndpoint -->|
| DELETE | `/api/_version_/fleet/fleets/{id:[0-9]+}/users` | user (session or API token) <!-- server/service/handler.go:330; handler deleteTeamUsersEndpoint -->|
| GET | `/api/_version_/fleet/fleets/{id:[0-9]+}/secrets` | user (session or API token) <!-- server/service/handler.go:331; handler teamEnrollSecretsEndpoint -->|
| GET | `/api/_version_/fleet/users` | user (session or API token) <!-- server/service/handler.go:333; handler listUsersEndpoint -->|
| POST | `/api/_version_/fleet/users/admin` | user (session or API token) <!-- server/service/handler.go:334; handler createUserEndpoint -->|
| POST | `/api/_version_/fleet/users/api_only` | user (session or API token) <!-- server/service/handler.go:335; handler createAPIOnlyUserEndpoint -->|
| PATCH | `/api/_version_/fleet/users/api_only/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:336; handler modifyAPIOnlyUserEndpoint -->|
| GET | `/api/_version_/fleet/users/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:337; handler getUserEndpoint -->|
| PATCH | `/api/_version_/fleet/users/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:338; handler modifyUserEndpoint -->|
| DELETE | `/api/_version_/fleet/users/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:339; handler deleteUserEndpoint -->|
| POST | `/api/_version_/fleet/users/{id:[0-9]+}/require_password_reset` | user (session or API token) <!-- server/service/handler.go:340; handler requirePasswordResetEndpoint -->|
| GET | `/api/_version_/fleet/users/{id:[0-9]+}/sessions` | user (session or API token) <!-- server/service/handler.go:341; handler getInfoAboutSessionsForUserEndpoint -->|
| DELETE | `/api/_version_/fleet/users/{id:[0-9]+}/sessions` | user (session or API token) <!-- server/service/handler.go:342; handler deleteSessionsForUserEndpoint -->|
| POST | `/api/_version_/fleet/change_password` | user (session or API token) <!-- server/service/handler.go:343; handler changePasswordEndpoint -->|
| GET | `/api/_version_/fleet/email/change/{token}` | user (session or API token) <!-- server/service/handler.go:345; handler changeEmailEndpoint -->|
| POST | `/api/_version_/fleet/targets` | user (session or API token) <!-- server/service/handler.go:347; handler searchTargetsEndpoint -->|
| POST | `/api/_version_/fleet/targets/count` | user (session or API token) <!-- server/service/handler.go:348; handler countTargetsEndpoint -->|
| POST | `/api/_version_/fleet/invites` | user (session or API token) <!-- server/service/handler.go:350; handler createInviteEndpoint -->|
| GET | `/api/_version_/fleet/invites` | user (session or API token) <!-- server/service/handler.go:351; handler listInvitesEndpoint -->|
| DELETE | `/api/_version_/fleet/invites/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:352; handler deleteInviteEndpoint -->|
| PATCH | `/api/_version_/fleet/invites/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:353; handler updateInviteEndpoint -->|
| POST | `/api/_version_/fleet/global/policies` | user (session or API token) <!-- server/service/handler.go:355; EndingAtVersion(v1); handler globalPolicyEndpoint -->|
| POST | `/api/_version_/fleet/policies` | user (session or API token) <!-- server/service/handler.go:356; StartingAtVersion(2022-04); handler globalPolicyEndpoint -->|
| GET | `/api/_version_/fleet/global/policies` | user (session or API token) <!-- server/service/handler.go:357; EndingAtVersion(v1); handler listGlobalPoliciesEndpoint -->|
| GET | `/api/_version_/fleet/policies` | user (session or API token) <!-- server/service/handler.go:358; StartingAtVersion(2022-04); handler listGlobalPoliciesEndpoint -->|
| GET | `/api/_version_/fleet/policies/count` | user (session or API token) <!-- server/service/handler.go:359; handler countGlobalPoliciesEndpoint -->|
| GET | `/api/_version_/fleet/global/policies/{policy_id}` | user (session or API token) <!-- server/service/handler.go:360; EndingAtVersion(v1); handler getPolicyByIDEndpoint -->|
| GET | `/api/_version_/fleet/policies/{policy_id}` | user (session or API token) <!-- server/service/handler.go:361; StartingAtVersion(2022-04); handler getPolicyByIDEndpoint -->|
| GET | `/api/_version_/fleet/policies/{policy_id}/automation_activities` | user (session or API token) <!-- server/service/handler.go:362; StartingAtVersion(2022-04); handler listPolicyAutomationActivitiesEndpoint -->|
| POST | `/api/_version_/fleet/global/policies/delete` | user (session or API token) <!-- server/service/handler.go:363; EndingAtVersion(v1); handler deleteGlobalPoliciesEndpoint -->|
| POST | `/api/_version_/fleet/policies/delete` | user (session or API token) <!-- server/service/handler.go:364; StartingAtVersion(2022-04); handler deleteGlobalPoliciesEndpoint -->|
| PATCH | `/api/_version_/fleet/global/policies/{policy_id}` | user (session or API token) <!-- server/service/handler.go:365; EndingAtVersion(v1); handler modifyGlobalPolicyEndpoint -->|
| PATCH | `/api/_version_/fleet/policies/{policy_id}` | user (session or API token) <!-- server/service/handler.go:366; StartingAtVersion(2022-04); handler modifyGlobalPolicyEndpoint -->|
| POST | `/api/_version_/fleet/policies/{policy_id}/reset` | user (session or API token) <!-- server/service/handler.go:367; StartingAtVersion(2022-04); handler resetPolicyEndpoint -->|
| POST | `/api/_version_/fleet/automations/reset` | user (session or API token) <!-- server/service/handler.go:368; handler resetAutomationEndpoint -->|
| POST | `/api/_version_/fleet/fleets/{fleet_id}/policies` | user (session or API token) <!-- server/service/handler.go:370; handler teamPolicyEndpoint -->|
| GET | `/api/_version_/fleet/fleets/{fleet_id}/policies` | user (session or API token) <!-- server/service/handler.go:371; handler listTeamPoliciesEndpoint -->|
| GET | `/api/_version_/fleet/fleets/{fleet_id}/policies/count` | user (session or API token) <!-- server/service/handler.go:372; handler countTeamPoliciesEndpoint -->|
| GET | `/api/_version_/fleet/fleets/{fleet_id}/policies/{policy_id}` | user (session or API token) <!-- server/service/handler.go:373; handler getTeamPolicyByIDEndpoint -->|
| POST | `/api/_version_/fleet/fleets/{fleet_id}/policies/delete` | user (session or API token) <!-- server/service/handler.go:374; handler deleteTeamPoliciesEndpoint -->|
| PATCH | `/api/_version_/fleet/fleets/{fleet_id}/policies/{policy_id}` | user (session or API token) <!-- server/service/handler.go:375; handler modifyTeamPolicyEndpoint -->|
| POST | `/api/_version_/fleet/spec/policies` | user (session or API token) <!-- server/service/handler.go:376; handler applyPolicySpecsEndpoint -->|
| POST | `/api/_version_/fleet/certificates` | user (session or API token) <!-- server/service/handler.go:378; handler createCertificateTemplateEndpoint -->|
| GET | `/api/_version_/fleet/certificates` | user (session or API token) <!-- server/service/handler.go:379; handler listCertificateTemplatesEndpoint -->|
| GET | `/api/_version_/fleet/certificates/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:380; handler getCertificateTemplateEndpoint -->|
| DELETE | `/api/_version_/fleet/certificates/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:381; handler deleteCertificateTemplateEndpoint -->|
| POST | `/api/_version_/fleet/spec/certificates` | user (session or API token) <!-- server/service/handler.go:382; handler applyCertificateTemplateSpecsEndpoint -->|
| DELETE | `/api/_version_/fleet/spec/certificates` | user (session or API token) <!-- server/service/handler.go:383; handler deleteCertificateTemplateSpecsEndpoint -->|
| GET | `/api/_version_/fleet/reports/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:385; handler getQueryEndpoint -->|
| GET | `/api/_version_/fleet/reports` | user (session or API token) <!-- server/service/handler.go:386; handler listQueriesEndpoint -->|
| GET | `/api/_version_/fleet/reports/{id:[0-9]+}/report` | user (session or API token) <!-- server/service/handler.go:387; handler getQueryReportEndpoint -->|
| POST | `/api/_version_/fleet/reports` | user (session or API token) <!-- server/service/handler.go:388; handler createQueryEndpoint -->|
| PATCH | `/api/_version_/fleet/reports/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:389; handler modifyQueryEndpoint -->|
| DELETE | `/api/_version_/fleet/reports/{name}` | user (session or API token) <!-- server/service/handler.go:390; handler deleteQueryEndpoint -->|
| DELETE | `/api/_version_/fleet/reports/id/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:391; handler deleteQueryByIDEndpoint -->|
| POST | `/api/_version_/fleet/reports/delete` | user (session or API token) <!-- server/service/handler.go:392; handler deleteQueriesEndpoint -->|
| POST | `/api/_version_/fleet/spec/reports` | user (session or API token) <!-- server/service/handler.go:393; handler applyQuerySpecsEndpoint -->|
| GET | `/api/_version_/fleet/spec/reports` | user (session or API token) <!-- server/service/handler.go:394; handler getQuerySpecsEndpoint -->|
| GET | `/api/_version_/fleet/spec/reports/{name}` | user (session or API token) <!-- server/service/handler.go:395; handler getQuerySpecEndpoint -->|
| GET | `/api/_version_/fleet/packs/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:397; handler getPackEndpoint -->|
| POST | `/api/_version_/fleet/packs` | user (session or API token) <!-- server/service/handler.go:398; handler createPackEndpoint -->|
| PATCH | `/api/_version_/fleet/packs/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:399; handler modifyPackEndpoint -->|
| GET | `/api/_version_/fleet/packs` | user (session or API token) <!-- server/service/handler.go:400; handler listPacksEndpoint -->|
| DELETE | `/api/_version_/fleet/packs/{name}` | user (session or API token) <!-- server/service/handler.go:401; handler deletePackEndpoint -->|
| DELETE | `/api/_version_/fleet/packs/id/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:402; handler deletePackByIDEndpoint -->|
| POST | `/api/_version_/fleet/spec/packs` | user (session or API token) <!-- server/service/handler.go:403; handler applyPackSpecsEndpoint -->|
| GET | `/api/_version_/fleet/spec/packs` | user (session or API token) <!-- server/service/handler.go:404; handler getPackSpecsEndpoint -->|
| GET | `/api/_version_/fleet/spec/packs/{name}` | user (session or API token) <!-- server/service/handler.go:405; handler getPackSpecEndpoint -->|
| GET | `/api/_version_/fleet/software/versions` | user (session or API token) <!-- server/service/handler.go:407; handler listSoftwareVersionsEndpoint -->|
| GET | `/api/_version_/fleet/software/versions/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:408; handler getSoftwareEndpoint -->|
| GET | `/api/_version_/fleet/software` | user (session or API token) <!-- server/service/handler.go:411; handler listSoftwareEndpoint -->|
| GET | `/api/_version_/fleet/software/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:413; handler getSoftwareEndpoint -->|
| GET | `/api/_version_/fleet/software/count` | user (session or API token) <!-- server/service/handler.go:415; handler countSoftwareEndpoint -->|
| GET | `/api/_version_/fleet/software/titles` | user (session or API token) <!-- server/service/handler.go:417; handler listSoftwareTitlesEndpoint -->|
| GET | `/api/_version_/fleet/software/titles/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:418; handler getSoftwareTitleEndpoint -->|
| POST | `/api/_version_/fleet/hosts/{host_id:[0-9]+}/software/{software_title_id:[0-9]+}/install` | user (session or API token) <!-- server/service/handler.go:419; handler installSoftwareTitleEndpoint -->|
| POST | `/api/_version_/fleet/hosts/{host_id:[0-9]+}/software/{software_title_id:[0-9]+}/uninstall` | user (session or API token) <!-- server/service/handler.go:421; handler uninstallSoftwareTitleEndpoint -->|
| GET | `/api/_version_/fleet/software/titles/{title_id:[0-9]+}/package` | user (session or API token) <!-- server/service/handler.go:425; handler getSoftwareInstallerEndpoint -->|
| POST | `/api/_version_/fleet/software/titles/{title_id:[0-9]+}/package/token` | user (session or API token) <!-- server/service/handler.go:426; handler getSoftwareInstallerTokenEndpoint -->|
| POST | `/api/_version_/fleet/software/package` | user (session or API token) <!-- server/service/handler.go:429; handler uploadSoftwareInstallerEndpoint -->|
| PATCH | `/api/_version_/fleet/software/titles/{id:[0-9]+}/name` | user (session or API token) <!-- server/service/handler.go:430; handler updateSoftwareNameEndpoint -->|
| PATCH | `/api/_version_/fleet/software/titles/{id:[0-9]+}/package` | user (session or API token) <!-- server/service/handler.go:432; handler updateSoftwareInstallerEndpoint -->|
| DELETE | `/api/_version_/fleet/software/titles/{title_id:[0-9]+}/available_for_install` | user (session or API token) <!-- server/service/handler.go:433; handler deleteSoftwareInstallerEndpoint -->|
| GET | `/api/_version_/fleet/software/install/{install_uuid}/results` | user (session or API token) <!-- server/service/handler.go:434; handler getSoftwareInstallResultsEndpoint -->|
| POST | `/api/_version_/fleet/software/batch` | user (session or API token) <!-- server/service/handler.go:438; handler batchSetSoftwareInstallersEndpoint -->|
| GET | `/api/_version_/fleet/software/batch/{request_uuid}` | user (session or API token) <!-- server/service/handler.go:439; handler batchSetSoftwareInstallersResultEndpoint -->|
| GET | `/api/_version_/fleet/software/titles/{title_id:[0-9]+}/icon` | user (session or API token) <!-- server/service/handler.go:442; handler getSoftwareTitleIconsEndpoint -->|
| PUT | `/api/_version_/fleet/software/titles/{title_id:[0-9]+}/icon` | user (session or API token) <!-- server/service/handler.go:443; handler putSoftwareTitleIconEndpoint -->|
| DELETE | `/api/_version_/fleet/software/titles/{title_id:[0-9]+}/icon` | user (session or API token) <!-- server/service/handler.go:444; handler deleteSoftwareTitleIconEndpoint -->|
| GET | `/api/_version_/fleet/software/app_store_apps` | user (session or API token) <!-- server/service/handler.go:447; handler getAppStoreAppsEndpoint -->|
| POST | `/api/_version_/fleet/software/app_store_apps` | user (session or API token) <!-- server/service/handler.go:448; handler addAppStoreAppEndpoint -->|
| PATCH | `/api/_version_/fleet/software/titles/{title_id:[0-9]+}/app_store_app` | user (session or API token) <!-- server/service/handler.go:449; handler updateAppStoreAppEndpoint -->|
| GET | `/api/_version_/fleet/software/self_service_categories` | user (session or API token) <!-- server/service/handler.go:452; handler getSelfServiceCategoriesEndpoint -->|
| POST | `/api/_version_/fleet/software/self_service_categories` | user (session or API token) <!-- server/service/handler.go:453; handler addSelfServiceCategoriesEndpoint -->|
| PATCH | `/api/_version_/fleet/software/self_service_categories/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:454; handler patchSelfServiceCategoriesEndpoint -->|
| DELETE | `/api/_version_/fleet/software/self_service_categories/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:455; handler deleteSelfServiceCategoriesEndpoint -->|
| PUT | `/api/_version_/fleet/setup_experience/software` | user (session or API token) <!-- server/service/handler.go:460; handler putSetupExperienceSoftware -->|
| GET | `/api/_version_/fleet/setup_experience/software` | user (session or API token) <!-- server/service/handler.go:461; handler getSetupExperienceSoftware -->|
| GET | `/api/_version_/fleet/setup_experience/script` | user (session or API token) <!-- server/service/handler.go:464; handler getSetupExperienceScriptEndpoint -->|
| POST | `/api/_version_/fleet/setup_experience/script` | user (session or API token) <!-- server/service/handler.go:465; handler setSetupExperienceScriptEndpoint -->|
| DELETE | `/api/_version_/fleet/setup_experience/script` | user (session or API token) <!-- server/service/handler.go:466; handler deleteSetupExperienceScriptEndpoint -->|
| POST | `/api/_version_/fleet/software/fleet_maintained_apps` | user (session or API token) <!-- server/service/handler.go:469; handler addFleetMaintainedAppEndpoint -->|
| GET | `/api/_version_/fleet/software/fleet_maintained_apps` | user (session or API token) <!-- server/service/handler.go:470; handler listFleetMaintainedAppsEndpoint -->|
| GET | `/api/_version_/fleet/software/fleet_maintained_apps/{app_id}` | user (session or API token) <!-- server/service/handler.go:471; handler getFleetMaintainedApp -->|
| GET | `/api/_version_/fleet/vulnerabilities` | user (session or API token) <!-- server/service/handler.go:474; handler listVulnerabilitiesEndpoint -->|
| GET | `/api/_version_/fleet/vulnerabilities/{cve}` | user (session or API token) <!-- server/service/handler.go:475; handler getVulnerabilityEndpoint -->|
| GET | `/api/_version_/fleet/host_summary` | user (session or API token) <!-- server/service/handler.go:478; handler getHostSummaryEndpoint -->|
| GET | `/api/_version_/fleet/hosts` | user (session or API token) <!-- server/service/handler.go:479; handler listHostsEndpoint -->|
| POST | `/api/_version_/fleet/hosts/delete` | user (session or API token) <!-- server/service/handler.go:480; handler deleteHostsEndpoint -->|
| GET | `/api/_version_/fleet/hosts/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:481; handler getHostEndpoint -->|
| GET | `/api/_version_/fleet/hosts/count` | user (session or API token) <!-- server/service/handler.go:482; handler countHostsEndpoint -->|
| POST | `/api/_version_/fleet/hosts/search` | user (session or API token) <!-- server/service/handler.go:483; handler searchHostsEndpoint -->|
| GET | `/api/_version_/fleet/hosts/identifier/{identifier}` | user (session or API token) <!-- server/service/handler.go:484; handler hostByIdentifierEndpoint -->|
| POST | `/api/_version_/fleet/hosts/identifier/{identifier}/query` | user (session or API token) <!-- server/service/handler.go:485; handler runLiveQueryOnHostEndpoint -->|
| POST | `/api/_version_/fleet/hosts/{id:[0-9]+}/query` | user (session or API token) <!-- server/service/handler.go:486; handler runLiveQueryOnHostByIDEndpoint -->|
| DELETE | `/api/_version_/fleet/hosts/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:487; handler deleteHostEndpoint -->|
| POST | `/api/_version_/fleet/hosts/transfer` | user (session or API token) <!-- server/service/handler.go:488; handler addHostsToTeamEndpoint -->|
| POST | `/api/_version_/fleet/hosts/transfer/filter` | user (session or API token) <!-- server/service/handler.go:489; handler addHostsToTeamByFilterEndpoint -->|
| POST | `/api/_version_/fleet/hosts/{id:[0-9]+}/refetch` | user (session or API token) <!-- server/service/handler.go:490; handler refetchHostEndpoint -->|
| GET | `/api/_version_/fleet/hosts/{id:[0-9]+}/device_mapping` | user (session or API token) <!-- server/service/handler.go:492; handler listHostDeviceMappingEndpoint -->|
| PUT | `/api/_version_/fleet/hosts/{id:[0-9]+}/device_mapping` | user (session or API token) <!-- server/service/handler.go:493; handler putHostDeviceMappingEndpoint -->|
| DELETE | `/api/_version_/fleet/hosts/{id:[0-9]+}/device_mapping/idp` | user (session or API token) <!-- server/service/handler.go:494; handler deleteHostIDPEndpoint -->|
| GET | `/api/_version_/fleet/hosts/report` | user (session or API token) <!-- server/service/handler.go:495; handler hostsReportEndpoint -->|
| GET | `/api/_version_/fleet/os_versions` | user (session or API token) <!-- server/service/handler.go:496; handler osVersionsEndpoint -->|
| GET | `/api/_version_/fleet/os_versions/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:497; handler getOSVersionEndpoint -->|
| GET | `/api/_version_/fleet/hosts/{id:[0-9]+}/reports/{report_id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:498; handler getHostQueryReportEndpoint -->|
| GET | `/api/_version_/fleet/hosts/{id:[0-9]+}/reports` | user (session or API token) <!-- server/service/handler.go:499; handler listHostReportsEndpoint -->|
| GET | `/api/_version_/fleet/hosts/{id:[0-9]+}/queries` | user (session or API token) <!-- server/service/handler.go:499; alt path of /api/_version_/fleet/hosts/{id:[0-9]+}/reports; handler listHostReportsEndpoint -->|
| GET | `/api/_version_/fleet/hosts/{id:[0-9]+}/health` | user (session or API token) <!-- server/service/handler.go:500; handler getHostHealthEndpoint -->|
| POST | `/api/_version_/fleet/hosts/{id:[0-9]+}/labels` | user (session or API token) <!-- server/service/handler.go:501; handler addLabelsToHostEndpoint -->|
| DELETE | `/api/_version_/fleet/hosts/{id:[0-9]+}/labels` | user (session or API token) <!-- server/service/handler.go:502; handler removeLabelsFromHostEndpoint -->|
| GET | `/api/_version_/fleet/hosts/{id:[0-9]+}/software` | user (session or API token) <!-- server/service/handler.go:503; handler getHostSoftwareEndpoint -->|
| GET | `/api/_version_/fleet/hosts/{id:[0-9]+}/certificates` | user (session or API token) <!-- server/service/handler.go:504; handler listHostCertificatesEndpoint -->|
| POST | `/api/_version_/fleet/hosts/{id:[0-9]+}/certificates/{template_id:[0-9]+}/resend` | user (session or API token) <!-- server/service/handler.go:505; handler resendHostCertificateTemplateEndpoint -->|
| GET | `/api/_version_/fleet/hosts/{id:[0-9]+}/recovery_lock_password` | user (session or API token) <!-- server/service/handler.go:506; handler getHostRecoveryLockPasswordEndpoint -->|
| GET | `/api/_version_/fleet/hosts/{id:[0-9]+}/device_url` | user (session or API token) <!-- server/service/handler.go:507; handler getHostDeviceURLEndpoint -->|
| GET | `/api/_version_/fleet/hosts/summary/mdm` | user (session or API token) <!-- server/service/handler.go:509; handler getHostMDMSummary -->|
| GET | `/api/_version_/fleet/hosts/{id:[0-9]+}/mdm` | user (session or API token) <!-- server/service/handler.go:510; handler getHostMDM -->|
| GET | `/api/_version_/fleet/hosts/{id:[0-9]+}/dep_assignment` | user (session or API token) <!-- server/service/handler.go:512; handler getHostDEPAssignmentEndpoint -->|
| POST | `/api/_version_/fleet/labels` | user (session or API token) <!-- server/service/handler.go:514; handler createLabelEndpoint -->|
| PATCH | `/api/_version_/fleet/labels/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:515; handler modifyLabelEndpoint -->|
| GET | `/api/_version_/fleet/labels/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:516; handler getLabelEndpoint -->|
| GET | `/api/_version_/fleet/labels` | user (session or API token) <!-- server/service/handler.go:517; handler listLabelsEndpoint -->|
| GET | `/api/_version_/fleet/labels/summary` | user (session or API token) <!-- server/service/handler.go:518; handler getLabelsSummaryEndpoint -->|
| GET | `/api/_version_/fleet/labels/{id:[0-9]+}/hosts` | user (session or API token) <!-- server/service/handler.go:519; handler listHostsInLabelEndpoint -->|
| DELETE | `/api/_version_/fleet/labels/{name}` | user (session or API token) <!-- server/service/handler.go:520; handler deleteLabelEndpoint -->|
| DELETE | `/api/_version_/fleet/labels/id/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:521; handler deleteLabelByIDEndpoint -->|
| POST | `/api/_version_/fleet/spec/labels` | user (session or API token) <!-- server/service/handler.go:522; handler applyLabelSpecsEndpoint -->|
| GET | `/api/_version_/fleet/spec/labels` | user (session or API token) <!-- server/service/handler.go:523; handler getLabelSpecsEndpoint -->|
| GET | `/api/_version_/fleet/spec/labels/{name}` | user (session or API token) <!-- server/service/handler.go:524; handler getLabelSpecEndpoint -->|
| POST | `/api/_version_/fleet/reports/{id:[0-9]+}/run` | user (session or API token) <!-- server/service/handler.go:527; handler runOneLiveQueryEndpoint -->|
| GET | `/api/_version_/fleet/reports/run` | user (session or API token) <!-- server/service/handler.go:529; handler runLiveQueryEndpoint -->|
| POST | `/api/_version_/fleet/reports/run` | user (session or API token) <!-- server/service/handler.go:533; handler createDistributedQueryCampaignEndpoint -->|
| POST | `/api/_version_/fleet/reports/run_by_identifiers` | user (session or API token) <!-- server/service/handler.go:534; handler createDistributedQueryCampaignByIdentifierEndpoint -->|
| POST | `/api/_version_/fleet/reports/run_by_names` | user (session or API token) <!-- server/service/handler.go:536; handler createDistributedQueryCampaignByIdentifierEndpoint -->|
| GET | `/api/_version_/fleet/packs/{id:[0-9]+}/scheduled` | user (session or API token) <!-- server/service/handler.go:538; handler getScheduledQueriesInPackEndpoint -->|
| POST | `/api/_version_/fleet/schedule` | user (session or API token) <!-- server/service/handler.go:539; EndingAtVersion(v1); handler scheduleQueryEndpoint -->|
| POST | `/api/_version_/fleet/packs/schedule` | user (session or API token) <!-- server/service/handler.go:540; StartingAtVersion(2022-04); handler scheduleQueryEndpoint -->|
| GET | `/api/_version_/fleet/schedule/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:541; handler getScheduledQueryEndpoint -->|
| PATCH | `/api/_version_/fleet/schedule/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:542; EndingAtVersion(v1); handler modifyScheduledQueryEndpoint -->|
| PATCH | `/api/_version_/fleet/packs/schedule/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:543; StartingAtVersion(2022-04); handler modifyScheduledQueryEndpoint -->|
| DELETE | `/api/_version_/fleet/schedule/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:544; EndingAtVersion(v1); handler deleteScheduledQueryEndpoint -->|
| DELETE | `/api/_version_/fleet/packs/schedule/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:545; StartingAtVersion(2022-04); handler deleteScheduledQueryEndpoint -->|
| GET | `/api/_version_/fleet/global/schedule` | user (session or API token) <!-- server/service/handler.go:547; EndingAtVersion(v1); handler getGlobalScheduleEndpoint -->|
| GET | `/api/_version_/fleet/schedule` | user (session or API token) <!-- server/service/handler.go:548; StartingAtVersion(2022-04); handler getGlobalScheduleEndpoint -->|
| POST | `/api/_version_/fleet/global/schedule` | user (session or API token) <!-- server/service/handler.go:549; EndingAtVersion(v1); handler globalScheduleQueryEndpoint -->|
| POST | `/api/_version_/fleet/schedule` | user (session or API token) <!-- server/service/handler.go:550; StartingAtVersion(2022-04); handler globalScheduleQueryEndpoint -->|
| PATCH | `/api/_version_/fleet/global/schedule/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:551; EndingAtVersion(v1); handler modifyGlobalScheduleEndpoint -->|
| PATCH | `/api/_version_/fleet/schedule/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:552; StartingAtVersion(2022-04); handler modifyGlobalScheduleEndpoint -->|
| DELETE | `/api/_version_/fleet/global/schedule/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:553; EndingAtVersion(v1); handler deleteGlobalScheduleEndpoint -->|
| DELETE | `/api/_version_/fleet/schedule/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:554; StartingAtVersion(2022-04); handler deleteGlobalScheduleEndpoint -->|
| GET | `/api/_version_/fleet/fleets/{fleet_id}/schedule` | user (session or API token) <!-- server/service/handler.go:556; handler getTeamScheduleEndpoint -->|
| POST | `/api/_version_/fleet/fleets/{fleet_id}/schedule` | user (session or API token) <!-- server/service/handler.go:557; handler teamScheduleQueryEndpoint -->|
| PATCH | `/api/_version_/fleet/fleets/{fleet_id}/schedule/{report_id}` | user (session or API token) <!-- server/service/handler.go:558; handler modifyTeamScheduleEndpoint -->|
| DELETE | `/api/_version_/fleet/fleets/{fleet_id}/schedule/{report_id}` | user (session or API token) <!-- server/service/handler.go:559; handler deleteTeamScheduleEndpoint -->|
| GET | `/api/_version_/fleet/carves` | user (session or API token) <!-- server/service/handler.go:561; handler listCarvesEndpoint -->|
| GET | `/api/_version_/fleet/carves/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:562; handler getCarveEndpoint -->|
| GET | `/api/_version_/fleet/carves/{id:[0-9]+}/block/{block_id}` | user (session or API token) <!-- server/service/handler.go:563; handler getCarveBlockEndpoint -->|
| GET | `/api/_version_/fleet/hosts/{id:[0-9]+}/macadmins` | user (session or API token) <!-- server/service/handler.go:565; handler getMacadminsDataEndpoint -->|
| GET | `/api/_version_/fleet/macadmins` | user (session or API token) <!-- server/service/handler.go:566; handler getAggregatedMacadminsDataEndpoint -->|
| GET | `/api/_version_/fleet/status/result_store` | user (session or API token) <!-- server/service/handler.go:568; handler statusResultStoreEndpoint -->|
| GET | `/api/_version_/fleet/status/live_query` | user (session or API token) <!-- server/service/handler.go:569; handler statusLiveQueryEndpoint -->|
| POST | `/api/_version_/fleet/scripts/run` | user (session or API token) <!-- server/service/handler.go:571; handler runScriptEndpoint -->|
| POST | `/api/_version_/fleet/scripts/run/sync` | user (session or API token) <!-- server/service/handler.go:572; handler runScriptSyncEndpoint -->|
| POST | `/api/_version_/fleet/scripts/run/batch` | user (session or API token) <!-- server/service/handler.go:573; handler batchScriptRunEndpoint -->|
| GET | `/api/_version_/fleet/scripts/results/{execution_id}` | user (session or API token) <!-- server/service/handler.go:574; handler getScriptResultEndpoint -->|
| POST | `/api/_version_/fleet/scripts` | user (session or API token) <!-- server/service/handler.go:575; handler createScriptEndpoint -->|
| GET | `/api/_version_/fleet/scripts` | user (session or API token) <!-- server/service/handler.go:576; handler listScriptsEndpoint -->|
| GET | `/api/_version_/fleet/scripts/{script_id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:577; handler getScriptEndpoint -->|
| PATCH | `/api/_version_/fleet/scripts/{script_id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:578; handler updateScriptEndpoint -->|
| DELETE | `/api/_version_/fleet/scripts/{script_id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:579; handler deleteScriptEndpoint -->|
| POST | `/api/_version_/fleet/scripts/batch` | user (session or API token) <!-- server/service/handler.go:580; handler batchSetScriptsEndpoint -->|
| POST | `/api/_version_/fleet/scripts/batch/{batch_execution_id:[a-zA-Z0-9-]+}/cancel` | user (session or API token) <!-- server/service/handler.go:581; handler batchScriptCancelEndpoint -->|
| GET | `/api/_version_/fleet/scripts/batch/summary/{batch_execution_id:[a-zA-Z0-9-]+}` | user (session or API token) <!-- server/service/handler.go:583; handler batchScriptExecutionSummaryEndpoint -->|
| GET | `/api/_version_/fleet/scripts/batch/{batch_execution_id:[a-zA-Z0-9-]+}/host_results` | user (session or API token) <!-- server/service/handler.go:585; handler batchScriptExecutionHostResultsEndpoint -->|
| GET | `/api/_version_/fleet/scripts/batch/{batch_execution_id:[a-zA-Z0-9-]+}/host-results` | user (session or API token) <!-- server/service/handler.go:585; alt path of /api/_version_/fleet/scripts/batch/{batch_execution_id:[a-zA-Z0-9-]+}/host_results; handler batchScriptExecutionHostResultsEndpoint -->|
| GET | `/api/_version_/fleet/scripts/batch/{batch_execution_id:[a-zA-Z0-9-]+}` | user (session or API token) <!-- server/service/handler.go:586; handler batchScriptExecutionStatusEndpoint -->|
| GET | `/api/_version_/fleet/scripts/batch` | user (session or API token) <!-- server/service/handler.go:587; handler batchScriptExecutionListEndpoint -->|
| GET | `/api/_version_/fleet/hosts/{id:[0-9]+}/scripts` | user (session or API token) <!-- server/service/handler.go:589; handler getHostScriptDetailsEndpoint -->|
| GET | `/api/_version_/fleet/hosts/{id:[0-9]+}/activities/upcoming` | user (session or API token) <!-- server/service/handler.go:590; handler listHostUpcomingActivitiesEndpoint -->|
| DELETE | `/api/_version_/fleet/hosts/{id:[0-9]+}/activities/upcoming/{activity_id}` | user (session or API token) <!-- server/service/handler.go:591; handler cancelHostUpcomingActivityEndpoint -->|
| POST | `/api/_version_/fleet/hosts/{id:[0-9]+}/lock` | user (session or API token) <!-- server/service/handler.go:592; handler lockHostEndpoint -->|
| POST | `/api/_version_/fleet/hosts/{id:[0-9]+}/unlock` | user (session or API token) <!-- server/service/handler.go:593; handler unlockHostEndpoint -->|
| POST | `/api/_version_/fleet/hosts/{id:[0-9]+}/wipe` | user (session or API token) <!-- server/service/handler.go:594; handler wipeHostEndpoint -->|
| POST | `/api/_version_/fleet/hosts/{id:[0-9]+}/clear_passcode` | user (session or API token) <!-- server/service/handler.go:595; handler clearPasscodeEndpoint -->|
| POST | `/api/_version_/fleet/hosts/{id:[0-9]+}/recovery_lock_password/rotate` | user (session or API token) <!-- server/service/handler.go:596; handler rotateRecoveryLockPasswordEndpoint -->|
| GET | `/api/_version_/fleet/hosts/{id:[0-9]+}/managed_account_password` | user (session or API token) <!-- server/service/handler.go:597; handler getHostManagedAccountPasswordEndpoint -->|
| POST | `/api/_version_/fleet/hosts/{id:[0-9]+}/managed_account_password/rotate` | user (session or API token) <!-- server/service/handler.go:598; handler rotateManagedLocalAccountPasswordEndpoint -->|
| POST | `/api/_version_/fleet/autofill/policy` | user (session or API token) <!-- server/service/handler.go:601; handler autofillPoliciesEndpoint -->|
| PUT | `/api/_version_/fleet/spec/secret_variables` | user (session or API token) <!-- server/service/handler.go:604; handler createSecretVariablesEndpoint -->|
| POST | `/api/_version_/fleet/custom_variables` | user (session or API token) <!-- server/service/handler.go:605; handler createSecretVariableEndpoint -->|
| GET | `/api/_version_/fleet/custom_variables` | user (session or API token) <!-- server/service/handler.go:606; handler listSecretVariablesEndpoint -->|
| DELETE | `/api/_version_/fleet/custom_variables/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:607; handler deleteSecretVariableEndpoint -->|
| GET | `/api/_version_/fleet/custom_host_vitals` | user (session or API token) <!-- server/service/handler.go:610; handler listCustomHostVitalsEndpoint -->|
| POST | `/api/_version_/fleet/custom_host_vitals` | user (session or API token) <!-- server/service/handler.go:611; handler createCustomHostVitalEndpoint -->|
| PATCH | `/api/_version_/fleet/custom_host_vitals/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:612; handler updateCustomHostVitalEndpoint -->|
| DELETE | `/api/_version_/fleet/custom_host_vitals/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:613; handler deleteCustomHostVitalEndpoint -->|
| PUT | `/api/_version_/fleet/hosts/{host_id:[0-9]+}/custom_host_vitals/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:614; handler setHostCustomHostVitalValueEndpoint -->|
| PUT | `/api/_version_/fleet/spec/custom_host_vitals` | user (session or API token) <!-- server/service/handler.go:615; handler upsertCustomHostVitalsEndpoint -->|
| GET | `/api/_version_/fleet/rest_api` | user (session or API token) <!-- server/service/handler.go:618; handler listAPIEndpointsEndpoint -->|
| GET | `/api/_version_/fleet/scim/details` | user (session or API token) <!-- server/service/handler.go:621; handler getScimDetailsEndpoint -->|
| POST | `/api/_version_/fleet/conditional-access/microsoft` | user (session or API token) <!-- server/service/handler.go:624; handler conditionalAccessMicrosoftCreateEndpoint -->|
| POST | `/api/_version_/fleet/conditional-access/microsoft/confirm` | user (session or API token) <!-- server/service/handler.go:625; handler conditionalAccessMicrosoftConfirmEndpoint -->|
| DELETE | `/api/_version_/fleet/conditional-access/microsoft` | user (session or API token) <!-- server/service/handler.go:626; handler conditionalAccessMicrosoftDeleteEndpoint -->|
| GET | `/api/_version_/fleet/conditional_access/idp/signing_cert` | user (session or API token) <!-- server/service/handler.go:629; handler conditionalAccessGetIdPSigningCertEndpoint -->|
| GET | `/api/_version_/fleet/conditional_access/idp/apple/profile` | user (session or API token) <!-- server/service/handler.go:630; handler conditionalAccessGetIdPAppleProfileEndpoint -->|
| PATCH | `/api/_version_/fleet/mdm/apple/setup` | user (session or API token) <!-- server/service/handler.go:634; handler updateMDMAppleSetupEndpoint -->|
| PATCH | `/api/_version_/fleet/setup_experience` | user (session or API token) <!-- server/service/handler.go:635; handler updateMDMAppleSetupEndpoint -->|
| POST | `/api/_version_/fleet/mdm/apple/enqueue` | user (session or API token) <!-- server/service/handler.go:649; handler enqueueMDMAppleCommandEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/commandresults` | user (session or API token) <!-- server/service/handler.go:653; handler getMDMAppleCommandResultsEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/commands` | user (session or API token) <!-- server/service/handler.go:657; handler listMDMAppleCommandsEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/profiles/{profile_id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:661; handler getMDMAppleConfigProfileEndpoint -->|
| DELETE | `/api/_version_/fleet/mdm/apple/profiles/{profile_id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:662; handler deleteMDMAppleConfigProfileEndpoint -->|
| POST | `/api/_version_/fleet/mdm/apple/profiles` | user (session or API token) <!-- server/service/handler.go:663; handler newMDMAppleConfigProfileEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/profiles` | user (session or API token) <!-- server/service/handler.go:664; handler listMDMAppleConfigProfilesEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/filevault/summary` | user (session or API token) <!-- server/service/handler.go:669; handler getMdmAppleFileVaultSummaryEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/profiles/summary` | user (session or API token) <!-- server/service/handler.go:674; handler getMDMAppleProfilesSummaryEndpoint -->|
| POST | `/api/_version_/fleet/mdm/apple/enrollment_profile` | user (session or API token) <!-- server/service/handler.go:678; handler createMDMAppleSetupAssistantEndpoint -->|
| POST | `/api/_version_/fleet/enrollment_profiles/automatic` | user (session or API token) <!-- server/service/handler.go:679; handler createMDMAppleSetupAssistantEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/enrollment_profile` | user (session or API token) <!-- server/service/handler.go:683; handler getMDMAppleSetupAssistantEndpoint -->|
| GET | `/api/_version_/fleet/enrollment_profiles/automatic` | user (session or API token) <!-- server/service/handler.go:684; handler getMDMAppleSetupAssistantEndpoint -->|
| GET | `/api/_version_/fleet/enrollment_profiles/automatic/default` | user (session or API token) <!-- server/service/handler.go:685; handler getDefaultMDMAppleSetupAssistantProfileEndpoint -->|
| DELETE | `/api/_version_/fleet/mdm/apple/enrollment_profile` | user (session or API token) <!-- server/service/handler.go:689; handler deleteMDMAppleSetupAssistantEndpoint -->|
| DELETE | `/api/_version_/fleet/enrollment_profiles/automatic` | user (session or API token) <!-- server/service/handler.go:690; handler deleteMDMAppleSetupAssistantEndpoint -->|
| POST | `/api/_version_/fleet/mdm/apple/installers` | user (session or API token) <!-- server/service/handler.go:695; handler uploadAppleInstallerEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/installers/{installer_id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:696; handler getAppleInstallerEndpoint -->|
| DELETE | `/api/_version_/fleet/mdm/apple/installers/{installer_id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:697; handler deleteAppleInstallerEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/installers` | user (session or API token) <!-- server/service/handler.go:698; handler listMDMAppleInstallersEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/devices` | user (session or API token) <!-- server/service/handler.go:699; handler listMDMAppleDevicesEndpoint -->|
| GET | `/api/_version_/fleet/mdm/manual_enrollment_profile` | user (session or API token) <!-- server/service/handler.go:704; handler getManualEnrollmentProfileEndpoint -->|
| GET | `/api/_version_/fleet/enrollment_profiles/manual` | user (session or API token) <!-- server/service/handler.go:705; handler getManualEnrollmentProfileEndpoint -->|
| POST | `/api/_version_/fleet/mdm/bootstrap` | user (session or API token) <!-- server/service/handler.go:712; handler uploadBootstrapPackageEndpoint -->|
| POST | `/api/_version_/fleet/bootstrap` | user (session or API token) <!-- server/service/handler.go:713; handler uploadBootstrapPackageEndpoint -->|
| GET | `/api/_version_/fleet/mdm/bootstrap/{fleet_id:[0-9]+}/metadata` | user (session or API token) <!-- server/service/handler.go:717; handler bootstrapPackageMetadataEndpoint -->|
| GET | `/api/_version_/fleet/bootstrap/{fleet_id:[0-9]+}/metadata` | user (session or API token) <!-- server/service/handler.go:718; handler bootstrapPackageMetadataEndpoint -->|
| DELETE | `/api/_version_/fleet/mdm/bootstrap/{fleet_id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:722; handler deleteBootstrapPackageEndpoint -->|
| DELETE | `/api/_version_/fleet/bootstrap/{fleet_id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:723; handler deleteBootstrapPackageEndpoint -->|
| GET | `/api/_version_/fleet/mdm/bootstrap/summary` | user (session or API token) <!-- server/service/handler.go:727; handler getMDMAppleBootstrapPackageSummaryEndpoint -->|
| GET | `/api/_version_/fleet/bootstrap/summary` | user (session or API token) <!-- server/service/handler.go:728; handler getMDMAppleBootstrapPackageSummaryEndpoint -->|
| POST | `/api/_version_/fleet/mdm/apple/bootstrap` | user (session or API token) <!-- server/service/handler.go:732; handler uploadBootstrapPackageEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/bootstrap/{fleet_id:[0-9]+}/metadata` | user (session or API token) <!-- server/service/handler.go:734; handler bootstrapPackageMetadataEndpoint -->|
| DELETE | `/api/_version_/fleet/mdm/apple/bootstrap/{fleet_id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:736; handler deleteBootstrapPackageEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/bootstrap/summary` | user (session or API token) <!-- server/service/handler.go:738; handler getMDMAppleBootstrapPackageSummaryEndpoint -->|
| POST | `/api/_version_/fleet/mdm/hosts/{id:[0-9]+}/lock` | user (session or API token) <!-- server/service/handler.go:744; handler deviceLockEndpoint -->|
| POST | `/api/_version_/fleet/mdm/hosts/{id:[0-9]+}/wipe` | user (session or API token) <!-- server/service/handler.go:745; handler deviceWipeEndpoint -->|
| GET | `/api/_version_/fleet/mdm/hosts/{id:[0-9]+}/profiles` | user (session or API token) <!-- server/service/handler.go:749; handler getHostProfilesEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple` | user (session or API token) <!-- server/service/handler.go:753; handler getAppleMDMEndpoint -->|
| GET | `/api/_version_/fleet/apns` | user (session or API token) <!-- server/service/handler.go:754; handler getAppleMDMEndpoint -->|
| POST | `/api/_version_/fleet/mdm/setup/eula` | user (session or API token) <!-- server/service/handler.go:760; handler createMDMEULAEndpoint -->|
| POST | `/api/_version_/fleet/setup_experience/eula` | user (session or API token) <!-- server/service/handler.go:761; handler createMDMEULAEndpoint -->|
| GET | `/api/_version_/fleet/mdm/setup/eula/metadata` | user (session or API token) <!-- server/service/handler.go:765; handler getMDMEULAMetadataEndpoint -->|
| GET | `/api/_version_/fleet/setup_experience/eula/metadata` | user (session or API token) <!-- server/service/handler.go:766; handler getMDMEULAMetadataEndpoint -->|
| DELETE | `/api/_version_/fleet/mdm/setup/eula/{token}` | user (session or API token) <!-- server/service/handler.go:770; handler deleteMDMEULAEndpoint -->|
| DELETE | `/api/_version_/fleet/setup_experience/eula/{token}` | user (session or API token) <!-- server/service/handler.go:771; handler deleteMDMEULAEndpoint -->|
| POST | `/api/_version_/fleet/mdm/apple/setup/eula` | user (session or API token) <!-- server/service/handler.go:774; handler createMDMEULAEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/setup/eula/metadata` | user (session or API token) <!-- server/service/handler.go:776; handler getMDMEULAMetadataEndpoint -->|
| DELETE | `/api/_version_/fleet/mdm/apple/setup/eula/{token}` | user (session or API token) <!-- server/service/handler.go:778; handler deleteMDMEULAEndpoint -->|
| POST | `/api/_version_/fleet/mdm/apple/profiles/preassign` | user (session or API token) <!-- server/service/handler.go:780; handler preassignMDMAppleProfileEndpoint -->|
| POST | `/api/_version_/fleet/mdm/apple/profiles/match` | user (session or API token) <!-- server/service/handler.go:781; handler matchMDMApplePreassignmentEndpoint -->|
| GET | `/api/_version_/fleet/assets` | user (session or API token) <!-- server/service/handler.go:784; handler listAppleDDMAssetsEndpoint -->|
| GET | `/api/_version_/fleet/assets/{asset_uuid}` | user (session or API token) <!-- server/service/handler.go:785; handler getAppleDDMAssetEndpoint -->|
| POST | `/api/_version_/fleet/assets` | user (session or API token) <!-- server/service/handler.go:786; handler createAppleDDMAssetEndpoint -->|
| DELETE | `/api/_version_/fleet/assets/{asset_uuid}` | user (session or API token) <!-- server/service/handler.go:787; handler deleteAppleDDMAssetEndpoint -->|
| POST | `/api/_version_/fleet/assets/batch` | user (session or API token) <!-- server/service/handler.go:788; handler batchSetAppleDDMAssetsEndpoint -->|
| GET | `/api/_version_/fleet/hosts/{id:[0-9]+}/configuration_profiles` | user (session or API token) <!-- server/service/handler.go:792; handler getHostProfilesEndpoint -->|
| POST | `/api/_version_/fleet/mdm/commands/run` | user (session or API token) <!-- server/service/handler.go:796; handler runMDMCommandEndpoint -->|
| POST | `/api/_version_/fleet/commands/run` | user (session or API token) <!-- server/service/handler.go:797; handler runMDMCommandEndpoint -->|
| GET | `/api/_version_/fleet/mdm/commandresults` | user (session or API token) <!-- server/service/handler.go:801; handler getMDMCommandResultsEndpoint -->|
| GET | `/api/_version_/fleet/commands/results` | user (session or API token) <!-- server/service/handler.go:802; handler getMDMCommandResultsEndpoint -->|
| GET | `/api/_version_/fleet/mdm/commands` | user (session or API token) <!-- server/service/handler.go:806; handler listMDMCommandsEndpoint -->|
| GET | `/api/_version_/fleet/commands` | user (session or API token) <!-- server/service/handler.go:807; handler listMDMCommandsEndpoint -->|
| PATCH | `/api/_version_/fleet/mdm/hosts/{id:[0-9]+}/unenroll` | user (session or API token) <!-- server/service/handler.go:811; handler mdmUnenrollEndpoint -->|
| DELETE | `/api/_version_/fleet/hosts/{id:[0-9]+}/mdm` | user (session or API token) <!-- server/service/handler.go:812; handler mdmUnenrollEndpoint -->|
| GET | `/api/_version_/fleet/mdm/disk_encryption/summary` | user (session or API token) <!-- server/service/handler.go:816; handler getMDMDiskEncryptionSummaryEndpoint -->|
| GET | `/api/_version_/fleet/disk_encryption` | user (session or API token) <!-- server/service/handler.go:817; handler getMDMDiskEncryptionSummaryEndpoint -->|
| GET | `/api/_version_/fleet/mdm/hosts/{id:[0-9]+}/encryption_key` | user (session or API token) <!-- server/service/handler.go:821; handler getHostEncryptionKey -->|
| GET | `/api/_version_/fleet/hosts/{id:[0-9]+}/encryption_key` | user (session or API token) <!-- server/service/handler.go:822; handler getHostEncryptionKey -->|
| GET | `/api/_version_/fleet/mdm/profiles/summary` | user (session or API token) <!-- server/service/handler.go:826; handler getMDMProfilesSummaryEndpoint -->|
| GET | `/api/_version_/fleet/configuration_profiles/summary` | user (session or API token) <!-- server/service/handler.go:827; handler getMDMProfilesSummaryEndpoint -->|
| GET | `/api/_version_/fleet/mdm/profiles/{profile_uuid}` | user (session or API token) <!-- server/service/handler.go:831; handler getMDMConfigProfileEndpoint -->|
| GET | `/api/_version_/fleet/configuration_profiles/{profile_uuid}` | user (session or API token) <!-- server/service/handler.go:832; handler getMDMConfigProfileEndpoint -->|
| DELETE | `/api/_version_/fleet/mdm/profiles/{profile_uuid}` | user (session or API token) <!-- server/service/handler.go:836; handler deleteMDMConfigProfileEndpoint -->|
| DELETE | `/api/_version_/fleet/configuration_profiles/{profile_uuid}` | user (session or API token) <!-- server/service/handler.go:837; handler deleteMDMConfigProfileEndpoint -->|
| GET | `/api/_version_/fleet/mdm/profiles` | user (session or API token) <!-- server/service/handler.go:841; handler listMDMConfigProfilesEndpoint -->|
| GET | `/api/_version_/fleet/configuration_profiles` | user (session or API token) <!-- server/service/handler.go:842; handler listMDMConfigProfilesEndpoint -->|
| POST | `/api/_version_/fleet/mdm/profiles` | user (session or API token) <!-- server/service/handler.go:846; handler newMDMConfigProfileEndpoint -->|
| POST | `/api/_version_/fleet/configuration_profiles` | user (session or API token) <!-- server/service/handler.go:847; handler newMDMConfigProfileEndpoint -->|
| PATCH | `/api/_version_/fleet/configuration_profiles/{profile_uuid}` | user (session or API token) <!-- server/service/handler.go:848; handler updateMDMConfigProfileEndpoint -->|
| POST | `/api/_version_/fleet/configuration_profiles/batch` | user (session or API token) <!-- server/service/handler.go:850; handler batchModifyMDMConfigProfilesEndpoint -->|
| POST | `/api/_version_/fleet/hosts/{host_id:[0-9]+}/configuration_profiles/resend/{profile_uuid}` | user (session or API token) <!-- server/service/handler.go:854; handler resendHostMDMProfileEndpoint -->|
| POST | `/api/_version_/fleet/hosts/{host_id:[0-9]+}/configuration_profiles/{profile_uuid}/resend` | user (session or API token) <!-- server/service/handler.go:855; handler resendHostMDMProfileEndpoint -->|
| POST | `/api/_version_/fleet/hosts/{host_id:[0-9]+}/name_template/resend` | user (session or API token) <!-- server/service/handler.go:856; handler resendHostNameTemplateEndpoint -->|
| POST | `/api/_version_/fleet/configuration_profiles/resend/batch` | user (session or API token) <!-- server/service/handler.go:857; handler batchResendMDMProfileToHostsEndpoint -->|
| GET | `/api/_version_/fleet/configuration_profiles/{profile_uuid}/status` | user (session or API token) <!-- server/service/handler.go:858; handler getMDMConfigProfileStatusEndpoint -->|
| PATCH | `/api/_version_/fleet/mdm/apple/settings` | user (session or API token) <!-- server/service/handler.go:862; handler updateMDMAppleSettingsEndpoint -->|
| POST | `/api/_version_/fleet/disk_encryption` | user (session or API token) <!-- server/service/handler.go:863; handler updateDiskEncryptionEndpoint -->|
| POST | `/api/_version_/fleet/host_name_template` | user (session or API token) <!-- server/service/handler.go:864; handler updateHostNameTemplateEndpoint -->|
| POST | `/api/_version_/fleet/mdm/apple/request_csr` | user (session or API token) <!-- server/service/handler.go:871; handler requestMDMAppleCSREndpoint -->|
| POST | `/api/_version_/fleet/mdm/apple/dep/key_pair` | user (session or API token) <!-- server/service/handler.go:874; handler newMDMAppleDEPKeyPairEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/ab_public_key` | user (session or API token) <!-- server/service/handler.go:875; handler generateABMKeyPairEndpoint -->|
| POST | `/api/_version_/fleet/ab_tokens` | user (session or API token) <!-- server/service/handler.go:876; handler uploadABMTokenEndpoint -->|
| DELETE | `/api/_version_/fleet/ab_tokens/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:877; handler deleteABMTokenEndpoint -->|
| GET | `/api/_version_/fleet/ab_tokens` | user (session or API token) <!-- server/service/handler.go:878; handler listABMTokensEndpoint -->|
| GET | `/api/_version_/fleet/ab_tokens/count` | user (session or API token) <!-- server/service/handler.go:879; handler countABMTokensEndpoint -->|
| PATCH | `/api/_version_/fleet/ab_tokens/{id:[0-9]+}/fleets` | user (session or API token) <!-- server/service/handler.go:880; handler updateABMTokenTeamsEndpoint -->|
| PATCH | `/api/_version_/fleet/ab_tokens/{id:[0-9]+}/renew` | user (session or API token) <!-- server/service/handler.go:881; handler renewABMTokenEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/request_csr` | user (session or API token) <!-- server/service/handler.go:883; handler getMDMAppleCSREndpoint -->|
| POST | `/api/_version_/fleet/mdm/apple/apns_certificate` | user (session or API token) <!-- server/service/handler.go:884; handler uploadMDMAppleAPNSCertEndpoint -->|
| DELETE | `/api/_version_/fleet/mdm/apple/apns_certificate` | user (session or API token) <!-- server/service/handler.go:885; handler deleteMDMAppleAPNSCertEndpoint -->|
| GET | `/api/_version_/fleet/vpp_tokens` | user (session or API token) <!-- server/service/handler.go:888; handler getVPPTokens -->|
| POST | `/api/_version_/fleet/vpp_tokens` | user (session or API token) <!-- server/service/handler.go:889; handler uploadVPPTokenEndpoint -->|
| PATCH | `/api/_version_/fleet/vpp_tokens/{id}/fleets` | user (session or API token) <!-- server/service/handler.go:890; handler patchVPPTokensTeams -->|
| PATCH | `/api/_version_/fleet/vpp_tokens/{id}/renew` | user (session or API token) <!-- server/service/handler.go:891; handler patchVPPTokenRenewEndpoint -->|
| DELETE | `/api/_version_/fleet/vpp_tokens/{id}` | user (session or API token) <!-- server/service/handler.go:892; handler deleteVPPToken -->|
| POST | `/api/_version_/fleet/software/app_store_apps/batch` | user (session or API token) <!-- server/service/handler.go:895; handler batchAssociateAppStoreAppsEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple_bm` | user (session or API token) <!-- server/service/handler.go:899; handler getAppleBMEndpoint -->|
| GET | `/api/_version_/fleet/abm` | user (session or API token) <!-- server/service/handler.go:901; handler getAppleBMEndpoint -->|
| POST | `/api/_version_/fleet/mdm/apple/profiles/batch` | user (session or API token) <!-- server/service/handler.go:910; handler batchSetMDMAppleProfilesEndpoint -->|
| POST | `/api/_version_/fleet/mdm/profiles/batch` | user (session or API token) <!-- server/service/handler.go:915; handler batchSetMDMProfilesEndpoint -->|
| POST | `/api/_version_/fleet/certificate_authorities` | user (session or API token) <!-- server/service/handler.go:918; handler createCertificateAuthorityEndpoint -->|
| GET | `/api/_version_/fleet/certificate_authorities` | user (session or API token) <!-- server/service/handler.go:919; handler listCertificateAuthoritiesEndpoint -->|
| GET | `/api/_version_/fleet/certificate_authorities/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:920; handler getCertificateAuthorityEndpoint -->|
| DELETE | `/api/_version_/fleet/certificate_authorities/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:921; handler deleteCertificateAuthorityEndpoint -->|
| PATCH | `/api/_version_/fleet/certificate_authorities/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:922; handler updateCertificateAuthorityEndpoint -->|
| POST | `/api/_version_/fleet/certificate_authorities/{id:[0-9]+}/request_certificate` | user (session or API token) <!-- server/service/handler.go:923; handler requestCertificateEndpoint -->|
| POST | `/api/_version_/fleet/spec/certificate_authorities` | user (session or API token) <!-- server/service/handler.go:924; handler batchApplyCertificateAuthoritiesEndpoint -->|
| GET | `/api/_version_/fleet/spec/certificate_authorities` | user (session or API token) <!-- server/service/handler.go:925; handler getCertificateAuthoritiesSpecEndpoint -->|
| POST | `/api/_version_/fleet/software/web_apps` | user (session or API token) <!-- server/service/handler.go:928; handler createAndroidWebAppEndpoint -->|
| GET | `/api/_version_/fleet/device/{token}` | device (device token) <!-- server/service/handler.go:939; handler getDeviceHostEndpoint -->|
| GET | `/api/_version_/fleet/device/{token}/desktop` | device (device token) <!-- server/service/handler.go:940; handler getFleetDesktopEndpoint -->|
| HEAD | `/api/_version_/fleet/device/{token}/ping` | device (device token) <!-- server/service/handler.go:941; handler devicePingEndpoint -->|
| POST | `/api/_version_/fleet/device/{token}/refetch` | device (device token) <!-- server/service/handler.go:942; handler refetchDeviceHostEndpoint -->|
| GET | `/api/_version_/fleet/device/{token}/device_mapping` | device (device token) <!-- server/service/handler.go:944; handler listDeviceHostDeviceMappingEndpoint -->|
| GET | `/api/_version_/fleet/device/{token}/macadmins` | device (device token) <!-- server/service/handler.go:945; handler getDeviceMacadminsDataEndpoint -->|
| GET | `/api/_version_/fleet/device/{token}/policies` | device (device token) <!-- server/service/handler.go:946; handler listDevicePoliciesEndpoint -->|
| GET | `/api/_version_/fleet/device/{token}/transparency` | device (device token) <!-- server/service/handler.go:947; handler transparencyURL -->|
| POST | `/api/_version_/fleet/device/{token}/debug/errors` | device (device token) <!-- server/service/handler.go:948; handler fleetdError -->|
| GET | `/api/_version_/fleet/device/{token}/software` | device (device token) <!-- server/service/handler.go:949; handler getDeviceSoftwareEndpoint -->|
| POST | `/api/_version_/fleet/device/{token}/software/install/{software_title_id}` | device (device token) <!-- server/service/handler.go:950; handler submitSelfServiceSoftwareInstall -->|
| POST | `/api/_version_/fleet/device/{token}/software/install_all` | device (device token) <!-- server/service/handler.go:951; handler submitSelfServiceSoftwareInstallAll -->|
| POST | `/api/_version_/fleet/device/{token}/software/uninstall/{software_title_id}` | device (device token) <!-- server/service/handler.go:952; handler submitDeviceSoftwareUninstall -->|
| GET | `/api/_version_/fleet/device/{token}/software/install/{install_uuid}/results` | device (device token) <!-- server/service/handler.go:953; handler getDeviceSoftwareInstallResultsEndpoint -->|
| GET | `/api/_version_/fleet/device/{token}/software/uninstall/{execution_id}/results` | device (device token) <!-- server/service/handler.go:954; handler getDeviceSoftwareUninstallResultsEndpoint -->|
| GET | `/api/_version_/fleet/device/{token}/software/self_service_categories` | device (device token) <!-- server/service/handler.go:955; handler getDeviceSelfServiceCategoriesEndpoint -->|
| GET | `/api/_version_/fleet/device/{token}/certificates` | device (device token) <!-- server/service/handler.go:956; handler listDeviceCertificatesEndpoint -->|
| POST | `/api/_version_/fleet/device/{token}/setup_experience/status` | device (device token) <!-- server/service/handler.go:957; handler getDeviceSetupExperienceStatusEndpoint -->|
| GET | `/api/_version_/fleet/device/{token}/software/titles/{software_title_id}/icon` | device (device token) <!-- server/service/handler.go:958; handler getDeviceSoftwareIconEndpoint -->|
| POST | `/api/_version_/fleet/device/{token}/mdm/linux/trigger_escrow` | device (device token) <!-- server/service/handler.go:959; handler triggerLinuxDiskEncryptionEscrowEndpoint -->|
| POST | `/api/_version_/fleet/device/{token}/bypass_conditional_access` | device (device token) <!-- server/service/handler.go:960; handler bypassConditionalAccessEndpoint -->|
| GET | `/api/_version_/fleet/device/{token}/mdm/apple/manual_enrollment_profile` | device (device token) <!-- server/service/handler.go:963; handler getDeviceMDMManualEnrollProfileEndpoint -->|
| GET | `/api/_version_/fleet/device/{token}/software/commands/{command_uuid}/results` | device (device token) <!-- server/service/handler.go:964; handler getDeviceMDMCommandResultsEndpoint -->|
| POST | `/api/_version_/fleet/device/{token}/configuration_profiles/{profile_uuid}/resend` | device (device token) <!-- server/service/handler.go:965; handler resendDeviceConfigurationProfileEndpoint -->|
| POST | `/api/_version_/fleet/device/{token}/migrate_mdm` | device (device token) <!-- server/service/handler.go:966; handler migrateMDMDeviceEndpoint -->|
| POST | `/api/osquery/config` | host (osquery node key) <!-- server/service/handler.go:998; handler getClientConfigEndpoint -->|
| POST | `/api/v1/osquery/config` | host (osquery node key) <!-- server/service/handler.go:998; alt path of /api/osquery/config; handler getClientConfigEndpoint -->|
| POST | `/api/osquery/distributed/read` | host (osquery node key) <!-- server/service/handler.go:1000; handler getDistributedQueriesEndpoint -->|
| POST | `/api/v1/osquery/distributed/read` | host (osquery node key) <!-- server/service/handler.go:1000; alt path of /api/osquery/distributed/read; handler getDistributedQueriesEndpoint -->|
| POST | `/api/osquery/distributed/write` | host (osquery node key) <!-- server/service/handler.go:1027; handler submitDistributedQueryResultsEndpoint -->|
| POST | `/api/v1/osquery/distributed/write` | host (osquery node key) <!-- server/service/handler.go:1027; alt path of /api/osquery/distributed/write; handler submitDistributedQueryResultsEndpoint -->|
| POST | `/api/osquery/carve/begin` | host (osquery node key) <!-- server/service/handler.go:1029; handler carveBeginEndpoint -->|
| POST | `/api/v1/osquery/carve/begin` | host (osquery node key) <!-- server/service/handler.go:1029; alt path of /api/osquery/carve/begin; handler carveBeginEndpoint -->|
| POST | `/api/osquery/log` | host (osquery node key) <!-- server/service/handler.go:1031; handler submitLogsEndpoint -->|
| POST | `/api/v1/osquery/log` | host (osquery node key) <!-- server/service/handler.go:1031; alt path of /api/osquery/log; handler submitLogsEndpoint -->|
| POST | `/api/osquery/yara/{name}` | host (osquery node key) <!-- server/service/handler.go:1033; handler getYaraEndpoint -->|
| POST | `/api/v1/osquery/yara/{name}` | host (osquery node key) <!-- server/service/handler.go:1033; alt path of /api/osquery/yara/{name}; handler getYaraEndpoint -->|
| GET | `/api/fleetd/certificates/{id:[0-9]+}` | android (orbit node key) <!-- server/service/handler.go:1040; handler getDeviceCertificateTemplateEndpoint -->|
| PUT | `/api/fleetd/certificates/{id:[0-9]+}/status` | android (orbit node key) <!-- server/service/handler.go:1041; handler updateCertificateStatusEndpoint -->|
| POST | `/api/fleet/orbit/device_token` | orbit (orbit node key) <!-- server/service/handler.go:1045; handler setOrUpdateDeviceTokenEndpoint -->|
| POST | `/api/fleet/orbit/config` | orbit (orbit node key) <!-- server/service/handler.go:1046; handler getOrbitConfigEndpoint -->|
| POST | `/api/fleet/orbit/scripts/request` | orbit (orbit node key) <!-- server/service/handler.go:1049; handler getOrbitScriptEndpoint -->|
| POST | `/api/fleet/orbit/scripts/result` | orbit (orbit node key) <!-- server/service/handler.go:1050; handler postOrbitScriptResultEndpoint -->|
| PUT | `/api/fleet/orbit/device_mapping` | orbit (orbit node key) <!-- server/service/handler.go:1051; handler putOrbitDeviceMappingEndpoint -->|
| POST | `/api/fleet/orbit/software_install/result` | orbit (orbit node key) <!-- server/service/handler.go:1052; handler postOrbitSoftwareInstallResultEndpoint -->|
| POST | `/api/fleet/orbit/software_install/package` | orbit (orbit node key) <!-- server/service/handler.go:1053; handler orbitDownloadSoftwareInstallerEndpoint -->|
| POST | `/api/fleet/orbit/software_install/details` | orbit (orbit node key) <!-- server/service/handler.go:1054; handler getOrbitSoftwareInstallDetails -->|
| POST | `/api/fleet/orbit/setup_experience/init` | orbit (orbit node key) <!-- server/service/handler.go:1055; handler orbitSetupExperienceInitEndpoint -->|
| POST | `/api/fleet/orbit/setup_experience/status` | orbit (orbit node key) <!-- server/service/handler.go:1060; handler getOrbitSetupExperienceStatusEndpoint -->|
| POST | `/api/fleet/orbit/disk_encryption_key` | orbit (orbit node key) <!-- server/service/handler.go:1063; handler postOrbitDiskEncryptionKeyEndpoint -->|
| POST | `/api/fleet/orbit/luks_data` | orbit (orbit node key) <!-- server/service/handler.go:1065; handler postOrbitLUKSEndpoint -->|
| POST | `/api/osquery/enroll` | none <!-- server/service/handler.go:1073; handler enrollAgentEndpoint -->|
| POST | `/api/v1/osquery/enroll` | none <!-- server/service/handler.go:1073; alt path of /api/osquery/enroll; handler enrollAgentEndpoint -->|
| GET | `/api/mdm/apple/enroll` | none <!-- server/service/handler.go:1082; handler mdmAppleEnrollEndpoint -->|
| POST | `/api/mdm/apple/enroll` | none <!-- server/service/handler.go:1083; handler mdmAppleEnrollEndpoint -->|
| GET | `/api/mdm/apple/installer` | none <!-- server/service/handler.go:1085; handler mdmAppleGetInstallerEndpoint -->|
| HEAD | `/api/mdm/apple/installer` | none <!-- server/service/handler.go:1086; handler mdmAppleHeadInstallerEndpoint -->|
| POST | `/api/_version_/fleet/ota_enrollment` | none <!-- server/service/handler.go:1087; handler mdmAppleOTAEndpoint -->|
| GET | `/api/_version_/fleet/mdm/bootstrap` | none <!-- server/service/handler.go:1091; handler downloadBootstrapPackageEndpoint -->|
| GET | `/api/_version_/fleet/bootstrap` | none <!-- server/service/handler.go:1092; handler downloadBootstrapPackageEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/bootstrap` | none <!-- server/service/handler.go:1095; handler downloadBootstrapPackageEndpoint -->|
| GET | `/api/_version_/fleet/mdm/setup/eula/{token}` | none <!-- server/service/handler.go:1099; handler getMDMEULAEndpoint -->|
| GET | `/api/_version_/fleet/setup_experience/eula/{token}` | none <!-- server/service/handler.go:1100; handler getMDMEULAEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/setup/eula/{token}` | none <!-- server/service/handler.go:1103; handler getMDMEULAEndpoint -->|
| GET | `/api/_version_/fleet/enrollment_profiles/ota` | none <!-- server/service/handler.go:1106; handler getOTAProfileEndpoint -->|
| POST | `/api/mdm/apple/account_driven_enroll/{token}` | none <!-- server/service/handler.go:1109; handler mdmAppleAccountEnrollEndpoint -->|
| POST | `/api/mdm/apple/account_driven_enroll` | none <!-- server/service/handler.go:1111; handler mdmAppleAccountEnrollEndpoint -->|
| POST | `/api/mdm/apple/psso/nonce` | none <!-- server/service/handler.go:1120; handler pssoNonceEndpoint -->|
| POST | `/api/mdm/apple/psso/registration` | none <!-- server/service/handler.go:1121; handler pssoRegistrationEndpoint -->|
| POST | `/api/mdm/apple/psso/token` | none <!-- server/service/handler.go:1122; handler pssoTokenEndpoint -->|
| GET | `/api/mdm/apple/psso/jwks` | none <!-- server/service/handler.go:1123; handler pssoJWKSEndpoint -->|
| POST | `/api/mdm/microsoft/discovery` | none <!-- server/service/handler.go:1132; handler mdmMicrosoftDiscoveryEndpoint -->|
| POST | `/api/mdm/microsoft/policy` | none <!-- server/service/handler.go:1135; handler mdmMicrosoftPolicyEndpoint -->|
| POST | `/api/mdm/microsoft/enroll` | none <!-- server/service/handler.go:1138; handler mdmMicrosoftEnrollEndpoint -->|
| POST | `/api/mdm/microsoft/management` | none <!-- server/service/handler.go:1142; handler mdmMicrosoftManagementEndpoint -->|
| GET | `/api/mdm/microsoft/tos` | none <!-- server/service/handler.go:1145; handler mdmMicrosoftTOSEndpoint -->|
| POST | `/api/fleet/orbit/enroll` | none (orbit enroll) <!-- server/service/handler.go:1149; handler enrollOrbitEndpoint -->|
| GET | `/api/_version_/fleet/software/titles/{title_id:[0-9]+}/in_house_app/{token:[a-f0-9-]+}` | none <!-- server/service/handler.go:1153; handler getInHouseAppPackageEndpoint -->|
| GET | `/api/_version_/fleet/software/titles/{title_id:[0-9]+}/in_house_app/manifest/{token:[a-f0-9-]+}` | none <!-- server/service/handler.go:1154; handler getInHouseAppManifestEndpoint -->|
| POST | `/api/osquery/carve/block` | none <!-- server/service/handler.go:1173; handler carveBlockEndpoint -->|
| POST | `/api/v1/osquery/carve/block` | none <!-- server/service/handler.go:1173; alt path of /api/osquery/carve/block; handler carveBlockEndpoint -->|
| GET | `/api/_version_/fleet/software/titles/{title_id:[0-9]+}/package/token/{token}` | none <!-- server/service/handler.go:1175; handler downloadSoftwareInstallerEndpoint -->|
| POST | `/api/_version_/fleet/perform_required_password_reset` | none <!-- server/service/handler.go:1178; handler performRequiredPasswordResetEndpoint -->|
| POST | `/api/_version_/fleet/users` | none <!-- server/service/handler.go:1179; handler createUserFromInviteEndpoint -->|
| GET | `/api/_version_/fleet/invites/{token}` | none <!-- server/service/handler.go:1180; handler verifyInviteEndpoint -->|
| POST | `/api/_version_/fleet/reset_password` | none <!-- server/service/handler.go:1181; handler resetPasswordEndpoint -->|
| POST | `/api/_version_/fleet/logout` | none <!-- server/service/handler.go:1182; handler logoutEndpoint -->|
| GET | `/api/_version_/fleet/logo` | none <!-- server/service/handler.go:1189; handler getOrgLogoEndpoint -->|
| POST | `/api/v1/fleet/sso` | none <!-- server/service/handler.go:1217; handler initiateSSOEndpoint -->|
| POST | `/api/v1/fleet/sso/callback` | none <!-- server/service/handler.go:1222; handler makeCallbackSSOEndpoint -->|
| GET | `/api/v1/fleet/sso` | none <!-- server/service/handler.go:1223; handler settingsSSOEndpoint -->|
| GET | `/api/_version_/fleet/results/` | none <!-- server/service/handler.go:1230; path prefix, not exact match; handler makeStreamDistributedQueryCampaignResultsHandler -->|
| POST | `/api/_version_/fleet/forgot_password` | none <!-- server/service/handler.go:1236; handler forgotPasswordEndpoint -->|
| POST | `/api/_version_/fleet/login` | none <!-- server/service/handler.go:1239; handler loginEndpoint -->|
| POST | `/api/_version_/fleet/sessions` | none <!-- server/service/handler.go:1241; handler sessionCreateEndpoint -->|
| HEAD | `/api/fleet/device/ping` | none <!-- server/service/handler.go:1243; handler devicePingEndpoint -->|
| HEAD | `/api/fleet/orbit/ping` | none <!-- server/service/handler.go:1245; handler orbitPingEndpoint -->|
| POST | `/api/_version_/fleet/calendar/webhook/{event_uuid}` | none <!-- server/service/handler.go:1248; handler calendarWebhookEndpoint -->|
| POST | `/api/_version_/fleet/mdm/sso` | none <!-- server/service/handler.go:1251; handler initiateMDMSSOEndpoint -->|
| POST | `/api/_version_/fleet/mdm/sso/callback` | none <!-- server/service/handler.go:1256; handler callbackMDMSSOEndpoint -->|
| GET | `/api/_version_/fleet/android_enterprise/signup_url` | user (session or API token) <!-- server/mdm/android/service/handler.go:25; handler enterpriseSignupEndpoint -->|
| GET | `/api/_version_/fleet/android_enterprise` | user (session or API token) <!-- server/mdm/android/service/handler.go:26; handler getEnterpriseEndpoint -->|
| DELETE | `/api/_version_/fleet/android_enterprise` | user (session or API token) <!-- server/mdm/android/service/handler.go:27; handler deleteEnterpriseEndpoint -->|
| GET | `/api/_version_/fleet/android_enterprise/signup_sse` | user (session or API token) <!-- server/mdm/android/service/handler.go:28; handler enterpriseSSE -->|
| GET | `/api/_version_/fleet/android_enterprise/connect/{token}` | none <!-- server/mdm/android/service/handler.go:35; handler enterpriseSignupCallbackEndpoint -->|
| GET | `/api/_version_/fleet/android_enterprise/enrollment_token` | none <!-- server/mdm/android/service/handler.go:36; handler enrollmentTokenEndpoint -->|
| POST | `/api/v1/fleet/android_enterprise/pubsub` | none <!-- server/mdm/android/service/handler.go:37; handler pubSubPushEndpoint -->|
| GET | `/api/_version_/fleet/activities` | user (session or API token) <!-- server/activity/internal/service/handler.go:28; handler listActivitiesEndpoint -->|
| GET | `/api/_version_/fleet/hosts/{id:[0-9]+}/activities` | user (session or API token) <!-- server/activity/internal/service/handler.go:29; handler listHostPastActivitiesEndpoint -->|
| GET | `/api/mdm/acme/{identifier}/new_nonce` | none (protocol auth in handler) <!-- server/mdm/acme/internal/service/handler.go:37; handler getNewNonceEndpoint -->|
| HEAD | `/api/mdm/acme/{identifier}/new_nonce` | none (protocol auth in handler) <!-- server/mdm/acme/internal/service/handler.go:38; handler getNewNonceEndpoint -->|
| POST | `/api/mdm/acme/{identifier}/new_nonce` | none (protocol auth in handler) <!-- server/mdm/acme/internal/service/handler.go:39; handler getNewNonceEndpoint -->|
| GET | `/api/mdm/acme/{identifier}/directory` | none (protocol auth in handler) <!-- server/mdm/acme/internal/service/handler.go:44; handler getDirectoryEndpoint -->|
| POST | `/api/mdm/acme/{identifier}/directory` | none (protocol auth in handler) <!-- server/mdm/acme/internal/service/handler.go:45; handler getDirectoryEndpoint -->|
| POST | `/api/mdm/acme/{identifier}/new_account` | none (protocol auth in handler) <!-- server/mdm/acme/internal/service/handler.go:47; handler createAccountEndpoint -->|
| POST | `/api/mdm/acme/{identifier}/new_order` | none (protocol auth in handler) <!-- server/mdm/acme/internal/service/handler.go:48; handler createOrderEndpoint -->|
| POST | `/api/mdm/acme/{identifier}/orders/{order_id}` | none (protocol auth in handler) <!-- server/mdm/acme/internal/service/handler.go:51; handler getOrderEndpoint -->|
| POST | `/api/mdm/acme/{identifier}/accounts/{account_id}/orders` | none (protocol auth in handler) <!-- server/mdm/acme/internal/service/handler.go:53; handler listOrdersEndpoint -->|
| POST | `/api/mdm/acme/{identifier}/orders/{order_id}/certificate` | none (protocol auth in handler) <!-- server/mdm/acme/internal/service/handler.go:55; handler getCertificateEndpoint -->|
| POST | `/api/mdm/acme/{identifier}/authorizations/{authorization_id}` | none (protocol auth in handler) <!-- server/mdm/acme/internal/service/handler.go:57; handler getAuthorizationEndpoint -->|
| POST | `/api/mdm/acme/{identifier}/challenges/{challenge_id}` | none (protocol auth in handler) <!-- server/mdm/acme/internal/service/handler.go:58; handler getChallengeEndpoint -->|
| POST | `/api/mdm/acme/{identifier}/orders/{order_id}/finalize` | none (protocol auth in handler) <!-- server/mdm/acme/internal/service/handler.go:59; handler finalizeOrderEndpoint -->|
| GET | `/api/_version_/fleet/charts/{metric}` | user (session or API token) <!-- server/chart/internal/service/handler.go:27; handler getChartDataEndpoint -->|

### Deprecated path aliases

Old paths still served, mapped onto the same handler as their current path by the
server's declarative alias table.

| Method | Deprecated path | Auth | Serves |
|---|---|---|---|
| POST | `/api/_version_/fleet/spec/teams` | user (session or API token) | alias of `/api/_version_/fleet/spec/fleets` <!-- server/service/handler_deprecated_paths.go:20 -->|
| PATCH | `/api/_version_/fleet/teams/{fleet_id:[0-9]+}/secrets` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{fleet_id:[0-9]+}/secrets` <!-- server/service/handler_deprecated_paths.go:24 -->|
| POST | `/api/_version_/fleet/teams` | user (session or API token) | alias of `/api/_version_/fleet/fleets` <!-- server/service/handler_deprecated_paths.go:28 -->|
| GET | `/api/_version_/fleet/teams` | user (session or API token) | alias of `/api/_version_/fleet/fleets` <!-- server/service/handler_deprecated_paths.go:32 -->|
| GET | `/api/_version_/fleet/teams/{id:[0-9]+}` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{id:[0-9]+}` <!-- server/service/handler_deprecated_paths.go:36 -->|
| PATCH | `/api/_version_/fleet/teams/{id:[0-9]+}` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{id:[0-9]+}` <!-- server/service/handler_deprecated_paths.go:40 -->|
| DELETE | `/api/_version_/fleet/teams/{id:[0-9]+}` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{id:[0-9]+}` <!-- server/service/handler_deprecated_paths.go:44 -->|
| POST | `/api/_version_/fleet/teams/{id:[0-9]+}/agent_options` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{id:[0-9]+}/agent_options` <!-- server/service/handler_deprecated_paths.go:48 -->|
| GET | `/api/_version_/fleet/teams/{id:[0-9]+}/users` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{id:[0-9]+}/users` <!-- server/service/handler_deprecated_paths.go:52 -->|
| PATCH | `/api/_version_/fleet/teams/{id:[0-9]+}/users` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{id:[0-9]+}/users` <!-- server/service/handler_deprecated_paths.go:56 -->|
| DELETE | `/api/_version_/fleet/teams/{id:[0-9]+}/users` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{id:[0-9]+}/users` <!-- server/service/handler_deprecated_paths.go:60 -->|
| GET | `/api/_version_/fleet/teams/{id:[0-9]+}/secrets` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{id:[0-9]+}/secrets` <!-- server/service/handler_deprecated_paths.go:64 -->|
| POST | `/api/_version_/fleet/team/{fleet_id}/policies` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{fleet_id}/policies` <!-- server/service/handler_deprecated_paths.go:70 -->|
| POST | `/api/_version_/fleet/teams/{fleet_id}/policies` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{fleet_id}/policies` <!-- server/service/handler_deprecated_paths.go:70 -->|
| GET | `/api/_version_/fleet/team/{fleet_id}/policies` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{fleet_id}/policies` <!-- server/service/handler_deprecated_paths.go:77 -->|
| GET | `/api/_version_/fleet/teams/{fleet_id}/policies` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{fleet_id}/policies` <!-- server/service/handler_deprecated_paths.go:77 -->|
| GET | `/api/_version_/fleet/team/{fleet_id}/policies/count` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{fleet_id}/policies/count` <!-- server/service/handler_deprecated_paths.go:84 -->|
| GET | `/api/_version_/fleet/teams/{fleet_id}/policies/count` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{fleet_id}/policies/count` <!-- server/service/handler_deprecated_paths.go:84 -->|
| GET | `/api/_version_/fleet/team/{fleet_id}/policies/{policy_id}` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{fleet_id}/policies/{policy_id}` <!-- server/service/handler_deprecated_paths.go:91 -->|
| GET | `/api/_version_/fleet/teams/{fleet_id}/policies/{policy_id}` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{fleet_id}/policies/{policy_id}` <!-- server/service/handler_deprecated_paths.go:91 -->|
| POST | `/api/_version_/fleet/team/{fleet_id}/policies/delete` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{fleet_id}/policies/delete` <!-- server/service/handler_deprecated_paths.go:98 -->|
| POST | `/api/_version_/fleet/teams/{fleet_id}/policies/delete` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{fleet_id}/policies/delete` <!-- server/service/handler_deprecated_paths.go:98 -->|
| PATCH | `/api/_version_/fleet/teams/{fleet_id}/policies/{policy_id}` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{fleet_id}/policies/{policy_id}` <!-- server/service/handler_deprecated_paths.go:105 -->|
| GET | `/api/_version_/fleet/queries/{id:[0-9]+}` | user (session or API token) | alias of `/api/_version_/fleet/reports/{id:[0-9]+}` <!-- server/service/handler_deprecated_paths.go:111 -->|
| GET | `/api/_version_/fleet/queries` | user (session or API token) | alias of `/api/_version_/fleet/reports` <!-- server/service/handler_deprecated_paths.go:115 -->|
| GET | `/api/_version_/fleet/queries/{id:[0-9]+}/report` | user (session or API token) | alias of `/api/_version_/fleet/reports/{id:[0-9]+}/report` <!-- server/service/handler_deprecated_paths.go:119 -->|
| POST | `/api/_version_/fleet/queries` | user (session or API token) | alias of `/api/_version_/fleet/reports` <!-- server/service/handler_deprecated_paths.go:123 -->|
| PATCH | `/api/_version_/fleet/queries/{id:[0-9]+}` | user (session or API token) | alias of `/api/_version_/fleet/reports/{id:[0-9]+}` <!-- server/service/handler_deprecated_paths.go:127 -->|
| DELETE | `/api/_version_/fleet/queries/{name}` | user (session or API token) | alias of `/api/_version_/fleet/reports/{name}` <!-- server/service/handler_deprecated_paths.go:131 -->|
| DELETE | `/api/_version_/fleet/queries/id/{id:[0-9]+}` | user (session or API token) | alias of `/api/_version_/fleet/reports/id/{id:[0-9]+}` <!-- server/service/handler_deprecated_paths.go:135 -->|
| POST | `/api/_version_/fleet/queries/delete` | user (session or API token) | alias of `/api/_version_/fleet/reports/delete` <!-- server/service/handler_deprecated_paths.go:139 -->|
| POST | `/api/_version_/fleet/spec/queries` | user (session or API token) | alias of `/api/_version_/fleet/spec/reports` <!-- server/service/handler_deprecated_paths.go:143 -->|
| GET | `/api/_version_/fleet/spec/queries` | user (session or API token) | alias of `/api/_version_/fleet/spec/reports` <!-- server/service/handler_deprecated_paths.go:147 -->|
| GET | `/api/_version_/fleet/spec/queries/{name}` | user (session or API token) | alias of `/api/_version_/fleet/spec/reports/{name}` <!-- server/service/handler_deprecated_paths.go:151 -->|
| GET | `/api/_version_/fleet/hosts/{id:[0-9]+}/queries/{report_id:[0-9]+}` | user (session or API token) | alias of `/api/_version_/fleet/hosts/{id:[0-9]+}/reports/{report_id:[0-9]+}` <!-- server/service/handler_deprecated_paths.go:157 -->|
| POST | `/api/_version_/fleet/queries/{id:[0-9]+}/run` | user (session or API token) | alias of `/api/_version_/fleet/reports/{id:[0-9]+}/run` <!-- server/service/handler_deprecated_paths.go:163 -->|
| GET | `/api/_version_/fleet/queries/run` | user (session or API token) | alias of `/api/_version_/fleet/reports/run` <!-- server/service/handler_deprecated_paths.go:167 -->|
| POST | `/api/_version_/fleet/queries/run` | user (session or API token) | alias of `/api/_version_/fleet/reports/run` <!-- server/service/handler_deprecated_paths.go:171 -->|
| POST | `/api/_version_/fleet/queries/run_by_identifiers` | user (session or API token) | alias of `/api/_version_/fleet/reports/run_by_identifiers` <!-- server/service/handler_deprecated_paths.go:175 -->|
| POST | `/api/_version_/fleet/queries/run_by_names` | user (session or API token) | alias of `/api/_version_/fleet/reports/run_by_names` <!-- server/service/handler_deprecated_paths.go:179 -->|
| GET | `/api/_version_/fleet/team/{fleet_id}/schedule` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{fleet_id}/schedule` <!-- server/service/handler_deprecated_paths.go:185 -->|
| GET | `/api/_version_/fleet/teams/{fleet_id}/schedule` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{fleet_id}/schedule` <!-- server/service/handler_deprecated_paths.go:185 -->|
| POST | `/api/_version_/fleet/team/{fleet_id}/schedule` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{fleet_id}/schedule` <!-- server/service/handler_deprecated_paths.go:192 -->|
| POST | `/api/_version_/fleet/teams/{fleet_id}/schedule` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{fleet_id}/schedule` <!-- server/service/handler_deprecated_paths.go:192 -->|
| PATCH | `/api/_version_/fleet/team/{fleet_id}/schedule/{report_id}` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{fleet_id}/schedule/{report_id}` <!-- server/service/handler_deprecated_paths.go:199 -->|
| PATCH | `/api/_version_/fleet/teams/{fleet_id}/schedule/{report_id}` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{fleet_id}/schedule/{report_id}` <!-- server/service/handler_deprecated_paths.go:199 -->|
| DELETE | `/api/_version_/fleet/team/{fleet_id}/schedule/{report_id}` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{fleet_id}/schedule/{report_id}` <!-- server/service/handler_deprecated_paths.go:206 -->|
| DELETE | `/api/_version_/fleet/teams/{fleet_id}/schedule/{report_id}` | user (session or API token) | alias of `/api/_version_/fleet/fleets/{fleet_id}/schedule/{report_id}` <!-- server/service/handler_deprecated_paths.go:206 -->|
| PATCH | `/api/_version_/fleet/ab_tokens/{id:[0-9]+}/teams` | user (session or API token) | alias of `/api/_version_/fleet/ab_tokens/{id:[0-9]+}/fleets` <!-- server/service/handler_deprecated_paths.go:215 -->|
| PATCH | `/api/_version_/fleet/abm_tokens/{id:[0-9]+}/fleets` | user (session or API token) | alias of `/api/_version_/fleet/ab_tokens/{id:[0-9]+}/fleets` <!-- server/service/handler_deprecated_paths.go:215 -->|
| PATCH | `/api/_version_/fleet/abm_tokens/{id:[0-9]+}/teams` | user (session or API token) | alias of `/api/_version_/fleet/ab_tokens/{id:[0-9]+}/fleets` <!-- server/service/handler_deprecated_paths.go:215 -->|
| PATCH | `/api/_version_/fleet/vpp_tokens/{id}/teams` | user (session or API token) | alias of `/api/_version_/fleet/vpp_tokens/{id}/fleets` <!-- server/service/handler_deprecated_paths.go:223 -->|
| POST | `/api/_version_/fleet/abm_tokens` | user (session or API token) | alias of `/api/_version_/fleet/ab_tokens` <!-- server/service/handler_deprecated_paths.go:229 -->|
| DELETE | `/api/_version_/fleet/abm_tokens/{id:[0-9]+}` | user (session or API token) | alias of `/api/_version_/fleet/ab_tokens/{id:[0-9]+}` <!-- server/service/handler_deprecated_paths.go:233 -->|
| GET | `/api/_version_/fleet/abm_tokens` | user (session or API token) | alias of `/api/_version_/fleet/ab_tokens` <!-- server/service/handler_deprecated_paths.go:237 -->|
| GET | `/api/_version_/fleet/abm_tokens/count` | user (session or API token) | alias of `/api/_version_/fleet/ab_tokens/count` <!-- server/service/handler_deprecated_paths.go:241 -->|
| PATCH | `/api/_version_/fleet/abm_tokens/{id:[0-9]+}/renew` | user (session or API token) | alias of `/api/_version_/fleet/ab_tokens/{id:[0-9]+}/renew` <!-- server/service/handler_deprecated_paths.go:245 -->|
| GET | `/api/_version_/fleet/mdm/apple/abm_public_key` | user (session or API token) | alias of `/api/_version_/fleet/mdm/apple/ab_public_key` <!-- server/service/handler_deprecated_paths.go:249 -->|

### Raw mux routes (MDM protocol and setup)

Registered directly on the router rather than through an endpointer. Each of these
carries its own protocol authentication (a device-management certificate, a SCEP
challenge, or pre-setup state) rather than a Fleet credential.

| Method | Path | Auth |
|---|---|---|
| ANY | `/api/v1/setup` | route-local or protocol <!-- server/service/handler.go:1276; raw: WithSetup; handler srv -->|
| ANY | `/api/setup` | route-local or protocol <!-- server/service/handler.go:1277; raw: WithSetup; handler srv -->|
| ANY | `/mdm/apple/service_discovery/{token}` | route-local or protocol <!-- server/service/handler.go:1399; raw: registerMDMServiceDiscovery; handler otel.WrapHandler -->|
| ANY | `/mdm/apple/service_discovery` | route-local or protocol <!-- server/service/handler.go:1400; raw: registerMDMServiceDiscovery; handler otel.WrapHandler -->|
| ANY | `/.well-known/apple-app-site-association` | route-local or protocol <!-- server/service/handler.go:1416; raw: registerPSSO; handler otel.WrapHandler -->|
| ANY | `/mdm/apple/scep` | route-local or protocol <!-- server/service/handler.go:1457; raw: registerSCEP; handler otel.WrapHandler -->|
| ANY | `/mdm/scep/proxy/` | route-local or protocol <!-- server/service/handler.go:1483; raw: RegisterSCEPProxy; handler scepHandler -->|
| ANY | `/mdm/apple/mdm` | route-local or protocol <!-- server/service/handler.go:1554; raw: registerMDM; handler otel.WrapHandler -->|
