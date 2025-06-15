import pytest
from datetime import datetime
from app.features import calculate_age, transform_user_info


def test_calculate_age():
    # Тест на корректный расчет возраста
    age = calculate_age("1.1.2000")
    current_year = datetime.now().year
    assert age == current_year - 2000

    # Тест на день рождения в этом году (еще не наступивший)
    today = datetime.today()
    future_bday_month = today.month + 1 if today.month < 12 else 12
    future_bday_year = today.year - 25
    age = calculate_age(f"28.{future_bday_month}.{future_bday_year}")
    assert age == 24

    # Тест на некорректный формат даты
    assert calculate_age("1.1") is None
    assert calculate_age("не дата") is None
    assert calculate_age("") is None


def test_transform_user_info():
    # Тест на полную информацию о пользователе
    user_info = {
        "has_photo": 1,
        "sex": 2,
        "has_mobile": 1,
        "relation": 1,
        "bdate": "15.5.1995",
        "city": {"id": 1, "title": "Москва"},
        "country": {"id": 1, "title": "Россия"},
        "counters": {
            "albums": 5,
            "friends": 150,
            "followers": 200
        }
    }

    transformed = transform_user_info(user_info)
    assert transformed["has_photo"] == 1
    assert transformed["sex"] == 2
    assert transformed["age"] is not None
    assert transformed["city"] == 1
    assert transformed["country"] == 1
    assert transformed["albums"] == 5
    assert transformed["friends"] == 150
    assert "followers" in transformed  # Проверяем наличие ключа

    # Тест на неполную информацию
    user_info_partial = {
        "sex": 1,
        "counters": {
            "friends": 100
        }
    }
    transformed_partial = transform_user_info(user_info_partial)
    assert transformed_partial["sex"] == 1
    assert transformed_partial["friends"] == 100
    assert transformed_partial["has_photo"] is None
    assert transformed_partial["age"] is None
    assert transformed_partial["city"] is None
    assert transformed_partial.get("albums") is None 
