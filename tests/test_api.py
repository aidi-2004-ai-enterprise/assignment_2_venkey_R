# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint returns API information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_predict_valid_input():
    """Test prediction with valid penguin data."""
    sample_data = {
        "bill_length_mm": 39.1,
        "bill_depth_mm": 18.7,
        "flipper_length_mm": 181,
        "body_mass_g": 3750
    }
    response = client.post("/predict", json=sample_data)
    assert response.status_code == 200
    data = response.json()
    assert "species" in data
    assert "confidence" in data

def test_predict_missing_field():
    """Test prediction with missing field."""
    invalid_data = {
        "bill_length_mm": 39.1,
        "bill_depth_mm": 18.7,
        "flipper_length_mm": 181
        # Missing body_mass_g
    }
    response = client.post("/predict", json=invalid_data)
    assert response.status_code == 422  # Validation error

def test_predict_invalid_data_type():
    """Test prediction with invalid data type."""
    invalid_data = {
        "bill_length_mm": "not_a_number",
        "bill_depth_mm": 18.7,
        "flipper_length_mm": 181,
        "body_mass_g": 3750
    }
    response = client.post("/predict", json=invalid_data)
    assert response.status_code == 422  # Validation error