"""Folium maps, time-series plots, and GeoJSON/HTML export."""
from __future__ import annotations

from pathlib import Path

import folium
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from branca.colormap import linear


def _tooltip_fields(layer: gpd.GeoDataFrame, limit: int = 6) -> list[str]:
    """Pick a few simple attribute columns for hover text (skip geometry / nested objects)."""
    fields = []
    for column in layer.columns:
        if column == "geometry":
            continue
        if layer[column].dtype == object and layer[column].map(lambda value: isinstance(value, (dict, list))).any():
            continue
        fields.append(column)
        if len(fields) >= limit:
            break
    return fields


def _add_geojson(fmap: folium.Map, name: str, layer: gpd.GeoDataFrame, *, max_features: int) -> None:
    """Add a vector layer; cap feature count so the HTML map stays usable."""
    if layer.empty:
        return
    frame = layer.to_crs("EPSG:4326")
    if len(frame) > max_features:
        frame = frame.iloc[:max_features]
    fields = _tooltip_fields(frame)
    tooltip = folium.GeoJsonTooltip(fields=fields) if fields else None
    folium.GeoJson(frame.__geo_interface__, name=name, tooltip=tooltip).add_to(fmap)


def impact_map(
    layers: dict[str, gpd.GeoDataFrame],
    *,
    center: tuple[float, float] | None = None,
    choropleth_layer: str | None = None,
    choropleth_column: str | None = None,
    max_features: int = 4000,
) -> folium.Map:
    """Build a layer-controlled Folium map. Large layers are sampled to stay interactive."""
    if not layers:
        raise ValueError("At least one map layer is required")
    frames = [layer.to_crs("EPSG:4326") for layer in layers.values() if not layer.empty]
    if not frames:
        raise ValueError("At least one non-empty map layer is required")
    if center is None:
        bounds = gpd.GeoDataFrame(pd.concat(frames, ignore_index=True), crs="EPSG:4326").total_bounds
        center = ((bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2)
    fmap = folium.Map(location=center, zoom_start=8, tiles="CartoDB positron", control_scale=True)

    # Optional choropleth (admin polygons coloured by a numeric column).
    if choropleth_layer and choropleth_column and choropleth_layer in layers:
        choro = layers[choropleth_layer].to_crs("EPSG:4326")
        values = pd.to_numeric(choro[choropleth_column], errors="coerce").fillna(0)
        maximum = float(values.max()) if len(values) else 0.0
        colormap = linear.YlOrRd_09.scale(0, maximum if maximum > 0 else 1)
        colormap.caption = choropleth_column
        def style_function(feature):
            value = feature["properties"].get(choropleth_column) or 0
            try:
                numeric = float(value)
            except (TypeError, ValueError):
                numeric = 0.0
            return {
                "fillColor": colormap(numeric),
                "color": "#555555",
                "weight": 0.6,
                "fillOpacity": 0.65 if numeric > 0 else 0.05,
            }
        fields = _tooltip_fields(choro)
        folium.GeoJson(
            choro.__geo_interface__,
            name=choropleth_layer,
            style_function=style_function,
            tooltip=folium.GeoJsonTooltip(fields=fields) if fields else None,
        ).add_to(fmap)
        colormap.add_to(fmap)

    for name, layer in layers.items():
        if name == choropleth_layer:
            continue
        _add_geojson(fmap, name, layer, max_features=max_features)
    folium.LayerControl().add_to(fmap)
    return fmap


def plot_temporal_evolution(
    frame: pd.DataFrame, *, date_column: str = "date", value_column: str = "impact_area_km2"
) -> plt.Axes:
    """Plot the disaster footprint through time."""
    if date_column not in frame or value_column not in frame:
        raise KeyError(f"Expected columns: {date_column!r}, {value_column!r}")
    axis = (
        frame.assign(**{date_column: pd.to_datetime(frame[date_column])})
        .sort_values(date_column)
        .plot(x=date_column, y=value_column, marker="o", title="Post-disaster footprint over time", legend=False)
    )
    axis.set_ylabel("Impact area (km2)")
    axis.grid(alpha=0.25)
    return axis


def export_geodataframe(frame: gpd.GeoDataFrame, path: str | Path) -> Path:
    """Export a GeoDataFrame using the format implied by its extension."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    frame.to_file(destination, driver="GeoJSON" if destination.suffix.lower() == ".geojson" else None)
    return destination
