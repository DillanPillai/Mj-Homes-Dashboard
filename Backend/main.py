# backend/main.py

from data_scraper.scraper import scrape_listings
from data_processing.cleaner import clean_data
from data_processing.transformer import transform_data
from data_processing.predictor import predict_rent  # ⬅️ New import
from data_processing.loader import save_to_db

def main():
    print("Starting MJ Home backend pipeline...")

    # Step 1: Scrape
    raw_data = scrape_listings()

    # Step 2: Clean
    cleaned_data = clean_data(raw_data)

    # Step 3: Transform
    transformed_data = transform_data(cleaned_data)

    # Step 4: Predict Rent Price
    predicted_data = predict_rent(transformed_data)  # ⬅️ ML prediction step

    # Step 5: Save
    save_to_db(predicted_data)

    print("Pipeline completed successfully!")

if __name__ == "__main__":
    main()
