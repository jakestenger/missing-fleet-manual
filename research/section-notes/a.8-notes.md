# a.8 API action and endpoint reference: citation ledger

Written 2026-08-25 against `fleet-v4.90.1`. Bases per STYLE §27, where **stated** means the cited
source establishes both the content and the scope of the claim.

## Stated

| Claim | Source |
|---|---|
| Every endpoint is registered through one of six authenticators: user, host, orbit, device, android, and no-auth | `server/service/handler.go:300,938,984,1039,1044,1071` |
| Declared API versions at this release are `v1` and `2022-04` | `server/service/handler.go:296` |
| A `latest` alias is appended to whatever versions are declared, and is a registered path rather than a redirect | `server/platform/endpointer/endpoint_utils.go:878,1147` |
| API tokens are tied to a Fleet user account and sent as `Authorization: Bearer <token>` | `docs/REST API/rest-api.md:49-56` |
| A token can be obtained from **My account > Get API token** or from the login endpoint | same |
| Email and password login is disabled for SSO and MFA users, who must take the token from the profile page | same, `:59` |
| Pagination uses `page`, `per_page`, `order_key`, `order_direction`, with `page` zero-based in Fleet's own example | `docs/REST API/rest-api.md:542` |
| Apple's SCEP and MDM protocol paths sit outside `/api` because they are not RESTful and not for API clients or browsers | `docs/Get started/FAQ.md`, What API endpoints should I expose |
| The full public-exposure matrix by platform and feature | `articles/what-api-endpoints-to-expose-to-the-public-internet.md:20-84` |

## Derived

| Conclusion | From | Reasoning |
|---|---|---|
| Reading the API as six classes of caller is the useful model | The six authenticators above | Fleet's reference is organized by resource, not by caller. The reframing is the book's and is the reason this appendix exists in this shape |
| A proxy or allowlist rule matching `/api/v1/` will miss traffic on the other two paths | The three registered paths, plus Fleet's own docs using `v1` and `latest` interchangeably | Fleet does not warn about this; the consequence follows from the registration behaviour |
| Separate orbit and osquery node keys mean a host can be half-working | The distinct orbit and host authenticators, plus the separate node keys established for 3.1 | Fleet documents the keys separately and does not draw this conclusion |
| The device class is the one most often missed in network planning | The exposure matrix includes device paths that are easy to omit | Judgement, not a Fleet claim |

## Unverified

Nothing in this appendix is asserted beyond the rows above. Where a boundary was not established,
the text does not claim one.

**Specifically not claimed**: how the `2022-04` version differs in behaviour from `v1`, if at all.
The registration was verified; the semantics were not, and no source at the tag was found stating
whether the two differ. The appendix says both paths exist and stops there.

## Scope decision

Written under the completeness standard recorded in `CONTRIBUTING.md` on 2026-08-25. This
appendix carries the model, the authentication rules, the versioning scheme and the exposure
matrix, and points at Fleet's reference for per-endpoint parameters rather than copying them.

Effect on the manual's cross-references: `build/check-crossrefs.py` previously flagged 2.6's
deferral to a.8 as reaching nothing. That warning has cleared. The remaining warning of that class
is 2.3's deferral to a.4, which is still an outline.

## Checks run

`check-links`, `check-crossrefs`, `check-absolutes`, `check-headings`, `check-activity-names`,
`unwrap`, site build. Whole-appendix consistency read performed, and read against 2.6, 2.7, 2.8,
3.1 and 3.7, which are the chapters that defer here or describe the same paths.
