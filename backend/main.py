from dotenv import load_dotenv
import os
import shutil
import logging
import pandas as pd

# Imports for FastAPI and related components
from fastapi import FastAPI, UploadFile, File, Request, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, validator
from routers.properties import router as properties_router

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app instance
app = FastAPI(title="MJ Home API")

# Register the router
app.include_router(properties_router)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load allowed suburbs
DATA_FILE = os.path.join("data_processing", "MockData.xlsx")
if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(f"MockData.xlsx not found at {DATA_FILE}")

try:
    df = pd.read_excel(DATA_FILE)
    ALLOWED_SUBURBS = sorted(df["Suburb"].dropna().astype(str).str.strip().unique().tolist())
    logger.info("Allowed suburbs loaded: %d suburbs", len(ALLOWED_SUBURBS))
except Exception as e:
    logger.error("Error loading suburbs from Excel: %s", str(e))
    ALLOWED_SUBURBS = []

# Pydantic Input Model
class RentalInput(BaseModel):
    bedrooms: int = Field(..., gt=0, description="Number of bedrooms (must be greater than 0)", example=3)
    bathrooms: int = Field(..., gt=0, description="Number of bathrooms (must be greater than 0)", example=1)
    floor_area: float = Field(..., gt=10, description="Floor area in square meters (must be greater than 10)", example=85)
    suburb: str = Field(..., description="Suburb name (must be from dataset)", example="Manurewa")

    @validator("suburb")
    def validate_suburb(cls, v):
        if not v.strip():
            raise ValueError("Suburb cannot be empty.")
        if v.strip().isdigit():
            raise ValueError("Suburb cannot be a number.")
        if v.strip() not in ALLOWED_SUBURBS:
            raise ValueError(f"Invalid suburb. Must be one of: {', '.join(ALLOWED_SUBURBS[:5])}...")
        return v.strip()

# Module Imports
from pipeline_main import main as run_pipeline
from data_processing.loader import save_to_db, fetch_processed_data
from data_scraper.scraper import scrape_listings
from data_processing.cleaner import clean_data
from data_processing.predictor import predict_rent
from Machine_Learning_Model.retrain_model import retrain_rent_model
from Machine_Learning_Model.predict_logger import log_prediction
from Machine_Learning_Model.rental_price_model import load_model, prepare_input_dataframe

# API Endpoints
@app.get("/", summary="Health Verification", description="Verify whether the MJ Home API is live and running.")
def read_root():
    return {"message": "MJ Home API is live"}

@app.post("/run-pipeline", summary="Trigger Pipeline", description="Manually trigger the complete data processing pipeline.")
def run_pipeline_endpoint():
    try:
        run_pipeline()
        return {"status": "Pipeline completed successfully"}
    except Exception as e:
        return {"status": "Error", "detail": str(e)}

@app.get("/data", summary="View Processed Data", description="Fetch cleaned and processed property data for the frontend dashboard.")
def get_data(limit: int = 100):
    data = fetch_processed_data(limit)
    return {"status": "success", "data": data}

@app.post("/retrain-model", summary="Retrain ML Model", description="Manually retrain the rental price prediction model using the latest data.")
def retrain_model_endpoint():
    result = retrain_rent_model()
    return {"status": "done", "message": result}

@app.post("/upload-data", summary="Upload and Retrain", description="Upload a new Excel dataset and automatically retrain the rental price model.")
async def upload_data(file: UploadFile = File(...)):
    try:
        logger.info("[UPLOAD] Upload endpoint hit")

        if not file.filename.endswith(".xlsx"):
            return {"status": "error", "message": "Invalid file format. Please upload an Excel .xlsx file."}

        save_path = os.path.join("data_processing", "MockData.xlsx")
        logger.info("[UPLOAD] Saving uploaded file to %s", save_path)

        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info("[UPLOAD] File saved. Starting model retraining...")
        retrain_result = retrain_rent_model()

        return {
            "status": "success",
            "message": "File uploaded and model retrained.",
            "retrain_result": retrain_result
        }

    except Exception as e:
        logger.error("[UPLOAD] Error during upload or retrain: %s", str(e))
        return {
            "status": "error",
            "message": f"Upload or retraining failed: {str(e)}"
        }

@app.post(
    "/predict",
    summary="Predict Rental Price",
    description="Submit property features to receive a predicted rental price.",
    response_model=dict
)
async def predict_rental_price(
    request: Request,
    input_data: RentalInput = Body(...)
):
    try:
        model = load_model()
        if model is None:
            raise HTTPException(status_code=500, detail="Model not loaded")

        df_input = prepare_input_dataframe(input_data)
        prediction = model.predict(df_input)[0]

        user_id = request.headers.get("X-User-ID", "anonymous")
        log_prediction(input_data.dict(), prediction, user_id)

        return {"predicted_rent": round(prediction, 2)}

    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))

    except Exception as e:
        logger.error("[PREDICT] Internal error: %s", str(e))
        raise HTTPException(status_code=500, detail="Prediction failed: " + str(e))

@app.get("/favicon.ico", summary="Favicon", description="Returns the favicon for the MJ Home API (used by browser tabs).")
async def favicon():
    return FileResponse("static/favicon.ico")

if __name__ == "__main__":
    import uvicorn
    print("MJ Home API Docs:")
    print("http://127.0.0.1:8000/docs")
    print("http://localhost:8000/docs")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
