# Response ↔ Impact Boundary Rules

The overlap between Response and Impact is the most common source of modelling confusion, and getting
it wrong risks double-counting or losing damage data. A CEMS Grading Product that reports "200 buildings
destroyed" is unambiguously a **Response** product — an action was taken to produce it — but the
building-damage count itself is **Impact** data. Without explicit rules, two ETL authors would model
the same source record differently. This section documents the **source-agnostic** decision procedure
published as the Monty Response ↔ Impact Boundary Rules (a named D1.1 component). It is the rule set
that turns EO products into cleanly separated, correctly linked Response and Impact items.

- **Response** = an *action taken or product produced* (a CEMS map, a Charter VAP, a UNOSAT assessment).
- **Impact** = an *estimated or realised effect on people or assets* (deaths, people affected, buildings
  destroyed, economic loss).

## Data-pattern catalogue

An ETL author runs this catalogue over **each attribute, layer, or table** in an incoming response
product and applies the matching modelling outcome:

| # | Data pattern | Example | Outcome |
| --- | --- | --- | --- |
| P1 | Geometry-only delineation (extent, no per-feature attributes) | Flood polygon, fire perimeter | Response only |
| P2 | Categorical class per feature (no numeric effect) | Damage grade per building; flooded/not per pixel | Response only (Both → split if aggregated to counts) |
| P3 | Numeric estimate of realised effect on people/assets | `buildings_destroyed: 87`, `hectares_flooded: 1450` | Impact — never in `response_detail` |
| P4 | Multi-thematic statistics table (one figure per thematic) | CEMS GRA `affected`/`total` per thematic | Both → split: one Response + one Impact per thematic |
| P5 | Provenance / methodology metadata | producer, method, sensor, processing chain | Response only |
| P6 | Lifecycle / status flag | CEMS `statusCode`, monitoring number | Response only |
| P7 | Activation / request record that triggers a response | Charter activation, CEMS activation | Neither — it is an **Event** |
| P8 | Free-text narrative / situational summary | CEMS Situational Report prose | Response only (any figures extracted → Impact) |
| P9 | Pre-event baseline (exposure before the event) | CEMS Reference Map, pre-event population | Response only (`eo-ref`) — no realised effect |

The key distinction is **P3 vs. P9**: a numeric figure is Impact only when it expresses a *realised
effect of the event*; the same kind of number measured *before* the event is a baseline that stays on
the Response item.

## Decision tree

Applied per attribute, first match wins:

1. **Activation / request record?** → **Event** item. Stop.
2. **Numeric estimate of a realised effect** on people/assets?
   - Single figure → **Impact** item.
   - One figure per thematic class → **Both → split**: one Response + one Impact per thematic.
3. **Geometry, per-feature class, pre-event baseline, or narrative?** → **Response only**.
4. **Provenance, methodology, or lifecycle/status flag?** → **Response only**, under `response_detail`.

## ETL splitting and linkage

When a product carries realised-effect figures (P3/P4), the transformer emits one Response item plus
one Impact item per numeric thematic. The paired items are joined durably and idempotently:

- **Shared `monty:corr_id`** on the Response and every paired Impact — the durable join key.
- **Deterministic item ids** derived from the Response `source_id` + thematic, so re-runs upsert rather
  than duplicate.
- On each Impact item, a canonical provenance link back to its Response:

```json
{
  "rel": "derived_from",
  "href": "response-EMSR-DEMO-001-GRA.json",
  "type": "application/json",
  "roles": ["response"]
}
```

![A multi-thematic CEMS Grading product splits into one Response item plus one Impact item per thematic class. Each Impact links back with `rel: derived_from` and all items share the same `monty:corr_id`.](response-impact-split.png)

A multi-thematic CEMS Grading product (figures for population, buildings, and roads) therefore becomes
**one Response item and three Impact items** — never a single Impact bundling all thematics, and never
the figures stuffed into `response_detail`. A synthetic worked fixture demonstrating this exact split
ships with the extension. Section 4 of deliverable D2.1 documents how a consumer re-pairs the two halves
through the STAC API.
