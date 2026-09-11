# Open Questions and Blockers

## 4.1 Four open architecture questions (D3.3 core)

Four questions, raised during design discussion, remain unresolved and should be answered before
substantial engineering investment in the trigger/orchestration piece (Section 2.1), since each shapes
the data model or the operating model rather than an implementation detail:

1. **How frequently will users create new notebook templates**, as opposed to running existing ones?
   This determines how much the authoring workflow needs to optimise for: a rare, heavier-weight
   activity for a small trusted group looks different from a frequent one needing a smoother UI.
2. **How frequently will users copy and run a template** for a new area or event? This determines
   compute and job-queue sizing, and whether pre-computation (see the baseline-strategy question in
   D2.3, Section 4.1) is worth the engineering investment.
3. **How "published" versus "scratchpad" should this be**: how authoritative and curated do outputs
   need to be, versus how much exploratory, un-reviewed analysis should the platform tolerate? This
   affects whether every run is discoverable by default or whether there is a review/promotion step
   before something becomes a citable, shareable artefact.
4. **Who is responsible for keeping the notebook catalogue tidy** over time, so that it does not become
   a graveyard of outdated, superseded analyses? This is a governance question, not a technical one, and
   needs an owner independent of who builds the platform.

These do not need certain answers before any engineering starts; a first, minimal implementation can
proceed on reasonable defaults. They should be explicitly discussed and provisionally answered rather
than left implicit, since the answers change the shape of the trigger/orchestration piece's data model,
in particular whether "published" status is a first-class field from day one.

**Current expectation.** The working assumption for questions 1 and 2 is a small number of trusted users
authoring notebooks, or forking an existing one for a new country, rather than a large open user base.
This should keep the authoring workflow and its authentication needs modest in scope (Section 4.2).

## 4.2 Authentication approach

The request for this platform includes a light authoring and authentication layer so that select users
can create notebooks. This is lower-risk than it might first appear: Montandon's own staging API already
authenticates users via IFRC's existing OpenID Connect identity provider, issuing Bearer tokens through
IFRC's `go.ifrc.org` platform, and this is already the mechanism IFRC users use today to
access Montandon data from notebooks. The straightforward path is for the trigger/orchestration piece to delegate
authentication to that same identity provider, rather than building or maintaining a separate user
store, restricting the authoring capability (as opposed to browsing published results) to a defined set
of authorised accounts within it. This is a design recommendation, not yet a confirmed decision, and
should be validated with whoever owns that identity platform on the IFRC side. There is also a
lower-effort fallback if time runs short: trigger runs manually via GitHub, with the project team as the
only authenticated users, needing no external identity integration at all. Either path keeps this piece
low-risk.

## 4.3 Shared dependency: baseline data strategy

The baseline risk-exposure computation-strategy question raised in D2.3 (Section 4.1), whether to
compute on demand, on a schedule, or once for all countries/hazards, directly affects this platform too,
since it determines whether Use Case 1's template notebook needs to run a real computation per request
or simply reads a precomputed dataset. That decision is not re-litigated here; resolving it (D2.3,
Section 5, item 1) has a direct, simplifying effect on this platform's design.

## 4.4 Realism of the WP3 timeline against the Readiness Review meeting

Given that D3.1, D3.2, and D3.4 are all sequenced after D3.3 reaching at least a minimal working state,
and D3.1 is planned to start in October, none of the three should be presented as demonstrable by the
Readiness Review meeting. The meeting should instead be used to confirm this sequencing is accepted and
get agreement on the phased plan in Section 5.
