"""Download GADM, OSM (Overpass), and GHSL population baselines. Results are cached under data/."""
from __future__ import annotations

import hashlib
import json
import math
import shutil
import time
from pathlib import Path
from typing import Any

import geopandas as gpd
import numpy as np
import pyproj
import rasterio
import requests
from rasterio.errors import RasterioIOError
from rasterio.transform import from_origin
from rasterio.windows import Window, from_bounds
from shapely.geometry import LineString, Point, Polygon

from config.config import CACHE_DIR, DATA_DIR, GHSL_COG_URL_TEMPLATE, HTTP_TIMEOUT_SECONDS, OVERPASS_URL

_USER_AGENT = {"User-Agent": "montandon-impact-estimation/0.1 (IFRC Montandon use case 2)"}

# GHS-POP R2023A on the Source Cooperative mirror: 100 m, ESRI:54009, nodata -200.
GHSL_EPOCHS = tuple(range(1975, 2031, 5))
GHSL_CRS = "ESRI:54009"
GHSL_NODATA = -200.0
GHSL_CELL_M = 100.0
_GHSL_X0 = -18_041_000.0
_GHSL_Y0 = 9_000_000.0
_GHSL_SPAN_M = 1_000_000.0
_GHSL_MAX_PIXELS = 80_000_000
_GDAL_COG_ENV = {
    "GDAL_DISABLE_READDIR_ON_OPEN": "EMPTY_DIR",
    "CPL_VSIL_CURL_ALLOWED_EXTENSIONS": ".tif",
    "GDAL_HTTP_MERGE_CONSECUTIVE_RANGES": "YES",
    "GDAL_HTTP_MULTIPLEX": "YES",
    "GDAL_HTTP_VERSION": "2",
    "CPL_VSIL_CURL_USE_HEAD": "NO",
    "VSI_CACHE": "TRUE",
    "GDAL_HTTP_USERAGENT": _USER_AGENT["User-Agent"],
    "GDAL_HTTP_TIMEOUT": str(HTTP_TIMEOUT_SECONDS),
}


def _get(url: str, *, params: dict[str, Any] | None = None, timeout: int | tuple[int, int] | None = None) -> requests.Response:
    response = requests.get(
        url, params=params, timeout=timeout or HTTP_TIMEOUT_SECONDS, headers=_USER_AGENT
    )
    response.raise_for_status()
    return response


def _path(prefix: str, value: str, suffix: str) -> Path:
    """Stable cache filename from a hash of the request key."""
    key = hashlib.sha256(value.encode("utf-8")).hexdigest()[:20]
    return CACHE_DIR / f"{prefix}_{key}{suffix}"


def fetch_ghsl_population(
    *,
    bbox: list[float],
    year: int = 2020,
    output_path: str | Path | None = None,
) -> Path:
    """Read a GHS-POP R2023A 100 m window and cache the mosaic.

    ``bbox`` is ``[west, south, east, north]`` in WGS84 degrees. The mirror is a
    set of Cloud Optimized GeoTIFFs on the ESRI:54009 Mollweide grid, so only
    the tiles covering that box are opened and only the overlapping pixels are
    transferred. ``year`` must be a five-year epoch from 1975 through 2030.
    Epochs 2025 and 2030 are model projections.
    """
    if year not in GHSL_EPOCHS:
        allowed = ", ".join(str(item) for item in GHSL_EPOCHS)
        raise ValueError(f"ghsl_epoch must be one of: {allowed}")
    if bbox is None or len(bbox) != 4:
        raise ValueError("bbox must be [west, south, east, north] in WGS84 degrees")
    west, south, east, north = (float(value) for value in bbox)
    if west >= east or south >= north:
        raise ValueError("bbox must have west < east and south < north")

    destination = Path(output_path) if output_path else DATA_DIR / "baseline" / f"ghsl_pop_{year}.tif"
    destination.parent.mkdir(parents=True, exist_ok=True)
    cache_key = hashlib.sha256(
        f"{year}|{west:.8f}|{south:.8f}|{east:.8f}|{north:.8f}".encode("utf-8")
    ).hexdigest()[:20]
    cache_path = CACHE_DIR / f"ghsl_pop_{year}_{cache_key}.tif"
    if _raster_cache_ok(cache_path):
        if destination.resolve() != cache_path.resolve():
            shutil.copyfile(cache_path, destination)
        return destination

    minx, miny, maxx, maxy = _snap_mollweide_bounds(*_bbox_to_mollweide(west, south, east, north))
    urls = [_ghsl_tile_url(year, row, col) for row, col in _tile_ids_for_bounds(minx, miny, maxx, maxy)]
    _mosaic_ghsl_window(urls, (minx, miny, maxx, maxy), cache_path)
    if destination.resolve() != cache_path.resolve():
        shutil.copyfile(cache_path, destination)
    return destination


def _raster_cache_ok(path: Path) -> bool:
    if not path.exists() or path.stat().st_size < 500:
        return False
    try:
        with rasterio.open(path) as src:
            return src.width > 0 and src.height > 0 and src.crs is not None
    except RasterioIOError:
        return False


def _bbox_to_mollweide(west: float, south: float, east: float, north: float) -> tuple[float, float, float, float]:
    """Envelope of a WGS84 box on ESRI:54009. Edges are sampled because meridians curve."""
    transformer = pyproj.Transformer.from_crs("EPSG:4326", GHSL_CRS, always_xy=True)
    samples = 17
    lons: list[float] = []
    lats: list[float] = []
    for index in range(samples):
        step = index / (samples - 1)
        lon = west + (east - west) * step
        lat = south + (north - south) * step
        lons.extend((lon, lon, west, east))
        lats.extend((south, north, lat, lat))
    xs, ys = transformer.transform(lons, lats)
    pairs = [(float(x), float(y)) for x, y in zip(xs, ys) if math.isfinite(x) and math.isfinite(y)]
    if not pairs:
        raise ValueError("bbox does not fall on the Mollweide grid")
    return (
        min(x for x, _ in pairs),
        min(y for _, y in pairs),
        max(x for x, _ in pairs),
        max(y for _, y in pairs),
    )


def _snap_mollweide_bounds(minx: float, miny: float, maxx: float, maxy: float) -> tuple[float, float, float, float]:
    """Expand bounds onto the 100 m GHSL pixel edges."""
    minx = _GHSL_X0 + math.floor((minx - _GHSL_X0) / GHSL_CELL_M) * GHSL_CELL_M
    maxx = _GHSL_X0 + math.ceil((maxx - _GHSL_X0) / GHSL_CELL_M) * GHSL_CELL_M
    maxy = _GHSL_Y0 - math.floor((_GHSL_Y0 - maxy) / GHSL_CELL_M) * GHSL_CELL_M
    miny = _GHSL_Y0 - math.ceil((_GHSL_Y0 - miny) / GHSL_CELL_M) * GHSL_CELL_M
    if maxx <= minx:
        maxx = minx + GHSL_CELL_M
    if maxy <= miny:
        maxy = miny + GHSL_CELL_M
    return minx, miny, maxx, maxy


def _tile_rc(x: float, y: float) -> tuple[int, int]:
    row = int((_GHSL_Y0 - y) // _GHSL_SPAN_M) + 1
    col = int((x - _GHSL_X0) // _GHSL_SPAN_M) + 1
    return row, col


def _tile_ids_for_bounds(minx: float, miny: float, maxx: float, maxy: float) -> list[tuple[int, int]]:
    """Tile indexes covering the snapped window. Exclusive edges stay with the tile they start."""
    inset = GHSL_CELL_M / 2
    row_north, col_west = _tile_rc(minx, maxy - inset)
    row_south, col_east = _tile_rc(maxx - inset, miny + inset)
    rows = range(min(row_north, row_south), max(row_north, row_south) + 1)
    cols = range(min(col_west, col_east), max(col_west, col_east) + 1)
    return [(row, col) for row in rows for col in cols]


def _ghsl_tile_url(year: int, row: int, col: int) -> str:
    return GHSL_COG_URL_TEMPLATE.format(year=year, row=row, col=col)


def _missing_remote_tile(exc: Exception) -> bool:
    text = str(exc).lower()
    return "404" in text or "not found" in text or "no such file" in text


def _mosaic_ghsl_window(urls: list[str], bounds: tuple[float, float, float, float], destination: Path) -> None:
    """Read each remote COG window and write one local GeoTIFF in ESRI:54009."""
    minx, miny, maxx, maxy = bounds
    width = int(round((maxx - minx) / GHSL_CELL_M))
    height = int(round((maxy - miny) / GHSL_CELL_M))
    if width <= 0 or height <= 0:
        raise ValueError("GHSL window is empty")
    if width * height > _GHSL_MAX_PIXELS:
        raise ValueError(
            f"GHSL window is {width}x{height} pixels; narrow the event bbox before reading 100 m cells"
        )
    mosaic = np.full((height, width), GHSL_NODATA, dtype="float32")
    found = 0
    with rasterio.Env(**_GDAL_COG_ENV):
        for url in urls:
            try:
                with rasterio.open(url) as src:
                    window = from_bounds(minx, miny, maxx, maxy, transform=src.transform)
                    window = window.round_offsets().round_lengths().intersection(Window(0, 0, src.width, src.height))
                    if window.width <= 0 or window.height <= 0:
                        continue
                    data = src.read(1, window=window)
                    win_transform = src.window_transform(window)
                    col0 = int(round((win_transform.c - minx) / GHSL_CELL_M))
                    row0 = int(round((maxy - win_transform.f) / GHSL_CELL_M))
                    row_count, col_count = data.shape
                    row_start = max(row0, 0)
                    col_start = max(col0, 0)
                    row_end = min(row0 + row_count, height)
                    col_end = min(col0 + col_count, width)
                    if row_end <= row_start or col_end <= col_start:
                        continue
                    mosaic[row_start:row_end, col_start:col_end] = data[
                        row_start - row0 : row_start - row0 + (row_end - row_start),
                        col_start - col0 : col_start - col0 + (col_end - col_start),
                    ]
                    found += 1
            except RasterioIOError as exc:
                if _missing_remote_tile(exc):
                    continue
                raise
    if found == 0:
        raise RuntimeError("GHSL window read failed: no published tile covers this bbox")

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".part")
    profile = {
        "driver": "GTiff",
        "height": height,
        "width": width,
        "count": 1,
        "dtype": "float32",
        "crs": GHSL_CRS,
        "transform": from_origin(minx, maxy, GHSL_CELL_M, GHSL_CELL_M),
        "nodata": GHSL_NODATA,
        "compress": "deflate",
    }
    with rasterio.open(temporary, "w", **profile) as dst:
        dst.write(mosaic, 1)
    temporary.replace(destination)


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
