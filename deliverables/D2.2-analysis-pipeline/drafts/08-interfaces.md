# Interfaces and Dependencies

The pipeline sits at the top of a progressive construction and depends on the outputs of Work Package 1
and deliverable D2.1. This section makes those interfaces explicit.

## Inputs

| Input | Provided by | Used for |
| --- | --- | --- |
| Harmonised STAC extension (SW1.1) | WP1 / D1.1 | The data model for EO Response items and their hazard-layer geometry |
| Reference ETL pipelines (SW1.2) | WP1 / D1.1 | Ingestion of Charter and CEMS products into Montandon |
| Correlation system | D2.1 | Attaching each EO hazard layer to the right event, hazard, and impact data |
| Response ↔ Impact boundary rules | WP1 / D1.1 | Clean, structured Impact records the analytics consume |
| Structured crisis data | Montandon (events, hazards, impacts, EO response products, DREF history) | The disaster context correlated to each event |
| Baseline exposure / vulnerability & base layers | External repositories used *directly* by the analysis — population (WorldPop/GHSL), admin (GADM/CODs), infrastructure (OSM), hazard/vulnerability (INFORM, STORM, Aqueduct, GEM). Not imported into Montandon. OCHA HDX is used within MapAction's own process rather than imported into Montandon. | Intersected with the EO footprints |
| Alert streams | Copernicus EMS RSS, Montandon, UNOSAT API | Event-driven triggers |
| *(future)* EOC field observations | Planned EOC–Montandon connection | Progressive refinement of rankings (D2.4 Use Case 3) |

## Outputs

| Output | Form | Consumer |
| --- | --- | --- |
| Analysis artifacts | Static HTML, PDF, JSON, map layers | IFRC GO platform, DREF workflow |
| Analysis outputs as STAC | Dedicated STAC collection(s) + STAC API methods (e.g. `response-prioritisation`), linked via `corr_id` to the event and source activation | **Charter clients (Charter Mapper overlay, Charter chatbot)**, IFRC GO, downstream apps |
| Prioritisation feedback | Ranked AOIs correlated to the Charter activation | **International Charter** — to help target the next acquisition / mapping |
| Reusable notebooks | Parameterised Jupyter notebooks | WP3 interactive tools and training |

## Dependency summary

- **On WP1 (D1.1):** the EO products the pipeline analyses exist in Montandon only because WP1 defined
  the Response model and the ETL that ingests them; and the structured Impact records the pipeline reads
  are the product of the WP1 Response ↔ Impact boundary rules.
- **On D2.1:** the pipeline's correctness depends on the correlation system to combine each EO layer
  with the right structured data.
- **Toward WP3:** the pipeline's notebooks and outputs are the raw material for the WP3 interactive
  tools, visualisation components, and training packages.

## Boundary of this deliverable

This report defines the architecture and interfaces. The concrete per-hazard methodologies, the output
schemas, and the operational validation with IFRC users are WP2 execution activities documented in the
subsequent deliverables (the readiness review D2.3 and the case-study report D2.4). Keeping the
architecture and interfaces stable while the analytical content is developed is a deliberate design
choice that de-risks delivery.
