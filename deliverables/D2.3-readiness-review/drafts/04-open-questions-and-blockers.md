# Open Questions and Blockers

This section lists what is unresolved as well as what is done. Some items are scoping decisions needed
from IFRC/ESA; others are engineering work already underway. None of these change the assessment that
the underlying design is sound; they are the specific things standing between today and December.

## 4.1 Use-case-specific

**UC1 — baseline-computation strategy.** Because baseline risk exposure does not change often (it is not
event-driven, unlike Use Cases 2 and 3), it does not need to be recomputed live for every user. Three
options are on the table:

1. Compute on demand, per user selection (simplest, but repeats identical work).
2. Pre-compute on a schedule (for example, yearly) for selected countries and hazards.
3. Pre-compute once for all countries, precisions, and hazards, and have notebooks reference the result
   rather than recompute it.

Option 2 or 3 is the current recommendation, since a pre-computed, cloud-hosted dataset is cheaper to
serve and simpler to keep consistent across published outputs. This requires a decision; see Section 5.

**UC2 — unvalidated against a real event.** The initial implementation has not been run end to end
against a live or recent Copernicus EMS or Charter activation, nor reviewed by a domain expert. This is
gated in part by Section 4.2 below: there is not yet a live CEMS or Charter event in Montandon to run it
against. This is the highest-priority item before Use Case 2 can be called demonstrable.

**UC3 — scope at MTR.** The full response-prioritisation methodology (Section 2.3) is ambitious and
depends on two use cases that are not yet stable. A decision is needed on whether the near-term target is
a full working implementation, a narrower slice (for example, the exposure/impact/vulnerability
components only, without historical burden and operational-gap weighting), or a specified-but-not-built
status carried into WP2 execution proper. Given the December deadline, this is a sequencing choice, not
a cause for concern in itself.

## 4.2 Cross-cutting: CEMS and Charter data not yet in Montandon

Use Cases 2 and 3 need Copernicus EMS and Charter hazard/response data in Montandon to validate against
real events; neither is loading yet (Section 2.4). Both transformers are implemented and merged in
`pystac-monty`, with active bug-fixing this week (related-link and event-matching fixes for CEMS). Both
`montandon-etl` deployment integrations are open: CEMS since 10 August 2026, Charter (draft) since 26
June 2026. Neither is blocked on design; both are normal integration and review work. Merging either one
is the fastest path to unblocking a real-event validation run for Use Case 2.

## 4.3 Cross-cutting: Montandon platform performance

The Montandon production database has a performance problem that affects every use case's notebooks,
since all query the same STAC API. This is tracked in
[issue #34](https://github.com/developmentseed/esa-montandon/issues/34). An initial investigation found
the roughly 100 GB database bloated by duplicate property indexes (500 or more redundant indexes on some
source partitions alone), caused by an indexing job that does not correctly detect existing indexes for
nested Monty fields. Basic autoscaling has been added, but further remediation, dropping the duplicate
indexes, vacuuming large partitions, and tuning memory settings, is blocked on staging-cluster access for
the engineer doing the work. Ownership is assigned and a plan exists; it is not yet complete. This is the
one risk capable of degrading all three use cases simultaneously, independent of their individual build
progress.

## 4.4 Cross-cutting: statistics export format

A related, lower-urgency open question is how to export platform-wide statistics (event counts by
hazard type, and similar aggregate figures useful for public reporting and for `montandondata.org`):
via a periodic GeoParquet export to cloud storage, or by querying the database directly. This does not
block any of the three use cases, but does affect how their outputs might eventually be aggregated and
published at scale. A decision is pending.

## 4.5 Validation against real user needs

IFRC and MapAction are conducting structured interviews with National Society operations teams (Zambia,
Ethiopia, Kenya, Niger, Honduras, Chile, Netherlands, Denmark, Bangladesh, and the Philippines) through
August 2026, to validate that the three use cases as specified match operational need. This work is in
progress but not complete at the time of this report. Early, directional findings from these interviews,
where available, should carry more weight in the Readiness Review discussion than polish on any single
notebook, since they test the premise the use-case series rests on.
