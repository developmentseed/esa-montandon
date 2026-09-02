# Montandon Use Case 2: Post-disaster Impact Estimation

Jupyter (and optional script) workflow for **who and what fall inside an observed disaster extent**. It is the second of three Montandon use cases (risk exposure → **impact** → response prioritisation).

After a Copernicus EMS activation, a user can re-run the analysis with their own administrative units, OSM infrastructure, and WorldPop population — more flexible than the published CEMS spreadsheet summary.

Copernicus is **not** queried over the network. You download the activation vectors yourself and drop them in `input/`.

---

## What a user does

1. Download the CEMS geospatial product (GeoPackage preferred) from the [Copernicus EMS mapping portal](https://mapping.emergency.copernicus.eu/).
2. Save it as:

   ```text
   input/copernicus/{activation_id}/data.gpkg
   ```

   Example: `input/copernicus/EMSR884/data.gpkg`. `data.geojson` is accepted if there is no `.gpkg`.
3. Edit `config/params.yaml` (`activation_id` must match the folder name; set `country_code` to the ISO3 of the event country). Comments in that file list allowed values.
4. Activate your conda environment and run the notebooks **in order**, restarting the kernel when you switch activation.
5. Share the files written under `data/` (see [Outputs](#outputs-to-share-with-the-team)).

Notebook 02 needs internet for GADM, WorldPop, and OpenStreetMap (Overpass). Notebook 01 only reads the local file.

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
| `notebooks/02_impact_analysis_workflow.ipynb` | Overlay admin + OSM + WorldPop; map and tables | Yes |
| `notebooks/03_temporal_evolution.ipynb` | Footprint area over time (one snapshot if only one product) | No (uses local file or `data/cems/temporal/`) |

---

## Outputs to share with the team

Notebook 01 does not write files; it is a check.

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

1. New folder: `input/copernicus/EMSR927/data.gpkg` (example).
2. In `params.yaml`: `activation_id`, `country_code`, `hazard_type`. Leave `bbox: null`.
3. After notebook 01, check attribute names. If there is no `damage` column (flood extent), leave the damage settings; all features are used. If the column is `damage_confidence` or `grading`, change `damage_column` / `damage_positive_value` to match.
4. Restart the kernel and run 01 → 02 → 03.

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
│   ├── 02_impact_analysis_workflow.ipynb
│   └── 03_temporal_evolution.ipynb
├── src/                      Shared Python used by the notebooks
│   ├── copernicus_loader.py
│   ├── baseline_fetcher.py
│   ├── spatial_analysis.py
│   ├── visualization.py
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
| `cems_fetcher.py` | Experimental remote CEMS client. Notebooks do not import it. |

### `notebooks/`

Thin orchestration: they read `params.yaml`, call `src/`, and display results. Logic lives in `src/` so it can be reused from `scripts/run_impact_workflow.py`.

### `input/` vs `data/`

- **`input/`** — you put CEMS data here; keep it with the project if the team should reproduce the run.
- **`data/`** — machine-written (maps, CSV, WorldPop/GADM cache). Do not commit; `.gitignore` already excludes it.

---

## How the analysis works (short)

1. Read CEMS polygons from disk. If a damage column exists, keep the positive class only.
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
- A single CEMS grading product yields one point on the temporal chart. Multiple dated GeoJSON files in `data/cems/temporal/` (or several dated layers in the GeoPackage) are needed for a real time series.
