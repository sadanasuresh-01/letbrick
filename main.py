from flask import Flask, render_template, request
import joblib
import numpy as np
import pandas as pd
import os

# Initialize Flask app
app = Flask(__name__)

# Get paths
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, '..', 'models', 'rental_model.pkl')
encoder_path = os.path.join(base_dir, '..', 'models', 'encoder.pkl')

# Load model and encoder
model = joblib.load(model_path)
encoder = joblib.load(encoder_path)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        bedrooms = float(request.form['bedrooms'])
        bathrooms = float(request.form['bathrooms'])
        squareft = float(request.form['size'])
        location = request.form['location']

        # Prepare data
        numerical_features = np.array([[bedrooms, bathrooms, squareft]])
        location_encoded = encoder.transform([[location]]).toarray()
        final_features = np.hstack((numerical_features, location_encoded))

        # Make prediction
        prediction = model.predict(final_features)[0]

        return render_template('result.html', prediction=round(prediction, 2))

    except Exception as e:
        print(f"Error: {e}")
        return render_template('index.html', prediction=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
