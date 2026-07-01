# Executive Summary

This report presents the technical assessment and reference architecture of the **automated analysis
pipeline** that combines structured disaster data with Earth Observation (EO) hazard layers. It is
deliverable D2.2 of the ESA "Application Development concerning Disaster Data and Analytics" activity.
Consistent with the mid-term stage of the work, it is an **architecture-level assessment**: it
establishes the design, the data-combination approach, and the technology choices, while the specific
hazard-analysis methodologies are developed during Work Package 2 execution.

## The opportunity

ESA-managed EO services produce authoritative hazard layers during a crisis — Copernicus and Charter
flood extents, burned areas, and building-damage grades. The humanitarian sector maintains the
structured record of the event and the population and infrastructure it exposes. Neither is fully
actionable alone: an EO flood-extent map does not by itself say how many people are affected, and a
population dataset does not say where today's flood actually reached. **Value comes from combining
them.**

The pipeline assessed here does exactly that, automatically. When a new disaster is detected, it brings
together the EO hazard layer and the structured exposure data correlated to the same event, runs a
documented analysis, and produces a decision-ready output — an exposure or damage estimate — that feeds
directly into IFRC's **Disaster Response Emergency Fund (DREF)** process. The aim is to turn ESA EO
products from maps that an expert must interpret into analytics that a humanitarian decision-maker can
act on within the first hours of a response.

## The approach in brief

The pipeline is **event-driven and modular**. Alert streams from Copernicus EMS, Montandon, and UNOSAT
trigger analysis automatically; the event correlation system (deliverable D2.1) determines which
structured data an EO layer should be combined with; analyses are packaged as interchangeable notebooks
so methods can be improved or substituted without re-engineering the pipeline; and outputs are published
where IFRC operational users already work. The whole design is built on open standards and open-source
components, released under the Apache 2.0 licence.

## Highlights at MTR

- **ESA EO products made decision-ready.** The architecture turns Copernicus and Charter hazard layers
  into exposure and damage analytics that feed the IFRC DREF funding process — connecting space-based
  observation to life-saving funding decisions.
- **Automated, event-driven response.** New activations from Copernicus EMS or new Montandon events
  trigger analysis automatically, compressing the time from satellite product to actionable figure.
- **Correlation-powered.** The pipeline reuses the D2.1 correlation system to combine each EO hazard
  layer with the *right* structured exposure and impact data for that specific disaster.
- **Modular and sustainable.** Analyses are interchangeable notebooks with documented methods, so IFRC
  and its partners can adapt and extend them — an approach designed for longevity beyond the project.
- **Open and interoperable by construction.** Built on eoAPI/STAC, Kubernetes, and Jupyter, all
  Apache 2.0 in the IFRC GitHub organisation, aligned with ESA's Open Science strategy and IFRC's
  operational platforms.

The remainder of this report sets out the conceptual approach (Section 2), the reference architecture
and its event-driven orchestration (Sections 3 and 6), the modular analytics and data-combination
model (Sections 4–5), the technology choices and interfaces (Sections 7–8), an architecture-level
feasibility and risk assessment (Section 9), and the roadmap to WP2 execution (Section 10).
