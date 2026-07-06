# Feasibility and Risk Assessment

This section assesses the architecture's feasibility at the mid-term stage and the principal risks,
with mitigations. It is an architecture-level assessment; operational validation is a WP2 execution
activity.

## Feasibility

The architecture is assessed as **feasible with low technical risk**, for three reasons:

- **Every component is proven and already in the stack.** eoAPI/STAC, Kubernetes, Jupyter/papermill,
  TiTiler, and `pystac-monty` are existing, open-source building blocks operated across Montandon and
  Development Seed's EO platforms. The pipeline composes them rather than inventing infrastructure.
- **The hard prerequisites are in place.** The data model (SW1.1) is released, and the correlation
  system (D2.1) that makes data combination correct is specified and built on the same STAC foundation.
- **The design is incremental.** Because analyses are modular notebooks registered in a matrix, the
  pipeline can deliver value with a single hazard/analysis pair and grow without re-engineering.

## Key risks and mitigations

| Risk | Assessment | Mitigation |
| --- | --- | --- |
| **EO product latency/availability** — a product may arrive hours after the event, or not at all for a given disaster | Medium | Montandon events trigger analysis independently of EO availability; EO-derived analyses run and update as products arrive (monitoring updates) |
| **Data-quality and coverage gaps** in exposure layers | Medium | Modular notebooks fall back to available layers and document data-quality limitations; multiple exposure sources (Montandon, HDX, national) reduce single-source dependence |
| **Compute cost under concurrent events** | Low–Medium | Queue-decoupled, resource-bounded Kubernetes jobs scale horizontally and are bounded per job; non-urgent analyses can be deprioritised |
| **Method validity across contexts** | Medium | Priority to peer-reviewed, openly accessible methods; validation with IFRC stakeholders during WP2 execution; substitutable notebooks allow region-specific variants |
| **Sustainability beyond the project** | Medium | Open-source, modular design in the IFRC GitHub organisation; notebooks documented for adaptation; alignment with IFRC operational platforms and MapAction training |

## Alignment with the Statement of Work

The architecture supports the WP2 deliverable chain: the event-correlation assessment (D2.1) and this
pipeline assessment (D2.2) at mid-term; the readiness review of the automated analysis pipeline (D2.3);
and the case studies demonstrating integrated analytics in realistic operational scenarios (D2.4). The
modular, event-driven design is what makes the later readiness and case-study milestones achievable on
the WP2 schedule.
