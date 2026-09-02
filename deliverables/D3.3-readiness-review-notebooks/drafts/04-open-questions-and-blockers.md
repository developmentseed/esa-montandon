# Open Questions and Blockers

## 4.1 Four open architecture questions (D3.3 core)

Four questions, raised during design discussion, remain genuinely unresolved and should be answered
before substantial engineering investment in the Django platform, because each shapes the data model or
the operating model rather than an implementation detail:

1. **How frequently will users create new notebook templates**, as opposed to running existing ones?
   This determines how much the authoring workflow needs to optimise for — a rare, heavier-weight
   activity for a small trusted group looks different from a frequent one needing a smoother UI.
2. **How frequently will users copy and run a template** for a new area or event? This determines
   compute and job-queue sizing, and whether pre-computation (see the baseline-strategy question in
   D2.3, Section 4.1) is worth the engineering investment.
3. **How "published" versus "scratchpad" should this be** — i.e., how authoritative and curated do
   outputs need to be, versus how much exploratory, unreviewed analysis should the platform tolerate?
   This affects whether every run is discoverable by default or whether there is a review/promotion
   step before something becomes a citable, shareable artefact.
4. **Who is responsible for keeping the notebook catalogue tidy** over time, so that it does not become
   a graveyard of outdated, superseded analyses? This is a governance question, not a technical one, and
   needs an owner independent of who builds the platform.

We do not think these need to be answered with certainty before any engineering starts — a first,
minimal implementation can proceed on reasonable defaults — but they should be explicitly discussed and
provisionally answered, rather than left implicit, since the answers meaningfully change the shape of
the Django data model (in particular, whether "published" status is a first-class field from day one).

## 4.2 Authentication approach

The user's request for this platform explicitly includes "a light authoring and authentication layer so
that select users can create notebooks." We believe this is lower-risk than it might first appear:
Montandon's own staging API already authenticates users via IFRC's existing OpenID Connect identity
provider (issuing Bearer tokens through IFRC's `goadmin-stage.ifrc.org` platform), and this is already
the mechanism IFRC users use today to access Montandon data from notebooks. The straightforward path is
for the Django platform to **delegate authentication to that same identity provider**, rather than
building or maintaining a separate user store — restricting the *authoring* capability (as opposed to
browsing published results) to a defined set of authorised accounts within it. This is a design
recommendation, not yet a confirmed decision, and should be validated with whoever owns that identity
platform on the IFRC side.

## 4.3 Shared dependency: baseline data strategy

The baseline risk-exposure computation-strategy question raised in D2.3 (Section 4.1) — whether to
compute on demand, on a schedule, or once for all countries/hazards — directly affects this platform
too, since it determines whether Use Case 1's template notebook needs to run a real computation per
request or simply reads a precomputed dataset. We do not re-litigate that decision here; we flag that
resolving it (D2.3, Section 5, item 1) has a direct, simplifying effect on this platform's design.

## 4.4 Realism of the WP3 timeline against the Readiness Review meeting

Given that D3.1, D3.2, and D3.4 are all sequenced after D3.3 reaching at least a minimal working state,
and D3.1 is explicitly planned to start in October, we think it is unrealistic to present any of the
three as demonstrable by the Readiness Review meeting. We would rather use the meeting to confirm this
sequencing is accepted and get agreement on the phased plan in Section 5, than imply readiness that does
not exist.
