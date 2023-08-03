from django.contrib.auth.decorators import login_required
from . import models
from django.apps import apps
from openpyxl import load_workbook
from django.http import JsonResponse
from django.http import HttpResponse
from django_datatables_view.base_datatable_view import BaseDatatableView
import os
from django.conf import settings
import subprocess
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from docxtpl import DocxTemplate
import pandas as pd
import requests
import json
import telebot
from telebot import types


bot = telebot.TeleBot('6083458782:AAHce7jw-k4EsQFmolRncB-b3u1B_EH-syg')

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user, created = UsersYa.objects.get_or_create(
        user_id=str(chat_id),  # Если такого пользователя нет, то он создается
    )

    if created:
        bot.send_message(chat_id, "Привет! Выберите город")
        send_cities(chat_id)
    else:
        bot.send_message(chat_id, f"Привет! Ваш текущий город {user.city}")


def send_cities(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=2)

    # Получаем список всех городов из базы данных
    cities = Locations.objects.values_list('city', flat=True).distinct()

    # Создаем кнопки для каждого города
    for city in cities:
        city_button = types.InlineKeyboardButton(city, callback_data=city)
        markup.add(city_button)

    bot.send_message(chat_id, "Выберите город:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.message:
        # Обновляем город пользователя в базе данных
        UsersYa.objects.filter(user_id=str(call.message.chat.id)).update(city=call.data)

        bot.send_message(call.message.chat.id, f"Вы выбрали город {call.data}")


bot.polling(none_stop=True)

