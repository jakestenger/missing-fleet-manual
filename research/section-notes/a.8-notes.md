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
| The device class described by two paths | The whole family named and its size stated | 26 routes are registered on the device endpointer at this release. Exposing the ping and desktop calls alone leaves an end user's device page loading and inert |
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
| The device endpointer registers 26 routes at this release, including policies, software install and uninstall, self-service, certificates, setup-experience status, Linux escrow triggering, conditional-access bypass and MDM migration | `server/service/handler.go:939-966` |
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
| A configured URL prefix is prepended to everything Fleet serves | `cmd/fleet/serve.go:230-231` |
| Apple device management can be configured with its own server URL | `server/service/appconfig.go:1557-1568` |

### The exposure matrix

Every path read from its registration. Grouped as the appendix groups them.

| Capability | Paths, and source |
|---|---|
| Baseline agent | osquery and Orbit families, `server/service/handler.go:1030-1046`; the full device family, `:937-966` |
| API clients and setup | `/api/setup` at `server/service/handler.go:1277`. **Not a versioned family** |
| Fleet SSO | `server/service/handler.go:1217-1223` |
| SCIM | `ee/server/scim/scim.go:283-284`, `/api/v1/` and `/api/latest/` only |
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

## Rounds

| Round | Verdict | Outcome |
|---|---|---|
| 1, coverage | NOT READY, six blocking items | All six applied. Appendix grew from 1,463 to about 2,340 words, almost all of it inventory that was missing |
| 2, evidence audit | Not yet run | |
| 3, whole-appendix and cross-appendix | Not yet run | |
