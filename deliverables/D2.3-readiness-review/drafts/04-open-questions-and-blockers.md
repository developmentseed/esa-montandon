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

**UC3 — reframed as an externally-led Utility Report.** The near-term target has changed again: rather
than a build, or an informal Charter-user review, the proposal from the ESA project manager is to engage
a third-party partner already active in a Charter activation, on a best-effort, non-committal basis, to
assess Montandon's data directly, irrespective of whether Charter-sourced content is itself present, and
produce a Utility Report on its relevance, fitness for purpose, and recommendations for future
improvement. UNOSAT, as Charter Project Manager for the current large-scale activation in Nepal, is the
leading candidate partner, and a Nepal activation with Red Cross involvement would additionally allow
linking National Society engagement to the results. This removes UC3's near-term dependency on Use Cases 1 and 2 stabilising, and on CEMS or Charter
data reaching Montandon (Section 4.2); building the composite prioritisation score itself (Section 2.3)
remains longer-term WP2 execution work, to be revisited in light of the Utility Report's findings.

## 4.2 Cross-cutting: CEMS and Charter data not yet on production

Use Case 2 needs Copernicus EMS and Charter hazard/response data in Montandon to validate against real
events; neither is on production yet, though both are close (Section 2.4). (Use Case 3's near-term Utility
Report activity does not need this: see Section 4.1.) Both transformers are
implemented and merged in `pystac-monty`, with active bug-fixing this week (related-link and
event-matching fixes for CEMS). CEMS data is now flowing in the alpha environment, with production hoped
for around 11 September 2026; Charter is expected on staging roughly a week later, around 17 September 2026. Neither is blocked on design; both are normal integration and review work nearing completion.

**pystac-monty versioning.** Separately, a small number of `pystac-monty` changes, including item
versioning, are implemented but not yet deployed to PROD. A follow-on item, adding the version field to
eoAPI's queryables so users can filter by transformer version, is tracked as
[monty-stac-extension#147](https://github.com/IFRCGo/monty-stac-extension/issues/147). Neither is a
blocker for Use Case 2 today, or for Use Case 3's near-term Utility Report; both should land before
Montandon's data is treated as fully reproducible for Use Case 3's eventual build.

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

IFRC and MapAction identified 11 National Society operations teams for structured interviews, including
Zambia, Ethiopia, Kenya, Niger, Honduras, Chile, Netherlands, Denmark, Bangladesh, and the Philippines, to
validate that the three use cases as specified match operational need. 6 of the 11 have been conducted so
far. Results to date strongly validate Use Cases 1 and 2. This is a substantive, positive signal and
should carry real weight in the Readiness Review discussion alongside build status, since it tests the
premise the use-case series rests on.
