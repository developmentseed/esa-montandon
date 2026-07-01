# Data-Combination Patterns

This section describes, at architecture level, how the pipeline combines EO hazard layers with structured
disaster data. The detailed algorithms belong to WP2 execution; the pattern below defines the interface
between the data and the analysis.

## The core pattern: footprint ∩ exposure

Every analysis family shares a common spatial pattern:

1. **Obtain the hazard footprint** from an EO Response product correlated to the event — a flood-extent
   polygon (`eo-del`), a burned area, or a damage-grade layer (`eo-gra`).
2. **Obtain the exposure layers** for the same area — population distribution, critical infrastructure,
   and administrative boundaries — from Montandon, OCHA HDX, and related repositories.
3. **Intersect and aggregate** — overlay the footprint on the exposure layers and compute statistics per
   administrative unit (for example, population within the observed extent, infrastructure in the graded
   zone), optionally weighted by vulnerability and coping-capacity indicators.

The output is a quantified, decision-ready figure attached to the event. The same pattern serves
baseline exposure, past-event impact, and forward projections, provided a hazard layer is available, and
it accommodates different targets — total population, vulnerable groups, or specific infrastructure
classes.

![The core data-combination operation: an EO hazard footprint intersected with exposure layers yields per-administrative-unit statistics of the people and assets within the observed hazard extent.](data-combination.png)

![Illustrative population-exposure analysis: an EO-derived hazard footprint intersected with a population layer and aggregated by administrative unit — the "footprint ∩ exposure" operation the pipeline automates for each event.](exposure-example.png)

## Correlation supplies the "which data" answer

The combination is only correct if the EO layer is intersected with the exposure and impact data for the
*right* disaster. That is the role of the correlation system (D2.1): given an incoming EO product, it
identifies the event, hazards, and impacts it belongs with, so the pipeline assembles a coherent data
context rather than intersecting mismatched layers. The correlation identifier also ties the analysis
output back to its event, so results are published against the correct disaster.

## Dependency on the Response ↔ Impact boundary rules

A crucial upstream dependency is the **Response ↔ Impact boundary rules** established in Work Package 1
(D1.1, Section 6, and the `response-impact-boundary.md` specification). Those rules govern how an EO
product that carries damage figures is split into a Response item (the product and its hazard-layer
geometry) plus one or more paired Impact items (the numeric figures). It is that split which yields the
**structured Impact records** the analytics consume: the pipeline reads clean, per-thematic impact
figures linked to the event, rather than having to parse statistics out of product metadata. The
pipeline therefore relies on — and does not re-derive — the boundary rules; it consumes their output.

## Data sources combined

| Layer | Role | Typical source |
| --- | --- | --- |
| EO hazard footprint | The observed extent/severity of the hazard | Copernicus EMS, International Charter, UNOSAT (via Montandon) |
| Structured event / hazard / impact | The disaster context and reported effects | Montandon (GDACS, EM-DAT, DesInventar, IFRC DREF, …) |
| Population & infrastructure exposure | The assets at risk within the footprint | Montandon, OCHA HDX, national datasets |
| Vulnerability & coping capacity | Weighting for resilience analysis | INFORM-aligned indicators, demographic/socio-economic data |

## Standardised but flexible outputs

Outputs are standardised enough to be consumed uniformly by the DREF workflow and IFRC GO, while
remaining flexible: because analyses are modular notebooks (Section 4), technical teams can adjust
parameters, targets, and methods to fit evolving operational requirements without altering the pipeline.
The precise output schemas and per-hazard methods are finalised in WP2 execution in consultation with
IFRC.
