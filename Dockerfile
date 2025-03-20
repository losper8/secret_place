# Используем Python 3.10 как базовый образ
FROM python:3.10

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы приложения в контейнер
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт 50446
EXPOSE 50446

# Запускаем приложение
CMD ["python", "main.py", "-c", "distributor/config/config.yaml"]
