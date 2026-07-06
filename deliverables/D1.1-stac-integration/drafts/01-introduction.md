# Introduction and Objectives

## Purpose of this report

This document is deliverable **D1.1 — Report of the technical assessment of STAC integration and
interoperability**, produced under Work Package 1 (WP1) of the ESA activity "Application Development
concerning Disaster Data and Analytics" (SoW ESA-EOP-SG-OF-0779). It presents the technical assessment
and design decisions that establish how Earth Observation (EO) products from ESA-managed platforms are
integrated into the IFRC Montandon Global Crisis Data Bank in an interoperable, standards-based way.

D1.1 accompanies two software deliverables it documents and depends on:

- **SW1.1 — Harmonised STAC extension adapted to relevant EO standards**, released as version 1.3.0 of
  the Monty STAC extension.
- **SW1.2 — Extract, Transform and Load (ETL) pipeline** reference implementation, in development in
  the `pystac-monty` library and the `montandon-etl` deployment repository.

## Context: bridging two data ecosystems

The Montandon Global Crisis Data Bank provides IFRC's 191 National Societies with a harmonised archive
of hazard, impact, and response data, exposed through open, API-driven services built on the
SpatioTemporal Asset Catalog (STAC) standard. Its data model and interoperability posture align
directly with ESA's priorities for open, standards-based EO data access.

This activity bridges the humanitarian and Earth Observation data ecosystems — two communities that
have historically operated in silos despite sharing operational goals in disaster management. ESA's EO
ecosystem, through the **International Charter "Space & Major Disasters"** and the **Copernicus
Emergency Management Service (CEMS)**, produces a wealth of structured, geospatially referenced products
that document a crisis and the mapping response to it. Integrating these products into Montandon brings
a new dimension to a data model that, until now, has focused on hazard and impact records.

## Scope of the technical assessment

WP1 establishes the foundational data architecture. Within that scope, this report assesses and
documents:

- The Montandon data model and the previously undefined **Response** construct that EO products
  populate (Sections 2–4).
- The harmonised Response taxonomy and the `monty:response_detail` field model shipped in SW1.1
  (Section 4).
- **Interoperability through STAC extension layering** — how Monty Response items reuse existing
  community extensions rather than duplicating them (Section 5).
- The **Response ↔ Impact boundary rules** that keep EO products and the impact figures they inform
  cleanly separated and correctly linked (Section 6).
- The **data-source analysis and mapping** for the priority EO sources — the International Charter,
  CEMS, and UNOSAT (Section 7).
- The **reference ETL implementation** approach (SW1.2) and the data-discovery and Open Science
  publication of all outputs (Sections 8–9).

## Relationship to the Statement of Work

This assessment responds to the SoW Task 1 requirements to "conduct a technical review of the
International Charter platform (Charter Mapper), Copernicus Emergency Management Service (CEMS), and
relevant EO platforms" and to "elaborate the mapping between the IFRC Montandon data model and the
Charter data model." All software and documentation described here are released under the Apache 2.0
licence in the IFRC GitHub organisation (`https://github.com/IFRCGo`), consistent with ESA's Open
Science strategy.
