from Backend.data_scraper.scraper import scrape_listings
from Backend.data_processing.cleaner import clean_data
from Backend.data_processing.predictor import predict_rent
from Backend.data_processing.loader import save_to_db

def main():
    print("Starting MJ Home backend pipeline...")

    raw_data = scrape_listings()
    cleaned_data = clean_data(raw_data)
    predicted_data = predict_rent(cleaned_data)
    save_to_db(predicted_data)

    print("Pipeline completed successfully!")

if __name__ == "__main__":
    main()
