from requests import Response

WEATHER_API_KEY = '47bb7070504db821c960ddf739c5f340'


def get_weather_url(city):
    base_url = f"https://api.openweathermap.org/data/2.5/weather"
    units = "?units=metric"
    city = f"&q={city}"
    api_key = f"&appid={WEATHER_API_KEY}"

    return base_url + units + city + api_key


def get_current_temperature(response: Response):
    data = response.json()
    print(data['main']['temp'])
    return str(data['main']['temp'])

