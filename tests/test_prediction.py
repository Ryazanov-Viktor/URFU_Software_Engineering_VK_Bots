from fastapi.testclient import TestClient
import pandas as pd
from app.main import app

client = TestClient(app)

def test_user_prediction_flow(mocker):
    """
    Тест, описывающий основной пользовательский сценарий (user story):
    "Как пользователь API, я хочу отправить ID пользователя и получить предсказание,
    является ли он ботом, вместе с вероятностью."
    """
    # GIVEN: У нас есть корректный ID пользователя
    user_id = "vk.com/id1"
    
    # AND: система может успешно собрать данные и сделать предсказание
    mocker.patch(
        "app.main.create_df_for_person",
        return_value=pd.DataFrame({"feature1": [1]}),
    )
    # Предположим, модель предсказывает "не бот" с высокой вероятностью
    mocker.patch(
        "app.main.make_prediction",
        return_value=(0, 0.95),  # (prediction=0, probability=0.95)
    )

    # WHEN: Я отправляю POST-запрос на /predict/
    response = client.post("/predict/", json={"uid": user_id})

    # THEN: Я должен получить успешный ответ
    assert response.status_code == 200

    # AND: Ответ должен содержать предсказание "не бот"
    data = response.json()
    assert data["prediction"] == 0
    assert data["probability"] == 0.95
    assert "not a bot" in data["message"]
    assert data["uid"] == user_id 
