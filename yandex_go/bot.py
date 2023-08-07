#pyTelegramBotAPI
#y0_AgAAAABv5zl7AAVM1QAAAADpoCiI_kW_PhLOSeCj8_3M4hipc2AoI8s

import datetime
import os
import sys
import django

DJANGO_PROJECT_PATH = 'C:\dbdit'
sys.path.append(DJANGO_PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ditdb.settings'

# Инициализируем Django
django.setup()

import telebot
from telebot import types
from django.db import models
from django.shortcuts import get_object_or_404
from yandex_go.models import *


# Создаем объект бота
bot = telebot.TeleBot('6083458782:AAHce7jw-k4EsQFmolRncB-b3u1B_EH-syg')

user_data = {}

####################### Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Добро пожаловать! Введите ваш логин:")
    bot.register_next_step_handler(message, check_login)

def check_login(message):
    login = message.text
    try:
        user = UsersYa.objects.get(login=login)
        user.user_id = str(message.chat.id)
        user.save()
        bot.send_message(user.user_id, f"Привет, {user.name}! Выберите ваш город из списка:")
        # Отправить список городов для выбора
        cities = Locations.objects.values_list('city', flat=True).distinct()
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        for city in cities:
            markup.add(telebot.types.KeyboardButton(city))
        bot.send_message(user.user_id, "Выберите город:", reply_markup=markup)
        bot.register_next_step_handler(message, set_city)
    except UsersYa.DoesNotExist:
        bot.send_message(message.chat.id, "Логин не найден. Попробуйте снова /start")

def set_city(message):
    user_id = message.chat.id
    chosen_city = message.text
    user = UsersYa.objects.get(user_id=user_id)
    user.chosen_city = chosen_city
    user.save()
    bot.send_message(user_id, "Введите ваш номер телефона +7... :")
    bot.register_next_step_handler(message, set_phone_number)

def set_phone_number(message):
    user_id = message.chat.id
    phone_number = message.text
    user = UsersYa.objects.get(user_id=user_id)
    user.phone_number = phone_number
    user.save()
    bot.send_message(user_id, "Спасибо за регистрацию! Ваши данные сохранены.")
    show_main_menu(user_id)

def show_main_menu(user_id):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    markup.add(telebot.types.KeyboardButton("Такси"), telebot.types.KeyboardButton("Доставка"))
    markup.add(telebot.types.KeyboardButton("Изменить город"))
    bot.send_message(user_id, "Выберите действие:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Изменить город")
def change_city(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Выберите ваш новый город из списка:")
    cities = Locations.objects.values_list('city', flat=True).distinct()
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    for city in cities:
        markup.add(telebot.types.KeyboardButton(city))
    bot.send_message(user_id, "Выберите город:", reply_markup=markup)
    bot.register_next_step_handler(message, update_city)

def update_city(message):
    user_id = message.chat.id
    chosen_city = message.text
    user = UsersYa.objects.get(user_id=user_id)
    user.chosen_city = chosen_city
    user.save()
    bot.send_message(user_id, f"Город успешно изменен на {chosen_city}!")
    show_main_menu(user_id)

# Обработка выбора "Такси"
@bot.message_handler(func=lambda message: message.text == "Такси")
def choose_pickup_location(message):
    user_id = message.chat.id
    user = UsersYa.objects.get(user_id=user_id)
    chosen_city = user.chosen_city
    bot.send_message(user_id, f"Выберите точку отправления в городе {chosen_city}:")
    locations = Locations.objects.filter(city=chosen_city)
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    for location in locations:
        markup.add(telebot.types.KeyboardButton(location.name))
    bot.send_message(user_id, "Выберите точку отправления:", reply_markup=markup)
    bot.register_next_step_handler(message, choose_destination_location)

def choose_destination_location(message):
    user_id = message.chat.id
    pickup_location = message.text
    user = UsersYa.objects.get(user_id=user_id)
    chosen_city = user.chosen_city
    bot.send_message(user_id, f"Выберите точку назначения в городе {chosen_city}:")
    locations = Locations.objects.filter(city=chosen_city)
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    for location in locations:
        markup.add(telebot.types.KeyboardButton(location.name))
    bot.send_message(user_id, "Выберите точку назначения:", reply_markup=markup)
    user.pickup_location = pickup_location
    user.save()
    bot.register_next_step_handler(message, request_taxi)

import requests

def request_taxi(message):
    user_id = message.chat.id
    user = UsersYa.objects.get(user_id=user_id)
    
    if user_id not in user_data:
        bot.send_message(user_id, "Что-то пошло не так. Пожалуйста, начните сначала.")
        return
    
    start_location = user_data[user_id]['pickup_location']
    destination_location = user_data[user_id]['destination_location']

    url = "https://b2b-api.go.yandex.ru/integration/2.0/orders/routestats"
    headers = {
        "Authorization": "Bearer <y0_AgAAAABv5zl7AAVM1QAAAADpoCiI_kW_PhLOSeCj8_3M4hipc2AoI8s>",
        "Content-Type": "application/json"
    }

    data = {
        "route": [
            [float(start_location.coordinate.split(',')[0]), float(start_location.coordinate.split(',')[1])],
            [float(destination_location.coordinate.split(',')[0]), float(destination_location.coordinate.split(',')[1])]
        ],
        "user_id": user.yandex_id
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        bot.send_message(user_id, "Запрос успешно выполнен")
        bot.send_message(user_id, f"Ответ от сервера: {response.json()}")
        
        # Создание записи в таблице Requests
        new_request = Requests(
            user=user,
            type=user_data[user_id]['request_type'],
            date=datetime.now(),
            start_point=start_location.name,
            destination_point=destination_location.name,
            receiver=None,  # Для такси, это None
            status=True,
            order=response.json().get("offer", "None")
        )
        new_request.save()
        
        # Очистка данных пользователя из user_data
        del user_data[user_id]
    else:
        bot.send_message(user_id, "Ошибка при выполнении запроса")
        bot.send_message(user_id, f"Статус код: {response.status_code}")
        bot.send_message(user_id, f"Ответ от сервера: {response.text}")


if __name__ == '__main__':
    bot.polling(none_stop=True)