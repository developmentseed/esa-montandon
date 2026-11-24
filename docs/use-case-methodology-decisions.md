# Use case notebooks: methodology review decisions

Decision log for [issue 60](https://github.com/developmentseed/esa-montandon/issues/60), which compares the two use
case notebooks in the notebook factory with the [proposed use case document](https://docs.google.com/document/d/1NEs8asslOlhcdOF30Tc1byJShRvxju3RVzmaxh9QOgY/edit?tab=t.0).
Answers come from the MapAction SMEs (comments on the issue) and from checks made while implementing. Last updated 2026-11-24.

| Notebook | Change | Status |
|---|---|---|
| Use Case 1, `uc1-risk-exposure` 0.4 | [notebook-factory#52](https://github.com/developmentseed/notebook-factory/pull/52) | in review |
| Use Case 2, `uc2-impact-estimation` 0.5 | same decisions, applied to the Copernicus EMS notebook | in progress |

## Decisions

| # | Question | Decision | Why |
|---|---|---|---|
| UC1.1 | Wildfire has no data | **Dropped** (and heatwave, which had no data either) | INFORM has no global wildfire methodology; the SME prefers a smaller, robust method. Revisit if one is found. |
| UC1.2, UC1.3 | Which infrastructure, from which source | **Health, schools, airports, ports** from OpenStreetMap through HOT's per-country GeoParquet extracts; one centroid per feature | See "Infrastructure source". |
| UC1.2, UC2.2 | Roads | **Dropped** | The exposure method only handles points. Road exposure is on the 2027 roadmap (HeiGIT already has a method). |
| UC1.4 | One population provider and resolution | **WorldPop R2025A for both**: 1 km in UC1, 100 m in UC2 | The SME accepts different resolutions (UC1 aggregates modelled hazards, UC2 uses observed events) but prefers one provider. WorldPop also has the age and sex structure that GHSL lacks. |
| UC2.1 | Children under five | **Under 5 and under 15**, broken out of the total people exposed | Exact in WorldPop; the total stays the headline. |
| UC2.3 | Data beyond Copernicus EMS | **Not in this version** | The SME suggests a separate notebook for Charter / WFP ADAM. |

## Infrastructure source

OSM tags used (HOT publishes one file per country and theme, whose columns are the OSM tags):

| Layer | HOT file | Filter |
|---|---|---|
| Health facilities | `health_facilities` | `healthcare=*`, or `amenity` hospital, clinic, doctors, dentist, pharmacy |
| Schools | `education_facilities` | `amenity=school` (the SME's tag; kindergartens, colleges and universities are no longer counted) |
| Airports | `airports` | `aeroway=aerodrome` (the airport itself: HOT's layer also holds runways, taxiways and helipads) |
| Ports | `sea_ports` | `industrial=port` or `harbour=yes` or `landuse=port`/`harbour` |

Ports use more than the SME's `landuse` tags because the OSM wiki marks `landuse=port` obsolete in favour of
`landuse=industrial` + `industrial=port`. In the Philippines the SME's tags match 17 features and `industrial=port` 405 (450 in all);
in Sri Lanka 10, 5 and 25.

Why not the alternatives (measured on 2026-11-23 unless noted):

| Source | Finding |
|---|---|
| OSM Layercake (used before) | Good for health and schools, but it has no `aeroway` column and `landuse` is not one of the keys that admit a feature, so no airports or ports. |
| Overpass API | Exact tags, but the public endpoints answered 502 or timed out and the policy asks automated clients to run their own instance. |
| Overture Maps | No port or harbour class; places are points only. Not tested further. |
| HeiGIT datasets on HDX | 802 per-country datasets (road surface, accessibility, risk indicators). A title search found no facility points (about 75% sure). |
| OurAirports, Oxford Port Watch (HDX) | Usable point data, but not OSM, with inconsistent or custom licences. Kept as fall-backs. |

HOT counts used as a check: Nepal has 7,355 health facilities, 25,684 schools and 58 aerodromes, and no matching port (it is landlocked);
Sri Lanka has 30 aerodromes and 25 ports. The files are rebuilt monthly (the notebooks print the file date), are range-readable, and the
URL is looked up through the HDX API (HOT publishes about 240 countries per theme there).

## Population

- Source: WorldPop Global2 R2025A, through the WorldPop API v3 (`POST /raster`): only the cells inside the area are transferred, and an area
  over the API's limit (100,000 km² without a key, 500,000 km² with one) is requested in tiles. A key is the `WORLDPOP_API_KEY` secret.
- WorldPop's own file server ignores HTTP range requests, so reading a window of its files is not possible; whole country files are 0.6 to
  15 MB at 1 km but 30 to 740 MB per band at 100 m.
- The earlier UC1 experiment with GHSL at 100 m was dropped.
- Caveats: R2025A is published as an alpha release with national totals aligned to the UN WPP; the numbers differ from the old
  WorldPop 2020 figures. WorldPop's age classes are 5 years wide, so **under 18 is not exact** (the API widens 0 to 17 into 0 to 19).
- Citation (CC BY 4.0): population doi:10.5258/SOTON/WP00839, age and sex doi:10.5258/SOTON/WP00841.

## Open questions for the SMEs

1. **Ports**: are `industrial=port`, `harbour=yes` and `landuse=port|harbour` the right set? (`harbour=yes` also marks a few small features.)
2. **Children**: is under 5 plus under 15 enough, or is under 18 needed (which would be approximate)?
3. **Schools**: should kindergartens, colleges and universities be counted too?
4. **Airports**: is `aeroway=aerodrome` alone right, or should small `aeroway=airstrip` and heliports count?
