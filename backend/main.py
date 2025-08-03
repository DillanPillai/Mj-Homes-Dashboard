from dotenv import load_dotenv
import os
import shutil
import logging
import sys

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# Corrected imports
from pipeline_main import main as run_pipeline
from data_processing.loader import save_to_db, fetch_processed_data
from data_scraper.scraper import scrape_listings
from data_processing.cleaner import clean_data
from data_processing.predictor import predict_rent
from Machine_Learning_Model.retrain_model import retrain_rent_model

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialise FastAPI app
app = FastAPI(title="MJ Home API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint - health check
@app.get("/", summary="Health Verification", description="Verify whether the MJ Home API is live and running.")
def read_root():
    return {"message": "MJ Home API is live"}

# Trigger pipeline manually
@app.post("/run-pipeline", summary="Trigger Pipeline", description="Manually trigger the complete data processing pipeline.")
def run_pipeline_endpoint():
    try:
        run_pipeline()
        return {"status": "Pipeline completed successfully"}
    except Exception as e:
        return {"status": "Error", "detail": str(e)}

# Get processed data for frontend dashboard
@app.get("/data", summary="View processed Data", description="Fetch cleaned and processed property data for the frontend dashboard.")
def get_data(limit: int = 100):
    data = fetch_processed_data(limit)
    return {"status": "success", "data": data}

# Manually retrain rental model on latest available data
@app.post("/retrain-model", summary="Retrain ML Model", description="Manually retrain the rental price prediction model using the latest available data.")
def retrain_model_endpoint():
    result = retrain_rent_model()
    return {"status": "done", "message": result}

# Upload a new dataset and retrain model automatically
@app.post("/upload-data", summary="Upload and Retrain", description="Upload a new Excel dataset and automatically retrain the rental price model.")
async def upload_data(file: UploadFile = File(...)):
    try:
        logger.info("[UPLOAD] Upload endpoint hit")

        # Validate file format
        if not file.filename.endswith(".xlsx"):
            return {
                "status": "error",
                "message": "Invalid file format. Please upload an Excel .xlsx file."
            }

        # Save the uploaded Excel file to the expected location
        save_path = os.path.join("data_processing", "MockData.xlsx")
        logger.info("[UPLOAD] Saving uploaded file to %s", save_path)
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Call model retraining logic
        logger.info("[UPLOAD] File saved. Starting model retraining...")
        retrain_result = retrain_rent_model()
        logger.info("[UPLOAD] Retraining complete.")

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

# Serve favicon to avoid 404
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")

# Show links to docs when running manually
if __name__ == "__main__":
    import uvicorn
    print("MJ Home API Docs available at:")
    print("http://127.0.0.1:8000/docs")
    print("http://localhost:8000/docs")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
