---
title: "API access, versioning, and exposure"
chapter: "Appendices and indexes"
section: "A.8"
sidebar_position: 8
verified_against: Fleet 4.91.0
verified_on: 2026-09-09
verified_source: "drafted against fleet-v4.90.0 (7c428c6e46), with every path in the exposure matrix read from the server's own route registrations rather than from the published reference. The complete route catalog was regenerated against fleet-v4.91.0 (35fc1c0244) with build/gen-api-catalog.py, taking the appendix from 560 registered routes to 562; both additions were read back from server/service/handler.go and their handlers at that tag, and cross-checked against the diff of every route-registering file between the two tags, rather than taken from the generator. Citation ledger at research/section-notes/a.8-notes.md, which records the evidence class of every path and distinguishes the routes Fleet registers from the ones it emits. Corrected 2026-09-08 (overnight campaign step 7, round-2 review blocker 1), verified at fleet-v4.91.0 (35fc1c0244): the catalog claimed none of the server's routes is omitted, which `cmd/fleet/serve.go` disproves with eleven root-mux registrations the generator never scans, among them `/enroll`, the over-the-air enrollment page this appendix's own Android baseline tells you to open. The completeness sentence is now scoped to the API router and names what sits above it. Three auth cells were wrong and were fixed in the generator so they cannot drift back: `/api/osquery/enroll` and its alt path verify an enroll secret in the handler (`server/service/osquery.go:112`), the Android Pub/Sub callback verifies Google's token against the stored asset (`server/mdm/android/service/pubsub.go:80-95`), and the two service-discovery paths and the app-site-association document are genuinely public rather than protocol-authenticated (`server/service/handler.go:1375-1400`, `server/service/apple_psso.go:198-217`). Row counts unchanged at 562 registrations, 496 endpointer, 58 aliases, 8 raw mux. Amended again 2026-09-08 (overnight campaign step 7, round-3 review findings 1 and 5), verified at fleet-v4.91.0 (35fc1c0244): the scope sentence written above named the API router as the catalog's boundary, and that is not the boundary it draws. The raw protocol group is bound on the root mux too (`cmd/fleet/serve.go:893,912` hand `rootMux` to registrars in `server/service/handler.go`), and six root-mux paths registered from the Premium tree were in neither the table nor the exclusion list: `/api/v1/fleet/scim/` and `/api/latest/fleet/scim/` (`ee/server/scim/scim.go:283-284`), `/api/fleet/orbit/host_identity/scep` (`ee/server/service/hostidentity/scep.go:103`), `/api/fleet/conditional_access/scep` (`ee/server/service/condaccess/scep.go:85`) and `/api/fleet/conditional_access/idp/metadata` and `/idp/sso` (`ee/server/service/condaccess/idp.go:156-157`). The paragraph now states the real boundary, which is which files the generator reads, and enumerates all fifteen root-mux paths outside it; those are every `rootMux` mount in `serve.go` and every `mux.Handle` in `ee/` at the tag, checked by grep. Also, the `none` legend promised that a row names any handler-local credential, which the invitation and EULA token rows disprove (`server/service/invites.go:332`, `ee/server/service/mdm.go:461,606` all skip authorization and rely on a path token while reading a bare `none`); the legend now says a bare `none` may still require a route-specific token and that the three named cells were read by hand rather than audited. The generated rows are unchanged. Amended again 2026-09-09 (overnight campaign step 7, round-4 review findings 1 and 2), both in the boundary paragraph round 3 rewrote. The catalog was said to read `server/service/handler.go` and four feature-module files and to list every registration found there in three groups, but the deprecated-alias group comes from a sixth file, `server/service/handler_deprecated_paths.go`, read through a separate constant and a separate pass (`build/gen-api-catalog.py:36` and the alias block below it), which the generated header three lines under the prose already named; the paragraph now attributes each group to its own source and says an alias carries the authentication of the path it aliases, which is what both the generator and Fleet's own `deprecatedPathAliases` comment describe. And the 'where a server private key is configured' qualifier governed three paths but gates four: `cmd/fleet/serve.go:919` opens one branch holding `hostidentity.RegisterSCEP`, `condaccess.RegisterSCEP` and `condaccess.RegisterIdP`, whose `else` arm logs that host identity and conditional access SCEP are both unavailable without the key, while the two SCIM mounts above it are Premium-gated only. The qualifier now covers host identity SCEP too, which matters because this paragraph is the only place in the appendix that path appears. The `none` legend also now says the osquery enroll endpoint serves both of its paths (`WithAltPaths` at `server/service/handler.go:1075`). The generated rows are unchanged"
further_reading:
  - https://fleetdm.com/docs/rest-api/rest-api
  - https://github.com/fleetdm/fleet/blob/fleet-v4.90.0/docs/REST%20API/rest-api.md
  - https://fleetdm.com/guides/what-api-endpoints-to-expose-to-the-public-internet
feature_requests:
  labels: [":product"]
  match: ["API", "endpoint", "REST", "token"]
  exclude: []
---

# API access, versioning, and exposure

![Reference](../_assets/icons/reference-light.svg) Start an API access review by identifying the caller and its credential. Fleet has five classes handled by shared authenticators. Other routes check credentials inside their own handlers or require none, so their requirements need to be checked individually.

Authentication and network reachability answer different questions. The caller model below explains credentials; the capability matrix later identifies the paths each workflow needs.

<a id="what-this-appendix-carries"></a>

## Coverage and related references

![Reference](../_assets/icons/reference-light.svg) This appendix covers callers, authentication, version prefixes, required network paths, and the registered route catalog.

Use Fleet’s REST API reference for endpoint parameters, request bodies, and response fields. It is maintained separately from the code, so compare it with your server’s release when behavior differs.

See [a.4](a.4-roles-and-permissions-matrix.md) for permissions, [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md) for the role model, and [a.5](a.5-interface-index.md) for interface coverage. [6.3](../06-automate-fleet/6.3-use-the-fleet-rest-api.md) provides practical API examples.

## Who calls Fleet, and what they present

![Reference](../_assets/icons/reference-light.svg) Five classes share Fleet credential checks. The last row groups routes with separate authentication behavior, including several registered directly on the root router.

| Class | Who calls it | What it presents |
|---|---|---|
| **User** | A person through the UI, `fleetctl` or a script; or an API-only account, which cannot use the UI, through `fleetctl`, GitOps or a script | A Fleet API token, as `Authorization: Bearer <token>` |
| **Host** | osquery on an enrolled device | The osquery node key issued at enrollment |
| **Orbit** | Orbit on an enrolled device | The Orbit node key, a separate credential from osquery's |
| **Device** | Fleet Desktop, and the **My device** page an end user opens | A per-device token, not a user account |
| **fleetd certificate** | fleetd, fetching a certificate template Fleet has asked it to install and reporting the result | The **Orbit** node key, in an `Authentication` header |
| **Route-local or protocol** | Everything that does not go through Fleet's shared authenticator. Some of these check a credential themselves; **some require none at all** | An enrollment secret, a download token, a SAML response, a query-string token, a device identity certificate, a credential inside a protocol message, or nothing |

> Route-local authentication varies by handler. Google’s Android callback uses a route-specific token; over-the-air enrollment uses an enroll secret; Apple MDM authenticates device identity certificates.
>
> Of the five Windows protocol paths, policy and enrollment use a request token. Management checks a device certificate whose common name contains the device identifier, falling back to a credential in the message. Discovery and terms of use require no credential.
>
> Registration comments describe the middleware layer. A management route labeled unauthenticated there can still reject an untrusted device inside its handler. Inspect that handler before classifying the route as open.

User authentication covers the administrator-facing REST API. Host and Orbit authentication use separate keys, so one agent channel can work while the other fails. [3.1](../03-connect-devices/3.1-enrollment-design-and-host-lifecycle.md) explains those credentials.

The Device class covers more than Fleet Desktop’s ping and policy count. It also serves policies, software inventory, self-service install and uninstall, certificates, setup status, Linux escrow, conditional-access bypass, and MDM migration. Exposing only ping and desktop calls can leave a device page that loads but cannot complete those actions.

The fleetd certificate caller is the agent fetching certificate templates and reporting results with its Orbit node key. Google’s Android event callback uses route-local authentication instead.

## How a user request authenticates

![Reference](../_assets/icons/reference-light.svg) API tokens inherit their account’s role and scope, and activities attribute work to that account. Give each automation its own account to make that attribution useful ([2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md)).

Send it as a bearer token:

```http
Authorization: Bearer <your token>
```

Get a token through **My account → Get API token**, or through the email-and-password login endpoint.

SSO and MFA accounts cannot use email-and-password login for this purpose; obtain their token from the UI profile page. For unattended work, create an API-only account with an explicit role ([2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md)).


<!-- IMAGE-TODO: assets/a.8-api-token-entry-points.webp
     QUESTION: How does a user obtain a token, and which account's permissions does it carry?
     PROMPT: DIAGRAM: Two token-acquisition paths: Signed-in profile page → Get API token; Eligible
     email/password login → Returned token. Mark SSO/MFA accounts as using the profile-page route,
     with the email/password route closed for them. Both paths converge on Authorization: Bearer
     <token> → Fleet user account → Role + scope checks. Use a dedicated API-only account as the
     automation example, not a shared personal identity. This covers user-authenticated API calls
     only; do not apply the bearer-token model to device, osquery, or MDM protocol endpoints.
     TERMINOLOGY: Fleet is the company, product, or server. Host groups are lowercase
     fleet/fleets, including headings and labels. Do not call these groups teams. Preserve
     exact code/API identifiers. These instructions are not text to render.
     DESIGN: Flat vector technical diagram. Fleet is software for managing computers; draw no
     vehicles. Use Inter labels and Roboto Mono identifiers. At 1400 px source width use 48 px
     titles, 36 px body labels, and at least 28 px secondary text; scale proportionally. Check at
     720 px reading width and intended print size. Use a 32 px spacing grid, at least 24 px node
     padding, and consistent corner radii. Center short node names; left-align multiline
     explanations. Never shrink text to fit. Use #F9FAFC background, #192147 headings and primary
     connectors, #515774 text, #8B8FA2 secondary connectors, #C5C7D1 borders, and #D3E8F3 or #E8F1F6
     quiet fills. Use #5CABDF and #C98DEF for named categories, #3AEFC4 for labelled positive
     outcomes, #D66C7B for labelled failures, and #FAA669 for labelled cautions. Tint large panels
     to 20 to 25 percent; full strength is for small marks. Keep text navy or slate, or off-white on
     a navy anchor. Never rely on colour alone. Use one arrowhead shape, consistent stroke weights,
     box-edge termination, and labelled branches and return paths. Keep connectors clear of text. No
     gradients, shadows, decorative icons, logo, watermark, em-dashes, or slogan footer. Render only
     the specified reader-facing labels. Choose orientation to fit the relationship, not a default
     poster. Keep captions outside the artwork. If labels crowd, split the figure before shrinking
     them. Keep editable SVG when the production method supports it.
     NOTE: Proposed 2026-09-08; editorial brief, not technical re-verification. Condense the two
     token-acquisition paragraphs and account/credential distinction. Keep the exact header example,
     endpoint authentication catalog, and automation-account instructions. Keep current prose and
     this TODO until the actual image is reviewed. Then check alt text against the artwork and
     retain an accessible summary plus all required technical qualifications.
     CANDIDATE: ../../research/visual-reviews/appendices/assets/a.8-api-token-entry-points.webp
     Rendered and inspected for the overnight batch; awaiting final joint review.
-->

<!-- IMAGE PENDING. Install reviewed artwork, then activate the image line below.
![Profile-page and eligible password-login paths issue a token belonging to a Fleet account; SSO and MFA users use the profile-page path.](assets/a.8-api-token-entry-points.webp)
-->

<a id="version-prefixes-expand-for-some-routes-and-not-others"></a>

## Version prefixes and literal paths

![Reference](../_assets/icons/reference-light.svg) A route using Fleet’s version placeholder expands to its module’s supported versions and a `latest` alias. A core route such as the host list therefore has three paths:

```
/api/v1/fleet/hosts
/api/2022-04/fleet/hosts
/api/latest/fleet/hosts
```

`latest` is a registered route alias handled directly, without request-time redirection.

> ### Expansion varies by module and route
>
> The core module declares `v1` and `2022-04`; Android declares only `v1`. Android’s versioned routes therefore have `v1` and `latest` forms, with no `2022-04` form.
>
> A route can narrow its module’s versions with start and end bounds. If it ends before the module’s newest version, it has no `latest` alias.
>
> Literal paths do not expand. These include `/api/v1/fleet/sso` and its callback, Android’s event callback, and root-router registrations for Apple MDM, SCEP, Apple service discovery, and the Platform SSO well-known document.

A proxy rule covering only `/api/v1/` misses equivalent calls using another registered prefix. Fleet’s documentation uses both `v1` and `latest`, so account for the paths your callers use.

Match the supported prefixes explicitly: `v1`, `2022-04`, and `latest`. Wildcard semantics differ by proxy and can accept unintended segments. Handle unversioned families separately: `/api/fleet/orbit/*`, `/api/osquery/*`, `/api/fleetd/*`, `/api/mdm/*`, `/api/setup`, and the root paths below.

<a id="paths-outside-api-a-prefix-and-which-base-url-fleet-advertises"></a>

## Root paths, URL prefixes, and advertised hostnames

![Reference](../_assets/icons/reference-light.svg) Fleet serves some protocol paths outside `/api`, including Apple MDM, SCEP, the custom SCEP proxy, and the Platform SSO well-known document.

A proxy exposing only `/api` can leave these workflows unavailable while the UI and REST calls work. Review the required paths when enabling another capability ([2.9](../02-administer-and-deploy-fleet/2.9-mdm-architecture-and-foundations.md)).

A configured URL prefix applies to the entire router, including root paths. Fleet strips it before dispatch. The paths in this appendix are origin-relative and assume no configured prefix.

An Apple MDM server URL changes the base URL Fleet advertises in selected device and profile links. It creates no second listener and does not remove paths from the main origin; both hostnames are expected to reach the same Fleet server.

| Advertised at the Apple URL | Still advertised at the main URL |
|---|---|
| `/enroll`, the over-the-air profile and `ota_enrollment` endpoints, and `/api/mdm/apple/enroll` | `/api/mdm/apple/installer` |
| `/mdm/apple/scep`, `/mdm/apple/mdm`, and the ACME family, inside enrollment profiles | Platform SSO's issuer, key set and app-site-association document |
| MDM setup SSO and account-driven enrollment | The in-house app **manifest** |
| Generated SCEP-proxy URLs, **including the ones written into Windows profiles** | The server URL fleetd is given |

With a configured CDN, Fleet can issue signed URLs for bootstrap packages and in-house app packages. If signing fails or the stored object cannot be confirmed, Fleet logs the failure and falls back to its own URL: the Apple base URL for bootstrap packages, or the main server URL for in-house packages.

Keep those Fleet download paths reachable even when using a CDN, since the fallback can be needed for an individual request. In-house app manifests always use the main Fleet URL, so a manifest and its package may use different origins.

For ingress planning, check the hostname actually advertised to the device. Each Fleet hostname you advertise must reach the same deployment.

## What has to be reachable, by capability

![Reference](../_assets/icons/reference-light.svg) Use this matrix to select the inbound paths required by each enabled capability.

> ### Matrix scope
>
> This matrix covers paths needed by external callers for the named capabilities: devices, end users, administrators, and third parties.
>
> Operator endpoints for health, version, metrics, and debug are covered in [7.4](../07-operate-fleet/7.4-observe-progress-and-service-health.md). Metrics is mounted only when credentials are configured or its basic authentication is explicitly disabled. General UI and asset routes are included here only when a listed workflow depends on them.
>
> An absent capability has not been assessed. For those listed, the matrix follows the URL Fleet emits to a device or external caller. A route may be registered under several prefixes while the workflow uses only one, sometimes a deprecated form. Opening that emitted path is sufficient for that flow; opening its aliases provides broader coverage.

SCIM and custom SCEP proxying require Premium. Okta conditional access additionally requires the server private key. Apple’s root protocol services also require that key and are not mounted without it.

**Baseline, for agents on devices that leave the network:**

| Path | For |
|---|---|
| `/api/osquery/*`, `/api/v1/osquery/*` | osquery check-in and log submission |
| `/api/fleet/orbit/*` | Orbit, including scripts and software |
| `/api/{v1,2022-04,latest}/fleet/device/*` | **The whole Device class.** Fleet Desktop's ping and counts, and everything an end user does on their own device page |

For off-network `fleetctl` and API clients, add `/api/{v1,2022-04,latest}/fleet/*`. Initial setup uses `/api/setup` and `/api/v1/setup`; it has no `2022-04` or `latest` variant.

Fleet account SSO uses the literal paths `/api/v1/fleet/sso` and `/api/v1/fleet/sso/callback`. Other API-version prefixes do not apply, although a configured URL prefix still does.

**SCIM provisioning** is prefix-mounted at `/api/v1/fleet/scim/` and `/api/latest/fleet/scim/`, and those two are what your identity provider needs ([2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md)). One SCIM path is outside that mount: the details endpoint is an ordinary core route and therefore also exists at `2022-04`. SCIM is Premium.

**For Apple device management**, add `/mdm/apple/scep` and `/mdm/apple/mdm`, both outside `/api`, plus `/api/mdm/apple/enroll` for automatic enrollment. Where hardware attestation is enabled, Fleet puts its own ACME directory URL into the enrollment profile, so add `/api/mdm/acme/*`. Where an installer is served to devices, that is `/api/mdm/apple/installer`.

**Setup-experience features each add their own:**

| Feature | What Fleet actually emits |
|---|---|
| Identity-provider authentication during setup | Three separate things, all needed: the browser starts at `/api/latest/fleet/mdm/sso`, the identity provider is given `/api/v1/fleet/mdm/sso/callback`, and the flow returns the user to the frontend route `/mdm/sso/callback`, which `/assets/*` serves |
| End user licence agreement | **`/api/latest/fleet/mdm/setup/eula/{token}`**, the deprecated form. The replacement `/api/*/fleet/setup_experience/eula/{token}` is registered and is not what this flow loads at the tag |
| Bootstrap package | **`/api/latest/fleet/mdm/bootstrap`**, also the deprecated form, hard-coded into the URL Fleet builds, **and used only when a CDN URL is not** (see above). Expose it either way |
| Fleet's Platform SSO extension | `/api/mdm/apple/psso/*` and `/.well-known/apple-app-site-association` |

Apple enrollment by link uses `/enroll`, `/api/v1/fleet/enrollment_profiles/ota`, then `/api/v1/fleet/ota_enrollment`. Fleet emits `v1` at both transitions, and all three paths must be reachable. This covers Macs using **Add hosts** as well as iPhones and iPads ([3.2](../03-connect-devices/3.2-enroll-macos-devices.md), [3.5](../03-connect-devices/3.5-enroll-ios-and-ipados-devices.md)).

For iOS/iPadOS in-house apps, expose both `/api/latest/fleet/software/titles/*/in_house_app/{token}` and `/api/latest/fleet/software/titles/*/in_house_app/manifest/{token}`. The manifest directs installation and remains on Fleet; a signed CDN URL can replace only the package download.

Account-driven user enrollment requires these separately registered paths:

| Path | For |
|---|---|
| `/mdm/apple/service_discovery/{token}` | The discovery document the device fetches first. A tokenless form is registered and deprecated |
| `/api/mdm/apple/account_driven_enroll/{token}` | The enrollment itself. A tokenless form is registered and deprecated |
| `/mdm/apple/account_driven_enroll/sso/{token}` | Its identity-provider hop. A tokenless form is registered and deprecated |
| The MDM SSO callback flow above | Shared with the setup-experience path, and needed here too |

**For Windows device management**, add the four Microsoft protocol paths under `/api/mdm/microsoft/`, which are `management`, `discovery`, `policy` and `enroll`, plus `/api/mdm/microsoft/tos` for automatic enrollment. [2.11](../02-administer-and-deploy-fleet/2.11-configure-windows-management.md) covers why exposing some but not all of these fails partway rather than cleanly.

Android uses `/enroll`, `/api/v1/fleet/android_enterprise/enrollment_token`, and `/api/v1/fleet/android_enterprise/connect/{token}` for enrollment and enablement. The module supports `v1` and `latest`, while the generated enrollment and signup links use `v1`. Google sends device events to the literal `/api/v1/fleet/android_enterprise/pubsub` callback, which requires a publicly reachable server URL ([2.12](../02-administer-and-deploy-fleet/2.12-bind-android-enterprise.md)).

**For delivering your own certificates to devices**, rather than Fleet's, add `/mdm/scep/proxy/*`, which sits outside `/api`. Where fleetd fetches and reports on those certificates, add `/api/fleetd/certificates/*`. The integrations these deliver from are created and managed through the `/api/*/fleet/certificate_authorities` endpoints, which are the API behind [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md); the per-authority `request_certificate` route issues from an existing authority and is accepted only for Hydrant and custom EST authorities.

Google Calendar calls `/api/v1/fleet/calendar/webhook/{event_uuid}`. Although all three prefixes are registered, Fleet supplies Google with the `v1` address.

**For Okta conditional access**, add `/api/fleet/conditional_access/scep`, `/api/fleet/conditional_access/idp/metadata` and `/api/fleet/conditional_access/idp/sso`. None of the three is versioned. **They do not all belong to the same origin**: Fleet builds the SSO URL against the conditional-access hostname, which is expected to be reached over mutual TLS, while metadata and SCEP sit on Fleet's ordinary origin. It is Premium, and requires the server private key.

## Data inventory and trust boundaries

![Reference](../_assets/icons/reference-light.svg) A data review needs to establish collection source, transport, storage, retention, external recipients, and controlling settings. Use this table to find the chapter covering each data class.

MySQL holds configuration, hosts, policies, activities, and escrowed credentials, including encrypted Apple certificate-authority material. File or object storage holds installers, icons, and bootstrap packages. Redis handles transient coordination such as live-report results and pending notifications. Other sensitive material remains in deployment configuration, including the server private key and Windows enrollment identity and key. [7.2](../07-operate-fleet/7.2-back-up-and-restore-service-state.md) covers this storage split and the three disk-encryption escrow chains; the data-specific chapters cover retention.

| Data class | Held in | Governed by |
|---|---|---|
| Host inventory: hardware, OS, network, local accounts, installed software | MySQL | [4.1](../04-know-your-devices/4.1-understand-hosts-vitals-and-inventory.md) for collection; [4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md) for software and vulnerabilities |
| Report and live-report results | MySQL, with live results transient in Redis | [4.2](../04-know-your-devices/4.2-run-queries-and-reports.md) |
| Disk-encryption recovery keys and macOS Recovery Lock | Encrypted at rest, by three separate escrow chains | [5.8](../05-manage-devices/5.8-enforce-disk-encryption-and-manage-recovery-credentials.md); storage and chains in [7.2](../07-operate-fleet/7.2-back-up-and-restore-service-state.md) |
| Configuration profiles, their variables, and secret variables | MySQL; secret values can be sourced from a secret manager | [5.2](../05-manage-devices/5.2-manage-configuration-profiles-and-declarative-settings.md) |
| Apple, Windows, and Android MDM credentials and tokens | MySQL, Apple material encrypted; server private key and Windows enrollment identity in configuration | [2.9](../02-administer-and-deploy-fleet/2.9-mdm-architecture-and-foundations.md) to [2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md); lifecycle in [7.6](../07-operate-fleet/7.6-maintain-credentials-certificates-and-access.md) |
| Activity and audit records, including the actor's identity | MySQL | [1.5](../01-foundations/1.5-audit-and-activity.md); delivery onward in [2.8](../02-administer-and-deploy-fleet/2.8-activity-audit-logs-and-log-delivery.md) |
| Human and service accounts: names, emails, password hashes, sessions, API tokens | MySQL | [2.6](../02-administer-and-deploy-fleet/2.6-user-accounts-roles-and-service-identities.md) |
| Server private key and other key material | Configuration, outside the database | [1.6](../01-foundations/1.6-the-fleet-server.md); preservation in [7.2](../07-operate-fleet/7.2-back-up-and-restore-service-state.md) |

Configured log destinations receive activity, audit, and osquery data ([2.8](../02-administer-and-deploy-fleet/2.8-activity-audit-logs-and-log-delivery.md)). Integrations authenticate to Apple ([2.9](../02-administer-and-deploy-fleet/2.9-mdm-architecture-and-foundations.md), [2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md)), Google ([2.12](../02-administer-and-deploy-fleet/2.12-bind-android-enterprise.md)), certificate authorities ([2.13](../02-administer-and-deploy-fleet/2.13-connect-certificate-authorities.md)), and identity providers ([2.5](../02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md)) using stored credentials or derived tokens. Fleet’s encryption private key remains on the server.

An enabled MCP server shares selected host, software, vulnerability, and policy data with the connected assistant ([6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md), [A.11](a.11-mcp-tool-reference.md)). Webhooks and integrations send their configured payloads, and support cases include the diagnostics you attach ([8.13](../08-troubleshooting/8.13-escalation.md)).

Fleet also fetches external data through outbound requests: vulnerability feeds ([4.4](../04-know-your-devices/4.4-understand-software-and-vulnerabilities.md)), maintained-app manifests ([5.4](../05-manage-devices/5.4-manage-software-and-applications.md)), and Apple VPP assignments and catalogs ([2.10](../02-administer-and-deploy-fleet/2.10-apple-mdm-configuration.md)). Android device and enterprise events arrive through Google’s Pub/Sub callback ([2.12](../02-administer-and-deploy-fleet/2.12-bind-android-enterprise.md)). The exposure matrix identifies the inbound paths.

## API conventions

![Reference](../_assets/icons/reference-light.svg) List endpoints share a convention: `page` for the zero-based page number, `per_page` for its size, `order_key` for the column to sort by, and `order_direction` for the direction.

```
GET /api/v1/fleet/activities?page=0&per_page=10&order_key=created_at&order_direction=desc
```

An endpoint's valid `order_key` values are its own, and Fleet's reference documents them per endpoint. [6.3](../06-automate-fleet/6.3-use-the-fleet-rest-api.md) covers paginating a large result set in practice.

## The shared response and error contract

![Reference](../_assets/icons/reference-light.svg) The shared JSON response format below was verified at Fleet 4.90.0. Use it alongside the catalog’s method, path, and authentication entries and the REST reference’s endpoint-specific fields.

Successful JSON calls return a named resource field, such as `hosts`, `activities`, or `api_endpoints`, inside an object. Writes return the created or updated resource in the same style. Responses default to `200 OK` unless the handler specifies another success status. An operation with no result body returns `204 No Content`.

List responses include paging information in `meta.has_next_results` and `meta.has_previous_results`; some also include a top-level `count`. Use the paging fields with `page` and `per_page` to retrieve a complete result set ([6.3](../06-automate-fleet/6.3-use-the-fleet-rest-api.md#page-filter-and-order-complete-result-sets)).

After a field rename, responses can include both current and deprecated keys. Read the expected key without assuming it is the only spelling present. [6.3](../06-automate-fleet/6.3-use-the-fleet-rest-api.md#renamed-fields-in-request-and-response-bodies) explains how this affects writes.

The error envelope contains a `message` and an `errors` array with `name` and `reason` entries. Some errors include a `uuid` that connects the response to a server log entry and can be included in a support case.

| Failure | Status | `message` |
|---|---|---|
| Validation failed | 422, or the handler's own status | `Validation Failed` |
| Caller lacks permission | 403 | `Permission Denied` |
| Resource not found | 404 | `Resource Not Found` |
| Resource already exists | 409 | `Resource Already Exists` |
| Conflicting state | 409 | `Conflict` |
| Malformed request | 400 | `Bad request` |

Authentication failures use `401`, while licence restrictions use `402`. These checks can occur outside the handler’s normal error path. [6.3](../06-automate-fleet/6.3-use-the-fleet-rest-api.md#handle-errors-limits-and-ambiguous-writes) explains how to handle these statuses and route-specific exceptions.

<a id="where-the-rest-lives"></a>

## Endpoint-specific documentation

![Reference](../_assets/icons/reference-light.svg) Fleet’s REST reference at `fleetdm.com/docs/rest-api/rest-api` documents request bodies, response fields, and parameters. That page follows the current release; the 4.90.0 copy linked under further reading provides the baseline used here. Compare versions when a documented field differs from your deployment. Contributor-facing endpoints are documented separately in Fleet’s repository.

Which actions each role may perform is [a.4](a.4-roles-and-permissions-matrix.md). Which surface can perform one at all is [a.5](a.5-interface-index.md), which carries every action against all four interfaces.

## Version notes

![Reference](../_assets/icons/reference-light.svg) Verified against Fleet 4.91.0. The core module declares `v1` and `2022-04`; other modules declare their own version sets. Eligible routes also receive a `latest` alias.

The catalog has 562 routes, two added since 4.90.0 and none removed. `POST /api/_version_/fleet/hosts/release_ab` releases host IDs from Apple Business, calling Apple’s disown operation once per affected ABM token. It requires a user token, global or fleet administrator access, and Premium, with a limit of 32,000 host IDs per request. Per-host statuses let eligible devices proceed while ineligible ones return their reasons.

`POST /api/fleet/orbit/managed_local_account` lets fleetd escrow a generated Windows local-account password or report a creation failure. It uses the Orbit node key, requires Windows MDM configuration, and rejects hosts not enrolled in Windows MDM.

The exposure matrix, route catalog, and API-only endpoint restriction list serve different purposes. The restriction list is consulted only for API-only accounts with a non-empty list, and only within the endpoint middleware that enforces it. Debug routes and live-query result streams use separate authentication and bypass that restriction; their own checks still apply ([a.4](a.4-roles-and-permissions-matrix.md)).

Fleet validates that restriction-catalog entries have registered routes, but that does not establish that every route appears in the list. Backward-compatible aliases can be absent. Treat the list as the accepted vocabulary for endpoint restrictions, rather than a count of all routes.

Recheck required paths when enabling a feature or upgrading Fleet. New capabilities and changed emitted URLs can alter ingress requirements.

## Retrieving the endpoint catalog

![How-to](../_assets/icons/howto-light.svg) Retrieve Fleet’s endpoint catalog to build an API-only account’s restriction list from accepted method-and-path pairs:

```
GET /api/v1/fleet/rest_api
```

The request requires a user session or API token with global or fleet administrator access and Premium. Free returns a missing-licence error; other roles are refused. Use the API directly, since there is no native `fleetctl` command, GitOps form, or UI control for this read.

The response is a JSON object with one field, `api_endpoints`, an array whose entries each carry the `method` and `path` an allowlist entry needs, alongside a `display_name` and a `deprecated` flag:

```json
{
  "api_endpoints": [
    { "method": "GET", "path": "/api/v1/fleet/hosts", "display_name": "List hosts", "deprecated": false }
  ]
}
```

Copy each required `method` and `path` pair literally, including its `/api/v1/fleet` prefix, into the API-only user’s restriction list. [6.6](../06-automate-fleet/6.6-connect-fleet-to-an-ai-assistant.md#two-starting-allowlist-profiles) gives examples. Within the middleware enforcing restrictions, the route must appear in both this catalog and the user’s list. A hand-written pair absent from the catalog cannot match.

## The complete route catalog

![Reference](../_assets/icons/reference-light.svg) This catalog was generated from route registrations at the pinned release, alongside the [configuration catalog](a.3-configuration-model-and-precedence.md#the-complete-configuration-key-catalog). It records registered paths independently of the hand-maintained REST reference. The generation scope is described below.

The exposure matrix identifies paths required by a workflow; the catalog lists registered API paths and their authentication classes. Device-management protocol routes are grouped last because they register directly on the router and generally use protocol-specific authentication.

`none` in the Auth column means there is no router-level Fleet credential check. The handler may still require a token, as EULA, invitation, and installer-download links do. Selected rows were inspected manually to identify handler-local authentication, including the live-query websocket, both osquery enrollment paths, and Android Pub/Sub. The remaining `none` rows have not all received that review; inspect the handler before treating one as unauthenticated.

The generator reads six files. `server/service/handler.go` and four feature-module handler files provide endpoint and raw protocol registrations. `server/service/handler_deprecated_paths.go` maps deprecated aliases to current handlers, whose authentication the aliases share. Root paths such as `/mdm/apple/scep`, `/mdm/apple/mdm`, and `/mdm/scep/proxy/` appear because the included handler file registers them.

Fifteen paths registered elsewhere are outside the generated table. Nine come from `cmd/fleet/serve.go`: `/healthz`, `/version`, `/metrics`, `/debug/`, `/`, `/assets/`, two literal `scim/details` shims, and `/enroll`.

Six come from the Premium tree: `/api/v1/fleet/scim/`, `/api/latest/fleet/scim/`, `/api/fleet/orbit/host_identity/scep`, `/api/fleet/conditional_access/scep`, `/api/fleet/conditional_access/idp/metadata`, and `/api/fleet/conditional_access/idp/sso`. The last four are mounted only with the server private key configured; otherwise startup logs explain their absence. The exposure matrix covers the SCIM and conditional-access paths. Add the host-identity SCEP path when using host identity certificates.

`_version_` represents the prefixes described in [Version prefixes and literal paths](#version-prefixes-and-literal-paths). HTML comments retain each handler and source location for editors.

<!-- To regenerate: python3 build/gen-api-catalog.py --out FILE  (FLEET_SRC overrides the source checkout). Pinned to fleet-v4.91.0 (35fc1c0244). -->
<!-- GENERATED by build/gen-api-catalog.py; do not edit by hand.
     source: server/service/handler.go, server/mdm/android/service/handler.go, server/activity/internal/service/handler.go, server/mdm/acme/internal/service/handler.go, server/chart/internal/service/handler.go + handler_deprecated_paths.go @ 35fc1c0244907c157a64d05d4ec291c0a3a20e32
     registrations found: 562; routes parsed: 562 (496 endpointer incl. alt paths, 58 deprecated aliases, 8 raw mux); unparsed: 0 -->

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
| POST | `/api/_version_/fleet/hosts/release_ab` | user (session or API token) <!-- server/service/handler.go:599; handler releaseABDevicesEndpoint -->|
| POST | `/api/_version_/fleet/autofill/policy` | user (session or API token) <!-- server/service/handler.go:602; handler autofillPoliciesEndpoint -->|
| PUT | `/api/_version_/fleet/spec/secret_variables` | user (session or API token) <!-- server/service/handler.go:605; handler createSecretVariablesEndpoint -->|
| POST | `/api/_version_/fleet/custom_variables` | user (session or API token) <!-- server/service/handler.go:606; handler createSecretVariableEndpoint -->|
| GET | `/api/_version_/fleet/custom_variables` | user (session or API token) <!-- server/service/handler.go:607; handler listSecretVariablesEndpoint -->|
| DELETE | `/api/_version_/fleet/custom_variables/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:608; handler deleteSecretVariableEndpoint -->|
| GET | `/api/_version_/fleet/custom_host_vitals` | user (session or API token) <!-- server/service/handler.go:611; handler listCustomHostVitalsEndpoint -->|
| POST | `/api/_version_/fleet/custom_host_vitals` | user (session or API token) <!-- server/service/handler.go:612; handler createCustomHostVitalEndpoint -->|
| PATCH | `/api/_version_/fleet/custom_host_vitals/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:613; handler updateCustomHostVitalEndpoint -->|
| DELETE | `/api/_version_/fleet/custom_host_vitals/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:614; handler deleteCustomHostVitalEndpoint -->|
| PUT | `/api/_version_/fleet/hosts/{host_id:[0-9]+}/custom_host_vitals/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:615; handler setHostCustomHostVitalValueEndpoint -->|
| PUT | `/api/_version_/fleet/spec/custom_host_vitals` | user (session or API token) <!-- server/service/handler.go:616; handler upsertCustomHostVitalsEndpoint -->|
| GET | `/api/_version_/fleet/rest_api` | user (session or API token) <!-- server/service/handler.go:619; handler listAPIEndpointsEndpoint -->|
| GET | `/api/_version_/fleet/scim/details` | user (session or API token) <!-- server/service/handler.go:622; handler getScimDetailsEndpoint -->|
| POST | `/api/_version_/fleet/conditional-access/microsoft` | user (session or API token) <!-- server/service/handler.go:625; handler conditionalAccessMicrosoftCreateEndpoint -->|
| POST | `/api/_version_/fleet/conditional-access/microsoft/confirm` | user (session or API token) <!-- server/service/handler.go:626; handler conditionalAccessMicrosoftConfirmEndpoint -->|
| DELETE | `/api/_version_/fleet/conditional-access/microsoft` | user (session or API token) <!-- server/service/handler.go:627; handler conditionalAccessMicrosoftDeleteEndpoint -->|
| GET | `/api/_version_/fleet/conditional_access/idp/signing_cert` | user (session or API token) <!-- server/service/handler.go:630; handler conditionalAccessGetIdPSigningCertEndpoint -->|
| GET | `/api/_version_/fleet/conditional_access/idp/apple/profile` | user (session or API token) <!-- server/service/handler.go:631; handler conditionalAccessGetIdPAppleProfileEndpoint -->|
| PATCH | `/api/_version_/fleet/mdm/apple/setup` | user (session or API token) <!-- server/service/handler.go:635; handler updateMDMAppleSetupEndpoint -->|
| PATCH | `/api/_version_/fleet/setup_experience` | user (session or API token) <!-- server/service/handler.go:636; handler updateMDMAppleSetupEndpoint -->|
| POST | `/api/_version_/fleet/mdm/apple/enqueue` | user (session or API token) <!-- server/service/handler.go:650; handler enqueueMDMAppleCommandEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/commandresults` | user (session or API token) <!-- server/service/handler.go:654; handler getMDMAppleCommandResultsEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/commands` | user (session or API token) <!-- server/service/handler.go:658; handler listMDMAppleCommandsEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/profiles/{profile_id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:662; handler getMDMAppleConfigProfileEndpoint -->|
| DELETE | `/api/_version_/fleet/mdm/apple/profiles/{profile_id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:663; handler deleteMDMAppleConfigProfileEndpoint -->|
| POST | `/api/_version_/fleet/mdm/apple/profiles` | user (session or API token) <!-- server/service/handler.go:664; handler newMDMAppleConfigProfileEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/profiles` | user (session or API token) <!-- server/service/handler.go:665; handler listMDMAppleConfigProfilesEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/filevault/summary` | user (session or API token) <!-- server/service/handler.go:670; handler getMdmAppleFileVaultSummaryEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/profiles/summary` | user (session or API token) <!-- server/service/handler.go:675; handler getMDMAppleProfilesSummaryEndpoint -->|
| POST | `/api/_version_/fleet/mdm/apple/enrollment_profile` | user (session or API token) <!-- server/service/handler.go:679; handler createMDMAppleSetupAssistantEndpoint -->|
| POST | `/api/_version_/fleet/enrollment_profiles/automatic` | user (session or API token) <!-- server/service/handler.go:680; handler createMDMAppleSetupAssistantEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/enrollment_profile` | user (session or API token) <!-- server/service/handler.go:684; handler getMDMAppleSetupAssistantEndpoint -->|
| GET | `/api/_version_/fleet/enrollment_profiles/automatic` | user (session or API token) <!-- server/service/handler.go:685; handler getMDMAppleSetupAssistantEndpoint -->|
| GET | `/api/_version_/fleet/enrollment_profiles/automatic/default` | user (session or API token) <!-- server/service/handler.go:686; handler getDefaultMDMAppleSetupAssistantProfileEndpoint -->|
| DELETE | `/api/_version_/fleet/mdm/apple/enrollment_profile` | user (session or API token) <!-- server/service/handler.go:690; handler deleteMDMAppleSetupAssistantEndpoint -->|
| DELETE | `/api/_version_/fleet/enrollment_profiles/automatic` | user (session or API token) <!-- server/service/handler.go:691; handler deleteMDMAppleSetupAssistantEndpoint -->|
| POST | `/api/_version_/fleet/mdm/apple/installers` | user (session or API token) <!-- server/service/handler.go:696; handler uploadAppleInstallerEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/installers/{installer_id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:697; handler getAppleInstallerEndpoint -->|
| DELETE | `/api/_version_/fleet/mdm/apple/installers/{installer_id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:698; handler deleteAppleInstallerEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/installers` | user (session or API token) <!-- server/service/handler.go:699; handler listMDMAppleInstallersEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/devices` | user (session or API token) <!-- server/service/handler.go:700; handler listMDMAppleDevicesEndpoint -->|
| GET | `/api/_version_/fleet/mdm/manual_enrollment_profile` | user (session or API token) <!-- server/service/handler.go:705; handler getManualEnrollmentProfileEndpoint -->|
| GET | `/api/_version_/fleet/enrollment_profiles/manual` | user (session or API token) <!-- server/service/handler.go:706; handler getManualEnrollmentProfileEndpoint -->|
| POST | `/api/_version_/fleet/mdm/bootstrap` | user (session or API token) <!-- server/service/handler.go:713; handler uploadBootstrapPackageEndpoint -->|
| POST | `/api/_version_/fleet/bootstrap` | user (session or API token) <!-- server/service/handler.go:714; handler uploadBootstrapPackageEndpoint -->|
| GET | `/api/_version_/fleet/mdm/bootstrap/{fleet_id:[0-9]+}/metadata` | user (session or API token) <!-- server/service/handler.go:718; handler bootstrapPackageMetadataEndpoint -->|
| GET | `/api/_version_/fleet/bootstrap/{fleet_id:[0-9]+}/metadata` | user (session or API token) <!-- server/service/handler.go:719; handler bootstrapPackageMetadataEndpoint -->|
| DELETE | `/api/_version_/fleet/mdm/bootstrap/{fleet_id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:723; handler deleteBootstrapPackageEndpoint -->|
| DELETE | `/api/_version_/fleet/bootstrap/{fleet_id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:724; handler deleteBootstrapPackageEndpoint -->|
| GET | `/api/_version_/fleet/mdm/bootstrap/summary` | user (session or API token) <!-- server/service/handler.go:728; handler getMDMAppleBootstrapPackageSummaryEndpoint -->|
| GET | `/api/_version_/fleet/bootstrap/summary` | user (session or API token) <!-- server/service/handler.go:729; handler getMDMAppleBootstrapPackageSummaryEndpoint -->|
| POST | `/api/_version_/fleet/mdm/apple/bootstrap` | user (session or API token) <!-- server/service/handler.go:733; handler uploadBootstrapPackageEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/bootstrap/{fleet_id:[0-9]+}/metadata` | user (session or API token) <!-- server/service/handler.go:735; handler bootstrapPackageMetadataEndpoint -->|
| DELETE | `/api/_version_/fleet/mdm/apple/bootstrap/{fleet_id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:737; handler deleteBootstrapPackageEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/bootstrap/summary` | user (session or API token) <!-- server/service/handler.go:739; handler getMDMAppleBootstrapPackageSummaryEndpoint -->|
| POST | `/api/_version_/fleet/mdm/hosts/{id:[0-9]+}/lock` | user (session or API token) <!-- server/service/handler.go:745; handler deviceLockEndpoint -->|
| POST | `/api/_version_/fleet/mdm/hosts/{id:[0-9]+}/wipe` | user (session or API token) <!-- server/service/handler.go:746; handler deviceWipeEndpoint -->|
| GET | `/api/_version_/fleet/mdm/hosts/{id:[0-9]+}/profiles` | user (session or API token) <!-- server/service/handler.go:750; handler getHostProfilesEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple` | user (session or API token) <!-- server/service/handler.go:754; handler getAppleMDMEndpoint -->|
| GET | `/api/_version_/fleet/apns` | user (session or API token) <!-- server/service/handler.go:755; handler getAppleMDMEndpoint -->|
| POST | `/api/_version_/fleet/mdm/setup/eula` | user (session or API token) <!-- server/service/handler.go:761; handler createMDMEULAEndpoint -->|
| POST | `/api/_version_/fleet/setup_experience/eula` | user (session or API token) <!-- server/service/handler.go:762; handler createMDMEULAEndpoint -->|
| GET | `/api/_version_/fleet/mdm/setup/eula/metadata` | user (session or API token) <!-- server/service/handler.go:766; handler getMDMEULAMetadataEndpoint -->|
| GET | `/api/_version_/fleet/setup_experience/eula/metadata` | user (session or API token) <!-- server/service/handler.go:767; handler getMDMEULAMetadataEndpoint -->|
| DELETE | `/api/_version_/fleet/mdm/setup/eula/{token}` | user (session or API token) <!-- server/service/handler.go:771; handler deleteMDMEULAEndpoint -->|
| DELETE | `/api/_version_/fleet/setup_experience/eula/{token}` | user (session or API token) <!-- server/service/handler.go:772; handler deleteMDMEULAEndpoint -->|
| POST | `/api/_version_/fleet/mdm/apple/setup/eula` | user (session or API token) <!-- server/service/handler.go:775; handler createMDMEULAEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/setup/eula/metadata` | user (session or API token) <!-- server/service/handler.go:777; handler getMDMEULAMetadataEndpoint -->|
| DELETE | `/api/_version_/fleet/mdm/apple/setup/eula/{token}` | user (session or API token) <!-- server/service/handler.go:779; handler deleteMDMEULAEndpoint -->|
| POST | `/api/_version_/fleet/mdm/apple/profiles/preassign` | user (session or API token) <!-- server/service/handler.go:781; handler preassignMDMAppleProfileEndpoint -->|
| POST | `/api/_version_/fleet/mdm/apple/profiles/match` | user (session or API token) <!-- server/service/handler.go:782; handler matchMDMApplePreassignmentEndpoint -->|
| GET | `/api/_version_/fleet/assets` | user (session or API token) <!-- server/service/handler.go:785; handler listAppleDDMAssetsEndpoint -->|
| GET | `/api/_version_/fleet/assets/{asset_uuid}` | user (session or API token) <!-- server/service/handler.go:786; handler getAppleDDMAssetEndpoint -->|
| POST | `/api/_version_/fleet/assets` | user (session or API token) <!-- server/service/handler.go:787; handler createAppleDDMAssetEndpoint -->|
| DELETE | `/api/_version_/fleet/assets/{asset_uuid}` | user (session or API token) <!-- server/service/handler.go:788; handler deleteAppleDDMAssetEndpoint -->|
| POST | `/api/_version_/fleet/assets/batch` | user (session or API token) <!-- server/service/handler.go:789; handler batchSetAppleDDMAssetsEndpoint -->|
| GET | `/api/_version_/fleet/hosts/{id:[0-9]+}/configuration_profiles` | user (session or API token) <!-- server/service/handler.go:793; handler getHostProfilesEndpoint -->|
| POST | `/api/_version_/fleet/mdm/commands/run` | user (session or API token) <!-- server/service/handler.go:797; handler runMDMCommandEndpoint -->|
| POST | `/api/_version_/fleet/commands/run` | user (session or API token) <!-- server/service/handler.go:798; handler runMDMCommandEndpoint -->|
| GET | `/api/_version_/fleet/mdm/commandresults` | user (session or API token) <!-- server/service/handler.go:802; handler getMDMCommandResultsEndpoint -->|
| GET | `/api/_version_/fleet/commands/results` | user (session or API token) <!-- server/service/handler.go:803; handler getMDMCommandResultsEndpoint -->|
| GET | `/api/_version_/fleet/mdm/commands` | user (session or API token) <!-- server/service/handler.go:807; handler listMDMCommandsEndpoint -->|
| GET | `/api/_version_/fleet/commands` | user (session or API token) <!-- server/service/handler.go:808; handler listMDMCommandsEndpoint -->|
| PATCH | `/api/_version_/fleet/mdm/hosts/{id:[0-9]+}/unenroll` | user (session or API token) <!-- server/service/handler.go:812; handler mdmUnenrollEndpoint -->|
| DELETE | `/api/_version_/fleet/hosts/{id:[0-9]+}/mdm` | user (session or API token) <!-- server/service/handler.go:813; handler mdmUnenrollEndpoint -->|
| GET | `/api/_version_/fleet/mdm/disk_encryption/summary` | user (session or API token) <!-- server/service/handler.go:817; handler getMDMDiskEncryptionSummaryEndpoint -->|
| GET | `/api/_version_/fleet/disk_encryption` | user (session or API token) <!-- server/service/handler.go:818; handler getMDMDiskEncryptionSummaryEndpoint -->|
| GET | `/api/_version_/fleet/mdm/hosts/{id:[0-9]+}/encryption_key` | user (session or API token) <!-- server/service/handler.go:822; handler getHostEncryptionKey -->|
| GET | `/api/_version_/fleet/hosts/{id:[0-9]+}/encryption_key` | user (session or API token) <!-- server/service/handler.go:823; handler getHostEncryptionKey -->|
| GET | `/api/_version_/fleet/mdm/profiles/summary` | user (session or API token) <!-- server/service/handler.go:827; handler getMDMProfilesSummaryEndpoint -->|
| GET | `/api/_version_/fleet/configuration_profiles/summary` | user (session or API token) <!-- server/service/handler.go:828; handler getMDMProfilesSummaryEndpoint -->|
| GET | `/api/_version_/fleet/mdm/profiles/{profile_uuid}` | user (session or API token) <!-- server/service/handler.go:832; handler getMDMConfigProfileEndpoint -->|
| GET | `/api/_version_/fleet/configuration_profiles/{profile_uuid}` | user (session or API token) <!-- server/service/handler.go:833; handler getMDMConfigProfileEndpoint -->|
| DELETE | `/api/_version_/fleet/mdm/profiles/{profile_uuid}` | user (session or API token) <!-- server/service/handler.go:837; handler deleteMDMConfigProfileEndpoint -->|
| DELETE | `/api/_version_/fleet/configuration_profiles/{profile_uuid}` | user (session or API token) <!-- server/service/handler.go:838; handler deleteMDMConfigProfileEndpoint -->|
| GET | `/api/_version_/fleet/mdm/profiles` | user (session or API token) <!-- server/service/handler.go:842; handler listMDMConfigProfilesEndpoint -->|
| GET | `/api/_version_/fleet/configuration_profiles` | user (session or API token) <!-- server/service/handler.go:843; handler listMDMConfigProfilesEndpoint -->|
| POST | `/api/_version_/fleet/mdm/profiles` | user (session or API token) <!-- server/service/handler.go:847; handler newMDMConfigProfileEndpoint -->|
| POST | `/api/_version_/fleet/configuration_profiles` | user (session or API token) <!-- server/service/handler.go:848; handler newMDMConfigProfileEndpoint -->|
| PATCH | `/api/_version_/fleet/configuration_profiles/{profile_uuid}` | user (session or API token) <!-- server/service/handler.go:849; handler updateMDMConfigProfileEndpoint -->|
| POST | `/api/_version_/fleet/configuration_profiles/batch` | user (session or API token) <!-- server/service/handler.go:851; handler batchModifyMDMConfigProfilesEndpoint -->|
| POST | `/api/_version_/fleet/hosts/{host_id:[0-9]+}/configuration_profiles/resend/{profile_uuid}` | user (session or API token) <!-- server/service/handler.go:855; handler resendHostMDMProfileEndpoint -->|
| POST | `/api/_version_/fleet/hosts/{host_id:[0-9]+}/configuration_profiles/{profile_uuid}/resend` | user (session or API token) <!-- server/service/handler.go:856; handler resendHostMDMProfileEndpoint -->|
| POST | `/api/_version_/fleet/hosts/{host_id:[0-9]+}/name_template/resend` | user (session or API token) <!-- server/service/handler.go:857; handler resendHostNameTemplateEndpoint -->|
| POST | `/api/_version_/fleet/configuration_profiles/resend/batch` | user (session or API token) <!-- server/service/handler.go:858; handler batchResendMDMProfileToHostsEndpoint -->|
| GET | `/api/_version_/fleet/configuration_profiles/{profile_uuid}/status` | user (session or API token) <!-- server/service/handler.go:859; handler getMDMConfigProfileStatusEndpoint -->|
| PATCH | `/api/_version_/fleet/mdm/apple/settings` | user (session or API token) <!-- server/service/handler.go:863; handler updateMDMAppleSettingsEndpoint -->|
| POST | `/api/_version_/fleet/disk_encryption` | user (session or API token) <!-- server/service/handler.go:864; handler updateDiskEncryptionEndpoint -->|
| POST | `/api/_version_/fleet/host_name_template` | user (session or API token) <!-- server/service/handler.go:865; handler updateHostNameTemplateEndpoint -->|
| POST | `/api/_version_/fleet/mdm/apple/request_csr` | user (session or API token) <!-- server/service/handler.go:872; handler requestMDMAppleCSREndpoint -->|
| POST | `/api/_version_/fleet/mdm/apple/dep/key_pair` | user (session or API token) <!-- server/service/handler.go:875; handler newMDMAppleDEPKeyPairEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/ab_public_key` | user (session or API token) <!-- server/service/handler.go:876; handler generateABMKeyPairEndpoint -->|
| POST | `/api/_version_/fleet/ab_tokens` | user (session or API token) <!-- server/service/handler.go:877; handler uploadABMTokenEndpoint -->|
| DELETE | `/api/_version_/fleet/ab_tokens/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:878; handler deleteABMTokenEndpoint -->|
| GET | `/api/_version_/fleet/ab_tokens` | user (session or API token) <!-- server/service/handler.go:879; handler listABMTokensEndpoint -->|
| GET | `/api/_version_/fleet/ab_tokens/count` | user (session or API token) <!-- server/service/handler.go:880; handler countABMTokensEndpoint -->|
| PATCH | `/api/_version_/fleet/ab_tokens/{id:[0-9]+}/fleets` | user (session or API token) <!-- server/service/handler.go:881; handler updateABMTokenTeamsEndpoint -->|
| PATCH | `/api/_version_/fleet/ab_tokens/{id:[0-9]+}/renew` | user (session or API token) <!-- server/service/handler.go:882; handler renewABMTokenEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/request_csr` | user (session or API token) <!-- server/service/handler.go:884; handler getMDMAppleCSREndpoint -->|
| POST | `/api/_version_/fleet/mdm/apple/apns_certificate` | user (session or API token) <!-- server/service/handler.go:885; handler uploadMDMAppleAPNSCertEndpoint -->|
| DELETE | `/api/_version_/fleet/mdm/apple/apns_certificate` | user (session or API token) <!-- server/service/handler.go:886; handler deleteMDMAppleAPNSCertEndpoint -->|
| GET | `/api/_version_/fleet/vpp_tokens` | user (session or API token) <!-- server/service/handler.go:889; handler getVPPTokens -->|
| POST | `/api/_version_/fleet/vpp_tokens` | user (session or API token) <!-- server/service/handler.go:890; handler uploadVPPTokenEndpoint -->|
| PATCH | `/api/_version_/fleet/vpp_tokens/{id}/fleets` | user (session or API token) <!-- server/service/handler.go:891; handler patchVPPTokensTeams -->|
| PATCH | `/api/_version_/fleet/vpp_tokens/{id}/renew` | user (session or API token) <!-- server/service/handler.go:892; handler patchVPPTokenRenewEndpoint -->|
| DELETE | `/api/_version_/fleet/vpp_tokens/{id}` | user (session or API token) <!-- server/service/handler.go:893; handler deleteVPPToken -->|
| POST | `/api/_version_/fleet/software/app_store_apps/batch` | user (session or API token) <!-- server/service/handler.go:896; handler batchAssociateAppStoreAppsEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple_bm` | user (session or API token) <!-- server/service/handler.go:900; handler getAppleBMEndpoint -->|
| GET | `/api/_version_/fleet/abm` | user (session or API token) <!-- server/service/handler.go:902; handler getAppleBMEndpoint -->|
| POST | `/api/_version_/fleet/mdm/apple/profiles/batch` | user (session or API token) <!-- server/service/handler.go:911; handler batchSetMDMAppleProfilesEndpoint -->|
| POST | `/api/_version_/fleet/mdm/profiles/batch` | user (session or API token) <!-- server/service/handler.go:916; handler batchSetMDMProfilesEndpoint -->|
| POST | `/api/_version_/fleet/certificate_authorities` | user (session or API token) <!-- server/service/handler.go:919; handler createCertificateAuthorityEndpoint -->|
| GET | `/api/_version_/fleet/certificate_authorities` | user (session or API token) <!-- server/service/handler.go:920; handler listCertificateAuthoritiesEndpoint -->|
| GET | `/api/_version_/fleet/certificate_authorities/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:921; handler getCertificateAuthorityEndpoint -->|
| DELETE | `/api/_version_/fleet/certificate_authorities/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:922; handler deleteCertificateAuthorityEndpoint -->|
| PATCH | `/api/_version_/fleet/certificate_authorities/{id:[0-9]+}` | user (session or API token) <!-- server/service/handler.go:923; handler updateCertificateAuthorityEndpoint -->|
| POST | `/api/_version_/fleet/certificate_authorities/{id:[0-9]+}/request_certificate` | user (session or API token) <!-- server/service/handler.go:924; handler requestCertificateEndpoint -->|
| POST | `/api/_version_/fleet/spec/certificate_authorities` | user (session or API token) <!-- server/service/handler.go:925; handler batchApplyCertificateAuthoritiesEndpoint -->|
| GET | `/api/_version_/fleet/spec/certificate_authorities` | user (session or API token) <!-- server/service/handler.go:926; handler getCertificateAuthoritiesSpecEndpoint -->|
| POST | `/api/_version_/fleet/software/web_apps` | user (session or API token) <!-- server/service/handler.go:929; handler createAndroidWebAppEndpoint -->|
| GET | `/api/_version_/fleet/device/{token}` | device (device token) <!-- server/service/handler.go:940; handler getDeviceHostEndpoint -->|
| GET | `/api/_version_/fleet/device/{token}/desktop` | device (device token) <!-- server/service/handler.go:941; handler getFleetDesktopEndpoint -->|
| HEAD | `/api/_version_/fleet/device/{token}/ping` | device (device token) <!-- server/service/handler.go:942; handler devicePingEndpoint -->|
| POST | `/api/_version_/fleet/device/{token}/refetch` | device (device token) <!-- server/service/handler.go:943; handler refetchDeviceHostEndpoint -->|
| GET | `/api/_version_/fleet/device/{token}/device_mapping` | device (device token) <!-- server/service/handler.go:945; handler listDeviceHostDeviceMappingEndpoint -->|
| GET | `/api/_version_/fleet/device/{token}/macadmins` | device (device token) <!-- server/service/handler.go:946; handler getDeviceMacadminsDataEndpoint -->|
| GET | `/api/_version_/fleet/device/{token}/policies` | device (device token) <!-- server/service/handler.go:947; handler listDevicePoliciesEndpoint -->|
| GET | `/api/_version_/fleet/device/{token}/transparency` | device (device token) <!-- server/service/handler.go:948; handler transparencyURL -->|
| POST | `/api/_version_/fleet/device/{token}/debug/errors` | device (device token) <!-- server/service/handler.go:949; handler fleetdError -->|
| GET | `/api/_version_/fleet/device/{token}/software` | device (device token) <!-- server/service/handler.go:950; handler getDeviceSoftwareEndpoint -->|
| POST | `/api/_version_/fleet/device/{token}/software/install/{software_title_id}` | device (device token) <!-- server/service/handler.go:951; handler submitSelfServiceSoftwareInstall -->|
| POST | `/api/_version_/fleet/device/{token}/software/install_all` | device (device token) <!-- server/service/handler.go:952; handler submitSelfServiceSoftwareInstallAll -->|
| POST | `/api/_version_/fleet/device/{token}/software/uninstall/{software_title_id}` | device (device token) <!-- server/service/handler.go:953; handler submitDeviceSoftwareUninstall -->|
| GET | `/api/_version_/fleet/device/{token}/software/install/{install_uuid}/results` | device (device token) <!-- server/service/handler.go:954; handler getDeviceSoftwareInstallResultsEndpoint -->|
| GET | `/api/_version_/fleet/device/{token}/software/uninstall/{execution_id}/results` | device (device token) <!-- server/service/handler.go:955; handler getDeviceSoftwareUninstallResultsEndpoint -->|
| GET | `/api/_version_/fleet/device/{token}/software/self_service_categories` | device (device token) <!-- server/service/handler.go:956; handler getDeviceSelfServiceCategoriesEndpoint -->|
| GET | `/api/_version_/fleet/device/{token}/certificates` | device (device token) <!-- server/service/handler.go:957; handler listDeviceCertificatesEndpoint -->|
| POST | `/api/_version_/fleet/device/{token}/setup_experience/status` | device (device token) <!-- server/service/handler.go:958; handler getDeviceSetupExperienceStatusEndpoint -->|
| GET | `/api/_version_/fleet/device/{token}/software/titles/{software_title_id}/icon` | device (device token) <!-- server/service/handler.go:959; handler getDeviceSoftwareIconEndpoint -->|
| POST | `/api/_version_/fleet/device/{token}/mdm/linux/trigger_escrow` | device (device token) <!-- server/service/handler.go:960; handler triggerLinuxDiskEncryptionEscrowEndpoint -->|
| POST | `/api/_version_/fleet/device/{token}/bypass_conditional_access` | device (device token) <!-- server/service/handler.go:961; handler bypassConditionalAccessEndpoint -->|
| GET | `/api/_version_/fleet/device/{token}/mdm/apple/manual_enrollment_profile` | device (device token) <!-- server/service/handler.go:964; handler getDeviceMDMManualEnrollProfileEndpoint -->|
| GET | `/api/_version_/fleet/device/{token}/software/commands/{command_uuid}/results` | device (device token) <!-- server/service/handler.go:965; handler getDeviceMDMCommandResultsEndpoint -->|
| POST | `/api/_version_/fleet/device/{token}/configuration_profiles/{profile_uuid}/resend` | device (device token) <!-- server/service/handler.go:966; handler resendDeviceConfigurationProfileEndpoint -->|
| POST | `/api/_version_/fleet/device/{token}/migrate_mdm` | device (device token) <!-- server/service/handler.go:967; handler migrateMDMDeviceEndpoint -->|
| POST | `/api/osquery/config` | host (osquery node key) <!-- server/service/handler.go:999; handler getClientConfigEndpoint -->|
| POST | `/api/v1/osquery/config` | host (osquery node key) <!-- server/service/handler.go:999; alt path of /api/osquery/config; handler getClientConfigEndpoint -->|
| POST | `/api/osquery/distributed/read` | host (osquery node key) <!-- server/service/handler.go:1001; handler getDistributedQueriesEndpoint -->|
| POST | `/api/v1/osquery/distributed/read` | host (osquery node key) <!-- server/service/handler.go:1001; alt path of /api/osquery/distributed/read; handler getDistributedQueriesEndpoint -->|
| POST | `/api/osquery/distributed/write` | host (osquery node key) <!-- server/service/handler.go:1028; handler submitDistributedQueryResultsEndpoint -->|
| POST | `/api/v1/osquery/distributed/write` | host (osquery node key) <!-- server/service/handler.go:1028; alt path of /api/osquery/distributed/write; handler submitDistributedQueryResultsEndpoint -->|
| POST | `/api/osquery/carve/begin` | host (osquery node key) <!-- server/service/handler.go:1030; handler carveBeginEndpoint -->|
| POST | `/api/v1/osquery/carve/begin` | host (osquery node key) <!-- server/service/handler.go:1030; alt path of /api/osquery/carve/begin; handler carveBeginEndpoint -->|
| POST | `/api/osquery/log` | host (osquery node key) <!-- server/service/handler.go:1032; handler submitLogsEndpoint -->|
| POST | `/api/v1/osquery/log` | host (osquery node key) <!-- server/service/handler.go:1032; alt path of /api/osquery/log; handler submitLogsEndpoint -->|
| POST | `/api/osquery/yara/{name}` | host (osquery node key) <!-- server/service/handler.go:1034; handler getYaraEndpoint -->|
| POST | `/api/v1/osquery/yara/{name}` | host (osquery node key) <!-- server/service/handler.go:1034; alt path of /api/osquery/yara/{name}; handler getYaraEndpoint -->|
| GET | `/api/fleetd/certificates/{id:[0-9]+}` | android (orbit node key) <!-- server/service/handler.go:1041; handler getDeviceCertificateTemplateEndpoint -->|
| PUT | `/api/fleetd/certificates/{id:[0-9]+}/status` | android (orbit node key) <!-- server/service/handler.go:1042; handler updateCertificateStatusEndpoint -->|
| POST | `/api/fleet/orbit/device_token` | orbit (orbit node key) <!-- server/service/handler.go:1046; handler setOrUpdateDeviceTokenEndpoint -->|
| POST | `/api/fleet/orbit/config` | orbit (orbit node key) <!-- server/service/handler.go:1047; handler getOrbitConfigEndpoint -->|
| POST | `/api/fleet/orbit/scripts/request` | orbit (orbit node key) <!-- server/service/handler.go:1050; handler getOrbitScriptEndpoint -->|
| POST | `/api/fleet/orbit/scripts/result` | orbit (orbit node key) <!-- server/service/handler.go:1051; handler postOrbitScriptResultEndpoint -->|
| PUT | `/api/fleet/orbit/device_mapping` | orbit (orbit node key) <!-- server/service/handler.go:1052; handler putOrbitDeviceMappingEndpoint -->|
| POST | `/api/fleet/orbit/software_install/result` | orbit (orbit node key) <!-- server/service/handler.go:1053; handler postOrbitSoftwareInstallResultEndpoint -->|
| POST | `/api/fleet/orbit/software_install/package` | orbit (orbit node key) <!-- server/service/handler.go:1054; handler orbitDownloadSoftwareInstallerEndpoint -->|
| POST | `/api/fleet/orbit/software_install/details` | orbit (orbit node key) <!-- server/service/handler.go:1055; handler getOrbitSoftwareInstallDetails -->|
| POST | `/api/fleet/orbit/setup_experience/init` | orbit (orbit node key) <!-- server/service/handler.go:1056; handler orbitSetupExperienceInitEndpoint -->|
| POST | `/api/fleet/orbit/setup_experience/status` | orbit (orbit node key) <!-- server/service/handler.go:1061; handler getOrbitSetupExperienceStatusEndpoint -->|
| POST | `/api/fleet/orbit/disk_encryption_key` | orbit (orbit node key) <!-- server/service/handler.go:1064; handler postOrbitDiskEncryptionKeyEndpoint -->|
| POST | `/api/fleet/orbit/managed_local_account` | orbit (orbit node key) <!-- server/service/handler.go:1066; handler postOrbitManagedLocalAccountEndpoint -->|
| POST | `/api/fleet/orbit/luks_data` | orbit (orbit node key) <!-- server/service/handler.go:1068; handler postOrbitLUKSEndpoint -->|
| POST | `/api/osquery/enroll` | enroll secret, verified inside the handler <!-- server/service/handler.go:1076; handler enrollAgentEndpoint -->|
| POST | `/api/v1/osquery/enroll` | enroll secret, verified inside the handler <!-- server/service/handler.go:1076; alt path of /api/osquery/enroll; handler enrollAgentEndpoint -->|
| GET | `/api/mdm/apple/enroll` | none <!-- server/service/handler.go:1085; handler mdmAppleEnrollEndpoint -->|
| POST | `/api/mdm/apple/enroll` | none <!-- server/service/handler.go:1086; handler mdmAppleEnrollEndpoint -->|
| GET | `/api/mdm/apple/installer` | none <!-- server/service/handler.go:1088; handler mdmAppleGetInstallerEndpoint -->|
| HEAD | `/api/mdm/apple/installer` | none <!-- server/service/handler.go:1089; handler mdmAppleHeadInstallerEndpoint -->|
| POST | `/api/_version_/fleet/ota_enrollment` | none <!-- server/service/handler.go:1090; handler mdmAppleOTAEndpoint -->|
| GET | `/api/_version_/fleet/mdm/bootstrap` | none <!-- server/service/handler.go:1094; handler downloadBootstrapPackageEndpoint -->|
| GET | `/api/_version_/fleet/bootstrap` | none <!-- server/service/handler.go:1095; handler downloadBootstrapPackageEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/bootstrap` | none <!-- server/service/handler.go:1098; handler downloadBootstrapPackageEndpoint -->|
| GET | `/api/_version_/fleet/mdm/setup/eula/{token}` | none <!-- server/service/handler.go:1102; handler getMDMEULAEndpoint -->|
| GET | `/api/_version_/fleet/setup_experience/eula/{token}` | none <!-- server/service/handler.go:1103; handler getMDMEULAEndpoint -->|
| GET | `/api/_version_/fleet/mdm/apple/setup/eula/{token}` | none <!-- server/service/handler.go:1106; handler getMDMEULAEndpoint -->|
| GET | `/api/_version_/fleet/enrollment_profiles/ota` | none <!-- server/service/handler.go:1109; handler getOTAProfileEndpoint -->|
| POST | `/api/mdm/apple/account_driven_enroll/{token}` | none <!-- server/service/handler.go:1112; handler mdmAppleAccountEnrollEndpoint -->|
| POST | `/api/mdm/apple/account_driven_enroll` | none <!-- server/service/handler.go:1114; handler mdmAppleAccountEnrollEndpoint -->|
| POST | `/api/mdm/apple/psso/nonce` | none <!-- server/service/handler.go:1123; handler pssoNonceEndpoint -->|
| POST | `/api/mdm/apple/psso/registration` | none <!-- server/service/handler.go:1124; handler pssoRegistrationEndpoint -->|
| POST | `/api/mdm/apple/psso/token` | none <!-- server/service/handler.go:1125; handler pssoTokenEndpoint -->|
| GET | `/api/mdm/apple/psso/jwks` | none <!-- server/service/handler.go:1126; handler pssoJWKSEndpoint -->|
| POST | `/api/mdm/microsoft/discovery` | none <!-- server/service/handler.go:1135; handler mdmMicrosoftDiscoveryEndpoint -->|
| POST | `/api/mdm/microsoft/policy` | none <!-- server/service/handler.go:1138; handler mdmMicrosoftPolicyEndpoint -->|
| POST | `/api/mdm/microsoft/enroll` | none <!-- server/service/handler.go:1141; handler mdmMicrosoftEnrollEndpoint -->|
| POST | `/api/mdm/microsoft/management` | none <!-- server/service/handler.go:1145; handler mdmMicrosoftManagementEndpoint -->|
| GET | `/api/mdm/microsoft/tos` | none <!-- server/service/handler.go:1148; handler mdmMicrosoftTOSEndpoint -->|
| POST | `/api/fleet/orbit/enroll` | none (orbit enroll) <!-- server/service/handler.go:1152; handler enrollOrbitEndpoint -->|
| GET | `/api/_version_/fleet/software/titles/{title_id:[0-9]+}/in_house_app/{token:[a-f0-9-]+}` | none <!-- server/service/handler.go:1156; handler getInHouseAppPackageEndpoint -->|
| GET | `/api/_version_/fleet/software/titles/{title_id:[0-9]+}/in_house_app/manifest/{token:[a-f0-9-]+}` | none <!-- server/service/handler.go:1157; handler getInHouseAppManifestEndpoint -->|
| POST | `/api/osquery/carve/block` | none <!-- server/service/handler.go:1176; handler carveBlockEndpoint -->|
| POST | `/api/v1/osquery/carve/block` | none <!-- server/service/handler.go:1176; alt path of /api/osquery/carve/block; handler carveBlockEndpoint -->|
| GET | `/api/_version_/fleet/software/titles/{title_id:[0-9]+}/package/token/{token}` | none <!-- server/service/handler.go:1178; handler downloadSoftwareInstallerEndpoint -->|
| POST | `/api/_version_/fleet/perform_required_password_reset` | none <!-- server/service/handler.go:1181; handler performRequiredPasswordResetEndpoint -->|
| POST | `/api/_version_/fleet/users` | none <!-- server/service/handler.go:1182; handler createUserFromInviteEndpoint -->|
| GET | `/api/_version_/fleet/invites/{token}` | none <!-- server/service/handler.go:1183; handler verifyInviteEndpoint -->|
| POST | `/api/_version_/fleet/reset_password` | none <!-- server/service/handler.go:1184; handler resetPasswordEndpoint -->|
| POST | `/api/_version_/fleet/logout` | none <!-- server/service/handler.go:1185; handler logoutEndpoint -->|
| GET | `/api/_version_/fleet/logo` | none <!-- server/service/handler.go:1192; handler getOrgLogoEndpoint -->|
| POST | `/api/v1/fleet/sso` | none <!-- server/service/handler.go:1220; handler initiateSSOEndpoint -->|
| POST | `/api/v1/fleet/sso/callback` | none <!-- server/service/handler.go:1225; handler makeCallbackSSOEndpoint -->|
| GET | `/api/v1/fleet/sso` | none <!-- server/service/handler.go:1226; handler settingsSSOEndpoint -->|
| GET | `/api/_version_/fleet/results/` | user (session or API token), authenticated inside the websocket handler <!-- server/service/handler.go:1233; path prefix, not exact match; handler makeStreamDistributedQueryCampaignResultsHandler -->|
| POST | `/api/_version_/fleet/forgot_password` | none <!-- server/service/handler.go:1239; handler forgotPasswordEndpoint -->|
| POST | `/api/_version_/fleet/login` | none <!-- server/service/handler.go:1242; handler loginEndpoint -->|
| POST | `/api/_version_/fleet/sessions` | none <!-- server/service/handler.go:1244; handler sessionCreateEndpoint -->|
| HEAD | `/api/fleet/device/ping` | none <!-- server/service/handler.go:1246; handler devicePingEndpoint -->|
| HEAD | `/api/fleet/orbit/ping` | none <!-- server/service/handler.go:1248; handler orbitPingEndpoint -->|
| POST | `/api/_version_/fleet/calendar/webhook/{event_uuid}` | none <!-- server/service/handler.go:1251; handler calendarWebhookEndpoint -->|
| POST | `/api/_version_/fleet/mdm/sso` | none <!-- server/service/handler.go:1254; handler initiateMDMSSOEndpoint -->|
| POST | `/api/_version_/fleet/mdm/sso/callback` | none <!-- server/service/handler.go:1259; handler callbackMDMSSOEndpoint -->|
| GET | `/api/_version_/fleet/android_enterprise/signup_url` | user (session or API token) <!-- server/mdm/android/service/handler.go:25; handler enterpriseSignupEndpoint -->|
| GET | `/api/_version_/fleet/android_enterprise` | user (session or API token) <!-- server/mdm/android/service/handler.go:26; handler getEnterpriseEndpoint -->|
| DELETE | `/api/_version_/fleet/android_enterprise` | user (session or API token) <!-- server/mdm/android/service/handler.go:27; handler deleteEnterpriseEndpoint -->|
| GET | `/api/_version_/fleet/android_enterprise/signup_sse` | user (session or API token) <!-- server/mdm/android/service/handler.go:28; handler enterpriseSSE -->|
| GET | `/api/_version_/fleet/android_enterprise/connect/{token}` | none <!-- server/mdm/android/service/handler.go:35; handler enterpriseSignupCallbackEndpoint -->|
| GET | `/api/_version_/fleet/android_enterprise/enrollment_token` | none <!-- server/mdm/android/service/handler.go:36; handler enrollmentTokenEndpoint -->|
| POST | `/api/v1/fleet/android_enterprise/pubsub` | Pub/Sub token, verified inside the handler <!-- server/mdm/android/service/handler.go:37; handler pubSubPushEndpoint -->|
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

The server’s alias table maps these older paths to the handlers serving their current replacements.

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

These routes register directly on the router. Most check protocol credentials or state, such as a device certificate, SCEP challenge, or pre-setup state. The two service-discovery paths and app-site-association document accept any caller, as their protocols require.

| Method | Path | Auth |
|---|---|---|
| ANY | `/api/v1/setup` | route-local or protocol <!-- server/service/handler.go:1279; raw: WithSetup; handler srv -->|
| ANY | `/api/setup` | route-local or protocol <!-- server/service/handler.go:1280; raw: WithSetup; handler srv -->|
| ANY | `/mdm/apple/service_discovery/{token}` | none (public) <!-- server/service/handler.go:1402; raw: registerMDMServiceDiscovery; handler otel.WrapHandler -->|
| ANY | `/mdm/apple/service_discovery` | none (public) <!-- server/service/handler.go:1403; raw: registerMDMServiceDiscovery; handler otel.WrapHandler -->|
| ANY | `/.well-known/apple-app-site-association` | none (public) <!-- server/service/handler.go:1419; raw: registerPSSO; handler otel.WrapHandler -->|
| ANY | `/mdm/apple/scep` | route-local or protocol <!-- server/service/handler.go:1460; raw: registerSCEP; handler otel.WrapHandler -->|
| ANY | `/mdm/scep/proxy/` | route-local or protocol <!-- server/service/handler.go:1486; raw: RegisterSCEPProxy; handler scepHandler -->|
| ANY | `/mdm/apple/mdm` | route-local or protocol <!-- server/service/handler.go:1557; raw: registerMDM; handler otel.WrapHandler -->|
