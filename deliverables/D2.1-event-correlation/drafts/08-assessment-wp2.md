# Assessment and Relevance to WP2

## Assessment findings

The event correlation system is well suited to its adapted role of linking EO products to humanitarian
disaster records:

- **The two-mechanism model is sufficient and robust.** The deterministic `corr_id` provides stable,
  idempotent pairing for EO products anchored on their source identifiers, while dynamic CQL2 correlation
  handles the flexible, multi-hazard, cross-source matching that real disasters require.
- **EO products fit the model without special cases.** An EO Response product correlates through the
  same queryables (`hazard_codes`, `country_codes`, `datetime`, `corr_id`) as any other item; the only
  additions are the `response_detail.type`/`source_id` filters and the `derived_from`/`prev`/`related`
  links, all already defined in the released v1.3.0 model.
- **Standards-based and transparent.** Using STAC API and OGC CQL2 keeps the correlation logic open and
  inspectable, and keeps Montandon interoperable with the wider geospatial tooling ecosystem — an
  explicit priority for both ESA and IFRC.
- **Designed for real disasters.** Multi-hazard cascades, multi-country events, cross-source
  co-activations (Copernicus ↔ Charter), and monitoring time series are all handled by the same
  machinery.

## Relevance to WP2 — the matching engine for the analysis pipeline

The correlation system is the **matching engine** on which the WP2 automated analysis pipeline
(deliverable D2.2) is built. In that pipeline, an incoming alert — a new Copernicus EMS activation, a new
Montandon event — triggers analysis. Correlation is what determines *which* structured disaster data an
EO hazard layer should be combined with:

- When a new EO product arrives, correlation attaches it to the right event, hazard, and impact records
  (Section 5), assembling the complete data context for that disaster.
- The analysis notebooks then operate on that correlated context — intersecting an EO hazard footprint
  with the population and exposure data linked to the same event — rather than on isolated, unlinked
  inputs.
- The `corr_id` provides the stable key that ties an analysis output back to its disaster, so results
  can be published against the event and surfaced in IFRC GO.

In short, D2.1 establishes *how* disparate records about one disaster are recognised as belonging
together; D2.2 uses that capability to *combine* them into decision-ready analytics.

## Next steps

- Complete the `pystac-monty` Response and pairing helpers (D1.1, SW1.2) so correlation of EO products
  is fully exercised end-to-end as the Charter and CEMS transformers come online.
- Validate the EO-product correlation flow against real Copernicus and Charter activations ingested into
  the Montandon STAC API.
- Feed the correlation layer into the WP2 event-driven orchestration documented in D2.2.
