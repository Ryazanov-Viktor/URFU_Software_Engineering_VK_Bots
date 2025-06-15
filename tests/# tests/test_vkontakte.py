# tests/test_vkontakte.py
import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from app.vk_api import get_user_info

@patch("app.vk_api.requests.get")
def test_get_user_info_success(mock_get):
    mock_get.return_value.json.return_value = {
        "response": [
            {
                "id": 1,
                "has_photo": 1,
                "sex": 2,
                "bdate": "1.1.1990",
                "city": {"id": 100, "title": "Moscow"},
                "country": {"id": 1, "title": "Russia"},
                "has_mobile": 1,
                "counters": {"friends": 100}
            }
        ]
    }

    result = get_user_info("1")
    assert result["id"] == 1
    assert result["city"]["title"] == "Moscow"


@patch("app.vk_api.requests.get")
def test_get_user_info_not_found(mock_get):
    mock_get.return_value.json.return_value = {"error": {}}

    with pytest.raises(HTTPException) as exc_info:
        get_user_info("invalid_id")

    assert exc_info.value.status_code == 404
