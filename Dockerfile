# Используем официальный образ Python
FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /order_book

# Скопируем файлы с зависимостями
COPY pyproject.toml poetry.lock /order_book/

# Poetry
RUN pip install --no-cache-dir poetry

# Зависимости приложения
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Копирование фалов
COPY . /order_book

# Открываем порт 8000
EXPOSE 8000

# Запуск
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]