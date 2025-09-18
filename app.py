from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import os
from datetime import datetime

app = Flask(__name__)

# Property types and postcode areas
PROPERTY_TYPES = ["Flat", "House", "Studio"]
POSTCODE_AREAS = ["OX1", "OX2", "OX3", "OX4", "OX5"]

# Simple prediction function (no ML needed for now)
def predict_rent(bedrooms, bathrooms, squareft, property_type, postcode_area):
    """
    Simple calculation based on average Oxford rents
    """
    base_price = 800
    price = base_price + (bedrooms * 250) + (bathrooms * 100) + (squareft * 0.2)
    
    if property_type == "House":
        price += 200
    elif property_type == "Studio":
        price -= 100
        
    # Postcode adjustment (OX1 is most expensive)
    postcode_adj = {"OX1": 200, "OX2": 150, "OX3": 100, "OX4": 50, "OX5": 0}
    price += postcode_adj.get(postcode_area, 0)
    
    return price

@app.route('/')
def home():
    return render_template('index.html', 
                         property_types=PROPERTY_TYPES,
                         postcode_areas=POSTCODE_AREAS)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        bedrooms = int(request.form.get('bedrooms', 1))
        bathrooms = int(request.form.get('bathrooms', 1))
        squareft = int(request.form.get('squareft', 700))
        property_type = request.form.get('property_type', 'Flat')
        postcode_area = request.form.get('postcode_area', 'OX1')
        
        print(f"Received: {bedrooms} bed, {bathrooms} bath, {squareft} sqft, {property_type}, {postcode_area}")
        
        # Make prediction
        prediction = predict_rent(bedrooms, bathrooms, squareft, property_type, postcode_area)
        
        # Calculate range
        lower_bound = max(300, prediction - 200)
        upper_bound = prediction + 200
        
        # Market average for comparison
        market_avg = 1250
        
        # Calculate comparison
        comparison_percent = ((prediction - market_avg) / market_avg) * 100
        
        if comparison_percent > 10:
            comparison_text = f"{abs(comparison_percent):.1f}% above average"
            comparison_width = 80 + min(20, (comparison_percent - 10) / 5)
        elif comparison_percent > 0:
            comparison_text = f"{comparison_percent:.1f}% above average"
            comparison_width = 60 + (comparison_percent / 10) * 20
        elif comparison_percent > -10:
            comparison_text = f"{abs(comparison_percent):.1f}% below average"
            comparison_width = 40 + (abs(comparison_percent) / 10) * 20
        else:
            comparison_text = f"{abs(comparison_percent):.1f}% below average"
            comparison_width = 20 + min(20, (abs(comparison_percent) - 10) / 5)
        
        return jsonify({
            'prediction': round(prediction, 2),
            'range': f"£{round(lower_bound)} - £{round(upper_bound)}",
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'squareft': squareft,
            'property_type': property_type,
            'postcode_area': postcode_area,
            'comparison_text': comparison_text,
            'comparison_width': comparison_width
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Internal server error. Please try again.'}), 500

@app.route('/market-stats')
def market_stats():
    """Return market statistics for the insights panel"""
    return jsonify({
        'avg_rent': 1250,
        'total_properties': 42,
        'expensive_area': 'OX1',
        'expensive_area_price': 1450,
        'cheap_area': 'OX5',
        'cheap_area_price': 950
    })

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'message': 'Server is running'})

# Production configuration
if os.environ.get('FLASK_ENV') == 'production':
    app.config['DEBUG'] = False
    app.config['TESTING'] = False
else:
    app.config['DEBUG'] = True

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs("templates", exist_ok=True)
    os.makedirs("models", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    print("Starting server... Go to http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True)