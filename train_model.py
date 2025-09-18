# train_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

def train_rental_model(data_path="data/oxford_rentals_cleaned.csv"):  # Make sure this path is correct
    """
    Train a rental price prediction model
    Args:
        data_path (str): Path to cleaned data CSV
    Returns:
        tuple: (model, preprocessing_pipeline, evaluation_metrics)
    """
    # Load cleaned data
    df = pd.read_csv(data_path)
    print(f"Training model on {len(df)} samples")
    print("Columns available:", df.columns.tolist())
    
    # Define features and target
    X = df[['bedrooms', 'bathrooms', 'property_type', 'postcode_area']]
    y = df['price']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Preprocessing pipeline
    categorical_features = ['property_type', 'postcode_area']
    numerical_features = ['bedrooms', 'bathrooms']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
    
    # Create and train model
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(
            n_estimators=100, 
            random_state=42,
            max_depth=10
        ))
    ])
    
    # Train model
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    # Cross-validation
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='r2')
    
    print(f"Model Performance:")
    print(f"MAE: £{mae:.2f}")
    print(f"RMSE: £{rmse:.2f}")
    print(f"R² Score: {r2:.3f}")
    print(f"Cross-validation R²: {cv_scores.mean():.3f} (±{cv_scores.std() * 2:.3f})")
    
    # Save model
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/rental_model.pkl")
    print("✅ Model saved to models/rental_model.pkl")
    
    # Test a sample prediction
    sample_input = pd.DataFrame({
        'bedrooms': [2],
        'bathrooms': [1],
        'property_type': ['Flat'],
        'postcode_area': ['OX1']
    })
    sample_prediction = model.predict(sample_input)[0]
    print(f"Sample prediction - 2 bed, 1 bath Flat in OX1: £{sample_prediction:.2f}")
    
    return model, {
        'mae': mae,
        'rmse': rmse,
        'r2': r2,
        'cv_scores': cv_scores
    }

if __name__ == "__main__":
    train_rental_model()