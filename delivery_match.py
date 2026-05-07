"""Delivery partner matching based on distance and rating."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from utils import haversine, safe_divide

CONSTANTS = {
    "route_path": "/delivery-match",
    "MAX_DISTANCE_KM": 50.0,
    "weight_distance": 0.7,
    "weight_rating": 0.3,
    "rating_scale_max": 5.0,
}

router = APIRouter(tags=["Delivery Match"])


class Location(BaseModel):
    """Lat/lon location model."""

    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)


class PartnerInput(BaseModel):
    """Delivery partner metadata used for ranking."""

    partner_id: str = Field(..., min_length=1)
    location: Location
    rating: float = Field(..., ge=0.0, le=CONSTANTS["rating_scale_max"])


class DeliveryMatchRequest(BaseModel):
    """Request body for delivery partner matching."""

    pickup: Location
    partners: list[PartnerInput]


@router.post(CONSTANTS["route_path"])
def match_delivery_partners(request: DeliveryMatchRequest) -> dict[str, Any]:
    """Rank delivery partners by distance and service rating."""
    if not request.partners:
        return {"matches": [], "source": "live"}

    scored = []
    for partner in request.partners:
        distance = haversine(
            request.pickup.lat, request.pickup.lon, partner.location.lat, partner.location.lon
        )
        distance_score = max(0.0, 1.0 - safe_divide(distance, CONSTANTS["MAX_DISTANCE_KM"], default=1.0))
        rating_score = safe_divide(partner.rating, CONSTANTS["rating_scale_max"], default=0.0)
        combined = (
            CONSTANTS["weight_distance"] * distance_score
            + CONSTANTS["weight_rating"] * rating_score
        )
        scored.append(
            {
                "partner_id": partner.partner_id,
                "distance_km": round(distance, 2),
                "distance_score": round(distance_score, 4),
                "rating_score": round(rating_score, 4),
                "match_score": round(combined, 4),
            }
        )
    ranked = sorted(scored, key=lambda x: x["match_score"], reverse=True)
    return {"matches": ranked, "source": "live"}
