import telebot
from TOKEN import TOKEN
from weather_controller import*
from menuhandler import*
from db import BotDB
from notifications import Notifications

bot = telebot.TeleBot(TOKEN)
botDB = BotDB('db.db')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, 'главное меню', reply_markup=menu_handler.markup)


@bot.message_handler(content_types=['text'])
def on_message(message):
    if message.text == 'Назад':
        menu_handler.goto_previous_menu()
    elif message.text == '☀️ Показать погоду':
        WeatherControl.weather_screen_activate(message.from_user.id, bot)
    elif message.text == '🌟 Оцените нас':
        menu_handler.change_menu('rate_us')
    elif message.text == 'Прогноз на день':
        menu_handler.change_menu('daily')
    elif message.text == 'На главную':
        menu_handler.change_menu('main')
    elif message.text == 'Изменить город':
        menu_handler.change_menu('enter_city_name')
        bot.send_message(message.from_user.id, 'Введите название города')
    elif message.text == 'Создать оповещение':
        menu_handler.change_menu('set_notification')
        bot.send_message(message.from_user.id, 'Введите время оповещения (В формате XX:XX)')
    else:
        if menu_handler.current_menu == 'enter_city_name':
            user_id = int(message.from_user.id)
            botDB.update_location(user_id, message.text.lower())
            WeatherControl.weather_screen_show_weather(message.text.lower(), message.chat.id, bot)
        elif menu_handler.current_menu == 'set_notification':
            time = message.text
            botDB.update_notification_time(int(message.from_user.id), time)
            Notifications.set_user_notification(int(message.from_user.id), bot, time)
            bot.send_message(message.from_user.id, 'Оповещение создано!')
            menu_handler.change_menu('main')
        elif menu_handler.current_menu == 'error':
            bot.send_message(message.from_user.id, f'Произошла ошибка. Попробуйте еще раз')
    bot.send_message(message.from_user.id, f'{menu_handler.current_menu}', reply_markup=menu_handler.markup)


bot.infinity_polling()
