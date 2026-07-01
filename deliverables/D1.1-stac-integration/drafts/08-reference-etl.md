# Reference ETL Implementation (SW1.2)

Deliverable SW1.2 is the reference Extract-Transform-Load implementation that converts native EO source
formats into Monty-compliant STAC Items. It is implemented as modular Python packages in the
**`pystac-monty`** library and deployed operationally through the **`montandon-etl`** pipelines,
consistent with the existing production ETL for sources such as GDACS and EM-DAT.

## Programmatic model support in `pystac-monty`

With the v1.3.0 schema released, `pystac-monty` is being extended with typed support for Response
items so ETL developers and notebook authors can create and query them programmatically, mirroring the
existing Hazard and Impact support:

- A **`ResponseDetail`** data structure mirroring the v1.3.0 `monty:response_detail` object exactly —
  the `type` vocabulary, `source_id`, `status`, `monitoring_number`, `producer`, `methodology`, and
  `sendai_targets` — surfaced through a `response_detail` accessor on the Monty extension.
- Validation enforcing the mandatory, regex-constrained `type`, the `status` and `methodology` enums,
  Sendai target uniqueness, and rejection of unknown keys, with round-trip serialisation validated
  against the published schema.
- A **Response ↔ Impact pairing helper** that emits an Impact item carrying a single thematic figure,
  pre-wired with the shared `corr_id` and the canonical `derived_from` link (Section 6), including a
  convenience for the multi-thematic split (pattern P4).
- Helpers for **extension layering** — declaring `disaster:` alongside `monty:` on Charter VAP items,
  and `processing:` on value-added products — so transformers reuse existing extensions rather than
  duplicating fields.

## ETL component structure

The reference transformers follow the established `pystac-monty` pattern of extractors, transformers,
and loaders:

- **Extractors** — connectors to source endpoints: the Charter Mapper STAC catalog/supervisor API, and
  the CEMS REST API and RSS feeds.
- **Transformers** — the mapping logic from Section 7: field normalisation, hazard-code translation,
  geometry harmonisation, and the Response/Impact split.
- **Loaders** — STAC-compliant output suitable for ingestion into Montandon via the eoAPI
  infrastructure, monitored through the `montandon-etl-dashboard`.

## Status and next steps

The data model (SW1.1) is released; the `pystac-monty` Response classes and pairing helpers, and the
Charter and CEMS transformers, are in active development for delivery in the next phase, building on the
mapping decisions documented in Section 7. This work is executed in close coordination with Togglecorp,
the maintainer of `pystac-monty` and the Montandon ETL infrastructure. The end-to-end validation
target is Charter and CEMS activations ingested into the Montandon STAC API with correct linkages and
queryable via eoAPI.
