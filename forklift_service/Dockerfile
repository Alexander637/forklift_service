# Используем базовый образ Python 3.13 на основе slim
FROM python:3.13-slim

# Обновляем список пакетов и устанавливаем зависимости для работы с PostgreSQL и netcat
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Открываем порт 8000 для приложения
EXPOSE 8000

# Запуск Django-приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]