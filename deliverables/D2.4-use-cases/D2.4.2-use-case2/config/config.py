"""Runtime paths and optional service URLs (override with environment variables)."""

from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = Path(os.getenv("MONTANDON_DATA_DIR", PROJECT_ROOT / "data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR = DATA_DIR / "cache"  # GADM JSON, WorldPop tif, etc.
CACHE_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_CRS = "EPSG:4326"
WEB_MERCATOR_CRS = "EPSG:3857"
# Unused by the notebooks (they read local files). Kept for optional STAC/WFS experiments.
CEMS_STAC_URL = os.getenv("CEMS_STAC_URL", "https://stac.dataspace.copernicus.eu/v1")
CEMS_WFS_URL = os.getenv("CEMS_WFS_URL", "https://example.invalid/cems/wfs")
CEMS_API_TOKEN = os.getenv("CEMS_API_TOKEN")
OVERPASS_URL = os.getenv("OVERPASS_URL", "https://overpass-api.de/api/interpreter")
HDX_API_URL = os.getenv("HDX_API_URL", "https://data.humdata.org/api/3/action")
WORLDPOP_GIS_URL_TEMPLATE = os.getenv(
    "WORLDPOP_GIS_URL_TEMPLATE",
    "https://data.worldpop.org/GIS/Population/Global_2000_2020_1km_UNadj/{year}/{iso}/{iso_lower}_ppp_{year}_1km_Aggregated_UNadj.tif",
)
HTTP_TIMEOUT_SECONDS = int(os.getenv("MONTANDON_HTTP_TIMEOUT", "120"))
