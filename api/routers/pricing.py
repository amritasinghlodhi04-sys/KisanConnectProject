from fastapi import APIRouter, HTTPException
from models.schemas import PricePredictionRequest
from services.model_service import MLModelService

router = APIRouter()
model_service = MLModelService()

@router.post("/price-recommend")
async def recommend_price(request: PricePredictionRequest):
    """
    Uses a Regression Model (Random Forest) to output a suggested price range.
    """
    try:
        # Pass features to the model service
        features = [request.crop, request.district, request.season, request.rainfall_mm]
        predicted_price = model_service.predict_price(features)
        
        # Create a dynamic range (e.g., +/- 10% for negotiation flexibility)
        min_price = round(predicted_price * 0.9, 2)
        max_price = round(predicted_price * 1.1, 2)
        
        return {
            "crop": request.crop,
            "district": request.district,
            "recommended_min_price": min_price,
            "recommended_max_price": max_price,
            "unit": "INR/kg"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/demand-forecast")
async def forecast_demand(crop_id: str, days_ahead: int = 7):
    """
    Uses Facebook Prophet to output future demand trends.
    """
    # In a real scenario, fetch past order data for this crop from DB here
    forecast_data = model_service.forecast_demand(crop_id, days_ahead)
    return {"crop_id": crop_id, "forecast": forecast_data}