"""Pytest suite for KisanConnect ML API endpoints."""

from __future__ import annotations

import os
from typing import Any

from fastapi.testclient import TestClient

os.environ["KC_DISABLE_MODEL_PRELOAD"] = "1"

from main import app

CONSTANTS = {
    "json_content_type": "application/json",
}

client = TestClient(app)


def assert_json_response(response: Any) -> dict[str, Any]:
    """Assert response is valid JSON object and return parsed payload."""
    assert response.status_code == 200
    assert CONSTANTS["json_content_type"] in response.headers.get("content-type", "")
    payload = response.json()
    assert isinstance(payload, dict)
    return payload


def test_root_endpoint() -> None:
    """Validate root endpoint returns expected metadata."""
    response = client.get("/")
    data = assert_json_response(response)
    assert data["service"] == "KisanConnect ML API"
    assert data["version"] == "1.0.0"


def test_health_endpoint() -> None:
    """Validate health endpoint payload shape."""
    response = client.get("/health")
    data = assert_json_response(response)
    assert data["status"] == "ok"
    assert data["source"] == "live"


def test_price_engine_endpoint() -> None:
    """Validate price engine response fields and source contract."""
    response = client.post(
        "/ml/price-engine",
        json={"crop": "Tomato", "state": "Madhya Pradesh", "market": "Bhopal"},
    )
    data = assert_json_response(response)
    assert "farmer_price" in data
    assert "consumer_price" in data
    assert "spread_ratio" in data
    assert data["source"] in {"live", "mock"}


def test_demand_forecast_endpoint() -> None:
    """Validate demand forecast returns requested number of points."""
    requested_weeks = 4
    response = client.post(
        "/ml/demand-forecast",
        json={"crop": "Onion", "state": "Maharashtra", "weeks": requested_weeks},
    )
    data = assert_json_response(response)
    assert data["weeks"] == requested_weeks
    assert len(data["forecast"]) == requested_weeks
    assert data["source"] == "live"


def test_reputation_score_endpoint() -> None:
    """Validate reputation endpoint handles zero-order edge case."""
    response = client.post(
        "/ml/reputation-score",
        json={"total_orders": 0, "completed_orders": 0, "rating": 4.5},
    )
    data = assert_json_response(response)
    assert data["fulfillment_rate"] == 0.0
    assert 0 <= data["reputation_score"] <= 100
    assert data["source"] == "live"


def test_delivery_match_endpoint() -> None:
    """Validate delivery matching returns ranked partner matches."""
    response = client.post(
        "/ml/delivery-match",
        json={
            "pickup": {"lat": 23.2599, "lon": 77.4126},
            "partners": [
                {"partner_id": "d1", "location": {"lat": 23.25, "lon": 77.4}, "rating": 4.5},
                {"partner_id": "d2", "location": {"lat": 23.1, "lon": 77.2}, "rating": 4.7},
            ],
        },
    )
    data = assert_json_response(response)
    assert isinstance(data["matches"], list)
    assert len(data["matches"]) == 2
    assert data["matches"][0]["match_score"] >= data["matches"][1]["match_score"]
    assert data["source"] == "live"


def test_carbon_footprint_endpoint() -> None:
    """Validate carbon footprint endpoint comparison string."""
    response = client.post(
        "/ml/carbon-footprint",
        json={"distance_km": 18.5, "trips_per_day": 2},
    )
    data = assert_json_response(response)
    assert "Equivalent to driving" in data["comparison"]
    assert data["estimated_co2_kg"] >= 0
    assert data["source"] == "live"


def test_seasonal_calendar_endpoint() -> None:
    """Validate seasonal calendar known crop payload."""
    response = client.post("/ml/seasonal-calendar", json={"crop": "Potato"})
    data = assert_json_response(response)
    assert "is_peak_season" in data
    assert isinstance(data["peak_months"], list)
    assert data["source"] in {"mock", "live"}
