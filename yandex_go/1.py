import requests

url = "https://b2b-api.go.yandex.ru*+/integration/2.0/orders/routestats"
headers = {
    "Authorization": "Bearer y0_AgAAAABv5zl7AAVM1QAAAADpoCiI_kW_PhLOSeCj8_3M4hipc2AoI8s"
}

data = {
    "route": [
        [
          43.240506,
          76.892447
        ],
        [
          43.353997 ,
          76.984596
        ]
    ],
    "user_id": "2b9eb9910c6d487aaeb3e6ba080bb33b"
}

response = requests.post(url, json=data, headers=headers, verify=False)

if response.status_code == 200:
    print("Запрос успешно выполнен")
    print("Ответ от сервера:")
    print(response.json())
else:
    print("Ошибка при выполнении запроса")
    print("Статус код:", response.status_code)
    print("Ответ от сервера:")
    print(response.text)
    
    
# url = "https://b2b-api.go.yandex.ru/integration/2.0/orders/users"
# headers = {
#     "Authorization": "Bearer y0_AgAAAABv5zl7AAVM1QAAAADpoCiI_kW_PhLOSeCj8_3M4hipc2AoI8s"
# }

# data = {
#         "fullname": "Каршалов Абзал",
#         "phone": "+77471114932",
#         "is_active": True,
# }

# response = requests.post(url, json=data, headers=headers, verify=False)

# if response.status_code == 200:
#     print("Запрос успешно выполнен")
#     print("Ответ от сервера:")
#     print(response.json())
# else:
#     print("Ошибка при выполнении запроса")
#     print("Статус код:", response.status_code)
#     print("Ответ от сервера:")
#     print(response.text)
    
    
# url = "https://b2b-api.go.yandex.ru/integration/2.0/users"
# params = {
#     "limit": 100
# }
# headers = {
#     "Authorization": "Bearer y0_AgAAAABv5zl7AAVM1QAAAADpoCiI_kW_PhLOSeCj8_3M4hipc2AoI8s"
# }

# response = requests.get(url, params=params, headers=headers, verify=False)

# if response.status_code == 200:
#     print("Запрос успешно выполнен")
#     print("Ответ от сервера:")
#     print(response.json())
# else:
#     print("Ошибка при выполнении запроса")
#     print("Статус код:", response.status_code)
#     print("Ответ от сервера:")
#     print(response.text)