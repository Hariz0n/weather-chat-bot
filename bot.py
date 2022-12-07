import telebot
from TOKEN import TOKEN
from weather_controller import *
from menuhandler import *
from db import BotDB
from notifications import Notifications

bot = telebot.TeleBot(TOKEN)
botDB = BotDB('db.db')
current_notification_date = ""

def change_current_notification_date(new_date):
    global current_notification_date
    current_notification_date = new_date
def format_schedule_output(user_schedule):
    return '\n'.join(f'{x}-{user_schedule[x]}' for x in user_schedule)

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
    elif message.text == 'На главную':
        menu_handler.change_menu('main')
    elif message.text == 'Изменить город':
        menu_handler.change_menu('enter_city_name')
        bot.send_message(message.from_user.id, 'Введите название города')
    elif message.text == "Оповещения":
        user_id = int(message.from_user.id)
        menu_handler.change_menu('notifications', user_id)
        bot.send_message(message.from_user.id, "Ваши оповещения: ")
    elif message.text == 'Создать оповещение':
        menu_handler.change_menu('set_notification')
        bot.send_message(message.from_user.id, 'Укажите дни недели и время:')
    else:
        if menu_handler.current_menu == 'enter_city_name':
            user_id = int(message.from_user.id)
            botDB.update_location(user_id, message.text.lower())
            WeatherControl.weather_screen_show_weather(message.text.lower(), message.chat.id, bot)
        elif menu_handler.current_menu == "notifications":
            user_id = int(message.from_user.id)
            notifications_dict = botDB.get_schedule(user_id)
            notification_date = message.text.split(' - ')[0]
            change_current_notification_date(notification_date)
            notification_time = notifications_dict[notification_date]
            menu_handler.change_menu('notification_details')
            bot.send_message(message.from_user.id, f'Оповещение: {notification_date} - {notification_time}')
        elif menu_handler.current_menu == 'set_notification':
            user_id = int(message.from_user.id)
            notification_days = message.text.split(' - ')[0]
            notification_times = message.text.split(' - ')[1]
            Notifications.set_user_notification(user_id, {notification_days: notification_times})
            user_schedule = botDB.get_schedule(user_id)
            user_schedule[notification_days] = notification_times
            botDB.update_schedule(user_id, user_schedule)
            bot.send_message(message.from_user.id, f'Оповещение создано')
        elif menu_handler.current_menu == 'notification_details':
            if message.text == 'Изменить время':
                menu_handler.change_menu('notification_set_time')
                bot.send_message(message.from_user.id, f'Введите новое время: ')
            if message.text == 'Изменить дни недели':
                menu_handler.change_menu('notification_set_date')
                bot.send_message(message.from_user.id, f'Введите новые дни недели: ')
            if message.text == 'Удалить оповещение':
                user_id = int(message.from_user.id)
                user_schedule = botDB.get_schedule(user_id)
                user_schedule.pop(current_notification_date)
                botDB.update_schedule(user_id, user_schedule)
                Notifications.set_user_notification(user_id, user_schedule)
                bot.send_message(message.from_user.id, 'Оповещение удалено!')
                menu_handler.change_menu('notifications', user_id)
            if message.text == 'Назад к оповещениям':
                bot.send_message(message.from_user.id, "Ваши оповещения: ")
                menu_handler.change_menu("notifications", int(message.from_user.id))
        elif menu_handler.current_menu == 'notification_set_time':
            user_id = int(message.from_user.id)
            user_schedule = botDB.get_schedule(user_id)
            user_schedule[current_notification_date] = message.text
            botDB.update_schedule(user_id, user_schedule)
            Notifications.set_user_notification(user_id, user_schedule)
            bot.send_message(message.from_user.id, f'Оповещение: {current_notification_date} - {user_schedule[current_notification_date]}')
            menu_handler.change_menu("notification_details")
        elif menu_handler.current_menu == 'notification_set_date':
            user_id = int(message.from_user.id)
            user_schedule = botDB.get_schedule(user_id)
            notification_time = user_schedule[current_notification_date]
            user_schedule.pop(current_notification_date)
            user_schedule[message.text] = notification_time
            botDB.update_schedule(user_id, user_schedule)
            Notifications.set_user_notification(user_id, user_schedule)
            change_current_notification_date(message.text)
            bot.send_message(message.from_user.id, f'Оповещение: {current_notification_date} - {user_schedule[current_notification_date]}')
            menu_handler.change_menu("notification_details")
        elif menu_handler.current_menu == 'error':
            bot.send_message(message.from_user.id, f'Произошла ошибка. Попробуйте еще раз')
    bot.send_message(message.from_user.id, f'{menu_handler.current_menu}', reply_markup=menu_handler.markup)


bot.infinity_polling()



