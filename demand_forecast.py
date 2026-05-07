"""Demand forecasting endpoint powered by cached Prophet models."""

from __future__ import annotations

import logging
from datetime import timedelta

import numpy as np
import pandas as pd
from fastapi import APIRouter
from prophet import Prophet
from pydantic import BaseModel, Field

from utils import normalize_crop, normalize_state

np.random.seed(42)

CONSTANTS = {
    "route_path": "/demand-forecast",
    "history_weeks": 104,
    "forecast_weeks_default": 12,
    "forecast_weeks_max": 52,
    "crop_list": ["tomato", "onion", "potato", "wheat", "rice"],
    "state_list": ["madhya pradesh", "maharashtra", "punjab", "karnataka"],
}

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Demand Forecast"])
MODEL_CACHE: dict[str, Prophet] = {}


class DemandForecastRequest(BaseModel):
    """Request payload for demand forecast generation."""

    crop: str = Field(..., min_length=2)
    state: str = Field(..., min_length=2)
    weeks: int = Field(default=CONSTANTS["forecast_weeks_default"], ge=1, le=CONSTANTS["forecast_weeks_max"])


def _model_key(crop: str, state: str) -> str:
    """Create deterministic model key for cache lookup."""
    return f"{crop}::{state}"


def build_synthetic_history(crop: str, state: str) -> pd.DataFrame:
    """Generate synthetic weekly demand data for two years."""
    weeks = CONSTANTS["history_weeks"]
    end_date = pd.Timestamp.today().normalize()
    start_date = end_date - timedelta(weeks=weeks - 1)
    dates = pd.date_range(start=start_date, periods=weeks, freq="W")

    # Crop/state hash offsets produce stable but distinct trajectories.
    crop_bias = (sum(ord(ch) for ch in crop) % 30) + 70
    state_bias = sum(ord(ch) for ch in state) % 20
    seasonality = 15 * np.sin(np.linspace(0, 6 * np.pi, weeks))
    trend = np.linspace(0, 8, weeks)
    noise = np.random.normal(loc=0, scale=4, size=weeks)
    demand = np.maximum(1.0, crop_bias + state_bias + seasonality + trend + noise)
    return pd.DataFrame({"ds": dates, "y": demand})


def train_and_cache_model(crop: str, state: str) -> None:
    """Train a Prophet model once and store it in cache."""
    key = _model_key(crop, state)
    if key in MODEL_CACHE:
        return
    history_df = build_synthetic_history(crop=crop, state=state)
    model = Prophet(weekly_seasonality=True, yearly_seasonality=True, daily_seasonality=False)
    model.fit(history_df)
    MODEL_CACHE[key] = model
    logger.info("Cached demand model for %s", key)


def preload_models() -> None:
    """Preload baseline crop/state combinations on application startup."""
    for crop in CONSTANTS["crop_list"]:
        for state in CONSTANTS["state_list"]:
            train_and_cache_model(crop=crop, state=state)


@router.post(CONSTANTS["route_path"])
def forecast_demand(request: DemandForecastRequest) -> dict[str, object]:
    """Return weekly demand forecast using cached Prophet model."""
    crop = normalize_crop(request.crop)
    state = normalize_state(request.state)
    key = _model_key(crop, state)
    if key not in MODEL_CACHE:
        train_and_cache_model(crop=crop, state=state)

    model = MODEL_CACHE[key]
    future = model.make_future_dataframe(periods=request.weeks, freq="W")
    forecast = model.predict(future).tail(request.weeks)

    points = [
        {"date": row.ds.date().isoformat(), "predicted_demand": round(float(row.yhat), 2)}
        for row in forecast.itertuples()
    ]
    return {
        "crop": crop,
        "state": state,
        "weeks": request.weeks,
        "forecast": points,
        "source": "live",
    }
