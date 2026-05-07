"""Price engine endpoint with live API and mock fallback."""

from __future__ import annotations

import logging
import os
from statistics import mean

import requests
from dotenv import load_dotenv
from fastapi import APIRouter
from pydantic import BaseModel, Field

from mock_data import MOCK_MANDI_PRICES
from utils import normalize_crop, normalize_state, safe_divide

load_dotenv()
API_KEY = os.getenv("DATA_GOV_API_KEY")

CONSTANTS = {
    "route_path": "/price-engine",
    "data_gov_url": "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070",
    "request_timeout_sec": 8,
    "max_records": 10,
    "default_markup_factor": 1.25,
    "placeholder_api_key": "your_api_key_here",
}

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Price Engine"])


class PriceEngineRequest(BaseModel):
    """Request body for price engine predictions."""

    crop: str = Field(..., min_length=2, description="Crop name")
    state: str = Field(..., min_length=2, description="State name")
    market: str | None = Field(default=None, description="Optional mandi market")


def fetch_live_mandi_price(crop: str, state: str, market: str | None) -> dict[str, object]:
    """Fetch mandi prices from Data.gov and return normalized response."""
    if not API_KEY or API_KEY.strip() == CONSTANTS["placeholder_api_key"]:
        logger.info("Skipping live mandi fetch because API key is missing/placeholder")
        return {"price": None, "source": "mock", "market_used": market or "unknown"}

    params = {
        "api-key": API_KEY,
        "format": "json",
        "offset": 0,
        "limit": CONSTANTS["max_records"],
        "filters[commodity]": crop.title(),
        "filters[state]": state.title(),
    }
    if market:
        params["filters[market]"] = market.title()

    try:
        response = requests.get(
            CONSTANTS["data_gov_url"], params=params, timeout=CONSTANTS["request_timeout_sec"]
        )
        response.raise_for_status()
        payload = response.json()
        records = payload.get("records", [])
        if not records:
            return {"price": None, "source": "live", "market_used": market or "unknown"}

        parsed_prices = []
        market_name = market or records[0].get("market", "unknown")
        for record in records:
            try:
                parsed_prices.append(float(record.get("modal_price", 0)))
            except (TypeError, ValueError):
                continue
        if not parsed_prices:
            return {"price": None, "source": "live", "market_used": market_name}
        return {"price": mean(parsed_prices), "source": "live", "market_used": market_name}
    except (requests.RequestException, ValueError) as exc:
        logger.warning("Live mandi fetch failed: %s", exc)
        return {"price": None, "source": "mock", "market_used": market or "unknown"}


def fetch_mock_price(crop: str, market: str | None) -> dict[str, object]:
    """Return price from static mock data as resilient fallback."""
    crop_prices = MOCK_MANDI_PRICES.get(crop)
    if not crop_prices:
        return {"price": None, "source": "mock", "market_used": market or "unknown"}

    if market and market.title() in crop_prices:
        return {
            "price": float(crop_prices[market.title()]),
            "source": "mock",
            "market_used": market.title(),
        }

    market_name = next(iter(crop_prices.keys()))
    return {"price": float(crop_prices[market_name]), "source": "mock", "market_used": market_name}


@router.post(CONSTANTS["route_path"])
def estimate_price(request: PriceEngineRequest) -> dict[str, object]:
    """Estimate fair farmer and consumer prices using mandi inputs."""
    crop = normalize_crop(request.crop)
    state = normalize_state(request.state)
    market = request.market.strip() if request.market else None

    live_result = fetch_live_mandi_price(crop=crop, state=state, market=market)
    if live_result["price"] is None:
        fallback = fetch_mock_price(crop=crop, market=market)
        base_price = float(fallback["price"] or 0.0)
        source = fallback["source"]
        market_used = fallback["market_used"]
    else:
        base_price = float(live_result["price"])
        source = str(live_result["source"])
        market_used = live_result["market_used"]

    farmer_price = round(base_price, 2)
    consumer_price = round(farmer_price * CONSTANTS["default_markup_factor"], 2)
    spread = round(consumer_price - farmer_price, 2)
    spread_ratio = round(safe_divide(spread, farmer_price, default=0.0), 4)

    return {
        "crop": crop,
        "state": state,
        "market": market_used,
        "farmer_price": farmer_price,
        "consumer_price": consumer_price,
        "spread": spread,
        "spread_ratio": spread_ratio,
        "source": source,
    }
