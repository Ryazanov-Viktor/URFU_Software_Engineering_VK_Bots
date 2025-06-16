from fastapi.testclient import TestClient
import pandas as pd

# Важно импортировать app из main, чтобы TestClient знал о нем
from app.main import app

client = TestClient(app)


def test_predict_endpoint_success(mocker):
    # Мокируем функции, чтобы изолировать эндпоинт от остальной логики
    mocker.patch(
        "app.main.create_df_for_person",
        return_value=pd.DataFrame({"feature1": [1], "feature2": [2]}),
    )
    mocker.patch(
        "app.main.make_prediction",
        return_value=(1, 0.99),  # (prediction, probability)
    )

    # Выполняем запрос к эндпоинту
    response = client.post("/predict/", json={"uid": "vk.com/durov"})

    # Проверяем успешный статус-код
    assert response.status_code == 200

    # Проверяем содержимое ответа
    data = response.json()
    assert data["uid"] == "vk.com/durov"
    assert data["prediction"] == 1
    assert data["probability"] == 0.99
    assert "The user is a bot" in data["message"]


def test_predict_endpoint_error(mocker):
    # Мокируем функцию create_df_for_person, чтобы она вызывала ошибку
    mocker.patch(
        "app.main.create_df_for_person",
        side_effect=Exception("VK API is down"),
    )

    # Выполняем запрос
    response = client.post("/predict/", json={"uid": "vk.com/durov"})

    # Проверяем, что сервер вернул ошибку 500
    assert response.status_code == 500

    # Проверяем тело ошибки
    data = response.json()
    assert data["detail"] == "VK API is down"


def test_health_check_endpoint():
    # Выполняем запрос к эндпоинту /health/
    response = client.get("/health/")

    # Проверяем статус-код и тело ответа
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
