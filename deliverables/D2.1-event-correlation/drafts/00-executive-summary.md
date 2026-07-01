# Executive Summary

This report documents the technical assessment of the **event correlation system** and how it is
adapted to link Earth Observation (EO) products from ESA-managed platforms to the humanitarian disaster
records held in the IFRC Montandon Global Crisis Data Bank. It is deliverable D2.1 of the ESA
"Application Development concerning Disaster Data and Analytics" activity.

## The problem the correlation system solves

A single disaster is described by many organisations at once, in incompatible ways. The **UN** and
national agencies register the event (through GDACS, GLIDE, EM-DAT); the **IFRC** records its human
impact and mounts a response; and ESA's EO services — the **International Charter "Space & Major
Disasters"** and the **Copernicus Emergency Management Service (CEMS)** — produce authoritative maps of
the flooded area, the burned extent, or the building damage. Each uses its own identifiers. Today, an
analyst wanting "everything known about this disaster" must manually reconcile these sources.

The correlation system is what makes that reconciliation automatic. It ties every record about the same
disaster — regardless of which organisation produced it — into a single, navigable cluster. Adapting it
to EO products means that when a Copernicus or Charter map is ingested, it is automatically attached to
the right event, hazard, and impact records, so an IFRC information manager finds the ESA EO product
sitting alongside the humanitarian data for that crisis, in one query.

## The approach

Montandon uses two complementary mechanisms, both built on open standards:

- A **correlation identifier** — a deterministic code derived from a disaster's date, country, location,
  and hazard type — that gives every related item a shared, stable join key.
- **Dynamic correlation queries** — standards-based STAC API filters that match items by hazard, country,
  time, and geography at query time, so users can correlate flexibly and handle complex multi-hazard
  events without any pre-computation.

For EO products specifically, the system anchors each product to its source identifier (a Copernicus
EMSR activation code, a Charter activation number, a UNOSAT product code), attaches it to the correct
event, and — where an EO product also reports damage figures — links those to separate impact records
using an explicit provenance edge. Cross-source ties (a Copernicus activation that co-occurs with a
Charter activation) and time-series monitoring updates are handled by the same mechanism.

## Highlights at MTR

- **"Everything about this disaster" in one place.** The correlation system unifies UN, IFRC, and ESA
  EO records for the same crisis into a single queryable cluster, breaking down the silos between the
  humanitarian and EO data ecosystems.
- **Authoritative ESA products, automatically placed.** Copernicus EMS, International Charter, and
  UNOSAT products are attached to the correct event, hazard, and impact records on ingest — no manual
  reconciliation.
- **Standards-based and transparent.** Correlation uses the open STAC API and OGC Common Query Language
  (CQL2); the logic is visible and adjustable, not a black box.
- **Built for real disasters.** The design explicitly handles multi-hazard cascades, multi-country
  events, cross-source co-activations, and evolving situations tracked through monitoring updates.
- **Foundations already in place.** The correlation model, algorithms, and the queryable data model it
  relies on are released as part of the Montandon platform and its open STAC extension; this report
  documents their adaptation to EO products and their role as the matching engine for the WP2 analysis
  pipeline (D2.2).

The remainder of this report presents the correlation model and its two mechanisms (Sections 2–3), the
core correlation algorithms (Section 4), their adaptation to EO response products (Section 5), an
end-to-end worked example (Section 6), and the implementation and its relevance to WP2 (Sections 7–8).
