"""Carbon footprint estimation for delivery trips."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

CONSTANTS = {
    "route_path": "/carbon-footprint",
    "co2_kg_per_km": 0.12,
    "comparison_vehicle_kg_per_km": 0.12,
}

router = APIRouter(tags=["Carbon Footprint"])


class CarbonFootprintRequest(BaseModel):
    """Request body for delivery carbon estimation."""

    distance_km: float = Field(..., ge=0.0)
    trips_per_day: int = Field(default=1, ge=1)


@router.post(CONSTANTS["route_path"])
def estimate_carbon_footprint(request: CarbonFootprintRequest) -> dict[str, float | str]:
    """Estimate total emitted CO2 and relatable distance equivalent."""
    total_km = request.distance_km * request.trips_per_day
    co2_kg = total_km * CONSTANTS["co2_kg_per_km"]
    equivalent_km = co2_kg / CONSTANTS["comparison_vehicle_kg_per_km"]
    return {
        "total_distance_km": round(total_km, 2),
        "estimated_co2_kg": round(co2_kg, 3),
        "comparison": f"Equivalent to driving {round(equivalent_km, 2)} km",
        "source": "live",
    }
