import telebot
from TOKEN import TOKEN
from main import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['город'])
def get_city_name(message):
    bot.send_message(message.from_user.id, 'Введите название города')

    @bot.message_handler(content_types=['text'])
    def call_weather(city_name):
        current_weather_data = get_weather_data(city_name.text)





bot.infinity_polling()
