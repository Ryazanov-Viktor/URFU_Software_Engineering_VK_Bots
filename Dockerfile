FROM python:3.10

# Создаем обычного пользователя
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Переходим в рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем
COPY --chown=user requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Копируем весь проект
COPY --chown=user . /app

# Запускаем FastAPI-приложение на нужном порту
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]