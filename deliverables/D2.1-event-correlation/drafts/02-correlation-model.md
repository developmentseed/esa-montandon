# The Monty Correlation Model

Montandon links items about the same disaster through two complementary mechanisms: a **static
correlation identifier** that gives related items a shared, deterministic join key, and **dynamic
STAC-based correlation** that matches items by their attributes at query time. The two are designed to
work together — the static identifier for fast, deterministic linking, the dynamic approach for
flexible, multi-hazard correlation.

## Mechanism 1 — the static correlation identifier

Every item can carry a correlation identifier (`monty:corr_id`) generated deterministically from the
metadata of its reference event. The identifier follows the format:

```text
{datetime}-{country_code}-{block_id}-{hazard_code}-{episode_number}-GDBC
```

Where:

- **`datetime`** — the event date/time (`YYYYMMDD` or full ISO 8601).
- **`country_code`** — ISO 3166-1 alpha-3 code of the affected country.
- **`block_id`** — a spatial grid cell. The Earth is divided into cells of 0.2° latitude/longitude
  (roughly 20 × 20 km); each cell has a unique block ID. Grouping by cell keeps genuinely co-located
  events together while separating events that are close in time but far apart.
- **`hazard_code`** — the primary hazard code from the 2025 UNDRR-ISC Hazard Information Profiles (for
  example `MH0600` for river flood, `GH0101` for earthquake); for multi-hazard events, the first code in
  the array.
- **`episode_number`** — distinguishes episodes that share the same date, country, and hazard.

![Anatomy of the correlation identifier: date, country, spatial grid block, primary hazard code, episode number, and the GDBC suffix.](corr-id-anatomy.png)

Because the identifier is derived from intrinsic event properties, two sources describing the same
disaster arrive at the same `corr_id` independently. Populating this identifier on all related items —
including EO Response products — gives a stable, deterministic key for pairing. A reference
implementation is provided in the `pystac-monty` library.

## Mechanism 2 — dynamic STAC-based correlation

Static identifiers are efficient but rigid. To handle the heterogeneity and multi-hazard complexity of
real disaster data, Montandon also supports **dynamic correlation**: rather than relying on a
pre-computed identifier, items are matched at query time using the STAC API's Filter extension and the
OGC **Common Query Language (CQL2)**. Items are correlated on:

- **Hazard codes** (`monty:hazard_codes`) — arrays of codes across classification systems (UNDRR-ISC,
  EM-DAT, GLIDE).
- **Country codes** (`monty:country_codes`) — ISO 3166-1 alpha-3 arrays.
- **Temporal extent** — `datetime`, `start_datetime`, `end_datetime`.
- **Spatial extent** — GeoJSON `geometry` and `bbox`.
- **Episode number** and, where present, the static **`corr_id`**.

This dynamic approach offers several advantages over static identifiers alone:

- **Flexibility** — correlation criteria can be tuned to the question being asked (tight or loose
  temporal windows, single or clustered hazards).
- **Multi-hazard support** — overlapping and cascading hazards are matched through array operators
  rather than forced into one identifier.
- **Real-time correlation** — no pre-computation; correlation happens at query time as new data arrives.
- **Transparency** — the correlation logic is expressed as a visible, adjustable query, not a hidden
  algorithm.
- **Standards-based** — it uses STAC API and OGC CQL2 conventions, keeping Montandon interoperable with
  the wider geospatial ecosystem.

## Using both together

![The two mechanisms are complementary: the deterministic `corr_id` and dynamic CQL2 queries both resolve to the same correlated cluster of Event, Hazard, Impact, and Response items.](correlation-mechanisms.png)

The recommended practice is to use both: generate the `corr_id` for reference events and propagate it to
related items (including EO products) for fast deterministic linking, and support dynamic queries for
flexible correlation and discovery. The `corr_id` remains available for backward compatibility and for
cases where exact, deterministic pairing is required; dynamic queries handle everything else. The next
sections detail the queryable fields (Section 3) and the algorithms (Section 4) that dynamic correlation
is built from.
