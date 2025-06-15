import random
from locust import HttpUser, task, between


class APIUser(HttpUser):
    # Пауза между запросами от 1 до 5 секунд
    wait_time = between(1, 5)

    @task
    def predict_task(self):
        """
        Задача, имитирующая запрос к эндпоинту /predict/.
        """
        # Генерируем случайный числовой ID для разнообразия запросов
        random_id = random.randint(1, 100000)
        # Заголовки и тело запроса
        headers = {"Content-Type": "application/json"}
        payload = {"uid": f"id{random_id}"}

        # Отправляем POST-запрос
        self.client.post("/predict/", json=payload, headers=headers, name="/predict/")
