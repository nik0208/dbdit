import telebot
import sqlite3
from telebot import types

TOKEN = '6083458782:AAHce7jw-k4EsQFmolRncB-b3u1B_EH-syg'
bot = telebot.TeleBot(TOKEN)

def get_db_connection():
    conn = sqlite3.connect('../db.sqlite3')
    cursor = conn.cursor()
    return conn, cursor

@bot.message_handler(commands=['start'])
def send_welcome(message):
    conn, cursor = get_db_connection()
    cursor.execute("SELECT DISTINCT city FROM Locations")
    cities = [item[0] for item in cursor.fetchall()]
    conn.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for city in cities:
        markup.add(types.KeyboardButton(city))

    bot.send_message(message.chat.id, "Выберите ваш город", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def save_city(message):
    city = message.text
    conn, cursor = get_db_connection()
    cursor.execute("SELECT DISTINCT city FROM Locations")
    cities = [item[0] for item in cursor.fetchall()]

    if city in cities:
        cursor.execute(f"INSERT INTO UsersYa (chosen_city) VALUES ('{city}')")
        conn.commit()
        conn.close()
        bot.send_message(message.chat.id, "Введите логин")
    else:
        conn.close()
        bot.send_message(message.chat.id, "Некорректный город, выберите из предложенных")

def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Такси'))
    markup.add(types.KeyboardButton('Доставка'))
    markup.add(types.KeyboardButton('Выбор города'))
    bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Такси':
        send_locations(message)
    elif message.text == 'Доставка':
        # Обработка кнопки Доставка
        pass
    elif message.text == 'Выбор города':
        send_welcome(message)

def send_locations(message):
    conn, cursor = get_db_connection()
    cursor.execute("SELECT name FROM Locations")
    locations = [item[0] for item in cursor.fetchall()]
    conn.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for location in locations:
        markup.add(types.KeyboardButton(location))

    bot.send_message(message.chat.id, "Выберите стартовую точку", reply_markup=markup)

bot.polling(none_stop=True)
