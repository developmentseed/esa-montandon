# Data Discovery and Interoperability Outcomes

The purpose of the data-model work is ultimately practical: an IFRC user must be able to discover and
access EO response products through the existing Montandon interfaces, without specialised knowledge of
each source platform. This section describes how the released model delivers that outcome.

## Discovery through the STAC API

Montandon exposes a STAC API with the OGC-aligned Filter (CQL2) extension. Because Response items carry
`monty:` queryable fields, a client can filter the catalog by the same attributes used for all other
Montandon data:

- **`monty:hazard_codes`** and **`monty:country_codes`** — find every item (event, hazard, impact,
  response) for a given hazard type and country.
- **`monty:corr_id`** — retrieve all items belonging to the same disaster.
- **`roles`** — restrict a query to `response` items.
- **`monty:response_detail.type`** — filter by product type (for example, only `eo-gra` grading
  products or only `eo-del` delineations).

This means a query such as "all delineation and grading products for the October 2024 Spain floods" is
a single CQL2 filter against one API — the complexity of the underlying Charter, CEMS, and UNOSAT
sources is abstracted away. The correlation mechanics that make this possible are the subject of
deliverable D2.1.

## Collections and access policies

Response data is organised into collections that enable filtering by data source, response type, and
hazard category. Each integrated source's data-access policy and attribution requirements are documented
so users understand any restrictions — for example, the Copernicus data policy requires attribution
("© European Union, Copernicus Emergency Management Service"), and Charter products carry their own
attribution terms.

## Open Science publication

All interoperability methods, schemas, and documentation are published as **open technical guidelines**
aligned with ESA's Open Science strategy:

- The **Monty STAC extension** (schema, taxonomy, best practices, boundary rules) — the
  `monty-stac-extension` repository, Apache 2.0.
- The **`pystac-monty`** library and the **`montandon-etl`** pipelines — Apache 2.0.
- All hosted in the IFRC GitHub organisation (`https://github.com/IFRCGo`), with the extension schema
  versioned and published at `https://ifrcgo.org/monty-stac-extension/`.

Publishing the interoperability standard openly and under a permissive licence lowers the barrier for
adoption across the humanitarian and EO communities and invites contribution — directly serving both
ESA's Open Science strategy and the ambition to position Montandon as a reference platform for
crisis-data interoperability.
