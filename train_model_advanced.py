# train_model_advanced.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
import seaborn as sns
import json
import os

def train_advanced_model():
    # Load penguins dataset
    df = sns.load_dataset("penguins")
    df = df.dropna()
    
    # Prepare features
    df_encoded = df.copy()
    df_encoded = pd.get_dummies(df_encoded, columns=['sex', 'island'])
    
    # Feature columns (matching your app)
    feature_columns = [
        'bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g', 'year',
        'sex_female', 'sex_male', 'island_Biscoe', 'island_Dream', 'island_Torgersen'
    ]
    
    # Prepare target
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df['species'])
    X = df_encoded[feature_columns]
    
    # Train model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = xgb.XGBClassifier(
        objective='multi:softprob',
        random_state=42,
        n_estimators=100
    )
    model.fit(X_train, y_train)
    
    # Test accuracy
    accuracy = model.score(X_test, y_test)
    print(f"Model accuracy: {accuracy:.4f}")
    
    # Save model and metadata
    os.makedirs("app/data", exist_ok=True)
    model.save_model("app/data/model.json")
    
    model_info = {
        "feature_columns": feature_columns,
        "species_classes": label_encoder.classes_.tolist(),
        "accuracy": accuracy
    }
    
    with open("app/data/model_info.json", "w") as f:
        json.dump(model_info, f, indent=2)
    
    print("✅ Model saved to app/data/model.json")
    print("✅ Model info saved to app/data/model_info.json")
    print(f"Species classes: {label_encoder.classes_}")

if __name__ == "__main__":
    train_advanced_model()