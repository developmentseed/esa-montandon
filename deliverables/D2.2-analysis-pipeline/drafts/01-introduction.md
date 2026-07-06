# Introduction and Scope

## Purpose of this report

This document is deliverable **D2.2 — Report of the technical assessment of the automated analysis
pipeline combining structured disaster data with EO hazard layers**, produced under Work Package 2 of
the ESA activity "Application Development concerning Disaster Data and Analytics". It defines the
reference architecture for an automated pipeline that enriches humanitarian disaster records with
analytics derived from Earth Observation hazard products.

## What "combining structured data with EO hazard layers" means

Two complementary kinds of data are brought together:

- **Structured disaster data** — the Montandon Event, Hazard, and Impact records, plus the exposure and
  vulnerability data associated with a location: population distribution, critical infrastructure,
  socio-economic indicators, sourced from Montandon, OCHA's Humanitarian Data Exchange (HDX), and
  related repositories.
- **EO hazard layers** — the geospatial footprints carried by EO Response products: flood extents,
  burned areas, and building-damage grades produced by Copernicus EMS, the International Charter, and
  UNOSAT, integrated into Montandon under Work Package 1 (deliverable D1.1).

The pipeline's core operation is to **intersect** an EO hazard footprint with the exposure and impact
data correlated to the same event, producing quantified analytics — how many people fall within today's
flood extent, how much infrastructure lies in the graded-damage zone — that a humanitarian
decision-maker can use directly.

## Scope of this assessment

Per the mid-term stage of the activity, this is an **architecture-level** assessment. It documents:

- the conceptual approach to combining the two data types (Section 2);
- the reference architecture of the event-driven pipeline (Section 3);
- the modular analytics workflow model (Section 4);
- the data-combination patterns and their dependency on the WP1 data model (Section 5);
- the event-driven orchestration (Section 6);
- the technology choices and rationale (Section 7);
- the interfaces and dependencies on WP1 and D2.1 (Section 8);
- an architecture-level feasibility and risk assessment (Section 9); and
- the roadmap to WP2 execution (Section 10).

The **specific hazard-analysis methodologies** — the exposure, damage, and resilience algorithms per
hazard type — are named at architecture level here and developed in detail during WP2 execution
(Phase 2.1), validated with IFRC stakeholders, and documented in the subsequent WP2 deliverables
(D2.3, D2.4). This separation keeps the architecture stable while the analytical content evolves.

## Relationship to the other deliverables

D2.2 builds on the two preceding deliverables. Work Package 1 (D1.1) integrated ESA EO products into
Montandon as Response items carrying hazard-layer geometry. Deliverable D2.1 established the correlation
system that ties each EO layer to the right structured data. This report describes the pipeline that
consumes both to produce analytics — the third layer of a progressive construction in which each phase
builds on its predecessor.
