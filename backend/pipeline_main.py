from data_scraper.scraper import scrape_listings
from data_processing.cleaner import clean_data
from data_processing.predictor import predict_rent
from data_processing.loader import save_to_db


def main():
    print("Starting MJ Home backend pipeline...")

    raw_data = scrape_listings()
    cleaned_data = clean_data(raw_data)
    predicted_data = predict_rent(cleaned_data)
    save_to_db(predicted_data)

    print("Pipeline completed successfully!")

if __name__ == "__main__":
    main()
