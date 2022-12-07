from telebot import types
from db import BotDB
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
                'buttons': ['☀️ Показать погоду', '🌟 Оцените нас', 'Изменить город', 'Оповещения'],
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
            "set_notification": {
                'buttons': ["На главную"]
            },
            'notifications': {
                'buttons': ["Создать оповещение"]
            },
            'notification_details': {
              'buttons': ['Изменить время', 'Изменить дни недели', 'Удалить оповещение', 'Назад к оповещениям']
            },
            'notification_set_time': {
              'buttons': ['Назад']
            },
            'notification_set_date': {
              'buttons': ['Назад']
            },
            'error': {
                'buttons': ['На главную']
            }
        }
        self.change_menu('main')

    def change_menu(self, menu_name, user_id=0):
        self.previous_menu = self.current_menu
        self.current_menu = menu_name
        self.markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [types.KeyboardButton(i) for i in self.menu_markup[menu_name]['buttons']]
        for button in buttons:
            self.markup.add(button)
        if menu_name == "notifications":
            self.set_notifications_screen_markup(user_id)

    def goto_previous_menu(self):
        if self.previous_menu != '':
            self.change_menu(self.previous_menu)

    pass

    def set_notifications_screen_markup(self, user_id):
        schedule = botDB.get_schedule(user_id)
        for date in schedule:
            self.markup.add(f'{date} - {schedule[date]}')
        self.markup.add('На главную')


menu_handler = MenuHandler()
