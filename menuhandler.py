from telebot import types
from db import*
from main import*
from shedule import ScheduleBot
from TOKEN import TOKEN
import telebot

bot = telebot.TeleBot(TOKEN)
botDB = BotDB('db.db')
scheduleBot = ScheduleBot()

class MenuHandler:
    markup = None

    def __init__(self):
        self.current_menu = 'main'
        self.previous_menu = ''
        self.menu_markup = {
            'main': {
                'buttons': ['☀️ Показать погоду', '🌟 Оцените нас', 'Изменить город', 'Создать оповещение'],
                'img': None,
                'content': None,
                'on_active': None
            },
            'rate_us': {
                'buttons': ['Назад'],
                'img': None,
                'content': None
            },
            'weather_info': {
                'buttons': ['На главную', 'Прогноз на день', 'Изменить город'],
                'img': None,
                'content': None
            },
            'enter_city_name': {
                'buttons': ['Назад']

            },
            'daily': {
                'buttons': ['Назад', 'На главную'],
                'img': None,
                'content': None
            },
            'set_notification': {
                'buttons': ['На главную']
            },
            'error': {
                'buttons': ['На главную']
            }
        }
        self.change_menu('main')

    def change_menu(self, menu_name):
        self.previous_menu = self.current_menu
        self.current_menu = menu_name
        self.markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [types.KeyboardButton(i) for i in self.menu_markup[menu_name]['buttons']]
        for button in buttons:
            self.markup.add(button)

    def goto_previous_menu(self):
        if self.previous_menu != '':
            self.change_menu(self.previous_menu)

menu_handler = MenuHandler()



def weather_screen_activate(user_id, bot):
    if botDB.is_user_exists(user_id):
        weather_screen_show_weather(botDB.get_location(user_id), user_id, bot)
    else:
        botDB.add_user(user_id)
        menu_handler.change_menu('enter_city_name')
        bot.send_message(user_id, 'Введите название города')
    pass

def weather_screen_show_weather(city_name, user_id, bot):
    image_link = get_weather_picture(city_name)
    city_name = city_name
    bot.send_photo(user_id, photo=open(fr'{image_link}', 'rb'),
                   caption=get_current_weather_info(city_name), reply_markup=menu_handler.markup)
    bot.send_message(user_id, image_link)
    menu_handler.change_menu('weather_info')


class Notifications:
    @staticmethod
    def set_user_notification(user_id, bot, user_time):
        scheduleBot.add_task(user_time, weather_screen_activate, user_id, bot)
    @staticmethod
    def set_notifications_from_DB(bot):
        for user in botDB.get_users():
            user_id = user[1]
            user_time = botDB.get_notification_time(user_id)
            Notifications.set_user_notification(user_id, bot, user_time)
            print(f'{user_id} - {user_time}')

Notifications.set_notifications_from_DB(bot)