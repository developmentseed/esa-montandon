# Executive Summary

This report documents the technical assessment of STAC integration and interoperability carried out
under Task 1 of the ESA "Application Development concerning Disaster Data and Analytics" activity. Its
purpose is to establish the data-model foundations that let Earth Observation (EO) products from
ESA-managed platforms flow into the IFRC Montandon Global Crisis Data Bank, and to make those products
discoverable and usable by the humanitarian community through a single, standards-based interface.

## The strategic opportunity

Disaster response draws on two data ecosystems that have historically operated in isolation. On one
side, ESA-managed and ESA-affiliated services — the **International Charter "Space & Major Disasters"**
and the **Copernicus Emergency Management Service (CEMS)** — produce authoritative, geospatially
precise maps of what is happening on the ground during a crisis. On the other, the humanitarian sector
— coordinated through the **IFRC**, **UN OCHA**, and **UNOSAT/UNITAR** — maintains the operational
record of events, their human impact, and the response mounted by 191 National Societies and their
partners.

Montandon is the first platform designed to hold both in one harmonised, open catalogue. This activity
connects ESA's EO assets into that catalogue. The result is not another data silo but a shared
"language" — an extension of the open **SpatioTemporal Asset Catalog (STAC)** standard — through which
an IFRC information manager can discover a Copernicus flood delineation or a Charter damage map for a
given disaster without needing to know how each source platform works internally.

## What has been achieved

The central deliverable of Task 1 — the harmonised STAC extension (SW1.1) — has been **specified,
implemented, and released** as version 1.3.0 of the Monty STAC extension, published openly under the
Apache 2.0 licence in the IFRC GitHub organisation. This release closes a long-standing gap in the
Montandon data model: the **Response** construct, which describes actions taken and products produced
during a crisis, is now fully defined alongside the existing Event, Hazard, and Impact constructs. EO
products from the Charter, CEMS, and UNOSAT map directly onto this new construct.

Delivering the model as a released, standards-compliant, openly licensed specification — rather than a
paper design — is deliberate. It demonstrates that the interoperability approach works in practice, it
aligns with ESA's Open Science strategy, and it positions Montandon as a credible reference platform
for crisis-data interoperability that the wider humanitarian and EO communities can adopt and extend.

## Highlights at MTR

- **A single interoperability standard, shipped.** The harmonised Response data model (SW1.1) is
  released as Monty STAC extension v1.3.0 — open, versioned, and Apache-2.0 licensed in the `IFRCGo`
  GitHub organisation.
- **ESA EO products have a home in Montandon.** International Charter, Copernicus EMS, and UNOSAT
  products now map onto a source-agnostic Response taxonomy, so a delineation or damage map is
  described the same way regardless of which agency produced it.
- **Reuse over reinvention.** The model layers onto existing community standards (the Terradue
  `disaster:` extension for the Charter, plus `processing:`, `eo:`, `sar:`, `sat:`) rather than
  duplicating them — maximising interoperability and minimising bespoke integration.
- **Clear rules that prevent double-counting.** An explicit Response ↔ Impact boundary keeps EO
  products and the humanitarian impact figures they inform cleanly separated and correctly linked.
- **On track for the reference ETL (SW1.2).** With the model released, the reference pipelines that
  ingest Charter and CEMS products into Montandon are in active development for delivery in the next
  phase.

The remainder of this report presents the technical detail behind these results: the Montandon data
model and the Response gap it closes (Sections 2–4), the STAC extension-layering and Response ↔ Impact
boundary rules (Sections 5–6), the source-by-source mapping of Charter, CEMS, and UNOSAT (Section 7),
and the reference ETL and data-discovery approach (Sections 8–9).
