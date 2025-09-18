import pandas as pd
import os

# Paths
data_dir = 'data'
raw_data_path = os.path.join(data_dir, 'raw_openrent.csv')
clean_data_path = os.path.join(data_dir, 'cleaned_openrent.csv')

# Ensure data folder exists
os.makedirs(data_dir, exist_ok=True)

# Load raw data
try:
    df = pd.read_csv(raw_data_path)
except FileNotFoundError:
    print(f"❌ {raw_data_path} not found. Please check the path.")
    exit()

print("📊 Columns in dataset:", df.columns.tolist())

# Standardize column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Check required columns
required_columns = ['bedrooms', 'bathrooms', 'squareft', 'price']
missing_cols = [col for col in required_columns if col not in df.columns]
if missing_cols:
    print(f"❌ Missing columns in dataset: {missing_cols}")
    exit()

# Drop rows with missing required values
df_cleaned = df.dropna(subset=required_columns)

# Filter out unrealistic values
df_cleaned = df_cleaned[
    (df_cleaned['price'].between(100, 10000)) &
    (df_cleaned['bedrooms'] > 0) &
    (df_cleaned['bathrooms'] > 0) &
    (df_cleaned['squareft'] > 50)
]

# Save cleaned data
df_cleaned.to_csv(clean_data_path, index=False)
print(f"✅ Cleaned data saved to {clean_data_path}")
print(f"✅ Final number of rows: {len(df_cleaned)}")
