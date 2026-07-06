# Queryables and Correlation Criteria

Dynamic correlation is expressed as CQL2 filters over the fields a STAC API advertises as
**queryables**. This section documents the queryable fields the correlation algorithms rely on and the
array operators that make multi-value matching possible.

## Core queryable fields

A Montandon STAC API implementing the Filter extension exposes these Monty fields (via its
`/queryables` endpoint) for use in filter expressions:

| Field | Type | Role in correlation |
| --- | --- | --- |
| `monty:hazard_codes` | array of string | Hazard classification codes (UNDRR-ISC, EM-DAT, GLIDE); the primary correlation attribute |
| `monty:country_codes` | array of string | ISO 3166-1 alpha-3 country codes |
| `monty:corr_id` | string | The static correlation identifier for deterministic pairing |
| `monty:episode_number` | integer | Distinguishes episodes of the same event |
| `roles` | array of string | Item type — `event`, `hazard`, `impact`, `response`, `reference`, `source` |
| `datetime` (and `start`/`end_datetime`) | timestamp | Temporal extent for time-window matching |
| `geometry` / `bbox` | geometry | Spatial extent for spatial intersection |

For EO Response products, two further queryables are decisive: **`monty:response_detail.type`** (filter
by product type — `eo-del`, `eo-gra`, …) and **`monty:response_detail.source_id`** (the native source
identifier — the Copernicus EMSR code, Charter activation, or UNOSAT product code). Hazard and impact
detail objects (`monty:hazard_detail.*`, `monty:impact_detail.*`) are also queryable for finer
correlation.

## Array operators

Because hazard and country codes are arrays, correlation depends on the STAC Filter extension's array
operators. The choice of operator determines how strict the match is:

| Operator | Meaning | Matches `["MH0600","FL"]` when query is… |
| --- | --- | --- |
| `a_equals` | Arrays exactly equal (same elements) | `["MH0600","FL"]` only |
| `a_contains` | Property array contains the element(s) | `"MH0600"` ✓, `"EQ"` ✗ |
| `a_overlaps` | At least one element in common | `["MH0600","EQ"]` ✓ |
| `a_containedBy` | All property elements are within the query array | `["MH0600","FL","nat-hyd-flo-flo"]` ✓ |

In practice, correlation uses **`a_contains`** for country codes (the item must cover the country of
interest) and **`a_overlaps`** for hazard codes (a match on any equivalent code across classification
systems is sufficient), because the same hazard is often expressed with different codes by different
sources — for example `MH0600`, `nat-hyd-flo-flo`, and `FL` all denote flooding.

## Temporal and spatial tolerance

Correlation rarely requires exact temporal or spatial equality. The algorithms therefore use tolerance:

- **Temporal windows** — `t_intersects` against an interval, or `t_after`/`t_before` bounds, to allow
  for the lag between an event and the impacts or EO products that report on it (impacts and damage
  assessments may appear days or weeks later).
- **Spatial tolerance** — `s_intersects` against a point, buffered geometry, or bounding box, for
  regional correlation rather than pixel-exact overlap.

## Hazard-hierarchy correlation

The 2025 UNDRR-ISC hazard structure is hierarchical, so a query can correlate across a whole hazard
cluster by matching any of its member codes — for example, matching any of the water-related flood
codes (`MH0600`–`MH0604`) to retrieve coastal, flash, and fluvial flooding together. This lets
correlation operate at the right level of generality for the question, which is essential when an EO
product's hazard classification is coarser or finer than the humanitarian record's.
