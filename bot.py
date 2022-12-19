import telebot
from TOKEN import TOKEN
from weather_controller import *
from menuhandler import *
from db import BotDB
from notifications import Notifications

bot = telebot.TeleBot(TOKEN)
botDB = BotDB('db.db')
current_notification_date = ""
notification_date = []
start_flag = True

def flag_start():
    global start_flag
    start_flag = False
def add_notification_date(date):
    global notification_date
    if date not in notification_date:
        notification_date.append(date)
def reset_notification_date():
    global notification_date
    notification_date = []

def change_notification_date():
    global notification_date
    global current_notification_date
    current_notification_date = ", ".join(notification_date)
def change_current_notification_date(new_date):
    global current_notification_date
    current_notification_date = new_date

def set_notification_date(message, next_step):
    user_id = message.from_user.id
    if message.text.lower() == 'далее':
        menu_handler.change_menu(next_step, user_id)
    elif message.text.lower() == 'назад к оповещениям':
        menu_handler.change_menu('notifications', user_id)
    elif message.text.lower() in ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']:
        add_notification_date(message.text.upper())

def format_schedule_output(user_schedule):
    return '\n'.join(f'{x}-{user_schedule[x]}' for x in user_schedule)

def edit_notification_date(user_id, message):
    user_schedule = botDB.get_schedule(user_id)
    notification_time = user_schedule[current_notification_date]
    user_schedule.pop(current_notification_date)
    change_notification_date()
    notification_dates = current_notification_date
    user_schedule[notification_dates] = notification_time
    botDB.update_schedule(user_id, user_schedule)
    Notifications.set_user_notification(user_id, user_schedule)
    reset_notification_date()
    menu_handler.change_menu("notification_details", user_id)
    bot.send_message(message.from_user.id,
                     f'Оповещение: {current_notification_date} - {user_schedule[current_notification_date]}')

@bot.message_handler(commands=['start'])
def start(message):
    menu_handler.change_menu('main', message.from_user.id)


@bot.message_handler(content_types=['text'])
def on_message(message):
    if start_flag:
        menu_handler.change_menu('main', message.from_user.id)
        flag_start()
    user_id = int(message.from_user.id)
    if message.text == 'Назад':
        menu_handler.goto_previous_menu(user_id)
    elif message.text == '☀️ Показать погоду':
        WeatherControl.weather_screen_activate(message.from_user.id, bot)
    elif message.text == '🌟 Оцените нас':
        menu_handler.change_menu('rate_us', user_id)
    elif message.text == 'На главную':
        menu_handler.change_menu('main', user_id)
    elif message.text == 'Изменить город':
        menu_handler.change_menu('enter_city_name', user_id)
    elif message.text == "Оповещения":
        menu_handler.change_menu('notifications', user_id)
    elif message.text == 'Создать оповещение':
        menu_handler.change_menu("set_notification_set_date", user_id)
    else:
        if menu_handler.current_menu == 'enter_city_name':
            if WeatherControl.is_valid_city(message.text.lower()):
                botDB.update_location(user_id, message.text.lower())
                WeatherControl.weather_screen_show_weather(message.text.lower(), message.chat.id, bot)
                timezone = WeatherControl.get_timezone(message.text.lower())
                botDB.update_time_zone(user_id, timezone)
            else:
                bot.send_message(message.from_user.id, 'В названии города допущена ошибка! Попробуйте еще раз', reply_markup=menu_handler.markup)

        elif menu_handler.current_menu == "notifications":
            reset_notification_date()
            notifications_dict = botDB.get_schedule(user_id)
            notification_dates = message.text.split(' - ')[0]
            change_current_notification_date(notification_dates)
            notification_time = notifications_dict[notification_dates]
            menu_handler.change_menu('notification_details', user_id)
            bot.send_message(message.from_user.id, f'Оповещение: {notification_dates} - {notification_time}', reply_markup=menu_handler.markup)
        elif menu_handler.current_menu == "set_notification_set_date":
            set_notification_date(message, 'set_notification_set_time')
        elif menu_handler.current_menu == 'set_notification_set_time':
            change_notification_date()
            notification_days = current_notification_date
            notification_times = message.text
            bot.send_message(message.from_user.id, message.text)
            Notifications.set_user_notification(user_id, {notification_days: notification_times})
            user_schedule = botDB.get_schedule(user_id)
            user_schedule[notification_days] = notification_times
            botDB.update_schedule(user_id, user_schedule)
            bot.send_message(message.from_user.id, f'Оповещение создано')
            menu_handler.change_menu('main', user_id)
        elif menu_handler.current_menu == 'notification_details':
            if message.text == 'Изменить время':
                menu_handler.change_menu('notification_edit_time', user_id)
            if message.text == 'Изменить дни недели':
                menu_handler.change_menu('notification_edit_date_enter', user_id)
            if message.text == 'Удалить оповещение':
                user_schedule = botDB.get_schedule(user_id)
                user_schedule.pop(current_notification_date)
                botDB.update_schedule(user_id, user_schedule)
                Notifications.set_user_notification(user_id, user_schedule)
                bot.send_message(message.from_user.id, 'Оповещение удалено!', reply_markup=menu_handler.markup)
                menu_handler.change_menu('notifications', user_id)
            if message.text == 'Назад к оповещениям':
                menu_handler.change_menu("notifications", user_id)

        elif menu_handler.current_menu == 'notification_edit_time':
            user_schedule = botDB.get_schedule(user_id)
            user_schedule[current_notification_date] = message.text
            botDB.update_schedule(user_id, user_schedule)
            Notifications.set_user_notification(user_id, user_schedule)
            menu_handler.change_menu("notification_details", user_id)
            bot.send_message(message.from_user.id,
                             f'Оповещение: {current_notification_date} - {user_schedule[current_notification_date]}', reply_markup=menu_handler.markup)
        elif menu_handler.current_menu == 'notification_edit_date_enter':
            user_id = message.from_user.id
            if message.text.lower() == 'далее':
                edit_notification_date(user_id, message)
                bot.send_message(message.from_user.id, "Дата изменена!")
                menu_handler.change_menu('notifications', user_id)
            elif message.text.lower() == 'назад к оповещениям':
                menu_handler.change_menu('notifications', user_id)
            elif message.text.lower() in ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']:
                add_notification_date(message.text.upper())

        elif menu_handler.current_menu == 'error':
            bot.send_message(message.from_user.id, f'Произошла ошибка. Попробуйте еще раз')


bot.infinity_polling()
