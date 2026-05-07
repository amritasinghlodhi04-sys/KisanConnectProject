"""Shared utility helpers for KisanConnect ML modules."""

from __future__ import annotations

import math

CONSTANTS = {
    "earth_radius_km": 6371.0,
}


def normalize_state(state: str) -> str:
    """Normalize state input for consistent downstream matching."""
    return " ".join(state.strip().lower().split())


def normalize_crop(crop: str) -> str:
    """Normalize crop input for consistent downstream matching."""
    return " ".join(crop.strip().lower().split())


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Compute great-circle distance in kilometers between coordinates."""
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a_val = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    )
    c_val = 2 * math.atan2(math.sqrt(a_val), math.sqrt(max(0.0, 1 - a_val)))
    return CONSTANTS["earth_radius_km"] * c_val


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide numbers and avoid division-by-zero exceptions."""
    if denominator == 0:
        return default
    return numerator / denominator
