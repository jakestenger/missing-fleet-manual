---
section: "A.1"
---

# a.1 Capability index, citation ledger

Drafted 2026-08-29 from a completed research pass that covered all 348 rows of the shared capability
register with no sampling. Held to Part IX's enumeration line and to the ruling in the same file that
**a.1 is the synonym layer and nothing else** ([`../appendix-structure.md`](../appendix-structure.md)).

**The research is the authority and was not redone.** It lives outside this repository at
`../../missing-fleet-manual-private/research-sensitive/a.1-index-research.md`, and carries the row
universe, the per-row synonym evidence with its `path:line` citations, the eight-group proposal, and
the coverage findings. Row identities come from
`../../missing-fleet-manual-private/research/capability-register.md`.

**What drafting added was arithmetic.** Every number the appendix prints was recounted mechanically
at `fleet-v4.90.1` (`dd0200f062`) or against the manual on disk before it was published, and eleven of
those recounts disagreed with the research. They are the first section below, because a synonym index
whose counts are wrong is worse than one with no counts in it.

## Counts recounted at the tag, and where the research was wrong

| Published in a.1 | The research said | Recount | Basis |
|---|---|---|---|
| **98 hand-written keyword lists** in the command palette | 101 | 98 | `grep -c 'keywords: \['` across `frontend/components/CommandPalette/groups/*.ts`: 5 in `automations.ts`, 25 in `commands.ts`, 20 in `controls.ts`, 9 in `mdm.ts`, 10 in `pages.ts`, 23 in `settings.ts`, 7 in `software.ts`. `derivations.ts` has none. One further `keywords` occurrence in `automations.ts:94` is a comment |
| **47 route aliases covering 58 deprecated paths** | "roughly 47 deprecated route paths" | 47 alias entries, 58 deprecated method-and-path pairs | `server/service/handler_deprecated_paths.go`: 47 `Method:` entries, and 58 strings inside the `DeprecatedPaths` slices, all distinct. 34 are team-shaped and 17 query-shaped |
| **44 deprecated GitOps keys** | not counted | 44 | `pkg/spec/gitops_deprecations.go`, `DeprecatedGitOpsKeyMappings`. Agrees with the 44 [a.7](../../manual/09-appendices/a.7-fleetctl-command-reference.md) publishes |

**The vendor-coverage column was wrong in eleven rows**, always in the direction of overstating the
gap. Recounted with word-boundary matching over `manual/**/*.md`, excluding a.1 itself, and split
between chapters (Parts 0 to VIII) and appendices:

| Term | Research | Chapters at recount |
|---|---|---|
| `AMAPI` | "zero occurrences in this manual" | **7** |
| `Managed Google Play` | "zero headings, neither word appears" | **3** |
| `LUKS` | "zero manual files" | **8** |
| `EST`, `PKI`, `Hydrant` | "all absent from the manual" | EST **0**, Hydrant **0**, PKI **1** (8.12) |
| `NDES`, `DigiCert`, `Smallstep` | implied absent with the group above | **2**, **1**, **2** |
| `DDM` | 2 files | **1** (8.8); `declarative device management` **3**, not 4 |
| `work profile` | 9 files | **6** |
| `Nudge` | 3 files | **1** chapter, plus a.3 |
| `Lost Mode` | 2 files | **1** |
| `Azure` | 3 files | **1** chapter (2.3, about cloud hosting). `Azure AD` **0** |
| `Okta` | 5 files | **3** chapters; the other two hits are a.4 and a.8 |

**The strongest claim in the research turned out to be false, and the replacement is stronger.** The
research said seven terms have zero heading coverage in all of Fleet's own documentation: Managed
Google Play, AMAPI, OMA-URI, SyncML, LUKS, Azure AD and Apps and Books. Counting `^#{1,6}` headings
across `docs/` and `articles/` at the tag: **only Managed Google Play, AMAPI and OMA-URI have zero.**
SyncML has 2 (`## SyncML structure`, `## SyncML`), LUKS 2 (`### LUKS (Linux)`, `### Escrow LUKS
data`), Azure AD 1 (`### Azure AD join`) and Apps and Books 1 (`### Apps and Books integration`).

So the appendix publishes the inverse claim instead, which is checkable and carries more force: **ten
of the vendor words appear in no chapter of this book** (Azure AD, LDAP, Workspace ONE, Kandji, Munki,
LAPS, EST, Hydrant, OMA-URI, Managed Apple ID), and **Fleet documents most of them**. Heading counts
at the tag: `EST` 14, `Jamf` 26, `Kandji` 8, `Munki` 8, `Hydrant` 4, `Workspace ONE` 3, `LAPS` 1,
`Active Directory` 1, `Managed Apple ID` 0. `OMA-URI` is the one word with zero headings in Fleet's
documentation **and** zero occurrences in this book's chapters, which makes it the single best row in
the appendix.

## Established at the tag

| Claim | Basis | Evidence |
|---|---|---|
| The fourteen vocabulary clashes are live at 4.90.1, and seven of them are defects | Stated | Re-verified individually, below |
| `dep_syncer` is a job name inside the schedule `apple_mdm_dep_profile_assigner` | Stated | Job registered in `cmd/fleet/cron.go`; schedule name in `server/fleet/cron_schedules.go:17`. Fleet's own documentation calls it "the `dep_syncer` cron job" at `docs/Contributing/architecture/mdm/automated-device-enrollment.md:39` and `docs/Contributing/product-groups/mdm/mdm-overview.md:182` |
| `app_enable_report_stats` is documented and not registered | Stated | Documented at `docs/Configuration/fleet-server-configuration.md:1007`. The server registers `app.enable_scheduled_query_stats` at `server/config/config.go:1440`, backed by the field at `:251` |
| Fleet's startup message names an unregistered key one line above the working flag | Stated | `cmd/fleet/serve.go:1186` and `:1203` print `updates.allow_missing_migrations`; the registered key is `upgrades.allow_missing_migrations` at `server/config/config.go:1750`; `serve.go:1187` and `:1204` give the correct `--upgrades_allow_missing_migrations` |
| `logger_path` is documented where osquery's flag is `logger_plugin` | Stated | `docs/Configuration/agent-configuration.md:45` documents `logger_path`. Fleet's own guide uses `--logger_plugin=tls` at `docs/Contributing/guides/enroll-hosts-with-plain-osquery.md:54` and `:80` |
| The environment-variable renames are still accepted | Stated | `DELETE_OTHER_FLEETS` with `DELETE_OTHER_TEAMS` at `cmd/fleetctl/fleetctl/gitops.go:54`, deprecation notice `:97`. `REPORT_NAME` with `QUERYNAME` at `query.go:78`, notice `:32`. `CERTIFICATE_RENEWAL_ID` with legacy `SCEP_RENEWAL_ID` at `server/fleet/mdm.go:92-93`, both matched by the regexp at `:133-134` |
| The three per-host channel variables are the real names | Stated. **Expanded from the research's `ORBIT_*_CHANNEL` wildcard**, because STYLE §26 makes a path with an unenumerated placeholder a template rather than a fact | `ORBIT_ORBIT_CHANNEL`, `ORBIT_OSQUERYD_CHANNEL`, `ORBIT_DESKTOP_CHANNEL`, the only three matching `ORBIT_[A-Z_]*CHANNEL` in `orbit/` and `cmd/` |
| `vulnerabilities.disable_schedule` is the key for moving vulnerability processing off the serving instances | Stated. **Added during drafting**, because the research gave the outcome and no key | `server/config/config.go:1727`, field at `:732`, read at `:2102` |
| `disable_events` is a name administrators actually type | Stated | Used as an agent command-line flag in Fleet's own repository configuration, `it-and-security/fleets/testing-and-qa.yml:45`, and in the Terraform provider tests |
| The SCIM attribute clash is between two of Fleet's own documentation pages, and the disputed attribute is `email` | Stated. **Corrected during drafting**: the first draft invented `userName` and `active` as the disputed pair | `manual/02-administer-and-deploy-fleet/2.5-identity-providers-sso-scim-and-role-sync.md:210`, which records the SSO page listing `email` among the required attributes while the host-vitals guide lists only `userName`, `givenName` and `familyName` |
| The manual contradicts itself on channels against families | Stated | `manual/01-foundations/1.2-how-fleet-reaches-a-device.md:129` heading "The five channels" over `:131` "five families" |
| `fleet` means both a scope and the estate inside this book | Stated | `manual/05-manage-devices/5.4-manage-software-and-applications.md:472` heading "Automatic updates update your library, not your fleet"; `manual/04-know-your-devices/4.5-monitor-fleet-wide-state.md:2` and `:18` "Monitor fleet-wide state" |
| Nineteen coined terms are this manual's and appear nowhere in Fleet | Stated for the manual half | Every coinage in the table was grepped against `manual/`; all nineteen resolve to the chapter the table names, and `sentinel`, `fleet move`, `re-fire`, `endpoint restrictions`, `break-glass` and `families` also appear in neighbouring chapters, which is why the table names where each is **defined** rather than where it appears |
| Group counts 32, 66, 8, 57, 98, 23, 44, 20 | Stated, and enforced | The build script asserts each group's printed count against the rows in that group's table, and the three group 5 sub-tables against 30, 52 and 16. It refuses to write the file otherwise |

## Deliberately not established

**Four things are open and the appendix does not paper over any of them.**

**CAP-048 is a row here and is merged into CAP-029 in a.2.** a.2's own ledger records the merge and
says the shared register still carries both, with a note to apply it before a.1 projects from the
register again. It was not applied. a.1 keeps both rows on purpose, because the two are distinct
**reader intents** landing on different chapters, "personal Mac" in 3.2 and "personal iPhone" in 3.5,
even though they are one platform contract. **The consequence is real and is recorded rather than
hidden: a reader following CAP-048 into a.2 will not find that identifier.** The clean fix is a
register decision rather than an appendix decision, and it belongs to whoever reconciles the register.

**a.2's four added capabilities have no a.1 row.** CAP-349 to CAP-352 were verified into a.2 during
its review rounds and never entered the register the a.1 research read, so they are outside the 348.
Three of the four are reachable through CAP-065, the end-user surface row, which is itself unowned.
Adding rows for them would have meant inventing synonyms, which is the one thing this appendix may not
do.

**Two symptom rows were assigned a chapter the research did not assign.** The research lists the
symptom entries with no capability row and says they "route to a chapter" without naming one. Where
the routing followed from an existing row it was taken from that row. Two did not: "my EDR is flagging
the fleetd agent" was routed to 3.8 then 8.4, and "switch to Fleet from Kolide Fleet" was **dropped**
rather than routed, because no chapter covers it and asserting `None` would have been a new coverage
claim beyond what the research checked. Fleet's own two removed-surface questions, "Where did the
Packs page go?" and "What happened to the Schedule page?", are in the closing section instead, where
the research had already established that packs have no owning chapter.

**CAP-006, the second factor, is published with the research's canonical chapter and the assignment is
weak.** 1.5 carries a substantial paragraph at `:121` about second-factor events being almost
unrecorded, which serves "why is my MFA not in the audit log" and not "how do I require a second
factor". 2.5 carries the configuration side at `:150`, as the break-glass account's authentication
method. The research checked ownership row by row and did not list CAP-006 among the seven unowned, so
its assignment stands here. **Raise it in coverage review.**

## The structural decisions, and the reasoning behind each

### The eight groups were adopted, and the appendix says why they are not part-shaped

The stub proposed five groups. The research tested them against all 348 rows and found the frame fails
at both ends and in the middle: identity and audit have no group, scoping has no group, diagnosis has
no group at all, credential lifecycle straddles two, the setup experience straddles two, agent
management splits three ways, and device management swells to a third of the index. **Nothing in
drafting contradicted any of that**, and the eight-group recommendation was adopted whole.

**The appendix publishes the reason rather than the failure analysis.** A reader needs to know that
the groups deliberately cut across the parts, and that three of them do so by name. The seven ways the
five-group frame broke are drafting history and stay here.

**The trap the grouping exists to avoid is stated in the appendix's own words**: groups shaped like
the manual's parts produce a re-worded contents page. That sentence is the appendix's defence of
itself and it earns its place, because a reviewer who does not know the constraint will propose
exactly that shape.

### The synonym cell carries words, and nothing else

**This is the largest editorial decision and it removed a lot of material.** The research's synonym
column mixes attested words with bolded behaviour notes: "Fleet does not record which secret a host
used", "removing `update_channels` does not revert anything", "first-added wins". Every one is true
and interesting, and none is a word anybody types.

They were dropped. The part agreement says a.1 is the synonym layer and nothing else, and it forbids
capability support and licensing here by name. A behaviour note in this table would be a fourth copy
of a claim that a.2 owns as a platform cell and the chapter owns as prose, and duplication across
projections is the failure the shared register exists to prevent.

**The exception is a naming fact.** Where the behaviour note is *about the name*, it stays: Apple's
word is Lost Mode and Fleet's button says Lock; the host action reads Live report and its value is
`query`; Fleet's own documentation attributes the Windows key pair's effect to macOS. Those are
routing information.

### Six markers, and why an unmarked word is the common case

The research's ten source tags (`[K]`, `[R]`, `[P]`, `[G]`, `[C]`, `[A]`, `[U]`, `[V]`, `[M]`, `[X]`)
are provenance, and provenance belongs in the ledger. What a reader needs is not where a word was
found but **what to do with it**, and only five distinctions change that: the word still works, the
word is the vendor's and Fleet will not match it, the word is this book's, two live names disagree, and
the answer is no. `[a.6]` is the sixth and is a boundary marker rather than a source tag.

**Marking every word would have made the column unreadable.** The 348 rows carry 1,166 terms and 162
markers: 63 `(still accepted)`, 56 `(vendor)`, 16 `(clash)`, 14 `[a.6]`, 7 `(ours)` and 6 `(no)`. So an
unmarked word is the default and a marker is a signal. The alternative considered and rejected was
carrying the research's tags verbatim, which would have published a taxonomy of evidence classes to a
reader who came to find a chapter.

**One row of the 348 has an empty last column**, CAP-312, rotating an integration secret. The
convention is still stated in the appendix's legend, because a reader meeting that cell needs to know
it means the row's own words are the search words rather than that something was missed.

### The canonical chapter is a link and the secondary is a number

One link per row, 348 of them, plus the appendix cross-references. Secondaries are plain section
numbers. **The visual difference is the point**: the column with the link is the one to open, which is
what "one canonical chapter each" means operationally. Linking both would have doubled the file and
made the two columns look interchangeable.

### The symptom table sits inside group 8 rather than at the front

It is the appendix's highest-value content and it was still filed where it belongs, because a reader
mid-incident scans headings and "When it did not work" is the heading they scan for. It is named in
the opening section so a cold arrival finds it.

**Thirty-three sentences**, each a string Fleet prints, a question Fleet's own documentation asks, or a
phrasing this manual records. The middle column resolves an ambiguity and stops short of the fix,
because the fix is Part VIII's and reproducing it here would recreate the symptom-cause-fix table
STYLE §5 forbids.

### The coverage gaps are a section, not a footnote

Twenty-four items in three shapes: seven outcomes with no owning chapter, three whose prerequisite is
unowned, fourteen searchable capabilities with neither a row nor a chapter. All published, none
softened, no link invented for any of them. The a.7 pass established the rule and reached the same
verdict independently on two of them, the self-hosted update repository and supplying vulnerability
data yourself.

**The count was reconciled against its rows** (7 + 3 + 14 = 24) rather than asserted, which is the
defect a.7's ledger records from its own first pass.

### No images

The other seven appendices carry none, and an index is a lookup surface rather than a relationship to
draw. A candidate diagram showing the eight groups against the nine parts was considered and dropped:
it would have illustrated the appendix's structure rather than Fleet's, which is the meta-commentary
STYLE §23 rules out.

## The build is asserted rather than typed

The appendix was generated from tokenised source by a script that holds the chapter map and expands
`{{4.2}}` into a relative link. It asserts, before opening the target file for writing: every mapped
path resolves to a file that exists; no token in the body is outside the map; no token survives
expansion; no em-dash is present; no capability identifier appears on two index rows; the index holds
exactly 348 rows; each group's printed count matches its table; and the three group 5 sub-tables match
30, 52 and 16.

**This is the direct answer to CONTRIBUTING's two scripted-edit incidents.** The document is built
whole in memory and written once, so a failure leaves the previous file intact, and nothing is
substituted into existing prose by pattern.

## Checks

`check-links.py` 0 problems across 75 files. `check-em-dashes.py` clean. `check-crossrefs.py` and
`check-headings.py` report nothing in a.1. `unwrap.py dryrun` 0 changes, 0 signature mismatches.

`check-activity-names.py` verified every activity type published in the index against Fleet's source
and returned **one** finding, `macos_updates` at a.1:469, which is a false positive: it is a GitOps and
API field name (`server/fleet/teams.go:91`, `:329`, `:410`) sitting in a cell beside real activity
names. `check-schedule-names.py` verified all 34 schedule names and `check-table-names.py` all table
names, both clean, which covers `apple_mdm_dep_profile_assigner`, `mdm_service_discovery`,
`apple_mdm_iphone_ipad_refetcher`, `activity_past` and `cron_stats`.

`check-absolutes.py` reports three lines in a.1, all bounded enumerations the sentence itself makes.
`check-outline-deferrals.py` reports the a.5 pointer at a.1:30 with no `[PROMISE]` tag, identical in
shape to the one a.2 carries at its own line 30.

## Rounds

| Round | Verdict | Outcome |
|---|---|---|
| Research | Complete, all 348 rows, no sampling | Adopted whole: the eight groups, the group 5 sub-grouping, the one-row-one-group ruling, the explicit-absence ruling, and the coverage findings |
| Drafting recount | **Eleven counts wrong** | Palette lists 101 to 98; deprecated routes given exactly as 47 aliases over 58 paths; the vendor-coverage column recounted in eleven rows; the "seven terms with zero heading coverage" claim withdrawn and replaced with a checkable inverse |
| Drafting corrections | Four inventions caught in the draft's own first pass | Two SCIM attribute names invented and replaced with the attested four; an Apple service-discovery term invented and dropped; the `ORBIT_*_CHANNEL` wildcard expanded to its three real names; the carve mention list corrected from 7.3 to the eight chapters that actually mention it |
| Draft review 1, coverage | **Not run** | |
| Draft review 2, cell-by-cell evidence | **Not run** | |
| Draft review 3, fresh whole read | **Not run** | |

**Part IX sets three review rounds and none has happened.** The `status` is `drafting` and the
frontmatter carries no `reviewed_by`, which is the honest state. Coverage review should start with
CAP-006, the CAP-048 divergence and the four a.2 capabilities that have no row.

## Defects

**The a.1 research produced three defect candidates and all three are already recorded in it**: the
class C icon-upload conflict, and two class D naming findings in the same area. Nothing in drafting
re-verified them, and nothing new was found.

**One arithmetic discrepancy is worth settling before the next filing.** The research's closing line
reads "Queue after these: C54, D49, S18", while the queue as handed to this drafting pass stands at
**C54, D48, S18**. The research reports one class C finding and two class D findings, so one of the two
class D findings appears not to have been entered. The queue is authoritative; the missing entry is the
one to check.

**Two defect-shaped findings in this manual are published in the appendix as routing facts**, because a
reader searching either word needs both spellings, and they are recorded here as corrections the owner
may want to make rather than only to document: 1.2's heading says channels where its own next paragraph
says families, and 5.4 uses `fleet` for the estate in one heading while using it for a scope elsewhere
in the same chapter.

**One stale claim outside this appendix was found while drafting and not changed.**
`manual/00-Introduction/0.1-how-to-use-this-manual.md:143` tells the reader the platform capability
matrix "is not written yet" and gives a workaround. a.2 is drafted, 272 rows and 1,632 platform cells.
The line is 0.1's to fix and touching it was out of scope for this pass.

## 2026-09-02 fix: stale a.7 cross-reference in "Where this index ends" (round3 B4)

The closing "Where this index ends" section said a.7 "still lists" `setup` "without an owning
chapter." That was true when written but a.7 was fixed in the same round3 batch (2.2 now owns
`setup`, [[a.7-notes]]). Updated the sentence to reflect that every a.7 command group now has an
owning chapter, while keeping the unrelated point that the local evaluation sandbox still has no
capability row in this index (a.7 and a.1 track different granularities — that gap is real and
unchanged).

## 2026-09-02 fix: CAP-ID register regeneration (round3 B1+M1, folding in m2's investigation)

Round 3 found a.2 silently reusing six of a.1's live IDs (CAP-349-354) for six unrelated
capabilities, and inventing six more (CAP-355-360) nowhere in a.1. Cross-checking each of the
twelve against a.1 and Fleet source (fleet-v4.90.1) rather than just renumbering them:

- **One was a straight duplicate.** a.2's "Rotate the managed local account's password" is the
  same capability as a.1's existing CAP-353 ("Retrieve or rotate the managed local administrator
  password"), authored independently under a colliding ID. Reassigned to CAP-353, no new row.
- **Eleven were genuinely new capabilities** a.2's platform research had verified against source
  but a.1 had never registered. Six get real chapter homes and joined the main tables: CAP-361/362
  (My Device page and Fleet Desktop menu-bar summary, [5.5]), CAP-363 (`orbit shell`, [8.4]),
  CAP-364 (agent restart forces an immediate update check, [3.8]), CAP-365 (self-service uninstall,
  [5.5]), CAP-366 (Android Play self-service toggle, [5.4]). Five have no owning chapter at all —
  Fleet does them but no chapter teaches them — and joined "Where this index ends" instead of the
  main tables: CAP-367/368/369 (Chromebook lock/release/erase, refused outright at source, and
  [5.7]'s own platform matrix has no ChromeOS column to record the refusal in), CAP-370 (per-host
  MDM unenrollment independent of the platform-wide switch — a.4 authorises it, no chapter teaches
  invoking it), CAP-371 (Fleet's own agent-side FileVault key rotation on an undecryptable key).
- Total outcomes: 354 → 360 (six real rows). Group/subsection counts updated: group 2 (68), group
  5 (104, Experiences 21), group 8 (21).

Also fixed the "How to read a row" promise that a.4 carries the same CAP-ID: it does not (152
administrator intents is a coarser grouping than 360 outcomes), corrected to name a.2/a.5 only, per
the finding's own sanctioned alternative rather than fabricating an unreliable a.4 crosswalk.

**m2's investigation, not adopted as a fix.** The round3 finding "a.1 has no capability row for
`fleetctl preview`" turns out to describe a.1's own long-standing, deliberate, documented design
decision (see "The local evaluation sandbox" in this same "Where this index ends" section, present
before this pass) — not a defect. Left as-is; see FIX-STATE.md's ledger for the SKIP reasoning.

New machine check added: `build/check-cap-ids.py` verifies every CAP-ID a.2 or a.5 uses exists in
a.1, and that a.2/a.5 agree verbatim wherever they carry the same row — the two checks a plain
uniqueness check inside one file cannot catch, and the exact shape of this bug. Six pre-existing
a.2/a.5 label mismatches surfaced by the new check (CAP-178, 189, 196, 228, 243, 275) were aligned
to a.2's wording, which cross-checking against source found more accurate in every case (a.5's
versions were narrower than the row's real platform scope, e.g. "Prepare a Mac" for a cross-platform
setup-experience row).

## 2026-09-02 fix: frontmatter row count never updated after the 354→360 growth (round4 RB1)

The CAP-361-to-371 growth recorded above (this same file, same date) updated every in-body count —
"360 outcomes", the group subtotals, the "How to read a row" cross-reference — but missed the
frontmatter's own `verified_source` field, which still said "a pass over all 354 rows". A reader
citing the frontmatter as the appendix's own claim about itself would get the pre-growth number.
Recounted the actual `CAP-###` table rows directly (360, confirmed by `grep -c` and independently by
`build/check-cap-ids.py`'s row-count assertion) and corrected the frontmatter to match. No other
number in the body needed touching; this was the one place the fix from earlier today didn't reach.

This is exactly the escape pattern RB1 named: a fix that touches the file it started in and stops,
leaving a sibling claim (here, a frontmatter field in the same file) stale. `check-cap-ids.py` now
asserts the frontmatter count against the actual row count on every run, so this specific drift
cannot recur silently.
