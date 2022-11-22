import requests
from TOKEN import API_KEY
from datetime import date, datetime
from db import BotDB
from menuhandler import*

botDB = BotDB('db.db')

class WeatherControl:
    @staticmethod
    def get_weather_data(city_name):
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&lang=ru&units=metric')
        return response.json()

    @staticmethod
    def get_current_weather_info(city_name):
        weather_data = WeatherControl.get_weather_data(city_name)
        weather_type_description = weather_data['weather'][0]["description"]
        weather_temp = WeatherControl.format_temp(weather_data["main"]["temp"])
        weather_temp_feelslike = WeatherControl.format_temp(weather_data["main"]["feels_like"])
        return f'Прогноз погоды в городе {city_name.title()} сейчас :' \
               f'\n Температура: {weather_temp}, на улице {weather_type_description} ' \
               f'\n Ощущается как {weather_temp_feelslike}' \
               f'\n Скорость ветра - {weather_data["wind"]["speed"]} м/с'

    @staticmethod
    def format_temp(temperature):
        return f'+{temperature}' if temperature > 0 else str(temperature)

    @staticmethod
    def get_weather_picture(city_name):
        weather_data = WeatherControl.get_weather_data(city_name)
        print(weather_data)
        weather_type_main = weather_data['weather'][0]['main']
        current_season = WeatherControl.get_current_season()
        image_src = fr'img\{current_season}\{current_season.title()}{weather_type_main}.png'
        return image_src

    @staticmethod
    def get_current_season():
        Y = 2000
        seasons = [('winter', (date(Y, 1, 1), date(Y, 3, 20))),
                   ('spring', (date(Y, 3, 21), date(Y, 6, 20))),
                   ('summer', (date(Y, 6, 21), date(Y, 9, 22))),
                   ('autumn', (date(Y, 9, 23), date(Y, 12, 20))),
                   ('winter', (date(Y, 12, 21), date(Y, 12, 31)))]
        now = date.today()
        if isinstance(now, datetime):
            now = now.date()
        now = now.replace(year=Y)
        return next(season for season, (start, end) in seasons
                    if start <= now <= end)

    @staticmethod
    def weather_screen_activate(user_id, bot):
        if botDB.is_user_exists(user_id):
            WeatherControl.weather_screen_show_weather(botDB.get_location(user_id), user_id, bot)
        else:
            botDB.add_user(user_id)
            menu_handler.change_menu('enter_city_name')
            bot.send_message(user_id, 'Введите название города')
        pass

    @staticmethod
    def weather_screen_show_weather(city_name, user_id, bot):
        image_link = WeatherControl.get_weather_picture(city_name)
        city_name = city_name
        bot.send_photo(user_id, photo=open(fr'{image_link}', 'rb'),
                       caption=WeatherControl.get_current_weather_info(city_name), reply_markup=menu_handler.markup)
        bot.send_message(user_id, image_link)
        menu_handler.change_menu('weather_info')
