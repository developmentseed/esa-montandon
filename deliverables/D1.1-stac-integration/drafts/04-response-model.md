# The Response Data Model (v1.3.0)

The harmonised Response data model is deliverable SW1.1. It was specified, implemented, validated, and
**released as version 1.3.0 of the Monty STAC extension** (published at
`https://ifrcgo.org/monty-stac-extension/v1.3.0/schema.json`, Apache 2.0). This section documents the
released model.

## What v1.3.0 adds

Version 1.3.0 introduces the Response construct as a peer of Event, Hazard, and Impact:

- A **`response` role** identifying an item as a Response, alongside the existing `event`, `hazard`,
  and `impact` roles.
- The **`monty:response_detail`** object carrying the response type code and its descriptive metadata.
- A **`related-response`** relation type for linking responses to the rest of the model.
- Updated JSON Schema, data-model documentation, and class diagram. The release validates all worked
  examples in the extension repository against the published schema.

## Response type codes

Response type codes use a two-level **`{domain}-{type}`** hierarchy, all lowercase and hyphen-separated,
matched by the schema pattern `^(eo|hum|fin)-[a-z0-9]+(-[a-z0-9]+)*$`. The domain groups responses into
Earth Observation, humanitarian, and financial:

| Domain | Prefix | Covers |
| --- | --- | --- |
| Earth Observation | `eo` | Satellite-derived products (Copernicus EMS, International Charter, UNOSAT) |
| Humanitarian | `hum` | Cluster-based operational response |
| Financial | `fin` | Appeals, funds, assessment budgets |

Codes are **source-agnostic**: a delineation product is `eo-del` whether it comes from CEMS, the
Charter, or UNOSAT. Source provenance is preserved through other fields and links (Section 5), not
encoded in the type code.

### EO response products (the primary use case)

| Code | Name | CEMS | Charter | UNOSAT |
| --- | --- | --- | --- | --- |
| `eo-dat` | Data Product (delivered imagery dataset) | — | Acquisition (calibrated) | GIS-ready download |
| `eo-ref` | Reference Product (pre-event baseline) | `REF` | Reference map VAP | Phase 0 basemap |
| `eo-fep` | First Estimate Product | `FEP` | Early VAP (best effort) | Phase 1 |
| `eo-del` | Delineation Product (affected extent) | `DEL` | Delineation VAP | Phase 2 flood extent |
| `eo-gra` | Grading Product (damage grade) | `GRA` | Grading VAP | Phase 2 damage assessment |
| `eo-pop` | Population Exposure | — (derived) | Population VAP | Phase 2 population analysis |
| `eo-mon` | Monitoring Update | `DEL-MON`, `GRA-MON` | — | Phase 3 monitoring |
| `eo-sr` | Situational Report | `SR` | — | — |
| `eo-vap` | Value-Added Product (generic fallback) | — | Charter VAP fallback | — |

![An example value-added damage product: an infrastructure-damage assessment for the La Guaira earthquake, Venezuela. Products of this kind map to the source-agnostic eo-gra (grading) or eo-vap code regardless of which organisation produces them. Courtesy Alexander Ariza, UN-SPIDER.](charter-vap-example.jpg)

A Charter **activation** is *not* a Response — because it bundles many subsequent deliveries, it is
modelled as a Monty **Event**. Charter **VAPs** and delivered **acquisitions** become Response items
(`eo-*` codes and `eo-dat` respectively). Humanitarian (`hum-shelter`, `hum-health`, `hum-wash`, …) and
financial (`fin-dref`, `fin-ea`, `fin-aa`, …) codes are defined as extensible placeholders for future
work beyond this contract's EO scope.

## The `monty:response_detail` object

`monty:response_detail` is the Monty-specific object attached to a Response item, analogous to
`hazard_detail` and `impact_detail`. It carries the response type code and the minimal metadata not
already expressed by another declared extension on the item:

| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| `type` | string | yes | Response type code (regex-constrained to the vocabulary above) |
| `source_id` | string | no | Native id in the source system (CEMS activation code, Charter call id, UNOSAT product code, DREF operation id) |
| `status` | string | no | `planned` / `in-production` / `published` / `finished` / `no-impact` / `withdrawn` |
| `monitoring_number` | integer | no | Present only on monitoring updates; the prior iteration is linked via STAC `rel: prev` |
| `producer` | string | no | Producing organisation (e.g. `JRC`, `UNOSAT`, `Airbus`, `IFRC`) |
| `methodology` | string | no | `human_interpreted` / `semi_automated` / `automated` / `modelled` |
| `sendai_targets` | array | no | Unique subset of the Sendai Framework targets `["A"…"G"]` |
| `sectors` | array | no | For `hum-*` items — IASC clusters / IFRC EPoA sectors |

`type` is the only mandatory field; the schema rejects unknown keys. Statistical figures that EO
products may carry (damage counts, affected populations) are explicitly **not** part of
`response_detail` — they become linked Impact items, per the boundary rules in Section 6.

## Sendai Framework crosswalk

Although the Sendai Framework targets are outcome metrics rather than a response taxonomy, annotating
Response items with the targets they contribute to enables policy-level aggregation and reporting. The
model provides an optional `sendai_targets` field and a default crosswalk per response type (for
example, `eo-gra` grading products default to targets **C** — economic loss — and **D** — infrastructure
damage; `eo-pop` population-exposure products default to target **B** — reduction of affected people).
These defaults can be overridden per item.
