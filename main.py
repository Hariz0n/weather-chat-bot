import requests
from TOKEN import API_KEY

def get_weather_data(city_name):
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&lang=ru&units=metric')
    return response.json()

get_weather_data('лондон')