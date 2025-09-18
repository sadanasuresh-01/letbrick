# sample_data.py
import pandas as pd
import numpy as np

# Create realistic sample data for Oxford
np.random.seed(42)  # For reproducible results
n_samples = 200

data = {
    'bedrooms': np.random.choice([0, 1, 2, 3, 4], size=n_samples, p=[0.1, 0.3, 0.4, 0.15, 0.05]),
    'bathrooms': np.random.choice([1, 2], size=n_samples, p=[0.7, 0.3]),
    'property_type': np.random.choice(['Flat', 'House', 'Studio'], size=n_samples, p=[0.6, 0.3, 0.1]),
    'postcode_area': np.random.choice(['OX1', 'OX2', 'OX3', 'OX4', 'OX5'], size=n_samples),
    'price': 0  # We'll calculate this based on features
}

df = pd.DataFrame(data)

# Calculate realistic prices based on features
df['price'] = 600 + (df['bedrooms'] * 250) + (df['bathrooms'] * 100)

# Adjust for property type
df.loc[df['property_type'] == 'House', 'price'] += 150
df.loc[df['property_type'] == 'Studio', 'price'] -= 100

# Adjust for postcode area (OX1 is most expensive)
postcode_adjustments = {'OX1': 200, 'OX2': 150, 'OX3': 100, 'OX4': 50, 'OX5': 0}
for postcode, adjustment in postcode_adjustments.items():
    df.loc[df['postcode_area'] == postcode, 'price'] += adjustment

# Add some random variation
df['price'] = df['price'] + np.random.normal(0, 50, n_samples)
df['price'] = df['price'].astype(int)

# Save to CSV
df.to_csv('data/oxford_rentals_cleaned.csv', index=False)
print(f"Created sample dataset with {len(df)} properties")
print(df.head())