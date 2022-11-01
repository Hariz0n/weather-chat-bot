import telebot
from TOKEN import TOKEN
from main import *
from telebot import types
from menuhandler import *

bot = telebot.TeleBot(TOKEN)


def send_weather_info(message):
    bot.send_message(message.from_user.id, 'Введите название города')

    @bot.message_handler(content_types=['text'])
    def call_weather(city_name):
        bot.send_message(message.from_user.id, 'чел')
        bot.send_message(message.from_user.id, get_weather_data(city_name.text)['main']['temp'])


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, 'главное меню', reply_markup=menu_handler.markup)


@bot.message_handler(content_types=['text'])
def on_message(message):
    if message.text == 'Назад':
        menu_handler.goto_previous_menu()
    elif message.text == '☀️ Показать погоду':
        menu_handler.change_menu('weather_info')
    elif message.text == '🌟 Оцените нас':
        menu_handler.change_menu('rate_us')
    bot.send_message(message.from_user.id, f'{menu_handler.current_menu}', reply_markup=menu_handler.markup)


bot.infinity_polling()
