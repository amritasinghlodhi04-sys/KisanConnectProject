"""
KisanConnect - Exploratory Data Analysis & Model Training Pipeline
-------------------------------------------------------------------
This script outlines the end-to-end workflow for the Machine Learning lifecycle.
Use this in a VSCode Interactive Window (Jupyter).
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle
import os

# ==========================================
# STEP 1: Collect and Clean Data
# ==========================================
print("Loading Agmarknet Dataset...")
# df = pd.read_csv('../data/raw/agmarknet_prices_3yrs.csv')

# Dummy data generation for workflow illustration
data = {
    'crop': ['Tomato', 'Onion', 'Potato', 'Tomato'],
    'district': ['Bhopal', 'Bhopal', 'Bengaluru', 'Damoh'],
    'season': ['Rabi', 'Kharif', 'Rabi', 'Zaid'],
    'rainfall_mm': [120, 80, 150, 40],
    'price_per_kg': [18.5, 25.0, 15.0, 22.0]
}
df = pd.DataFrame(data)

# Data Cleaning
print("Cleaning data: Handling missing values and encoding categoricals...")
# df.dropna(inplace=True)
df_encoded = pd.get_dummies(df, columns=['crop', 'district', 'season'])

# ==========================================
# STEP 2: Exploratory Data Analysis (EDA) & Training
# ==========================================
print("Splitting dataset...")
X = df_encoded.drop('price_per_kg', axis=1)
y = df_encoded['price_per_kg']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training Random Forest Regressor for Price Prediction...")
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

score = rf_model.score(X_test, y_test)
print(f"Model R^2 Score: {score:.4f}")

# ==========================================
# STEP 3: Saving Models Using Pickle
# ==========================================
save_dir = '../saved_models'
os.makedirs(save_dir, exist_ok=True)

model_path = os.path.join(save_dir, 'price_rf_model.pkl')
with open(model_path, 'wb') as f:
    pickle.dump(rf_model, f)

print(f"Model successfully saved to {model_path}")
print("Ready for FastAPI deployment!")