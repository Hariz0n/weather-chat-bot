import telebot
from TOKEN import TOKEN
from main import *
from telebot import types
from menuhandler import *
import datetime
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, 'главное меню', reply_markup=menu_handler.markup)


@bot.message_handler(content_types=['text'])
def on_message(message):

    if message.text == 'Назад':
        menu_handler.goto_previous_menu()
    elif message.text == '☀️ Показать погоду':
        menu_handler.change_menu('enter_city_name')
        bot.send_message(message.from_user.id, 'Введите название города')
    elif message.text == '🌟 Оцените нас':
        menu_handler.change_menu('rate_us')
    elif message.text == 'Прогноз на день':
        menu_handler.change_menu('daily')
    elif message.text == 'На главную':
        menu_handler.change_menu('main')
    else:
        if menu_handler.current_menu == 'enter_city_name':
            image_link = get_weather_picture(message.text.lower())
            city_name = message.text.lower()
            bot.send_photo(message.chat.id, photo=open(r'img\autumn\AutumnClouds.png', 'rb'),
                           caption=get_current_weather_info(message.text.lower()), reply_markup=menu_handler.markup)
            menu_handler.change_menu('weather_info')
    bot.send_message(message.from_user.id, f'{menu_handler.current_menu}', reply_markup=menu_handler.markup)

bot.infinity_polling()
