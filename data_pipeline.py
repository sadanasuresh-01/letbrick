import schedule
import time
from scraper import scrape_rightmove_oxford
from clean_data import clean_property_data
from train_model import train_rental_model
import os

def run_full_pipeline():
    print("🚀 Starting data pipeline...")
    
    # Scrape new data
    print("1. Scraping new data...")
    df = scrape_rightmove_oxford(pages=2)
    
    if not df.empty:
        # Save and clean
        df.to_csv("data/oxford_rentals_raw.csv", index=False)
        clean_df = clean_property_data()
        
        # Retrain model if we have enough data
        if len(clean_df) >= 20:
            print("3. Retraining model...")
            train_rental_model()
        else:
            print("⚠️  Not enough data for retraining")
    else:
        print("❌ No data collected")
    
    print("✅ Pipeline completed")

# Schedule to run daily at 2 AM
schedule.every().day.at("02:00").do(run_full_pipeline)

if __name__ == "__main__":
    # Run immediately first time
    run_full_pipeline()
    
    # Then run on schedule
    while True:
        schedule.run_pending()
        time.sleep(60)