import telebot
from django.core.wsgi import get_wsgi_application
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ditdb.settings')
application = get_wsgi_application()

from yandex_go.models import Locations, UsersYa, Requests


TOKEN = '6083458782:AAHce7jw-k4EsQFmolRncB-b3u1B_EH-syg'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user, created = UsersYa.objects.get_or_create(
        user_id=message.from_user.id,
        defaults={'name': message.from_user.first_name}
    )
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    city_list = Locations.objects.values_list('city', flat=True).distinct()
    for city in city_list:
        markup.add(telebot.types.KeyboardButton(city))
    bot.send_message(message.chat.id, 'Выберите свой город:', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in Locations.objects.values_list('city', flat=True).distinct())
def choose_city(message):
    user = UsersYa.objects.get(user_id=message.from_user.id)
    user.chosen_city = message.text
    user.save()
    bot.send_message(message.chat.id, 'Вы успешно выбрали город. Доступные команды: /taxi, /delivery, /choose_city')


@bot.message_handler(commands=['taxi'])
def order_taxi(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    user = UsersYa.objects.get(user_id=message.from_user.id)
    location_list = Locations.objects.filter(city=user.chosen_city).values_list('name', flat=True)
    for location in location_list:
        markup.add(telebot.types.KeyboardButton(location))
    bot.send_message(message.chat.id, 'Выберите начальную точку:', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in Locations.objects.filter(city=UsersYa.objects.get(user_id=message.from_user.id).chosen_city).values_list('name', flat=True))
def choose_start_point(message):
    # Реализация выбора начальной точки и затем отправки сообщения о выборе конечной точки аналогична предыдущей функции.

@bot.message_handler(commands=['choose_city'])
def choose_city_command(message):
    # Реализация данной функции аналогична функции send_welcome.

@bot.message_handler(commands=['delivery'])
def delivery_command(message):
    # Реализация данной функции пока не проработана, согласно вашим требованиям.

bot.polling(none_stop=True)
