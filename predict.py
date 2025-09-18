# src/predict.py

import joblib
import numpy as np

# Load the trained model
model = joblib.load('models/rental_model.pkl')

# Example inputs — change these as needed
bedrooms = 2
bathrooms = 1
squareft = 700

# Prepare input data exactly as during training
input_features = np.array([[bedrooms, bathrooms, squareft]])

# Predict the price
predicted_price = model.predict(input_features)

print("Predicted price:", predicted_price[0])
