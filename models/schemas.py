from pydantic import BaseModel, Field
from typing import List, Optional

class PricePredictionRequest(BaseModel):
    crop: str = Field(..., example="Tomato")
    district: str = Field(..., example="Bhopal")
    season: str = Field(..., example="Rabi")
    rainfall_mm: float = Field(..., example=120.5)

class NLPRequest(BaseModel):
    voice_transcript: str = Field(..., example="मुझे पचास किलो प्याज बेचना है")

class CarbonEstimateRequest(BaseModel):
    farm_lat: float = Field(..., example=23.8388) # Damoh coords
    farm_lon: float = Field(..., example=79.4411)
    buyer_lat: float = Field(..., example=12.9716) # Bengaluru coords
    buyer_lon: float = Field(..., example=77.5946)
    weight_kg: float = Field(..., example=500)