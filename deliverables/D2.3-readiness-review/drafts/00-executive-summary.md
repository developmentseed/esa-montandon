# Executive Summary

This report is deliverable D2.3 of the ESA "Application Development concerning Disaster Data and
Analytics" activity. It is the readiness review for Work Package 2, prepared ahead of the Readiness
Review meeting. It covers how close the three crisis-analytics use cases (population and infrastructure
risk exposure, post-disaster impact estimation, and operational response prioritisation) are to being
usable, what remains before each is ready, and the plan to complete that work.

Deliverable D2.2 (July 2026) assessed the pipeline's architecture: the design that lets structured
disaster data and EO hazard layers be combined automatically. This report assesses execution: what has
been built against that design, and what remains.

## Where things stand

Progress is uneven across the three use cases. None is yet at a state a National Society user could use
unassisted.

- **Use Case 1 (Risk Exposure)** is furthest along. MapAction has delivered the baseline
  exposure-calculation notebooks and ported them into a Streamlit interface, open for review. Three
  hazards are covered; a fourth, wildfire, remains to be added.
- **Use Case 2 (Impact Estimation)** has an initial notebook implementation opened for review this
  week. It has not yet been run against a live event end to end.
- **Use Case 3 (Response Prioritisation)** is the most developed on paper. Its methodology, data
  sources, and worked example are fully specified in the D2.4 use-case narrative. No notebook
  implementation has started, and it depends on outputs from Use Cases 1 and 2 that are themselves
  still forming.

## Confidence

Confidence in reaching a usable state on schedule is medium-high for Use Case 1, medium for Use Case 2,
and medium-low for Use Case 3, pending a scoping decision on how much of it is demonstrated at MTR
versus deferred to WP2 execution. None of this reflects architecture risk: the D2.2 pipeline design is
sound and already reused across all three. The remaining risk is in sequencing and resourcing the
notebook build-out.

## What could block progress

Two cross-cutting issues could slow all three use cases regardless of individual progress. The
Montandon staging database has index bloat and a query-performance risk that is only partly mitigated.
The strategy for how, and how often, baseline exposure data should be computed and published is still
undecided. Both are tracked and owned; neither is resolved.

## What this report covers

Section 2 gives the state of work for each use case, based on the pull requests, notebooks, and open
issues in the repository. Section 3 assesses confidence and readiness for each. Section 4 details the
open questions and blockers, including the two cross-cutting risks above. Section 5 sets out the
implementation plan to close the remaining gaps. Section 6 concludes with next steps and topics for the
Readiness Review meeting.
