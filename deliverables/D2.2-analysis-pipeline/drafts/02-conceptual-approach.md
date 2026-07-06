# Conceptual Approach

## From products to decisions

Today, combining an EO hazard product with humanitarian exposure data is a manual, desktop GIS task —
an analyst downloads a Copernicus flood extent, loads a population raster, clips one to the other, and
computes statistics by administrative area. This is slow, hard to reproduce, and difficult to scale
across the many events that occur simultaneously. The pipeline's purpose is to make this operation
**automatic, reproducible, and event-driven**, so the analytical output is available in the first hours
of a response rather than days later.

## Three ingredients

The approach rests on three ingredients, each supplied by earlier work:

1. **Structured disaster data and EO hazard layers in one catalog.** Work Package 1 (D1.1) brought ESA
   EO products into Montandon as Response items alongside the Event, Hazard, and Impact records. Both
   the "what happened" and the "what the satellite saw" now live in the same STAC-based catalog.
2. **Correlation as the join.** Deliverable D2.1's correlation system determines which structured
   records an EO hazard layer belongs with — the event it documents, the hazards it delineates, the
   exposure and impact data for the same disaster. Correlation is what makes the combination *correct*:
   it ensures today's flood extent is intersected with the exposure data for the right place and event.
3. **Modular notebooks as analysis units.** Each analysis — population exposure, damage assessment,
   resilience indicators — is packaged as a parameterised notebook. Notebooks are treated as
   interchangeable objects: any one can be substituted for another provided its inputs and outputs match,
   which lets methods be improved or specialised without changing the pipeline around them.

## The combination operation

At its heart the pipeline performs a spatial combination: take the **hazard footprint** carried by an EO
Response product (a flood polygon, a burned-area extent, a damage-grade layer) and intersect it with the
**exposure layers** (population, infrastructure) and the structured impact records correlated to the same
event. The result is a quantified estimate — people or assets within the observed hazard extent —
attached back to the event so it can be published and consumed.

## Design principles

- **Event-driven, not batch.** Analysis is triggered by the arrival of new data (a Copernicus
  activation, a new Montandon event), so outputs track live situations.
- **Reproducible.** Analyses are documented notebooks run by machine, not ad-hoc desktop steps, so a
  result can be regenerated and audited.
- **Modular.** Adding a hazard type or improving a method means adding or swapping a notebook, not
  re-engineering the pipeline.
- **Operationally targeted.** Outputs are shaped for the IFRC DREF decision cycle and published where
  operational users already work (IFRC GO), not left as raw layers.
- **Open.** Every component is open-source (Apache 2.0) in the IFRC GitHub organisation, aligned with
  ESA's Open Science strategy.
