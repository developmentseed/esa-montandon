# Introduction and Scope

## Purpose of this report

This document is deliverable **D2.1 — Report of the technical assessment of the event correlation
system adapted to relevant EO data products**, produced under Work Package 2 of the ESA activity
"Application Development concerning Disaster Data and Analytics". It assesses the mechanism by which
Montandon links records about the same disaster across heterogeneous sources, and documents how that
mechanism is applied to Earth Observation response products from the International Charter, Copernicus
EMS, and UNOSAT.

## The correlation problem

Montandon collects four kinds of item — Event, Hazard, Impact, and Response (see deliverable D1.1) —
from many independent sources. Every source produces at least an Event item that provides context;
hazards, impacts, and responses attach to that context. The correlation problem is to determine, for
any two items, whether they describe the **same real-world disaster**, even though they originate from
different organisations that share no common identifier.

This is not a trivial join. Real disasters are frequently **multi-hazard**: an earthquake triggers a
tsunami and landslides; a drought is followed by a heatwave and then flooding. The combined impact of
such cascades differs from the sum of the individual events, and disaster reporting increasingly needs
to recognise these connections rather than treat each hazard in isolation. Montandon's data model — and
its correlation system — are designed for exactly this heterogeneity.

## Why correlation matters for EO integration

The integration of ESA EO products (deliverable D1.1) gives Montandon a new class of item: EO Response
products such as Copernicus delineation maps, Charter value-added products, and UNOSAT damage
assessments. These products are only useful in context. A flood-extent map is valuable because it can
be placed against the event that caused it, the hazard it delineates, and the population impact it
informs.

The correlation system is what supplies that context. Adapting it to EO products means answering, for
each incoming product:

- **Which event does this product belong to?** (attach a Copernicus/Charter/UNOSAT product to the right
  Montandon event and hazard)
- **What impacts does it inform?** (link the damage figures a product carries to separate Impact
  records)
- **How does it relate to other EO products?** (cross-source co-activations, and monitoring updates of a
  prior product)

## Scope

This report covers: the two correlation mechanisms Montandon provides (Section 2); the queryable fields
and operators they rely on (Section 3); the four core correlation algorithms (Section 4); their
adaptation to EO response products, which is the new work of this deliverable (Section 5); an end-to-end
worked example (Section 6); the implementation and API (Section 7); and the assessment findings and the
correlation system's role as the matching engine for the WP2 analysis pipeline documented in D2.2
(Section 8).
