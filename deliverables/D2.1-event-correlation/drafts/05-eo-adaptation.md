# Correlation adapted to EO Response Products

The core algorithms correlate the base Montandon constructs. This section documents how the same
mechanism is adapted to Earth Observation response products — the new work of this deliverable. There
are four aspects: attaching a product to its event, pairing a product with the impacts it informs,
linking products across sources, and chaining monitoring updates.

## 5.1 Attaching an EO product to its event and hazard

When a Copernicus EMS, Charter, or UNOSAT product is ingested, it must be attached to the correct
Montandon event and hazard. The procedure combines source-id anchoring with dynamic correlation:

1. **Anchor on the source identifier.** Each EO product carries a native identifier in
   `monty:response_detail.source_id` — a Copernicus activation code (`EMSR842`), a Charter activation
   (`disaster:activation_id`, e.g. `ACT-849`), or a UNOSAT product code (`FL20240926ESP`). This anchors
   the product and makes ingestion idempotent (re-ingesting the same product updates rather than
   duplicates it).
2. **Derive the correlation key.** From the product's activation metadata — date, country
   (`monty:country_codes`), and hazard (`monty:hazard_codes`) — derive the `corr_id` using the standard
   algorithm (D2.1 §2.1), or run the Event-to-Event query (Algorithm 1) to find an existing reference
   event that matches.
3. **Attach and link.** Set the resolved `corr_id` on the Response item and add explicit relation
   links: `reference-event` to the canonical Montandon event and `source-event` to the source-side event
   item; `related` links (with `roles: ["hazard"]`) to the hazard(s) the product addresses.

![Attaching an incoming EO product to its event: anchor on the source identifier, derive the correlation id, find the reference event, then attach the Response with the shared `corr_id` and relation links.](eo-attach-sequence.png)

The Response item is then discoverable through exactly the same queries as any other item. Finding
every EO product for an event is Algorithm 2/3 with the role set to `response`:

```text
roles IN ('response') AND monty:corr_id = '20241027-ESP-FL-2-GCDB'
```

Filtering to a specific product type adds one clause, for example only grading products:

```text
roles IN ('response') AND monty:corr_id = '20241027-ESP-FL-2-GCDB'
  AND monty:response_detail.type = 'eo-gra'
```

## 5.2 Pairing an EO product with the impacts it informs

Many EO products carry damage or exposure figures (a grading product reporting affected populations and
destroyed buildings per thematic class). Under the Response ↔ Impact boundary rules (D1.1 §6), those
figures are modelled as **separate Impact items**, not fields on the Response. Correlation ties the two
halves together:

- The Response and each derived Impact share the **same `monty:corr_id`**.
- Each Impact carries a canonical provenance link back to the Response:

```json
{
  "rel": "derived_from",
  "href": "response-EMSR744-GRA.json",
  "type": "application/json",
  "roles": ["response"]
}
```

A consumer re-pairs the two halves through the STAC API. To retrieve everything for a paired record,
query the shared `corr_id`; to go from a Response to its downstream Impacts, add a role clause; to go
from an Impact back to its source Response, follow the `derived_from` link (authoritative) or query the
`corr_id` filtered to `roles` containing `response`:

```text
monty:corr_id = '20260615T000000Z-DEMO-FL-001-DEMO' AND 'impact' IN roles
```

This is what lets an analyst move seamlessly from an ESA damage-grading product to the population and
infrastructure impact estimates it produced, and back.

## 5.3 Cross-source linkage

EO products are frequently produced for the same disaster by more than one service. When a Copernicus
activation co-occurs with a Charter activation, the Copernicus product records the Charter reference
(`charterNumber`) as a **`rel: related` link (with `roles: ["response"]`)** to the corresponding Charter
value-added product item, rather than duplicating Charter-native fields. Both products already share the
event `corr_id`, so they surface together in an event-level query; the explicit link additionally
records the direct correspondence between the two products. The same pattern links a grading product to
the delineation product it refines.

## 5.4 Monitoring chains

Delineation and grading products are re-issued as **monitoring updates** as a situation evolves. Each
update carries `monty:response_detail.monitoring_number` and a **`rel: prev`** link to the prior
iteration, forming an ordered chain. All iterations share the event `corr_id`, so a query returns the
full time series for an event, while the `prev` links and monitoring numbers preserve their order — the
basis for tracking, for example, how a flood extent changes over successive Copernicus updates.

## 5.5 Source-identifier anchoring summary

| Source | Anchor identifier | Carried as |
| --- | --- | --- |
| Copernicus EMS | Activation code (`EMSR842`) | `monty:response_detail.source_id` |
| International Charter | Activation id (`849`) | `disaster:activation_id` (+ `source_id` = `ACT-849`) |
| UNOSAT | Product code (`FL20240926ESP`) | `monty:response_detail.source_id` and item `id` |

Anchoring on the native identifier keeps correlation deterministic and idempotent across ETL re-runs,
while the derived `corr_id` and dynamic queries provide the flexible, cross-source linking.
