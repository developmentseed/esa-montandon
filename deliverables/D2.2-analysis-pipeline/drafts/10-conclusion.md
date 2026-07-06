# Conclusion and Roadmap

## Assessment outcome

The automated analysis pipeline that combines structured disaster data with EO hazard layers is
assessed as a **feasible, low-risk architecture** that turns ESA Earth Observation products into
decision-ready analytics for humanitarian response. Its defining characteristics are:

- **Event-driven** — alert streams from Copernicus EMS, Montandon, and UNOSAT trigger analysis
  automatically, compressing the time from satellite product to actionable figure.
- **Correlation-powered** — the D2.1 correlation system ensures each EO hazard layer is combined with the
  right structured exposure and impact data for that specific disaster.
- **Modular** — analyses are interchangeable, documented notebooks, so methods can be improved,
  specialised, and sustained without re-engineering the pipeline.
- **Open and interoperable** — built entirely from proven open-source components (eoAPI/STAC, Kubernetes,
  Jupyter, TiTiler, `pystac-monty`), released under Apache 2.0, aligned with ESA's Open Science strategy
  and IFRC's operational platforms.

The strategic payoff is direct and runs both ways: it connects space-based observation managed by ESA to
the DREF funding decisions that drive IFRC's response — giving 191 National Societies faster,
evidence-based analytics grounded in authoritative EO data — and it feeds humanitarian prioritisation
**back to the International Charter** to help target its next acquisitions. The three analysis families
the pipeline runs are made concrete as the use cases in deliverable **D2.4** (exposure, impact, and
response prioritisation).

## Roadmap to WP2 execution

This report defines the architecture; the following WP2 execution activities build the pipeline on it:

1. **Phase 2.1 — Modular event analytics.** Develop the exposure, damage, and resilience notebooks for
   the priority hazards (floods, wildfires, earthquakes, cyclones), prioritising peer-reviewed methods
   and validating inputs and outputs with IFRC stakeholders.
2. **Phase 2.2 — Event-driven pipeline.** Implement the listener, correlation-driven orchestration,
   Kubernetes job execution, and artifact publishing described in Sections 3 and 6, wiring the notebooks
   into automated, event-triggered execution.
3. **Phase 2.3 — Documentation and case studies.** Produce the operational documentation and the
   documented case studies demonstrating the pipeline in realistic scenarios (deliverables D2.3 and
   D2.4).

Each phase builds on the released WP1 foundations (D1.1) and the correlation system (D2.1), continuing
the progressive construction in which data integration, correlation, and analytics compound into an
operational capability for combining ESA Earth Observation with humanitarian crisis data.
