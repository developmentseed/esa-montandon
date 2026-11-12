"""Runtime paths and optional service URLs (override with environment variables)."""

from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = Path(os.getenv("MONTANDON_DATA_DIR", PROJECT_ROOT / "data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR = DATA_DIR / "cache"  # GADM JSON, GHSL window, etc.
CACHE_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_CRS = "EPSG:4326"
WEB_MERCATOR_CRS = "EPSG:3857"
# Montandon STAC catalog. Item and search calls need a bearer token; it is never logged.
MONTANDON_STAC_URL = os.getenv("MONTANDON_STAC_URL", "https://montandon-eoapi.ifrc.org/stac").rstrip("/")
MONTANDON_STAC_TOKEN = os.getenv(
    "MONTANDON_STAC_TOKEN",
    "YOUR_TOKEN_HERE",
)
# Unused by the notebooks. Kept so the old experimental STAC client still imports.
CEMS_STAC_URL = os.getenv("CEMS_STAC_URL", "https://stac.dataspace.copernicus.eu/v1")
CEMS_WFS_URL = os.getenv("CEMS_WFS_URL", "https://example.invalid/cems/wfs")
CEMS_API_TOKEN = os.getenv("CEMS_API_TOKEN")
OVERPASS_URL = os.getenv("OVERPASS_URL", "https://overpass-api.de/api/interpreter")
HDX_API_URL = os.getenv("HDX_API_URL", "https://data.humdata.org/api/3/action")
# GHS-POP R2023A Cloud Optimized GeoTIFF on Source Cooperative. {row} and {col}
# are the Mollweide tile indexes (R{row}_C{col}); {year} is a five-year epoch.
GHSL_COG_URL_TEMPLATE = os.getenv(
    "GHSL_COG_URL_TEMPLATE",
    "https://data.source.coop/nlebovits/ghsl/pop-{year}/pop-{year}-R{row}_C{col}/"
    "GHS_POP_E{year}_GLOBE_R2023A_54009_100_V1_0_R{row}_C{col}.tif",
)
HTTP_TIMEOUT_SECONDS = int(os.getenv("MONTANDON_HTTP_TIMEOUT", "120"))
