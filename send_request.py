# -*- coding: utf-8 -*-
import requests
import json

# URL вашего API
url = 'http://localhost:50446/api/v1/redirect'

# Данные, которые вы хотите отправить в формате JSON
data = {
    "emb_name": "name_1",
    "idx": "read",
    "method": "GET",
    "content": {"id": 0}
}

# Заголовки
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

try:
    # Отправка POST-запроса
    response = requests.post(url, headers=headers, json=data)

    # Проверка статус-кода ответа
    response.raise_for_status()  # Поднимает исключение для кода ответа 4xx/5xx

    # Если успешный ответ, выводим его
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())

except requests.exceptions.RequestException as e:
    # Обработка ошибок
    print("An error occurred:", e)
