from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .data_scraper.scraper import scrape_listings
from .data_processing.cleaner import clean_data
from .data_processing.transformer import transform_data
from .data_processing.predictor import predict_rent
from .data_processing.loader import save_to_db


app = FastAPI(title="MJ Home API")

# Allow all origins for now
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
def run_pipeline():
    try:
        raw_data = scrape_listings()
        cleaned_data = clean_data(raw_data)
        transformed_data = transform_data(cleaned_data)
        predicted_data = predict_rent(transformed_data)
        save_to_db(predicted_data)
        return {"status": "Pipeline completed successfully"}
    except Exception as e:
        return {"status": "Error", "detail": str(e)}
