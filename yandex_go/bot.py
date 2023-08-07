#pyTelegramBotAPI

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

# Обработчик команды /start
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

# Добавьте обработку остальных действий пользователя (выбор такси, доставки, смена города)

if __name__ == '__main__':
    bot.polling(none_stop=True)