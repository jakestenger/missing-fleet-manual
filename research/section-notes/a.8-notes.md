---
section: "A.8"
---

# a.8 API access, versioning, and exposure: citation ledger

Written 2026-08-25. **Rewritten 2026-08-29** after review round 1 of 3, which returned NOT READY with
six blocking items. Held to Part IX's evidence rule
([`../appendix-structure.md`](../appendix-structure.md)), which for this appendix means the exposure
matrix is held to a stronger standard than the prose around it: for its declared capability set it
must be a complete, release-locked inventory, because an omitted path produces a broken or unsafe
ingress design.

Bases per STYLE §27, where **stated** means the cited source establishes both the content and the
scope of the claim.

## The lesson from round 1, recorded first because it caused most of the defects

**The first draft's exposure matrix was sourced from a Fleet article, not from route registrations.**
The old version of this ledger says so in as many words: its source row for "the full public-exposure
matrix by platform and feature" cites `articles/what-api-endpoints-to-expose-to-the-public-internet.md`.

That single decision produced seven wholly missing capabilities and nine wrong or incomplete paths,
and it produced them invisibly, because an article organised by capability looks exactly like a
complete inventory organised by capability. **A hand-maintained document cannot be the evidence for a
completeness claim about the thing it documents.** Everything below is now read from the server's own
registrations at `fleet-v4.90.1`, commit `dd0200f062`.

The project already had this rule for defaults, after three settings were found where the generated
reference disagreed with what the server registers. It did not have it for routes. It does now.

## What round 1 changed

| Was | Now | Why it was wrong |
|---|---|---|
| "Every endpoint is registered through one of six authenticators" | Six **caller classes**, stated as an ingress model rather than a registration claim | False as written. The Apple MDM protocol paths, the SCEP service, Apple service discovery and the Platform SSO well-known document are registered directly on the root router and pass through no endpointer at all |
| **Android**: "Google's Android Management API, calling back into Fleet", presenting "its own token" | **fleetd certificate**: fleetd on a device presenting the **Orbit node key** in an `Authentication` header | The Android-authenticated endpointer serves the fleetd certificate routes. Fleet's own comment says the Orbit node key is used because it is the only credential available once MDM setup completes. Google's callback is a different thing and belongs to the route-local class |
| **No auth**, "None" | **Route-local or protocol** | Unsafe terminology. The group includes enrollment secrets, download tokens, SAML responses, query-string tokens and device identity certificates, and Fleet's own registration comment describes these routes as performing custom one-time authentication. A reader planning ingress from the word "none" would conclude they need no protection |
| The device class described by two paths | The whole family named by what it does, with **no count** | Exposing the ping and desktop calls alone leaves an end user's device page loading and inert. I first wrote the size as 26; it is **25**, and round 2 ruled the number out of the appendix altogether since the prefix is the ingress contract |
| "A route is registered under each version its module declares" | "A route **declared with Fleet's version placeholder** is registered..." | Literal and root-mux routes bypass the mechanism entirely |
| "Match `/api/*/fleet/` where you can" | Match `v1`, `2022-04` and `latest` explicitly, then the unversioned families separately | Wildcard segment syntax differs between proxies and can accept segments never intended |
| "Fleet's own machine-readable route catalogue carries 234 entries" | The **allowlist catalogue for API-only accounts**, with its validation direction stated | It is not a route inventory |

## Stated, source checked at the tag

### The caller model

| Claim | Source |
|---|---|
| Six caller classes exist as an ingress model: user, host, orbit, device, fleetd certificate, route-local or protocol | `server/service/handler.go:937,1035,1044,1067` |
| The fleetd certificate routes authenticate with the **Orbit node key** in an `Authentication` header, and Fleet's comment says why | `server/service/handler.go:1035-1041`, `server/service/endpoint_utils.go:256` |
| Google's Android event callback is registered with no standard authenticator and verifies a route-specific query token | `server/mdm/android/service/handler.go:30`, `server/mdm/android/service/pubsub.go:80` |
| Apple MDM protocol services are registered directly on the root mux | `server/service/handler.go:1342` |
| Routes in the route-local class perform custom one-time authentication | `server/service/handler.go:1067`, Fleet's own registration comment |
| The device endpointer registers **25** routes at this release, covering policies, software install and uninstall, self-service, certificates, setup-experience status, Linux escrow triggering, conditional-access bypass and MDM migration. **The count is not published** | `server/service/handler.go:939-966` |
| API tokens are tied to a Fleet user account and sent as `Authorization: Bearer <token>`; obtainable from **My account > Get API token** or the login endpoint; email and password login disabled for SSO and MFA users | `docs/REST API/rest-api.md:49-59` |

### Versioning

| Claim | Source |
|---|---|
| The core module declares `v1` and `2022-04` | `server/service/handler.go:292` |
| The Android module declares `v1` alone | `server/mdm/android/service/handler.go:35` |
| A route's own start and end constraints narrow its module's ordered set, and `latest` is omitted where a route ends before the module's last version | `server/platform/endpointer/endpoint_utils.go:1115` |
| `latest` is inserted into the route expression and handled directly, not a redirect | `server/platform/endpointer/endpoint_utils.go:1144` |
| Fleet's SSO initiation and callback are literal `v1` paths | `server/service/handler.go:1217,1222` |
| Android's Pub/Sub callback is a literal `v1` path | `server/mdm/android/service/handler.go:18` |
| A configured URL prefix is prepended to everything Fleet serves, **including root-mux handlers**, because Fleet wraps the completed root mux and strips the prefix before dispatch | `cmd/fleet/serve.go:993-996`. **Corrected at round 2**: my first citation, `:230-231`, only normalises and validates the setting |
| The Apple server URL selects **which base URL Fleet advertises** for certain MDM flows. It does not create a second listener and does not make any path unreachable at the main origin; Fleet's guidance is that it resolves to the same server | `server/fleet/app.go:199-205,331-342`. **Corrected at round 2**, where my first version had paths moving between origins |

### The exposure matrix

Every path read from its registration. Grouped as the appendix groups them.

| Capability | Paths, and source |
|---|---|
| Baseline agent | osquery and Orbit families, `server/service/handler.go:1030-1046`; the full device family, `:937-966` |
| API clients and setup | `/api/setup` at `server/service/handler.go:1277`. **Not a versioned family** |
| Fleet SSO | `server/service/handler.go:1217-1223` |
| SCIM | Prefix mounts at `ee/server/scim/scim.go:283-284`, `/api/v1/` and `/api/latest/`. **The details endpoint is a core route and also exists at `2022-04`**, `server/service/handler.go:621` |
| Apple MDM, ACME, installer | `server/service/handler.go:1085`; ACME directory `server/mdm/apple/apple_mdm.go:156`; installer path constant `server/mdm/apple/apple_mdm.go:57` |
| Setup experience: EULA, bootstrap, MDM SSO callback | `server/service/handler.go:761`, `:713`, `:1250` |
| Enrollment by link, including `ota_enrollment` | `server/service/handler.go:1087`, and the profile that sends the device there, `server/mdm/apple/apple_mdm.go:1772` |
| In-house apps, **both** paths | `server/service/handler.go:1153-1154` |
| Windows MDM protocol paths | Unchanged from the first draft and re-confirmed at review |
| Android enrollment token and enablement callback | `server/mdm/android/service/handler.go:35` |
| Certificate delivery | SCEP proxy path constant `server/mdm/apple/apple_mdm.go:68`; fleetd certificates `server/service/handler.go:1039` |
| Google Calendar webhook | `server/service/handler.go:1248`, and the URL Fleet supplies to Google, `ee/server/calendar/google_calendar.go:233` |
| Okta conditional access | `ee/server/service/condaccess/scep.go:25`, `ee/server/service/condaccess/idp.go:36-37` |

**Seven capabilities were absent entirely** before this round: Fleet SSO, SCIM, Google Calendar, Okta
conditional access, certificate delivery, Apple ACME hardware attestation, and the full device
family. **The SCIM omission also broke an explicit promise live in 2.2**, which sends readers here for
SCIM endpoints.

**Nine path corrections** were applied to capabilities already present: setup, EULA, bootstrap, OTA
enrollment, in-house apps, account-driven enrollment, MDM SSO callback, Android prefixes and
enablement, and the Apple installer download.

## Derived

| Conclusion | From | Reasoning |
|---|---|---|
| Reading the request surface as six classes of caller is the useful model | The authenticators and the root-mux registrations above | Fleet's reference is organised by resource, not by caller. The reframing is the book's, and is why this appendix exists in this shape |
| A rule matching `/api/v1/` misses the other prefixes and the unversioned families | The registration behaviour, plus Fleet's own docs using `v1` and `latest` interchangeably | Fleet does not warn about this |
| Match three explicit prefixes rather than a wildcard segment | Wildcard semantics differ between proxies | Operational judgement on top of a verified fact |
| Separate Orbit and osquery node keys mean a host can be half-working | The distinct authenticators and keys established for 3.1 | Fleet documents the keys separately and does not draw the conclusion |
| The device class is the one most often missed in network planning | Its size, and that its two best-known paths are the two usually exposed | Judgement, not a Fleet claim |

## Not established

**Whether the matrix is complete beyond the capabilities named.** The appendix now declares its
inclusion rule and its exclusions and says in terms that a capability absent from it has not been
assessed, rather than been found to need nothing. That is the honest position given that seven
capabilities were missing from a matrix which read as complete.

**A parsed derivation of the 234 and 12 counts.** Round 1 asked for the catalogue to be parsed
through Fleet's own loader and type, with its duplicate and route-registration validation run, rather
than counted textually. **There is no Go toolchain on this machine**, so that has not been done. The
numbers are numerically confirmed and are carried with their unit and meaning corrected. A future
pass with a toolchain should produce the parsed derivation before this appendix is stamped.

**How `2022-04` differs in behaviour from `v1`, if at all.** Registration verified; semantics not.
No source at the tag was found stating whether the two differ. The appendix says both paths exist and
stops there.

## Operational practice

The prefix-matching advice, the treatment of unversioned families, the exclusion of operator surfaces
from the matrix, and the instruction to re-check after an upgrade are all judgement built on the
verified facts above, and are labelled as such in the text.

## Rejected, and why

**"Every route belongs to exactly one of six classes."** Withdrawn rather than reworded. It read as a
statement about Fleet's implementation and was false as one.

**"No auth" as a class name.** Rejected as unsafe rather than merely imprecise.

## Checks run

`check-links`, `check-em-dashes`, `check-crossrefs`, `check-absolutes`, `check-frequency-claims`,
`unwrap` dry run. Read against 2.2, 2.3, 2.6, 2.7, 2.8, 3.1, 3.2, 3.5, 3.7 and 6.3, which are the
chapters that defer here or describe the same paths.



## Round 2, the evidence audit

Round 2 returned NOT READY with eight items. Its central finding is a refinement of round 1's rule
and is the more useful sentence of the two:

> **Registrations establish which routes exist and their exact matching boundaries. The caller, the
> URL producer or the protocol profile establishes which of those routes a capability actually needs
> exposed.**

Round 1 fixed the matrix by reading registrations instead of an article. Round 2 showed that
registrations alone still overexpose, because Fleet registers a route under all three version
prefixes and then emits exactly one of them. Six rows were wrong in that direction, and two of them
named the wrong path entirely.

| Capability | Registered | What Fleet emits | Source |
|---|---|---|---|
| Setup-experience EULA | `/api/*/fleet/setup_experience/eula/{token}` | **`/api/latest/fleet/mdm/setup/eula/{token}`, the deprecated form** | `frontend/utilities/endpoints.ts:216`, loaded at `frontend/pages/MDMAppleSSOCallbackPage/MDMAppleSSOCallbackPage.tsx:52-57` |
| Bootstrap package | `/api/*/fleet/bootstrap` | **`/api/latest/fleet/mdm/bootstrap`, the deprecated form**, hard-coded | `server/fleet/mdm.go:267-274` |
| Setup-experience SSO | Callback under all three | Initiation `/api/latest/fleet/mdm/sso`; callback given to the IdP `/api/v1/fleet/mdm/sso/callback`; return to frontend `/mdm/sso/callback` | `frontend/utilities/endpoints.ts:197`, `ee/server/service/mdm.go:867-875`, `frontend/router/index.tsx:170-177` |
| Enrollment by link | All three, both hops | **`v1` at both hops** | `server/service/frontend.go:199-213`, `server/mdm/apple/apple_mdm.go:1771-1784` |
| In-house apps | All three | **`latest`**, for the manifest and the package | `server/datastore/mysql/activities.go:1539-1545`, `ee/server/service/in_house_apps.go:195-209` |
| Google Calendar webhook | All three | **`v1`**, which is what Google is given | `ee/server/calendar/google_calendar.go:224-238` |
| Android enrollment and callback | `v1` and `latest` | **`v1`** in the enrollment page and the signup callback | `frontend/templates/enroll-ota.html:577`, `server/mdm/android/service/service.go:187` |

### Other round-2 corrections applied

| Was | Now |
|---|---|
| SCIM has "those two prefixes only" | True of the prefix-mounted SCIM protocol resources. **The details endpoint is an ordinary core route and also exists at `2022-04`** (`server/service/handler.go:621`, `:296`) |
| Fleet SSO "reachable under no other prefix" | "no other **API-version** prefix". A configured URL prefix still precedes it |
| "Most of its members require something", of the route-local class | Withdrawn. Fleet's comment covers one registration group; the class as this appendix defines it also contains root-mux and protocol handlers, so the comment cannot carry a frequency claim over it |
| Account-driven enrollment as "the account-driven paths" | Enumerated: service discovery, the enrollment itself, its SSO hop, each with a deprecated tokenless form, plus the shared MDM SSO callback (`server/mdm/apple/apple_mdm.go:43-55`, `server/service/handler.go:1108-1111,1372-1400`) |
| Okta conditional access as one origin | The SSO URL is built for the conditional-access hostname and expected over mutual TLS; metadata and SCEP are on Fleet's ordinary origin (`server/fleet/app.go:345-370`, `ee/server/service/condaccess/idp.go:700-737`) |
| No licence or mount prerequisites | SCIM and the SCEP proxy are Premium; conditional access is Premium **and** needs the server private key, as do Apple's root protocol services, which are not mounted without it (`cmd/fleet/serve.go:845-935`) |
| The metrics endpoint "not mounted unless you configure credentials" | Also mounted when basic authentication is **explicitly disabled** (`cmd/fleet/serve.go:943-955`) |

### The counts are withdrawn

Round 2 confirmed 234 entries and 12 deprecated, and confirmed no duplicate normalised pairs. It
still ruled the numbers unpublishable under the method this appendix agreed, because the prose stated
them without qualification while the ledger declared the required derivation undone. **They are out
of the appendix**, which now describes what the catalogue is without sizing it.

One thing round 2 added that matters more than the number: **the catalogue constrains only API-only
accounts that carry a non-empty endpoint restriction list** (`server/service/middleware/auth/api_only.go:21-67`).
It is not a general allowlist.

### Evidence rows added after round 2

Round 2 found the ledger asserting less than the appendix. Now carried: account-driven enrollment and
the frontend routes, Windows with a source rather than "re-confirmed at review"
(`server/mdm/microsoft/microsoft_mdm.go:12-45`, `server/service/handler.go:1132-1145`), the setup SSO
initiation and frontend callback, Platform SSO's paths, `/enroll`, the metrics mount condition, and
the API-only enforcement semantics.

Four rows moved from **stated** to **derived**, because registration proves existence and not
necessity: the six-class model, every "this capability requires external reachability" mapping, the
Apple base-URL coverage boundary, and the route-local frequency claim, which was withdrawn outright.

## Rounds

| Round | Verdict | Outcome |
|---|---|---|
| 1, coverage | NOT READY, six blocking items | All six applied. Seven capabilities and nine paths added; 1,463 words to about 2,340 |
| 2, evidence audit | NOT READY, eight items | All eight applied. Six rows changed from registered aliases to emitted paths, two of them to deprecated paths that are the ones in use |
| 3, whole-appendix and cross-appendix | Not yet run | |
