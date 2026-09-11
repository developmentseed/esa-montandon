# Executive Summary

This report is deliverable D2.3 of the ESA "Application Development concerning Disaster Data and
Analytics" activity. It is the readiness review for Work Package 2, prepared ahead of the Readiness
Review meeting. It covers how close the three crisis-analytics use cases (population and infrastructure
risk exposure, post-disaster impact estimation, and operational response prioritisation) are to being
usable, what remains before each is ready, and the plan to complete that work.

Deliverable D2.2 (July 2026) assessed the pipeline's architecture: the design that lets structured
disaster data and EO hazard layers be combined automatically. This report assesses execution: what has
been built against that design, and what remains. The case-study deliverable this work feeds into (D2.4)
is due in December 2026, so this report weighs the soundness of the design and the trajectory of the
work more heavily than whether every notebook is finished today; build status is one input, not the
whole assessment.

## Where things stand

Progress is uneven across the three use cases, and each is further along than a first look at the
underlying repositories alone would suggest.

- **Use Case 1 (Risk Exposure)** is furthest along. MapAction has delivered baseline exposure-calculation
  notebooks covering three out four planned hazards (flood, cyclone, earthquake with wildfire under development), parameterised
  so the same notebook runs for any country, and published as a working example. An earlier Streamlit
  prototype explored a guided-form interface but is not expected to be the long-term interface.
- **Use Case 2 (Impact Estimation)** has an initial notebook implementation, built by MapAction, opened
  for review this week. It has not yet been run against a live event end to end, and the Copernicus EMS
  and Charter data it depends on is not yet flowing into Montandon (see below).
- **Use Case 3 (Response Prioritisation)** has been reframed for this cycle. Rather than building the
  composite prioritisation notebook specified in the D2.4 narrative, the plan is to engage a third-party
  Charter-active partner, most likely UNOSAT given their role as Charter Project Manager for the current
  large-scale activation in Nepal, to use the Montandon database while working that activation and
  produce a Utility Report on the data's relevance, fitness for purpose, and recommendations for future
  improvement. This is a best-effort engagement with no delivery commitment, which substantially lowers
  WP2's own execution risk; the originally specified composite-score implementation remains a longer-term
  direction rather than a near-term commitment. The specific activation and partner are not yet
  finalised.

None of the three yet lets a National Society user run a new analysis of their own without technical
support; that self-service layer is the subject of WP3 (see D3.3).

## Confidence

Confidence in reaching a usable state ahead of D2.4 is high for Use Case 1, medium-high for Use Case 2,
and, in its reframed form, medium-high for Use Case 3: it no longer depends on WP2 engineering effort, on
Use Cases 1 and 2 stabilising first, or on the CEMS/Charter ETL timeline, since it is an external
partner's best-effort assessment of Montandon rather than a built composite score. The main uncertainty
is whether a suitable partner and activation are confirmed and whether the partner delivers, not
engineering risk. None of this reflects architecture risk: the D2.2 pipeline design is sound and already
reused by Use Cases 1 and 2. The remaining risk is in sequencing, in getting real disaster data flowing,
and in a small number of open decisions, not in the design itself.

## What could block progress

Three issues could slow the use cases regardless of individual notebook progress. The Copernicus EMS and
International Charter ETL pipelines, which supply the EO hazard data Use Cases 2 and 3 depend on, are
close but not yet loading data into Montandon on staging: Copernicus EMS data is now flowing in the alpha
environment, with staging expected around 11 September 2026, and Charter is expected on staging roughly a
week after that. The Montandon production database has index bloat and a
query-performance risk that is only partly mitigated ([issue #34](https://github.com/developmentseed/esa-montandon/issues/34)).
The strategy for how, and how often, baseline exposure data should be computed and published is still
undecided. All three are tracked and owned; the ETL timeline is now close to resolved, the other two are not.

## What this report covers

Section 2 gives the state of work for each use case and for the CEMS/Charter ETL pipelines, based on the
engineering work completed, the notebooks produced, and open issues across the relevant repositories.
Section 3 assesses confidence
and readiness for each. Section 4 details the open questions and blockers, including the cross-cutting
risks above. Section 5 sets out the implementation plan to close the remaining gaps. Section 6 concludes
with next steps and topics for the Readiness Review meeting.
