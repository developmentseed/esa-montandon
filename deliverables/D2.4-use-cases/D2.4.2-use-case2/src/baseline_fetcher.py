"""Download GADM, OSM (Overpass), and WorldPop baselines. Results are cached under data/."""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any

import geopandas as gpd
import rasterio
import requests
from rasterio.windows import from_bounds
from shapely.geometry import LineString, Point, Polygon

from config.config import CACHE_DIR, DATA_DIR, HTTP_TIMEOUT_SECONDS, OVERPASS_URL, WORLDPOP_GIS_URL_TEMPLATE

_USER_AGENT = {"User-Agent": "montandon-impact-estimation/0.1 (IFRC Montandon use case 2)"}


def _get(url: str, *, params: dict[str, Any] | None = None, timeout: int | tuple[int, int] | None = None) -> requests.Response:
    response = requests.get(
        url, params=params, timeout=timeout or HTTP_TIMEOUT_SECONDS, headers=_USER_AGENT
    )
    response.raise_for_status()
    return response


def _download_file(url: str, destination: Path, *, timeout: tuple[int, int] = (30, 600)) -> None:
    """Stream a large file to disk via a .part temp path, then rename."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = destination.with_suffix(destination.suffix + ".part")
    with requests.get(url, stream=True, timeout=timeout, headers=_USER_AGENT) as response:
        response.raise_for_status()
        with tmp_path.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 256):
                if chunk:
                    handle.write(chunk)
    tmp_path.replace(destination)


def _path(prefix: str, value: str, suffix: str) -> Path:
    """Stable cache filename from a hash of the request key."""
    key = hashlib.sha256(value.encode("utf-8")).hexdigest()[:20]
    return CACHE_DIR / f"{prefix}_{key}{suffix}"


def fetch_worldpop_population(
    *,
    country_code: str,
    year: int = 2020,
    bbox: list[float] | None = None,
    output_path: str | Path | None = None,
) -> Path:
    """Download WorldPop 1 km unconstrained population and optionally clip to bbox."""
    if not country_code:
        raise ValueError("country_code is required for WorldPop downloads")
    iso = country_code.upper()
    url = WORLDPOP_GIS_URL_TEMPLATE.format(year=year, iso=iso, iso_lower=iso.lower())
    destination = Path(output_path) if output_path else DATA_DIR / "baseline" / f"{iso.lower()}_ppp_{year}_1km.tif"
    destination.parent.mkdir(parents=True, exist_ok=True)
    source_path = CACHE_DIR / f"worldpop_{iso.lower()}_{year}_1km.tif"
    if not source_path.exists() or source_path.stat().st_size < 10_000:
        _download_file(url, source_path)
    if bbox is None:
        if destination.resolve() != source_path.resolve():
            destination.write_bytes(source_path.read_bytes())
        return destination
    _clip_raster(source_path, destination, bbox)
    return destination


def _clip_raster(source: Path, destination: Path, bbox: list[float]) -> None:
    """Write a WGS84 window of the country raster (bbox = west, south, east, north)."""
    west, south, east, north = bbox
    with rasterio.open(source) as src:
        window = from_bounds(west, south, east, north, transform=src.transform)
        window = window.round_offsets().round_lengths().intersection(
            rasterio.windows.Window(0, 0, src.width, src.height)
        )
        data = src.read(window=window)
        transform = src.window_transform(window)
        profile = src.profile.copy()
        profile.update(height=data.shape[1], width=data.shape[2], transform=transform)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with rasterio.open(destination, "w", **profile) as dst:
            dst.write(data)


def _geometry_from_osm(element: dict[str, Any]):
    """Node → Point; closed way → Polygon; otherwise LineString."""
    if element.get("type") == "node":
        return Point(element["lon"], element["lat"])
    coords = [(p["lon"], p["lat"]) for p in element.get("geometry") or []]
    if len(coords) < 2:
        return None
    if element.get("type") in {"way", "relation"} and len(coords) >= 4 and coords[0] == coords[-1]:
        return Polygon(coords)
    return LineString(coords)


def _infra_type(tags: dict[str, Any]) -> str:
    if tags.get("amenity") in {"hospital", "school"}:
        return tags["amenity"]
    if tags.get("aeroway") == "aerodrome":
        return "airport"
    highway = tags.get("highway")
    if highway in {"primary", "secondary"}:
        return f"{highway}_road"
    return tags.get("amenity") or tags.get("highway") or tags.get("aeroway") or "unknown"


def _empty_infrastructure() -> gpd.GeoDataFrame:
    return gpd.GeoDataFrame(
        columns=["osm_id", "osm_type", "infra_type", "name", "tags", "geometry"],
        geometry="geometry",
        crs="EPSG:4326",
    )


def _rows_from_overpass(elements: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for element in elements:
        geom = _geometry_from_osm(element)
        if geom is None or geom.is_empty:
            continue
        osm_tags = element.get("tags") or {}
        rows.append(
            {
                "osm_id": element.get("id"),
                "osm_type": element.get("type"),
                "infra_type": _infra_type(osm_tags),
                "name": osm_tags.get("name"),
                "tags": json.dumps(osm_tags, ensure_ascii=False),
                "geometry": geom,
            }
        )
    return rows


def _overpass_query(query: str) -> requests.Response:
    """POST to Overpass; retry and fall back to a public mirror on 429/errors."""
    endpoints = [OVERPASS_URL, "https://overpass.kumi.systems/api/interpreter"]
    last_error: Exception | None = None
    for endpoint in dict.fromkeys(endpoints):
        for _attempt in range(2):
            try:
                response = requests.post(
                    endpoint, data={"data": query}, headers=_USER_AGENT, timeout=(15, 120)
                )
                if response.status_code == 429:
                    time.sleep(8)
                    continue
                response.raise_for_status()
                return response
            except requests.RequestException as exc:
                last_error = exc
                time.sleep(3)
    if last_error:
        raise last_error
    raise requests.RequestException("Overpass request failed")


def fetch_osm_infrastructure(
    *, bbox: list[float], infrastructure_filters: list[str] | None = None
) -> gpd.GeoDataFrame:
    """Query Overpass for health, education, transport, and airport features.

    Each filter is requested separately so a roads timeout still returns hospitals.
    """
    if len(bbox) != 4:
        raise ValueError("bbox must be [west, south, east, north]")
    filters = infrastructure_filters or ["hospital", "school", "primary_road", "secondary_road", "airport"]
    tags = {
        "hospital": "nwr[amenity=hospital];",
        "school": "nwr[amenity=school];",
        "primary_road": "way[highway=primary];",
        "secondary_road": "way[highway=secondary];",
        "airport": "nwr[aeroway=aerodrome];",
    }
    south, west, north, east = bbox[1], bbox[0], bbox[3], bbox[2]  # Overpass uses south,west,north,east
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    for item in filters:
        clause = tags.get(item)
        if not clause:
            continue
        query = f"[out:json][timeout:90];({clause[:-1]}({south},{west},{north},{east}););out geom;"
        try:
            response = _overpass_query(query)
            rows.extend(_rows_from_overpass(response.json().get("elements", [])))
        except requests.RequestException as exc:
            errors.append(f"{item}: {exc}")
    if not rows:
        empty = _empty_infrastructure()
        empty.attrs["overpass_errors"] = errors
        return empty
    result = gpd.GeoDataFrame(rows, geometry="geometry", crs="EPSG:4326")
    result.attrs["overpass_errors"] = errors
    return result.drop_duplicates(subset=["osm_id", "osm_type"], keep="first")


def fetch_admin_boundaries(*, country_code: str, admin_level: int = 2, source: str = "gadm") -> gpd.GeoDataFrame:
    """Read administrative boundaries from GADM (default) or a future HDX source."""
    if not country_code or admin_level not in {1, 2, 3}:
        raise ValueError("country_code and admin_level 1, 2, or 3 are required")
    if source == "hdx":
        raise NotImplementedError("HDX COD URLs are country-specific; use admin_source: gadm")
    if source != "gadm":
        raise ValueError("source must be 'gadm' or 'hdx'")
    iso = country_code.upper()
    url = f"https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_{iso}_{admin_level}.json"
    path = _path("admin", f"{iso}_{admin_level}", ".geojson")
    if not path.exists():
        response = _get(url, timeout=max(HTTP_TIMEOUT_SECONDS, 120))
        path.write_bytes(response.content)
    return gpd.read_file(path)
