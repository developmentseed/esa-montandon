# Core Correlation Algorithms

Dynamic correlation is realised as four core algorithms, each a CQL2 filter template over the
queryables of Section 3. They correlate the base Montandon constructs; Section 5 extends them to EO
Response products.

## Algorithm 1 — Event-to-Event

**Purpose:** find all source events, from different providers, that describe the same disaster.
**Criteria:** compatible hazard codes, same country, overlapping time (optionally overlapping space).

```json
{
  "filter-lang": "cql2-json",
  "filter": {
    "op": "and",
    "args": [
      {"op": "a_overlaps", "args": [{"property": "monty:hazard_codes"}, ["MH0600", "nat-hyd-flo-flo", "FL"]]},
      {"op": "a_contains", "args": [{"property": "monty:country_codes"}, "ESP"]},
      {"op": "t_intersects", "args": [{"property": "datetime"}, {"interval": ["2024-10-27T00:00:00Z", "2024-10-28T00:00:00Z"]}]},
      {"op": "in", "args": ["event", {"property": "roles"}]}
    ]
  }
}
```

The equivalent CQL2-Text form is compact and human-readable:

```text
roles IN ('event') AND
a_overlaps(monty:hazard_codes, ARRAY['MH0600','nat-hyd-flo-flo','FL']) AND
a_contains(monty:country_codes, 'ESP') AND
t_intersects(datetime, INTERVAL('2024-10-27T00:00:00Z','2024-10-28T00:00:00Z'))
```

This links, for example, the GDACS, GLIDE, and EM-DAT records for one flood into a single set — the
basis for data reconciliation and for establishing the reference event that anchors a `corr_id`.

## Algorithm 2 — Event-to-Hazard

**Purpose:** find all hazard items for an event. **Criteria:** match by `corr_id` if available, else by
hazard codes, country, and temporal/spatial overlap. Where a static identifier exists, the query is a
direct match:

```text
roles IN ('hazard') AND monty:corr_id = '20241027-ESP-FL-2-GCDB'
```

Otherwise the dynamic form (hazard codes + country + time window, restricted to `roles` containing
`hazard`) retrieves the hazard assessments — useful for isolating the individual hazards of a
multi-hazard event.

## Algorithm 3 — Event-to-Impact

**Purpose:** aggregate all impact items for an event. **Criteria:** hazard codes and country, with a
temporal window widened to account for reporting lag (impacts often arrive days or weeks after the
event):

```text
roles IN ('impact') AND
a_overlaps(monty:hazard_codes, ARRAY['MH0600','FL']) AND
a_contains(monty:country_codes, 'ESP') AND
t_after(datetime, '2024-10-27T00:00:00Z') AND t_before(datetime, '2024-11-10T00:00:00Z')
```

This gathers impact estimates from all sources for comparison and aggregation over time.

## Algorithm 4 — Hazard-to-Impact

**Purpose:** attribute impacts to a specific hazard within a multi-hazard event. **Criteria:** same
`corr_id` **and** the specific hazard code (optionally spatial intersection between hazard and impact
geometries, and temporal causality):

```text
roles IN ('impact') AND monty:corr_id = '20241027-ESP-FL-2-GCDB' AND
a_contains(monty:hazard_codes, 'MH0603')
```

This is what allows a cascading disaster to be analysed hazard-by-hazard — determining which hazard
caused which impact.

## From base constructs to EO products

These four algorithms correlate events, hazards, and impacts. An EO Response product is, for correlation
purposes, another item carrying `monty:hazard_codes`, `monty:country_codes`, `datetime`, and (once
attached) a `corr_id`. Section 5 shows how the same query machinery attaches an incoming Copernicus,
Charter, or UNOSAT product to its event, and links the impacts it informs.
