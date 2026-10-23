# Montandon Use Case 2: Post-disaster Impact Estimation

Jupyter (and optional script) workflow for **who and what fall inside an observed disaster extent**. It is the second of three Montandon use cases (risk exposure → **impact** → response prioritisation).

After a Copernicus EMS activation, a user can re-run the analysis with their own administrative units, OSM infrastructure, and WorldPop population — more flexible than the published CEMS spreadsheet summary.

`notebooks/01_cems_api_ingestion.ipynb` reads the public Rapid Mapping API and caches vector layers under `data/cache/cems/{activation_id}/`. Notebooks 02 and 03 read that cache. They do not read `input/`. `01_cems_data_ingestion` still uses a local file when one is present.

---

## What a user does

1. Run `notebooks/01_cems_api_ingestion.ipynb`. It downloads the activation into `data/cache/cems/{activation_id}/`.
2. Edit `config/params.yaml` (`activation_id` must match that cache folder; set `country_code` to the ISO3 of the event country). Comments in that file list allowed values.
3. Activate your conda environment and run notebooks 02 and 03, restarting the kernel when you switch activation. Notebook 03 uses each cached monitoring step. Dated GeoJSON files in `data/cems/temporal/` still override the cache when that folder is not empty.
4. Share the files written under `data/` (see [Outputs](#outputs-to-share-with-the-team)).

The older local notebook `01_cems_data_ingestion` still reads `input/copernicus/{activation_id}/data.gpkg` (or `data.geojson`) and is not used by notebook 02.

Notebook 02 needs internet for GADM, WorldPop, and OpenStreetMap (Overpass). `01_cems_data_ingestion` only reads the local file. `01_cems_api_ingestion` needs internet for the Rapid Mapping API.

---

## Setup

Use a **conda** environment. Creating a new one is optional if you already have a suitable env (then only activate it and install packages).

```powershell
conda create -n montandon python=3.11 -y
conda activate montandon
pip install -r requirements.txt
```

Pick a Jupyter kernel that points at this env when you open the notebooks.

Optionally, run the same analysis as notebook 02 without Jupyter:

```powershell
python scripts/run_impact_workflow.py
```

---

## Workflow

| Notebook | Role | Network |
|---|---|---|
| `notebooks/01_cems_data_ingestion.ipynb` | Inspect local layers, counts, columns, damage filter | No |
| `notebooks/01_cems_api_ingestion.ipynb` | Same kind of check, read from the Rapid Mapping API | Yes |
| `notebooks/02_impact_analysis_workflow.ipynb` | Overlay admin + OSM + WorldPop using the API cache | Yes |
| `notebooks/03_temporal_evolution.ipynb` | Footprint over time from cached monitoring steps | Yes (delivery times; vectors are local) |

---

## Outputs to share with the team

The local notebook 01 does not write files; it is a check. The API notebook caches GeoJSON under `data/cache/cems/`.

**From notebook 02** (main package):

| File | Content |
|---|---|
| `data/impact_by_admin.csv` | Per admin unit: damaged-feature count, footprint km², exposed population, total population |
| `data/impact_by_admin.geojson` | Same table as polygons (QGIS / GIS) |
| `data/impact_map.html` | Interactive map (admin choropleth + infrastructure points) |

**From notebook 03:**

| File | Content |
|---|---|
| `data/temporal_impact.csv` | Date, area km², feature count, source layer |
| `data/temporal_impact.png` | Time-series chart |

Those output names are reused. Copy the folder if you need to keep a previous activation.

---

## Switching to another activation

1. Set `activation_id` and `country_code` in `params.yaml`. Leave `bbox: null`.
2. Run `01_cems_api_ingestion`, then notebook 02. The cache folder is `data/cache/cems/{activation_id}/`.
3. After notebook 01, check attribute names. Grading layers use `damage_gra` (`Destroyed`, `Damaged`, `Possibly damaged`). If that column is missing, every geometry in the latest analysed layer is kept.

---

## Project structure

```text
montandon_impact_estimation/
├── README.md
├── requirements.txt          Python packages
├── .gitignore                Ignores data/, .venv/, caches
├── config/
│   ├── __init__.py
│   ├── config.py             Paths, CRS, service URLs (env overrides)
│   └── params.yaml           User settings for this run
├── input/copernicus/{id}/    Your CEMS file (data.gpkg or data.geojson)
├── notebooks/
│   ├── 01_cems_data_ingestion.ipynb
│   ├── 01_cems_api_ingestion.ipynb
│   ├── 02_impact_analysis_workflow.ipynb
│   └── 03_temporal_evolution.ipynb
├── src/                      Shared Python used by the notebooks
│   ├── copernicus_loader.py
│   ├── baseline_fetcher.py
│   ├── spatial_analysis.py
│   ├── visualization.py
│   ├── cems_api.py           Rapid Mapping client (notebooks 01 API and 02)
│   └── cems_fetcher.py       Unused by notebooks (optional STAC/WFS)
├── scripts/
│   └── run_impact_workflow.py
└── data/                     Generated outputs + download cache (gitignored)
```

### `config/`

| File | Job |
|---|---|
| `params.yaml` | **This is what you edit for each event.** Activation id, country, admin level, damage filter, OSM layers, output paths. |
| `config.py` | Project root, `data/` and cache dirs, WorldPop/Overpass URLs. Change via environment variables if needed; do not put event-specific values here. |

### `src/`

| File | Job |
|---|---|
| `copernicus_loader.py` | Find the local CEMS file, load layers, apply the damage filter, build bbox. |
| `baseline_fetcher.py` | GADM boundaries, Overpass OSM, WorldPop 1 km raster (cached). |
| `spatial_analysis.py` | UTM CRS, count/area by admin, infrastructure inside impact, population under the damage mask. |
| `visualization.py` | Folium map, temporal plot, GeoJSON export. |
| `cems_api.py` | Rapid Mapping client. Notebook 01 downloads vectors; notebook 02 reads that cache. |
| `cems_fetcher.py` | Experimental remote CEMS client. Notebooks do not import it. |

### `notebooks/`

Thin orchestration: they read `params.yaml`, call `src/`, and display results. Logic lives in `src/` so it can be reused from `scripts/run_impact_workflow.py`.

### `input/` vs `data/`

- **`input/`** — you put CEMS data here; keep it with the project if the team should reproduce the run.
- **`data/`** — machine-written (maps, CSV, WorldPop/GADM cache). Do not commit; `.gitignore` already excludes it.

---

## How the analysis works (short)

1. Read the latest cached CEMS layers for the activation. Where `damage_gra` exists, keep Destroyed, Damaged, and Possibly damaged.
2. Derive a bounding box from those polygons (`bbox: null`).
3. Load GADM units for `country_code` / `target_admin_level` and keep those that intersect the box.
4. Query OSM for the selected infrastructure types; keep features that intersect impact.
5. Download WorldPop 1 km, rasterise the impact mask (`all_touched`), and sum population per admin unit.
6. Export admin-level table + choropleth map. Population on a 1 km grid is a **settlement-scale** estimate, not a building-level headcount.

---

## Limitations

- `baseline.admin_source: hdx` is not implemented; use `gadm`.
- `target_age_group` is reserved and unused.
- Overpass may rate-limit roads; hospitals/schools can still succeed.
- Point and line grading layers have little or no polygon area, so the temporal chart can stay near zero while `feature_count` still changes. A folder of dated GeoJSON files in `data/cems/temporal/` overrides the cache.
