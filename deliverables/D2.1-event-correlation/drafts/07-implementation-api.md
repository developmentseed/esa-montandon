# Implementation and API

## The Montandon STAC API

Correlation is performed against the Montandon STAC API, which implements the STAC API Filter extension
with CQL2. The staging endpoint is:

```text
https://montandon-eoapi-stage.ifrc.org/stac
```

Complex correlations use the `/search` endpoint with a POST request carrying a `cql2-json` filter:

```bash
curl -X POST 'https://montandon-eoapi-stage.ifrc.org/stac/search' \
  -H 'Content-Type: application/json' \
  -d '{ "filter-lang": "cql2-json", "filter": { ... }, "limit": 100 }'
```

The `/queryables` endpoint advertises the filterable fields (Section 3), so clients can discover the
correlation vocabulary programmatically.

## Programmatic access

Two libraries make correlation ergonomic:

- **`pystac-client`** — the standard STAC API client; the correlation filters in this report are issued
  directly through its `search()` interface.
- **`pystac-monty`** — the Monty-specific library, which provides the reference implementation of the
  `corr_id` algorithm and typed access to Monty fields (hazard/impact/response detail). As documented in
  D1.1, it is being extended with Response support and Response ↔ Impact pairing helpers, so notebook
  authors and ETL developers can build and follow correlations without constructing raw queries.

## Query performance

The correlation approach is designed to scale:

- **Indexing** — `monty:hazard_codes`, `monty:country_codes`, `datetime`, and `monty:corr_id` are the
  fields correlation depends on and should be indexed.
- **Progressive filtering** — begin with the most selective criteria (country, date range) before
  applying broader hazard-overlap clauses.
- **Deterministic fast path** — where a `corr_id` exists, direct identifier matching is faster than
  spatial/temporal queries and is preferred for exact pairing.
- **Pagination and caching** — large result sets are paginated; frequently used correlations can be
  cached.

## Error handling

The correlation documentation records the common failure modes and their remedies: timeouts are
resolved by adding more selective filters; empty results usually indicate an array operator applied to a
scalar (or vice versa); and unexpected results typically trace to hazard-code incompatibility across
classification systems, resolved by using `a_overlaps` across the equivalent codes (Section 3).
