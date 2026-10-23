"""CRS-aware vector/raster operations: overlay, counts, population under the mask."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import rasterize
from rasterio.windows import from_bounds
from rasterio.windows import transform as window_transform
from rasterstats import zonal_stats


def choose_analysis_crs(gdf: gpd.GeoDataFrame) -> str:
    """Choose a local UTM CRS from geometry centroid for metric calculations."""
    if gdf.empty or gdf.crs is None:
        raise ValueError("A non-empty GeoDataFrame with a CRS is required")
    return gdf.estimate_utm_crs().to_string()


def admin_id_column(admin: gpd.GeoDataFrame) -> str:
    """First matching GADM / COD id column (GID_2, GID_1, …)."""
    for column in ("GID_3", "GID_2", "GID_1", "ADM2_PCODE", "ADM1_PCODE", "shapeID", "id"):
        if column in admin.columns:
            return column
    return str(admin.columns[0])


def admin_name_column(admin: gpd.GeoDataFrame) -> str:
    """Human-readable admin name to sit beside the id in exports."""
    for column in ("NAME_3", "NAME_2", "NAME_1", "ADM2_EN", "ADM1_EN", "shapeName", "name"):
        if column in admin.columns:
            return column
    return admin_id_column(admin)


def align_vector_layers(layers: Iterable[gpd.GeoDataFrame], target_crs: str) -> list[gpd.GeoDataFrame]:
    """Reproject all vector layers to target_crs and drop null geometries."""
    aligned = []
    for layer in layers:
        if layer.crs is None:
            raise ValueError("Every vector layer must have a CRS")
        cleaned = layer.loc[layer.geometry.notna()].copy()
        aligned.append(cleaned.to_crs(target_crs))
    return aligned


def overlay_impact_admin(
    impact: gpd.GeoDataFrame, admin: gpd.GeoDataFrame, *, target_crs: str | None = None
) -> gpd.GeoDataFrame:
    """Intersect impact polygons with admin units and add area in square kilometres."""
    if impact.empty or admin.empty:
        return gpd.GeoDataFrame(columns=[*admin.columns, "impact_area_km2"], geometry="geometry", crs=admin.crs)
    crs = target_crs or choose_analysis_crs(admin)
    intersection = gpd.overlay(impact.to_crs(crs), admin.to_crs(crs), how="intersection", keep_geom_type=False)
    intersection["impact_area_km2"] = intersection.geometry.area / 1_000_000
    return intersection


def summarize_impact_by_admin(
    impact: gpd.GeoDataFrame,
    admin: gpd.GeoDataFrame,
    *,
    target_crs: str | None = None,
    id_column: str | None = None,
) -> gpd.GeoDataFrame:
    """Return one row per admin unit with damaged-feature counts and footprint area."""
    if admin.empty:
        raise ValueError("Admin boundaries are required")
    crs = target_crs or choose_analysis_crs(admin)
    key = id_column or admin_id_column(admin)
    name_col = admin_name_column(admin)
    admin_metric = admin.to_crs(crs).copy()
    if impact.empty:
        summary = admin_metric.copy()
        summary["impact_feature_count"] = 0
        summary["impact_area_km2"] = 0.0
        return summary.to_crs("EPSG:4326")

    # Spatial join in metres, then count features and sum footprint area per admin unit.
    impact_metric = impact.to_crs(crs).copy()
    impact_metric["_impact_area_m2"] = impact_metric.geometry.area
    joined = gpd.sjoin(
        impact_metric[["_impact_area_m2", "geometry"]],
        admin_metric[[key, name_col, "geometry"]] if name_col != key else admin_metric[[key, "geometry"]],
        predicate="intersects",
        how="inner",
    )
    stats = (
        joined.groupby(key, dropna=False)
        .agg(impact_feature_count=("_impact_area_m2", "count"), impact_area_km2=("_impact_area_m2", "sum"))
        .reset_index()
    )
    stats["impact_area_km2"] = stats["impact_area_km2"] / 1_000_000
    summary = admin_metric.merge(stats, on=key, how="left")
    summary["impact_feature_count"] = summary["impact_feature_count"].fillna(0).astype(int)
    summary["impact_area_km2"] = summary["impact_area_km2"].fillna(0.0)
    return summary.to_crs("EPSG:4326")


def clip_features_to_impact(features: gpd.GeoDataFrame, impact: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Keep infrastructure (or other) features that intersect the impact layer."""
    if features.empty or impact.empty:
        return features.iloc[0:0].copy()
    left = features.loc[features.geometry.notna()].copy()
    right = impact.to_crs(left.crs)[["geometry"]]
    hits = gpd.sjoin(left, right, predicate="intersects", how="inner")
    return left.loc[left.index.isin(hits.index.unique())].copy()


def population_by_zone(
    admin: gpd.GeoDataFrame, raster_path: str | Path, *, stats: tuple[str, ...] = ("sum", "mean")
) -> pd.DataFrame:
    """Compute population zonal statistics with raster CRS alignment."""
    with rasterio.open(raster_path) as src:
        zones = admin.to_crs(src.crs)
        result = zonal_stats(zones, raster_path, stats=list(stats), nodata=src.nodata, geojson_out=False)
    return pd.DataFrame(result, index=admin.index)


def population_under_impact(
    admin: gpd.GeoDataFrame,
    impact: gpd.GeoDataFrame,
    raster_path: str | Path,
    *,
    all_touched: bool = True,
) -> pd.DataFrame:
    """Sum population raster cells that touch the impact mask, by admin unit.

    Building footprints are much smaller than a 1 km WorldPop cell. ``all_touched``
    counts a cell if any damaged feature overlaps it, which is the intended
    settlement-level exposure estimate for grading products.
    """
    key = admin_id_column(admin)
    if impact.empty:
        return pd.DataFrame({key: admin[key], "pop_total": np.nan, "pop_exposed": 0.0})

    with rasterio.open(raster_path) as src:
        # Clip the raster to the impact extent, then mask cells that touch damage.
        bounds = impact.to_crs(src.crs).total_bounds
        window = from_bounds(*bounds, transform=src.transform).round_offsets().round_lengths()
        window = window.intersection(rasterio.windows.Window(0, 0, src.width, src.height))
        if window.width <= 0 or window.height <= 0:
            return pd.DataFrame({key: admin[key], "pop_total": np.nan, "pop_exposed": 0.0})
        transform = window_transform(window, src.transform)
        pop = src.read(1, window=window).astype("float64")
        nodata = src.nodata
        if nodata is not None:
            pop = np.where(pop == nodata, 0.0, pop)
        pop = np.nan_to_num(pop, nan=0.0)
        shapes = [
            (geom, 1)
            for geom in impact.to_crs(src.crs).geometry
            if geom is not None and not geom.is_empty
        ]
        mask = rasterize(
            shapes,
            out_shape=pop.shape,
            transform=transform,
            fill=0,
            dtype="uint8",
            all_touched=all_touched,
        )
        exposed = pop * mask  # 0 outside the damage mask
        zones = admin.to_crs(src.crs)
        total_stats = zonal_stats(
            zones, pop, affine=transform, stats=["sum"], nodata=0, geojson_out=False
        )
        exposed_stats = zonal_stats(
            zones, exposed, affine=transform, stats=["sum"], nodata=0, geojson_out=False
        )

    output = pd.DataFrame(
        {
            key: admin[key].values,
            "pop_total": [row["sum"] if row["sum"] is not None else 0.0 for row in total_stats],
            "pop_exposed": [row["sum"] if row["sum"] is not None else 0.0 for row in exposed_stats],
        }
    )
    return output


def summarize_exposure(impact: gpd.GeoDataFrame, population: pd.DataFrame, *, id_column: str) -> pd.DataFrame:
    """Aggregate impact area and population statistics by an admin identifier."""
    area = impact.groupby(id_column, dropna=False)["impact_area_km2"].sum().rename("impact_area_km2")
    output = population.join(area, how="left").fillna({"impact_area_km2": 0})
    return output.reset_index()
