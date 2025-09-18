import pandas as pd
import os

input_path = "data/cleaned_openrent.xlsx"
output_path = "data/oxford_rentals.csv"

# Check if input file exists
if not os.path.exists(input_path):
    raise FileNotFoundError(f"{input_path} not found. Please check the path.")

# Read the Excel file
df = pd.read_excel(input_path)

# Save as CSV
df.to_csv(output_path, index=False)

print(f"✅ Converted {input_path} to {output_path}")
print("Preview of converted data:")
print(df.head())
