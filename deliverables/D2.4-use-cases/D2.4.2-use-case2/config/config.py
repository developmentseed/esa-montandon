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
# Montandon STAC catalog. Item and search calls need a bearer token; it is never logged.
MONTANDON_STAC_URL = os.getenv("MONTANDON_STAC_URL", "https://montandon-eoapi.ifrc.org/stac").rstrip("/")
MONTANDON_STAC_TOKEN = os.getenv(
    "MONTANDON_STAC_TOKEN",
    "eyJhbGciOiJSUzI1NiIsImtpZCI6IlNpcllQbE96bWVacUZsdkpUZDBXdmF0dlc4UDYyZG04Y0stRGhwQkxubjQiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiI1ZWQ2ZjE1Yy04ZTg4LTQ0MDgtOGM0Mi0yYmIxNzhjMDVlOGMiLCJ1c2VySWQiOjE1NDYzLCJpYXQiOjE3OTA3NTQ0OTAsImV4cCI6MTgyMjI5MDQ5MCwiaW5Nb3ZlbWVudCI6dHJ1ZX0.XPs8paIhG18A2L2Jh0xrc-2E2Yn-7kpXdkc285VcWlZy2idywuNxI-e0yJGk7BMipCFECIURhl1qEtQJ0954S8ZMdHxt-I0FufVQWyz8ScoS3VhhUGkK3w3EdBK2i3XCfRttwsOkcSjP8ZYf1BPAtSmqdRFfj-c6QjRUZBQ-8uxDgWcAjEoEOnNZE0lfxImsfL8euCdsJTInK9bJflKK8SE2NTuahZnW7V2hZndNt1EnMPDVf_qK53EmPF0WABE1uETrvczIyBuNqHMh0QqsSE0u73AJ92XxBWifoAJb9SJSJWJViDRvzIJpY198Vt11jwVt_HVGX-58HQHgsqEjz4647epSgTkqS-lIwlXwodP3wYabh92KHMXffmqiby8t6wAdvcETYsXpTqu0UueqExqj5Q0ABtPzNfu7FwJqF8Bs28hubemTG5zn-iVDwcF6CFebBveCvCHa4cEs0dnfMoGQRkNA1zkREg0DjzdkLrcAz4_g3HU7Ai_RptJvlmZrTTZMUVTDSlui8OhFASLGQrs9QZm6Vs2VkEpAslcUm76tAQRLHTkCXW1sm9wL7lqkFs-s0xBuP4ZD56_AMo08iL3hlq6bsY7HkH38Lzbo6haq7kbdNjR2h4ir4urVAFwxdPg2DeZvo4rcxuMnSzVYpIhJfmm2L81V-zpkpKdHLY8",
)
# Unused by the notebooks. Kept so the old experimental STAC client still imports.
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
