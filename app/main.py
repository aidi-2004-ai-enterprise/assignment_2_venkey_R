# app/main.py
import logging
import sys
from typing import Dict

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Penguin Species Classification API",
    description="A production-ready API for predicting penguin species using XGBoost",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Simple Pydantic models for testing
class PenguinFeatures(BaseModel):
    bill_length_mm: float
    bill_depth_mm: float
    flipper_length_mm: float
    body_mass_g: float

class PredictionResponse(BaseModel):
    species: str
    confidence: float
    message: str = "Prediction successful"

# Routes
@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Penguin Species Classification API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "API is running"
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict_penguin_species(features: PenguinFeatures):
    """
    Predict penguin species based on physical measurements.
    
    For now, this is a mock implementation.
    """
    try:
        # Mock prediction logic (replace with actual model later)
        if features.bill_length_mm > 45:
            species = "Gentoo"
            confidence = 0.85
        elif features.bill_depth_mm > 18:
            species = "Adelie"
            confidence = 0.78
        else:
            species = "Chinstrap"
            confidence = 0.82
        
        return PredictionResponse(
            species=species,
            confidence=confidence
        )
        
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)
