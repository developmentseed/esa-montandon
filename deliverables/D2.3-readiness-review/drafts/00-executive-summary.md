# Executive Summary

This report is deliverable D2.3 of the ESA "Application Development concerning Disaster Data and
Analytics" activity. It is the **readiness review** for Work Package 2: an honest status check, ahead
of the Readiness Review meeting, on how close the three crisis-analytics use cases — population and
infrastructure risk exposure, post-disaster impact estimation, and operational response prioritisation
— are to being usable, what stands between them and that state, and the plan to close the gap.

Where deliverable D2.2 (July 2026) assessed the pipeline's **architecture** — the design that would let
structured disaster data and EO hazard layers be combined automatically — this report assesses
**execution**: what has actually been built against that design, and what has not.

## Where things stand

Progress is real but uneven across the three use cases, and none is yet at a state a National Society
user could pick up unassisted.

- **Use Case 1 (Risk Exposure)** is furthest along. MapAction has delivered the baseline
  exposure-calculation notebooks and ported them into a Streamlit interface (open for review), covering
  three hazards with a fourth — wildfire — still to be added.
- **Use Case 2 (Impact Estimation)** has an initial notebook implementation opened for review this
  week. It has not yet been exercised against a live event end-to-end.
- **Use Case 3 (Response Prioritisation)** is the most developed on paper — its methodology, data
  sources, and worked example are fully specified in the D2.4 use-case narrative — but has no notebook
  implementation started, and depends on outputs from Use Cases 1 and 2 that are themselves still
  forming.

## Confidence

We have **medium-high confidence** in Use Case 1 reaching a usable state on schedule, **medium
confidence** in Use Case 2, and **medium-low confidence** in Use Case 3 absent a scoping decision on how
much of it is demonstrated at MTR versus deferred to WP2 execution proper. None of these are
architecture risks — the D2.2 pipeline design is sound and already reused across all three — they are
sequencing and resourcing risks in the notebook build-out itself.

## What could block us

Two cross-cutting issues could slow all three use cases regardless of individual progress: the
Montandon staging database carries significant index bloat and query-performance risk that is only
partly mitigated, and the underlying question of how — and how often — baseline exposure data should be
computed and published is still open. Both are tracked and owned, but neither is resolved.

## What this report covers

Section 2 gives the state of work for each use case against the evidence in the repository (pull
requests, notebooks, and open issues). Section 3 assesses confidence and readiness for each. Section 4
details the open questions and blockers, including the two cross-cutting risks above. Section 5 sets
out the implementation plan to close the gap between where we are and a demonstrable, reviewable state.
Section 6 concludes with next steps and what we recommend discussing at the Readiness Review meeting.
