from telebot import types


class MenuHandler:
    markup = None

    def __init__(self):
        self.current_menu = 'main'
        self.previous_menu = ''
        self.menu_buttons = {
            'main': ['☀️ Показать погоду', '🌟 Оцените нас'],
            'rate_us': ['Назад'],
            'weather_info': ['Назад']
        }
        self.change_menu('main')

    def change_menu(self, menu_name):
        self.previous_menu = self.current_menu
        self.current_menu = menu_name
        self.markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [types.KeyboardButton(i) for i in self.menu_buttons[menu_name]]
        for button in buttons:
            self.markup.add(button)

    def goto_previous_menu(self):
        if self.previous_menu != '':
            self.change_menu(self.previous_menu)


menu_handler = MenuHandler()
