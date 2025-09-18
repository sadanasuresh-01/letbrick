from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

# Load the trained model
model = joblib.load("models/price_model.pkl")

# Define the input structure
class RentInput(BaseModel):
    bedrooms: int
    bathrooms: int
    latitude: float
    longitude: float

@app.post("/predict")
def predict_price(data: RentInput):
    features = np.array([[data.bedrooms, data.bathrooms, data.latitude, data.longitude]])
    prediction = model.predict(features)[0]
    return {"predicted_rent": round(prediction, 2)}
    