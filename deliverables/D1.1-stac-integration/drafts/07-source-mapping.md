# Data-Source Analysis and Mapping

This section documents how each priority EO source maps onto the Monty model. The mapping decisions
below are the analytical foundation for the reference ETL (Section 8); the detailed per-source analysis
documents are being finalised in the extension repository's `docs/model/sources/` directory alongside
the existing source analyses (GDACS, EM-DAT, DesInventar, and others).

## International Charter (Priority 1)

The Charter Mapper platform already exposes a STAC catalog using the Terradue `disaster:` extension,
which significantly reduces integration complexity: the task is a STAC-to-STAC mapping rather than
building a STAC representation from scratch. The entity mapping is:

| Charter entity | Monty entity | Notes |
| --- | --- | --- |
| Call | Event | The initial trigger that mobilises the Charter; anchors the correlation |
| Activation | Event / Hazard | An activation bundles subsequent deliveries — modelled as an Event, with hazard(s) derived from `disaster:types` |
| Acquisition (calibrated) | Response (`eo-dat`) | The delivered dataset responders use to build products |
| Value-Added Product | Response (`eo-del` / `eo-gra` / `eo-pop` / `eo-vap`) | Best-effort classification; damage figures split to Impact per Section 6 |

![Mapping the International Charter entities onto the Monty model: Calls and Activations become Events, Areas become Hazards, calibrated Acquisitions and Value-Added Products become Responses, and VAP damage figures feed Impact items.](charter-to-monty-map.png)

The `disaster:` extension is declared alongside `monty:` on Charter Response items, with
`disaster:activation_id`, `disaster:activation_status`, `disaster:resolution_class`, and
`disaster:types` reused directly. Charter hazard types map to `monty:hazard_codes`; the Charter Call
ID anchors the `monty:corr_id`. Because the Charter distinguishes object type but not product type,
VAPs are classified as specifically as the metadata allows, falling back to the generic `eo-vap` where
delineation vs. grading cannot be determined.

Access to the Charter catalog is being coordinated with ESA and ACRI-ST; a subset of calls,
activations, and areas is already reachable through the Charter supervisor API, enabling mapping work
to proceed in parallel with full-catalog access provisioning.

## Copernicus EMS Rapid Mapping (Priority 2)

CEMS exposes a public REST API and RSS feeds rather than a STAC catalog, so the ETL transforms JSON API
responses into STAC items. The mapping is:

| CEMS entity | Monty entity | Response type |
| --- | --- | --- |
| Activation (e.g. `EMSR842`) | Event | — (activation code anchors the correlation) |
| Reference Map | Response | `eo-ref` |
| First Estimate Product | Response | `eo-fep` |
| Delineation Product | Response | `eo-del` |
| Grading Product | Response | `eo-gra` (+ Impact items from its damage statistics) |
| Situational Report | Response | `eo-sr` |
| Monitoring variant | Response | same code, `monitoring_number` set |

CEMS-specific fields map into `monty:response_detail`: the activation `code` → `source_id`; product
`type` → the response type code; `statusCode` (`F`/`N`/`W`/`I`) → `status`; `monitoring`/`monitoringNumber`
→ `monitoring_number`. Grading Product damage statistics (per-thematic `affected`/`total`) are split
into separate Impact items (Section 6). A Charter co-activation (`charterNumber`) is expressed as a
`rel: related` link to the corresponding Charter VAP Response item, not as a `disaster:` field. The
resolution class is carried on the linked acquisition items.

## UNOSAT (subject to feasibility)

UNOSAT provides valuable humanitarian mapping products but has no STAC extension and no code
vocabulary, distributing products through HDX with HTML metadata. Its phase-based structure maps to
the source-agnostic EO codes: preliminary situational awareness → `eo-fep`; flood extent → `eo-del`;
damage density → `eo-gra`; population exposure → `eo-pop`; monitoring → `eo-mon`. Because access and
metadata mechanisms require further investigation, UNOSAT is treated as a feasibility assessment: it
is confirmed as a candidate third source, to be integrated within the timeline if access supports it
or documented as a follow-on otherwise. A worked UNOSAT damage-assessment example already validates
against the v1.3.0 schema, demonstrating the mapping is sound.

![UNOSAT earthquake damage-assessment map (Morocco). UNOSAT products carry no source codes of their own; their phase-based products map to the source-agnostic EO codes — damage density to eo-gra, population exposure to eo-pop. Courtesy UNOSAT — UNITAR.](unosat-da-example.jpg)

## Hazard-code interoperability

Across all three sources, native hazard/disaster types map to `monty:hazard_codes`, which carries at
least one code from a recognised classification (the 2025 UNDRR-ISC Hazard Information Profiles being
the primary system). This is what allows an EO product to be correlated with hazard and impact records
originating from entirely different sources — the subject of deliverable D2.1.
