from telebot import types
from db import*
from main import*

botDB = BotDB('db.db')

class MenuHandler:
    markup = None

    def __init__(self):
        self.current_menu = 'main'
        self.previous_menu = ''
        self.menu_markup = {
            'main': {
                'buttons': ['☀️ Показать погоду', '🌟 Оцените нас', 'Изменить город'],
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




def weather_screen_activate(message, bot):
    user_id = int(message.from_user.id)
    if botDB.is_user_exists(user_id):
        weather_screen_show_weather(botDB.get_location(user_id), message.chat.id, bot)
    else:
        botDB.add_user(user_id)
        menu_handler.change_menu('enter_city_name')
        bot.send_message(message.from_user.id, 'Введите название города')
    pass

def weather_screen_show_weather(city_name, chat_id, bot):
    image_link = get_weather_picture(city_name)
    city_name = city_name
    bot.send_photo(chat_id, photo=open(fr'{image_link}', 'rb'),
                   caption=get_current_weather_info(city_name), reply_markup=menu_handler.markup)
    bot.send_message(chat_id, image_link)
    menu_handler.change_menu('weather_info')
