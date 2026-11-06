"""Read one CEMS activation from the Montandon STAC catalog.

The catalog is https://montandon-eoapi.ifrc.org/stac. Item and search calls
need ``MONTANDON_STAC_TOKEN``. Vector GeoJSON assets from ``cems-response``
are cached under ``data/cache/cems/{code}/`` together with ``manifest.json``.
Notebooks 02 and 03 read that cache and do not call Copernicus.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import geopandas as gpd
import pandas as pd
import requests

from config.config import CACHE_DIR, HTTP_TIMEOUT_SECONDS, MONTANDON_STAC_TOKEN, MONTANDON_STAC_URL

_USER_AGENT = {"User-Agent": "montandon-impact-estimation/0.1 (IFRC Montandon use case 2)"}
_VECTOR_TIMEOUT = (30, 180)
_MANIFEST_NAME = "manifest.json"
_RELATED_COLLECTIONS = ("cems-hazards", "cems-response", "cems-impacts")
_IMPACT_COLUMNS = [
    "item_id",
    "datetime",
    "category",
    "type",
    "value",
    "unit",
    "estimate_type",
]
_AOI_RE = re.compile(r"AOI(\d+)", re.IGNORECASE)
_MONIT_RE = re.compile(r"MONIT(\d+)", re.IGNORECASE)
_THEME_RE = re.compile(r"(?:PRODUCT|MONIT\d+)_(.+)_v\d+$", re.IGNORECASE)


def fetch_event(code: str) -> dict[str, Any]:
    """Return the ``cems-events`` item ``cems-event-{code}``."""
    code = _require_code(code)
    url = f"{MONTANDON_STAC_URL}/collections/cems-events/items/cems-event-{code}"
    response = requests.get(url, headers=_stac_headers(), timeout=HTTP_TIMEOUT_SECONDS)
    if response.status_code == 404:
        raise LookupError(f"No Montandon CEMS event found for {code}")
    _raise_for_status(response)
    return response.json()


def fetch_stac_activation(code: str) -> dict[str, Any]:
    """Event item plus hazards, responses, and impacts that share its ``monty:corr_id``."""
    event = fetch_event(code)
    properties = event.get("properties") or {}
    corr_id = properties.get("monty:corr_id")
    if not corr_id:
        raise LookupError(f"{event.get('id')} has no monty:corr_id")
    return {
        "code": _require_code(code),
        "corr_id": corr_id,
        "event": event,
        "hazards": search_by_corr_id("cems-hazards", corr_id),
        "responses": search_by_corr_id("cems-response", corr_id),
        "impacts": search_by_corr_id("cems-impacts", corr_id),
    }


def search_by_corr_id(collection: str, corr_id: str) -> list[dict[str, Any]]:
    """Page a STAC search filtered on the documented ``monty:corr_id`` queryable."""
    if collection not in _RELATED_COLLECTIONS:
        raise ValueError(f"Unsupported collection {collection}")
    body = {
        "collections": [collection],
        "filter": {"op": "=", "args": [{"property": "monty:corr_id"}, corr_id]},
        "filter-lang": "cql2-json",
        "limit": 100,
    }
    return _search(body)


def event_summary(event: dict[str, Any]) -> dict[str, Any]:
    """Fields used to identify the Montandon event before looking at related items."""
    properties = event.get("properties") or {}
    return {
        "id": event.get("id"),
        "title": properties.get("title"),
        "datetime": properties.get("datetime"),
        "country_codes": ", ".join(properties.get("monty:country_codes") or []),
        "hazard_codes": ", ".join(properties.get("monty:hazard_codes") or []),
        "corr_id": properties.get("monty:corr_id"),
    }


def hazard_table(items: list[dict[str, Any]]) -> pd.DataFrame:
    """One row per ``cems-hazards`` item."""
    rows = []
    for item in items:
        properties = item.get("properties") or {}
        geometry = item.get("geometry") or {}
        rows.append(
            {
                "id": item.get("id"),
                "title": properties.get("title"),
                "datetime": properties.get("datetime"),
                "hazard_codes": ", ".join(properties.get("monty:hazard_codes") or []),
                "geometry_type": geometry.get("type"),
            }
        )
    return pd.DataFrame(rows)


def response_table(items: list[dict[str, Any]]) -> pd.DataFrame:
    """One row per ``cems-response`` item."""
    rows = []
    for item in items:
        properties = item.get("properties") or {}
        detail = properties.get("monty:response_detail") or {}
        rows.append(
            {
                "id": item.get("id"),
                "title": properties.get("title"),
                "datetime": properties.get("datetime"),
                "response_type": detail.get("type"),
                "status": detail.get("status"),
                "monitoring_number": detail.get("monitoring_number"),
                "source_id": detail.get("source_id"),
            }
        )
    return pd.DataFrame(rows)


def asset_index(responses: list[dict[str, Any]]) -> pd.DataFrame:
    """Every response asset. Only ``application/geo+json`` rows are downloaded."""
    rows = []
    for item in responses:
        for name, asset in (item.get("assets") or {}).items():
            rows.append(
                {
                    "item_id": item.get("id"),
                    "asset": name,
                    "media_type": asset.get("type"),
                    "roles": ", ".join(asset.get("roles") or []),
                    "href": asset.get("href"),
                    "download": _is_vector_asset(asset),
                }
            )
    return pd.DataFrame(rows)


def impact_stats_table(impacts: list[dict[str, Any]]) -> pd.DataFrame:
    """``monty:impact_detail`` from each ``cems-impacts`` item.

    These are the figures Montandon already publishes. They are not the
    admin-level overlay computed in notebook 02.
    """
    rows = []
    for item in impacts:
        properties = item.get("properties") or {}
        detail = properties.get("monty:impact_detail") or {}
        rows.append(
            {
                "item_id": item.get("id"),
                "datetime": properties.get("datetime"),
                "category": detail.get("category"),
                "type": detail.get("type"),
                "value": detail.get("value"),
                "unit": detail.get("unit"),
                "estimate_type": detail.get("estimate_type"),
            }
        )
    return pd.DataFrame(rows, columns=_IMPACT_COLUMNS)


def vector_cache_dir(code: str) -> Path:
    """``data/cache/cems/{code}/`` (honours ``MONTANDON_DATA_DIR``)."""
    path = CACHE_DIR / "cems" / str(code).strip()
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_response_vectors(
    responses: list[dict[str, Any]],
    code: str,
) -> tuple[dict[str, gpd.GeoDataFrame], list[str]]:
    """Download response GeoJSON assets into the cache and load each file.

    A layer that fails is reported and skipped. Files already in the cache are
    reused. ``manifest.json`` records the STAC datetime used by notebook 03.
    """
    code = _require_code(code)
    cache_dir = vector_cache_dir(code)
    loaded: dict[str, gpd.GeoDataFrame] = {}
    errors: list[str] = []
    manifest_layers: list[dict[str, Any]] = []
    for record in _vector_assets(responses):
        path = _cache_path(cache_dir, record["href"], record["asset"])
        label = f"{record['item_id']}:{record['asset']}"
        try:
            if not path.exists() or path.stat().st_size == 0:
                _download_file(record["href"], path)
            frame = gpd.read_file(path)
            if frame.crs is None:
                frame = frame.set_crs("EPSG:4326")
            frame["cems_layer"] = path.stem
            frame["stac_item"] = record["item_id"]
            frame["monitoring_number"] = record["monitoring_number"]
            frame["delivery_time"] = record["datetime"]
            loaded[path.stem] = frame
            manifest_layers.append(
                {
                    "file": path.name,
                    "item_id": record["item_id"],
                    "asset": record["asset"],
                    "href": record["href"],
                    "datetime": record["datetime"],
                    "monitoring_number": record["monitoring_number"],
                }
            )
        except Exception as exc:
            errors.append(f"{label}: {exc}")
    _write_manifest(cache_dir, code, manifest_layers)
    return loaded, errors


def load_cached_vectors(code: str) -> dict[str, gpd.GeoDataFrame]:
    """Load the latest cached GeoJSON for each area of interest and theme.

    Notebook 01 stores every response vector, including monitoring repeats and
    ``notAnalysed`` extents. Notebook 02 should see one current layer per area
    and theme, so this keeps the highest monitoring number and drops layers
    whose name is ``notAnalysed``.
    """
    files = _cached_geojsons(code)
    if not files:
        folder = CACHE_DIR / "cems" / str(code).strip()
        raise FileNotFoundError(
            f"No cached CEMS vectors in {folder}. Run notebooks/01_cems_api_ingestion.ipynb first."
        )
    grouped: dict[tuple[str, str], list[tuple[int, Path]]] = {}
    for path in files:
        aoi, monitoring, family = _layer_identity(path)
        if family.lower() == "notanalysed":
            continue
        grouped.setdefault((aoi, family), []).append((monitoring, path))
    selected: list[Path] = []
    for versions in grouped.values():
        newest = max(monitoring for monitoring, _path in versions)
        selected.extend(path for monitoring, path in versions if monitoring == newest)
    if not selected:
        raise FileNotFoundError(f"Cached CEMS vectors for {code} contain no analysed layers.")
    loaded: dict[str, gpd.GeoDataFrame] = {}
    for path in sorted(selected):
        frame = gpd.read_file(path)
        if frame.crs is None:
            frame = frame.set_crs("EPSG:4326")
        loaded[path.stem] = frame
    return loaded


def cached_timeline(code: str) -> list[dict[str, Any]]:
    """Analysed cache files in monitoring order.

    Delivery times come from ``manifest.json`` written by notebook 01. This
    function does not call the catalog again. ``notAnalysed`` layers are omitted,
    and every monitoring step is kept.
    """
    files = _cached_geojsons(code)
    if not files:
        folder = CACHE_DIR / "cems" / str(code).strip()
        raise FileNotFoundError(
            f"No cached CEMS vectors in {folder}. Run notebooks/01_cems_api_ingestion.ipynb first."
        )
    delivered = _manifest_times(code)
    rows = []
    for path in files:
        aoi, monitoring, family = _layer_identity(path)
        if family.lower() == "notanalysed":
            continue
        rows.append(
            {
                "path": path,
                "layer": path.stem,
                "aoi": aoi,
                "monitoring_number": monitoring,
                "family": family,
                "delivery_time": delivered.get(path.name),
            }
        )
    rows.sort(key=lambda row: (row["delivery_time"] or "", row["monitoring_number"], row["layer"]))
    if not rows:
        raise FileNotFoundError(f"Cached CEMS vectors for {code} contain no analysed layers.")
    return rows


def _require_code(code: str) -> str:
    if not code or not str(code).strip():
        raise ValueError("activation code is required")
    return str(code).strip()


def _stac_headers() -> dict[str, str]:
    if not MONTANDON_STAC_TOKEN:
        raise RuntimeError(
            "MONTANDON_STAC_TOKEN is not set. The Montandon STAC catalog requires a bearer token "
            "from the IFRC identity provider (https://goadmin.ifrc.org)."
        )
    return {**_USER_AGENT, "Authorization": f"Bearer {MONTANDON_STAC_TOKEN}"}


def _raise_for_status(response: requests.Response) -> None:
    if response.status_code == 401:
        raise RuntimeError("Montandon STAC rejected the bearer token (401).")
    response.raise_for_status()


def _search(body: dict[str, Any]) -> list[dict[str, Any]]:
    headers = _stac_headers()
    url: str | None = f"{MONTANDON_STAC_URL}/search"
    payload: dict[str, Any] | None = body
    features: list[dict[str, Any]] = []
    seen: set[str] = set()
    for _page in range(50):
        if url is None or url in seen:
            break
        seen.add(url)
        if payload is None:
            response = requests.get(url, headers=headers, timeout=HTTP_TIMEOUT_SECONDS)
        else:
            response = requests.post(url, json=payload, headers=headers, timeout=HTTP_TIMEOUT_SECONDS)
        _raise_for_status(response)
        page = response.json()
        features.extend(page.get("features") or [])
        payload = None
        url = next(
            (
                link.get("href")
                for link in page.get("links") or []
                if link.get("rel") == "next" and link.get("href")
            ),
            None,
        )
    return features


def _is_vector_asset(asset: dict[str, Any]) -> bool:
    href = asset.get("href") or ""
    media = (asset.get("type") or "").lower()
    return href.startswith("http") and "geo+json" in media


def _vector_assets(responses: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records = []
    for item in responses:
        properties = item.get("properties") or {}
        detail = properties.get("monty:response_detail") or {}
        for name, asset in (item.get("assets") or {}).items():
            if not _is_vector_asset(asset):
                continue
            records.append(
                {
                    "item_id": item.get("id"),
                    "asset": name,
                    "href": asset["href"],
                    "datetime": properties.get("datetime"),
                    "monitoring_number": detail.get("monitoring_number"),
                }
            )
    return records


def _write_manifest(cache_dir: Path, code: str, layers: list[dict[str, Any]]) -> None:
    document = {"code": code, "layers": layers}
    (cache_dir / _MANIFEST_NAME).write_text(json.dumps(document, indent=2), encoding="utf-8")


def _manifest_times(code: str) -> dict[str, str]:
    path = CACHE_DIR / "cems" / str(code).strip() / _MANIFEST_NAME
    if not path.exists():
        return {}
    document = json.loads(path.read_text(encoding="utf-8"))
    times = {}
    for layer in document.get("layers") or []:
        filename = layer.get("file")
        when = layer.get("datetime")
        if filename and when:
            times[str(filename)] = str(when)
    return times


def _cached_geojsons(code: str) -> list[Path]:
    folder = CACHE_DIR / "cems" / str(code).strip()
    files = []
    for pattern in ("*.json", "*.geojson"):
        for path in sorted(folder.glob(pattern)):
            if path.is_file() and path.name != _MANIFEST_NAME and not path.name.endswith(".part"):
                files.append(path)
    return files


def _layer_identity(path: Path) -> tuple[str, int, str]:
    """Return ``(aoi, monitoring_number, theme)`` parsed from a cache filename."""
    stem = path.stem
    aoi_match = _AOI_RE.search(stem)
    monitoring_match = _MONIT_RE.search(stem)
    theme_match = _THEME_RE.search(stem)
    token = theme_match.group(1) if theme_match else stem
    family = token[:-1] if len(token) > 1 and token[-1] in {"A", "P", "L"} else token
    aoi = aoi_match.group(1) if aoi_match else stem
    monitoring = int(monitoring_match.group(1)) if monitoring_match else 0
    return aoi, monitoring, family


def _cache_path(cache_dir: Path, url: str, layer_name: str) -> Path:
    leaf = url.rstrip("/").split("/")[-1].split("?")[0]
    if not leaf or leaf in {".", ".."}:
        leaf = layer_name.replace("\\", "/").rstrip("/").split("/")[-1] + ".geojson"
    safe = "".join(char if char.isalnum() or char in "-_." else "_" for char in leaf)
    return cache_dir / safe


def _download_file(url: str, destination: Path) -> None:
    """Stream a GeoJSON to a ``.part`` file, then rename it into place.

    Asset hosts are public object storage. The STAC bearer token is not sent.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".part")
    with requests.get(url, stream=True, timeout=_VECTOR_TIMEOUT, headers=_USER_AGENT) as response:
        response.raise_for_status()
        with temporary.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 256):
                if chunk:
                    handle.write(chunk)
    temporary.replace(destination)
