# A.10 subject index — section notes

## Fix-loop round (2026-09-02, round4 RM11)

Second wave of missing front-door terms, same defect class as round-3's M16 (a different eight
terms, no overlap). Confirmed via direct grep that A.10 had zero hits for: endpoint allowlist,
observer-plus, managed local account, CSP, LocURI, OMA-DM, OOBE, ESP, CVSS, EPSS, healthz,
sysdiagnose, Prometheus.

- **observer-plus:** no fix needed under that spelling. Round4 m5 (this same fix loop, earlier
  batch) corrected every book occurrence of the hyphenated form to canonical **Observer+**, which
  A.10 already indexes. The hyphenated term no longer appears anywhere in `manual/`.
- **managed local account:** added as an alias pointing at the existing "LAPS and the managed
  local administrator account" entry rather than duplicating it.
- Added: CSP (owning section 8.9, §8.9.6), endpoint allowlist (6.6 + A.11), EPSS (4.4), ESP (5.5),
  healthz (8.14 + 8.3), LocURI (8.9), OMA-DM (8.9 + 1.2), OOBE (5.5), Prometheus (7.4),
  sysdiagnose (8.2 + 8.8).
- Each entry's owning section was picked by finding where the book actually explains the term
  (not just mentions it), same standard A.10's frontmatter already commits to.

A.10 has no generated/systematic coverage check, so this defect class (new vocabulary entering
the book without an index entry) will keep recurring; a future round could consider generating a
candidate-term list from bolded first-use spots and diffing it against A.10's headword list.

## Round6 M12 (2026-09-03) — index routes for account lifecycle + MFA

Added: "account lifecycle" (see -> user account, A); "MFA" (see -> two-factor
authentication, M); "second factor" (see -> two-factor authentication, S); "two-factor
authentication" (2.6 to enable, 1.5 for the audit caveat, T); "user account" (2.6, U).
Closes the M12 reference-test dead-ends ("Enable email MFA", role/account lifecycle). Owning
sections picked where the book actually teaches the thing (2.6), same standard as the rest of
A.10. links=0.

## Round6 M14 (2026-09-03) — privacy/data-boundary vocabulary added

Added index routes for the privacy-review vocabulary the finding flagged as missing: data
classification (see), data egress, data inventory and trust boundaries (D); personal data
(see), privacy review (see) (P); retention (R); trust boundary (see) (T). All resolve to the
new A.8 map anchor. Closes the M14 reference-test dead-end ("conduct a privacy review").
links=0.

## round6 M17: declaration asset routes (2026-09-03)

Added "declaration asset" (D) routing to 5.2#declaration-assets and 8.8#888-ddm-declarations, plus
an "asset (Apple DDM)" see-reference (A). Closes the M17 dead-end where A.8 emitted the five asset
routes but no index term led a reader to the workflow that makes them usable. links=0.

## 2026-09-04 fix: subject-index routing for first-run setup (round8 MJ-H)

Added "first administrator" (see first-run setup) and "first-run setup" ->
2.2#complete-first-run-setup under F, a new ## I section carrying "initialize the server" (see
first-run setup), and "setup screen" (see first-run setup) under S. Disambiguated from the device
"setup assistant" / "setup experience" entries that route to 3.2/5.5. Full source citation in
[[a.1-notes]].

## 2026-09-04 fix: subject-index routing for the go-live decision (round8 m14)

Added "go-live decision" (G, see production readiness), "handoff and handover" (H, see production
readiness), "production readiness" (P) -> 7.7#the-go-live-decision plus the 2.1 pilot cross-ref, and
"readiness" (R, see production readiness). m14 asked to extend a.1's no-capability-row register to
cover the go-live decision; research showed the go-live decision is the book's own synthesized
readiness gate (7.7:154-164), not a Fleet-attested capability, so it fails that register's criterion
("attested in Fleet but have no capability row") the same way the manual-assembled infrastructure
intake checklist was re-audited out (a.1:768). The reviewer's real concern is searchability, so it
is served here in a.10 rather than by a false register row; the a.1 register stays at eight (first-run
setup only, MJ-H). links=0, crossrefs/headings=0.
