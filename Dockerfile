# Используем официальный образ Python
FROM python:3.10

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY app/requirements.txt /app/requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем исходный код
COPY app /app

# Открываем порт (по умолчанию FastAPI использует 8000)
EXPOSE 8000

# Команда для запуска приложения
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
