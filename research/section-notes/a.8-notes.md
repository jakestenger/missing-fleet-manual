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
| The fleetd certificate routes authenticate with the **Orbit node key** in an `Authentication` header, and Fleet's comment says why | `server/service/handler.go:1035-1041`, `server/service/endpoint_utils.go:256` |
| Google's Android event callback is registered with no standard authenticator and verifies a route-specific query token | `server/mdm/android/service/handler.go:30`, `server/mdm/android/service/pubsub.go:80` |
| Apple MDM protocol services are registered directly on the root mux | `server/service/handler.go:1342` |
| The device endpointer registers **25** routes at this release, covering policies, software install and uninstall, self-service, certificates, setup-experience status, Linux escrow triggering, conditional-access bypass and MDM migration. **The count is not published** | `server/service/handler.go:939-966` |
| API tokens are tied to a Fleet user account and sent as `Authorization: Bearer <token>`; obtainable from **My account > Get API token** or the login endpoint; email and password login disabled for SSO and MFA users | `docs/REST API/rest-api.md:49-59` |
| **The Windows management endpoint authenticates the device inside the handler**, by a client certificate whose common name carries the device identifier or a credential in the SyncML message, with a one-time rekey path. Fleet's registration comment describes the middleware layer only | `server/service/microsoft_mdm.go:1209-1235`, `:1273-1310`. **Corrected at round 5**, after I had asserted the opposite from the comment alone |
| Discovery and terms-of-use require no credential | `server/service/handler.go:1131-1145`, and the handlers beneath |
| Platform SSO's API family and the app-site-association document | `server/service/handler.go:1085` and the frontend router registrations |
| `/enroll` is a frontend-served route, not an API route | `server/service/frontend.go:199-213` |
| The metrics endpoint mounts when credentials are configured **or** basic authentication is explicitly disabled | `cmd/fleet/serve.go:943-955` |
| The API-only catalogue constrains only API-only accounts carrying a non-empty endpoint restriction list | `server/service/middleware/auth/api_only.go:21-67` |
| A user token inherits its account's role and scope, and the activity record attributes work to it | Established for 2.6 and unchanged |
| List endpoints share `page`, `per_page`, `order_key`, `order_direction` | `docs/REST API/rest-api.md:542` |

### Versioning

| Claim | Source |
|---|---|
| The core module declares `v1` and `2022-04` | `server/service/handler.go:296` |
| The chart module declares `v1` and `2022-04` | `server/chart/internal/service/handler.go:24-27` |
| The activity module declares `v1` and `latest` explicitly. **It receives the appended alias as well**, since the shared endpointer appends one regardless; an earlier version of this row said otherwise and was wrong | `server/activity/internal/service/handler.go:41-43`, `server/platform/endpointer/endpoint_utils.go:1144-1150` |
| The Android module declares `v1` alone | `server/mdm/android/service/handler.go:40-42` |
| SCIM is not a versioned module at all: two literal prefix mounts, `v1` and `latest` | `ee/server/scim/scim.go:280-284` |
| **The union across every version-bearing module is `v1`, `2022-04`, `latest` and nothing else** | The four module rows above |
| **Literal mounts are a separate population: their prefix is written out rather than expanded.** SCIM's two mounts carry `v1` and `latest` literally; the Apple root protocol services and the ACME feature module carry no version segment at all. **Literal means not expanded, which is not the same as unprefixed**, and an earlier version of this row conflated them | `ee/server/scim/scim.go:280-284`, `server/service/handler.go:1342`, `cmd/fleet/serve.go:748-754` with `server/mdm/acme/internal/service/handler.go:18-60`. **Narrowed at round 4**, which found the earlier claim covering "every module and root mount" while omitting ACME |
| A route's own start and end constraints narrow its module's ordered set, and `latest` is omitted where a route ends before the module's last version | `server/platform/endpointer/endpoint_utils.go:1115` |
| `latest` is inserted into the route expression and handled directly, not a redirect | `server/platform/endpointer/endpoint_utils.go:1144` |
| Fleet's SSO initiation and callback are literal `v1` paths | `server/service/handler.go:1217,1222` |
| Android's Pub/Sub callback is a literal `v1` path | `server/mdm/android/service/handler.go:18` |
| A configured URL prefix is prepended to everything Fleet serves, **including root-mux handlers**, because Fleet wraps the completed root mux and strips the prefix before dispatch | `cmd/fleet/serve.go:993-996`. **Corrected at round 2**: my first citation, `:230-231`, only normalises and validates the setting |
| The Apple server URL setting exists, is validated as a URL, and Fleet's guidance is that it resolves to the same server | `server/fleet/app.go:199-205,331-342`, `server/service/appconfig.go:1557-1568`. **Which flows advertise it is derived, below** |

### Registrations, which establish that a path exists

Every path read from its registration. **That a capability needs a given path exposed is derived, not stated**, and lives in the Derived table below; a registration proves existence and nothing about necessity.

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
| Windows MDM protocol paths, and which of them authenticate | `server/mdm/microsoft/microsoft_mdm.go:12-45`, registered `server/service/handler.go:1131-1145`. **Discovery, management and terms-of-use are unauthenticated and Fleet's comments say so**; policy and enrollment authenticate by a token in the request |
| Android enrollment token and enablement callback | `server/mdm/android/service/handler.go:35` |
| Certificate delivery | SCEP proxy path constant `server/mdm/apple/apple_mdm.go:68`; fleetd certificates `server/service/handler.go:1039` |
| Google Calendar webhook | `server/service/handler.go:1248`, and the URL Fleet supplies to Google, `ee/server/calendar/google_calendar.go:233` |
| Okta conditional access | `ee/server/service/condaccess/scep.go:25`, `ee/server/service/condaccess/idp.go:36-37` |

**Seven capabilities were absent entirely** before this round: Fleet SSO, SCIM, Google Calendar, Okta
conditional access, certificate delivery, Apple ACME hardware attestation, and the full device
family. **The SCIM omission also broke an explicit promise live in 2.5**, which sends readers here for
SCIM endpoints.

**Nine path corrections** were applied to capabilities already present: setup, EULA, bootstrap, OTA
enrollment, in-house apps, account-driven enrollment, MDM SSO callback, Android prefixes and
enablement, and the Apple installer download.

## Derived

| Conclusion | From | Reasoning |
|---|---|---|
| **Reading the request surface as five shared-credential caller classes plus a residue** | The authenticators and the root-mux registrations above | Fleet's reference is organised by resource, not by caller. The reframing is the book's and is why this appendix exists in this shape. **Demoted at round 3** from six peer classes, because the sixth is defined by absence and implies nothing |
| **That a capability requires a given path to be externally reachable** | The registration, plus the caller or the URL producer | This is the whole exposure matrix, and it is derived. Registration establishes existence and matching; only the caller or the emitted URL establishes necessity. **Moved here from Stated at round 4** |
| **Which flows advertise the Apple base URL and which stay on the main one** | `server/service/devices.go:880-889`, `server/service/frontend.go:199-213`, `server/mdm/apple/util.go:165-174`, `server/mdm/apple/apple_mdm.go:215-230,1431-1465,1527-1537`, `ee/server/service/mdm.go:867-875`, `server/worker/apple_mdm.go:703-715`, `server/mdm/apple/profile_processor.go:421-495`; and on the main URL, `server/service/apple_mdm.go:2177-2179,6414-6418`, `server/fleet/apple_psso.go:123-130`, `ee/server/service/in_house_apps.go:206-209` | Derived from reading every producer of a device-facing URL, not from the configuration validator. **Moved here from Stated at round 4, sourced at round 5** |
| **The Apple base URL also reaches the SCEP-proxy URLs written into Windows profiles** | `server/mdm/microsoft/profile_variables.go:186-188` | Not obvious from the setting's name, which says Apple |
| **Two downloads can leave Fleet's origins entirely**, and fall back when signing fails | `server/worker/apple_mdm.go:703-756` for the bootstrap package, falling back to the Apple base URL; `ee/server/service/in_house_apps.go:206-218` for the in-house package, falling back to the main server URL and logging the failure | The path stays registered and reachable either way. Which origin a device is sent to is conditional on configuration and on whether signing worked |
| A rule matching `/api/v1/` misses the other prefixes and the unversioned families | The registration behaviour, plus Fleet's own docs using `v1` and `latest` interchangeably | Fleet does not warn about this |
| Match three explicit prefixes rather than a wildcard segment | Wildcard semantics differ between proxies | Operational judgement on top of a verified fact |
| Separate Orbit and osquery node keys mean a host can be half-working | The distinct authenticators and keys established for 3.1 | Fleet documents the keys separately and does not draw the conclusion |
| The device class is the one most often missed in network planning | Its size, and that its two best-known paths are the two usually exposed | Judgement, not a Fleet claim |

## Not established

**Whether the matrix is complete beyond the capabilities named.** The appendix now declares its
inclusion rule and its exclusions and says in terms that a capability absent from it has not been
assessed, rather than been found to need nothing. That is the honest position given that seven
capabilities were missing from a matrix which read as complete.

**A parsed derivation of the catalogue counts.** Rounds 1 and 2 asked for the catalogue to be parsed
through Fleet's own loader and type, with its duplicate and route-registration validation run, rather
than counted textually. **There is no Go toolchain on this machine**, so it has not been done, and
**the numbers are therefore out of the appendix entirely** rather than carried with a caveat. 6.3 was
publishing them too and no longer does. A future pass with a toolchain can restore them with a real
derivation.

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
`unwrap` dry run. Read against 2.5, 2.6, 2.9, 2.10, 2.11, 2.12, 3.1, 3.2, 3.5, 3.8 and 6.3, which are the
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

Round 2 found the ledger asserting less than the appendix, and **round 5 found this paragraph still
claiming rows the tables did not contain**. They are in the tables above now: Platform SSO, `/enroll`,
the metrics mount condition, the API-only enforcement semantics, token inheritance, and the list
conventions.

**Round 3 found this addendum describing moves the tables had not made. Round 4 found the same thing again**, because I repaired the sentence rather than the tables. They are moved now, in the tables: the caller model, the exposure mapping and the Apple base-URL boundary are in **Derived** and nowhere else, and the route-local universal is deleted. Twice is a pattern, and the lesson is that a ledger entry describing a reclassification is not a reclassification.



## Round 3, the whole read

Round 3 returned NOT READY with seven items, and six of the seven were **corrections that had not
landed** rather than new findings. That is this project's signature defect arriving on schedule: the
round-2 fixes went in fast, two of them only into this ledger, and the ledger then described the
appendix as repaired when it was not.

| Round 2 said | What had actually happened |
|---|---|
| Replace the Apple origin claim | Written into the ledger only. **The appendix still said paths move to another origin** |
| Correct the metrics mount condition | Ledger only. The appendix still said "unless you configure credentials" |
| Withdraw the counts | Done in a.8. **6.3 was still publishing 234 and 12, and citing a.8 as agreeing** |
| Name the prerequisites | Done, but the sentence said "three capabilities" and listed four |
| Reclassify the ledger rows | Described in the addendum, not performed in the tables |

Applied now, plus three round-3 findings of its own:

**The six-class frame is demoted.** Round 3's argument is that the opening promised the class decides
what a `401` means and whether a path may be exposed, and the appendix never organises either answer
that way; meanwhile the sixth row is a residue defined by absence, and the paragraph beneath it
correctly says membership implies nothing. So it is now **five shared-credential classes plus
everything else**, the promise about `401` and exposure is gone, and the tripled hedge is one
sentence.

**The deferrals to a.4 and a.5 were written in the present tense** for appendices that are empty
outlines, which every other chapter in the book is careful not to do. They now say "not written yet"
and name what answers the question today.

**Two chapters were carrying a.8's withdrawn or superseded claims.** 3.2 promised a Mac enrolling by
link needs two paths on top of the protocol paths; the corrected chain has three, and the third is
the one whose absence leaves an enrollment that starts and never finishes. And 6.3 opened by saying
everything an administrator does goes through the API, which is not true of the settings the server
reads at startup.

**One class of claim the User row got grammatically wrong**: it read as though an API-only account
could work through the interface. It cannot.



## Round 5, and the cap

Round 5 returned NOT READY and said plainly that a sixth full review is not worth running: what
remains is bounded, and two of the four items were required corrections rather than polish. Applied,
and this appendix now stops at five rounds, which is the project's cap. It stays at `drafting` for the
whole-book pass.

**The item worth recording is one I got wrong in the opposite direction.** Round 4 told me three of
the five Windows protocol endpoints require nothing, citing Fleet's registration comments, and I
wrote it into the appendix and filed it in the defect queue as S10. It is false. The comment describes
the **middleware layer**: the route is not wrapped in Fleet's standard authenticator. The handler
beneath authenticates the device by a client certificate whose common name carries the device
identifier, or by a credential inside the SyncML message. Only discovery and terms-of-use genuinely
require nothing, and both are pre-enrollment surfaces where that is ordinary.

**S10 is withdrawn**, with its reasoning kept in the queue, because the mistake is the useful part:
the queue already carried D15, a stale Fleet comment that both Fleet's documentation and this manual
had taken as fact, and the rule written down beside it is *read the executed path, not the comment
above it*. I filed S10 the same night.

The other three: both content-delivery paths can fall back to a Fleet origin when signing fails, to
different origins, and the exposure rows now say so instead of contradicting the paragraph above them;
the literal-mount row conflated *not expanded* with *unprefixed*, when SCIM's two mounts carry `v1`
and `latest` literally; and the governing structure note still described a.8's claim as six classes.

## Rounds

| Round | Verdict | Outcome |
|---|---|---|
| 1, coverage | NOT READY, six items | Seven capabilities and nine paths added. The matrix had been sourced from an article |
| 2, evidence audit | NOT READY, eight items | Six rows changed from registered aliases to emitted paths, two of them deprecated paths that are the ones in use |
| 3, whole read | NOT READY, seven items | Six were round-2 fixes that had not landed, two only in this ledger. The caller frame demoted; two chapters corrected |
| 4, verification | NOT READY, four items | The ledger reclassification claimed a second time and not performed. The Apple origin table corrected |
| 5, verification | NOT READY, four items | **Capped here.** The Windows authentication claim reversed and S10 withdrawn; the CDN fallbacks qualified; the ledger's outstanding evidence rows written into the tables |

## Round6 M14 (2026-09-03) — added "Data inventory and trust boundaries" map

A privacy/data-protection review had no route: the material was dispersed across
1.6/2.8/4.1/6.6/7.2/7.6/8.13 and A.10 carried no entry for privacy, personal data, data
classification, retention, or data egress ("conduct a privacy review" dead-ended). A.9 is
intentionally reserved (0.1:250, labs out of scope) and a new appendix is a large ripple, so
the map went into A.8, whose charter word is "exposure" and which already frames itself as
"the matrix network reviews ask for" (a privacy review is the sibling). New section placed
after the exposure matrix, before "API conventions".

It is a NAVIGATIONAL map, deliberately: every cell points to the owning chapter that carries
the verified fact, rather than re-asserting retention/egress specifics I would have to verify
independently (the finding's defect is a missing route, not wrong facts). Storage framing is
taken verbatim-in-substance from 7.2:41-60 (verified at fleet-v4.90.0 via the 7.2 chapter,
itself source-checked): MySQL system of record incl. Apple CA material encrypted; file/object
storage for installer/icon/bootstrap bytes; Redis transient; server private key + Windows
enrollment identity live outside the DB in configuration; three separate disk-encryption
escrow chains. Egress recipients cited to their owning chapters (2.8 logs, 2.9/2.10 Apple,
2.12 Google, 2.13 CAs, 2.5 IdP, 6.6/A.11 MCP, Part VI integrations, 8.13 support diagnostics);
inbound = vuln feed (4.4). No new product claims beyond those already in the cited chapters.

Also: 0.1 gained a 7th reading path ("If you are conducting a privacy or data-protection
review...") -> the A.8 map anchor; the intro count "Six indexes" -> "Seven starting points"
(only occurrence, grep-confirmed; not a frequency-claim check target). A.10 gained: data
classification, data egress, data inventory and trust boundaries (D); personal data, privacy
review (P); retention (R); trust boundary (T) -> all route to the A.8 map. check-links 0
(anchor resolves); table-names/column-names/crossrefs/headings/cap-ids(367)/em-dashes/
absolutes/shell-placeholders/pinned-links/activity-names all green.

## round11 D-COMP4 (2026-09-05): endpoint-catalogue retrieval how-to

Added a "Retrieving the endpoint catalogue" how-to section to a.8 (after Version notes,
before the complete route catalog). Verified vs fleet-v4.90.0 (7c428c6e46):
- Route: `ue.GET("/api/_version_/fleet/rest_api", listAPIEndpointsEndpoint, ...)` at
  server/service/handler.go:618 (user-authenticated; session or API token).
- Free/OSS path server/service/api_endpoints.go: ListAPIEndpoints SkipAuthorization then
  returns fleet.ErrMissingLicense -> Premium only.
- EE path ee/server/service/api_endpoints.go:11-15: Authorize(api_endpoint, ActionRead)
  then apiendpoints.GetAPIEndpoints().
- authz server/authz/policy.rego ~1476-1488: allow read on object.type=="api_endpoint"
  for global admin OR any team admin only; all other roles denied.
- Response shape server/service/api_endpoints.go: listAPIEndpointsResponse wraps
  `api_endpoints` = []fleet.APIEndpoint; struct fields method, path, display_name,
  deprecated (NormalizedPath is json:"-", not serialized) — server/fleet/api_endpoints.go:13.

Register decision (JUDGMENT, diverges from the finding's literal "formal CAP + a.5 row"):
used the a.1 no-capability-row register (nine outcomes -> ten, eight rows) matching D-COMP3
one firing earlier, NOT a formal CAP. Reasons: (1) a formal CAP couples a.1's frontmatter
count to a new a.2 platform-matrix row + an a.5 interface row + a.5's recomputed interface
tallies (check-cap-ids assertions 8/9); (2) two structurally identical register additions in
the same round should be handled the same way; the honest state is taught-but-unrowed. The
capability's own permission (`api_endpoint · read`) already exists as an a.4 row, and its
API-only interface is noted in the register row prose. a.10 gained an "endpoint catalogue"
subject entry. Full checker suite exit 0 (links/em-dashes/cap-ids 367/register-counts/
crossrefs/headings/table-names/column-names/verified/absolutes/shell-placeholders/pinned).

## D-COMP6 (round 11) — the shared response and error contract

Added a "The shared response and error contract" section between "API conventions" and
"Where the rest lives", per round-10 FINDINGS §D COMP-6 ("add an API request/response
contract layer for a.8"). SCOPE call (bounded, my judgment): documented the *shared
envelope* every JSON route uses, NOT per-endpoint request/response bodies. Per-endpoint
shapes stay deferred to Fleet's own REST reference (a.8 has always declined them, and
reproducing hundreds of bodies would rot per release and duplicate Fleet's reference). The
envelope is stable across releases and verifiable, so it is the reference-appropriate slice.

Verified vs fleet-v4.90.0 (7c428c6e46):
- Error envelope: `server/platform/endpointer/transport_error.go` — `JsonError{Message,
  Code(omitempty), Errors []map[string]string(omitempty), UUID(omitempty)}`; `EncodeError`
  maps error class -> message + status: validationErrorInterface -> "Validation Failed" 422
  (or the error's own Status() if it implements one), permissionErrorInterface ->
  "Permission Denied" 403, NotFoundErrorInterface -> "Resource Not Found" 404,
  ExistsErrorInterface -> "Resource Already Exists" 409, conflictErrorInterface ->
  "Conflict" 409, badRequestErrorInterface -> "Bad request" 400. `errors` entries use
  {name, reason} (baseError uses name:"base"). 401 (missing/invalid credential) and 402
  (license, `licenseError.StatusCode()` = PaymentRequired, per C2) are raised around the
  handler, so they are named as out-of-table.
- Success envelope: `server/platform/endpointer/endpoint_utils.go` generic encoder — default
  200; `statuser` responses set their own status; `204 No Content` returns empty body. Body
  is the JSON-marshalled response struct (top-level object keyed by resource name; embedded
  `Err error json:"error,omitempty"` absent on success because the error path is taken via
  Errorer/EncodeError first).
- List envelope: resource under a named field (`hosts` = `listHostsResponse` at
  server/service/hosts.go:107; `activities`), `meta *fleet.PaginationMetadata json:"meta"`
  with `has_next_results`/`has_previous_results` (server/fleet/meta.go:8), some responses add
  a top-level `count` (e.g. listHostUpcomingActivitiesResponse at activities.go:48).
  PaginationMetadata.TotalResults is `json:"-"`, so not surfaced as `count`; `count` is a
  separate per-response field, hence "some list responses add".
- Forwards-compat key duplication: the generic encoder's `aliasRules`/`DuplicateJSONKeys`
  path emits old+new keys for a renamed field (endpoint_utils.go ~1218). Ties to 6.3's
  "renamed fields" section.

Adjusted "Where the rest lives" so it no longer contradicts the new section: it now says it
gives method/path/auth "and the shared envelope above" and defers only *per-endpoint*
bodies/fields/parameters (previously it said it did not reproduce "response shapes ... or
error codes", which the new section now does at the envelope level). Pure prose + one
6-row class->status->message markdown table + two code blocks; no CAP, no register row, no
counted-table change, so cap-ids/register-counts untouched. Cross-refs to 6.3 anchors
(#page-filter-and-order-complete-result-sets, #the-renamed-fields-which-will-bite-you-on-a-write,
#handle-errors-limits-and-ambiguous-writes) validated by check-links. Full suite exit 0.
