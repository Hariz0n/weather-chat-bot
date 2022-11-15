import requests
from TOKEN import API_KEY
from datetime import date, datetime

def get_weather_data(city_name):
    response = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&lang=ru&units=metric')
    return response.json()


def get_current_weather_info(city_name):
    weather_data = get_weather_data(city_name)
    weather_type_description = weather_data['weather'][0]["description"]
    weather_temp = format_temp(weather_data["main"]["temp"])
    weather_temp_feelslike = format_temp(weather_data["main"]["feels_like"])
    return f'Прогноз погоды в городе {city_name.title()} сейчас :' \
           f'\n Температура: {weather_temp}, на улице {weather_type_description} ' \
           f'\n Ощущается как {weather_temp_feelslike}' \
           f'\n Скорость ветра - {weather_data["wind"]["speed"]} м/с'

def format_temp(temperature):
    return f'+{temperature}' if temperature > 0 else str(temperature)

def get_weather_picture(city_name):
    weather_data = get_weather_data(city_name)
    print(weather_data)
    weather_type_main = weather_data['weather'][0]['main']
    current_season = get_current_season()
    image_src = fr'img\{current_season}\{current_season.title()}{weather_type_main}.png'
    return image_src


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
