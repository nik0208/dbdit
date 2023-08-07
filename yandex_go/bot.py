import os
import sys
import django

sys.path.append('C:\dbdit\dbdit')
os.environ['DJANGO_SETTINGS_MODULE'] = 'ditdb.settings'
django.setup()


import telebot
from telebot import types
from django.apps import *
from ditdb.yandex_go.models import *



TOKEN = '6083458782:AAHce7jw-k4EsQFmolRncB-b3u1B_EH-syg'
bot = telebot.TeleBot(TOKEN)

auth_steps = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Пожалуйста, введи свой логин:")
    auth_steps[message.chat.id] = 'login'

@bot.message_handler(func=lambda message: auth_steps.get(message.chat.id) == 'login')
def handle_login(message):
    login = message.text.strip()
    try:
        user = models.UsersYa.objects.get(login=login)
        auth_steps[message.chat.id] = 'city'
        bot.send_message(message.chat.id, "Выбери свой текущий город:")
        # Здесь можешь создать InlineKeyboard для выбора города
    except models.UsersYa.DoesNotExist:
        bot.send_message(message.chat.id, "Пользователь не найден. Попробуй еще раз:")

# Продолжи здесь, добавив обработчики для остальных этапов авторизации и работы с ботом.
# Напоминаю, что для InlineKeyboard можно использовать метод bot.send_message с параметром reply_markup.

# Запускаем бот
bot.polling()


