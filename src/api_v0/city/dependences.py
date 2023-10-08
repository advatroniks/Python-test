from requests import Response
from src.config import db_settings

WEATHER_API_KEY = db_settings.WEATHER_API_KEY


def get_weather_url(city: str):
    """
    Функция принимает city(str) название города.
    Составляет URL для запроса к API openweather.
    :param city: Имя города для запроса к API.
    :returns: URL для запроса к API.
    """
    base_url = f"https://api.openweathermap.org/data/2.5/weather"
    units = "?units=metric"
    city = f"&q={city}"
    api_key = f"&appid={WEATHER_API_KEY}"

    return base_url + units + city + api_key


def get_current_temperature(response: Response):
    """
    Функция принимает объект Response. Сериализует его в JSON object.
    Возвращает значение температуры в градусах ЦЕЛЬСИЯ(str)
    :param response: Response object, ответ от API openweather по конкретному городу.
    :returns: Температура в конкретном городе на данный момент времени.(str)
    """
    data = response.json()
    print(data['main']['temp'])
    return str(data['main']['temp'])

