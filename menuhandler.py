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
                'on_change': "Вы находитесь в главном меню. Выберите одно из предложенных действий"
            },
            'rate_us': {
                'buttons': ['1', '2', '3', '4', '5', 'Назад'],
                'on_change': "Для оценки перейдите по ссылке: "
            },
            'weather_info': {
                'buttons': ['На главную', 'Изменить город'],
                'on_change': ['Выберите одно из предложенных действий: ']
            },
            'enter_city_name': {
                'buttons': ['Назад'],
                'on_change': 'Введите название города'
            },
            "set_notification": {
                'buttons': ["На главную"],
            },
            'notifications': {
                'buttons': ["Создать оповещение"],
                'on_change': "Ваши оповещения: "
            },
            'notification_details': {
                'buttons': ['Изменить время', 'Изменить дни недели', 'Удалить оповещение', 'Назад к оповещениям']
            },
            'notification_edit_time': {
                'buttons': ['Назад'],
                'on_change': 'Введите новое время: '
            },
            'notification_edit_date': {
                'buttons': [],
            },
            'notification_edit_date_enter': {
                'buttons': ['Назад'],
                'on_change': 'Введите новые дни недели: '
            },
            "set_notification_set_date": {
                'buttons': [],
                'on_change': 'Выберите дни недели и нажмите \'Далее\': '
            },
            'set_notification_set_time': {
                'buttons': ['Назад'],
                'on_change': 'Введите время оповещения (HH:MM): '
            },
            'error': {
                'buttons': ['На главную']
            }
        }

    def change_menu(self, menu_name, user_id):
        self.previous_menu = self.current_menu
        self.current_menu = menu_name
        self.markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [types.KeyboardButton(i) for i in self.menu_markup[menu_name]['buttons']]
        for button in buttons:
            self.markup.add(button)
        if menu_name == "notifications":
            self.set_notifications_screen_markup(user_id)
        elif menu_name == 'notification_edit_date_enter' or menu_name == "set_notification_set_date":
            self.set_edit_date_markup()
        if 'on_change' in self.menu_markup[self.current_menu]:
            bot.send_message(str(user_id), self.menu_markup[self.current_menu]['on_change'], reply_markup=self.markup)

    def goto_previous_menu(self, user_id):
        if self.previous_menu != '':
            self.change_menu(self.previous_menu, user_id)

    pass

    def set_notifications_screen_markup(self, user_id):
        schedule = botDB.get_schedule(user_id)
        for date in schedule:
            self.markup.add(f'{date} - {schedule[date]}')
        self.markup.add('На главную')

    def set_edit_date_markup(self):
        self.markup.add('Далее')
        for date in ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']:
            self.markup.add(f'{date}')
        self.markup.add('На главную')


menu_handler = MenuHandler()
