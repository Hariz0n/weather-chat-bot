import requests
from TOKEN import API_KEY
from datetime import date, datetime
from db import BotDB
from menuhandler import *

botDB = BotDB('db.db')


class WeatherControl:
    weather_codes = {

        # Group 2xx: Thunderstorm
        "200": lambda weather: fr"./img/{weather}/Thunderstorm.jpg",
        "201": lambda weather: fr"./img/{weather}/Thunderstorm.jpg",
        "202": lambda weather: fr"./img/{weather}/Thunderstorm.jpg",
        "210": lambda weather: fr"./img/{weather}/Thunderstorm.jpg",
        "211": lambda weather: fr"./img/{weather}/Thunderstorm.jpg",
        "212": lambda weather: fr"./img/{weather}/Thunderstorm.jpg",
        "221": lambda weather: fr"./img/{weather}/Thunderstorm.jpg",
        "230": lambda weather: fr"./img/{weather}/Thunderstorm.jpg",
        "231": lambda weather: fr"./img/{weather}/Thunderstorm.jpg",
        "232": lambda weather: fr"./img/{weather}/Thunderstorm.jpg",

        # Group 3xx: Drizzle
        "300": lambda weather: fr"./img/{weather}/Drizzle.jpg",
        "301": lambda weather: fr"./img/{weather}/Drizzle.jpg",
        "302": lambda weather: fr"./img/{weather}/Drizzle.jpg",
        "310": lambda weather: fr"./img/{weather}/Drizzle.jpg",
        "311": lambda weather: fr"./img/{weather}/Drizzle.jpg",
        "312": lambda weather: fr"./img/{weather}/Drizzle.jpg",
        "313": lambda weather: fr"./img/{weather}/Drizzle.jpg",
        "314": lambda weather: fr"./img/{weather}/Drizzle.jpg",
        "321": lambda weather: fr"./img/{weather}/Drizzle.jpg",

        # Group 5xx: Rain
        "500": lambda weather: fr"./img/{weather}/Rain.jpg",
        "501": lambda weather: fr"./img/{weather}/Rain.jpg",
        "502": lambda weather: fr"./img/{weather}/Rain.jpg",
        "503": lambda weather: fr"./img/{weather}/Rain.jpg",
        "504": lambda weather: fr"./img/{weather}/Rain.jpg",
        "511": lambda weather: fr"./img/{weather}/Rain.jpg",
        "520": lambda weather: fr"./img/{weather}/Rain.jpg",
        "521": lambda weather: fr"./img/{weather}/Rain.jpg",
        "522": lambda weather: fr"./img/{weather}/Rain.jpg",
        "531": lambda weather: fr"./img/{weather}/Rain.jpg",

        # Group 6xx: Snow
        "600": lambda weather: fr"./img/{weather}/Snow.jpg",
        "601": lambda weather: fr"./img/{weather}/Snow.jpg",
        "602": lambda weather: fr"./img/{weather}/Snow.jpg",
        "611": lambda weather: fr"./img/{weather}/Snow.jpg",
        "612": lambda weather: fr"./img/{weather}/Snow.jpg",
        "613": lambda weather: fr"./img/{weather}/Snow.jpg",
        "615": lambda weather: fr"./img/{weather}/Snow.jpg",
        "616": lambda weather: fr"./img/{weather}/Snow.jpg",
        "620": lambda weather: fr"./img/{weather}/Snow.jpg",
        "621": lambda weather: fr"./img/{weather}/Snow.jpg",
        "622": lambda weather: fr"./img/{weather}/Snow.jpg",

        # Group 7xx: Atmosphere ?туман по временам года или обычный, шквалистый ветер
        "701": lambda weather: fr"./img/Other/Mist.jpg",
        "711": lambda weather: fr"./img/Other/Smoke.jpg",
        "721": lambda weather: fr"./img/Other/Mist.jpg",
        "731": lambda weather: fr"./img/Other/Dust.jpg",
        "741": lambda weather: fr"./img/Other/Mist.jpg",
        "751": lambda weather: fr"./img/Other/Dust.jpg",
        "761": lambda weather: fr"./img/Other/Dust.jpg",
        "762": lambda weather: fr"./img/Other/Ash.jpg",
        "771": lambda weather: fr"./img/Other/Tornado.jpg",  # пока поставлю торнадо
        "781": lambda weather: fr"./img/Other/Tornado.jpg",

        # Group 800: Clear
        "800": lambda weather: fr"./img/{weather}/Clear.jpg",

        # Group 80x: Clouds
        "801": lambda weather: fr"./img/{weather}/Clouds25.jpg",
        "802": lambda weather: fr"./img/{weather}/Clouds25.jpg",
        "803": lambda weather: fr"./img/{weather}/Clouds85.jpg",
        "804": lambda weather: fr"./img/{weather}/Clouds85.jpg",
    }

    @staticmethod
    def get_weather_data(city_name):
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&lang=ru&units=metric')
        print(f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&lang=ru&units=metric')
        return response.json()
    @staticmethod
    def get_weather_forecast(city_name):
        response = requests.get(f'http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}&lang=ru&units=metric')
        return response.json()
    @staticmethod
    def get_timezone(city_name):
        weather_data = WeatherControl.get_weather_data(city_name)
        print(int(weather_data['timezone']))
        return int(weather_data['timezone'])
    @staticmethod
    def is_valid_city(city_name):
        response = WeatherControl.get_weather_data(city_name)
        return response['cod'] == 200

    @staticmethod
    def get_current_weather_info(city_name):
        weather_data = WeatherControl.get_weather_data(city_name)
        weather_type_description = weather_data['weather'][0]["description"]
        weather_temp = WeatherControl.format_temp(weather_data["main"]["temp"])
        weather_temp_feelslike = WeatherControl.format_temp(weather_data["main"]["feels_like"])
        weather_forecast = WeatherControl.get_weather_forecast(city_name)['list'][:2]
        print(weather_forecast)
        return f'Прогноз погоды в городе {city_name.title()} сейчас:' \
               f'\n  На улице {weather_type_description}' \
               f'\n  🌡️Температура: {weather_temp} °C' \
               f'\n  🌡️Ощущается как {weather_temp_feelslike} °C' \
               f'\n  💨Скорость ветра - {weather_data["wind"]["speed"]} м/с' \
               f'\n\nВ ближайшие 3 часа будет {weather_forecast[0]["weather"][0]["description"]}' \
               f'\nВ ближайшие 6 часа будет {weather_forecast[1]["weather"][0]["description"]}'

    @staticmethod
    def format_temp(temperature):
        return f'+{temperature}' if temperature > 0 else str(temperature)

    @staticmethod
    def get_weather_picture(city_name):
        weather_data = WeatherControl.get_weather_data(city_name)
        print(weather_data)
        weather_type_id = str(weather_data['weather'][0]['id'])
        current_season = WeatherControl.get_current_season()
        image_src = WeatherControl.weather_codes[weather_type_id](current_season)
        return image_src

    @staticmethod
    def get_current_season():
        current_month = datetime.today().month
        if current_month == 12 or 1 <= current_month <= 2:
            return 'Winter'
        elif 3 <= current_month <= 5:
            return 'Spring'
        elif 6 <= current_month <= 8:
            return 'Summer'
        elif 9 <= current_month <= 11:
            return 'Autumn'


    @staticmethod
    def weather_screen_activate(user_id, bot):
        if botDB.is_user_exists(user_id):
            WeatherControl.weather_screen_show_weather(botDB.get_location(user_id), user_id, bot)
        else:
            botDB.add_user(user_id)
            menu_handler.change_menu('enter_city_name', user_id)
        pass

    @staticmethod
    def weather_screen_show_weather(city_name, user_id, bot):
        image_link = WeatherControl.get_weather_picture(city_name)
        city_name = city_name
        bot.send_photo(user_id, photo=open(fr'{image_link}', 'rb'),
                       caption=WeatherControl.get_current_weather_info(city_name), reply_markup=menu_handler.markup)
        menu_handler.change_menu('weather_info', user_id)
