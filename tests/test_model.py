# tests/test_model.py
import joblib
import numpy as np
from app.model import make_prediction

def test_make_prediction():
    model = joblib.load("model/model.pkl")
    mock_data = np.array([[1, 0.5, 0.3, 2, 0, 0.7, 0.4, 1]])
    prediction, probability = make_prediction(mock_data)
    
    assert prediction in [0, 1]
    assert 0 <= probability <= 1
