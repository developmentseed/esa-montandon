# EO Source Landscape and Framework Survey

Before designing the Response construct, we surveyed the established frameworks that classify disaster
response products and activities, to determine whether an existing taxonomy could be adopted and what
structure the Monty Response taxonomy should take. The full survey is published as an appendix to the
Monty Response taxonomy reference; this section summarises the findings that drove the design.

## Priority EO sources

Three Earth Observation services are the primary integration targets for this activity. They are the
sources whose products populate the Response construct.

### International Charter "Space & Major Disasters"

A worldwide collaboration between space agencies that provides satellite-derived data and products to
support disaster response, activated within hours to days of a fast-onset disaster. The Charter Mapper
platform already exposes a **STAC catalog** and uses the **Terradue `disaster:` STAC extension** as its
data model — the authoritative machine-readable schema for Charter items. Its object model distinguishes
activations, areas, acquisitions (raw satellite data), and value-added products (VAPs — the processed
maps). Crucially, the `disaster:` extension classifies object type (`activation`, `area`, `acquisition`,
`vap`) and hazard type, but does **not** further distinguish product types (delineation vs. grading) —
a gap the Monty response type codes fill.

### Copernicus Emergency Management Service (CEMS) Rapid Mapping

An EU-funded satellite mapping service and the most formally specified EO product taxonomy of all
frameworks surveyed. CEMS defines five product types with stable, published three-letter codes:

| Code | Product | Timing | Description |
| --- | --- | --- | --- |
| `REF` | Reference Product | Pre-event | Baseline of territory and assets prior to the emergency |
| `FEP` | First Estimate Product | Post-event, hours | Fast, rough assessment of the most affected locations |
| `DEL` | Delineation Product | Post-event | Event impact extent and affected area |
| `GRA` | Grading Product | Post-event | Damage grade, distribution, and extent (superset of DEL) |
| `SR` | Situational Report | Cross-cutting | Online report presenting the event and activation |

CEMS exposes a public REST API and RSS alert feeds rather than a STAC catalog, and there is no CEMS
STAC extension. Delineation and Grading products can be re-issued as **monitoring** updates.

![Copernicus EMS delineation product (Monitoring #1) for activation EMSR773 over Valencia, Spain — the observed flood extent, mapped to the eo-del response type. © European Union, Copernicus Emergency Management Service.](cems-del-example.png)

![Copernicus EMS grading product for EMSR773 (AOI03 Horta Sud, Valencia region, Spain) — per-feature damage classification, mapped to the eo-gra response type. © European Union, Copernicus Emergency Management Service.](cems-gra-example.png)

### UNOSAT (UNITAR) Rapid Mapping

UNITAR's satellite analysis service producing humanitarian mapping products, with a strong focus on
floods. Its products are organised into service phases (pre-crisis baseline; ~24-hour preliminary
situational awareness; ~72-hour impact and damage assessment; ongoing monitoring). UNOSAT uses
descriptive product names with no published code vocabulary and no STAC extension, distributing
products through the Humanitarian Data Exchange (HDX).

## Secondary frameworks (humanitarian and policy)

The survey also assessed humanitarian and policy frameworks — **OCHA 3W/4W**, the **IASC Cluster
system**, the **IFRC Emergency Plan of Action (EPoA)/DREF** sectors, the **Sendai Framework**
monitoring indicators, and the **PDNA** methodology. These describe the humanitarian sector layer
(shelter, health, WASH, protection, and so on) or policy-level outcome metrics rather than EO product
types. They inform the humanitarian (`hum-*`) and financial (`fin-*`) placeholder domains of the
taxonomy and the Sendai crosswalk, but they are secondary to the EO focus of this contract.

## Findings that drove the design

Three conclusions from the survey shaped the Response taxonomy:

1. **No single framework can be adopted wholesale.** CEMS has the most code-ready product vocabulary;
   the Charter has a live STAC extension but no product-type codes; UNOSAT has neither. A harmonised,
   **source-agnostic** taxonomy is required so that a delineation map is described the same way whether
   it comes from CEMS, the Charter, or UNOSAT.
2. **Reuse existing STAC standards where they exist.** The Terradue `disaster:` extension is the live
   Charter data model and must be *used*, not merely referenced. The design therefore layers Monty
   fields onto existing extensions rather than duplicating them (Section 5).
3. **A shallow, extensible structure fits.** The response space is small and still settling, so a
   two-level `domain → type` hierarchy is appropriate — richer than a flat list, but able to grow
   without breaking existing codes. This mirrors the shape of the frameworks surveyed, none of which
   uses more than two levels for response products.
