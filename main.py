"""Main FastAPI application for the KisanConnect ML service."""

from __future__ import annotations

import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from carbon_footprint import router as carbon_router
from delivery_match import router as delivery_router
from demand_forecast import preload_models, router as demand_router
from price_engine import router as price_router
from reputation_score import router as reputation_router
from seasonal_calendar import router as seasonal_router

CONSTANTS = {
    "service_name": "KisanConnect ML API",
    "version": "1.0.0",
    "disable_preload_env": "KC_DISABLE_MODEL_PRELOAD",
    # CORS: `allow_credentials=True` MUST NOT be used with `allow_origins=["*"]` (browser will block).
    "cors_development_origins": [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8000",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8000",
    ],
    # Any http/https origin in development (Swagger, local frontends, tunnel URLs).
    "cors_development_origin_regex": r"https?://.*",
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=CONSTANTS["service_name"], version=CONSTANTS["version"])
# Middleware must run before routing; register CORS immediately after creating the app.
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(CONSTANTS["cors_development_origins"]),
    allow_origin_regex=CONSTANTS["cors_development_origin_regex"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(price_router, prefix="/ml")
app.include_router(demand_router, prefix="/ml")
app.include_router(reputation_router, prefix="/ml")
app.include_router(delivery_router, prefix="/ml")
app.include_router(carbon_router, prefix="/ml")
app.include_router(seasonal_router, prefix="/ml")


@app.on_event("startup")
def startup_event() -> None:
    """Load and cache ML models during service startup."""
    if os.getenv(CONSTANTS["disable_preload_env"], "0") == "1":
        logger.info("Skipping model preload due to %s=1", CONSTANTS["disable_preload_env"])
        return
    logger.info("Preloading demand forecasting models")
    preload_models()


@app.get("/", tags=["System"])
def root() -> dict[str, str]:
    """Return service metadata."""
    return {"service": CONSTANTS["service_name"], "version": CONSTANTS["version"]}


@app.get("/health", tags=["System"])
def health_check() -> dict[str, str]:
    """Return health status for monitoring."""
    return {"status": "ok", "source": "live"}