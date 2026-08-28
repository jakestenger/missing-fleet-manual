# Section notes

Two kinds of file live here, and only one of them is in this repository.

**Citation ledgers** (`5.4-notes.md`, `8.2-notes.md`, and so on) stay here. They record what a
chapter claims and on what basis, separating what was source-checked from what was derived and what
remains unverified, plus what was rejected and why.

**Working research notes** for Part V are **not here.** They are at
`missing-fleet-manual-private/research-sensitive/`.

## Why the working notes moved, 2026-08-28

This repository is public. While researching 5.8, whose subject is credentials that decrypt disks,
the independent reviewer set an explicit disclosure line and then found the research notes had
crossed it. A sweep found the same shape in Part V's other notes: several described, in actionable
detail, how to reach credentials or authorization gaps that are **unfixed at this release**.

The chapters themselves are written to the disclosure line and say what an administrator needs:
which roles can reach what, that certain reads are logged or state-changing, and how to handle
credential material. They do not describe the routes. Leaving the routes in the working notes, in a
public repository, would have defeated that with no benefit to any reader.

**No exposure occurred.** The notes were moved while the branch was unpushed, and the affected
commits were purged from history in the same pass.

## The rule

**Research notes inherit the disclosure line of the chapter they support.** They are the easier of
the two to forget, because nobody reviews them as prose. When a chapter's subject is sensitive, keep
its working notes out of this repository and cite them from the ledger instead.
