# Conclusion and Next Steps

## Assessment outcome

The technical assessment of STAC integration and interoperability is complete for its central purpose:
Montandon now has a released, standards-based, openly licensed data model into which ESA's EO products
integrate cleanly. The previously undefined Response construct — the one gap in the four-construct
Montandon model — has been designed, implemented, validated, and shipped as **Monty STAC extension
v1.3.0 (SW1.1)**.

The design meets the interoperability objectives of the Statement of Work:

- **A single, source-agnostic vocabulary** describes EO response products consistently across the
  International Charter, Copernicus EMS, and UNOSAT.
- **Reuse of existing community standards** — the Terradue `disaster:` extension and the
  `processing:`/`eo:`/`sar:`/`sat:` families — maximises interoperability and avoids reinventing
  metadata that the EO ecosystem already understands.
- **Explicit boundary rules** keep EO products and the impact figures they inform correctly separated
  and linked, so the same source data is modelled consistently by every ETL author.
- **Discovery through one STAC API** lets IFRC users find EO products alongside all other Montandon
  data using familiar queries.

## Status summary

| Deliverable | Status |
| --- | --- |
| SW1.1 — Harmonised STAC extension | Released as Monty STAC extension v1.3.0 (Apache 2.0) |
| D1.1 — This technical assessment report | Delivered at MTR |
| SW1.2 — Reference ETL pipeline | In development (`pystac-monty` Response support, Charter & CEMS transformers) |
| Per-source analysis documents (Charter, CEMS) | In progress in `docs/model/sources/` |

## Next steps toward WP2

With the interoperability foundation released, the WP1 work continues into the reference ETL
(SW1.2) — completing the `pystac-monty` Response classes and the Charter and CEMS transformers, and
deploying them through `montandon-etl` for end-to-end validation against the Montandon STAC API. These
data entry points then anchor Work Package 2: the **event correlation system** that ties incoming EO
products to the right events, hazards, and impacts (deliverable D2.1), and the **automated analysis
pipeline** that combines this structured disaster data with EO hazard layers to produce decision-ready
analytics for IFRC operations (deliverable D2.2).
