from dotenv import load_dotenv
import os

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Backend.pipeline_main import main as run_pipeline
from Backend.data_processing.loader import save_to_db, fetch_processed_data
from Backend.data_scraper.scraper import scrape_listings
from Backend.data_processing.cleaner import clean_data
from Backend.data_processing.predictor import predict_rent
from Backend.Machine_Learning_Model.retrain_model import retrain_rent_model  # to retrain model for latest updates

app = FastAPI(title="MJ Home API")

# Enable CORS so frontend can call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "MJ Home API is live"}

# Pipeline trigger endpoint
@app.post("/run-pipeline")
def run_pipeline_endpoint():
    try:
        run_pipeline()
        return {"status": "Pipeline completed successfully"}
    except Exception as e:
        return {"status": "Error", "detail": str(e)}

# Get processed data
@app.get("/data")
def get_data(limit: int = 100):
    data = fetch_processed_data(limit)
    return {"status": "success", "data": data}

# Retrain rental model on demand for most recent updates
@app.post("/retrain-model")
def retrain_model_endpoint():
    result = retrain_rent_model()
    return {"status": "done", "message": result}
