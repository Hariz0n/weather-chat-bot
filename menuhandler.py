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
    pass


menu_handler = MenuHandler()
