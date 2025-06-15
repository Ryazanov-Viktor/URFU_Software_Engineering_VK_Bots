# tests/conftest.py
from unittest.mock import patch
import pytest


@pytest.fixture
def mock_all():
    with patch("app.vk_api.get_user_info", return_value={"id": 1}):
        with patch("app.vk_api.get_friends_ids", return_value=([2, 3], 2)):
            with patch("app.features.get_graph_features", return_value=dict()):
                yield
