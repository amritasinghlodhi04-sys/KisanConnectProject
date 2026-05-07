"""Reputation scoring endpoint for farmers."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

from utils import safe_divide

CONSTANTS = {
    "route_path": "/reputation-score",
    "rating_scale_max": 5.0,
    "weight_fulfillment": 0.5,
    "weight_rating": 0.5,
}

router = APIRouter(tags=["Reputation Score"])


class ReputationScoreRequest(BaseModel):
    """Request body for farmer reputation calculation."""

    total_orders: int = Field(..., ge=0)
    completed_orders: int = Field(..., ge=0)
    rating: float = Field(..., ge=0.0, le=CONSTANTS["rating_scale_max"])


@router.post(CONSTANTS["route_path"])
def calculate_reputation_score(request: ReputationScoreRequest) -> dict[str, float | str]:
    """Compute a 0-100 reputation score from reliability and rating."""
    total_orders = max(0, request.total_orders)
    completed_orders = min(max(0, request.completed_orders), total_orders)
    fulfillment_rate = safe_divide(completed_orders, total_orders, default=0.0)
    normalized_rating = safe_divide(request.rating, CONSTANTS["rating_scale_max"], default=0.0)
    weighted_score = (
        CONSTANTS["weight_fulfillment"] * fulfillment_rate
        + CONSTANTS["weight_rating"] * normalized_rating
    )
    reputation_score = round(100 * weighted_score, 2)
    return {
        "reputation_score": reputation_score,
        "fulfillment_rate": round(fulfillment_rate, 4),
        "normalized_rating": round(normalized_rating, 4),
        "source": "live",
    }
