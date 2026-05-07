"""Seasonal crop calendar endpoint using synthetic demand metadata."""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel, Field

from utils import normalize_crop

CONSTANTS = {
    "route_path": "/seasonal-calendar",
    "crop_calendar": {
        "tomato": {"peak_months": [11, 12, 1, 2], "season_label": "winter peak"},
        "onion": {"peak_months": [3, 4, 5], "season_label": "summer peak"},
        "potato": {"peak_months": [12, 1, 2], "season_label": "rabi harvest"},
        "wheat": {"peak_months": [3, 4], "season_label": "rabi harvest"},
        "rice": {"peak_months": [10, 11], "season_label": "kharif harvest"},
    },
}

router = APIRouter(tags=["Seasonal Calendar"])


class SeasonalCalendarRequest(BaseModel):
    """Request body for seasonal crop insights."""

    crop: str = Field(..., min_length=2)


@router.post(CONSTANTS["route_path"])
def get_seasonal_calendar(request: SeasonalCalendarRequest) -> dict[str, object]:
    """Return current seasonal context for a crop."""
    crop = normalize_crop(request.crop)
    crop_info = CONSTANTS["crop_calendar"].get(crop)
    if not crop_info:
        return {
            "crop": crop,
            "is_peak_season": False,
            "season_label": "unknown",
            "peak_months": [],
            "source": "mock",
        }
    current_month = datetime.utcnow().month
    is_peak = current_month in crop_info["peak_months"]
    return {
        "crop": crop,
        "is_peak_season": is_peak,
        "season_label": crop_info["season_label"],
        "peak_months": crop_info["peak_months"],
        "source": "mock",
    }
