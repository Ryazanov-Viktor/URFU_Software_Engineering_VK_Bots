# tests/test_integration.py
from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

@pytest.fixture
def mock_all():
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("app.vk_api.get_user_info", lambda x: {
            "id": 1,
            "has_photo": 1,
            "sex": 2,
            "bdate": "1.1.1990",
            "city": {"id": 100, "title": "Moscow"},
            "country": {"id": 1, "title": "Russia"},
            "has_mobile": 1,
            "counters": {"friends": 100}
        })
        mp.setattr("app.vk_api.get_friends_ids", lambda user_id, d: ([2, 3], 2))
        yield

def test_predict_endpoint(mock_all):
    response = client.post("/predict/", json={"link": "https://vk.com/id1"}) 
    assert response.status_code == 200
