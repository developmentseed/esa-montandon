"""Read one Copernicus EMS Rapid Mapping activation from the public dashboard API.

The detail endpoint returns the activation, its areas of interest, and every
product. Published vector layers (format ``vt``) are GeoJSON files. This module
caches those files under ``data/cache/cems/{code}/`` and does not touch
``input/copernicus/``.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import geopandas as gpd
import pandas as pd
import requests

from config.config import CACHE_DIR, CEMS_RAPIDMAPPING_URL, HTTP_TIMEOUT_SECONDS

_USER_AGENT = {"User-Agent": "montandon-impact-estimation/0.1 (IFRC Montandon use case 2)"}
_VECTOR_TIMEOUT = (30, 180)
_STAT_COLUMNS = [
    "scope",
    "aoi_number",
    "aoi_name",
    "product_type",
    "monitoring_number",
    "thematic",
    "subclass",
    "unit",
    "total",
    "affected",
]


def fetch_activation(code: str) -> dict[str, Any]:
    """Return the activation detail payload for an EMSR code.

    The endpoint is public and unauthenticated. It answers
    ``{count, next, previous, results: [activation]}``.
    """
    if not code or not str(code).strip():
        raise ValueError("activation code is required")
    code = str(code).strip()
    response = requests.get(
        CEMS_RAPIDMAPPING_URL,
        params={"code": code},
        timeout=HTTP_TIMEOUT_SECONDS,
        headers=_USER_AGENT,
    )
    response.raise_for_status()
    payload = response.json()
    results = payload.get("results") or []
    matches = [item for item in results if item.get("code") == code]
    if not matches:
        raise LookupError(f"No Rapid Mapping activation found for {code}")
    return matches[0]


def activation_summary(activation: dict[str, Any]) -> dict[str, Any]:
    """Fields used to identify the event before looking at products."""
    countries = []
    for country in activation.get("countries") or []:
        if isinstance(country, dict):
            name = country.get("name")
            if name:
                countries.append(str(name))
        elif country:
            countries.append(str(country))
    aois = activation.get("aois") or []
    n_products = sum(len(aoi.get("products") or []) for aoi in aois)
    return {
        "code": activation.get("code"),
        "name": activation.get("name"),
        "category": activation.get("category"),
        "sub_category": activation.get("subCategory"),
        "countries": ", ".join(countries),
        "event_time": activation.get("eventTime"),
        "closed": activation.get("closed"),
        "gdacs_id": activation.get("gdacsId"),
        "charter_number": activation.get("charterNumber"),
        "n_aois": len(aois),
        "n_products": n_products,
    }


def product_catalog(activation: dict[str, Any]) -> pd.DataFrame:
    """One row per AOI product: status, monitoring step, vector count, ZIP link."""
    rows = []
    for aoi in activation.get("aois") or []:
        products = aoi.get("products") or []
        if not products:
            rows.append(
                {
                    "aoi_number": aoi.get("number"),
                    "aoi_name": aoi.get("name"),
                    "type": None,
                    "monitoring_number": None,
                    "status_code": None,
                    "delivery_time": None,
                    "n_vector_layers": 0,
                    "n_cog_layers": 0,
                    "download_path": None,
                }
            )
        for product in products:
            version = product.get("version") or {}
            layers = product.get("layers") or []
            rows.append(
                {
                    "aoi_number": product.get("aoiNumber", aoi.get("number")),
                    "aoi_name": product.get("aoiName", aoi.get("name")),
                    "type": product.get("type"),
                    "monitoring_number": product.get("monitoringNumber"),
                    "status_code": version.get("statusCode"),
                    "delivery_time": version.get("deliveryTime"),
                    "n_vector_layers": sum(1 for layer in layers if layer.get("format") == "vt"),
                    "n_cog_layers": sum(1 for layer in layers if layer.get("format") == "cog"),
                    "download_path": product.get("downloadPath"),
                }
            )
    return pd.DataFrame(rows)


def layer_index(activation: dict[str, Any]) -> pd.DataFrame:
    """Every product layer. Vector rows carry a GeoJSON url; COG rows usually do not."""
    rows = []
    for aoi in activation.get("aois") or []:
        for product in aoi.get("products") or []:
            version = product.get("version") or {}
            for layer in product.get("layers") or []:
                rows.append(
                    {
                        "aoi_number": product.get("aoiNumber", aoi.get("number")),
                        "aoi_name": product.get("aoiName", aoi.get("name")),
                        "product_type": product.get("type"),
                        "monitoring_number": product.get("monitoringNumber"),
                        "status_code": version.get("statusCode"),
                        "format": layer.get("format"),
                        "layer": layer.get("name"),
                        "url": layer.get("json"),
                    }
                )
    return pd.DataFrame(rows)


def published_vector_layers(activation: dict[str, Any]) -> list[dict[str, Any]]:
    """GeoJSON links for products whose ``statusCode`` is ``F`` (published)."""
    records = []
    for aoi in activation.get("aois") or []:
        for product in aoi.get("products") or []:
            version = product.get("version") or {}
            if version.get("statusCode") != "F":
                continue
            for layer in product.get("layers") or []:
                if layer.get("format") != "vt" or not layer.get("json"):
                    continue
                records.append(
                    {
                        "layer": layer.get("name"),
                        "url": layer["json"],
                        "aoi_number": product.get("aoiNumber", aoi.get("number")),
                        "aoi_name": product.get("aoiName", aoi.get("name")),
                        "product_type": product.get("type"),
                        "monitoring_number": product.get("monitoringNumber"),
                        "delivery_time": version.get("deliveryTime"),
                    }
                )
    return records


def vector_cache_dir(code: str) -> Path:
    """``data/cache/cems/{code}/`` (honours ``MONTANDON_DATA_DIR``)."""
    path = CACHE_DIR / "cems" / str(code).strip()
    path.mkdir(parents=True, exist_ok=True)
    return path


_AOI_RE = re.compile(r"AOI(\d+)", re.IGNORECASE)
_MONIT_RE = re.compile(r"MONIT(\d+)", re.IGNORECASE)
_THEME_RE = re.compile(r"(?:PRODUCT|MONIT\d+)_(.+)_v\d+$", re.IGNORECASE)


def load_cached_vectors(code: str) -> dict[str, gpd.GeoDataFrame]:
    """Load the latest cached GeoJSON for each area of interest and theme.

    Notebook 01 stores every published vector layer, including monitoring
    repeats and ``notAnalysed`` extents. Notebook 02 should see one current
    layer per area and theme, so this keeps the highest monitoring number and
    drops layers whose name is ``notAnalysed``.
    """
    folder = CACHE_DIR / "cems" / str(code).strip()
    files = [
        path
        for pattern in ("*.json", "*.geojson")
        for path in sorted(folder.glob(pattern))
        if path.is_file() and not path.name.endswith(".part")
    ]
    if not files:
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
    """Analysed cache files in monitoring order, with a delivery time when the API responds.

    ``notAnalysed`` layers are omitted. Every monitoring step is kept, unlike
    ``load_cached_vectors``, which keeps only the latest step for notebook 02.
    """
    folder = CACHE_DIR / "cems" / str(code).strip()
    files = [
        path
        for pattern in ("*.json", "*.geojson")
        for path in sorted(folder.glob(pattern))
        if path.is_file() and not path.name.endswith(".part")
    ]
    if not files:
        raise FileNotFoundError(
            f"No cached CEMS vectors in {folder}. Run notebooks/01_cems_api_ingestion.ipynb first."
        )
    delivered = _delivery_times(code)
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


def _delivery_times(code: str) -> dict[str, str]:
    """Map a cached GeoJSON filename to the product ``deliveryTime``. The API is optional."""
    try:
        activation = fetch_activation(code)
    except Exception:
        return {}
    delivered = {}
    for record in published_vector_layers(activation):
        leaf = str(record["url"]).rstrip("/").split("/")[-1].split("?")[0]
        if record.get("delivery_time"):
            delivered[leaf] = record["delivery_time"]
    return delivered


def _layer_identity(path: Path) -> tuple[str, int, str]:
    """Return ``(aoi, monitoring_number, theme)`` parsed from a cache filename."""
    stem = path.stem
    aoi_match = _AOI_RE.search(stem)
    monitoring_match = _MONIT_RE.search(stem)
    theme_match = _THEME_RE.search(stem)
    token = theme_match.group(1) if theme_match else stem
    # CEMS suffixes A/P/L are area, point, and line versions of one theme.
    family = token[:-1] if len(token) > 1 and token[-1] in {"A", "P", "L"} else token
    aoi = aoi_match.group(1) if aoi_match else stem
    monitoring = int(monitoring_match.group(1)) if monitoring_match else 0
    return aoi, monitoring, family


def load_published_vectors(
    activation: dict[str, Any],
) -> tuple[dict[str, gpd.GeoDataFrame], list[str]]:
    """Download published vector GeoJSON into the cache and load each file.

    A layer that fails to download or parse is reported and skipped. Files
    already in the cache are reused.
    """
    code = activation.get("code")
    if not code:
        raise ValueError("activation has no code")
    cache_dir = vector_cache_dir(str(code))
    loaded: dict[str, gpd.GeoDataFrame] = {}
    errors: list[str] = []
    for record in published_vector_layers(activation):
        layer_name = str(record["layer"])
        path = _cache_path(cache_dir, record["url"], layer_name)
        try:
            if not path.exists() or path.stat().st_size == 0:
                _download_file(record["url"], path)
            frame = gpd.read_file(path)
            if frame.crs is None:
                frame = frame.set_crs("EPSG:4326")
            frame["cems_layer"] = layer_name
            frame["aoi_number"] = record["aoi_number"]
            frame["aoi_name"] = record["aoi_name"]
            frame["product_type"] = record["product_type"]
            frame["monitoring_number"] = record["monitoring_number"]
            frame["delivery_time"] = record["delivery_time"]
            loaded[layer_name] = frame
        except Exception as exc:
            errors.append(f"{layer_name}: {exc}")
    return loaded, errors


def impact_stats_table(activation: dict[str, Any]) -> pd.DataFrame:
    """Activation totals plus statistics on each published GRA or GRM product.

    These are the figures Copernicus already publishes. They are not the
    admin-level overlay computed in notebook 02.
    """
    rows = _stat_rows(activation.get("stats"), scope="activation")
    for aoi in activation.get("aois") or []:
        for product in aoi.get("products") or []:
            product_type = product.get("type")
            if product_type not in {"GRA", "GRM"}:
                continue
            version = product.get("version") or {}
            if version.get("statusCode") != "F":
                continue
            rows.extend(
                _stat_rows(
                    product.get("stats"),
                    scope="product",
                    aoi_number=product.get("aoiNumber", aoi.get("number")),
                    aoi_name=product.get("aoiName", aoi.get("name")),
                    product_type=product_type,
                    monitoring_number=product.get("monitoringNumber"),
                )
            )
    return pd.DataFrame(rows, columns=_STAT_COLUMNS)


def _stat_rows(stats: Any, **context: Any) -> list[dict[str, Any]]:
    """Flatten ``{thematic: {subclass: {total, affected, unit}}}`` or a scalar map."""
    base = {column: context.get(column) for column in _STAT_COLUMNS}
    if not isinstance(stats, dict):
        return []
    rows = []
    for thematic, payload in stats.items():
        if isinstance(payload, dict) and payload and all(isinstance(value, dict) for value in payload.values()):
            for subclass, figures in payload.items():
                unit = figures.get("unit") or figures.get("totalUnit") or None
                rows.append(
                    {
                        **base,
                        "thematic": thematic,
                        "subclass": subclass,
                        "unit": unit or None,
                        "total": figures.get("total"),
                        "affected": figures.get("affected"),
                    }
                )
            continue
        if isinstance(payload, dict):
            rows.append(
                {
                    **base,
                    "thematic": thematic,
                    "subclass": None,
                    "unit": payload.get("unit") or payload.get("totalUnit"),
                    "total": payload.get("total", payload.get("value")),
                    "affected": payload.get("affected"),
                }
            )
            continue
        rows.append(
            {
                **base,
                "thematic": thematic,
                "subclass": None,
                "unit": None,
                "total": payload,
                "affected": None,
            }
        )
    return rows


def _cache_path(cache_dir: Path, url: str, layer_name: str) -> Path:
    leaf = url.rstrip("/").split("/")[-1].split("?")[0]
    if not leaf or leaf in {".", ".."}:
        leaf = layer_name.replace("\\", "/").rstrip("/").split("/")[-1] + ".geojson"
    safe = "".join(char if char.isalnum() or char in "-_." else "_" for char in leaf)
    return cache_dir / safe


def _download_file(url: str, destination: Path) -> None:
    """Stream a GeoJSON to a ``.part`` file, then rename it into place."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".part")
    with requests.get(url, stream=True, timeout=_VECTOR_TIMEOUT, headers=_USER_AGENT) as response:
        response.raise_for_status()
        with temporary.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 256):
                if chunk:
                    handle.write(chunk)
    temporary.replace(destination)
