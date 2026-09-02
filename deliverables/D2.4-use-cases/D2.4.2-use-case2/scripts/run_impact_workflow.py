"""Run the impact workflow without Jupyter (same steps as notebook 02)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from shapely.geometry import box

from src.baseline_fetcher import fetch_admin_boundaries, fetch_osm_infrastructure, fetch_worldpop_population
from src.copernicus_loader import (
    bbox_from_geodataframe,
    concat_layers,
    copernicus_file,
    filter_impact,
    load_copernicus_layers,
    load_params,
)
from src.spatial_analysis import (
    admin_id_column,
    admin_name_column,
    choose_analysis_crs,
    clip_features_to_impact,
    population_under_impact,
    summarize_impact_by_admin,
)
from src.visualization import export_geodataframe, impact_map


def main() -> None:
    # 1. Local Copernicus vectors, filtered by the damage settings in params.yaml
    params = load_params(ROOT)
    cop_file = copernicus_file(ROOT, params["activation_id"])
    print("loading", cop_file, flush=True)
    impact = filter_impact(concat_layers(load_copernicus_layers(cop_file)), params)
    bbox = params.get("bbox") or bbox_from_geodataframe(
        impact, float((params.get("impact") or {}).get("bbox_buffer_deg", 0.05))
    )
    print("impact", len(impact), "bbox", bbox, flush=True)

    # 2. Admin units that intersect the event bbox
    admin = fetch_admin_boundaries(
        country_code=params["country_code"],
        admin_level=int(params["target_admin_level"]),
        source=params["baseline"]["admin_source"],
    )
    admin = admin[admin.to_crs("EPSG:4326").intersects(box(*bbox))].copy()
    print("admin", len(admin), flush=True)

    # 3. OSM infrastructure (Overpass; individual filters may fail without stopping the run)
    infrastructure = fetch_osm_infrastructure(
        bbox=bbox, infrastructure_filters=params["baseline"]["infrastructure_filters"]
    )
    print("infra", len(infrastructure), infrastructure.attrs.get("overpass_errors"), flush=True)

    # 4. WorldPop 1 km raster (optional: analysis continues if the download fails)
    population_path = None
    try:
        population_path = fetch_worldpop_population(
            country_code=params["country_code"],
            year=int(params["baseline"]["worldpop_year"]),
            bbox=bbox,
            output_path=ROOT / "data" / "baseline" / "population.tif",
        )
        print("population", population_path, flush=True)
    except Exception as exc:
        print("WorldPop failed", exc, flush=True)

    # 5. Counts / area / population by admin, then map + CSV / GeoJSON
    crs = choose_analysis_crs(admin)
    id_col = admin_id_column(admin)
    name_col = admin_name_column(admin)
    impact_admin = summarize_impact_by_admin(impact, admin, target_crs=crs, id_column=id_col)
    exposed_infra = clip_features_to_impact(infrastructure, impact)
    if population_path:
        population = population_under_impact(admin, impact, population_path)
        impact_admin = impact_admin.merge(population, on=id_col, how="left")
        impact_admin["pop_exposed"] = impact_admin["pop_exposed"].fillna(0)
        impact_admin["pop_total"] = impact_admin["pop_total"].fillna(0)
    else:
        impact_admin["pop_exposed"] = None
        impact_admin["pop_total"] = None

    ranked = impact_admin.drop(columns="geometry").sort_values("impact_feature_count", ascending=False)
    cols = [c for c in [id_col, name_col, "impact_feature_count", "impact_area_km2", "pop_exposed", "pop_total"] if c in ranked.columns]
    print(ranked[cols].head(10).to_string(index=False), flush=True)

    point_infra = exposed_infra[exposed_infra.geometry.geom_type.isin(["Point", "MultiPoint"])] if len(exposed_infra) else exposed_infra
    fmap = impact_map(
        {"Exposed population / damage count": impact_admin, "Infrastructure in impact (points)": point_infra},
        choropleth_layer="Exposed population / damage count",
        choropleth_column="impact_feature_count",
    )
    out_html = ROOT / params["outputs"]["map_html"]
    out_csv = ROOT / params["outputs"]["zonal_csv"]
    out_geojson = ROOT / params["outputs"]["zonal_geojson"]
    out_html.parent.mkdir(parents=True, exist_ok=True)
    fmap.save(out_html)
    ranked[cols].to_csv(out_csv, index=False, encoding="utf-8-sig")
    export_geodataframe(impact_admin.to_crs("EPSG:4326"), out_geojson)
    print("wrote", out_html, out_csv, out_geojson, "exposed_infra", len(exposed_infra), flush=True)


if __name__ == "__main__":
    main()
