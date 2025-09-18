import pandas as pd

def clean_data():
    # Step 1: Read the raw data
    df = pd.read_csv("data/raw_openrent.csv")

    # Step 2: Drop rows with any missing values
    df = df.dropna()

    # Step 3: Remove outliers where price is too high
    df = df[df["price"] < 5000]

    # Step 4: Extract number of bedrooms using regex
    df["bedrooms"] = df["description"].str.extract(r"(\d+) bed")
    df["bedrooms"] = df["bedrooms"].fillna(1).astype(int)

    # Step 5: Create a new column for property type
    df["property_type"] = df["description"].apply(
        lambda x: "Flat" if "flat" in x.lower()
        else "House" if "house" in x.lower()
        else "Other"
    )

    # Step 6: Save the cleaned data to a new CSV file
    df.to_csv("data/cleaned_openrent.csv", index=False)
    print("✅ Cleaned data saved to data/cleaned_openrent.csv")

# Run the function when this script is executed
if __name__ == "__main__":
    clean_data()
