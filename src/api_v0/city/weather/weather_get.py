from src.city.check_exist_city import check_existing_city
from src.city.dependences import get_current_temperature
WEATHER_API_KEY = ''


def get_weather(city: str):
    city_response = check_existing_city(city)
    return get_current_temperature(city_response)
