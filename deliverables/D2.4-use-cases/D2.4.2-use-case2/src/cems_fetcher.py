"""Optional Copernicus STAC/WFS client.

The current notebooks do not call this module; they read
input/copernicus/{activation_id}/data.gpkg instead.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

import geopandas as gpd
import requests

from config.config import CACHE_DIR, CEMS_API_TOKEN, CEMS_STAC_URL, CEMS_WFS_URL, HTTP_TIMEOUT_SECONDS


def _request(url: str, *, params: dict[str, Any] | None = None) -> requests.Response:
    headers = {"Authorization": f"Bearer {CEMS_API_TOKEN}"} if CEMS_API_TOKEN else {}
    response = requests.get(url, params=params, headers=headers, timeout=HTTP_TIMEOUT_SECONDS)
    response.raise_for_status()
    return response


def _cache_path(url: str, suffix: str = ".json") -> Path:
    key = hashlib.sha256(url.encode("utf-8")).hexdigest()[:20]
    return CACHE_DIR / f"cems_{key}{suffix}"


def query_stac(collections: Iterable[str], *, bbox: list[float] | None = None,
               datetime: str | None = None, activation_id: str | None = None) -> dict[str, Any]:
    """Search a CEMS-compatible STAC API and cache the JSON response."""
    payload: dict[str, Any] = {"collections": list(collections), "limit": 100}
    if bbox:
        if len(bbox) != 4:
            raise ValueError("bbox must be [west, south, east, north]")
        payload["bbox"] = bbox
    if datetime:
        payload["datetime"] = datetime
    if activation_id:
        payload["ids"] = [activation_id]
    url = CEMS_STAC_URL.rstrip("/") + "/search"
    cache_file = _cache_path(url + json.dumps(payload, sort_keys=True))
    if cache_file.exists():
        return json.loads(cache_file.read_text(encoding="utf-8"))
    response = _request(url, params=payload)
    result = response.json()
    cache_file.write_text(json.dumps(result), encoding="utf-8")
    return result


def activation_assets(search_result: dict[str, Any]) -> list[dict[str, Any]]:
    """Return normalized asset records from a STAC search result."""
    assets = []
    for item in search_result.get("features", []):
        for name, asset in item.get("assets", {}).items():
            href = asset.get("href")
            if href:
                assets.append({"item_id": item.get("id"), "name": name, "href": href,
                               "title": asset.get("title"), "media_type": asset.get("type")})
    return assets


def download_asset(href: str, destination: str | Path, *, overwrite: bool = False) -> Path:
    """Stream a remote CEMS asset to disk, reusing an existing file by default."""
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        return path
    response = _request(href)
    path.write_bytes(response.content)
    return path


def query_wfs(type_name: str, *, bbox: list[float] | None = None, output_format: str = "geojson") -> gpd.GeoDataFrame:
    """Fetch a CEMS vector layer from WFS as a GeoDataFrame."""
    params: dict[str, Any] = {"service": "WFS", "request": "GetFeature", "version": "2.0.0",
                              "typeNames": type_name, "outputFormat": output_format}
    if bbox:
        params["bbox"] = ",".join(map(str, bbox)) + ",EPSG:4326"
    response = _request(CEMS_WFS_URL, params=params)
    return gpd.GeoDataFrame.from_features(response.json(), crs="EPSG:4326")
