import pytest
from unittest.mock import Mock
from app.vk_api import extract_id_from_link, get_user_info, get_friends_ids


@pytest.mark.parametrize("link, expected_id", [
    ("https://vk.com/id12345", "12345"),
    ("http://vk.com/id12345", "12345"),
    ("vk.com/id12345", "12345"),
    ("https://vk.com/durov", "durov"),
    ("vk.com/durov", "durov"),
    ("durov", "durov"),
    ("id12345", "id12345"),
])
def test_extract_id_from_link(link, expected_id):
    assert extract_id_from_link(link) == expected_id


def test_get_user_info_success(mocker):
    # Мокируем успешный ответ от API
    mock_response = Mock()
    mock_response.json.return_value = {
        "response": [{"id": 1, "first_name": "Павел"}]
    }
    mocker.patch("requests.get", return_value=mock_response)

    user_info = get_user_info("1")
    assert user_info is not None
    assert user_info["id"] == 1


def test_get_user_info_not_found(mocker):
    # Мокируем ответ, когда пользователь не найден
    mock_response = Mock()
    mock_response.json.return_value = {"error": "invalid user id"}
    mocker.patch("requests.get", return_value=mock_response)

    # Проверяем, что выбрасывается HTTPException (или возвращается None/пустой dict в зависимости от реализации)
    # В вашей реализации выбрасывается HTTPException, но для unit-теста проще проверить возврат
    with pytest.raises(Exception):
        get_user_info("несуществующий_id")


def test_get_friends_ids_success(mocker):
    # Мокируем успешный ответ
    mock_response = Mock()
    mock_response.json.return_value = {
        "response": {"count": 2, "items": [10, 20]}
    }
    mocker.patch("requests.get", return_value=mock_response)

    friends, count = get_friends_ids("1")
    assert count == 2
    assert friends == [10, 20]


def test_get_friends_ids_private_profile(mocker):
    # Мокируем ответ для закрытого профиля
    mock_response = Mock()
    mock_response.json.return_value = {
        "error": {"error_code": 30, "error_msg": "This profile is private"}
    }
    mocker.patch("requests.get", return_value=mock_response)

    friends, count = get_friends_ids("1")
    assert count == 0
    assert friends == [] 
