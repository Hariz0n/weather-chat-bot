import telebot
from TOKEN import TOKEN
from menuhandler import menu_handler
from shedule import ScheduleBot
from weather_controller import WeatherControl
from db import BotDB

botDB = BotDB('db.db')
bot = telebot.TeleBot(TOKEN)
scheduleBot = ScheduleBot()


class Notifications:
    @staticmethod
    def set_user_notification(user_id, schedule):
        try:
            scheduleBot.delete_user_tasks(user_id)
            user_timezone = botDB.get_time_zone(user_id)
            scheduleBot.add_week_tasks(schedule, user_timezone, user_id, WeatherControl.weather_screen_activate, user_id, bot)
        except:
            bot.send_message(user_id, 'Неправильнй формат времени!')
            menu_handler.change_menu('main', user_id)

    @staticmethod
    def set_notifications_from_DB():
        for user in botDB.get_users():
            user_id = user[1]
            user_schedule = botDB.get_schedule(user_id)
            Notifications.set_user_notification(user_id, user_schedule)
            print(f'{user_id} - {user_schedule}')
    @staticmethod
    def reset_notifications(user_id):
        scheduleBot.delete_user_tasks(user_id)

Notifications.set_notifications_from_DB()
