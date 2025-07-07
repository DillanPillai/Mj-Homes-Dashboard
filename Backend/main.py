from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Backend.pipeline_main import main as run_pipeline
from Backend.data_processing.loader import save_to_db, fetch_processed_data
from Backend.data_scraper.scraper import scrape_listings
from Backend.data_processing.cleaner import clean_data
from Backend.data_processing.predictor import predict_rent

app = FastAPI(title="MJ Home API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "MJ Home API is live"}

@app.post("/run-pipeline")
def run_pipeline_endpoint():
    try:
        run_pipeline()
        return {"status": "Pipeline completed successfully"}
    except Exception as e:
        return {"status": "Error", "detail": str(e)}

@app.get("/data")
def get_data(limit: int = 100):
    data = fetch_processed_data(limit)
    return {"status": "success", "data": data}
