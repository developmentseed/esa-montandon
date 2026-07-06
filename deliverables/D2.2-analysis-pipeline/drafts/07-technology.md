# Technology Choices and Rationale

The architecture is deliberately built from proven, open-source components already in use across the
Montandon platform and Development Seed's EO work. This minimises technical risk, maximises
interoperability, and keeps every deliverable open under the Apache 2.0 licence.

| Component | Role in the pipeline | Rationale |
| --- | --- | --- |
| **eoAPI / STAC API** | Catalog and query layer for structured data and EO layers | The Montandon platform is already built on eoAPI; the pipeline reuses its STAC API and CQL2 querying rather than introducing a new data layer |
| **`pystac-monty`** | Typed access to Monty items and correlation from within notebooks | The reference library for the Monty model (D1.1); gives notebooks high-level data access without raw queries |
| **Kubernetes** | On-demand, isolated, resource-bounded analysis jobs | Scales to concurrent events; isolates failures; the Montandon infrastructure already deploys on Kubernetes |
| **Jupyter + papermill** | Parameterised, reproducible notebook execution | Notebooks are both the development medium for analysts and the execution unit in production; papermill injects per-event parameters |
| **Message queue / event bus** | Decouples detection from computation | Absorbs bursts, orders work, and lets stages scale and fail independently |
| **Cloud object storage** | Durable storage of analysis artifacts | Standard, low-cost, and directly linkable from IFRC GO |
| **TiTiler** | Dynamic tiling for raster visualisation | Development Seed's open-source dynamic tile server; renders EO and derived layers on the fly for notebooks, IFRC GO, and the WP3 tools |

## Design rationale

- **Reuse over novelty.** Every major component is already part of the Montandon or Development Seed EO
  stack. The pipeline composes existing, battle-tested building blocks rather than introducing new
  infrastructure, which lowers delivery risk and accelerates implementation.
- **Standards-based interoperability.** STAC, OGC CQL2, and OGC-aligned tiling (WMTS / OGC API Tiles via
  TiTiler) keep the pipeline interoperable with standard GIS clients and with ESA's EO infrastructure.
- **Reproducibility and auditability.** Notebook-based analyses executed as isolated jobs produce
  regenerable, inspectable results — important for outputs that inform funding decisions.
- **Open Science.** All software is released under Apache 2.0 in the IFRC GitHub organisation, aligned
  with ESA's Open Science strategy and enabling community reuse and contribution.
