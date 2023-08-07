import requests

url = "https://b2b-api.go.yandex.ru/integration/2.0/orders/routestats"
headers = {
    "Authorization": "y0_AgAAAABv5zl7AAVM1QAAAADpoCiI_kW_PhLOSeCj8_3M4hipc2AoI8s"
}

data = {
    "route": [
        [43.240506, 76.892447],
        [43.353997, 76.984596]
    ],
    "user_id": "RuslanPushV"
}

response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    print("Запрос успешно выполнен")
    print("Ответ от сервера:")
    print(response.json())
else:
    print("Ошибка при выполнении запроса")
    print("Статус код:", response.status_code)
    print("Ответ от сервера:")
    print(response.text)