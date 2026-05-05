from fastapi import FastAPI
from api.routers import pricing, nlp, farmer, sustainability

app = FastAPI(
    title="KisanConnect ML API",
    description="AI/ML Microservice for the KisanConnect direct marketplace.",
    version="1.0.0"
)

# Include API Routers
app.include_router(pricing.router, prefix="/ml", tags=["Pricing & Demand"])
app.include_router(nlp.router, prefix="/ml", tags=["NLP & Voice"])
app.include_router(farmer.router, prefix="/ml", tags=["Farmer Intelligence"])
app.include_router(sustainability.router, prefix="/ml", tags=["Sustainability & Health"])

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "healthy", "service": "kisanconnect-ml"}