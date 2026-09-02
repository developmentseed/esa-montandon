"""Load Copernicus CEMS vectors from the local activation folder (no API)."""
from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import pandas as pd
import yaml


def project_root_from_cwd() -> Path:
    """Notebooks live in /notebooks; helpers expect the project root."""
    cwd = Path.cwd()
    return cwd.parent if cwd.name == "notebooks" else cwd


def load_params(root: Path) -> dict:
    """Read config/params.yaml (activation id, country, damage filter, …)."""
    return yaml.safe_load((root / "config" / "params.yaml").read_text(encoding="utf-8"))


def copernicus_file(root: Path, activation_id: str) -> Path:
    """Resolve input/copernicus/{id}/data.gpkg, with data.geojson as fallback."""
    folder = root / "input" / "copernicus" / activation_id
    gpkg = folder / "data.gpkg"
    geojson = folder / "data.geojson"
    path = gpkg if gpkg.exists() else geojson
    if not path.exists():
        raise FileNotFoundError(
            f"No Copernicus data found in {folder}; expected data.gpkg or data.geojson"
        )
    return path


def load_copernicus_layers(path: Path) -> dict[str, gpd.GeoDataFrame]:
    """Read every GeoPackage layer, or a single GeoJSON as {'data': …}."""
    if path.suffix.lower() == ".gpkg":
        names = gpd.list_layers(path)["name"].tolist()
        return {name: gpd.read_file(path, layer=name) for name in names}
    return {"data": gpd.read_file(path)}


def concat_layers(layers: dict[str, gpd.GeoDataFrame]) -> gpd.GeoDataFrame:
    """Stack layers and keep the source layer name in copernicus_layer."""
    frames = []
    for name, layer in layers.items():
        frame = layer.copy()
        frame["copernicus_layer"] = name
        frames.append(frame)
    first_crs = frames[0].crs
    return gpd.GeoDataFrame(pd.concat(frames, ignore_index=True), crs=first_crs)


def filter_impact(impact: gpd.GeoDataFrame, params: dict) -> gpd.GeoDataFrame:
    """Keep features where damage_column == damage_positive_value.

    If that column is missing (typical flood/burn extent), keep all geometries.
    """
    settings = params.get("impact") or {}
    column = settings.get("damage_column", "damage")
    positive = settings.get("damage_positive_value", 1)
    if column not in impact.columns:
        return impact.loc[impact.geometry.notna()].copy()
    selected = impact.loc[impact.geometry.notna() & (impact[column] == positive)].copy()
    return selected


def bbox_from_geodataframe(frame: gpd.GeoDataFrame, buffer_deg: float = 0.05) -> list[float]:
    """Return [west, south, east, north] in WGS84, padded by buffer_deg."""
    if frame.empty:
        raise ValueError("Cannot derive bbox from an empty GeoDataFrame")
    west, south, east, north = frame.to_crs("EPSG:4326").total_bounds
    return [
        float(west - buffer_deg),
        float(south - buffer_deg),
        float(east + buffer_deg),
        float(north + buffer_deg),
    ]


def layer_summary(layers: dict[str, gpd.GeoDataFrame]) -> pd.DataFrame:
    """One inspection row per layer: counts, geometry type, CRS, attribute names."""
    rows = []
    for name, layer in layers.items():
        geom_types = sorted(layer.geometry.geom_type.dropna().unique())
        rows.append(
            {
                "layer": name,
                "feature_count": len(layer),
                "geometry_type": ", ".join(geom_types),
                "crs": str(layer.crs),
                "columns": ", ".join(c for c in layer.columns if c != "geometry"),
            }
        )
    return pd.DataFrame(rows)
