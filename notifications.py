import telebot
from TOKEN import TOKEN
from shedule import ScheduleBot
from weather_controller import WeatherControl
from db import BotDB

botDB = BotDB('db.db')
bot = telebot.TeleBot(TOKEN)
scheduleBot = ScheduleBot()


class Notifications:
    @staticmethod
    def set_user_notification(user_id, bot, user_time):
        scheduleBot.add_task(user_time, WeatherControl.weather_screen_activate, user_id, bot)

    @staticmethod
    def set_notifications_from_DB(bot):
        for user in botDB.get_users():
            user_id = user[1]
            user_time = botDB.get_notification_time(user_id)
            Notifications.set_user_notification(user_id, bot, user_time)
            print(f'{user_id} - {user_time}')


Notifications.set_notifications_from_DB(bot)
