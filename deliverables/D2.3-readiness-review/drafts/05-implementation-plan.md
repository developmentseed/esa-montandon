# Implementation Plan

This plan sequences the work needed to move each use case from its current state (Section 2) to a
demonstrable one, resolves the open questions in Section 4 where they gate that work, and is scoped to
land ahead of the Readiness Review meeting on 14 September 2026 wherever realistic, with a small number
of items explicitly carried into full WP2 execution rather than forced into the MTR window.

## Immediate (before the Readiness Review meeting)

1. **Decide the baseline-computation strategy for UC1** (Section 4.1). We recommend option 2 or 3
   (scheduled or full pre-computation, published to cloud storage) over recomputing on demand, because
   it also resolves the notebook-vs-Streamlit duplication by giving both a common data source to read
   from. This is a decision, not new engineering, and should be made this week.
2. **Add wildfire exposure data to UC1**, closing the last gap in the four-hazard baseline set.
3. **Run UC2 end-to-end against one real, recent event** (a live or recent Copernicus EMS activation)
   and get it reviewed by an IFRC or MapAction domain expert. This is the single most valuable thing we
   can do to convert UC2 from "implemented" to "validated" before the meeting.
4. **Progress the database remediation** (Section 4.2) as far as staging-cluster access allows — at
   minimum, complete the index cleanup on the highest-bloat partitions, since this is the change most
   likely to visibly affect notebook responsiveness before the meeting.
5. **Bring forward early findings from the National Society interviews** (Section 4.4), even if the
   full interview round is not complete, so the Readiness Review discussion is grounded in what
   operational users have actually said so far.

## Short-term (through end of September 2026)

6. **Decide and communicate UC3's MTR scope** (Section 4.1) — a full implementation, a defined narrower
   slice, or a specified-but-deferred status — so effort is not spent building against an unconfirmed
   target.
7. **If UC3 is in scope for a partial build**, start with the exposure × impact × vulnerability
   composite (reusing UC1 and UC2 outputs directly), deferring the historical-burden and
   operational-gap-and-accessibility components — both explicitly marked optional in the specification
   — to full WP2 execution.
8. **Resolve the remaining database work**: complete the vacuum/reindex pass, apply the autoscaling
   settings tuned to the cleaned-up database, and revisit the `context=off` and write-load settings
   proposed during the investigation.

## WP2 execution (beyond MTR)

9. **Complete the National Society interview round** and feed findings back into use-case refinement —
   particularly relevant if any interviewed National Society flags a use case as lower-priority or
   surfaces a need the current three do not cover.
10. **Reconcile UC1's notebook and Streamlit interfaces** into the single, agreed user experience implied
    by the baseline-computation decision in item 1, rather than maintaining both indefinitely.
11. **Build out the historical-burden and operational-gap components of UC3**, if deferred per item 7,
    once UC1 and UC2 are stable and validated.
12. **Resolve the statistics-export question** (Section 4.3) as the aggregate-reporting need becomes
    concrete — most plausibly once `montandondata.org`'s public reporting requirements are firmer.

## Ownership

Database remediation is owned within the platform engineering effort, currently gated on staging-cluster
access; escalating that access is itself an action item for this plan. UC1 notebook and application work
is owned by MapAction, with Development Seed supporting infrastructure and hosting. UC2 and UC3
notebook development follows the same MapAction-led, Development-Seed-supported pattern. We recommend
naming a single decision-owner for the baseline-computation strategy (item 1) and the UC3 scope decision
(item 6) at the Readiness Review meeting itself, since both are currently open questions rather than
assigned tasks.
